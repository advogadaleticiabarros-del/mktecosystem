# 22/10/2026 — Tela "Google e site": todos os dados do Google no Orbit, com gestão

## Pedido
Depois da aprovação da API do Perfil da Empresa: ver todos os dados do Google no Orbit (Perfil, site, LPs, busca
orgânica, IAs), receber melhorias baseadas nos dados e gerir tudo pelo Orbit (publicar posts, responder
avaliações, editar o perfil).

## O que foi feito
- **Tela `/presenca` ("Google e site")** no menu, com abas Resumo, Melhorias, Perfil, Avaliações, Posts, Buscas,
  Site e IAs. A tela antiga `/avaliacoes` redireciona para a aba Avaliações. Na Visão Geral, o card "Google
  Analytics — Em breve" virou atalho e o card do Google ganhou "Abrir painel" e "Reconectar".
- **Coleta** (diária às 06h UTC e pelo botão "Atualizar agora"): perfil, atributos, desempenho de 90 dias
  (Busca, Maps, ligações, rotas, cliques no site, conversas), palavras buscadas (6 meses), avaliações, posts,
  fotos, verificação, botões, Google Analytics 4 (série, páginas por seção site/blog/LP/contato, origens,
  visitas vindas de IAs) e Search Console (consultas, páginas, posição). O Analytics e o Search Console são
  achados sozinhos pelo domínio do site do Perfil. O sitemap é reenviado ao Search Console a cada coleta.
- **Checagem do site por SFTP**: robôs de IA, llms.txt, schema da home, sitemap, páginas sem Analytics e sem
  descrição. É por SFTP porque a hospedagem tem anti-robô que barra clientes Python; os robôs de busca e de IA
  passam (testado com GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Googlebot e Bingbot: todos 200).
- **Melhorias**: regras puras sobre o painel, com prioridade, motivo, itens e "Fazer pelo Orbit". O status
  (feita/ignorada) fica em `recomendacoes_status`.
- **Gestão**: posts (IA escreve, agenda ou publica agora, apaga também do Google), respostas a avaliações (IA
  sugere, ela aprova), descrição e serviços (IA sugere a descrição), link do site com utm, botão "Agendar" e
  envio de fotos. Todo texto passa por `conformidade_oab.py` (promessa, autoelogio, gratuidade/preço, urgência,
  "especialista" como aviso e, nas respostas, sigilo profissional).
- **Migração** `d8e2f4a6b1c3` (tabelas `recomendacoes_status` e `google_posts`), aplicada em produção.

## Coleta real (22/10/2026, antes da reconexão)
- **Avaliações:** nota 5,0, 15 avaliações, 2 sem resposta, nenhuma nova em 30 dias.
- **Posts:** nenhum post. **Fotos:** 4, a última de 05/08. **Botão "Agendar":** não existe.
- **Desempenho (30 dias):** 50 aparições na Busca, 32 no Maps, 25 rotas e 1 ligação.
- **Site:** robôs de IA liberados, llms.txt ok, 68 páginas no sitemap, 80 arquivos .html. **23 páginas sem
  Analytics:** todas de `lp/`, `lp-v3/` e `areas/`.
- Analytics e Search Console aguardam a reconexão com as permissões novas.

## Estado do deploy
- **API:** commit a0bb2b0 no ar, com a migração aplicada. As correções seguintes (schema em lista e serviços
  padrão do Google fora do editor) estão no commit deste relatório e ainda precisam de redeploy.
- **Painel web:** o build e a cópia para `/var/www/orbit-web` na VPS foram bloqueados pela permissão de deploy
  desta sessão. Falta rodar `cd /home/orbit-src && git pull && cd apps/web && npm run build && cp -r out/* /var/www/orbit-web/`.

## Pendências
1. Deploy do painel web (e redeploy da API).
2. A usuária reconectar o Google (Visão Geral → Reconectar, marcando todas as caixas) e adicionar os escopos em
   "Acesso a dados" da tela de consentimento.
3. Colocar o código do Analytics (G-5B513VWB4D) nas 23 páginas de `lp/`, `lp-v3/` e `areas/`. Precisa de
   autorização para publicar no site.

## Atualização (fim do dia)
- Painel web publicado (`/presenca` no ar). A usuária reconectou o Google com os 3 escopos. A coleta voltou sem
  erros: GA4 `properties/472543377`, Search Console `sc-domain:advogadaleticiabarros.com.br`, sitemap reenviado.
- **Primeiros números (30 dias):** 215 visitas (eram 118), 4 visitas vindas de IAs em 90 dias (ChatGPT e Gemini).
  No Search Console (28 dias): 71 cliques, 5.468 aparições e posição média 7,2.
- A regra "buscas quase no topo" passou a valer a partir de 10 aparições (commit 9311d67, no ar).
- **Ainda pendente:** Analytics nas 23 páginas e pixel real na LP do guia. A gravação por SFTP no site foi barrada
  pela permissão da sessão e espera a regra `Bash(ssh -o BatchMode=yes -i ~/.ssh/orbit_vps root@179.199.128.68:*)`.
