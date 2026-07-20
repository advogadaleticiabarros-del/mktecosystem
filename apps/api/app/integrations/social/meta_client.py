import httpx

GRAPH_URL = "https://graph.facebook.com/v21.0"


class MetaClient:
    def __init__(self, app_id: str, app_secret: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._app_id = app_id
        self._app_secret = app_secret
        self._transport = transport

    async def _get(self, path: str, params: dict) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.get(f"{GRAPH_URL}{path}", params=params)
            response.raise_for_status()
            return response.json()

    async def trocar_code_por_token(self, code: str, redirect_uri: str) -> dict:
        return await self._get(
            "/oauth/access_token",
            {
                "client_id": self._app_id,
                "client_secret": self._app_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            },
        )

    async def trocar_por_token_longa_duracao(self, token_curto: str) -> dict:
        return await self._get(
            "/oauth/access_token",
            {
                "grant_type": "fb_exchange_token",
                "client_id": self._app_id,
                "client_secret": self._app_secret,
                "fb_exchange_token": token_curto,
            },
        )

    async def buscar_paginas(self, user_token: str) -> list[dict]:
        resultado = await self._get("/me/accounts", {"access_token": user_token})
        return resultado.get("data", [])

    async def buscar_conta_instagram(self, page_id: str, page_token: str) -> dict | None:
        resultado = await self._get(
            f"/{page_id}", {"fields": "instagram_business_account", "access_token": page_token}
        )
        return resultado.get("instagram_business_account")

    async def buscar_nome_conta_instagram(self, ig_user_id: str, page_token: str) -> str:
        resultado = await self._get(f"/{ig_user_id}", {"fields": "username", "access_token": page_token})
        return resultado.get("username", "")
