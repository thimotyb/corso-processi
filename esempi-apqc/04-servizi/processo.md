# 5.0 Deliver Services — esempio di processo APQC
*Fonte: APQC Process Classification Framework (PCF) Cross-Industry, versione 8.0.*
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 5.0 | Deliver Services |
| Process Group | 5.2 | Manage service delivery resources (20040) |
| Process | 5.2.2 | Create and manage resource plan (20050) |

**Evento di innesco (trigger):** Previsione della domanda di servizio disponibile (output di 5.2.1)
**Evento finale / output di processo:** Piano risorse pubblicato e capacità allocata ai team di delivery

## 2. Activity del processo (dal PCF)
| Codice | Activity |
|---|---|
| 5.2.2.1 | Define and manage skills taxonomy (20051) |
| 5.2.2.2 | Create resource plan (20052) |
| 5.2.2.3 | Match resource demand with capacity, skills, and capabilities (20053) |
| 5.2.2.4 | Collaborate with suppliers and partners to supplement skills and capabilities (20054) |
| 5.2.2.5 | Identify critical resources and supplier capacity (20055) |
| 5.2.2.6 | Monitor and manage resource capacity and availability (20056) |

## 3. Scomposizione in Task (esempio didattico)
Le Task non sono definite dal PCF a questo livello di dettaglio: la loro individuazione è compito dell'analista di processo. Esempio di scomposizione dell'Activity **"Match resource demand with capacity, skills, and capabilities (20053)"**:

1. Confrontare il fabbisogno previsto con la capacità disponibile per competenza
2. Individuare i gap di competenza/capacità per periodo
3. Proporre azioni di copertura (formazione, staffing, subappalto)
4. Aggiornare il piano risorse con le azioni approvate

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Team di forecasting della domanda (5.2.1), HR, fornitori/partner esterni | Previsione della domanda, mappa delle competenze, disponibilità risorse | Definire tassonomia competenze → Creare il piano risorse → Confrontare domanda e capacità → Coinvolgere fornitori/partner → Individuare risorse critiche → Monitorare capacità nel tempo | Piano risorse aggiornato e capacità allocata | Team di delivery del servizio, Program/Project Management |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel processo |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Previsione della domanda, mappa competenze, calendario disponibilità |
| Output | Risultato prodotto dal processo | Piano risorse per periodo/competenza |
| Tempi | Durata tipica del processo | 1-2 settimane per ciclo di pianificazione |
| Costi | Risorse economiche assorbite | Ore Resource Manager, eventuale costo di staffing esterno |
| Volumi | Quantità/frequenza di esecuzione | Mensile, per ciascuna linea di servizio |
| Ruoli | Attori coinvolti | Resource/Capacity Manager, HR, fornitori/partner |
| Sistemi | Applicativi/strumenti a supporto | Resource management tool, sistema HR, ERP |
| Vincoli | Limiti operativi o normativi | Disponibilità reale delle competenze critiche, vincoli contrattuali con i partner |
| Rischi / colli di bottiglia | Punti critici del processo | Gap di competenze non coperti in tempo; sovra/sotto-allocazione delle risorse |

## 6. Scheda processo sintetica
- **Nome processo:** 5.2.2 Create and manage resource plan (20050)
- **Process owner:** Resource/Capacity Manager
- **Obiettivo:** Garantire che la capacità e le competenze disponibili coprano la domanda di servizio prevista
- **Confini:** da "Previsione della domanda di servizio disponibile (output di 5.2.1)" a "Piano risorse pubblicato e capacità allocata ai team di delivery"
- **Ruoli coinvolti:** Resource/Capacity Manager, HR, fornitori/partner esterni
- **Sistemi coinvolti:** Resource management tool, sistema HR, ERP
- **KPI:** % copertura della domanda; tempo di risoluzione dei gap di competenza; utilizzo delle risorse
- **Rischi / colli di bottiglia:** Gap di competenze critiche non coperti; dipendenza da fornitori esterni; previsioni della domanda poco affidabili

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/) (BPMN 2.0, non eseguibile: `isExecutable="false"`, pensato solo come diagramma di rappresentazione per l'aula).
Corsie (lane): Resource/Capacity Manager, HR / Fornitori esterni.
