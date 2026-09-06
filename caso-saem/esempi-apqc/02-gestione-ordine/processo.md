# Gestione ordine cliente SAEM · TO-BE MaxNet III

Modello didattico BPMN 2.0, non eseguibile, dalla richiesta commerciale alla spedizione e alla fatturazione. Aprire [processo.bpmn](processo.bpmn) nel Camunda Modeler: i sei sottoprocessi contengono attività reali e diagrammi di dettaglio navigabili. La vista principale è in [processo.png](processo.png).

## Perimetro e fonti

Il modello segue il macroprocesso TO-BE della tesi (PDF 95 / pagina stampata 83): D.1 offerta, D.2A/B acquisizione normale e urgente, D.2C variazioni, D.7 selezione spedizioniere, D.9A–C evasione, D.10 partenza e D.11 fatturazione. Il portale è rivolto ai clienti attivi. Le attività commerciali preliminari di laboratorio/omologazione, l'onboarding del nuovo cliente, l'approvvigionamento completo del fornitore e l'incasso successivo alla fatturazione sono fuori dal perimetro di questo modello; l'incasso al ritiro/contrassegno è invece rappresentato.

Fonti ed estrazioni sono conservate nel [dossier riutilizzabile](../../fonti-estratte/README.md): testo di 67 pagine, 17 rendering, relazioni strutturate e impronta del PDF. Per le prossime revisioni partire dal dossier; riesaminare il PDF solo per punti non ancora coperti o ambigui.

Il processo attraversa più domini: offerta commerciale, acquisizione ordine, logistica e fatturazione. Non gli viene attribuito artificialmente un unico codice APQC. I riferimenti D.1–D.11 sono quelli della mappatura SCOR/UML della tesi. La fatturazione si raccorda anche alla [scheda SAEM già esistente](../07-finance/processo.md).

## Viste disponibili

| Vista | BPMN autonomo | Anteprima |
|---|---|---|
| Percorso complessivo | [Processo](processo.bpmn) | [PNG](processo.png) |
| D.1 · Preparazione e autorizzazione offerta | [BPMN](dettagli/offerta.bpmn) | [PNG](dettagli/offerta.png) |
| D.2A/B · Inserimento ordine normale e urgente | [BPMN](dettagli/ordine.bpmn) | [PNG](dettagli/ordine.png) |
| D.2C · Variazioni prima del rilascio · Variante sviluppatori | [BPMN](dettagli/modifica.bpmn) | [PNG](dettagli/modifica.png) |
| Consegna pianificata · Evasione e fatturazione | [BPMN](dettagli/consegna.bpmn) | [PNG](dettagli/consegna.png) |
| D.7 / D.9A–C / D.10 · Evasione della consegna | [BPMN](dettagli/logistica.bpmn) | [PNG](dettagli/logistica.png) |
| D.11 · Fatturazione della bolla evasa | [BPMN](dettagli/fattura.bpmn) | [PNG](dettagli/fattura.png) |

I file autonomi sono copie di consultazione generate dalle stesse definizioni dei sottoprocessi incorporati: il modello completo non dipende dalla loro presenza per aprire i dettagli. Non sono Call Activity vuote. Nel Modeler usare il comando di navigazione del sottoprocesso; in alternativa aprire il relativo file autonomo.

## Lettura del diagramma

- Le corsie riportano responsabilità operative. I task del front office rappresentano l'interazione del cliente attraverso MaxNet; il cliente esterno è un partecipante separato nella vista complessiva.
- Il foglio è un Data Object: offerta, ordine, conferma, bolla, documento di trasporto o fattura.
- Il cilindro è un Data Store Reference: database o archivio persistente. Più cilindri con nome Emaxgest5 sono riferimenti allo stesso database, posti vicino ai task per leggibilità.
- Le frecce tratteggiate dati sono Data Input/Output Association native. Quelle di messaggio fra cliente e SAEM restano Message Flow, semanticamente distinti.
- Le proiezioni del database raccolgono le tabelle usate da un task. Il nome grafico può essere abbreviato con «…»: documentazione dell'icona, documentazione dell'attività e matrice sottostante riportano l'elenco completo e il CRUD per tabella.
- Per gli archivi logistici senza schema fisico documentato compare «tabella non specificata». «Archivi gestionali / documentali» è un raggruppamento logico, non un nuovo database inventato.
- Gateway, eventi e timer sono documentati; non eseguono direttamente accessi SQL. Le condizioni hanno etichette di business, non espressioni pronte per un motore.
- Il sottoprocesso per consegna è multi-istanza parallelo: rappresenta le date/quantità delle consegne concordate. Il processo termina con successo soltanto dopo il completamento di tutte le consegne.

