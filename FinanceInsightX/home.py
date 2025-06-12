import streamlit as st

st.set_page_config(
    page_title="Finance Insight X",
    page_icon="assets/icon_green.svg",
    layout="wide",
)

# 1) Carrega o CSS
with open("assets/home.css", "r", encoding="utf-8") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# 2) Carrega o SVG inline
with open("assets/icon_wt.svg", "r", encoding="utf-8") as svg_file:
    icon_wt = svg_file.read()

# 3) Mostra a tela splash com o botão HTML
st.markdown(f"""
<div class="splash-screen">
    <div class="splash-logo">{icon_wt}</div>
    <div class="splash-title">Finance</div>
    <div class="splash-subtitle">Insight X</div>
    <div class="splash-description">
        Sistema de Monitoramento de<br>Consumo de Energia
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("Entrar", key="login_btn", use_container_width=True):
    st.switch_page("pages/login.py")
