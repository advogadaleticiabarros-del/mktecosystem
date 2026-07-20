# Integração Instagram/Facebook (Meta) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Conectar a conta Instagram/Facebook da Letícia via OAuth da Meta, publicar automaticamente conteúdo agendado e aprovado, e coletar métricas reais para a Visão Geral e as dicas da IA.

**Architecture:** Token de acesso armazenado criptografado (Fernet) em `social_connections`. Um serviço de renderização server-side (Playwright) gera as imagens dos criativos e as serve num endpoint público próprio. Dois workers do APScheduler existente: publicação (hora em hora) e métricas (diário).

**Tech Stack:** FastAPI + SQLAlchemy async + Alembic, `cryptography` (Fernet), `httpx` (chamadas à Graph API), `playwright` (render), APScheduler (já em uso), Next.js no frontend.

## Global Constraints
- Token de acesso da Meta nunca aparece em log nem em resposta de API — sempre criptografado em repouso.
- Toda query filtra por `tenant_id`.
- Publicação só ocorre para `scheduled_posts` cujo `content_piece` está `aprovado` — nunca publica rascunho.
- Novas env vars já configuradas no Railway: `META_APP_ID`, `META_APP_SECRET`, `META_REDIRECT_URI`, `ENCRYPTION_KEY`.
- Novo volume persistente `media` precisa ser criado no Railway (mesmo padrão do volume do Postgres) antes do deploy final — ver Task 8.

---

### Task 1: Criptografia de token + modelos `social_connections`/`social_metrics`

**Files:**
- Create: `apps/api/app/core/crypto.py`
- Create: `apps/api/app/models/social_connection.py`
- Create: `apps/api/app/models/social_metric.py`
- Modify: `apps/api/app/models/__init__.py`
- Modify: `apps/api/alembic/env.py`
- Modify: `apps/api/app/config.py`
- Modify: `apps/api/pyproject.toml`
- Test: `apps/api/tests/test_crypto.py`

**Interfaces:**
- Produces: `encrypt_token(plaintext: str) -> str`, `decrypt_token(ciphertext: str) -> str` em `app.core.crypto`; `SocialConnection(id, tenant_id, plataforma, page_id, ig_user_id, nome_conta, access_token_encrypted, expira_em, status, conectado_em)`; `SocialMetric(id, tenant_id, tipo, referencia_id, metricas, coletado_em)`.

- [ ] **Step 1: Escrever o teste de criptografia**

```python
# apps/api/tests/test_crypto.py
from app.core.crypto import decrypt_token, encrypt_token


def test_encrypt_decrypt_roundtrip():
    original = "EAAG_token_de_exemplo_super_secreto"
    ciphertext = encrypt_token(original)
    assert ciphertext != original
    assert decrypt_token(ciphertext) == original
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_crypto.py -v`
Expected: FAIL (`ModuleNotFoundError: No module named 'app.core.crypto'`)

- [ ] **Step 3: Adicionar `cryptography` às dependências**

Em `apps/api/pyproject.toml`, dentro de `dependencies = [...]`, adicionar:
```toml
    "cryptography>=42.0",
```
Run: `py -m pip install "cryptography>=42.0"`

- [ ] **Step 4: Implementar `app/core/crypto.py`**

```python
from cryptography.fernet import Fernet

from app.config import settings


def _fernet() -> Fernet:
    return Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_token(plaintext: str) -> str:
    return _fernet().encrypt(plaintext.encode()).decode()


def decrypt_token(ciphertext: str) -> str:
    return _fernet().decrypt(ciphertext.encode()).decode()
```

- [ ] **Step 5: Adicionar `ENCRYPTION_KEY` ao config**

Em `apps/api/app/config.py`, adicionar dentro da classe `Settings`:
```python
    ENCRYPTION_KEY: str = "Yx8N1p3aFq7bT2mZ5rC9wL0eJ4iH6sV8dK1oQ3nR7g="
```
(valor padrão só para dev/testes locais — produção já tem a chave real setada no Railway)

- [ ] **Step 6: Rodar teste de criptografia e confirmar que passa**

Run: `py -m pytest tests/test_crypto.py -v`
Expected: PASS

- [ ] **Step 7: Criar os modelos**

```python
# apps/api/app/models/social_connection.py
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SocialConnection(Base):
    __tablename__ = "social_connections"
    __table_args__ = (
        UniqueConstraint("tenant_id", "plataforma", name="uq_social_connections_tenant_plataforma"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    plataforma: Mapped[str] = mapped_column(String(20))
    page_id: Mapped[str] = mapped_column(String(50))
    ig_user_id: Mapped[str] = mapped_column(String(50))
    nome_conta: Mapped[str] = mapped_column(String(200))
    access_token_encrypted: Mapped[str] = mapped_column(Text)
    expira_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ativo")
    conectado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
```

```python
# apps/api/app/models/social_metric.py
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SocialMetric(Base):
    __tablename__ = "social_metrics"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    tipo: Mapped[str] = mapped_column(String(20))
    referencia_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    metricas: Mapped[dict] = mapped_column(JSON, default=dict)
    coletado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
```

- [ ] **Step 8: Registrar os modelos**

Em `apps/api/app/models/__init__.py`, adicionar:
```python
from app.models.social_connection import SocialConnection  # noqa: F401
from app.models.social_metric import SocialMetric  # noqa: F401
```

