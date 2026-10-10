# Passagem de contexto — Orbit / Letícia Barros (09/10/2026)

Escrito para o próximo perfil do Claude que continuar este trabalho. Leia este arquivo
inteiro, depois `docs/CONTEXTO_PROJETO.md` (estado técnico completo) e os três documentos
de conteúdo citados abaixo. Tudo o que estava só na memória do perfil anterior está aqui.

## Quem é a usuária e como ela trabalha

- **Letícia Barros**, advogada solo em Vitória/ES (OAB/ES 39.948), áreas trabalhista,
  previdenciária, família e consumidor. Instagram `@adv.leticiabarros2`. Não é técnica,
  mas é precisa e exigente com design. A conta de e-mail que opera o Claude é da Jessica
  (equipe dela); as mensagens vêm em português, muitas vezes do celular.
- **Prefere ação direta**: não pedir confirmação a cada passo. Fazer, mostrar o resultado
  e perguntar só o que muda o rumo. Workaround a irrita quando ela quer a correção real.
- **Seja honesta sobre limites.** Ela pediu, com todas as letras: "se você não consegue
  fazer perfeito, preciso que me fale". Não entregue algo ruim fingindo que está bom.
- **Sempre commit + push + deploy** ao fim de cada pedido que mexa no repo, sem perguntar.
- **Ela vê as artes no celular**: mande link público da imagem
  (`https://api.orbit.advogadaleticiabarros.com.br/media/<arquivo>`) ou tira de prévia.
- **TDD e módulos profundos** em todo código novo (regra do `CLAUDE.md`).
- **Não programar nada sem ela aprovar.** Ela aprova a arte, depois pede para agendar.

## Documentos que mandam (leia antes de produzir conteúdo)

| Arquivo | O que define |
| --- | --- |
| `docs/MANUAL_CONTEUDO_REDES.md` | Regras OAB (Provimento 205/2021), Meta (máx. 5 hashtags, rótulo de IA), especificações, primeiro comentário obrigatório, checklist |
| `docs/ESTRATEGIA_CRESCIMENTO_ORGANICO.md` | Pilares, funil, plano de 90 dias, métricas, estudo de carrossel |
| `docs/PROCESSO_PRODUCAO_CARROSSEL.md` | Roteiro → fonte primária → arte; direção visual; **diagramação de peças únicas; regra de não usar recorte; padrão aprovado da pergunta** |

Prioridade em conflito: OAB > Meta > design system > criatividade.

## Identidade visual (não negociável)

- Café escuro `#231E1A`/`#1E1814`, dourado `#C9A962`, areia `#E8DED1`.
- **Fonte de títulos: EB Garamond (desde 09/10/2026), nunca Cormorant.** A família Cormorant
  desenha o circunflexo e o agudo altos e soltos da letra ("sobreviv^ência", "Voc^ê") e a
  Letícia reprovou: "esse erro não pode acontecer". Conferir acentos em toda prévia.
- **Faixas douradas no topo e no rodapé de toda peça** (`render_criativo._aplicar_acabamento_dourado`).
  Ela já reclamou quando sumiram: "não tire minha identidade".
- EB Garamond (títulos, itálico dourado no destaque) + Inter (texto, rótulos),
  algarismos alinhados (`font-variant-numeric: lining-nums`). Nada abaixo de 22 px.
- Acabamento fosco (granulação), logo dourada como marca d'água onde fizer sentido.
- Sem selo de verificado falso. Sem marca de terceiros nem texto em inglês nas fotos.

## PADRÃO APROVADO — Pergunta (v6, 09/10/2026)

Aprovado por ela como "nosso novo padrão". Regra gravada em `PROCESSO_PRODUCAO_CARROSSEL.md`.

- Foto inteira (Pexels) com **um único objeto ou gesto ligado ao tema**, luz real, sem recorte.
- Caixa de vidro fosco **centralizada na vertical e na horizontal**, faixa dourada
  "ME FAÇA UMA PERGUNTA" (ou "ME CONTA O QUE ACONTECEU" para relatos), pergunta em
  Cormorant com o trecho-chave em `<em>` (itálico dourado), perfil `adv.leticiabarros2`
  + "Advogada · <área>" no rodapé da caixa.
- Cabeçalho: "LETÍCIA BARROS / ADVOCACIA" à esquerda, "DIREITO DE / <ÁREA>" à direita.
- Pílula embaixo: "A RESPOSTA ESTÁ NA LEGENDA".
- Se o objeto ficar atrás da caixa, descer a foto (`desce`) ou trocar a foto.
- Código: gerador oficial `app/templates/pergunta_card.html` +
  `render_criativo.html_pergunta / renderizar_pergunta(foto_path=..., area=..., foto_posicao=..., brilho=..., desce=...)`
  (testes em `tests/test_render_criativo.py`). Produção em lote:
  `apps/api/_saida_producao_1510/pergunta_v6.py` (dicionário `PECAS`, fotos em
  `_fotos_pexels/<id>.jpg`).
