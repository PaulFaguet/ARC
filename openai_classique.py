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
        ['Classer des mots-clés en différentes catégories', 'Classer les mots-clés suivants en 3 catégories : cave, vin, température, humidité, Ma Cave à Vin, blog, passion, etc.'],
        ['Générer une étude mots-clés', 'Génère une étude mots-clés sur les caves à vin de vieillissement'],
        ['Améliorer la précision, la qualité et la longueur des réponses', 'Rajouter "Lets think step by step" à la fin du message'],
        ['Trouver des questions sur un sujet', 'Liste les 10 principales questions que se pose le grand public à propos des caves à vin de vieillissement'],
        ['Trouver des sujets à aborder pour une thématique', 'Donne moi les principaux sujets à propos des caves à vin de vieillissement pour le grand public'],
        ['Lister des arguments/avantages/inconvénients', 'Cite moi les avantages et inconvénients des caves à vin de vieillissement'],
        ['Trouver les problématiques d\'une audience cible précise concernant une thématique précise', 'Liste les 5 principaux problèmes que rencontre le grand public à propos des caves à vin de vieillissement'],
        ['Trouver les expressions à inclure pour renforcer un texte', 'Donne moi les expressions en restant dans le champ lexical/champ sémantique des caves à vin de vieillissement (à inclure dans une page de description)'],
        ['Regrouper les mots-clés en clusters thématiques', 'Regroupe les mots-clés suivants en clusters (proximité sémantique) (puis donne un nom à chaque cluster)'],
        ['Regrouper les mots-clés selon l\'intention de recherche associée', 'Je veux connaître l\'intention de recherche de chaque mot-clé de la liste, à classer parmi navigationnelle, informationnelle, commerciale ou transactionelle'],
        ['Déterminer le sentiment d\'un texte', 'Pour chaque texte de la liste, indique le sentiment qui s\'en dégage : positif, neutre ou négatif'],
        ['Générer le plan d\'un article', 'Donne le plan d\'un article sur les caves à vin de vieillissement (ayant pour titre "[Titre]") qui s\'adresse au grand public. Le plan doit être présenté sous forme de liste à 2 niveaux : les titres des grandes parties et ceux des sous-parties'],
        ['Générer un brief éditorial', 'Fais un brief éditorial qui détaille ce qu\'un rédacteur doit faire pour écrire un article de qualité ayant pour titre "[TITRE]". Il s\adresse au grand public. Propose un nouveau titre, un plan (avec des H2 et H3), les mots-clés importants, des entités (marques, produits, services, dates clés), les principales sources d\information'],
        ['Générer un texte court (méta description)', 'Pour un article dont le titre est "[TITRE]", fournis un texte attractif entre x et y caractères pour une meta description, puis une introduction de quelques phrases'],
        ['Générer des titres', 'Donne moi des titres pour des articles sur les caves à vin de vieillissement qui ciblent le grand public'],
        ['Générer une description de fiche produit', 'Fais une description d\'une cave à vin de vieillissement qui sera publiée sur une fiche produit d\'un site ecommerce. En incluant un sous-titre pour chaque partie, détaille les caractéristiques, explique à qui il est destiné, à quoi il sert, comment on l\'installe, comment on l\'utilise, combien de temps il peut servir, pourquoi ce produit et pas un autre, etc.'],
        ['Générer une nouvelle version d\'un texte', 'Fais une nouvelle version de ce texte : [texte]'],
        ['Générer un glossaire/lexique', 'Fais un glossaire des termes de la thématiques des caves à vin de vieillissement. Présente osus la forme de liste avec chaque définition en une seule phrase'],
        ['Reformuler un texte qui contient des phrases longues', 'Reformle ce texte avec des phrases courtes et faciles à lire'],
        ['Reformuler un texte en changeant le ton', 'Reformule ce texte dans un style romantique, avec un mélange des registres comiques et tragiques, hyperbole et antithèse'],
        ['Améliorer un texte en rajoutant des expressions de transition', 'Reformule le texte pour inciter le lecteur à lire jusqu\'au bout. Ajoute des transition entre les différentes parties.'],
        ['Reformuler un texte en modifiant les répétitions', 'Reformule ce texte en retirant les répétitions, en utilisant davantage de synonymes'],
        ['Générer un QCM', 'Génère un QCM à propos des caves à vin de vieillissement. Je veux 3 questions avec 3 réponses possibles, dont 1 seule est bonne. Cite la source d\'information'],
        ['Corriger les fautes d\'orthographe et de grammaire', 'Corrige les fautes d\'orthographe, de grammaire et de ponctuation dans le texte suivant, sans modifier les phrases : [texte]'],
        ['Générer une expression régulière (REGEX)', 'Génère la regex correspondant [consigne de la regex]'],
    ], 
    index=[[i for i in range(1, 35)]]
)

with st.sidebar:
    st.header("Exemples d'utilisation")
    st.write("Ces exemples de prompts sont issus des sites suivants : %s" % ", ".join(["https://beta.openai.com/examples", "https://www.webrankinfo.com/dossiers/conseils/chatgpt-seo", "https://learnprompting.org/docs/intro", "https://flowgpt.com/"]))
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
    st.write('---')
    st.write(response['choices'][0]['text'])