Em `apps/api/alembic/env.py`, adicionar `social_connection, social_metric,` na lista de imports de `app.models`.

- [ ] **Step 9: Gerar e aplicar a migration**

Run:
```bash
cd apps/api
py -m alembic revision --autogenerate -m "social_connections e social_metrics"
py -m alembic upgrade head
```
Expected: duas tabelas novas detectadas e migration aplicada sem erro.

- [ ] **Step 10: Commit**

```bash
git add apps/api/app/core/crypto.py apps/api/app/models apps/api/alembic apps/api/app/config.py apps/api/pyproject.toml apps/api/tests/test_crypto.py
git commit -m "feat: criptografia de token e modelos social_connections/social_metrics"
```

---

### Task 2: Fluxo OAuth de conexão com o Instagram

**Files:**
- Create: `apps/api/app/integrations/social/__init__.py`
- Create: `apps/api/app/integrations/social/meta_client.py`
- Create: `apps/api/app/routers/integracoes.py`
- Create: `apps/api/app/schemas/social_connection.py`
- Modify: `apps/api/app/main.py`
- Test: `apps/api/tests/test_integracoes_instagram.py`

**Interfaces:**
- Consumes: `encrypt_token`/`decrypt_token` (Task 1), `SocialConnection` (Task 1), `get_current_user` (`app.core.deps`).
- Produces: `MetaClient.trocar_code_por_token(code, redirect_uri) -> dict`, `MetaClient.trocar_por_token_longa_duracao(token) -> dict`, `MetaClient.buscar_paginas(user_token) -> list[dict]`, `MetaClient.buscar_conta_instagram(page_id, page_token) -> dict | None`. Rotas `GET /integracoes`, `GET /integracoes/instagram/iniciar`, `GET /integracoes/instagram/callback`, `DELETE /integracoes/instagram`.

- [ ] **Step 1: Escrever o teste do cliente Meta (mock httpx)**

```python
# apps/api/tests/test_integracoes_instagram.py
import httpx
import pytest

from app.integrations.social.meta_client import MetaClient


@pytest.mark.anyio
async def test_trocar_code_por_token():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "code=abc123" in str(request.url)
        return httpx.Response(200, json={"access_token": "user_token_curto", "token_type": "bearer"})

    transport = httpx.MockTransport(handler)
    client = MetaClient(app_id="123", app_secret="segredo", transport=transport)
    resultado = await client.trocar_code_por_token("abc123", "https://api.example.com/callback")
    assert resultado["access_token"] == "user_token_curto"


@pytest.mark.anyio
async def test_buscar_paginas():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"data": [{"id": "111", "name": "Advogada Letícia Barros", "access_token": "page_token"}]},
        )

    transport = httpx.MockTransport(handler)
    client = MetaClient(app_id="123", app_secret="segredo", transport=transport)
    paginas = await client.buscar_paginas("user_token")
    assert paginas[0]["id"] == "111"
    assert paginas[0]["access_token"] == "page_token"


@pytest.mark.anyio
async def test_buscar_conta_instagram():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json={"instagram_business_account": {"id": "999"}, "id": "111"}
        )

    transport = httpx.MockTransport(handler)
    client = MetaClient(app_id="123", app_secret="segredo", transport=transport)
    conta = await client.buscar_conta_instagram("111", "page_token")
    assert conta["id"] == "999"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_integracoes_instagram.py -v`
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 3: Implementar `MetaClient`**

```python
# apps/api/app/integrations/social/__init__.py
```
(arquivo vazio)

```python
# apps/api/app/integrations/social/meta_client.py
import httpx

GRAPH_URL = "https://graph.facebook.com/v21.0"


class MetaClient:
    def __init__(self, app_id: str, app_secret: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._app_id = app_id
        self._app_secret = app_secret
        self._transport = transport

    async def _get(self, path: str, params: dict) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.get(f"{GRAPH_URL}{path}", params=params)
            response.raise_for_status()
            return response.json()

    async def trocar_code_por_token(self, code: str, redirect_uri: str) -> dict:
        return await self._get(
            "/oauth/access_token",
            {
                "client_id": self._app_id,
                "client_secret": self._app_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            },
        )

    async def trocar_por_token_longa_duracao(self, token_curto: str) -> dict:
        return await self._get(
            "/oauth/access_token",
            {
                "grant_type": "fb_exchange_token",
                "client_id": self._app_id,
                "client_secret": self._app_secret,
                "fb_exchange_token": token_curto,
            },
        )

    async def buscar_paginas(self, user_token: str) -> list[dict]:
        resultado = await self._get("/me/accounts", {"access_token": user_token})
        return resultado.get("data", [])

    async def buscar_conta_instagram(self, page_id: str, page_token: str) -> dict | None:
        resultado = await self._get(
            f"/{page_id}", {"fields": "instagram_business_account", "access_token": page_token}
        )
        return resultado.get("instagram_business_account")

    async def buscar_nome_conta_instagram(self, ig_user_id: str, page_token: str) -> str:
        resultado = await self._get(f"/{ig_user_id}", {"fields": "username", "access_token": page_token})
        return resultado.get("username", "")
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_integracoes_instagram.py -v`
Expected: PASS (3 testes)

- [ ] **Step 5: Schema e rotas**

