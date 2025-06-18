import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = 'https://www.folha.uol.com.br/'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')

noticias = []

for a in soup.find_all('a'):
    titulo = a.get_text(strip=True)
    link = a.get('href')

    if titulo and link and len(titulo) > 30 and '/202' in link:
        if not link.startswith('http'):
            link = 'https://www.folha.uol.com.br' + link
        noticias.append({
            'Título': titulo,
            'Link': link,
            'Seção': 'Principal',
            'Data': datetime.now().strftime('%d/%m/%Y')
        })

df_folha = pd.DataFrame(noticias).drop_duplicates(subset='Título')
df_folha.to_csv('noticias_folha_dataframe.csv', index=False, encoding='utf-8')
