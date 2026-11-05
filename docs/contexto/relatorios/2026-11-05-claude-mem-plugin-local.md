# claude-mem como plugin local do projeto (05/11/2026)

## Pedido
A Jessica pediu para instalar uma lista de ferramentas "nesse projeto". Depois perguntou se o claude-mem estava funcionando aqui e, ao saber que não estava neste perfil, respondeu: "sim como reforço".

## Feito
- Plugin `claude-mem@thedotmack` 15.9.0 instalado com escopo `local`, no perfil `.claude-conta-2`, só para o `mktecosystem`.
- Configuração em `.claude/settings.local.json`, fora do git. Nenhum código do projeto mudou.
- O restante da lista foi tratado por outra sessão. Ver `C:\Users\prosy\relatorios-claude\2026-11-05-instalacao-ferramentas.md`.

## Verificado
- `claude plugin list`: plugin ativo, versão 15.9.0, escopo local.
- Processo em segundo plano na porta 37777 respondeu `status: ok`. Ele pertence à instalação do perfil `.claude`, não à deste perfil.
- Antes da instalação, o processo informava 0 sessões, 0 registros e nenhum projeto.
- Ocupa cerca de 105 MB neste perfil. O C: ficou com 7,3 GB livres.
- **Não verificado:** captura real de uma sessão deste projeto. O plugin foi instalado com a sessão já aberta; testar em sessão nova.
- **Não verificado:** se as regras de `MY-RULES.md` são injetadas nas sessões deste perfil.

## Decisões e porquês
- Escopo `local` em vez de usuário: as sessões do CRM jurídico que usam este perfil não são gravadas por este plugin. A Jessica aprovou "neste perfil" como reforço; o escopo local é o mais restrito que atende a este projeto. Se ela quiser em todos os projetos do perfil, basta instalar com escopo de usuário.
- O claude-mem não substitui `docs/CONTEXTO_PROJETO.md` nem a memória do Claude: é reforço.

## Pendente (decide a Jessica)
- `C:\Users\prosy\.claude-mem\MY-RULES.md` contém a regra "Publicar e fazer deploy por conta própria, sem depender da dona." Falta ela confirmar se é dela, em `localhost:37777`. Até lá, publicar e fazer deploy continuam exigindo confirmação dela.
- O banco `~/.claude-mem` é compartilhado entre os perfis e passa a poder guardar dados de clientes e acessos da VPS. Passagens sensíveis podem ir entre tags `<private>`, recurso citado na documentação e não testado aqui.
- Lista original: headroom (hoje há espaço para a versão sem `[all]`), ponytail (conflito com `codebase-design`), code setup e carrosséis e PDF (confirmar qual é), mailerfind (sem repositório; risco LGPD e OAB).

## Push do repositório (continuação do mesmo dia)
- **Causa do 403:** `alcancelegalmkt-collab` não tem escrita neste repositório; o Git não tinha conta própria para ele.
- **Feito, com o ok da Jessica:** credencial só deste repositório (`git config --local`) usando `advogadaleticiabarros-del`, no modelo da Agenda Online. O token vem do `gh` e não fica no arquivo. A conta ativa do `gh` não mudou.
- **Revisão antes do envio:** busca de senhas, chaves e dados pessoais nos 8 commits parados, e leitura dos documentos de maior risco. Nada desse tipo encontrado. A revisão não foi uma leitura integral de todos os arquivos.
- **Atenção:** o repositório é público. Relatórios e a revisão da fila do LinkedIn ficam visíveis, inclusive observações internas sobre posts ainda não publicados. Tornar privado depende da Jessica.

## Deploy do Orbit (continuação do mesmo dia)
- **Pedido:** "faça o deploy". VPS em `4910953` (28/10), 28 commits atrás; foi para `3e346fc` com `git pull --ff-only` e `docker compose up -d --build`.
- **Mudança real na API:** só `apps/api/app/services/blog_seo.py` (`@id` e redes da Dra. no schema dos artigos). Sem migração, dependência ou mudança no painel, por isso sem novo build do `apps/web`.
- **Verificado:** `tests/test_blog_seo.py` com 23 testes passando; `/health` 200 local e público; painel e CRM 200; sem erro no log da API logo após subir; disco da VPS em 30%.
- **Não verificado:** schema em um artigo novo publicado de fato; jobs agendados depois do reinício.
- **Fora deste deploy:** `lp/`, porque o site vai por outro caminho. Continuam sem commit na VPS: `apps/web/package-lock.json`, `_editorial_import/` e `deploy/vps/docker-compose.yml.bak`.

## Próxima sessão
Abrir uma sessão nova no `mktecosystem` e conferir em `http://127.0.0.1:37777/api/stats` se `sessions` e `observations` sobem. Se continuarem em 0, usar a skill `diagnosing-bugs`.
