import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv

url = 'https://www.folha.uol.com.br/'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')

noticias = []

for item in soup.find_all('a'):
    texto = item.get_text(strip=True)
    if texto and len(texto) > 40:
        noticias.append({
            'Título': texto,
            'Seção': 'Principal',
            'Data': datetime.now().strftime('%d/%m/%Y')
        })

# Remove duplicatas
noticias_unicas = {n['Título']: (n['Seção'], n['Data']) for n in noticias}

with open('noticias_folha.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Título', 'Seção', 'Data'])
    for titulo, (secao, data) in noticias_unicas.items():
        writer.writerow([titulo, secao, data])

df_folha = pd.DataFrame(
    [{'Título': titulo, 'Seção': secao, 'Data': data} for titulo, (secao, data) in noticias_unicas.items()]
)
df_folha.to_csv('noticias_folha_dataframe.csv', index=False, encoding='utf-8')

print(df_folha.head())
print(f'{len(df_folha)} notícias salvas em "noticias_folha_dataframe.csv".')
