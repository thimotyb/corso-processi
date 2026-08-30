# 6.0 Manage Customer Service — esempio di processo APQC
*Fonte: APQC Process Classification Framework (PCF) Cross-Industry, versione 8.0.*
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 6.0 | Manage Customer Service |
| Process Group | 6.2 | Plan and manage customer service contacts (10379) |
| Process | 6.2.2 | Manage customer service problems, requests, and inquiries (10388) |

**Evento di innesco (trigger):** Ricezione di una richiesta, problema o quesito da parte del cliente
**Evento finale / output di processo:** Risposta fornita al cliente (ed eventuale opportunità di upsell trasmessa alle vendite)

## 2. Activity del processo (dal PCF)
| Codice | Activity |
|---|---|
| 6.2.2.1 | Receive customer problems, requests, and inquiries (10394) |
| 6.2.2.2 | Analyze problems, requests, and inquiries (13482) |
| 6.2.2.3 | Resolve customer problems, requests, and inquiries (10395) |
| 6.2.2.4 | Respond to customer problems, requests, and inquiries (10396) |
| 6.2.2.5 | Identify and capture upsell/cross-sell opportunities (16928) |
| 6.2.2.6 | Deliver opportunity to sales team (16937) |

> Nota didattica: il diagramma introduce un gateway esclusivo dopo l'analisi, per distinguere il ramo di risoluzione diretta dal ramo con opportunità di upsell/cross-sell — coerente con le Activity 6.2.2.5 e 6.2.2.6 del PCF.

## 3. Scomposizione in Task (esempio didattico)
Le Task non sono definite dal PCF a questo livello di dettaglio: la loro individuazione è compito dell'analista di processo. Esempio di scomposizione dell'Activity **"Analyze problems, requests, and inquiries (13482)"**:

1. Classificare la richiesta per tipologia e priorità
2. Verificare lo storico cliente e i contratti/SLA applicabili
3. Determinare se serve escalation tecnica o commerciale
4. Assegnare la richiesta all'operatore/team competente

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Cliente, canali di contatto (telefono, email, chat, portale) | Richiesta/problema/quesito del cliente, storico cliente, SLA contrattuali | Ricevere la richiesta → Analizzarla → Risolverla (o identificare upsell) → Rispondere al cliente → Trasmettere l'opportunità alle vendite | Richiesta risolta e risposta al cliente; eventuale lead commerciale | Cliente finale, team Vendite (per le opportunità identificate) |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel processo |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Richiesta cliente, storico contatti, SLA |
| Output | Risultato prodotto dal processo | Richiesta risolta, risposta al cliente, eventuale lead commerciale |
| Tempi | Durata tipica del processo | Minuti (chat) a giorni (problemi complessi), secondo SLA |
| Costi | Risorse economiche assorbite | Costo per contatto gestito (ore operatore, costo canale) |
| Volumi | Quantità/frequenza di esecuzione | Centinaia/migliaia di contatti al mese, secondo la base clienti |
| Ruoli | Attori coinvolti | Customer Service Representative, team Vendite (per upsell) |
| Sistemi | Applicativi/strumenti a supporto | CRM/ticketing, telefonia/chat, knowledge base |
| Vincoli | Limiti operativi o normativi | SLA contrattuali, normative su privacy/reclami |
| Rischi / colli di bottiglia | Punti critici del processo | Codice/categoria errata in analisi; escalation tardiva; opportunità di upsell non trasmesse alle vendite |

## 6. Scheda processo sintetica
- **Nome processo:** 6.2.2 Manage customer service problems, requests, and inquiries (10388)
- **Process owner:** Customer Service Manager
- **Obiettivo:** Gestire in modo tempestivo ed efficace richieste, problemi e reclami dei clienti, valorizzando anche eventuali opportunità commerciali
- **Confini:** da "Ricezione di una richiesta, problema o quesito da parte del cliente" a "Risposta fornita al cliente (ed eventuale opportunità di upsell trasmessa alle vendite)"
- **Ruoli coinvolti:** Customer Service Representative, team Vendite
- **Sistemi coinvolti:** CRM/ticketing, telefonia/chat, knowledge base
- **KPI:** Tempo medio di risoluzione; First Contact Resolution; customer satisfaction (CSAT); n. lead trasmessi alle vendite
- **Rischi / colli di bottiglia:** Errata classificazione della richiesta; mancato rispetto SLA; perdita di opportunità di upsell non intercettate

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/) (BPMN 2.0, non eseguibile: `isExecutable="false"`, pensato solo come diagramma di rappresentazione per l'aula).
Corsie (lane): Customer Service Representative, Team Vendite.
