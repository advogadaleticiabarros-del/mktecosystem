"""Confere um e-mail antes de entrar na lista: formato, e-mail descartável e se o domínio recebe e-mail.

Interface: `VerificadorEmail().verificar(email)` → `Verificacao` com `situacao`:
- "ok": pode entrar na lista;
- "invalido": formato errado (nem consulta a internet);
- "descartavel": e-mail temporário (10minutemail etc.);
- "sem_caixa": o domínio não recebe e-mail (sem registro MX).
Fonte: Disify (sem chave); se cair, o Kickbox aberto responde só sobre descartável. Se as duas caírem, volta
"ok" com `conferido=False`: melhor aceitar do que perder um contato real.
"""
import re
from dataclasses import dataclass

import httpx

DISIFY = "https://www.disify.com/api/email/{email}"
KICKBOX = "https://open.kickbox.com/v1/disposable/{dominio}"
FORMATO = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)


@dataclass(frozen=True)
class Verificacao:
    email: str
    situacao: str
    conferido: bool = True


class VerificadorEmail:
    def __init__(self, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._transport = transport

    async def verificar(self, email: str) -> Verificacao:
        email = (email or "").strip().lower()
        if not FORMATO.match(email):
            return Verificacao(email, "invalido")
        async with httpx.AsyncClient(transport=self._transport, timeout=15) as c:
            try:
                r = await c.get(DISIFY.format(email=email))
                r.raise_for_status()
                d = r.json()
                if not d.get("format", True):
                    return Verificacao(email, "invalido")
                if d.get("disposable"):
                    return Verificacao(email, "descartavel")
                if d.get("dns") is False:
                    return Verificacao(email, "sem_caixa")
                return Verificacao(email, "ok")
            except (httpx.HTTPError, ValueError):
                pass
            try:
                r = await c.get(KICKBOX.format(dominio=email.split("@")[1]))
                r.raise_for_status()
                return Verificacao(email, "descartavel" if r.json().get("disposable") else "ok")
            except (httpx.HTTPError, ValueError):
                return Verificacao(email, "ok", conferido=False)
