# Agendador: como o ciclo roda sozinho

A skill não fica rodando em segundo plano. Quem dispara a rodada semanal é o agendador do sistema operacional, que abre a ferramenta de IA em modo não interativo e manda um prompt curto. Entre uma rodada e outra nada fica aberto e nada consome tokens.

## Três níveis de gatilho

1. **Manual com lembrete (nível 1).** Sem instalar nada: o usuário cria um lembrete recorrente no calendário e, na hora, pede "rode a fábrica de conteúdo, modo rodar". Funciona em qualquer ferramenta e é o plano B se o agendador falhar.
2. **Agendador do sistema (nível 2).** Windows: Agendador de Tarefas. Mac/Linux: cron. É o que os scripts desta skill registram.
3. **Agendadores nativos das ferramentas.** Existem, mas cada ferramenta tem o seu e os que rodam na nuvem não enxergam a pasta local. Não fazem parte desta skill.

## O que o computador precisa para a rodada acontecer

- Ligado e com a sessão do usuário aberta no horário (ou no primeiro momento depois dele, no Windows, com a opção "executar assim que possível").
- Pasta do projeto acessível. Se o projeto está no Google Drive, o Drive precisa estar sincronizado e montado.
- Ferramenta de IA instalada e já logada (conta ou chave de API configurada).
- Permissões pré-liberadas para a pasta do projeto, porque no modo não interativo ninguém pode clicar em "permitir".

## Comando por ferramenta

Os scripts montam o comando certo. A tabela mostra o que eles fazem e o que conferir, porque as opções de permissão mudam entre versões. **Rode `--help` da sua ferramenta antes de confiar nas flags de permissão.**

| Ferramenta | Modo não interativo | Permissões (conferir na sua versão) |
|---|---|---|
| Claude Code | `claude -p "<prompt>"` | liberar leitura/escrita na pasta do projeto, por exemplo `--permission-mode acceptEdits` e lista de ferramentas permitidas |
| Codex | `codex exec "<prompt>"` | modo automático restrito à pasta de trabalho, conforme a versão |
| OpenCode | `opencode run "<prompt>"` | permissões no arquivo de configuração do OpenCode |

Escopo de permissão: dê à rodada acesso apenas à pasta do projeto ExpxAgents. Não use modos que liberam tudo sem limite de pasta.

## Prompt que o agendador envia

Curto e igual para qualquer ferramenta, porque a inteligência está na skill:

> Leia `{skill_path}/SKILL.md` e execute, nesta ordem, o modo `agendar` e depois o modo `rodar` da skill fabrica-de-conteudo. Esta é uma execução autônoma agendada: não faça perguntas. O `agendar` só trata peças que um humano já aprovou em `_ciclo/aprovados/` (e só publica de verdade se o config estiver em modo real sem confirmação). O `rodar` nunca publica nem agenda. A pasta de trabalho é o projeto ExpxAgents atual.

## Registrar (Windows)

No PowerShell, dentro da pasta do projeto:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill_path>\scripts\registrar-agendador.ps1" `
  -ProjetoDir "C:\caminho\do\projeto" -SkillPath "<skill_path>" `
  -Ferramenta claude -Dia Monday -Hora 07:00
```

O script cria `_ciclo\rodar-ciclo.ps1` (o que a tarefa executa) e registra a tarefa `FabricaDeConteudo-Semanal` com "executar assim que possível se perder o horário". Para testar sem esperar: `Start-ScheduledTask -TaskName FabricaDeConteudo-Semanal`. Para remover: `Unregister-ScheduledTask -TaskName FabricaDeConteudo-Semanal -Confirm:$false`.

## Registrar (Mac/Linux)

```bash
bash "<skill_path>/scripts/registrar-agendador.sh" "/caminho/do/projeto" "<skill_path>" claude 1 07:00
```

Os argumentos são: pasta do projeto, pasta da skill, ferramenta, dia da semana (0 a 6, sendo 1 = segunda) e hora. O cron **não recupera** rodadas perdidas com o computador desligado; nesse caso use o nível 1 como complemento.

## Como saber se rodou

- `_ciclo/logs/` ganha um arquivo por rodada, e o de hoje existe.
- `_ciclo/estado.md` mostra a data da última rodada e a semana produzida.
- O modo `status` resume tudo isso e avisa se a última rodada tem mais de 8 dias.
- O script grava também a saída bruta da ferramenta em `_ciclo/logs/saida-AAAA-MM-DD.txt`, útil quando algo falha.

## Custo

Cada rodada consome tokens do plano ou da API em que a ferramenta está logada, e o volume depende do número de peças da semana. Meça as duas primeiras rodadas reais e use isso como base antes de aumentar o volume.

## Pausar, remover e retomar

Pelo Claude: peça "desativar a fábrica de conteúdo" (e "reativar" para voltar). Direto no terminal, com os scripts:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill_path>\scripts\desativar-agendador.ps1" -Acao pausar
```

As ações são `pausar`, `retomar` e `remover` (Windows). No Mac/Linux: `bash desativar-agendador.sh pausar|retomar|remover`. Pausar comenta a linha do cron (ou desabilita a tarefa) e mantém tudo o mais; remover apaga só o agendamento. Nenhuma das ações toca em `_ciclo/`.
