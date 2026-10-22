"""Acesso HTTP às APIs do Google com um access token já renovado.

Erros viram `GoogleApiErro` com um `tipo` que a tela sabe explicar:
- "api_desativada": a API não foi ativada no Cloud Console (traz `ativar_em`);
- "reconectar": o token não tem a permissão (escopo) pedida, é preciso reconectar;
- "sem_acesso": a conta conectada não tem acesso ao recurso;
- "nao_encontrado" e "falha": o resto.
"""
import httpx


class GoogleApiErro(Exception):
    def __init__(self, tipo: str, mensagem: str, ativar_em: str | None = None) -> None:
        super().__init__(mensagem)
        self.tipo = tipo
        self.mensagem = mensagem
        self.ativar_em = ativar_em

    def como_dict(self) -> dict:
        return {"tipo": self.tipo, "mensagem": self.mensagem, "ativar_em": self.ativar_em}


def _classificar(response: httpx.Response) -> GoogleApiErro:
    try:
        erro = response.json().get("error", {})
    except ValueError:
        erro = {}
    mensagem = erro.get("message") or response.text[:300] or f"HTTP {response.status_code}"
    detalhes = erro.get("details", [])
    motivos = {d.get("reason") for d in detalhes if isinstance(d, dict)}
    if "SERVICE_DISABLED" in motivos:
        ativar_em = next(
            (d.get("metadata", {}).get("activationUrl") for d in detalhes if d.get("reason") == "SERVICE_DISABLED"),
            None,
        )
        return GoogleApiErro("api_desativada", mensagem, ativar_em)
    if "ACCESS_TOKEN_SCOPE_INSUFFICIENT" in motivos or "insufficient authentication scopes" in mensagem.lower():
        return GoogleApiErro("reconectar", mensagem)
    if response.status_code in (401, 403):
        return GoogleApiErro("sem_acesso", mensagem)
    if response.status_code == 404:
        return GoogleApiErro("nao_encontrado", mensagem)
    return GoogleApiErro("falha", mensagem)


class GoogleApi:
    def __init__(self, access_token: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._headers = {"Authorization": f"Bearer {access_token}"}
        self._transport = transport

    async def chamar(
        self, metodo: str, url: str, *, params: dict | None = None, json: dict | None = None
    ) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=40) as client:
            response = await client.request(metodo, url, params=params, json=json, headers=self._headers)
        if response.status_code >= 400:
            raise _classificar(response)
        return response.json() if response.content else {}

    async def get(self, url: str, params: dict | None = None) -> dict:
        return await self.chamar("GET", url, params=params)

    async def paginar(self, url: str, campo: str, params: dict | None = None, limite: int = 10) -> list:
        """Junta as páginas de uma listagem (`nextPageToken`) até `limite` páginas."""
        itens: list = []
        params = dict(params or {})
        for _ in range(limite):
            resultado = await self.get(url, params)
            itens.extend(resultado.get(campo, []))
            token = resultado.get("nextPageToken")
            if not token:
                break
            params["pageToken"] = token
        return itens
