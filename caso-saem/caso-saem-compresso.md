# Il caso SAEM S.p.A. (versione didattica compressa)

*Adattato da: C. Bozzoli, "Reengineering del sistema di gestione ordini in ottica e-commerce: il caso SAEM S.p.A.", tesi di laurea, Politecnico di Milano, A.A. 2004-2005 (relatore Prof. Ing. T. Barbieri). Versione compressa per uso didattico: azienda, organizzazione e processi reali; omessi SCOR/UML di dettaglio, cruscotto KPI, requisiti IT e mock-up delle interfacce, presenti nella tesi originale.*

## 1. L'azienda

SAEM S.p.A., fondata nel 1904, è un **distributore** italiano di prodotti industriali ad alto contenuto tecnologico (non produce: importa e distribuisce prodotti di case produttrici internazionali di cui è rappresentante esclusivo). Sede a Brugherio, magazzino chimico a Pantigliate.

- **Fatturato:** 12,5-25 milioni di euro; **organico:** ~57 dipendenti + 16 agenti + una rete di ~340 distributori sul territorio.
- **Clienti:** oltre 3.500 attivi, in 25 settori industriali (meccanica 17%, commercio 13%, componentistica 10%, elettrodomestici 10%, elettrica 8%...).
- **Fornitori:** oltre 100 case produttrici, per più di 2.000 codici prodotto.
- **Prodotti:** adesivi e sigillanti industriali, lubrificanti speciali, macchine utensili, componenti per automazione, prodotti per elettrotecnica, materiali compositi.
- **Struttura:** funzionale al primo livello, 4 divisioni al secondo livello (Chimica, Macchine, Componenti, Hi-Tech). L'organizzazione vendite è a matrice: Responsabili Prodotto (esperti di tecnologia), Responsabili Industria (esperti di settore) e Responsabili Area (esperti di territorio) si coordinano in team mensili.
- **Certificazioni:** ISO 9001 e ISO 14001.
- **Posizionamento competitivo:** la tecnologia non basta più a differenziare (è "condizione necessaria"); il vantaggio competitivo si gioca su **tempestività di risposta**, **personalizzazione** e **assistenza tecnica pre/post vendita**. Vincolo operativo: molti prodotti hanno shelf life breve → trade-off tra tempestività e livello di scorte a magazzino.

**Ruoli chiave che compaiono nei processi:**

| Sigla | Ruolo |
|---|---|
| DIRV | Direttore Vendite (per Chimica o Meccanica) |
| FC | Funzionario Commerciale (marketing, gestisce l'offerta tecnica al cliente) |
| RGC | Responsabile Gestione Commerciale (vendite, inserisce ordini a sistema) |
| RTRAF | Responsabile Traffico (inserisce ordini a fornitore) |
| RMAG / SMAG | Responsabile / Segretario Magazzino |
| RACQ | Responsabile Acquisti |

**Sistemi informativi (contesto storico, anni 2000):** *Pragma* — vecchio sistema Client/Server a caratteri (DOS), usato per gestione commerciale e ordini; *MaxGestCS* — sistema più recente (Java + PostgreSQL) per anagrafiche clienti/fornitori/articoli. I due sistemi vengono sincronizzati ogni notte. Su questa base legacy l'azienda ha deciso di costruire un portale di e-commerce B2B ("MaxNet") per i clienti attivi.

## 2. Il problema che ha innescato il progetto

Il processo di gestione ordini (offerta → ordine → evasione → fatturazione), interamente manuale (fax, telefono, e-mail), generava due criticità sistematiche:

1. **Conversione delle unità di misura**: i clienti ordinano in unità proprie (es. grammi), SAEM vende in confezioni indivisibili (fusti, cartucce) → conversione manuale a rischio d'errore.
2. **Doppia codifica articolo**: ogni cliente usa un proprio codice interno diverso da quello SAEM → l'operatore deve tradurre a mano dalla descrizione.

Questi errori di imputazione generavano costi di gestione resi, ritardi di consegna e un peggioramento del servizio percepito — da cui la decisione della direzione di reingegnerizzare il processo introducendo un portale di inserimento ordini diretto da parte del cliente.

## 3. Quattro processi reali utilizzabili come esercitazione

### 3.1 Selezione e qualifica dei fornitori *(→ APQC 4.2.3 Select suppliers and develop/maintain contracts)*

Il DIRV avvia la ricerca di un nuovo fornitore (o di uno già qualificato per una nuova linea prodotti). Prima di una ricerca di mercato autonoma, SAEM sfrutta un **consorzio europeo** di aziende simili per reperire informazioni sui candidati.

Flusso: DIRV invia al candidato un **questionario di prevalutazione** (anagrafica, organizzazione, sistema qualità) → se necessario, **visita** presso la casa produttrice e stesura di un rapporto di visita → il fornitore fornisce listini, schede tecniche e di sicurezza → valutazione secondo una tecnica di **vendor rating** su 5 parametri pesati → se approvato, creazione dell'anagrafica fornitore/prodotto a sistema. La lista fornitori qualificati è riesaminata **semestralmente**; un fornitore che non soddisfa i requisiti può essere sottoposto ad azioni correttive o rimosso dalla lista. Anche il fornitore, simmetricamente, valuta la capacità di SAEM di distribuire i suoi prodotti (caso reale citato: l'accordo con Petrol per i lubrificanti speciali).

