import pandas as pd

df = pd.read_csv('data/french_words.csv')  # assumes header columns like French, English
words_list = df.to_dict(orient='records')
print(words_list[:5])  # preview first 5 rows