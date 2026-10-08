import asyncio
from datetime import datetime, timezone

import httpx

GRAPH_URL = "https://graph.facebook.com/v21.0"


class InstagramAPI:
    _espera_segundos = 3
    _tentativas_status = 40

    def __init__(self, page_token: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._page_token = page_token
        self._transport = transport

    async def _aguardar(self, container_id: str) -> None:
        """A Meta processa a imagem antes de aceitar a publicação; publicar antes do
        FINISHED dá erro ("media not ready"). Resposta sem status = pronto."""
        for _ in range(self._tentativas_status):
            estado = (await self._get(f"/{container_id}", {"fields": "status_code"})).get("status_code")
            if estado in (None, "FINISHED", "PUBLISHED"):
                return
            if estado in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"A Meta recusou a mídia do container {container_id} ({estado})")
            await asyncio.sleep(self._espera_segundos)
        raise RuntimeError(f"A Meta não terminou de processar o container {container_id}")

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
        await self._aguardar(container["id"])
        publicado = await self._post(f"/{ig_user_id}/media_publish", {"creation_id": container["id"]})
        return publicado["id"]

    async def publicar_carrossel(self, ig_user_id: str, urls_imagens: list[str], legenda: str = "") -> str:
        containers_ids = []
        for url in urls_imagens:
            container = await self._post(
                f"/{ig_user_id}/media", {"image_url": url, "is_carousel_item": "true"}
            )
            await self._aguardar(container["id"])
            containers_ids.append(container["id"])

        container_pai = await self._post(
            f"/{ig_user_id}/media",
            {"media_type": "CAROUSEL", "children": ",".join(containers_ids), "caption": legenda},
        )
        await self._aguardar(container_pai["id"])
        publicado = await self._post(f"/{ig_user_id}/media_publish", {"creation_id": container_pai["id"]})
        return publicado["id"]

    async def posts_de_perfil_publico(self, ig_user_id: str, username: str, limite: int = 30) -> list[dict]:
        """Posts recentes de outra conta comercial/criador (business discovery)."""
        campos = (f"business_discovery.username({username}){{media.limit({limite})"
                  "{caption,media_type,like_count,comments_count,timestamp,permalink}}")
        resposta = await self._get(f"/{ig_user_id}", {"fields": campos})
        return resposta.get("business_discovery", {}).get("media", {}).get("data", [])

    async def comentar(self, media_id: str, texto: str) -> str:
        """Comenta no post como o próprio perfil (o "primeiro comentário")."""
        comentario = await self._post(f"/{media_id}/comments", {"message": texto})
        return comentario["id"]

    async def listar_publicacoes(self, ig_user_id: str, limite: int = 2000) -> list[dict]:
        """Todas as publicações do perfil, cada uma com `insights` = {métrica: valor}.

        Um insight que a API recusa (post antigo, métrica não suportada) vira {}
        para aquele post, sem derrubar a lista.
        """
        campos = "id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count"
        posts: list[dict] = []
        params: dict = {"fields": campos, "limit": 100}
        while len(posts) < limite:
            pagina = await self._get(f"/{ig_user_id}/media", params)
            posts += pagina.get("data", [])
            paging = pagina.get("paging", {})
            if not paging.get("next"):
                break
            params = {"fields": campos, "limit": 100, "after": paging.get("cursors", {}).get("after")}

        limitador = asyncio.Semaphore(8)

        async def com_insights(post: dict) -> dict:
            async with limitador:
                post["insights"] = await self._insights_do_post(post)
            return post

        return list(await asyncio.gather(*(com_insights(p) for p in posts)))

    async def _insights_do_post(self, post: dict) -> dict:
        if post.get("media_product_type") == "REELS":
            tentativas = ["reach,saved,shares,total_interactions,views,likes,comments"]
        else:
            tentativas = [
                "reach,saved,shares,total_interactions,views,likes,comments,profile_visits,follows",
                "reach,saved,shares,total_interactions,views,likes,comments",
            ]
        for metricas in tentativas:
            try:
                resposta = await self._get(f"/{post['id']}/insights", {"metric": metricas})
            except httpx.HTTPStatusError:
                continue
            return {d["name"]: d["values"][0]["value"] for d in resposta.get("data", []) if d.get("values")}
        return {}

    async def buscar_raio_x(self, ig_user_id: str, agora: datetime | None = None) -> dict:
        """Retrato da conta: perfil, alcance diário (90 dias), novos seguidores
        por dia (30 dias), totais dos últimos 30 dias e público."""
        agora = agora or datetime.now(timezone.utc)
        fim = int(agora.timestamp())
        dia = 86400

        async def serie(metrica: str, janelas: int) -> list[list]:
            pontos: dict[str, int] = {}
            for k in range(janelas):
                ate = fim - k * 30 * dia
                try:
                    r = await self._get(
                        f"/{ig_user_id}/insights",
                        {"metric": metrica, "period": "day", "since": ate - 30 * dia, "until": ate},
                    )
                except httpx.HTTPStatusError:
                    continue
                for item in r.get("data", []):
                    for v in item.get("values", []):
                        pontos[v["end_time"][:10]] = v.get("value", 0)
            return [[d, pontos[d]] for d in sorted(pontos)]

        totais_metricas = "reach,views,accounts_engaged,total_interactions,profile_views,website_clicks,likes,comments,saves,shares"
        totais: dict = {}
        try:
            r = await self._get(
                f"/{ig_user_id}/insights",
                {"metric": totais_metricas, "period": "day", "metric_type": "total_value",
                 "since": fim - 29 * dia, "until": fim},
            )
            totais = {d["name"]: d.get("total_value", {}).get("value", 0) for d in r.get("data", [])}
        except httpx.HTTPStatusError:
            pass

        demografia: dict = {}
        for chave, breakdown in (("cidades", "city"), ("idade", "age"), ("genero", "gender")):
            try:
                r = await self._get(
                    f"/{ig_user_id}/insights",
                    {"metric": "follower_demographics", "period": "lifetime",
                     "metric_type": "total_value", "breakdown": breakdown},
                )
                resultados = r["data"][0]["total_value"]["breakdowns"][0]["results"]
                demografia[chave] = {x["dimension_values"][0]: x["value"] for x in resultados}
            except (httpx.HTTPStatusError, KeyError, IndexError):
                demografia[chave] = {}

        perfil = await self._get(
            f"/{ig_user_id}", {"fields": "username,followers_count,follows_count,media_count"}
        )
        return {
            "perfil": perfil,
            "serie_alcance": await serie("reach", 3),
            "serie_seguidores": await serie("follower_count", 1),
            "totais_30d": totais,
            "demografia": demografia,
        }

    async def buscar_metricas_conta(self, ig_user_id: str) -> dict:
        perfil = await self._get(f"/{ig_user_id}", {"fields": "followers_count"})
        insights = await self._get(f"/{ig_user_id}/insights", {"metric": "reach", "period": "week"})
        alcance = 0
        for item in insights.get("data", []):
            if item.get("name") == "reach":
                valores = item.get("values", [])
                alcance = valores[-1]["value"] if valores else 0
        return {"seguidores": perfil.get("followers_count", 0), "alcance_7d": alcance}
