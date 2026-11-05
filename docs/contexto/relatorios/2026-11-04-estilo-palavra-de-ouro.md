# Estilo Palavra de Ouro

## Pedido

"Salve esse como mais um estilo nosso! De um nome", sobre as peças com palavra em ouro e foto em preto e branco.

## Feito

- Nome escolhido: **Palavra de Ouro**.
- Regras em `docs/ESTILO_PALAVRA_DE_OURO.md`, com ponteiros em `docs/PASSAGEM_DE_CONTEXTO.md` e `docs/CONTEXTO_PROJETO.md`.
- Código em `producao/estilos/palavra-de-ouro/` (`base.py`, `gerar.py`), com 9 peças de referência em `pecas/` e 2 fotos em `fotos/`. Os JPG ficam só neste computador, porque o `.gitignore` os exclui.

## Verificado

- `gerar.py` rodou da pasta nova e gerou as 9 peças. Comparadas com as prévias: 6 idênticas (diferença média 0) e 3 do grito com 0,52 a 0,97, atribuídas à qualidade de JPG (90 na prévia, 89 aqui).
- Não verificado: citações legais em fonte oficial, licença da Pexels (site bloqueou a leitura), celular real, avaliação da Dra.
- `gerar.py` depende de `_fotos_pexels`, de `fotos/` e dos assets de `apps/api`. As fotos `.jpg` não vão para o git, então em outro computador o script não roda sem elas.

## Decisões e porquês

- "Esse" foi lido como a série de 6 peças mais as 3 do grito, que têm o mesmo tratamento.
- O estilo exclui foto da Dra., porque preto e branco contraria a regra de imagem original dela.
- O manual não foi alterado: o estilo convive com a regra do véu como pendência explícita.
- Só commit local, sem push, porque não foi pedido.

## Pendente

Jessica e Dra. decidem: revisão jurídica, licença das fotos, avaliação OAB e a diferença com o véu do manual.

## Próxima sessão

Para nova peça: ler `docs/ESTILO_PALAVRA_DE_OURO.md`, acrescentar em `P` de `gerar.py` com nome novo, sem sobrescrever peça pronta. Skills: `voz-leticia`, `contexto-orbit`.
