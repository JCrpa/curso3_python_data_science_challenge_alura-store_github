import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime

@st.cache_data
def carregar_dados():
    caminho_base = "./base-de-dados-challenge-1/"  # Ajuste o caminho se necessário
    arquivos_lojas = ['loja_1.csv', 'loja_2.csv', 'loja_3.csv', 'loja_4.csv']
    lista_tabelas = []

    for arquivo in arquivos_lojas:
        caminho_completo = os.path.join(caminho_base, arquivo)
        df_loja = pd.read_csv(caminho_completo)
        nome_loja = arquivo.split('.')[0].capitalize().replace('_', ' ')
        df_loja['Loja'] = nome_loja
        # Renomeando a coluna 'Preço' para 'Valor_Venda'
        if 'Preço' in df_loja.columns:
            df_loja.rename(columns={'Preço': 'Valor_Venda'}, inplace=True)
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
    """Calcula o total de vendas por categoria (contagem de ocorrências)."""
    return dados.groupby('Categoria do Produto')['Produto'].count()

def calcular_faturamento_por_categoria(dados):
    """Calcula o faturamento total por categoria."""
    return dados.groupby('Categoria do Produto')['Valor_Venda'].sum()

def calcular_vendas_faturamento_por_categoria_loja(dados, categoria):
    """Calcula vendas (contagem) e faturamento por categoria e loja."""
    return dados[dados['Categoria do Produto'] == categoria].groupby('Loja').agg({'Produto': 'count', 'Valor_Venda': 'sum'})

def calcular_distribuicao_notas(dados):
    """Calcula a distribuição das notas."""
    return dados['Avaliação da compra'].value_counts().sort_index()

def calcular_media_avaliacoes_por_produto(dados):
    """Calcula a média das avaliações por produto."""
    return dados.groupby('Produto')['Avaliação da compra'].mean().sort_values(ascending=False)

st.title("Análise de Dados da AluraStore")

aba_faturamento, aba_vendas_categoria, aba_avaliacoes = st.tabs(
    ["Faturamento", "Vendas por Categoria", "Avaliações"]
)

dados = carregar_dados()

with aba_faturamento:
    st.header("Análise de Faturamento")
    st.write("Esta seção mostra o faturamento total e por loja. Use o filtro abaixo para selecionar as lojas desejadas.")

    # Seleção de Loja (usando multiselect com opção "Todas")
    lojas_disponiveis = dados['Loja'].unique()
    opcoes_lojas = ["Todas"] + list(lojas_disponiveis)
    lojas_selecionadas = st.multiselect("Selecione as Lojas:", opcoes_lojas, default=["Todas"], key="filtro_lojas")

    if "Todas" in lojas_selecionadas:
        dados_filtrados_faturamento = dados
    else:
        dados_filtrados_faturamento = dados[dados['Loja'].isin(lojas_selecionadas)]

    faturamento_total = calcular_faturamento_total(dados_filtrados_faturamento)
    st.subheader("Faturamento Total")
    st.write(f"O faturamento total é: R$ {faturamento_total:,.2f}")

    faturamento_por_loja = calcular_faturamento_por_loja(dados_filtrados_faturamento)
    # Converter Series para DataFrame e formatar
    faturamento_por_loja_df = faturamento_por_loja.reset_index()
    faturamento_por_loja_df.columns = ['Loja', 'Faturamento']  # Renomear colunas para melhor clareza
    st.subheader("Faturamento por Loja")
    st.dataframe(faturamento_por_loja_df.style.format({"Faturamento": "R$ {:,.2f}"}))

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
    st.write("Esta seção mostra as vendas e o faturamento por categoria. Selecione uma categoria para ver os detalhes.")

    # Seleção de Categoria
    categoria_selecionada = st.selectbox("Selecione uma Categoria:", dados['Categoria do Produto'].unique())

    # Criar placeholders na ordem desejada
    info_placeholder = st.empty()
    vendas_loja_placeholder = st.empty() # Placeholder para "Vendas e Faturamento por Loja"
    separator_placeholder = st.empty()
    vendas_total_placeholder = st.empty()
    faturamento_total_placeholder = st.empty()
    grafico_vendas_placeholder = st.empty()
    grafico_faturamento_placeholder = st.empty()

    # Filtrar os dados com base na categoria selecionada
    dados_filtrados_categoria = dados[dados['Categoria do Produto'] == categoria_selecionada]

    # Calcular vendas e faturamento para a categoria selecionada
    vendas_categoria_selecionada = dados_filtrados_categoria['Produto'].count()
    faturamento_categoria_selecionada = dados_filtrados_categoria['Valor_Venda'].sum()

    # Preencher o placeholder das informações principais
    with info_placeholder.container():
        st.subheader(f"Informações da Categoria: {categoria_selecionada}")
        st.write(f"**Total de Vendas:** {vendas_categoria_selecionada}")
        st.write(f"**Faturamento Total:** R$ {faturamento_categoria_selecionada:,.2f}")

    # Preencher o placeholder de "Vendas e Faturamento por Loja"
    with vendas_loja_placeholder.container():
        st.subheader(f"Vendas e Faturamento de {categoria_selecionada} por Loja")
        vendas_faturamento_categoria_loja = calcular_vendas_faturamento_por_categoria_loja(dados, categoria_selecionada)
        st.dataframe(vendas_faturamento_categoria_loja.style.format({"Valor_Venda": "R$ {:,.2f}"}), key=f"vendas_categoria_loja_{categoria_selecionada}")

    separator_placeholder.markdown("---")

    # Preencher os placeholders das tabelas gerais
    with vendas_total_placeholder.container():
        st.subheader("Total de Vendas por Categoria")
        vendas_por_categoria = dados.groupby('Categoria do Produto')['Produto'].count()
        st.dataframe(vendas_por_categoria)

    with faturamento_total_placeholder.container():
        st.subheader("Faturamento por Categoria")
        faturamento_por_categoria_df = dados.groupby('Categoria do Produto')['Valor_Venda'].sum().reset_index()
        faturamento_por_categoria_df.columns = ['Categoria do Produto', 'Faturamento']
        st.dataframe(faturamento_por_categoria_df.style.format({"Faturamento": "R$ {:,.2f}"}))

    # Preencher os placeholders dos gráficos
    with grafico_vendas_placeholder.container():
        st.subheader("Gráfico de Vendas por Categoria")
        fig_vendas_categoria, ax_vendas_categoria = plt.subplots(figsize=(10, 5))
        vendas_por_categoria.plot(kind='bar', ax=ax_vendas_categoria, color='lightgreen')
        ax_vendas_categoria.set_title("Total de Vendas por Categoria", fontsize=16)
        ax_vendas_categoria.set_xlabel("Categoria do Produto", fontsize=12)
        ax_vendas_categoria.set_ylabel("Total de Vendas", fontsize=12)
        ax_vendas_categoria.tick_params(axis='x', rotation=45)
        st.pyplot(fig_vendas_categoria)

    with grafico_faturamento_placeholder.container():
        st.subheader("Gráfico de Faturamento por Categoria")
        fig_faturamento_categoria, ax_faturamento_categoria = plt.subplots(figsize=(10, 5))
        faturamento_por_categoria = dados.groupby('Categoria do Produto')['Valor_Venda'].sum()
        faturamento_por_categoria.plot(kind='bar', ax=ax_faturamento_categoria, color='lightcoral')
        ax_faturamento_categoria.set_title("Faturamento por Categoria", fontsize=16)
        ax_faturamento_categoria.set_xlabel("Categoria do Produto", fontsize=12)
        ax_faturamento_categoria.set_ylabel("Faturamento", fontsize=12)
        ax_faturamento_categoria.tick_params(axis='x', rotation=45)
        st.pyplot(fig_faturamento_categoria)

