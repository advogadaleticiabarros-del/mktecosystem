"""Dicas automáticas v1: a IA analisa os dados internos do tenant e recomenda.

V1 usa o que já existe no banco (produção, status, lições de edição, e-mail).
Quando as integrações externas chegarem (Instagram/GA4/GMB), os mesmos dados
entram neste resumo e as dicas ficam mais afiadas — a interface não muda.
"""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.ai.base import AIClient
from app.models.contact import Contact
from app.models.content_piece import ContentPiece
from app.models.email_send import EmailSend
from app.models.marketing_memory import MarketingMemory
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost

INSIGHTS_PROMPT = """\
Você é estrategista de marketing de um escritório de advocacia (conformidade
OAB: nunca sugerir promessa de resultado nem captação ativa).

Dados das últimas 4 semanas da operação:
{dados}

Gere de 3 a 5 dicas ACIONÁVEIS e específicas para melhorar o desempenho, em
ordem de impacto. Cada dica: uma frase de diagnóstico + uma ação concreta.
Não invente métricas que não estão nos dados. Se um dado estiver zerado,
a dica pode ser justamente ativar aquela frente.

Responda em JSON:
{{"dicas": [{{"titulo": "...", "diagnostico": "...", "acao": "..."}}]}}
"""


async def _coletar_dados(db: AsyncSession, tenant_id: uuid.UUID) -> str:
    janela = datetime.now(timezone.utc) - timedelta(weeks=4)

    async def _count(stmt) -> int:
        return (await db.execute(stmt)).scalar_one()

    pautas = await _count(
        select(func.count(Pauta.id)).where(
            Pauta.tenant_id == tenant_id, Pauta.criado_em >= janela
        )
    )
    linhas = [f"- Pautas pesquisadas: {pautas}"]

    por_status = await db.execute(
        select(ContentPiece.status, func.count(ContentPiece.id))
        .where(ContentPiece.tenant_id == tenant_id, ContentPiece.criado_em >= janela)
        .group_by(ContentPiece.status)
    )
    for status, total in por_status.all():
        linhas.append(f"- Conteúdos '{status}': {total}")

    por_formato = await db.execute(
        select(ContentPiece.tipo, func.count(ContentPiece.id))
        .where(
            ContentPiece.tenant_id == tenant_id,
            ContentPiece.status == "aprovado",
            ContentPiece.criado_em >= janela,
        )
        .group_by(ContentPiece.tipo)
    )
    for tipo, total in por_formato.all():
        linhas.append(f"- Aprovados no formato '{tipo}': {total}")

    agendados = await _count(
        select(func.count(ScheduledPost.id)).where(
            ScheduledPost.tenant_id == tenant_id,
            ScheduledPost.status.in_(("planejado", "pronto")),
        )
    )
    publicados = await _count(
        select(func.count(ScheduledPost.id)).where(
            ScheduledPost.tenant_id == tenant_id, ScheduledPost.status == "publicado"
        )
    )
    linhas.append(f"- Publicações agendadas pendentes: {agendados}; publicadas: {publicados}")

    contatos = await _count(
        select(func.count(Contact.id)).where(
            Contact.tenant_id == tenant_id, Contact.status == "ativo"
        )
    )
    novos = await _count(
        select(func.count(Contact.id)).where(
            Contact.tenant_id == tenant_id, Contact.criado_em >= janela
        )
    )
    linhas.append(f"- Contatos ativos: {contatos} (novos na janela: {novos})")

    emails = await _count(
        select(func.count(EmailSend.id)).where(
            EmailSend.tenant_id == tenant_id,
            EmailSend.status == "enviado",
            EmailSend.criado_em >= janela,
        )
    )
    linhas.append(f"- E-mails entregues na janela: {emails}")

    licoes = (
        (
            await db.execute(
                select(MarketingMemory.aprendizado)
                .where(
                    MarketingMemory.tenant_id == tenant_id,
                    MarketingMemory.aprendizado.is_not(None),
                )
                .order_by(MarketingMemory.id.desc())
                .limit(3)
            )
        )
        .scalars()
        .all()
    )
    if licoes:
        linhas.append("- Últimas correções feitas pela cliente nos textos gerados:")
        linhas.extend(f"  * {licao[:200]}" for licao in licoes)

    return "\n".join(linhas)


async def gerar_insights(db: AsyncSession, tenant_id: uuid.UUID, ai: AIClient) -> list[dict]:
    dados = await _coletar_dados(db, tenant_id)
    resultado = await ai.generate_json(INSIGHTS_PROMPT.format(dados=dados))
    dicas = resultado.get("dicas", [])
    return [
        {
            "titulo": str(d.get("titulo", "")),
            "diagnostico": str(d.get("diagnostico", "")),
            "acao": str(d.get("acao", "")),
        }
        for d in dicas
        if d.get("titulo")
    ]
