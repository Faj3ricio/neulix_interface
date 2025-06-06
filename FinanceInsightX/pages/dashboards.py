import streamlit as st
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

css_path = os.path.join(project_root, "assets", "home.css")
icon = os.path.join(project_root, "assets", "icon_bl.svg")

st.set_page_config(page_title="Dashboard",page_icon=icon, layout="wide", initial_sidebar_state="collapsed")

# 1) Leitura do CSS
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <div class="main-logo">
        <span style="font-size: 2rem;">🌱</span>
        <div>
            <div class="main-title">Finance</div>
            <div class="main-subtitle">Insight X</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Botão de logout no canto superior direito
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    if st.button("✕ Sair", key="logout_btn"):
        st.switch_page("home.py")

# Card principal do sistema
st.markdown("""
<div class="energy-card">
    <div class="energy-title">Sistema de<br>monitoramento de<br>Consumo de Energia</div>
</div>
""", unsafe_allow_html=True)

# Conteúdo do dashboard

# Exemplo de métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Consumo Atual", "1.2 kW", "↑ 5%")
with col2:
    st.metric("Economia Hoje", "R$ 15,30", "↓ 2%")
with col3:
    st.metric("Eficiência", "87%", "↑ 3%")
with col4:
    st.metric("Status", "Normal", "✅")

# Gráfico exemplo
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Dados exemplo
dates = pd.date_range('2024-01-01', periods=30, freq='D')
consumption = np.random.normal(100, 20, 30).cumsum()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=consumption,
    mode='lines+markers',
    name='Consumo de Energia',
    line=dict(color='#f4d03f', width=3),
    marker=dict(color='#2c3e20', size=6)
))

fig.update_layout(
    title="Consumo de Energia - Últimos 30 dias",
    xaxis_title="Data",
    yaxis_title="Consumo (kWh)",
    template="plotly_white",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Botão para voltar ao início
if st.button("🔄 Voltar ao início", key="home_btn", use_container_width=True):
    st.switch_page("home.py")