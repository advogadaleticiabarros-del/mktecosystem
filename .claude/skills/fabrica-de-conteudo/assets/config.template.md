# Configuração da fábrica de conteúdo

> Preenchido no modo `configurar`. O modo `rodar` lê este arquivo e nunca pergunta nada ao usuário, então tudo que uma squad poderia perguntar precisa estar respondido aqui.

## Geral
- mes: AAAA-MM
- objetivo_do_mes: (ex.: gerar leads para a oferta X / autoridade no tema Y)
- publico: (quem é o dono, sócio ou líder que o conteúdo precisa atingir)
- skill_path: (caminho absoluto da pasta desta skill; o agendador usa)
- ferramenta: claude | codex | opencode
- agendador_nome: FabricaDeConteudo-Semanal

## Squads (confirmadas pelo usuário no configurar)
- planejamento: (código e caminho da squad que planeja o mês e também publica, ex.: @expxagents-gabriel/planejador-de-conteudo)
- producao-estatica: (código e caminho da squad de carrosséis e estáticos, ex.: @squad-design/criativos-estaticos)
- producao-video: (código e caminho da squad de edição de vídeo, ex.: @gabriel/squad-editor)
- analise: (código e caminho da squad de análise, ex.: @expx/instagram-advisor)
- planejador_output: (pasta onde o planejamento salvou a copy aprovada)
- pasta_videos_gravados: (pasta onde ficam os vídeos brutos que a squad de vídeo vai editar)
- analise_ativa: sim | nao
- publicacao_disponivel: sim | nao (a squad de planejamento tem etapa de publicação na Meta?)
- reels_sem_gravacao: sim | nao (sim = reels só com texto animado e fundos de banco, sem gravação)
- manual_de_copy: (caminho do manual de estilo/copy da empresa, se houver) (nao, se não houver acesso aos dados do perfil)

## Perfis e volume semanal
| Perfil | Carrosséis | Reels (vídeo) | Posts estáticos |
|---|---|---|---|
| (perfil 1) | 0 | 0 | 0 |
| (perfil 2) | 0 | 0 | 0 |

## Rodada
- dia_da_rodada: segunda
- hora_da_rodada: 07:00
- semana_alvo: a semana seguinte à da rodada (o ciclo produz com antecedência, nunca para o mesmo dia)

## Arte
- templates_liberados: (lista de templates aprovados, ex.: t01, t03)
- banco_de_imagens: (ex.: Pexels, ou "apenas tipográfico")
- regra: o agente escolhe entre os templates liberados e nunca inventa layout

## Agendamento
- modo: simulado | real
- confirmar_antes: sim | nao (nao = o agendar publica sozinho o que está em aprovados/, só vale com modo real)
- grade_de_horarios: (ex.: 08h perfil 1 · 12h perfil 2 · 18h perfil 1)
- regra: nenhum post do mesmo perfil colado; no máximo 1 carrossel por perfil por dia
- token_meta: verificado no `.env` pelo nome da variável; o valor nunca é lido nem registrado

## Limites de execução
- tentativas_por_peca: 2
- se_bloqueio: registrar em estado.md, pular a peça e seguir com as demais
