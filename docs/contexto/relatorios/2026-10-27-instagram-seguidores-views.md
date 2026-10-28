# Instagram: seguidores e visualizações (27/10/2026)

## Pedido
"Aqui vamos tratar do instagram" → "Preciso ganhar seguidores e viws" (com prints do método dos 10 passos de um post
do @denderson.ai) → "Faça o que for necessário".

## Feito
- Análise com os números reais do banco do Orbit (337 posts e o retrato da conta, só leitura na VPS):
  `docs/ANALISE_INSTAGRAM_2026-10-27.md` (diagnóstico, Reels acima do dobro da média, horário, o que muda,
  30 ideias de Reels com gancho A/B, rotina de sexta, limites dos dados). Resumo em `docs/CONTEXTO_PROJETO.md`,
  seção "Instagram: seguidores e visualizações".
- Commit `b71f738`: a coleta pede `ig_reels_avg_watch_time` para Reels e grava em `instagram_posts.tempo_medio_ms`
  (migração `b4d6f8a0c2e4`). Se a Meta recusar a métrica, a coleta volta às métricas de sempre.

## Verificado
- Testes: 2 novos (falharam antes, passaram depois); suíte da API com 362 testes passando.
- Agenda de 28/10 a 30/11 lida em produção: no máximo 1 post de feed por dia e Reels em terça e sexta, mais os de
  28, 29 e 30/10, que já estavam marcados.
- **Não verificado:** se a Meta aceita `ig_reels_avg_watch_time` na v21 para esta conta. A API nova **não foi
  publicada na VPS**, porque a permissão bloqueou o deploy nesta sessão.

## Decisões e porquês
- Não mudei a agenda, o horário das 21h nem a regra dos 2 Reels por semana. São regras dela (23/10/2026), e a
  amostra de horário é pequena. Ficou como proposta com teste.
- O formato que funcionou ("Fez a grávida chorar? Processamos") é para copiar no jeito (rosto, humor, cena real),
  não na frase: "Processamos" insinua resultado (manual, OAB).
- Dois ganchos foram corrigidos antes de salvar: a prisão por pensão é pelas 3 últimas parcelas, e o genitor pode,
  sim, pedir prestação de contas da pensão, por isso saiu o gancho "pensão não dá direito de controlar".

## Pendente
- Publicar a API na VPS (`git pull` + `docker compose up -d --build api`; a migração roda ao subir) e clicar em
  "Atualizar dados" na tela Crescimento. Quem decide: a Jessica, liberando o deploy.
- Ok da Dra./Jessica para as 6 propostas da seção 4 da análise.

## Próxima sessão
Depois do deploy e da coleta, ler `tempo_medio_ms` dos 85 Reels e acrescentar à análise quais ganchos seguram mais
(skill `contexto-orbit`; para roteiro, `leticia-reels-premium` e `voz-leticia`).
