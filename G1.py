import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv

url = 'https://g1.globo.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

noticias = []

for item in soup.find_all('a', class_='feed-post-link'):
    titulo = item.get_text().strip()
    link = item['href']
    if titulo and len(titulo) > 20:
        noticias.append({
            'Título': titulo,
            'Link': link,
            'Seção': 'Principal',
            'Data': datetime.now().strftime('%d/%m/%Y')
        })

# Salva com o campo "Link"
df = pd.DataFrame(noticias)
df.to_csv('noticias_g1_dataframe.csv', index=False, encoding='utf-8')
