import pandas as pd 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Liste des scopes d'accès requis
scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Authentification avec les informations d'identification et les scopes
credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scopes)
client = gspread.authorize(credentials)

file_id = '1zpTiptkUGEj0EVMbvOMoIMnbSFnR-R4XZyvuaM_xzto'

# Ouvrir le fichier Google Sheet
sheet = client.open_by_key(file_id)
