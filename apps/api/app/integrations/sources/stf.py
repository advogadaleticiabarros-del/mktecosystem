import httpx

from app.integrations.sources.base import BROWSER_USER_AGENT, SourceDocument, clean_html

STF_URL = "https://portal.stf.jus.br/textos/verTexto.asp?servico=informativoSTF"


async def fetch_stf() -> SourceDocument:
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            STF_URL,
            headers={"User-Agent": BROWSER_USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"},
        )
    response.raise_for_status()
    return SourceDocument(fonte="STF", url=STF_URL, texto=clean_html(response.text))
