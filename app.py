import streamlit as st
import pandas as pd

# Configuração da página - Fundo Escuro
st.set_page_config(page_title="Plantão PSI", layout="wide")

# CSS para o visual TOTAL BLACK + MARROM CAFÉ
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main { background-color: #000000 !important; color: #FFFFFF; }
    .logo-text { font-family: 'Helvetica', sans-serif; color: #8D6E63; font-size: 36px; font-weight: bold; letter-spacing: 2px; }
    .logo-sub { color: #FFFFFF; font-size: 32px; font-weight: bold; }
    .patient-card { 
        background-color: #0A0A0A; padding: 15px; border-radius: 8px; border: 1px solid #333333;
        border-top: 4px solid #4E342E; margin-bottom: 15px; text-align: center;
    }
    .stButton>button { background-color: #4E342E; color: white; border: none; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #6D4C41; color: white; }
    textarea { background-color: #0A0A0A !important; color: white !important; border: 1px solid #4E342E !important; }
    input { background-color: #0A0A0A !important; color: white !important; border: 1px solid #4E342E !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="logo-text">PLANTÃO <span class="logo-sub">PSI</span></p>', unsafe_allow_html=True)
st.markdown('<p style="color: #8D6E63; font-style: italic;">Gestão em Psicologia Hospitalar</p>', unsafe_allow_html=True)

if 'pacientes' not in st.session_state:
    st.session_state.pacientes = [
        {"leito": str(i), "nome": f"Leito {i}", "idade": "--", "historia": "", "exame": "", "conduta": ""} 
        for i in range(1, 11)
    ]

cols = st.columns(5)
for idx, p in enumerate(st.session_state.pacientes):
    with cols[idx % 5]:
        st.markdown(f'<div class="patient-card"><span style="color: #8D6E63; font-weight: bold;">LEITO {p["leito"]}</span><br><span style="font-size: 14px; color: #FFFFFF;">{p["nome"]}</span></div>', unsafe_allow_html=True)
        if st.button(f"VER FICHA", key=f"btn_{idx}"):
            st.session_state.selecionado = idx

if 'selecionado' in st.session_state:
    idx = st.session_state.selecionado
    p = st.session_state.pacientes[idx]
    st.divider()
    st.markdown(f"### 📝 Ficha de Evolução: {p['nome']} (Leito {p['leito']})")
    col_id1, col_id2 = st.columns([3, 1])
    with col_id1:
        st.session_state.pacientes[idx]['nome'] = st.text_input("Nome Completo", p['nome'])
    with col_id2:
        st.session_state.pacientes[idx]['idade'] = st.text_input("Idade", p['idade'])
    tab1, tab2, tab3 = st.tabs(["HISTÓRIA / ADMISSÃO", "AVALIAÇÃO PSÍQUICA", "CONDUTAS E MANEJO"])
    with tab1:
        st.session_state.pacientes[idx]['historia'] = st.text_area("Histórico:", p['historia'], height=200)
    with tab2:
        st.session_state.pacientes[idx]['exame'] = st.text_area("Exame Psíquico:", p['exame'], height=200)
    with tab3:
        st.session_state.pacientes[idx]['conduta'] = st.text_area("Condutas:", p['conduta'], height=200)
    if st.button("💾 SALVAR"):
        st.success("Salvo!")

st.divider()
if st.button("🖨️ GERAR MAPA PARA IMPRESSÃO"):
    st.write("### Passagem de Plantão - Psicologia")
    df = pd.DataFrame(st.session_state.pacientes)
    st.table(df[['leito', 'nome', 'historia', 'exame', 'conduta']])