## Scelte e limiti espliciti

1. **AS-IS e TO-BE:** i CRUD del capitolo VII valgono per MaxNet. Logistica e fatturazione derivano dalle procedure originali mantenute nel macroprocesso TO-BE; non vengono associate arbitrariamente a tabelle MaxNet.
2. **D.2C:** viene adottata la variante degli sviluppatori: copia in carrello, riverifica, sostituzione dell'ordine originale e nuova priorità. La proposta alternativa dell'autrice con aggiornamenti U* e conservazione della priorità resta distinta nel dossier, non è mescolata al flusso realizzato.
3. **Autorizzazioni:** DIRV valuta deroghe sul prezzo dell'offerta; FC approva l'ordine urgente. Un ordine urgente respinto non procede all'evasione. La fonte non specifica la cancellazione automatica o il rilascio degli impegni su quel rifiuto: il modello non li inventa.
4. **Rami di chiusura e rimedio:** rinuncia, abbandono modifiche, risoluzione blocchi contabili, ripianificazione e sostituzione del mezzo ADR rendono espliciti esiti operativi. Dove sono elaborazioni didattiche, sono segnalati nel task e nei dati strutturati.
5. **Variazioni:** la finestra modellata è prima del rilascio alla logistica. Dopo una modifica si torna al riesame commerciale, comprendendo le autorizzazioni applicabili. Le modifiche a merce già spedita appartengono ad altri processi, compresi i resi.
6. **Consegne parziali e fatturazione:** l'orchestrazione per consegna è un'elaborazione BPMN. Ogni bolla evasa entra nel successivo ciclo settimanale; il diagramma non impone di attendere l'ultima consegna per fatturare le precedenti. Il raggruppamento di più bolle in una fattura resta competenza del processo contabile; questo modello per ordine non implementa un batch globale.
7. **Doppia fatturazione:** le bolle già fatturate manualmente sono escluse dall'emissione. La verifica della loro registrazione contabile è un raccordo didattico esplicito.
8. **Persistenza:** C/R/U/D sui documenti descrivono la trasformazione informativa; solo le righe con tabelle nominali documentate specificano accessi fisici. Le operazioni composite, la concorrenza sulle scorte, la compensazione degli impegni e le autorizzazioni eseguibili richiedono una progettazione ulteriore.
9. **Contesto storico:** i controlli ADR e i canali Postel/posta riproducono il caso SAEM dell'epoca, non costituiscono istruzioni normative o architetturali aggiornate.

## SIPOC

| Fornitori di input | Input | Processo | Output | Destinatari |
|---|---|---|---|---|
| Cliente, FC, DIRV, magazzino, contabilità, spedizioniere | Richiesta, anagrafiche, prezzi/offerte, disponibilità, stato contabile, dati trasporto | Offerta → acquisizione → riesame/variazioni → evasione → fatturazione | Offerta autorizzata, ordine, piano consegne, bolle evase, fatture e prima nota | Cliente, magazzino, RGC, contabilità |

Indicatori utili: lead time offerta; tempo da conferma cliente ad acquisizione ordine; frequenza delle riverifiche negative; quota ordini urgenti respinti; puntualità della consegna; bolle evase non ancora fatturate. Nessun target numerico viene inventato.

## Tracciabilità informativa

Righe estratte dai commenti CRUD e dalle descrizioni/figure della tesi. I nomi delle attività sono traduzioni funzionali BPMN. Il campo «Relazione e dettaglio» specifica a quali tabelle si applicano le singole lettere, evitando di assegnare l'intero CRUD indiscriminatamente a tutti gli archivi del gruppo.

### SAEM · Gestione ordine cliente · TO-BE

Scenario: TO-BE MaxNet III. Fonte di contesto: PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11.

