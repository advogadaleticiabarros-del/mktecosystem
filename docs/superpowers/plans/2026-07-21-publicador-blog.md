# Publicador Automático de Blog — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Quando um artigo aprovado chega na sua vaga agendada, o Orbit gera o HTML/capa no design real do blog e publica sozinho via SFTP (artigo + `index.html` + `sitemap.xml`).

**Architecture:** Mesmo padrão já usado para o Instagram (`instagram_publisher.py` + job no `scheduler.py`): um orquestrador `blog_publisher.py` varre `ScheduledPost` prontos, delega renderização (Jinja2 + Playwright) e edição de HTML/XML (BeautifulSoup + string insert) a serviços puros, e publica via um cliente SFTP fino sobre `asyncssh`.

**Tech Stack:** FastAPI, SQLAlchemy async, Jinja2, Playwright, BeautifulSoup4 (já presente), asyncssh (novo), APScheduler.

## Global Constraints

- Capa do artigo é simples (dourado/preto), **não** fotográfica — estilo fotográfico é escopo exclusivo do Estúdio de Criativos do Instagram, fora deste plano.
- Credenciais SFTP já estão no Railway (`orbit-api`): `BLOG_SFTP_HOST=147.93.38.211`, `BLOG_SFTP_PORT=65002`, `BLOG_SFTP_USER=u528898188`, `BLOG_SFTP_PASSWORD` (definida), `BLOG_SFTP_PATH=/home/u528898188/domains/advogadaleticiabarros.com.br/public_html/blog/`.
- Categoria do artigo vem sempre de `Pauta.area`, sem mapeamento adicional.
- Nenhuma migração de banco — reaproveita `ScheduledPost`/`ContentPiece` como estão.
- Publicação nunca derruba o job inteiro: erro em um agendamento incrementa `tentativas`, marca `status="erro"` na 3ª falha, e o loop segue para o próximo (mesmo padrão de `instagram_publisher.py`).

---

## File Structure

- `apps/api/app/config.py` — adiciona campos `BLOG_SFTP_*`.
- `apps/api/pyproject.toml` — adiciona dependência `asyncssh`.
- `apps/api/app/services/blog_slug.py` (novo) — `gerar_slug(titulo) -> str`.
- `apps/api/app/routers/content.py` — estende o prompt `"artigo"` para pedir `meta_description` e `resumo`.
- `apps/api/app/templates/blog_artigo.html` (novo) — página completa do artigo.
- `apps/api/app/templates/capa_artigo.html` (novo) — capa 1200×630.
- `apps/api/app/services/render_artigo_blog.py` (novo) — `estimar_tempo_leitura`, `renderizar_artigo_html`, `renderizar_capa_artigo`.
- `apps/api/app/integrations/publish/__init__.py` (novo, vazio) e `apps/api/app/integrations/publish/sftp_client.py` (novo) — `SFTPClient` (upload/download/close).
- `apps/api/app/services/blog_index_editor.py` (novo) — `inserir_card`, `inserir_sitemap_entry`.
- `apps/api/app/services/blog_publisher.py` (novo) — `publicar_agendamentos_prontos(db) -> int`.
- `apps/api/app/scheduler.py` — chama o novo publicador dentro de `job_envios()`.
- Testes espelhando cada arquivo acima em `apps/api/tests/`.

---

### Task 1: Config e dependência SFTP

**Files:**
- Modify: `apps/api/app/config.py`
- Modify: `apps/api/pyproject.toml`
- Test: `apps/api/tests/test_config_blog_sftp.py`

**Interfaces:**
- Produces: `settings.BLOG_SFTP_HOST: str`, `settings.BLOG_SFTP_PORT: int`, `settings.BLOG_SFTP_USER: str`, `settings.BLOG_SFTP_PASSWORD: str`, `settings.BLOG_SFTP_PATH: str` — usados pelas Tasks 5 e 7.

- [ ] **Step 1: Write the failing test**

```python
# apps/api/tests/test_config_blog_sftp.py
from app.config import Settings


def test_settings_tem_campos_sftp_do_blog_com_defaults_vazios():
    s = Settings(_env_file=None)
    assert s.BLOG_SFTP_HOST == ""
    assert s.BLOG_SFTP_PORT == 22
    assert s.BLOG_SFTP_USER == ""
    assert s.BLOG_SFTP_PASSWORD == ""
    assert s.BLOG_SFTP_PATH == ""
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/api && pytest tests/test_config_blog_sftp.py -v`
Expected: FAIL com `AttributeError` (campo não existe em `Settings`)

- [ ] **Step 3: Add the fields**

Em `apps/api/app/config.py`, adicione ao final da classe `Settings` (depois de `GROQ_API_KEY: str = ""`):

```python
    BLOG_SFTP_HOST: str = ""
    BLOG_SFTP_PORT: int = 22
    BLOG_SFTP_USER: str = ""
    BLOG_SFTP_PASSWORD: str = ""
    BLOG_SFTP_PATH: str = ""
```

