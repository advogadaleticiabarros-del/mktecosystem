#!/usr/bin/env bash
# Registra a rodada semanal da fabrica de conteudo no cron (Mac/Linux).
#
# Uso:
#   bash registrar-agendador.sh <pasta-do-projeto> <pasta-da-skill> [ferramenta] [dia 0-6] [hora HH:MM]
# Exemplo:
#   bash registrar-agendador.sh "$HOME/expxagents" "$HOME/expxagents/.claude/skills/fabrica-de-conteudo" claude 1 07:00
#
# O cron nao recupera rodadas perdidas com o computador desligado. Se isso for um risco,
# use tambem o gatilho manual com lembrete (ver references/agendador.md).
# Confira as flags de permissao da sua ferramenta com --help e ajuste _ciclo/rodar-ciclo.sh se precisar.
set -euo pipefail

PROJETO="${1:?informe a pasta do projeto ExpxAgents}"
SKILL="${2:?informe a pasta da skill fabrica-de-conteudo}"
FERR="${3:-claude}"
DIA="${4:-1}"
HORA="${5:-07:00}"

[ -d "$PROJETO/squads" ] && [ -d "$PROJETO/_expxagents" ] || { echo "Nao achei squads/ e _expxagents/ em $PROJETO" >&2; exit 1; }
[ -f "$SKILL/SKILL.md" ] || { echo "Nao achei SKILL.md em $SKILL" >&2; exit 1; }
case "$FERR" in claude|codex|opencode) ;; *) echo "Ferramenta invalida: $FERR" >&2; exit 1 ;; esac
command -v "$FERR" >/dev/null 2>&1 || { echo "Ferramenta '$FERR' nao esta no PATH" >&2; exit 1; }

H=$((10#${HORA%%:*}))
M=$((10#${HORA##*:}))

mkdir -p "$PROJETO/_ciclo/logs"
RUNNER="$PROJETO/_ciclo/rodar-ciclo.sh"

cat > "$RUNNER" <<'EOF'
#!/usr/bin/env bash
# Gerado por registrar-agendador.sh. Executado pelo cron a cada rodada.
cd "__PROJETO__" || exit 1
mkdir -p _ciclo/logs
SAIDA="_ciclo/logs/saida-$(date +%F).txt"
PROMPT="Leia __SKILL__/SKILL.md e execute, nesta ordem, o modo agendar e depois o modo rodar da skill fabrica-de-conteudo. Esta e uma execucao autonoma agendada: nao faca perguntas. O agendar so trata pecas ja aprovadas por um humano em _ciclo/aprovados/. O rodar nunca publica nem agenda. A pasta de trabalho e o projeto ExpxAgents atual."

echo "[$(date -Iseconds)] inicio (__FERR__)" >> "$SAIDA"
case "__FERR__" in
  # ---- PERMISSOES (confira com --help da sua versao) ----
  claude)   claude -p "$PROMPT" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash" >> "$SAIDA" 2>&1 ;;
  codex)    codex exec "$PROMPT" >> "$SAIDA" 2>&1 ;;
  opencode) opencode run "$PROMPT" >> "$SAIDA" 2>&1 ;;
  # -------------------------------------------------------
esac
echo "[$(date -Iseconds)] fim (codigo $?)" >> "$SAIDA"
EOF

sed -i.bak \
  -e "s|__PROJETO__|$PROJETO|g" \
  -e "s|__SKILL__|$SKILL|g" \
  -e "s|__FERR__|$FERR|g" "$RUNNER" && rm -f "$RUNNER.bak"
chmod +x "$RUNNER"

MARCA="# fabrica-de-conteudo"
LINHA="$M $H * * $DIA /usr/bin/env bash \"$RUNNER\" $MARCA"
( crontab -l 2>/dev/null | grep -v "$MARCA" || true; echo "$LINHA" ) | crontab -

echo "Rodada registrada no cron: dia da semana $DIA as $HORA, usando $FERR."
echo "Script da rodada: $RUNNER"
echo "Para remover: crontab -l | grep -v '$MARCA' | crontab -"
