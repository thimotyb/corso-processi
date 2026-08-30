#!/usr/bin/env bash
# Ferma l'ambiente Camunda 8 del laboratorio.
#
#   ./camunda-down.sh          # ferma i container, mantiene i dati
#   ./camunda-down.sh --wipe   # ferma e cancella i volumi (dati persi)
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

if [[ "${1:-}" == "--wipe" ]]; then
  docker compose down --volumes
  echo "Container fermati e volumi rimossi."
else
  docker compose down
  echo "Container fermati. I dati restano nei volumi (riavvio con ./camunda-up.sh)."
fi
