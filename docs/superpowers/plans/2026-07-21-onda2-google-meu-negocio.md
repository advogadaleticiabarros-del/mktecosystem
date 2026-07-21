# Google Meu Negócio (Business Profile) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Conectar o Google Meu Negócio da Letícia via OAuth (refresh token), coletar métricas diárias (buscas, ligações, pedidos de rota, visualizações) e permitir responder avaliações direto pelo Orbit.

**Architecture:** Reaproveita a tabela `social_connections` já existente (Instagram usa o mesmo padrão) com `plataforma="google_business"`. `access_token_encrypted` guarda o **refresh token** (Google, não expira); o access token é obtido sob demanda a cada chamada. Worker diário reaproveita o scheduler já existente. Avaliações são buscadas ao vivo (sem tabela de cache).

**Tech Stack:** FastAPI + SQLAlchemy async, `httpx` para a API do Google, mesmos padrões de `app/integrations/social/` já usados para o Instagram.

## Global Constraints
- Token do Google (refresh token) nunca aparece em log nem em resposta de API — sempre criptografado em repouso (`app.core.crypto`, já existe).
- Toda query filtra por `tenant_id`.
- Falha nas chamadas ao Google Business Profile API é tratada como falha silenciosa no worker (loga e pula) — não derruba o job dos outros tenants.
- Sem resposta gerada por IA a avaliações — sempre texto escrito pela usuária.
- Novas env vars: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` (padrão dev: `http://localhost:8000/integracoes/google-business/callback`).

---

### Task 1: Cliente Google OAuth + Business Profile (troca de token)

**Files:**
- Create: `apps/api/app/integrations/social/google_business_client.py`
- Modify: `apps/api/app/config.py`
- Test: `apps/api/tests/test_google_business_client.py`

**Interfaces:**
- Produces: `GoogleBusinessClient.trocar_code_por_tokens(code, redirect_uri) -> dict` (retorna `access_token`, `refresh_token`, `expires_in`); `GoogleBusinessClient.renovar_access_token(refresh_token) -> str`; `GoogleBusinessClient.listar_contas(access_token) -> list[dict]`; `GoogleBusinessClient.listar_locais(access_token, account_id) -> list[dict]`.

- [ ] **Step 1: Escrever o teste (mocks httpx)**

```python
# apps/api/tests/test_google_business_client.py
import httpx
import pytest

from app.integrations.social.google_business_client import GoogleBusinessClient


@pytest.mark.anyio
async def test_trocar_code_por_tokens():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "oauth2.googleapis.com/token" in str(request.url)
        return httpx.Response(
            200,
            json={
                "access_token": "access_curto",
                "refresh_token": "refresh_longo",
                "expires_in": 3599,
                "token_type": "Bearer",
            },
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    resultado = await client.trocar_code_por_tokens("codigo123", "https://api.example.com/callback")
    assert resultado["access_token"] == "access_curto"
    assert resultado["refresh_token"] == "refresh_longo"


@pytest.mark.anyio
async def test_renovar_access_token():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "grant_type=refresh_token" in str(request.content)
        return httpx.Response(200, json={"access_token": "access_novo", "expires_in": 3599})

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    novo_token = await client.renovar_access_token("refresh_longo")
    assert novo_token == "access_novo"


@pytest.mark.anyio
async def test_listar_contas():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"accounts": [{"name": "accounts/123", "accountName": "Advogada Letícia Barros"}]},
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    contas = await client.listar_contas("access_token")
    assert contas[0]["name"] == "accounts/123"


@pytest.mark.anyio
async def test_listar_locais():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"locations": [{"name": "locations/456", "title": "Escritório Letícia Barros"}]},
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    locais = await client.listar_locais("access_token", "accounts/123")
    assert locais[0]["name"] == "locations/456"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_google_business_client.py -v`
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 3: Implementar o cliente**

```python
# apps/api/app/integrations/social/google_business_client.py
import httpx

TOKEN_URL = "https://oauth2.googleapis.com/token"
ACCOUNT_MGMT_URL = "https://mybusinessaccountmanagement.googleapis.com/v1"
BUSINESS_INFO_URL = "https://mybusinessbusinessinformation.googleapis.com/v1"


class GoogleBusinessClient:
    def __init__(
        self, client_id: str, client_secret: str, transport: httpx.AsyncBaseTransport | None = None
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._transport = transport

    async def _post_token(self, data: dict) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.post(
                TOKEN_URL,
                data={"client_id": self._client_id, "client_secret": self._client_secret, **data},
            )
            response.raise_for_status()
            return response.json()

    async def _get(self, url: str, access_token: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.get(
                url, params=params or {}, headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()

    async def trocar_code_por_tokens(self, code: str, redirect_uri: str) -> dict:
        return await self._post_token(
            {"code": code, "redirect_uri": redirect_uri, "grant_type": "authorization_code"}
        )

    async def renovar_access_token(self, refresh_token: str) -> str:
        resultado = await self._post_token(
            {"refresh_token": refresh_token, "grant_type": "refresh_token"}
        )
        return resultado["access_token"]

    async def listar_contas(self, access_token: str) -> list[dict]:
        resultado = await self._get(f"{ACCOUNT_MGMT_URL}/accounts", access_token)
        return resultado.get("accounts", [])

    async def listar_locais(self, access_token: str, account_id: str) -> list[dict]:
        resultado = await self._get(
            f"{BUSINESS_INFO_URL}/{account_id}/locations",
            access_token,
            params={"readMask": "name,title"},
        )
        return resultado.get("locations", [])
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_google_business_client.py -v`
Expected: PASS (4 testes)

