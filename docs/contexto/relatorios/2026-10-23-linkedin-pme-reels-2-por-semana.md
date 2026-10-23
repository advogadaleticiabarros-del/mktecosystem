# 23/10/2026: LinkedIn para PMEs, página para empresas, Reels 2 por semana e TikTok

## Pedido

- "Conseguimos monitorar o que do LinkedIn com essa API? Existem dados? Podemos programar postagens? Vamos montar
  uma estratégia para captar empresas PME com assessoria jurídica e prevenção trabalhista." Resposta: "todos, vamos
  montar completo e manter a mesma estratégia até janeiro de 2027".
- "Temos que movimentar a página além do perfil" (página da empresa criada no LinkedIn).
- "Quero reels apenas 2 vezes por semana no Instagram, para dar tempo de ter destaque." Também perguntou se o
  Instagram segue um calendário e como está o editorial do TikTok.
- Objetivo dela: "entrar em 2027 com mais reconhecimento público" da marca Letícia Barros, em várias frentes e
  automatizando tudo.

## Feito

- **Código do LinkedIn** (commit `de50544`, no ar):
  - painel do Google ganhou `analytics.linkedin` (visitas e contatos vindos do LinkedIn, 90 dias);
  - a tela `/linkedin` ganhou o card Resultados, a edição de post na fila, "Aprovar todos os rascunhos" e a fila em ordem de data;
  - UTM automático nos links do site (`link_com_utm`) e menção de página no texto (`escapar_texto`).
- **Fila:** 26 posts "Empresa em dia" como **rascunho**, de 27/10/2026 a 28/01/2027, terças e quintas às 8h. Texto-fonte em
  `producao/linkedin/posts-empresa-em-dia-out26-jan27.json`. Todos passaram pela checagem da OAB.
- **Estratégia:** `docs/ESTRATEGIA_LINKEDIN_PME.md`, com a regra OAB, os públicos, os pilares, o calendário, o funil, a página,
  as métricas e o passo a passo da Community Management API. Também está referenciada no `CLAUDE.md`.
- **Página para empresas regerada** (`lp/_gerar_lp_empresas.py` → `lp/empresas-adequacao-trabalhista-2026.html`):
  - EC 141 promulgada em 16/10;
  - multas da NR-1 descritas como "suspensas temporariamente";
  - seção e formulário do Checklist 2027, que envia o contato ao CRM com a marca `[ISCA checklist-empresas-2027]` e libera o PDF.
- **Checklist 2027 para empresas:** `lp/checklist-2027-empresas.pdf`, com 5 páginas. O modelo é `lp/checklist-2027-empresas-pdf.html` e o gerador é
  `lp/_gerar_pdf_checklist_empresas.py`.
- **Capa da página da empresa no LinkedIn:** `producao/linkedin/capa-pagina-linkedin@2x.png` (gerador
  `gerar_capa_pagina.py`).
- **Reels 2 por semana:**
  - `DIAS_REELS = {1, 4}` em `apps/api/app/services/agenda.py`: Reels só na terça e na sexta às 21h, e o feed nos outros dias;
  - o calendário de produção foi remarcado (20 itens). O log de antes e depois está em `/root/orbit-backups/remarcacao_reels_2026-10-23.json` na VPS;
  - a regra foi registrada no `MANUAL_CONTEUDO_REDES.md`, na `ESTRATEGIA_CRESCIMENTO_ORGANICO.md`, no `PLANO_CONTEUDO_NOV_2026.md` e na memória.
- **Teste do painel do Google:** deixou de depender da data do dia (`datas_fixas`).
- **Contexto:** atualizado em `docs/CONTEXTO_PROJETO.md` (seção de 23/10).

## Verificado

- Suíte da API: 328 testes passando. `tsc --noEmit` do web sem erros.
- Deploy de `de50544` na VPS: API reconstruída e web copiado. A atualização do painel do Google em produção rodou,
  e `analytics.linkedin` voltou com 0 visitas (esperado: nada foi postado ainda).
