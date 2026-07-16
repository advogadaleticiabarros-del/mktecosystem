from dataclasses import dataclass

import certifi
from bs4 import BeautifulSoup

BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# Some minimal container images (e.g. Railway's Nixpacks builds) ship
# without a complete system CA bundle, which makes httpx's default TLS
# verification fail with CERTIFICATE_VERIFY_FAILED even for legitimate
# sites. Pointing httpx at certifi's bundled CA file explicitly sidesteps
# that regardless of what the underlying system trust store looks like.
TLS_VERIFY = certifi.where()


@dataclass
class SourceDocument:
    fonte: str
    url: str
    texto: str


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())
