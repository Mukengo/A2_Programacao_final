import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def raspar_g1_ampliado():
    # Lista de seções populares do G1 para coletar mais notícias
    secoes = [
        '',  # Página inicial
        'ultimas-noticias',
        'politica',
        'economia',
        'tecnologia',
        'mundo',
        'ciencia',
        'educacao',
        'saude',
        'turismo',
        'ambiente',
        'carros',
        'pop-arte',
        'natureza',
        'bemestar',
        'lgbtqia'
    ]

    base_url = 'https://g1.globo.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}

    noticias = []
    links_unicos = set()

    for secao in secoes:
        url = base_url + secao + '/' if secao else base_url
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.find_all('a', class_='feed-post-link'):
            titulo = item.get_text(strip=True)
            link = item.get('href')

            if titulo and link and len(titulo) > 20 and link not in links_unicos:
                links_unicos.add(link)
                noticias.append({
                    'Título': titulo,
                    'Link': link,
                    'Seção': secao if secao else 'principal',
                    'Data': datetime.now().strftime('%d/%m/%Y')
                })

    df = pd.DataFrame(noticias)
    df.to_csv('noticias_g1_dataframe.csv', index=False, encoding='utf-8')
    print(f'{len(df)} notícias salvas em "noticias_g1_dataframe.csv".')

# Executa a função
raspar_g1_ampliado()