```python
# apps/api/app/schemas/social_connection.py
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SocialConnectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    plataforma: str
    nome_conta: str
    status: str
    conectado_em: datetime
```

```python
# apps/api/app/routers/integracoes.py
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import encrypt_token
from app.core.deps import get_current_user
from app.core.security import create_access_token, decode_access_token
from app.db import get_db
from app.integrations.social.meta_client import MetaClient
from app.models.social_connection import SocialConnection
from app.models.user import User
from app.schemas.social_connection import SocialConnectionOut

router = APIRouter(prefix="/integracoes", tags=["integracoes"])

SCOPES = "pages_show_list,pages_read_engagement,instagram_basic,instagram_content_publish,business_management"


def get_meta_client() -> MetaClient:
    return MetaClient(app_id=settings.META_APP_ID, app_secret=settings.META_APP_SECRET)


@router.get("", response_model=list[SocialConnectionOut])
async def listar_conexoes(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[SocialConnection]:
    result = await db.execute(
        select(SocialConnection).where(SocialConnection.tenant_id == current_user.tenant_id)
    )
    return list(result.scalars().all())


@router.get("/instagram/iniciar")
async def iniciar_conexao_instagram(
    current_user: Annotated[User, Depends(get_current_user)],
) -> RedirectResponse:
    # o state carrega o tenant_id assinado, para o callback (público) saber a quem associar
    state = create_access_token(current_user.id)
    params = {
        "client_id": settings.META_APP_ID,
        "redirect_uri": settings.META_REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "response_type": "code",
    }
    return RedirectResponse(f"https://www.facebook.com/v21.0/dialog/oauth?{urlencode(params)}")


@router.get("/instagram/callback")
async def callback_instagram(
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

    client = get_meta_client()
    token_curto = await client.trocar_code_por_token(code, settings.META_REDIRECT_URI)
    token_longo = await client.trocar_por_token_longa_duracao(token_curto["access_token"])

    paginas = await client.buscar_paginas(token_longo["access_token"])
    if not paginas:
        raise HTTPException(status_code=422, detail="Nenhuma Página do Facebook encontrada para esta conta")

    pagina = paginas[0]
    conta_ig = await client.buscar_conta_instagram(pagina["id"], pagina["access_token"])
    if conta_ig is None:
        raise HTTPException(status_code=422, detail="Essa Página não tem uma conta Instagram Business vinculada")

    nome_conta = await client.buscar_nome_conta_instagram(conta_ig["id"], pagina["access_token"])
    expira_em = datetime.now(timezone.utc) + timedelta(seconds=token_longo.get("expires_in", 5184000))

    existente = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == user.tenant_id, SocialConnection.plataforma == "instagram"
        )
    )
    conexao = existente.scalar_one_or_none()
    if conexao is None:
        conexao = SocialConnection(tenant_id=user.tenant_id, plataforma="instagram")
        db.add(conexao)

    conexao.page_id = pagina["id"]
    conexao.ig_user_id = conta_ig["id"]
    conexao.nome_conta = nome_conta or pagina["name"]
    conexao.access_token_encrypted = encrypt_token(pagina["access_token"])
    conexao.expira_em = expira_em
    conexao.status = "ativo"

    await db.commit()
    return RedirectResponse(f"{settings.FRONTEND_URL}/visao-geral?conectado=instagram")


@router.delete("/instagram", status_code=204)
async def desconectar_instagram(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    result = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == current_user.tenant_id, SocialConnection.plataforma == "instagram"
        )
    )
    conexao = result.scalar_one_or_none()
    if conexao is not None:
        conexao.status = "desconectado"
        await db.commit()
```

- [ ] **Step 6: Adicionar `META_APP_ID`, `META_APP_SECRET`, `META_REDIRECT_URI`, `FRONTEND_URL` ao config**

Em `apps/api/app/config.py`, adicionar:
```python
    META_APP_ID: str = ""
    META_APP_SECRET: str = ""
    META_REDIRECT_URI: str = "http://localhost:8000/integracoes/instagram/callback"
    FRONTEND_URL: str = "http://localhost:3000"
```

- [ ] **Step 7: Registrar o router**

Em `apps/api/app/main.py`, importar `integracoes` junto dos outros routers e adicionar `app.include_router(integracoes.router)`.

- [ ] **Step 8: Rodar a suíte completa**

Run: `py -m pytest tests -q`
Expected: todos passando (nenhuma quebra nos testes existentes)

- [ ] **Step 9: Commit**

```bash
git add apps/api/app/integrations/social apps/api/app/routers/integracoes.py apps/api/app/schemas/social_connection.py apps/api/app/main.py apps/api/app/config.py apps/api/tests/test_integracoes_instagram.py
git commit -m "feat: fluxo OAuth de conexão com Instagram (Meta Graph API)"
```

---

### Task 3: Renderização server-side dos criativos

**Files:**
- Create: `apps/api/app/services/render_criativo.py`
- Create: `apps/api/app/templates/carrossel_slide.html`
- Create: `apps/api/app/routers/media.py`
- Modify: `apps/api/app/main.py`
- Modify: `apps/api/pyproject.toml`
- Test: `apps/api/tests/test_render_criativo.py`

**Interfaces:**
- Produces: `renderizar_slide(texto: str, indice: int, total: int, identidade_visual: dict, caminho_saida: str) -> None`; `GET /media/{arquivo}` serve arquivos de `apps/api/media/`.

