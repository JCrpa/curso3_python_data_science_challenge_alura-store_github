import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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

def calcular_faturamento_total(dados):
    """Calcula o faturamento total."""
    return dados['Valor_Venda'].sum()

def calcular_faturamento_por_loja(dados):
    """Calcula o faturamento por loja."""
    return dados.groupby('Loja')['Valor_Venda'].sum()

def calcular_vendas_por_categoria(dados):
    """Calcula o total de vendas por categoria."""
    return dados.groupby('Categoria')['Quantidade'].sum()

def calcular_faturamento_por_categoria(dados):
    """Calcula o faturamento total por categoria."""
    return dados.groupby('Categoria')['Valor_Venda'].sum()

def calcular_vendas_faturamento_por_categoria_loja(dados, categoria):
    """Calcula vendas e faturamento por categoria e loja."""
    return dados[dados['Categoria'] == categoria].groupby('Loja').agg({'Quantidade': 'sum', 'Valor_Venda': 'sum'})

st.title("Análise de Dados da AluraStore")

aba_faturamento, aba_vendas_categoria, aba_avaliacoes = st.tabs(
    ["Faturamento", "Vendas por Categoria", "Avaliações"]
)

dados = carregar_dados()

with aba_faturamento:
    st.header("Análise de Faturamento")

    # Seleção de Loja
    lojas_selecionadas = st.multiselect("Selecione as Lojas:", dados['Loja'].unique(), default=dados['Loja'].unique())
    dados_filtrados = dados[dados['Loja'].isin(lojas_selecionadas)]

    faturamento_total = calcular_faturamento_total(dados_filtrados)
    st.subheader("Faturamento Total")
    st.write(f"O faturamento total é: R$ {faturamento_total:,.2f}")

    faturamento_por_loja = calcular_faturamento_por_loja(dados_filtrados)
    st.subheader("Faturamento por Loja")
    st.dataframe(faturamento_por_loja)

    # Gráfico de Faturamento por Loja
    st.subheader("Gráfico de Faturamento por Loja")
    fig_faturamento_loja, ax_faturamento_loja = plt.subplots(figsize=(10, 5))
    faturamento_por_loja.plot(kind='bar', ax=ax_faturamento_loja, color='skyblue')
    ax_faturamento_loja.set_title("Faturamento por Loja", fontsize=16)
    ax_faturamento_loja.set_xlabel("Loja", fontsize=12)
    ax_faturamento_loja.set_ylabel("Faturamento", fontsize=12)
    ax_faturamento_loja.tick_params(axis='x', rotation=0)
    st.pyplot(fig_faturamento_loja)

with aba_vendas_categoria:
    st.header("Análise de Vendas por Categoria")

    # Seleção de Categoria
    categoria_selecionada = st.selectbox("Selecione uma Categoria:", dados['Categoria'].unique())

    vendas_por_categoria = calcular_vendas_por_categoria(dados)
    st.subheader("Total de Vendas por Categoria")
    st.dataframe(vendas_por_categoria)

    faturamento_por_categoria = calcular_faturamento_por_categoria(dados)
    st.subheader("Faturamento por Categoria")
    st.dataframe(faturamento_por_categoria)

    # Vendas e Faturamento por Categoria e Loja
    st.subheader(f"Vendas e Faturamento de {categoria_selecionada} por Loja")
    vendas_faturamento_categoria_loja = calcular_vendas_faturamento_por_categoria_loja(dados, categoria_selecionada)
    st.dataframe(vendas_faturamento_categoria_loja)

    # Gráfico de Vendas por Categoria
    st.subheader("Gráfico de Vendas por Categoria")
    fig_vendas_categoria, ax_vendas_categoria = plt.subplots(figsize=(10, 5))
    vendas_por_categoria.plot(kind='bar', ax=ax_vendas_categoria, color='lightgreen')
    ax_vendas_categoria.set_title("Total de Vendas por Categoria", fontsize=16)
    ax_vendas_categoria.set_xlabel("Categoria", fontsize=12)
    ax_vendas_categoria.set_ylabel("Total de Vendas", fontsize=12)
    ax_vendas_categoria.tick_params(axis='x', rotation=45)
    st.pyplot(fig_vendas_categoria)

    # Gráfico de Faturamento por Categoria
    st.subheader("Gráfico de Faturamento por Categoria")
    fig_faturamento_categoria, ax_faturamento_categoria = plt.subplots(figsize=(10, 5))
    faturamento_por_categoria.plot(kind='bar', ax=ax_faturamento_categoria, color='lightcoral')
    ax_faturamento_categoria.set_title("Faturamento por Categoria", fontsize=16)
    ax_faturamento_categoria.set_xlabel("Categoria", fontsize=12)
    ax_faturamento_categoria.set_ylabel("Faturamento", fontsize=12)
    ax_faturamento_categoria.tick_params(axis='x', rotation=45)
    st.pyplot(fig_faturamento_categoria)

with aba_avaliacoes:
    st.header("Análise de Avaliações")
    st.write("Aqui vamos mostrar a análise de avaliações.")