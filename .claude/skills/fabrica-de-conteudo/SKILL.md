---
name: fabrica-de-conteudo
description: Automatiza o ciclo PDCA das redes sociais com as squads do ExpxAgents - planejamento do mês, produção semanal em lote (estáticos, carrosséis e vídeos), revisão humana, publicação e análise que alimenta o próximo planejamento, rodando sozinho por agendador. Use sempre que o usuário pedir para configurar, rodar, agendar, aprovar, ver o status, desativar, pausar, reativar ou cancelar o agendamento da fábrica, "reprovei", "ajusta os reprovados", "refaz as peças", falar em "fábrica de conteúdo", "ciclo semanal", "automatizar as squads", "rodar o ciclo", "pauta do mês", "lote da semana" ou "fila de agendamento", mesmo sem citar o nome da skill.
---

# Fábrica de Conteúdo

> **Regras obrigatórias:** `C:/Users/prosy/mktecosystem/docs/MANUAL_CONTEUDO_REDES.md` (OAB, Meta, specs, design system, checklist). Em conflito, o manual vence esta skill.


Esta skill conecta as squads de redes sociais do ExpxAgents num ciclo contínuo de quatro momentos: planejar (pauta e roteiros do mês), executar (produção em lote por semana), checar (análise do perfil) e agir (as melhorias entram no planejamento seguinte). O humano entra em dois pontos: aprovar a pauta do mês e revisar o lote da semana. O resto roda sozinho.

A ideia central: **calibrar primeiro, automatizar depois.** Automatizar um processo que ainda não gera peças boas só multiplica retrabalho. Por isso o modo `configurar` termina com uma rodada piloto aprovada pelo usuário, e só então registra o agendador.

## Os sete modos

Identifique o modo pelo pedido do usuário. Se vier de um agendador (prompt dizendo execução autônoma/agendada), execute `agendar` e depois `rodar`, nessa ordem, sem fazer perguntas.

| Modo | Quando | Interativo? |
|---|---|---|
| `configurar` | Uma vez por mês, ou na primeira vez | Sim. Pode e deve fazer perguntas |
| `rodar` | Toda semana, disparado pelo agendador ou manualmente | Não. Nunca pergunta nada |
| `agendar` | Depois que o usuário aprovou peças em `aprovados/`. Pode rodar sozinho pelo agendador | Opcional (ver o modo) |
| `ajustar` | O usuário reprovou peças ("reprovei", "ajusta"), ou há pastas em `_ciclo/reprovados/` | Não precisa perguntar: o `ajustes.txt` responde |
| `status` | A qualquer momento | Sim, só leitura |
| `desativar` | Quando quiser pausar ou cancelar tudo que foi programado | Sim, curto |
| `reativar` | Para voltar a rodar depois de desativar | Sim, curto |

Todos os arquivos de trabalho ficam em `_ciclo/` na raiz do projeto ExpxAgents (a pasta que contém `squads/` e `_expxagents/`). Os modelos dos arquivos estão em `assets/`. Se `_ciclo/` não existir, só o modo `configurar` pode criá-la.

Leia `references/squads-map.md` antes de agir em qualquer modo: ele diz quais squads entram em cada etapa, o que cada uma recebe e entrega, e como descobrir o código real de cada uma na instalação.

## Modo configurar

