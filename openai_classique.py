import streamlit as st 
import os
import openai 
import pandas as pd 
# from dotenv import load_dotenv

st.set_page_config(page_title="Adcom - OpenAI", page_icon="favicon.ico", layout="wide", initial_sidebar_state="expanded")

# load_dotenv()

# DEV
# openai.api_key = os.getenv("OPENAI_API_KEY")

# PROD
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title('OPEN AI')

col1, col2 = st.columns(2)
sub_col1, sub_col2 = st.columns(2)

with col1:
    language = st.multiselect("Choisissez une ou plusieurs langue(s) :", ('Allemand', 'Anglais', 'Danois', 'Espagnol', 'Finlandais', 'Français', 'Italien', 'Norvégien', 'Néerlandais', 'Portugais', 'Russe', 'Suédois'), default=['Français'], help="Choisissez une ou plusieurs langues, la traduction est gérée directement selon les langages choisis.")

with col2:
    algo = st.selectbox(label="Choisissez un algorithme :", options=('text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001'), help="DaVinci es le plus polyvalent, Curie est utile pour le ML et l'analyse prédictive, Babbage est utile pour l'analyse de données et le traitement, Ada est utile pour l'automatisation de tâches complexes https://beta.openai.com/docs/models/gpt-3")

with sub_col1:
    words_number = st.slider("Choisissez le nombre de mots (tokens) à générer :", 50, 2000, (250, 750), 50, help="Un token correspond plus ou moins à une syllabe. 'Chat' = 1 token, 'Montagne' = 3 tokens, 'Sarkozy' = 4 tokens car mot peu commun.")

with sub_col2:
    temperature = st.slider("Choisissez la température (originalité) :", 0.0, 1.0, 0.5, 0.05, help="Une température plus élevée signifie que le modèle prendra plus de risques. Essayez 0.9 pour des applications plus créatives et 0 pour celles avec une réponse bien définie. Avec une température de 0.9, il est probable que les résultats soient en anglais.")


df_examples = pd.DataFrame(
    columns=['Utilisation', 'Saisie'],
    data=[
        ['Créateur de liste de mots-clés', 'Liste 10 mots-clés en rapport avec le vin et les caves à vin'],
        ['Générateur d\'idées/Brainstorming', 'Brainstorm des idées de contenu en rapport avec le vin et les caves à vin'],
        ['Génération d\'une FAQ', 'Crée une liste de 10 questions fréquemment posées sur les caves à vin'],
        ['Utilisation d\'un langage plus ou moins soutenu', 'Ecrit un texte comme un humain à propos des caves à vins'],
        ['Générateur de structure de texte', 'Crée un plan de dissertation en rapport avec les caves à vin et leurs détails techniques'],
        ['Générateur de texte à partie de mots/phrases clé(e)s', 'Ecrit un texte en rapport avec les caves à vin en te basant sur ces mots-clés : cave, vin, température, humidité, Ma Cave à Vin, blog, passion, etc.'],
        ['Extracteur de mots-clés', 'Extrait les mots clés de ce texte : [entrer un texte]'],
        # ['Traducteur', 'Traduit ce texte en 1. anglais, 2. espagnol, et 3. portugais : [entrer un texte]'],
        ['Résumé de texte', 'Résume ce texte : [entrer un texte]'],
        ['Utilisation d\'un pronom différent', 'Ecrit un texte à propos des caves à vins en utilisant le pronom "je"'],
    ], 
    index=['1', '2', '3', '4', '5', '6', '7', '8', '9']
)

with st.sidebar:
    st.header("Exemples d'utilisation")
    st.table(df_examples)

st.write("Voici la page des exemples d'utilisation de l'API de OpenAI : https://beta.openai.com/examples")

input = st.text_area("Entrez une phrase pour l'algorithme GPT-3 :")



text = f"{input}. Rédige un texte entre {words_number[0]} et {words_number[1]} mots. Traduction en {', '.join(language)}."
if st.button('Générer le texte'):
    response = openai.Completion.create(
        engine = algo,
        prompt = text,
        temperature= temperature,
        max_tokens= 1000
    )
    # create a separated line
    st.write('---')
    st.write(response['choices'][0]['text'])



