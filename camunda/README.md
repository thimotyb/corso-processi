# Ambiente Camunda 8 — laboratorio del corso

Configurazione **minima** di Camunda 8.9 Self-Managed per l'uso in aula:
Orchestration Cluster (Zeebe + Operate + Tasklist + API REST + MCP) e Connectors,
con storage secondario **H2 su file**. Nessun Elasticsearch, Keycloak, Web Modeler,
Optimize o Console. Non e' una configurazione di produzione.

Deriva dalla distribuzione ufficiale `camunda/camunda-distributions`
(release `docker-compose-8.9`, variante *lightweight*); `configuration/application-h2.yaml`
e `connector-secrets.txt` sono ripresi da quella distribuzione senza modifiche.

## Prerequisiti

- Docker Desktop con backend WSL2 — `docker` &ge; 20.10.16, `docker compose` &ge; 2.24
- circa 3–4 GB di RAM liberi

## Uso

```bash
cd camunda
./camunda-up.sh          # avvia e attende che il cluster sia pronto
./camunda-up.sh --pull   # come sopra, aggiornando prima le immagini
./camunda-down.sh        # ferma, mantenendo i dati
./camunda-down.sh --wipe # ferma e azzera i dati
```

In alternativa, comandi Docker Compose diretti dalla cartella `camunda/`:

```bash
docker compose up -d
docker compose ps
docker compose logs -f orchestration
docker compose down
```

## Endpoint

| Servizio | URL | Credenziali |
|---|---|---|
| Operate | http://localhost:8080/operate | `demo` / `demo` |
| Tasklist | http://localhost:8080/tasklist | `demo` / `demo` |
| API REST del cluster | http://localhost:8080/v2 | API non protetta |
| MCP del cluster (operativo) | http://localhost:8080/mcp/cluster | — |
| Zeebe gRPC | localhost:26500 | plaintext |

## Collegamento con il Camunda Desktop Modeler

Il Modeler e' installato sul PC (non in Docker). Per distribuire un diagramma con il
tool `deploy_process` del plugin `camunda-mcp`, impostare prima di avviare il Modeler:

```
ZEEBE_ADDRESS=localhost:26500
```

Non servono `ZEEBE_CLIENT_ID` / `ZEEBE_CLIENT_SECRET`: in questa configurazione da
laboratorio l'API e' non protetta e la comunicazione gRPC e' in chiaro. La guida
`../site/lab-camunda-mcp.html` descrive l'intero flusso.

## File

| File | Contenuto |
|---|---|
| `docker-compose.yml` | stack minimo: `camunda-data-init`, `orchestration`, `connectors` |
| `.env` | versioni immagini pinnate (8.9.17 / 8.9.9) e parametri di rete |
| `configuration/application-h2.yaml` | config del cluster: auth basic `demo/demo`, API non protetta, storage H2, MCP attivo |
| `connector-secrets.txt` | segreti per i Connectors (vuoto: aggiungere `NOME=VALORE` per riga) |
| `camunda-up.sh` / `camunda-down.sh` | script di avvio e arresto |

## Aggiornare le versioni

Modificare `CAMUNDA_VERSION` e `CAMUNDA_CONNECTORS_VERSION` in `.env`. I valori
correnti seguono la release ufficiale `docker-compose-8.9`.
