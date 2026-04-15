import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Plantão PSI", layout="wide")

# CSS para o visual TOTAL BLACK + MARROM CAFÉ + ABAS
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    .main { background-color: #000000 !important; color: #FFFFFF; }
    .logo-text { font-family: 'Helvetica', sans-serif; color: #8D6E63; font-size: 36px; font-weight: bold; letter-spacing: 2px; }
    .logo-sub { color: #FFFFFF; font-size: 32px; font-weight: bold; }
    .patient-card { 
        background-color: #0A0A0A; padding: 20px; border-radius: 8px; border: 1px solid #333333;
        border-top: 4px solid #4E342E; text-align: center; height: 120px;
    }
    /* Estilo dos botões e abas */
    .stButton>button { background-color: #4E342E; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #6D4C41; color: white; border: none; }
    textarea { background-color: #0A0A0A !important; color: white !important; border: 1px solid #4E342E !important; }
    input { background-color: #0A0A0A !important; color: white !important; border: 1px solid #4E342E !important; }
    
    /* Customizando as abas do Streamlit */
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; gap: 20px; }
    .stTabs [data-baseweb="tab"] { color: #8D6E63; font-weight: bold; font-size: 18px; }
    .stTabs [aria-selected="true"] { color: #FFFFFF !important; border-bottom-color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# Título fixo
st.markdown('<p class="logo-text">PLANTÃO <span class="logo-sub">PSI</span></p>', unsafe_allow_html=True)

# Inicializando o Banco de Dados se não existir
if 'pacientes' not in st.session_state:
    st.session_state.pacientes = {
        str(i): {"nome": f"Leito {i}", "idade": "--", "historia": "", "exame": "", "conduta": ""} 
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