- [ ] **Step 1: Escrever o teste (verifica que o PNG é gerado e tem o tamanho certo)**

```python
# apps/api/tests/test_render_criativo.py
import os

import pytest
from PIL import Image

from app.services.render_criativo import renderizar_slide

IDENTIDADE_VISUAL_TESTE = {
    "cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"},
}


@pytest.mark.anyio
async def test_renderiza_slide_1080x1350(tmp_path):
    saida = tmp_path / "slide-1.png"
    await renderizar_slide(
        texto="Direitos da gestante no trabalho",
        indice=0,
        total=5,
        identidade_visual=IDENTIDADE_VISUAL_TESTE,
        caminho_saida=str(saida),
    )
    assert saida.exists()
    with Image.open(saida) as img:
        assert img.size == (1080, 1350)
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_render_criativo.py -v`
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 3: Adicionar dependências**

Em `apps/api/pyproject.toml`:
```toml
    "playwright>=1.48",
    "jinja2>=3.1",
```
Run:
```bash
py -m pip install "playwright>=1.48" "jinja2>=3.1" pillow
py -m playwright install --with-deps chromium
```

- [ ] **Step 4: Criar o template do slide**

```html
<!-- apps/api/app/templates/carrossel_slide.html -->
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; }
  .slide {
    width: 1080px; height: 1350px;
    background: {{ fundo }};
    color: {{ areia }};
    display: flex; flex-direction: column; justify-content: space-between;
    padding: 96px; font-family: Inter, sans-serif; position: relative; overflow: hidden;
  }
  .texto { font-size: {{ tamanho_fonte }}px; line-height: 1.25; font-weight: {{ peso_fonte }}; }
  .rodape { display: flex; justify-content: space-between; border-top: 1px solid {{ dourado }}44; padding-top: 32px; }
</style>
</head>
<body>
  <div class="slide">
    <div style="display:flex;align-items:center;gap:16px;">
      <div style="width:40px;height:40px;border-radius:50%;border:2px solid {{ dourado }};display:flex;align-items:center;justify-content:center;">
        <div style="width:14px;height:14px;border-radius:50%;background:{{ dourado }};"></div>
      </div>
      <span style="font-size:26px;letter-spacing:2px;color:{{ dourado }};">{{ nome_conta }}</span>
    </div>
    <div style="flex:1;display:flex;align-items:center;">
      <p class="texto">{{ texto }}</p>
    </div>
    <div class="rodape">
      <span style="font-size:24px;color:{{ dourado }};">{{ instagram }}</span>
      <span style="font-size:22px;color:{{ areia }}99;">{{ rodape_direita }}</span>
    </div>
  </div>
</body>
</html>
```

- [ ] **Step 5: Implementar `render_criativo.py`**

```python
# apps/api/app/services/render_criativo.py
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


async def renderizar_slide(
    texto: str,
    indice: int,
    total: int,
    identidade_visual: dict,
    caminho_saida: str,
    nome_conta: str = "LETÍCIA BARROS",
    instagram: str = "@adv.leticiabarros2",
) -> None:
    cores = identidade_visual.get("cores", {})
    capa = indice == 0
    final = indice == total - 1
    html = _env.get_template("carrossel_slide.html").render(
        texto=texto,
        fundo=cores.get("fundo_escuro", "#231E1A"),
        dourado=cores.get("dourado", "#C9A962"),
        areia=cores.get("areia", "#E8DED1"),
        tamanho_fonte=72 if capa else 60 if final else 52,
        peso_fonte=700 if capa or final else 500,
        nome_conta=nome_conta,
        instagram=instagram,
        rodape_direita="OAB/ES 39.948" if final else f"{indice + 1} / {total}",
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html)
        await page.screenshot(path=caminho_saida)
        await browser.close()
```

- [ ] **Step 6: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_render_criativo.py -v`
Expected: PASS

- [ ] **Step 7: Endpoint de mídia pública**

```python
# apps/api/app/routers/media.py
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/media", tags=["media"])

MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)


@router.get("/{arquivo}")
async def servir_midia(arquivo: str) -> FileResponse:
    caminho = (MEDIA_DIR / arquivo).resolve()
    if MEDIA_DIR.resolve() not in caminho.parents or not caminho.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(caminho)
```

Registrar em `apps/api/app/main.py`: importar `media` e `app.include_router(media.router)`.

- [ ] **Step 8: Commit**

```bash
git add apps/api/app/services/render_criativo.py apps/api/app/templates apps/api/app/routers/media.py apps/api/app/main.py apps/api/pyproject.toml apps/api/tests/test_render_criativo.py
git commit -m "feat: renderização server-side dos criativos (Playwright) e endpoint de mídia pública"
```

---

### Task 4: Publicação automática no Instagram (worker)

**Files:**
- Create: `apps/api/app/integrations/social/instagram_api.py`
- Create: `apps/api/app/services/instagram_publisher.py`
- Modify: `apps/api/app/models/scheduled_post.py`
- Modify: `apps/api/app/scheduler.py`
- Test: `apps/api/tests/test_instagram_publisher.py`

**Interfaces:**
- Consumes: `SocialConnection`, `decrypt_token` (Task 1), `renderizar_slide` (Task 3), `ScheduledPost` (já existe).
- Produces: `InstagramAPI.publicar_carrossel(ig_user_id, urls_imagens) -> str` (retorna o post id); `publicar_agendamentos_prontos(db) -> int` (quantidade publicada).

- [ ] **Step 1: Adicionar `platform_post_id` e `tentativas` ao `ScheduledPost`**

Em `apps/api/app/models/scheduled_post.py`, adicionar dois campos à classe:
```python
    platform_post_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tentativas: Mapped[int] = mapped_column(Integer, default=0)
