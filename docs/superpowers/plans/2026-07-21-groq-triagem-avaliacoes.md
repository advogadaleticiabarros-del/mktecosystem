# Groq — Triagem de Avaliações — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Classificar avaliações do Google Meu Negócio sem resposta como `urgente`/`normal` via Groq, e ordenar a lista com as urgentes primeiro.

**Architecture:** `GroqClient` novo implementando o mesmo protocolo `AIClient` (`generate_json`/`generate_text`) já usado pelo `GeminiClient`. Um serviço `classificar_avaliacoes` roda em paralelo (`asyncio.gather`) sobre as avaliações sem resposta, chamado dentro da rota `GET /avaliacoes` já existente.

**Tech Stack:** `httpx` (API do Groq, formato compatível com OpenAI `chat/completions`), `asyncio.gather` para paralelismo.

## Global Constraints
- Avaliação já respondida (`reviewReply` presente) nunca é enviada ao Groq — recebe `urgencia: null` direto.
- Falha na chamada ao Groq nunca derruba a listagem — vira `urgencia: null` para aquela avaliação, resto da lista segue normal.
- Nova env var: `GROQ_API_KEY` (vazia em dev → `GroqClient` sem key retorna erro tratado como falha silenciosa pelo serviço de triagem, mesmo padrão do `ResendClient`).
- Modelo: `llama-3.3-70b-versatile`.

---

### Task 1: `GroqClient`

**Files:**
- Create: `apps/api/app/integrations/ai/groq_client.py`
- Modify: `apps/api/app/config.py`
- Test: `apps/api/tests/test_groq_client.py`

**Interfaces:**
- Produces: `GroqClient(api_key, transport=None)` implementando `generate_json(prompt: str) -> dict` e `generate_text(prompt: str) -> str` (mesmo protocolo `AIClient` de `app/integrations/ai/base.py`).

- [ ] **Step 1: Escrever o teste**

```python
# apps/api/tests/test_groq_client.py
import json

import httpx
import pytest

from app.integrations.ai.groq_client import GroqClient


@pytest.mark.anyio
async def test_generate_text():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "groq.com/openai/v1/chat/completions" in str(request.url)
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Olá!"}}]},
        )

    transport = httpx.MockTransport(handler)
    client = GroqClient(api_key="chave", transport=transport)
    resultado = await client.generate_text("diga oi")
    assert resultado == "Olá!"


@pytest.mark.anyio
async def test_generate_json():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": '{"urgencia": "normal"}'}}]},
        )

    transport = httpx.MockTransport(handler)
    client = GroqClient(api_key="chave", transport=transport)
    resultado = await client.generate_json("classifique")
    assert resultado == {"urgencia": "normal"}


@pytest.mark.anyio
async def test_generate_text_sem_api_key_levanta_erro():
    client = GroqClient(api_key="")
    with pytest.raises(ValueError):
        await client.generate_text("oi")
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_groq_client.py -v`
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 3: Implementar**

```python
# apps/api/app/integrations/ai/groq_client.py
import json

import httpx

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


class GroqClient:
    def __init__(self, api_key: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._api_key = api_key
        self._transport = transport

    async def _chat(self, prompt: str, forcar_json: bool) -> str:
        if not self._api_key:
            raise ValueError("GROQ_API_KEY não configurada")

        body = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }
        if forcar_json:
            body["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json=body,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def generate_text(self, prompt: str) -> str:
        return await self._chat(prompt, forcar_json=False)

    async def generate_json(self, prompt: str) -> dict:
        texto = await self._chat(prompt, forcar_json=True)
        return json.loads(texto)
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_groq_client.py -v`
Expected: PASS (3 testes)

- [ ] **Step 5: Adicionar env var**

Em `apps/api/app/config.py`, adicionar dentro da classe `Settings`:
```python
    GROQ_API_KEY: str = ""
```

- [ ] **Step 6: Commit**