- Prévia: https://api.orbit.advogadaleticiabarros.com.br/media/perguntas-v6-tira.jpg

## PADRÃO APROVADO — Capa de carrossel "Ouro editorial" (09/10/2026)

Escolhida pela Letícia entre 4 opções (`_saida_producao_1510/capas_opcoes.py`, prévia
`pecas/capas-opcoes/`). Ela reprovou capas "sem brilho, sem personalidade, fotos cortadas".
- Foto do tema em tela cheia, ORIGINAL em alta do Pexels (`_fotos_pexels/original-<chave>.jpg`,
  ~2400×3600), enquadrada pelo rosto detectado (OpenCV 4.10): pessoa à direita, rosto a ~34%
  da altura. Sem rosto frontal: foco manual em `FOCO_CAPA` (carrossel_v5.py).
- Tratamento de cinema, véu escuro à esquerda e embaixo, luz dourada no canto, grão.
- Título em ouro metalizado (EB Garamond 800, até 150 px, ajuste pela largura do texto),
  subtítulo itálico, apoio com marca-texto e pílula da lei, moldura fina com cantoneiras.
- Render em 2x (2160×2700) reduzido para 1080×1350 em todo o carrossel.
- Código: `capa_fecho.capa_ouro` + `capa_fecho.enquadrar`. Fechamento: retrato inteiro da
  Letícia em rodízio (`capa_fecho.fecho`). A Letícia não aparece na capa.

## PADRÃO APROVADO — Mito ou Lei (v3, 09/10/2026)

Aprovado por ela ("aprovado... salve como o novo padrão"). Regra completa no item 9 de
`PROCESSO_PRODUCAO_CARROSSEL.md`.

- Afirmação e explicação no **mesmo cartão de vidro**; selo-medalhão gravado (sem brilho de
  moeda) **encaixado no topo do cartão, centralizado**. Nunca entre os blocos (ela reprovou:
  quebra a leitura) e nunca no canto (a grade 3:4 do perfil corta as laterais).
- MITO: afirmação riscada com fio dourado fino + rótulo "A VERDADE". LEI: sem risco +
  "O QUE DIZ A LEI". Referência legal em pílula de uma linha. "✦ Salve para consultar
  quando precisar ✦" abaixo do cartão (meta da série: salvamentos).
- Código: `app/templates/mito_card.html` + `render_criativo.renderizar_mito_ou_lei(afirmacao,
  veredito, explicacao, referencia, identidade, caminho)`. Lote: `_saida_producao_1510/mito_v3.py`.
- Prévia: https://api.orbit.advogadaleticiabarros.com.br/media/mito-v3-lote.jpg

### Regra: recorte automático não entra em peça

Ela reprovou duas vezes recortes feitos com rembg (borda serrilhada, sombra residual,
objetos sem sentido, vários objetos). Não usar. Foto inteira com um objeto resolve.

### Regras de 10/10/2026: representatividade e objetos

- O público é miscigenado, com maioria negra: nas fotos de pessoas usar **mais pessoas negras**
  (identificação), sem deixar de usar pessoas brancas, só com menos frequência.
- Objetos dos carrosséis sempre ligados ao tema do slide (no v5: 1º objeto no item 01, 2º no 02,
  3º no 03). Só a biblioteca `_recortes` aprovada. Não usar `corte-caneta` (marca PARKER) nem
  `corte-ursinho` (na verdade é uma ponta de caneta; o ursinho é `obj-ursinho2`).

### Estudo das referências dela (09/10/2026)

Um objeto grande com luz dramática (maleta, ampulheta, cadeira de couro, papel amassado),
fundo atmosférico com grão, serifa grande + sans pequena, um destaque por peça, marca
discreta no topo, cartões de vidro flutuando. Usar isso nas próximas frentes.

## Estado do conteúdo (atualizado em 09/10/2026, noite)

- **Publicado**: 08/10 19h (relato assédio) — primeira publicação automática + primeiro comentário.
  09/10: frase do pet (9h) e pergunta do pet v6 (12h, post 18096433796113138, já com a arte nova;
  ela pediu para atrasar às 12h02, quando já tinha saído).
- **Agendado (ScheduledPost "pronto", Instagram, 12h)**: perguntas v6 de
  11/10 (abandono), 13/10 (férias da colega), 15, 17, 19, 21, 23, 25, 27, 29, 31/10 e 02/11.
  Também estão agendados os carrosséis/frases de 09–14/10 (programação anterior).
- **Agendado (Instagram, 19h)**: os 9 Mito ou Lei v3 aprovados em 09/10 — 16, 18, 20, 22,
  24, 26, 28, 30/10 e 01/11 (backup antes: `/root/orbit-backups/antes-mito-v3-20261009.sql.gz`).
- **Agendado depois (09/10)**: os 10 carrosséis v5 com capa Ouro editorial (18h, 15/10–02/11), o
  carrossel cômico da pensão (10/10 15h) e os 3 Reels da série gestante (15, 17 e 19/10, 20h30,
  publicação automática pelo Orbit).
