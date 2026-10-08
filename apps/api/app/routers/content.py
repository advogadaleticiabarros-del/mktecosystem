import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.ai.base import AIClient
from app.integrations.ai.fabrica import criar_ia
from app.integrations.ai.gemini import GeminiClient
from app.integrations.ai.groq_client import GroqClient
from app.integrations.search.tavily_client import TavilyClient
from app.models.content_piece import ContentPiece
from app.models.marketing_memory import MarketingMemory
from app.models.pauta import Pauta
from app.models.tenant import TenantConfig
from app.models.user import User
from app.schemas.content_piece import (
    ContentPieceManualCreate,
    ContentPieceOut,
    ContentPieceUpdate,
    GerarRequest,
)
from app.services.agenda import agendar_conteudo_aprovado
from app.services.chaves_api import obter_chave
from app.services.cerebro import memorias_de_edicao, registrar_edicao
from app.services.verificacao_atualidade import verificar_atualidade

router = APIRouter(prefix="/content", tags=["content"])


def get_ai_client(openai_key: str | None = None) -> AIClient:
    """Gemini com a OpenAI de reserva (cota do Gemini estourada não trava a geração)."""
    return criar_ia(openai_key) or GeminiClient(api_key=settings.GEMINI_API_KEY)


VOZ_BLOCK = """\
REGRAS DE VOZ (inegociáveis, sempre aplicar):
{principios}

PROIBIÇÕES:
{proibicoes}

Identificação: {oab}
"""

PROMPTS = {
    "artigo": (
        "Escreva um artigo de blog completo (1200-1800 palavras) sobre '{titulo}' "
        "(ângulo: {angulo}, área: {area}). Estrutura: gancho, H2s com keyword, "
        "Perguntas frequentes, Leia também, 1 caso típico do escritório, 2 CTAs.\n"
        "{voz}\nResponda em JSON: {{\"titulo\": str, \"html\": str, "
        "\"meta_description\": str (até 155 caracteres, resumindo o artigo para SEO), "
        "\"resumo\": str (1-2 frases curtas, usadas como chamada nos cards do blog)}}"
    ),
    "carrossel": (
        "Crie um carrossel de Instagram sobre '{titulo}' (ângulo: {angulo}) usando "
        "a estrutura Value-Stack: slide 1 é a capa e compete sozinha no feed antes "
        "de alguém saber que é um carrossel — precisa declarar a quantidade exata "
        "de itens e a entrega exata (ex.: '5 direitos que...'), não um título vago. "
        "Slides do meio: um direito/dica por slide, direto, sem enrolação. Último "
        "slide: fecha o loop com uma ação clara (comente, salve, procure orientação). "
        "Entre 6 e 10 slides — o número da capa tem que bater exatamente com quantos "
        "slides de conteúdo existem, nunca arredondar pra cima com slide de enchimento. "
        "O último slide pede para salvar e mandar para quem precisa. Escreva também a "
        "legenda do post: gancho na primeira linha, 2 parágrafos curtos, convite para "
        "salvar e 5 hashtags do setor.\n"
        "{voz}\nResponda em JSON: {{\"slides\": [str, ...], \"legenda\": str}}"
    ),
    "legenda": (
        "Escreva a legenda do post de Instagram sobre '{titulo}' (ângulo: {angulo}). "
        "Gancho + 3 parágrafos + chamada para o blog + gancho do próximo post + "
        "5 hashtags específicas do tema, em CamelCase.\n"
        "{voz}\nResponda em JSON: {{\"texto\": str}}"
    ),
    "stories": (
        "Crie um roteiro de 3 stories (9:16) sobre '{titulo}' (ângulo: {angulo}): "
        "anúncio do tema, ponto principal, chamada para o link do blog.\n"
        "{voz}\nResponda em JSON: {{\"roteiro\": [str, str, str]}}"
    ),
    "reels": (
        "Roteirize um Reels/TikTok (formato vertical 9:16, 15-30 segundos) sobre "
        "'{titulo}' (ângulo: {angulo}). Regra dos 3 segundos: os 3 primeiros "
        "segundos precisam ter gancho visual + gancho falado + texto na tela "
        "batendo juntos, ou a pessoa passa o vídeo. Estrutura Problema-Solução: "
        "[0-3s] gancho declarando o problema; [3-10s] por que isso importa; "
        "[10-25s] a orientação/solução; [25-30s] CTA claro. Cada legenda de tela: "
        "no máximo 2 linhas, 3-5 palavras por linha, sincronizada com a fala. "
        "Sugira o tom/clima de áudio de tendência (ex.: 'batida crescente e "
        "tensa', 'som de suspense que resolve') para buscar na biblioteca nativa "
        "do Instagram/TikTok — não invente nome de música específica, já que não "
        "há acesso ao catálogo real de áudios da plataforma.\n"
        "{voz}\nResponda em JSON: {{\"gancho\": str, \"roteiro\": "
        "[{{\"tempo\": str, \"cena\": str, \"texto_tela\": str}}, ...], "
        "\"legenda\": str, \"cta\": str, \"audio_sugestao\": str}}"
    ),
    "estatico": (
        "Crie o briefing de uma arte estática única para Instagram/feed sobre "
        "'{titulo}' (ângulo: {angulo}). Defina o conceito visual (o que aparece "
        "na imagem), o texto de overlay (curto, direto, legível em miniatura), "
        "e a legenda do post. Formato quadrado ou 4:5, sem depender de vídeo ou "
        "carrossel.\n"
        "{voz}\nResponda em JSON: {{\"conceito_visual\": str, \"texto_overlay\": "
        "str, \"legenda\": str, \"cta\": str}}"
    ),
    "frase": (
        "Escreva uma frase de impacto para um card de Instagram sobre '{titulo}' "
        "(ângulo: {angulo}). No máximo 20 palavras, na primeira pessoa da advogada "
        "ou falando direto com a leitora, sem termo jurídico, feita para ser "
        "compartilhada. Marque com <em>...</em> as 2 a 4 palavras decisivas (ficam "
        "em dourado). Escreva também a legenda: 1 parágrafo que explica a frase e "
        "um convite para mandar a quem precisa ouvir isso.\n"
        "{voz}\nResponda em JSON: {{\"frase\": str, \"legenda\": str}}"
    ),
    "pergunta": (
        "Escreva a dúvida real de uma cliente sobre '{titulo}' (ângulo: {angulo}), "
        "do jeito que ela falaria no WhatsApp, em primeira pessoa e com no máximo "
        "18 palavras (ex.: 'Fui demitida grávida. E agora?'). A legenda responde a "
        "pergunta de forma curta e clara, sem juridiquês, e termina com 'Já passou "
        "por isso? Me conta nos comentários'.\n"
        "{voz}\nResponda em JSON: {{\"pergunta\": str, \"legenda\": str}}"
    ),
}

