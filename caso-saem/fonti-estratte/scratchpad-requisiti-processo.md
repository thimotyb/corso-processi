# Scratchpad — requisiti del processo e requisiti informativi SAEM

Questo scratchpad raccoglie le evidenze estratte dalla tesi di C. Bozzoli, *Reengineering del sistema di gestione ordini in ottica e-commerce: il caso SAEM S.p.A.*, e le regole di analisi da riutilizzare senza ripetere il parsing del PDF.

Fonte primaria: `resources/casoSAEM.pdf`.

Testo consultabile: [`testo-pagine.md`](testo-pagine.md). Le pagine indicate sono quelle stampate nella tesi, salvo diversa indicazione.

## Tesi interpretativa da conservare

La sezione didattica **2.1 Come distinguere i livelli** deve spiegare anche come passare dalla distinzione tra funzione, processo, attività e task all'**estrazione e documentazione dei requisiti del processo**.

La tesi mostra una catena progressiva:

```text
analisi del business
  -> attività del processo supportabili dall'IT
  -> entità informative candidate
  -> relazioni di lettura e scrittura
  -> casi d'uso
  -> specifiche testuali
  -> requisiti numerati
  -> verifica iterativa tra processo, dati e sistema
```

Questa catena deve guidare sia il testo di M1 sia l'analisi dei diagrammi BPMN del caso SAEM.

## 1. Due livelli di requisito

La tesi distingue, sul piano del metodo, due livelli collegati:

- **Requisiti del processo aziendale**: obiettivo, confini, attività, ruoli, input, output, regole, vincoli, eccezioni, condizioni di avvio e di conclusione.
- **Requisiti informativi e IT**: funzionalità che il sistema deve offrire e informazioni che deve leggere, creare, aggiornare o cancellare.

Il passaggio dai requisiti di business ai requisiti IT avviene per selezione e dettaglio progressivo; non si deve confondere la descrizione del processo con la specifica tecnica del database o del software.

## 2. Raccolta dei requisiti di prodotto e servizio

Nel capitolo III, pagina stampata 23, la tesi indica che il riesame dei requisiti deve considerare almeno:

- requisiti esplicitamente contenuti nell'anagrafica cliente;
- requisiti non precisati dal cliente, ma necessari per l'uso specifico o conosciuto;
- requisiti cogenti relativi ai prodotti;
- requisiti aggiuntivi stabiliti dall'azienda;
- ulteriori informazioni da formalizzare, quando necessario, con documenti dedicati.

Prima che l'organizzazione si impegni a fornire il prodotto o il servizio, i requisiti devono essere **riesaminati**.

La stessa pagina segnala anche esigenze di tracciabilità: il sistema conserva gli autori delle offerte e delle loro modifiche, le autorizzazioni e gli autori delle modifiche agli ordini.

## 3. Dal problema operativo al requisito

Nel capitolo VI, pagine stampate 77-80, l'analisi del processo di gestione ordini parte da problemi osservati nel processo reale:

- differenza tra le unità di misura usate dal cliente e quelle usate da SAEM;
- codici articolo del cliente diversi dai codici interni SAEM;
- necessità di ricondurre descrizione e codice cliente all'articolo corretto;
- errori che aumentano il tempo di evasione;
- resi e rilavorazioni dovuti a errori o modifiche dell'ordine;
- impatto sulla qualità percepita del servizio;
- necessità di rendere le procedure frequenti, semplici e veloci.

Questi problemi diventano requisiti e vincoli del nuovo processo: conversione delle unità, ricerca dell'articolo, verifica disponibilità, controllo dei dati, gestione delle modifiche, riduzione degli errori e miglioramento dei tempi di risposta.

## 4. Assembly Line come strumento di derivazione

Capitolo VII, paragrafo 7.1, pagine stampate 92-93.

La Assembly Line collega tre livelli:

1. **modello di business**: attività del processo selezionate perché supportabili da un sistema IT;
2. **elementi informativi candidati**: strutture dati o unità informative significative o probabili nel sistema;
3. **relazioni di lettura e scrittura**: collegamenti tra attività ed entità.

