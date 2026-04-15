import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plantão PSI", layout="wide")

# CSS: Preto no uso, Branco na impressão
st.markdown("""<style>
@media screen {
    .stApp{background-color:#000}.main{color:#FFF}
    .card{background-color:#0A0A0A;padding:10px;border-radius:8px;border-top:4px solid #4E342E;text-align:center;margin-bottom:5px;min-height:100px}
    textarea,input{background-color:#0A0A0A!important;color:#FFF!important;border:1px solid #4E342E!important}
}
@media print {
    .stApp, .main, body { background-color: white !important; color: black !important; }
    .stTabs, button, hr, .stMarkdown:has(p.logo) { display: none !important; }
    table { color: black !important; border: 1px solid black !important; }
}
.logo{color:#8D6E63;font-size:30px;font-weight:bold}
.tag{font-size:9px;padding:2px 4px;border-radius:4px;margin:1px;display:inline-block;font-weight:bold;color:#FFF}
.t-vm{background-color:#e74c3c}.t-pal{background-color:#9b59b6}.t-del{background-color:#f39c12}.t-iso{background-color:#3498db}.t-conf{background-color:#2ecc71}.t-esp{background-color:#1abc9c}
</style>""",unsafe_allow_html=True)

st.markdown('<p class="logo">PLANTÃO <span style="color:#FFF">PSI</span></p>',unsafe_allow_html=True)

unidades = {
    "UCV 1": ["1","2","3","4","5","6","7"],
    "UCV 2": ["10","11","12","13","14","15","16","17","40","41"],
    "UCV 3 (Interconsulta)": ["IC 1","IC 2","IC 3","IC 4","IC 5"],
    "UCV 4 (Interconsulta)": ["IC 6","IC 7","IC 8","IC 9","IC 10"]
}

if 'db' not in st.session_state:
    st.session_state.db = {l: {"n":"","h":"","c":"","vm":False,"es":False,"de":False,"is":False,"cp":False,"cf":False} for u in unidades.values() for l in u}

t1, t2 = st.tabs(["🏥 UNIDADES", "🖨️ PASSAGEM"])

with t1:
    unid = st.selectbox("UTI:", list(unidades.keys()))
    cols = st.columns(5)
    for idx, l in enumerate(unidades[unid]):
        p = st.session_state.db[l]
        with cols[idx % 5]:
            ts = "".join([f'<span class="tag t-{k}">{v}</span>' for k,v,cond in [('vm','VM',p['vm']),('esp','ESP',p['es']),('del','DEL',p['de']),('iso','ISO',p['is']),('pal','CP',p['cp']),('conf','CONF',p['cf'])] if cond])
            st.markdown(f'<div class="card"><b style="color:#8D6E63">L{l}</b><br><small>{p["n"] if p["n"] else "Vazio"}</small><br>{ts}</div>',unsafe_allow_html=True)
            if st.button("ABRIR", key=f"b{l}"): st.session_state.f = l
    if 'f' in st.session_state:
        f = st.session_state.f
        st.divider()
        st.session_state.db[f]['n'] = st.text_input("Paciente", st.session_state.db[f]['n'])
        m = st.columns(6)
        st.session_state.db[f]['vm']=m[0].checkbox("VM",p['vm'],key=f'vm{f}')
        st.session_state.db[f]['es']=m[1].checkbox("ESP",p['es'],key=f'es{f}')
        st.session_state.db[f]['de']=m[2].checkbox("DEL",p['de'],key=f'de{f}')
        st.session_state.db[f]['is']=m[3].checkbox("ISO",p['is'],key=f'is{f}')
        st.session_state.db[f]['cp']=m[4].checkbox("CP",p['cp'],key=f'cp{f}')
        st.session_state.db[f]['cf']=m[5].checkbox("CONF",p['cf'],key=f'cf{f}')
        st.session_state.db[f]['h'] = st.text_area("História Médica", st.session_state.db[f]['h'])
        st.session_state.db[f]['c'] = st.text_area("Conduta PSI", st.session_state.db[f]['c'])
        if st.button("SALVAR"):
            del st.session_state.f
            st.rerun()

with t2:
    lp = [{"Leito":k,"Paciente":v['n'],"Clinica":", ".join([n for c,n in [('vm','VM'),('es','ESP'),('de','DEL'),('is','ISO'),('cp','CP'),('cf','CONF')] if v[c]]),"História":v['h'],"Conduta":v['c']} for k,v in st.session_state.db.items() if v['n']]
    if lp: st.table(pd.DataFrame(lp))
    else: st.info("Vazio")
