import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse
import pandas as pd

# Lista ampliada de seções do G1 (14 seções principais + especiais)
secoes = [
    'https://g1.globo.com/',
    'https://g1.globo.com/politica/',
    'https://g1.globo.com/economia/',
    'https://g1.globo.com/mundo/',
    'https://g1.globo.com/brasil/',
    'https://g1.globo.com/saude/',
    'https://g1.globo.com/tecnologia/',
    'https://g1.globo.com/ciencia/',
    'https://g1.globo.com/educacao/',
    'https://g1.globo.com/pop-arte/',
    'https://g1.globo.com/esportes/',
    'https://g1.globo.com/carros/',
    'https://g1.globo.com/turismo-e-viagem/',
    'https://g1.globo.com/ciencia-e-saude/'
]

noticias = []

for url in secoes:
    print(f'Raspando: {url}')
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        secao = urlparse(url).path.strip('/').split('/')[-1].capitalize()
        if not secao:  # Para a página principal
            secao = 'Principal'

        # Coleta todos os elementos que podem conter notícias
        for elemento in soup.find_all(['div', 'a']):
            classes = elemento.get('class', [])

            # Padrão 1: Notícias principais
            if 'feed-post-body' in classes:
                titulo_tag = elemento.find('a', class_='feed-post-link')
                if titulo_tag:
                    texto = titulo_tag.get_text(strip=True)
                    if texto:
                        data_tag = elemento.find('span', class_='feed-post-datetime')
                        data = data_tag.get_text(strip=True) if data_tag else 'Hoje'
                        noticias.append({'Título': texto, 'Seção': secao, 'Data': data})

            # Padrão 2: Notícias secundárias
            elif 'bstn-fd-relateditem' in classes:
                titulo_tag = elemento.find('a')
                if titulo_tag:
                    texto = titulo_tag.get_text(strip=True)
                    if texto:
                        data_tag = elemento.find('span', class_='feed-post-datetime') or elemento.find('span', class_='bstn-fd-relatedtime')
                        data = data_tag.get_text(strip=True) if data_tag else 'Hoje'
                        noticias.append({'Título': texto, 'Seção': secao, 'Data': data})

            # Padrão 3: Links diretos de notícias
            elif 'feed-post-link' in classes:
                texto = elemento.get_text(strip=True)
                if texto:
                    noticias.append({'Título': texto, 'Seção': secao, 'Data': 'Hoje'})

    else:
        print(f'Erro ao acessar: {url} — Código {response.status_code}')

# Remove duplicatas (mesmo método original)
noticias_unicas = {}
for noticia in noticias:
    noticias_unicas[noticia['Título']] = (noticia['Seção'], noticia['Data'])

# Gera o CSV (idêntico ao original)
with open('noticias_g1.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Título', 'Seção', 'Data'])
    for titulo, (secao, data) in noticias_unicas.items():
        writer.writerow([titulo, secao, data])

noticias_lista = [
    {'Título': titulo, 'Seção': secao, 'Data': data}
    for titulo, (secao, data) in noticias_unicas.items()
]

# Cria o DataFrame
df_g1 = pd.DataFrame(noticias_lista, columns=['Título', 'Seção', 'Data'])

# (Opcional) Salva em CSV
df_g1.to_csv('noticias_g1_dataframe.csv', index=False, encoding='utf-8')

from datetime import datetime

# Supondo que df_g1 é seu DataFrame
df_g1['Data'] = df_g1['Data'].replace(
    'Hoje',
    datetime.now().strftime('%d/%m/%Y')
)

print(df_g1.head())
print(f'{len(df_g1)} notícias salvas no DataFrame e em "noticias_g1_dataframe.csv".')

print(f'{len(noticias_unicas)} notícias salvas em "noticias_g1.csv".')
