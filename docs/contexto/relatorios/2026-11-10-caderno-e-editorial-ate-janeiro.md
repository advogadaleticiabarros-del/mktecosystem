# Caderno da marca e editorial até 31/01/2027 (10/11/2026)

## Pedido

Jessica: "no doc ... mostrando o feed tem alguns sem capa, analise e providencie e estão faltando posts pode ser 2 -
quando sair reels pode sair as outras publicações ao meio dia - organize tudo que fizemos essa semana, monte um caderno
com os estilos ... e organize nosso editorial até o final do mês de janeiro ... feed harmônico, bonito, estiloso, viral
... não escuro". Depois: "salve todo o contexto lá no Orbit", "estilo Flagrante, quero que produza mais para completar,
organize quantos de cada estilo e formato sairá por semana", "no domingo um vídeo reels original dela" (escolher a hora),
e, sobre as capas de domingo: "não ficaram boas! Coloque em 3D alguma foto da Dra sentada".

## Feito

- **Agenda** (`apps/api/app/services/agenda.py`, testes `tests/test_agenda_um_por_dia.py`): 2 no feed por dia, post às
  12:00 e Reels às 19:00, sem disputarem a vaga. O teste com data fixa no passado ficou relativo.
- **Orbit (produção)**, por `apps/api/_saida_producao_1510/montar_editorial_jan.py` → `editorial_jan.json` →
  `aplicar_editorial_jan.py` (container):
  - posts das 11h/14h de 11/11 em diante passaram para 12h;
  - 59 peças novas aprovadas e agendadas: 34 Manchetes avulsas (12h), 8 peças de marca (Verbete, 5 Papel e Ouro claras,
    Errata, Palavra de Ouro "Hora extra", com legendas novas), 9 Reels Flagrante prontos e nunca publicados (04/12 e
    terças/sextas de janeiro), 8 Reels Mito ou Lei de janeiro;
  - 17 frases Manchete da reserva (quinta 19h e 12h de janeiro);
  - 7 Reels gravados pela Dra. nos domingos 15/11 a 27/12, 15h30, **pausados**, com capa nova (o Limbo 1/2 saiu de 05 e
    08/01);
  - Mito ou Lei de 07/01 (quinta) foi para 06/01.
- **Mito ou Lei de janeiro**: `conteudo_jan.py` (afirmações já aprovadas como estático em out/nov), `mito_lei.py` (TELA
  01-13 a 01-30) e `capas_mito_foto.py` (fotos Pexels novas). 01-30 refeito com pergunta curta (passava da margem);
  capa 01-13 trocada (a foto cortava a cabeça).
- **Capa "Domingo com a Dra."**: `producao/reels/capas_dra.py`, retrato real dela sentada em quadro dourado girado em 3D.
- **Caderno**: `docs/CADERNO_DA_MARCA.md`; editorial `docs/EDITORIAL_ATE_JAN_2027.md` (com a lista dia a dia lida do
  Orbit); página `/caderno` no Orbit web (`apps/web/app/(app)/caderno/page.tsx`, `apps/web/lib/markdown.ts`, item no
  menu); página visual https://claude.ai/artifact/P9qD3jR6JvvRoMj6kZGBWf (`pagina_caderno.py` + `.html`).
- Regras atualizadas: `CLAUDE.md`, `docs/PASSAGEM_DE_CONTEXTO.md`, `docs/CONTEXTO_PROJETO.md`, skill `leticia-reels-motion`,
  memória (`reels-2-por-semana`, `domingo-com-a-dra`, `feed-claro`).
- Entraram junto no commit arquivos de outra sessão que agora estão em produção: `producao/estilos/manchete/legendas.md`,
  `flagrante_estaticos.py`, `gerar.py`, `docs/ESTILO_MANCHETE.md` e os episódios Flagrante 23 a 34.

## Verificado

- 372 testes da API passando; `tsc --noEmit` do web sem erro; teste do leitor de Markdown (`lib/markdown.test.mts`) ok.
- Backup antes: `/root/orbit-backups/antes-editorial-jan-20261110.sql.gz` (1,27 MB).
- Depois de aplicar: segunda simulação não mudaria nada; de 11/11 a 31/01 todo dia tem post às 12h (25/12 livre de
  propósito) e nenhum dia tem mais de 2 no feed. Links públicos (jpg e mp4) respondendo 206/200 com o tipo certo.
