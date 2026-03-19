import streamlit as st
import subprocess
import os
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
# ── Botão de limpar sessão ─────────────────────────────────────────────────────
if st.button("🗑️ Limpar e começar novo case"):
    for key in ["resultado_arquiteto", "business_case", "requests_arquiteto",
                "codigo_gerado", "requests_dev"]:
        st.session_state.pop(key, None)
    if os.path.exists("solucao_gerada.py"):
        os.remove("solucao_gerada.py")
    st.rerun()

# ── Input do business case ─────────────────────────────────────────────────────
business_case = st.text_area(
    label="Business Case",
    placeholder="Ex: Uma empresa de e-commerce quer automatizar o atendimento ao cliente...",
    height=180,
    key="business_case_input"
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

    # ── Agente Construtor ──────────────────────────────────────────────────────
    st.divider()
    st.subheader("🔨 Agente Construtor")
    st.markdown("Clique abaixo para salvar o código em um arquivo `.py` e executá-lo.")

    if st.button("🚀 Construir e Executar", type="primary"):
        caminho_arquivo = "solucao_gerada.py"

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(codigo.codigo_python)
        st.success(f"✅ Arquivo salvo em `{caminho_arquivo}`")

        with st.spinner("⚙️ Executando o código gerado..."):
            resultado_execucao = subprocess.run(
                ["python", caminho_arquivo],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )

        if resultado_execucao.stdout:
            st.subheader("📟 Output da Execução")
            st.code(resultado_execucao.stdout, language="bash")

        if resultado_execucao.returncode != 0:
            st.subheader("❌ Erro na Execução")
            st.error(resultado_execucao.stderr)
        else:
            st.success("✅ Código executado com sucesso!")