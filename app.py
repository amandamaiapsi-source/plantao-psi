import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Plantão PSI", layout="wide")

# CSS para visual TOTAL BLACK + CAFÉ
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main { background-color: #000000 !important; color: #FFFFFF; }
    .logo-text { font-family: 'Helvetica', sans-serif; color: #8D6E63; font-size: 36px; font-weight: bold; letter-spacing: 2px; }
    .logo-sub { color: #FFFFFF; font-size: 32px; font-weight: bold; }
    .patient-card { 
        background-color: #0A0A0A; padding: 10px; border-radius: 8px; border: 1px solid #333333;
        border-top: 4px solid #4E342E; text-align: center; margin-bottom: 5px; min-height: 150px;
    }
    .stButton>button { background-color: #4E342E; color: white; border: none; font-weight: bold; width: 100%; font-size: 12px; }
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

# Inicialização de dados robusta
if 'pacientes' not in st.session_state:
    st.session_state.pacientes = {str(i): {
        "nome": f"Leito {i}", "idade": "", "historia": "", "exame": "", "conduta": "",
        "vm": False, "delirium": False, "isolamento": False, "paliativo": False, "alta": False
    } for i in range(1, 11)}

aba_mapa, aba_passagem = st.tabs(["🗺️ MAPA DE LEITOS", "🖨️ GERAR PASSAGEM"])

# --- ABA MAPA ---
with aba_mapa:
    cols = st.columns(5)
    for i in range(1, 11):
        l_id = str(i)
        p = st.session_state.pacientes[l_id]
        with cols[(i-1) % 5]:
            # Tags visuais no card
            tags_html = ""
            if p['vm']: tags_html += '<span class="tag tag-vm">VM</span>'
            if p['delirium']: tags_html += '<span class="tag tag-del">DEL</span>'
            if p['paliativo']: tags_html += '<span class="tag tag-pal">PAL</span>'
            if p['isolamento']: tags_html += '<span class="tag tag-iso">ISO</span>'
            
            st.markdown(f"""
                <div class="patient-card">
                    <span style="color: #8D6E63; font-weight: bold;">LEITO {l_id}</span><br>
                    <span style="font-size: 13px; font-weight: bold;">{p["nome"]}</span><br>
                    <div style="margin-top: 5px;">{tags_html}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ABRIR PRONTUÁRIO", key=f"ed_{l_id}"):
                st.session_state.leito_foco = l_id

    if 'leito_foco' in st.session_state:
        l_id = st.session_state.leito_foco
        p = st.session_state.pacientes[l_id]
        st.divider()
        st.subheader(f"📝 Clínica Psicológica: Leito {l_id}")
        
        # Identificação e Marcadores Rápidos
        c1, c2 = st.columns([2, 2])
        st.session_state.pacientes[l_id]['nome'] = c1.text_input("Nome", p['nome'], key=f"n_{l_id}")
        st.session_state.pacientes[l_id]['idade'] = c2.text_input("Idade", p['idade'], key=f"i_{l_id}")
        
        st.write("**Marcadores Clínicos (Alimentam a Passagem):**")
        m1, m2, m3, m4, m5 = st.columns(5)
        st.session_state.pacientes[l_id]['vm'] = m1.checkbox("Vent. Mecânica", p['vm'], key=f"vm_{l_id}")
        st.session_state.pacientes[l_id]['delirium'] = m2.checkbox("Delirium", p['delirium'], key=f"del_{l_id}")
        st.session_state.pacientes[l_id]['isolamento'] = m3.checkbox("Isolamento", p['isolamento'], key=f"iso_{l_id}")
        st.session_state.pacientes[l_id]['paliativo'] = m4.checkbox("C. Paliativos", p['paliativo'], key=f"pal_{l_id}")
        st.session_state.pacientes[l_id]['alta'] = m5.checkbox("Previsão Alta", p['alta'], key=f"alt_{l_id}")

        t1, t2, t3 = st.tabs(["HISTÓRIA / ADMISSÃO", "AVALIAÇÃO PSÍQUICA", "CONDUTA"])
        st.session_state.pacientes[l_id]['historia'] = t1.text_area("História Clínica / Queixa:", p['historia'], height=150, key=f"h_{l_id}")
        st.session_state.pacientes[l_id]['exame'] = t2.text_area("Exame Mental / Posição Subjetiva:", p['exame'], height=150, key=f"e_{l_id}")
        st.session_state.pacientes[l_id]['conduta'] = t3.text_area("Manejo e Pendências:", p['conduta'], height=150, key=f"c_{l_id}")
        
        if st.button("💾 SALVAR E VOLTAR AO MAPA"):
            del st.session_state.leito_foco
            st        str(i): {"nome": f"Leito {i}", "idade": "--", "historia": "", "exame": "", "conduta": ""} 
        for i in range(1, 11)
    }

# Menu de Navegação Superior (Igual ao do médico)
aba_geral, aba_passagem = st.tabs(["🗺️ MAPA DE UNIDADE", "🖨️ PASSAGEM DE PLANTÃO"])

with aba_geral:
    # Grid de Leitos
    cols = st.columns(5)
    for i in range(1, 11):
        leito_id = str(i)
        p = st.session_state.pacientes[leito_id]
        with cols[(i-1) % 5]:
            st.markdown(f'<div class="patient-card"><span style="color: #8D6E63; font-weight: bold;">LEITO {leito_id}</span><br><span style="font-size: 14px; color: #FFFFFF;">{p["nome"]}</span></div>', unsafe_allow_html=True)
            if st.button(f"EDITAR LEITO {leito_id}", key=f"edit_{leito_id}"):
                st.session_state.leito_ativo = leito_id

    # Se um leito for selecionado, abre a ficha abaixo
    if 'leito_ativo' in st.session_state:
        leito_id = st.session_state.leito_ativo
        p = st.session_state.pacientes[leito_id]
        st.divider()
        st.markdown(f"### 📝 Editando Leito {leito_id}")
        
        c1, c2 = st.columns([3, 1])
        st.session_state.pacientes[leito_id]['nome'] = c1.text_input("Nome do Paciente", p['nome'], key=f"nome_{leito_id}")
        st.session_state.pacientes[leito_id]['idade'] = c2.text_input("Idade", p['idade'], key=f"idade_{leito_id}")
        
        t1, t2, t3 = st.tabs(["História", "Exame Psíquico", "Condutas"])
        st.session_state.pacientes[leito_id]['historia'] = t1.text_area("História/Demanda:", p['historia'], height=150, key=f"hist_{leito_id}")
        st.session_state.pacientes[leito_id]['exame'] = t2.text_area("Exame Mental/Posição Subjetiva:", p['exame'], height=150, key=f"ex_{leito_id}")
        st.session_state.pacientes[leito_id]['conduta'] = t3.text_area("Manejo e Pendências:", p['conduta'], height=150, key=f"cond_{leito_id}")
        
        if st.button("✅ SALVAR E FECHAR", key="save"):
            st.success("Dados salvos!")
            del st.session_state.leito_ativo
            st.rerun()

with aba_passagem:
    st.markdown("### 📋 Mapa de Passagem (Todos os Leitos)")
    
    # Criando a tabela para impressão
    dados_impressao = []
    for i in range(1, 11):
        p = st.session_state.pacientes[str(i)]
        # Só inclui se o nome tiver sido alterado ou se houver conduta
        if p['nome'] != f"Leito {i}" or p['conduta'] != "":
            dados_impressao.append({
                "Leito": i,
                "Paciente": f"{p['nome']} ({p['idade']}a)",
                "História/Exame": f"{p['historia']}\n\nEXAME: {p['exame']}",
                "Condutas/Pendências": p['conduta']
            })
    
    if dados_impressao:
        df = pd.DataFrame(dados_impressao)
        st.table(df)
        st.info("💡 Para imprimir: Clique com o botão direito na página > Imprimir (ou Ctrl + P).")
    else:
        st.warning("Nenhum dado preenchido para gerar a passagem.")
