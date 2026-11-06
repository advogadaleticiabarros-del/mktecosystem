# Relatório · efeitos sonoros v2 nos 4 Reels do 13º (06/11/2026)

## Pedido
Jessica: "vamos melhorar a estética desses reels? Dos 4" (2/3 e 3/3 13º sem susto, 13º proporcional, 13º as 4 regras).
Ela escolheu o estilo Papel e Ouro com a mesma narração, mas no meio do trabalho mudou: "só melhore o efeito sonoro".
O visual não mudou.

## Feito
- `producao/reels/series/13-reels-procedural/work/som2.py` (cópia do que rodou em `C:\tmp\videos-reels\13-reels-procedural\work`):
  efeitos novos sintetizados em numpy, sem direitos de terceiros. Whoosh com varredura de filtro e passagem esquerda→direita,
  impacto grave com cauda, clique de papel no lugar do "pop", carimbo abafado, sino suave (Mi6/Si6) no fechamento e
  cintilação em grãos no "pó". Todos mais baixos que antes. Mesmos momentos (`montar_cfg`); voz e trilha iguais; vídeo
  copiado do Reels publicado (sem re-render).
- Arquivos novos `/app/media/<nome>-som2.mp4`. As 4 peças (aprovadas) apontam para eles, e `corpo.video_antes_som2` guarda
  o endereço antigo. Os arquivos antigos continuam no servidor. Script `subir2/trocar_video_som2.py`.

## Verificado
- Loudness igual ao publicado (−14,0 a −14,6 LUFS, pico ≤ −0,1 dBFS), mesma duração; os 4 respondem 206 video/mp4.
- Não verificado: escuta humana. Ninguém ouviu ainda.

## Pendente
- A Jessica ouvir (cópias em `C:\tmp\videos-reels\13-reels-procedural\renders_som2\`). Para voltar: trocar `video` por
  `video_antes_som2` na peça.
- 1º deles vai ao ar em 10/11 21h.