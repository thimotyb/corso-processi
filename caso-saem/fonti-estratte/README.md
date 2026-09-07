# Evidenze SAEM riutilizzabili

Archivio locale dell'estrazione svolta il 6 settembre 2026 per la gestione ordine cliente. Consultare questo dossier prima di ripetere il parsing del PDF.

- `estrazione-ordine.json`: attività, flussi, responsabilità, archivi, relazioni CRUD e riferimenti alla fonte, in formato riutilizzabile.
- `scratchpad-requisiti-processo.md`: evidenze sulla raccolta, derivazione, specifica e gestione iterativa dei requisiti, con riferimenti alle pagine della tesi.
- `testo-pagine.md`: testo delle pagine consultate; numerazione PDF da 1 e corrispondente pagina stampata.
- `pagine/`: rendering delle figure esaminate visivamente. Le frecce delle figure non sono ricostruibili dal solo testo estratto.
- `manifest.json`: impronta SHA-256 del PDF e pagine archiviate, per riconoscere eventuali cambiamenti della fonte.
- `../esempi-apqc/02-gestione-ordine/processo.md`: perimetro, scelte BPMN, matrice attività–dati e limiti documentati.

Fonte: `resources/casoSAEM.pdf`, C. Bozzoli, tesi sul caso SAEM, A.A. 2004–2005. Il dossier conserva un estratto di lavoro della fonte già presente nel progetto.

## Distinzioni da conservare

- Assembly Line e CRUD del capitolo VII descrivono il TO-BE, anche quando usano tabelle esistenti.
- MaxGestCS e MaxNet sono applicazioni; PostgreSQL è il DBMS; Emaxgest5 è il database. Il testo originale talvolta chiama Emaxgest5 anche «DBMS».
- D.2C presenta la variante sviluppatori (sostituzione ordine, nuova priorità) e la proposta dell'autrice (aggiornamento, mantenimento priorità). I CRUD in corsivo/asteriscati sono della seconda variante; il BPMN realizzato adotta la prima.
- Le procedure logistiche e contabili mantenute dal macroprocesso TO-BE usano archivi descritti dalla fonte; non attribuire loro tabelle del capitolo VII senza evidenza.
- `evidence` nei dati strutturati distingue esplicitazioni didattiche e dettagli non specificati; una fonte associata a un task non rende automaticamente documentata ogni scelta BPMN.

La matrice strutturata descrive relazioni di business e accesso ai dati; non è una specifica SQL eseguibile. Eventuali implementazioni richiedono anche transazioni, concorrenza e riconciliazione degli impegni di magazzino.
