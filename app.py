import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os  # Importe o módulo os

@st.cache_data
def carregar_dados():
    caminho_base = "./base-de-dados-challenge-1/"  # Ajuste o caminho se necessário
    arquivos_lojas = ['loja_1.csv', 'loja_2.csv', 'loja_3.csv', 'loja_4.csv']
    lista_tabelas = []

    for arquivo in arquivos_lojas:
        caminho_completo = os.path.join(caminho_base, arquivo)
        df_loja = pd.read_csv(caminho_completo)
        lista_tabelas.append(df_loja)

    dados = pd.concat(lista_tabelas, ignore_index=True)
    return dados

st.title("Análise de Dados da AluraStore")

aba_faturamento, aba_vendas_categoria, aba_avaliacoes = st.tabs(
    ["Faturamento", "Vendas por Categoria", "Avaliações"]
)

dados = carregar_dados()

with aba_faturamento:
    st.header("Análise de Faturamento")
    st.write("Dados Carregados:")
    st.dataframe(dados.head())

    # Resto da análise de faturamento...

with aba_vendas_categoria:
    st.header("Análise de Vendas por Categoria")
    st.write("Dados Carregados:")
    st.dataframe(dados.head())

    # Resto da análise de vendas por categoria...

with aba_avaliacoes:
    st.header("Análise de Avaliações")
    st.write("Dados Carregados:")
    st.dataframe(dados.head())

    # Resto da análise de avaliações...