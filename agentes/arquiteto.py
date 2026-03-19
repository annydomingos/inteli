import requests
import streamlit as st
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic import BaseModel

load_dotenv()

HEADERS = {"User-Agent": "AulaAgentes/1.0 (aula didatica)"}

# ── Output estruturado do Agente Arquiteto ─────────────────────────────────────
class ArquiteturaDeAgentes(BaseModel):
    arquitetura_1_prompt_chaining: str
    arquitetura_2_orchestrator_workers: str
    arquitetura_3_parallelization: str
    arquitetura_4_routing: str
    recomendacao_final: str


# ── Agente Arquiteto ───────────────────────────────────────────────────────────
agente_arquiteto = Agent(
    model=OpenRouterModel("openai/gpt-4o-mini"),
    output_type=ArquiteturaDeAgentes,
    system_prompt=(
        "Você é um arquiteto sênior de sistemas multi-agentes com IA. "
        "Sua especialidade é analisar problemas de negócio e estruturar soluções "
        "usando padrões de orquestração de agentes.\n\n"

        "Você conhece profundamente os 4 padrões de arquitetura abaixo:\n\n"

        "## ARQUITETURA 1 — Prompt Chaining\n"
        "Agentes especializados executam em sequência fixa definida no código. "
        "A saída de um vira a entrada do próximo (via output_type estruturado). "
        "O fluxo é sempre o mesmo, independente da pergunta. "
        "Os agentes não sabem que fazem parte de um pipeline.\n"
        "Ideal para: fluxos previsíveis, tarefas sequenciais com dependência clara entre etapas, "
        "pipelines de transformação de dados, geração de documentos em etapas.\n\n"

        "## ARQUITETURA 2 — Orchestrator-Workers\n"
        "Um agente orquestrador decide em runtime quais workers acionar e em qual ordem, "
        "com base na pergunta recebida. Os workers são ferramentas do orquestrador. "
        "O orquestrador não tem especialidade, apenas sabe delegar. "
        "O fluxo é dinâmico — cada pergunta pode acionar uma combinação diferente de workers.\n"
        "Ideal para: problemas com múltiplos caminhos possíveis, perguntas abertas, "
        "assistentes inteligentes que precisam combinar habilidades diferentes.\n\n"

        "## ARQUITETURA 3 — Parallelization\n"
        "Tarefas independentes entre si são executadas simultaneamente com async/await e asyncio.gather. "
        "O resultado de A não depende de B, então não há motivo para esperar. "
        "Reduz drasticamente o tempo de execução quando há múltiplas subtarefas paralelas.\n"
        "Ideal para: análises de múltiplas fontes ao mesmo tempo, geração simultânea de variações, "
        "consultas independentes que precisam ser consolidadas ao final.\n\n"

        "## ARQUITETURA 4 — Routing\n"
        "Um agente roteador classifica a pergunta e transfere para o especialista correto, "
        "que responde diretamente. O roteador não sintetiza nada — apenas direciona. "
        "Cada especialista é autônomo e completo para seu domínio.\n"
        "Ideal para: sistemas com domínios bem definidos e separados, chatbots com múltiplas "
        "áreas de atuação, suporte técnico com categorias distintas.\n\n"

        "## SUA TAREFA\n"
        "Quando receber um business case, você deve:\n"
        "1. Para cada uma das 4 arquiteturas, descrever como ela seria aplicada especificamente, descrevendo claramente quantos agentes e quais funções cada um executaria"
        "ao problema apresentado — com exemplos concretos dos agentes envolvidos, "
        "o fluxo de dados, os papéis de cada agente e as vantagens naquele contexto.\n"
        "2. Ao final, dar sua recomendação fundamentada de qual arquitetura (ou combinação) "
        "seria a mais indicada para o caso, justificando com base em: complexidade do fluxo, "
        "variabilidade das entradas, necessidade de paralelismo e clareza dos domínios.\n\n"
        "Seja técnico, específico e direto. Evite respostas genéricas — "
        "cada resposta deve ser moldada ao business case recebido.\n"
        "Responda sempre em português."
    ),
)


# ── Frontend Streamlit ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agente Arquiteto",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Agente Arquiteto de Sistemas Multi-Agentes")
st.markdown("Descreva seu **business case** e receba uma análise completa das 4 arquiteturas de orquestração de agentes, com recomendação final.")

business_case = st.text_area(
    label="Business Case",
    placeholder="Ex: Uma empresa de e-commerce quer automatizar o atendimento ao cliente...",
    height=180
)

if st.button("Analisar", type="primary", disabled=not business_case.strip()):
    with st.spinner("Analisando business case... aguarde."):
        resposta = agente_arquiteto.run_sync(business_case)
        resultado = resposta.output

    st.divider()

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

    st.caption(f"Chamadas à API: {resposta.usage().requests}")