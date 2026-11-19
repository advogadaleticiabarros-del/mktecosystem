# Auditoria de SEO: advogadaleticiabarros.com.br (19/11/2026)

Feita com a skill **claude-seo** (a mesma do Reels de referência do @promptepipoca, comando `/seo audit`), rodando neste
computador. Foram lidas as 82 páginas do mapa do site e os 14 links internos que estão fora dele.

**Nota geral: 76/100** (bom; a base técnica está sólida, o que puxa a nota para baixo são as imagens pesadas e detalhes de
título, descrição e páginas duplicadas).

| Área | Peso | Nota |
|---|---|---|
| Técnico (rastreio, indexação, segurança) | 22% | 82 |
| Conteúdo | 23% | 80 |
| Na página (título, descrição, H1, links) | 20% | 74 |
| Dados estruturados (schema) | 10% | 78 |
| Velocidade | 10% | 60 (estimada; ver abaixo) |
| Prontidão para IA (ChatGPT, Gemini, AI Overviews) | 10% | 85 |
| Imagens | 5% | 55 |

**Velocidade:** o teste oficial do Google (PageSpeed) recusou por limite da cota gratuita compartilhada. A nota foi
estimada pelo peso das páginas e pela resposta do servidor. Para medir de verdade: pagespeed.web.dev ou uma chave de API
do Google.

## O que já está bom

- HTTPS em todas as páginas; `http://` e `www` redirecionam para o endereço certo (um salto só).
- As 82 páginas do mapa do site respondem 200, todas em `pt-BR`, nenhuma bloqueada sem querer.
- `robots.txt` liberado e apontando o mapa do site; página inexistente devolve 404 de verdade.
- `llms.txt` publicado e dentro das regras; o texto aparece sem depender de JavaScript (IA lê tudo).
- Servidor rápido: ~0,4 s por página, com compressão gzip.
- Schema em 73 das 82 páginas: artigos com BlogPosting + FAQ + Breadcrumb, home com Attorney/LegalService com endereço,
  telefone, horário e redes.
- Artigos longos (a maioria acima de 600 palavras), com fonte legal.

## Problemas, do mais urgente ao menos

### Alta (resolver nesta semana)

1. **Imagens pesadas na home (cerca de 360 KB só em PNG).** `santiagopradoebarrosescritorioadvogadas.png` (139 KB),
   `hero-leticia-sem-fundo.png` (99 KB), `logo-800x800.png` (55 KB, usada como logo pequeno). Sem versão WebP, sem
   `width`/`height` (a página "pula" enquanto carrega, o que o Google mede como CLS) e sem `loading="lazy"` nas que ficam
   abaixo da dobra. Correção: converter para WebP, logo em tamanho real, declarar largura e altura, lazy fora da primeira
   tela. É o que mais pesa na velocidade no celular.
2. **Páginas duplicadas abertas ao Google: `/lp-v3/gestante-clt.html` e `/lp-v3/pensao-alimenticia.html`.** São versões
   antigas das páginas em `/lp/`, sem canonical e sem noindex, e ainda recebem links de 3 artigos
   (`fui-demitida-gravida-o-que-fazer`, `pai-nao-paga-pensao-o-que-fazer`, `pensao-alimenticia-como-funciona`). O Google
   pode dividir a força entre as duas versões. Correção: trocar os links dos artigos para `/lp/...` e redirecionar
   `/lp-v3/` para `/lp/` (301 no nginx).
3. **Cinco páginas de campanha sem canonical, sem imagem de compartilhamento e sem schema:** `/lp/gestante-clt.html`,
   `/lp/pensao-alimenticia.html`, `/lp/bpc-loas-criancas.html`, `/lp/insalubridade-clt.html`,
   `/lp/assessoria-empresarial.html`. Correção: canonical apontando para si mesma, `og:image` e schema `Service` + FAQ
   (o mesmo das páginas de área).

