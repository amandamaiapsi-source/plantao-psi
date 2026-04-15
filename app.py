import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plantão PSI", layout="wide")

st.markdown("""<style>.stApp{background-color:#000}.main{color:#FFF}.logo{color:#8D6E63;font-size:30px;font-weight:bold}
.card{background-color:#0A0A0A;padding:10px;border-radius:8px;border-top:4px solid #4E342E;text-align:center;margin-bottom:5px}
.stButton>button{background-color:#4E342E;color:#FFF;font-size:11px}
textarea,input{background-color:#0A0A0A!important;color:#FFF!important;border:1px solid #4E342E!important}
.tag{font-size:10px;padding:2px 5px;border-radius:4px;margin:2px;display:inline-block;font-weight:bold;color:#FFF}
.tag-vm{background-color:#e74c3c}.tag-pal{background-color:#9b59b6}.tag-del{background-color:#f39c12}</style>""",unsafe_allow_html=True)

st.markdown('<p class="logo">PLANTÃO <span style="color:#FFF">PSI</span></p>',unsafe_allow_html=True)

if 'pcs' not in st.session_state:
    st.session_state.pcs = {str(i):{"nome":f"Leito {i}","id":"","h":"","e":"","c":"","vm":False,"de":False,"pa":False} for i in range(1,11)}

a1, a2 = st.tabs(["🗺️ MAPA", "🖨️ PASSAGEM"])

with a1:
    c = st.columns(5)
    for i in range(1, 11):
        l = str(i)
        p = st.session_state.pcs[l]
        with c[(i-1)%5]:
            ts = ""
            if p['vm']: ts += '<span class="tag tag-vm">VM</span>'
            if p['de']: ts += '<span class="tag tag-del">DEL</span>'
            if p['pa']: ts += '<span class="tag tag-pal">PAL</span>'
            st.markdown(f'<div class="card"><b style="color:#8D6E63">L{l}</b><br><small>{p["nome"]}</small><br>{ts}</div>',unsafe_allow_html=True)
            if st.button("ABRIR", key=f"b{l}"): st.session_state.f = l

    if 'f' in st.session_state:
        f = st.session_state.f
        st.divider()
        st.write(f"### Editando Leito {f}")
        st.session_state.pcs[f]['nome'] = st.text_input("Paciente", st.session_state.pcs[f]['nome'])
        m1,m2,m3 = st.columns(3)
        st.session_state.pcs[f]['vm'] = m1.checkbox("VM", st.session_state.pcs[f]['vm'])
        st.session_state.pcs[f]['de'] = m2.checkbox("Delirium", st.session_state.pcs[f]['de'])
        st.session_state.pcs[f]['pa'] = m3.checkbox("Paliativo", st.session_state.pcs[f]['pa'])
        st.session_state.pcs[f]['h'] = st.text_area("História", st.session_state.pcs[f]['h'])
        st.session_state.pcs[f]['e'] = st.text_area("Exame", st.session_state.pcs[f]['e'])
        st.session_state.pcs[f]['c'] = st.text_area("Conduta", st.session_state.pcs[f]['c'])
        if st.button("SALVAR"):
            del st.session_state.f
            st.rerun()

with a2:
    st.write("### Relatório")
    lp = []
    for k,v in st.session_state.pcs.items():
        if v['nome'] != f"Leito {k}":
            cl = []
            if v['vm']: cl.append("VM")
            if v['de']: cl.append("DEL")
            if v['pa']: cl.append("PAL")
            lp.append({"Leito":k,"Paciente":v['nome'],"Clin":", ".join(cl),"Exame":v['e'],"Conduta":v['c']})
    if lp: st.table(pd.DataFrame(lp))
    else: st.info("Vazio")
