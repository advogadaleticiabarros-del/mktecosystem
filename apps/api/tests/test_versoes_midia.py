"""Material pronto nunca some (regra de 16/10/2026): trocar o vídeo ou a imagem de uma peça guarda a versão anterior
em corpo.versoes_anteriores, seja qual for o caminho (API, script, publicador)."""
import pytest
from sqlalchemy.orm.attributes import flag_modified

from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant


async def _peca(db, corpo):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    pauta = Pauta(tenant_id=tenant.id, titulo="Guarda", angulo="reels", area="Família", origem="manual",
                  fonte="manual", relevante_para_conteudo=True)
    db.add(pauta)
    await db.flush()
    peca = ContentPiece(tenant_id=tenant.id, pauta_id=pauta.id, tipo="reels", status="aprovado", corpo=corpo)
    db.add(peca)
    await db.commit()
    return peca


@pytest.mark.anyio
async def test_trocar_o_video_guarda_o_anterior(db_session):
    peca = await _peca(db_session, {"video": "https://x/media/guarda-1.mp4?v=g1", "legenda": "L"})
    peca.corpo = {**peca.corpo, "video": "https://x/media/guarda-1.mp4?v=limpo2"}
    await db_session.commit()
    await db_session.refresh(peca)
    assert peca.corpo["video"].endswith("limpo2")
    assert [v["video"] for v in peca.corpo["versoes_anteriores"]] == ["https://x/media/guarda-1.mp4?v=g1"]
    assert peca.corpo["versoes_anteriores"][0]["em"]


@pytest.mark.anyio
async def test_varias_trocas_acumulam_e_imagens_tambem_contam(db_session):
    peca = await _peca(db_session, {"imagens": ["a1.jpg", "a2.jpg"]})
    for versao in (["b1.jpg"], ["c1.jpg"]):
        peca.corpo = {**peca.corpo, "imagens": versao}
        await db_session.commit()
    await db_session.refresh(peca)
    assert [v["imagens"] for v in peca.corpo["versoes_anteriores"]] == [["a1.jpg", "a2.jpg"], ["b1.jpg"]]


@pytest.mark.anyio
async def test_mudar_so_texto_ou_status_nao_cria_versao(db_session):
    peca = await _peca(db_session, {"video": "v1.mp4", "legenda": "L"})
    peca.corpo = {**peca.corpo, "legenda": "Nova"}
    peca.status = "publicado"
    await db_session.commit()
    await db_session.refresh(peca)
    assert "versoes_anteriores" not in peca.corpo


@pytest.mark.anyio
async def test_alteracao_no_lugar_com_flag_modified_tambem_guarda(db_session):
    peca = await _peca(db_session, {"imagem": "frase-v1.jpg"})
    peca.corpo["imagem"] = "frase-v2.jpg"
    flag_modified(peca, "corpo")
    await db_session.commit()
    await db_session.refresh(peca)
    assert peca.corpo["imagem"] == "frase-v2.jpg"
    assert peca.corpo["versoes_anteriores"][0]["imagem"] == "frase-v1.jpg"
