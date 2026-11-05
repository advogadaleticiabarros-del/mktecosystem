# Teste do estilo Objeto em Cena

## Pedido

A Jessica enviou prints de um perfil de advocacia em azul, com objetos em cena: "mais uma alternativa, aplique nosso designe system e nossos assuntos e faça 3 posts para o feed para que eu possa ver".

## Feito

- 3 peças de teste em 1080×1440: gestante (`01-te-disseram`), assédio moral (`02-caderno`) e hora extra (`03-relogio`).
- Código em `producao/estilos/objeto-em-cena/`: `gerar.py`, `retocar.py` e `legendas.md` (legenda, primeiro comentário e texto alternativo). Usa `base.py` de `producao/estilos/palavra-de-ouro/`.
- Peças e fotos retocadas ficam só neste computador, porque o git ignora JPG e PNG em `producao/`. `retocar.py` e `gerar.py` as recriam.
- Página privada para ver no celular: https://claude.ai/artifact/VdPWeYFcMPUeTkf3cBFoyS
- Nome "Objeto em Cena" é provisório. Não há `docs/ESTILO_*.md`, porque o estilo ainda não foi aprovado.

## Verificado

- As 3 peças renderizaram e foram conferidas em imagem: acentos, quebras de linha e retoques. As peças 01 e 03 também em tamanho real.
- Não verificado: citações legais em fonte oficial, celular real, tela da página publicada, avaliação da Dra.

## Decisões e porquês

- **Fora de propósito:** palavra repetida ao fundo e círculo atrás da pessoa, porque a linha Brilho foi reprovada em 04/11 ("não é a direção").
- **Sem letra atrás do objeto:** exigiria recorte, proibido pela regra atual. A fita passa só pela frente.
- **Fotos:** só do banco local. A busca nova no Pexels dependia de leitura na VPS de produção, e a permissão foi negada. Não foi contornada.
- **Retoques (`retocar.py`):** tirada a marca SHARP e "QUARTZ" do relógio (Pexels 31103955) e a marca e os dados do ultrassom (Pexels 32592295). Uma borda da foto do ultrassom ficou levemente irregular, o que só aparece com zoom.
- **Caderno e caneta:** desenhados em código, como o teste de gravidez de "Deu positivo", por falta de foto adequada no banco.

## Pendente

- **Jessica:** aprovar, ajustar ou descartar o estilo.
- **Jessica:** decidir se a foto da gestante fica, porque a modelo é branca e a regra pede mais pessoas negras. Trocar por foto nova do Pexels exige liberar o acesso à VPS.
- **Dra.:** conferir ADCT, art. 10, II, b; Súmula 244, I, do TST; Constituição, art. 7º, XVI; CLT, art. 59. Avaliar também o tom de "Humilhada no trabalho?".
- **Manual:** a peça do caderno usa fundo claro, que conta para o limite de 1 slide claro a cada 4, pendência já aberta em `docs/ESTILO_PAPEL_E_OURO.md`.

## Próxima sessão

Se aprovado: criar `docs/ESTILO_OBJETO_EM_CENA.md` com o nome definitivo, apontar em `docs/PASSAGEM_DE_CONTEXTO.md` e `docs/CONTEXTO_PROJETO.md` e gerar peça nova com nome novo em `gerar.py`. Não agendar sem aprovação. Skills: `voz-leticia`, `contexto-orbit`.
