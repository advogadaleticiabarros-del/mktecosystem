#!/usr/bin/env bash
# Pausa, retoma ou remove a rodada semanal da fabrica de conteudo no cron (Mac/Linux).
# Nao apaga nada da pasta _ciclo.
# Uso: bash desativar-agendador.sh pausar|retomar|remover
set -euo pipefail
ACAO="${1:?informe: pausar, retomar ou remover}"
MARCA="# fabrica-de-conteudo"
ATUAL="$(crontab -l 2>/dev/null || true)"
if ! printf '%s\n' "$ATUAL" | grep -qF "$MARCA"; then echo "Nenhuma linha '$MARCA' no cron. Nada a fazer."; exit 0; fi
case "$ACAO" in
  pausar)  printf '%s\n' "$ATUAL" | awk -v m="$MARCA" 'index($0,m) && substr($0,1,1)!="#"{print "#PAUSADO " $0; next}{print}' | crontab - ;;
  retomar) printf '%s\n' "$ATUAL" | sed 's/^#PAUSADO //' | crontab - ;;
  remover) printf '%s\n' "$ATUAL" | grep -vF "$MARCA" | crontab - || true ;;
  *) echo "Acao invalida: $ACAO" >&2; exit 1 ;;
esac
echo "Feito ($ACAO). Cron atual:"; crontab -l 2>/dev/null | grep -F "$MARCA" || echo "(nenhuma linha da fabrica)"