La parte superiore contiene la porzione del modello di business considerata; la parte inferiore contiene le linee con gli elementi informativi candidati; la parte intermedia evidenzia quali attività leggono o scrivono tali elementi.

Le relazioni di lettura e scrittura consentono di derivare i casi d'uso relativi ai requisiti informativi del sistema.

Le entità sono dette **candidate** perché una successiva analisi può stabilire che debbano:

- essere confermate;
- evolvere;
- essere accorpate con altre entità;
- essere eliminate.

Nel progetto SAEM il DBMS Emaxgest5 viene mantenuto. Per questo le entità rappresentate nelle Assembly Line corrispondono, nei casi analizzati, alle tabelle effettivamente presenti nel database PostgreSQL, non soltanto a entità concettuali candidate.

## 5. Matrice CRUD come validazione

Capitolo VII, paragrafo 7.2, pagine stampate 98-108.

La matrice CRUD mette in relazione:

- **righe**: attività business o attività della Assembly Line;
- **colonne**: archivi, entità o tabelle utilizzate;
- **celle**: operazioni compiute dal sistema.

Codifica da conservare:

- **C — Create**: inserimento o creazione di una nuova istanza;
- **R — Read**: lettura o recupero di dati;
- **U — Update**: aggiornamento di dati esistenti;
- **D — Delete**: cancellazione di dati.

Le tavole CRUD della tesi sono derivate dalle Assembly Line e da attività di testing sui moduli del sistema in sviluppo e sul database di prova. Servono a verificare l'interazione tra modello del processo e modello dei dati.

La matrice CRUD è il livello sintetico delle informazioni di accesso ai dati. Non costituisce una specifica SQL completa: non descrive da sola transazioni, concorrenza, vincoli tecnici o riconciliazioni.

## 6. Esempi di evidenza CRUD nell'ordine telematico

### Creazione del carrello

La creazione di un nuovo ordine comporta:

- lettura dei dati del cliente;
- lettura dei termini di consegna;
- lettura dei parametri IVA;
- lettura e aggiornamento del numero progressivo del carrello;
- creazione della testata del carrello.

### Ricerca e inserimento degli articoli

La ricerca di un articolo legge informazioni da:

- `Articoli`;
- `Articoli_storico`;
- `Scadmag`;
- `Articoli_listino`;
- altre informazioni relative a offerte e clienti, secondo la variante del processo.

La disponibilità viene calcolata usando dati correnti, storico, scadenze e listini. Le righe del carrello vengono create, lette e aggiornate durante l'inserimento e la modifica.

### Conferma dell'ordine

Alla conferma, il sistema:

- rilegge e verifica i dati del cliente;
- ricalcola i parametri economici e l'IVA;
- legge testata e righe del carrello;
- copia la testata in `Portcli`;
- copia le righe in `Riportc`;
- cancella il carrello provvisorio se la trasformazione ha esito positivo;
- genera messaggi in caso di richiesta o anomalia.

### Ordine urgente

Per l'ordine urgente sono presenti ulteriori requisiti:

- generazione di una richiesta di approvazione;
- lettura dei riferimenti di testata e righe;
- invio del messaggio al funzionario commerciale;
- aggiornamento del flag `AUTORIZZATO` in `Portcli`;
- generazione dell'esito di approvazione o mancata approvazione verso il cliente.

## 7. Dai casi d'uso ai requisiti

Capitolo VII, paragrafo 7.3, pagine stampate 114-119 e successive.

I casi d'uso descrivono il comportamento del sistema dal punto di vista dell'utente esterno. Rappresentano funzionalità ottenute dalle interazioni tra attori ed entità informative.

Per ogni caso d'uso la tesi raccoglie:

- **attori**;
- **breve descrizione**;
- **flusso principale degli eventi**;
- **flussi alternativi**;
- **precondizioni**;
- **postcondizioni**;
- **eccezioni**;
- **frequenza stimata di utilizzo**;
- **criticità**.

I casi d'uso sono prima rappresentati graficamente e poi descritti in linguaggio naturale. La specifica testuale definisce cosa il sistema deve fare quando l'attore attiva il caso d'uso.

Esempio: il caso d'uso “Imposta testata offerta” documenta selezione del cliente, recupero dei dati, inserimento dei dati di validità, verifica, errori di ricerca e dati non validi.

