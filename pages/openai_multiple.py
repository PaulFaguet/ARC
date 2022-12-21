import streamlit as st
import pandas as pd
import openai
import os 
# from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from io import BytesIO
from xlsxwriter import Workbook
# from bert_score import score 
import nltk
import textstat as ts
from math import ceil 

# load_dotenv()

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_json(orient='records', indent=4, force_ascii=False)

def sendMail(path_to_results_file, recipients):
    
    recipients = recipients.split(',')
    smtp_axess = os.getenv('TNR_SMTP_AXESS')
    user_axess = os.getenv('TNR_USER_AXESS')
    port = os.getenv('TNR_PORT_MAIL')
    
    # smtp_axess = st.secrets["TNR_SMTP_AXESS"]
    # user_axess = st.secrets["TNR_USER_AXESS"]
    # port = st.secrets["TNR_PORT_MAIL"]
    
    
    msg = MIMEMultipart()
    msg['Subject'] = f"Génération de textes avec OpenAI"
    msg['From'] = user_axess
    msg['To'] = ','.join(recipients)

    msg.attach(MIMEText('Ci-joint les résultats de la génération de textes avec OpenAI.', 'plain'))
    
    
    part_one = MIMEBase('application', "octet-stream")
    part_one.set_payload((open(path_to_results_file, "rb")).read())
    encoders.encode_base64(part_one)
    part_one.add_header('Content-Disposition', f'attachment; filename="resultat.xlsx"')
    msg.attach(part_one)
    
    with smtplib.SMTP(smtp_axess, port) as smtp:
        smtp.sendmail(user_axess, recipients, msg.as_string())
    
    print('Message sent to Mail')
    return 

st.set_page_config(layout="wide")

st.title("OPEN AI")


# output = BytesIO()
# wb = Workbook(output, {'in_memory': True})
# ws = wb.add_worksheet()

# with wb:
#     ws.write('A1', 'Article ID')
#     ws.write('B1', 'Client')
#     ws.write('C1', 'Type de page')
#     ws.write('D1', 'Sujet')
#     ws.write('E1', 'Consignes')
#     ws.write('F1', 'Nombre de mots')
#     ws.write('G1', 'Structure')
#     ws.write('H1', 'Mots clés primaires')
#     ws.write('I1', 'Mots clés secondaires')
#     ws.write('J1', 'Meta titre')
#     ws.write('K1', 'Meta description')
#     ws.write('L1', 'Texte')
#     ws.write('M1', 'Résultat')

with st.sidebar:     
    st.info("Le bouton de téléchargement s'affichera ici dès que les résultats seront prêts")
    # st.download_button(
    #         label="Télécharger exemple.xlsx",
    #         data=output.getvalue(),
    #         file_name='exemple.xlsx',
    #         mime='application/vnd.ms-excel',
    # )




file_input = st.file_uploader("Importer un fichier XLSX", type="xlsx")

if st.button("Générer") and file_input:
    file = pd.read_excel(file_input)
    st.write(file[["Article ID", "Client", "Type de page", "Sujet", "Consignes", "Nombre de mots", "Structure", "Mots clés primaires", "Mots clés secondaires"]])
    file.columns = file.columns.str.replace(' ', '_')

    with open("result.txt", "w", encoding='utf-8') as f:
        f.write('')
        
    for row in file.itertuples():
        sujet = row.Sujet
        type = row.Type_de_page 
        consigne = row.Consignes
        client = row.Client
        structure = row.Structure
        keywords = row.Mots_clés_primaires
        keyword_seconds = row.Mots_clés_secondaires
        nombre_mots = row.Nombre_de_mots
        structure = structure.replace('</h2>', '</h2>\n').replace('</h1>', '</h1>\n')
        
        prompt = f"Rédige un texte d'environ {nombre_mots} mots {consigne} sur la thématique de {sujet}. Respecte la structure suivante : {structure}. Intègre les mots-clés suivants dans votre texte : {keywords}. Veillez à ce que votre texte soit bien structuré et facile à lire, tout en respectant les consignes fournies et en intégrant chaque mot-clé au moins une fois."
        
        response = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt = prompt,
        temperature= 0.5,
        max_tokens= 1000
        )
                
        response = response['choices'][0]['text'].split("\n")
        response = [line for line in response if line != '']
        response = '\n'.join(response)
        response = response.replace('"', '"""')
        
        ts.set_lang("fr")
        flesch = ts.flesch_reading_ease(response)
        dc = ts.dale_chall_readability_score(response)
        fk = ts.flesch_kincaid_grade(response)
        ari = ts.automated_readability_index(response)
        grade_moyen = round((dc + fk + ari) / 3, 2)
        rt = ts.reading_time(response)
        rt = ceil(rt / 60) if rt > 60 else ceil(rt)
        
        file.loc[row.Index, 'Résultat'] = response 
        with open("result.txt", "a", encoding='utf-8') as f:
            f.write(f"""
Requête n°{row.Index+1}
Client : {client}
Sujet : {sujet}
--- 
Flesch : {flesch}
Grade moyen : {grade_moyen} (Dale Chall {dc}, Flesch Kincaid {fk}, Automated Readability Index {ari})
Reading time : environ {rt} {"secondes" if rt < 60 else "minutes"}
Nombre de mots : {len(response.split())}, Nombre de tokens : {len(nltk.tokenize.word_tokenize(response))}
---
{response}
---
            """)
    
#   Nombre de tokens : {len(word_tokenize(response))}, Nombre de mots : {len(response.split())}

    with st.sidebar: 
        st.success("Résultats disponibles")
        with open("result.txt", "r", encoding='utf-8') as f:
            resp = f.read()
            st.download_button(
                label="Télécharger les résultats (.txt)",
                data=resp,
                file_name='result.txt',
                mime='text/plain',
            )