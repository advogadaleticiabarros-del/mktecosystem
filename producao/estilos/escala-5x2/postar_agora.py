"""(19/11/2026) Publica AGORA no Instagram o carrossel "Decreto da escala 5x2 assinado", a pedido da Jessica ("post",
"Ainda não, poste você"). Roda dentro do contêiner vps-api-1, com as 8 artes já copiadas para /app/media.

Cria Pauta + ContentPiece (carrossel, aprovado, imagens enviadas) + ScheduledPost (instagram, carrossel, hoje, pronto)
e publica só este agendamento, com a mesma sequência do instagram_publisher (carrossel + primeiro comentário).
Idempotente: se a peça já existir publicada, não publica de novo.
Uso: python postar_agora.py /tmp/editorial5x2.json"""
import asyncio
import json
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import select

from app.config import settings
from app.core.crypto import decrypt_token
from app.db import SessionLocal
from app.integrations.social.instagram_api import InstagramAPI
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant
from app.services.agendamento_horario import hoje_brasilia
from app.services.instagram_publisher import MEDIA_DIR, _conexao_ativa

TITULO = "Decreto da escala 5x2 assinado"
NOMES = [f"escala-5x2-v1-{i}.jpg" for i in range(1, 9)]


async def main(caminho: str) -> None:
    ed = json.load(open(caminho, encoding="utf-8"))[0]
    for n in NOMES:
        assert (MEDIA_DIR / n).is_file(), f"falta {n} em {MEDIA_DIR}"
    imagens = [f"{settings.PUBLIC_API_URL}/media/{n}" for n in NOMES]
    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        ja = (await db.execute(select(ContentPiece).where(ContentPiece.tenant_id == tid, ContentPiece.tipo == "carrossel",
                                                          ContentPiece.corpo["imagens"][0].as_string() == imagens[0]))).scalars().first()
        if ja and ja.status == "publicado":
            raise SystemExit("já publicado; nada feito")
        if ja is None:
            pauta = Pauta(tenant_id=tid, titulo=TITULO, angulo="direitos", area="Trabalhista", origem="manual",
                          fonte="Referência do TST (instagram.com/p/Df7ZFwQhh2r); Decreto 13.173 de 19/11/2026",
                          relevante_para_conteudo=True, status="em_producao", data_editorial=hoje_brasilia())
            db.add(pauta)
            await db.flush()
            ja = ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="carrossel", status="aprovado", versao=1,
                              corpo={"imagens": imagens, "legenda": ed["legenda"],
                                     "primeiro_comentario": ed["primeiro_comentario"], "estilo": "escala-5x2",
                                     "rotulo_ia": False, "programacao": {"data": hoje_brasilia().isoformat(),
                                                                        "hora": f"{agora:%H:%M}"}})
            db.add(ja)
            await db.flush()
        ag = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == ja.id))).scalars().first()
        if ag is None:
            ag = ScheduledPost(tenant_id=tid, content_piece_id=ja.id, titulo=TITULO, canal="instagram", formato="carrossel",
                               data_agendada=hoje_brasilia(), horario=f"{agora:%H:%M}", status="pronto")
            db.add(ag)
        await db.commit()

        conexao = await _conexao_ativa(db, tid)
        assert conexao, "sem conexão Instagram ativa"
        api = InstagramAPI(page_token=decrypt_token(conexao.access_token_encrypted))
        post_id = await api.publicar_carrossel(conexao.ig_user_id, imagens, legenda=ed["legenda"],
                                               location_id=settings.INSTAGRAM_LOCATION_ID or None)
        ag.status, ag.platform_post_id, ja.status = "publicado", post_id, "publicado"
        await db.commit()
        print("publicado", post_id)
        try:
            await api.comentar(post_id, ed["primeiro_comentario"])
            print("primeiro comentário ok")
        except Exception as e:  # o post já está no ar; não republicar
            print("AVISO comentário falhou:", e)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
