# Mapa das squads da fábrica

Consulte este arquivo nos modos `configurar`, `rodar` e `agendar`.

## O ciclo PDCA das redes sociais

A fábrica roda o ciclo que o GT apresenta: planejar, executar, checar e agir, recomeçando depois da análise.

| Etapa | Squad de referência | O que faz | Quando roda |
|---|---|---|---|
| 01 Planejar | `@expxagents-gabriel/planejador-de-conteudo` | Pesquisa o nicho, define as pautas e roteiriza cada peça do calendário do mês | Mensal, no `configurar` |
| 02 Executar (estático e carrossel) | `@squad-design/criativos-estaticos` | Produz os carrosséis e os posts estáticos, peça por peça | Semanal, no `rodar` |
| 03 Executar (vídeo) | `@gabriel/squad-editor` | Edita os vídeos e Reels previstos no calendário | Semanal, no `rodar` |
| 04 Publicação | etapa de publicação da squad de planejamento, **se a versão instalada tiver** (ver "Publicação" abaixo) | Agenda cada peça aprovada na Meta; sem essa etapa, o `agendar` gera só a fila | Depois da aprovação, no `agendar` |
| 05 Checar e agir | `@expx/instagram-advisor` | Analisa os relatórios do perfil e aponta as melhorias para o próximo planejamento | Semanal, no início do `rodar`, e como insumo do próximo `configurar` |

O planejador aparece duas vezes: no começo, para planejar e escrever a copy, e na publicação, para agendar. A análise fecha o círculo: o que ela aponta entra no planejamento seguinte e nas regras de calibração.

## Squads por função (não por nome)

Os códigos acima são os de referência, mas a instalação de cada pessoa pode ter outros. Por isso a skill trabalha por **função** e grava no `config.md` o código real de cada uma, confirmado pelo usuário no `configurar`. No `rodar` e no `agendar`, use sempre o código gravado no config, nunca um nome de memória.

| Função no config | Reconheça pela descrição |
|---|---|
| `planejamento` | Planeja o conteúdo do mês: nicho, pautas, roteiros, calendário. Também executa a publicação |
| `producao-estatica` | Produz carrosséis e posts estáticos |
| `producao-video` | Edita vídeos e Reels |
| `analise` | Analisa relatórios e métricas de perfil do Instagram |

**Como descobrir no `configurar`:**

1. Varra a pasta `squads/` atrás de arquivos `squad.yaml`, inclusive dentro de pastas com escopo (por exemplo `squads/@squad-design/criativos-estaticos/`). De cada um, leia `code`, `name` e `description`. Se existir `squads/_index.yaml`, use-o como apoio para nomes e aliases, mas ele pode estar desatualizado ou não listar squads instaladas por `expxagents add`. Em seguida, para cada função, liste as candidatas.
2. Se houver uma única candidata clara, proponha-a. Se houver várias ou nenhuma, mostre as encontradas e peça que o usuário escolha ou informe o código.
3. Confirme o mapa completo antes de gravar. Uma squad errada contamina o ciclo inteiro.
4. Grave no `config.md` o código e o caminho da pasta de cada squad escolhida. Se algum `squad.yaml` estiver vazio (0 bytes), a instalação falhou: avise o usuário, sugira reinstalar a squad fora do Google Drive e não tente usar essa squad.

## Caminho de cada peça no modo rodar

O `rodar` não escreve copy: a copy do mês foi escrita e aprovada pelo planejamento. Para cada peça da semana alvo na `pauta-do-mes.md`:

1. **Localizar a copy aprovada** no output do planejador (`planejador_output` no config).
2. **Produzir conforme o formato**, com as regras de `calibracao.md` como obrigatórias:
   - **Carrossel e estático:** envie a copy à squad `producao-estatica`.
   - **Vídeo e Reels:** se o config disser `reels_sem_gravacao: sim`, use o caminho da squad de vídeo que gera vídeo só com texto animado e fundos de banco (sem material gravado) e não procure brutos. Caso contrário, a squad `producao-video` edita a partir de vídeos gravados. Procure os brutos em `pasta_videos_gravados` do config. Se a gravação ainda não existir, registre o bloqueio "aguardando gravação" e siga com as outras peças; não tente editar sem material.
3. **Guardar** o resultado em `_ciclo/para-revisar/`.

Confirme na primeira rodada que a squad de estáticos entrega o arquivo final (imagem pronta). Se entregar apenas especificação, marque a peça como `render: pendente` e não improvise uma renderização: é exatamente isso que gera arte feia em lote.

## Publicação (modo agendar)

Nem toda versão da squad de planejamento tem etapa de publicação. No `configurar`, abra o `squad.yaml` da squad de planejamento e procure um step que publique ou agende na Meta; grave no config `publicacao_disponivel: sim` ou `nao`. Se for `nao`, o modo `agendar` funciona sempre como simulado (gera a fila) e você avisa o usuário de que a publicação é manual pelo Meta Business Suite. Nunca improvise uma publicação. O `agendar` só aciona essa etapa com peças que o usuário moveu para `aprovados/`, com token da Meta presente no `.env` e com confirmação do usuário. Sem token, o `agendar` grava a fila em `_ciclo/fila-de-agendamento.md` e para.

## Análise (checar e agir)

No início de cada `rodar`, se `analise_ativa` for `sim` no config, rode a squad `analise`. Ela depende de dados do perfil (normalmente acesso à conta ou relatórios exportados). Se faltar acesso, registre no log, use o `feedback.md` manual como alternativa e siga. Do relatório mais recente, extraia até três melhorias concretas, acrescente-as em `_ciclo/melhorias.md` com a data e aplique-as à semana alvo (temas, ganchos, formatos). Melhorias que se repetirem em duas análises viram regra em `calibracao.md`.

## Adaptações do modo autônomo

O runner do ExpxAgents já prevê execução por agendador: correntes (`chain`) rodam sem confirmação e as travas de qualidade só registram problemas. Os checkpoints de aprovação declarados em `squad.yaml` continuam existindo, por isso a skill define a sua própria regra (ver "Checkpoints das squads em modo autônomo" no `SKILL.md`).

A etapa final do planejador também mapeia as squads de produção e pergunta se deve despachar as demandas. O `rodar` chama as squads de produção diretamente, porque ele não pode responder a essa pergunta.

## Perguntas que as squads fazem e de onde vêm as respostas

Squads costumam perguntar quantidade, formato, público e tom no início. No `rodar` essas respostas vêm de `_ciclo/config.md` (volume, perfis e mapa de squads), `_ciclo/pauta-do-mes.md` (tema e formato) e `_ciclo/calibracao.md` (tom e regras). Se uma squad fizer uma pergunta que nenhum desses arquivos responde, trate como bloqueio da peça (regra 8 do modo `rodar`).
