from unittest.mock import patch

import pytest

from app.services.radar_juridico import Achado
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


@pytest.mark.anyio
async def test_buscar_pautas_roda_o_radar_juridico(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    class Pesquisador:
        async def pesquisar(self, areas, evitar, hoje):
            return [
                Achado("Revisão de benefício por incapacidade", "resumo", "Previdenciário",
                       "direitos", "STF", "https://stf", True),
                Achado("Alteração de rito em recurso especial", "resumo", "Processual",
                       "sinceridade", "STJ", "https://stj", False),
            ]

    with patch("app.routers.pautas.criar_pesquisador", return_value=Pesquisador()):
        response = await client.post(
            "/pautas/buscar", headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {p["fonte"] for p in body} == {"STF", "STJ"}
    assert all(p["origem"].startswith("radar_juridico") for p in body)


@pytest.mark.anyio
async def test_buscar_pautas_sem_chave_de_pesquisa_retorna_503(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    with patch("app.routers.pautas.criar_pesquisador", return_value=None):
        response = await client.post(
            "/pautas/buscar", headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 503


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
