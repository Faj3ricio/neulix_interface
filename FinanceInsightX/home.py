import streamlit as st

st.set_page_config(
    page_title="Finance Insight X",
    page_icon="assets/icon_green.svg",
    layout="wide",
)

# Leitura do CSS
with open("assets/base.css", "r", encoding="utf-8") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="splash-screen">
    <div class="splash-logo">🌱</div>
    <div class="splash-title">Finance</div>
    <div class="splash-subtitle">Insight X</div>
    <div class="splash-description">Sistema de Monitoramento de<br>Consumo de Energia</div>

    <!-- Button -->
    <button class="splash-button" id="entrar-btn" onclick="handleEntrarClick()">
        Entrar
    </button>
</div>

<script>
function handleEntrarClick() {
    const streamlitButton = window.parent.document.querySelector('[data-testid="baseButton-primary"]');
    if (streamlitButton) {
        streamlitButton.click();
    } else {
        const buttons = window.parent.document.querySelectorAll('button');
        for (let btn of buttons) {
            if (btn.textContent.includes('Entrar')) {
                btn.click();
                break;
            }
        }
    }
}
</script>
""", unsafe_allow_html=True)

# Botão invisível do Streamlit que controla a navegação real
# Este botão é escondido pelo CSS mas ainda funciona para navegação
if st.button("Entrar", key="enter_btn", type="primary"):
    st.switch_page("pages/login.py")