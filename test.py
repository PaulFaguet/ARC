from classes.arc_multiple import ARC_Multiple
import pandas as pd 
import time


test = ARC_Multiple(r'C:\Users\PFA\OneDrive - Axess OnLine\Bureau\Adcom - Brief.xlsx')
# in the df, read the value in the column "Client" with index 0
client = test.df.loc[0, "Client"]