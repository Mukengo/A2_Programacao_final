import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout="wide")
st.title("📰 Comparador de Notícias - G1, CNN e Folha")

aba = st.selectbox("Escolha o que deseja visualizar", ['Comparativo Geral', 'G1', 'CNN', 'Folha'])

if aba == 'Comparativo Geral':
    st.header("📊 Quantidade de Notícias por Site")
    st.image('grafico_quantidade.png')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🧠 G1")
        st.image('nuvem_g1.png')
        st.dataframe(pd.read_csv('top_palavras_g1.csv'))
    with col2:
        st.subheader("🧠 CNN")
        st.image('nuvem_cnn.png')
        st.dataframe(pd.read_csv('top_palavras_cnn.csv'))
    with col3:
        st.subheader("🧠 Folha")
        st.image('nuvem_folha.png')
        st.dataframe(pd.read_csv('top_palavras_folha.csv'))

else:
    nome_site = aba
    nome_arquivo = nome_site.lower()

    st.header(f"📰 Notícias do {nome_site}")
    df = pd.read_csv(f'noticias_{nome_arquivo}_dataframe.csv')

# Cria link clicável em HTML
def transformar_em_link(row):
    return f'<a href="{row["Link"]}" target="_blank">{row["Título"]}</a>'

df['Título com Link'] = df.apply(transformar_em_link, axis=1)

# Mostra a tabela com link
st.write("Clique no título para acessar a notícia:")
st.write(df[['Título com Link', 'Seção', 'Data']].to_html(escape=False, index=False), unsafe_allow_html=True)


    st.subheader("☁️ Nuvem de Palavras")
    st.image(f'nuvem_{nome_arquivo}.png')

    st.subheader("🔝 Principais Palavras")
    df_top = pd.read_csv(f'top_palavras_{nome_arquivo}.csv')
    st.dataframe(df_top)
