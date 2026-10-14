<#
  Pausa, retoma ou remove a rodada semanal da fabrica de conteudo (Agendador de Tarefas do Windows).
  Nao apaga nada da pasta _ciclo.

  Uso:
    powershell -ExecutionPolicy Bypass -File desativar-agendador.ps1 -Acao pausar
    ... -Acao retomar
    ... -Acao remover
#>
param(
  [Parameter(Mandatory = $true)][ValidateSet("pausar", "retomar", "remover")][string]$Acao,
  [string]$NomeTarefa = "FabricaDeConteudo-Semanal"
)
$ErrorActionPreference = "Stop"
$t = Get-ScheduledTask -TaskName $NomeTarefa -ErrorAction SilentlyContinue
if (-not $t) { Write-Host "Tarefa '$NomeTarefa' nao encontrada. Nada a fazer."; exit 0 }
switch ($Acao) {
  "pausar"  { Disable-ScheduledTask -TaskName $NomeTarefa | Out-Null }
  "retomar" { Enable-ScheduledTask  -TaskName $NomeTarefa | Out-Null }
  "remover" { Unregister-ScheduledTask -TaskName $NomeTarefa -Confirm:$false }
}
$t = Get-ScheduledTask -TaskName $NomeTarefa -ErrorAction SilentlyContinue
if ($t) { Write-Host ("Tarefa '$NomeTarefa': estado " + $t.State) } else { Write-Host "Tarefa '$NomeTarefa' removida." }