```
(usar os imports `String`, `Integer` já presentes no arquivo)

Run:
```bash
cd apps/api
py -m alembic revision --autogenerate -m "scheduled_posts: platform_post_id e tentativas"
py -m alembic upgrade head
```

- [ ] **Step 2: Escrever o teste do publisher (com mocks)**

```python
# apps/api/tests/test_instagram_publisher.py
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.crypto import encrypt_token
from app.core.security import hash_password
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User
from app.services.instagram_publisher import publicar_agendamentos_prontos


async def _setup(db, com_conexao=True):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={}, identidade_visual={"cores": {}}))
    if com_conexao:
        db.add(
            SocialConnection(
                tenant_id=tenant.id,
                plataforma="instagram",
                page_id="111",
                ig_user_id="999",
                nome_conta="adv.leticiabarros2",
                access_token_encrypted=encrypt_token("token-falso"),
                status="ativo",
            )
        )
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Tema", angulo="direitos", area="Trabalhista",
        origem="manual", fonte="manual", relevante_para_conteudo=True,
    )
    db.add(pauta)
    await db.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="carrossel",
        corpo={"slides": ["a", "b", "c"]}, status="aprovado",
    )
    db.add(piece)
    await db.flush()
    agendamento = ScheduledPost(
        tenant_id=tenant.id, content_piece_id=piece.id, titulo="Tema",
        canal="instagram", formato="carrossel",
        data_agendada=date.today() - timedelta(days=1), horario="11:00", status="pronto",
    )
    db.add(agendamento)
    await db.commit()
    return tenant, agendamento


@pytest.mark.anyio
async def test_publica_agendamento_pronto(db_session):
    tenant, agendamento = await _setup(db_session)

    with patch("app.services.instagram_publisher.renderizar_slide", new=AsyncMock()), patch(
        "app.services.instagram_publisher.InstagramAPI"
    ) as MockAPI:
        instancia = MockAPI.return_value
        instancia.publicar_carrossel = AsyncMock(return_value="post_123")
        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 1
    await db_session.refresh(agendamento)
    assert agendamento.status == "publicado"
    assert agendamento.platform_post_id == "post_123"


@pytest.mark.anyio
async def test_sem_conexao_pula_silenciosamente(db_session):
    tenant, agendamento = await _setup(db_session, com_conexao=False)
    publicados = await publicar_agendamentos_prontos(db_session)
    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "pronto"


@pytest.mark.anyio
async def test_falha_incrementa_tentativas_e_marca_erro_apos_3(db_session):
    tenant, agendamento = await _setup(db_session)
    agendamento.tentativas = 2
    await db_session.commit()

    with patch("app.services.instagram_publisher.renderizar_slide", new=AsyncMock()), patch(
        "app.services.instagram_publisher.InstagramAPI"
    ) as MockAPI:
        instancia = MockAPI.return_value
        instancia.publicar_carrossel = AsyncMock(side_effect=Exception("erro da API"))
        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "erro"
    assert agendamento.tentativas == 3
```

- [ ] **Step 3: Rodar e confirmar que falha**

Run: `py -m pytest tests/test_instagram_publisher.py -v`
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 4: Implementar `InstagramAPI`**

```python
# apps/api/app/integrations/social/instagram_api.py
import httpx

GRAPH_URL = "https://graph.facebook.com/v21.0"


class InstagramAPI:
    def __init__(self, page_token: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._page_token = page_token
        self._transport = transport

    async def _post(self, path: str, data: dict) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=60) as client:
            response = await client.post(
                f"{GRAPH_URL}{path}", data={**data, "access_token": self._page_token}
            )
            response.raise_for_status()
            return response.json()

    async def publicar_imagem_unica(self, ig_user_id: str, image_url: str, legenda: str = "") -> str:
        container = await self._post(f"/{ig_user_id}/media", {"image_url": image_url, "caption": legenda})
        publicado = await self._post(f"/{ig_user_id}/media_publish", {"creation_id": container["id"]})
        return publicado["id"]

    async def publicar_carrossel(self, ig_user_id: str, urls_imagens: list[str]) -> str:
        containers_ids = []
        for url in urls_imagens:
            container = await self._post(
                f"/{ig_user_id}/media", {"image_url": url, "is_carousel_item": "true"}
            )
            containers_ids.append(container["id"])

        container_pai = await self._post(
            f"/{ig_user_id}/media",
            {"media_type": "CAROUSEL", "children": ",".join(containers_ids)},
        )
        publicado = await self._post(f"/{ig_user_id}/media_publish", {"creation_id": container_pai["id"]})
        return publicado["id"]
```

- [ ] **Step 5: Implementar o publisher**

```python
# apps/api/app/services/instagram_publisher.py
import logging
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import decrypt_token
from app.integrations.social.instagram_api import InstagramAPI
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.models.tenant import TenantConfig
from app.services.render_criativo import renderizar_slide

