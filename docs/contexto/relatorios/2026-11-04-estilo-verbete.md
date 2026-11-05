# Estilo Verbete

## Pedido

A Jessica enviou a peça do dicionário com "Agora esse, gostei também", logo depois de pedir para salvar o estilo Palavra de Ouro com um nome.

## Feito

- Lido como o mesmo pedido: guardar como estilo. Nome: **Verbete**.
- Regras em `docs/ESTILO_VERBETE.md`, com ponteiros em `docs/PASSAGEM_DE_CONTEXTO.md` e `docs/CONTEXTO_PROJETO.md`.
- Código em `producao/estilos/verbete/gerar.py`, com a função `verbete(...)` para novos termos. A peça fica em `pecas/`, só neste computador.

## Verificado

- `gerar.py` rodou e gerou a peça. Conferi em tamanho real: disposição, textos e foto iguais à peça aprovada. Na comparação de pixels com a prévia, a diferença média foi 1,13 (maior 44); a causa exata não foi investigada.
- Não verificado: celular real, OAB-ES, revisão da Dra.

## Decisões e porquês

- Reaproveita `base.py` da Palavra de Ouro, para o dourado e a textura ficarem iguais nos dois estilos.
- Nenhuma peça nova foi criada, porque o pedido foi sobre esta. Os termos do documento são só sugestão.
- Só commit local, sem push, porque não foi pedido.

## Pendente

Jessica e Dra. decidem: frase do nome, retrato real, consulta à OAB-ES e push dos commits.

## Próxima sessão

Para nova peça: acrescentar em `P` de `gerar.py`, com nome novo. Skills: `voz-leticia`, `contexto-orbit`.
