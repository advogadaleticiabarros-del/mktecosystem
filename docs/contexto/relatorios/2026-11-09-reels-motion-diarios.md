# 09/11/2026 · Reels motion diários, lote 1 (7 dias)

## Pedido
"Quero mais Reels nesse sentido do 23:47 em motion... pelo menos 1 motion original desse por dia, com variados
assuntos e com a mesma criatividade, ótimos efeitos sonoros."

## Feito
- Motor `producao/estilos/papel-e-ouro/motion-diario/motor.py`, no molde do 23:47 (Papel e Ouro, sem narração).
  Efeitos reais da Mixkit (licença livre, uso comercial): mensagem, digitação, relógio, página, escrita, moedas, erro,
  whoosh, impacto, carimbo, brilho, sino. Vibração sintetizada igual à do 23:47. Volume normalizado a -14 LUFS.
- 7 episódios, cada um com mecânica visual própria e legenda (`<pasta>/legenda.json`, 5 hashtags, rótulo de IA desligado):
  1. Atestado recusado (conversa com "digitando...") · Lei 605/1949
  2. Holerite sem hora extra (contador de 46h e recibo) · CF art. 7º, XVI
  3. Ponto britânico (folha carimbada e horário real escrito em ouro) · Súmula 338, III TST
  4. "Pede demissão" (direitos riscados um a um) · CLT art. 484-A
  5. Vender as férias (calendário de 30 dias, volta a 10) · CLT art. 143
  6. Almoço de 20 min (cronômetro e barra do que faltou) · CLT art. 71
  7. Experiência além de 90 dias (contador de dias) · CLT arts. 445 e 451
- Uso: `python NN_assunto.py amostras` (prévia) e `python NN_assunto.py video`.

## Verificado
- Área segura ok em todas as amostras. Volumes e durações conferidos no render.

## Pendente
- Aprovação da Jessica/Dra. dos textos (situações fictícias; comentários respondidos só em tese).
- Decidir onde entra "1 por dia": Instagram está limitado a terça e sexta 21h; TikTok tem 5 por semana.
- Não agendado nem publicado.

## Atualização (09/11/2026, à tarde) · lote 2 e fechamento novo
Pedido: "pode fazer mais, vamos soltar pelo menos 2 por semana desses, e coloque leia a legenda... e coloque também,
quer ficar por dentro dos seus direitos, clique em seguir e compartilhe com quem precisa saber disso."
- Fechamento novo no motor (versão v2, 22 s): "Leia a legenda" em marca-texto, depois "Quer ficar por dentro dos seus
  direitos?" e "Clique em seguir e compartilhe com quem precisa saber disso.", com som. A mesma frase entra na legenda
  antes da ressalva final. Os 7 do lote 1 foram renderizados de novo como `<nome>-v2.mp4`; os originais ficaram guardados.
- Lote 2 (6 novos): 08 salário por fora, 09 sem carteira na experiência, 10 salário atrasado, 11 FGTS não depositado,
  12 sem folga, 13 aviso prévio no horário normal.
- Página de aprovação para a Dra. (gerada por `gerar_pagina.py`): https://claude.ai/artifact/3wR9ZJ3KxvrNhCkSv9BAVo
- Volume entre -14,6 e -16,7 LUFS (só efeitos, sem voz). Área segura ok em todos.
- Ritmo: pelo menos 2 por semana. Ainda não agendado: falta a aprovação da Dra. e conferir as vagas de terça e sexta
  21h, que já têm Reels do 13º e de gestante até 11/12.

## Aprovação e nome (09/11/2026)
"Todos aprovados": os 13. O estilo passou a se chamar **Flagrante**, documentado em `docs/ESTILO_FLAGRANTE.md`.
