import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Análise de Dados da AluraStore")

aba_faturamento, aba_vendas_categoria, aba_avaliacoes = st.tabs(
    ["Faturamento", "Vendas por Categoria", "Avaliações"]
)

with aba_faturamento:
    st.header("Análise de Faturamento")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Faturamento Total")
        st.write("Aqui vamos mostrar o faturamento total.")

    with col2:
        st.subheader("Faturamento por Loja")
        st.write("Aqui vamos mostrar o faturamento por loja.")

with aba_vendas_categoria:
    st.header("Análise de Vendas por Categoria")

    with st.expander("Vendas de Eletrodomésticos"):
        st.write("Informações detalhadas sobre as vendas de eletrodomésticos.")

    with st.expander("Vendas de Eletrônicos"):
        st.write("Informações detalhadas sobre as vendas de eletrônicos.")

with aba_avaliacoes:
    st.header("Análise de Avaliações")
    st.write("Aqui vamos mostrar a análise de avaliações.")