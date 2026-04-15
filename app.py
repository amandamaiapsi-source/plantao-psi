import streamlit as st
import pandas as pd

# Configuração da página - Fundo Escuro
st.set_page_config(page_title="Plantão PSI", layout="wide")

# CSS para o visual TOTAL BLACK + MARROM CAFÉ
st.markdown("""
    <style>
    /* Fundo Totalmente Preto */
    .stApp { background-color: #000000 !important; }
    .main { background-color: #000000 !important; color: #FFFFFF; }
    
    /* Título: PLANTÃO PSI */
    .logo-text {
        font-family: 'Helvetica', sans-serif;
        color: #8D6E63; /* Marrom Café */
        font-size: 36px;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }
    .logo-sub { color: #FFFFFF; font-size: 32px; font-weight: bold; }

    /* Cards dos Leitos - Preto com borda marrom */
    .patient-card { 
        background-color: #0A0A0A; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid #333333;
        border-top: 4px solid #4E342E;
        margin-bottom: 15px;
        text-align: center;
    }
    
    /* Botões em Marrom Café */
    .stButton>button {
        background-color: #4E342E;
        color: white;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #6D4C41;
        border: none;
        color: white;
    }
    
    /* Inputs e Áreas de texto - Escuros para não brilhar na UTI */
    textarea { background-color: #0A0A0A !important; color: white !important; border: 1px solid #4E342E !important; }
    input { background-color: #0A0A0A !important; color: white !important; border: 1px solid #4E342E !important; }
    
    /* Cor das abas */
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF; }
    .stTabs [aria-selected="true"] { color: #8D6E63 !important; border-bottom-color: #8D6E63 !important; }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho
st.markdown('<p class="logo-text">PLANTÃO <span class="logo-sub">PSI</span></p>', unsafe_allow_html=True)
st.markdown('<p style="color: #8D6E63; font-style: italic;">Gestão em Psicologia Hospitalar</p>', unsafe_allow_html=True)

# Banco de dados temporário
if 'pacientes' not in st.session_state:
    st.session_state.pacientes = [
        {"leito": str(i), "nome": f"Leito {i}", "idade": "--", "historia": "", "exame": "", "conduta": ""} 
        for i in range(1, 11)
    ]

# Grid de Leitos
cols = st.columns(5)
for idx, p in enumerate(st.session_state.pacientes):
    with cols[idx % 5]:
        st.markdown(f"""
        <div class="patient-card">
            <span style="color: #8D6E6
