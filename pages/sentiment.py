from classes.classe_sentiment import Sentiment

import streamlit as st 
import pandas as pd 
import traceback
from datetime import datetime


def formate_options(options):
    options_json = {
        'execution_time': False,
        'export': False
    }
    
    if options:
        if 'Temps d\'exécution' in options:
            options_json['execution_time'] = True
            
        if 'Export' in options:
            options_json['export'] = True  

    return options_json








file_input = st.file_uploader("Importer un fichier XLSX", type="xlsx")

options = st.multiselect('Choisissez les options à ajouter', 
    ['Temps d\'exécution', 'Export'], 
    help='"Temps d\'exécution" permet d\'afficher le temps d\'exécution du traitement. "Export en excel" permet d\'exporter les résultats en excel.', 
    default=['Export']
)

if st.button('Lancer le traitement'):
    if file_input is not None:
        df = pd.read_excel(file_input)
        
        formatted_options = formate_options(options)
        
        sentiment = Sentiment(df, export=formatted_options['export'], execution_time=formatted_options['execution_time'])

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


