# Publicador Automático de Blog — Design

**Data:** 2026-07-21
**Status:** Aprovado para implementação

## Contexto

O blog real da Letícia (`https://advogadaleticiabarros.com.br/blog/`) é um site
estático hospedado na Hostinger, mantido hoje manualmente e publicado por um
automation separado (`advogadaleticiabarros-del/blogautomaticoleticia`, não
integrado ao Orbit). No Orbit, quando um `ContentPiece` do tipo `artigo` é
aprovado, `agendar_conteudo_aprovado()` já cria um `ScheduledPost` com
`canal="blog"` — mas isso é só uma categorização visual no calendário; **nada
publica de fato**. Este design fecha esse gap: publicar o artigo aprovado no
blog real, sozinho, via SFTP.

## Objetivo

Quando um `ScheduledPost` de `canal="blog"` chega na sua data agendada, o
Orbit deve: gerar o HTML completo do artigo no design real do site, gerar uma
capa simples, e publicar tudo via SFTP — sem intervenção manual.

## Escopo

Dentro do escopo:
- Renderizar o artigo em HTML fiel ao design system real do blog.
- Gerar meta description, resumo (excerpt) e slug para o artigo.
- Gerar uma capa simples (marca dourado/preto), sem estilo fotográfico.
- Publicar via SFTP: o HTML do artigo + atualização do `index.html` do blog
  (as duas grades) + atualização do `sitemap.xml`.
- Job recorrente (mesmo padrão do publicador do Instagram) que varre
  `ScheduledPost` com `canal="blog"` prontos para publicar.

Fora do escopo (não faz parte deste design):
- Estilo fotográfico/realista de imagem de capa — isso é exclusivo do
  Estúdio de Criativos do Instagram, já registrado como pendência separada.
- Qualquer alteração no automation externo `blogautomaticoleticia`.
- Edição/retry manual de um artigo já publicado (fica pra depois, se for
  necessário).

## Arquitetura

Segue exatamente o mesmo padrão já usado para o Instagram
(`app/services/instagram_publisher.py` + job no `scheduler.py`):

1. **Geração de conteúdo (extensão do prompt existente)** — o prompt do tipo
   `artigo` em `app/routers/content.py` passa a pedir também
   `meta_description` e `resumo` no JSON de resposta, além de `titulo` e
   `html`. Isso significa que `ContentPiece.corpo` para `tipo="artigo"` passa
   a ter 4 chaves: `titulo`, `html`, `meta_description`, `resumo`.

2. **`app/services/blog_slug.py`** — função pura `gerar_slug(titulo: str) -> str`
   que normaliza acentos, minúsculas, troca espaços/pontuação por hífen. Sem
   dependência nova (usa `unicodedata` da stdlib).

3. **`app/services/render_artigo_blog.py`** — dois renderizadores Jinja2 +
   Playwright, seguindo o padrão de `render_criativo.py`:
   - `renderizar_artigo_html(...)` → renderiza `templates/blog_artigo.html`
     (novo) para uma string HTML completa, usando a estrutura real do site
     (head com meta tags/OG/JSON-LD, breadcrumb, hero com categoria/título/
     data/tempo de leitura, corpo do artigo, CTA de WhatsApp).
   - `renderizar_capa_artigo(...)` → renderiza `templates/capa_artigo.html`
     (novo, reaproveitando a paleta de `identidade_visual.cores` do tenant,
     mesmo estilo texto-dourado-em-fundo-escuro do carrossel) para PNG via
     Playwright, tamanho 1200×630 (padrão og:image).

4. **`app/integrations/publish/sftp_client.py`** — cliente fino sobre
   `asyncssh` (nova dependência, já é assíncrona — combina com o resto do
   codebase) com 3 métodos: `upload(caminho_remoto, conteudo_bytes)`,
   `download(caminho_remoto) -> bytes` (para ler `index.html`/`sitemap.xml`
   atuais antes de editar) e `close()`. Credenciais vêm de
   `settings.BLOG_SFTP_HOST/PORT/USER/PASSWORD/PATH` (já configuradas no
   Railway).

