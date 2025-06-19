import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv

url = 'https://noticias.uol.com.br/'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')

noticias = []

for item in soup.find_all('a'):
    texto = item.get_text(strip=True)
    link = item.get('href')

    # Filtra só textos maiores que 40 caracteres e links relativos ou absolutos no UOL
    if texto and len(texto) > 40 and link and ('/noticias/' in link or link.startswith('https://noticias.uol.com.br')):
        noticias.append({
            'Título': texto,
            'Seção': 'Principal',
            'Data': datetime.now().strftime('%d/%m/%Y'),
            'Link': link if link.startswith('http') else 'https://noticias.uol.com.br' + link
        })

# Remove duplicatas pelo título
noticias_unicas = {n['Título']: n for n in noticias}

with open('noticias_uol.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Título', 'Seção', 'Data', 'Link'])
    for n in noticias_unicas.values():
        writer.writerow([n['Título'], n['Seção'], n['Data'], n['Link']])

df_uol = pd.DataFrame(noticias_unicas.values())
df_uol.to_csv('noticias_uol_dataframe.csv', index=False, encoding='utf-8')

print(df_uol.head())
print(f'{len(df_uol)} notícias salvas em "noticias_uol_dataframe.csv".')