| ID / attività | Entità / sistema / tabelle | Relazione e dettaglio | Fonte PDF / stampata |
|---|---|---|---|
| `Sub_Offerta` · D.1 · Preparare e autorizzare offerta | Offerta [autorizzata] | **C** · Offerta disponibile oppure esito di chiusura; vedi dettaglio D.1. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `Sub_Ordine` · D.2A/B · Acquisire ordine normale / urgente | Offerta [autorizzata] | **R** · Offerta valida quando necessaria; catalogo è alternativa. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `Sub_Ordine` · D.2A/B · Acquisire ordine normale / urgente | Ordine [acquisito] | **C** · Ordine con esito acquisizione/autorizzazione. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `M_Controllo` · RGC · Riesaminare ordine e stato contabile | Ordine [acquisito] | **R** · Ordine da riesaminare. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `M_Controllo` · RGC · Riesaminare ordine e stato contabile | Stato contabile cliente; Gestionale · tabella non specificata | **R** · Problemi contabili / cliente bloccato; tabella non specificata. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `M_Blocco` · RGC / CONT · Risolvere blocchi o concordare rinuncia | Stato contabile cliente; Gestionale · tabella non specificata | **R/U?** · Risoluzione: aggiornamenti fisici non specificati; ramo didattico. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `Sub_Modifica` · D.2C · Modificare / annullare ordine | Ordine [acquisito] | **R/U/D** · Modifica o annullamento; CRUD fisico nel dettaglio. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `M_Conferma` · RGC · Comunicare conferma e piano consegne | Conferma / piano consegne | **C** · Conferma al cliente e date di evasione. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `Sub_Consegna` · Per ogni consegna · Evadere e fatturare | Conferma / piano consegne | **R** · Un'istanza per ciascuna consegna concordata. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |
| `Sub_Consegna` · Per ogni consegna · Evadere e fatturare | Fatture / prima nota | **C** · Fatture e registrazioni per le bolle evase. | PDF 95 / stampata 83; dettagli D.1, D.2, D.7, D.9, D.10, D.11 |

Esplicitazioni / limiti per attività:

- `M_Controllo`: Esplicita; chiusura/reiterazione del blocco resa esplicita didatticamente.
- `M_Blocco`: Ramo di risoluzione didattico: fonte segnala problemi contabili / cliente bloccato.
- `M_Conferma`: Esplicita; piano per consegna è aggregazione didattica delle date di evasione.

### D.1 · Preparazione e autorizzazione offerta

Scenario: TO-BE MaxNet III. Fonte di contesto: PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100.

| ID / attività | Entità / sistema / tabelle | Relazione e dettaglio | Fonte PDF / stampata |
|---|---|---|---|
| `O_Login` · Accedere e identificare il cliente | Emaxgest5 · Persone / Clienti | **R** · Persone: autenticazione operatore; Clienti: identificazione destinatario. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Contatto` · Creare contatto e categoria industriale | Emaxgest5 · Clienti / Categorie | **R/C** · Categorie R; Clienti C per nuovo contatto. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Testata` · Impostare testata offerta | Emaxgest5 · Persone / Clienti | **R** · Dati cliente ed esecutore della testata. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Testata` · Impostare testata offerta | Emaxgest5 · Offerte_testate | **C** · Creazione testata confermata. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Riga` · Aggiungere articolo, quantità e prezzo | Emaxgest5 · Articoli; Articoli_storico / Scadmag / Articoli_listino | **R** · Anagrafica, confezioni, listino; storico e Scadmag se si verifica disponibilità. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Riga` · Aggiungere articolo, quantità e prezzo | Emaxgest5 · Offerte_articoli | **C** · Creare riga di offerta. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_ModPrezzo` · Modificare prezzo della riga | Emaxgest5 · Offerte_articoli | **R/U** · Leggere e aggiornare prezzo riga. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Richiesta` · Generare richiesta autorizzazione | Emaxgest5 · Offerte_articoli | **R** · Riferimenti e prezzo della riga sotto soglia. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Richiesta` · Generare richiesta autorizzazione | Emaxgest5 · Offerte_testate | **R** · Riferimenti testata della richiesta. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Richiesta` · Generare richiesta autorizzazione | Emaxgest5 · Persone / Clienti | **R** · Esecutore della richiesta. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Richiesta` · Generare richiesta autorizzazione | Emaxgest5 · Messaggi | **C** · Messaggio al DIRV. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Richiesta` · Generare richiesta autorizzazione | Richiesta / esito deroga | **C** · Richiesta di deroga. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_DIRV` · DIRV · Valutare deroga al prezzo | Richiesta / esito deroga | **R/U** · Valutazione ed esito; persistenza dell'esito non specificata. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Rivedere` · FC · Rivedere o ritirare proposta | Richiesta / esito deroga | **R** · Esito negativo da riesaminare. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Conferma` · Confermare e numerare offerta | Emaxgest5 · Offerta_testata_n_offerta | **R/U** · Leggere e incrementare progressivo offerta. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Conferma` · Confermare e numerare offerta | Emaxgest5 · Offerte_articoli | **R** · Righe della proposta da confermare. | PDF 96, 100, 106, 110–112 / stampate 84, 88, 94, 98–100 |
| `O_Pubblica` · Rendere offerta visibile al cliente | Offerta [autorizzata] | **C** · Offerta resa visibile dopo autorizzazione; modalità di aggiornamento fisico non specificata. | PDF 100 / 88 |