## 8. Numerazione e gestione evolutiva

La tesi stabilisce che i requisiti sono descritti principalmente mediante asserzioni in linguaggio naturale e numerati secondo:

- numerazione derivata dalla struttura del documento dei requisiti;
- numerazione sequenziale all'interno della categoria del requisito.

Il documento dei casi d'uso evolve con l'avanzamento dello sviluppo. Nella fase iniziale contiene una descrizione breve; viene poi completato in modo **iterativo e incrementale**.

Regola didattica da riutilizzare: ogni requisito deve avere un identificativo stabile, una fonte, una descrizione verificabile e un collegamento al punto del processo, all'attore e ai dati coinvolti.

## 9. Regole per l'analisi BPMN del caso SAEM

Quando si aggiorna un diagramma BPMN:

1. partire dall'attività di business, non dalla tabella;
2. identificare l'attore o il ruolo che esegue l'attività;
3. annotare input, output, regole e condizioni;
4. collegare le entità informative lette o scritte;
5. usare Data Object per documenti o informazioni che attraversano il flusso;
6. usare Data Store Reference per archivi o sistemi persistenti;
7. annotare le operazioni CRUD solo quando sono documentate dalla fonte;
8. distinguere dati esplicitamente presenti nella tesi da inferenze didattiche;
9. ricondurre ogni requisito a una fonte e, quando possibile, a pagina e tabella;
10. verificare che ogni entità collegata sia raggiungibile e coerente con l'attività.

Non si deve dedurre una tabella concreta soltanto perché un'attività richiede genericamente un'informazione. La presenza di una fonte associata a un task non dimostra automaticamente ogni dettaglio della soluzione BPMN o SQL.

## 10. Riferimenti puntuali nella fonte estratta

- Requisiti cliente, requisiti impliciti, cogenti, aziendali e riesame: pagina stampata 23.
- Criticità del processo ordine e motivazione del nuovo modello: pagine stampate 77-80.
- Metodo Assembly Line e passaggio da business analysis a requisiti IT: pagine stampate 92-93.
- Tabelle CRUD e loro significato: pagine stampate 98-108.
- Casi d'uso, derivazione dei requisiti e specifica iterativa: pagine stampate 114-119 e successive.
- Estratto testuale locale: `testo-pagine.md`, righe relative alle sezioni sopra indicate.

## Stato dello scratchpad

- Analisi iniziale completata: 7 settembre 2026.
- Fonte verificata: `resources/casoSAEM.pdf` con dossier locale già estratto.
- Prossimo utilizzo previsto: riscrittura della sezione M01 2.1 e revisione della documentazione dei diagrammi BPMN SAEM.

## Standardizzazione, suite ERP e automazione

Ricerca aggiunta il 7 settembre 2026 per arricchire M1, sezione 3.

### Distinzione metodologica

Conservare questa distinzione:

- **APQC e SCOR** sono framework per classificare, descrivere e confrontare i processi;
- **Oracle NetSuite e SAP** sono suite gestionali che traducono processi standardizzati in ruoli, dati, transazioni, controlli, configurazioni e automazioni;
- la classificazione fornisce il linguaggio e il perimetro;
- la suite ERP rende il processo operativo e automatizzabile.

La standardizzazione non significa imporre la stessa procedura a ogni organizzazione. Significa definire un flusso sufficientemente stabile e leggibile, con eventi, ruoli, dati, regole e risultati attesi, così che possa essere configurato, misurato e automatizzato.

### Oracle NetSuite SuiteSuccess

Fonte ufficiale: [NetSuite Applications Suite — SuiteSuccess](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1511800348.html).

La documentazione descrive SuiteSuccess come una metodologia con componenti predefiniti basati su leading practices e adattati al settore e ai ruoli degli utenti. Tra i componenti indicati:

- processi aziendali forniti tramite SuiteApps;
- ruoli e centri operativi;
- dashboard;
- KPI e scorecard;
- moduli e funzionalità abilitate;
- moduli, report, ricerche salvate e preferenze predefinite;
- piano dei conti e configurazioni coerenti con il settore.

