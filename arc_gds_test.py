import pandas as pd 
import gspread
import numpy as np
import datetime

gc = gspread.service_account(filename='service_account.json')

sheet = gc.open_by_key('1zpTiptkUGEj0EVMbvOMoIMnbSFnR-R4XZyvuaM_xzto')

ws_to_avoid = sheet.worksheets()[:4]

start_col = 17 # column Q

df = pd.DataFrame()
df_transformed = pd.DataFrame(columns=['Date', 'Client', 'Sujet / Titre de la page', 'Généré par IA', 'URL', 'Page indexée', 'Groupement de mots-clés', 'Trafic Naturel', 'Position Moyenne', 'Impressions', 'CTR', 'M±X', 'Date de publication'])

for ws in sheet.worksheets():
    if ws not in ws_to_avoid:
        if ws.title == "L'appart Fitness":
            # concat the value of the worksheet without the first row of the sheet, the second row is the header
            df = pd.concat([df, pd.DataFrame(ws.get_all_values()[2:], columns=ws.get_all_values()[1])], ignore_index=True)
            df = df[['N°', 'Sujet / Titre de la page', 'Date de publication', 'Groupement de mots-clés', 
                    'Contenu généré par IA', 'Page indexée sur Google ?', 'URL', 
                    'Trafic Naturel M-1', 'Position Moyenne M-1', 'Impressions M-1', 'CTR M-1', 
                    'Trafic naturel M+1', 'Position moyenne M+1', 'Impressions M+1', 'CTR M+1', 
                    'Trafic naturel M+2', 'Position moyenne M+2', 'Impressions M+2', 'CTR M+2',
                    'Trafic naturel M+3', 'Position moyenne M+3', 'Impressions M+3', 'CTR M+3', 
                    'Trafic naturel M+4', 'Position moyenne M+4', 'Impressions M+4', 'CTR M+4', 
                    'Trafic naturel M+5', 'Position moyenne M+5', 'Impressions M+5', 'CTR M+5',
                    'Trafic naturel M+6', 'Position moyenne M+6', 'Impressions M+6', 'CTR M+6'
                ]]
            
            # Parcourir les lignes du dataframe initial
            for i in range(len(df)):
                trafic_m1 = df.iloc[i]['Trafic Naturel M-1']
                date_publication = df.iloc[i]['Date de publication']
                try:
                    ia = True if df.iloc[i]['Contenu généré par IA'] == 'Oui' else False
                except:
                    ia = False
                try:
                    indexed = df.iloc[i]['Page indexée sur Google ?']
                    if indexed == '':
                        indexed = False
                    else:
                        indexed = True
                except:
                    indexed = False
                url = df.iloc[i]['URL']
                
                # Vérifier s'il y a une valeur dans la colonne "Trafic Naturel M-1"
                if pd.notnull(trafic_m1) and date_publication != '':
                    sujet = df.iloc[i]['Sujet / Titre de la page']
                    keywords = df.iloc[i]['Groupement de mots-clés']
                    
                    # Ajouter la première ligne avec les informations de la publication
                    df_transformed.loc[i] = [date_publication, ws.title, sujet, ia, indexed, url, keywords, np.nan, np.nan, np.nan, np.nan, 'M+0', date_publication]
                    
                    # Calculer la date correspondant à M-1 (-31 jours)
                    date_m1 = datetime.datetime.strptime(date_publication, "%Y-%m-%d") - datetime.timedelta(days=31)
                    date_m1_formatted = date_m1.strftime("%Y-%m-%d")

                    # Récupérer les données du mois M-1
                    trafic_m1 = float(df.iloc[i]['Trafic Naturel M-1'].replace(',', '.'))
                    position_moyenne_m1 = float(df.iloc[i]['Position Moyenne M-1'].replace(',', '.'))
                    impressions_m1 = float(df.iloc[i]['Impressions M-1'].replace(',', '.'))
                    ctr_m1 = float(df.iloc[i]['CTR M-1'].replace(',', '.'))

                    # Ajouter les données du mois M-1 à df_transformed
                    df_m1 = pd.DataFrame([[date_m1_formatted, ws.title, sujet, ia, indexed, url, keywords, trafic_m1, position_moyenne_m1, impressions_m1, ctr_m1, 'M-1', date_publication]],
                                        columns=['Date', 'Client', 'Sujet / Titre de la page',  'Généré par IA', 'Page indexée', 'URL', 'Groupement de mots-clés', 'Trafic Naturel', 'Position Moyenne', 'Impressions', 'CTR', 'M±X', 'Date de publication'])
                    df_transformed = pd.concat([df_m1, df_transformed], ignore_index=True)

                    # Parcourir les colonnes du dataframe initial
                    for col in df.columns:
                        if col.startswith('Trafic naturel M+'):
                            month = col.split('M+')[1]
                            index = int(month)
                            date = datetime.datetime.strptime(date_publication, "%Y-%m-%d") + datetime.timedelta(days=index*31)
                            date_formatted = date.strftime("%Y-%m-%d")

                            # Vérifier s'il y a une valeur dans la colonne correspondant à M+X
                            if pd.notnull(df.iloc[i][col]) and df.iloc[i][col] != '':
                                trafic_naturel = float(df.iloc[i][col].replace(',', '.'))
                                position_moyenne = float(df.iloc[i]['Position moyenne M+' + month].replace(',', '.'))
                                impressions = float(df.iloc[i]['Impressions M+' + month].replace(',', '.'))
                                ctr = float(df.iloc[i]['CTR M+' + month].replace(',', '.'))

                                # Ajouter les données du mois M+X à df_transformed
                                df_month = pd.DataFrame([[date_formatted, ws.title, sujet, ia, indexed, url, keywords, trafic_naturel, position_moyenne, impressions, ctr, 'M+' + month, date_publication]],
                                                        columns=['Date', 'Client', 'Sujet / Titre de la page', 'Généré par IA', 'Page indexée', 'URL', 'Groupement de mots-clés', 'Trafic Naturel', 'Position Moyenne', 'Impressions', 'CTR', 'M±X', 'Date de publication'])
                                df_transformed = pd.concat([df_transformed, df_month], ignore_index=True)
                            else:
                                # Sortir de la boucle for imbriquée si aucune donnée en M+X
                                break

# Afficher le dataframe transformé
df_transformed = df_transformed.sort_values(by=['Sujet / Titre de la page', 'Date'], ignore_index=True)
# df_transformed.to_csv('data.csv', index=False)