with aba_avaliacoes:
    st.header("Análise de Avaliações")
    st.write("Esta seção mostra a distribuição das notas e a média das avaliações por produto. Selecione um produto para ver os detalhes.")

    # Seleção de Produto
    produto_selecionado = st.selectbox("Selecione um Produto:", dados['Produto'].unique())

    # Criar placeholders para as informações do produto selecionado
    media_produto_placeholder = st.empty()
    separator_placeholder_avaliacao = st.empty()

    distribuicao_notas = calcular_distribuicao_notas(dados)
    st.subheader("Distribuição das Notas")
    st.dataframe(distribuicao_notas)

    media_avaliacoes_produto = calcular_media_avaliacoes_por_produto(dados)
    # Converter Series para DataFrame e formatar
    media_avaliacoes_produto_df = media_avaliacoes_produto.reset_index()
    media_avaliacoes_produto_df.columns = ['Produto', 'Média da Avaliação'] # Renomear colunas
    st.subheader("Média das Avaliações por Produto")
    st.dataframe(media_avaliacoes_produto_df.style.format({"Média da Avaliação": "{:.2f}"}))

    # Preencher o placeholder com a média de avaliação do produto selecionado
    with media_produto_placeholder.container():
        st.subheader(f"Média de Avaliação de {produto_selecionado}")
        media_produto_selecionado = dados[dados['Produto'] == produto_selecionado]['Avaliação da compra'].mean()
        st.write(f"A média de avaliação de {produto_selecionado} é: {media_produto_selecionado:.2f}")

    separator_placeholder_avaliacao.markdown("---")

    # Gráfico de Distribuição das Notas
    st.subheader("Gráfico de Distribuição das Notas")
    fig_distribuicao_notas, ax_distribuicao_notas = plt.subplots(figsize=(8, 4))
    distribuicao_notas.plot(kind='bar', ax=ax_distribuicao_notas, color='orange')
    ax_distribuicao_notas.set_title("Distribuição das Notas", fontsize=16)
    ax_distribuicao_notas.set_xlabel("Avaliação", fontsize=12) # Melhorando o label
    ax_distribuicao_notas.set_ylabel("Quantidade", fontsize=12)
    ax_distribuicao_notas.tick_params(axis='x', rotation=0)
    st.pyplot(fig_distribuicao_notas)