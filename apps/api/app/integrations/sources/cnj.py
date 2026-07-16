import httpx

from app.integrations.sources.base import (
    BROWSER_USER_AGENT,
    TLS_VERIFY,
    SourceDocument,
    clean_html,
)

CNJ_URL = "https://www.cnj.jus.br/agencia-cnj/noticias-do-judiciario/"


async def fetch_cnj() -> SourceDocument:
    async with httpx.AsyncClient(timeout=20, verify=TLS_VERIFY) as client:
        response = await client.get(CNJ_URL, headers={"User-Agent": BROWSER_USER_AGENT})
    response.raise_for_status()
    return SourceDocument(fonte="CNJ", url=CNJ_URL, texto=clean_html(response.text))
