## Contexto do projeto

Antes de qualquer trabalho neste repositório, leia `docs/CONTEXTO_PROJETO.md` — é o
resumo vivo do estado do projeto (arquitetura, o que está pronto, pendências,
decisões não-óbvias), mantido pra evitar reler tudo a cada sessão. Ao terminar uma
mudança relevante, atualize esse arquivo (ver `.claude/skills/contexto-orbit/SKILL.md`
para o que/como registrar).

## Conteúdo para Instagram e Facebook (obrigatório)

Toda peça de rede social (carrossel, frase, pergunta, estático, Reels, Stories, Facebook),
seja gerada por prompt do Orbit, template de render ou feita à mão, segue
`docs/MANUAL_CONTEUDO_REDES.md`: regras da OAB (Provimento 205/2021), políticas da Meta
(máx. 5 hashtags, originalidade, rótulo de IA), especificações (1080×1440 feed, áreas
seguras), uso do design system (contraste, escala tipográfica, nada abaixo de 22 px) e
checklist. Prioridade em conflito: OAB > Meta > design system > criatividade. Ao mexer em
prompts de geração (`app/routers/content.py`) ou templates (`app/templates/`), alinhar
com esse manual. Pedido da usuária em 08/10/2026.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Agent skills

### Issue tracker

Issues no GitHub Issues do repo (`gh` CLI). Ver `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: `GLOSSARY.md` + `docs/adr/` na raiz (criados sob demanda, não antecipadamente). Ver `docs/agents/domain.md`.

### Design de código (obrigatório)

Use a skill `codebase-design` em **todo** trabalho que crie ou reestruture código (módulo novo, refatoração, integração, feature que toque mais de um arquivo): projete módulos profundos (muito comportamento atrás de interface pequena), com dependências externas injetadas (APIs, banco, envio) pra permitir testar pela mesma interface que o resto do sistema usa. Combine com TDD. Pedido explícito da usuária (29/09/2026): "vamos usar em tudo que der".
