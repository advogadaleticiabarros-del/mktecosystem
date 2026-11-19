"""(19/11/2026) Publica o artigo das dúvidas do decreto da 5x2. Cópia do publicador de 16/11.
Publica os artigos pelo publicador oficial do Orbit (roda dentro do contêiner vps-api-1).

Uso: python publicar.py /tmp/spec.json
Cria Pauta + ContentPiece (aprovado) + ScheduledPost (blog, pronto, hoje) e chama publicar_agendamentos_prontos,
que gera HTML, capa, card no índice, sitemap, llms.txt e avisa Bing/IndexNow. Depois troca o <title> pelo título
curto do Google. Faz backup do índice, sitemap e llms.txt antes.
"""
import asyncio
import io
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx
from PIL import Image
from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant
from app.services.agendamento_horario import hoje_brasilia
from app.services.blog_publisher import MEDIA_DIR, publicar_agendamentos_prontos
from app.services.central_google import _site_padrao

FOTOS = {  # Pexels, escolhida em 19/11/2026 (a mesma da capa do carrossel do decreto)
    "escala-5x2-decreto-duvidas": 3801439,  # caixa no balcão
}


async def capa(slug: str) -> None:
    async with httpx.AsyncClient(timeout=60, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}) as c:
        url = f"https://images.pexels.com/photos/{FOTOS[slug]}/pexels-photo-{FOTOS[slug]}.jpeg?auto=compress&w=1600"
        im = Image.open(io.BytesIO((await c.get(url)).content)).convert("RGB")
    r = max(1200 / im.width, 630 / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)))
    x, y = (im.width - 1200) // 2, int((im.height - 630) * 0.4)
    im.crop((x, y, x + 1200, y + 630)).save(MEDIA_DIR / f"capa-{slug}.jpg", "JPEG", quality=86)


async def main(caminho_spec: str) -> None:
    spec = json.load(open(caminho_spec, encoding="utf-8"))
    MEDIA_DIR.mkdir(exist_ok=True)
    site = _site_padrao()
    bkp = Path(f"/tmp/bkp_blog_{datetime.now():%Y%m%d-%H%M%S}")
    bkp.mkdir()
    for arq in ("blog/index.html", "sitemap.xml", "llms.txt"):
        (bkp / arq.replace("/", "__")).write_text(await site.ler(arq) or "", encoding="utf-8")
    print("backup", bkp)

    async with SessionLocal() as db:
        tenant = (await db.execute(select(Tenant))).scalars().first()
        for a in spec:
            ja = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "artigo"))).scalars().all()
            assert not any((p.corpo or {}).get("slug") == a["slug"] for p in ja), f"já existe: {a['slug']}"
            await capa(a["slug"])
            pauta = Pauta(tenant_id=tenant.id, titulo=a["titulo"], angulo="educativo", area="Trabalhista",
                          origem="manual", fonte="Pesquisa de 19/11/2026 (EC 141, Decreto 13.173, liminar STF 12/11)",
                          relevante_para_conteudo=True, status="aprovada", data_editorial=hoje_brasilia(),
                          verificado_em=datetime.now(timezone.utc))
            db.add(pauta)
            await db.flush()
            piece = ContentPiece(tenant_id=tenant.id, pauta_id=pauta.id, tipo="artigo", status="aprovado",
                                 verificado_em=datetime.now(timezone.utc),
                                 corpo={"titulo": a["titulo"], "slug": a["slug"],
                                        "meta_description": a["meta_description"], "resumo": a["resumo"],
                                        "html": a["html"], "capa_arquivo": f"capa-{a['slug']}.jpg"})
            db.add(piece)
            await db.flush()
            db.add(ScheduledPost(tenant_id=tenant.id, content_piece_id=piece.id, titulo=a["titulo"], canal="blog",
                                 formato="artigo", data_agendada=hoje_brasilia(), horario="00:00", status="pronto"))
        await db.commit()
        n = await publicar_agendamentos_prontos(db)
        print("publicados", n)

    sftp, raiz = site._sftp, site._raiz
    for a in spec:
        html = await site.ler(f"blog/{a['slug']}.html")
        velho = f"<title>{a['titulo']} | Dra. Letícia Barros</title>"
        if html.count(velho) == 1:
            html = html.replace(velho, f"<title>{a['titulo_google']} | Dra. Letícia Barros</title>")
            await sftp.upload(f"{raiz}/blog/{a['slug']}.html", html.encode("utf-8"))
            print("title ok", a["slug"])
        else:
            print("AVISO title não encontrado", a["slug"])


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
