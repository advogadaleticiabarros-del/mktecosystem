# Estúdio de Criativos — Estilo Real (formatos "Pergunta" e "Segunda Jurídica")

**Data:** 2026-07-22
**Status:** Aprovado para implementação

## Contexto

O Estúdio de Criativos do Orbit hoje só renderiza `tipo="carrossel"` (5 slides, texto
dourado sobre fundo escuro sólido, sem foto). As peças `tipo="legenda"` (posts de
imagem única) são geradas como texto puro e **nunca ganham imagem** — não existe
nenhum render para elas em lugar nenhum do sistema hoje.

A usuária já publica, manualmente, dois formatos de imagem única no Instagram real
dela (@adv.leticiabarros2) que não existem no Orbit:

- **"Me faça uma pergunta"** — o formato mais usado dela, dezenas de exemplos na
  grade real.
- **"Segunda Jurídica"** — faixa vermelha "NOVA LEI" + manchete de impacto.

Analisando a grade completa do Instagram real dela (ver memória
`identidade-visual-instagram-real-leticia`), alguns elementos de marca se repetem em
quase todo post, independente do formato, e devem virar padrão em qualquer template
novo:

- Textura de **marca d'água diagonal** do selo dourado, tileada em baixa opacidade
  sobre o fundo.
- **Linha/moldura dourada** fina delimitando topo e/ou rodapé da composição.
- **Glow dourado sutil** ao redor de elementos-chave (borda da foto de perfil,
  painel de texto) — nunca forte, dá profundidade sem competir com o texto.
- Grading de cor consistente (dourado/preto/creme) aplicado **sobre a foto**, não só
  um escurecimento plano — fotos com cores originais diferentes saem com a mesma
  paleta de marca.

## Escopo

Dentro do escopo:
1. Banco de fotos próprio (gerado pela usuária no nano banana / Gemini Image),
   organizado por categoria de cena, reutilizável entre pautas.
2. Dois templates novos de render: `pergunta` e `segunda_juridica`, aplicados a
   `ContentPiece` de `tipo="legenda"`.
3. Campo novo `manchete` no prompt de geração da legenda (frase curta de impacto
   pra imagem, sem mudar o campo `texto` que já existe pra legenda do post).
4. Escolha manual do formato visual (Pergunta ou Segunda Jurídica) na tela de
   Aprovação/Criativos — não há tentativa de adivinhar automaticamente qual usar.
5. Estúdio de Criativos (frontend) passa a listar e renderizar `legenda` além de
   `carrossel`.
6. Execução de ponta a ponta assistida (gerar pauta → conteúdo → aprovar formato →
   inserir → agendar) como validação final, uma vez que o pipeline estiver pronto.

Fora de escopo (explicitamente, para não inflar):
- O estilo do `carrossel` continua como está — não mexe.
- Publicação automática no Instagram do novo formato de imagem única (hoje só
  `formato="carrossel"` publica sozinho via `instagram_publisher.py`) — abre como
  próximo passo natural depois que os templates existirem, mas não faz parte deste
  trabalho.
- Detecção automática de qual dos dois formatos usar por pauta — é escolha manual.

## Banco de fotos

**Categorias** (genéricas por cena, reutilizáveis em qualquer área do direito —
decisão explícita da usuária, não um banco por área jurídica):

1. `escritorio` — pessoa em ambiente de trabalho/escritório, documentos, atendimento
2. `familia` — família em casa, cotidiano doméstico
3. `trabalho-braçal` — trabalhadores em obra/indústria/serviço
4. `retrato-humano` — retratos de pessoas reais em contextos diversos (idoso,
   gestante, jovem trabalhador), tom introspectivo/reflexivo

4 fotos por categoria = 16 imagens no lote inicial. Ficam em
`apps/api/media/banco_fotos/<categoria>/foto-01.jpg` (a 04.jpg), formato retrato
(proporção próxima de 4:5 ou 3:4), mínimo 1080px de largura. O serviço de render
escolhe uma foto por peça dentro da categoria (round-robin por categoria, pra não
repetir sempre a mesma foto em sequência).

**Prompts para gerar no nano banana** (Gemini 2.5 Flash Image) — um por categoria,
gerar 4 variações de cada:

