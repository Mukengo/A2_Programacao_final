import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv

# Lista de seções principais
secoes = [
    'https://www.cnnbrasil.com.br',
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

    for h3 in soup.find_all('h3'):
        titulo = h3.get_text(strip=True)
        if titulo and len(titulo) > 30:  # Filtra títulos curtos demais
            noticias.append({
                'Título': titulo,
                'Seção': secao,
                'Data': datetime.now().strftime('%d/%m/%Y')
            })

# Remove duplicatas
noticias_unicas = {n['Título']: (n['Seção'], n['Data']) for n in noticias}

with open('noticias_cnn.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Título', 'Seção', 'Data'])
    for titulo, (secao, data) in noticias_unicas.items():
        writer.writerow([titulo, secao, data])

df_cnn = pd.DataFrame(
    [{'Título': titulo, 'Seção': secao, 'Data': data} for titulo, (secao, data) in noticias_unicas.items()]
)
df_cnn.to_csv('noticias_cnn_dataframe.csv', index=False, encoding='utf-8')

print(df_cnn.head())
print(f'{len(df_cnn)} notícias salvas em "noticias_cnn_dataframe.csv".')