- [ ] **Step 4: Add the dependency**

Em `apps/api/pyproject.toml`, adicione `"asyncssh>=2.14",` à lista `dependencies` (depois de `"jinja2>=3.1",`). Então instale:

Run: `cd apps/api && pip install -e .`
Expected: instala `asyncssh` sem erro

- [ ] **Step 5: Run test to verify it passes**

Run: `cd apps/api && pytest tests/test_config_blog_sftp.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
cd apps/api
git add app/config.py pyproject.toml tests/test_config_blog_sftp.py
git commit -m "feat: config SFTP do blog + dependência asyncssh"
```

---

### Task 2: Slug do artigo

**Files:**
- Create: `apps/api/app/services/blog_slug.py`
- Test: `apps/api/tests/test_blog_slug.py`

**Interfaces:**
- Produces: `gerar_slug(titulo: str) -> str` — usado pelas Tasks 4 e 7.

- [ ] **Step 1: Write the failing test**

```python
# apps/api/tests/test_blog_slug.py
from app.services.blog_slug import gerar_slug


def test_remove_acentos_e_usa_minusculas():
    assert gerar_slug("Carga Horária Máxima CLT") == "carga-horaria-maxima-clt"


def test_troca_pontuacao_por_hifen():
    assert gerar_slug("Pedi demissão, grávida: posso reverter?") == "pedi-demissao-gravida-posso-reverter"


def test_colapsa_espacos_e_hifens_duplicados():
    assert gerar_slug("Racismo   no  trabalho -- como provar") == "racismo-no-trabalho-como-provar"


def test_remove_hifen_nas_bordas():
    assert gerar_slug("  -BPC/LOAS em 2026- ") == "bpc-loas-em-2026"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/api && pytest tests/test_blog_slug.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'app.services.blog_slug'`

- [ ] **Step 3: Write minimal implementation**

```python
# apps/api/app/services/blog_slug.py
import re
import unicodedata


def gerar_slug(titulo: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    minusculo = sem_acento.lower()
    apenas_alfanumerico = re.sub(r"[^a-z0-9]+", "-", minusculo)
    return apenas_alfanumerico.strip("-")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/api && pytest tests/test_blog_slug.py -v`
Expected: PASS (4 testes)

- [ ] **Step 5: Commit**

```bash
cd apps/api
git add app/services/blog_slug.py tests/test_blog_slug.py
git commit -m "feat: gerador de slug para artigos do blog"
```

---

### Task 3: Estender o prompt do artigo com meta description e resumo

**Files:**
- Modify: `apps/api/app/routers/content.py:39-45`

**Interfaces:**
- Produces: `ContentPiece.corpo` para `tipo="artigo"` passa a conter `{"titulo": str, "html": str, "meta_description": str, "resumo": str}` — usado pela Task 4/7.

- [ ] **Step 1: Update the prompt**

Em `apps/api/app/routers/content.py`, troque a entrada `"artigo"` do dicionário `PROMPTS`:

```python
    "artigo": (
        "Escreva um artigo de blog completo (1200-1800 palavras) sobre '{titulo}' "
        "(ângulo: {angulo}, área: {area}). Estrutura: gancho, H2s com keyword, "
        "Perguntas frequentes, Leia também, 1 caso típico do escritório, 2 CTAs.\n"
        "{voz}\nResponda em JSON: {{\"titulo\": str, \"html\": str, "
        "\"meta_description\": str (até 155 caracteres, resumindo o artigo para SEO), "
        "\"resumo\": str (1-2 frases curtas, usadas como chamada nos cards do blog)}}"
    ),
```

Nenhum teste novo é necessário aqui: `tests/test_content_gerar.py::test_gerar_creates_four_content_pieces` já mocka `generate_json` (não valida o texto do prompt) e continua passando sem alteração.

- [ ] **Step 2: Run the existing test to confirm nothing broke**

Run: `cd apps/api && pytest tests/test_content_gerar.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
cd apps/api
git add app/routers/content.py
git commit -m "feat: prompt de artigo passa a gerar meta_description e resumo"
```

---

### Task 4: Templates e renderização (HTML do artigo + capa)

**Files:**
- Create: `apps/api/app/templates/blog_artigo.html`
- Create: `apps/api/app/templates/capa_artigo.html`
- Create: `apps/api/app/services/render_artigo_blog.py`
- Test: `apps/api/tests/test_render_artigo_blog.py`

**Interfaces:**
- Consumes: nada de tasks anteriores (arquivos novos e independentes).
- Produces:
  - `estimar_tempo_leitura(html: str) -> int`
  - `renderizar_artigo_html(*, titulo: str, meta_description: str, categoria: str, resumo: str, corpo_html: str, slug: str, data_publicacao: date, whatsapp: str = "5527995151402", oab: str = "OAB/ES 39.948") -> str` (retorna a página HTML completa como string)
  - `async def renderizar_capa_artigo(*, titulo: str, categoria: str, identidade_visual: dict, caminho_saida: str) -> None` (grava PNG 1200×630)
  - usados pela Task 7.

