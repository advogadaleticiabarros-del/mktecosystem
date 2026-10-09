from datetime import date, datetime, timezone

import httpx
import pytest

from app.integrations.social.instagram_api import InstagramAPI
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant
from app.services.grade_instagram import montar_grade

HOJE = date(2026, 10, 9)


async def _base(db):
    t = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(t)
    await db.flush()
    p = Pauta(tenant_id=t.id, titulo="Tema", angulo="direitos", area="Trabalhista", origem="manual",
              fonte="manual", relevante_para_conteudo=True)
    db.add(p)
    await db.flush()
    return t, p


def _peca(t, p, tipo, corpo, status="aprovado"):
    return ContentPiece(tenant_id=t.id, pauta_id=p.id, tipo=tipo, corpo=corpo, status=status)


class LeitorFalso:
    def __init__(self, posts):
        self.posts = posts

    async def recentes(self):
        return self.posts


@pytest.mark.anyio
async def test_grade_junta_agendados_rascunhos_e_publicados_do_mais_novo_para_o_mais_antigo(db_session):
    t, p = await _base(db_session)
    agendada = _peca(t, p, "carrossel", {"imagens": ["https://x/c1.jpg", "https://x/c2.jpg"], "legenda": "Leg C",
                                         "primeiro_comentario": "PC"})
    rascunho = _peca(t, p, "pergunta", {"imagem": "https://x/q.jpg", "legenda": "Leg Q",
                                        "programacao": {"data": "2026-10-15", "hora": "12:00"}}, status="rascunho")
    story = _peca(t, p, "stories", {"imagem": "https://x/s.jpg"})
    db_session.add_all([agendada, rascunho, story])
    await db_session.flush()
    db_session.add_all([
        ScheduledPost(tenant_id=t.id, content_piece_id=agendada.id, titulo="T", canal="instagram", formato="carrossel",
                      data_agendada=date(2026, 10, 11), horario="20:00", status="pronto"),
        ScheduledPost(tenant_id=t.id, content_piece_id=story.id, titulo="T", canal="instagram", formato="story",
                      data_agendada=date(2026, 10, 11), horario="10:00", status="pronto"),
    ])
    await db_session.commit()
    leitor = LeitorFalso([{"timestamp": "2026-10-08T22:00:16+0000", "media_url": "https://cdn/p.jpg", "caption": "Publicado",
                           "permalink": "https://instagram.com/p/x", "media_type": "IMAGE"}])

    grade = await montar_grade(db_session, t.id, leitor, HOJE)

    assert [(g.data, g.hora, g.status) for g in grade] == [
        ("2026-10-15", "12:00", "rascunho"),
        ("2026-10-11", "20:00", "agendado"),
        ("2026-10-08", "19:00", "publicado"),
    ]
    assert grade[1].imagens == ["https://x/c1.jpg", "https://x/c2.jpg"]
    assert grade[1].primeiro_comentario == "PC"
    assert grade[2].permalink == "https://instagram.com/p/x"


@pytest.mark.anyio
async def test_sem_instagram_conectado_mostra_so_o_que_esta_no_orbit(db_session):
    t, p = await _base(db_session)
    db_session.add(_peca(t, p, "frase", {"imagem": "https://x/f.jpg", "programacao": {"data": "2026-10-20", "hora": "15:00"}},
                         status="rascunho"))
    await db_session.commit()

    grade = await montar_grade(db_session, t.id, None, HOJE)

    assert [(g.data, g.tipo) for g in grade] == [("2026-10-20", "frase")]


@pytest.mark.anyio
async def test_leitor_que_falha_nao_derruba_a_grade(db_session):
    t, p = await _base(db_session)
    db_session.add(_peca(t, p, "frase", {"imagem": "https://x/f.jpg", "programacao": {"data": "2026-10-20", "hora": "15:00"}},
                         status="rascunho"))
    await db_session.commit()

    class Quebrado:
        async def recentes(self):
            raise RuntimeError("Meta fora do ar")

    grade = await montar_grade(db_session, t.id, Quebrado(), HOJE)

    assert len(grade) == 1


@pytest.mark.anyio
async def test_instagram_api_lista_posts_com_imagem():
    def responder(request: httpx.Request) -> httpx.Response:
        assert "media_url" in request.url.params["fields"]
        return httpx.Response(200, json={"data": [{"id": "1", "media_url": "https://cdn/a.jpg"}]})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    assert await api.posts_com_imagem("999", 12) == [{"id": "1", "media_url": "https://cdn/a.jpg"}]


@pytest.mark.anyio
async def test_endpoint_da_grade_responde_sem_instagram_conectado(client, db_session):
    from app.core.security import create_access_token, hash_password
    from app.models.user import User

    t, p = await _base(db_session)
    u = User(tenant_id=t.id, email="l@x.com", nome="L", hashed_password=hash_password("x"), role="owner")
    db_session.add(u)
    db_session.add(_peca(t, p, "frase", {"imagem": "https://x/f.jpg", "programacao": {"data": "2099-01-01", "hora": "15:00"}},
                         status="rascunho"))
    await db_session.commit()

    resp = await client.get("/calendario/grade", headers={"Authorization": f"Bearer {create_access_token(u.id)}"})

    assert resp.status_code == 200
    assert resp.json()[0]["tipo"] == "frase"
