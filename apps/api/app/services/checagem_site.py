"""Checagem do site para SEO e para as IAs, lendo os arquivos publicados.

O site fica atrás de uma proteção anti-robô da hospedagem que barra clientes de
automação (os robôs de busca e de IA passam). Por isso a checagem lê os arquivos
direto da hospedagem: o adaptador `Site` sabe `ler(caminho)` e `listar_html()`.
Em produção é `SiteSftp` (mesmo acesso SFTP do publicador do blog).

Interface: `await checar_site(site, dominio)` devolve:
- `robos_ia_bloqueados`: robôs de IA que o robots.txt proíbe de ler o site inteiro;
- `llms_txt`: se existe /llms.txt;
- `home`: título, descrição, tipos de dados estruturados (schema.org) e se tem Analytics;
- `sitemap`: quantas páginas lista;
- `paginas_html`: quantas páginas .html existem;
- `paginas_sem_analytics` e `paginas_sem_descricao`: páginas a corrigir (sem rascunhos `_*`).
"""
import asyncio
import re
from typing import Protocol

ROBOS_IA = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot",
            "Google-Extended", "Applebot-Extended", "CCBot", "Bingbot"]
TAG_ANALYTICS = re.compile(r"G-[A-Z0-9]{6,12}|GTM-[A-Z0-9]{4,8}")
TIPO_SCHEMA = re.compile(r'"@type"\s*:\s*(\[[^\]]*\]|"[A-Za-z]+")')
IGNORAR = re.compile(r"(^|/)(_|404|google[0-9a-f]+\.html|BingSiteAuth)")


class Site(Protocol):
    async def ler(self, caminho: str) -> str | None: ...

    async def listar_html(self) -> list[str]: ...


class SiteSftp:
    def __init__(self, sftp, raiz: str) -> None:
        self._sftp = sftp
        self._raiz = raiz.rstrip("/")

    async def ler(self, caminho: str) -> str | None:
        try:
            return (await self._sftp.download(f"{self._raiz}/{caminho}")).decode("utf-8", "replace")
        except Exception:
            return None

    async def listar_html(self) -> list[str]:
        return await self._sftp.listar_recursivo(self._raiz, ".html")

    async def ler_bytes(self, caminho: str) -> bytes | None:
        try:
            return await self._sftp.download(f"{self._raiz}/{caminho}")
        except Exception:
            return None


def robos_bloqueados(robots: str) -> list[str]:
    """Robôs (da lista ROBOS_IA) com `Disallow: /` no grupo deles ou no grupo `*`."""
    grupos: dict[str, list[str]] = {}
    agentes: list[str] = []
    lendo_regras = False
    for linha in robots.splitlines():
        linha = linha.split("#", 1)[0].strip()
        if ":" not in linha:
            continue
        chave, valor = (p.strip() for p in linha.split(":", 1))
        chave = chave.lower()
        if chave == "user-agent":
            if lendo_regras:
                agentes, lendo_regras = [], False
            agentes.append(valor.lower())
            for a in agentes:
                grupos.setdefault(a, [])
        elif chave in ("disallow", "allow"):
            lendo_regras = True
            for a in agentes:
                grupos[a].append(f"{chave}:{valor}".replace(" ", ""))

    bloqueados = []
    for robo in ROBOS_IA:
        regras = grupos.get(robo.lower(), grupos.get("*", []))
        if "disallow:/" in regras and "allow:/" not in regras:
            bloqueados.append(robo)
    return bloqueados


def _meta(html: str, nome: str) -> str | None:
    achado = re.search(rf'<meta[^>]+name=["\']{nome}["\'][^>]*content=["\']([^"\']*)', html, re.IGNORECASE)
    return achado.group(1).strip() if achado else None


def _e_redirecionamento(html: str) -> bool:
    return bool(re.search(r'http-equiv=["\']refresh', html, re.IGNORECASE))


async def checar_site(site: Site, dominio: str) -> dict:
    home, robots, llms, sitemap = await asyncio.gather(
        site.ler("index.html"), site.ler("robots.txt"), site.ler("llms.txt"), site.ler("sitemap.xml")
    )
    home = home or ""
    urls_sitemap = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap or "")

    paginas = [p for p in await site.listar_html() if not IGNORAR.search(p)]
    sem_analytics: list[str] = []
    sem_descricao: list[str] = []
    semaforo = asyncio.Semaphore(4)

    async def conferir(caminho: str) -> None:
        async with semaforo:
            html = await site.ler(caminho)
        if not html or _e_redirecionamento(html):
            return
        if not TAG_ANALYTICS.search(html):
            sem_analytics.append(caminho)
        if not _meta(html, "description"):
            sem_descricao.append(caminho)

    await asyncio.gather(*(conferir(p) for p in paginas))

    titulo = re.search(r"<title>(.*?)</title>", home, re.IGNORECASE | re.DOTALL)
    return {
        "dominio": dominio,
        "home": {
            "titulo": titulo.group(1).strip() if titulo else None,
            "descricao": _meta(home, "description"),
            "schemas": sorted({t for bloco in TIPO_SCHEMA.findall(home) for t in re.findall(r"[A-Za-z]+", bloco)}),
            "tem_analytics": bool(TAG_ANALYTICS.search(home)),
        },
        "robots_txt": robots is not None,
        "robos_ia_bloqueados": robos_bloqueados(robots) if robots else [],
        "llms_txt": llms is not None,
        "sitemap": {"ok": sitemap is not None, "paginas": len(urls_sitemap)},
        "paginas_html": len(paginas),
        "paginas_sem_analytics": sorted(sem_analytics),
        "paginas_sem_descricao": sorted(sem_descricao),
    }
