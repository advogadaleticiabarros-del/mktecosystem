"""Roda DENTRO do container da API: sobe os Reels antigos (01 a 11, anteriores ao padrão motion) como RASCUNHO, sem
data, para a Letícia ver e decidir no Estúdio de criativos (pedido de 15/10/2026: "quero tudo que produzimos lá").
Vídeos convertidos para o formato da API da Meta (H.264, AAC 128 kbps, faststart) e copiados para /app/media.
Muitos já podem ter sido postados: a legenda da peça avisa para conferir antes de aprovar. Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/subir_acervo_reels.py
"""
import asyncio

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant

ACERVO = [
    ("acervo-01-folga-jogo", "Folga em dia de jogo do Brasil", "Trabalhista"),
    ("acervo-02-insalubridade", "Insalubridade: quem tem direito", "Trabalhista"),
    ("acervo-03-gestante-demitida", "Gestante demitida: o que fazer", "Trabalhista"),
    ("acervo-04-guarda-compartilhada", "Guarda compartilhada", "Família"),
    ("acervo-05-institucional", "Reels institucional (gravação da Dra. Letícia)", "Institucional"),
    ("acervo-06-3-erros-demissao", "3 erros que fazem você perder direitos na demissão", "Trabalhista"),
    ("acervo-07-assedio-moral-sinais", "Assédio moral: 3 sinais que ninguém te conta", "Trabalhista"),
    ("acervo-08-reel-08", "Reels 08 (gravação da Dra. Letícia)", "Institucional"),
    ("acervo-09-dia-do-advogado", "Dia do Advogado (vídeo longo, 5 min 36 s)", "Institucional"),
    ("acervo-10-gestante-aviso-previo", "Engravidou durante o aviso prévio?", "Trabalhista"),
    ("acervo-11-aviso-previo-broll", "Gestante e aviso prévio (versão com imagens reais)", "Trabalhista"),
]

AVISO = ("ACERVO: Reels produzido antes do padrão atual (motion v2). Confira se ele já foi postado antes de aprovar. "
         "Se quiser reaproveitar, use \"Pedir ajuste\" para pedir legenda nova, corte ou nova versão no padrão atual.")


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        n = 0
        for arquivo, tema, area in ACERVO:
            titulo = f"Acervo de Reels: {tema}"
            p = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == titulo))).scalars().first()
            if not p:
                p = Pauta(tenant_id=tid, titulo=titulo, angulo="reels", area=area, origem="manual",
                          fonte="Acervo de Reels (C:/tmp/videos-reels)", relevante_para_conteudo=True, status="em_producao")
                db.add(p)
                await db.flush()
            ja = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == p.id, ContentPiece.tipo == "reels"))).scalars().first()
            if ja:
                continue
            db.add(ContentPiece(tenant_id=tid, pauta_id=p.id, tipo="reels", status="rascunho", versao=1, corpo={
                "video": f"{settings.PUBLIC_API_URL}/media/{arquivo}.mp4?v=acervo1", "legenda": AVISO, "acervo": True}))
            n += 1
        await db.commit()
        print("reels do acervo criados:", n)


asyncio.run(main())
