# 3.0 Market and Sell Products and Services — esempio di processo APQC
*Fonte: APQC Process Classification Framework (PCF) Cross-Industry, versione 8.0.*
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 3.0 | Market and Sell Products and Services |
| Process Group | 3.4 | Develop sales strategy (10103) |
| Process | 3.4.1 | Develop sales forecast (10129) |

**Evento di innesco (trigger):** Avvio del ciclo periodico di pianificazione commerciale (mensile/trimestrale)
**Evento finale / output di processo:** Previsione di vendita approvata e distribuita a Sales, Operations e Finance

## 2. Activity del processo (dal PCF)
| Codice | Activity |
|---|---|
| 3.4.1.1 | Gather current and historic order information (10134) |
| 3.4.1.2 | Analyze sales trends and patterns (10135) |
| 3.4.1.3 | Generate sales forecast (10136) |
| 3.4.1.4 | Analyze historical and planned promotions and events (10137) |

## 3. Scomposizione in Task (esempio didattico)
Le Task non sono definite dal PCF a questo livello di dettaglio: la loro individuazione è compito dell'analista di processo. Esempio di scomposizione dell'Activity **"Generate sales forecast (10136)"**:

1. Selezionare il metodo previsionale (statistico, giudizionale o misto) per segmento/canale
2. Applicare il modello ai dati storici e correggere per stagionalità
3. Validare la previsione con Sales Management
4. Pubblicare la previsione nel sistema di pianificazione

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Sistema ordini/CRM, Marketing (calendario promozioni), Sales Management | Storico ordini, dati di mercato, calendario promozioni ed eventi | Raccogliere storico ordini → Analizzare trend e pattern di vendita → Analizzare promozioni/eventi passati e pianificati → Generare la previsione | Previsione di vendita per periodo/canale/segmento | Sales Management, Operations/Supply Chain (per il piano della domanda), Finance (budget) |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel processo |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Storico ordini, calendario promozioni, dati di mercato |
| Output | Risultato prodotto dal processo | Previsione di vendita per periodo/canale |
| Tempi | Durata tipica del processo | 3-5 giorni lavorativi per ciclo |
| Costi | Risorse economiche assorbite | Ore Sales Analyst, licenza tool di forecasting |
| Volumi | Quantità/frequenza di esecuzione | Mensile o trimestrale, per ciascuna linea di prodotto/canale |
| Ruoli | Attori coinvolti | Sales Analyst, Sales Management |
| Sistemi | Applicativi/strumenti a supporto | CRM, tool di demand forecasting, ERP |
| Vincoli | Limiti operativi o normativi | Qualità e completezza dei dati storici disponibili |
| Rischi / colli di bottiglia | Punti critici del processo | Previsioni distorte da eventi eccezionali; ritardo nella validazione da parte del management |

## 6. Scheda processo sintetica
- **Nome processo:** 3.4.1 Develop sales forecast (10129)
- **Process owner:** Sales Planning Manager
- **Obiettivo:** Produrre una previsione di vendita affidabile a supporto della pianificazione commerciale, della produzione e del budget
- **Confini:** da "Avvio del ciclo periodico di pianificazione commerciale (mensile/trimestrale)" a "Previsione di vendita approvata e distribuita a Sales, Operations e Finance"
- **Ruoli coinvolti:** Sales Analyst, Sales Management
- **Sistemi coinvolti:** CRM, tool di demand forecasting, ERP
- **KPI:** Accuratezza della previsione (forecast accuracy); tempo di ciclo; frequenza di revisione
- **Rischi / colli di bottiglia:** Dati storici incompleti; mancata considerazione di eventi/promozioni; disallineamento con Operations sul piano della domanda

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/) (BPMN 2.0, non eseguibile: `isExecutable="false"`, pensato solo come diagramma di rappresentazione per l'aula).
Corsie (lane): Sales Analyst, Sales Management.
