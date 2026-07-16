import xml.etree.ElementTree as ET

import httpx

from app.integrations.sources.base import BROWSER_USER_AGENT, TLS_VERIFY, SourceDocument

JUSLABORIS_URL = "https://juslaboris.tst.jus.br/open-search/discover"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


async def fetch_tst(query: str = "informativo") -> SourceDocument:
    async with httpx.AsyncClient(timeout=20, verify=TLS_VERIFY) as client:
        response = await client.get(
            JUSLABORIS_URL,
            params={"query": query, "format": "atom"},
            headers={"User-Agent": BROWSER_USER_AGENT},
        )
    response.raise_for_status()

    root = ET.fromstring(response.text)
    lines = []
    for entry in root.findall("atom:entry", ATOM_NS):
        title = entry.findtext("atom:title", default="", namespaces=ATOM_NS)
        published = entry.findtext("atom:published", default="", namespaces=ATOM_NS)
        lines.append(f"{title} — publicado em {published}")

    return SourceDocument(fonte="TST", url=JUSLABORIS_URL, texto="\n".join(lines))
