# 9.0 Manage Financial Resources — versione SAEM S.p.A.
*Versione arricchita, radicata nel caso SAEM (vedi `caso-saem/caso-saem-compresso.md` e `resources/casoSAEM.pdf`), della scheda astratta [`esempi-apqc/07-finance/processo.md`](../../../esempi-apqc/07-finance/processo.md) — stessa gerarchia APQC PCF v8.0, stesso Process, narrazione e ruoli reali del caso.*
## 0. Scenario
Con cadenza settimanale SAEM elabora le fatture relative a tutte le bolle di evasione della settimana. Il processo distingue tre canali di emissione/invio: fatture singole spedite per posta normale dal magazzino/traffico insieme (o dopo) la merce, fatture inviate in massa tramite il servizio esterno Postel (che le stampa, imbusta e spedisce per conto di SAEM) e fatture per le vendite in contrassegno, gestite separatamente perché legate all'incasso al momento della consegna.
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 9.0 | Manage Financial Resources |
| Process Group | 9.2 | Perform revenue accounting (10729) |
| Process | 9.2.2 | Invoice customer (10743) |

**Evento di innesco (trigger):** Evento di cadenza settimanale del ciclo di fatturazione
**Evento finale / output di processo:** Le fatture della settimana sono emesse, instradate per canale e trasferite in prima nota contabile

## 2. Activity del processo (dal PCF, istanziate sul caso SAEM)
| Codice | Activity | Come si manifesta in SAEM |
|---|---|---|
| 9.2.2.1 | Maintain customer/product master files (10794) | Anagrafiche clienti/prodotto già gestite in MaxGestCS, verificate in caso di note di credito/debito manuali |
| 9.2.2.2 | Generate customer billing data (10795) | Verifica che tutte le bolle evase nel periodo siano caricate a sistema e non già fatturate manualmente; elaborazione e stampa delle fatture |
| 9.2.2.3 | Transmit billing data to customers (10796) | Instradamento per canale: fatture singole per posta, file fatture a Postel, fatture in contrassegno allegate alla merce |
| 9.2.2.4 | Post receivable entries (10797) | Trasferimento delle fatture emesse in prima nota contabile |
| 9.2.2.5 | Resolve customer billing inquiries (10798) | Gestione delle contestazioni, spesso originate da errori di codifica articolo/quantità nell'ordine originario |

## 3. Scomposizione in Task (esempio SAEM)
Esempio di scomposizione dell'Activity **"Generate customer billing data (10795)"**, così come descritta nel caso:

1. Estrarre le bolle evase nella settimana e non ancora fatturate
2. Verificare che non siano già state fatturate/note manualmente (credito/debito)
3. Elaborare e stampare le fatture per il periodo
4. Predisporre i lotti per canale (posta normale, Postel, contrassegno)

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Magazzino (bolle di evasione), Traffico (RTRAF) | Bolle evase della settimana, liste di note di credito/debito caricate manualmente | Verificare le bolle non fatturate → Elaborare e stampare le fatture → Instradare per canale (posta / Postel / contrassegno) → Trasferire in prima nota contabile | Fatture emesse, instradate e registrate in contabilità | Cliente finale, Contabilità generale (riconciliazione) |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel caso SAEM |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Bolle evase della settimana, note di credito/debito manuali |
| Output | Risultato prodotto dal processo | Fatture emesse, instradate e registrate in prima nota |
| Tempi | Durata tipica del processo | Ciclo settimanale, elaborazione in 1-2 giorni lavorativi |
| Costi | Risorse economiche assorbite | Ore Contabilità/RCONT, costo del servizio Postel per stampa/imbustamento/spedizione |
| Volumi | Quantità/frequenza di esecuzione | Tutte le bolle evase nella settimana, su una base di oltre 3.500 clienti attivi |
| Ruoli | Attori coinvolti | Contabilità (RCONT), Traffico (RTRAF), Magazzino, Postel (servizio esterno) |
| Sistemi | Applicativi/strumenti a supporto | Pragma/MaxGestCS (fatturazione), servizio esterno Postel |
| Vincoli | Limiti operativi o normativi | Le fatture in contrassegno devono essere allegate alla merce prima della spedizione |
| Rischi / colli di bottiglia | Punti critici del processo | Contestazioni originate da errori di codifica articolo/quantità nell'ordine; disallineamento tra fatturazione manuale e automatica delle note di credito/debito |

## 6. Scheda processo sintetica
- **Nome processo:** 9.2.2 Invoice customer (10743)
- **Process owner:** Responsabile Contabilità (RCONT)
- **Obiettivo:** Emettere con puntualità settimanale fatture corrette verso i clienti, instradandole per il canale corretto e registrandole in contabilità
- **Confini:** da "Evento di cadenza settimanale del ciclo di fatturazione" a "Le fatture della settimana sono emesse, instradate per canale e trasferite in prima nota contabile"
- **Ruoli coinvolti:** Contabilità (RCONT), Traffico (RTRAF), Magazzino, Postel
- **Sistemi coinvolti:** Pragma/MaxGestCS, servizio esterno Postel
- **KPI:** Tempo di chiusura del ciclo settimanale; % fatture contestate; % fatture gestite tramite Postel vs canale tradizionale
- **Rischi / colli di bottiglia:** Contestazioni per errori di codifica ereditati dal processo d'ordine; ritardi nel servizio esterno Postel

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/). Rispetto alla versione astratta, questo diagramma introduce un gateway a tre rami (canale di invio: posta normale / Postel / contrassegno), assente nella versione astratta lineare.
Corsie (lane): Contabilità (RCONT), Magazzino / Traffico (RTRAF).
