import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openrouter import OpenRouterModel
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
def load_environment():
    load_dotenv()

# Modelo Pydantic para representar o resultado de cada agente
class CurriculumInfo(BaseModel):
    nome: str
    habilidades: list
    experiencia: list
    pretensao_salarial: float

# 1. Definição dos Workers

# Worker para extrair informações do currículo
worker_extrair_info = Agent(
    model=OpenRouterModel(model='openai/gpt-4o-mini'),
    system_prompt='Extrair e estruturar informações de um currículo.'
)

async def extrair_info(ctx: RunContext[None], curriculo: str) -> CurriculumInfo:
    """Extrai informações do currículo para estruturar dados do candidato."""
    return await worker_extrair_info.run_sync(curriculo)

# Worker para verificar o perfil do candidato
worker_verificar_perfil = Agent(
    model=OpenRouterModel(model='openai/gpt-4o-mini'),
    system_prompt='Verificar se o perfil do candidato atende aos requisitos da vaga.'
)

async def verificar_perfil(ctx: RunContext[None], info: CurriculumInfo) -> bool:
    """Verifica se o perfil do candidato está conforme o esperado."""
    return await worker_verificar_perfil.run_sync(info)

# Worker para pesquisar o mercado salarial
worker_pesquisar_salario = Agent(
    model=OpenRouterModel(model='openai/gpt-4o-mini'),
    system_prompt='Pesquise o mercado para avaliar a pretensão salarial.'
)

async def pesquisar_salario(ctx: RunContext[None], pretensao: float) -> bool:
    """Avalia se a pretensão salarial está na faixa do mercado."""
    return await worker_pesquisar_salario.run_sync(pretensao)

# Worker para gerar parecer técnico
worker_parecer_tecnico = Agent(
    model=OpenRouterModel(model='openai/gpt-4o-mini'),
    system_prompt='Gere um parecer técnico sobre o candidato.'
)

async def parecer_tecnico(ctx: RunContext[None], info: CurriculumInfo) -> str:
    """Gera um parecer técnico baseado nas informações do candidato."""
    return await worker_parecer_tecnico.run_sync(info)

# Worker para gerar parecer comportamental
worker_parecer_comportamental = Agent(
    model=OpenRouterModel(model='openai/gpt-4o-mini'),
    system_prompt='Gere um parecer comportamental sobre o candidato.'
)

async def parecer_comportamental(ctx: RunContext[None], info: CurriculumInfo) -> str:
    """Gera um parecer comportamental baseado nas informações do candidato."""
    return await worker_parecer_comportamental.run_sync(info)

# Worker para enviar feedback por e-mail
worker_feedback_email = Agent(
    model=OpenRouterModel(model='openai/gpt-4o-mini'),
    system_prompt='Redija um e-mail de feedback para o candidato.'
)

async def redigir_feedback(ctx: RunContext[None], candidato: CurriculumInfo, aprovado: bool) -> str:
    """Redige um e-mail de feedback personalizado para o candidato."""
    return await worker_feedback_email.run_sync((candidato, aprovado))

# 2. Orquestrador

orquestrador = Agent(
    model=OpenRouterModel(model='openai/gpt-4o-mini'),
    system_prompt='Orquestre o processo seletivo do candidato.'
)

async def processar_selecao(curriculo: str):
    # Extrair informações do currículo
    info_curriculo = await extrair_info(None, curriculo)
    # Avaliar o perfil com base nas informações
    perfil_ok = await verificar_perfil(None, info_curriculo)
    # Pesquisar mercado para a pretensão salarial
    salario_ok = await pesquisar_salario(None, info_curriculo.pretensao_salarial)
    # Gerar pareceres
    parecer1 = await parecer_tecnico(None, info_curriculo)
    parecer2 = await parecer_comportamental(None, info_curriculo)
    # Redigir feedback
    feedback = await redigir_feedback(None, info_curriculo, perfil_ok and salario_ok)
    return feedback

async def main():
    load_environment()
    curriculo_exemplo = 'Exemplo de currículo'
    resultado = await processar_selecao(curriculo_exemplo)
    print(resultado)

if __name__ == '__main__':
    asyncio.run(main())