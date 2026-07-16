import httpx

from app.integrations.sources.base import (
    BROWSER_USER_AGENT,
    SourceDocument,
    clean_html,
)

STF_URL = "https://portal.stf.jus.br/textos/verTexto.asp?servico=informativoSTF"

# portal.stf.jus.br sends a malformed TLS chain: position 1 duplicates the
# leaf certificate (*.stf.jus.br) instead of the actual intermediate CA
# (GlobalSign GCC R6 AlphaSSL CA 2025), confirmed with
# `openssl s_client -connect portal.stf.jus.br:443` (verify code 21,
# "unable to verify the first certificate"). This is a server-side
# misconfiguration on STF's end, not fixable by any client-side CA bundle —
# TST and CNJ both verify cleanly with the default trust store. Read-only
# fetch of public jurisprudence bulletins, no sensitive data exchanged.
STF_TLS_VERIFY = False


async def fetch_stf() -> SourceDocument:
    async with httpx.AsyncClient(timeout=20, verify=STF_TLS_VERIFY) as client:
        response = await client.get(
            STF_URL,
            headers={"User-Agent": BROWSER_USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"},
        )
    response.raise_for_status()
    return SourceDocument(fonte="STF", url=STF_URL, texto=clean_html(response.text))