JORNAL_PROMPT = (
    "Você monta a edição semanal do 'Radar Jurídico da Semana', a partir do "
    "material já pesquisado e curado abaixo (ângulo principal: {angulo}, área: "
    "{area}). Escreva a edição em blocos: um resumo de abertura (100-180 "
    "palavras), 'Destaque da Semana' (a decisão principal, '{titulo}'), "
    "'Direito do Trabalho', 'Direito de Família', 'O que isso muda na "
    "prática?', 'Julgamentos para acompanhar' e 'Fontes oficiais' (tribunal, "
    "processo/tema, data e link, quando o material trouxer). Nunca invente "
    "decisão, número de processo, data, tribunal, súmula ou resultado que não "
    "esteja no material.\n"
    "{voz}\n"
    "MATERIAL JÁ PESQUISADO (única fonte permitida — não pesquise nada além "
    "disso):\n{material}\n\n"
    "Responda em JSON: {{\"titulo\": str, \"html\": str, "
    "\"meta_description\": str (até 155 caracteres), "
    "\"resumo\": str (1-2 frases para o card/CTA)}}"
)

RADAR_ORIGENS_MANCHETE = {"radar_juridico_manchete", "jornalista_manchete"}


@router.post("/gerar", response_model=list[ContentPieceOut])
async def gerar_conteudo(
    payload: GerarRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[ContentPiece]:
    ai_client = get_ai_client(await obter_chave(db, current_user.tenant_id, "openai"))

    pauta_result = await db.execute(
        select(Pauta).where(
            Pauta.id == payload.pauta_id, Pauta.tenant_id == current_user.tenant_id
        )
    )
    pauta = pauta_result.scalar_one_or_none()
    if pauta is None:
        raise HTTPException(status_code=404, detail="Pauta not found")

    config_result = await db.execute(
        select(TenantConfig).where(TenantConfig.tenant_id == current_user.tenant_id)
    )
    tenant_config = config_result.scalar_one_or_none()
    voz_data = tenant_config.voz if tenant_config else {}
    voz_block = VOZ_BLOCK.format(
        principios="\n".join(f"- {p}" for p in voz_data.get("principios", [])),
        proibicoes="\n".join(f"- {p}" for p in voz_data.get("proibicoes", [])),
        oab=voz_data.get("oab", ""),
    )

    licoes = await memorias_de_edicao(db, current_user.tenant_id)

    def _com_licoes(prompt: str) -> str:
        if not licoes:
            return prompt
        return prompt + (
            "\n\nLIÇÕES DE EDIÇÕES ANTERIORES (a cliente corrigiu estes pontos "
            "em conteúdos passados — evite repetir):\n" + licoes
        )

    pieces = []
    for tipo, template in PROMPTS.items():
        prompt = template.format(
            titulo=pauta.titulo, angulo=pauta.angulo, area=pauta.area, voz=voz_block
        )
        if pauta.conteudo_bruto:
            prompt += (
                "\n\nMATERIAL JÁ PESQUISADO (use como fonte principal — não "
                "invente decisão, número de processo, data ou tribunal além do "
                "que está aqui):\n" + pauta.conteudo_bruto
            )
        corpo = await ai_client.generate_json(_com_licoes(prompt))
        piece = ContentPiece(
            tenant_id=current_user.tenant_id,
            pauta_id=pauta.id,
            tipo=tipo,
            corpo=corpo,
            status="rascunho",
            versao=1,
        )
        db.add(piece)
        pieces.append(piece)

    if pauta.origem in RADAR_ORIGENS_MANCHETE and pauta.conteudo_bruto:
        prompt = JORNAL_PROMPT.format(
            titulo=pauta.titulo,
            angulo=pauta.angulo,
            area=pauta.area,
            voz=voz_block,
            material=pauta.conteudo_bruto,
        )
        corpo = await ai_client.generate_json(_com_licoes(prompt))
        jornal_piece = ContentPiece(
            tenant_id=current_user.tenant_id,
            pauta_id=pauta.id,
            tipo="jornal",
            corpo=corpo,
            status="rascunho",
            versao=1,
        )
        db.add(jornal_piece)
        pieces.append(jornal_piece)

    if pauta.status in ("sugerida", "aprovada", "guardada"):
        pauta.status = "em_producao"
    await db.commit()
    for p in pieces:
        await db.refresh(p)
    return pieces


@router.get("", response_model=list[ContentPieceOut])
async def listar_content_pieces(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    tipo: str | None = None,
    status: str | None = None,
    pauta_id: uuid.UUID | None = None,
) -> list[ContentPiece]:
    query = select(ContentPiece).where(ContentPiece.tenant_id == current_user.tenant_id)
    if tipo is not None:
        query = query.where(ContentPiece.tipo == tipo)
    if status is not None:
        query = query.where(ContentPiece.status == status)
    if pauta_id is not None:
        query = query.where(ContentPiece.pauta_id == pauta_id)
    query = query.order_by(ContentPiece.criado_em.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("", response_model=ContentPieceOut, status_code=201)
async def criar_content_piece_manual(
    payload: ContentPieceManualCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ContentPiece:
    pauta_result = await db.execute(
        select(Pauta).where(
            Pauta.id == payload.pauta_id, Pauta.tenant_id == current_user.tenant_id
        )
    )
    if pauta_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Pauta not found")

    piece = ContentPiece(
        tenant_id=current_user.tenant_id,
        pauta_id=payload.pauta_id,
        tipo=payload.tipo,
        corpo=payload.corpo,
        status=payload.status,
        versao=1,
    )
    db.add(piece)
    await db.commit()
    await db.refresh(piece)
    return piece


@router.patch("/{piece_id}", response_model=ContentPieceOut)
async def atualizar_content_piece(
    piece_id: str,
    payload: ContentPieceUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ContentPiece:
    try:
        piece_uuid = uuid.UUID(piece_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid piece_id")

    result = await db.execute(
        select(ContentPiece).where(
            ContentPiece.id == piece_uuid, ContentPiece.tenant_id == current_user.tenant_id
        )
    )
    piece = result.scalar_one_or_none()
    if piece is None:
        raise HTTPException(status_code=404, detail="Content piece not found")

    if payload.corpo is not None and payload.corpo != piece.corpo:
        await registrar_edicao(db, piece, payload.corpo)
        piece.corpo = payload.corpo
    if payload.status is not None:
        piece.status = payload.status

    if payload.status == "aprovado":
        pauta_result = await db.execute(
            select(Pauta).where(
                Pauta.id == piece.pauta_id,
                Pauta.tenant_id == current_user.tenant_id,
            )
        )
        pauta = pauta_result.scalar_one()
        if settings.TAVILY_API_KEY:
            alerta, verificado_em = await verificar_atualidade(
                titulo=pauta.titulo,
                area=pauta.area,
                ai_client=GroqClient(api_key=settings.GROQ_API_KEY),
                tavily_client=TavilyClient(api_key=settings.TAVILY_API_KEY),
            )
            piece.alerta_atualidade = alerta
            piece.verificado_em = verificado_em
        db.add(
            MarketingMemory(
                tenant_id=current_user.tenant_id,
                content_piece_id=piece.id,
                tema=pauta.titulo,
                angulo=pauta.angulo,
                formato=piece.tipo,
                metricas={},
                aprendizado=None,
            )
        )
        await agendar_conteudo_aprovado(db, piece)

    await db.commit()
    await db.refresh(piece)
    return piece
