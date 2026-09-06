# Roadmap dei diagrammi SAEM

Stato: pianificata il 6 settembre 2026. Questo documento definisce gli interventi; la revisione dei BPMN è ancora da eseguire.

Fonte primaria: [tesi originale SAEM](../resources/casoSAEM.pdf). La [versione didattica compressa](caso-saem-compresso.md) serve da sintesi, ma omette parte dei requisiti informativi. I diagrammi Eriksson–Penker, gli Assembly Line, le matrici CRUD e le descrizioni originali devono quindi essere consultati direttamente.

## Inventario e priorità

Sono presenti tre serie complete `processo.md`, `processo.bpmn`, `processo.png`:

| Processo | Percorso | Intervento |
|---|---|---|
| Selezione e qualifica fornitori | [03-acquisti](esempi-apqc/03-acquisti/processo.md) | Raffinare decisioni, rivalutazione e relazioni informative |
| Ritiro prodotti, resi e riparazione deceleratori | [05-customer-service](esempi-apqc/05-customer-service/processo.md) | Chiarire varianti, autorizzazioni e documenti di rientro/riparazione |
| Fatturazione settimanale | [07-finance](esempi-apqc/07-finance/processo.md) | Esplicitare bolle, canali di invio e passaggio alla contabilità |

La sintesi descrive anche la gestione ordine cliente: i quattro processi descritti non corrispondono ancora a quattro BPMN realizzati.

| Fase | Priorità | Lavoro e risultato atteso | Dipendenza |
|---|---|---|---|
| 0 | Necessaria | Inventariare diagrammi originali, descrizioni e CRUD; estrarre la matrice attività–dati con riferimenti puntuali, distinguendo AS-IS e TO-BE | Nessuna |
| 1 | Alta | Creare il processo centrale offerta → ordine → evasione, con collegamento alla fatturazione; mantenere separate le varianti del sistema originale e del progetto e-commerce | 0 |
| 2 | Alta | Raffinare resi e deceleratori: autorizzazione DIRV, non conformità, diagnosi, preventivo, accettazione cliente, riparazione e restituzione | 0 |
| 3 | Alta | Raffinare qualifica fornitori: prevalutazione, visita eventuale, vendor rating, approvazione, anagrafiche e rivalutazione semestrale | 0 |
| 4 | Media | Raffinare fatturazione: verifica bolle, esclusione documenti già fatturati, emissione, Postel/posta/contrassegno e prima nota | 0; raccordo con 1 |
| 5 | Media | Dettagliare preparazione offerta come sottoprocesso autonomo se la vista complessiva diventa troppo densa; mantenere gli stessi identificativi e riferimenti dati | 1 |
| 6 | Media | Dettagliare evasione/logistica: spedizioniere, autorizzazione, bolle e carico veicolo, con raccordo a fatturazione | 1 e 4 |
| 7 | Successiva | Valutare programmazione ordini a fornitore, controllo qualità in ingresso e reso a fornitore | Consolidamento delle fasi precedenti |

Le fasi 2–4 possono procedere indipendentemente dopo l'estrazione delle rispettive fonti. Le fasi 5–6 sono viste di dettaglio: evitare copie divergenti del processo centrale.

## Modalità obbligatoria di analisi e disegno

Per ogni attività ricostruire sia il lavoro svolto sia le informazioni utilizzate e prodotte. Applicare questa modalità ai nuovi diagrammi SAEM e a ogni revisione di quelli esistenti.

