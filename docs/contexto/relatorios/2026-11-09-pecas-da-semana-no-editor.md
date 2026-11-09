# Peças da semana no editor de artes

## Pedido

"Coloque tudo que fizemos e produzimos na semana passada lá no editor."

## Feito

- `producao/editor/importar_estilos.py` roda o `gerar.py` de cada estilo e intercepta a foto da peça. Os textos viram camadas editáveis, com fonte, tamanho, cor, itálico, negrito, ouro com brilho e rotação de 90°. O resto (fotos, faixas, selos, grão) vira a camada "Fundo (foto e acabamento)". Nada em `producao/estilos` é gravado.
- 35 peças novas no editor: Palavra de Ouro (9), Verbete (1), Papel e Ouro (9), Objeto em Cena (3), Manchete (13). Com `grito-D-editorial` e `grito-D-luz`, são 37.
- Editor: fonte Playfair Display (usada no Manchete), pesos 300 a 900 das três fontes, `<b>` e `<sup>` nos textos. O texto colado deixou de trazer o conteúdo de `<script>` e `<style>`.

## Verificado

- 48 testes passaram (`python -m pytest producao/editor/tests -p no:cacheprovider`).
- Todas as peças renderizadas pelo editor foram comparadas com o JPG pronto: diferença média de 0,8 a 6,1 em 255. Grávida, Verbete, Trabalho e Doar sangue também foram conferidas por imagem.
- `git status producao/estilos` limpo depois da importação.
- Não verificado: o uso pela Jessica.

## Decisões e porquês

- Fundo único em vez de reconstruir fotos e faixas: é fiel e vale para todo estilo. A contrapartida é que foto e faixa não se movem separadas; para trocar a foto, usa-se "+ Foto" por cima.
- Ficam no fundo, sem edição: texto atrás de outra camada (letras "TRABALHO" atrás do retrato), texto inclinado em ângulo que não é múltiplo de 90° (caderno e revista do Manchete, por isso 0 textos) e texto de SVG (selo circular). Os realces (marca-texto, risco) também ficam no fundo: se o texto se mover, o realce não vai junto.
- `grito-D-editorial` não foi reimportada, para não apagar os ajustes da Jessica.
- Fora do editor: Reels e vídeos (o editor é de imagem estática), os 3 JPG antigos soltos em `manchete/pecas` sem gerador e os comparativos.

## Pendente

- Jessica: dizer se quer edição também das peças inclinadas.

## Próxima sessão

Peça nova de estilo: rodar `python importar_estilos.py <estilo>`. A peça que já existe no editor é pulada. Skills: `codebase-design`, `tdd`.

## Revisão dos textos (mesmo dia)

Pedido: "revise todos os textos e concordâncias, deve ser simples o entendimento, bater o olho e ler rápido".

- `producao/editor/revisar_textos_2026_11_09.py`: 14 peças com texto mais curto, concordância e precisão legal. Exemplos: exame "ATÉ 3 DIAS" (CLT 473, XII diz "até"), grávida "Gravidez não é justa causa para demitir", errata "Demitido sem justa causa recebe o 13º proporcional", assinatura repetida retirada do cabeçalho em 3 peças. Cada peça guarda `original.json`; os JPG prontos não mudaram. `grito-D-editorial` (da Jessica) não foi tocada.
- Defeito da importação corrigido: trecho de outra cor sobre marca-texto dourado vinha claro e ilegível. Agora vira `<mark>` com `cor_marca` (4 peças: avó, te disseram, relógio, 23:47).
- Os textos que ficaram no fundo (clara-01 com a tarja do art. 391, clara-08 com "prometer" riscado) não podem ser revisados no editor.
- Achado: `manchete/gerar.py` já tem 34 peças (14 a 34 feitas depois); elas não estão no editor.
- Carrosséis v5 (Ouro editorial, foto escura em tela cheia) ficam escuros ao lado das peças claras: simulação de grade feita, decisão de direção com a Jessica.