1. **Verificar o ambiente e mapear as squads.** Confirme que a raiz do projeto tem as pastas `squads/` e `_expxagents/`. O `squads/_index.yaml` é opcional: squads instaladas com `expxagents add` nem sempre entram nele, então nunca dependa dele. Os nomes de squad variam entre instalações, então trabalhe por função: siga o passo "Como descobrir no `configurar`" do mapa, proponha o código real de cada função (planejamento, produção estática, produção de vídeo e análise), peça a confirmação do usuário e grave o mapa na seção "Squads" do `config.md`, com o **código e o caminho da pasta** de cada squad. Se faltar uma função, pare e diga qual, em vez de improvisar uma substituta.
1b. **Checar os pré-requisitos antes de seguir**, porque cada instalação é diferente e uma falha aqui só aparece no meio da piloto. Monte uma lista do que está OK e do que falta, mostre ao usuário e resolva junto com ele antes do passo 2:
   - **Squads instaladas.** Para cada função sem squad, diga qual squad de referência do mapa resolve e peça que o usuário a instale pela plataforma ExpxAgents. Não siga sem as quatro funções (a de análise pode ficar desligada com `analise_ativa: nao`).
   - **Instalação íntegra.** `squad.yaml` com 0 bytes ou pasta `agents/` vazia indica instalação quebrada (comum em pastas sincronizadas como Google Drive ou OneDrive): peça para reinstalar.
   - **Identidade visual.** Abra o design system da squad de estáticos (ex.: `design-system.md`) e a pasta de logo dela. Se ainda estiver com valores de exemplo ("[Nome da Empresa]", cores padrão) ou sem logo, peça ao usuário a pasta ou o link da identidade da marca, extraia logo, cores e fontes e preencha com a confirmação dele. Sem isso a squad de estáticos bloqueia a produção.
   - **Chaves.** Verifique só pelo nome da variável, com `grep -q`, se o `.env` tem a chave do banco de imagens (ex.: `PEXELS_API_KEY`) e, se a publicação for real, o token da Meta. Nunca exiba valores. Se algum passo de uma squad mandar imprimir o `.env`, troque pela verificação por nome.
   - **Ferramentas de renderização.** Node, as dependências da squad (Puppeteer) e, para vídeo, FFmpeg. Se o `npm install` falhar dentro de pasta sincronizada (erro EBADF), instale numa pasta temporária local e aponte para ela.
   - **Manual de copy.** Pergunte se a empresa tem manual de estilo ou de copy e grave o caminho em `manual_de_copy` no config. Se não tiver, siga sem.
2. **Entrevistar o usuário** (use a ferramenta de perguntas se existir, senão converse). Colete e grave em `_ciclo/config.md`, a partir de `assets/config.template.md`: mês e objetivo, perfis, volume semanal por perfil e formato, dia e hora da rodada, ferramenta de IA usada (claude, codex ou opencode), pasta dos vídeos gravados, se a análise está ativa, se a publicação será real (há token da Meta no `.env`) ou apenas simulada em fila e, sendo real, se o `agendar` deve rodar direto ou pedir confirmação antes, e os templates de arte liberados. Essas respostas existem porque, no modo `rodar`, ninguém estará lá para responder às perguntas que as squads costumam fazer.
3. **Planejar o mês.** Se houver relatório de análise recente, leia-o antes e use as melhorias como insumo. Rode a squad de planejamento com os dados do config. Ela é interativa por natureza (aprova persona, referências e estratégia, revisa o pacote de conteúdo), e é por isso que este passo vive no `configurar`. Ao final, o calendário do mês e a copy de cada peça estão escritos e aprovados. Condense em `_ciclo/pauta-do-mes.md` (modelo em `assets/pauta-do-mes.template.md`) os temas de cada semana, o formato de cada peça e o caminho do arquivo de copy de cada uma; grave também em `planejador_output` do config a pasta onde o planejador salvou o resultado.
4. **Checkpoint 1: aprovação da pauta e da copy.** Mostre a pauta e espere a aprovação. É a única decisão estratégica do ciclo, então vale a atenção do usuário.
5. **Rodada piloto.** Produza uma peça de cada formato previsto (um estático, um carrossel e, se houver gravação disponível, um vídeo), seguindo o mesmo caminho do modo `rodar`, mas com o usuário acompanhando. Apresente o resultado e pergunte o que melhorar. Repita até o usuário dizer que o padrão está bom. Cada correção vira uma regra em `_ciclo/calibracao.md` (modelo em `assets/calibracao.template.md`).
6. **Por que a calibração vai num arquivo próprio.** O runner do ExpxAgents mantém só as 10 entradas mais recentes em `_memory/memories.md` de cada squad. Uma regra de qualidade gravada só lá se perde em poucas rodadas. Em `_ciclo/calibracao.md` ela fica para sempre e é lida a cada execução.
7. **Registrar o agendador**, somente depois da piloto aprovada e com a confirmação do usuário. Leia `references/agendador.md` e use os scripts de `scripts/`. Grave o caminho absoluto desta skill em `skill_path` e o nome da tarefa em `agendador_nome` no config. A tarefa agendada executa `agendar` e depois `rodar`.
8. **Iniciar o estado.** Crie `_ciclo/estado.md` a partir do modelo, com a semana 1 como próxima a produzir. Crie também as pastas `para-revisar/`, `aprovados/`, `reprovados/` e `arquivo/`, e copie `assets/como-reprovar.template.md` para `_ciclo/reprovados/COMO-REPROVAR.md`.

