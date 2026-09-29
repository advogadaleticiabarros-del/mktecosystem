"""Radar Jurídico automático: pesquisa diária de novidades jurídicas que
viram pautas no Orbit, sem nenhum passo manual.

Interface: `rodar_radar(db, tenant_id, pesquisador, hoje)` → pautas criadas.
Por trás dela ficam: leitura das áreas do tenant, janela de 30 dias de temas
já sugeridos (enviada ao pesquisador como "evitar" e também filtrada depois,
porque o modelo nem sempre obedece), deduplicação por similaridade de título,
limite de 8 pautas por rodada e a escolha da manchete do Jornal às segundas.

O `Pesquisador` é a seam: `OpenAIPesquisador` (web search da OpenAI,
preferido) ou `TavilyGeminiPesquisador` (reserva com as chaves que o Orbit já
tem). `criar_pesquisador()` escolhe pelo que estiver configurado.
"""
import json
import re
import unicodedata
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from difflib import SequenceMatcher
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pauta import Pauta
from app.models.tenant import TenantConfig

JANELA_DEDUP_DIAS = 30
MAX_PAUTAS_POR_RODADA = 8
SIMILARIDADE_REPETIDO = 0.85
ORIGEM_MANCHETE = "radar_juridico_manchete"
ORIGEM_SATELITE = "radar_juridico_satelite"


@dataclass
class Achado:
    titulo: str
    resumo: str
    area: str
    angulo: str
    fonte: str
    url: str
    relevante_para_conteudo: bool


class Pesquisador(Protocol):
    async def pesquisar(self, areas: list[str], evitar: list[str], hoje: date) -> list[Achado]: ...


PROMPT_RADAR = """\
Você é o Radar Jurídico de uma advogada brasileira (Vitória/ES) que produz \
conteúdo para leigos no Instagram, blog e newsletter. Áreas de atuação: {areas}.

Hoje é {hoje}. Encontre as novidades jurídicas dos ÚLTIMOS 7 DIAS que mais \
interessam ao público dessas áreas: decisões do STF, STJ, TST, TNU, TRFs e TJES; \
teses e temas repetitivos; súmulas; leis, MPs e decretos publicados; portarias \
e mudanças de regra do INSS, Ministério do Trabalho e CNJ; notícias de grande \
repercussão que geram dúvida jurídica na população.

Regras:
- Só inclua fatos que você encontrou em fonte confiável, com link. Nunca \
invente decisão, número de processo, data ou resultado.
- Prefira fontes oficiais (sites de tribunais, gov.br, Planalto, DOU); imprensa \
jurídica (Conjur, Migalhas, JOTA) só quando não houver a oficial.
- Traga de 5 a 10 achados, variados entre as áreas; não repita o mesmo fato.
- NÃO traga nada destes temas, já trabalhados recentemente:
{evitar}

Para cada achado:
- titulo: manchete curta e clara, em linguagem de leigo (máx. 90 caracteres)
- resumo: 3 a 5 frases — o que aconteceu, quem decidiu/publicou, quando, e o \
que muda na prática para a pessoa comum
- area: uma das áreas de atuação acima
- angulo: "direitos" (oportunidade para a pessoa) ou "sinceridade" (risco/cautela)
- fonte: nome curto da fonte (ex.: STF, TST, INSS, Planalto, Conjur)
- url: link da fonte
- relevante_para_conteudo: true se é simples de explicar e atrai cliente; \
false se é técnico/processual demais para virar post

Responda SOMENTE com JSON: {{"achados": [...]}}
"""


def montar_prompt(areas: list[str], evitar: list[str], hoje: date) -> str:
    return PROMPT_RADAR.format(
        areas=", ".join(areas) or "Trabalhista, Previdenciário, Família, Consumidor",
        hoje=hoje.strftime("%d/%m/%Y"),
        evitar="\n".join(f"- {t}" for t in evitar) or "- (nenhum)",
    )


