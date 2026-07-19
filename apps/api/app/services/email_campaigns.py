"""Geração de rascunhos de campanhas de e-mail na voz do tenant.

Nada aqui envia e-mail: o resultado sempre entra como status="rascunho"
e depende de aprovação humana na tela /emails.
"""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.ai.base import AIClient
from app.models.content_piece import ContentPiece
from app.models.email_campaign import EmailCampaign
from app.models.pauta import Pauta
from app.models.tenant import TenantConfig

WELCOME_TIPOS = ["boas_vindas_1", "boas_vindas_2", "boas_vindas_3"]

WELCOME_PROMPT = """\
Você escreve e-mails para a advogada com esta voz e princípios:
{voz}

Escreva a sequência de boas-vindas para quem acabou de deixar o contato no site
pedindo para falar com a advogada. São 3 e-mails:

1. Enviado na hora: boas-vindas, o que a pessoa pode esperar, tom acolhedor,
   reforço de que ela será atendida pessoalmente.
2. Enviado no dia 2: conteúdo educativo sobre o direito mais comum dos clientes
   (área trabalhista/previdenciária), sem prometer resultado.
3. Enviado no dia 5: convite claro para agendar uma conversa (WhatsApp), com
   tom de disponibilidade, não de pressão.

Regras obrigatórias (OAB): nunca prometer resultado; usar "pode ter direito",
"a lei prevê", "vamos avaliar"; tom educativo, jamais mercantilizar.

Responda em JSON:
{{"emails": [{{"assunto": "...", "corpo_html": "<p>...</p>", "corpo_texto": "..."}}, ...]}}
(exatamente 3 itens, na ordem. corpo_html usa apenas <p>, <strong>, <a>, <br>.)
"""

NEWSLETTER_PROMPT = """\
Você escreve a newsletter semanal da advogada com esta voz e princípios:
{voz}

Artigos publicados esta semana no blog:
{artigos}

Escreva UM e-mail de newsletter que apresenta esses artigos: um parágrafo de
abertura conectando com o cotidiano do leitor, depois um bloco por artigo
(título como link + 2 frases de resumo que geram curiosidade sem clickbait),
e um fechamento curto convidando a responder o e-mail com dúvidas.

Regras obrigatórias (OAB): nunca prometer resultado; tom educativo.

Responda em JSON:
{{"assunto": "...", "corpo_html": "<p>...</p>", "corpo_texto": "..."}}
(corpo_html usa apenas <p>, <strong>, <a>, <h2>, <br>.)
"""


async def _voz_do_tenant(db: AsyncSession, tenant_id: uuid.UUID) -> str:
    result = await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == tenant_id))
    config = result.scalar_one_or_none()
    return str(config.voz) if config else ""


async def gerar_boas_vindas(
    db: AsyncSession, tenant_id: uuid.UUID, ai: AIClient
) -> list[EmailCampaign]:
    """Gera os 3 rascunhos da sequência. Arquiva rascunhos anteriores do mesmo tipo."""
    voz = await _voz_do_tenant(db, tenant_id)
    data = await ai.generate_json(WELCOME_PROMPT.format(voz=voz))
    emails = data.get("emails", [])
    if len(emails) != 3:
        raise ValueError(f"IA retornou {len(emails)} e-mails; esperava 3.")

    antigos = await db.execute(
        select(EmailCampaign).where(
            EmailCampaign.tenant_id == tenant_id,
            EmailCampaign.tipo.in_(WELCOME_TIPOS),
            EmailCampaign.status == "rascunho",
        )
    )
    for antigo in antigos.scalars():
        antigo.status = "arquivado"

    campanhas = []
    for tipo, email in zip(WELCOME_TIPOS, emails):
        campanha = EmailCampaign(
            tenant_id=tenant_id,
            tipo=tipo,
            assunto=email["assunto"],
            corpo_html=email["corpo_html"],
            corpo_texto=email["corpo_texto"],
        )
        db.add(campanha)
        campanhas.append(campanha)
    await db.commit()
    for c in campanhas:
        await db.refresh(c)
    return campanhas


async def gerar_rascunho_newsletter(
    db: AsyncSession, tenant_id: uuid.UUID, ai: AIClient
) -> EmailCampaign | None:
    """Monta o rascunho da newsletter com o conteúdo aprovado dos últimos 7 dias.

    Sem conteúdo na janela, não cria rascunho (retorna None).
    """
    since = datetime.now(timezone.utc) - timedelta(days=7)
    result = await db.execute(
        select(ContentPiece, Pauta)
        .join(Pauta, ContentPiece.pauta_id == Pauta.id)
        .where(
            ContentPiece.tenant_id == tenant_id,
            ContentPiece.tipo == "blog",
            ContentPiece.status == "aprovado",
            ContentPiece.criado_em >= since,
        )
    )
    rows = result.all()
    if not rows:
        return None

    artigos = "\n\n".join(
        f"- Título: {pauta.titulo}\n  Resumo do conteúdo: {str(piece.corpo)[:500]}"
        for piece, pauta in rows
    )
    voz = await _voz_do_tenant(db, tenant_id)
    data = await ai.generate_json(NEWSLETTER_PROMPT.format(voz=voz, artigos=artigos))

    campanha = EmailCampaign(
        tenant_id=tenant_id,
        tipo="newsletter",
        assunto=data["assunto"],
        corpo_html=data["corpo_html"],
        corpo_texto=data["corpo_texto"],
    )
    db.add(campanha)
    await db.commit()
    await db.refresh(campanha)
    return campanha
