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

st.title('Assistance à la Rédaction de Contenu - Classique')

col1, col2 = st.columns(2)

with col1:
    words_number = st.slider("Choisissez la longueur à générer :", 50, 2000, 750, 50, help="Un token correspond plus ou moins à une syllabe. 'Chat' = 1 token, 'Montagne' = 3 tokens, 'Sarkozy' = 4 tokens car mot peu commun.")

# with col2:
#     algo = st.selectbox(label="Choisissez un algorithme :", options=('text-davinci-003', 'text-curie-001'), help="DaVinci es le plus polyvalent, Curie est utile pour le ML et l'analyse prédictive https://beta.openai.com/docs/models/gpt-3")

with col2:
    temperature = st.slider("Choisissez la température (originalité) :", 0.0, 1.0, 0.5, 0.05, help="Une température plus élevée signifie que le modèle prendra plus de risques. Essayez 0.9 pour des applications plus créatives et 0 pour celles avec une réponse bien définie. Avec une température de 0.9, il est probable que les résultats soient en anglais.")


df_examples = pd.DataFrame(
    columns=['Utilisation', 'Saisie', 'Type'],
    data=[
        ['Créer une liste de mots-clés', 'Liste 10 mots-clés en rapport avec le vin et les caves à vin', 'Mots-clés'],
        ['Générer des idées/Brainstorming', 'Brainstorm des idées de contenu en rapport avec le vin et les caves à vin', 'Génération d\'idées'],
        ['Générer une FAQ', 'Crée une liste de 10 questions fréquemment posées sur les caves à vin', 'Questions/FAQ'],
        ['Utiliser un langage plus ou moins soutenu', 'Ecrit un texte comme un humain à propos des caves à vins', 'Syntaxe'],
        ['Générer une structure de texte/Générer le plan d\'un article', 'Crée un plan de dissertation en rapport avec les caves à vin et leurs détails techniques', 'Structure de texte'],
        ['Générer un texte à partir de mots/phrases clé(e)s', 'Ecrit un texte en rapport avec les caves à vin en te basant sur ces mots-clés : cave, vin, température, humidité, Ma Cave à Vin, blog, passion, etc.', 'Mots-clés'],
        ['Extraire des mots-clés', 'Extrait les mots clés de ce texte : [entrer un texte]', 'Mots-clés'],
        ['Traduire un texte', 'Traduit ce texte en [Langues] : [entrer un texte]', 'Autres'],
        ['Résumer un texte', 'Résume ce texte : [entrer un texte]', 'Autres'],
        ['Résumer un texte en liste à puces', 'Résume cela comme une liste à puces: [texte collé]', 'Autres'],
        ['Utiliser un pronom différent', 'Ecrit un texte à propos des caves à vins en utilisant le pronom "je"', 'Syntaxe'],
        ['Classer des mots-clés en différentes catégories/Regrouper les mots-clés en clusters thématiques', 'Classer les mots-clés suivants en 3 catégories : cave, vin, température, humidité, Ma Cave à Vin, blog, passion, etc.', 'Mots-clés'],
        ['Générer une étude mots-clés', 'Génère une étude mots-clés sur les caves à vin de vieillissement', 'Mots-clés'],
        ['Améliorer la précision, la qualité et la longueur des réponses', 'Rajouter "Lets think step by step" à la fin du message', 'Structure de texte'],
        ['Trouver des questions sur un sujet', 'Liste les 10 principales questions que se pose le grand public à propos des caves à vin de vieillissement', 'Questions/FAQ'],
        ['Trouver des sujets à aborder pour une thématique', 'Donne moi les principaux sujets à propos des caves à vin de vieillissement pour le grand public', 'Mots-clés'],
        ['Lister des arguments/avantages/inconvénients', 'Cite moi les avantages et inconvénients des caves à vin de vieillissement', 'Autres'],
        ['Trouver les problématiques d\'une audience cible précise concernant une thématique précise', 'Liste les 5 principaux problèmes que rencontre le grand public à propos des caves à vin de vieillissement', 'Génération d\'idées'],
        ['Trouver les expressions à inclure pour renforcer un texte', 'Donne moi les expressions en restant dans le champ lexical/champ sémantique des caves à vin de vieillissement (à inclure dans une page de description)', 'Génération d\'idées'],
        # ['Regrouper les mots-clés en clusters thématiques', 'Regroupe les mots-clés suivants en clusters (proximité sémantique) (puis donne un nom à chaque cluster)'],
        ['Regrouper les mots-clés selon l\'intention de recherche associée', 'Je veux connaître l\'intention de recherche de chaque mot-clé de la liste, à classer parmi navigationnelle, informationnelle, commerciale ou transactionelle', 'Mots-clés'],
        ['Déterminer le sentiment d\'un texte', 'Pour chaque texte de la liste, indique le sentiment qui s\'en dégage : positif, neutre ou négatif', 'Autres'],
        # ['Générer le plan d\'un article', 'Donne le plan d\'un article sur les caves à vin de vieillissement (ayant pour titre "[Titre]") qui s\'adresse au grand public. Le plan doit être présenté sous forme de liste à 2 niveaux : les titres des grandes parties et ceux des sous-parties'],
        ['Générer un brief éditorial', 'Fais un brief éditorial qui détaille ce qu\'un rédacteur doit faire pour écrire un article de qualité ayant pour titre "[TITRE]". Il s\adresse au grand public. Propose un nouveau titre, un plan (avec des H2 et H3), les mots-clés importants, des entités (marques, produits, services, dates clés), les principales sources d\information', 'Structure de texte'],
        ['Générer un texte court (méta description)', 'Pour un article dont le titre est "[TITRE]", fournis un texte attractif entre x et y caractères pour une meta description, puis une introduction de quelques phrases', 'Structure de texte'],
        ['Générer des titres', 'Donne moi des titres pour des articles sur les caves à vin de vieillissement qui ciblent le grand public', 'Structure de texte'],
        ['Générer une description de fiche produit', 'Fais une description d\'une cave à vin de vieillissement qui sera publiée sur une fiche produit d\'un site ecommerce. En incluant un sous-titre pour chaque partie, détaille les caractéristiques, explique à qui il est destiné, à quoi il sert, comment on l\'installe, comment on l\'utilise, combien de temps il peut servir, pourquoi ce produit et pas un autre, etc.', 'Structure de texte'],
        ['Générer une nouvelle version d\'un texte', 'Fais une nouvelle version de ce texte : [texte]', 'Structure de texte'],
        ['Générer un glossaire/lexique', 'Fais un glossaire des termes de la thématiques des caves à vin de vieillissement. Présente osus la forme de liste avec chaque définition en une seule phrase', 'Autres'],
        ['Reformuler un texte qui contient des phrases longues', 'Reformule ce texte avec des phrases courtes et faciles à lire', 'Syntaxe'],
        ['Reformuler un texte en changeant le ton', 'Reformule ce texte dans un style romantique, avec un mélange des registres comiques et tragiques, hyperbole et antithèse', 'Syntaxe'],
        ['Améliorer un texte en rajoutant des expressions de transition', 'Reformule le texte pour inciter le lecteur à lire jusqu\'au bout. Ajoute des transition entre les différentes parties.', 'Syntaxe'],
        # ['Reformuler un texte en modifiant les répétitions', 'Reformule ce texte en retirant les répétitions, en utilisant davantage de synonymes'],
        ['Générer un QCM', 'Génère un QCM à propos des caves à vin de vieillissement. Je veux 3 questions avec 3 réponses possibles, dont 1 seule est bonne. Cite la source d\'information', 'Autres'],
        ['Corriger les fautes d\'orthographe et de grammaire', 'Corrige les fautes d\'orthographe, de grammaire et de ponctuation dans le texte suivant, sans modifier les phrases : [texte]', 'Syntaxe'],
        ['Générer une expression régulière (REGEX)', 'Génère la regex correspondant [consigne de la regex]', 'Autres'],
        ['Développer un sujet', 'Développe le sujet suivant : [sujet]', 'Génération d\'idées'],
    ], 
    index=[[i for i in range(1, 35)]]
)


