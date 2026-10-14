---
name: leticia-blog-artigo
description: Use quando for escrever E publicar um artigo de blog para a Dra. Letícia Barros (advogadaleticiabarros.com.br) — do tema ao link no ar. Cobre voz, template, capa e publicação via SFTP.
---

# Artigo de blog da Letícia — do tema ao link no ar

Pipeline real: `apps/api/app/services/render_artigo_blog.py` (repo
`C:\tmp\mktecosystem`) + publicação manual/automática via SFTP na Hostinger.
Aprendido com dor em 2026-07-22 — vários bugs reais só apareceram depois do
primeiro artigo ir pro ar. Siga esta ordem pra não repetir.

## 1. Escrever o texto

- Use a skill `voz-leticia` pra qualquer texto (título, meta description,
  resumo, corpo, FAQ).
- **SEO/GEO:** o termo de busca principal do tema precisa aparecer no título
  (H1), não só espalhado pelo corpo — é o campo com mais peso pra indexação
  e pro que motores de busca por IA extraem como resposta direta. Ver
  [[orbit-estrategia-crescimento-instagram]] pra lista de termos-base do
  nicho dela.
- Nunca a palavra "deficiência" — troque por "necessidades especiais".
- CTA do artigo é sempre impessoal: **"Se essa é a sua situação, procure uma
  advogada de confiança"** — nunca "fale comigo", "analiso seu caso", nunca
  link direto de WhatsApp no meio do texto (viola ética OAB).
- **Mostre o rascunho completo pra usuária e espere aprovação antes de
  gerar HTML ou subir qualquer coisa.** Publicar e corrigir ao vivo gera
  retrabalho que ela já reclamou explicitamente — acertar antes de publicar.

## 2. Escolher a foto (capa + dentro do artigo)

- `renderizar_capa_artigo(foto_path=...)` só recorta a foto pro tamanho
  1200×630 — **nunca mais sobrepõe título/logo/texto na imagem** (ela pediu
  expressamente pra tirar isso; código já corrigido, não reintroduzir).
  A mesma imagem serve pro card do blog, pro og:image e pro
  `<figure class="article-cover">` dentro do artigo.
- Se o tema tiver pasta própria em
  `C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\` (ex:
  `IDOSAS APOSENTADORIA E BEM ESTAR` pra aposentadoria/INSS/idosos, `BPC`
  pra BPC/LOAS/autismo), usar direto essa pasta sem perguntar de novo.
  Senão, perguntar à usuária qual pasta/foto usar.

## 3. Gerar o HTML do artigo

```python
from app.services.render_artigo_blog import renderizar_artigo_html, renderizar_capa_artigo
```

- `renderizar_artigo_html` usa o template `blog_artigo.html`, que **precisa**
  ter `<header>` de navegação, `<footer>` completo e o `<style>` inline com
  as classes de artigo (`.article-hero`, `.article-body`, `.callout-box`,
  `.article-cta`, `.prova-table`, `.article-cover`). Isso já está no template
  atual — se for editar o template, NUNCA remover essas três coisas, foi
  exatamente a falta delas que quebrou o primeiro artigo publicado (saiu sem
  nenhum estilo, sem menu, sem rodapé).
- Compare sempre com um artigo real que já está no ar (ex:
  `racismo-no-trabalho-como-provar-e-seus-direitos.html`) se algo parecer
  errado depois de publicado — é o jeito mais rápido de achar o que falta.

## 4. Publicar via SFTP

Credenciais e caminho (confirme antes que a senha não mudou — checar hPanel
se der `PermissionDenied`):
- Host `147.93.38.211`, porta `65002`, usuário `u528898188`
- **Caminho relativo** (a sessão SFTP já abre dentro de `/home/u528898188`,
  NUNCA repetir esse prefixo):
  `domains/advogadaleticiabarros.com.br/public_html/blog/`
- Sobe: `{slug}.html`, `capas/{slug}.png`, `index.html` atualizado (card
  novo) e `../sitemap.xml` atualizado.
- `blog_publisher.py` faz isso automaticamente se o `ScheduledPost` (canal
  `blog`, formato `artigo`) estiver com `content_piece_id` de uma peça
  `aprovada` e o horário já tiver chegado — roda a cada hora, minuto :15,
  via `app/scheduler.py` em produção.

## 5. Verificar de verdade (não confiar em screenshot só)

```bash
curl -s "https://advogadaleticiabarros.com.br/blog/{slug}.html?_=$(date +%s)" | grep -c "article-hero\|blog-grid"
```

Tem que ter `article-hero` e **zero** `blog-grid`. Confira também que o card
apareceu em `blog/index.html` e no `sitemap.xml`. Se a usuária disser que
está "errado" mas o servidor confirma certo, pode ser cache de navegador —
mas só suspeitar disso DEPOIS de comparar com um artigo real via curl, nunca
antes. Perdemos tempo real nessa ordem errada.

## 6. Registrar no Calendário

`ScheduledPost` canal=`blog`, formato=`artigo`, `content_piece_id` da peça
aprovada, `status="pronto"` — o publicador automático troca pra `"publicado"`
sozinho quando sobe.

## 7. Pedir indexação no Google Search Console

Propriedade `advogadaleticiabarros.com.br` já verificada (2026-07-29, via
arquivo HTML, mesmo arquivo/token não reaproveitável pra outra verificação
futura). Depois de publicar:
- Pedir pra usuária colar a URL do artigo na barra "Inspecionar qualquer
  URL" do Search Console e clicar em "Solicitar indexação" — acelera de
  dias pra horas.
- Sitemap (`sitemap.xml`) já está enviado uma vez; não precisa reenviar a
  cada artigo novo, o Google rastreia sozinho, mas pedir indexação manual
  do artigo específico continua valendo a pena pra notícia quente/atual.