### 3.2 Gestione dell'ordine cliente: offerta → ordine → evasione *(→ APQC 6.0 Customer Service / 3.0 Market and Sell)*

Il cliente contatta il FC per una richiesta di offerta (quotazione o sostituzione di un prodotto/tecnologia). Il FC analizza il bisogno, individua una soluzione ed eventualmente avvia una fase di **omologazione** (test in laboratorio SAEM, presso il cliente o presso il fornitore); esito positivo → il prodotto viene omologato e inserito nella distinta base del cliente. Il FC prepara l'offerta (prezzo verificato contro la soglia minima; sotto soglia serve l'autorizzazione del DIRV) → invio al cliente.

Il cliente ordina (nuovo cliente: solo via fax; cliente consolidato: e-mail o telefono, con compilazione di un modulo "Proposta d'ordine"). L'ordine, dopo l'approvazione del DIRV, viene inserito a sistema dalla RGC, che verifica lo stato contabile del cliente e la disponibilità del prodotto (giacenza, impegni di altri ordini, arrivi da fornitore). Se la data richiesta non è disponibile, la RGC concorda col cliente una nuova data. L'evasione (per gli ordini in porto franco) comprende: selezione dello spedizioniere, generazione bolle, prelievo e controllo merce a magazzino (incluse verifiche ADR per merce pericolosa), carico veicolo, fatturazione settimanale delle bolle evase.

### 3.3 Ritiro e gestione dei resi *(→ APQC 6.3 Service products after sales)*

A causa di errori di imputazione o invii errati, il cliente può respingere la merce. Il reso deve essere **concordato** con il cliente da FC o RGC e **autorizzato dal DIRV** prima di essere accettato: senza autorizzazione il magazzino non accetta il reso. Se l'errore è di SAEM, viene compilata una Non Conformità. Il materiale rientrato viene allocato nell'area "non conforme" del magazzino in attesa di decisione (restituzione al fornitore, rilavorazione, o accettazione a stock).

Caso particolare — **riparazione dei deceleratori**: il magazzino riceve il pezzo guasto, lo smonta per diagnosticare il difetto → se riparabile in sede, il FC prepara un'offerta di riparazione (descrizione intervento, tempi, costo) → dopo l'ok del cliente, riparazione (in sede o dal fornitore), controlli finali, marchiatura e restituzione al cliente con bolla riportante il numero di serie.

### 3.4 Fatturazione *(→ APQC 9.2.2 Invoice customer)*

Con cadenza **settimanale**, si verifica che tutte le bolle evase siano state caricate a sistema (escludendo quelle già fatturate manualmente), si elabora e stampa la fattura. Le fatture seguono canali diversi a seconda del cliente: invio postale tradizionale, invio a mezzo file elettronico tramite Postel (servizio di stampa/imbustamento/spedizione per conto di SAEM), o gestione a parte per le vendite in contrassegno. Le fatture vengono infine trasferite in prima nota contabile.

## 4. Come usarlo in aula

Per ciascuno dei quattro processi sopra descritti si può ripetere l'esercizio già impostato per gli esempi APQC: individuare Category/Process Group/Process/Activity nel PCF, scomporre in Task, costruire SIPOC e matrice delle variabili, disegnare il BPMN con le corsie per ruolo (DIRV, FC, RGC, RTRAF, RMAG). A differenza degli esempi "puri" già preparati, qui i partecipanti lavorano su un caso con **criticità reali già documentate** (doppia codifica articoli, autorizzazioni di prezzo/reso, shelf life breve) da usare come base per la discussione su rischi e colli di bottiglia.