with st.sidebar:
    st.header("Exemples d'utilisation")
    st.write("Ces exemples de prompts sont issus des sites suivants : %s" % ", ".join(["https://beta.openai.com/examples", "https://www.webrankinfo.com/dossiers/conseils/chatgpt-seo", "https://learnprompting.org/docs/intro", "https://flowgpt.com/"]))
    st.table(df_examples[['Utilisation', 'Saisie']])

# st.write("Voici la page des exemples d'utilisation de l'API de OpenAI : https://beta.openai.com/examples")
inputs = ['Liste moi des mots-clés en rapport avec le [SUJET]', # KW
     'Brainstorm des idées de contenu en rapport avec le [SUJET]', # Brainstorm
     'Crée une liste de question fréquemment posées en rapport avec le [SUJET]', # Questions/FAQ
     'Ecrit un texte à propos du [SUJET] en utilisant un langage simple', # Syntaxe
     'Crée une structure de texte pour un [TYPE DE CONTENU] en rapport avec le [SUJET] OU Donne le plan d\'un article sur le [SUJET] (ayant pour titre [TITRE]) qui s\'adresse à [CIBLE]', # Structure de texte
     'Ecrit un texte en rapport avec le [SUJET] en te basant sur ces mots-clés : [MOTS-CLES]', # KW
     'Extrait les mots-clés de ce texte : [TEXTE]', # KW
     'Traduit ce texte en [LANGUE] : [TEXTE]', # Traduction
     'Résume ce texte : [TEXTE]', # Résumé
     'Résume cela comme une liste à puces: [TEXTE]', # Résumé
     'Ecrit un texte en rapport avec le [SUJET] en utilisant le pronom [PRONOM]', # Syntaxe
     'Classe les mots-clés suivants en X catégories : [MOTS-CLES] OU Regroupe les mots-clés suivants en clusters (proximité sémantique) puis donne leur chacun un nom : [MOTS-CLES]', # KW
     'Génère une étude de mots-clés en rapport avec le [SUJET]', # KW
     'Procédons point par point.', # Structure de texte
     'Liste les 10 principales questions que se pose la [CIBLE] à propos du [SUJET]', # Questions/FAQ
     'Liste moi les principaux sujets à propos du [SUJET] pour la [CIBLE]', # KW
     'Liste les avantages et inconvénients du [SUJET]', # Avantages/inconvénients
     'Liste les principaux problèmes que rencontre la [CIBLE] à propos du [SUJET]', # Brainstorm
     'Liste moi les expressions en restant dans le champ lexical/champ sémantique du [SUJET] (à inclure dans un [TYPE DE CONTENU])', # Brainstorm
     'Je veux connaître l\'intention de recherche de chaque mot-clé de la liste, à classer parmi navigationnelle, informationnelle, commerciale ou transactionelle : [MOTS-CLES]', # KW
     'Pour chaque texte de la liste, indique le sentiment qui s\'en dégage : positif, neutre ou négatif. [TEXTES]', # Sentiment
     'Génère un brief éditorial qui détaille ce qu\'un rédacteur SEO doit faire pour écrire un article de qualité ayant pour titre "[TITRE]". Il s\'adresse à [CIBLE]. Propose un nouveau titre, un plan (avec des H2 et H3), les mots-clés importants, des entités (marques, produits, services, dates clés), les principales sources d\information', # Structure de texte
     'Génère un texte de méta description pour un article ayant pour titre [TITRE]', # Structure de texte
     'Donne moi des titres pour des [TYPES DE CONTENUS] sur le [SUJET] qui ciblent la [CIBLE]', # Structure de texte
     'Fais une description du [SUJET] qui sera publiée sur une fiche produit d\'un site ecommerce. En incluant un sous-titre pour chaque partie, détaille les caractéristiques, explique à qui il est destiné, à quoi il sert, comment on l\'installe, comment on l\'utilise, combien de temps il peut servir, pourquoi ce produit et pas un autre, etc.', # Structure de texte
     'Génère une nouvelle version de ce texte : [TEXTE]', # Syntaxe
     'Génère un glossaire/lexique des termes en rapport avec le [SUJET]', # Structure de texte
     'Reformule ce texte avec des phrases plus courtes/simples et faciles à lire/en supprimant les répétitions/en utilisant davantage de synonymes : [TEXTE]', # Syntaxe
     'Reformule ce texte dans le style [STYLE], avec des [FIGURES DE STYLE] : [TEXTE]', # Syntaxe
     'Reformule ce texte pour inciter le lecteur à lire jusqu\'au bout en ajoutant des transitions entre les parties : [TEXTE]', # Syntaxe
     'Génère un QCM à propos du [SUJET] pour la [CIBLE] en suivant cette structure [STRUCTURE]', # Questions/FAQ
     'Corrige les fautes d\'orthographe, de grammaire, de syntaxe et de ponctuation dans le texte suivant : [TEXTE]', # Syntaxe
     'Génère une expression régulère qui permet de [CONSIGNE]', # Regex
     'Développe le sujet suivant : [SUJET]', # Brainstorm
    ]

