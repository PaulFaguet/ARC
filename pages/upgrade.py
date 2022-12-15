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

# load_dotenv()

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_json(orient='records', indent=4, force_ascii=False)

# def sendMail(path_to_results_file, recipients):
    
#     recipients = recipients.split(',')
#     # smtp_axess = os.getenv('TNR_SMTP_AXESS')
#     # user_axess = os.getenv('TNR_USER_AXESS')
#     # port = os.getenv('TNR_PORT_MAIL')
    
#     smtp_axess = st.secrets["TNR_SMTP_AXESS"]
#     user_axess = st.secrets["TNR_USER_AXESS"]
#     port = st.secrets["TNR_PORT_MAIL"]
    
    
#     msg = MIMEMultipart()
#     msg['Subject'] = f"Génération de textes avec OpenAI"
#     msg['From'] = user_axess
#     msg['To'] = ','.join(recipients)

#     msg.attach(MIMEText('Ci-joint les résultats de la génération de textes avec OpenAI.', 'plain'))
    
    
#     part_one = MIMEBase('application', "octet-stream")
#     part_one.set_payload((open(path_to_results_file, "rb")).read())
#     encoders.encode_base64(part_one)
#     part_one.add_header('Content-Disposition', f'attachment; filename="resultat.xlsx"')
#     msg.attach(part_one)
    
#     with smtplib.SMTP(smtp_axess, port) as smtp:
#         smtp.sendmail(user_axess, recipients, msg.as_string())
    
#     print('Message sent to Mail')
#     return 


st.title("XLSX")

file_input = st.file_uploader("Upload a file", type="xlsx")
# file = pd.read_excel('Adcom - Brief création textes pages catégories.xlsx')

if file_input:
    st.success("File uploaded")
    file = pd.read_excel(file_input)
    st.table(file)
    
    file.columns = file.columns.str.replace(' ', '_')

    for row in file.itertuples():
        sujet = row.Sujet
        type = row.Type_de_page 
        consigne = row.Consignes
        structure = row.Structure
        keywords = row.Mots_clés
        nombre_mots = row.Nombre_de_mots
        structure = structure.replace('</h2>', '</h2>\n').replace('</h1>', '</h1>\n').replace('[CAVE]', '[KEYWORD]\n')
        
    
        response = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt = f"Rédige un texte d'environ {nombre_mots} mots {consigne} sur la thématique de {sujet}. Respecte la structure suivante : {structure} Inclue les mots-clés suivants dans votre texte : {keywords}. Veillez à ce que votre texte soit bien structuré et facile à lire, tout en respectant les consignes fournies.",
        temperature= 0.5,
        max_tokens= 1000
        )
        
        response = response['choices'][0]['text'].split("\n")
        response = [line for line in response if line != '']
        response = '\n'.join(response)
        response = response.replace('"', '"""')
        # print(response)
        
        file.loc[row.Index, 'Résultat'] = response 
        
    # file.to_json('result.json', orient='records', indent=4, force_ascii=False)
    file_json = convert_df(file)
    st.download_button(
        label="Download data as JSON",
        data=file_json,
        file_name='result.json',
        mime='application/json',
    )



# import json
# from html import unescape

# # for all the strings in the json file, if it contains unescape characters, unescape them and replace the string then save the file
# with open('result.json') as f:
#     data = json.load(f)
#     for value in data[0].values():
#         if type(value) == 'str':
#             if '\\u' in value:
#                 value = unescape(value)
#     # data = json.dumps(data, indent=4)
#     # pd.DataFrame(data).to_json('resulta.json', orient='records', indent=4, force_ascii=True)
#     # save the file

# file_json = pd.read_json('test.json')
# file_json['Résultat'] = response['choices'][0]['text']
# # formatage réponse
# res = response['choices'][0]['text'].split("\n")
# res = [line for line in res if line != '']

# file_json.to_json('test.json', orient='records', indent=4)
# with open('test.json', 'r') as f:
#     data = json.load(f)
#     for item in data[0].values():
#         if isinstance(item, str):
#             lines = item.split("\n")
            
    
#     lines = [line for line in lines if line != '']

#     # in the json file, replace the content of the 'Résultat' key with the new text
#     data[0]['Résultat'] = lines
    