```bash
git add apps/api/app/integrations/ai/groq_client.py apps/api/app/config.py apps/api/tests/test_groq_client.py
git commit -m "feat: cliente Groq (mesmo protocolo AIClient do Gemini)"
```

---

### Task 2: Serviço de triagem

**Files:**
- Create: `apps/api/app/services/triagem_avaliacoes.py`
- Test: `apps/api/tests/test_triagem_avaliacoes.py`

**Interfaces:**
- Consumes: `AIClient` protocol (Task 1).
- Produces: `async def classificar_avaliacoes(avaliacoes: list[dict], groq: AIClient) -> list[dict]` — retorna a mesma lista com campo `urgencia` adicionado em cada item, **ordenada com `urgencia == "urgente"` primeiro**, preservando a ordem relativa original dentro de cada grupo.

- [ ] **Step 1: Escrever o teste**

```python
# apps/api/tests/test_triagem_avaliacoes.py
from unittest.mock import AsyncMock

import pytest

from app.services.triagem_avaliacoes import classificar_avaliacoes


def _avaliacao(name: str, comment: str, star: str = "FIVE", respondida: bool = False) -> dict:
    item = {
        "name": name,
        "reviewer": {"displayName": "Cliente"},
        "starRating": star,
        "comment": comment,
    }
    if respondida:
        item["reviewReply"] = {"comment": "Obrigada!"}
    return item


@pytest.mark.anyio
async def test_classifica_e_ordena_urgentes_primeiro():
    avaliacoes = [
        _avaliacao("r1", "Muito bom, recomendo", star="FIVE"),
        _avaliacao("r2", "Péssimo atendimento, nunca mais volto", star="ONE"),
        _avaliacao("r3", "Ok", star="THREE"),
    ]

    groq = AsyncMock()
    groq.generate_json.side_effect = [
        {"urgencia": "normal"},
        {"urgencia": "urgente"},
        {"urgencia": "normal"},
    ]

    resultado = await classificar_avaliacoes(avaliacoes, groq)

    assert resultado[0]["name"] == "r2"
    assert resultado[0]["urgencia"] == "urgente"
    assert [a["name"] for a in resultado[1:]] == ["r1", "r3"]


@pytest.mark.anyio
async def test_avaliacao_respondida_nao_chama_groq():
    avaliacoes = [_avaliacao("r1", "Ótimo", respondida=True)]
    groq = AsyncMock()

    resultado = await classificar_avaliacoes(avaliacoes, groq)

    assert resultado[0]["urgencia"] is None
    groq.generate_json.assert_not_called()


@pytest.mark.anyio
async def test_falha_do_groq_vira_urgencia_nula():
    avaliacoes = [_avaliacao("r1", "Comentário qualquer")]
    groq = AsyncMock()
    groq.generate_json.side_effect = Exception("erro de rede")

    resultado = await classificar_avaliacoes(avaliacoes, groq)

    assert resultado[0]["urgencia"] is None
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_triagem_avaliacoes.py -v`
Expected: FAIL (`ModuleNotFoundError`)

- [ ] **Step 3: Implementar**