Evidenza metodologica: il processo standard non è soltanto un diagramma. Comprende anche persone, responsabilità, dati, schermate, indicatori e configurazioni applicative.

La documentazione sui controlli interni fornisce un esempio concreto per **Order to Cash**: gli articoli dell'ordine cliente vengono riportati nella fattura, la fattura può essere inviata al cliente, lo stato dell'ordine viene aggiornato automaticamente e il sistema genera la relativa registrazione contabile.

Fonte ufficiale: [NetSuite — Standard Internal Controls](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4750146419.html).

Esempio didattico da riutilizzare:

```text
ordine cliente
  -> evasione
  -> fatturazione
  -> aggiornamento dello stato
  -> registrazione contabile
```

Il punto da evidenziare non è il prodotto specifico, ma la relazione tra standardizzazione e automazione: quando dati, stati e regole sono definiti, il passaggio successivo può essere eseguito dal sistema senza ricostruire ogni volta il significato dell'operazione.

### SAP: processi end-to-end e scope item

Fonte ufficiale: [SAP Help — Process Hierarchy](https://help.sap.com/docs/SUPPORT_CONTENT/sm/3518046721.html).

La documentazione SAP usa esempi di processi end-to-end come:

- **Order to Cash**;
- **Procure to Pay**;
- **Source to Pay**;
- **Order to Fulfill**;
- **Invoice to Pay**.

Questi processi attraversano più domini funzionali e collegano attività commerciali, logistiche e finanziarie. L'esempio Order to Cash può iniziare dall'interazione con il cliente o dal web shop e coinvolgere vendite, produzione, supply chain e finance.

SAP descrive inoltre i processi standard come solution processes o scope item, accompagnati da documentazione, configurazioni e procedure di test.

Fonte ufficiale: [SAP Help — Access the SAP Best Practice Documents](https://help.sap.com/docs/SAP_S4HANA_CLOUD/1e9ba004e0504506a135afda960e9495/f622b930db3e458d9a4022047ef81ac6.html?form=MG0AV3).

### Esempio SAP: Procure to Pay

Il processo può essere rappresentato come:

```text
richiesta di acquisto
  -> assegnazione della fonte di approvvigionamento
  -> ordine al fornitore
  -> ricezione di beni o servizi
  -> verifica della fattura
  -> pagamento
```

La documentazione SAP mostra anche che le regole possono automatizzare la selezione di richieste di acquisto, l'assegnazione delle fonti, la creazione degli ordini e l'esecuzione pianificata delle attività.

Fonte ufficiale: [SAP Help — Manage Rules for Automation of Business Processes](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/af9ef57f504840d2b81be8667206d485/852a52a67c2c442ead085aa07b9fe8d4.html).

### Principio didattico da riutilizzare in M1

Testo concettuale da cui partire per la sezione 3:

> La standardizzazione diventa particolarmente utile quando un processo deve essere supportato da una piattaforma gestionale. Le suite ERP propongono spesso flussi applicativi predefiniti, ruoli, dati, controlli e indicatori. L'organizzazione può adottare questi flussi come riferimento, configurarli e automatizzare le attività ripetitive. La classificazione del processo fornisce il linguaggio e il perimetro; la piattaforma gestionale traduce quel processo in transazioni, regole e integrazioni.

Esempio da utilizzare in aula:

> Nel processo Order to Cash, la registrazione dell'ordine può alimentare automaticamente evasione, fatturazione, aggiornamento dello stato e registrazione contabile. Nel processo Procure to Pay, una richiesta di acquisto può attivare la selezione del fornitore, la creazione dell'ordine, la ricezione e il controllo della fattura. L'automazione è possibile perché il processo è stato prima standardizzato: sono noti gli eventi, i dati, i ruoli, le regole e gli output attesi.

### Limiti da ricordare

- Le fonti Oracle e SAP descrivono funzionalità e contenuti delle rispettive piattaforme: non devono essere presentate come definizioni universali di processo.
- Gli esempi servono a mostrare il rapporto tra standardizzazione e automazione, non a trasformare M1 in un corso ERP.
- Un processo standard di una suite può essere configurato e adattato; l'organizzazione deve comunque verificare requisiti, dati, ruoli, controlli, conformità e differenze rispetto al proprio modo di operare.