Esplicitazioni / limiti per attività:

- `O_DIRV`: Autorizzazione esplicita PDF 36/24 e 100/88; tabelle dell'esito non specificate.
- `O_Rivedere`: Gestione del rifiuto resa esplicita didatticamente.

### D.2A/B · Inserimento ordine normale e urgente

Scenario: TO-BE MaxNet III. Fonte di contesto: PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107.

| ID / attività | Entità / sistema / tabelle | Relazione e dettaglio | Fonte PDF / stampata |
|---|---|---|---|
| `I_Login` · Autenticare cliente attivo | Emaxgest5 · Clienti | **R** · Autenticazione cliente attivo; diagramma descrive il sistema storico, non una raccomandazione di gestione credenziali. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Testata` · Ricevere destinazione / termini e creare carrello | Emaxgest5 · Clienti | **R** · Dati cliente / codice IVA. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Testata` · Ricevere destinazione / termini e creare carrello | Emaxgest5 · Cliedesta / Tabella_iva | **R** · Cliedesta: destinazione e disposizioni; Tabella_iva: parametri. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Testata` · Ricevere destinazione / termini e creare carrello | Emaxgest5 · Carrello_testata / Carrello_righe; Carrello_testata_n_carrello | **C/R/U** · Carrello_testata C; progressivo Carrello_testata_n_carrello R/U. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Riga` · Selezionare codice SAEM e multipli di confezione | Emaxgest5 · Articoli | **R** · Codici SAEM e confezioni indivisibili. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Riga` · Selezionare codice SAEM e multipli di confezione | Emaxgest5 · Carrello_testata / Carrello_righe; Carrello_testata_n_carrello | **C** · Carrello_righe: inserimento articolo. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_RichOfferta` · Inviare richiesta offerta / rinnovo | Emaxgest5 · Messaggi | **C** · Richiesta con riferimenti cliente/articolo. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_RichOfferta` · Inviare richiesta offerta / rinnovo | Emaxgest5 · Clienti | **R** · Riferimenti del cliente. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_RichOfferta` · Inviare richiesta offerta / rinnovo | Emaxgest5 · Articoli | **R** · Riferimenti dell'articolo. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Prezzo` · Calcolare prezzo, sconto, IVA e disponibilità | Emaxgest5 · Offerte_articoli; Articoli_listino / Clienti_sconto | **R** · Prezzo offerta oppure listino con sconto cliente. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Prezzo` · Calcolare prezzo, sconto, IVA e disponibilità | Emaxgest5 · Clienti | **R** · Codice IVA cliente. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Prezzo` · Calcolare prezzo, sconto, IVA e disponibilità | Emaxgest5 · Cliedesta / Tabella_iva | **R** · Parametri Tabella_iva. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Prezzo` · Calcolare prezzo, sconto, IVA e disponibilità | Emaxgest5 · Articoli / Articoli_storico / Scadmag | **R** · Disponibilità da anagrafica / storico / Scadmag. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Conferma` · Cliente · Confermare il carrello | Emaxgest5 · Carrello_testata / Carrello_righe; Carrello_testata_n_carrello | **R** · Carrello sottoposto a conferma. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Verifica` · Riverificare prezzi, disponibilità e date | Emaxgest5 · Articoli / Articoli_storico / Scadmag | **R** · Riverifica disponibilità e date prima della registrazione. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Verifica` · Riverificare prezzi, disponibilità e date | Emaxgest5 · Offerte_articoli; Articoli_listino / Clienti_sconto | **R** · Ricalcolo prezzi e sconti. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Verifica` · Riverificare prezzi, disponibilità e date | Emaxgest5 · Clienti | **R** · Codice IVA. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Verifica` · Riverificare prezzi, disponibilità e date | Emaxgest5 · Cliedesta / Tabella_iva | **R** · Parametri IVA. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Verifica` · Riverificare prezzi, disponibilità e date | Emaxgest5 · Carrello_testata / Carrello_righe; Carrello_testata_n_carrello | **R** · Testata e righe da riverificare. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Modifica` · Modificare quantità / dati carrello | Emaxgest5 · Carrello_testata / Carrello_righe; Carrello_testata_n_carrello | **R/U** · Leggere e modificare dati di testata/righe. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Parziale` · Concordare date e trasformare in evasione parziale | Emaxgest5 · Carrello_testata / Carrello_righe; Carrello_testata_n_carrello | **R/C/U** · Testata R/U; righe R/C/U per date/quantità parziali. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Parziale` · Concordare date e trasformare in evasione parziale | Emaxgest5 · Articoli / Articoli_storico / Scadmag | **R** · Disponibilità per data. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Registra` · Creare ordine, impegnare scorte e rimuovere carrello | Emaxgest5 · Carrello_testata / Carrello_righe; Carrello_testata_n_carrello | **R/D** · Copiare testata e righe e cancellare carrello dopo esito positivo. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Registra` · Creare ordine, impegnare scorte e rimuovere carrello | Emaxgest5 · Portcli / Riportc | **C** · Portcli C; Riportc C. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Registra` · Creare ordine, impegnare scorte e rimuovere carrello | Emaxgest5 · Movimenti_articolo | **C** · Memorizzare quantità impegnate. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Registra` · Creare ordine, impegnare scorte e rimuovere carrello | Emaxgest5 · Articoli / Articoli_storico / Scadmag | **U** · Solo Articoli_storico e Scadmag: aggiornamenti movimentazione. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_RichUrgenza` · Inviare richiesta approvazione FC | Emaxgest5 · Portcli / Riportc | **R** · Riferimenti Portcli. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_RichUrgenza` · Inviare richiesta approvazione FC | Emaxgest5 · Messaggi | **C** · Richiesta approvazione FC. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_FC` · FC · Valutare urgenza e disponibilità | Emaxgest5 · Articoli / Articoli_storico / Scadmag | **R** · Disponibilità per valutare urgenza. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_FC` · FC · Valutare urgenza e disponibilità | Emaxgest5 · Portcli / Riportc | **R** · Ordine oggetto della valutazione. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Autorizza` · Impostare AUTORIZZATO e notificare cliente | Emaxgest5 · Portcli / Riportc | **R/U** · Portcli U AUTORIZZATO positivo; Portcli/Riportc R per messaggio. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Autorizza` · Impostare AUTORIZZATO e notificare cliente | Emaxgest5 · Messaggi | **C** · Messaggio di approvazione. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Autorizza` · Impostare AUTORIZZATO e notificare cliente | Emaxgest5 · Clienti | **R** · Indirizzo e-mail e destinatario. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Autorizza` · Impostare AUTORIZZATO e notificare cliente | Ordine urgente [esito] | **C** · Ordine autorizzato. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Respinto` · Notificare urgenza non approvata | Emaxgest5 · Messaggi | **C** · Messaggio di mancata approvazione. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Respinto` · Notificare urgenza non approvata | Emaxgest5 · Clienti | **R** · Destinatario notifica. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Respinto` · Notificare urgenza non approvata | Ordine urgente [esito] | **C** · Ordine non autorizzato; cancellazione e rilascio scorte non specificati, non simulati. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |
| `I_Codice` · Restituire codice ordine / conferma | Ordine [confermato] / codice | **C** · Codice dell'ordine accettato. | PDF 97–98, 107–108, 113–119 / stampate 85–86, 95–96, 101–107 |

