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