- [ ] **Step 1: Create the article template**

```html
<!-- apps/api/app/templates/blog_artigo.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo }} | Dra. Letícia Barros</title>
    <meta name="description" content="{{ meta_description }}">
    <link rel="canonical" href="{{ canonical_url }}">

    <meta property="og:title" content="{{ titulo }}">
    <meta property="og:description" content="{{ meta_description }}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{{ canonical_url }}">
    <meta property="article:author" content="Dra. Letícia Barros">
    <meta property="article:section" content="{{ categoria }}">
    <meta property="article:published_time" content="{{ data_iso }}">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="../css/pages.css?v=20260626">
    <link rel="stylesheet" href="../css/micro-interactions.css">

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": {{ titulo|tojson }},
      "description": {{ meta_description|tojson }},
      "author": {"@type": "Person", "name": "Dra. Letícia Barros"},
      "datePublished": "{{ data_iso }}"
    }
    </script>
</head>
<body>

<section class="article-hero">
    <div class="container">
        <div class="breadcrumb" style="margin-bottom: 32px;">
            <a href="../index.html">Home</a> &rsaquo;
            <a href="index.html">Blog</a> &rsaquo;
            {{ categoria }}
        </div>
        <span class="cat-badge">{{ categoria }}</span>
        <h1>{{ titulo }}</h1>
        <div class="article-meta">
            <span>Por <a href="../sobre.html">Dra. Letícia Barros</a> — {{ oab }}</span>
            <span class="dot">&bull;</span>
            <span><i class="fa-regular fa-calendar"></i> {{ data_extenso }}</span>
            <span class="dot">&bull;</span>
            <span><i class="fa-regular fa-clock"></i> {{ tempo_leitura }} min de leitura</span>
        </div>
    </div>
</section>

<div class="gold-line"></div>

<section>
<div class="article-body">
{{ corpo_html|safe }}

<div class="article-cta">
    <h3>Ficou com dúvidas sobre o seu caso?</h3>
    <p>Analiso o seu caso gratuitamente. Fale agora comigo pelo WhatsApp.</p>
    <a href="https://wa.me/{{ whatsapp }}" class="btn-whatsapp" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp"></i> Falar agora</a>
</div>
</div>
</section>

</body>
</html>
```

- [ ] **Step 2: Create the cover template**

```html
<!-- apps/api/app/templates/capa_artigo.html -->
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; }
  .capa {
    width: 1200px; height: 630px;
    background: {{ fundo }};
    color: {{ areia }};
    display: flex; flex-direction: column; justify-content: space-between;
    padding: 80px; font-family: Inter, sans-serif; position: relative; overflow: hidden;
  }
  .titulo { font-size: 56px; line-height: 1.2; font-weight: 700; max-width: 900px; }
  .categoria { font-size: 22px; letter-spacing: 3px; color: {{ dourado }}; text-transform: uppercase; }
</style>
</head>
<body>
  <div class="capa">
    <div style="display:flex;align-items:center;gap:16px;">
      <div style="width:48px;height:48px;border-radius:50%;border:2px solid {{ dourado }};display:flex;align-items:center;justify-content:center;">
        <div style="width:16px;height:16px;border-radius:50%;background:{{ dourado }};"></div>
      </div>
      <span class="categoria">{{ categoria }}</span>
    </div>
    <p class="titulo">{{ titulo }}</p>
  </div>
</body>
</html>
```

- [ ] **Step 3: Write the failing test**

```python
# apps/api/tests/test_render_artigo_blog.py
from datetime import date

import pytest
from PIL import Image

from app.services.render_artigo_blog import (
    estimar_tempo_leitura,
    renderizar_artigo_html,
    renderizar_capa_artigo,
)

IDENTIDADE_VISUAL_TESTE = {
    "cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"},
}


def test_estima_tempo_leitura_por_contagem_de_palavras():
    html = "<p>" + ("palavra " * 400) + "</p>"
    assert estimar_tempo_leitura(html) == 2


def test_estima_tempo_leitura_minimo_de_1_minuto():
    assert estimar_tempo_leitura("<p>texto curto</p>") == 1


def test_renderiza_html_do_artigo_com_campos_principais():
    html = renderizar_artigo_html(
        titulo="Carga horária máxima CLT",
        meta_description="Descrição para SEO",
        categoria="Trabalhista",
        resumo="Resumo curto",
        corpo_html="<p>Conteúdo do artigo</p>",
        slug="carga-horaria-maxima-clt",
        data_publicacao=date(2026, 7, 21),
    )
    assert "Carga horária máxima CLT" in html
    assert "Descrição para SEO" in html
    assert "Trabalhista" in html
    assert "Conteúdo do artigo" in html
    assert "carga-horaria-maxima-clt.html" in html
    assert "21 de julho de 2026" in html


@pytest.mark.anyio
async def test_renderiza_capa_1200x630(tmp_path):
    saida = tmp_path / "capa.png"
    await renderizar_capa_artigo(
        titulo="Carga horária máxima CLT",
        categoria="Trabalhista",
        identidade_visual=IDENTIDADE_VISUAL_TESTE,
        caminho_saida=str(saida),
    )
    assert saida.exists()
    with Image.open(saida) as img:
        assert img.size == (1200, 630)
```

