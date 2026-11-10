# 10/11/2026 · Reels de terça e sexta trocados pelos Flagrante, e API com capa própria

## Pedido
"Quero tudo nos formatos novos" e "Pode aplicar" (Jessica), depois de ver a grade do feed até 01/01/2027.

## Feito
- Backup antes: `/root/orbit-backups/antes-reels-flagrante-20261110.sql.gz`.
- API atualizada na VPS (git pull até `bf6f48c`, rebuild do `api`): o publicador passa a mandar `cover_url` quando a peça tem `corpo.capa` (commit f3d6370).
  - O rebuild quebrou: o playwright novo precisa de `libatomic1`, ausente na imagem (exit 127). O Dockerfile agora instala essa biblioteca. Enquanto o build falhava, a API antiga ficou no ar. `/app/media` é um volume (`orbit_media`) e nada se perdeu.
- `apps/api/_saida_producao_1510/reels_flagrante.py` + `reels_flagrante.json`. Para cada dia, cria pauta e peça reels nova (vídeo, capa textura, legenda e primeiro comentário do `legenda.json` do episódio) e aponta o agendamento de 21h para ela. A peça antiga vai para `corpo.reserva`. Simulação, aplicação e segunda simulação ("já trocado" em todos).
- Trocas, mesma data às 21h:
  - 10/11 13º salário · 13/11 Gestante dispensada · 17/11 Gestante e pedido de demissão
  - 20/11 Cabelo no trabalho · 24/11 Doação de sangue · 27/11 Licença-maternidade
  - 01/12 Pensão atrasada · 08/12 Fim da 6x1 · 11/12 Revista íntima
  - 15/12 Amigo secreto · 18/12 Temporário · 22/12 Natal com pais separados · 29/12 Pensão paga pela avó
- Vídeos e capas em `/app/media/flagrante-<ep>-v2.mp4` e `flagrante-<ep>-capa-textura.jpg` (HTTP 200 conferido). `montar_midia` da peça de hoje devolve vídeo, capa e legenda certos (sem publicar).
- Mito ou Lei: os 27 agendados já são Reels no formato novo (trabalho da outra sessão de hoje). O único "mito" antigo era o Reels "pensão: mito dos 30%" (11/12), trocado aqui.
- Grade atualizada: https://claude.ai/artifact/ANhFGaQydP9XewYQoE59Kg (versão 3, lida do Orbit depois da troca).

## Não feito / pendente
- Carrosséis continuam no modelo atual: os modelos novos esperam a escolha da Dra. (decisão de 09/11).
- Os Reels Mito ou Lei não têm capa própria. Usam o quadro de 9 s, e na grade o título "Mito ou Lei?" aparece cortado.
- Não verificado: a publicação real com `cover_url`. A primeira vai ser hoje às 21h; conferir no Instagram se a capa textura entrou.
- Os 20 Flagrante restantes (01 a 14, 16, 20, 27, 28, 30, 31) e os 34 Manchete avulsos estão sem data.
