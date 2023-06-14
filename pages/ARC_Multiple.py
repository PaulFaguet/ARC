from classes.arc_multiple import ARC_Multiple
from classes.template_xlsx_file import Template_XLSX

import streamlit as st


st.set_page_config(layout="wide")

st.title('Assistance à la Rédaction de Contenu - Multiple')
st.header('MINTENANCE DU MODULE')

# with st.sidebar:     
#     st.info("Le bouton de téléchargement s'affichera ici dès que les résultats seront prêts")

# _, template_download_col2, _ = st.columns([1, 1, 1])
# with template_download_col2:
#     st.download_button(
#             label="Template_OpenAI.xlsx",
#             data=Template_XLSX()._create_template_xlsx_file().getvalue(),
#             file_name='Template_OpenAI.xlsx',
#             mime='application/vnd.ms-excel',
#     )
    
# st.info("Téléchargez le fichier Template_OpenAI.xlsx ci-dessus, remplissez-le et importez-le dans l'application ci-dessous. Pensez à remplir les champs indiqués comme obligatoires.")
# st.info("Pour une meilleure lecture et compréhension du fichier d'exemple, pensez à aligner le texte au centre, à centrer le contenu et à activer le renvoi à la ligne automatique.")

# file_input = st.file_uploader("Importer un fichier XLSX", type="xlsx")

# st.write(st.session_state)
# if st.button("Générer") and file_input:
#     arc_multiple = ARC_Multiple(file_input)

#     st.write(arc_multiple.df[["Article_ID", "Client", "Type_de_page", "Sujet", "Consignes", "Nombre_de_mots", "Structure", "Mots_clés_primaires", "Mots_clés_secondaires"]])

#     # with open("result.txt", "w", encoding='utf-8') as f:
#     #     f.write('')    
   
#     info_col1, info_col2 = st.columns([4, 1])
#     for index in range(len(arc_multiple.df)):
        
#         row = arc_multiple._parse_df_by_row(index)
        
#         with info_col1:
#             st.info(f"Rédaction en cours pour {row['client']} : \"{row['sujet']}\" ({row['type']})")
#         with info_col2:
#             st.success(f"{row['article_id']/len(arc_multiple.df)*100:.2f}%")
        
#         arc_multiple.run(index)
        
#         # affiche le bouton pendant la boucle
#         # if "results" in st.session_state:
#         #     with st.sidebar: 
#         #         st.success("Résultats disponibles")
#         #         # download button to download the results stocked in the session state
#         #         st.download_button(
#         #             label=f"Télécharger les résultats ({len(st.session_state.results)})",
#         #             data="\n".join(st.session_state.results),
#         #             file_name='result.txt',
#         #             mime='text/plain',
#         #             key="during_loop"
#         #         )
#     with open(f"{row['client']}-{row['sujet']}-{index+1}.txt", "r", encoding='utf-8') as f:
#         resp = f.read()
#         file_name = f"{row['client']}-{row['sujet']}-{index+1}.txt"
#         st.download_button(
#             label=f"Télécharger les résultats",
#             data=open('result.txt', "r", encoding='utf-8').read(),
#             file_name='result.txt',
#             mime='text/plain',
#             on_click=arc_multiple._delete_result_file('result.txt'),
#             # mime="application/msword"
#         )
                    
#     # affiche le bouton après la boucle
#     # if "results" in st.session_state:
#     #     with st.sidebar: 
#     #         st.success("Résultats disponibles")
#     #         # download button to download the results stocked in the session state
#     #         st.download_button(
#     #             label=f"Télécharger tous les résultats",
#     #             data="\n".join(st.session_state.results),
#     #             file_name='result.txt',
#     #             mime='text/plain',
#     #             key="after_loop"
#     #         )
            