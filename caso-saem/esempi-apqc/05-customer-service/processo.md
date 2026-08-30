# 6.0 Manage Customer Service — versione SAEM S.p.A.
*Versione arricchita, radicata nel caso SAEM (vedi `caso-saem/caso-saem-compresso.md` e `resources/casoSAEM.pdf`), della scheda astratta [`esempi-apqc/05-customer-service/processo.md`](../../../esempi-apqc/05-customer-service/processo.md) — stessa gerarchia APQC PCF v8.0, stesso Process, narrazione e ruoli reali del caso.*
## 0. Scenario
A causa della doppia codifica articolo (il cliente usa un codice interno diverso da quello SAEM) o di errori nella conversione delle unità di misura, il cliente può respingere la merce ricevuta. Un caso particolare è il servizio di riparazione dei deceleratori (componenti meccanici) commercializzati da SAEM: il cliente restituisce il pezzo guasto per la riparazione anziché per un errore di fornitura. In entrambi i casi nessun reso viene accettato dal magazzino senza una autorizzazione esplicita del Direttore Vendite (DIRV).
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 6.0 | Manage Customer Service |
| Process Group | 6.2 | Plan and manage customer service contacts (10379) |
| Process | 6.2.2 | Manage customer service problems, requests, and inquiries (10388) |

**Evento di innesco (trigger):** Il cliente respinge un prodotto ricevuto oppure restituisce un deceleratore guasto per la riparazione
**Evento finale / output di processo:** Il reso è gestito (accettato, rifiutato o rilavorato) oppure il deceleratore è riparato e restituito al cliente

## 2. Activity del processo (dal PCF, istanziate sul caso SAEM)
| Codice | Activity | Come si manifesta in SAEM |
|---|---|---|
| 6.2.2.1 | Receive customer problems, requests, and inquiries (10394) | FC o RGC riceve la segnalazione di reso o la richiesta di riparazione dal cliente |
| 6.2.2.2 | Analyze problems, requests, and inquiries (13482) | Si determina se si tratta di un reso per errore di fornitura o di una richiesta di riparazione (es. deceleratore guasto) |
| 6.2.2.3 | Resolve customer problems, requests, and inquiries (10395) | Per i resi: autorizzazione DIRV e allocazione a magazzino; per le riparazioni: diagnosi, offerta di intervento, riparazione |
| 6.2.2.4 | Respond to customer problems, requests, and inquiries (10396) | Comunicazione al cliente dell'esito (accettazione reso, rifiuto, o restituzione del prodotto riparato) |

## 3. Scomposizione in Task (esempio SAEM)
Esempio di scomposizione dell'Activity **"Analyze problems, requests, and inquiries (13482)"**, così come descritta nel caso:

1. Verificare se il reso è dovuto a un errore di SAEM (codice/quantità) o del cliente
2. Controllare la presenza dell'autorizzazione del DIRV prima di procedere
3. Nel caso di un deceleratore, smontarlo per diagnosticare la causa del guasto
4. Decidere se la richiesta richiede l'apertura di una Non Conformità

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Cliente (segnalazione di reso o richiesta di riparazione), fornitore (per resi/riparazioni da girare a monte) | Bolla di reso o del deceleratore, motivazione del reso/guasto, autorizzazione del DIRV | Ricevere la segnalazione → Analizzare (reso semplice o riparazione) → Autorizzare e gestire a magazzino → Rispondere al cliente (reso gestito o prodotto riparato restituito) | Reso gestito (accettato/rifiutato/rilavorato) o deceleratore riparato e restituito al cliente | Cliente finale, fornitore (per i resi girati a monte o le riparazioni esterne) |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel caso SAEM |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Bolla di reso, motivo della restituzione, autorizzazione DIRV |
| Output | Risultato prodotto dal processo | Reso gestito, Non Conformità aperta se necessario, deceleratore riparato e restituito |
| Tempi | Durata tipica del processo | Da pochi giorni (reso semplice) a diverse settimane (riparazione esterna dal fornitore) |
| Costi | Risorse economiche assorbite | Costo della riparazione, eventuale nota di credito, ore FC/RGC/DIRV |
| Volumi | Quantità/frequenza di esecuzione | Ricorrente: criticità nota del caso legata alla doppia codifica articolo tra cliente e SAEM |
| Ruoli | Attori coinvolti | Funzionario Commerciale (FC), Responsabile Gestione Commerciale (RGC), DIRV, Magazzino (RMAG/SMAG) |
| Sistemi | Applicativi/strumenti a supporto | Pragma/MaxGestCS (Non Conformità, anagrafica ordini/resi) |
| Vincoli | Limiti operativi o normativi | Nessun reso è accettato dal magazzino senza autorizzazione esplicita del DIRV |
| Rischi / colli di bottiglia | Punti critici del processo | Merce accettata senza autorizzazione; ritardo nella diagnosi del guasto; dipendenza dai tempi del fornitore per le riparazioni esterne |

## 6. Scheda processo sintetica
- **Nome processo:** 6.2.2 Manage customer service problems, requests, and inquiries (10388)
- **Process owner:** Direttore Vendite (DIRV) / Responsabile Gestione Commerciale (RGC)
- **Obiettivo:** Gestire in modo controllato resi e riparazioni, minimizzando i costi di gestione e mantenendo la soddisfazione del cliente
- **Confini:** da "Il cliente respinge un prodotto ricevuto oppure restituisce un deceleratore guasto per la riparazione" a "Il reso è gestito (accettato, rifiutato o rilavorato) oppure il deceleratore è riparato e restituito al cliente"
- **Ruoli coinvolti:** FC, RGC, DIRV, Magazzino (RMAG/SMAG)
- **Sistemi coinvolti:** Pragma, MaxGestCS
- **KPI:** Tempo medio di gestione del reso; % resi dovuti a errore SAEM; tempo medio di riparazione dei deceleratori
- **Rischi / colli di bottiglia:** Doppia codifica articolo che genera resi evitabili; dipendenza dai tempi di riparazione del fornitore esterno

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/). Rispetto alla versione astratta, questo diagramma introduce due gateway innestati (tipo di richiesta: reso o riparazione; poi, sul ramo riparazione, accettazione del preventivo da parte del cliente) invece del singolo gateway di upsell della versione astratta.
Corsie (lane): FC / RGC, DIRV, Magazzino (RMAG/SMAG).
