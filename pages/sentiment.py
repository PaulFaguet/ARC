import streamlit as st 
import os
import openai 
import pandas as pd 
from dotenv import load_dotenv
import time
import asyncio


load_dotenv()

class Sentiment:
    def __init__(self, df: pd.DataFrame, to_excel: bool = False, execution_time: bool = False):
        self.df = df
        self.to_excel = to_excel
        self.execution_time = execution_time
        
        self.time_duration = None
    
    @staticmethod
    def _question_davinci_model(review: str) -> str:
        prompt = f"D'après l'avis suivant, détermine le sentiment exprimé : positif, neutre ou négatif.\n\nAvis : {review}\n\nSentiment :"
        
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.1,
            max_tokens=50,
        )
        
        response = response['choices'][0]['text'].replace('.', '').lower()
        
        return response

    def _process_row(self, row: pd.Series) -> str:
        return self._question_davinci_model(row['Review'])
    
    
    def _formate_df(self):
        self.df = self.df[['Last Updated Date', 'ID', 'Review']]
        
        return 
    
    def run(self):
        self._formate_df()
        
        if self.execution_time:
            start = time.time()
        
        results = [self._process_row(row) for _, row in self.df.iterrows()]
        
        if self.execution_time:
            self.time_duration = time.time() - start
            st.info(f'Execution time : {self.time_duration/60} minutes')
            
        self.df['Sentiment'] = results
        
        if self.to_excel:
            self.df.to_excel('Résultats_Sentiments.xlsx', index=False)
            
        return

def formate_options(options):
    options_json = {
        'execution_time': False,
        'to_excel': False
    }
    
    if options:
        if 'Temps d\'exécution' in options:
            options_json['execution_time'] = True
            
        if 'Export en excel' in options:
            options_json['to_excel'] = True  

    return options_json








file_input = st.file_uploader("Importer un fichier XLSX", type="xlsx")

options = st.multiselect('Choisissez les options à ajouter', ['Temps d\'exécution', 'Export en excel'])

if st.button('Lancer le traitement'):
    if file_input is not None:
        st.info('Le traitement a démarré')
        
        df = pd.read_excel(file_input)
        df = df[:50]
        
        formatted_options = formate_options(options)
        
        sentiment = Sentiment(df, to_excel=formatted_options['to_excel'], execution_time=formatted_options['execution_time'])

        st.write(sentiment.df[['Last Updated Date', 'ID', 'Review']])
        
        sentiment.run()
        
        st.success("Résultats")
        st.write(sentiment.df[['Last Updated Date', 'ID', 'Sentiment', 'Review']])
        
    else:
        st.error('Veuillez importer un fichier XLSX ou CSV')