logger = logging.getLogger(__name__)
MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
LIMITE_TENTATIVAS = 3


async def _agendamentos_prontos(db: AsyncSession) -> list[ScheduledPost]:
    agora = datetime.now(timezone.utc)
    hoje = agora.date()
    resultado = await db.execute(
        select(ScheduledPost).where(
            ScheduledPost.canal == "instagram",
            ScheduledPost.status == "pronto",
            ScheduledPost.data_agendada <= hoje,
        )
    )
    return list(resultado.scalars().all())


async def _conexao_ativa(db: AsyncSession, tenant_id: uuid.UUID) -> SocialConnection | None:
    resultado = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == tenant_id,
            SocialConnection.plataforma == "instagram",
            SocialConnection.status == "ativo",
        )
    )
    return resultado.scalar_one_or_none()


async def publicar_agendamentos_prontos(db: AsyncSession) -> int:
    publicados = 0
    for agendamento in await _agendamentos_prontos(db):
        conexao = await _conexao_ativa(db, agendamento.tenant_id)
        if conexao is None:
            logger.info("Tenant %s sem conexão Instagram ativa; pulando.", agendamento.tenant_id)
            continue

        piece = (
            await db.execute(
                select(ContentPiece).where(ContentPiece.id == agendamento.content_piece_id)
            )
        ).scalar_one_or_none()
        if piece is None or piece.status != "aprovado":
            continue

        tenant_config = (
            await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == agendamento.tenant_id))
        ).scalar_one_or_none()
        identidade_visual = tenant_config.identidade_visual if tenant_config else {}

        page_token = decrypt_token(conexao.access_token_encrypted)
        api = InstagramAPI(page_token=page_token)

        try:
            slides = piece.corpo.get("slides", [])
            urls_imagens = []
            for i, texto in enumerate(slides):
                nome_arquivo = f"{agendamento.id}-{i}.png"
                caminho = MEDIA_DIR / nome_arquivo
                await renderizar_slide(texto, i, len(slides), identidade_visual, str(caminho))
                urls_imagens.append(f"{settings.PUBLIC_API_URL}/media/{nome_arquivo}")

            post_id = await api.publicar_carrossel(conexao.ig_user_id, urls_imagens)
        except Exception:
            logger.exception("Falha ao publicar agendamento %s", agendamento.id)
            agendamento.tentativas += 1
            if agendamento.tentativas >= LIMITE_TENTATIVAS:
                agendamento.status = "erro"
            await db.commit()
            continue

        agendamento.status = "publicado"
        agendamento.platform_post_id = post_id
        await db.commit()
        publicados += 1

    return publicados
```

- [ ] **Step 6: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_instagram_publisher.py -v`
Expected: PASS (3 testes)

- [ ] **Step 7: Plugar no scheduler**

Em `apps/api/app/scheduler.py`, dentro de `job_envios()`, adicionar a chamada (junto das de e-mail já existentes):
```python
from app.services.instagram_publisher import publicar_agendamentos_prontos
```
E dentro da função `job_envios`, após as linhas de `processar_boas_vindas`/`processar_fila_newsletter`:
```python
        ig = await publicar_agendamentos_prontos(db)
        if ig:
            logger.info("Publicados %d posts no Instagram.", ig)
```

- [ ] **Step 8: Rodar a suíte completa**

Run: `py -m pytest tests -q`
Expected: todos passando

- [ ] **Step 9: Commit**

```bash
git add apps/api/app/integrations/social/instagram_api.py apps/api/app/services/instagram_publisher.py apps/api/app/models/scheduled_post.py apps/api/app/scheduler.py apps/api/alembic apps/api/tests/test_instagram_publisher.py
git commit -m "feat: publicação automática de carrosséis no Instagram via worker"
```

---

### Task 5: Coleta diária de métricas

**Files:**
- Create: `apps/api/app/services/instagram_metrics.py`
- Modify: `apps/api/app/integrations/social/instagram_api.py`
- Modify: `apps/api/app/scheduler.py`
- Modify: `apps/api/app/routers/dashboard.py`
- Test: `apps/api/tests/test_instagram_metrics.py`

**Interfaces:**
- Consumes: `SocialConnection`, `decrypt_token`, `InstagramAPI` (Task 4).
- Produces: `InstagramAPI.buscar_metricas_conta(ig_user_id) -> dict`; `coletar_metricas_diarias(db) -> int` (quantidade de tenants coletados); campo `instagram` no payload de `GET /dashboard/resumo`.

- [ ] **Step 1: Escrever o teste**

```python
# apps/api/tests/test_instagram_metrics.py
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.crypto import encrypt_token
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric
from app.models.tenant import Tenant
from app.services.instagram_metrics import coletar_metricas_diarias


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(
        SocialConnection(
            tenant_id=tenant.id, plataforma="instagram", page_id="111", ig_user_id="999",
            nome_conta="adv.leticiabarros2", access_token_encrypted=encrypt_token("token"), status="ativo",
        )
    )
    await db.commit()
    return tenant


@pytest.mark.anyio
async def test_coleta_metricas_grava_social_metric(db_session):
    tenant = await _setup(db_session)

    with patch("app.services.instagram_metrics.InstagramAPI") as MockAPI:
        instancia = MockAPI.return_value
        instancia.buscar_metricas_conta = AsyncMock(
            return_value={"seguidores": 1200, "alcance_7d": 3400}
        )
        coletados = await coletar_metricas_diarias(db_session)

    assert coletados == 1
    metrica = (await db_session.execute(select(SocialMetric))).scalar_one()
    assert metrica.tipo == "conta"
    assert metrica.metricas["seguidores"] == 1200
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_instagram_metrics.py -v`
Expected: FAIL

