# 8.0 Manage Information Technology (IT) — esempio di processo APQC
*Fonte: APQC Process Classification Framework (PCF) Cross-Industry, versione 8.0.*
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 8.0 | Manage Information Technology (IT) |
| Process Group | 8.7 | Create and manage support services/solutions (20866) |
| Process | 8.7.8 | Operate IT user support (20921) |

**Evento di innesco (trigger):** Segnalazione di un problema/richiesta IT da parte di un utente
**Evento finale / output di processo:** Richiesta risolta e chiusa (o gestita in continuità/recovery se critica)

## 2. Activity del processo (dal PCF)
| Codice | Activity |
|---|---|
| 8.7.8.1 | Triage IT issues/requests (20922) |
| 8.7.8.2 | Provide IT resolution capabilities (20923) |
| 8.7.8.3 | Manage IT user requests (20925) |
| 8.7.8.4 | Escalate IT requests (20926) |
| 8.7.8.5 | Resolve IT issues/requests (20927) |
| 8.7.8.6 | Execute IT continuity and recovery action (20928) |

> Nota didattica: il diagramma introduce un gateway esclusivo dopo il triage per distinguere la risoluzione al primo livello (Service Desk) dall'escalation al secondo livello, coerente con le Activity 8.7.8.4 e 8.7.8.5 del PCF.

## 3. Scomposizione in Task (esempio didattico)
Le Task non sono definite dal PCF a questo livello di dettaglio: la loro individuazione è compito dell'analista di processo. Esempio di scomposizione dell'Activity **"Triage IT issues/requests (20922)"**:

1. Registrare il ticket con categoria, priorità e impatto
2. Verificare se si tratta di un incidente noto (knowledge base)
3. Determinare se è risolvibile al primo livello o richiede escalation
4. Assegnare il ticket alla coda/gruppo di competenza

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Utente interno, sistemi di monitoraggio IT (alert automatici) | Segnalazione utente o alert di sistema, storico ticket, knowledge base | Effettuare il triage → Risolvere al primo livello oppure Escalare → Gestire la richiesta → Risolvere → (se critico) eseguire continuità/recovery | Ticket risolto e chiuso, con eventuale azione di continuità operativa | Utente interno, Business owner del servizio impattato |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel processo |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Segnalazione utente, alert di monitoraggio, knowledge base |
| Output | Risultato prodotto dal processo | Ticket risolto e chiuso, azione di recovery se necessaria |
| Tempi | Durata tipica del processo | Minuti/ore per il primo livello; ore/giorni per escalation, secondo SLA |
| Costi | Risorse economiche assorbite | Costo per ticket gestito (ore Service Desk/specialisti) |
| Volumi | Quantità/frequenza di esecuzione | Decine/centinaia di ticket al giorno, secondo la dimensione dell'organizzazione |
| Ruoli | Attori coinvolti | Service Desk (primo livello), specialisti IT (secondo livello) |
| Sistemi | Applicativi/strumenti a supporto | ITSM/ticketing tool, knowledge base, sistemi di monitoraggio |
| Vincoli | Limiti operativi o normativi | SLA/OLA contrattuali, politiche di sicurezza IT |
| Rischi / colli di bottiglia | Punti critici del processo | Triage errato con escalation inutile o mancata; SLA non rispettati su incidenti critici |

## 6. Scheda processo sintetica
- **Nome processo:** 8.7.8 Operate IT user support (20921)
- **Process owner:** IT Service Desk Manager
- **Obiettivo:** Garantire una gestione tempestiva ed efficace delle richieste e degli incidenti IT segnalati dagli utenti
- **Confini:** da "Segnalazione di un problema/richiesta IT da parte di un utente" a "Richiesta risolta e chiusa (o gestita in continuità/recovery se critica)"
- **Ruoli coinvolti:** Service Desk (primo livello), specialisti IT (secondo livello)
- **Sistemi coinvolti:** ITSM/ticketing tool, knowledge base, sistemi di monitoraggio
- **KPI:** % risoluzione al primo livello; tempo medio di risoluzione; rispetto SLA; tasso di re-apertura ticket
- **Rischi / colli di bottiglia:** Escalation tardiva su incidenti critici; conoscenza insufficiente al primo livello; mancanza di piani di continuità per servizi critici

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/) (BPMN 2.0, non eseguibile: `isExecutable="false"`, pensato solo come diagramma di rappresentazione per l'aula).
Corsie (lane): Service Desk (1° livello), Specialisti IT (2° livello).
