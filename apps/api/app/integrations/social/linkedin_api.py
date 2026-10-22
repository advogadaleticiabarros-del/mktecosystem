"""API oficial do LinkedIn para publicar no perfil pessoal (produto "Share on LinkedIn", escopo w_member_social).

- OAuth: `url_autorizacao`, `trocar_code` (token de 60 dias; o LinkedIn não dá refresh token a apps comuns)
  e `perfil` (OpenID Connect: `sub` vira o autor `urn:li:person:<sub>`).
- `LinkedInApi.publicar(autor, texto, artigo=None)` -> URN do post. Com `artigo` (link, título, descrição e,
  se houver, bytes da capa), o post sai com o card do link; a capa é enviada pela API de imagens.
- O texto vai no formato "little text" do LinkedIn: caracteres reservados são escapados (senão o post é cortado)
  e as hashtags viram o modelo de hashtag do LinkedIn, para continuarem clicáveis.
- O cabeçalho `LinkedIn-Version` (AAAAMM) muda todo mês e versões antigas são desligadas: começamos dois meses
  atrás e, se o LinkedIn disser que a versão não existe, recuamos um mês por vez.
"""
import re
from datetime import date
from urllib.parse import urlencode

import httpx

AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
API_URL = "https://api.linkedin.com"
ESCOPOS = "openid profile w_member_social"
RESERVADOS = re.compile(r"([\\|{}@\[\]()<>*_~#])")
HASHTAG = re.compile(r"(?<![\w#])#([A-Za-zÀ-ÿ0-9_]+)")


class LinkedInErro(Exception):
    def __init__(self, mensagem: str, status: int = 0, reconectar: bool = False) -> None:
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status
        self.reconectar = reconectar


def escapar_texto(texto: str) -> str:
    """Formato "little text": escapa os reservados e transforma #tag em {hashtag|\\#|tag}."""
    partes, ultimo = [], 0
    for m in HASHTAG.finditer(texto):
        partes.append(RESERVADOS.sub(r"\\\1", texto[ultimo:m.start()]))
        partes.append("{hashtag|\\#|" + m.group(1) + "}")
        ultimo = m.end()
    partes.append(RESERVADOS.sub(r"\\\1", texto[ultimo:]))
    return "".join(partes)


def url_autorizacao(client_id: str, redirect_uri: str, state: str) -> str:
    return AUTH_URL + "?" + urlencode({
        "response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri,
        "state": state, "scope": ESCOPOS,
    })


async def trocar_code(client_id: str, client_secret: str, code: str, redirect_uri: str,
                      transport: httpx.AsyncBaseTransport | None = None) -> dict:
    async with httpx.AsyncClient(transport=transport, timeout=30) as c:
        r = await c.post(TOKEN_URL, data={
            "grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri,
            "client_id": client_id, "client_secret": client_secret,
        })
    if r.status_code >= 400:
        raise LinkedInErro(f"O LinkedIn recusou a conexão: {r.text[:200]}", r.status_code)
    return r.json()


async def perfil(access_token: str, transport: httpx.AsyncBaseTransport | None = None) -> dict:
    async with httpx.AsyncClient(transport=transport, timeout=30) as c:
        r = await c.get(f"{API_URL}/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    if r.status_code >= 400:
        raise LinkedInErro(f"Não deu para ler o perfil: {r.text[:200]}", r.status_code, r.status_code == 401)
    return r.json()


async def credenciais_validas(client_id: str, client_secret: str,
                              transport: httpx.AsyncBaseTransport | None = None) -> bool:
    """Testa o par Client ID + Secret sem login: só `invalid_client` quer dizer chave errada (apps comuns não têm
    o fluxo client_credentials, então os outros erros também confirmam que o par existe)."""
    async with httpx.AsyncClient(transport=transport, timeout=30) as c:
        r = await c.post(TOKEN_URL, data={"grant_type": "client_credentials", "client_id": client_id,
                                          "client_secret": client_secret})
    if r.status_code < 400:
        return True
    corpo = r.json() if r.content and r.headers.get("content-type", "").startswith("application/json") else {}
    return corpo.get("error") != "invalid_client" and r.status_code != 401


def _versao_inicial(hoje: date) -> str:
    total = hoje.year * 12 + hoje.month - 1 - 2
    return f"{total // 12}{total % 12 + 1:02d}"


def _mes_anterior(versao: str) -> str:
    total = int(versao[:4]) * 12 + int(versao[4:]) - 1 - 1
    return f"{total // 12}{total % 12 + 1:02d}"


class LinkedInApi:
    def __init__(self, access_token: str, transport: httpx.AsyncBaseTransport | None = None,
                 hoje: date | None = None) -> None:
        self._token = access_token
        self._transport = transport
        self.versao = _versao_inicial(hoje or date.today())

    async def _rest(self, metodo: str, caminho: str, json: dict | None = None,
                    params: dict | None = None) -> httpx.Response:
        for _ in range(12):
            headers = {"Authorization": f"Bearer {self._token}", "LinkedIn-Version": self.versao,
                       "X-Restli-Protocol-Version": "2.0.0"}
            async with httpx.AsyncClient(transport=self._transport, timeout=40) as c:
                r = await c.request(metodo, f"{API_URL}{caminho}", json=json, params=params, headers=headers)
            if r.status_code == 426 or "NONEXISTENT_VERSION" in r.text or "VERSION_MISSING" in r.text:
                self.versao = _mes_anterior(self.versao)
                continue
            if r.status_code == 401:
                raise LinkedInErro("A conexão com o LinkedIn venceu. Reconecte na Visão Geral.", 401, True)
            if r.status_code >= 400:
                raise LinkedInErro(f"O LinkedIn recusou: {r.text[:300]}", r.status_code)
            return r
        raise LinkedInErro("Nenhuma versão da API do LinkedIn foi aceita.")

    async def subir_imagem(self, autor: str, conteudo: bytes) -> str:
        r = await self._rest("POST", "/rest/images", params={"action": "initializeUpload"},
                             json={"initializeUploadRequest": {"owner": autor}})
        valor = r.json()["value"]
        async with httpx.AsyncClient(transport=self._transport, timeout=60) as c:
            envio = await c.put(valor["uploadUrl"], content=conteudo, headers={"Authorization": f"Bearer {self._token}"})
        if envio.status_code >= 400:
            raise LinkedInErro(f"Falha ao enviar a imagem: {envio.text[:200]}", envio.status_code)
        return valor["image"]

    async def publicar(self, autor: str, texto: str, artigo: dict | None = None) -> str:
        corpo: dict = {
            "author": autor,
            "commentary": escapar_texto(texto),
            "visibility": "PUBLIC",
            "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }
        if artigo:
            card = {"source": artigo["link"], "title": artigo.get("titulo") or artigo["link"]}
            if artigo.get("descricao"):
                card["description"] = artigo["descricao"]
            if artigo.get("capa"):
                card["thumbnail"] = await self.subir_imagem(autor, artigo["capa"])
            corpo["content"] = {"article": card}
        r = await self._rest("POST", "/rest/posts", json=corpo)
        return r.headers.get("x-restli-id") or r.headers.get("x-linkedin-id") or ""

    async def apagar(self, post_urn: str) -> None:
        from urllib.parse import quote

        await self._rest("DELETE", f"/rest/posts/{quote(post_urn, safe='')}")


def link_do_post(post_urn: str) -> str:
    return f"https://www.linkedin.com/feed/update/{post_urn}/"
