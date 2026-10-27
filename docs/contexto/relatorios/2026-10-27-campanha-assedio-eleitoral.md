# Campanha "demissão pelo voto" (assédio eleitoral) · 27/10/2026

## Pedido
Jessica, 27/10/2026: "empresários estão demitindo funcionários que votaram em candidatos diferentes, precisamos abordar
de forma estratégica em todos os canais"; "urgente, postar de imediato e ter formulários para captação dos leads".
Ordem final: artigo + Stories → LP → 1 frase → carrossel bem explicativo → 1 estático; "só sobre isso hoje"; Reels
animado (com a voz da Dra. clonada das gravações dela) só depois; "faça para os trabalhadores primeiro, depois
LinkedIn". A LP deve ser "extremamente explicativa, ensine como pegar provas, quais servem".

## Feito
- Briefing com fatos e regras: `producao/campanhas/2026-10-assedio-eleitoral/BRIEFING.md`.
- LP no ar: https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html (fonte `lp/demissao-por-voto.html`,
  publicação `producao/campanhas/2026-10-assedio-eleitoral/blog-lp/publicar_lp.py`).
- Artigo no ar: https://advogadaleticiabarros.com.br/blog/demitido-por-causa-do-voto-o-que-a-lei-garante.html
  (texto e script em `blog-lp/`; sitemap, índice do blog e llms.txt atualizados; Bing avisado).
- Stories (8), carrossel (9 slides, peça `66ac094b`, versão de 7 slides em `versoes_anteriores`), frase (`c9c4e179`,
  15h), estático (`07c91c31`, 20h): rascunho no Orbit; scripts em `carrossel-stories/` e `frase-estatico/`; JPGs em
  `apps/api/_saida_producao_1510/pecas/` e `Desktop\ASSEDIO ELEITORAL\`.
- LinkedIn: `linkedin-post.md`, na fila do Orbit em rascunho (`5f13e925`, marcado 27/10 17h30, não sai sem aprovação).
- Reels: `producao/reels/series/22-assedio-eleitoral-motion/` (roteiro, serie.py, legendas, créditos Pexels).

## Verificado
- LP e artigo: HTTP 200 no ar, FAQPage presente, nenhum termo vetado pela OAB ("consulta gratuita", "especialista",
  "garanta"). Formulários testados no ar: 201 e 200 (lead de teste no CRM).
- Artes conferidas por imagem (acentos, contraste, área segura). Checagem OAB do Orbit: LinkedIn, legendas e
  primeiros comentários sem problema.
- Backups no Orbit antes de cada escrita (`/root/orbit-backups/pre-linkedin-assedio-2026-10-27.sql.gz`,
  `pre-assedio-eleitoral-2026-10-27.sql.gz`, `pre-assedio-frase-estatico-2026-10-27.sql.gz`); contagens antes e
  depois sem perda.
- Não verificado: indexação no Google (IndexNow deu 403, problema antigo da chave).

## Decisões e porquês
- Neutro: nada de partido, candidato ou "lado" (OAB, Provimento 205/2021), apesar de a onda de demissões mirar
  eleitores de um lado. Frase-chave: "não importa em quem você votou".
- O formulário pede "orientação", sem promessa e sem "consulta gratuita".
- Adesivo dos Stories e "link da bio" levam à LP (tem o formulário), não ao artigo.
- Separado: ameaça antes do voto = crime (Código Eleitoral, art. 301); demissão depois do voto = dispensa
  discriminatória (Lei 9.029, art. 4º).
- Artigo publicado sem a revisão prévia que a skill do blog pede, por causa do "postar de imediato".

## Pendente
- Jessica: aprovar no Editorial a frase (15h), o carrossel (18h) e o estático (20h); postar os Stories pelo app;
  trocar o link da bio pela LP (`utm_medium=bio`); fixar os primeiros comentários; postar o Facebook à mão
  (`Desktop\ASSEDIO ELEITORAL\carrossel\LEGENDAS.txt`); apagar o lead "TESTE CLAUDE - apagar" no CRM; Search
  Console → "Solicitar indexação" nas duas URLs; ler o artigo.
- Jessica: decidir se o "Reels 3/3 gestante" de hoje 21h vai para terça 03/11 21h (sexta 30/10 já tem "Guarda 3/3").
- Jessica: criar o clone de voz no ElevenLabs (Voices → Add a new voice → Instant) com
  `Desktop\NOVOS REELS\voz-para-clonar-leticia.wav` e mandar o voice id. Reels do voto: Trial Reels ou troca de slot.
- LinkedIn `5f13e925`: definir data e trocar o link pelo artigo quando ela liberar.
- Slide 04 do carrossel: foto do celular com borda borrada; refazer se ela pedir.
- Dra.: gravar o roteiro da série 21 (`producao/reels/series/21-assedio-eleitoral/roteiro-gravacao.md`).

## Próxima sessão
Com o voice id: em `C:\tmp\videos-reels\22-assedio-eleitoral-motion\work\`, `py narrar.py ../fontes/roteiro.txt
../fontes`, mandar a frase de teste, depois `py serie.py --checar` → `--amostras` → `py serie.py 1` (skill
`leticia-reels-motion`). Ver os leads `[LP demissao-por-voto]` no CRM e os números da campanha no GA4
(`utm_campaign=assedio-eleitoral-2026`).
