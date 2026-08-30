# 1.0 Develop Vision and Strategy — esempio di processo APQC
*Fonte: APQC Process Classification Framework (PCF) Cross-Industry, versione 8.0.*
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 1.0 | Develop Vision and Strategy |
| Process Group | 1.1 | Define the business concept and long-term vision (17040) |
| Process | 1.1.1 | Assess the external environment (10017) |

**Evento di innesco (trigger):** Avvio del ciclo di pianificazione strategica annuale
**Evento finale / output di processo:** Report di analisi ambientale e competitiva consegnato al team di Pianificazione Strategica

## 2. Activity del processo (dal PCF)
| Codice | Activity |
|---|---|
| 1.1.1.1 | Identify competitors (19945) |
| 1.1.1.2 | Analyze and evaluate competition (10021) |
| 1.1.1.3 | Identify potential product or service alternatives (21421) |
| 1.1.1.4 | Identify economic trends (10022) |
| 1.1.1.5 | Identify political and regulatory factors (10023) |
| 1.1.1.6 | Identify environmental factors (10027) |
| 1.1.1.7 | Identify social and cultural changes (10026) |
| 1.1.1.8 | Assess new technologies (10024) |
| 1.1.1.9 | Analyze demographics (10025) |
| 1.1.1.10 | Evaluate intellectual property (16790) |

> Nota didattica: nel diagramma BPMN le 10 Activity reali sono raggruppate in 4 task rappresentativi, per mantenere il diagramma leggibile in aula; la tabella qui sopra riporta invece l'elenco completo e autentico del PCF.

## 3. Scomposizione in Task (esempio didattico)
Le Task non sono definite dal PCF a questo livello di dettaglio: la loro individuazione è compito dell'analista di processo. Esempio di scomposizione dell'Activity **"Analyze and evaluate competition (10021)"**:

1. Raccogliere dati su prezzi, prodotti e canali dei concorrenti diretti
2. Confrontare posizionamento, quote di mercato e proposta di valore
3. Sintetizzare punti di forza e debolezza in una matrice competitiva
4. Individuare minacce e opportunità competitive da riportare nel report finale

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Fonti di mercato (report di settore, osservatori economici), direzione commerciale, ufficio studi esterno | Dati di mercato, report settoriali, dati vendite interni, normative vigenti | Identificare concorrenti → Analizzare competizione e alternative → Analizzare trend macro (economici, normativi, ambientali, sociali) → Valutare tecnologie e demografia → Valutare IP → Consolidare report | Report di analisi ambientale e competitiva | Team di Pianificazione Strategica (Process 1.1.4 Establish strategic vision), Direzione Generale |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel processo |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Report di settore, dati vendite, normative |
| Output | Risultato prodotto dal processo | Report di analisi ambientale e competitiva |
| Tempi | Durata tipica del processo | 3-4 settimane per ciclo di pianificazione |
| Costi | Risorse economiche assorbite | Ore analista + eventuali licenze di ricerche di mercato |
| Volumi | Quantità/frequenza di esecuzione | 1-2 volte l'anno (ciclo strategico) |
| Ruoli | Attori coinvolti | Market Intelligence Analyst, Strategic Planning Team |
| Sistemi | Applicativi/strumenti a supporto | BI/market intelligence tool, repository documentale, CRM |
| Vincoli | Limiti operativi o normativi | Disponibilità e affidabilità delle fonti esterne |
| Rischi / colli di bottiglia | Punti critici del processo | Dati di mercato obsoleti o incompleti; ritardo nella sintesi finale |

## 6. Scheda processo sintetica
- **Nome processo:** 1.1.1 Assess the external environment (10017)
- **Process owner:** Responsabile Market Intelligence / Strategic Planning
- **Obiettivo:** Fornire una lettura aggiornata del contesto esterno (competitivo, economico, normativo, tecnologico) a supporto della definizione della visione strategica
- **Confini:** da "Avvio del ciclo di pianificazione strategica annuale" a "Report di analisi ambientale e competitiva consegnato al team di Pianificazione Strategica"
- **Ruoli coinvolti:** Market Intelligence Analyst, Strategic Planning Team
- **Sistemi coinvolti:** BI/market intelligence tool, repository documentale, CRM
- **KPI:** Copertura delle fonti analizzate; tempo di produzione del report; numero di insight actionable recepiti nella strategia
- **Rischi / colli di bottiglia:** Dati di mercato incompleti o non aggiornati; bias nella selezione delle fonti; tempi di consolidamento troppo lunghi rispetto al ciclo di pianificazione

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/) (BPMN 2.0, non eseguibile: `isExecutable="false"`, pensato solo come diagramma di rappresentazione per l'aula).
Corsie (lane): Market Intelligence Analyst, Strategic Planning Team.