- [ ] **Step 4: Run test to verify it fails**

Run: `cd apps/api && pytest tests/test_render_artigo_blog.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'app.services.render_artigo_blog'`

- [ ] **Step 5: Write minimal implementation**

```python
# apps/api/app/services/render_artigo_blog.py
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

MESES = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]

BLOG_BASE_URL = "https://advogadaleticiabarros.com.br/blog/"


def estimar_tempo_leitura(html: str) -> int:
    texto = BeautifulSoup(html, "html.parser").get_text()
    palavras = len(texto.split())
    return max(1, round(palavras / 200))


def renderizar_artigo_html(
    *,
    titulo: str,
    meta_description: str,
    categoria: str,
    resumo: str,
    corpo_html: str,
    slug: str,
    data_publicacao: date,
    whatsapp: str = "5527995151402",
    oab: str = "OAB/ES 39.948",
) -> str:
    data_extenso = f"{data_publicacao.day} de {MESES[data_publicacao.month - 1]} de {data_publicacao.year}"
    template = _env.get_template("blog_artigo.html")
    return template.render(
        titulo=titulo,
        meta_description=meta_description,
        categoria=categoria,
        resumo=resumo,
        corpo_html=corpo_html,
        canonical_url=f"{BLOG_BASE_URL}{slug}.html",
        data_iso=data_publicacao.isoformat(),
        data_extenso=data_extenso,
        tempo_leitura=estimar_tempo_leitura(corpo_html),
        whatsapp=whatsapp,
        oab=oab,
    )


async def renderizar_capa_artigo(
    *,
    titulo: str,
    categoria: str,
    identidade_visual: dict,
    caminho_saida: str,
) -> None:
    cores = identidade_visual.get("cores", {})
    html = _env.get_template("capa_artigo.html").render(
        titulo=titulo,
        categoria=categoria,
        fundo=cores.get("fundo_escuro", "#231E1A"),
        dourado=cores.get("dourado", "#C9A962"),
        areia=cores.get("areia", "#E8DED1"),
    )
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 630})
        await page.set_content(html)
        await page.screenshot(path=caminho_saida)
        await browser.close()
```

- [ ] **Step 6: Run test to verify it passes**

Run: `cd apps/api && pytest tests/test_render_artigo_blog.py -v`
Expected: PASS (5 testes)

- [ ] **Step 7: Commit**

```bash
cd apps/api
git add app/templates/blog_artigo.html app/templates/capa_artigo.html app/services/render_artigo_blog.py tests/test_render_artigo_blog.py
git commit -m "feat: renderização do HTML e da capa do artigo de blog"
```

---

### Task 5: Cliente SFTP

**Files:**
- Create: `apps/api/app/integrations/publish/__init__.py`
- Create: `apps/api/app/integrations/publish/sftp_client.py`
- Test: `apps/api/tests/test_sftp_client.py`

**Interfaces:**
- Produces: `SFTPClient(host: str, port: int, user: str, password: str)` com `async def upload(self, caminho_remoto: str, conteudo: bytes) -> None`, `async def download(self, caminho_remoto: str) -> bytes`, `async def close(self) -> None` — usado pela Task 7.

- [ ] **Step 1: Create the empty package init**

```python
# apps/api/app/integrations/publish/__init__.py
```

- [ ] **Step 2: Write the failing test**

