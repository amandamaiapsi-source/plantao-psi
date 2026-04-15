import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plantão PSI - Amanda Maia", layout="wide")

# CSS Estilo Café & Black
st.markdown("""<style>.stApp{background-color:#000}.main{color:#FFF}.logo{color:#8D6E63;font-size:30px;font-weight:bold}
.card{background-color:#0A0A0A;padding:10px;border-radius:8px;border-top:4px solid #4E342E;text-align:center;margin-bottom:5px;min-height:100px}
.stButton>button{background-color:#4E342E;color:#FFF;font-size:11px}
textarea,input{background-color:#0A0A0A!important;color:#FFF!important;border:1px solid #4E342E!important}
.tag{font-size:9px;padding:2px 4px;border-radius:4px;margin:1px;display:inline-block;font-weight:bold;color:#FFF}
.t-vm{background-color:#e74c3c}.t-pal{background-color:#9b59b6}.t-del{background-color:#f39c12}.t-iso{background-color:#3498db}.t-conf{background-color:#2ecc71}.t-esp{background-color:#1abc9c}</style>""",unsafe_allow_html=True)

st.markdown('<p class="logo">PLANTÃO <span style="color:#FFF">PSI</span></p>',unsafe_allow_html=True)

# Definição das Unidades
unidades = {
    "UCV 1": ["1","2","3","4","5","6","7"],
    "UCV 2": ["10","11","12","13","14","15","16","17","40","41"],
    "UCV 3 (Interconsulta)": ["IC 1","IC 2","IC 3","IC 4","IC 5"],
    "UCV 4 (Interconsulta)": ["IC 6","IC 7","IC 8","IC 9","IC 10"]
}

if 'db' not in st.session_state:
    st.session_state.db = {}
    for unidade in unidades.values():
        for l in unidade:
            st.session_state.db[l] = {"n":"","h":"","c":"","vm":False,"es":False,"de":False,"is":False,"cp":False,"cf":False}

tab_unid, tab_pass = st.tabs(["🏥 UNIDADES", "🖨️ PASSAGEM GERAL"])

with tab_unid:
    unid_select = st.selectbox("Selecione a UTI:", list(unidades.keys()))
    cols = st.columns(5)
    for idx, l in enumerate(unidades[unid_select]):
        p = st.session_state.db[l]
        with cols[idx % 5]:
            ts = ""
            if p['vm']: ts += '<span class="tag t-vm">VM</span>'
            if p['es']: ts += '<span class="tag t-esp">ESP</span>'
            if p['de']: ts += '<span class="tag t-del">DEL</span>'
            if p['is']: ts += '<span class="tag t-iso">ISO</span>'
            if p['cp']: ts += '<span class="tag t-pal">CP</span>'
            if p['cf']: ts += '<span class="tag t-conf">CONF</span>'
            st.markdown(f'<div class="card"><b style="color:#8D6E63">LEITO {l}</b><br><small>{p["n"] if p["n"] else "Vazio"}</small><br>{ts}</div>',unsafe_allow_html=True)
            if st.button("ABRIR", key=f"b{l}"): st.session_state.f = l

    if 'f' in st.session_state:
        f = st.session_state.f
        st.divider()
        st.write(f"### 📝 Editando Leito {f} ({unid_select})")
        st.session_state.db[f]['n'] = st.text_input("Nome do Paciente", st.session_state.db[f]['n'])
        
        st.write("**Marcadores Clínicos:**")
        m1,m2,m3,m4,m5,m6 = st.columns(6)
        st.session_state.db[f]['vm'] = m1.checkbox("VM", st.session_state.db[f]['vm'], key=f"vm{f}")
        st.session_state.db[f]['es'] = m2.checkbox("V. Espontânea", st.session_state.db[f]['es'], key=f"es{f}")
        st.session_state.db[f]['de'] = m3.checkbox("Delirium", st.session_state.db[f]['de'], key=f"de{f}")
        st.session_state.db[f]['is'] = m4.checkbox("Isolamento", st.session_state.db[f]['is'], key=f"is{f}")
        st.session_state.db[f]['cp'] = m5.checkbox("C. Paliativos", st.session_state.db[f]['cp'], key=f"cp{f}")
        st.session_state.db[f]['cf'] = m6.checkbox("Conferência", st.session_state.db[f]['cf'], key=f"cf{f}")
        
        st.session_state.db[f]['h'] = st.text_area("História Médica / Problemas (Copiar do Prontuário):", st.session_state.db[f]['h'], height=150)
        st.session_state.db[f]['c'] = st.text_area("Conduta Psicológica / Manejo:", st.session_state.db[f]['c'], height=150)
        
        if st.button("💾 SALVAR E VOLTAR"):
            del st.session_state.f
            st.rerun()

with tab_pass:
    st.write("### 📋 Relatório de Passagem de Plantão")
    lp = []
    for k,v in st.session_state.db.items():
        if v['n'] != "":
            cl = []
            if v['vm']: cl.append("VM")
            if v['es']: cl.append("V.ESP")
            if v['de']: cl.append("DELIRIUM")
            if v['is']: cl.append("ISO")
            if v['cp']: cl.append("CP")
            if v['cf']: cl.append("CONF")
            lp.append({"Leito":k, "Paciente":v['n'], "Clínica":", ".join(cl), "História/Problemas":v['h'], "Conduta PSI":v['c']})
    if lp: st.table(pd.DataFrame(lp))
    else: st.info("Nenhum paciente cadastrado nas UTIs.")
