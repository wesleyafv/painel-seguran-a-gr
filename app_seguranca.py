import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Monitoramento GR")
st.title("🛡️ Central de Riscos Logísticos - Ocorrências Correlacionadas")
st.markdown("Exibindo ocorrências pré-filtradas no banco de dados (Intervalo máximo de 30 minutos).")

# -------------------------------------------------------------------------
# 1. CARGA DOS DADOS MASTIGADOS DO BANCO
# -------------------------------------------------------------------------
@st.cache_data
def carregar_dados_gr_prontos():
    # Lê o CSV gerado pela sua query SQL com os joins e filtros de tempo prontos
    df_original = pd.read_csv('perda_sinal.csv', sep=None, encoding='latin-1', engine='python')
    df_original.columns = df_original.columns.str.replace('"', '').str.strip()
    
    # Detector de variações de caixa de texto para o ID da viagem
    for col in df_original.columns:
        if 'VIAGEM' in col.upper() and 'ID' in col.upper():
            df_original = df_original.rename(columns={col: 'id_viagem'})
            break

    # Garante que as coordenadas sejam tratadas como números decimais purificados
    colunas_geo = ['latitude_sinal', 'longitude_sinal', 'latitude_panico', 'longitude_panico']
    for col in colunas_geo:
        if col in df_original.columns:
            df_original[col] = pd.to_numeric(df_original[col], errors='coerce')
            
    # Remove qualquer linha que tenha vindo com coordenada corrompida ou nula
    df_original = df_original.dropna(subset=['latitude_sinal', 'longitude_sinal'])
    
    return df_original

# Executa a leitura rápida
try:
    df_crise = carregar_dados_gr_prontos()
except FileNotFoundError:
    st.error("Erro: O arquivo `perda_sinal.csv` não foi encontrado na pasta atual.")
    st.stop()

# -------------------------------------------------------------------------
# 2. MÉTRICAS NA BARRA LATERAL (Sidebar)
# -------------------------------------------------------------------------
st.sidebar.header("Métricas do Painel")
if not df_crise.empty and 'id_viagem' in df_crise.columns:
    total_casos = len(df_crise['id_viagem'].unique())
else:
    total_casos = len(df_crise)

st.sidebar.metric(label="🚨 Viagens Alerta Máximo (30 min)", value=total_casos)

# -------------------------------------------------------------------------
# 3. RENDERIZAÇÃO DO MAPA GEOGRÁFICO
# -------------------------------------------------------------------------
st.subheader("🗺️ Mapa Espacial de Ocorrências e Áreas de Risco")

if not df_crise.empty:
    centro_lat = df_crise['latitude_sinal'].mean()
    centro_lon = df_crise['longitude_sinal'].mean()
    zoom_inicial = 6
else:
    centro_lat, centro_lon = -19.9245, -43.9352 # Centro em MG/RJ caso vazio
    zoom_inicial = 5

m = folium.Map(location=[centro_lat, centro_lon], zoom_start=zoom_inicial, tiles="OpenStreetMap")

if not df_crise.empty:
    # 📡 Camada 1: Mapa de Calor focado estritamente na Perda de Sinal
    coordenadas_calor = df_crise[['latitude_sinal', 'longitude_sinal']].values.tolist()
    HeatMap(coordenadas_calor, radius=22, blur=15, min_opacity=0.5, name="Zonas de Perda de Sinal").add_to(m)
    
    # 🚨 Camada 2: Clusters de Marcadores focados no acionamento do Botão de Pânico
    cluster_panico = MarkerCluster(name="Pontos de Pânico Relacionados").add_to(m)
    for _, linha in df_crise.iterrows():
        id_v = int(linha['id_viagem']) if 'id_viagem' in linha and pd.notna(linha['id_viagem']) else "N/I"
        minutos = linha['intervalo_minutos'] if 'intervalo_minutos' in linha else "N/I"
        evt_panico = linha['evento_panico'] if 'evento_panico' in linha else "Botão Pânico"
        
        folium.Marker(
            location=[linha['latitude_panico'], linha['longitude_panico']],
            popup=f"🚨 <b>ALERTA MÁXIMO GR</b><br>"
                  f"ID Viagem: {id_v}<br>"
                  f"Intervalo: {minutos} min<br>"
                  f"Regra: {evt_panico}",
            icon=folium.Icon(color='darkred', icon='remove-sign')
        ).add_to(cluster_panico)

# Ativa o painel de controle de camadas no canto superior direito do mapa
folium.LayerControl().add_to(m)

# Mostra o mapa na tela do Streamlit
st_folium(m, width="100%", height=650, key="mapa_gr_direto_sql")

# -------------------------------------------------------------------------
# 4. EXIBIÇÃO DA TABELA ANALÍTICA
# -------------------------------------------------------------------------
st.subheader("📋 Relatório Analítico de Viagens Alvo")
if not df_crise.empty:
    # Mostra na tabela exatamente a estrutura que a sua query SQL gera
    st.dataframe(df_crise, use_container_width=True)
else:
    st.info("Nenhum dado encontrado para exibição.")