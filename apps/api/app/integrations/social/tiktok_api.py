"""TikTok (Login Kit + Content Posting API v2).

Interface:
- `url_autorizacao(client_key, redirect_uri, state)`: para onde mandar a pessoa autorizar o Orbit.
- `trocar_code_por_tokens(...)` / `renovar_tokens(...)`: devolvem `TokensTikTok` (access de 24 h, refresh de 1 ano).
- `TikTokAPI(access_token).perfil()`: nome e usuário da conta conectada.
- `TikTokAPI(access_token).publicar_video(video, legenda, ia=False)` -> {modo, publish_id, post_id, privacidade}.
  Envia o arquivo (FILE_UPLOAD, em partes; não precisa verificar domínio no app da TikTok) e:
  - `modo="publico"`: post direto e público, quando a conta permite e o app já passou pela auditoria da TikTok;
  - `modo="rascunho"`: se o app ainda não foi auditado (a TikTok só aceitaria post privado), o vídeo vai para a
    caixa de rascunhos do TikTok da conta, que recebe uma notificação e publica pelo app, público, com a legenda.
  Espera até PUBLISH_COMPLETE (público) ou SEND_TO_USER_INBOX (rascunho).
Erros da TikTok viram `ErroTikTok` com o código e a mensagem dela.
"""
import asyncio
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx

API = "https://open.tiktokapis.com"
ESCOPOS = "user.info.basic,video.upload,video.publish"
PUBLICO = "PUBLIC_TO_EVERYONE"
FINAIS = {"PUBLISH_COMPLETE": "publico", "SEND_TO_USER_INBOX": "rascunho"}
PARTE = 10_000_000  # 10 MB; a TikTok aceita partes de 5 a 64 MB, e a última pode ir até 128 MB
MINIMO_PARTE = 5_000_000
NAO_AUDITADO = ("unaudited_client", "privacy_level_option_mismatch")


class ErroTikTok(RuntimeError):
    """A TikTok recusou ou não concluiu a operação."""

    def __init__(self, mensagem: str, codigo: str = "") -> None:
        super().__init__(mensagem)
        self.codigo = codigo


@dataclass(frozen=True)
class TokensTikTok:
    access_token: str
    refresh_token: str
    open_id: str
    expira_em: datetime
    refresh_expira_em: datetime

    def para_json(self) -> str:
        d = asdict(self)
        d["expira_em"], d["refresh_expira_em"] = self.expira_em.isoformat(), self.refresh_expira_em.isoformat()
        return json.dumps(d)

    @classmethod
    def de_json(cls, texto: str) -> "TokensTikTok":
        d = json.loads(texto)
        return cls(d["access_token"], d["refresh_token"], d["open_id"],
                   datetime.fromisoformat(d["expira_em"]), datetime.fromisoformat(d["refresh_expira_em"]))


def url_autorizacao(client_key: str, redirect_uri: str, state: str) -> str:
    return "https://www.tiktok.com/v2/auth/authorize/?" + urlencode({
        "client_key": client_key, "scope": ESCOPOS, "response_type": "code", "redirect_uri": redirect_uri, "state": state})


async def _tokens(dados: dict, transport) -> TokensTikTok:
    async with httpx.AsyncClient(transport=transport, timeout=30) as client:
        resposta = await client.post(f"{API}/v2/oauth/token/", data=dados)
    corpo = resposta.json() if resposta.content else {}
    if corpo.get("error") or not corpo.get("access_token"):
        raise ErroTikTok(corpo.get("error_description") or corpo.get("error") or f"HTTP {resposta.status_code}",
                         str(corpo.get("error") or ""))
    agora = datetime.now(timezone.utc)
    return TokensTikTok(corpo["access_token"], corpo["refresh_token"], corpo["open_id"],
                        agora + timedelta(seconds=int(corpo.get("expires_in", 86400))),
                        agora + timedelta(seconds=int(corpo.get("refresh_expires_in", 31536000))))


async def trocar_code_por_tokens(client_key, client_secret, code, redirect_uri, transport=None) -> TokensTikTok:
    return await _tokens({"client_key": client_key, "client_secret": client_secret, "code": code,
                          "grant_type": "authorization_code", "redirect_uri": redirect_uri}, transport)


async def renovar_tokens(client_key, client_secret, refresh_token, transport=None) -> TokensTikTok:
    return await _tokens({"client_key": client_key, "client_secret": client_secret,
                          "grant_type": "refresh_token", "refresh_token": refresh_token}, transport)