```python
# apps/api/app/services/triagem_avaliacoes.py
"""Classifica avaliações do Google Meu Negócio sem resposta como urgente/normal.

Usa o Groq (rápido, gratuito) em vez do Gemini — é só classificação de uma
palavra, não geração de conteúdo. Falha na IA nunca derruba a listagem.
"""
import asyncio
import logging

from app.integrations.ai.base import AIClient

logger = logging.getLogger(__name__)

PROMPT = """\
Classifique esta avaliação de cliente de um escritório de advocacia como
"urgente" ou "normal".

Urgente: nota baixa (1-2 estrelas) OU comentário com reclamação explícita
sobre atendimento, erro ou injustiça — mesmo com nota mediana.
Normal: elogio, neutro, ou crítica leve sem reclamação grave.

Nota: {nota}
Comentário: {comentario}

Responda em JSON: {{"urgencia": "urgente"}} ou {{"urgencia": "normal"}}
"""


async def _classificar_uma(avaliacao: dict, groq: AIClient) -> str | None:
    if avaliacao.get("reviewReply") is not None:
        return None
    try:
        prompt = PROMPT.format(
            nota=avaliacao.get("starRating", ""),
            comentario=avaliacao.get("comment", "(sem comentário)"),
        )
        resultado = await groq.generate_json(prompt)
        urgencia = resultado.get("urgencia")
        return urgencia if urgencia in ("urgente", "normal") else None
    except Exception:
        logger.exception("Falha ao classificar avaliação %s via Groq", avaliacao.get("name"))
        return None


async def classificar_avaliacoes(avaliacoes: list[dict], groq: AIClient) -> list[dict]:
    urgencias = await asyncio.gather(*[_classificar_uma(a, groq) for a in avaliacoes])
    for avaliacao, urgencia in zip(avaliacoes, urgencias):
        avaliacao["urgencia"] = urgencia

    urgentes = [a for a in avaliacoes if a["urgencia"] == "urgente"]
    outras = [a for a in avaliacoes if a["urgencia"] != "urgente"]
    return urgentes + outras
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_triagem_avaliacoes.py -v`
Expected: PASS (3 testes)

- [ ] **Step 5: Commit**

```bash
git add apps/api/app/services/triagem_avaliacoes.py apps/api/tests/test_triagem_avaliacoes.py
git commit -m "feat: serviço de triagem de avaliações (urgente/normal) via Groq"
```

---

### Task 3: Integrar na rota `GET /avaliacoes`

**Files:**
- Modify: `apps/api/app/routers/avaliacoes.py`
- Test: `apps/api/tests/test_avaliacoes.py`

**Interfaces:**
- Consumes: `classificar_avaliacoes` (Task 2), `GroqClient` (Task 1).

- [ ] **Step 1: Escrever o teste (adicionar ao arquivo existente)**

```python
# apps/api/tests/test_avaliacoes.py — adicionar ao final
@pytest.mark.anyio
async def test_listar_avaliacoes_inclui_urgencia_e_ordena(client, db_session):
    tenant, user = await _setup(db_session)
    token = create_access_token(user.id)

    mock_google = AsyncMock()
    mock_google.renovar_access_token.return_value = "access_novo"
    mock_google.listar_avaliacoes.return_value = [
        {
            "name": "locations/456/reviews/1",
            "reviewer": {"displayName": "A"},
            "starRating": "FIVE",
            "comment": "Ótimo",
        },
        {
            "name": "locations/456/reviews/2",
            "reviewer": {"displayName": "B"},
            "starRating": "ONE",
            "comment": "Péssimo",
        },
    ]

    mock_groq = AsyncMock()
    mock_groq.generate_json.side_effect = [
        {"urgencia": "normal"},
        {"urgencia": "urgente"},
    ]

    with patch("app.routers.avaliacoes.get_google_client", return_value=mock_google), patch(
        "app.routers.avaliacoes.get_groq_client", return_value=mock_groq
    ):
        resp = await client.get("/avaliacoes", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    body = resp.json()
    assert body[0]["name"] == "locations/456/reviews/2"
    assert body[0]["urgencia"] == "urgente"
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `cd apps/api && py -m pytest tests/test_avaliacoes.py::test_listar_avaliacoes_inclui_urgencia_e_ordena -v`
Expected: FAIL (`AttributeError` — `get_groq_client` não existe)

- [ ] **Step 3: Implementar**

Em `apps/api/app/routers/avaliacoes.py`, adicionar imports:
```python
from app.integrations.ai.groq_client import GroqClient
from app.services.triagem_avaliacoes import classificar_avaliacoes
```

Adicionar função e modificar a rota:
```python
def get_groq_client() -> GroqClient:
    return GroqClient(api_key=settings.GROQ_API_KEY)


