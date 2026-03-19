import streamlit as st
from dotenv import load_dotenv
from agentes.arquiteto import agente_arquiteto
from agentes.dev import agente_dev

load_dotenv()

# ── Configuração da página ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agente Arquiteto + Dev",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Agente Arquiteto de Sistemas Multi-Agentes")
st.markdown("Descreva seu **business case**, receba a análise das 4 arquiteturas e gere o **código Python pronto** para implementar.")

# ── Input do business case ─────────────────────────────────────────────────────
business_case = st.text_area(
    label="Business Case",
    placeholder="Ex: Uma empresa de e-commerce quer automatizar o atendimento ao cliente...",
    height=180
)

if st.button("Analisar Arquiteturas", type="primary", disabled=not business_case.strip()):
    with st.spinner("🏗️ Agente Arquiteto analisando o business case..."):
        resposta_arquiteto = agente_arquiteto.run_sync(business_case)
        st.session_state.resultado_arquiteto = resposta_arquiteto.output
        st.session_state.business_case = business_case
        st.session_state.requests_arquiteto = resposta_arquiteto.usage().requests

# ── Exibe resultado do arquiteto se já foi gerado ──────────────────────────────
if "resultado_arquiteto" in st.session_state:
    resultado = st.session_state.resultado_arquiteto

    st.divider()
    st.subheader("📐 Análise de Arquiteturas")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🔗 Arquitetura 1 — Prompt Chaining", expanded=True):
            st.write(resultado.arquitetura_1_prompt_chaining)

        with st.expander("🎛️ Arquitetura 3 — Parallelization", expanded=True):
            st.write(resultado.arquitetura_3_parallelization)

    with col2:
        with st.expander("🧠 Arquitetura 2 — Orchestrator-Workers", expanded=True):
            st.write(resultado.arquitetura_2_orchestrator_workers)

        with st.expander("🔀 Arquitetura 4 — Routing", expanded=True):
            st.write(resultado.arquitetura_4_routing)

    st.divider()
    st.subheader("⭐ Recomendação do Arquiteto")
    st.success(resultado.recomendacao_final)
    st.caption(f"Chamadas à API (arquiteto): {st.session_state.requests_arquiteto}")

    # ── Botão de autorização para o Agente Dev ─────────────────────────────────
    st.divider()
    if st.button("👨‍💻 Gerar Código com o Agente Dev", type="primary"):
        with st.spinner("👨‍💻 Agente Dev gerando o código Python..."):
            prompt_dev = (
                f"## Business Case\n{st.session_state.business_case}\n\n"
                f"## Arquitetura Recomendada pelo Arquiteto\n{resultado.recomendacao_final}"
            )
            resposta_dev = agente_dev.run_sync(prompt_dev)
            st.session_state.codigo_gerado = resposta_dev.output
            st.session_state.requests_dev = resposta_dev.usage().requests

# ── Exibe código gerado se já foi gerado ──────────────────────────────────────
if "codigo_gerado" in st.session_state:
    codigo = st.session_state.codigo_gerado

    st.subheader("📄 Código Gerado")
    st.info(codigo.explicacao)
    st.code(codigo.codigo_python, language="python")
    st.caption(f"Chamadas à API (dev): {st.session_state.requests_dev}")

