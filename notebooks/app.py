# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# 1. Configuração Inicial e Carregamento de Dados
# ----------------------------------------------------

# Título principal do Dashboard
st.title('Dashboard de Análise de Anúncios de Venda de Carros')

# Cabeçalho para a seção de dados
st.header('Análise Exploratória do Conjunto de Dados de Veículos')

# Caminho para o seu arquivo CSV
# CERTIFIQUE-SE DE QUE ESTE NOME ESTÁ CORRETO E O ARQUIVO NO MESMO DIRETÓRIO!
CSV_PATH = 'vehicles.csv'

# Função para carregar os dados (com cache para otimização)


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Adicionando tratamento de dados conforme discutido anteriormente,
    # para garantir que os gráficos funcionem.
    # Ex: Criar a coluna 'manufacturer'
    df['manufacturer'] = df['model'].apply(lambda x: str(
        x).split(' ')[0] if pd.notna(x) else 'Unknown')
    df['manufacturer'] = df['manufacturer'].str.title()
    return df


# Carrega o DataFrame
car_data = load_data(CSV_PATH)

# Opcional: Mostrar as primeiras linhas do DataFrame para depuração
# st.write("Primeiras 5 linhas do dataset:")
# st.write(car_data.head())


# ----------------------------------------------------
# 2. Componentes Interativos para Geração de Gráficos
# ----------------------------------------------------

# Criar uma caixa de seleção para o Histograma de Odômetro
st.subheader('Visualize a Distribuição dos Dados')
build_odometer_histogram = st.checkbox('Criar Histograma de Quilometragem')

if build_odometer_histogram:  # Se a caixa de seleção for marcada
    st.write(
        'Criando um histograma para a distribuição da quilometragem dos veículos.')

    # É uma boa prática remover NaNs da coluna que você vai plotar
    # para evitar problemas ou para ter uma visualização mais precisa dos dados válidos.
    car_data_filtered_odometer = car_data.dropna(subset=['odometer']).copy()

    # Criar o histograma
    fig_hist = px.histogram(
        car_data_filtered_odometer,
        x="odometer",
        title="Distribuição da Quilometragem (Odômetro)",
        labels={
            "odometer": "Quilometragem (Odômetro)",
            "count": "Número de Veículos"
        },
        template="plotly_white",
        nbins=50  # Ajuste conforme a granularidade desejada
    )

    # Exibir o gráfico Plotly interativo
    st.plotly_chart(fig_hist, use_container_width=True)


# Criar uma caixa de seleção para o Gráfico de Dispersão (Preço vs. Odômetro)
build_scatter_price_odo = st.checkbox(
    'Criar Gráfico de Dispersão: Preço vs. Quilometragem')

if build_scatter_price_odo:  # Se a caixa de seleção for marcada
    st.write('Criando um gráfico de dispersão para analisar a relação entre preço e quilometragem, colorindo pela condição do veículo.')

    # É importante filtrar NaNs das colunas que serão usadas no gráfico
    car_data_filtered_price_odo = car_data.dropna(
        subset=['price', 'odometer', 'condition']).copy()

    # Criar o gráfico de dispersão
    fig_scatter = px.scatter(
        car_data_filtered_price_odo,
        x="odometer",
        y="price",
        color="condition",  # Adiciona a condição como cor
        title="Preço vs. Quilometragem (Odômetro) por Condição do Veículo",
        labels={
            "odometer": "Quilometragem (Odômetro)",
            "price": "Preço",
            "condition": "Condição do Veículo"
        },
        # Informações adicionais ao passar o mouse
        hover_data=['model_year', 'model'],
        template="plotly_white",
        opacity=0.7  # Transparência para pontos sobrepostos
    )

    # Exibir o gráfico Plotly interativo
    st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------------------------------------
# Fim do app.py
# ----------------------------------------------------
