from datetime import datetime, timedelta, timezone

import httpx
import pytest
from sqlalchemy import select

from app.integrations.social.instagram_api import InstagramAPI
from app.models.pauta import Pauta
from app.models.tenant import Tenant
from app.services.radar_referencias import PostReferencia, vigiar

AGORA = datetime(2026, 10, 8, 12, tzinfo=timezone.utc)


def _p(perfil, legenda, curtidas, comentarios=0, dias=1, link=None):
    return PostReferencia(
        perfil=perfil, legenda=legenda, formato="CAROUSEL_ALBUM", curtidas=curtidas, comentarios=comentarios,
        publicado_em=AGORA - timedelta(days=dias), link=link or f"https://instagram.com/p/{perfil}{curtidas}{dias}",
    )


class LeitorFalso:
    def __init__(self, posts_por_perfil, falhar=()):
        self.posts = posts_por_perfil
        self.falhar = falhar

    async def posts_recentes(self, perfil):
        if perfil in self.falhar:
            raise RuntimeError("perfil indisponível")
        return self.posts.get(perfil, [])


async def _tenant(db):
    t = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(t)
    await db.commit()
    return t


def _normais(perfil, n=6):
    return [_p(perfil, f"Post comum {i}. Sem destaque.", 100 + i) for i in range(n)]


@pytest.mark.anyio
async def test_post_muito_acima_da_media_do_perfil_vira_pauta(db_session):
    t = await _tenant(db_session)
    destaque = _p("atualizacao_trabalhista", "STF fixa tese sobre FGTS na rescisão. Entenda o que muda.", 900, 50)
    leitor = LeitorFalso({"atualizacao_trabalhista": _normais("atualizacao_trabalhista") + [destaque]})

    pautas = await vigiar(db_session, t.id, leitor, ["atualizacao_trabalhista"], AGORA)

    assert len(pautas) == 1
    p = pautas[0]
    assert p.titulo == "STF fixa tese sobre FGTS na rescisão"
    assert p.origem == "referencia_instagram"
    assert p.fonte == "@atualizacao_trabalhista"
    assert p.status == "sugerida"
    assert p.data_editorial is None
    assert p.area == "Trabalhista"
    assert p.apuracao["link"] == destaque.link
    assert "não repostar" in p.conteudo_bruto.lower()


@pytest.mark.anyio
async def test_nao_repete_post_ja_sugerido(db_session):
    t = await _tenant(db_session)
    destaque = _p("diariojustica", "Banco deve devolver Pix de golpe, decide STJ.", 900, 40)
    leitor = LeitorFalso({"diariojustica": _normais("diariojustica") + [destaque]})

    await vigiar(db_session, t.id, leitor, ["diariojustica"], AGORA)
    segunda = await vigiar(db_session, t.id, leitor, ["diariojustica"], AGORA)

    assert segunda == []
    total = (await db_session.execute(select(Pauta))).scalars().all()
    assert len(total) == 1
    assert total[0].area == "Consumidor"


@pytest.mark.anyio
async def test_ignora_post_antigo_e_limita_por_perfil(db_session):
    t = await _tenant(db_session)
    antigos = [_p("trtespiritosanto", "Decisão antiga bombou.", 5000, dias=6)]
    destaques = [_p("trtespiritosanto", f"Tema forte número {i}.", 2000 + i, 30) for i in range(5)]
    leitor = LeitorFalso({"trtespiritosanto": _normais("trtespiritosanto", 10) + antigos + destaques})

    pautas = await vigiar(db_session, t.id, leitor, ["trtespiritosanto"], AGORA)

    assert len(pautas) == 3
    assert all("antiga" not in p.titulo for p in pautas)
    assert pautas[0].relevancia >= pautas[-1].relevancia


@pytest.mark.anyio
async def test_perfil_que_falha_nao_derruba_os_outros(db_session):
    t = await _tenant(db_session)
    destaque = _p("diariojustica", "Pensão alimentícia: STJ muda cálculo.", 900, 40)
    leitor = LeitorFalso({"diariojustica": _normais("diariojustica") + [destaque]}, falhar={"atualizacao_trabalhista"})

    pautas = await vigiar(db_session, t.id, leitor, ["atualizacao_trabalhista", "diariojustica"], AGORA)

    assert [p.fonte for p in pautas] == ["@diariojustica"]
    assert pautas[0].area == "Família"


@pytest.mark.anyio
async def test_instagram_api_le_perfil_publico_via_business_discovery():
    pedidos = []

    def responder(request: httpx.Request) -> httpx.Response:
        pedidos.append(dict(request.url.params))
        return httpx.Response(200, json={"business_discovery": {"media": {"data": [
            {"caption": "Legenda", "media_type": "IMAGE", "like_count": 10, "comments_count": 2,
             "timestamp": "2026-10-07T15:00:00+0000", "permalink": "https://instagram.com/p/x"},
        ]}}})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    posts = await api.posts_de_perfil_publico("999", "diariojustica")

    assert "business_discovery.username(diariojustica)" in pedidos[0]["fields"]
    assert posts == [{"caption": "Legenda", "media_type": "IMAGE", "like_count": 10, "comments_count": 2,
                      "timestamp": "2026-10-07T15:00:00+0000", "permalink": "https://instagram.com/p/x"}]
