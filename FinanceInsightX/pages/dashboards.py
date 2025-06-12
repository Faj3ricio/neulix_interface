import streamlit as st
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

css_path = os.path.join(project_root, "assets", "dashboard.css")
icon = os.path.join(project_root, "assets", "icon_green.svg")

st.set_page_config(page_title="Dashboard", page_icon=icon, layout="wide", initial_sidebar_state="collapsed")

# 1) Leitura do CSS
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Remove elementos vazios do Streamlit
st.markdown("""
<script>
// Remove elementos vazios após carregamento
setTimeout(function() {
    const emptyDivs = document.querySelectorAll('div:empty');
    emptyDivs.forEach(div => {
        if (div.offsetHeight < 50 && div.offsetWidth > 200) {
            div.style.display = 'none';
        }
    });
}, 1000);
</script>
""", unsafe_allow_html=True)

HERE = os.path.dirname(os.path.abspath(__file__))
# sobe um nível (..), entra em assets e aponta pro SVG
svg_path = os.path.join(HERE, os.pardir, "assets", "icon_wt.svg")

# lê o SVG
with open(svg_path, "r", encoding="utf-8")  as svg_file:
    icon_wt = svg_file.read()

# Header principal
st.markdown(f"""
<div class="main-header">
    <div class="main-logo">
        <div class="dash-logo">{icon_wt}</div>
        <div>
            <div class="main-title">Finance</div>
            <div class="main-subtitle">Insight X</div>
        </div>
    </div>
    <div class="logout-container">
        <button class="logout-btn" onclick="window.location.reload()">✕ Sair</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Card principal do sistema
st.markdown("""
<div class="energy-card">
    <div class="energy-icon">⚡</div>
    <div class="energy-title">Sistema de Monitoramento<br>de Consumo de Energia</div>
    <div class="energy-subtitle">Dashboard em Tempo Real</div>
</div>
""", unsafe_allow_html=True)

# Métricas principais
st.markdown('<div class="metrics-section">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-value">1.2 kW</div>
        <div class="metric-label">Consumo Atual</div>
        <div class="metric-change positive">↑ 5%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">💰</div>
        <div class="metric-value">R$ 15,30</div>
        <div class="metric-label">Economia Hoje</div>
        <div class="metric-change negative">↓ 2%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-value">87%</div>
        <div class="metric-label">Eficiência</div>
        <div class="metric-change positive">↑ 3%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">✅</div>
        <div class="metric-value">Normal</div>
        <div class="metric-label">Status</div>
        <div class="metric-change neutral">Online</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Seção de gráficos
st.markdown('<div class="charts-section">', unsafe_allow_html=True)

# Gráfico 1: Consumo de Energia ao longo do tempo
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Dados exemplo para consumo de energia
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    consumption = np.random.normal(100, 20, 30).cumsum()

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=dates,
        y=consumption,
        mode='lines+markers',
        name='Consumo de Energia',
        line=dict(color='#baa03b', width=4),
        marker=dict(color='#2c3e20', size=8),
        fill='tozeroy',
        fillcolor='rgba(244, 208, 63, 0.1)'
    ))

    fig1.update_layout(
        title={
            'text': "Consumo de Energia - Últimos 30 dias",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#f4f4f4', 'family': 'Arial Black'}
        },
        xaxis_title="Data",
        yaxis_title="Consumo (kWh)",
        template="plotly_white",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    fig1.update_xaxes(gridcolor='rgba(44, 62, 32, 0.1)')
    fig1.update_yaxes(gridcolor='rgba(44, 62, 32, 0.1)')

    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Gráfico 2: Distribuição de Consumo por Período
    periods = ['Manhã', 'Tarde', 'Noite', 'Madrugada']
    consumption_by_period = [25, 35, 30, 10]
    colors = ['#f4d03f', '#2c3e20', '#f7dc6f', '#3a4a2a']

    fig2 = go.Figure(data=[go.Pie(
        labels=periods,
        values=consumption_by_period,
        hole=.4,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=3))
    )])

    fig2.update_layout(
        title={
            'text': "Consumo por Período do Dia",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#f4f4f4', 'family': 'Arial Black'}
        },
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Terceiro gráfico: Comparação Mensal
st.markdown('<div class="chart-container full-width">', unsafe_allow_html=True)

months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
current_year = [120, 135, 110, 145, 130, 125]
previous_year = [140, 150, 125, 160, 145, 135]

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    name='2024',
    x=months,
    y=current_year,
    marker_color='#f4d03f',
    marker_line=dict(color='#2c3e20', width=2)
))

fig3.add_trace(go.Bar(
    name='2023',
    x=months,
    y=previous_year,
    marker_color='#2c3e20',
    marker_line=dict(color='#f4d03f', width=2)
))

fig3.update_layout(
    title={
        'text': "Comparativo de Consumo Mensal - 2023 vs 2024",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#f4f4f4', 'family': 'Arial Black'}
    },
    xaxis_title="Mês",
    yaxis_title="Consumo (kWh)",
    barmode='group',
    template="plotly_white",
    height=450,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=40, r=40, t=80, b=40)
)

fig3.update_xaxes(gridcolor='rgba(44, 62, 32, 0.1)')
fig3.update_yaxes(gridcolor='rgba(44, 62, 32, 0.1)')

st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Quarto gráfico: Eficiência Energética
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Gráfico de gauge para eficiência
    fig4 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=87,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': 80},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#f4d03f"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"}],
            'threshold': {
                'line': {'color': "#2c3e20", 'width': 4},
                'thickness': 0.75,
                'value': 90}}
    ))

    fig4.update_layout(
        title={
            'text': "Indicador de Eficiência (%)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#f4f4f4', 'family': 'Arial Black'}
        },
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Gráfico de economia em R$
    days = list(range(1, 31))
    savings = np.cumsum(np.random.normal(0.5, 0.2, 30))

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=days,
        y=savings,
        mode='lines+markers',
        name='Economia Acumulada',
        line=dict(color='#2c3e20', width=4),
        marker=dict(color='#f4d03f', size=8, line=dict(color='#2c3e20', width=2)),
        fill='tozeroy',
        fillcolor='rgba(44, 62, 32, 0.1)'
    ))

    fig5.update_layout(
        title={
            'text': "Economia Acumulada (R$)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#f4f4f4', 'family': 'Arial Black'}
        },
        xaxis_title="Dia do Mês",
        yaxis_title="Economia (R$)",
        template="plotly_white",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    fig5.update_xaxes(gridcolor='rgba(44, 62, 32, 0.1)')
    fig5.update_yaxes(gridcolor='rgba(44, 62, 32, 0.1)')

    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Botão para voltar ao início
st.markdown('<div class="bottom-section">', unsafe_allow_html=True)
if st.button("Voltar ao início", key="home_btn", use_container_width=False):
    st.switch_page("home.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)