1. Identificare attività, ruolo, evento di avvio, decisioni e risultato nella fonte originale.
2. Estrarre entità informative lette, create, aggiornate o eliminate dalle relazioni Eriksson–Penker/Assembly Line, dalle matrici CRUD e dalle descrizioni. Controllare visivamente frecce e legenda dei diagrammi: l'estrazione del solo testo non basta a ricostruire le relazioni.
3. Distinguere entità di business (ordine, cliente, fattura), documenti (bolla, questionario), sistemi applicativi e tabelle fisiche. Registrare anche flussi manuali o cartacei quando documentati.
4. Associare sistemi e tabelle soltanto quando la fonte lo consente. Scrivere `non specificato nella fonte` per i dettagli mancanti; marcare separatamente le inferenze da verificare. Conservare la grafia originale dei nomi tecnici.
5. Specificare sempre lo scenario AS-IS o TO-BE. Una tabella del progetto MaxNet non dimostra che un'attività del processo precedente leggesse quella tabella; la sincronizzazione fra sistemi non dimostra un accesso diretto dell'operatore.
6. Riportare nel BPMN gli oggetti informativi principali e le relative associazioni; conservare il dettaglio tecnico nella documentazione delle attività e nella matrice della scheda processo.

### Convenzione BPMN

- Usare le corsie per le responsabilità. Annotare il sistema utilizzato nel task; una responsabilità automatizzata va distinta solo quando è documentata.
- Rappresentare documenti e informazioni di processo con Data Object; usare Data Store per archivi persistenti. Collegarli alle attività con associazioni dati in ingresso e in uscita, mantenendo distinto il flusso di controllo.
- Etichettare gli stati significativi, per esempio `Offerta [bozza]` e `Offerta [confermata]`. Per aggiornamenti mostrare lettura/scrittura e indicare `U`; per cancellazioni annotare esplicitamente `D` nella documentazione.
- Mostrare sul disegno le entità necessarie alla comprensione. Elencare tutte le tabelle documentate nella matrice e nella documentazione del task, evitando un diagramma illeggibile.
- Dare alle attività identificativi stabili, riusati nella matrice attività–dati e nelle viste di dettaglio. Usare `bpmn:documentation` per input, output, sistema/archivio, tabelle, CRUD, scenario, fonte e stato dell'evidenza.

### Matrice attività–dati

Aggiungere a ciascun `processo.md` una sezione «Tracciabilità informativa». Una riga rappresenta una relazione attività–entità–archivio; usare più righe quando un task accede a più entità o sistemi.

| ID BPMN / attività | Scenario | Entità o documento | Input / output e stato | Sistema / archivio | Tabella fisica | CRUD | Fonte: pagina PDF / stampata, figura o sezione | Evidenza |
|---|---|---|---|---|---|---|---|---|
| Da compilare nell'analisi | AS-IS / TO-BE | Nome di business | Letto / prodotto / modificato | Nome originale o non specificato | Nome originale o non specificato | C / R / U / D, oppure non determinabile | Riferimento puntuale | Esplicita / inferita da verificare / non specificata |

CRUD: C = creazione, R = lettura, U = aggiornamento, D = cancellazione. Non dedurre automaticamente una scrittura su database dalla produzione di un documento.

## Punti di partenza per l'estrazione

Le pagine seguenti sono numeri di pagina del file PDF, contando da 1. Nella matrice finale aggiungere anche la numerazione stampata e il riferimento alla figura/tabella originale.

| Fonte | Informazioni da ricostruire |
|---|---|
| PDF pp. 32, 35–39 | Qualifica fornitori, gestione ordine, fatturazione, resi e riparazione: attività e documenti del contesto originale |
| PDF pp. 40–43 | Ruoli di Pragma, MaxGestCS, PostgreSQL e MaxNet; sincronizzazioni e confine tra situazione esistente e progetto |
| PDF pp. 104–110 | Metodo Assembly Line, relazioni di lettura/scrittura, tabelle del DBMS Emaxgest5 e derivazione delle matrici CRUD |
| PDF pp. 111–125 | CRUD di offerta/ordini: estrarre ogni relazione nel suo scenario e controllare le figure collegate |
| PDF pp. 126–134 | Derivazione dei casi d'uso e descrizioni di autenticazione, testata offerta, contatto, riga offerta e disponibilità |