# add the inputs df to the examples df as the col 'Input'
df_examples['Input'] = inputs

inp_col1, inp_col2 = st.columns(2)
with inp_col1:
        action_selector = st.multiselect("Choisissez une ou plusieurs actions", df_examples['Type'].unique(), ['Mots-clés', 'Syntaxe'])

inputs_df = pd.DataFrame({'Consigne': df_examples['Utilisation'].values.tolist(), 'Input': inputs, 'Type': df_examples['Type'].values.tolist()})

with inp_col2:
    input_selector = st.selectbox("Choisissez un input pré-rempli", inputs_df[inputs_df['Type'].isin(action_selector)])

input = st.text_area("Entrez une phrase pour l'algorithme GPT-3 :", value=inputs_df[inputs_df['Consigne'] == input_selector]['Input'].values[0] if input_selector else "")



text = f"{input}. Tu es un rédacteur dans une agence de référencement web qui rédige des textes pour soigner le SEO. Le texte se doit d'être intelligible et de respecter les consignes fournies ci-dessus. Le texte doit être d'environ {words_number} mots."
if st.button('Générer le texte'):
    response = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt = text,
        temperature= temperature,
        max_tokens= 1000
    )
    st.write('---')
    st.write(response['choices'][0]['text'])


cosignes = df_examples['Utilisation'].values.tolist()


df_test = pd.DataFrame({'Utilisation': cosignes, 'Input': inputs})