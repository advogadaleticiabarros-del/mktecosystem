import logging

import httpx

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"


class ResendClient:
    """Entrega de e-mail via API transacional do Resend.

    Sem api_key configurada (dev), send() vira no-op logado e retorna None,
    para o restante do fluxo poder rodar sem credenciais.
    """

    def __init__(
        self,
        api_key: str,
        sender: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._api_key = api_key
        self._sender = sender
        self._transport = transport

    async def send(self, to: str, subject: str, html: str, text: str) -> str | None:
        if not self._api_key:
            logger.info("RESEND_API_KEY ausente; e-mail para %s não enviado (no-op).", to)
            return None

        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.post(
                RESEND_API_URL,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={
                    "from": self._sender,
                    "to": [to],
                    "subject": subject,
                    "html": html,
                    "text": text,
                },
            )
            response.raise_for_status()
            return response.json().get("id")


def montar_rodape(assinatura: str, unsubscribe_url: str) -> str:
    return (
        '<hr style="border:none;border-top:1px solid #ddd;margin:32px 0 16px">'
        f'<p style="font-size:12px;color:#888">{assinatura}<br>'
        "Você recebe este e-mail porque se cadastrou em nosso site. "
        f'<a href="{unsubscribe_url}">Descadastrar</a></p>'
    )