## Modo rodar (autônomo)

Este modo roda sem ninguém olhando. A regra que organiza todas as outras: **ele pode produzir e guardar, mas nunca publicar, agendar, apagar ou perguntar.** Produzir e guardar é reversível e barato de corrigir na revisão; o resto não é.

Sequência:

1. **Conferir se a fábrica está ativa e travar a execução.** Se o `estado.md` tiver `fabrica_ativa: nao`, encerre sem fazer nada e registre em `logs/`. Se existir `_ciclo/rodando.lock`, encerre sem fazer nada (outra rodada está ativa ou travou; registre em `logs/`). Senão crie o lock. Remova o lock ao terminar, mesmo com erro.
2. **Ler o contexto**, em uma leitura só: `_ciclo/config.md`, `_ciclo/estado.md`, `_ciclo/calibracao.md`, `_ciclo/pauta-do-mes.md` e, se existirem, `_ciclo/melhorias.md` e `_ciclo/feedback.md`.
2b. **Refazer reprovados.** Execute o modo `ajustar` antes de qualquer outra coisa, inclusive quando a semana alvo já foi produzida: peça reprovada pelo humano não pode esperar a semana seguinte.
3. **Evitar rodada duplicada.** Se o `estado.md` diz que a semana alvo já foi produzida, encerre e registre. Agendadores com "executar ao ligar" podem disparar duas vezes.
4. **Checar e agir.** Se `analise_ativa` for `sim`, rode a squad de análise e aplique as melhorias à semana alvo, conforme a seção "Análise" do mapa. Sem acesso aos dados, use o `feedback.md` manual (os melhores e piores posts da semana) e depois mova-o para `logs/`. Se nenhum dos dois existir, siga sem ajuste; a ausência de análise não pode travar a produção.
5. **Produzir o lote.** O `rodar` não escreve copy: a copy do mês já foi escrita e aprovada pelo planejamento. Para cada peça da semana alvo na pauta, siga o "Caminho de cada peça" do mapa, usando os códigos gravados na seção "Squads" do `config.md` (nunca um nome de memória). Passe a cada squad o conteúdo de `calibracao.md` como regras obrigatórias. Execute a squad lendo o protocolo do runner em `_expxagents/core/runner.pipeline.md`, usando o caminho gravado no `config.md` (sem depender de índice).
6. **Checkpoints das squads em modo autônomo.** As squads têm checkpoints de aprovação pensados para um humano. Aqui eles viram uma regra: se o avaliador da squad aprovou, a peça segue para `_ciclo/para-revisar/`; se reprovou, tente corrigir no máximo duas vezes (o limite evita laço infinito e gasto de tokens); se ainda reprovar, guarde em `_ciclo/para-revisar/_reprovadas/` com o motivo (essa pasta é de reprovação automática pelo avaliador; a `reprovados/` da raiz de `_ciclo/` é a do humano, tratada no modo `ajustar`). A aprovação final é sempre do humano, na revisão semanal.
7. **Arte só com template aprovado.** O agente escolhe entre os templates listados no config e nunca inventa layout. É o que mantém o visual consistente ao longo de dezenas de peças sem alguém olhando.
8. **Nunca pedir nada.** Se faltar uma informação (incluindo vídeo gravado para editar), registre em `estado.md` na seção de bloqueios, pule só essa peça e continue as demais. Uma peça travada não pode parar o lote.
9. **Fechar.** Atualize `estado.md` (semana produzida, peças por status, bloqueios, data da última análise, semana seguinte), grave um resumo de 10 linhas em `_ciclo/logs/AAAA-MM-DD.md` e libere o lock.

