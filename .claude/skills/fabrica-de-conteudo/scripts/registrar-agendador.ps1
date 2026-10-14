<#
  Registra a rodada semanal da fabrica de conteudo no Agendador de Tarefas do Windows.

  Uso (PowerShell):
    powershell -ExecutionPolicy Bypass -File registrar-agendador.ps1 `
      -ProjetoDir "C:\caminho\do\projeto" -SkillPath "C:\caminho\da\skill\fabrica-de-conteudo" `
      -Ferramenta claude -Dia Monday -Hora 07:00

  O que faz:
    1. Confere se a pasta do projeto, a skill e a ferramenta existem.
    2. Cria _ciclo\rodar-ciclo.ps1, o script que a tarefa executa.
    3. Registra a tarefa semanal com "executar assim que possivel se perder o horario".

  Antes de confiar na rodada agendada, rode "claude --help" (ou codex/opencode) e confira as
  opcoes de permissao da sua versao. Ajuste a secao PERMISSOES em _ciclo\rodar-ciclo.ps1 se precisar.
#>
param(
  [Parameter(Mandatory = $true)][string]$ProjetoDir,
  [Parameter(Mandatory = $true)][string]$SkillPath,
  [ValidateSet("claude", "codex", "opencode")][string]$Ferramenta = "claude",
  [ValidateSet("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")][string]$Dia = "Monday",
  [string]$Hora = "07:00",
  [string]$NomeTarefa = "FabricaDeConteudo-Semanal"
)

$ErrorActionPreference = "Stop"

if (-not ((Test-Path -LiteralPath (Join-Path $ProjetoDir "squads")) -and (Test-Path -LiteralPath (Join-Path $ProjetoDir "_expxagents")))) {
  throw "Nao encontrei as pastas squads e _expxagents em '$ProjetoDir'. Aponte para a raiz do projeto ExpxAgents."
}
if (-not (Test-Path -LiteralPath (Join-Path $SkillPath "SKILL.md"))) {
  throw "Nao encontrei SKILL.md em '$SkillPath'."
}
if (-not (Get-Command $Ferramenta -ErrorAction SilentlyContinue)) {
  throw "A ferramenta '$Ferramenta' nao foi encontrada no PATH. Abra um terminal onde ela funciona e rode de novo."
}

$cicloDir = Join-Path $ProjetoDir "_ciclo"
New-Item -ItemType Directory -Force -Path (Join-Path $cicloDir "logs") | Out-Null

$modelo = @'
# Gerado por registrar-agendador.ps1. Executado pelo Agendador de Tarefas a cada rodada.
$ErrorActionPreference = "Continue"
$projeto = '__PROJETO__'
$skill = '__SKILL__'
$ferramenta = '__FERRAMENTA__'

Set-Location -LiteralPath $projeto
$logDir = Join-Path $projeto "_ciclo\logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$data = Get-Date -Format "yyyy-MM-dd"
$saida = Join-Path $logDir ("saida-" + $data + ".txt")

$prompt = "Leia " + $skill + "\SKILL.md e execute, nesta ordem, o modo agendar e depois o modo rodar da skill fabrica-de-conteudo. Esta e uma execucao autonoma agendada: nao faca perguntas. O agendar so trata pecas ja aprovadas por um humano em _ciclo/aprovados/. O rodar nunca publica nem agenda. A pasta de trabalho e o projeto ExpxAgents atual."

# ---- PERMISSOES (confira com --help da sua versao) ----
# Libera leitura e escrita na pasta do projeto e o uso de shell para as squads de arte.
$permissoesClaude = @("--permission-mode", "acceptEdits", "--allowedTools", "Read,Write,Edit,Glob,Grep,Bash")
# -------------------------------------------------------

("[" + (Get-Date -Format s) + "] inicio (" + $ferramenta + ")") | Out-File -FilePath $saida -Append -Encoding utf8

switch ($ferramenta) {
  "claude"   { & claude -p $prompt @permissoesClaude *>> $saida }
  "codex"    { & codex exec $prompt *>> $saida }
  "opencode" { & opencode run $prompt *>> $saida }
}

("[" + (Get-Date -Format s) + "] fim (codigo " + $LASTEXITCODE + ")") | Out-File -FilePath $saida -Append -Encoding utf8
'@

$runner = Join-Path $cicloDir "rodar-ciclo.ps1"
$conteudo = $modelo.Replace("__PROJETO__", $ProjetoDir).Replace("__SKILL__", $SkillPath).Replace("__FERRAMENTA__", $Ferramenta)
Set-Content -LiteralPath $runner -Value $conteudo -Encoding UTF8

$acao = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument ("-NoProfile -ExecutionPolicy Bypass -File `"" + $runner + "`"")
$gatilho = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Dia -At $Hora
$config = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 3)

Register-ScheduledTask -TaskName $NomeTarefa -Action $acao -Trigger $gatilho -Settings $config `
  -Description "Rodada semanal da fabrica de conteudo (skill fabrica-de-conteudo, modo rodar)" -Force | Out-Null

Write-Host ""
Write-Host "Tarefa '$NomeTarefa' registrada: toda $Dia as $Hora, usando $Ferramenta."
Write-Host "Script da rodada: $runner"
Write-Host "Testar agora:  Start-ScheduledTask -TaskName $NomeTarefa"
Write-Host "Remover:       Unregister-ScheduledTask -TaskName $NomeTarefa -Confirm:`$false"
