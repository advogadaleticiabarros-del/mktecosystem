# 10/11/2026 · Reels piloto "Mito ou Lei" no estilo Flagrante

- Pedido: Reels dinâmico da série Mito ou Lei, com motion e efeitos sonoros, na identidade nova (Flagrante / Papel e Ouro).
- Feito: `producao/estilos/papel-e-ouro/motion-diario/34_mito_feriado.py` (tema do plano de novembro: "Feriado trabalhado é hora extra de 50%" → MITO).
- Mecânica nova: título cai letra a letra, afirmação digitada, roleta MITO/LEI com tique-taque, carimbo com impacto e clarão, contador 50%→100%, calendário de folga, pergunta em marca-texto, fechamento fixo.
- 18 efeitos sonoros (Mixkit), sem música nem voz. Área segura ok. 26 s.
- Saída: `34-mito-feriado/34-mito-feriado-v2.mp4` + `legenda.json` (Lei 605/1949, art. 9º; Súmula 146 do TST).
- Pendente: aprovação da Jessica; não entrou na página de aprovação nem foi agendado ou commitado.

## Série inteira (10/11/2026, mesmo dia)
- Pedido: "trocar todos dessa serie para reels nesse mesmo estilo"; dias: segunda, quarta e sábado às 19h (sem os outros Reels).
- Gerador: `producao/estilos/papel-e-ouro/motion-diario/mito_lei.py` (TELA por tema; saída em `mito-lei/<MM-DD>-<slug>/`). 25 vídeos + o piloto = 26, área segura ok.
- Grade e página: `gerar_pagina_mito.py` → `mito-lei/aprovacao.html`, publicada em https://claude.ai/artifact/TwkcA9cXu5wJvhGNKwSKV2.
- Ajustes: tema de 18/12 virou "tem que cair até sexta, 18/12" (vai em 16/12); comentário do racismo sem a data de 20/11; 3 temas + gestante foram para 02, 04, 07 e 09/01/2027.
- Orbit: `apps/api/_saida_producao_1510/mito_reels.py` + `mito_reels.json` (peça reels nova por tema, estático vai para a reserva). **NÃO APLICADO**: espera a aprovação da página. Antes: backup do banco, rodar sem `--aplicar`, subir os mp4 para /app/media com o nome `mito-lei-*.mp4`.

## Carimbo novo (v3, 10/11/2026)
- Pedido: carimbo mais rápido e chamativo, MITO vermelho vivo e LEI dourado brilhante, batida mais forte e tremor.
- Feito em `mito_lei.py`: queda em 0,09 s, clarão na cor do veredito, onda e respingos de tinta, tremor forte, botão MITO vermelho, som carimbo duplo + impacto grave. Saída `-v3.mp4` (v2 guardado).
- Exemplo: `mito-lei/11-16-gestante-insalubre/11-16-gestante-insalubre-v3.mp4`. Os demais só depois da aprovação.
- Som do carimbo trocado por batida seca sintetizada (`batida()` no motor.py: grave com queda de afinação + estalo), a pedido da Jessica.
- Antes da batida: som de vento sintetizado (`vento()` no motor.py, 0,7 s subindo) e o carimbo agora desce durante esse som (7,55 s até bater em 7,89 s).
- Meia roleta no rodapé (canvas, 8 fatias MITO/LEI, gira 3 voltas e para no veredito, fatia acende) com clique de lingueta sintetizado (`clique()` no motor.py) a cada fatia; substitui o tique-taque.
- Roleta movida para o rodapé e aumentada (raio 410 px, base em y 1570, acima da faixa da legenda do Instagram). Fica fora do recorte 3:4 da grade de propósito; o aviso de área segura dela é esperado.
- Roleta reposicionada: centro na borda de cima da faixa dourada inferior (y 1901), raio 520; o corte fica rente ao dourado, metade de baixo fora da tela.
- Gancho (pesquisa sobre retenção nos 3 primeiros segundos): afirmação na tela desde 0,1 s e digitada em 0,85 s, título junto, desafio "⏱ Responda antes da roleta parar" em 1,25 s, roleta de 2,4 a 7,6 s (5 voltas, 40 cliques).
- CTA final: cartão de perfil "Dra. Letícia Barros · @adv.leticiabarros2" com botão Seguir, mão tocando e virando "Seguindo ✓" (22,5 a 24,2 s), som de toque e brilho.

## Aplicado no Orbit (10/11/2026)
- Aprovação da Jessica: "pode replicar nos demais e redistribuir as publicações"; depois "finalizar tudo".
- Incluídos: 13º parcela única (era estático 18/11 14h) vai para Reels 25/11 19h; BPC vai para 11/01. 25/12 fica livre para a mensagem de Natal.
- Backup: `/root/orbit-backups/antes-mito-reels-20261110.sql.gz`. 27 vídeos v3 em /app/media (`mito-lei-*-v3.mp4`, link público 200 conferido). `mito_reels.py --aplicar`: 27 peças reels novas agendadas 19h (11/11 a 11/01), 12 estáticos saíram da agenda e todos os 27 estáticos ficaram na reserva.
- Agenda conferida depois (`ver_calendario.py`): 27 Reels Mito ou Lei, 16 Reels, 26 carrosséis, 6 posts, 15 artigos; nenhum dia com mais de 2 no feed.
- Páginas: aprovação https://claude.ai/artifact/TwkcA9cXu5wJvhGNKwSKV2 · calendário do feed https://claude.ai/artifact/MFQHA4vTwbS28VMho92LpZ
- Atenção: 02/01 tem um Reels de acervo pausado às 21h; se for reativado, o dia terá 2 Reels.
