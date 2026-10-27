# Estilo "tela dividida" (26/10/2026)

Segundo estilo de Reels, ao lado do padrão premium de `../motor/` (que continua intacto: pedido da Jessica, "gosto muito dele").
**Antes de editar qualquer Reel, pergunte qual estilo: inteiro com banco de imagens (`motor/`) e/ou tela dividida (este).**
Os dois vão ser testados lado a lado para ver qual traz mais resultado.

Referência visual: Reels de explicação (diagrama animado no alto, pessoa embaixo, símbolo que volta e se completa, pergunta em
balão de comentário), vestidos com a identidade do escritório (café e dourado, EB Garamond itálico dourado, pílulas, rodapé).

Uso: copie `../motor/` para `NN-nome/work/` e depois copie por cima os arquivos desta pasta.
- `engine.html`: o do motor + cena com `"painel": <altura>` (painel café no alto; legenda na linha da divisão; cabeçalho e
  barra no pé do painel). Cena sem `painel` fica igual ao padrão.
- `fx.js`: o do motor, com o verificador da legenda ajustado (na tela dividida ela fica abaixo do cabeçalho).
- `diagramas.py`: peças prontas para o painel (título, relógio recorrente, calendário, recibo, dezembro, comparação, balão,
  meses, balança papel × prática). Cada uma devolve a lista de elementos com os tempos presos às palavras da fala.
O rosto vai para a metade de baixo pelo `kb` do fundo (deslocamento vertical positivo).
