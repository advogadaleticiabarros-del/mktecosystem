# 10/11/2026 · Capa dos Reels Mito ou Lei (proposta, nada aplicado)

## Pedido
"Vamos fazer uma capa para o Reels mito ou lei. Siga nossa nova identidade. Acho que pode ser um pouco mais clara para não escurecer tanto o nosso feed." No meio do trabalho chegou uma referência (foto emoldurada em papel, com a pessoa saindo do quadro): "poderíamos fazer as capas com fotos que seguem o tema".

## Feito
- `producao/estilos/papel-e-ouro/motion-diario/capas_mito.py`: primeira versão, só tipografia, em papel claro e na variação com faixa café (`capa-papel.jpg`, `capa-faixa.jpg`, só 11-20 e 12-18).
- `capas_mito_foto.py`: a versão com foto, nas 27 capas (`mito-lei/<MM-DD>-<slug>/capa-foto.jpg`).
  - Papel claro com fibra, faixas e fio em dourado metálico, "Mito ou Lei?" com Lei em ouro mais profundo, afirmação do vídeo em itálico e MITO ou LEI sem o veredito.
  - A foto é a do tema (banco Pexels das perguntas). O recorte (rembg com `isnet-general-use`; o modelo padrão estoura a memória) acha o topo da pessoa ou do objeto e o põe 120 px acima da borda de cima da moldura. Quando o topo já está cortado na foto ou é só um fiapo, a capa sai sem o efeito (5 de 27).
  - Rascunhos guardados como `capa-foto-rascunho1.jpg` e `-rascunho2.jpg`.
- Página: https://claude.ai/artifact/6nWwSfXf1ZBYEi8KfMGq1e. Mostra a grade do feed até 31/12 com as capas novas e as 27 capas.

## Pendente
- Fotos que não combinam com a afirmação: 12/11, 14/11, 16/11, 28/11, 06/12, 08/12, 22/12 e 28/12. Fotos repetidas: 30/11 (igual a 08/11) e 18/12 (igual a 14/12).
- Aprovação da Jessica.
- Para aplicar: subir as capas para `/app/media` e pôr `corpo.capa` nas 27 peças reels `estilo=flagrante-mito-ou-lei`. A API já manda `cover_url`.