### D.2C · Variazioni prima del rilascio · Variante sviluppatori

Scenario: TO-BE MaxNet III. Fonte di contesto: PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113.

| ID / attività | Entità / sistema / tabelle | Relazione e dettaglio | Fonte PDF / stampata |
|---|---|---|---|
| `V_Apri` · Aprire ordine inserito | Emaxgest5 · Portcli / Riportc | **R** · Visualizzare testata e righe. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Annulla` · Cancellare testata e righe ordine | Emaxgest5 · Portcli / Riportc | **D** · Eliminare Portcli e Riportc; non confondere con U* alternativa. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Copia` · Copiare ordine in nuovo carrello | Emaxgest5 · Portcli / Riportc | **R** · Leggere ordine originale. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Copia` · Copiare ordine in nuovo carrello | Emaxgest5 · Carrello_testata / Carrello_righe | **C** · Creare carrello da ordine originale. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Edit` · Modificare destinazione, date, quantità / aggiungere righe | Emaxgest5 · Carrello_testata / Carrello_righe | **R/U/C** · Testata R/U; righe R/U, C per articoli aggiunti. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Edit` · Modificare destinazione, date, quantità / aggiungere righe | Emaxgest5 · Offerte_articoli / Articoli_listino; Clienti / Clienti_sconto / Tabella_iva | **R** · Prezzi / IVA per righe modificate o nuove. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Conferma` · Cliente · Confermare modifiche | Emaxgest5 · Carrello_testata / Carrello_righe | **R** · Dati sottoposti a conferma. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Check` · Riverificare offerte, prezzi, IVA e disponibilità | Emaxgest5 · Carrello_testata / Carrello_righe | **R** · Dati da riverificare. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Check` · Riverificare offerte, prezzi, IVA e disponibilità | Emaxgest5 · Offerte_articoli / Articoli_listino; Clienti / Clienti_sconto / Tabella_iva | **R** · Prezzo offerta o listino/sconto, codice e parametri IVA. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Check` · Riverificare offerte, prezzi, IVA e disponibilità | Emaxgest5 · Articoli / Articoli_storico; Scadmag / Movimenti_articolo | **R** · Disponibilità: Articoli, Articoli_storico, Scadmag; non attribuire R a Movimenti_articolo. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Parziale` · Trasformare carrello in evasione parziale | Emaxgest5 · Carrello_testata / Carrello_righe | **R/U/C** · Testata R/U, righe R/U/C per quantità e date. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Parziale` · Trasformare carrello in evasione parziale | Emaxgest5 · Articoli / Articoli_storico; Scadmag / Movimenti_articolo | **R** · Articoli, Articoli_storico, Scadmag per date di disponibilità. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Sostituisci` · Sostituire ordine originale e aggiornare impegni | Emaxgest5 · Portcli / Riportc | **D/C** · Eliminare vecchia testata/righe e creare nuove dopo verifiche positive. Variante sviluppatori: perdita della priorità originale. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Sostituisci` · Sostituire ordine originale e aggiornare impegni | Emaxgest5 · Carrello_testata / Carrello_righe | **R/D** · Copiare e rimuovere carrello dopo conferma. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Sostituisci` · Sostituire ordine originale e aggiornare impegni | Emaxgest5 · Articoli / Articoli_storico; Scadmag / Movimenti_articolo | **C/U** · Movimenti_articolo C; Articoli_storico e Scadmag U. Verificare riconciliazione impegni preesistenti prima di un'implementazione eseguibile. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Sostituisci` · Sostituire ordine originale e aggiornare impegni | Ordine [sostituito · nuova priorità] | **C** · Ordine sostituito, da riesaminare anche per eventuale urgenza. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |
| `V_Abbandona` · Abbandonare modifiche · mantenere ordine originale | Emaxgest5 · Portcli / Riportc | **R** · Ordine originale mantenuto; ramo didattico. | PDF 94, 99, 109, 120–125 / stampate 82, 87, 97, 108–113 |

