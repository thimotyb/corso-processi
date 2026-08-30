# 4.0 Manage Supply Chain for Physical Products — esempio di processo APQC
*Fonte: APQC Process Classification Framework (PCF) Cross-Industry, versione 8.0.*
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 4.0 | Manage Supply Chain for Physical Products |
| Process Group | 4.2 | Procure materials and services (10216) |
| Process | 4.2.3 | Select suppliers and develop/maintain contracts (10278) |

**Evento di innesco (trigger):** Necessità di approvvigionamento identificata (nuova categoria merceologica o rinnovo contratto)
**Evento finale / output di processo:** Contratto di fornitura firmato e attivo a sistema

## 2. Activity del processo (dal PCF)
| Codice | Activity |
|---|---|
| 4.2.3.1 | Select suppliers (10288) |
| 4.2.3.2 | Certify and validate suppliers (10289) |
| 4.2.3.3 | Negotiate and establish contracts (10290) |
| 4.2.3.4 | Manage contracts (10291) |

## 3. Scomposizione in Task (esempio didattico)
Le Task non sono definite dal PCF a questo livello di dettaglio: la loro individuazione è compito dell'analista di processo. Esempio di scomposizione dell'Activity **"Negotiate and establish contracts (10290)"**:

1. Definire i termini negoziali (prezzo, SLA, penali, durata)
2. Condurre la trattativa con il fornitore selezionato
3. Sottoporre il contratto ad approvazione legale/finanziaria
4. Formalizzare la firma e caricare il contratto a sistema

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Category Manager, mercato fornitori, ufficio legale | Fabbisogno di approvvigionamento, albo fornitori, criteri di qualifica | Selezionare fornitori → Certificare e validare fornitori → Negoziare e stipulare il contratto → Gestire il contratto nel tempo | Contratto di fornitura attivo e fornitore qualificato | Operations/Produzione (utilizzatore della fornitura), Finance (impegno di spesa) |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel processo |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Fabbisogno di acquisto, albo fornitori, capitolato tecnico |
| Output | Risultato prodotto dal processo | Contratto di fornitura firmato, fornitore qualificato a sistema |
| Tempi | Durata tipica del processo | 4-8 settimane per una nuova fornitura critica |
| Costi | Risorse economiche assorbite | Ore Procurement/Legale, eventuali costi di audit fornitore |
| Volumi | Quantità/frequenza di esecuzione | Variabile per categoria merceologica; tipicamente alcune decine/anno |
| Ruoli | Attori coinvolti | Category/Procurement Manager, ufficio legale, fornitore |
| Sistemi | Applicativi/strumenti a supporto | ERP/modulo Procurement, Contract Management System, albo fornitori |
| Vincoli | Limiti operativi o normativi | Soglie di approvazione, normative su gare/qualifica fornitori |
| Rischi / colli di bottiglia | Punti critici del processo | Fornitore unico/dipendenza; ritardi nell'approvazione legale; mancata certificazione qualità |

## 6. Scheda processo sintetica
- **Nome processo:** 4.2.3 Select suppliers and develop/maintain contracts (10278)
- **Process owner:** Procurement/Category Manager
- **Obiettivo:** Selezionare e contrattualizzare fornitori affidabili alle migliori condizioni di prezzo, qualità e servizio
- **Confini:** da "Necessità di approvvigionamento identificata (nuova categoria merceologica o rinnovo contratto)" a "Contratto di fornitura firmato e attivo a sistema"
- **Ruoli coinvolti:** Category/Procurement Manager, ufficio legale, fornitore
- **Sistemi coinvolti:** ERP/modulo Procurement, Contract Management System
- **KPI:** Tempo medio di attivazione contratto; % fornitori certificati; risparmio negoziale ottenuto
- **Rischi / colli di bottiglia:** Dipendenza da fornitore unico; ritardi autorizzativi; clausole contrattuali non allineate agli SLA richiesti

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/) (BPMN 2.0, non eseguibile: `isExecutable="false"`, pensato solo come diagramma di rappresentazione per l'aula).
Corsie (lane): Procurement/Category Manager, Ufficio Legale.
