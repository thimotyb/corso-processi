# Esempi di processo APQC — corso processi-MOCI06

Materiale di supporto per il corso **processi-MOCI06 - Classificazione e analisi dei processi industriali**
(sillabo: `sillabo_processi_MOCI06.docx`, cartella Dropbox `corsi/processi`).

Per ciascuno dei 7 domini APQC scelti, la cartella `esempi-apqc/<dominio>/` contiene:

- **`processo.md`** — collocazione nella gerarchia PCF (Category → Process Group → Process → Activity),
  scomposizione in Task (esempio didattico), SIPOC, matrice delle variabili di processo, scheda processo
  sintetica. Copre gli "Output attesi" del sillabo (mappa gerarchica, scheda processo, elenco attività/task,
  matrice delle variabili).
- **`processo.bpmn`** — rappresentazione BPMN 2.0 dello stesso processo, con corsie (swimlane) per ruolo.
  Non eseguibile (`isExecutable="false"`): pensato solo come diagramma da mostrare/discutere in aula,
  aprendolo in [Camunda Modeler](https://camunda.com/download/modeler/) (gratuito) — coerente con i
  "cenni a BPMN" previsti nel Giorno 2 del sillabo.

Tutte le gerarchie (Category/Process Group/Process/Activity) sono estratte dal documento originale
**APQC Process Classification Framework (PCF) — Cross-Industry, versione 8.0** (file
`K016809_APQC Process Classification Framework (PCF) - Cross-Industry - PDF Version 8.0.pdf`, presente
nella stessa cartella Dropbox). Il livello Task, che il PCF lascia alla singola organizzazione, è stato
aggiunto a scopo didattico ed è segnalato esplicitamente come tale in ogni scheda.

## Domini trattati

| Cartella | Category APQC | Process Group | Process |
|---|---|---|---|
| `01-vision-strategy` | 1.0 Develop Vision and Strategy | 1.1 Define the business concept and long-term vision | 1.1.1 Assess the external environment |
| `02-vendite` | 3.0 Market and Sell Products and Services | 3.4 Develop sales strategy | 3.4.1 Develop sales forecast |
| `03-acquisti` | 4.0 Manage Supply Chain for Physical Products | 4.2 Procure materials and services | 4.2.3 Select suppliers and develop/maintain contracts |
| `04-servizi` | 5.0 Deliver Services | 5.2 Manage service delivery resources | 5.2.2 Create and manage resource plan |
| `05-customer-service` | 6.0 Manage Customer Service | 6.2 Plan and manage customer service contacts | 6.2.2 Manage customer service problems, requests, and inquiries |
| `06-it` | 8.0 Manage Information Technology (IT) | 8.7 Create and manage support services/solutions | 8.7.8 Operate IT user support |
| `07-finance` | 9.0 Manage Financial Resources | 9.2 Perform revenue accounting | 9.2.2 Invoice customer |

I processi in **05-customer-service** e **06-it** includono un gateway esclusivo (ramo di escalation /
ramo di upsell) e sono i più indicati per introdurre in aula i costrutti di base BPMN oltre alla semplice
sequenza di attività.

## Come usare i file BPMN con Camunda

1. Installare [Camunda Modeler](https://camunda.com/download/modeler/) (desktop, gratuito).
2. Aprire il file `processo.bpmn` del dominio scelto: File → Open File.
3. I diagrammi sono pronti per la proiezione in aula così come sono; possono anche essere usati come
   punto di partenza per un'esercitazione (es. chiedere ai partecipanti di aggiungere un ramo di
   eccezione, un ruolo mancante o un secondo livello di Task).

Non è prevista alcuna esecuzione dei processi (nessun motore Camunda collegato): l'uso è puramente
di modellazione/rappresentazione, coerente con il taglio metodologico e non tecnico del corso.

## Ambiente Camunda 8 per il laboratorio

La cartella `camunda/` contiene una configurazione Docker Compose minima di Camunda 8.9 Self-Managed (Orchestration Cluster + Connectors, storage H2) per distribuire e osservare i processi in aula:

```bash
cd camunda
./camunda-up.sh      # avvia (Operate/Tasklist su http://localhost:8080, demo/demo)
./camunda-down.sh    # ferma
```

Dettagli e collegamento con il Camunda Desktop Modeler: `camunda/README.md` e `site/lab-camunda-mcp.html`.

## Plugin MCP nel Camunda Modeler

La cartella `modeler/` contiene gli script per installare il plugin `camunda-mcp` nel Camunda Desktop Modeler (server MCP su `localhost:3100` per generare i BPMN dai prompt):

```bash
cd modeler
./install-camunda-mcp.sh                 # da WSL (rileva %APPDATA% di Windows)
# oppure, su Windows:
#   powershell -ExecutionPolicy Bypass -File .\install-camunda-mcp.ps1
```

Dettagli: `modeler/README.md`.
