---
name: contexto-orbit
description: Use no início de qualquer trabalho no projeto Orbit (mktecosystem) para carregar o estado atual do projeto sem precisar reler tudo, e SEMPRE ao final de uma mudança/implementação relevante para manter esse estado atualizado. Aplica-se a qualquer pedido sobre o Orbit, a advogada Letícia Barros, o CRM/SaaS de marketing, o blog dela, ou qualquer arquivo dentro deste repositório.
---

# Contexto Orbit

Este projeto mantém um único documento vivo com o estado real do projeto —
arquitetura, o que está pronto, o que está pendente, decisões não-óbvias — pra evitar
reler toda a base de código ou toda a conversa anterior a cada nova sessão. Isso
economiza tempo e tokens.

## Ao começar a trabalhar

1. Leia `docs/CONTEXTO_PROJETO.md` inteiro antes de fazer qualquer outra coisa
   (Read, Glob, git log) — ele já resume arquitetura, o que existe, o que falta e
   os gotchas conhecidos. Só investigue o código diretamente para o que este
   documento não cobrir ou para confirmar um detalhe específico antes de agir.
2. Se a tarefa tocar algo com spec/plano em `docs/superpowers/specs/` ou
   `docs/superpowers/plans/`, localize e leia o mais recente relacionado antes de
   propor qualquer mudança — não redecida algo que já foi decidido e documentado.
3. Trate o conteúdo do documento como ponto de partida, não como verdade absoluta:
   se algo parecer desatualizado ao mexer no código real, confie no código e depois
   corrija o documento.

## Ao terminar uma mudança

**Sempre que uma implementação, feature, bugfix não-trivial, decisão de design, ou
mudança de infraestrutura for concluída nesta sessão** (não precisa esperar o fim da
conversa inteira — atualize a cada marco fechado), edite
`docs/CONTEXTO_PROJETO.md`:

- **"O que está pronto"**: adicione o que acabou de ser entregue, com detalhe
  suficiente pra alguém sem contexto entender o que existe sem ler código.
- **"Pendências conhecidas"**: remova o que foi resolvido, adicione o que ficou
  descoberto/adiado durante o trabalho, reordene por proximidade de virar trabalho
  ativo.
- **"Decisões e observações não-óbvias"**: registre qualquer decisão que não seria
  óbvia só lendo o código (por que algo foi feito de um jeito específico, o que foi
  descartado e por quê, gotchas de infraestrutura descobertos).
- Atualize a data em "Última atualização" no topo do arquivo.

Sê específico e denso, mas não duplique o que já está documentado em
`docs/superpowers/specs/`/`docs/superpowers/plans/` — linke pra lá em vez de repetir
o conteúdo completo de uma spec.

Depois de editar, **commit o arquivo** junto com o resto da mudança (mesmo commit ou
um commit `docs:` separado, dependendo do fluxo que já estiver em andamento) — ele
deve viajar com o histórico do projeto, não ficar só local.

## O que NÃO colocar neste documento

- Histórico de commits ou quem mudou o quê — isso é `git log`/`git blame`.
- Detalhes de implementação que mudam a cada refactor (nomes exatos de função,
  número de linha) — isso fica em specs/planos versionados ou é lido do código.
- Estado efêmero da tarefa em andamento na conversa atual (isso é TodoWrite, não
  este arquivo).