- [ ] **Step 5: Adicionar env vars ao config**

Em `apps/api/app/config.py`, adicionar dentro da classe `Settings`:
```python
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/integracoes/google-business/callback"
```

- [ ] **Step 6: Commit**

```bash
git add apps/api/app/integrations/social/google_business_client.py apps/api/app/config.py apps/api/tests/test_google_business_client.py
git commit -m "feat: cliente OAuth + Business Profile API do Google Meu Negócio"
```

---

### Task 2: Fluxo de conexão (OAuth) — rotas

**Files:**
- Modify: `apps/api/app/routers/integracoes.py`
- Test: `apps/api/tests/test_integracoes_google_business.py`

**Interfaces:**
- Consumes: `GoogleBusinessClient` (Task 1), `encrypt_token`/`decrypt_token`, `SocialConnection`, `create_access_token`/`decode_access_token` (já existem, usados pelo fluxo do Instagram).
- Produces: rotas `GET /integracoes/google-business/iniciar`, `GET /integracoes/google-business/callback`, `DELETE /integracoes/google-business`.

- [ ] **Step 1: Escrever o teste**

```python
# apps/api/tests/test_integracoes_google_business.py
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User


async def _make_tenant_and_user(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(TenantConfig(tenant_id=tenant.id, voz={}))
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
async def test_callback_google_business_cria_conexao(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    state = create_access_token(user.id)

    mock_client = AsyncMock()
    mock_client.trocar_code_por_tokens.return_value = {
        "access_token": "access_curto",
        "refresh_token": "refresh_longo",
        "expires_in": 3599,
    }
    mock_client.listar_contas.return_value = [{"name": "accounts/123", "accountName": "Letícia Barros"}]
    mock_client.listar_locais.return_value = [
        {"name": "locations/456", "title": "Escritório Letícia Barros"}
    ]

    with patch("app.routers.integracoes.get_google_client", return_value=mock_client):
        resp = await client.get(
            f"/integracoes/google-business/callback?code=abc&state={state}",
            follow_redirects=False,
        )

    assert resp.status_code == 307
    assert "conectado=google_business" in resp.headers["location"]

    conexao = (
        await db_session.execute(
            select(SocialConnection).where(SocialConnection.plataforma == "google_business")
        )
    ).scalar_one()
    assert conexao.page_id == "accounts/123"
    assert conexao.ig_user_id == "locations/456"
    assert conexao.nome_conta == "Escritório Letícia Barros"
    assert conexao.status == "ativo"


@pytest.mark.anyio
async def test_desconectar_google_business(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)
    db_session.add(
        SocialConnection(
            tenant_id=tenant.id,
            plataforma="google_business",
            page_id="accounts/123",
            ig_user_id="locations/456",
            nome_conta="Escritório",
            access_token_encrypted="x",
            status="ativo",
        )
    )
    await db_session.commit()

    resp = await client.delete(
        "/integracoes/google-business", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 204

    conexao = (
        await db_session.execute(
            select(SocialConnection).where(SocialConnection.plataforma == "google_business")
        )
    ).scalar_one()
    assert conexao.status == "desconectado"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_integracoes_google_business.py -v`
Expected: FAIL (`AttributeError` — rota/função não existem)

- [ ] **Step 3: Implementar as rotas**

Em `apps/api/app/routers/integracoes.py`, adicionar os imports:
```python
from app.integrations.social.google_business_client import GoogleBusinessClient
```

