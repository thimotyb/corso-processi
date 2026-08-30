#!/usr/bin/env bash
# Avvia un server statico locale per il sito del corso (cartella ./site)
# e apre il browser sulla home.
#
#   ./start-site.sh            # porta 8080
#   ./start-site.sh 9000       # porta a scelta
#   PORT=9000 ./start-site.sh  # idem, via variabile d'ambiente
#   NO_OPEN=1 ./start-site.sh  # non aprire il browser

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/site"
PORT="${1:-${PORT:-8080}}"
URL="http://localhost:${PORT}/index.html"

if [[ ! -f "$ROOT/index.html" ]]; then
  echo "errore: $ROOT/index.html non trovato. Eseguire prima:  python3 site/build_site.py" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "errore: serve python3 per il server statico." >&2
  exit 1
fi

# porta occupata? prova le successive
port_busy() { (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null && { exec 3>&- 3<&-; return 0; } || return 1; }
tries=0
while port_busy "$PORT" && (( tries < 20 )); do
  echo "porta $PORT occupata, provo $((PORT+1))"
  PORT=$((PORT+1)); tries=$((tries+1))
done
URL="http://localhost:${PORT}/index.html"

open_browser() {
  [[ "${NO_OPEN:-}" == "1" ]] && return 0
  local u="$1"
  if command -v wslview       >/dev/null 2>&1; then wslview "$u"
  elif command -v xdg-open     >/dev/null 2>&1; then xdg-open "$u" >/dev/null 2>&1
  elif command -v explorer.exe >/dev/null 2>&1; then explorer.exe "$u" 2>/dev/null || true
  elif command -v open         >/dev/null 2>&1; then open "$u"
  else echo "apri manualmente: $u"
  fi
}

echo "Sito del corso servito da:  $ROOT"
echo "URL:                        $URL"
echo "Premi Ctrl+C per fermare."
echo

# apri il browser dopo un attimo, quando il server è su
( sleep 1; open_browser "$URL" ) &

cd "$ROOT"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
