# Relatório · listas por causa do voto (28/10/2026)

## Pedido
Jessica: "há pessoas incitando a demissão em massa de eleitores [de um partido] por causa do resultado da eleição...
Existem listas circulando por cidades do Brasil inteiro e de dentro do ES (sabido uma em Cachoeiro-ES), preciso
publicar sobre isso, tudo relativo ao direito, de quem está nessa lista, no que implica etc."

## Feito
- Pesquisa das notícias de 27-28/10 e da base legal. Resultado e textos em
  `producao/campanhas/2026-10-assedio-eleitoral/listas/ROTEIRO.md`: fatos conferidos, o que a lei diz por perfil
  (empregado, profissional/comércio, empresa), passo a passo, carrossel de 7 slides, legenda, 3 Stories, artigo
  completo (slug `nome-em-lista-por-causa-do-voto-o-que-fazer`), post de LinkedIn e roteiro de Reels para a Dra.
- `docs/CONTEXTO_PROJETO.md`: linha nova na seção da campanha "demissão pelo voto".

## Verificado
- Matérias lidas: A Gazeta (listas no ES, 6 cidades, Cachoeiro com igrejas), Brasil 247/O Globo (530 denúncias em
  menos de 2 dias, 2.467 no ano), Brasil de Fato (MG, PR, PB). Links no fim do roteiro.
- Artigos de lei citados de memória e conferidos no raciocínio (CP 103, 139, 140, 147, 147-A; CLT 483 "e"; LGPD 5º
  II e 6º IX; Lei 9.029 arts. 1º e 4º). **Não verificado** na fonte primária nesta sessão: Delegacia Online da PCES
  e a situação dos embargos do STF sobre o art. 19 do Marco Civil.
- Nada foi publicado, gerado em arte ou agendado.

## Decisões e porquês
- **Neutro**, sem partido nem candidato, como no `BRIEFING.md` da campanha (OAB, Provimento 205/2021), embora as
  listas de agora mirem eleitores de um lado.
- A matéria do ES fala de **boicote** a profissionais, comércio e igrejas, não de lista de funcionários para demitir.
  As peças tratam os dois casos e dizem com honestidade que deixar de comprar não é ilegal; o ilegal é expor,
  ofender, ameaçar e o empregador discriminar.
- Nunca reproduzir uma lista nem citar nomes ligados a ela (repetiria o dano).
- Não afirmar que "toda lista é crime" (a A Gazeta diz isso, mas depende do conteúdo).
- Destaque ao prazo de 6 meses da queixa-crime, o mais curto e menos conhecido.

## Pendente
- Aprovação da Jessica/Dra. dos textos (e se quer todas as peças ou parte).
- Depois do ok: arte do carrossel (modelo `../urnas/carrossel_v10.py`), artigo no ar (skill `leticia-blog-artigo`),
  agendamento no Orbit (1 feed por dia; Reels só ter/sex 21h, e sexta 30/10 já tem o Reels animado da campanha).
- Gravação do Reels pela Dra., se ela quiser.

## Próxima sessão
Ler `listas/ROTEIRO.md`, aplicar os ajustes pedidos, gerar a arte do carrossel e publicar o artigo com
`leticia-blog-artigo`. Skills: `voz-leticia`, `leticia-carrossel`, `leticia-blog-artigo`, `contexto-orbit`.

## Continuação: frases-notícia (mesmo dia)
- Pedido: "quero uma frase para chamar a atenção, deve ser notícia direta, ninguém vai ficar lendo post no Instagram
  sobre isso, vamos fazer igual às frases".
- Feito: 4 frases no modelo das frases da campanha do voto (fundo escuro, caixa-alta, fecho dourado) em
  `producao/frases/2026-10-28-listas-voto/` (`gerar_frases.py`, 4 PNG 1080x1440, `LEGENDAS.md` no mesmo formato das
  anteriores, com WhatsApp, como a Jessica aprovou para essas frases). As frases anteriores ficaram intactas.
- Verificado: as 4 imagens abertas e conferidas (texto dentro da largura, letra entre 94 e 100 px, fonte e assinatura).
- Pendente: escolher qual(is) vão ao ar e subir ao Orbit como rascunho (modelo:
  `producao/frases/2026-10-28-demitido-posicao-politica/subir_orbit.py`, JPG em `/app/media/voto-<nome>.jpg`).