- **Novembro aprovado em 10/10**: os 13 carrosséis, 13 frases e 13 perguntas foram aprovados por ela e
  agendados (12h/15h/18h, backup `/root/orbit-backups/antes-aprovar-nov-20261010.sql.gz`). Ainda em
  rascunho: os 15 Mito ou Lei. Os 4 artigos foram aprovados e agendados também em 10/10 (segundas 9h).
- **Novembro (03/11–02/12), em rascunho aguardando ela** (NÃO agendar sem aprovação): plano
  `docs/PLANO_CONTEUDO_NOV_2026.md`, produzido em 09/10 no padrão aprovado: 13 dias de tema
  (pergunta 12h, frase 15h, carrossel 18h), 15 Mito ou Lei (19h, dias pares) e 4 artigos de blog
  (segundas 9h). Fonte: `_saida_producao_1510/conteudo_nov.py` e `artigos_nov.py`; geradores
  `DADOS=nov carrossel_v5.py`, `pergunta_v6.py`, `producao_nov.py`, `capas_artigos_nov.py`;
  envio `subir_nov.py`. Reels de novembro: esperando os áudios dela (comandos do NotebookLM em
  `docs/REELS_NOTEBOOKLM_NOV_2026.md`).
- Para agendar uma peça aprovada: criar `ScheduledPost(canal="instagram", formato="post"
  ou "carrossel", data/hora de corpo.programacao, status="pronto")` e mudar a peça para
  `aprovado`. Modelo de script: `/c/tmp/v6/agendar.py` (copiado em
  `apps/api/_saida_producao_1510/agendar_perguntas_v6.py`).

## Próximos passos prováveis

1. Levar o padrão novo (foto inteira + objeto + vidro) para **frases** e **capas de
   carrossel**, mostrando prévia antes de trocar em massa (Mito ou Lei já feito: v3).
2. Depois da aprovação dela, agendar o resto do lote 15/10–02/11.
3. Escolha automática de foto Pexels por tema (hoje é curadoria manual por folha de contato).
4. Pendências antigas: em `CONTEXTO_PROJETO.md` → "Pendências conhecidas".
5. Pergunta em aberto dela: "tem como criar um servidor na VPS?" — respondi que sim,
   e perguntei o que ela quer rodar. Sem resposta ainda.

## Infra e acesso

- VPS Hostinger `179.199.128.68` (srv1921337), mesma máquina do CRM jurídico dela.
  Orbit em `/home/orbit-src` (git), Docker Compose em `deploy/vps` (serviços `api`, `db`).
- O perfil anterior usava a chave SSH `~/.ssh/orbit_vps` (comentário `claude-orbit-deploy`
  em `/root/.ssh/authorized_keys`). Comando:
  `ssh -i ~/.ssh/orbit_vps -o IdentitiesOnly=yes -o BatchMode=yes root@179.199.128.68 '...'`.
  Não testar outras chaves de `~/.ssh`. O novo perfil precisa da regra de permissão
  `Bash(ssh -i ~/.ssh/orbit_vps root@179.199.128.68:*)` e `Bash(scp -i ~/.ssh/orbit_vps:*)`.
- **Deploy da API**: backup do banco →
  `cd /home/orbit-src && git pull --ff-only && cd deploy/vps && docker compose up -d --build api`.
- **Backup**: `U=$(docker compose exec -T db printenv POSTGRES_USER); docker compose exec -T db pg_dumpall -U "$U" | gzip > /root/orbit-backups/<nome>.sql.gz`
  (conferir que o arquivo não tem 20 bytes).
- **Deploy do web**: `cd apps/web && npm run build && cp -r out/* /var/www/orbit-web/` (na VPS).
- **Mídia pública**: `docker compose cp <pasta>/. api:/app/media/` →
  `https://api.orbit.advogadaleticiabarros.com.br/media/<arquivo>`.
- **Scripts no banco**: copiar o .py para o container e rodar
  `docker compose exec -T -e PYTHONPATH=/app api python /tmp/<script>.py`
  (`from app.db import SessionLocal`).
- **Pexels**: chave criptografada no painel Chaves do Orbit;
  `obter_chave(db, tenant_id, "pexels")` dentro do container. CDN do Pexels exige User-Agent.
- Instagram: publicação e primeiro comentário automáticos (Graph API v21). Não é possível
  fixar comentário pela API. Facebook: primeiro comentário ainda é manual.
- VPS roda em UTC; os horários do Orbit são de Brasília (−3 h).
- Disco C: do Windows já encheu uma vez; limpar temporários próprios.

## Outros projetos da mesma usuária (fora deste repositório)

- **CRMLRTICIA** (CRM jurídico, Node, na mesma VPS em `/home/crma`, porta 3001): tem
  assistente por WhatsApp e briefing de audiência. Regras: commit+push automático,
  staging seletivo (app.js/whatsapp.js/styles.css costumam ter WIP alheio), toda mudança
  atualiza `docs/manual/` e o espelho no cofre Obsidian.
- **Giro Custom Car** (`C:\Users\prosy\girocustomcar`), negócio separado.
