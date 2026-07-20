import httpx

GRAPH_URL = "https://graph.facebook.com/v21.0"


class InstagramAPI:
    def __init__(self, page_token: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._page_token = page_token
        self._transport = transport

    async def _post(self, path: str, data: dict) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=60) as client:
            response = await client.post(
                f"{GRAPH_URL}{path}", data={**data, "access_token": self._page_token}
            )
            response.raise_for_status()
            return response.json()

    async def _get(self, path: str, params: dict) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.get(
                f"{GRAPH_URL}{path}", params={**params, "access_token": self._page_token}
            )
            response.raise_for_status()
            return response.json()

    async def publicar_imagem_unica(self, ig_user_id: str, image_url: str, legenda: str = "") -> str:
        container = await self._post(f"/{ig_user_id}/media", {"image_url": image_url, "caption": legenda})
        publicado = await self._post(f"/{ig_user_id}/media_publish", {"creation_id": container["id"]})
        return publicado["id"]

    async def publicar_carrossel(self, ig_user_id: str, urls_imagens: list[str]) -> str:
        containers_ids = []
        for url in urls_imagens:
            container = await self._post(
                f"/{ig_user_id}/media", {"image_url": url, "is_carousel_item": "true"}
            )
            containers_ids.append(container["id"])

        container_pai = await self._post(
            f"/{ig_user_id}/media",
            {"media_type": "CAROUSEL", "children": ",".join(containers_ids)},
        )
        publicado = await self._post(f"/{ig_user_id}/media_publish", {"creation_id": container_pai["id"]})
        return publicado["id"]

    async def buscar_metricas_conta(self, ig_user_id: str) -> dict:
        perfil = await self._get(f"/{ig_user_id}", {"fields": "followers_count"})
        insights = await self._get(f"/{ig_user_id}/insights", {"metric": "reach", "period": "week"})
        alcance = 0
        for item in insights.get("data", []):
            if item.get("name") == "reach":
                valores = item.get("values", [])
                alcance = valores[-1]["value"] if valores else 0
        return {"seguidores": perfil.get("followers_count", 0), "alcance_7d": alcance}