Adicionar (após o bloco de `get_meta_client`):
```python
GOOGLE_SCOPES = "https://www.googleapis.com/auth/business.manage"


def get_google_client() -> GoogleBusinessClient:
    return GoogleBusinessClient(
        client_id=settings.GOOGLE_CLIENT_ID, client_secret=settings.GOOGLE_CLIENT_SECRET
    )


@router.get("/google-business/iniciar")
async def iniciar_conexao_google_business(
    token: Annotated[str, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RedirectResponse:
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    result = await db.execute(select(User).where(User.id == user_id))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    state = create_access_token(current_user.id)
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "scope": GOOGLE_SCOPES,
        "state": state,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    }
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}")


@router.get("/google-business/callback")
async def callback_google_business(
    db: Annotated[AsyncSession, Depends(get_db)],
    code: Annotated[str, Query()],
    state: Annotated[str, Query()],
) -> RedirectResponse:
    user_id = decode_access_token(state)
    if user_id is None:
        raise HTTPException(status_code=400, detail="state inválido")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=400, detail="usuário não encontrado")

    client = get_google_client()
    tokens = await client.trocar_code_por_tokens(code, settings.GOOGLE_REDIRECT_URI)

    contas = await client.listar_contas(tokens["access_token"])
    if not contas:
        raise HTTPException(status_code=422, detail="Nenhuma conta do Google Meu Negócio encontrada")
    conta = contas[0]

    locais = await client.listar_locais(tokens["access_token"], conta["name"])
    if not locais:
        raise HTTPException(status_code=422, detail="Nenhum local encontrado nessa conta")
    local = locais[0]

    existente = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == user.tenant_id,
            SocialConnection.plataforma == "google_business",
        )
    )
    conexao = existente.scalar_one_or_none()
    if conexao is None:
        conexao = SocialConnection(tenant_id=user.tenant_id, plataforma="google_business")
        db.add(conexao)

    conexao.page_id = conta["name"]
    conexao.ig_user_id = local["name"]
    conexao.nome_conta = local.get("title", conta.get("accountName", ""))
    conexao.access_token_encrypted = encrypt_token(tokens["refresh_token"])
    conexao.expira_em = None
    conexao.status = "ativo"

    await db.commit()
    return RedirectResponse(f"{settings.FRONTEND_URL}/visao-geral?conectado=google_business")


@router.delete("/google-business", status_code=204)
async def desconectar_google_business(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    result = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == current_user.tenant_id,
            SocialConnection.plataforma == "google_business",
        )
    )
    conexao = result.scalar_one_or_none()
    if conexao is not None:
        conexao.status = "desconectado"
        await db.commit()
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_integracoes_google_business.py -v`
Expected: PASS (2 testes)

- [ ] **Step 5: Rodar a suíte completa**

Run: `py -m pytest tests -q`
Expected: todos passando

- [ ] **Step 6: Commit**

```bash
git add apps/api/app/routers/integracoes.py apps/api/tests/test_integracoes_google_business.py
git commit -m "feat: fluxo OAuth de conexão com Google Meu Negócio"
```

---

### Task 3: Métricas diárias

**Files:**
- Modify: `apps/api/app/integrations/social/google_business_client.py`
- Create: `apps/api/app/services/google_business_metrics.py`
- Modify: `apps/api/app/scheduler.py`
- Modify: `apps/api/app/routers/dashboard.py`
- Test: `apps/api/tests/test_google_business_metrics.py`

**Interfaces:**
- Produces: `GoogleBusinessClient.buscar_metricas(access_token, location_id) -> dict` (retorna `{"buscas": int, "chamadas": int, "pedidos_rota": int, "visualizacoes": int}`); `coletar_metricas_google_business(db) -> int`.

- [ ] **Step 1: Escrever o teste do cliente (métricas)**

```python
# apps/api/tests/test_google_business_client.py — adicionar ao final do arquivo
@pytest.mark.anyio
async def test_buscar_metricas():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "multiDailyMetricTimeSeries": [
                    {
                        "dailyMetricTimeSeries": [
                            {
                                "dailyMetric": "CALL_CLICKS",
                                "timeSeries": {"datedValues": [{"value": "3"}, {"value": "5"}]},
                            },
                            {
                                "dailyMetric": "BUSINESS_DIRECTION_REQUESTS",
                                "timeSeries": {"datedValues": [{"value": "2"}]},
                            },
                        ]
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    metricas = await client.buscar_metricas("access_token", "locations/456")
    assert metricas["chamadas"] == 8
    assert metricas["pedidos_rota"] == 2
    assert metricas["buscas"] == 0
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_google_business_client.py::test_buscar_metricas -v`
Expected: FAIL (`AttributeError`)

- [ ] **Step 3: Implementar `buscar_metricas` no cliente**

Em `apps/api/app/integrations/social/google_business_client.py`, adicionar constante e método:
```python
PERFORMANCE_URL = "https://businessprofileperformance.googleapis.com/v1"

METRICAS_DESEJADAS = {
    "BUSINESS_IMPRESSIONS_DESKTOP_SEARCH": "buscas",
    "BUSINESS_IMPRESSIONS_MOBILE_SEARCH": "buscas",
    "CALL_CLICKS": "chamadas",
    "BUSINESS_DIRECTION_REQUESTS": "pedidos_rota",
}
```
E o método na classe:
```python
    async def buscar_metricas(self, access_token: str, location_id: str) -> dict:
        resultado = await self._get(
            f"{PERFORMANCE_URL}/{location_id}:fetchMultiDailyMetricsTimeSeries",
            access_token,
            params={
                "dailyMetrics": list(METRICAS_DESEJADAS.keys()),
                "dailyRange.start_date.year": "2026",
            },
        )
        totais = {"buscas": 0, "chamadas": 0, "pedidos_rota": 0, "visualizacoes": 0}
        for bloco in resultado.get("multiDailyMetricTimeSeries", []):
            for serie in bloco.get("dailyMetricTimeSeries", []):
                metrica = serie.get("dailyMetric")
                chave = METRICAS_DESEJADAS.get(metrica)
                if chave is None:
                    continue
                valores = serie.get("timeSeries", {}).get("datedValues", [])
                totais[chave] += sum(int(v.get("value", 0)) for v in valores)
        return totais
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_google_business_client.py -v`
Expected: PASS (5 testes)