Esplicitazioni / limiti per attività:

- `V_Annulla`: D Portcli/Riportc esplicita. Rilascio impegni da verificare: non inventato.
- `V_Abbandona`: Chiusura didattica: fonte cancella l'ordine originale soltanto dopo verifiche positive; pulizia carrello non specificata.

### Consegna pianificata · Evasione e fatturazione

Scenario: TO-BE · logistica mantenuta; orchestrazione per consegna didattica. Fonte di contesto: PDF 37, 95, 113–117 / stampate 25, 83, 101–105.

| ID / attività | Entità / sistema / tabelle | Relazione e dettaglio | Fonte PDF / stampata |
|---|---|---|---|
| `Sub_Logistica` · D.7 / D.9 / D.10 · Preparare e spedire | Piano consegna [data / quantità] | **R** · Lotto e data corrente; preparazione bolle prima del ritiro. | PDF 37, 95, 113–117 / stampate 25, 83, 101–105 |
| `Sub_Logistica` · D.7 / D.9 / D.10 · Preparare e spedire | Bolla [evasa] | **C** · Bolla evasa e dati di partenza. | PDF 37, 95, 113–117 / stampate 25, 83, 101–105 |
| `Sub_Fattura` · D.11 · Fatturare bolle e registrare | Bolla [evasa] | **R** · Solo bolle evase non già fatturate. | PDF 37, 95, 113–117 / stampate 25, 83, 101–105 |
| `Sub_Fattura` · D.11 · Fatturare bolle e registrare | Fattura / prima nota | **C** · Fattura e registrazione; raggruppamento settimanale è nel processo contabile. | PDF 37, 95, 113–117 / stampate 25, 83, 101–105 |
| `C_Ripiano` · RGC · Ripianificare consegna e data | Piano consegna [data / quantità] | **R/U** · Nuova data concordata; dettagli di tabella non specificati. | PDF 37, 95, 113–117 / stampate 25, 83, 101–105 |

Esplicitazioni / limiti per attività:

- `C_Ripiano`: Ritorno operativo didattico per mancata partenza; non chiude la consegna come fatturata.

### D.7 / D.9A–C / D.10 · Evasione della consegna

Scenario: TO-BE · attività logistiche mantenute dal processo originale. Fonte di contesto: PDF 37, 72–74, 95 / stampate 25, 60–62, 83.