Organize `para-revisar/` por semana e perfil, por exemplo `para-revisar/2026-S41/perfil-x/carrossel-01/`, com um `LEIA-ME.md` na pasta da semana listando cada peça, o tema, o formato e se passou no avaliador de primeira ou após correção. Quem revisa deve conseguir decidir em poucos minutos.

## Modo ajustar

O humano revisa assim: gostou, move a pasta da peça de `para-revisar/` para `aprovados/`; não gostou, move para `reprovados/` e escreve um `ajustes.txt` dentro dela (uma linha por ajuste; instruções em `_ciclo/reprovados/COMO-REPROVAR.md`).

1. Se o `estado.md` tiver `fabrica_ativa: nao`, encerre e avise. Liste as pastas em `_ciclo/reprovados/`. Pasta sem `ajustes.txt` fica parada; avise o usuário qual é.
2. Para cada peça, leia o `ajustes.txt` e identifique se o ajuste é de copy (texto, gancho, CTA, legenda) ou de produção (arte, vídeo). Ajuste de copy: refaça a copy com a squad de planejamento, lendo antes `_memory/licoes-aprendidas.md` e `_memory/doutrina-de-copy.md` da squad, se existirem, e o manual de estilo de copy da instalação, se o config apontar um em `manual_de_copy` (quando existir, ele é eliminatório). Ajuste de produção: refaça com a squad do formato. Siga as mesmas regras do `rodar` (calibração, templates, avaliador, limite de 2 correções).
3. Devolva a peça refeita para `para-revisar/` com sufixo de versão (`-v2`, `-v3`) e um `o-que-mudou.md` que responde a cada linha do `ajustes.txt`. Mova a pasta reprovada original para `_ciclo/arquivo/`.
4. Linhas que começam com `SEMPRE:`, e ajustes que já apareceram em duas peças, viram regra em `calibracao.md`; regra de copy vai também para o topo de `licoes-aprendidas.md` da squad de planejamento, se ela tiver esse arquivo.
5. Atualize `estado.md` e diga ao usuário o que voltou para revisão. Nunca toque em `aprovados/`.

O modo `rodar` também executa este modo no começo, antes de produzir o lote da semana.

## Modo agendar

Pode ser usado de duas formas: na mão, quando o usuário pede "agendar", ou sozinho, quando o agendador do sistema o chama antes do `rodar`. A segunda forma só acontece se o config disser `agendamento.modo: real` e `confirmar_antes: nao`.