5. **`app/services/blog_index_editor.py`** — funções puras de manipulação de
   HTML/XML (usando `BeautifulSoup`, nova dependência leve) que recebem o
   conteúdo atual de `index.html` e `sitemap.xml` (baixados via SFTP) e
   devolvem a versão atualizada:
   - `inserir_card(html_atual, artigo) -> str` — insere o novo `<a class="blog-card">`
     como primeiro filho de **ambas** as grades (`#blogGridRecent` e
     `#blogGrid`), no formato real capturado do site (imagem, badge "Novo",
     categoria, título, resumo, tempo de leitura).
   - `inserir_sitemap_entry(xml_atual, artigo) -> str` — insere `<url>` do
     novo artigo no `sitemap.xml`.

6. **`app/services/blog_publisher.py`** — orquestrador, mesmo formato de
   `instagram_publisher.py`:
   - `_agendamentos_prontos(db)` — `ScheduledPost` com `canal="blog"`,
     `status="pronto"`, `data_agendada <= hoje`.
   - `publicar_agendamentos_prontos(db) -> int` — para cada agendamento
     pronto: busca o `ContentPiece` (deve estar `status="aprovado"`, senão
     pula), busca a `Pauta` (categoria = `pauta.area`), gera slug, renderiza
     HTML do artigo e a capa, conecta via SFTP, baixa `index.html` e
     `sitemap.xml` atuais, aplica os inserts, sobe os 3 arquivos (novo HTML
     do artigo, `index.html` atualizado, `sitemap.xml` atualizado) mais a
     capa PNG. Em caso de sucesso: marca `status="publicado"` e grava a URL
     final em `platform_post_id`. Em caso de erro: mesmo padrão de retry do
     Instagram — incrementa `tentativas`, marca `status="erro"` após 3
     falhas, nunca derruba o job inteiro (`try/except` por agendamento).

7. **Scheduler** — `scheduler.py` importa
   `publicar_agendamentos_prontos as publicar_blog_prontos` e chama dentro
   de `job_envios()` (mesmo job de hora em hora que já publica Instagram),
   somando ao log existente.

## Dados e campos novos

- `Settings` (`app/config.py`): `BLOG_SFTP_HOST`, `BLOG_SFTP_PORT` (int,
  default 22), `BLOG_SFTP_USER`, `BLOG_SFTP_PASSWORD`, `BLOG_SFTP_PATH` — já
  criadas no Railway (`orbit-api`).
- `ContentPiece.corpo` (tipo `artigo`): `{"titulo": str, "html": str,
  "meta_description": str, "resumo": str}`.
- Nenhuma migração de banco necessária — reaproveita `ScheduledPost` e
  `ContentPiece` como estão.

## Categoria

Vem direto de `Pauta.area` (ex.: "Trabalhista", "Previdenciário"). O
`data-cat` do card usa a versão slugificada (`gerar_slug(pauta.area)`); o
texto visível da categoria usa `pauta.area` como está.

## Tratamento de erro

Mesmo padrão já validado no Instagram: qualquer exceção durante a publicação
de um agendamento (falha de conexão SFTP, erro ao gerar HTML, etc.) é
capturada, incrementa `tentativas`, marca `status="erro"` na 3ª falha, e o
loop continua para o próximo agendamento — uma falha nunca impede os demais
de serem publicados.

## Testes

Seguindo TDD como o resto do projeto:
- `tests/test_blog_slug.py` — casos de acentuação, espaços duplos,
  caracteres especiais.
- `tests/test_render_artigo_blog.py` — mocka Playwright, garante que o HTML
  final contém título/meta description/categoria/CTA.
- `tests/test_blog_index_editor.py` — dado um `index.html`/`sitemap.xml` de
  fixture (trecho real capturado do site), garante que o card/entrada é
  inserido nas 2 grades e no sitemap, sem quebrar o resto do documento.
- `tests/test_blog_publisher.py` — espelha
  `tests/test_instagram_publisher.py`: mocka SFTP client e renderizadores,
  cobre publica-com-sucesso, sem-`ContentPiece`-aprovado, falha incrementa
  tentativas/marca erro após 3.

## Fora de dúvida (confirmado com a usuária)

- Capa do artigo fica simples (dourado/preto), não fotográfica — isso é só
  para o Instagram, separadamente.
- Credenciais SFTP já coletadas e salvas no Railway
  (`BLOG_SFTP_HOST=147.93.38.211`, `PORT=65002`,
  `USER=u528898188`, `PATH=/home/u528898188/domains/advogadaleticiabarros.com.br/public_html/blog/`).