- [ ] **Step 5: Escrever o teste do coletor**

```python
# apps/api/tests/test_google_business_metrics.py
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.crypto import encrypt_token
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric
from app.models.tenant import Tenant
from app.services.google_business_metrics import coletar_metricas_google_business


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(
        SocialConnection(
            tenant_id=tenant.id,
            plataforma="google_business",
            page_id="accounts/123",
            ig_user_id="locations/456",
            nome_conta="Escritório",
            access_token_encrypted=encrypt_token("refresh_token_falso"),
            status="ativo",
        )
    )
    await db.commit()
    return tenant


@pytest.mark.anyio
async def test_coleta_metricas_google_business(db_session):
    tenant = await _setup(db_session)

    with patch("app.services.google_business_metrics.GoogleBusinessClient") as MockClient:
        instancia = MockClient.return_value
        instancia.renovar_access_token = AsyncMock(return_value="access_novo")
        instancia.buscar_metricas = AsyncMock(
            return_value={"buscas": 40, "chamadas": 8, "pedidos_rota": 2, "visualizacoes": 100}
        )
        coletados = await coletar_metricas_google_business(db_session)

    assert coletados == 1
    metrica = (await db_session.execute(select(SocialMetric))).scalar_one()
    assert metrica.tipo == "google_business"
    assert metrica.metricas["chamadas"] == 8


@pytest.mark.anyio
async def test_falha_na_coleta_nao_interrompe(db_session):
    await _setup(db_session)

    with patch("app.services.google_business_metrics.GoogleBusinessClient") as MockClient:
        instancia = MockClient.return_value
        instancia.renovar_access_token = AsyncMock(side_effect=Exception("token revogado"))
        coletados = await coletar_metricas_google_business(db_session)

    assert coletados == 0
```

- [ ] **Step 6: Rodar e confirmar que falha**

Run: `py -m pytest tests/test_google_business_metrics.py -v`
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 7: Implementar o coletor**

```python
# apps/api/app/services/google_business_metrics.py
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import decrypt_token
from app.integrations.social.google_business_client import GoogleBusinessClient
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric

logger = logging.getLogger(__name__)


async def coletar_metricas_google_business(db: AsyncSession) -> int:
    conexoes = (
        await db.execute(
            select(SocialConnection).where(
                SocialConnection.plataforma == "google_business", SocialConnection.status == "ativo"
            )
        )
    ).scalars().all()

    coletados = 0
    for conexao in conexoes:
        refresh_token = decrypt_token(conexao.access_token_encrypted)
        client = GoogleBusinessClient(
            client_id=settings.GOOGLE_CLIENT_ID, client_secret=settings.GOOGLE_CLIENT_SECRET
        )
        try:
            access_token = await client.renovar_access_token(refresh_token)
            metricas = await client.buscar_metricas(access_token, conexao.ig_user_id)
        except Exception:
            logger.exception("Falha ao coletar métricas do Google Meu Negócio (tenant %s)", conexao.tenant_id)
            continue

        db.add(
            SocialMetric(
                tenant_id=conexao.tenant_id, tipo="google_business", referencia_id=None, metricas=metricas
            )
        )
        await db.commit()
        coletados += 1

    return coletados
```

- [ ] **Step 8: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_google_business_metrics.py -v`
Expected: PASS (2 testes)

- [ ] **Step 9: Plugar no scheduler**

Em `apps/api/app/scheduler.py`, adicionar import:
```python
from app.services.google_business_metrics import coletar_metricas_google_business
```
Modificar `job_metricas_instagram` (renomear para refletir que cobre as duas fontes):
```python
async def job_metricas_fontes_externas() -> None:
    async with SessionLocal() as db:
        ig = await coletar_metricas_diarias(db)
        gmb = await coletar_metricas_google_business(db)
        if ig or gmb:
            logger.info("Métricas coletadas: %d Instagram, %d Google Meu Negócio.", ig, gmb)
```
E em `criar_scheduler()`, trocar a linha `scheduler.add_job(job_metricas_instagram, CronTrigger(hour=6))` por:
```python
    scheduler.add_job(job_metricas_fontes_externas, CronTrigger(hour=6))