```python
# apps/api/tests/test_sftp_client.py
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.integrations.publish.sftp_client import SFTPClient


@pytest.mark.anyio
async def test_upload_conecta_uma_vez_e_escreve_arquivo():
    with patch("app.integrations.publish.sftp_client.asyncssh.connect", new=AsyncMock()) as mock_connect:
        conn = mock_connect.return_value
        sftp = AsyncMock()
        conn.start_sftp_client = AsyncMock(return_value=sftp)
        arquivo_remoto = AsyncMock()
        arquivo_remoto.write = AsyncMock()
        sftp.open = MagicMock()
        sftp.open.return_value.__aenter__ = AsyncMock(return_value=arquivo_remoto)
        sftp.open.return_value.__aexit__ = AsyncMock(return_value=False)

        cliente = SFTPClient(host="h", port=65002, user="u", password="p")
        await cliente.upload("index.html", b"<html></html>")

        mock_connect.assert_awaited_once_with(
            "h", port=65002, username="u", password="p", known_hosts=None
        )
        arquivo_remoto.write.assert_awaited_once_with(b"<html></html>")


@pytest.mark.anyio
async def test_download_le_arquivo_remoto():
    with patch("app.integrations.publish.sftp_client.asyncssh.connect", new=AsyncMock()) as mock_connect:
        conn = mock_connect.return_value
        sftp = AsyncMock()
        conn.start_sftp_client = AsyncMock(return_value=sftp)
        arquivo_remoto = AsyncMock()
        arquivo_remoto.read = AsyncMock(return_value=b"conteudo atual")
        sftp.open = MagicMock()
        sftp.open.return_value.__aenter__ = AsyncMock(return_value=arquivo_remoto)
        sftp.open.return_value.__aexit__ = AsyncMock(return_value=False)

        cliente = SFTPClient(host="h", port=65002, user="u", password="p")
        conteudo = await cliente.download("sitemap.xml")

        assert conteudo == b"conteudo atual"
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd apps/api && pytest tests/test_sftp_client.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'app.integrations.publish.sftp_client'`

- [ ] **Step 4: Write minimal implementation**

```python
# apps/api/app/integrations/publish/sftp_client.py
import asyncssh


class SFTPClient:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._conn = None
        self._sftp = None

    async def _ensure_conn(self) -> None:
        if self._conn is None:
            self._conn = await asyncssh.connect(
                self._host,
                port=self._port,
                username=self._user,
                password=self._password,
                known_hosts=None,
            )
            self._sftp = await self._conn.start_sftp_client()

    async def upload(self, caminho_remoto: str, conteudo: bytes) -> None:
        await self._ensure_conn()
        async with self._sftp.open(caminho_remoto, "wb") as arquivo:
            await arquivo.write(conteudo)

    async def download(self, caminho_remoto: str) -> bytes:
        await self._ensure_conn()
        async with self._sftp.open(caminho_remoto, "rb") as arquivo:
            return await arquivo.read()

    async def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            await self._conn.wait_closed()
            self._conn = None
            self._sftp = None
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd apps/api && pytest tests/test_sftp_client.py -v`
Expected: PASS (2 testes)

- [ ] **Step 6: Commit**

```bash
cd apps/api
git add app/integrations/publish/ tests/test_sftp_client.py
git commit -m "feat: cliente SFTP fino sobre asyncssh"
```

---

### Task 6: Edição do index.html e do sitemap.xml

**Files:**
- Create: `apps/api/app/services/blog_index_editor.py`
- Test: `apps/api/tests/test_blog_index_editor.py`

**Interfaces:**
- Produces: `inserir_card(html_atual: str, *, url: str, imagem: str, categoria: str, categoria_slug: str, titulo: str, resumo: str, tempo_leitura: int) -> str` e `inserir_sitemap_entry(xml_atual: str, *, url: str, data_iso: str) -> str` — usados pela Task 7.

- [ ] **Step 1: Write the failing test**

```python
# apps/api/tests/test_blog_index_editor.py
from app.services.blog_index_editor import inserir_card, inserir_sitemap_entry

INDEX_FIXTURE = """
<div class="blog-grid" id="blogGridRecent">
    <a href="antigo.html" class="blog-card" data-cat="trabalhista">
        <h3>Artigo antigo</h3>
    </a>
</div>
<div class="blog-grid" id="blogGrid">
    <a href="antigo.html" class="blog-card" data-cat="trabalhista">
        <h3>Artigo antigo</h3>
    </a>
</div>
"""

SITEMAP_FIXTURE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    "  <url><loc>https://advogadaleticiabarros.com.br/blog/antigo.html</loc></url>\n"
    "</urlset>\n"
)


def test_insere_card_nas_duas_grades():
    resultado = inserir_card(
        INDEX_FIXTURE,
        url="novo-artigo.html",
        imagem="https://images.unsplash.com/foto.jpg",
        categoria="Trabalhista",
        categoria_slug="trabalhista",
        titulo="Novo artigo",
        resumo="Resumo do novo artigo",
        tempo_leitura=6,
    )
    assert resultado.count("Novo artigo") == 2
    assert resultado.count('href="novo-artigo.html"') == 2
    assert resultado.count("Artigo antigo") == 2


def test_card_novo_vem_antes_do_antigo_em_cada_grade():
    resultado = inserir_card(
        INDEX_FIXTURE,
        url="novo-artigo.html",
        imagem="https://images.unsplash.com/foto.jpg",
        categoria="Trabalhista",
        categoria_slug="trabalhista",
        titulo="Novo artigo",
        resumo="Resumo do novo artigo",
        tempo_leitura=6,
    )
    assert resultado.index("Novo artigo") < resultado.index("Artigo antigo")


def test_insere_entrada_no_sitemap():
    resultado = inserir_sitemap_entry(
        SITEMAP_FIXTURE, url="https://advogadaleticiabarros.com.br/blog/novo-artigo.html", data_iso="2026-07-21"
    )
    assert "<loc>https://advogadaleticiabarros.com.br/blog/novo-artigo.html</loc>" in resultado
    assert "<lastmod>2026-07-21</lastmod>" in resultado
    assert "<loc>https://advogadaleticiabarros.com.br/blog/antigo.html</loc>" in resultado
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/api && pytest tests/test_blog_index_editor.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'app.services.blog_index_editor'`

