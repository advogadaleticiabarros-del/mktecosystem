# Reels no máximo às 19h (10/11/2026)

## Pedido
Jessica: "mude todos os reels para no maximo as 19h00, as 21h00 nao estou conseguindo ter visualizações nem curtidas".

## O que mudou
- `apps/api/app/services/agenda.py`: `HORARIO_REELS = "19:00"` e `limitar_horario_reels()`; Reels com hora combinada
  (`corpo.programacao`) depois das 19h também cai para 19:00. Testes em `tests/test_agenda_um_por_dia.py` (commit `6551f57`).
- Banco do Orbit (produção): 16 Reels agendados às 21:00 (10/11 a 08/01/2027, inclusive o "Acervo" pausado de 02/01)
  passaram para 19:00, com `corpo.programacao.hora` junto. Os Mito ou Lei já estavam às 19h. Nenhum Reels futuro
  ficou depois das 19h. Backup antes: `/root/orbit-backups/antes-reels-19h.sql.gz`. Script:
  `C:\Users\prosy\AppData\Local\Temp\claude\...\scratchpad\reels_19h.py` (lista; `--aplicar` muda).
- Regras atualizadas: `CLAUDE.md`, `docs/MANUAL_CONTEUDO_REDES.md`, `docs/ESTRATEGIA_CRESCIMENTO_ORGANICO.md`,
  `docs/ESTRATEGIA_TIKTOK.md`, `docs/CONTEXTO_PROJETO.md`, skill `leticia-reels-motion`, memória `reels-2-por-semana`.

## Pendências
- Deploy da API feito pela Jessica (19h52, 10/11). Conferido na produção: Reels novo sai às 19:00, hora combinada de
  21:00 vira 19:00, 18:00 fica 18:00; nenhum Reels agendado depois das 19h; API respondendo 200, sem erros no log.
- O Reels de hoje (10/11, "Flagrante: 13º salário") foi trocado às 19h08, já depois das 19h: o publicador o pega na
  rodada seguinte (a cada 5 min). Conferido: ficou "publicado" às 19h10.
- O teste `test_reels_com_data_combinada_fora_de_terca_ou_sexta_vai_para_a_proxima` falha por usar data fixa no passado
  (30/10/2026); já falhava antes desta mudança.
- TikTok tem grade própria (`GRADE_TIKTOK`) e não foi mexido.
