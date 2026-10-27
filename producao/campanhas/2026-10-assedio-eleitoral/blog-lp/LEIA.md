# Blog e landing page · campanha demissão por causa do voto (27/10/2026)

## No ar
- LP com formulário: https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html
  (fonte: `lp/demissao-por-voto.html`; fundo `assets/images/lp/lp-demissao-voto.jpg`, Pexels 9301910)
- Artigo: https://advogadaleticiabarros.com.br/blog/demitido-por-causa-do-voto-o-que-a-lei-garante.html
  (corpo: `artigo-demitido-por-causa-do-voto.html`; capa `blog/capas/<slug>.jpg`, mesma foto)
- Os dois entraram no `sitemap.xml`; o artigo também entrou no índice do blog e no `llms.txt`. O Bing foi avisado (200).
  O IndexNow respondeu 403 (chave de verificação, problema antigo).

## Formulário
- `POST https://crm.advogadaleticiabarros.com.br/api/public/lead`, `area=trabalhista`, UTMs em campos próprios
  (`utm_campaign` padrão `assedio-eleitoral-2026`), `landing_page`, mensagem começando `[LP demissao-por-voto]`
  com o que aconteceu, quando, cidade, posição do formulário (topo/fim) e relato.
- O `/js/conversoes.js` do site conta `generate_lead` e o pixel "Lead" quando o CRM responde OK.
- Teste real em 27/10: lead "TESTE CLAUDE - apagar" (27 90000-0001). Excluir pela tela de leads do CRM.

## Links com UTM
- Stories: `...?utm_source=instagram&utm_medium=stories&utm_campaign=assedio-eleitoral-2026`
- Artigo → LP: `utm_source=blog&utm_medium=artigo`, `utm_content` = topo, meio, fim, cta-final.

## Fatos conferidos
Ver `../BRIEFING.md`. A seção de gravação usa o STF Tema 237 (RE 583.937): "É lícita a prova consistente em gravação
ambiental realizada por um dos interlocutores sem conhecimento do outro". A ressalva do STF vale só para o processo
eleitoral, não para o trabalhista. Na denúncia ao MPT, a home do mpt.mp.br traz "Selecione o estado para realizar a denúncia".

## Backups (no container `api` da VPS)
`/tmp/bkp_lp_voto/` (versão anterior da LP) e `/tmp/bkp_artigo_voto/` (índice do blog, sitemap e llms.txt de antes).
