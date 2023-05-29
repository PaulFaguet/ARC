from classes.classe_sentiment import Sentiment

import pandas as pd 
import time

start = time.time()
# df = pd.read_excel('Sentiment Test.xlsx')
df2 = pd.read_excel('Hippopotamus_Yext.xlsx')
print('IMPORT', time.time() - start)

start = time.time()
sentiment = Sentiment(df2[:3000])
print('INSTANCIATION', time.time() - start)

start = time.time()
sentiment.run()
print('RUN', time.time() - start)