### Média (resolver neste mês)

4. **Links internos para `index.html` em 67 páginas.** O menu leva para `/index.html` e `/blog/index.html` em vez de `/`
   e `/blog/`. O canonical salva a indexação, mas o Google gasta rastreio com o endereço repetido. Correção: trocar os
   links do menu no template.
5. **Links internos com UTM.** A home e alguns artigos linkam `/lp/demissao-por-voto.html?utm_...` (8 variações) e a
   calculadora do 13º também. O canonical está certo, mas UTM em link interno embaralha os números do Analytics (a visita
   vira "campanha" em vez de "orgânico"). Correção: tirar o UTM dos links internos; usar evento de clique se precisar medir.
6. **Títulos longos demais (9 páginas, o Google corta depois de ~60 caracteres).** Os piores: `/lp/demissao-por-voto.html`
   (111), `chefe-manda-mensagem-no-whatsapp...` (92), `/lp/calculadora-13-salario.html` (87). Também
   `/areas/direito-familia.html`, `/areas/direito-previdenciario.html`, `/escritorio.html` e três artigos (67 a 71).
7. **Descrições longas (7 páginas acima de 165 caracteres):** `demissao-por-voto` (236), `escritorio` (228),
   `direito-previdenciario` (216), `calculadora-13-salario` (205) e outras três.
8. **Páginas de área sem imagem de compartilhamento.** As 7 páginas em `/areas/` não têm `og:image`: quando alguém manda
   o link no WhatsApp, aparece sem foto.
9. **Páginas curtas:** `/contato.html` (235 palavras), `/escritorio.html` (363), artigo
   `pedi-demissao-gravida-posso-reverter` (358), `/areas/assessoria-juridica.html` (506). O artigo é o que importa:
   ampliar com exemplo, passo a passo e FAQ.
10. **Dois H1 iguais** no artigo `gravidez-e-trabalho-conheca-seus-direitos-essenciais...`. Deixar um só.
11. **Sem cabeçalhos de segurança** (HSTS, X-Content-Type-Options, Referrer-Policy). Não muda posição no Google
    diretamente, mas é boa prática e entra em auditorias. Correção de 3 linhas no `nginx-site-leticia.conf`.

### Baixa (quando der)

12. Três famílias de fonte do Google na home (Cormorant, Inter, Playfair) com muitos pesos. Cortar pesos que não são
    usados acelera a primeira pintura.
13. Widget da Elfsight (33 KB de script de terceiro). Se for só para avaliações, dá para trocar por bloco estático.
14. Schema da home usa o e-mail Gmail; se existir e-mail do domínio, preferir o do domínio (passa mais confiança).
15. Contato, política de privacidade e termos sem schema (baixo impacto).

## Plano de ação

| Fase | Quando | O quê |
|---|---|---|
| 1 | Esta semana | Itens 1, 2 e 3 (imagens, `/lp-v3/`, canonical e schema das LPs) |
| 2 | Próximas 2 semanas | Itens 4 a 8 (menu sem `index.html`, UTM interno, títulos, descrições, `og:image`) |
| 3 | Dezembro | Itens 9 a 11 (ampliar páginas curtas, H1 duplo, cabeçalhos de segurança) |
| 4 | Contínuo | Medir velocidade no PageSpeed; checar Search Console todo mês (skill `leticia-seo-local`) |

## Como foi feito

- Skill claude-seo 2.5.0 (motor instalado em 19/11/2026 com `claude-seo setup`, a pedido da Jessica).
- Leitura da home renderizada, varredura das 82 URLs do `sitemap.xml` e dos links internos, teste de prontidão para
  agentes de IA (`agentic_check.py`), peso dos arquivos da home.
- Não medido nesta rodada: velocidade real no celular (PageSpeed recusou por cota), dados do Search Console e do
  Google Analytics (sem credenciais da API nesta skill), backlinks.
- Nenhuma mudança foi feita no site.
