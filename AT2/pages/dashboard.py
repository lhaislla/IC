import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard INEP", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def carregar_dados():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_excel = os.path.join(diretorio_atual, "..", "data", "INDIC_BRASIL_2010_2024.xlsx")
    
    colunas_padrao = [
        'Ano_Fluxo', 'Total', 'Feminino', 'Masculino', 'Amarela', 'Branca',
        'Indigena', 'Parda', 'Preta', 'Etnia_Sem_Decl', 'Idade_Ate_19', 'Idade_20_22',
        'Idade_23_24', 'Idade_25_29', 'Idade_30_39', 'Idade_40_49', 'Idade_50_mais', 
        'Def_Sim', 'Def_Nao'
    ]
    
    datasets = {'Evasão': 'TX_EVASAO', 'Conclusão': 'TX_CONCLUSAO', 
                'Retenção': 'TX_RETENCAO', 'Permanência': 'TX_PERMANENCIA'}
    
    lista_final = []
    for nome_finalidade, aba in datasets.items():
        df = pd.read_excel(caminho_excel, sheet_name=aba, skiprows=7, header=None)
        df = df.iloc[:, :len(colunas_padrao)]
        df.columns = colunas_padrao
        df = df[df['Ano_Fluxo'].astype(str).str.contains('-', na=False)].copy()
        cols_num = colunas_padrao[1:]
        df[cols_num] = df[cols_num].apply(pd.to_numeric, errors='coerce')
        df['Finalidade'] = nome_finalidade
        lista_final.append(df)
        
    return pd.concat(lista_final, ignore_index=True)


def gerar_grafico_genero(df, indicador):
    df_plot = df[
        (df['Finalidade'] == indicador) & 
        (df['Ano_Fluxo'].str.contains('20', na=False))
    ].copy()

    fig = px.line(
        df_plot, 
        x='Ano_Fluxo', 
        y=['Feminino', 'Masculino'],
        markers=True,

        color_discrete_map={
            'Feminino': 'green', 
            'Masculino': 'blue'
        },
        title=f"Evolução da Taxa de {indicador} por Gênero",
        labels={
            'value': f'Taxa de {indicador} (%)', 
            'variable': 'Gênero',
            'Ano_Fluxo': 'Ano Fluxo' 
        }
    )
    
    fig.update_yaxes(tickformat=".2f", ticksuffix="%", range=[0, 100])
    
    fig.update_layout(
        xaxis_title="Ano Fluxo", 
        legend_title_text='Gênero',
        margin=dict(l=50, r=50, t=80, b=50),
        template="plotly_white"
    )
    
    return st.plotly_chart(fig, use_container_width=True)

def gerar_grafico_etnia(df, indicador):
    df_filtrado = df[
        (df['Finalidade'] == indicador) & 
        (df['Ano_Fluxo'].str.contains('20', na=False))
    ].copy()

    colunas_raca = ['Amarela', 'Branca', 'Indigena', 'Parda', 'Preta']
    df_long = df_filtrado.melt(
        id_vars=['Ano_Fluxo'], 
        value_vars=colunas_raca,
        var_name='Etnia', 
        value_name='Taxa'
    )

    fig = px.bar(
        df_long, 
        x='Ano_Fluxo', 
        y='Taxa',
        color='Etnia',
        barmode='group',
        title=f"Comparativo da Taxa de {indicador} por Etnia",
        labels={
            'Taxa': f'Taxa de {indicador} (%)', 
            'Ano_Fluxo': 'Ano Fluxo',
            'Etnia': 'Etnia' 
        }
    )
    fig.update_yaxes(tickformat=".2f", ticksuffix="%", range=[0, 100])
    fig.update_layout(
        xaxis_title="Ano Fluxo", yaxis_title=f"Taxa de {indicador} (%)",
        legend_title_text='Etnia', template="plotly_white",
        margin=dict(l=50, r=50, t=80, b=50)
    )
    return st.plotly_chart(fig, use_container_width=True)

def gerar_dispersao_etnia_ano(df, indicador):
    df_filtrado = df[
        (df['Finalidade'] == indicador) & 
        (df['Ano_Fluxo'].str.contains('20', na=False))
    ].copy()

    colunas_raca = ['Amarela', 'Branca', 'Indigena', 'Parda', 'Preta']
    df_long = df_filtrado.melt(
        id_vars=['Ano_Fluxo'], 
        value_vars=colunas_raca,
        var_name='Etnia', 
        value_name='Taxa'
    )

    fig = px.scatter(
        df_long, 
        x='Ano_Fluxo', 
        y='Taxa',      
        color='Etnia', 
        size='Taxa',
        title=f"Dispersão Étnica da Taxa de {indicador} - Série Histórica",
        labels={
            'Taxa': f"Taxa de {indicador} (%)", 
            'Ano_Fluxo': 'Ano Fluxo',
            'Etnia': 'Etnia' 
        }
    )
    fig.update_traces(
        hovertemplate="Ano: %{x}<br>Etnia: %{fullData.name}<br>Taxa: %{y:.2f}%",
        marker=dict(size=14, line=dict(width=1, color='DarkSlateGrey'))
    )
    fig.update_yaxes(tickformat=".2f", ticksuffix="%", range=[0, 100])
    fig.update_layout(
        template="plotly_white", xaxis_title="Ano Fluxo",
        yaxis_title=f"Taxa de {indicador} (%)",
        margin=dict(l=50, r=50, t=80, b=50), hovermode="closest"
    )
    return st.plotly_chart(fig, use_container_width=True)


df_br = carregar_dados()
st.title("📊 Indicadores de Fluxo da Educação Superior")
col1, col2 = st.columns([1, 1])

with col1:
    indicador_selecionado = st.selectbox(
        "Indicador:",
        ['Conclusão', 'Evasão', 'Retenção', 'Permanência']
    )

with col2:
    lista_anos = sorted(df_br['Ano_Fluxo'].unique())
    anos_selecionados = st.multiselect(
        "Ano do Fluxo:",
        options=lista_anos,
        default=lista_anos
    )

df_filtrado_ano = df_br[df_br['Ano_Fluxo'].isin(anos_selecionados)]

if not anos_selecionados:
    st.warning("Selecione ao menos um ano para gerar os gráficos.")
else:
    st.write("---")
    gerar_grafico_genero(df_filtrado_ano, indicador_selecionado)

    st.write("---")
    gerar_grafico_etnia(df_filtrado_ano, indicador_selecionado)

    st.write("---")
    gerar_dispersao_etnia_ano(df_filtrado_ano, indicador_selecionado)