import streamlit as st 
import os
import openai 

# DEV
# openai.api_key = os.getenv("OPENAI_API_KEY")

# PROD
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title('OPEN AI')

col1, col2 = st.columns(2)
sub_col1, sub_col2 = st.columns(2)

with col1:
    language = st.radio("Choisissez une langue :", ('Français', 'Anglais', 'Italien', 'Allemand', 'Espagnol', 'Portugais'))
with col2:
    algo = st.radio("Choisissez un algorithme :", ('text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001'), help="DaVinci es le plus polyvalent, Curie est utile pour le ML et l'analyse prédictive, Babbage est utile pour l'analyse de données et le traitement, Ada est utile pour l'automatisation de tâches complexes.")

with sub_col1:
    words_number = st.slider("Choisissez le nombre de mots à générer :", 50, 2000, (250, 750), 50)

with sub_col2:
    temperature = st.slider("Température :", 0.0, 1.0, 0.5, 0.05)
st.write("""
         Une température plus élevée signifie que le modèle prendra plus de risques. 
         Essayez 0,9 pour des applications plus créatives et 0 pour celles avec une réponse bien définie. \n
         Avec une température de 0.9, il est probable que les résultats soient en anglais.
         """)

st.write("Voici la page des exemples d'utilisation de l'API de OpenAI : https://beta.openai.com/examples")

# keywords = st.text_input("Entrez les mots clés à utiliser pour la génération de texte, séparez les d'une virgule :")
# keywords = keywords.lower().split(", ")
# st.write(keywords)

# structure = st.radio("Choisissez une structure :", options=('Personnalisée', 'Classique (H1 - H2 - H2)', 'Flaubert (H1 - H2 H3 - H2 H3'))


input = st.text_area("Entrez une phrase pour l'algorithme GPT-3 :")

st.button('Générer le texte')

# if structure == 'Classique (H1 - H2 - H2)':
#     input = f"""
#     Respecte la structure suivante :
#     <h1>[CAVE]</h1>
#     <h2>Qu'est ce qu'une [CAVE] ?</h2>
#     <h2>Comment choisir sa cave [CAVE] ?</h2>
#     <h2>Quelles marques de [CAVE] proposées sur Ma Cave a Vin ?</h2>
#     <h2>Nos conseils pour l'achat de votre [CAVE]</h2>
#     <h2>Comparer les [CAVE]</h2>
#     <h2>Quelle température pour une [CAVE] ?</h2>
#     <h2>Où installer sa [CAVE] ?</h2>
#     """
#     st.write(input)
text = f"{input}. Rédige un texte entre {words_number[0]} et {words_number[1]} mots. Traduction en {language}."

response = openai.Completion.create(
    engine = algo,
    prompt = text,
    temperature= temperature,
    max_tokens= 1000
)

# st.write(text)

st.write(response['choices'][0]['text'])
