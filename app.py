import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Plantão PSI", layout="wide")

# CSS para visual PROFISSIONAL TOTAL BLACK
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main { background-color: #000000 !important; color: #FFFFFF; }
    .logo-text { font-family: 'Helvetica', sans-serif; color: #8D6E63; font-size: 36px; font-weight: bold; letter-spacing: 2px; }
    .logo-sub { color: #FFFFFF; font-size: 32px; font-weight: bold; }
    .patient-card { 
        background-color: #0A0A0A; padding: 15px; border-radius: 8px; border: 1px solid #333333;
        border-top: 4px solid #4E342E; text-align: center; margin-bottom: 5px; min-height: 140px;
    }
    .stButton>button { background-color: #4E342E; color: white; border: none; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #6D4C41; color: white; }
    textarea, input { background-color: #0A0A0A !important; color: white !important; border: 1px solid #4E342E !important; }
    .tag { font-size: 10px; padding: 2px 5px; border-radius: 4px; margin: 2px; display: inline-block; font-weight: bold; color: white; }
    .tag-vm { background-color: #e74c3c; }
    .tag-pal { background-color: #9b59b6; }
    .tag-del { background-color: #f39c12; }
    .tag-iso { background-color: #3498db; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="logo-text">PLANTÃO <span class="logo-sub">PSI</span></p>', unsafe_allow_html=True)

# Inicialização de dados (Limpa e sem mostrar código bruto)
if 'pacientes' not in st.session_state:
    st.session_state.pacientes = {str(i): {
        "nome": f"Leito {i}", "idade": "", "historia": "", "exame": "", "conduta": "",
        "vm": False, "delirium": False, "isolamento": False, "paliativo": False, "alta": False
    } for i in range(1, 11)}

aba_mapa, aba_passagem = st.tabs(["🗺️ MAPA DE LEITOS", "🖨️ GERAR PASSAGEM"])

with aba_mapa:
    cols = st.columns(5)
    for i in range(1, 11):
        l_id = str(i)
        p = st.session_state.pacientes[l_id]
        with cols[(i-1) % 5]:
            tags_html = ""
            if p['vm']: tags_html += '<span class="tag tag-vm">VM</span>'
            if p['delirium']: tags_html += '<span class="tag tag-del">DEL</span>'
            if p['paliativo']: tags_html += '<span class="tag tag-pal">PAL</span>'
            if p['isolamento']: tags_html += '<span class="tag tag-iso">ISO</span>'
            
            st.markdown(f'<div class="patient-card"><span style="color: #8D6E63; font-weight: bold;">LEITO {l_id}</span><br><span style="font-size: 13px; font-weight: bold;">{p["nome"]}</span><br><div style="margin-top: 5px;">{tags_html}</div></div>', unsafe_allow_html=True)
            if st.button(f"ABRIR PRONTUÁRIO", key=f"btn_{l_id}"):
                st.session_state.leito_foco = l_id

    # ÁREA DE EDIÇÃO LIMPA
    if 'leito_foco' in st.session_state:
        l_id = st.session_state.leito_foco
        p = st.session_state.pacientes[l_id]
        st.divider()
        st.subheader(f"📝 Clínica Psicológica: Leito {l_id}")
        
        c1, c2 = st.columns([3, 1])
        st.session_state.pacientes[l_id]['nome'] = c1.text_input("Nome do Paciente", p['nome'], key=f"n_in_{l_id}")
        st.session_state.pacientes[l_id]['idade'] = c2.text_input("Idade", p['idade'], key=f"i_in_{l_id}")
        
        st.write("**Marcadores de UTI:**")
        m1, m2, m3, m4 = st.columns(4)
        st.session_state.pacientes[l_id]['vm'] = m1.checkbox("Vent. Mecânica", p['vm'], key=f"vm_c_{l_id}")
        st.session_state.pacientes[l_id]['delirium'] = m2.checkbox("Delirium", p['delirium'], key=f"del_c_{l_id}")
        st.session_state.pacientes[l_id]['isolamento'] = m3.checkbox("Isolamento", p['isolamento'], key=f"iso_c_{l_id}")
        st.session_state.pacientes[l_id]['paliativo'] = m4.checkbox("C. Paliativos", p['paliativo'], key=f"pal_c_{l_id}")

        t1, t2, t3 = st.tabs(["HISTÓRIA / ADMISSÃO", "AVALIAÇÃO PSÍQUICA", "CONDUTA"])
        with t1:
            st.session_state.pacientes[l_id]['historia'] = st.text_area("História Clínica:", p['historia'], height=150, key=f"h_tx_{l_id}")
        with t2:
            st.session_state.pacientes[idx]['exame'] = st.text_area("Exame Mental:", p['exame'], height=150, key=f"e_tx_{l_id}")
        with t3:
            st.session_state.pacientes[l_id]['conduta'] = st.text_area("Manejo e Pendências:", p['conduta'], height=150, key=f"c_tx_{l_id}")
        
        if st.button("💾 SALVAR E FECHAR"):
            del st.session_state.leito_foco
            st.rerun()

with aba_passagem:
    st.header("📋 Passagem de Plantão")
    lista = []
    for id_p, info in st.session_state.pacientes.items():
        if info['nome'] != f"Leito {id_p}":
            clinica = []
            if info['vm']: clinica.append("VM")
            if info['delirium']: clinica.append("DELIRIUM")
            if info['isol
