# 9.0 Manage Financial Resources — esempio di processo APQC
*Fonte: APQC Process Classification Framework (PCF) Cross-Industry, versione 8.0.*
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 9.0 | Manage Financial Resources |
| Process Group | 9.2 | Perform revenue accounting (10729) |
| Process | 9.2.2 | Invoice customer (10743) |

**Evento di innesco (trigger):** Ordine evaso / servizio erogato, pronto per la fatturazione
**Evento finale / output di processo:** Fattura trasmessa al cliente e registrata a contabilità (partita aperta in AR)

## 2. Activity del processo (dal PCF)
| Codice | Activity |
|---|---|
| 9.2.2.1 | Maintain customer/product master files (10794) |
| 9.2.2.2 | Generate customer billing data (10795) |
| 9.2.2.3 | Transmit billing data to customers (10796) |
| 9.2.2.4 | Post receivable entries (10797) |
| 9.2.2.5 | Resolve customer billing inquiries (10798) |

## 3. Scomposizione in Task (esempio didattico)
Le Task non sono definite dal PCF a questo livello di dettaglio: la loro individuazione è compito dell'analista di processo. Esempio di scomposizione dell'Activity **"Generate customer billing data (10795)"**:

1. Estrarre le righe di ordine/servizio evase e non ancora fatturate
2. Applicare prezzi, sconti e condizioni contrattuali
3. Calcolare imposte/tasse applicabili
4. Generare la bozza di fattura e sottoporla a controllo

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Ordine cliente/erogazione servizio (fonte a monte), anagrafica clienti/prodotti | Dati di consegna/erogazione, listino prezzi, condizioni contrattuali, aliquote fiscali | Mantenere anagrafiche → Generare i dati di fatturazione → Trasmettere la fattura al cliente → Registrare la partita in contabilità → Gestire eventuali contestazioni | Fattura emessa e registrata, partita aperta in Accounts Receivable | Cliente finale, processo 9.2.3 Process accounts receivable, Finance/Controllo di gestione |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel processo |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Dati di consegna/erogazione, listino prezzi, aliquote fiscali |
| Output | Risultato prodotto dal processo | Fattura emessa e registrata in contabilità |
| Tempi | Durata tipica del processo | Da poche ore (fatturazione automatica) a 2-3 giorni (casi manuali/contestati) |
| Costi | Risorse economiche assorbite | Ore Billing Specialist, costi di trasmissione (es. fatturazione elettronica) |
| Volumi | Quantità/frequenza di esecuzione | Da decine a migliaia di fatture al mese, secondo il business |
| Ruoli | Attori coinvolti | Billing Specialist, Accounts Receivable |
| Sistemi | Applicativi/strumenti a supporto | ERP/modulo fatturazione, sistema di fatturazione elettronica, CRM |
| Vincoli | Limiti operativi o normativi | Normativa fiscale su fatturazione (es. fatturazione elettronica obbligatoria), termini contrattuali |
| Rischi / colli di bottiglia | Punti critici del processo | Dati anagrafici errati; errori di calcolo imposte; ritardi che impattano il DSO (Days Sales Outstanding) |

## 6. Scheda processo sintetica
- **Nome processo:** 9.2.2 Invoice customer (10743)
- **Process owner:** Billing/Accounts Receivable Manager
- **Obiettivo:** Emettere fatture corrette e tempestive verso i clienti, garantendo la corretta registrazione contabile dei crediti
- **Confini:** da "Ordine evaso / servizio erogato, pronto per la fatturazione" a "Fattura trasmessa al cliente e registrata a contabilità (partita aperta in AR)"
- **Ruoli coinvolti:** Billing Specialist, Accounts Receivable
- **Sistemi coinvolti:** ERP/modulo fatturazione, sistema di fatturazione elettronica
- **KPI:** Tempo medio di emissione fattura; % fatture contestate; Days Sales Outstanding (DSO)
- **Rischi / colli di bottiglia:** Errori su prezzi/imposte che generano contestazioni; ritardi di fatturazione che allungano il ciclo di incasso

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/) (BPMN 2.0, non eseguibile: `isExecutable="false"`, pensato solo come diagramma di rappresentazione per l'aula).
Corsie (lane): Billing Specialist, Accounts Receivable.