- [ ] **Step 3: Adicionar `buscar_metricas_conta` ao `InstagramAPI`**

Em `apps/api/app/integrations/social/instagram_api.py`, adicionar o método (usar `_get`, análogo a `_post`):
```python
    async def _get(self, path: str, params: dict) -> dict:
        import httpx as _httpx
        async with _httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.get(f"{GRAPH_URL}{path}", params={**params, "access_token": self._page_token})
            response.raise_for_status()
            return response.json()

    async def buscar_metricas_conta(self, ig_user_id: str) -> dict:
        perfil = await self._get(f"/{ig_user_id}", {"fields": "followers_count"})
        insights = await self._get(
            f"/{ig_user_id}/insights", {"metric": "reach", "period": "week"}
        )
        alcance = 0
        for item in insights.get("data", []):
            if item.get("name") == "reach":
                valores = item.get("values", [])
                alcance = valores[-1]["value"] if valores else 0
        return {"seguidores": perfil.get("followers_count", 0), "alcance_7d": alcance}
```

- [ ] **Step 4: Implementar `coletar_metricas_diarias`**

```python
# apps/api/app/services/instagram_metrics.py
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypto import decrypt_token
from app.integrations.social.instagram_api import InstagramAPI
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric

logger = logging.getLogger(__name__)


async def coletar_metricas_diarias(db: AsyncSession) -> int:
    conexoes = (
        await db.execute(
            select(SocialConnection).where(
                SocialConnection.plataforma == "instagram", SocialConnection.status == "ativo"
            )
        )
    ).scalars().all()

    coletados = 0
    for conexao in conexoes:
        page_token = decrypt_token(conexao.access_token_encrypted)
        api = InstagramAPI(page_token=page_token)
        try:
            metricas = await api.buscar_metricas_conta(conexao.ig_user_id)
        except Exception:
            logger.exception("Falha ao coletar métricas do tenant %s", conexao.tenant_id)
            continue

        db.add(
            SocialMetric(tenant_id=conexao.tenant_id, tipo="conta", referencia_id=None, metricas=metricas)
        )
        await db.commit()
        coletados += 1

    return coletados
```

- [ ] **Step 5: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_instagram_metrics.py -v`
Expected: PASS

- [ ] **Step 6: Plugar no scheduler (job diário)**

Em `apps/api/app/scheduler.py`, importar `coletar_metricas_diarias` e adicionar um novo job:
```python
    scheduler.add_job(job_metricas_instagram, CronTrigger(hour=6))
```
Com a função correspondente:
```python
async def job_metricas_instagram() -> None:
    async with SessionLocal() as db:
        n = await coletar_metricas_diarias(db)
        if n:
            logger.info("Métricas do Instagram coletadas para %d tenant(s).", n)
