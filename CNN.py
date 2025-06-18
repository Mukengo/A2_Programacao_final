import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

secoes = [
    'https://www.cnnbrasil.com.br/',
    'https://www.cnnbrasil.com.br/politica/',
    'https://www.cnnbrasil.com.br/economia/',
    'https://www.cnnbrasil.com.br/internacional/',
    'https://www.cnnbrasil.com.br/saude/',
    'https://www.cnnbrasil.com.br/tecnologia/',
    'https://www.cnnbrasil.com.br/esportes/'
]

noticias = []

for url in secoes:
    print(f'Raspando: {url}')
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')

    secao = url.split('/')[-2].capitalize() if url.endswith('/') else url.split('/')[-1].capitalize()
    if 'brasil' in secao.lower():
        secao = 'Principal'

    for a in soup.find_all('a', class_='home__list__tag__link'):
        link = a.get('href')
        titulo = a.get_text(strip=True)

        # Filtra links incompletos
        if link and not link.startswith('http'):
            link = 'https://www.cnnbrasil.com.br' + link

        if titulo and link and len(titulo) > 20:
            noticias.append({
                'Título': titulo,
                'Link': link,
                'Seção': secao,
                'Data': datetime.now().strftime('%d/%m/%Y')
            })

df_cnn = pd.DataFrame(noticias).drop_duplicates(subset='Título')
df_cnn.to_csv('noticias_cnn_dataframe.csv', index=False, encoding='utf-8')
