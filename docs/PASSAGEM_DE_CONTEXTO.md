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
- **Faixas douradas no topo e no rodapé de toda peça** (`render_criativo._aplicar_acabamento_dourado`).
  Ela já reclamou quando sumiram: "não tire minha identidade".
- Cormorant Garamond (títulos, itálico dourado no destaque) + Inter (texto, rótulos),
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

### Regra: recorte automático não entra em peça

Ela reprovou duas vezes recortes feitos com rembg (borda serrilhada, sombra residual,
objetos sem sentido, vários objetos). Não usar. Foto inteira com um objeto resolve.

### Estudo das referências dela (09/10/2026)

Um objeto grande com luz dramática (maleta, ampulheta, cadeira de couro, papel amassado),
fundo atmosférico com grão, serifa grande + sans pequena, um destaque por peça, marca
discreta no topo, cartões de vidro flutuando. Usar isso nas próximas frentes.

## Estado do conteúdo (09/10/2026)

- **Publicado**: 08/10 19h (relato assédio) — primeira publicação automática + primeiro comentário.
- **Agendado (ScheduledPost "pronto", Instagram, 12h)**: perguntas v6 de 09/10 (pet),
  11/10 (abandono), 13/10 (férias da colega), 15, 17, 19, 21, 23, 25, 27, 29, 31/10 e 02/11.
  Também estão agendados os carrosséis/frases de 09–14/10 (programação anterior).
- **Rascunho, aguardando ela** (NÃO agendar): carrosséis v5, frases v2 e 9 Mito ou Lei v2
  do lote 15/10–02/11. Ela disse: "ainda não programe os demais, ainda vamos mudar
  algumas coisas". Doc de aprovação do lote:
  https://claude.ai/code/artifact/2f39add3-ba5e-4eb5-bc0e-47fae877428d
- Para agendar uma peça aprovada: criar `ScheduledPost(canal="instagram", formato="post"
  ou "carrossel", data/hora de corpo.programacao, status="pronto")` e mudar a peça para
  `aprovado`. Modelo de script: `/c/tmp/v6/agendar.py` (copiado em
  `apps/api/_saida_producao_1510/agendar_perguntas_v6.py`).

## Próximos passos prováveis

1. Levar o padrão novo (foto inteira + objeto + vidro) para **frases**, **capas de
   carrossel** e **Mito ou Lei**, mostrando prévia antes de trocar em massa.
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
