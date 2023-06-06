from classes.arc_multiple import ARC_Multiple
import pandas as pd 
import time


df = pd.read_csv(r'C:\Users\PFA\OneDrive - Axess OnLine\Bureau\open_ai\Feuille de calcul sans titre - Feuille 1 (1).csv')

def trouver_differences_csv(file_path):
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(file_path)

    # Comparer chaque ligne avec la ligne précédente et trouver les différences
    differences = df.ne(df.shift())
    print("differences",differences)

    # Vérifier si des différences existent
    if differences.any().any():
        # Afficher les différences
        for index, row in differences.iterrows():
            print(f"Différences à la ligne {index + 1}:")
            print(row[row].index.tolist())

    else:
        print("Aucune différence trouvée entre les lignes du CSV.")

# Exemple d'utilisation
trouver_differences_csv(r"C:\Users\PFA\OneDrive - Axess OnLine\Bureau\open_ai\Feuille de calcul sans titre - Feuille 1 (1).csv")