- [ ] **Step 3: Write minimal implementation**

```python
# apps/api/app/services/blog_index_editor.py
from bs4 import BeautifulSoup


def inserir_card(
    html_atual: str,
    *,
    url: str,
    imagem: str,
    categoria: str,
    categoria_slug: str,
    titulo: str,
    resumo: str,
    tempo_leitura: int,
) -> str:
    card_html = (
        f'<a href="{url}" class="blog-card" data-cat="{categoria_slug}" '
        'style="border-color: rgba(201,169,98,0.35);">'
        '<div class="blog-card-image" style="position:relative;">'
        f'<img src="{imagem}" alt="{titulo}" loading="lazy">'
        '<span style="position:absolute;top:12px;left:12px;background:var(--dourado);'
        "color:#231E1A;font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:700;"
        'letter-spacing:1.5px;text-transform:uppercase;padding:4px 10px;border-radius:999px;">Novo</span>'
        "</div>"
        '<div class="blog-card-body">'
        f'<span class="blog-card-cat">{categoria}</span>'
        f"<h3>{titulo}</h3>"
        f"<p>{resumo}</p>"
        '<div class="blog-card-meta">'
        f'<span><i class="fa-regular fa-clock"></i> {tempo_leitura} min de leitura</span>'
        '<span class="read-more">Ler artigo <i class="fa-solid fa-arrow-right"></i></span>'
        "</div></div></a>"
    )

    soup = BeautifulSoup(html_atual, "html.parser")
    for grid_id in ("blogGridRecent", "blogGrid"):
        grid = soup.find(id=grid_id)
        if grid is not None:
            novo_card = BeautifulSoup(card_html, "html.parser")
            grid.insert(0, novo_card)
    return str(soup)


def inserir_sitemap_entry(xml_atual: str, *, url: str, data_iso: str) -> str:
    entrada = f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{data_iso}</lastmod>\n  </url>\n"
    marcador = "<urlset"
    posicao_fim_tag = xml_atual.index(">", xml_atual.index(marcador)) + 1
    return xml_atual[:posicao_fim_tag] + "\n" + entrada + xml_atual[posicao_fim_tag:]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/api && pytest tests/test_blog_index_editor.py -v`
Expected: PASS (3 testes)

- [ ] **Step 5: Commit**

```bash
cd apps/api
git add app/services/blog_index_editor.py tests/test_blog_index_editor.py
git commit -m "feat: edição de index.html e sitemap.xml do blog"
```

---

### Task 7: Orquestrador `blog_publisher.py`

**Files:**
- Create: `apps/api/app/services/blog_publisher.py`
- Test: `apps/api/tests/test_blog_publisher.py`

**Interfaces:**
- Consumes:
  - `gerar_slug(titulo: str) -> str` (Task 2)
  - `renderizar_artigo_html(**kwargs) -> str`, `renderizar_capa_artigo(**kwargs) -> None` (Task 4)
  - `SFTPClient(host, port, user, password)` com `upload`/`download`/`close` (Task 5)
  - `inserir_card(**kwargs) -> str`, `inserir_sitemap_entry(**kwargs) -> str` (Task 6)
  - `ContentPiece.corpo` de tipo `artigo` com chaves `titulo`, `html`, `meta_description`, `resumo` (Task 3)
  - `settings.BLOG_SFTP_HOST/PORT/USER/PASSWORD/PATH` (Task 1)
- Produces: `async def publicar_agendamentos_prontos(db: AsyncSession) -> int` — usado pela Task 8.

- [ ] **Step 1: Write the failing test**

