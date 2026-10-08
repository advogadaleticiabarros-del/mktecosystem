from unittest.mock import AsyncMock, patch

import pytest

from app.core.security import create_access_token, hash_password
from app.models.pauta import Pauta
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User

TIPOS_PADRAO = ["artigo", "carrossel", "legenda", "stories", "reels", "estatico", "frase", "pergunta"]

FAKE_RESULTS_PADRAO = {
    "artigo": {"titulo": "Tema", "html": "<p>artigo</p>"},
    "carrossel": {"slides": ["s1", "s2", "s3", "s4", "s5", "s6"]},
    "legenda": {"texto": "legenda aqui"},
    "stories": {"roteiro": ["frame 1", "frame 2", "frame 3"]},
    "reels": {
        "gancho": "gancho",
        "roteiro": [{"tempo": "0-3s", "cena": "cena", "texto_tela": "texto"}],
        "legenda": "legenda reels",
        "cta": "cta",
        "audio_sugestao": "batida crescente",
    },
    "estatico": {
        "conceito_visual": "conceito",
        "texto_overlay": "overlay",
        "legenda": "legenda estatico",
        "cta": "cta",
    },
    "frase": {"frase": "Pensão não é <em>ajuda</em>.", "legenda": "legenda frase"},
    "pergunta": {"pergunta": "Fui demitida grávida. E agora?", "legenda": "resposta na legenda"},
}


@pytest.mark.anyio
async def test_gerar_creates_seis_content_pieces(client, db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(
        TenantConfig(
            tenant_id=tenant.id,
            voz={"principios": ["Sem juridiquês"], "oab": "OAB/ES 39.948"},
            identidade_visual={}, ctas={}, regras_compliance={}, canais={},
        )
    )
    user = User(
        tenant_id=tenant.id, email="l@example.com", nome="L",
        hashed_password=hash_password("senha"), role="owner",
    )
    db_session.add(user)
    pauta = Pauta(
        tenant_id=tenant.id, titulo="BPC/LOAS em 2026", angulo="direitos",
        area="Previdenciário", origem="manual", fonte="manual",
        relevante_para_conteudo=True, status="sugerida",
    )
    db_session.add(pauta)
    await db_session.commit()

    token = create_access_token(user.id)

    with patch("app.routers.content.get_ai_client") as mock_get_ai:
        mock_ai = AsyncMock()
        mock_ai.generate_json.side_effect = [FAKE_RESULTS_PADRAO[t] for t in TIPOS_PADRAO]
        mock_get_ai.return_value = mock_ai

        response = await client.post(
            "/content/gerar",
            json={"pauta_id": str(pauta.id)},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    body = response.json()
    tipos = {piece["tipo"] for piece in body}
    assert tipos == set(TIPOS_PADRAO)
    await db_session.refresh(pauta)
    assert pauta.status == "em_producao"
    assert all(piece["status"] == "rascunho" for piece in body)


@pytest.mark.anyio
async def test_gerar_pauta_manchete_do_radar_cria_tambem_o_jornal(client, db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(
        TenantConfig(
            tenant_id=tenant.id,
            voz={"principios": ["Sem juridiquês"], "oab": "OAB/ES 39.948"},
            identidade_visual={}, ctas={}, regras_compliance={}, canais={},
        )
    )
    user = User(
        tenant_id=tenant.id, email="l2@example.com", nome="L",
        hashed_password=hash_password("senha"), role="owner",
    )
    db_session.add(user)
    pauta = Pauta(
        tenant_id=tenant.id, titulo="NR-1 e riscos psicossociais", angulo="direitos",
        area="Trabalhista", origem="radar_juridico_manchete", fonte="chatgpt-radar",
        relevante_para_conteudo=True, status="sugerida",
        conteudo_bruto="STF confirma suspensão temporária das multas da NR-1...",
    )
    db_session.add(pauta)
    await db_session.commit()

    token = create_access_token(user.id)

    jornal = {"titulo": "Radar Jurídico — NR-1", "html": "<p>edição semanal</p>"}

    with patch("app.routers.content.get_ai_client") as mock_get_ai:
        mock_ai = AsyncMock()
        mock_ai.generate_json.side_effect = [FAKE_RESULTS_PADRAO[t] for t in TIPOS_PADRAO] + [jornal]
        mock_get_ai.return_value = mock_ai

        response = await client.post(
            "/content/gerar",
            json={"pauta_id": str(pauta.id)},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    body = response.json()
    tipos = {piece["tipo"] for piece in body}
    assert tipos == set(TIPOS_PADRAO) | {"jornal"}
    jornal_piece = next(p for p in body if p["tipo"] == "jornal")
    assert jornal_piece["corpo"]["titulo"] == "Radar Jurídico — NR-1"

    # o prompt de cada peça deve carregar o material já pesquisado, para não
    # deixar a IA "pesquisar" de novo por cima da curadoria feita no ChatGPT
    prompts_usados = [call.args[0] for call in mock_ai.generate_json.call_args_list]
    assert all("STF confirma suspensão temporária das multas da NR-1" in p for p in prompts_usados)


@pytest.mark.anyio
async def test_gerar_pauta_satelite_do_radar_nao_cria_jornal(client, db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(
        TenantConfig(
            tenant_id=tenant.id,
            voz={"principios": ["Sem juridiquês"], "oab": "OAB/ES 39.948"},
            identidade_visual={}, ctas={}, regras_compliance={}, canais={},
        )
    )
    user = User(
        tenant_id=tenant.id, email="l3@example.com", nome="L",
        hashed_password=hash_password("senha"), role="owner",
    )
    db_session.add(user)
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Medida protetiva não prejudica vítima", angulo="direitos",
        area="Família", origem="radar_juridico_satelite", fonte="chatgpt-radar",
        relevante_para_conteudo=True, status="sugerida",
        conteudo_bruto="STJ decide que medida protetiva não pode prejudicar a vítima...",
    )
    db_session.add(pauta)
    await db_session.commit()

    token = create_access_token(user.id)

    with patch("app.routers.content.get_ai_client") as mock_get_ai:
        mock_ai = AsyncMock()
        mock_ai.generate_json.side_effect = [FAKE_RESULTS_PADRAO[t] for t in TIPOS_PADRAO]
        mock_get_ai.return_value = mock_ai

        response = await client.post(
            "/content/gerar",
            json={"pauta_id": str(pauta.id)},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    tipos = {piece["tipo"] for piece in response.json()}
    assert tipos == set(TIPOS_PADRAO)


def test_prompts_de_frase_pergunta_e_carrossel_pedem_o_que_vira_imagem_e_legenda():
    from app.routers.content import PROMPTS

    assert '"frase": str' in PROMPTS["frase"] and '"legenda": str' in PROMPTS["frase"]
    assert '"pergunta": str' in PROMPTS["pergunta"] and '"legenda": str' in PROMPTS["pergunta"]
    assert '"legenda": str' in PROMPTS["carrossel"]
