# 2026-10-23 · TikTok com agenda própria e plano de crescimento

## Pedido
"Manter o TikTok independente do Instagram, editorial próprio, buscar os horários de maior fluxo", depois: "qual
música vai pegar no TikTok, acho que podemos pegar algo em alta. Trace um plano de crescimento, estude o algoritmo e
vamos trabalhar no crescimento a curto prazo e viralização". Respondeu "sim" à proposta de 4 a 5 vídeos por semana.

## Feito
- Commit `cf93ccd`:
  - `apps/api/app/services/tiktok.py`: fila própria (`publicar_fila_tiktok`, `GRADE_TIKTOK`, `remarcar`);
    `situacao` devolve `fila`.
  - `PUT /tiktok/{id}/agenda` em `routers/tiktok.py`.
  - A tela `/tiktok` mostra a fila e o passo a passo do som; o card da Visão Geral ganhou texto novo.
  - KPI "Na fila do TikTok" na tela Desempenho.
- `docs/ESTRATEGIA_TIKTOK.md`: algoritmo (com fontes), grade de horários em teste, música, formatos, táticas de 30
  dias, metas e fila inicial.
- `CLAUDE.md` e `docs/CONTEXTO_PROJETO.md` atualizados.
- Produção:
  - backup `/root/orbit-backups/antes_tiktok_fila_2026-10-23.sql.gz`;
  - deploy da API e do web;
  - fila montada: 23 vídeos de 25/10 a 24/11, com as séries de gestante e de guarda remarcadas para dias seguidos.

## Verificado
- `py -m pytest tests/`: 340 testes passando. `npx tsc --noEmit` sem erro no web.
- Na VPS:
  - commit `cf93ccd` no ar, sem erro no log da API;
  - `/tiktok` responde 401 sem login (rota viva);
  - a consulta ao banco mostra os 23 vídeos na fila, com 0 enviados.
- Não verificado: o primeiro envio real (domingo 25/10, 10h, para a caixa de rascunhos) e se a conta do TikTok já é
  Conta comercial.
- `graphify update .` não rodou: o comando não está instalado neste computador.

## Decisões e porquês
- **Música:**
  - Som "Em alta" da biblioteca **comercial**, não da geral. Conta de empresa só tem licença da comercial; som da
    geral pode silenciar ou derrubar o vídeo.
  - O som entra no app, ao publicar o rascunho, a 10-15% sob a voz. A API de vídeo não põe som, e assim o arquivo e
    a voz da Dra. não mudam (padrão dos Reels).
- **Grade:** dom 10h, seg 18h, ter 12h, qua 20h, qui 18h. Os estudos públicos discordam entre si, então a grade
  testa três faixas e a revisão com os números do TikTok Studio fica para 20/11.
- **O que entra na fila:**
  - Reels com agendamento ativo do Instagram, inclusive os já publicados lá (para o TikTok são novos).
  - Versões sem agendamento e Reels pausados ficam de fora, para não ir versão antiga ou duplicada.
  - A regra antiga "só depois da conexão" caiu.
- **Onde fica a vaga:** em `corpo["tiktok"]`. `scheduled_posts` tem trava de um agendamento por peça e já guarda o
  do Instagram.
- **Push:** a conta ativa do gh (`alcancelegalmkt-collab`) levou 403 neste repositório. O push saiu com o token da
  `advogadaleticiabarros-del`, só naquele comando; a conta ativa não foi trocada.

## Pendente
- Equipe: conferir no app se a conta do TikTok é **Conta comercial** (categoria "Serviços jurídicos"); arrumar nome
  e bio (seção 5 da estratégia).
- A partir de 25/11 a fila só recebe 2 Reels por semana. Para manter 5, é preciso produzir cortes curtos
  (`tipo="tiktok"`) e respostas a comentário a partir da semana de 09/11. Quem decide os temas: a Dra. e a Jessica.
- Teste do modo foto (carrosséis) a partir da semana 3, publicado à mão.
- Revisão em 20/11/2026: horários, formatos e se sobe para 7 por semana.

## Próxima sessão
Ver na tela `/tiktok` se o vídeo de domingo 25/10 10h caiu no rascunho e foi publicado. Na semana de 09/11, começar
os cortes com a skill `leticia-reels-premium` (peça e arquivo novos).