def parse_achados(texto: str) -> list[Achado]:
    """Extrai achados do texto do modelo, tolerando bloco ```json e itens
    incompletos (descartados em vez de derrubar a rodada inteira)."""
    inicio, fim = texto.find("{"), texto.rfind("}")
    if inicio == -1 or fim <= inicio:
        return []
    try:
        dados = json.loads(texto[inicio : fim + 1])
    except json.JSONDecodeError:
        return []

    achados = []
    for item in dados.get("achados", []):
        if not isinstance(item, dict) or not item.get("titulo") or not item.get("resumo"):
            continue
        achados.append(
            Achado(
                titulo=str(item["titulo"]).strip()[:300],
                resumo=str(item["resumo"]).strip(),
                area=str(item.get("area") or "Geral")[:100],
                angulo=item.get("angulo") if item.get("angulo") in ("direitos", "sinceridade") else "direitos",
                fonte=str(item.get("fonte") or "web")[:200],
                url=str(item.get("url") or ""),
                relevante_para_conteudo=bool(item.get("relevante_para_conteudo", True)),
            )
        )
    return achados


def _normalizar(titulo: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", sem_acento.lower()).split())


def _repetido(titulo: str, vistos: list[str]) -> bool:
    n = _normalizar(titulo)
    return any(SequenceMatcher(None, n, v).ratio() >= SIMILARIDADE_REPETIDO for v in vistos)


async def rodar_radar(
    db: AsyncSession, tenant_id: uuid.UUID, pesquisador: Pesquisador, hoje: date
) -> list[Pauta]:
    config = (
        await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == tenant_id))
    ).scalar_one_or_none()
    areas = list(config.voz.get("areas", [])) if config else []

    desde = datetime.now(timezone.utc) - timedelta(days=JANELA_DEDUP_DIAS)
    recentes = (
        await db.execute(
            select(Pauta.titulo).where(Pauta.tenant_id == tenant_id, Pauta.criado_em >= desde)
        )
    ).scalars().all()

    achados = await pesquisador.pesquisar(areas, list(recentes), hoje)

    vistos = [_normalizar(t) for t in recentes]
    novos: list[Achado] = []
    for achado in achados:
        if _repetido(achado.titulo, vistos):
            continue
        vistos.append(_normalizar(achado.titulo))
        novos.append(achado)
    novos = novos[:MAX_PAUTAS_POR_RODADA]

    # O Jornal é semanal: só a segunda-feira elege manchete.
    manchete = None
    if hoje.weekday() == 0:
        manchete = next((a for a in novos if a.relevante_para_conteudo), None)

    pautas = []
    for achado in novos:
        conteudo = achado.resumo + (f"\n\nFonte: {achado.fonte} — {achado.url}" if achado.url else "")
        pauta = Pauta(
            tenant_id=tenant_id,
            titulo=achado.titulo,
            angulo=achado.angulo,
            area=achado.area,
            origem=ORIGEM_MANCHETE if achado is manchete else ORIGEM_SATELITE,
            fonte=achado.fonte,
            relevante_para_conteudo=achado.relevante_para_conteudo,
            status="sugerida",
            conteudo_bruto=conteudo,
            data_editorial=hoje,
        )
        db.add(pauta)
        pautas.append(pauta)

    await db.commit()
    for p in pautas:
        await db.refresh(p)
    return pautas


def criar_pesquisador() -> Pesquisador | None:
    """OpenAI se houver chave; senão Tavily + Gemini; senão None (radar desligado)."""
    from app.config import settings

    if settings.OPENAI_API_KEY:
        from app.integrations.radar.openai_pesquisador import OpenAIPesquisador

        return OpenAIPesquisador(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_RADAR_MODEL)
    if settings.TAVILY_API_KEY and settings.GEMINI_API_KEY:
        from app.integrations.ai.gemini import GeminiClient
        from app.integrations.radar.tavily_gemini_pesquisador import TavilyGeminiPesquisador
        from app.integrations.search.tavily_client import TavilyClient

        return TavilyGeminiPesquisador(
            tavily=TavilyClient(api_key=settings.TAVILY_API_KEY),
            ai=GeminiClient(api_key=settings.GEMINI_API_KEY),
        )
    return None
