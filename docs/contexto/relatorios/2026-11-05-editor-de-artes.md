# Editor de artes manual

## Pedido

"Eu quero poder mexer nos designs, manualmente, quero que você faça, mas quero poder alterar", com solução gratuita. Entre editor próprio, Canva, Figma e Penpot, a Jessica escolheu o editor próprio ("vamos na primeira opção").

## Feito

- Editor em `producao/editor/`, aberto por `Abrir editor.bat` ou pelo atalho `Editor de artes` na Área de Trabalho deste computador.
- `acervo.py` guarda as peças e as regras da marca; `servidor.py` escuta só em 127.0.0.1:8765; `web/peca.js` é o único desenho, usado pela tela e pela exportação; `web/editor.js` cuida da interação.
- Primeira peça: `grito-D-editorial`, criada por `importar_grito_d.py`. A peça do estilo Palavra de Ouro não foi alterada.
- Fontes EB Garamond e Inter copiadas para `web/`, com licença em `licencas-fontes/`, para exportar igual sem internet.
- Dá para: escrever, destacar trecho, arrastar (com encosto e guias), redimensionar, mudar fonte, peso, cor e fundo, trocar ou somar foto, ajustar brilho e contraste, mudar camadas, duplicar, excluir, desfazer, criar nova versão, voltar ao original e baixar JPG 1080×1440.

## Verificado

- 34 testes passaram (`python -m pytest producao/editor/tests -p no:cacheprovider`), 8 deles no editor em navegador real.
- Exportação comparada com `grito-D-editorial.jpg` do estilo: diferença média abaixo de 1 em 255, máximo 29, compatível com a compressão do JPG.
- Uso completo numa cópia temporária, conferido por imagem: arrastar, redimensionar, reescrever, destacar e baixar, sem erro no navegador.
- `Abrir editor.bat` subiu o servidor e respondeu em 127.0.0.1:8765.
- Não verificado: o clique real no atalho com abertura do navegador (o teste usou navegador desativado), o uso pela Jessica e a exportação de foto enviada de celular em formato HEIC (o envio de PNG foi testado).
- `graphify update .` não rodou: o comando não está instalado neste computador.

## Decisões e porquês

- Editor próprio em vez de Canva ou Figma: mantém ouro com brilho e máscaras, e o Claude lê o que ela alterou em `peca.json`.
- A exportação usa Playwright na mesma página da peça, para sair igual à tela. Bibliotecas de captura no navegador não garantem máscara e mistura.
- Nada de material pronto é sobrescrito: cada exportação vira arquivo novo em `saidas/`, e `original.json` não muda.
- Só EB Garamond e Inter e nada abaixo de 22 px: regras da marca e do manual, barradas no servidor. Fundo e cor são livres, então texto dourado em fundo claro não é barrado, embora o manual proíba.
- Texto vazio não é aceito; para tirar um texto, usa-se Excluir.

## Pendente

- Jessica: testar no uso real e dizer o que falta.
- Jessica: decidir o envio ao GitHub (commit só local). O editor depende de fotos que o git ignora, então em outro computador `foto.jpg` não existirá.
- Levar as outras peças para o editor quando a Jessica aprovar; cada estilo precisa de um importador.
- A crítica da arte continua aberta: faixa fina e foto de cena de trabalho. Ver `2026-11-05-grito-critica-direcao-de-arte.md`.

## Próxima sessão

Ler `pecas/<nome>/peca.json` para ver o que ela alterou. Para nova peça, seguir `importar_grito_d.py` com um documento próprio, ou usar "Nova versão" no editor. Skills: `codebase-design`, `tdd`, `contexto-orbit`.
