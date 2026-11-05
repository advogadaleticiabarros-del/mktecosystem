# Estilo Palavra de Ouro

Estilo visual aprovado pela Jessica em 04/11/2026 ("Salve esse como mais um estilo nosso"). É mais um estilo da marca e não substitui os outros. Nenhuma peça foi publicada ainda, e a Dra. Letícia ainda não avaliou o estilo.

**A ideia:** uma única palavra em ouro diz o tema, uma foto em preto e branco dá a emoção, e uma frase curta muda o sentido da palavra. Exemplo: "GRITAR não é cobrar."

- Código: `producao/estilos/palavra-de-ouro/` (`python gerar.py [prefixo]`). As composições ficam em `gerar.py` e o visual em `base.py`.
- Peças de referência: `producao/estilos/palavra-de-ouro/pecas/`. Ficam só no computador da Jessica, porque o git ignora JPG em `producao/`. O `gerar.py` as recria.

## Regras visuais

| Item | Valor |
| --- | --- |
| Formato | 1080×1440 |
| Fundo | Café `#231E1A`, fosco, com grão muito leve atrás do conteúdo |
| Palavra | EB Garamond 500, caixa alta, até 226 px (reduz para caber em 892 px de largura), em ouro com brilho |
| Frase | EB Garamond 500, com a palavra-chave em itálico 400, na cor areia |
| Apoio | Inter 400 ou 500, nada abaixo de 22 px, com a lei citada quando houver |
| Margens | 96 px nas laterais |
| Foto | Sem véu, preto e branco, com leve tom quente: `grayscale(1) sepia(.14) contrast(1.06)` |
| Ouro | O gradiente `FOIL` de `base.py`, na palavra, nos fios e nas faixas de topo e rodapé |
| Assinatura | Letícia Barros · OAB/ES 39.948 em toda peça |

## Três composições

1. **Faixa de cinema** (`faixa`, peças `01-hora-extra`, `03-assinar`, `grito-C-boca`): palavra no topo, foto em faixa larga entre fios de ouro, frase embaixo. É a mais sóbria.
2. **Foto grande** (`rosto`, peças `02-salario`, `05-antes`, `06-burnout`, `grito-B-close`): foto no alto dissolvendo no fundo, palavra na base.
3. **Palavra vertical** (peças `04-gravida`, `grito-A-perfil`): palavra girada à esquerda, texto em cima e foto embaixo, à direita, sem texto sobre a foto.

## O que escolher para a foto

- Prefira objeto, mãos, silhueta ou detalhe: a imagem precisa contar a história antes da leitura.
- Sem marca de terceiros, como logotipo em relógio ou notebook.
- Confira o enquadramento: a primeira versão de `02-salario` deixava a carteira numa posição constrangedora.
- **Foto da Dra. não entra neste estilo:** o preto e branco alteraria a cor dela, o que a regra de imagem original proíbe. Só foto de banco recebe esse tratamento.

## Antes de publicar

- **Revisão da Dra.:** as citações legais das peças de referência foram escritas de memória e não foram conferidas em fonte oficial.
- **Licença:** as fotos são da Pexels, e a licença não foi lida porque o site bloqueou o acesso. De memória, ela não permite mostrar pessoa identificável de forma negativa. Rostos reais em papel de chefe abusivo (`grito-A-perfil`, `grito-B-close`) são os casos de maior risco, e `06-burnout` também pede atenção. Fotos do grito: Pexels 10675499 e 5089721.
- **OAB:** imagens fortes precisam passar pelo critério de sobriedade do Provimento 205/2021. `grito-C-boca` é a opção mais segura do grito.
- **Grade:** todas as peças são escuras, e a queixa inicial era perfil "apagado, escuro". Alterne com peças em papel claro em vez de publicar em sequência.
- **Manual:** o estilo não usa o véu de 55-70% previsto em `docs/MANUAL_CONTEUDO_REDES.md`. O manual não foi alterado, e essa diferença ainda espera decisão.