```python
# apps/api/tests/test_blog_publisher.py
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant, TenantConfig
from app.services.blog_publisher import publicar_agendamentos_prontos

INDEX_FIXTURE = (
    '<div class="blog-grid" id="blogGridRecent"></div>'
    '<div class="blog-grid" id="blogGrid"></div>'
)
SITEMAP_FIXTURE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>\n'
)


async def _setup(db, status_piece="aprovado"):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={}, identidade_visual={"cores": {}}))
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Carga horária máxima CLT", angulo="direitos", area="Trabalhista",
        origem="manual", fonte="manual", relevante_para_conteudo=True,
    )
    db.add(pauta)
    await db.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="artigo",
        corpo={
            "titulo": "Carga horária máxima CLT",
            "html": "<p>Conteúdo do artigo</p>",
            "meta_description": "Descrição SEO",
            "resumo": "Resumo curto",
        },
        status=status_piece,
    )
    db.add(piece)
    await db.flush()
    agendamento = ScheduledPost(
        tenant_id=tenant.id, content_piece_id=piece.id, titulo="Carga horária máxima CLT",
        canal="blog", formato="artigo",
        data_agendada=date.today() - timedelta(days=1), horario="11:00", status="pronto",
    )
    db.add(agendamento)
    await db.commit()
    return tenant, agendamento


@pytest.mark.anyio
async def test_publica_agendamento_pronto(db_session):
    tenant, agendamento = await _setup(db_session)

    with patch("app.services.blog_publisher.renderizar_capa_artigo", new=AsyncMock()), patch(
        "app.services.blog_publisher.SFTPClient"
    ) as MockSFTP:
        instancia = MockSFTP.return_value
        instancia.download = AsyncMock(side_effect=[INDEX_FIXTURE.encode(), SITEMAP_FIXTURE.encode()])
        instancia.upload = AsyncMock()
        instancia.close = AsyncMock()

        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 1
    await db_session.refresh(agendamento)
    assert agendamento.status == "publicado"
    assert agendamento.platform_post_id == "https://advogadaleticiabarros.com.br/blog/carga-horaria-maxima-clt.html"
    # 4 uploads: HTML do artigo, capa, index.html, sitemap.xml
    assert instancia.upload.await_count == 4
    instancia.close.assert_awaited_once()


@pytest.mark.anyio
async def test_content_piece_nao_aprovado_nao_publica(db_session):
    tenant, agendamento = await _setup(db_session, status_piece="rascunho")

    with patch("app.services.blog_publisher.renderizar_capa_artigo", new=AsyncMock()), patch(
        "app.services.blog_publisher.SFTPClient"
    ) as MockSFTP:
        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 0
    MockSFTP.assert_not_called()
    await db_session.refresh(agendamento)
    assert agendamento.status == "pronto"


@pytest.mark.anyio
async def test_falha_incrementa_tentativas_e_marca_erro_apos_3(db_session):
    tenant, agendamento = await _setup(db_session)
    agendamento.tentativas = 2
    await db_session.commit()

    with patch("app.services.blog_publisher.renderizar_capa_artigo", new=AsyncMock()), patch(
        "app.services.blog_publisher.SFTPClient"
    ) as MockSFTP:
        instancia = MockSFTP.return_value
        instancia.download = AsyncMock(side_effect=Exception("falha de conexão"))
        instancia.upload = AsyncMock()
        instancia.close = AsyncMock()

        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "erro"
    assert agendamento.tentativas == 3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/api && pytest tests/test_blog_publisher.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'app.services.blog_publisher'`

- [ ] **Step 3: Write minimal implementation**

