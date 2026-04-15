import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plantão PSI - Amanda Maia", layout="wide")

# CSS: Visual Fundo Branco com detalhes Café
st.markdown("""<style>
    .stApp { background-color: white !important; color: black !important; }
    .main { color: black !important; }
    .logo { color: #4E342E; font-size: 30px; font-weight: bold; margin-bottom: 0px; }
    .card { 
        background-color: #Fdf5f2; padding: 10px; border-radius: 8px; 
        border: 1px solid #ddd; border-top: 5px solid #8D6E63; 
        text-align: center; margin-bottom: 5px; min-height: 100px;
    }
    /* Estilo dos inputs para fundo branco */
    textarea, input { background-color: white !important; color: black !important; border: 1px solid #8D6E63 !important; }
    .stButton>button { background-color: #8D6E63; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #4E342E; color: white; }
    
    /* Tags coloridas para os marcadores */
    .tag { font-size: 9px; padding: 2px 5px; border-radius: 4px; margin: 1px; display: inline-block; font-weight: bold; color: white; }
    .t-vm { background-color: #e74c3c; } .t-esp { background-color: #1abc9c; }
    .t-del { background-color: #f39c12; } .t-iso { background-color: #3498db; }
    .t-cp { background-color: #9b59b6; } .t-conf { background-color: #2ecc71; }
</style>""", unsafe_allow_html=True)

st.markdown('<p class="logo">PLANTÃO <span style="color:#8D6E63">PSI</span></p>', unsafe_allow_html=True)
st.markdown('<small style="color:#666">Gestão em Psicologia Hospitalar | Amanda Maia</small>', unsafe_allow_html=True)

# Estrutura exata das suas UTIs
unidades = {
    "UCV 1 (7 Leitos)": [str(i) for i in range(1, 8)],
    "UCV 2 (10 Leitos)": ["10", "11", "12", "13", "14", "15", "16", "17", "40", "41"],
    "UCV 3 (15 Leitos)": [str(i) for i in range(18, 33)],
    "UCV 4 (7 Leitos)": [str(i) for i in range(33, 40)]
}

if 'db' not in st.session_state:
    st.session_state.db = {l: {"n":"","h":"","c":"","vm":False,"es":False,"de":False,"is":False,"cp":False,"cf":False} for u in unidades.values() for l in u}

t1, t2 = st.tabs(["🏥 MAPA DE UNIDADES", "🖨️ RELATÓRIO DE PASSAGEM"])

with t1:
    unid_select = st.selectbox("Selecione a Unidade:", list(unidades.keys()))
    cols = st.columns(5)
    for idx, l in enumerate(unidades[unid_select]):
        p = st.session_state.db[l]
        with cols[idx % 5]:
            ts = ""
            if p['vm']: ts += '<span class="tag t-vm">VM</span>'
            if p['es']: ts += '<span class="tag t-esp">ESP</span>'
            if p['de']: ts += '<span class="tag t-del">DEL</span>'
            if p['is']: ts += '<span class="tag t-iso">ISO</span>'
            if p['cp']: ts += '<span class="tag t-cp">CP</span>'
            if p['cf']: ts += '<span class="tag t-conf">CONF</span>'
            
            st.markdown(f"""
                <div class="card">
                    <b style="color:#4E342E">LEITO {l}</b><br>
                    <small style="color:#333">{"<b>"+p['n']+"</b>" if p['n'] else "Vazio"}</small><br>
                    <div style="margin-top:5px">{ts}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"EDITAR L{l}", key=f"btn_{l}"):
                st.session_state.foco = l

    if 'foco' in st.session_state:
        f = st.session_state.f