1. Se o `estado.md` tiver `fabrica_ativa: nao`, encerre e avise.
2. Leia `estado.md` e liste o que está em `_ciclo/aprovados/` (peças que o usuário moveu para lá depois da revisão). Se não houver nada, registre no log e encerre.
3. Nunca toque em `para-revisar/`. Só o que o humano aprovou é publicável.
4. Verifique se existe token da Meta no `.env` do projeto, **sem exibir o valor**. Se não existir, ou se o config diz "simulado", grave `_ciclo/fila-de-agendamento.md` com perfil, formato, data e horário sugeridos, legenda e caminho de cada arquivo, e pare aí.
5. Com token e `modo: real`: se o config diz `confirmar_antes: sim` (ou se o pedido veio de uma conversa e o usuário não disse para agendar direto), mostre a lista e peça confirmação. Se diz `confirmar_antes: nao`, siga sem perguntar: a aprovação humana já aconteceu quando a peça foi movida para `aprovados/`. Quando o agendador chamar este modo, nunca pergunte nada.
6. Se `publicacao_disponivel` no config for `nao`, trate como simulado: grave a fila, avise e pare. Senão, acione a etapa de publicação da squad de planejamento (ver o mapa), entregando as peças aprovadas. Distribua os horários conforme a grade do config, sem posts do mesmo perfil colados.
7. Mova cada peça agendada com sucesso para `_ciclo/agendados/` (assim ela nunca é agendada duas vezes). Peça que falhar continua em `aprovados/`, com o motivo registrado em `estado.md` e no log. Registre o que foi agendado em `estado.md`.

## Modo status

Somente leitura. Mostre: semana atual, o que está em produção, `para-revisar/`, `aprovados/`, `reprovados/` (e quais estão sem `ajustes.txt`), bloqueios abertos, data da última rodada e da última análise, peças em `agendados/` e se o agendador está registrado. Mostre também se a fábrica está ativa e o estado do agendador. Se a última rodada tem mais de 8 dias, avise.

## Modos desativar e reativar

**desativar** pausa tudo que foi programado, sem apagar nada do que foi produzido.

1. Leia `estado.md` e `config.md` (nome do agendador em `agendador_nome`, sistema operacional, ferramenta). Se o nome não estiver gravado, procure a tarefa `FabricaDeConteudo-Semanal` (Windows) ou a linha com `# fabrica-de-conteudo` no cron (Mac/Linux).
2. Mostre ao usuário o que será desligado (a tarefa encontrada e o que ela faz) e pergunte se quer **pausar** (padrão, reversível) ou **remover** de vez. Espere a resposta.
3. Execute com `scripts/desativar-agendador.ps1` (Windows) ou `scripts/desativar-agendador.sh` (Mac/Linux), usando a ação escolhida. Confirme depois, listando o agendador, que ele ficou desabilitado ou removido. Se algo falhar, diga qual comando o usuário pode rodar.
4. Grave `fabrica_ativa: nao` e `agendador_registrado: nao` (ou `pausado`) no `estado.md` e um registro curto em `logs/`. A partir daí `rodar` e `agendar` se recusam a trabalhar, mesmo se alguém os chamar.
5. Se existir `_ciclo/rodando.lock` com mais de 3 horas, é de uma rodada travada: apague-o e registre. Se for mais recente, avise que pode haver uma rodada em andamento e não apague.
6. Nunca apague `_ciclo/`, pauta, calibração, `para-revisar/`, `aprovados/` nem `agendados/`. Peças já agendadas na Meta não são canceladas por este modo; avise que isso se faz na própria Meta.

**reativar** faz o caminho inverso: confirme com o usuário, retome ou registre de novo o agendador (script de `registrar` se foi removido, ação `retomar` se foi pausado), grave `fabrica_ativa: sim` no `estado.md` e rode o modo `status` para mostrar a próxima rodada.

## Regras de segurança

- Nunca imprimir, copiar ou registrar em log o conteúdo de `.env` ou qualquer token.
- Nunca apagar arquivos de outras pastas do projeto. Esta skill só escreve dentro de `_ciclo/` e nas pastas de saída das próprias squads.
- Nunca alterar `squad.yaml` ou os prompts dos agentes para "melhorar" o resultado; melhorias vão para `calibracao.md`.
- O modo `rodar` nunca publica nem agenda. O modo `agendar` autônomo só mexe no que o humano colocou em `aprovados/`.
- No modo `rodar`, se algo inesperado acontecer (pasta ausente, índice quebrado), registre no log e encerre limpo em vez de tentar consertar.
