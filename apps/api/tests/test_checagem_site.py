import pytest

from app.services.checagem_site import checar_site, robos_bloqueados

HOME = """<html><head><title>Letícia Barros</title>
<meta name="description" content="Advocacia trabalhista">
<script type="application/ld+json">{"@type": ["Attorney", "LegalService"], "author": {"@type": "Person"}}</script>
<script src="https://www.googletagmanager.com/gtag/js?id=G-5B513VWB4D"></script></head></html>"""


class SiteFalso:
    def __init__(self, arquivos: dict[str, str]) -> None:
        self.arquivos = arquivos

    async def ler(self, caminho: str) -> str | None:
        return self.arquivos.get(caminho)

    async def listar_html(self) -> list[str]:
        return sorted(c for c in self.arquivos if c.endswith(".html"))


def test_robos_bloqueados_por_grupo_proprio_e_por_asterisco():
    robots = "User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n"
    assert robos_bloqueados(robots) == ["GPTBot"]
    assert set(robos_bloqueados("User-agent: *\nDisallow: /\n")) >= {"ClaudeBot", "PerplexityBot"}
    assert robos_bloqueados("User-agent: *\nDisallow: /admin\n") == []


@pytest.mark.anyio
async def test_checar_site_acha_paginas_a_corrigir():
    site = SiteFalso({
        "index.html": HOME,
        "robots.txt": "User-agent: *\nAllow: /\nUser-agent: CCBot\nDisallow: /\n",
        "sitemap.xml": "<urlset><url><loc>https://ex.com.br/</loc></url><url><loc>https://ex.com.br/lp/g.html</loc></url></urlset>",
        "lp/guia.html": "<html><head><title>Guia</title></head></html>",
        "lp/_rascunho.html": "<html>sem nada</html>",
        "antigo.html": '<meta http-equiv="refresh" content="0; url=/">',
    })
    resultado = await checar_site(site, "ex.com.br")

    assert resultado["home"]["titulo"] == "Letícia Barros"
    assert resultado["home"]["descricao"] == "Advocacia trabalhista"
    assert resultado["home"]["schemas"] == ["Attorney", "LegalService", "Person"]
    assert resultado["home"]["tem_analytics"] is True
    assert resultado["llms_txt"] is False
    assert resultado["robos_ia_bloqueados"] == ["CCBot"]
    assert resultado["sitemap"] == {"ok": True, "paginas": 2}
    assert resultado["paginas_sem_analytics"] == ["lp/guia.html"]
    assert resultado["paginas_sem_descricao"] == ["lp/guia.html"]
