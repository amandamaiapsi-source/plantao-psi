import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plantão PSI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main { background-color: #000000 !important; color: #FFFFFF; }
    .logo-text { font-family: 'Helvetica', sans-serif; color: #8D6E63; font-size: 36px; font-weight: bold; }
    .logo-sub { color: #FFFFFF; font-size: 32px; font-weight: bold; }
    .patient-card { 
        background-color: #0A0A0A; padding: 15px; border-radius: 8px; border: 1px solid #333333;
        border-top: 4px solid #4E342E; text-align: center; margin-bottom: 5px; min-height: 140px;
    }
    .stButton>button { background-color: #4E342E; color: white; border: none; font-weight: bold; width: 100%; }
    textarea, input { background-color: #0A0A0A !important; color: white !important; border: 1px solid #4E342E !important; }
    .tag { font-size: 10px; padding: 2px 5px; border-radius: 4px; margin: 2px; display: inline-block; font-weight: bold; color: white; }
    .tag-vm { background-color: #e74c3c; } .tag-pal { background-color: #9b59b6; }
    .tag-del { background-color: #f39c12; } .tag-iso { background-color: #3498db; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="logo-text">PLANTÃO <span class="logo-sub">PSI</span></p>', unsafe_allow_html=True)

if 'pacientes' not in st.session_state:
    st.session_state.pacientes = {str(i): {
        "nome": f"Leito {i}", "idade": "", "hist": "", "exam": "", "cond": "",
        "vm": False, "del": False, "iso": False, "pal": False
    } for i in range(1, 11)}

aba_mapa, aba_pass = st.tabs(["🗺️ MAPA", "🖨️ PASSAGEM"])

with aba_mapa:
    cols = st.columns(5)
    for i in range(1, 11):
        l_id = str(i)
        p = st.session_state.pacientes[l_id]
        with cols[(i-1) % 5]:
            tags = ""
            if p['vm']: tags += '<span class="tag tag-vm">VM</span>'
            if p['del']: tags += '<span class="tag tag-del">DEL</span>'
            if p['pal']: tags += '<span class="tag tag-pal">PAL</span>'
            if p['iso']: tags += '<span class="tag tag-iso">ISO</span>'
            st.markdown(f'<div class="patient-card"><span style="color: #8D6E63; font-weight: bold;">LEITO {l_id}</span><br>{p["nome"]}<br><div>{tags}</div></div>', unsafe_allow_html=True)
            if st.button("ABRIR", key=f"b_{l_id}"):
                st.session_state.foco = l_id

    if 'foco' in st.session_state:
        f = st.session_state.foco
        p = st.session_state.pacientes[f]
        st.divider()
        c1, c2 = st.columns([3, 1])
        st.session_state.pacientes[f]['nome'] = c1.text_input("Nome", p['nome'], key=f"n_{f}")
        st.session_state.pacientes[f]['idade'] = c2.text_input("Idade", p['idade'], key=f"i_{f}")
        m1, m2, m3, m4 = st.columns(4)
        st.session_state.pacientes[f]['vm'] = m1.checkbox("VM", p['vm'], key=f"v_{f}")
        st.session_state.pacientes[f]['del'] = m2.checkbox("Delirium", p['del'], key=f"d_{f}")
        st.session_state.pacientes[f]['iso'] = m3.checkbox("Isolamento", p['iso'], key=f"s_{f}")
        st.session_state.pacientes[f]['pal'] = m4.checkbox("Paliativo", p['pal'], key=f"p_{f}")
        t1, t2, t3 = st.tabs(["HISTÓRIA", "EXAME", "CONDUTA"])
        st.session_state.pacientes[f]['hist'] = t1.text_area("História:", p['hist'], key=f"h_{f}")
        st.session_state.pacientes[f]['exam'] = t2.text_area("Exame:", p['exam'], key=f"e_{f}")
        st.session_state.pacientes[f]['cond'] = t3.text_area("Conduta:", p['cond'], key=f"c_{f}")
        if st.button("SALVAR"):
            del st.session_state.foco
            st.rerun()

with aba_pass:
