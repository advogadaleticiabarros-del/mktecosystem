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
