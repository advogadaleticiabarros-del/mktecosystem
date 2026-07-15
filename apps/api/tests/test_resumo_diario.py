from datetime import datetime, timedelta, timezone

import pytest

from app.core.security import create_access_token, hash_password
from app.models.pauta import Pauta
from app.models.tenant import Tenant
from app.models.user import User


@pytest.mark.anyio
async def test_resumo_diario_includes_all_pautas_regardless_of_content_flag(client, db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    user = User(
        tenant_id=tenant.id, email="l@example.com", nome="L",
        hashed_password=hash_password("senha"), role="owner",
    )
    db_session.add(user)

    db_session.add_all(
        [
            Pauta(
                tenant_id=tenant.id, titulo="Tema de conteúdo", angulo="direitos",
                area="Trabalhista", origem="buscada", fonte="CNJ",
                relevante_para_conteudo=True, status="sugerida",
            ),
            Pauta(
                tenant_id=tenant.id, titulo="Tema técnico processual", angulo="tecnico",
                area="Processual", origem="buscada", fonte="STF",
                relevante_para_conteudo=False, status="sugerida",
            ),
            Pauta(
                tenant_id=tenant.id, titulo="Tema antigo", angulo="direitos",
                area="Trabalhista", origem="buscada", fonte="CNJ",
                relevante_para_conteudo=True, status="sugerida",
                criado_em=datetime.now(timezone.utc) - timedelta(days=5),
            ),
        ]
    )
    await db_session.commit()

    token = create_access_token(user.id)
    response = await client.get(
        "/pautas/resumo-diario", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    titulos = [p["titulo"] for p in response.json()]
    assert "Tema de conteúdo" in titulos
    assert "Tema técnico processual" in titulos
    assert "Tema antigo" not in titulos