- Não verificado: aparência no celular real, revisão
  jurídica das legendas novas.

## Decisões e porquês

- Domingo 15h30: os dois Reels de domingo com mais alcance do perfil (1.900 e 1.362 contas) saíram entre 15h29 e 15h46.
- Reels da Dra. pausados: a Jessica achou a edição antiga feia (10/11); saem quando a versão do motor moderno for aprovada.
- Flagrante "produzir mais": havia 20 episódios prontos e aprovados (09/11) nunca usados; 9 cobriram as vagas até 29/01 e
  11 ficam para fevereiro. Não renderizei episódios novos.
- Capa 3D por perspectiva, sem recorte: o recorte automático do cabelo da Dra. já tinha sido reprovado.
- Vídeo "Acervo: Gestante demitida" (02/01, pausado) não tem a Dra.; ficou fora dos domingos e sem capa.
- Capas textura do Flagrante (café) são o ponto mais escuro da grade; mantidas (aprovadas em 09/11), com a variação clara
  disponível.

## Pendente

- **Deploy** (commit 2e47c9c): a permissão automática negou o deploy. A agenda no banco já está aplicada; o deploy
  só muda o auto-agendamento novo (12h) e põe a página `/caderno` no Orbit. Comandos: API `cd /home/orbit-src && git pull
  --ff-only && cd deploy/vps && docker compose up -d --build api`; web `cd apps/web && npm run build && cp -r out/*
  /var/www/orbit-web/`.

- Dra.: conferir citações legais das 34 Manchetes e das 8 legendas novas de marca.
- Jessica: aprovar a versão moderna dos Reels da Dra. para despausar os domingos; Dra. gravar 5 vídeos para os domingos de
  janeiro (03, 10, 17, 24, 31).
- Carrosséis de janeiro não existem: seg/qua/sáb 12h estão com estáticos até serem produzidos.
- Jessica decide se troca as capas textura do Flagrante pela variação clara.

## Próxima sessão

Conferir no Orbit (`ver_feed.py`) e na página do caderno; para janeiro, produzir carrosséis (skill `leticia-carrossel`,
`docs/PROCESSO_PRODUCAO_CARROSSEL.md`) e editar as gravações novas da Dra. (skill `leticia-reels-premium`).

## Continuação (11/11/2026): fevereiro

- **Pedido:** "Pode fazer até ao máximo que der dá até fevereiro ou março?"
- **Feito:** fevereiro inteiro no Orbit (48 ações: 35 peças novas e 13 perguntas da reserva com arte clara). Detalhes em
  `docs/CONTEXTO_PROJETO.md` (seção Fevereiro de 2027) e `docs/EDITORIAL_DO_FEED.md` (novo nome do editorial).
  Capas Moldura Viva com 12 fotos Pexels novas; Carnaval e doméstica trocadas depois de conferidas.
- **Verificado:** simulação antes e depois (a segunda não mudaria nada); de 11/11 a 28/02 todo dia tem post às 12h e
  nenhum dia passa de 2 no feed; página do caderno atualizada (versão 2). Em 6 vídeos de fevereiro a linha da base legal
  passa 2 a 4 px do limite de área segura por alguns segundos (mantido).
- **Disco C:** encheu duas vezes. Apaguei só o que eu tinha gerado: áudios intermediários `som.wav` de vídeos já prontos,
  pastas de envio e o modelo isnet do rembg (baixa de novo sozinho). Restam ~130 MB livres: precisa de limpeza da Jessica
  antes de qualquer render grande.
- **Pendente:** conferência jurídica da Dra. dos textos novos de fevereiro (12 Mito ou Lei, 9 frases, 6 acentos);
  quintas e domingos de fevereiro com 1 post; março (14 Mito ou Lei, 6 Flagrantes, posts das 12h, vídeos da Dra.);
  deploy (ainda negado pela permissão automática).

## Continuação (11/11/2026): arquivo de conferência

- **Pedido:** "Me mande um arquivo para conferência sempre e já com os criativos".
- **Feito:** `pagina_conferencia.py` + `.html` (lê os JSON do editorial e as artes da mídia do Orbit). Primeira conferência,
  89 peças (35 textos novos, 34 Manchetes com citação a conferir, 20 artes novas com texto aprovado):
  https://claude.ai/artifact/UQfXHmqpQQ8F9kAoDJaM7Z. Regra gravada no `CLAUDE.md` e na memória.