```

- [ ] **Step 10: Expor no dashboard**

Em `apps/api/app/routers/dashboard.py`, no bloco onde `ultima_metrica` do Instagram é buscada, adicionar logo abaixo:
```python
    ultima_metrica_gmb = (
        await db.execute(
            select(SocialMetric)
            .where(SocialMetric.tenant_id == tenant_id, SocialMetric.tipo == "google_business")
            .order_by(SocialMetric.coletado_em.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    google_business = ultima_metrica_gmb.metricas if ultima_metrica_gmb else None
```
E adicionar `"google_business": google_business,` ao dicionário retornado (ao lado de `"instagram": instagram,`).

- [ ] **Step 11: Rodar a suíte completa e commitar**

Run: `py -m pytest tests -q`
Expected: todos passando

```bash
git add apps/api/app/integrations/social/google_business_client.py apps/api/app/services/google_business_metrics.py apps/api/app/scheduler.py apps/api/app/routers/dashboard.py apps/api/tests
git commit -m "feat: coleta diária de métricas do Google Meu Negócio + exposição no dashboard"
```

---

### Task 4: Responder avaliações (backend)

**Files:**
- Modify: `apps/api/app/integrations/social/google_business_client.py`
- Create: `apps/api/app/routers/avaliacoes.py`
- Create: `apps/api/app/schemas/avaliacao.py`
- Modify: `apps/api/app/main.py`
- Test: `apps/api/tests/test_avaliacoes.py`

**Interfaces:**
- Produces: `GoogleBusinessClient.listar_avaliacoes(access_token, location_id) -> list[dict]`; `GoogleBusinessClient.responder_avaliacao(access_token, review_name, texto) -> None`; rotas `GET /avaliacoes`, `POST /avaliacoes/{review_id}/responder`.

- [ ] **Step 1: Escrever o teste do cliente (avaliações)**

```python
# apps/api/tests/test_google_business_client.py — adicionar ao final
@pytest.mark.anyio
async def test_listar_avaliacoes():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "reviews": [
                    {
                        "name": "locations/456/reviews/789",
                        "reviewer": {"displayName": "Maria S."},
                        "starRating": "FIVE",
                        "comment": "Excelente atendimento",
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    avaliacoes = await client.listar_avaliacoes("access_token", "locations/456")
    assert avaliacoes[0]["reviewer"]["displayName"] == "Maria S."


@pytest.mark.anyio
async def test_responder_avaliacao():
    chamadas = []

    def handler(request: httpx.Request) -> httpx.Response:
        chamadas.append(request)
        return httpx.Response(200, json={"comment": "Obrigada pela confiança!"})

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    await client.responder_avaliacao(
        "access_token", "locations/456/reviews/789", "Obrigada pela confiança!"
    )
    assert len(chamadas) == 1
    assert chamadas[0].method == "PUT"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_google_business_client.py::test_listar_avaliacoes tests/test_google_business_client.py::test_responder_avaliacao -v`
Expected: FAIL (`AttributeError`)

- [ ] **Step 3: Implementar no cliente**

Em `apps/api/app/integrations/social/google_business_client.py`, adicionar:
```python
    async def listar_avaliacoes(self, access_token: str, location_id: str) -> list[dict]:
        resultado = await self._get(f"{BUSINESS_INFO_URL}/{location_id}/reviews", access_token)
        return resultado.get("reviews", [])

    async def responder_avaliacao(self, access_token: str, review_name: str, texto: str) -> None:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.put(
                f"{BUSINESS_INFO_URL}/{review_name}/reply",
                json={"comment": texto},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_google_business_client.py -v`
Expected: PASS (7 testes)

- [ ] **Step 5: Escrever o teste das rotas**

```python
# apps/api/tests/test_avaliacoes.py
from unittest.mock import AsyncMock, patch

import pytest

from app.core.crypto import encrypt_token
from app.core.security import create_access_token, hash_password
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={}))
    db.add(
        SocialConnection(
            tenant_id=tenant.id,
            plataforma="google_business",
            page_id="accounts/123",
            ig_user_id="locations/456",
            nome_conta="Escritório",
            access_token_encrypted=encrypt_token("refresh_falso"),
            status="ativo",
        )
    )
    user = User(
        tenant_id=tenant.id,
        email="leticia@example.com",
        nome="Letícia",
        hashed_password=hash_password("senha"),
        role="owner",
    )
    db.add(user)
    await db.commit()
    return tenant, user


@pytest.mark.anyio
async def test_listar_avaliacoes(client, db_session):
    tenant, user = await _setup(db_session)
    token = create_access_token(user.id)

    mock_client = AsyncMock()
    mock_client.renovar_access_token.return_value = "access_novo"
    mock_client.listar_avaliacoes.return_value = [
        {
            "name": "locations/456/reviews/789",
            "reviewer": {"displayName": "Maria S."},
            "starRating": "FIVE",
            "comment": "Excelente",
        }
    ]

    with patch("app.routers.avaliacoes.get_google_client", return_value=mock_client):
        resp = await client.get("/avaliacoes", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    assert resp.json()[0]["reviewer"]["displayName"] == "Maria S."


@pytest.mark.anyio
async def test_responder_avaliacao(client, db_session):
    tenant, user = await _setup(db_session)
    token = create_access_token(user.id)

    mock_client = AsyncMock()
    mock_client.renovar_access_token.return_value = "access_novo"

    with patch("app.routers.avaliacoes.get_google_client", return_value=mock_client):
        resp = await client.post(
            "/avaliacoes/locations%2F456%2Freviews%2F789/responder",
            json={"texto": "Obrigada pela confiança!"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    mock_client.responder_avaliacao.assert_awaited_once()


@pytest.mark.anyio
async def test_listar_avaliacoes_sem_conexao_retorna_422(client, db_session):
    tenant = Tenant(nome="Outra", slug="outra", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(TenantConfig(tenant_id=tenant.id, voz={}))
    user = User(
        tenant_id=tenant.id,
        email="outra@example.com",
        nome="Outra",
        hashed_password=hash_password("senha"),
        role="owner",
    )
    db_session.add(user)
    await db_session.commit()
    token = create_access_token(user.id)

    resp = await client.get("/avaliacoes", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 422
```

- [ ] **Step 6: Rodar e confirmar que falha**

Run: `py -m pytest tests/test_avaliacoes.py -v`
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 7: Implementar schema e rotas**

```python
# apps/api/app/schemas/avaliacao.py
from pydantic import BaseModel


class ResponderAvaliacaoIn(BaseModel):
    texto: str
```

```python
# apps/api/app/routers/avaliacoes.py
from typing import Annotated
from urllib.parse import unquote

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import decrypt_token
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.social.google_business_client import GoogleBusinessClient
from app.models.social_connection import SocialConnection
from app.models.user import User
from app.schemas.avaliacao import ResponderAvaliacaoIn

router = APIRouter(prefix="/avaliacoes", tags=["avaliacoes"])


def get_google_client() -> GoogleBusinessClient:
    return GoogleBusinessClient(
        client_id=settings.GOOGLE_CLIENT_ID, client_secret=settings.GOOGLE_CLIENT_SECRET
    )


async def _conexao_ativa(db: AsyncSession, tenant_id) -> SocialConnection:
    result = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == tenant_id,
            SocialConnection.plataforma == "google_business",
            SocialConnection.status == "ativo",
        )
    )
    conexao = result.scalar_one_or_none()
    if conexao is None:
        raise HTTPException(
            status_code=422, detail="Google Meu Negócio não conectado. Conecte na Visão Geral."
        )
    return conexao


@router.get("")
async def listar_avaliacoes(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[dict]:
    conexao = await _conexao_ativa(db, current_user.tenant_id)
    client = get_google_client()
    access_token = await client.renovar_access_token(decrypt_token(conexao.access_token_encrypted))
    return await client.listar_avaliacoes(access_token, conexao.ig_user_id)


@router.post("/{review_id:path}/responder")
async def responder_avaliacao(
    review_id: str,
    payload: ResponderAvaliacaoIn,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict[str, str]:
    conexao = await _conexao_ativa(db, current_user.tenant_id)
    client = get_google_client()
    access_token = await client.renovar_access_token(decrypt_token(conexao.access_token_encrypted))
    await client.responder_avaliacao(access_token, unquote(review_id), payload.texto)
    return {"status": "ok"}
```

- [ ] **Step 8: Registrar o router**

Em `apps/api/app/main.py`, importar `avaliacoes` junto dos outros routers e adicionar `app.include_router(avaliacoes.router)`.

- [ ] **Step 9: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_avaliacoes.py -v`
Expected: PASS (3 testes)

- [ ] **Step 10: Rodar a suíte completa**

Run: `py -m pytest tests -q`
Expected: todos passando

- [ ] **Step 11: Commit**

```bash
git add apps/api/app/integrations/social/google_business_client.py apps/api/app/routers/avaliacoes.py apps/api/app/schemas/avaliacao.py apps/api/app/main.py apps/api/tests/test_avaliacoes.py
git commit -m "feat: listar e responder avaliações do Google Meu Negócio"
```

---

### Task 5: Frontend — conectar na Visão Geral + página de Avaliações

**Files:**
- Modify: `apps/web/app/(app)/visao-geral/page.tsx`
- Modify: `apps/web/components/app-shell.tsx`
- Create: `apps/web/app/(app)/avaliacoes/page.tsx`

**Interfaces:**
- Consumes: `GET /integracoes`, `GET /integracoes/google-business/iniciar` (redirect), `DELETE /integracoes/google-business`, `GET /avaliacoes`, `POST /avaliacoes/{id}/responder`.

- [ ] **Step 1: Ler o estado atual do arquivo**

Run: `cat "apps/web/app/(app)/visao-geral/page.tsx"` (a estrutura de `FONTES_FUTURAS`/card do Instagram pode ter mudado desde a Onda 2 parte 1 — confirmar antes de editar)

- [ ] **Step 2: Adicionar estado e handlers do Google Meu Negócio**

Seguindo exatamente o padrão já usado para `instagramConectado`/`conectarInstagram`/`desconectarInstagram` no mesmo arquivo, adicionar:
```tsx
const googleBusinessConectado = conexoes.find(
  (c) => c.plataforma === "google_business" && c.status === "ativo",
);

function conectarGoogleBusiness() {
  const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  const token = localStorage.getItem("token") ?? "";
  window.location.href = `${base}/integracoes/google-business/iniciar?token=${encodeURIComponent(token)}`;
}

async function desconectarGoogleBusiness() {
  await apiFetch("/integracoes/google-business", { method: "DELETE" });
  setConexoes((prev) => prev.filter((c) => c.plataforma !== "google_business"));
}
```

- [ ] **Step 3: Adicionar `google_business` ao tipo `Resumo`**

```tsx
type Resumo = {
  instagram: { seguidores: number; alcance_7d: number } | null;
  google_business: { buscas: number; chamadas: number; pedidos_rota: number; visualizacoes: number } | null;
  // ...demais campos inalterados
};
```

- [ ] **Step 4: Trocar o card "Google Meu Negócio" de `FONTES_FUTURAS` por card real**

Remover a entrada `{ nome: "Google Meu Negócio", ... }` do array `FONTES_FUTURAS` (sobra só o card de Google Analytics como "Em breve"). No lugar, adicionar — ao lado do card do Instagram, antes do `.map(FONTES_FUTURAS)` — um card seguindo exatamente a estrutura do card do Instagram (ícone `MapPin`, já importado):
```tsx
<Card className="p-5">
  <div className="flex items-center justify-between">
    <MapPin className="h-5 w-5 text-primary" />
    <Badge className={googleBusinessConectado ? "bg-primary/15 text-primary" : undefined} variant={googleBusinessConectado ? undefined : "secondary"}>
      {googleBusinessConectado ? "Conectado" : "Não conectado"}
    </Badge>
  </div>
  <p className="mt-3 text-sm font-medium">Google Meu Negócio</p>
  <p className="mt-1 text-xs text-muted-foreground">
    {googleBusinessConectado
      ? resumo.google_business
        ? `${resumo.google_business.chamadas} ligações · ${resumo.google_business.pedidos_rota} rotas (7d)`
        : googleBusinessConectado.nome_conta
      : "Buscas locais, ligações, rotas"}
  </p>
  <button
    type="button"
    onClick={googleBusinessConectado ? desconectarGoogleBusiness : conectarGoogleBusiness}
    className="mt-3 text-xs font-medium text-primary hover:underline"
  >
    {googleBusinessConectado ? "Desconectar" : "Conectar"}
  </button>
</Card>
```

- [ ] **Step 5: Build de checagem**

Run: `cd apps/web && npm run build`
Expected: build verde

- [ ] **Step 6: Adicionar item "Avaliações" na barra lateral**

Em `apps/web/components/app-shell.tsx`, importar `Star` de `lucide-react` e adicionar ao array `NAV_ITEMS` (após o item de Configurações):
```tsx
  { href: "/avaliacoes", label: "Avaliações", icon: Star },
```

- [ ] **Step 7: Criar a página de avaliações**

```tsx
// apps/web/app/(app)/avaliacoes/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Star } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Card } from "@/components/ui/card";

type Avaliacao = {
  name: string;
  reviewer: { displayName: string };
  starRating: string;
  comment?: string;
  reviewReply?: { comment: string };
};

const ESTRELAS: Record<string, number> = {
  ONE: 1,
  TWO: 2,
  THREE: 3,
  FOUR: 4,
  FIVE: 5,
};

export default function AvaliacoesPage() {
  const [avaliacoes, setAvaliacoes] = useState<Avaliacao[] | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [respostas, setRespostas] = useState<Record<string, string>>({});
  const [enviando, setEnviando] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    apiFetch("/avaliacoes").then(async (resp) => {
      if (resp.status === 401) {
        router.push("/login");
        return;
      }
      if (!resp.ok) {
        const body = await resp.json().catch(() => null);
        setErro(body?.detail ?? "Não foi possível carregar as avaliações.");
        return;
      }
      setAvaliacoes(await resp.json());
    });
  }, [router]);

  async function responder(reviewName: string) {
    const texto = respostas[reviewName]?.trim();
    if (!texto) return;
    setEnviando(reviewName);
    try {
      const resp = await apiFetch(`/avaliacoes/${encodeURIComponent(reviewName)}/responder`, {
        method: "POST",
        body: JSON.stringify({ texto }),
      });
      if (resp.ok) {
        setAvaliacoes((prev) =>
          prev
            ? prev.map((a) =>
                a.name === reviewName ? { ...a, reviewReply: { comment: texto } } : a,
              )
            : prev,
        );
      }
    } finally {
      setEnviando(null);
    }
  }

  return (
    <AppShell title="Avaliações" description="Responda avaliações do Google Meu Negócio">
      {erro && (
        <Card className="p-6 text-sm text-muted-foreground">{erro}</Card>
      )}
      {!erro && !avaliacoes && <p className="text-sm text-muted-foreground">Carregando...</p>}
      {avaliacoes && avaliacoes.length === 0 && (
        <Card className="p-6 text-sm text-muted-foreground">Nenhuma avaliação ainda.</Card>
      )}
      <div className="space-y-4">
        {avaliacoes?.map((a) => (
          <Card key={a.name} className="p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium">{a.reviewer.displayName}</p>
              <div className="flex items-center gap-0.5">
                {Array.from({ length: ESTRELAS[a.starRating] ?? 0 }).map((_, i) => (
                  <Star key={i} className="h-3.5 w-3.5 fill-primary text-primary" />
                ))}
              </div>
            </div>
            {a.comment && <p className="mt-2 text-sm text-muted-foreground">{a.comment}</p>}

            {a.reviewReply ? (
              <p className="mt-3 rounded-md bg-accent/40 p-3 text-xs text-muted-foreground">
                <span className="font-medium text-foreground">Sua resposta: </span>
                {a.reviewReply.comment}
              </p>
            ) : (
              <div className="mt-3 space-y-2">
                <textarea
                  value={respostas[a.name] ?? ""}
                  onChange={(e) =>
                    setRespostas((prev) => ({ ...prev, [a.name]: e.target.value }))
                  }
                  rows={2}
                  placeholder="Escreva sua resposta..."
                  className="w-full rounded-md border border-border bg-background p-2 text-xs"
                />
                <button
                  type="button"
                  onClick={() => responder(a.name)}
                  disabled={enviando === a.name || !respostas[a.name]?.trim()}
                  className="flex items-center gap-1.5 rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-primary-foreground disabled:opacity-60"
                >
                  {enviando === a.name && <Loader2 className="h-3 w-3 animate-spin" />}
                  Responder
                </button>
              </div>
            )}
          </Card>
        ))}
      </div>
    </AppShell>
  );
}
```

- [ ] **Step 8: Build final**

Run: `cd apps/web && npm run build`
Expected: build verde, todas as rotas listadas incluindo `/avaliacoes`

- [ ] **Step 9: Commit**

```bash
git add "apps/web/app/(app)/visao-geral/page.tsx" apps/web/components/app-shell.tsx "apps/web/app/(app)/avaliacoes/page.tsx"
git commit -m "feat: conectar Google Meu Negócio na Visão Geral + página de Avaliações"
```

---

### Task 6: Deploy + guia de setup do Google Cloud (com a usuária)

- [ ] **Step 1: Rodar a suíte completa uma última vez**

Run: `cd apps/api && py -m pytest tests -q`
Expected: todos passando

- [ ] **Step 2: Deploy do backend**

Run:
```bash
export RAILWAY_API_TOKEN="<token da sessão>"
cd /c/tmp/mktecosystem
railway up ./apps/api --path-as-root --service orbit-api --detach
```
Aguardar `SUCCESS` (mesmo padrão de verificação usado nos deploys anteriores: poll no GraphQL `deployment(id).status`).

- [ ] **Step 3: Deploy do frontend**

Run:
```bash
railway up ./apps/web --path-as-root --service orbit-web --detach
```
Aguardar `SUCCESS` e confirmar `curl -s -o /dev/null -w "%{http_code}" https://orbit-web-production-0a39.up.railway.app/avaliacoes/` retorna `200`.

- [ ] **Step 4: Guiar a criação das credenciais do Google Cloud (passo manual da usuária)**

1. console.cloud.google.com → criar projeto (ex: `orbit-mkt`)
2. **APIs & Services → Library**: habilitar "My Business Account Management API", "My Business Business Information API", "Business Profile Performance API"
3. **APIs & Services → OAuth consent screen**: tipo Externo, preencher nome do app, e-mail de suporte, domínio autorizado
4. **APIs & Services → Credentials → Create Credentials → OAuth client ID**, tipo "Web application", Authorized redirect URI: `https://orbit-api-production-0029.up.railway.app/integracoes/google-business/callback`
5. Copiar **Client ID** e **Client Secret**

- [ ] **Step 5: Configurar as credenciais no Railway**

Run (com os valores reais fornecidos pela usuária):
```bash
railway variables --service orbit-api \
  --set "GOOGLE_CLIENT_ID=<valor>" \
  --set "GOOGLE_CLIENT_SECRET=<valor>" \
  --set "GOOGLE_REDIRECT_URI=https://orbit-api-production-0029.up.railway.app/integracoes/google-business/callback"
```

- [ ] **Step 6: Guiar o pedido de acesso à Business Profile API (passo manual da usuária, 3–10 dias)**

Formulário oficial de acesso (link a confirmar no momento, pois a Google reorganiza a URL periodicamente — buscar "Google Business Profile API access request form" caso o link direto tenha mudado): preencher com Location ID (`locations/456`, obtido após a primeira tentativa de conexão), justificativa de uso ("gestão do próprio perfil da advogada, sem terceiros"), site `advogadaleticiabarros.com.br`.

- [ ] **Step 7: Teste real após aprovação (retomar quando o Google liberar)**

Login no Orbit → Visão Geral → Conectar no card do Google Meu Negócio → autorizar → confirmar card "Conectado" → esperar a próxima passada do worker diário (ou aguardar o dia seguinte) → conferir números no card → ir em Avaliações e responder uma de teste.