```python
# apps/api/app/services/blog_publisher.py
import logging
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.integrations.publish.sftp_client import SFTPClient
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import TenantConfig
from app.services.blog_index_editor import inserir_card, inserir_sitemap_entry
from app.services.blog_slug import gerar_slug
from app.services.render_artigo_blog import (
    estimar_tempo_leitura,
    renderizar_artigo_html,
    renderizar_capa_artigo,
)

logger = logging.getLogger(__name__)
MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
LIMITE_TENTATIVAS = 3
BLOG_BASE_URL = "https://advogadaleticiabarros.com.br/blog/"


async def _agendamentos_prontos(db: AsyncSession) -> list[ScheduledPost]:
    agora = datetime.now(timezone.utc)
    hoje = agora.date()
    resultado = await db.execute(
        select(ScheduledPost).where(
            ScheduledPost.canal == "blog",
            ScheduledPost.status == "pronto",
            ScheduledPost.data_agendada <= hoje,
        )
    )
    return list(resultado.scalars().all())


async def publicar_agendamentos_prontos(db: AsyncSession) -> int:
    publicados = 0
    MEDIA_DIR.mkdir(exist_ok=True)

    for agendamento in await _agendamentos_prontos(db):
        piece = (
            await db.execute(
                select(ContentPiece).where(ContentPiece.id == agendamento.content_piece_id)
            )
        ).scalar_one_or_none()
        if piece is None or piece.status != "aprovado":
            continue

        pauta = (
            await db.execute(select(Pauta).where(Pauta.id == piece.pauta_id))
        ).scalar_one_or_none()
        categoria = pauta.area if pauta else "Direito"

        tenant_config = (
            await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == agendamento.tenant_id))
        ).scalar_one_or_none()
        identidade_visual = tenant_config.identidade_visual if tenant_config else {}

        sftp = SFTPClient(
            host=settings.BLOG_SFTP_HOST,
            port=settings.BLOG_SFTP_PORT,
            user=settings.BLOG_SFTP_USER,
            password=settings.BLOG_SFTP_PASSWORD,
        )

        try:
            titulo = piece.corpo["titulo"]
            slug = gerar_slug(titulo)
            categoria_slug = gerar_slug(categoria)
            url_artigo = f"{BLOG_BASE_URL}{slug}.html"

            html_artigo = renderizar_artigo_html(
                titulo=titulo,
                meta_description=piece.corpo["meta_description"],
                categoria=categoria,
                resumo=piece.corpo["resumo"],
                corpo_html=piece.corpo["html"],
                slug=slug,
                data_publicacao=date.today(),
            )

            caminho_capa_local = MEDIA_DIR / f"{agendamento.id}-capa.png"
            await renderizar_capa_artigo(
                titulo=titulo,
                categoria=categoria,
                identidade_visual=identidade_visual,
                caminho_saida=str(caminho_capa_local),
            )
            capa_bytes = caminho_capa_local.read_bytes()

            index_atual = (await sftp.download(f"{settings.BLOG_SFTP_PATH}index.html")).decode("utf-8")
            sitemap_atual = (await sftp.download(f"{settings.BLOG_SFTP_PATH}../sitemap.xml")).decode("utf-8")

            index_novo = inserir_card(
                index_atual,
                url=f"{slug}.html",
                imagem=f"capas/{slug}.png",
                categoria=categoria,
                categoria_slug=categoria_slug,
                titulo=titulo,
                resumo=piece.corpo["resumo"],
                tempo_leitura=estimar_tempo_leitura(piece.corpo["html"]),
            )
            sitemap_novo = inserir_sitemap_entry(
                sitemap_atual, url=url_artigo, data_iso=date.today().isoformat()
            )

            await sftp.upload(f"{settings.BLOG_SFTP_PATH}{slug}.html", html_artigo.encode("utf-8"))
            await sftp.upload(f"{settings.BLOG_SFTP_PATH}capas/{slug}.png", capa_bytes)
            await sftp.upload(f"{settings.BLOG_SFTP_PATH}index.html", index_novo.encode("utf-8"))
            await sftp.upload(f"{settings.BLOG_SFTP_PATH}../sitemap.xml", sitemap_novo.encode("utf-8"))
        except Exception:
            logger.exception("Falha ao publicar artigo do agendamento %s", agendamento.id)
            agendamento.tentativas += 1
            if agendamento.tentativas >= LIMITE_TENTATIVAS:
                agendamento.status = "erro"
            await db.commit()
            await sftp.close()
            continue

        await sftp.close()
        agendamento.status = "publicado"
        agendamento.platform_post_id = url_artigo
        await db.commit()
        publicados += 1

    return publicados
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/api && pytest tests/test_blog_publisher.py -v`
Expected: PASS (3 testes)

- [ ] **Step 5: Commit**

```bash
cd apps/api
git add app/services/blog_publisher.py tests/test_blog_publisher.py
git commit -m "feat: orquestrador do publicador automático de blog"
```

---

### Task 8: Ligar ao scheduler

**Files:**
- Modify: `apps/api/app/scheduler.py`
- Test: manual (o job já roda coberto pelos testes unitários da Task 7; aqui só garantimos que o import/wiring não quebra a suíte)

**Interfaces:**
- Consumes: `publicar_agendamentos_prontos(db) -> int` da Task 7.

- [ ] **Step 1: Wire the new publisher into `job_envios`**

Em `apps/api/app/scheduler.py`, adicione o import (junto aos outros da seção de imports, mantendo ordem alfabética por módulo):

```python
from app.services.blog_publisher import publicar_agendamentos_prontos as publicar_blog_prontos
```

E troque o corpo de `job_envios`:

```python
async def job_envios() -> None:
    async with SessionLocal() as db:
        resend = _resend()
        bv = await processar_boas_vindas(db, resend)
        nl = await processar_fila_newsletter(db, resend)
        ig = await publicar_agendamentos_prontos(db)
        blog = await publicar_blog_prontos(db)
        if bv or nl or ig or blog:
            logger.info(
                "Envios: %d boas-vindas, %d newsletter, %d Instagram, %d blog.", bv, nl, ig, blog
            )
```

- [ ] **Step 2: Run the full suite to confirm nothing broke**

Run: `cd apps/api && pytest -v`
Expected: PASS em todos os testes (suíte completa, incluindo os novos das Tasks 1-7)

- [ ] **Step 3: Commit**

```bash
cd apps/api
git add app/scheduler.py
git commit -m "feat: liga o publicador de blog ao job horário do scheduler"
```

---

## Após a implementação

Depois que todas as tasks passarem localmente:
1. Deploy do `orbit-api` no Railway (`railway up ./apps/api --path-as-root --service orbit-api --detach`), já com `BLOG_SFTP_*` configuradas.
2. Teste ponta a ponta real: aprovar um artigo de teste na Aprovação, aguardar a próxima vaga do playbook e o próximo tick do job (a cada hora, minuto 15), depois conferir manualmente no site (`index.html`, `sitemap.xml` e a página do artigo) se tudo publicou corretamente.
