# Groq — Triagem de Avaliações do Google Meu Negócio

**Objetivo:** classificar automaticamente cada avaliação ainda sem resposta como `urgente` ou `normal`, usando o Groq (grátis, ~320 tokens/seg), para a advogada abrir a tela de Avaliações e já ver o que precisa de atenção primeiro — sem precisar ler todas.

## Por que o Groq aqui
- Tarefa é classificação simples (1 palavra de saída), não geração de conteúdo — não precisa da profundidade do Gemini.
- Groq já é usado com sucesso no CRM da mesma usuária para triagem — padrão validado, mesma conta.
- Free tier (30 req/min, ~1.000/dia) folgado para o volume de avaliações de um único escritório.
- API compatível com o formato OpenAI (`chat/completions`), simples de implementar via `httpx`, seguindo o mesmo protocolo `AIClient` (`generate_json`/`generate_text`) já usado pelo `GeminiClient` — nenhuma mudança no restante do código que usa IA.

## Componentes

### 1. `GroqClient` (novo, mesmo protocolo `AIClient`)
`app/integrations/ai/groq_client.py`: implementa `generate_json`/`generate_text` via `POST https://api.groq.com/openai/v1/chat/completions`, modelo `llama-3.3-70b-versatile`. Nova env var `GROQ_API_KEY`.

### 2. Classificação (serviço novo)
`app/services/triagem_avaliacoes.py`: `classificar_avaliacoes(avaliacoes: list[dict], groq: AIClient) -> list[dict]` — para cada avaliação sem `reviewReply`, monta um prompt curto com nota + comentário, pede ao Groq responder `{"urgencia": "urgente"|"normal"}` (uma classificação por vez, chamadas em paralelo via `asyncio.gather` — volume baixo, sem necessidade de lote). Adiciona o campo `urgencia` ao dict da avaliação. Avaliações já respondidas recebem `urgencia: null` sem chamar a IA.

**Critério de "urgente":** nota 1-2 estrelas OU comentário com tom de insatisfação explícita (reclamação de atendimento, erro, injustiça) — critério dado ao modelo via prompt, não hardcoded em regras de nota isoladas (evita falso-negativo de nota 3 com reclamação grave).

### 3. Integração na rota existente
`GET /avaliacoes` (já existe): depois de buscar as avaliações do Google, passa pela classificação e ordena com `urgente` primeiro, mantendo a ordem original do Google dentro de cada grupo.

**Falha do Groq:** se a chamada falhar (rede, rate limit), a avaliação recebe `urgencia: null` (mesmo tratamento de "sem classificação") — nunca quebra a listagem por causa da triagem.

### 4. Frontend
Página `/avaliacoes`: avaliação com `urgencia: "urgente"` ganha borda esquerda vermelha (`border-l-2 border-destructive`) e uma badge pequena "Urgente" ao lado do nome. Sem alarme sonoro/popup — só o sinal visual na lista já ordenada.

## Fora de escopo
Fallback automático do Gemini para o Groq (infra futura, não pedida agora), variantes de legenda via Groq (outro caso de uso, fica pra depois), notificação por e-mail/push de avaliação urgente.

## Testes
- Unit: `GroqClient` (mock httpx, mesmo padrão do `MetaClient`/`GoogleBusinessClient`).
- Unit: `classificar_avaliacoes` — avaliação respondida não chama a IA; falha da IA não quebra, retorna `urgencia: null`; ordenação urgente-primeiro.
