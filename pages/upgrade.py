import streamlit as st
import pandas as pd
import openai
import os 
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

load_dotenv()

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def sendMail(path_to_results_file, recipients):
    
    recipients = list(recipients)
    smtp_axess = 'smtp.axess.fr'
    user_axess = 'monitoring-adcom@axess.fr'
    port = 25
    
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


st.title("XLSX")

file_input = st.file_uploader("Upload a file", type="xlsx")
recipients = st.text_input("Destinataire", value="paul.faguet@axess.fr")

if file_input and recipients:
    st.success("File uploaded")
    file = pd.read_excel(file_input)
    st.table(file)
    
    file.columns = file.columns.str.replace(' ', '_')
    # file['Résultat'] = file['Résultat'].astype(str)

    for row in file.itertuples():
        sujet = row.Sujet
        type = row.Type_de_page 
        consigne = row.Consignes
        structure = row.Structure
        keywords = row.Mots_clés
        nombre_mots = row.Nombre_de_mots
    
        response = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt = f"""
                Rédige un texte d'environ {nombre_mots} mots {consigne} sur la thématique de {sujet}.
                Respecte la structure suivante :
                {structure}
                Inclue les mots-clés suivants dans votre texte : {keywords}. 
                Veillez à ce que votre texte soit bien structuré et facile à lire, tout en respectant les consignes fournies. 
            """,
        temperature= 0.5,
        max_tokens= 1000
        )

        # st.write(response['choices'][0]['text'])

        file.loc[row.Index, 'Résultat'] = response['choices'][0]['text']
    file.to_excel('result.xlsx', index=False)
    sendMail('result.xlsx', [recipients])
    


import numpy as np 
# create a random df wih string
df_test = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

for row in df_test.itertuples():
    df_test.loc[row.Index, 'A'] = 'test'
    df_test.loc[row.Index, 'B'] = 'test'
    df_test.loc[row.Index, 'C'] = 'test'
    df_test.loc[row.Index, 'D'] = 'test'
