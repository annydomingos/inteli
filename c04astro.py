import requests
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel

load_dotenv()

HEADERS = {"User-Agent": "AulaAgentes/1.0 (aula didatica)"}

def pesquisar_wikipedia(termo: str) -> str:
    """
    Pesquisa informações sobre um tema na Wikipedia em português.
    Use quando precisar de informações factuais sobre qualquer assunto.
    Pode ser chamada múltiplas vezes para temas diferentes.
    """
    try:
        busca = requests.get(
            "https://pt.wikipedia.org/w/api.php",
            params={"action": "query", "list": "search",
                    "srsearch": termo, "format": "json", "srlimit": 1},
            timeout=5, headers=HEADERS,
        )
        resultados = busca.json().get("query", {}).get("search", [])
        if not resultados:
            return f"Não encontrei nada sobre '{termo}'."

        titulo = resultados[0]["title"]
        resumo = requests.get(
            f"https://pt.wikipedia.org/api/rest_v1/page/summary/{titulo.replace(' ', '_')}",
            timeout=5, headers=HEADERS,
        )
        texto = resumo.json().get("extract", "Sem resumo.") if resumo.status_code == 200 else "Não encontrado."
        return f"[Artigo: {titulo}]\n{texto}"

    except Exception as e:
        return f"Erro: {e}"


modelo = OpenRouterModel("openai/gpt-4o-mini")
pergunta = "O que é processamento de linguagem natural?"
pergunta_astrologia = "O que significa Mercúrio retrógrado e como ele afeta os signos?"

# ── Sem ferramenta — responde de memória ──────────────────────────────────────
agente_sem = Agent(
    model=modelo,
    system_prompt="Você é um assistente de pesquisa.",
)

# ── Com ferramenta — busca antes de responder ─────────────────────────────────
agente_com = Agent(
    model=modelo,
    tools=[pesquisar_wikipedia],
    system_prompt=(
        "Você é um assistente de pesquisa. "
        "Sempre pesquise o tema antes de responder — nunca responda de memória."
    ),
)

# ── Especialista em astrologia ────────────────────────────────────────────────
agente_astrologo = Agent(
    model=modelo,
    tools=[pesquisar_wikipedia],
    system_prompt=(
        "Você é um astrólogo experiente e apaixonado, com décadas de estudo em astrologia ocidental e védica. "
        "Seu papel é interpretar e explicar temas astrológicos com profundidade, clareza e entusiasmo. "
        "Quando receber uma pergunta, siga estas diretrizes:\n\n"
        "1. Pesquise o tema na Wikipedia quando precisar de embasamento histórico ou conceitual sobre planetas, signos, casas ou movimentos astrológicos.\n"
        "2. Estruture sua resposta cobrindo:\n"
        "   - O significado simbólico e mitológico do tema (planeta, signo, aspecto, etc.)\n"
        "   - Como ele se manifesta na prática no dia a dia das pessoas\n"
        "   - Impactos específicos por signo ou mapa natal, quando relevante\n"
        "   - Conselhos práticos para o período ou situação astrológica\n"
        "3. Use linguagem acessível, mas rica em termos astrológicos. Explique os termos técnicos quando necessário.\n"
        "4. Mantenha um tom acolhedor, reflexivo e encorajador — a astrologia serve como ferramenta de autoconhecimento.\n"
        "5. Seja claro que a astrologia é uma tradição simbólica e interpretativa, não uma ciência preditiva exata.\n"
        "Responda sempre em português."
    ),
)

print("=" * 60)
print("SEM FERRAMENTA:")
print("=" * 60)
r1 = agente_sem.run_sync(pergunta)
print(r1.output)
print(f"\nChamadas à API: {r1.usage().requests}")

print("\n" + "=" * 60)
print("COM FERRAMENTA:")
print("=" * 60)
r2 = agente_com.run_sync(pergunta)
print(r2.output)
print(f"\nChamadas à API: {r2.usage().requests}")

print("\n" + "=" * 60)
print("ESPECIALISTA EM ASTROLOGIA:")
print("=" * 60)
r3 = agente_astrologo.run_sync(pergunta_astrologia)
print(r3.output)
print(f"\nChamadas à API: {r3.usage().requests}")