@router.get("")
async def listar_avaliacoes(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[dict]:
    conexao = await _conexao_ativa(db, current_user.tenant_id)
    client = get_google_client()
    access_token = await client.renovar_access_token(decrypt_token(conexao.access_token_encrypted))
    avaliacoes = await client.listar_avaliacoes(access_token, conexao.ig_user_id)
    return await classificar_avaliacoes(avaliacoes, get_groq_client())
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `py -m pytest tests/test_avaliacoes.py -v`
Expected: PASS (todos, incluindo o novo)

- [ ] **Step 5: Rodar a suíte completa**

Run: `py -m pytest tests -q`
Expected: todos passando

- [ ] **Step 6: Commit**

```bash
git add apps/api/app/routers/avaliacoes.py apps/api/tests/test_avaliacoes.py
git commit -m "feat: classificar urgência das avaliações na listagem (Groq)"
```

---

### Task 4: Frontend — badge de urgência

**Files:**
- Modify: `apps/web/app/(app)/avaliacoes/page.tsx`

**Interfaces:**
- Consumes: campo `urgencia: "urgente" | "normal" | null` já presente no retorno de `GET /avaliacoes`.

- [ ] **Step 1: Ler o estado atual do arquivo**

Run: `cat "apps/web/app/(app)/avaliacoes/page.tsx"` (confirmar estrutura exata antes de editar)

- [ ] **Step 2: Adicionar o campo ao tipo `Avaliacao`**

```tsx
type Avaliacao = {
  name: string;
  reviewer: { displayName: string };
  starRating: string;
  comment?: string;
  reviewReply?: { comment: string };
  urgencia: "urgente" | "normal" | null;
};
```

- [ ] **Step 3: Aplicar o estilo condicional no `Card` de cada avaliação**

Trocar a linha do `<Card key={a.name} className="p-5">` por:
```tsx
<Card
  key={a.name}
  className={a.urgencia === "urgente" ? "border-l-2 border-destructive p-5" : "p-5"}
>
```

E, no bloco com o nome do avaliador, adicionar a badge ao lado:
```tsx
<div className="flex items-center gap-2">
  <p className="text-sm font-medium">{a.reviewer.displayName}</p>
  {a.urgencia === "urgente" && (
    <span className="rounded-full bg-destructive/15 px-2 py-0.5 text-[10px] font-medium text-destructive">
      Urgente
    </span>
  )}
</div>
```
(substitui o `<p className="text-sm font-medium">{a.reviewer.displayName}</p>` isolado que já existe dentro do `<div className="flex items-center justify-between">`)

- [ ] **Step 4: Build de checagem**

Run: `cd apps/web && npm run build`
Expected: build verde

- [ ] **Step 5: Commit**

```bash
git add "apps/web/app/(app)/avaliacoes/page.tsx"
git commit -m "feat: badge de urgência nas avaliações (Groq)"
```

---

### Task 5: Deploy

- [ ] **Step 1: Rodar a suíte completa uma última vez**

Run: `cd apps/api && py -m pytest tests -q`
Expected: todos passando

- [ ] **Step 2: Configurar `GROQ_API_KEY` no Railway**

Passo manual da usuária: criar chave em [console.groq.com/keys](https://console.groq.com/keys), depois:
```bash
export RAILWAY_API_TOKEN="<token da sessão>"
cd /c/tmp/mktecosystem
railway variables --service orbit-api --set "GROQ_API_KEY=<valor>"
```

- [ ] **Step 3: Deploy do backend e frontend**

```bash
railway up ./apps/api --path-as-root --service orbit-api --detach
railway up ./apps/web --path-as-root --service orbit-web --detach
```
Aguardar `SUCCESS` em ambos (poll no GraphQL `deployment(id).status`, mesmo padrão dos deploys anteriores).

- [ ] **Step 4: Verificar**

Run: `curl -s -o /dev/null -w "%{http_code}" https://orbit-api-production-0029.up.railway.app/health`
Expected: `200`