def partes_do_envio(tamanho: int) -> tuple[int, int]:
    """(tamanho da parte, quantidade de partes) pela regra da TikTok: abaixo de 5 MB vai inteiro; acima, partes de
    10 MB e a sobra entra na última."""
    if tamanho <= MINIMO_PARTE:
        return tamanho, 1
    return PARTE, max(1, tamanho // PARTE)


class TikTokAPI:
    def __init__(self, access_token: str, transport: httpx.AsyncBaseTransport | None = None,
                 espera: float = 5.0, tentativas: int = 120) -> None:
        self._token = access_token
        self._transport = transport
        self._espera = espera
        self._tentativas = tentativas

    async def _chamar(self, metodo: str, caminho: str, **kw) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=60) as client:
            resposta = await client.request(metodo, f"{API}{caminho}", headers={
                "Authorization": f"Bearer {self._token}", "Content-Type": "application/json; charset=UTF-8"}, **kw)
        corpo = resposta.json() if resposta.content else {}
        erro = corpo.get("error") or {}
        if resposta.status_code >= 400 or (isinstance(erro, dict) and erro.get("code") not in (None, "ok")):
            codigo = erro.get("code", "") if isinstance(erro, dict) else str(erro)
            mensagem = erro.get("message", "") if isinstance(erro, dict) else ""
            raise ErroTikTok(f"{codigo}: {mensagem}", str(codigo))
        return corpo.get("data") or {}

    async def perfil(self) -> dict:
        dados = await self._chamar("GET", "/v2/user/info/", params={"fields": "open_id,display_name,avatar_url"})
        return dados.get("user", {})

    async def _iniciar_publico(self, origem: dict, legenda: str, ia: bool) -> dict:
        info = await self._chamar("POST", "/v2/post/publish/creator_info/query/", json={})
        if PUBLICO not in (info.get("privacy_level_options") or []):
            raise ErroTikTok("a conta não permite post público por API", "privacy_level_option_mismatch")
        post_info = {"title": legenda[:2200], "privacy_level": PUBLICO, "disable_duet": False,
                     "disable_comment": False, "disable_stitch": False, "video_cover_timestamp_ms": 1000}
        if ia:
            post_info["is_aigc"] = True
        return await self._chamar("POST", "/v2/post/publish/video/init/",
                                  json={"post_info": post_info, "source_info": origem})

    async def _enviar(self, upload_url: str, video: bytes, parte: int, total: int) -> None:
        async with httpx.AsyncClient(transport=self._transport, timeout=300) as client:
            for i in range(total):
                inicio = i * parte
                fim = len(video) if i == total - 1 else inicio + parte
                r = await client.put(upload_url, content=video[inicio:fim], headers={
                    "Content-Type": "video/mp4", "Content-Range": f"bytes {inicio}-{fim - 1}/{len(video)}"})
                if r.status_code >= 400:
                    raise ErroTikTok(f"envio do vídeo recusado (parte {i + 1}/{total}): HTTP {r.status_code}",
                                     "upload_falhou")

    async def publicar_video(self, video: bytes, legenda: str, ia: bool = False) -> dict:
        parte, total = partes_do_envio(len(video))
        origem = {"source": "FILE_UPLOAD", "video_size": len(video), "chunk_size": parte, "total_chunk_count": total}
        try:
            dados, privacidade = await self._iniciar_publico(origem, legenda, ia), PUBLICO
        except ErroTikTok as erro:
            if not any(c in erro.codigo for c in NAO_AUDITADO):
                raise
            dados, privacidade = await self._chamar("POST", "/v2/post/publish/inbox/video/init/",
                                                    json={"source_info": origem}), None
        publish_id = dados["publish_id"]
        await self._enviar(dados["upload_url"], video, parte, total)
        for _ in range(self._tentativas):
            st = await self._chamar("POST", "/v2/post/publish/status/fetch/", json={"publish_id": publish_id})
            situacao = st.get("status")
            if situacao in FINAIS:
                ids = st.get("publicaly_available_post_id") or []
                return {"modo": FINAIS[situacao], "publish_id": publish_id, "privacidade": privacidade,
                        "post_id": str(ids[0]) if ids else None}
            if situacao == "FAILED":
                raise ErroTikTok(f"publicação falhou: {st.get('fail_reason')}", str(st.get("fail_reason") or "failed"))
            await asyncio.sleep(self._espera)
        raise ErroTikTok("a TikTok não concluiu a publicação a tempo", "tempo_esgotado")
