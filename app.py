import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout='wide')
st.title("Comparativo de Notícias: UOL, G1 e Folha")

# --- Carregar dados e imagens diretamente da raiz ---
uol = pd.read_csv('noticias_uol_dataframe.csv')
g1 = pd.read_csv('noticias_g1_dataframe.csv')
folha = pd.read_csv('noticias_folha_dataframe.csv')

img_uol = Image.open('nuvem_uol.png')
img_g1 = Image.open('nuvem_g1.png')
img_folha = Image.open('nuvem_folha.png')
img_grafico = Image.open('grafico_comparativo.png')

# --- Menu lateral ---
menu = st.sidebar.radio("Escolha uma página:", ['Comparativo Geral', 'UOL', 'G1', 'Folha'])

# --- Página Comparativa ---
if menu == 'Comparativo Geral':
    st.header("📊 Quantidade de Notícias por Site")
    st.image(img_grafico, use_container_width=True)

    st.markdown("### 🔠 Palavras mais frequentes")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("UOL")
        uol_palavras = pd.read_csv("palavras_uol.csv")
        st.dataframe(uol_palavras)

    with col2:
        st.subheader("G1")
        g1_palavras = pd.read_csv("palavras_g1.csv")
        st.dataframe(g1_palavras)

    with col3:
        st.subheader("Folha")
        folha_palavras = pd.read_csv("palavras_folha.csv")
        st.dataframe(folha_palavras)

# --- Página UOL ---
elif menu == 'UOL':
    st.header("📰 Notícias - UOL")
    st.image(img_uol, use_container_width=True)
    st.dataframe(uol)

# --- Página G1 ---
elif menu == 'G1':
    st.header("📰 Notícias - G1")
    st.image(img_g1, use_container_width=True)
    st.dataframe(g1)

# --- Página Folha ---
elif menu == 'Folha':
    st.header("📰 Notícias - Folha")
    st.image(img_folha, use_container_width=True)
    st.dataframe(folha)
