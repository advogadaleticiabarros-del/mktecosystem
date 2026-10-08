from unittest.mock import patch

import pytest

import json

from app.integrations.noticias.base import Noticia
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User
from app.core.security import hash_password, create_access_token


async def _make_tenant_and_user(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(
        TenantConfig(
            tenant_id=tenant.id,
            voz={"areas": ["Trabalhista", "Previdenciário"]},
            identidade_visual={},
            ctas={},
            regras_compliance={},
            canais={},
        )
    )
    user = User(
        tenant_id=tenant.id,
        email="leticia@example.com",
        nome="Letícia",
        hashed_password=hash_password("senha"),
        role="owner",
    )
    db_session.add(user)
    await db_session.commit()
    return tenant, user


class _Buscador:
    async def buscar(self, consulta, dias):
        return [Noticia("TST garante estabilidade a gestante temporária", "https://tst.jus.br/a", "TST", "trecho", None)]


class _Redator:
    def __init__(self):
        self.prompts = []

    async def generate_text(self, prompt):
        self.prompts.append(prompt)
        return json.dumps({"pautas": [{
            "grupos": [1], "manchete": "Gestante temporária tem estabilidade", "gancho": "g", "fatos": "f",
            "o_que_muda": "m", "area": "Trabalhista", "angulo": "direitos", "urgencia": "alta",
            "relevancia": 80, "relevante_para_conteudo": True, "formatos": {},
        }]})


@pytest.mark.anyio
async def test_buscar_pautas_roda_o_jornalista(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    with patch("app.routers.pautas.criar_jornalista", return_value=(_Buscador(), _Redator())):
        response = await client.post("/pautas/buscar", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["origem"].startswith("jornalista")
    assert body[0]["urgencia"] == "alta"
    assert body[0]["apuracao"]["verificacao"]["nivel"] == "oficial"
    assert body[0]["relevancia"] == 85


@pytest.mark.anyio
async def test_pedido_ao_jornalista_com_foco(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)
    redator = _Redator()

    with patch("app.routers.pautas.criar_jornalista", return_value=(_Buscador(), redator)):
        response = await client.post(
            "/pautas/jornalista", json={"foco": "estabilidade da gestante"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    assert response.json()[0]["apuracao"]["pedido"] == "estabilidade da gestante"
    assert "estabilidade da gestante" in redator.prompts[0]


@pytest.mark.anyio
async def test_jornalista_sem_chave_retorna_503(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    with patch("app.routers.pautas.criar_jornalista", return_value=None):
        response = await client.post("/pautas/buscar", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 503


@pytest.mark.anyio
async def test_mudar_status_da_pauta(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    headers = {"Authorization": f"Bearer {create_access_token(user.id)}"}
    criada = (await client.post("/pautas", json={"titulo": "T", "angulo": "direitos", "area": "Família"},
                                headers=headers)).json()

    ok = await client.patch(f"/pautas/{criada['id']}", json={"status": "guardada"}, headers=headers)
    invalido = await client.patch(f"/pautas/{criada['id']}", json={"status": "qualquer"}, headers=headers)

    assert ok.status_code == 200 and ok.json()["status"] == "guardada"
    assert invalido.status_code == 422


@pytest.mark.anyio
async def test_list_pautas_filters_by_relevante_para_conteudo(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    from app.models.pauta import Pauta

    db_session.add_all(
        [
            Pauta(
                tenant_id=tenant.id, titulo="Pauta de conteúdo", angulo="direitos",
                area="Trabalhista", origem="buscada", fonte="CNJ",
                relevante_para_conteudo=True, status="sugerida",
            ),
            Pauta(
                tenant_id=tenant.id, titulo="Pauta só informativa", angulo="tecnico",
                area="Processual", origem="buscada", fonte="CNJ",
                relevante_para_conteudo=False, status="sugerida",
            ),
        ]
    )
    await db_session.commit()

    response = await client.get(
        "/pautas", params={"relevante_para_conteudo": "true"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["titulo"] == "Pauta de conteúdo"


@pytest.mark.anyio
async def test_create_manual_pauta(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    response = await client.post(
        "/pautas",
        json={
            "titulo": "BPC/LOAS negado por erro no CadÚnico",
            "angulo": "direitos",
            "area": "Previdenciário",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["origem"] == "manual"
    assert body["relevante_para_conteudo"] is True


@pytest.mark.anyio
async def test_criar_pauta_de_radar_com_conteudo_bruto(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    response = await client.post(
        "/pautas",
        json={
            "titulo": "NR-1 e riscos psicossociais: o que muda após decisão do STF",
            "angulo": "direitos",
            "area": "Trabalhista",
            "origem": "radar_juridico_manchete",
            "conteudo_bruto": "STF confirma suspensão temporária das multas da NR-1...",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["origem"] == "radar_juridico_manchete"
    assert body["fonte"] == "chatgpt-radar"
    assert body["conteudo_bruto"] == "STF confirma suspensão temporária das multas da NR-1..."
