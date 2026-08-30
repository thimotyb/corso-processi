#!/usr/bin/env bash
# Installa il plugin camunda-mcp nel Camunda Desktop Modeler.
#
# Uso tipico (Modeler su Windows, questo script da WSL):
#   ./install-camunda-mcp.sh
#
# Opzioni:
#   --latest            installa l'ultima release invece della versione pinnata
#   --version vX.Y.Z    installa un tag specifico (default: v2.0.0)
#   --from-source       git clone + npm ci + npm run build (richiede Node >=20 e git)
#   --force             sovrascrive un'installazione esistente senza chiedere
#
# Percorso cartella dati del Modeler:
#   - Windows via WSL: rilevato da %APPDATA% (cmd.exe)
#   - override manuale: MODELER_DATA=/percorso/camunda-modeler ./install-camunda-mcp.sh
#   - Modeler nativo Linux: MODELER_DATA="$HOME/.config/camunda-modeler"
set -euo pipefail

REPO="JesseLeresche/Camunda-mcp"
VERSION="v2.0.0"
LATEST=0
FROM_SOURCE=0
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --latest) LATEST=1 ;;
    --version) VERSION="$2"; shift ;;
    --from-source) FROM_SOURCE=1 ;;
    --force) FORCE=1 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "opzione sconosciuta: $1" >&2; exit 2 ;;
  esac
  shift
done

# --- cartella dati del Modeler ------------------------------------------------
if [[ -z "${MODELER_DATA:-}" ]]; then
  if command -v cmd.exe >/dev/null 2>&1; then
    appdata_win="$(cmd.exe /c 'echo %APPDATA%' 2>/dev/null | tr -d '\r')"
    if [[ -n "$appdata_win" && "$appdata_win" != "%APPDATA%" ]]; then
      MODELER_DATA="$(wslpath -u "$appdata_win")/camunda-modeler"
    fi
  fi
fi
if [[ -z "${MODELER_DATA:-}" ]]; then
  echo "errore: impossibile determinare la cartella del Modeler." >&2
  echo "        rilancia con  MODELER_DATA=/percorso/camunda-modeler ./install-camunda-mcp.sh" >&2
  exit 1
fi
if [[ ! -d "$MODELER_DATA" ]]; then
  echo "errore: $MODELER_DATA non esiste." >&2
  echo "        avvia una volta il Camunda Modeler, oppure passa MODELER_DATA=..." >&2
  exit 1
fi

PLUGINS_DIR="$MODELER_DATA/resources/plugins"
DEST="$PLUGINS_DIR/camunda-mcp"
mkdir -p "$PLUGINS_DIR"

if [[ -d "$DEST" && $FORCE -eq 0 ]]; then
  read -r -p "Esiste gia' $DEST - sovrascrivo? [s/N] " a
  [[ "$a" =~ ^[sSyY]$ ]] || { echo "annullato."; exit 0; }
fi

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

if [[ $FROM_SOURCE -eq 1 ]]; then
  command -v git  >/dev/null || { echo "errore: git non trovato." >&2; exit 1; }
  command -v node >/dev/null || { echo "errore: Node.js non trovato (serve >=20)." >&2; exit 1; }
  echo "Clono e compilo dai sorgenti..."
  git clone --depth 1 "https://github.com/$REPO.git" "$WORK/src"
  ( cd "$WORK/src" && npm ci && npm run build )
  SRC="$WORK/src"
  echo "Nota: 'kb_search' (ricerca knowledge base) richiede better-sqlite3 ricompilato"
  echo "      per l'Electron del Modeler; i 12 tool di modellazione funzionano senza."
else
  if [[ $LATEST -eq 1 ]]; then
    VERSION="$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" | grep -oE '"tag_name": *"[^"]+"' | head -1 | cut -d'"' -f4)"
    [[ -n "$VERSION" ]] || { echo "errore: impossibile leggere l'ultima release da GitHub." >&2; exit 1; }
  fi
  URL="https://github.com/$REPO/releases/download/$VERSION/camunda-mcp-$VERSION.zip"
  echo "Release:  $VERSION"
  echo "Sorgente: $URL"
  curl -fSL -o "$WORK/pkg.zip" "$URL"
  ( cd "$WORK" && unzip -q pkg.zip )
  SRC="$WORK/camunda-mcp"
fi

[[ -f "$SRC/index.js" ]] || { echo "errore: struttura inaspettata, manca $SRC/index.js" >&2; exit 1; }

rm -rf "$DEST"
cp -r "$SRC" "$DEST"

VER="$(grep -oE '"version": *"[^"]+"' "$DEST/package.json" | head -1 | cut -d'"' -f4 || true)"
cat <<EOF

Installato in:  $DEST
Versione:       ${VER:-sconosciuta}

Prossimi passi:
  1. Riavvia il Camunda Desktop Modeler.
  2. Menu Plugins -> deve comparire "MCP Server: Running (port 3100)".
  3. Nel progetto, .mcp.json:
       { "mcpServers": { "camunda-modeler": { "type": "http", "url": "http://localhost:3100/mcp" } } }
  4. Deploy su Camunda 8: imposta ZEEBE_ADDRESS=localhost:26500 prima di avviare il Modeler.

Verifica rapida (a Modeler avviato):
  curl -s -X POST http://localhost:3100/mcp \\
    -H 'Content-Type: application/json' \\
    -H 'Accept: application/json, text/event-stream' \\
    -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
EOF