| ID / attività | Entità / sistema / tabelle | Relazione e dettaglio | Fonte PDF / stampata |
|---|---|---|---|
| `L_Corriere` · Selezionare spedizioniere qualificato per zona | Archivio spedizionieri qualificati; Tabella non specificata | **R** · Spedizionieri qualificati, zona e condizioni. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Prepara` · EDP · Elaborare bolle e controlli economici | Gestionale · ordini, bolle, anagrafiche,; scorte, contabilità / listini · tabelle non specificate | **R** · Ordini, cliente, scorte, bolle, insoluti, condizioni commerciali. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Prepara` · EDP · Elaborare bolle e controlli economici | Bolla [prelievo] | **C** · Elaborazione preliminare bolle. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Sblocca` · CONT / DIRV · Riesaminare insoluti e autorizzazioni | Gestionale · ordini, bolle, anagrafiche,; scorte, contabilità / listini · tabelle non specificate | **R** · Insoluti / prezzi / autorizzazioni; fonte D.9A. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Sblocca` · CONT / DIRV · Riesaminare insoluti e autorizzazioni | Autorizzazione evasione / riesame | **C** · Esito riesame; CRUD di tabelle non specificato. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Autorizza` · RGC · Completare dati e autorizzare stampa bolle | Autorizzazione evasione / riesame | **R/U** · Autorizzazione evasione e dati per stampa. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Autorizza` · RGC · Completare dati e autorizzare stampa bolle | Bolla [prelievo] | **R/U** · Completamento bolle / trasporto. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Stampa` · SMAG · Stampare bolle di prelievo | Bolla [prelievo] | **R** · Stampa delle bolle autorizzate. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Prelievo` · Prelevare merce e verificare corrispondenza / scadenze | Bolla [prelievo] | **R** · Righe e quantità da prelevare. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Prelievo` · Prelevare merce e verificare corrispondenza / scadenze | Anagrafica prodotti / scorte; Tabella non specificata | **R** · Prodotti, scorte, lotti/scadenze; dettaglio tabelle non specificato. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_NC` · Aprire non conformità e isolare merce | Non conformità | **C** · Segnalazione non conformità; isolamento fisico non è Data Object. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Sostituisci` · RGC / MAG · Reperire merce conforme o ripianificare | Non conformità | **R** · Non conformità e rimedio; ramo didattico. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_ADRProd` · Verificare schede e conformità ADR del prodotto | Schede prodotto / prescrizioni ADR; Archivio documentale | **R** · Controllo documentale nel caso storico, non istruzioni normative attuali. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Allegati` · Richiedere schede e stampare certificati | Bolla [prelievo] | **R** · Note e richieste di allegati. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Allegati` · Richiedere schede e stampare certificati | Schede tecniche / certificati | **C** · Richiedere documenti a RGC/RTRAF e stampare certificati. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Imballa` · Allegare documenti, imballare ed etichettare | Schede tecniche / certificati | **R** · Allegare documenti quando richiesti. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Imballa` · Allegare documenti, imballare ed etichettare | Etichette / documenti di consegna | **C** · Etichette / documenti accompagnamento. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Arrivo` · Identificare ritirante, colli e veicolo | Etichette / documenti di consegna | **R** · Identificare colli, ritirante e destinazione. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Arrivo` · Identificare ritirante, colli e veicolo | Archivio spedizionieri qualificati; Tabella non specificata | **R** · Identità ritirante e spedizioniere. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_CheckADR` · Verificare idoneità veicolo e conducente ADR | Documenti veicolo / conducente | **R** · Documenti veicolo/conducente; controllo storico SAEM. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Cambia` · Richiedere mezzo / conducente idonei | Documenti veicolo / conducente | **R** · Esito non idoneo, nuovo controllo obbligatorio. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Incasso` · Verificare incasso o documenti di contrassegno | Documenti incasso / contrassegno | **R/U** · Verificare incasso o contrassegno; tabelle non specificate. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Carica` · Completare bolla, caricare e consegnare merce | Bolla [completata / evasa] | **C** · Completare dati consegna / targa e bolla. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Carica` · Completare bolla, caricare e consegnare merce | Etichette / documenti di consegna | **R** · Colli / etichette / documenti. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Partenza` · RMAG / SMAG · Registrare dati di partenza | Bolla [completata / evasa] | **R** · Dati effettivi di partenza. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |
| `L_Partenza` · RMAG / SMAG · Registrare dati di partenza | Archivio bolle / stato ordine; Gestionale · tabella non specificata | **U** · Aggiornare archivio bolle e stato ordine. | PDF 37, 72–74, 95 / stampate 25, 60–62, 83 |

Esplicitazioni / limiti per attività:

- `L_Sostituisci`: Risoluzione didattica dopo non conformità documentata.
- `L_Cambia`: Ramo di rimedio didattico al controllo ADR documentato; nessuna partenza su esito negativo.

### D.11 · Fatturazione della bolla evasa

Scenario: TO-BE · fatturazione mantenuta dal processo originale. Fonte di contesto: PDF 75 / stampata 63; PDF 37 / 25.

| ID / attività | Entità / sistema / tabelle | Relazione e dettaglio | Fonte PDF / stampata |
|---|---|---|---|
| `F_Verifica` · Verificare caricamento bolle ed escludere già fatturate | Archivio bolle evase / bolle fatturate; Gestionale · tabelle non specificate | **R** · Tutte le bolle evase caricate; esclusione già fatturate manualmente. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Recupera` · Recuperare fattura emessa e relativo stato contabile | Archivio fatture emesse; Tabella non specificata | **R** · Fattura già emessa. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Recupera` · Recuperare fattura emessa e relativo stato contabile | Prima nota contabile; Tabella non specificata | **R** · Stato registrazione per evitare duplicati; raccordo didattico. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Emetti` · Elaborare e stampare fattura | Archivio bolle evase / bolle fatturate; Gestionale · tabelle non specificate | **R/U** · Bolle da fatturare; stato di fatturazione è inferenza funzionale, tabella non specificata. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Emetti` · Elaborare e stampare fattura | Archivio fatture emesse; Tabella non specificata | **C** · Fattura prodotta; struttura fisica non specificata. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Emetti` · Elaborare e stampare fattura | Fattura [emessa] | **C** · Fattura emessa. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Posta` · Smistare e spedire fattura per posta | Fattura [emessa] | **R** · Smistare / spedire fattura. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Posta` · Smistare e spedire fattura per posta | Anagrafica cliente · canale invio; Tabella non specificata | **R** · Indirizzo destinatario. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Postel` · EDP · Generare e trasmettere file Postel | Fattura [emessa] | **R** · Dati fattura. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Postel` · EDP · Generare e trasmettere file Postel | File fatture Postel | **C** · File fatture Postel. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Contrassegno` · RTRAF / MAG · Gestire fattura contrassegno | Fattura [contrassegno] | **R/U** · Invio documenti a magazzino e archiviazione secondo D.11. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_Archivia` · Archiviare fattura / aggiornare catalogatore | Catalogatore / archivio fatture | **U** · Archivio fatture e catalogatore. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_PrimaNota` · Trasferire fattura in prima nota | Fattura [emessa] | **R** · Dati fattura emessa. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_PrimaNota` · Trasferire fattura in prima nota | Prima nota contabile; Tabella non specificata | **C** · Trasferimento fattura in prima nota. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_RegManuale` · Registrare fattura manuale in prima nota | Archivio fatture emesse; Tabella non specificata | **R** · Fattura manuale già esistente. | PDF 75 / stampata 63; PDF 37 / 25 |
| `F_RegManuale` · Registrare fattura manuale in prima nota | Prima nota contabile; Tabella non specificata | **C** · Solo quando non già registrata; raccordo didattico. | PDF 75 / stampata 63; PDF 37 / 25 |

Esplicitazioni / limiti per attività:

- `F_Recupera`: Raccordo didattico: esclusione bolle già fatturate esplicita, verifica contabile evita duplicazioni.
- `F_RegManuale`: Raccordo didattico per documento già emesso; prevenzione della doppia registrazione.

## Manutenzione e verifica

Le definizioni riutilizzabili sono in [estrazione-ordine.json](../../fonti-estratte/estrazione-ordine.json); [genera-bpmn.mjs](../../fonti-estratte/genera-bpmn.mjs) genera il modello completo e le sei viste autonome senza rileggere il PDF. Modificare prima le definizioni, poi rigenerare e riesportare dal Modeler. Una modifica fatta solo a una copia autonoma non viene propagata automaticamente.

Il dossier contiene un comando separato per riestrarre le fonti: non è necessario per modificare i diagrammi. Le anteprime sono esportate dal Camunda Modeler via MCP. L'importazione MCP diretta ha un limite di dimensione: il modello completo viene aperto da file, poi verificato e salvato tramite MCP; i dettagli più piccoli possono essere importati direttamente.

Controlli: conformità XSD BPMN 2.0, unicità e risoluzione degli ID, raggiungibilità dei nodi, copertura delle associazioni dati, assenza di attraversamenti delle forme da parte dei sequence flow e controllo visivo delle anteprime. Il controllo automatico di layout MCP sul modello completo supera il timeout: la verifica geometrica viene eseguita localmente sui BPMN DI.
