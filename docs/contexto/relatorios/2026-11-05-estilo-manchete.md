# Estilo Manchete e 10 criativos fora da caixa

## Pedido

A Jessica aprovou as 3 peças da referência em café e ouro: "pronto, é isso que eu quero! De um nome para esse estilo, e crie mais 10 criativos sobre assuntos fora da caixa". Depois acrescentou: "inclua as bordas douradas superiores e inferiores, que já é uma das marcas".

## Feito

- Estilo registrado como **Manchete** em `docs/ESTILO_MANCHETE.md`, com ponteiros em `docs/PASSAGEM_DE_CONTEXTO.md` e `docs/CONTEXTO_PROJETO.md`.
- `producao/estilos/referencia-cores/` virou `producao/estilos/manchete/`. As peças sem faixas seguem em `pecas/` com os nomes antigos (`01-te-disseram`, `02-caderno`, `03-palavra`).
- Faixas douradas em todas as peças. As 3 aprovadas foram geradas de novo como `manchete-01` a `manchete-03`.
- 10 peças novas em `fora_da_caixa.py` (`manchete-04` a `manchete-13`): cabelo, amigo secreto, preço no caixa, estacionamento, revista íntima, exame preventivo, banheiro, story como prova, pensão dos avós e doação de sangue. Textos em `legendas.md`.
- Página privada: https://claude.ai/artifact/K6rDQEM3yyaXANby9q74PL

## Verificado

- As 13 peças renderizaram e foram conferidas na grade. As peças 07, 08 e 11 também em tamanho real.
- `montar_pagina.py`, script temporário da página, conferiu que as 13 legendas têm até 5 hashtags e nenhum travessão.
- Não verificado: citações legais em fonte oficial, celular real, tela da página publicada, licença das fotos do Pexels, avaliação da Dra.

## Decisões e porquês

- **Nome:** Manchete, porque o título grande com faixa é o traço comum das peças.
- **Letra:** a Playfair Display fica neste estilo. A aprovação foi sobre essa letra, sem as faixas, e as faixas foram o único acréscimo pedido.
- **Imagens:** só do banco local e da biblioteca `_recortes`, porque o acesso ao Pexels pela VPS foi negado. A foto do banheiro foi trocada porque mostrava um ursinho sem relação com o tema. O nome de um contato na tela do celular foi coberto.
- **Temas:** só com regra que dá para explicar em tese. Ficaram de fora perda gestacional, por ser delicado, e pejotização, que tinha discussão aberta no STF até onde este trabalho sabe.

## Pendente

- **Jessica:** aprovar as 10 peças. Nada foi agendado.
- **Dra.:** conferir as citações legais e os pontos de `docs/ESTILO_MANCHETE.md`, seção "Antes de publicar".
- **Jessica e Dra.:** a estrutura fica muito próxima à do perfil de um colega advogado.

## Próxima sessão

Ajustar conforme a resposta dela e, com aprovação, agendar pelo processo de `docs/PASSAGEM_DE_CONTEXTO.md`. Peça nova: função nova em `fora_da_caixa.py`, nome novo e texto em `legendas.md`. Skills: `voz-leticia`, `contexto-orbit`.
