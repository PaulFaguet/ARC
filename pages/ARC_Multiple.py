from classes.arc_multiple import ARC_Multiple
from classes.template_xlsx_file import Template_XLSX

import streamlit as st


st.set_page_config(layout="wide")

st.title('Assistance à la Rédaction de Contenu - Multiple')

with st.sidebar:     
    st.info("Le bouton de téléchargement s'affichera ici dès que les résultats seront prêts")

_, template_download_col2, _ = st.columns([1, 1, 1])
with template_download_col2:
    st.download_button(
            label="Template_OpenAI.xlsx",
            data=Template_XLSX()._create_template_xlsx_file().getvalue(),
            file_name='Template_OpenAI.xlsx',
            mime='application/vnd.ms-excel',
    )
    
st.info("Téléchargez le fichier Template_OpenAI.xlsx ci-dessus, remplissez-le et importez-le dans l'application ci-dessous. Pensez à remplir les champs indiqués comme obligatoires.")
st.info("Pour une meilleure lecture et compréhension du fichier d'exemple, pensez à aligner le texte au centre, à centrer le contenu et à activer le renvoi à la ligne automatique.")

st.warning("Il y a 2 solutions pour récupérer les résultats. La 1ère consiste à attendre que fichier ait été traité entièrement. La 2nde consiste à recevoir les résultats un à un par mail au fur et à mesure de leur génération. Cette 2nde solution est plus longue mais permet de récupérer les résultats plus rapidement. Les deux solutions sont cumulables.")

file_input = st.file_uploader("Importer un fichier XLSX", type="xlsx")
email_col1, email_col2 = st.columns([1, 2])
with email_col1:
    export_mail = st.radio("Recevoir les résultats un à un par mail", ("Oui", "Non"), help="Permet de recevoir les résultats un à un par mail au fur et à mesure de leur génération.")
    export_mail = True if export_mail == "Oui" else False
if export_mail == True:
    with email_col2:
        mail_input = st.text_input("Adresse mail")
else:
    mail_input = None

if st.button("Générer") and file_input:
    if export_mail == True and not mail_input:
        st.error("Veuillez renseigner une adresse mail")
    else:
        arc_multiple = ARC_Multiple(file_input, export_mail, mail_input)

        st.write(arc_multiple.df[["Article_ID", "Client", "Type_de_page", "Sujet", "Consignes", "Nombre_de_mots", "Structure", "Mots_clés_primaires", "Mots_clés_secondaires"]])

        with open("result.txt", "w", encoding='utf-8') as f:
            f.write('')    
    
        info_col1, info_col2 = st.columns([4, 1])
        for index in range(len(arc_multiple.df)):
            
            row = arc_multiple._parse_df_by_row(index)
            
            with info_col1:
                st.info(f"Rédaction en cours pour {row['client']} : \"{row['sujet']}\" ({row['type']})")
            with info_col2:
                st.success(f"{row['article_id']/len(arc_multiple.df)*100:.2f}%")
            
            arc_multiple.run(index)
            
        with st.sidebar: 
            st.success("Résultats disponibles")
            st.download_button(
                label=f"Télécharger tous les résultats",
                data=open('result.txt', "r", encoding='utf-8').read(),
                file_name='result.txt',
                mime='text/plain'
            )
            