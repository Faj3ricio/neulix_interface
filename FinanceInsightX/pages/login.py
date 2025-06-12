import streamlit as st
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

css_path = os.path.join(project_root, "assets", "login.css")
icon = os.path.join(project_root, "assets", "icon_green.svg")

st.set_page_config(page_title="Dashboard",page_icon=icon, layout="wide", initial_sidebar_state="collapsed")

# 1) Leitura do CSS
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="login-screen">
    <div class="geometric-bg">
        <div class="geometric-shape shape-1"></div>
        <div class="geometric-shape shape-2"></div>
        <div class="geometric-shape shape-3"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Container centralizado
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Botão X para fechar
    if st.button("✕", key="close_btn", help="Voltar"):
        st.switch_page("home.py")

    HERE = os.path.dirname(os.path.abspath(__file__))
    # sobe um nível (..), entra em assets e aponta pro SVG
    svg_path = os.path.join(HERE, os.pardir, "assets", "icon_wt.svg")

    # lê o SVG
    with open(svg_path, "r", encoding="utf-8")  as svg_file:
        icon_wt = svg_file.read()

    # Card de login
    with st.container():
        st.markdown(f"""
        <div class="login-container">
            <div class="login-logo">{icon_wt}</div>
            <div class="login-title">Finance</div>
            <div class="login-subtitle">Insight X</div>
            <div class="login-label">Login</div>
        </div>
        """, unsafe_allow_html=True)

        # Formulário
        email = st.text_input("", placeholder="Email", key="email")
        senha = st.text_input("", placeholder="Senha", type="password", key="senha")

        if st.button("Continue →", key="continue_btn", use_container_width=True):
            if email and senha:
                st.switch_page("pages/dashboards.py")
            else:
                st.error("Por favor, preencha todos os campos!")