- Conexão do LinkedIn em produção: ativa, vence em 22/12/2026.
- 26 rascunhos inseridos em produção (consulta: fila com 26, todos "rascunho").
- Remarcação dos Reels aplicada e listada.
- PDF do checklist conferido página por página em imagem. Página para empresas conferida em print de computador e de
  celular (sem rolagem lateral).
- **Não verificado:**
  - o envio real do formulário do checklist ao CRM (a página ainda não está no ar);
  - a regra nova da agenda em produção (entra no deploy do segundo commit desta tarefa);
  - a data exata da etapa das 42 horas: as fontes divergem entre 15 e 16/12, por isso os textos dizem "dezembro" e
    "dois meses depois da publicação".

## Decisões e porquês

- **Posts na fila como rascunho, nada aprovado:** a Jessica lê e aprova. A fila agora edita e aprova em lote.
- **Posts com link esperam o link estar no ar:** os que apontam para a página para empresas só saem depois que ela for publicada, e os de
  dezembro esperam os artigos agendados no blog.
- **Três afirmações tiradas dos posts por não serem firmes:**
  - teste de gravidez na dispensa (o TST tem decisões dos dois lados);
  - casos de transição da licença-paternidade;
  - contagem do art. 477 com aviso indenizado.
- **Três palavras trocadas:** "promoção" (no sentido de carreira) e "garantidos" travavam a checagem da OAB. Foram trocadas no texto, sem
  afrouxar o verificador.
- **Reels:**
  - pulei as datas especiais (20/11, 04/12, 25/12, 01/01);
  - em novembro mudei dois carrosséis para dias liberados;
  - em dezembro não mexi no feed, que tem data temática todo dia: alguns dias de Reels também têm o carrossel das 14h.
- **Publicar na página e ler impressões ficou para depois da aprovação do LinkedIn:** exige a Community Management API num
  app separado. Código feito antes da aprovação não teria como ser testado.
- **TikTok não foi mexido:** o código é de outra sessão, não está commitado, e a decisão de seguir é da Jessica.

## Pendente

- **Jessica:**
  - aprovar a página para empresas e o Checklist. Depois de aprovados, subir por SFTP a LP em `lp/`, o PDF em `assets/downloads/`, o sitemap e o llms.txt, e ligar a página "Assessoria Jurídica" a ela;
  - ler e aprovar os 26 posts em `/linkedin`.
- **Jessica ou Dra.:**
  - mandar o número da página da empresa (URL "Ver como administrador"), para as citações virarem menção;
  - pôr a capa na página;
  - convidar conexões para seguir a página;
  - pedir a Community Management API (seção 9 da estratégia).
- **Dra.:**
  - rotina de comentários de 15 minutos, 3 vezes por semana;
  - reconectar o LinkedIn até 22/12.
- **Jessica, sobre o TikTok:** decidir se segue. Para seguir é preciso: commitar o código da outra sessão, criar as rotas de conexão e o job, conectar a conta e pedir a auditoria do app (sem ela, só post privado).
- **Stories de 16/10:** 6 ficaram como "pronto" e não saíram, porque o Orbit não publica Stories. Decidir se descarta.

## Próxima sessão

1. Ler `docs/ESTRATEGIA_LINKEDIN_PME.md` e a seção de 23/10 em `docs/CONTEXTO_PROJETO.md`.
2. Se a página para empresas foi aprovada: publicar a LP e o PDF (SFTP, mesmo procedimento da skill `leticia-blog-artigo`, passo 4) e conferir
   o formulário ponta a ponta com um lead de teste marcado como teste no CRM.
3. Se chegou o número da página: trocar "Página do escritório: Letícia Barros Advocacia e Consultoria Jurídica"
   pela menção `@[Letícia Barros Advocacia e Consultoria Jurídica](urn:li:organization:<número>)` nos posts da fila.
- Skills: `codebase-design` (código), `contexto-orbit` (registro), `leticia-blog-artigo` (publicação no site).
