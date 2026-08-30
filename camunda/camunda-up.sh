#!/usr/bin/env bash
# Avvia l'ambiente Camunda 8 del laboratorio e attende che sia pronto.
#
#   ./camunda-up.sh          # avvia e attende l'health check
#   ./camunda-up.sh --pull   # aggiorna prima le immagini
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

command -v docker >/dev/null || { echo "errore: docker non trovato." >&2; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "errore: serve Docker Compose v2." >&2; exit 1; }

[[ "${1:-}" == "--pull" ]] && docker compose pull

echo "Avvio dei container Camunda 8 (prima esecuzione: download immagini, alcuni minuti)..."
docker compose up -d

echo -n "Attendo che l'Orchestration Cluster sia healthy "
for _ in $(seq 1 90); do
  status="$(docker inspect -f '{{.State.Health.Status}}' corso-camunda 2>/dev/null || echo starting)"
  [[ "$status" == "healthy" ]] && { echo " ok"; break; }
  echo -n "."; sleep 2
done
echo

if [[ "${status:-}" != "healthy" ]]; then
  echo "L'avvio non risulta completato. Log recenti:" >&2
  docker compose logs --tail 40 orchestration >&2
  exit 1
fi

cat <<'INFO'

Camunda 8 e' pronto.

  Operate            http://localhost:8080/operate      (demo / demo)
  Tasklist           http://localhost:8080/tasklist      (demo / demo)
  API REST cluster   http://localhost:8080/v2
  MCP del cluster    http://localhost:8080/mcp/cluster
  Zeebe gRPC         localhost:26500

Deploy dal Camunda Desktop Modeler (plugin camunda-mcp):
  impostare  ZEEBE_ADDRESS=localhost:26500  prima di avviare il Modeler
  (nessuna credenziale: API non protetta in questa configurazione da laboratorio).

Stop:            ./camunda-down.sh
Stop + azzera:   ./camunda-down.sh --wipe
INFO
