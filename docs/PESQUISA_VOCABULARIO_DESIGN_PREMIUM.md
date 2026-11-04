# Vocabulário de design premium: nomes, execução e aplicação à marca

Pesquisa de 04/11/2026, feita a pedido da Jessica. Serve para pedir, pesquisar referência e executar peças de Instagram da Dra. Letícia Barros (HTML/CSS com Playwright, às vezes Pillow/OpenCV, fotos reais).

**Este documento não muda nenhuma regra.** O manual, o processo de carrossel e os padrões aprovados continuam valendo. Onde uma técnica depende de mudar regra, isso está escrito e depende de aprovação.

## 1. Resumo

- **A virada de 2026 é a favor desta marca.** O relatório da Canva tem uma tendência chamada [Opt-Out Era: layout limpo, serifa, marca simples](https://www.mediainfoline.com/brand/canva-unveils-2026-design-trends-the-year-of-imperfect-by-design). A Envato afirma que [a imperfeição sinaliza autenticidade num mundo de conteúdo polido de IA](https://elements.envato.com/lp/creative-trends-2026/). São fontes comerciais: leia como opinião informada, não como dado.
- **O nome do efeito pedido é "text behind subject"** (também "text behind person", "text behind image", "layered typography"). O termo geral é camadas de profundidade (depth layering). Em HTML são três camadas: foto, texto, recorte da mesma foto por cima.
- **O gargalo é a máscara, não o CSS.** Recomendação (inferência): começar com texto atrás de **objeto de borda dura**, cortado à mão. Pessoa com cabelo fica para quando houver foto planejada e tratamento manual. A regra do recorte fica como está até a Letícia decidir (seção 4.1).
- **Cara de IA vem mais do padrão repetido do que de um efeito.** Os sinais mais citados: nenhum espaço vazio, texto minúsculo, tudo no mesmo raio e na mesma sombra, brilho dourado uniforme, composição centrada por padrão, ícones e faixas intercambiáveis. Teste rápido: [o logo de um concorrente ficaria igualmente bem nesta peça?](https://kognie.com/blog/ai-design-tool-that-doesnt-look-ai-generated)
- **Alerta:** parte do que já está aprovado na marca aparece nas listas de sinais de IA: cartão de vidro, título dourado metalizado, brilhos ✦, eixo centralizado, emoji em cada item. Nada disso está revogado aqui. A seção 3 mostra como reduzir o risco, e a Jessica decide.
- **O que mais rende com menos risco (inferência):** sombra de contato em cor de café, sombra de janela real no fundo, contraste forte de escala, fio duplo com paginação de revista, textura de papel real, marca-texto desenhado à mão, foto que atravessa dois slides.

**Limite importante desta pesquisa:** li texto, não imagens. Nenhuma foto, pin ou vídeo foi visto. Detalhes na seção 6.

## 2. Glossário

### Como ler

- Na coluna **Nesta marca**: **Direto** (serve direto), **Cuidado** (serve com cuidado) ou **Evitar** (evitar nesta marca). Essa classificação é sempre inferência minha, a partir das regras da seção 4.
- A coluna **Executar** é inferência minha, salvo quando traz link.
- "Uso corrente" significa definição comum da área, sem fonte específica lida nesta pesquisa.
- Fonte com a marca **(t)** foi vista só em trecho de busca; sem marca, a página abriu (seção 6).
- As palavras de busca ficam em inglês porque é assim que os resultados aparecem.

### 2.1 Profundidade e sobreposição

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| text behind subject / texto atrás do sujeito | Palavra passa atrás da pessoa ou do objeto | text behind subject, text behind person | Foto + texto + recorte alinhado (receita 4.1) | **Cuidado**, exige máscara. [Canva](https://www.canva.com/features/add-text-behind-image/) (t), [Pinterest](https://www.pinterest.com/ideas/typography-portrait-ideas/918178766921/) (t) |
| object overlapping type / objeto sobre a letra | Só parte do objeto invade a letra | object overlapping text | Igual, com sobreposição pequena | **Cuidado**, melhor com objeto. [YouTube, Kim de Been](https://www.youtube.com/watch?v=49JsIVh2Cfw) |
| faded text behind subject / texto que some atrás | Texto dissolve no fundo atrás da figura | faded text behind subject | `mask-image` em gradiente no texto | **Cuidado**. [YouTube, Kim de Been](https://www.youtube.com/watch?v=uByS5nrxfiw) |
| depth layering, layered typography / camadas de profundidade | Elementos em planos diferentes | layered typography poster, depth layering | Pilha com `z-index`, sombras coerentes | **Direto** sem recorte (cartão e texto sobre foto). [Framer](https://www.framer.com/community/marketplace/components/3d-depth-text-effect/) (t) |
| foreground, midground, background / primeiro plano, plano médio, fundo | Os três planos da cena | layered depth composition | Desfoque leve no fundo, nitidez no objeto | **Direto**. Termo em galerias de prompt (t); uso corrente |
| overlap / sobreposição | Um elemento cobre parte de outro | overlapping layout | Margem negativa, `position:absolute` | **Direto**. [Adobe: sobreposição e assimetria](https://www.adobe.com/express/learn/blog/design-trends-2026) |
| interleaving, intertwine / entrelaçamento | Fica ora na frente, ora atrás, como um trançado | intertwine illustrator, interlocking type | Illustrator: Object > Intertwine > Make. HTML: duas cópias com `clip-path` | **Cuidado**. [Adobe Intertwine](https://helpx.adobe.com/illustrator/desktop/manage-objects/reshape-transform-objects/create-intertwined-objects.html) (t) |
| occlusion / oclusão | O que está na frente esconde o de trás | occlusion depth cue | Decorre das camadas | **Direto**. Uso corrente |
| parallax / paralaxe | Planos se movem em velocidades diferentes | parallax layers, 2.5D photo | Só em vídeo: camadas animadas | **Cuidado**, só Reels. Uso corrente |
| out of bounds, pop-out, breaking the frame / fora da moldura | Parte do sujeito sai da moldura da foto | out of bounds effect, pop out frame | Moldura atrás, recorte por cima, sombra | **Cuidado**, exige máscara, nunca sobre as faixas. [PhotoshopCafe via busca](https://photoshopcafe.com/?p=20744) (t), [CreativePro](https://creativepro.com/creating-out-of-bounds-effect-photoshop/) (t) |
| 3D pop-out / saída em 3D | Mesmo efeito com perspectiva forte | 3D pop out photo effect | Recorte + sombra + perspectiva | **Evitar**, chamativo. [Corel](https://learn.corel.com/tutorials/create-an-out-of-bounds-photo/) (t) |
| forced perspective / perspectiva forçada | Escala falsa entre planos | forced perspective poster | Foto real planejada | **Cuidado**. Galerias de prompt (t); uso corrente |
| glass card, floating card / cartão flutuante | Cartão acima da foto, sem recorte | floating card layout | `backdrop-filter`, sombra em camadas | **Direto**, já aprovado em Pergunta e Mito. Ver sinal 8 da seção 3 |

### 2.2 Elementos que envolvem ou transpassam

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| ribbon wrap / fita envolvente | Fita passa à frente e atrás da pessoa | ribbon wrap person, ribbon around subject | SVG em duas metades; recorte cobre o trecho de trás | **Cuidado**. Busca direta quase só trouxe faixas planas |
| ribbon of light / fita de luz | Fita luminosa ao redor da figura | ribbon of light photoshop | Pincel + Screen + máscara | **Evitar**, fica efeito de filtro. [YouTube, Blue Lightning](https://www.youtube.com/watch?v=tJUpAz4aQJs) |
| wrap-around lines / linhas envolventes | Fios finos contornam o sujeito | wrap lines around person | SVG `path` com traço, trecho de trás mascarado | **Cuidado**, o arco foi reprovado (seção 4). Uso corrente |
| orbit lines / linhas de órbita | Elipses ao redor do objeto | orbit lines design | SVG `ellipse` em duas metades | **Cuidado**, é arco. Busca sem fonte específica |
| swoosh / traço em curva | Curva rápida com ponta afinada | swoosh graphic | SVG `path` | **Evitar**, datado (inferência) |
| swirl, glowing swirl / redemoinho luminoso | Espiral de luz em volta da pessoa | glowing swirl around person | Caminho + brilho | **Evitar**, neon. [YouTube, NitroLandTutorials](https://www.youtube.com/watch?v=WRaHcwql6Ng) |
| flowing lines / linhas fluidas | Feixe de curvas paralelas | flowing lines background | SVG gerado por curvas | **Cuidado**, só como fundo discreto. Uso corrente |
| light trails / rastro de luz | Riscos de luz, como longa exposição | light trails photoshop, path blur | Path Blur no Photoshop | **Evitar**. [YouTube, Brendan Williams](https://www.youtube.com/watch?v=cIWDAoUjb1o) |
| light painting / pintura com luz | Fotografia real com fonte móvel | light painting portrait | Só em ensaio real | **Cuidado**, real sim, simulado não. Uso corrente |
| text wrap around subject / texto contornando a figura | Linhas de texto seguem o contorno | wrap text around person, surrounding text | Por caminho (abaixo); em bloco, `shape-outside` | **Cuidado**, leitura difícil. [PiXimperfect](https://www.youtube.com/watch?v=fCFEDVMw9q4), [Brendan Williams](https://www.youtube.com/watch?v=5L307t7scSo), [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/shape-outside) |
| displacement text / texto deformado pela forma | Letras acompanham o volume do corpo ou do tecido | photoshop displace text | Filtro Displace; sem HTML equivalente simples | **Evitar**. [Photoshop Roadmap](https://www.photoshoproadmap.com/how-to-create-a-text-and-photo-poster-with-displacement-effects-in-photoshop/) (t) |
| text on a path / texto em caminho | Texto segue uma linha curva | text on path, textPath | SVG `<textPath>` | **Direto** em selo; **Cuidado** em curva longa. [MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath) |
| typographic halo / halo de texto | Anel de texto em torno de cabeça ou objeto | circular text around object | `<textPath>` em círculo | **Cuidado**: em objeto sim; em torno da cabeça da Dra. vira autoengrandecimento (inferência) |
| thread, string / fio, linha de costura | Linha fina que costura elementos | thread overlay, string art | PNG real ou SVG com tremor leve | **Cuidado**. [Creative Market](https://creativemarket.com/Feelsoul/292259404-70-Sentimental-threads) (t) |
| tape, washi tape / fita adesiva | Fita prende foto ou texto | tape collage | Foto real de fita, sem sombra falsa | **Cuidado**, informal. Uso corrente |
| liquid wrap / envoltório líquido | Forma líquida envolve o objeto | liquid wrap, chrome liquid | 3D | **Evitar**. [Envato: Organic flow](https://author.envato.com/hub/graphic-design-trends-2026/) |
| wire / arame | Linha rígida contornando | wire line art | SVG | **Evitar**, sem relação com a marca (inferência). Uso corrente |
| line art overlay / desenho de linha sobre foto | Traço desenhado por cima da fotografia | line art over photo, mixed media portrait | SVG sobre foto | **Cuidado**, nunca sobre o rosto da Dra. [Pixlr](https://pixlr.com/design/line-art-maker/) (t) |
| image wrap / imagem moldada ao objeto | Estampa acompanha o volume | wrap image around object | Displace ou warp | **Evitar**. [YouTube, VerticDesigns](https://www.youtube.com/watch?v=hBZe6bfHSJ4) |

### 2.3 Sombras e luz

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| drop shadow / sombra projetada simples | Cópia borrada atrás do elemento | drop-shadow vs box-shadow | PNG com transparência: `filter: drop-shadow()` segue a forma | **Cuidado**, sozinha fica barata. [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/filter-function/drop-shadow) |
| contact shadow / sombra de contato | Sombra curta, escura, onde o objeto toca | contact shadow | Elipse borrada sob o objeto | **Direto**, é a que mais dá realismo. [Photoshop Roadmap](https://photoshoproadmap.com/add-text-behind-a-subject-with-realistic-shadows-in-photoshop) |
| cast shadow / sombra projetada | Sombra longa, ditada pela direção da luz | cast shadow | Forma do objeto distorcida + `blur` | **Direto**. Mesma fonte |
| long shadow / sombra longa | Sombra chapada a 45 graus | long shadow flat design | `text-shadow` repetido | **Evitar**, moda de [por volta de 2013](https://webdesignerdepot.com/flat-design-casts-a-long-shadow) (t) |
| soft shadow, hard shadow / sombra suave, dura | [Borda dura indica luz direta; suave, luz difusa](https://photoshoproadmap.com/add-text-behind-a-subject-with-realistic-shadows-in-photoshop) | hard light shadow | Controlar o `blur` | **Direto**: combinar com a luz da foto |
| ambient occlusion / oclusão de ambiente | Escurecimento nas frestas e encontros | ambient occlusion | Gradiente escuro pequeno nas junções | **Direto**. Mesma fonte |
| layered shadow / sombra em camadas | Várias sombras somadas com queda natural | layered box-shadow, smooth shadow | Ver receita 4.3 | **Direto**. [Josh Comeau](https://www.joshwcomeau.com/css/designing-shadows/) |
| color-matched shadow / sombra na cor do fundo | Sombra tingida, não preta | shadow color matching | Sombra em café `#1E1814`, nunca `#000` puro | **Direto**. [Josh Comeau](https://www.joshwcomeau.com/css/designing-shadows/) |
| gobo, window shadow / sombra de janela | Luz recortada por um molde | gobo overlay, window shadow overlay | PNG real em `multiply` | **Direto** no fundo, fora do rosto. [PetaPixel](https://petapixel.com/2024/01/03/v-flat-worlds-new-shadow-boards-mimic-sunlight-through-windows) (t), [Planet Photoshop](https://planetphotoshop.com/using-photoshop-to-create-digital-gobos.html) (t) |
| palm or leaf shadow overlay / sombra de folhagem | Sombra de plantas sobre a superfície | leaves shadow overlay | Igual | **Cuidado**, clima de praia; janela ou persiana combinam mais. [Adobe Stock](https://stock.adobe.com/images/abstract-window-shadow-with-light-effect-overlay-leaves-shadow-silhouette-element-object-for-spring-summer-overlay-on-mockup-product-presentation/827485995) (t) |
| rim light / luz de contorno | Luz por trás que desenha a borda do sujeito | rim light portrait | Na foto real; simular fica falso | **Direto** se vier da foto. [StudioBinder](https://www.studiobinder.com/blog/what-is-a-rim-light-photography-definition/) (t) |
| glow / brilho difuso | Halo de luz em volta | outer glow | `text-shadow` amplo | **Evitar** em texto: [efeitos excluídos para não parecer IA](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md) |
| bloom / florescimento de luz | Altas luzes transbordam | bloom effect | Cópia borrada em `screen` | **Evitar**. Moda de games, [PC Gamer](https://www.pcgamer.com/six-terrible-graphical-effects-that-need-to-stop) (t) |
| light leak / vazamento de luz | Luz que vaza no filme | light leak overlay | PNG em `screen` | **Cuidado**, um toque, longe do rosto. [StudioBinder](https://www.studiobinder.com/blog/light-leak-overlay-download/) (t) |
| lens flare / reflexo de lente | Reflexo da lente contra a luz | lens flare | PNG em `screen` | **Evitar**: [vira clichê sem fonte de luz visível](https://3d.irpr.agency/glossary/lens-flare/) (t) |
| chiaroscuro / claro-escuro | [Alto contraste de luz e sombra para dar drama e guiar o olhar](https://www.adobe.com/creativecloud/video/discover/low-key-vs-high-key-lighting.html) (t) | chiaroscuro portrait, low key | Foto low-key real, fundo café | **Direto**, é o que as referências dela fazem |
| volumetric light, god rays / luz volumétrica | Feixes visíveis no ar | volumetric light | Foto real | **Cuidado**, simulada lembra IA (inferência). Uso corrente |
| vignette / vinheta | [Escurecimento em direção às bordas](https://www.adobe.com/uk/creativecloud/photography/discover/what-is-vignette-in-photography) (t) | vignette | `radial-gradient` em café | **Direto**, já está no processo; suave |
| dodge and burn / clarear e escurecer | [Técnica de laboratório para regular exposição por áreas](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html) (t) | dodge and burn | [Camada em Soft Light](https://blogs.adobe.com/jkost/2018/08/working-with-blend-modes-in-photoshop-cc.html) (t) | **Direto** em foto de banco e objeto; **Evitar** na Dra. |
| neumorphism / neumorfismo | [Elementos que parecem extrudados do fundo](https://en.wikipedia.org/wiki/Neumorphism) (t) | neumorphism | Sombras claras e escuras | **Evitar**, baixo contraste |
| glassmorphism / vidro fosco | [Translucidez e desfoque que parecem vidro fosco](https://www.nngroup.com/articles/glassmorphism/) | glassmorphism | [`backdrop-filter`](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter) | **Cuidado**: aprovado nas séries, não expandir. [NN/g: usar com moderação e testar contraste](https://www.nngroup.com/articles/glassmorphism/) |
| reeded glass, fractal glass / vidro canelado | [Vidro que divide a imagem em tiras distorcidas](https://design.tutsplus.com/tutorials/how-to-create-a-reeded-glass-photo-effect-in-photoshop--cms-109005) | fractal glass effect | Mapa de deslocamento | **Evitar**, moda de ferramenta (inferência). Aparece em [#photoshoptutorial](https://www.instagram.com/explore/tags/photoshoptutorial/) |

### 2.4 Linhas e fios

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| hairline / fio finíssimo | [O fio mais fino imprimível, abaixo de 1 ponto, sem medida acordada](https://www.oreilly.com/library/view/the-complete-manual/9780132821926/chapter-45.html) (t) | hairline rule | `border-top: 2px` (ver nota abaixo) | **Direto** |
| rule / fio | Linha reta que separa ou organiza | rule line typography | `border` ou `<hr>` | **Direto**. [PrintWiki](https://printwiki.org/Rule_Line) (t) |
| double rule / fio duplo | Duas linhas paralelas | double rule | `border-top: 6px double` | **Direto** |
| Oxford rule / fio Oxford | [Borda de um fio grosso e um fino lado a lado](https://www.printmag.com/design-culture/how-the-oxford-rule-led-to-rolling-stone/) | oxford rule | Dois `div`, receita 4.5 | **Direto**, com história de imprensa e livro |
| Scotch rule / fio escocês | [Fio duplo, em geral com o de cima mais pesado](https://www.oreilly.com/library/view/the-complete-manual/9780132821926/chapter-45.html) (t); ver [TypeDrawers](https://typedrawers.com/discussion/comment/61959) (t) | scotch rule | Igual, invertido | **Direto**. Fontes divergem no detalhe |
| keyline / fio-guia | [Contorno que marca forma e posição da arte](https://en.wikipedia.org/wiki/Keyline) (t) | keyline border | Moldura fina interna | **Direto**, já há moldura fina nas capas |
| corner bracket / cantoneira | Só os cantos de uma moldura | corner frame lines | Quatro `div` com duas bordas | **Direto**, já aprovado na capa Ouro editorial. Busca só trouxe ferragens |
| crop marks / marcas de corte | [Fios que definem os limites do corte](https://helpx.adobe.com/indesign/using/printers-marks-bleeds.html) (t) | crop marks | Fios curtos fora da área | **Cuidado**, decorativo, ar técnico |
| registration marks / marcas de registro | [Alvos que alinham as chapas de cor](https://helpx.adobe.com/indesign/using/printers-marks-bleeds.html) (t) | registration mark | SVG pequeno | **Cuidado**, um só, ou nenhum |
| guilloche / guilhochê | [Padrão repetitivo gravado mecanicamente](https://blog.fontlab.com/2026/04/14/money-lace-guilloche-intaglio-spirograph/) (t), usado em [cédulas e documentos](https://regulaforensics.com/glossary/banknotes/guilloches/) (t) | guilloche pattern | SVG paramétrico, dourado a baixa opacidade | **Direto** como fundo de selo; ar de documento, sem imitar papel oficial |
| ornament / ornamento | Elemento decorativo tipográfico | printer's ornament | Glifo da fonte | **Cuidado**, um por peça |
| grid lines / linhas de grade | Grade à mostra como elemento | visible grid | `background` com gradientes lineares | **Cuidado**, ar técnico (ver Swiss) |
| contour lines / curvas de nível | Linhas de mapa topográfico | contour lines background | SVG | **Evitar**, sem relação com o tema (inferência). Uso corrente |
| arcs / arcos | Curvas abertas decorativas | arc lines | SVG `path` | **Evitar** sem pedido: [ela reprovou o arco em 10/10](PASSAGEM_DE_CONTEXTO.md) |
| flourish / floreio | Curva ornamental de caligrafia | flourish typography | Vetor ou swash | **Cuidado**, um só |
| dingbat / símbolo tipográfico | [Ornamento ou espaçador de composição](https://wikiwand.com/en/Fleuron_(typography)) (t) | dingbats | Glifo | **Cuidado**; ✦ já está em uso, ver sinal 10 |
| fleuron, hedera / flor tipográfica | [Glifo decorativo; a folha de hera ❦ é o clássico](https://wikiwand.com/en/Fleuron_(typography)) (t) | fleuron, aldus leaf | [U+2767 ❧](https://codepoints.net/U+2767) (t); conferir se a fonte tem | **Direto** como separador de seção, alternativa ao ✦ |
| seal / selo | Marca circular de autenticação | seal design | SVG + `textPath` | **Direto**, já aprovado no Mito (gravado, sem brilho de moeda) |
| pilcrow / sinal de parágrafo | O símbolo ¶ | pilcrow | Glifo | **Cuidado**, detalhe de texto legal (inferência) |
| section sign / parágrafo legal | O símbolo § | section sign | Glifo em EB Garamond | **Direto**: nasce do próprio direito, sem clichê (inferência) |

**Nota sobre fio fino (inferência):** a peça de 1080 px aparece com cerca de 390 pontos de largura no celular. Fio de 1 px quase some, e [fio fino tende a fechar quando vazado do preto](https://www.oreilly.com/library/view/the-complete-manual/9780132821926/chapter-45.html) (t). Usar 2 px como mínimo, e testar no celular.

### 2.5 Tipografia

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| kinetic typography / tipografia em movimento | [Letras e palavras animadas](https://en.wikipedia.org/wiki/Kinetic_typography) (t) | kinetic typography | Reels, motor próprio | **Direto** só em vídeo, sem exagero |
| editorial typography / tipografia editorial | Lógica de revista: título, olho, corpo | editorial type system | Hierarquia em 3 ou 4 níveis | **Direto**. [Awwwards](https://www.awwwards.com/typography-heavy-design.html) |
| type as image / tipo como imagem | A palavra é a imagem principal | type as image, type-led | Título ocupa a peça | **Direto**, é o formato Frase |
| oversized type / tipo gigante | Muito maior que o esperado | oversized type | 200 px ou mais | **Direto** |
| cropped type / letra cortada | Parte da letra sai da peça | cropped typography | `overflow: hidden` | **Cuidado**: só decorativa, respeitando a área segura; nunca cortar palavra que precisa ser lida |
| masked type, image in text / foto dentro da letra | [A imagem só aparece dentro das letras](https://www.creativebloq.com/computer-arts/masking-type-10079462) (t) | image in text, clipping mask text | [`background-clip: text`](https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip) | **Direto** em fundo café com foto de objeto; **Evitar** com o rosto da Dra. |
| knockout type / texto vazado | [O fundo aparece através das letras](https://fontbundles.net/design-school/how-to-make-a-knockout-design-in-illustrator) (t) | knockout text | `mix-blend-mode` ou máscara SVG | **Cuidado**, conferir contraste |
| outlined, stroke type / letra só com contorno | Só o traço, sem preenchimento | outline text | [`-webkit-text-stroke`](https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-text-stroke) | **Cuidado**: serifa fina em contorno fica frágil; só 120 px ou mais |
| stacked type / tipo empilhado | Palavras uma sobre a outra, justas | stacked typography | `line-height` 0,9 | **Direto**, conferir colisão de acentos |
| ligature / ligadura | [Duas letras fundidas num glifo](https://fonts.google.com/knowledge/glossary) (t) | ligatures | [`font-variant-ligatures`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings) | **Direto**, é o que uma fonte de IA comum não traz (inferência) |
| swash / floreio de letra | [Variante com terminações elaboradas](https://fonts.google.com/knowledge/glossary) (t) | swash italic | [`"swsh"`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings). A [EB Garamond tem itálicos swash](https://tug.ctan.org/fonts/ebgaramond/README) (t) | **Direto**, uma letra por peça. Testar na fonte instalada |
| drop cap / capitular | [Letra inicial que desce por 2 ou mais linhas](https://www.creativebloq.com/design/fonts-typography/typography-glossary-an-a-z-of-type-terms) (t). Ver [InfoDesign](https://infodesign.emnuvens.com.br/infodesign/article/view/806) (t) | drop cap | `::first-letter`, `initial-letter` | **Direto** em slide de texto |
| small caps / versalete | [Maiúsculas desenhadas para conviver com minúsculas](https://fonts.google.com/knowledge/introducing_type/introducing_alternate_glyphs) (t) | small caps | [`font-variant-caps: small-caps`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings) | **Direto**: usar tamanho nominal 28 px ou mais, porque a altura visual fica menor que 22 px (inferência) |
| optical size / tamanho óptico | [Versões da fonte ajustadas por faixa de tamanho](https://fonts.google.com/knowledge/choosing_type/choosing_typefaces_that_have_optical_sizes) (t) | optical sizes, opsz | `font-optical-sizing` se a fonte tiver o eixo | **Cuidado**, não confirmei o eixo na EB Garamond |
| tracking / espaçamento geral | [Espaço entre todas as letras de um trecho](https://fonts.google.com/knowledge/glossary/tracking_letter_spacing) (t) | tracking | `letter-spacing` | **Direto**: positivo em caixa alta, [negativo em títulos grandes](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) |
| kerning / ajuste de pares | [Espaço entre um par de letras](https://designshack.net/articles/typography/typography-terms-what-they-mean) (t) | kerning | `font-kerning: normal` + ajuste manual em `span` | **Direto**, conferir "Vo", "Te" e "Ao" em títulos |
| mixed type / mistura de tipos | Serifa com sans, romano com itálico | serif italic headline | `<em>` no destaque | **Direto**, assinatura da marca |
| ghost type / texto fantasma | Palavra ou número gigante e quase invisível | ghost text background | Opacidade 6 a 12% | **Direto**, decorativo, nunca com informação |
| justified block / bloco justificado | Linhas de largura igual | justified type | `text-align: justify`, `hyphens` | **Cuidado**, só em largura boa, cria rios |
| marginalia / anotação na margem | Nota ao lado do bloco, como em livro | margin notes editorial | Inter 22 a 24 px na margem | **Direto**, ótima para artigo de lei (a busca não trouxe definição) |
| pull quote / olho | [Trecho destacado em tipo maior](https://www.fineprintschool.com/glossary-of-printing-terms/pull-quote) (t) | pull quote | EB Garamond itálico + fio | **Direto**. [Adobe](https://helpx.adobe.com/sk/indesign/how-to/make-pull-quote-callout.html) (t) |
| kicker / chapéu | [Linha curta acima do título](https://www.mediabistro.com/go-freelance/business-basics/tk-mb-media-glossary/) (t) | kicker | Inter 600 caixa alta | **Direto**, já é regra |
| deck, standfirst / linha fina | [Texto entre título e corpo](https://www.mediabistro.com/go-freelance/business-basics/tk-mb-media-glossary/) (t) | deck, dek | EB Garamond itálico médio | **Direto** |
| folio, running head / paginação, cabeçalho corrido | [Número de página e texto repetido no topo](https://www.mediabistro.com/go-freelance/business-basics/tk-mb-media-glossary/) (t) | running head | Paginador "03 / 08" | **Direto**, já é regra |
| foil type / letra em folha metálica | Imita hot stamping | gold foil text | Ver 4.8 | **Cuidado**, sem brilho exagerado |
| lining vs oldstyle figures / algarismos alinhados e de texto | [Alinhados seguem a altura das maiúsculas; os de texto têm ascendentes e descendentes](https://fonts.google.com/knowledge/introducing_type/understanding_numerals) (t) | oldstyle figures | `font-variant-numeric` | Alinhados: **Direto**. De texto: **Evitar**, a regra pede alinhados |
| micrography, typographic portrait / retrato de palavras | [Rosto formado por texto](https://in.pinterest.com/nouranosama980/typography-portraits/) (t) | typographic portrait | Mapa de luminosidade | **Evitar**: altera a imagem da Dra. |
| deformation typography / tipo deformado | Letra distorcida de propósito | new creative deformation | Warp, escala | **Evitar**; mas vale o critério ["two-second read"](https://guide.pinterest.com/design/new-creative-deformation/): a mensagem precisa ser lida em dois segundos |
| variable font / fonte variável | [Um arquivo com faixa de pesos e larguras](https://www.awwwards.com/typography-heavy-design.html) | variable fonts | `font-variation-settings` | **Direto** como ferramenta |

### 2.6 Texturas e acabamentos

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| film grain / grão de filme | [Textura com quantidade, tamanho e rugosidade](https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/enhance-texture-with-grain.html) (t) | film grain overlay | Camada abaixo da pessoa (4.6) | **Direto** no fundo; **proibido** no rosto da Dra. |
| noise / ruído | Ruído digital fino | svg noise | [`feTurbulence` `fractalNoise`](https://css-tricks.com/grainy-gradients/) | **Direto**, baixa opacidade |
| halftone / retícula | Imagem em pontos | halftone effect | [Filtro Color Halftone](https://www.shutterstock.com/blog/photoshop-tutorial-mimic-risograph-effect) (t) | **Cuidado**: só em objeto ou fundo; nunca na Dra. |
| risograph / risografia | [Grão, desencontro e sobreposição de tintas](https://designshack.net/articles/inspiration/risograph-style-backgrounds) (t) | risograph effect | Duas cores + `multiply` + desalinho | **Evitar**, é informal e colorido (inferência) |
| paper texture / textura de papel | Fibra e irregularidade do papel | paper texture overlay | Scan real em `multiply` | **Direto**, já na direção v4. [Texto no vinco fica bem com Multiply](https://gomedia.com/tutorials/crumpled-paper-texture-freebie/) (t) |
| torn paper, ripped edge / papel rasgado | [Borda rasgada, com o branco do papel](https://blog.spoongraphics.co.uk/?p=11336) (t) | torn paper edge | PNG real de scan | **Cuidado**, uma borda só; rasgo vetorial denuncia |
| crumpled paper / papel amassado | Vincos de papel | crumpled paper texture | Scan em `multiply` | **Direto**, ela citou papel amassado nas referências |
| photocopy / fotocópia | Alto contraste e sujeira de copiadora | photocopy effect | Levels + grão | **Evitar** na Dra.; **Cuidado** em documento genérico. [#posterdesign](https://www.instagram.com/explore/tags/posterdesign/) |
| washi / papel japonês | Papel de fibra longa | washi paper texture | Scan | **Cuidado**, a busca não trouxe fonte |
| linen / linho | Trama fina de tecido | linen texture | Scan em `soft-light` | **Direto** em fundo, sutil (inferência) |
| canvas / tela | Trama mais grossa | canvas texture | Igual | **Cuidado**, lembra pintura |
| marble / mármore | Pedra com veios | marble texture | Foto real | **Evitar**: mármore e dourado são clichê de "advocacia de luxo" (inferência) |
| gold foil / folha de ouro | [Folha metálica aplicada a quente](https://madegooddesigns.com/spot-uv-vs-foil/) (t) | gold foil texture | Ver 4.8 | **Cuidado** |
| emboss, deboss / relevo alto e baixo | [Relevo em alto ou baixo no papel](https://madegooddesigns.com/emboss-vs-deboss/) (t) | blind emboss, deboss mockup | Luz e sombra de 1 px, cor igual ao fundo | **Direto** para logo em marca d'água, é discreto |
| letterpress / tipografia de prensa | [Impressão antiga, marca o papel](https://madegooddesigns.com/emboss-vs-deboss/) (t) | letterpress mockup | Texto com sombra interna sutil sobre papel | **Direto**, sutil |
| spot UV / verniz localizado | [Verniz brilhante transparente sobre área fosca](https://madegooddesigns.com/spot-uv-vs-foil/) (t) | spot uv mockup | Reflexo em `screen` sobre letra | **Cuidado**, só faz sentido em foto real de impresso |
| wax seal / selo de cera | Lacre de cera | wax seal | Foto real do lacre | **Cuidado**, um só em peça especial; é ornamental |
| plastic wrap / plástico filme | [Reflexos de plástico, usados em Screen](https://we.graphics/item/plastic-wrap-overlay-textures) (t) | plastic wrap overlay | PNG em `screen` | **Evitar**, moda de capa de disco (inferência) |
| duotone / duotom | [Troca as cores por duas, seguindo a luminosidade](https://learn.g2.com/duotone-effect) (t) | duotone | Gradient map ou SVG `feColorMatrix` | **Direto** em banco e objeto (café e dourado); **proibido** na Dra. |
| tritone / tritom | [Três cores; o termo duotone é usado errado para isso](https://blog.prototypr.io/duotone-in-web-design-875d8e90da4b) (t) | tritone | Igual | **Cuidado**, [pode ficar duro](https://www.websitebuilderinsider.com/how-do-you-make-a-tritone-in-photoshop/) (t) |
| gradient mesh / malha de gradiente | Gradiente com vários pontos de cor | mesh gradient | Vários `radial-gradient` | **Evitar**, gradiente genérico é sinal de IA |
| grainy gradient / gradiente com grão | Gradiente com ruído | grainy gradient | [CSS-Tricks](https://css-tricks.com/grainy-gradients/) | **Cuidado**: só café para café, como luz, sem cor nova |
| chromatic aberration, RGB split / aberração cromática | [Franja de cor imitando defeito de lente](https://limeup.io/glossary/chromatic-aberration/) (t) | rgb split | Canais deslocados | **Evitar**, foge da paleta |
| scanline / linhas de varredura | Linhas de monitor antigo | scanlines | `repeating-linear-gradient` | **Evitar** |
| overlay / sobreposição de textura | Camada que combina com a de baixo | texture overlay | `mix-blend-mode` | **Direto**. [Lista de valores, MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode) |
| multiply / multiplicação | [Resultado sempre mais escuro](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html) (t) | multiply blend | `mix-blend-mode: multiply` | **Direto**: sombra e papel |
| screen / tela | [Resultado sempre mais claro](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html) (t) | screen blend | `screen` | **Direto**: luz e poeira |
| overlay mode / sobrepor | [Multiplica ou clareia conforme o cinza 50%; comum para textura](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html) (t) | overlay blend | `overlay` | **Direto** |
| soft light / luz suave | [Versão mais gentil do Overlay](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html) (t) | soft light blend | `soft-light` | **Direto**: linho, papel |
| color burn / superexposição de cor | [Escurece aumentando o contraste](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html) (t) | color burn | `color-burn` | **Cuidado**, satura, testar |

### 2.7 Tratamento de imagem

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| cutout / recorte | Sujeito isolado do fundo | cutout photo | Caneta (Pen) ou Select and Mask | **Cuidado**: ver regra, seção 4.1 |
| collage / colagem | Pedaços combinados | editorial collage | PNGs reais | **Cuidado**: ela reprovou vários objetos juntos. [Adobe](https://www.adobe.com/express/learn/blog/design-trends-2026) |
| photomontage / fotomontagem | [Imagem montada a partir de fotografias](https://en.wikipedia.org/wiki/Photomontage) (t) | photomontage | Igual | **Cuidado**: nunca para criar situação que não existiu |
| scrapbook / álbum de recortes | [Elementos que parecem colecionados, não compostos](https://author.envato.com/hub/graphic-design-trends-2026/) | scrapbook style | Adesivo, fita, nota | **Evitar** como estilo da peça; informal |
| sticker / adesivo | [Recorte com contorno branco grosso](https://picsart.com/blog/ootd-sticker-peeling-trend/) (t) | die cut sticker | Traço branco no PNG | **Evitar** na Dra.; **Cuidado** em pílula de série |
| double exposure / dupla exposição | [Duas fotos fundidas numa só](https://bwillcreative.com/how-to-create-a-double-exposure-in-photoshop/) (t) | double exposure | [tutvid](https://www.youtube.com/watch?v=HYVDlajEZOI), [Katty Ros](https://www.youtube.com/watch?v=Dz31tzl_U-4) | **Evitar** na Dra.; **Cuidado** em objeto e cidade |
| dispersion / dispersão | [Sujeito se desfaz em partículas](https://www.youtube.com/watch?v=EjkUZE84VWg) | dispersion effect | Máscara + pincel | **Evitar**, efeito de 2015 e cara de filtro (inferência) |
| halftone portrait / retrato em retícula | Rosto em pontos | halftone portrait | Filtro | **Evitar**: altera a Dra. |
| color grading / gradação de cor | [Tinge sombras, meios-tons e altas luzes em separado](https://blog.adobe.com/en/publish/2020/10/20/introducing-color-grading) (t) | color grading | Lightroom, LUT | **Direto** em banco; **proibido** na Dra. |
| split toning / tonalização dividida | [Tinge altas luzes e sombras](https://helpx.adobe.com/ph_fil/lightroom-classic/how-to/stylize-photo-with-split-toning.html) (t) | split toning | Sombras café, altas luzes areia | **Direto** em banco |
| tonal range / faixa tonal | Do preto ao branco da imagem | tonal range | Levels, curvas | **Direto** em banco. Uso corrente |
| selective color / cor seletiva | Foto em P&B com uma cor | selective color | Máscara | **Evitar**, é clichê (inferência) |
| cinematic crop / corte de cinema | Corte largo e tenso | cinematic crop | Faixa horizontal de foto | **Direto** |
| motion blur / desfoque de movimento | Rastro de movimento | motion blur | Filtro | **Cuidado**, real sim |
| long exposure / longa exposição | Tempo longo de captura | long exposure | Foto real | **Cuidado**, real sim |
| photo in shape, arch frame / foto em forma, em arco | Foto dentro de forma | arch photo frame | `clip-path`, `border-radius` | **Cuidado**: arco lembra template de Canva (inferência). [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path) |
| mask / máscara | Esconde sem apagar | layer mask, css mask | [`mask-image`](https://developer.mozilla.org/en-US/docs/Web/CSS/mask-image); [Adobe](https://helpx.adobe.com/si/photoshop/how-to/make-selection-layer-mask.html) (t) | **Direto** como técnica |
| clipping mask / máscara de recorte | Camada aparece só dentro da de baixo | clipping mask | `clip-path`, `background-clip` | **Direto** |
| matting / recorte fino | Separa fio de cabelo e borda translúcida | image matting, hair matting | [BiRefNet + trimap + ViTMatte](https://ice-ice-bear.github.io/posts/2026-04-13-matting-libraries) | **Cuidado**, só como base para retoque e com aprovação |
| editorial retouch / retoque editorial | Retoque que preserva textura de pele | frequency separation, natural retouch | Profissional | **Evitar** por nós; a imagem da Dra. fica original |
| 3D render / render 3D | Objeto modelado | 3D render | Blender | **Evitar**: [3D genérico é sinal de IA](https://braindetox.kr/en/posts/ai_design_tell_detection.html) |
| mockup / simulação | Arte aplicada em objeto real | letterpress mockup | Foto de papel com arte aplicada | **Cuidado**: [frontal demais denuncia, sombra é o que convence](https://elistit-web.pages.dev/guides/how-to-make-realistic-etsy-mockups/) (t) |

### 2.8 Disposição e composição

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| grid / grade | [Guias que estruturam a página](https://chiefofdesign.com.br/en/grid-design/) | layout grid | CSS Grid, 6 colunas | **Direto**, já é regra |
| modular grid / grade modular | [Colunas cruzadas com guias, formando módulos](https://chiefofdesign.com.br/en/grid-design/) | modular grid | `grid-template-rows` | **Direto** |
| hierarchical grid / grade hierárquica | [Zonas horizontais de larguras diferentes](https://chiefofdesign.com.br/en/grid-design/) | hierarchical grid | Linhas de altura diferente | **Direto** |
| baseline grid / grade de linha de base | [Prende tudo a um mesmo ritmo vertical](https://issuu.com/alina.nicholas01/docs/process_book_-_modular_grid) (t) | baseline grid | `line-height` múltiplo de 8 | **Direto** |
| Swiss, International Style / estilo suíço | [Grades, sem serifa, foto objetiva, branco como estrutura](https://madegooddesigns.com/graphic-design-styles/) | swiss poster | Grade + fio; a serifa fica | **Cuidado**: usar a grade, não a tipografia |
| asymmetry / assimetria | Equilíbrio sem espelhar | asymmetrical layout | Texto em duas colunas de 6 | **Cuidado**: peça única é centrada pela regra; carrossel pode variar |
| rule of thirds / regra dos terços | Pontos fortes em 1/3 da tela | rule of thirds | Rosto a cerca de 34% já é regra na capa | **Direto**. A busca específica não trouxe a Adobe |
| golden ratio / proporção áurea | Razão 1,618 | golden ratio | Só como ajuda | **Cuidado**: há [revisão que não vê ligação com beleza](https://pubmed.ncbi.nlm.nih.gov/38228978/) (t); não é prova de qualidade |
| F and Z pattern / padrões F e Z | [F é padrão de texto sem pistas fortes](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) (t); [Z vai do alto à esquerda ao rodapé à direita em peça com pouco texto](https://ixdf.org/literature/article/visual-hierarchy-organizing-content-to-follow-natural-eye-movement-patterns) (t) | z pattern layout | Título, foto, chamada em Z | **Direto** |
| focal point / ponto focal | O que o olho vê primeiro | focal point | Um por peça, já é regra | **Direto** |
| hierarchy / hierarquia | [Ordem por importância: cor, contraste, escala, agrupamento](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/) (t) | visual hierarchy | Até [3 tamanhos, 2 grandes](https://www.nngroup.com/articles/principles-visual-design/) (t) | **Direto** |
| visual tension / tensão visual | Elementos quase se tocando ou no limite | visual tension | Texto a 8 px do objeto | **Direto**. Uso corrente |
| negative space / espaço negativo | [Dar uma função ao vazio: "60% de espaço negativo, um elemento focal"](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md) | negative space | Reservar uma área vazia | **Direto** |
| white space / respiro | Vazio entre blocos, [agrupa por proximidade](https://ixdf.org/literature/topics/visual-hierarchy) (t) | white space | [Entre grupos, ao menos o dobro de dentro](https://braindetox.kr/en/posts/ai_design_tell_detection.html) | **Direto** |
| editorial layout / diagramação editorial | Lógica de revista | editorial layout | Chapéu, título, linha fina, corpo, olho | **Direto** |
| text-image schemes / esquemas L, U, T, H, I | [Como blocos de texto cercam a imagem](https://chiefofdesign.com.br/en/grid-design/) (t) | column layout | CSS Grid | **Direto** |
| Bento grid / grade bento | [Caixas de tamanhos variados, como marmita japonesa](https://banani.co/definitions/bento-grid) (t) | bento grid | `grid-area` | **Cuidado**: [tudo encaixotado é pista recorrente](https://venngage.com/blog/ai-slop-in-design/); só para slide salvável |
| rule-breaking / quebra de regra | [Escolher um único lugar para fugir do padrão](https://braindetox.kr/en/posts/ai_design_tell_detection.html) | break the grid | Uma quebra por peça | **Cuidado**: ajuda, mas OAB e design system vêm antes |
| diagonal / diagonal | Texto ou corte inclinado | diagonal layout | `transform: rotate` | **Evitar** na peça sóbria; leve em anotação |
| cropped figure / figura cortada | Pessoa cortada pela borda | cropped figure | Enquadre apertado | **Direto**, mas ela reprovou "fotos cortadas" quando sem intenção |
| bleed, full bleed / sangria, sangria total | [Arte passa da linha de corte, sem borda branca](https://helpx.adobe.com/indesign/desktop/print/page-set-up-and-printer-marks/print-bleed-and-slug-areas.html) (t) | full bleed | Foto em 100% da peça | **Direto**, com as faixas por cima |
| generous margins / margens generosas | Margem maior que o mínimo | generous margins | 96 px em slide de frase | **Direto**, regra pede 72 px como base; conferir área segura |
| seamless carousel, continuous panorama / carrossel contínuo | [Tela larga cortada em slides iguais](https://www.krumzi.com/blog/seamless-instagram-carousel) | seamless carousel, panorama carousel | Ver 4.7 | **Direto**, foto ponte é o padrão |
| rhythm / ritmo | Alternância entre peças | visual rhythm | Escuro, claro, escuro; regra de 1 claro a cada 4 | **Direto** |
| scale contrast / contraste de escala | Muito grande ao lado de muito pequeno | scale contrast | 200 px + 28 px | **Direto**, [ela já usa nas referências](PROCESSO_PRODUCAO_CARROSSEL.md) |
| overprinting / sobreimpressão | [Repetição e impressão sobre impressão](https://www.behance.net/gallery/242915265/Experimental-typography-poster-work-7) (t) | overprint | `multiply` em texto | **Evitar**: [sobreposição atrapalhou a leitura](https://www.behance.net/gallery/58228481/Typographic-Poem-Poster) (t) |
| optical center / centro óptico | Pouco acima do centro geométrico | optical center | Deslocar 3 a 5% para cima | **Direto**, [já é regra](PROCESSO_PRODUCAO_CARROSSEL.md) |
| leading lines / linhas guia | Olhar ou fio aponta para o título | leading lines | Olhar da foto direcionado ao texto | **Direto**. Uso corrente |

### 2.9 Estilos nomeados

| Inglês / português | Traços | Buscar por | Como usar aqui | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| editorial luxury / luxo editorial | [Restrição, proporção, branco deliberado](https://magtype-fonts-b1.pages.dev/elegant-typography-for-luxury-editorial-layouts-luxury-and-fashion-fonts) (t, página fraca) | editorial luxury | Direção geral | **Direto**, sem usar a palavra "luxo" em texto |
| quiet luxury / luxo silencioso | [Cores contidas, ofício, sem marca evidente](https://en.wikipedia.org/wiki/Quiet_luxury) (t); [a textura faz boa parte do trabalho](https://www.blendnow.com/blog/quiet-luxury-aesthetic-the-complete-guide) (t) | quiet luxury aesthetic | Papel, fios, escala | **Direto**, conversa com "discrição e sobriedade" do art. 3º |
| old money / dinheiro antigo | [Herança, brasões, tipo atemporal](https://creativemarket.com/blog/balmoral-heritage-old-money-aesthetics) (t) | old money aesthetic | Só tipografia | **Cuidado**: nada de brasão, sinal de riqueza ou ostentação |
| dark academia / academia sombria | [Fundo escuro, âmbar e dourado, serifa clássica, textura](https://trends.daisyui.com/trend/dark-academia/) (t) | dark academia | Muito perto da paleta | **Direto** como referência; é tendência online, não movimento |
| Opt-Out Era | [Limpo, serifa, marca simples](https://www.mediainfoline.com/brand/canva-unveils-2026-design-trends-the-year-of-imperfect-by-design); [+54% em buscas, segundo cobertura](https://campaignbrief.com/?p=305692) (t) | clean layout serif | Frase | **Direto** |
| neo-minimalism / neominimalismo | [Minimalismo calmo com textura e calor](https://author.envato.com/hub/graphic-design-trends-2026/) | neo minimalism | Slide claro | **Direto** |
| Swiss / suíço | Ver 2.8 | swiss style | Só a grade | **Cuidado** |
| neo-brutalism / neobrutalismo | [Contraste, caixas, bordas grossas, cores vivas](https://www.nngroup.com/articles/neobrutalism/) | neobrutalism | Nada | **Evitar** |
| Art Deco | [Geometria, chevrons, metálicos](https://madegooddesigns.com/graphic-design-styles/); ["Neo Deco" no Pinterest 2026](https://ppc.land/pinterest-unveils-21-consumer-trends-for-2026-advertising-campaigns/) (t) | art deco, neo deco | Fios em degraus, cantos | **Cuidado**: um detalhe; o conjunto puxa ostentação |
| Art Nouveau | [Curvas de planta e do corpo](https://madegooddesigns.com/graphic-design-styles/) | art nouveau | Nada | **Evitar** |
| Bauhaus | [Geometria, cores primárias, sem ornamento](https://madegooddesigns.com/graphic-design-styles/) | bauhaus | Nada | **Evitar** |
| Y2K | Brilho e cromo dos anos 2000 | y2k | Nada | **Evitar** |
| maximalism / maximalismo | [Denso, em camadas, saturado](https://madegooddesigns.com/graphic-design-styles/) | maximalism | Nada | **Evitar**, contrário à sobriedade |
| anti-design | [Rejeita regras, abraça caos e assimetria](https://www.creativebloq.com/design/graphic-design/what-is-anti-design-the-trend-that-tears-up-the-rule-book) (t) | anti design | Nada | **Evitar** |
| mid-century / meados do século | [Formas simples, calor artesanal, ilustração](https://madegooddesigns.com/graphic-design-styles/) | mid century | Em ilustração, se houver | **Cuidado** |
| retrofuturism, chrome / retrofuturismo, cromo | [Futuro visto do passado](https://trends.daisyui.com/trend/retro-futurism/) (t); cromo e brilho tendem a parecer baratos (trecho de busca, sem autor identificado) | retrofuturism | Nada | **Evitar** |
| grunge | [Textura gasta, caótico](https://madegooddesigns.com/graphic-design-styles/) | grunge | Nada | **Evitar** |
| Memphis, postmodern / pós-moderno | [Padrões em choque, cor alegre](https://madegooddesigns.com/graphic-design-styles/) | memphis design | Nada | **Evitar** |
| punk, new wave | [Fotocópia, recorte tipo bilhete](https://madegooddesigns.com/graphic-design-styles/) | punk zine | Nada | **Evitar** |
| brutalism / brutalismo | [Cru, assimétrico, tipo gigante e grosseiro](https://madegooddesigns.com/graphic-design-styles/) | brutalist | Nada | **Evitar** |
| flat design / design plano | [Cor sólida, sem sombra](https://madegooddesigns.com/graphic-design-styles/) | flat design | Nada | **Evitar** como estilo |
| minimalism / minimalismo | [Branco generoso, só o essencial](https://madegooddesigns.com/graphic-design-styles/) | minimal | Frase | **Direto** |

**Tendências de 2025 e 2026 com nome** (quase tudo de fornecedores; é sinal do mercado, não regra):

| Lista | Serve à marca (inferência) | Com cuidado | Não serve |
| --- | --- | --- | --- |
| [Canva 2026](https://www.mediainfoline.com/brand/canva-unveils-2026-design-trends-the-year-of-imperfect-by-design), lema "Imperfect by Design" | Opt-Out Era, Texture Check | Explorecore (zine calmo), Drama Club (cinema) | Reality Warp, Prompt Playground, Notes App Chic, GrannyWave, Zinegeist, Block Party |
| [Adobe Express 2026](https://www.adobe.com/express/learn/blog/design-trends-2026) | Warm, personal visual style; Organic and imperfect design | Freeform and storytelling layouts; Collage and layered visual elements | Maximalist; Surreal; Immersive high-energy; All our senses; Exaggerated letters |
| [Vistaprint](https://www.vistaprint.ca/hub/graphic-design-trends) | Tactile Craft | Micro-Industrial (texto técnico como detalhe) | Distorted Cut, Neon-Noir, Digi-Cute, Hyper-Bloom, Frutiger Aero Revival, Hyper-Individualism, Elemental Folk, Candid Camera Roll |
| [Envato 2026](https://author.envato.com/hub/graphic-design-trends-2026/) | Neo-minimalism | Dual aesthetics | Chaos packaging, Saturation revival, Retro futurism, Organic flow, Scrapbook |
| [G2](https://learn.g2.com/graphic-design-trends) | Serif fonts; Handcrafted and imperfect elements | Mixed-media | Bold maximalist palettes; Organic blobs |
| [Pinterest Predicts 2026](https://ppc.land/pinterest-unveils-21-consumer-trends-for-2026-advertising-campaigns/) (t) | Textura e tato | Neo Deco | Gimme Gummy, Circus |

### 2.10 Elementos gráficos de apoio

| Inglês / português | O que é | Buscar por | Executar | Nesta marca e fonte |
| --- | --- | --- | --- | --- |
| pill / pílula | Etiqueta de cantos redondos; [é convenção de aparência](https://www.w3.org/2021/03/04-openui-irc) (t) | pill tag | `border-radius: 30px` | **Direto**, já aprovada |
| tag / etiqueta | Rótulo de categoria | tag label | Kicker | **Direto** |
| badge / insígnia | [Rótulo estático](https://smart-interface-design-patterns.com/articles/badges-chips-tags-pills/) (t) | badge | Pequeno rótulo | **Cuidado**: nunca imitar "verificado" |
| seal / selo | Ver 2.4 | seal | SVG | **Direto**. Sem símbolos oficiais da OAB ([art. 5º §2º](https://www.oabgo.org.br/arquivos/downloads/provimento-205-1351880.pdf)) |
| stamp / carimbo | Marca de carimbo, com falhas | rubber stamp texture | Scan em `multiply` | **Cuidado**: não simular carimbo de órgão público ou decisão (inferência) |
| sticker / adesivo | Ver 2.7 | sticker | | **Evitar** |
| annotation / anotação | Nota curta que comenta a imagem | annotation design | Inter 22 a 24 px + fio | **Direto** |
| handwritten note / nota à mão | Letra manuscrita real | handwritten note | Escrita real escaneada | **Cuidado**: a regra permite duas famílias de fonte; escrita real é imagem, não fonte, e depende de aprovação |
| callout / chamada | Bloco ligado a um ponto | callout | Fio + texto | **Direto** |
| arrow / seta | Indica direção | hand drawn arrow | SVG desenhado | **Cuidado**: [chevron em todo CTA é padrão](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design); usar uma única para deslizar |
| hand-drawn underline / sublinhado à mão | Traço irregular | hand drawn underline | SVG exclusivo, feito à mão | **Direto**: em claro, é o destaque previsto no processo |
| highlighter / marca-texto | Faixa de cor atrás do texto | highlighter text | `linear-gradient` a 60% da altura, borda irregular | **Direto**, já aprovado; só dourado com texto escuro |
| strikethrough rule / fio de risco | Fio riscando a afirmação | strikethrough | Fio dourado fino | **Direto**, já no Mito |
| editorial data-viz / gráfico editorial | Gráfico com rótulo no próprio dado | editorial data visualization | SVG; skill `dataviz` | **Direto** com dado de fonte oficial; sem resultado de caso |
| one-number stat / número em destaque | [Número grande carregado de sentido](https://www.edwardtufte.com/?p=445) (t) | big number typography | EB Garamond 200 px, lining | **Direto**: prazo ou artigo; nunca valor a receber |
| custom icon / ícone próprio | Ícone desenhado para a marca | custom iconography | SVG fino, mesmo traço | **Direto**: [ícone em círculo em tudo é padrão genérico](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) |
| glass card / cartão de vidro | Ver 2.3 | glass card | `backdrop-filter` | **Cuidado**: mantém nas séries aprovadas |
| caption, cutline / legenda de foto | [Texto que descreve a foto](https://www.mediabistro.com/go-freelance/business-basics/tk-mb-media-glossary/) (t) | photo caption | Inter 22 px | **Direto**, dá ar de revista |
| monogram / monograma | Iniciais como símbolo | monogram | Já há logo | **Cuidado**: não criar outro símbolo |
| footnote / nota de rodapé | Referência legal numerada | footnote design | Número sobrescrito + Inter 22 px | **Direto**: mostra a fonte e é natural em direito (inferência) |

## 3. O que dá cara de IA e como evitar

**Natureza das fontes:** são blogs e fornecedores, não pesquisa. [Nenhum sinal sozinho é prova](https://www.krumzi.com/blog/is-this-image-ai-generated). A coluna **Situação na marca** é inferência minha.

| # | Sinal | Quem diz | Antídoto | Situação na marca |
| --- | --- | --- | --- | --- |
| 1 | Nenhum espaço vazio, o olho não descansa | [Mika Reyes](https://mikareyes.com/ai/how-to-spot-ai-made-graphic-design-and-posters.md) | Dar função ao vazio; um elemento focal | Atenção a capas densas: título, subtítulo, apoio, pílula e moldura juntos |
| 2 | Muita informação em texto minúsculo | [Mika Reyes](https://mikareyes.com/ai/how-to-spot-ai-made-graphic-design-and-posters.md) | Cortar palavras para o importante crescer | Regra de 22 px e 40 palavras já protege |
| 3 | Fontes sem lógica | [Mika Reyes](https://mikareyes.com/ai/how-to-spot-ai-made-graphic-design-and-posters.md) | Duas fontes de propósito | Coberto |
| 4 | Estilos que brigam (vetor, 3D, textura) | [Mika Reyes](https://mikareyes.com/ai/how-to-spot-ai-made-graphic-design-and-posters.md) | Uma linguagem visual | Cuidado ao somar técnicas desta lista: no máximo duas novas por peça (inferência) |
| 5 | Dedos, letras e rostos que se desfazem de perto | [Mika Reyes](https://mikareyes.com/ai/how-to-spot-ai-made-graphic-design-and-posters.md), [Krumzi](https://www.krumzi.com/blog/is-this-image-ai-generated) | Foto real; [texto sempre em camada separada](https://www.krumzi.com/blog/is-this-image-ai-generated) | Render em HTML já resolve o texto |
| 6 | Luz dourada uniforme, até em cena interna | [Krumzi](https://www.krumzi.com/blog/is-this-image-ai-generated) | Foto com [ponto quente, alta luz estourada, temperaturas mistas](https://www.krumzi.com/blog/is-this-image-ai-generated) | **Risco real**: paleta dourada. Dourado em fio e letra, e luz da foto vinda de uma direção; evitar brilho geral acrescentado |
| 7 | Título dourado em 3D, brilho, gradiente neon | [Mika Reyes, legenda do exemplo ruim](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md) | [Pedir sem gradiente, sem 3D, sem glow](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md) | **Conflito com o aprovado**: "ouro metalizado" na capa. Mantém enquanto aprovado; reduzir o brilho é decisão dela |
| 8 | Vidro fosco e bolhas 3D genéricas | [Brain Detox](https://braindetox.kr/en/posts/ai_design_tell_detection.html) | Foto real, dado real ou vazio. [Usar vidro com moderação](https://www.nngroup.com/articles/glassmorphism/) | **Conflito com o aprovado**: Pergunta v6 e Mito v3 usam vidro. Sugestão: não levar a séries novas |
| 9 | Mesma sombra suave em todo cartão; sombra, borda e tinta juntas | [Brain Detox](https://braindetox.kr/en/posts/ai_design_tell_detection.html), [UX Skill](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) | Sombra só no que flutua; escolher um dos três | Revisar cartões |
| 10 | Brilhos decorativos (sparkles) | [Mika Reyes](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md) | Trocar por ornamento tipográfico: ❦ ou § | "✦ Salve para consultar" faz parte do padrão aprovado do Mito. Testar alternativa só com pedido |
| 11 | Mesmo raio grande em tudo | [Brain Detox](https://braindetox.kr/en/posts/ai_design_tell_detection.html), [UX Skill](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) | Raio por função; zero em foto editorial | A regra já traz 8/12/20/30; aplicar por função |
| 12 | Todo intervalo igual | [Brain Detox](https://braindetox.kr/en/posts/ai_design_tell_detection.html) | Entre grupos, o dobro de dentro | Compatível com o ritmo de 8 px |
| 13 | Layout centrado e espelhado por padrão | [Kognie](https://kognie.com/blog/ai-design-tool-that-doesnt-look-ai-generated), [UX Skill](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) | Decidir o eixo; [texto corrido à esquerda](https://braindetox.kr/en/posts/ai_design_tell_detection.html) | Peça única centrada é regra aprovada e tem motivo (recorte da grade). Corpo longo em carrossel pode alinhar à esquerda |
| 14 | Gradientes genéricos de preenchimento | [Kognie](https://kognie.com/blog/ai-design-tool-that-doesnt-look-ai-generated), [Brain Detox](https://braindetox.kr/en/posts/ai_design_tell_detection.html) | Cor sólida + um destaque | Paleta protege; gradiente só para véu |
| 15 | Decoração sem relação com o tema | [Kognie](https://kognie.com/blog/ai-design-tool-that-doesnt-look-ai-generated) | Cada elemento precisa de motivo | Coincide com a reprovação dos objetos soltos |
| 16 | Faixas de pincel, ícones em círculo, divisores, caixas, chamadas iguais em qualquer peça | [Venngage](https://venngage.com/blog/ai-slop-in-design/) | [Buscar referência fora do setor: capas de revista, cartaz de museu, embalagem, disco](https://venngage.com/blog/ai-slop-in-design/) | Pesquisar fora de "advocacia" é a dica mais útil |
| 17 | Polido, mas não comunica nada | [Venngage](https://venngage.com/blog/ai-slop-in-design/) | [Objetivo, público e mensagem únicos, em uma linha](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md) | Roteiro antes da arte já cobre |
| 18 | Tipografia quase certa: pesos e símbolos variam | [Venngage](https://venngage.com/blog/ai-slop-in-design/) | Ajuste real de peso e espaçamento | Conferir "%", "§" e acentos em lote |
| 19 | Sem nenhuma direção de estilo | [Mika Reyes](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md) | Nomear o estilo com precisão | Para isso serve este glossário |
| 20 | Inter em título, tamanhos padrão | [UX Skill](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) | Título em face editorial | Coberto: Inter só em texto |
| 21 | Título grande sem aperto de letras | [UX Skill](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) | Tracking em torno de -0,03em acima de 48 px | Testar em EB Garamond, conferir acentos |
| 22 | Linhas longas no título principal | [UX Skill](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) | 30 a 45 caracteres | [Regra atual: 20 a 26](PROCESSO_PRODUCAO_CARROSSEL.md), mais estrita |
| 23 | Emoji antes de cada item | [Brain Detox](https://braindetox.kr/en/posts/ai_design_tell_detection.html), [UX Skill](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) | Remover ou trocar por ícone | **Conflito**: o manual pede "até 5 itens com emoji-ícone" na legenda. Só observação |
| 24 | Frases paralelas, ritmo igual, números redondos inventados | [Brain Detox](https://braindetox.kr/en/posts/ai_design_tell_detection.html), [UX Skill](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design) | Frases variadas, substantivo concreto, número medido | Manual e skill `voz-leticia` já cobrem |
| 25 | Pele lisa e cerosa, sem poros | [Krumzi](https://www.krumzi.com/blog/is-this-image-ai-generated), [Morphic](https://morphic.com/resources/how-to/fix-ai-generated-skin-realistic) (t) | Foto real sem retoque | Coberto pela regra de imagem da Dra. |
| 26 | Falta de microdetalhe em tecido, madeira, metal | [resumo de busca, UpSampler](https://upsampler.com/blog/make-ai-images-look-real) (t) | Foto de alta resolução, com riscos reais | Ao curar Pexels, olhar a 100% |
| 27 | Geometria impossível, reflexo ou sombra que não batem com a luz | [Krumzi](https://www.krumzi.com/blog/is-this-image-ai-generated) | [Mesma direção de luz em todas as sombras](https://www.joshwcomeau.com/css/designing-shadows/) | Conferir em toda sombra acrescentada |
| 28 | Peça serve para qualquer um | [Kognie, teste de troca de logo](https://kognie.com/blog/ai-design-tool-that-doesnt-look-ai-generated) | Elemento próprio: Oxford rule, §, citação da lei, foto real | Aplicar como última conferência |

**Discussões do Reddit:** não abri nenhuma (seção 6). Um resumo de busca mencionava um fio sobre "vale da estranheza" em tipografia, mas não localizei a origem, por isso não uso como evidência.

**Três armadilhas (inferência):**

- Colocar grão em tudo também virou padrão. [Designers buscam grão e fibra como reação ao polimento](https://elements.envato.com/learn/envato-unpacked) (t). Se todo perfil fizer igual, deixa de distinguir. O que distingue é material real escaneado e foto real.
- "Imperfeito" não é "descuidado". A marca é sóbria: a imperfeição fica em textura e traço, nunca em texto torto, sombra errada ou recorte ruim.
- A etiqueta "premium" vem de tirar coisas. [AI gera mais; design bom decide o que remover](https://mikareyes.com/ai/how-to-spot-ai-made-graphic-design-and-posters.md).

## 4. Aplicação à marca

### Regras que limitam tudo abaixo

- **OAB primeiro.** O [art. 3º do Provimento 205/2021](https://www.oabgo.org.br/arquivos/downloads/provimento-205-1351880.pdf) pede caráter informativo, discrição e sobriedade; o §1º veda ostentação e promoção pessoal. O art. 5º §2º permite logomarca, imagens e fotos, e veda símbolos oficiais da OAB. O art. 6º, parágrafo único, veda ostentação de bens. O provimento não fala de recursos gráficos: **o enquadramento abaixo é inferência minha, não parecer jurídico.**
- **Leitura prática (inferência):** o efeito pode ser elaborado; o que não pode é parecer exaltação. Figura enorme com palavra em volta, halo e efeitos de "poder" chegam perto de promoção pessoal.
- Paleta `#231E1A`/`#1E1814`, `#C9A962`, `#E8DED1`. EB Garamond + Inter. Nunca Cormorant. Nada abaixo de 22 px. Faixas douradas no topo e no rodapé sempre. Até 5 hashtags.
- Texto dourado em fundo claro: proibido. Em areia, destaque em café itálico com sublinhado dourado.
- Imagem da Dra.: sem filtro, sem grão e sem cor mexida no rosto. Tudo que tem "só em banco" abaixo vale para isso.
- Fotos reais, sem marca de terceiros, sem texto em inglês.
- **Reprovações que continuam valendo:** recorte automático; vários objetos juntos; objeto solto sem relação com o tema; [arco](PASSAGEM_DE_CONTEXTO.md); selo no canto ou no meio; "fotos cortadas" sem intenção; [a Letícia na capa do carrossel Ouro editorial](PASSAGEM_DE_CONTEXTO.md).

### Contradições que encontrei nos documentos (precisam de decisão)

1. **Fonte de título:** o manual (seção 4) fala em Playfair Display; a passagem diz EB Garamond. O item 10 do processo (Pergunta v6) ainda cita Cormorant. Aqui uso EB Garamond.
2. **Recorte:** a direção v4 do processo descreve rembg, mas a regra de 09/10, posterior, proíbe. Prevalece a regra.
3. **Arcos:** a direção v4 cita "linhas e arcos que atravessam"; a passagem registra que ela reprovou o arco em 10/10. Prevalece a reprovação.
4. **IA:** o manual aceita retratos dela feitos com IA, liberados em 09/10; o processo diz "nunca". Esta pesquisa considerou só fotos reais; a decisão continua em aberto.
5. **Formato:** o manual fala em 1080x1440, e a passagem em 1080x1350. Fora dos documentos, [um blog do setor diz que peça de 1440 px de altura não pode ser impulsionada](https://www.tryordinal.com/blog/instagram-post-size). Não confirmei com a Meta. Vale checar se a peça for para mídia paga.
6. **Grão:** o processo pede acabamento com granulação; a regra da imagem veta no rosto. Resolvido na camada: grão abaixo da pessoa (4.6).

Nada do Projeto Viraliza (proposta de 04/11/2026, ainda sem aprovação) está considerado aqui: véu e proporção de slides claros seguem como no manual.

### 4.1 Texto atrás do sujeito: **Cuidado**, depende de aprovação

**Por que combina (inferência):** dá profundidade sem efeito novo e deixa a foto ser a protagonista. É o recurso que a Jessica nomeou no pedido.

**Situação da regra:** o [processo](PROCESSO_PRODUCAO_CARROSSEL.md) diz que recorte automático (rembg) não entra em peça publicada e que "se uma peça exigir recorte perfeito, avisar a Letícia antes". Esta técnica exige máscara, logo **muda a prática atual e depende de aprovação**. Este documento não revoga nada.

**Exigência de qualidade proposta (inferência, para ela aprovar):**

| Item | Exigência |
| --- | --- |
| Ordem de teste | 1º objeto de borda dura (cadeira, maleta, ampulheta, livro). 2º pessoa de banco com cabelo preso. 3º a Dra., só em foto planejada |
| Origem da máscara | **Manual**: [caneta ou laço poligonal para precisão](https://photoshoproadmap.com/photoshop-tutorial-how-to-place-text-behind-an-object-in-a-photo). Cabelo: [Select and Mask do Photoshop](https://helpx.adobe.com/ph_fil/photoshop/how-to/select-mask-hair.html) (t), [com Shift Edge para reduzir franja](https://helpx.adobe.com/ph_fil/photoshop/how-to/fine-tune-layer-masks.html) (t) |
| Ferramenta automática | Só como rascunho a retocar. [BiRefNet leva vantagem sobre rembg em cabelo em alguns testes](https://dev.to/om_prakash_3311f8a4576605/birefnet-vs-rembg-vs-u2net-which-background-removal-model-actually-works-in-production-d2f) (t), e o [fluxo BiRefNet + trimap + ViTMatte](https://ice-ice-bear.github.io/posts/2026-04-13-matting-libraries) é o recomendado num levantamento. São relatos individuais. Não achei comparação com recorte manual. Apps de Canva como [Text Layer](https://www.canva.com/apps/AAGTWQQRb54/text-layer) (t) recortam sozinhos: mesmo risco do rembg |
| Fundo da foto | Liso, contrastando com o sujeito; sem sombra caindo no fundo perto da borda |
| Resolução | Foto com 2160 px ou mais de largura para o render em 2x, como já é feito |
| Onde a letra passa | Só atrás de ombro, braço, tronco ou objeto. **Nunca atrás de cabelo solto** na primeira fase |
| Quanto cobre | Até 20 ou 25% de uma ou duas letras. A palavra precisa ler em [dois segundos](https://guide.pinterest.com/design/new-creative-deformation/) |
| Aprovação da máscara | A 200%, sobre café, areia e dourado: sem halo, sem serrilha, sem resto de sombra |
| Acentos | Conferir: acento escondido muda a palavra ("sobrevivência") |
| Faixas | Por cima de todas as camadas; o sujeito nunca as cobre |
| Sombra | [Ler a luz da foto, usar cor tirada dela, e combinar contato e ambiente](https://photoshoproadmap.com/add-text-behind-a-subject-with-realistic-shadows-in-photoshop): a sombra do sujeito cai sobre o texto |

```html
<div class="peca"><!-- position:relative; isolation:isolate; 1080x1440 -->
  <img class="c" src="{{foto_data_uri}}">             <!-- foto inteira -->
  <div class="grao"></div>                            <!-- só no fundo -->
  <h1 class="titulo">Prazo</h1>                       <!-- EB Garamond 280 px -->
  <img class="c" src="{{mascara_data_uri}}"
       style="filter:drop-shadow(0 12px 24px rgb(30 24 20 / .45))">
  <!-- mesma foto, mesmo enquadramento, só o sujeito -->
  <div class="faixas"></div>                          <!-- sempre por último -->
</div>
```

**Atenção técnica:** o [`mask-image` trata imagem `file://` como transparente](https://developer.mozilla.org/en-US/docs/Web/CSS/mask-image). O render atual usa `set_content` e base64 (`render_criativo.py`), o que deve evitar isso, mas testar (inferência).

### 4.2 Foto ponte entre slides: **Direto**

É o padrão atual: [foto real que atravessa do slide 3 para o 4, sem moldura, dissolvendo no fundo](PASSAGEM_DE_CONTEXTO.md). Nome para buscar: seamless carousel. Regra externa: [rosto, logo e palavra importante longe da emenda; a mesma proporção em todos os slides](https://www.krumzi.com/blog/seamless-instagram-carousel). Não confundir com "grid em mosaico", que o manual proíbe.

### 4.3 Sombra de verdade: **Direto**

**Por que:** [sombra é o que mais define se algo parece real](https://incomixofficial.blogspot.com/2026/05/psychology-of-presentation-lighting-angles-mockups.html) (t). As [regras de Josh Comeau](https://www.joshwcomeau.com/css/designing-shadows/): uma só direção de luz, várias camadas, sombra na cor do fundo.

```css
.cartao { box-shadow:
  0 1px 2px  rgb(30 24 20 / .40),   /* contato */
  0 4px 8px  rgb(30 24 20 / .30),
  0 16px 32px rgb(30 24 20 / .25);  /* ambiente */ }
.objeto { filter: drop-shadow(0 18px 22px rgb(30 24 20 / .5)); } /* segue a forma do PNG */
```

Só no que flutua: [cartão, sim; todo bloco, não](https://braindetox.kr/en/posts/ai_design_tell_detection.html).

### 4.4 Sombra de janela (gobo) e luz real: **Direto**

**Por que:** cria luz com direção, o oposto do brilho dourado uniforme. [Overlays vendidos para multiply e overlay](https://stock.adobe.com/images/tree-branches-shadows-gobo-effect-on-a-transparent-background-4k-uhd-1-1-ratio-square-realistic-shadows-for-multiply-blend-mode-for-mockups-light-casting-on-a-surface-30-opacity-pure-black/1230420430) (t) existem, mas o melhor é fotografar a sombra real da janela do escritório numa parede clara (inferência). Conferir licença e se a imagem de banco não é gerada por IA.

```css
.gobo { position:absolute; inset:0; background:url(...) center/cover;
        mix-blend-mode:multiply; opacity:.35; pointer-events:none; }
```

Sobre foto da Dra., só no fundo, nunca no rosto. Slide claro de areia é o melhor uso.

### 4.5 Fios de revista: Oxford rule, chapéu, paginação: **Direto**

**Por que:** o [fio Oxford vem do livro de 1499 e da imprensa, e é a borda da Rolling Stone](https://www.printmag.com/design-culture/how-the-oxford-rule-led-to-rolling-stone/). Dá autoridade sem ostentar. Respeita as faixas: o fio fica dentro, como cabeçalho.

```css
.oxford { border-top: 6px solid #C9A962; padding-top: 6px; }
.oxford::before { content:""; display:block; border-top: 2px solid #C9A962; }
```

Sistema completo (inferência): chapéu Inter, título EB Garamond, linha fina itálica, corpo Inter, nota de rodapé com o artigo da lei, paginador. Cantoneiras só onde já aprovadas.

### 4.6 Papel e grão no lugar certo: **Direto**

**Por que:** é [a direção v4](PROCESSO_PRODUCAO_CARROSSEL.md) aprovada para slide claro. Preferir scan real de papel a papel gerado (inferência): [quem compra premium quer ver fibra e dobra](https://creatsy.com/blog/1924095317-stationery-mockup-guide-how-to-present-envelopes-notebooks-stickers-desk-sets) (t).

```css
.papel { background:#E8DED1; }
.papel::after { content:""; position:absolute; inset:0;
  background:url(papel-scan.jpg) center/cover;
  mix-blend-mode:multiply; opacity:.5; }
/* grão via SVG, antes da camada da pessoa */
.grao { position:absolute; inset:0; opacity:.08; mix-blend-mode:overlay;
  background:url("data:image/svg+xml,..."); } /* feTurbulence fractalNoise, baseFrequency .65, stitchTiles */
```

Fonte do filtro: [CSS-Tricks](https://css-tricks.com/grainy-gradients/). Foto da Dra. sem recorte: excluir o rosto com `mask-image: radial-gradient(...)`. Com camadas, basta o grão ficar abaixo do recorte. O grão precisa ser pequeno: no celular, o olho vê textura, não sujeira.

### 4.7 Contraste de escala e texto fantasma: **Direto**

**Por que:** é rápido de reconhecer e [as referências dela usam](PROCESSO_PRODUCAO_CARROSSEL.md). Até [3 tamanhos, 2 grandes](https://www.nngroup.com/articles/principles-visual-design/) (t).

```css
.fantasma { position:absolute; right:-40px; top:180px;
  font:400 620px/1 "EB Garamond"; color:#C9A962; opacity:.10;
  font-variant-numeric: lining-nums; z-index:0; }
```

Decorativo: a informação não pode depender dele. Pode ser número do artigo, sinal § ou número do slide. Se for cortar, que seja só a parte decorativa; nada crítico fora da faixa central.

### 4.8 Dourado: fio e letra, sem brilho: **Cuidado**

**Por que tem cuidado:** [dourado 3D com brilho é o exemplo clássico do que evitar](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md), e ela já pediu ["medalha gravada, sem brilho de moeda"](PROCESSO_PRODUCAO_CARROSSEL.md). O padrão "ouro metalizado" da capa segue aprovado. Sugestão para testar, com pedido:

```css
.foil { color:#C9A962; }                       /* chapado: padrão mais seguro */
.foil-textura { background:url(folha-scan.jpg) center/cover;
  -webkit-background-clip:text; background-clip:text; color:transparent; }
```

Sem `text-shadow`: [sombra em texto transparente estraga o recorte](https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip). Conferir 7,3:1 sobre o café, sempre com fundo de reserva. A textura precisa ter pouca variação de claro e escuro.

### 4.9 Foto dentro da palavra: **Direto** (com objeto ou textura)

Masked type: serve em "Frase" ou capa de série, com foto de papel, couro, madeira, em fundo café. [`background-clip:text`](https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip). Letra pesada, 200 px ou mais. Nunca o rosto da Dra. dentro da letra. Conferir contraste.

### 4.10 Selo e texto em caminho: **Direto** em selo; **Cuidado** fora

```html
<svg viewBox="0 0 400 400"><path id="c" fill="none"
  d="M200 40a160 160 0 1 1 -.1 0"/><text font-family="Inter" font-size="26" fill="#C9A962">
  <textPath href="#c">LETÍCIA BARROS · ADVOCACIA · OAB/ES 39.948 ·</textPath></text></svg>
```

[`textPath`, MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath). Calcular o tamanho pelo render final: nada abaixo de 22 px. Guilhochê como fundo do selo pode dar o ar de documento sem brilho. Linha ou texto em volta da pessoa: é parente do arco reprovado, testar só com pedido.

### 4.11 Marcas humanas: marca-texto, sublinhado, nota: **Direto**

**Por que:** [traços desenhados à mão compensam o polimento](https://learn.g2.com/graphic-design-trends). Marca-texto já é aprovado.

```css
.marca { background:linear-gradient(transparent 58%, #C9A962 58% 92%, transparent 92%);
         color:#231E1A; }
```

Regra (inferência): desenhar à mão 6 a 10 traços SVG diferentes e fazer rodízio. Traço único repetido volta a ser padrão. Um destaque por peça.

### 4.12 Capitular, olho, versalete e nota de rodapé: **Direto**

```css
.corpo::first-letter { font:500 120px/.85 "EB Garamond"; float:left; margin:8px 12px 0 0; color:#C9A962; }
.versalete { font-variant-caps:small-caps; font-size:30px; letter-spacing:.06em; }
.titulo { font-variant-numeric:lining-nums; font-variant-ligatures:common-ligatures discretionary-ligatures;
          letter-spacing:-.02em; }
```

[Preferir `font-variant` a `font-feature-settings`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings). A [EB Garamond tem versalete e swash no pacote completo](https://tug.ctan.org/fonts/ebgaramond/README) (t), mas a versão em uso precisa ser testada: se faltar, o navegador cria versalete falso, e isso é pior que nada (inferência). Em café sobre areia, a capitular fica café, não dourada.

### 4.13 Duotone e gradação em foto de banco: **Direto**, só banco

Dá unidade ao banco Pexels. Sombras em café, altas luzes em areia (`mix-blend-mode` ou gradient map prévio em Pillow/OpenCV). Nunca na Dra. Em foto de pessoa, duotone apaga o tom de pele e enfraquece a identificação que a [regra de representatividade](PASSAGEM_DE_CONTEXTO.md) busca (inferência). Na dúvida, aplicar só a objeto.

### 4.14 Slide de dado e prazo: **Direto**

Número grande em EB Garamond, rótulo direto no dado e fonte legal em nota. Só dado de fonte primária, sem valor de causa, sem resultado.

### Classificação rápida

| Direto | Cuidado | Evitar nesta marca |
| --- | --- | --- |
| Sombra de contato e em camadas, gobo no fundo, Oxford rule, fios, chapéu e paginação, papel real, grão abaixo da pessoa, contraste de escala, texto fantasma, número grande, capitular, olho, versalete real, marca-texto, sublinhado à mão, nota de rodapé, §, fleuron, selo com guilhochê, foto ponte, duotone em banco, masked type com textura, chiaroscuro real, rim light real | Texto atrás de objeto ou pessoa, pop-out, entrelaçamento, fita e linhas envolventes, foto em forma, vidro fosco fora das séries, foil com textura, Art Deco de detalhe, letra cortada, assimetria em peça única, colagem, papel rasgado, selo de cera, carimbo, nota manuscrita | Neon, swirl, lens flare, bloom, glow, long shadow, neumorfismo, cromo, 3D genérico, dispersão, dupla exposição na Dra., retrato em retícula na Dra., mármore, risografia, RGB split, scanline, mesh gradient, sticker, scrapbook, Y2K, neobrutalismo, maximalismo, anti-design, tipo deformado |

## 5. Onde pesquisar referência

**Regra de busca (com base em [Venngage](https://venngage.com/blog/ai-slop-in-design/)):** procurar fora do setor jurídico. As hashtags abaixo são para pesquisar, não para colocar em legenda (o limite de 5 continua).

### YouTube

Canais confirmados por consulta ao oEmbed do YouTube. Não assisti aos vídeos; a qualidade é desconhecida.

| Assunto | Termos | Vídeos e canais encontrados |
| --- | --- | --- |
| Texto atrás, Photoshop | text behind subject, text behind person | [Kim de Been, com contorno](https://www.youtube.com/watch?v=49JsIVh2Cfw); [Kim de Been, esmaecido](https://www.youtube.com/watch?v=uByS5nrxfiw); [Creativity With Pixel](https://www.youtube.com/watch?v=FZ60Acmoqoc) |
| Texto atrás, Canva | text behind image canva | [Art Design with Canva](https://www.youtube.com/watch?v=tZ89_43WK18); [Gravenberg Tutorials](https://www.youtube.com/watch?v=ptN_UcIMipM); [Grow With Rachel](https://www.youtube.com/watch?v=kkz09akbiZg) |
| Texto contornando | wrap text around subject | [PiXimperfect](https://www.youtube.com/watch?v=fCFEDVMw9q4); [Kim de Been](https://www.youtube.com/watch?v=tXAP9kkrHcg); [Brendan Williams](https://www.youtube.com/watch?v=5L307t7scSo); [Blue Lightning](https://www.youtube.com/watch?v=L3e1ZqIB31Y); [Motion Mation](https://www.youtube.com/watch?v=6vEACYQJUwM); [Guided Resolution](https://www.youtube.com/watch?v=wY-wXGkiOwY) |
| Fita, swirl, rastro | ribbon of light, light swirl, light trails | [Blue Lightning](https://www.youtube.com/watch?v=tJUpAz4aQJs); [A.J. Wood](https://www.youtube.com/watch?v=CRj7Ak2OxuE); [NitroLandTutorials](https://www.youtube.com/watch?v=WRaHcwql6Ng); [Sleeklens](https://www.youtube.com/watch?v=pbpdJDbsBws) |
| Dupla exposição, dispersão | double exposure, dispersion effect | [tutvid](https://www.youtube.com/watch?v=HYVDlajEZOI); [Katty Ros](https://www.youtube.com/watch?v=Dz31tzl_U-4); [Webflippy](https://www.youtube.com/watch?v=VRREbCo83b0); [Doodle Royalty](https://www.youtube.com/watch?v=EjkUZE84VWg); [Gokce Design](https://www.youtube.com/watch?v=rWMhQaslA-0); [Always Creating](https://www.youtube.com/watch?v=EVHn1JL_Hn4) |
| Carrossel contínuo | seamless carousel | [Design Xstream, Figma](https://www.youtube.com/watch?v=QTh3k_YiNow); [Created by Wayne](https://www.youtube.com/watch?v=OsdvkR51jCg); [Social Media with Josie](https://www.youtube.com/watch?v=UU-N_8wRGr8); [J Stewart's Laboratory](https://www.youtube.com/watch?v=Ad0UYGKGIH4); [Repixo](https://www.youtube.com/watch?v=YjPoFyoBr_g); [Laressa Ngoeun](https://www.youtube.com/watch?v=Caq6Jssjnro) |
| Fontes e carrossel | luxury fonts, carousel ideas | [Roger Coles](https://www.youtube.com/watch?v=Gr7Y0q50mkI); [SuminCreates](https://www.youtube.com/watch?v=O-IQ9Zio30w) |

Canais citados em listas (trecho de busca): [Spoon Graphics](https://blog.spoongraphics.co.uk/?p=9474), [PHLEARN](https://www.youtube.com/@phlearn), Photoshop Training Channel e [Envato Tuts+](https://design.tutsplus.com/articles/100-best-text-effect-tutorials--cms-28650). A busca não trouxe Yes I'm a Designer, Satori Graphics nem Will Paterson; não sei dizer se têm conteúdo útil aqui.

### Instagram

Páginas públicas de hashtag abertas em 04/11/2026. Cada uma mostrou cerca de 12 Reels. As contagens são as do cabeçalho naquele dia. Li só legenda e nome: não vi as peças nem avaliei o trabalho. Popular não significa bom.

| Hashtag (lida) | Contas que apareceram | Hashtags vizinhas |
| --- | --- | --- |
| [#editorialdesign](https://www.instagram.com/explore/tags/editorialdesign/) (cerca de 4,7 milhões) | studio_palme, zachex, kirsten.humpfer, rimatelier_, zita.fernandez, omeroron | #artdirection, #publicationdesign, #typeposter, #fvckingdesign, #youaretypography |
| [#typeposter](https://www.instagram.com/explore/tags/typeposter/) | estudiohusmee, _bradmead, joaquinlluis, tyl.markok, vosk.design, minimal.layout, papersarchive | #typographicposter, #swissposter, #collectgraphics, #printisntdead, #thedesignblacklist, #graphicindex |
| [#posterdesign](https://www.instagram.com/explore/tags/posterdesign/) (37 milhões) | rar3hare, waveindex, panter.vision (fotocópia), rkreate, studiorevv | #postereveryday, #minimalart, #japanesedesign |
| [#artdirection](https://www.instagram.com/explore/tags/artdirection/) | itsnicethat, domestika, studio.laboom, openbook.studio, sloestudios | #creativedirection, #moodboard |
| [#collagedesign](https://www.instagram.com/explore/tags/collagedesign/) | robdraper1 (letras em camadas), wiidoomedia, cutandplaced | #collageart, #scanography, #collageanimation |
| [#seamlesscarousel](https://www.instagram.com/explore/tags/seamlesscarousel/) | em.creates.content, creatlvblin, boundsocial.studio, alessacreative | #carouselpost, #crsel, #carouseltutorial |
| [#graphicdesigntrends](https://www.instagram.com/explore/tags/graphicdesigntrends/) | lorem.ipsum.designs, catalinafacentedesign (texturas), kobdesignuk, conti.creations, bau.artspace | #textureart, #DesignTrends2027, #MoodboardInspo |
| [#photoshoptutorial](https://www.instagram.com/explore/tags/photoshoptutorial/) (739 mil) | gfx.flexart (vidro, retícula), aartstock, dxretouching (dodge and burn) | #HalftoneEffect, #DodgeAndBurn |
| [#typography](https://www.instagram.com/explore/tags/typography/) (117 milhões) | Quase só Reels virais de motivação e CapCut | Pouco útil para a marca |
| [#advocacia](https://www.instagram.com/explore/tags/advocacia/) (39 milhões) | Advogados falando para a câmera | **Não usar como referência** visual nem de conduta: pelas legendas, parte não parece seguir o padrão do manual (inferência, sem análise caso a caso) |

Sem abrir (caiu na tela de login): [#textbehindsubject](https://www.instagram.com/explore/tags/textbehindsubject/), [#carouseldesign](https://www.instagram.com/explore/tags/carouseldesign/), [#typographyposter](https://www.instagram.com/explore/tags/typographyposter/), [#designjuridico](https://www.instagram.com/explore/tags/designjuridico/), [#lawfirmbranding](https://www.instagram.com/explore/tags/lawfirmbranding/). Pode valer abrir logada. Ferramentas e perfis de carrossel vistos em busca: [@panoramaker.app](https://www.instagram.com/panoramaker.app/), [@panosliceapp](https://www.instagram.com/panosliceapp/), [@oppenapp](https://www.instagram.com/oppenapp/).

### Pinterest

Só vi títulos e trechos. Termos de verdade que apareceram: **Text Behind Person, Text Behind Image, Typography Poster With Photo, Character Collage Poster, Bold Typography Poster Design, Typography Collage Graphic Design** ([página de ideias](https://www.pinterest.com/ideas/typography-portrait-ideas/918178766921/)). Outras páginas: [Poster Design with Text](https://www.pinterest.com/ideas/poster-design-with-text/900198791301/), [pasta Posters editorial](https://fr.pinterest.com/martinlavielle/posters-editorial/), [Magazine Layout](https://ie.pinterest.com/paulclarkin35/magazine-layout-text-based/), [guia de deformação](https://guide.pinterest.com/design/new-creative-deformation/) (a página abriu, sem editor identificado).

Termos sugeridos para testar (inferência): `editorial magazine layout serif`, `dark academia poster`, `quiet luxury editorial`, `oxford rule layout`, `window shadow editorial`, `book cover serif italic`, `law journal cover`.

### Behance, Dribbble, Awwwards, tipografia

- **Behance** (só por busca): [carousel design](https://www.behance.net/search/projects/carousel%20design), [law firm branding](https://www.behance.net/search/projects/law%20firm%20branding?locale=en_US), [lawyer firm social media](https://www.behance.net/search/projects/lawyer%20firm%20social%20media), [typographic poster](https://www.behance.net/search/projects/typographic%20poster?locale=en_US). Projetos: [Umut Akkan](https://www.behance.net/gallery/242915265/Experimental-typography-poster-work-7), [Antara Raman](https://www.behance.net/gallery/58228481/Typographic-Poem-Poster). Nicho jurídico brasileiro: [Fabiola Carmo](https://www.behance.net/fabiolacarmo), [Martineli Academy](https://www.behance.net/MartineliAcademy).
- **Dribbble** (só por busca): [editorial poster](https://dribbble.com/search/editorial-poster), [typographic portrait](https://dribbble.com/tags/typographic-portrait), [typography poster](https://dribbble.com/search/typography-poster), [Typography Collage Poster, Florian Delearde](https://dribbble.com/shots/25335558-Typography-Collage-Poster).
- **Awwwards**: [Typography-Heavy Web Design](https://www.awwwards.com/typography-heavy-design.html), [serifa com sem serifa](https://www.awwwards.com/inspiration/serif-and-sans-serif-typography-combination).
- **Fonts In Use e Typewolf**: [escritórios de advocacia](https://fontsinuse.com/tags/1763/lawyers-law-firms) (os casos vistos em trecho usam sem serifa, o que torna a serifa da marca um diferencial, inferência), [EB Garamond em uso](https://www.fontsinuse.com/typefaces/31479/eb-garamond), [Typewolf](https://www.typewolf.com/editorial-new).
- **Em português**: [Chief of Design, grid](https://chiefofdesign.com.br/en/grid-design/), [impacto com tipografia](https://chiefofdesign.com.br/en/5-formas-interessantes-de-causar-um-impacto-visual-atraves-da-tipografia/), [InfoDesign, capitulares](https://infodesign.emnuvens.com.br/infodesign/article/view/806), [Aurum, identidade para advogados](https://www.aurum.com.br/blog/?p=8519) (evitar balança e Themis, em linha com o manual).
- **Glossários**: [Fonts Knowledge, Google](https://fonts.google.com/knowledge/glossary), [Typography Guru](https://typography.guru/term/), [Fontology](https://www.fonts.com/content/learning/fontology/glossary/h), [Creative Bloq](https://www.creativebloq.com/design/fonts-typography/typography-glossary-an-a-z-of-type-terms).

## 6. O que consegui e não consegui ler

**Limite geral:** a ferramenta devolve o texto da página resumido, e a busca devolve títulos e trechos. Não vi nenhuma imagem nem vídeo. Citações são curtas e vieram desse resumo; antes de reproduzir alguma como frase exata, abrir a fonte.

| Rede ou site | Situação |
| --- | --- |
| **YouTube** | Busca e títulos. Canal confirmado pelo oEmbed em 38 de 39 vídeos consultados (1 não respondeu). Página do vídeo abre sem descrição. **Não assisti e não tenho transcrição.** A skill `watch` poderia fazer isso depois |
| **Instagram** | 10 de 15 páginas de hashtag abriram com legendas e nomes; 5 caíram em login, sem padrão claro. **Sem ver as imagens.** Perfis individuais não foram abertos, só listados em busca |
| **Pinterest** | **Só trecho de busca.** Páginas de ideias e pastas vieram vazias. Exceção: o guia em `guide.pinterest.com` |
| **Reddit** | **Bloqueado** na busca filtrada e na leitura direta. Nada lido |
| **Behance** | Busca filtrada funcionou; leitura direta 403. **Só trecho** |
| **Dribbble** | Busca filtrada funcionou; a leitura veio vazia. **Só trecho** |
| **Awwwards** | Uma página lida (de cerca de 2020), resto por trecho |
| **Adobe** | Páginas de ajuda bloquearam (403): **Photoshop, Illustrator, Lightroom e InDesign só por trecho**. Página de tendências do Express lida |
| **Canva** | Páginas bloquearam (403). Só trecho. Relatório 2026 lido em cobertura de imprensa, não no original |
| **MDN** | Lido: mix-blend-mode, mask-image, background-clip, textPath, drop-shadow, shape-outside, font-feature-settings, clip-path, backdrop-filter, text-stroke |
| **Creative Bloq, Google Fonts, Freepik, Business Wire** | Abriram sem corpo ou bloquearam. Só título e trecho |
| **It's Nice That, Fonts In Use, Typewolf, Chief of Design** | Trecho; Chief of Design: grid lido |
| **Designerd, Print Mag** | Designerd não apareceu. Print: artigo do Oxford rule lido |
| **Shutterstock, Freepik (2026)** | Não achei relatório oficial de 2026. Só relatórios antigos |
| **Provimento 205/2021** | **Lido na íntegra** em PDF da OAB/GO, com anexo |
| **Documentos internos** | Lidos: manual, processo; passagem nas seções visuais; contexto por busca |

**Lacunas conhecidas:**

- Nenhum artigo definitivo sobre fita, órbita, arame, fio ou "typographic halo": os nomes são de uso, mas a busca trouxe pouco. Trate esses nomes como aproximados.
- Nenhuma comparação direta entre recorte manual, Photoshop e modelos de IA.
- A OAB não trata de efeito gráfico: não há base direta para dizer que um efeito é proibido.
- Não confirmei quais recursos OpenType a EB Garamond em uso tem.
- Não vi exemplos de advocacia premium: as buscas no nicho trouxeram quase só pedidos de freelancer.

## 7. Fontes

As marcadas com (t) só foram vistas em trecho de busca.

**Oficiais e técnicas**

- MDN: [mix-blend-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode), [mask-image](https://developer.mozilla.org/en-US/docs/Web/CSS/mask-image), [background-clip](https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip), [textPath](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath), [drop-shadow](https://developer.mozilla.org/en-US/docs/Web/CSS/filter-function/drop-shadow), [shape-outside](https://developer.mozilla.org/en-US/docs/Web/CSS/shape-outside), [font-feature-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/font-feature-settings), [clip-path](https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path), [backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter), [text-stroke](https://developer.mozilla.org/en-US/docs/Web/CSS/-webkit-text-stroke)
- Adobe (t): [modos de mesclagem](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html), [Julieanne Kost](https://blogs.adobe.com/jkost/2018/08/working-with-blend-modes-in-photoshop-cc.html), [dodge e burn](https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html), [grão](https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/enhance-texture-with-grain.html), [split toning](https://helpx.adobe.com/ph_fil/lightroom-classic/how-to/stylize-photo-with-split-toning.html), [color grading](https://blog.adobe.com/en/publish/2020/10/20/introducing-color-grading), [chiaroscuro](https://www.adobe.com/creativecloud/video/discover/low-key-vs-high-key-lighting.html), [vinheta](https://www.adobe.com/uk/creativecloud/photography/discover/what-is-vignette-in-photography), [máscara](https://helpx.adobe.com/si/photoshop/how-to/make-selection-layer-mask.html), [ajustar máscara](https://helpx.adobe.com/ph_fil/photoshop/how-to/fine-tune-layer-masks.html), [cabelo](https://helpx.adobe.com/ph_fil/photoshop/how-to/select-mask-hair.html), [Intertwine](https://helpx.adobe.com/illustrator/desktop/manage-objects/reshape-transform-objects/create-intertwined-objects.html), [marcas de impressão](https://helpx.adobe.com/indesign/using/printers-marks-bleeds.html), [sangria](https://helpx.adobe.com/indesign/desktop/print/page-set-up-and-printer-marks/print-bleed-and-slug-areas.html), [olho](https://helpx.adobe.com/sk/indesign/how-to/make-pull-quote-callout.html)
- [Adobe Express, tendências 2026](https://www.adobe.com/express/learn/blog/design-trends-2026)
- Canva (t): [texto atrás de imagem](https://www.canva.com/features/add-text-behind-image/), [app Text Layer](https://www.canva.com/apps/AAGTWQQRb54/text-layer)
- Google Fonts (t): [glossário](https://fonts.google.com/knowledge/glossary), [tracking](https://fonts.google.com/knowledge/glossary/tracking_letter_spacing), [glifos alternativos](https://fonts.google.com/knowledge/introducing_type/introducing_alternate_glyphs), [numerais](https://fonts.google.com/knowledge/introducing_type/understanding_numerals), [tamanhos ópticos](https://fonts.google.com/knowledge/choosing_type/choosing_typefaces_that_have_optical_sizes)
- [Provimento 205/2021, OAB/GO](https://www.oabgo.org.br/arquivos/downloads/provimento-205-1351880.pdf). [EB Garamond, README CTAN](https://tug.ctan.org/fonts/ebgaramond/README) (t)
- NN/g: [glassmorphism](https://www.nngroup.com/articles/glassmorphism/), [neobrutalismo](https://www.nngroup.com/articles/neobrutalism/), [hierarquia](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/) (t), [princípios](https://www.nngroup.com/articles/principles-visual-design/) (t), [padrão F](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) (t)

**Design e tutoriais**

- [Print Mag, Oxford rule](https://www.printmag.com/design-culture/how-the-oxford-rule-led-to-rolling-stone/); [Josh Comeau, sombras](https://www.joshwcomeau.com/css/designing-shadows/); [CSS-Tricks, grão](https://css-tricks.com/grainy-gradients/); [Tuts+, vidro canelado](https://design.tutsplus.com/tutorials/how-to-create-a-reeded-glass-photo-effect-in-photoshop--cms-109005); [Photoshop Roadmap, texto atrás](https://photoshoproadmap.com/photoshop-tutorial-how-to-place-text-behind-an-object-in-a-photo); [Photoshop Roadmap, sombras](https://photoshoproadmap.com/add-text-behind-a-subject-with-realistic-shadows-in-photoshop); [Krumzi, carrossel contínuo](https://www.krumzi.com/blog/seamless-instagram-carousel); [Chief of Design, grid](https://chiefofdesign.com.br/en/grid-design/); [Aurum](https://www.aurum.com.br/blog/?p=8519); [Made Good Designs, estilos](https://madegooddesigns.com/graphic-design-styles/); [matting](https://ice-ice-bear.github.io/posts/2026-04-13-matting-libraries); [Awwwards](https://www.awwwards.com/typography-heavy-design.html); [Ordinal, tamanhos](https://www.tryordinal.com/blog/instagram-post-size)
- (t): [CreativePro](https://creativepro.com/creating-out-of-bounds-effect-photoshop/), [PhotoshopCafe](https://photoshopcafe.com/?p=20744), [Corel](https://learn.corel.com/tutorials/create-an-out-of-bounds-photo/), [Photoshop Roadmap, deslocamento](https://www.photoshoproadmap.com/how-to-create-a-text-and-photo-poster-with-displacement-effects-in-photoshop/), [Planet Photoshop](https://planetphotoshop.com/using-photoshop-to-create-digital-gobos.html), [PetaPixel](https://petapixel.com/2024/01/03/v-flat-worlds-new-shadow-boards-mimic-sunlight-through-windows), [StudioBinder, rim light](https://www.studiobinder.com/blog/what-is-a-rim-light-photography-definition/), [StudioBinder, light leak](https://www.studiobinder.com/blog/light-leak-overlay-download/), [The Complete Manual of Typography](https://www.oreilly.com/library/view/the-complete-manual/9780132821926/chapter-45.html), [TypeDrawers](https://typedrawers.com/discussion/comment/61959), [PrintWiki](https://printwiki.org/Rule_Line), [Keyline](https://en.wikipedia.org/wiki/Keyline), [Fleuron](https://wikiwand.com/en/Fleuron_(typography)), [FontLab, guilhochê](https://blog.fontlab.com/2026/04/14/money-lace-guilloche-intaglio-spirograph/), [Regula](https://regulaforensics.com/glossary/banknotes/guilloches/), [Creative Bloq, glossário](https://www.creativebloq.com/design/fonts-typography/typography-glossary-an-a-z-of-type-terms), [Creative Bloq, máscara de tipo](https://www.creativebloq.com/computer-arts/masking-type-10079462), [Creative Bloq, anti-design](https://www.creativebloq.com/design/graphic-design/what-is-anti-design-the-trend-that-tears-up-the-rule-book), [Made Good Designs, emboss](https://madegooddesigns.com/emboss-vs-deboss/), [spot UV e foil](https://madegooddesigns.com/spot-uv-vs-foil/), [Mediabistro](https://www.mediabistro.com/go-freelance/business-basics/tk-mb-media-glossary/), [Fine Print School](https://www.fineprintschool.com/glossary-of-printing-terms/pull-quote), [Shutterstock, riso](https://www.shutterstock.com/blog/photoshop-tutorial-mimic-risograph-effect), [Design Shack, riso](https://designshack.net/articles/inspiration/risograph-style-backgrounds), [Design Shack, termos](https://designshack.net/articles/typography/typography-terms-what-they-mean), [G2, duotone](https://learn.g2.com/duotone-effect), [Prototypr, duotone](https://blog.prototypr.io/duotone-in-web-design-875d8e90da4b), [Go Media, papel](https://gomedia.com/tutorials/crumpled-paper-texture-freebie/), [Spoon Graphics, papel rasgado](https://blog.spoongraphics.co.uk/?p=11336), [plástico filme](https://we.graphics/item/plastic-wrap-overlay-textures), [Picsart, adesivo](https://picsart.com/blog/ootd-sticker-peeling-trend/), [Bwillcreative](https://bwillcreative.com/how-to-create-a-double-exposure-in-photoshop/), [PubMed, proporção áurea](https://pubmed.ncbi.nlm.nih.gov/38228978/), [IxDF](https://ixdf.org/literature/topics/visual-hierarchy), [Bento](https://banani.co/definitions/bento-grid), [Quiet luxury](https://en.wikipedia.org/wiki/Quiet_luxury), [Blend](https://www.blendnow.com/blog/quiet-luxury-aesthetic-the-complete-guide), [Creative Market, old money](https://creativemarket.com/blog/balmoral-heritage-old-money-aesthetics), [Dark academia](https://trends.daisyui.com/trend/dark-academia/), [Retrofuturismo](https://trends.daisyui.com/trend/retro-futurism/), [Long shadow](https://webdesignerdepot.com/flat-design-casts-a-long-shadow), [Lens flare](https://3d.irpr.agency/glossary/lens-flare/), [PC Gamer](https://www.pcgamer.com/six-terrible-graphical-effects-that-need-to-stop), [Aberração cromática](https://limeup.io/glossary/chromatic-aberration/), [Kinetic typography](https://en.wikipedia.org/wiki/Kinetic_typography), [Photomontage](https://en.wikipedia.org/wiki/Photomontage), [Neumorfismo](https://en.wikipedia.org/wiki/Neumorphism), [Tufte](https://www.edwardtufte.com/?p=445), [badge e pill](https://smart-interface-design-patterns.com/articles/badges-chips-tags-pills/), [W3C Open UI](https://www.w3.org/2021/03/04-openui-irc), [BiRefNet x rembg](https://dev.to/om_prakash_3311f8a4576605/birefnet-vs-rembg-vs-u2net-which-background-removal-model-actually-works-in-production-d2f), [mockup, Elistit](https://elistit-web.pages.dev/guides/how-to-make-realistic-etsy-mockups/), [mockup, Creatsy](https://creatsy.com/blog/1924095317-stationery-mockup-guide-how-to-present-envelopes-notebooks-stickers-desk-sets), [mockup, blog](https://incomixofficial.blogspot.com/2026/05/psychology-of-presentation-lighting-angles-mockups.html)

**Tendências**

- [Canva, via Mediainfoline](https://www.mediainfoline.com/brand/canva-unveils-2026-design-trends-the-year-of-imperfect-by-design); [Vistaprint](https://www.vistaprint.ca/hub/graphic-design-trends); [Envato, autores](https://author.envato.com/hub/graphic-design-trends-2026/); [Envato, página de tendências](https://elements.envato.com/lp/creative-trends-2026/); [G2](https://learn.g2.com/graphic-design-trends); [Pinterest, via PPC Land](https://ppc.land/pinterest-unveils-21-consumer-trends-for-2026-advertising-campaigns/) (t); [Campaign Brief](https://campaignbrief.com/?p=305692) (t); [Envato Unpacked](https://elements.envato.com/learn/envato-unpacked) (t); [Creative Bloq, tendências 2026, só o título](https://www.creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026)

**Cara de IA**

- [Mika Reyes, reconhecer](https://mikareyes.com/ai/how-to-spot-ai-made-graphic-design-and-posters.md); [Mika Reyes, corrigir](https://mikareyes.com/ai/how-to-fix-ai-looking-graphic-design-and-posters.md); [Venngage](https://venngage.com/blog/ai-slop-in-design/); [Krumzi](https://www.krumzi.com/blog/is-this-image-ai-generated); [Kognie](https://kognie.com/blog/ai-design-tool-that-doesnt-look-ai-generated); [Brain Detox](https://braindetox.kr/en/posts/ai_design_tell_detection.html); [UX Skill wiki](https://github.com/Laith0003/ux-skill/wiki/How-to-detect-AI-slop-in-your-design); [UpSampler](https://upsampler.com/blog/make-ai-images-look-real) (t); [Morphic](https://morphic.com/resources/how-to/fix-ai-generated-skin-realistic) (t)
- Bloqueados, não lidos: [uxdesign.cc](https://uxdesign.cc/how-to-de-slopify-your-designs-4c40c57c1dc9), [Creativepool](https://creativepool.com/bhiorns/articles/how-to-avoid-making-creative-work-that-looks-like-ai.35166), [UX Planet](https://uxplanet.org/how-to-spot-ai-generated-design-697aaabe76c8), [Towards AI](https://pub.towardsai.net/10-signs-of-ai-generated-design-and-how-to-make-yours-not-look-like-it-482ff7da81fc)

**Internas**

- `docs/MANUAL_CONTEUDO_REDES.md`, `docs/PROCESSO_PRODUCAO_CARROSSEL.md`, `docs/PASSAGEM_DE_CONTEXTO.md`, `apps/api/app/services/render_criativo.py`
