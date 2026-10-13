# Demo BPMN — APQC 2.1.1.4

**Attività APQC:** `2.1.1.4 Plan and develop cost and quality targets` (ID `10073`).
Gerarchia: `2.0 Develop and Manage Products and Services` → `2.1 Govern and manage product/service development program` → `2.1.1 Manage product and service portfolio`.

**Fonte:** `resources/K016808_APQC Process Classification Framework (PCF) - Cross-Industry - Excel Version 8.0.xlsx`, foglio `2.0`, riga 8 (anche nel foglio `Combined`, riga 138), colonne A–G.

La definizione APQC richiede di stabilire obiettivi di costo di sviluppo e standard di qualità per il portafoglio o per singole nuove offerte, preparare il piano della spesa, confrontare gli standard con offerte interne e concorrenti e coinvolgere la direzione e le funzioni di finanza, progettazione, produzione/erogazione e qualità. **APQC non prescrive i Task, i database, un gateway di approvazione o la loro sequenza:** questi sono elementi ipotizzati per la demo.

## Swimlane e ruoli ipotizzati

| Swimlane | Attività assegnate | Significato |
|---|---|---|
| Sistemi informativi (automazioni) | Estrarre baseline, simulare scenari, registrare target approvati | Funzioni applicative candidate all'automazione; gli eventi iniziale e finale sono collocati qui solo per leggibilità. |
| Responsabile prodotto/servizio | Definire target e piano di spesa, rivedere la proposta | Responsabilità della proposta, con contributi di Finance e Qualità. |
| Direzione e funzioni specialistiche | Valutare con direzione e funzioni, decidere se gli obiettivi sono validati | Coinvolge direzione, finanza/budget, progettazione, produzione o erogazione e controllo qualità. |

Il Data Store Reference denominato `PLM Sogei`, presente nella scheda del Modeler, è stato conservato e associato alla lettura della baseline. Il nome del sistema **non proviene dalla definizione APQC** e va confermato prima di usarlo come fonte reale.

## Scomposizione proposta

| Passaggio BPMN | Tipo | Responsabilità o fonti dati ipotizzate | Esito |
|---|---|---|---|
| Estrarre baseline interna | Service Task, automatizzabile | Lettura da **PLM/Portfolio DB** (offerte, specifiche, standard correnti), **ERP/Costing DB** (costi e budget storici), **QMS/Quality DB** (difetti, reclami, indicatori di qualità) | Baseline verificabile |
| Simulare scenari costo-qualità | Service Task, automatizzabile | Lettura da ERP/Costing e QMS; confronto con un **Market Intelligence DB** alimentato da benchmark concorrenti verificati | Scenari e scostamenti da valutare |
| Definire target e piano di spesa | User Task, umano | Product/Service Manager, Finance/Controller e Qualità | Proposta di target misurabili e spesa prevista |
| Valutare con direzione e funzioni | User Task, umano | Direzione, finanza, progettazione, produzione o erogazione, controllo qualità | Esito della valutazione e osservazioni |
| Obiettivi validati? | Gateway esclusivo | Decisione umana rappresentata con rami «Sì» e «No» | Approvazione o richiesta di revisione |
| Rivedere la proposta | User Task, umano | Responsabili di prodotto/servizio, Finance e Qualità | Nuova proposta da riesaminare |
| Registrare target approvati | Service Task, automatizzabile | Scrittura in **PLM/Portfolio DB** (specifiche), **PPM/Budget Planning DB** (piano della spesa), **QMS/Quality DB** (indicatori e soglie) | Target e budget disponibili, con versione e approvatori |

Le sigle dei sistemi indicano **tipi di fonti ipotetiche**, non applicazioni accertate: PLM = Product Lifecycle Management, ERP = Enterprise Resource Planning, QMS = Quality Management System, PPM = Project Portfolio Management. Il database dei concorrenti richiede una raccolta di dati lecita e curata; il diagramma non prevede raccolta automatica dal web. I Service Task indicano candidati all'automazione, ma il file BPMN è **non eseguibile** e non contiene connessioni reali ai database.

L'evento iniziale indica un portafoglio o idee di offerta da valutare. Non presuppone che i concetti siano già selezionati: i target di costo e qualità possono infatti alimentare la prioritizzazione dei concetti descritta nella vicina attività `2.1.1.3`.

**File:** `apqc-2.1.1.4-target-costo-qualita.bpmn`.
