from classes.classe_sentiment import Sentiment

import streamlit as st 
import pandas as pd 
import traceback
from datetime import datetime



st.title('Analyse de sentiments')

file_input = st.file_uploader("Importer un fichier XLSX", type="xlsx")

options_col1, options_col2 = st.columns(2)
with options_col1:
    export = st.checkbox('Exporter les résultats en excel', value=True)
with options_col2:
    execution_time = st.checkbox('Afficher le temps d\'exécution', value=False)

if st.button('Lancer le traitement'):
    if file_input is not None:
        df = pd.read_excel(file_input)
        
        sentiment = Sentiment(df, export=export, execution_time=execution_time)

        st.write(sentiment.df[['Last Updated Date', 'ID', 'Review']])
        
        try:
            sentiment.run()
        
            st.success("Résultats")
            st.write(sentiment.df[['Last Updated Date', 'ID', 'Sentiment', 'Review']])
            
            # Export to CSV if
            if sentiment.export:
                with st.sidebar:
                    st.download_button(
                        label="Télécharger les résultats",
                        data=sentiment.df.to_csv(index=False, sep=';'),
                        file_name=f"Résultats-Sentiments-{datetime.today().strftime('%d-%m-%Y')}.csv",
                        mime="text/csv",
                    )
        
                # os.remove(f"Résultats-Sentiments-{datetime.today().strftime('%d-%m-%Y')}.csv")
        
        except:
            st.error('Une erreur est survenue')
            st.error(traceback.format_exc())
        
    else:
        st.error('Veuillez importer un fichier XLSX ou CSV')


