# Estilo Papel e Ouro

## Pedido

A Jessica enviou a grade de 9 peças: "Gostei de todos esses pode registrar também".

## Feito

- Nome: **Papel e Ouro**, escolhido para não confundir com o padrão "Ouro editorial" já existente.
- Regras e a ordem da grade em `docs/ESTILO_PAPEL_E_OURO.md`, com ponteiros em `docs/PASSAGEM_DE_CONTEXTO.md` e `docs/CONTEXTO_PROJETO.md`.
- Código levado do scratchpad para `producao/estilos/papel-e-ouro/` (`gerar.py`, `linha_clara.py`, `linha_objetos.py`). Peças e grade em JPG ficam só neste computador.

## Verificado

- `gerar.py` rodou da pasta nova: as 9 peças ficaram idênticas às aprovadas (diferença 0 em cada pixel).
- Não verificado: citações legais em fonte oficial, celular real, avaliação da Dra.

## Decisões e porquês

- Só as 9 peças da imagem entram como aprovadas. `linha_clara.py` e `linha_objetos.py` guardam as outras composições, mas `gerar.py` só gera as 9.
- O manual não foi alterado: as diferenças com a regra de slides claros e com o véu ficam como pendência explícita.
- Só commit local, sem push, porque não foi pedido.

## Pendente

Jessica e Dra. decidem: regra de slides claros, véu, revisão jurídica, frase do nome e push dos commits.

## Próxima sessão

Para nova peça: ler `docs/ESTILO_PAPEL_E_OURO.md`, criar a composição com nome novo e acrescentá-la à lista em `gerar.py`. Skills: `voz-leticia`, `contexto-orbit`.