> **Categoria `escritorio`:**
> "Fotografia realista, luz natural suave, de uma mulher brasileira adulta em um
> escritório de advocacia moderno e acolhedor, folheando documentos ou atendendo um
> cliente. Expressão confiante e humana, não posada. Tons terrosos e dourados quentes
> no ambiente (madeira, luz dourada de fim de tarde). Enquadramento vertical (retrato),
> com espaço livre e mais escuro de um dos lados do quadro para sobrepor texto depois.
> Fotografia editorial, não corporativa fria — sem sorriso forçado de banco de
> imagens. Sem texto, sem logotipos, sem marca d'água na imagem."

> **Categoria `familia`:**
> "Fotografia realista, luz natural, de uma família brasileira em casa em um momento
> cotidiano genuíno (conversando à mesa, brincando com uma criança, organizando
> papéis em casa). Tons quentes e terrosos, ambiente simples e real, não um lar de
> revista. Enquadramento vertical (retrato), com uma área mais escura/neutra de um
> lado do quadro para permitir sobrepor texto. Fotografia documental humanizada, sem
> pose de banco de imagens genérico. Sem texto, sem logotipos, sem marca d'água."

> **Categoria `trabalho-braçal`:**
> "Fotografia realista, luz natural de ambiente externo ou de obra/indústria, de um
> trabalhador ou trabalhadora brasileiro em contexto de trabalho braçal (construção
> civil, entrega, serviço, indústria), em ação, com dignidade e sem estereótipo de
> pobreza. Tons terrosos e dourados na iluminação (fim de tarde/luz quente). Vertical
> (retrato), com espaço mais escuro de um lado do quadro para sobrepor texto depois.
> Sem texto, sem logotipos, sem marca d'água, sem capacete/uniforme com marca de
> empresa visível."

> **Categoria `retrato-humano`:**
> "Retrato fotográfico realista de uma pessoa brasileira comum (varie idade e
> contexto entre as gerações: pessoa idosa, gestante, jovem adulto), expressão
> pensativa e humana, não sorridente/posada. Luz natural suave e quente, fundo
> desfocado em tons terrosos/dourados. Enquadramento vertical (retrato), com espaço
> negativo mais escuro de um lado do quadro pra sobrepor texto depois. Fotografia
> editorial humanizada, não stock corporativo. Sem texto, sem logotipos, sem marca
> d'água."

Regra comum a todos: **vertical, tom terroso/dourado quente, espaço de respiro para
texto, sem texto/logo/marca d'água embutidos, sem pose de banco de imagens
genérico** — mesmas restrições já usadas pelo squad de referência
(`curador-imagens.md`), adaptadas pra geração em vez de busca.

## Templates de render

Seguem o padrão já estabelecido em `app/services/render_criativo.py` /
`app/templates/carrossel_slide.html` (Jinja2 + Playwright screenshot), mas cada um
como novo arquivo — não reescreve o carrossel existente.

**`app/templates/criativo_pergunta.html`** — zonas:
- Foto de fundo (uma das 16 do banco) preenchendo o quadro, com grading
  dourado/preto por cima (não escurecimento plano — overlay com `mix-blend-mode` na
  cor da marca, mantendo detalhe da foto visível).
- Textura de marca d'água diagonal do selo dourado sobre toda a composição.
- Linha dourada fina no topo.
- Balão de texto (retângulo arredondado creme/bege, com "cauda" triangular
  apontando pra foto de perfil) contendo a `manchete`.
- Cabeçalho do balão: círculo do avatar (usa a mesma inicial "LB" do `Avatar`
  já usado no app) + nome "Letícia Barros" + selo de verificado azul (ícone,
  visualmente idêntico ao badge de conta verificada do Instagram — é reconhecimento
  de padrão visual, não integração real com a API do Instagram).
- Glow dourado sutil ao redor do balão e do avatar.
- Selo circular dourado (o mesmo `LogoMark`) no rodapé.

**`app/templates/criativo_segunda_juridica.html`** — zonas:
- Foto de fundo com o mesmo grading dourado/preto.
- Textura de marca d'água diagonal.
- Faixa vermelha sólida no canto superior esquerdo com texto branco "NOVA LEI".
- Manchete (`manchete`) grande e de impacto sobre a foto, tipografia de destaque
  (`--font-display` do próprio sistema de fontes já usado no resto do Orbit).