Per fornitori cercare questionario, rapporto di visita, listini, schede tecniche/sicurezza, valutazione e anagrafiche. Per resi cercare autorizzazione, non conformità, documenti di rientro, offerta di riparazione e bolla con numero di serie. Per fatturazione cercare bolle evase, fatture, file Postel e registrazioni contabili. Questi sono oggetti da verificare e mappare: i relativi nomi di tabelle non vanno inventati.

### Prima estrazione verificata

Verifica testuale sulla fonte originale: gli Assembly Line e i CRUD del capitolo VII descrivono il **TO-BE**, pur utilizzando tabelle esistenti. MaxGestCS è l'applicazione; PostgreSQL è il DBMS; Emaxgest5 è il database mantenuto dal progetto, chiamato anche «DBMS» nel testo originale. L'allineamento notturno descritto è Novell → Emaxgest5 (PDF 40–43 / stampate 28–31). MaxNet III è descritto alle PDF 101–103 / stampate 89–91.

| Sezione | Pagine PDF | Pagine stampate |
|---|---|---|
| Assembly Line D.1, D.2A, D.2B, D.2C | 106, 107, 108, 109 | 94, 95, 96, 97 |
| CRUD D.1 Inserimento offerta | 110–112 | 98–100 |
| CRUD D.2A Inserimento ordine telematico | 113–117 | 101–105 |
| CRUD D.2B Inserimento ordine urgente | 118–119 | 106–107 |
| CRUD D.2C Modifica ordine | 120–125 | 108–113 |

Le associazioni seguenti sono esplicite nei commenti CRUD. I nomi delle attività sono sintesi funzionali, da associare agli ID BPMN durante la modellazione. Il contesto comune è TO-BE / MaxNet III / database Emaxgest5 su PostgreSQL.

| Attività | Entità informativa | Tabella | Operazione e risultato | Fonte PDF / stampata |
|---|---|---|---|---|
| Inserire nuovo contatto per offerta | Potenziale cliente | `Clienti` | C: nuova scheda cliente | 111 / 99 |
| Gestire riga offerta | Riga offerta | `Offerte_articoli` | C/R/U/D a seconda di inserimento, lettura, modifica o annullamento; da separare per task | 112 / 100 |
| Confermare ordine dopo verifiche positive | Testata e righe ordine | `Portcli`, `Riportc` | C: copia della testata e delle righe del carrello | 117 / 105 |
| Approvare ordine urgente | Testata ordine | `Portcli` | U: campo `AUTORIZZATO` impostato a valore positivo | 119 / 107 |
| Annullare ordine inserito | Testata e righe ordine | `Portcli`, `Riportc` | D: cancellazione di testata e righe | 120–121 / 108–109 |

**Variante da preservare:** D.2C confronta la procedura degli sviluppatori con la proposta dell'autrice per mantenere la priorità dell'ordine. Corsivi e asterischi distinguono l'alternativa (PDF 94 e 120–122 / stampate 82 e 108–110). Verificarli visivamente e rappresentare due varianti nominate, evitando di sommarne le operazioni in un solo flusso.

Questa è un'estrazione iniziale dai commenti testuali: la fase 0 resta aperta per la ricostruzione completa e il controllo visivo dei diagrammi originali.

## Criteri di completamento di ciascuna fase

- Scheda processo, matrice attività–dati, BPMN e anteprima PNG aggiornati e coerenti.
- Ogni attività ha relazioni informative documentate oppure un'esplicita indicazione dei dati non specificati; le inferenze sono riconoscibili.
- Evidenza tracciabile alla pagina e al diagramma/descrizione originale; AS-IS e TO-BE non sono mescolati implicitamente.
- Apertura e controllo visivo in Camunda Modeler: leggibilità di corsie, etichette, flussi e associazioni dati; nessuna sovrapposizione che impedisca la lettura.
- Modelli didattici con `isExecutable="false"`; eventuale versione eseguibile richiede una progettazione dedicata.
- Collegamenti e anteprime nel materiale didattico allineati quando si pubblica la revisione.

Primo intervento operativo: completare l'estrazione attività–dati della gestione ordine e dell'offerta, quindi costruire il BPMN centrale della fase 1.
