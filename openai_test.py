import streamlit as st 
import os
import openai 

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title('OPEN AI')

language = st.radio("Choisissez une langue :", ('Français', 'Anglais', 'Italien', 'Allemand', 'Coréen'))

words_number = st.slider("Choisissez le nombre de mots à générer :", 50, 2000, (250, 750), 50)

temperature = st.slider("Température :", 0.0, 1.0, 0.5, 0.05)
st.write("""
         Une température plus élevée signifie que le modèle prendra plus de risques. 
         Essayez 0,9 pour des applications plus créatives et 0 pour celles avec une réponse bien définie. \n
         Avec une température de 0.9, il est probable que les résultats soient en anglais.
         """)

st.write("Voici la page des exemples d'utilisation de l'API de OpenAI : https://beta.openai.com/examples")
input = st.text_area("Entrez une phrase pour l'algorithme GPT-3 :")

st.button('Générer le texte')

text = f"{input}. Rédige un texte entre {words_number[0]} et {words_number[1]} mots. Traduction en {language}."
 
response = openai.Completion.create(
    engine = 'text-davinci-002',
    prompt = text,
    temperature= temperature,
    max_tokens= 1000
)

st.write(text)

st.write(response['choices'][0]['text'])