## Continuação: as 4 frases com as duas sócias e legenda explicativa
- Pedido: "Faça todas, embaixo coloque o nome de Dra Letícia e Dra Carolina Prado OAB 29557" e "Faça uma legenda explicativa".
- Feito: `*-duas-advogadas-1080x1440.png` (4 artes, assinatura em duas linhas; as PNG anteriores, só com a Letícia,
  ficaram intactas). `LEGENDAS.md` ganhou a seção 0 "legenda explicativa" (serve para o carrossel das 4 ou para cada
  uma) e as duas assinaturas nas legendas 1 a 4.
- Não verificado: a seccional da Dra. Carolina. A arte usa "OAB/ES 29.557" (o escritório é do ES); confirmar com a Jessica.
- Pendente: formato (carrossel das 4 ou posts separados), horário e subir ao Orbit como rascunho.

## Continuação: no Orbit
- Pedido: "Coloque elas no Orbit".
- Feito: um carrossel em **rascunho** com as 4 artes (capa Cachoeiro, depois 6 cidades, seu nome, recebeu lista),
  legenda explicativa no Instagram e no Facebook, primeiro comentário com o link /voto, alt text, programação 28/10 18h.
  Peça `8126928c-c4ff-45aa-94e3-7dfdb9999ec9`, pauta `3ca54d6d-1c83-4093-a53f-4e183a37cb8f`. Script
  `producao/frases/2026-10-28-listas-voto/subir_orbit.py`.
- A legenda explicativa tinha 2.814 caracteres (o Instagram aceita 2.200); foi enxugada para 2.032 (2.046 contando os
  emojis como o Instagram) e atualizada no rascunho.
- Verificado: as 4 imagens respondem 200 (image/jpeg) em `api.orbit.advogadaleticiabarros.com.br/media/listas-voto-*.jpg`;
  a peça está `rascunho`, 4 imagens, programação gravada; contagem de peças antes/depois sem perda (carrossel 46 → 47).
- Pendente: aprovar no Editorial (ou postar à mão e marcar como publicado); confirmar a seccional da Dra. Carolina.

## Continuação: Stories e artigo do blog
- Pedido: "faça as frases em storie, e gere um artigo sobre isso para que eu possa divulgar e rankear no google também".
- Stories: `producao/frases/2026-10-28-listas-voto/gerar_stories.py` → `story-listas-voto-1..4-1080x1920.png` (áreas
  livres de 270 px no topo e 420 px embaixo; o 4 tem "Passo a passo no link abaixo" e espaço para o adesivo). No Orbit
  em **rascunho**, mesma pauta `3ca54d6d`, 28/10 18h05 a 18h08 (`subir_stories.py`); o story 4 leva o link do artigo
  com UTM e a reserva `/voto` se o artigo não estiver no ar. Imagens 200 em `/media/story-listas-voto-*.jpg`.
  `gerar_frases.py` ganhou a guarda `if __name__` (o gerador dos Stories importa os textos dele).
- Artigo: corpo em `producao/campanhas/2026-10-assedio-eleitoral/blog-lp/artigo-lista-por-causa-do-voto.html`, título
  "Lista por causa do voto é crime? O que a lei garante a quem está nela", slug `lista-por-causa-do-voto-e-crime`;
  capa `capa-blog-lista-voto.jpg` (Pexels 13801812, Mizuno K; descartadas fotos com logo da Apple). Script pronto
  `publicar_artigo_listas.py` (cópia do fluxo de `publicar_artigo.py`: backup, HTML, capa, índice, sitemap, llms.txt,
  IndexNow e Bing). **Não publicado:** a skill `leticia-blog-artigo` manda mostrar o rascunho e esperar o ok.
- Delegacia Online do ES: não confirmado que aceita crime contra a honra; o artigo diz só "Polícia Civil" e explica que
  o BO não basta (queixa-crime por advogado em 6 meses).
- Publicar: `scp` do corpo, da capa e do script para a VPS → `docker compose cp` para `/tmp` do container `api` →
  `docker compose exec -T -e PYTHONPATH=/app -w /app api python /tmp/publicar_artigo_listas.py` → conferir com curl
  (`article-hero` presente, `blog-grid` zero, card no índice, URL no sitemap) → pedir indexação no Search Console.