```

- [ ] **Step 7: Expor no dashboard**

Em `apps/api/app/routers/dashboard.py`, dentro de `resumo()`, antes do `return`, adicionar:
```python
    from app.models.social_metric import SocialMetric

    ultima_metrica = (
        await db.execute(
            select(SocialMetric)
            .where(SocialMetric.tenant_id == tenant_id, SocialMetric.tipo == "conta")
            .order_by(SocialMetric.coletado_em.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    instagram = ultima_metrica.metricas if ultima_metrica else None
```
E adicionar `"instagram": instagram,` ao dicionário retornado.

- [ ] **Step 8: Rodar a suíte completa e commitar**

Run: `py -m pytest tests -q`
Expected: todos passando

```bash
git add apps/api/app/services/instagram_metrics.py apps/api/app/integrations/social/instagram_api.py apps/api/app/scheduler.py apps/api/app/routers/dashboard.py apps/api/tests/test_instagram_metrics.py
git commit -m "feat: coleta diária de métricas do Instagram + exposição no dashboard"
```

---

### Task 6: Frontend — conectar de verdade na Visão Geral

**Files:**
- Modify: `apps/web/app/(app)/visao-geral/page.tsx`
- Modify: `apps/web/lib/api.ts` (se necessário adicionar helper)

**Interfaces:**
- Consumes: `GET /integracoes`, `GET /integracoes/instagram/iniciar` (redirect), `DELETE /integracoes/instagram`.

- [ ] **Step 1: Ler o estado atual do arquivo**

Run: `cat apps/web/app/\(app\)/visao-geral/page.tsx` (para conferir a estrutura exata de `FONTES_FUTURAS` antes de editar — pode ter mudado desde a Onda 1)

- [ ] **Step 2: Buscar conexões ativas**

Adicionar estado e efeito, junto dos já existentes (`resumo`, `dicas`):
```tsx
type Conexao = { id: string; plataforma: string; nome_conta: string; status: string };

const [conexoes, setConexoes] = useState<Conexao[]>([]);

useEffect(() => {
  apiFetch("/integracoes").then(async (resp) => {
    if (resp.ok) setConexoes(await resp.json());
  });
}, []);

const instagramConectado = conexoes.find((c) => c.plataforma === "instagram" && c.status === "ativo");

async function conectarInstagram() {
  const base = process.env.NEXT_PUBLIC_API_URL ?? "";
  const token = localStorage.getItem("orbit_token");
  window.location.href = `${base}/integracoes/instagram/iniciar?token=${token}`;
}

async function desconectarInstagram() {
  await apiFetch("/integracoes/instagram", { method: "DELETE" });
  setConexoes((prev) => prev.filter((c) => c.plataforma !== "instagram"));
}
```

- [ ] **Step 3: Trocar o card do Instagram no bloco `FONTES_FUTURAS`**

Substituir a renderização do card "Instagram" (dentro do `.map` de `FONTES_FUTURAS`) por uma renderização condicional própria, antes do map genérico:
```tsx
<Card className="p-5">
  <div className="flex items-center justify-between">
    <Camera className="h-5 w-5 text-primary" />
    <Badge className={instagramConectado ? "bg-primary/15 text-primary" : "bg-secondary"}>
      {instagramConectado ? "Conectado" : "Não conectado"}
    </Badge>
  </div>
  <p className="mt-3 text-sm font-medium">Instagram</p>
  <p className="mt-1 text-xs text-muted-foreground">
    {instagramConectado ? instagramConectado.nome_conta : "Alcance, seguidores, melhores posts"}
  </p>
  <button
    type="button"
    onClick={instagramConectado ? desconectarInstagram : conectarInstagram}
    className="mt-3 text-xs font-medium text-primary hover:underline"
  >
    {instagramConectado ? "Desconectar" : "Conectar"}
  </button>
</Card>
```
Manter GA4 e Google Meu Negócio como estavam (cards "Em breve" do array `FONTES_FUTURAS`, sem o Instagram nesse array).

- [ ] **Step 4: Build**

Run: `cd apps/web && npm run build`
Expected: build verde, sem erros de tipo

- [ ] **Step 5: Commit**

```bash
git add apps/web/app/\(app\)/visao-geral/page.tsx
git commit -m "feat: conectar Instagram de verdade na Visão Geral"
```

---

### Task 7: Ajustar `PUBLIC_API_URL` do token na URL de callback

**Nota de segurança:** o Step 2 da Task 6 passa o JWT como query param (`?token=`) na URL de redirect para `/integracoes/instagram/iniciar`, porque esse endpoint precisa de autenticação mas é acessado via navegação de página inteira (não fetch). Esse token só trafega nessa única requisição interna e não fica em nenhum log de terceiros — é aceitável aqui pelo mesmo padrão usado em `create_access_token` para o `state` do OAuth.

**Files:**
- Modify: `apps/api/app/routers/integracoes.py`

- [ ] **Step 1: Aceitar o token via query param nesse endpoint específico**

Em `iniciar_conexao_instagram`, trocar a dependência `Depends(get_current_user)` (que só lê o header `Authorization`) por uma leitura direta do query param, já que a navegação de página inteira não envia headers customizados:
```python
from fastapi import Query


@router.get("/instagram/iniciar")
async def iniciar_conexao_instagram(
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
    # resto da função permanece igual
```

- [ ] **Step 2: Rodar a suíte completa**

Run: `cd apps/api && py -m pytest tests -q`
Expected: todos passando

- [ ] **Step 3: Commit**

```bash
git add apps/api/app/routers/integracoes.py
git commit -m "fix: aceitar token via query param em /integracoes/instagram/iniciar (navegação de página inteira)"
```

---

### Task 8: Deploy — volume de mídia, env vars finais e verificação real

- [ ] **Step 1: Criar o volume de mídia no Railway**

Run:
```bash
export RAILWAY_API_TOKEN="<token da sessão>"
cd /c/tmp/mktecosystem
railway volume add --service orbit-api --mount-path /app/media
```
Expected: volume criado e anexado ao serviço `orbit-api`.

- [ ] **Step 2: Confirmar env vars já setadas**

Run: `railway variables --service orbit-api --json`
Expected: `META_APP_ID`, `META_APP_SECRET`, `META_REDIRECT_URI`, `ENCRYPTION_KEY` presentes (já foram setadas durante o brainstorming desta feature). Adicionar `FRONTEND_URL`:
```bash
railway variables --service orbit-api --set "FRONTEND_URL=https://orbit.advogadaleticiabarros.com.br"
```

- [ ] **Step 3: Deploy**

Run: `cd apps/api && railway up . --path-as-root --service orbit-api --detach`
(usar `--path-as-root` sempre — ver nota na memória do projeto sobre o bug do Railway/monorepo)

- [ ] **Step 4: Verificar saúde e rotas novas**

Run:
```bash
curl -s https://orbit-api-production-0029.up.railway.app/health
curl -s https://orbit-api-production-0029.up.railway.app/openapi.json | grep -o "integracoes"
```
Expected: `{"status":"ok"}` e `integracoes` presente nas rotas.

- [ ] **Step 5: Teste real end-to-end com a usuária**

Passo manual (não automatizável): pedir para a Letícia logar no Orbit, ir em Visão Geral, clicar "Conectar" no card do Instagram, autorizar na tela da Meta, confirmar que volta para `/visao-geral?conectado=instagram` com o card mostrando "Conectado". Depois aprovar um carrossel de teste, agendar para poucos minutos à frente no Calendário, e confirmar que o worker publica sozinho.