- Linha dourada de moldura no rodapé + selo circular dourado.

**`app/services/render_criativo.py`** ganha duas novas funções, mesma assinatura
geral de `renderizar_slide` (Jinja2 render → Playwright screenshot → PNG):
- `renderizar_pergunta(manchete, foto_path, identidade_visual, caminho_saida, nome_conta=..., instagram=...)`
- `renderizar_segunda_juridica(manchete, foto_path, identidade_visual, caminho_saida, nome_conta=..., instagram=...)`

Uma função auxiliar `escolher_foto(categoria) -> str` faz o round-robin dentro de
`apps/api/media/banco_fotos/<categoria>/`. A categoria por peça vem de um mapeamento
fixo a partir de `Pauta.area` (mesmo padrão de área já usado no publicador de blog):

| `Pauta.area` (ou substring) | categoria de foto |
|---|---|
| "Trabalhista" | `trabalho-braçal` |
| "Previdenciário" | `retrato-humano` |
| "Família" | `familia` |
| qualquer outra / não mapeada | `escritorio` (fallback padrão) |

Comparação por substring (case-insensitive) contra o valor de `area`, não igualdade
exata — evita quebrar se o texto da área vier com variação.

## Mudanças de dados

- **Prompt de `legenda`** (`app/routers/content.py`, `PROMPTS["legenda"]`): passa a
  pedir também `"manchete": str` (frase de impacto, até 8 palavras) no JSON de
  resposta, além do `"texto"` que já existe. `ContentPiece.corpo` para `tipo="legenda"`
  passa a ter `{"texto": str, "manchete": str}`.
- **Escolha de formato**: novo campo `formato_imagem: "pergunta" | "segunda_juridica" | null`
  dentro do mesmo `corpo` JSON, setado via o `PATCH /content/{id}` que já existe (não
  precisa de rota nova) quando a usuária escolhe o formato na tela de Aprovação ou no
  Estúdio de Criativos. Enquanto `formato_imagem` for `null`, a peça aparece na lista
  mas sem preview de imagem (usuária escolhe antes de gerar/baixar).
- Nenhuma migração de banco necessária — `corpo` já é uma coluna JSON livre.

## Estúdio de Criativos (frontend)

`app/(app)/criativos/page.tsx` passa a buscar `tipo=carrossel` **e** `tipo=legenda`
(duas chamadas, ou uma chamada sem filtro de tipo — decisão de implementação). Para
peças `legenda`:
- Se `formato_imagem` ainda não foi escolhido, mostra os dois botões de formato
  ("Pergunta" / "Segunda Jurídica") em vez de preview.
- Depois de escolhida, chama o backend pra renderizar (reaproveita o padrão de
  `renderizar_slide` já usado — render acontece sob demanda quando a usuária abre a
  peça, não é pré-gerado em lote) e mostra a imagem com o mesmo botão de download
  (`toPng`) que o carrossel já tem.

## Testes

Seguindo TDD como o resto do projeto:
- `tests/test_render_criativo_pergunta.py` / `test_render_criativo_segunda_juridica.py`
  — real Playwright render (mesmo padrão de `test_render_criativo.py`), confere
  dimensão da imagem e presença dos textos esperados.
- `tests/test_escolher_foto.py` — round-robin dentro de uma categoria, fallback
  quando a categoria não tem fotos ainda.
- Teste do prompt de `legenda` estendido: mesma lógica de `test_content_gerar.py`
  (mocka `generate_json`, não precisa reavaliar o texto do prompt).
- `tests/test_content_aprovar.py` (ou arquivo equivalente): confere que
  `PATCH /content/{id}` com `corpo.formato_imagem` persiste corretamente — já é
  comportamento genérico do endpoint, teste serve pra travar a regra.

## Validação final (execução assistida)

Depois do pipeline pronto: gerar uma pauta real, aprovar o conteúdo `legenda`,
escolher um dos dois formatos, conferir o render, aprovar (dispara o agendamento
automático já existente via `agenda.py`) — ponta a ponta, feito nesta mesma conversa
como prova de que o fluxo funciona.
