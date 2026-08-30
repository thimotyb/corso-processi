#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera il sito del corso processi-MOCI06 (home + 7 moduli + guida di laboratorio).

Riusa CSS/JS del corso datamesh (skill claude-course-builder): albero struttura a
due livelli, evidenziazione sezione attiva, pulsante di stampa, foglio di stile per
la stampa. Contenuti in italiano per coerenza con sillabo_processi_MOCI06.docx.
"""
import html
import pathlib

ROOT = pathlib.Path("/home/thimoty/git/corso-processi/site")
CH = ROOT / "chapters"

COURSE = "processi-MOCI06 — Classificazione e analisi dei processi industriali"

MODULES = [
    ("01", "M01 - Concetto di processo e logica cross-industry"),
    ("02", "M02 - APQC PCF: Category, Process Group, Process"),
    ("03", "M03 - Dalla Activity al Task"),
    ("04", "M04 - Variabili di processo e relazioni"),
    ("05", "M05 - Indicatori e misurazione"),
    ("06", "M06 - Rappresentazione: SIPOC, process map, swimlane, BPMN"),
    ("07", "M07 - Scheda processo completa (laboratorio integrato)"),
]

# id dell'ultima sezione (esercitazione) di ogni modulo — calcolato dal contenuto
LAB_ANCHOR = {}

# ---- contenuto dei moduli -------------------------------------------------------
# ogni modulo: lista di sezioni (livello, "numero titolo", [paragrafi], nota|None)
# livello 1 -> <h2>, livello 2 -> <h3>
CONTENT = {
"01": dict(
 sections=[
  (1,"1 Che cos'è un processo aziendale",[
   "Un processo aziendale è un insieme ordinato di attività che trasforma input in output di valore per un cliente interno o esterno. Ha un obiettivo dichiarato, un punto di inizio e uno di fine, e attraversa spesso più funzioni organizzative.",
   "La prospettiva per processi guarda al flusso di lavoro end-to-end, non alla singola unità che lo esegue. I confini del processo stabiliscono cosa è incluso e cosa resta fuori: l'evento che lo innesca e il risultato che lo chiude.",
  ],None),
  (2,"1.1 Obiettivo, confini, input e output",[
   "L'obiettivo esprime il motivo per cui il processo esiste, in termini di risultato per il cliente. Gli input sono le risorse informative e materiali necessarie ad avviarlo; gli output sono i prodotti o servizi che consegna.",
   "Input e output vanno nominati in modo concreto e verificabile, così da poterli riconoscere quando si presentano e da poterli misurare.",
  ],None),
  (2,"1.2 Clienti interni ed esterni",[
   "Il cliente del processo è chi riceve e utilizza l'output. Può essere esterno all'organizzazione oppure un'altra funzione interna che a sua volta alimenta un processo successivo.",
   "Riconoscere il cliente aiuta a stabilire quali caratteristiche dell'output contano davvero: tempestività, completezza, accuratezza, forma.",
  ],None),
  (2,"1.3 Evento di innesco ed evento finale",[
   "Ogni processo parte da un evento identificabile: l'arrivo di un ordine, una richiesta, una scadenza temporale. Termina con un evento altrettanto netto: un pagamento registrato, un servizio erogato, un documento approvato.",
   "Tra i due eventi si colloca tutto ciò che il processo governa. Definirli con precisione è la premessa per misurare durata, costi e responsabilità.",
  ],None),
  (1,"2 Funzione, processo, attività, task",[
   "Questi quattro termini descrivono livelli diversi. La funzione è un'unità organizzativa permanente (vendite, acquisti, IT). Il processo è un flusso di lavoro trasversale orientato a un risultato. L'attività è un passo del processo che produce un esito intermedio. Il task è l'azione elementare che compone un'attività.",
  ],None),
  (2,"2.1 Le quattro nozioni a confronto",[
   "La funzione risponde alla domanda «chi»; il processo alla domanda «come si ottiene il risultato»; l'attività a «quale passo»; il task a «quale gesto operativo».",
   "Una stessa funzione partecipa a più processi, e uno stesso processo impegna più funzioni.",
  ],None),
  (2,"2.2 Errori tipici di classificazione",[
   "Gli errori più comuni sono confondere il nome di una funzione con quello di un processo, descrivere un processo come elenco di reparti coinvolti anziché come sequenza di attività, e scendere al dettaglio del task quando serve ancora la vista d'insieme.",
   "Un buon test è verificare che il nome del processo contenga un verbo e un oggetto: «evadere l'ordine cliente», non «ufficio ordini».",
  ],None),
  (1,"3 Logica cross-industry",[
   "Una classificazione cross-industry descrive i processi con un vocabolario comune valido per settori diversi. Permette di confrontare organizzazioni eterogenee, riusare schemi di analisi e comunicare senza ambiguità tra funzioni e consulenti.",
  ],None),
  (2,"3.1 Perché una tassonomia comune",[
   "Senza un riferimento condiviso, ogni reparto nomina i processi a modo proprio e il confronto diventa impossibile. Una tassonomia comune fornisce nomi stabili e una gerarchia già definita, riducendo il tempo speso a mettersi d'accordo sui termini.",
  ],None),
  (2,"3.2 Benefici: analisi, benchmarking, digitalizzazione",[
   "Una vista ordinata dei processi supporta l'analisi organizzativa, il benchmarking con dati esterni, la definizione di responsabilità e indicatori, e le iniziative di digitalizzazione e automazione, che richiedono processi descritti in modo esplicito.",
  ],"I sette esempi in <code>esempi-apqc/</code> mostrano processi reali collocati in questo schema, uno per dominio funzionale."),
  (1,"4 Laboratorio",[
   "Scegliere un processo reale o simulato del proprio contesto. Redigere una scheda di mezza pagina con: obiettivo, evento di innesco, evento finale, tre input principali, output, cliente.",
   "Confrontare le schede in aula e discutere i confini scelti: dove un partecipante ha incluso un passo che un altro ha lasciato fuori, e perché.",
  ],None),
 ],
 kt=[
  "Un processo trasforma input in output di valore, con obiettivo, confini ed eventi di inizio e fine espliciti.",
  "Funzione, processo, attività e task sono livelli distinti: il nome di un processo contiene un verbo e un oggetto.",
  "Il cliente del processo, interno o esterno, determina quali caratteristiche dell'output sono rilevanti.",
  "Una tassonomia cross-industry dà nomi stabili e una gerarchia condivisa, presupposto di confronto e digitalizzazione.",
 ]),

"02": dict(
 sections=[
  (1,"1 Il Process Classification Framework di APQC",[
   "Il Process Classification Framework (PCF) di APQC è una tassonomia di processi aziendali organizzata in livelli gerarchici. Nasce per il benchmarking e viene usato come riferimento per mappare, confrontare e migliorare i processi.",
   "La versione Cross-Industry è indipendente dal settore e raccoglie i processi comuni alla maggior parte delle organizzazioni.",
  ],None),
  (2,"1.1 Origine e scopo",[
   "APQC è un'organizzazione di ricerca sul miglioramento delle prestazioni. Il PCF fornisce un elenco strutturato di processi con codici numerici stabili, così che organizzazioni diverse possano riferirsi agli stessi elementi.",
   "Lo scopo dichiarato è rendere confrontabili le prestazioni di processo, all'interno di un'azienda e verso l'esterno.",
  ],None),
  (2,"1.2 La versione Cross-Industry 8.0",[
   "La versione Cross-Industry copre i processi comuni a quasi tutte le organizzazioni, dai processi operativi a quelli di gestione e supporto. Ogni voce ha un codice gerarchico, per esempio 6.2.2, e un identificativo numerico univoco.",
   "È un punto di partenza da adattare al contesto specifico: alcune voci non si applicano, altre vanno aggiunte mantenendo la tracciabilità verso il codice PCF.",
  ],None),
  (1,"2 I livelli alti della gerarchia",[
   "Il PCF articola i processi su più livelli. I primi tre — Category, Process Group, Process — costituiscono l'ossatura con cui collocare qualsiasi attività aziendale.",
  ],None),
  (2,"2.1 Category (livello 1)",[
   "La Category è il raggruppamento più ampio, per esempio «Develop Vision and Strategy» o «Manage Customer Service». Rappresenta un'area di processi omogenea per finalità.",
   "Le Category operative descrivono la catena del valore; quelle di gestione e supporto descrivono le funzioni abilitanti.",
  ],None),
  (2,"2.2 Process Group (livello 2)",[
   "Il Process Group suddivide la Category in insiemi coerenti di processi. Dentro «Manage Customer Service» si trova, per esempio, «Plan and manage customer service contacts».",
   "Il Process Group aiuta a navigare la Category senza ancora entrare nel dettaglio operativo.",
  ],None),
  (2,"2.3 Process (livello 3)",[
   "Il Process è l'unità di analisi principale: ha un obiettivo, un innesco e un output, ed è governabile da un responsabile. «Manage customer service problems, requests, and inquiries» è un esempio di Process.",
   "È a questo livello che si costruiscono scheda processo, SIPOC e diagramma.",
  ],None),
  (1,"3 Identificare le Category in azienda",[
   "Collocare i processi reali nel PCF richiede di partire dalle finalità, non dai reparti. Si individuano prima le Category presenti, poi i Process Group pertinenti, infine i Process effettivamente eseguiti.",
  ],None),
  (2,"3.1 Processi operativi, di gestione e di supporto",[
   "I processi operativi generano direttamente valore per il cliente esterno: sviluppare prodotti, vendere, consegnare. I processi di gestione e supporto rendono possibile l'operatività: gestire IT, risorse umane, risorse finanziarie.",
   "La distinzione orienta le priorità di analisi e la scelta degli indicatori.",
  ],None),
  (2,"3.2 Esempi per dominio",[
   "Gli esempi del corso coprono sette domini: visione e strategia, vendite, acquisti, servizi, customer service, IT, finance. Ciascuno è collocato nei primi tre livelli PCF e poi sviluppato fino alla Activity.",
  ],"Per ogni dominio, <code>esempi-apqc/&lt;dominio&gt;/processo.md</code> riporta la collocazione PCF completa (Category → Process Group → Process → Activity) con i codici numerici originali."),
  (1,"4 Laboratorio",[
   "Scegliere un processo della propria organizzazione e collocarlo nei primi tre livelli del PCF, usando la tabella dei sette domini come riferimento. Motivare la scelta della Category in due righe.",
  ],None),
 ],
 kt=[
  "Il PCF è una tassonomia gerarchica di processi con codici stabili, pensata per confronto e miglioramento.",
  "I primi tre livelli sono Category, Process Group e Process; il Process è l'unità di analisi principale.",
  "La collocazione parte dalle finalità del processo, non dai reparti che lo eseguono.",
  "La distinzione tra processi operativi e processi di gestione e supporto orienta priorità e indicatori.",
 ]),

"03": dict(
 sections=[
  (1,"1 Il livello Activity",[
   "La Activity è il quarto livello del PCF: un passo del Process che produce un risultato intermedio riconoscibile. «Analyze problems, requests, and inquiries» è una Activity del processo di customer service.",
   "Le Activity sono descritte dal PCF con un verbo e un oggetto e con un identificativo numerico.",
  ],None),
  (2,"1.1 Definizione secondo il PCF",[
   "Ogni Process del PCF è scomposto in un elenco ordinato di Activity. L'elenco è un riferimento, non un vincolo: un'organizzazione può eseguirne solo una parte o aggiungerne di proprie, mantenendo la tracciabilità verso il codice PCF.",
  ],None),
  (2,"1.2 Leggere codice e identificativo",[
   "Una Activity si presenta come «6.2.2.2 Analyze problems, requests, and inquiries (13482)». Il codice 6.2.2.2 indica la posizione gerarchica; il numero tra parentesi è l'identificativo univoco APQC, utile per riferimenti stabili nel tempo.",
  ],None),
  (1,"2 Il livello Task",[
   "Il Task è l'azione elementare che compone una Activity. Il PCF si ferma alla Activity perché i Task dipendono dall'organizzazione, dagli strumenti e dalle prassi locali. Individuare i Task è compito dell'analista di processo.",
  ],None),
  (2,"2.1 Perché il PCF si ferma alla Activity",[
   "Sotto la Activity la variabilità tra organizzazioni diventa troppo alta per una tassonomia comune. Fissare i Task nel framework lo renderebbe rigido e poco riusabile.",
   "La separazione mantiene stabile la parte condivisa e lascia libera quella specifica.",
  ],None),
  (2,"2.2 Criteri per individuare Task elementari",[
   "Un Task è ben definito quando ha un esecutore unico, un esito verificabile e una durata breve rispetto alla Activity.",
   "Se un presunto Task richiede più ruoli o più decisioni, va scomposto ulteriormente. Se due Task si eseguono sempre insieme e dallo stesso ruolo, possono essere accorpati.",
  ],None),
  (1,"3 Scomposizione pratica",[
   "La scomposizione parte dal verbo della Activity e lo articola nei passi necessari a completarla, nell'ordine in cui si presentano.",
  ],None),
  (2,"3.1 Dal verbo della Activity ai passi operativi",[
   "Per «Analyze problems, requests, and inquiries» i Task possono essere: classificare la richiesta per tipologia e priorità; verificare storico cliente e SLA applicabili; determinare se serve escalation; assegnare la richiesta al ruolo competente.",
   "Ogni Task è un'azione con esito osservabile.",
  ],None),
  (2,"3.2 Granularità: quando fermarsi",[
   "Si smette di scomporre quando un ulteriore dettaglio non cambia responsabilità, tempi o strumenti. La granularità giusta è quella che rende il processo eseguibile e misurabile senza trasformarsi in un manuale di istruzioni.",
  ],"In <code>esempi-apqc/</code> ogni scheda riporta un esempio di scomposizione in Task di una Activity, segnalato esplicitamente come aggiunta didattica non presente nel PCF."),
  (1,"4 Laboratorio",[
   "Prendere una Activity di uno dei domini APQC e scomporla in quattro-sei Task, indicando per ciascuno l'esecutore e l'esito verificabile.",
   "Confrontare le scomposizioni in aula e discutere le differenze di granularità.",
  ],None),
 ],
 kt=[
  "La Activity è il quarto livello PCF: un passo del Process con esito intermedio, descritto da verbo e oggetto.",
  "Il PCF non definisce i Task perché dipendono da organizzazione, strumenti e prassi locali.",
  "Un Task ben definito ha esecutore unico, esito verificabile e durata breve rispetto alla Activity.",
  "La scomposizione si ferma quando un dettaglio in più non cambia responsabilità, tempi o strumenti.",
 ]),

"04": dict(
 sections=[
  (1,"1 Le variabili di processo",[
   "Le variabili di processo sono le grandezze che descrivono come il processo si comporta. Servono a caratterizzarlo, confrontarlo nel tempo e individuare dove intervenire. Si raggruppano in poche famiglie ricorrenti.",
  ],None),
  (2,"1.1 Input e output",[
   "Gli input sono ciò che il processo consuma per produrre il risultato: dati, documenti, materiali, autorizzazioni. Gli output sono ciò che consegna al cliente.",
   "Descrivere input e output in modo concreto è la base per tutte le altre variabili.",
  ],None),
  (2,"1.2 Tempi, costi, volumi",[
   "Il tempo misura la durata dall'innesco alla chiusura, incluse le attese. Il costo somma le risorse assorbite: ore di lavoro, costo dei sistemi, materiali. Il volume esprime quante volte il processo viene eseguito in un periodo.",
   "Insieme danno la dimensione economica del processo.",
  ],None),
  (2,"1.3 Ruoli, sistemi, vincoli, rischi",[
   "I ruoli sono gli attori che eseguono le attività. I sistemi sono gli applicativi a supporto. I vincoli sono limiti operativi o normativi da rispettare. I rischi sono gli eventi che possono degradare l'esito o bloccare il flusso.",
  ],None),
  (1,"2 La matrice delle variabili",[
   "La matrice delle variabili raccoglie in una tabella unica tutte le famiglie, con una descrizione e un esempio riferito al processo in analisi. È lo strumento che rende confrontabili processi diversi.",
  ],None),
  (2,"2.1 Struttura della matrice",[
   "Le righe sono le famiglie di variabili: input, output, tempi, costi, volumi, ruoli, sistemi, vincoli, rischi. Le colonne sono la descrizione generale e l'esempio concreto nel processo. Una riga aggiuntiva può annotare i colli di bottiglia.",
  ],None),
  (2,"2.2 Compilazione a partire dalla scheda processo",[
   "La matrice si compila leggendo la scheda processo e traducendone i contenuti in valori per ciascuna famiglia.",
   "Dove un valore manca, la lacuna stessa è un risultato utile: indica un aspetto del processo non ancora governato.",
  ],None),
  (1,"3 Relazioni tra variabili",[
   "Le variabili non sono indipendenti. Riconoscere le relazioni aiuta a prevedere l'effetto di un intervento.",
  ],None),
  (2,"3.1 Dipendenze, cause, effetti",[
   "Un aumento dei volumi allunga i tempi se la capacità resta invariata; un vincolo normativo introduce controlli che aumentano i costi; una classificazione errata a monte propaga errori a valle.",
   "Mappare queste catene rende espliciti i punti in cui agire.",
  ],None),
  (2,"3.2 Eccezioni e colli di bottiglia",[
   "Le eccezioni sono i percorsi alternativi che il processo segue in casi particolari. I colli di bottiglia sono i punti in cui il lavoro si accumula.",
   "Entrambi vanno individuati perché determinano gran parte della variabilità di tempi e costi.",
  ],"La scheda di ogni dominio in <code>esempi-apqc/</code> contiene una matrice delle variabili già compilata, utile come modello."),
  (1,"4 Laboratorio",[
   "Costruire la matrice delle variabili per la Activity scomposta nel Modulo 3. Aggiungere una riga con almeno un collo di bottiglia e indicare una relazione causa-effetto tra due variabili.",
  ],None),
 ],
 kt=[
  "Le variabili di processo si raggruppano in famiglie ricorrenti: input, output, tempi, costi, volumi, ruoli, sistemi, vincoli, rischi.",
  "La matrice delle variabili raccoglie le famiglie in una tabella con descrizione ed esempio concreto.",
  "Una lacuna nella matrice segnala un aspetto del processo non ancora governato.",
  "Le variabili sono legate da dipendenze e catene causa-effetto; eccezioni e colli di bottiglia spiegano gran parte della variabilità.",
 ]),

"05": dict(
 sections=[
  (1,"1 Perché misurare un processo",[
   "Misurare serve a sapere se il processo raggiunge il suo obiettivo, a confrontarne le prestazioni nel tempo e a decidere dove intervenire con dati anziché con impressioni. Senza misura, il miglioramento non è verificabile.",
  ],None),
  (2,"1.1 Controllo, confronto, miglioramento",[
   "Il controllo verifica che il processo resti entro limiti attesi. Il confronto mette a paragone periodi, sedi o organizzazioni. Il miglioramento usa la misura come riferimento prima e dopo un intervento.",
   "I tre usi richiedono indicatori stabili e definiti in modo univoco.",
  ],None),
  (2,"1.2 Efficienza ed efficacia",[
   "L'efficacia misura quanto l'output soddisfa il cliente: tempestività, qualità, completezza. L'efficienza misura quante risorse sono servite a produrlo: costo unitario, tempo di lavorazione.",
   "Un processo può essere efficace ma inefficiente, o viceversa.",
  ],None),
  (1,"2 Definire un KPI",[
   "Un indicatore chiave di prestazione è una misura scelta perché rappresentativa dell'obiettivo del processo. Va definito in modo che due persone diverse, con gli stessi dati, ottengano lo stesso valore.",
  ],None),
  (2,"2.1 Formula, unità, frequenza, fonte del dato",[
   "La definizione di un KPI comprende la formula di calcolo, l'unità di misura, la frequenza di rilevazione e la fonte da cui provengono i dati.",
   "Senza questi quattro elementi l'indicatore è ambiguo e non confrontabile.",
  ],None),
  (2,"2.2 Target e soglie",[
   "Il target è il valore atteso; le soglie delimitano le fasce di attenzione e di allarme. Target e soglie vanno fissati con un riferimento — storico interno, benchmark esterno, requisito contrattuale — e riesaminati periodicamente.",
  ],None),
  (1,"3 Collegare KPI e variabili",[
   "Gli indicatori più utili sono quelli legati alle variabili critiche del processo individuate nella matrice.",
  ],None),
  (2,"3.1 Dai colli di bottiglia agli indicatori di allerta",[
   "Ogni collo di bottiglia suggerisce un indicatore che ne segnala l'aggravarsi: coda in attesa, tempo di giacenza, percentuale di casi in escalation.",
   "Monitorare questi valori permette di intervenire prima che l'effetto si propaghi a valle.",
  ],None),
  (2,"3.2 Esempi per dominio",[
   "Per il customer service: tempo medio di risoluzione, risoluzione al primo contatto, soddisfazione del cliente. Per il ciclo attivo di finance: tempo di emissione fattura, percentuale di fatture con errori.",
   "Ogni dominio ha indicatori tipici da adattare al contesto.",
  ],"Le schede in <code>esempi-apqc/</code> includono una voce KPI coerente con l'obiettivo e i rischi del processo descritto."),
  (1,"4 Laboratorio",[
   "Definire due o tre KPI per il processo in analisi. Per ciascuno specificare formula, unità, frequenza, fonte del dato e un target motivato.",
  ],None),
 ],
 kt=[
  "La misura rende il miglioramento verificabile e sostituisce le impressioni con i dati.",
  "Efficacia ed efficienza sono dimensioni distinte: un processo può eccellere in una e non nell'altra.",
  "Un KPI è definito solo se ha formula, unità, frequenza e fonte del dato; target e soglie richiedono un riferimento.",
  "Gli indicatori più utili nascono dalle variabili critiche e dai colli di bottiglia della matrice.",
 ]),

"06": dict(
 sections=[
  (1,"1 Rappresentazioni sintetiche",[
   "Rappresentare un processo significa renderlo leggibile a colpo d'occhio. Le forme sintetiche precedono i diagrammi e ne preparano i contenuti.",
  ],None),
  (2,"1.1 Tabelle e matrici",[
   "Tabelle e matrici organizzano in righe e colonne gli elementi del processo: attività e responsabili, variabili e valori, rischi e contromisure. Sono rapide da compilare e da confrontare, e non richiedono strumenti grafici.",
  ],None),
  (2,"1.2 SIPOC: struttura e uso",[
   "Il SIPOC descrive il processo in cinque colonne: Supplier, Input, Process, Output, Customer. La colonna centrale contiene le macro-fasi in cinque-sette passi.",
   "Serve a fissare i confini e gli scambi con l'esterno prima di entrare nel dettaglio.",
  ],None),
  (1,"2 Process map e swimlane",[
   "I diagrammi di flusso mostrano la sequenza delle attività e le decisioni. Le corsie aggiungono la dimensione della responsabilità.",
  ],None),
  (2,"2.1 Mappa di processo per fasi",[
   "La process map dispone le attività nell'ordine di esecuzione, con i punti di decisione e gli esiti. Evidenzia ripetizioni, attese e passaggi di consegna. È la base per discutere semplificazioni.",
  ],None),
  (2,"2.2 Corsie per ruolo",[
   "Nel diagramma a corsie ogni corsia rappresenta un ruolo o un'unità, e ogni attività sta nella corsia di chi la esegue.",
   "I passaggi tra corsie rendono visibili gli handoff, spesso all'origine di ritardi ed errori.",
  ],None),
  (1,"3 Cenni a BPMN",[
   "BPMN (Business Process Model and Notation) è lo standard OMG per rappresentare i processi in modo formale, con un insieme di simboli condiviso.",
  ],None),
  (2,"3.1 Elementi di base",[
   "Gli elementi fondamentali sono l'evento (cerchio) per inizio, fine e accadimenti intermedi; l'attività (rettangolo arrotondato) per il lavoro svolto; il gateway (rombo) per le diramazioni; il flusso di sequenza (freccia) per l'ordine. Le corsie collocano gli elementi per responsabilità.",
  ],None),
  (2,"3.2 Quando serve una notazione formale",[
   "Una notazione formale conviene quando il diagramma deve essere interpretato senza ambiguità da persone diverse, quando descrive percorsi alternativi e condizioni, o quando è il punto di partenza per l'automazione.",
   "Per una panoramica rapida, SIPOC e process map restano più economici.",
  ],None),
  (1,"4 Visualizzare gli esempi con Camunda",[
   "I file <code>esempi-apqc/&lt;dominio&gt;/processo.bpmn</code> contengono i sette processi in notazione BPMN 2.0 con corsie per ruolo, pensati per essere proiettati e discussi in aula. Si aprono con Camunda Modeler, gratuito, senza alcun motore di esecuzione collegato.",
   "In aula: aprire due esempi — tra cui customer service o IT, che includono un gateway esclusivo — e leggere insieme corsie, eventi e diramazioni; poi chiedere ai partecipanti di aggiungere un ramo di eccezione o un ruolo mancante.",
   "Per chi vuole approfondire, un assistente AI collegato a Camunda tramite MCP può generare la prima bozza del diagramma da una scheda processo. La revisione del diagramma resta sempre a carico dell'analista.",
  ],"La guida <a href=\"../lab-camunda-mcp.html\">Laboratorio BPMN con Camunda e assistente MCP</a> raccoglie prerequisiti, installazione e primo esempio per chi vuole provare la generazione assistita."),
  (1,"5 Laboratorio",[
   "Aprire due esempi APQC in Camunda Modeler. Per ciascuno: identificare corsie, evento di innesco, evento finale e gateway. Aggiungere un ramo di eccezione plausibile e salvarne una copia.",
  ],None),
 ],
 kt=[
  "SIPOC e tabelle fissano confini e scambi prima del dettaglio grafico.",
  "La process map mostra sequenza e decisioni; le corsie aggiungono la responsabilità e rendono visibili gli handoff.",
  "BPMN è lo standard OMG: evento, attività, gateway, flusso di sequenza e corsie sono gli elementi di base.",
  "I file .bpmn del corso servono a visualizzare e discutere gli esempi; un assistente AI via MCP può produrre una bozza, ma la revisione è dell'analista.",
 ]),

"07": dict(
 sections=[
  (1,"1 La scheda processo sintetica",[
   "La scheda processo raccoglie in una pagina tutto ciò che serve per capire, governare e migliorare un processo. È il deliverable che integra i risultati dei moduli precedenti.",
  ],None),
  (2,"1.1 I campi della scheda",[
   "I campi minimi sono: nome del processo con codice PCF, process owner, obiettivo, confini (evento di innesco ed evento finale), ruoli coinvolti, sistemi coinvolti, KPI, rischi e colli di bottiglia.",
   "Ogni campo deve essere compilabile in poche righe.",
  ],None),
  (2,"1.2 Coerenza con i livelli gerarchici",[
   "Il nome e il codice collegano la scheda alla gerarchia PCF; l'elenco delle attività richiama le Activity del Process; la scomposizione in Task documenta il livello operativo.",
   "La scheda è coerente quando questi riferimenti si corrispondono senza salti.",
  ],None),
  (1,"2 Costruire la scheda end-to-end",[
   "La costruzione segue l'ordine dei moduli: collocazione, scomposizione, variabili, indicatori, rappresentazione.",
  ],None),
  (2,"2.1 Dalla collocazione PCF alla matrice delle variabili",[
   "Si parte dai primi tre livelli PCF per fissare identità e confini, si elencano le Activity, se ne scompone almeno una in Task, quindi si compila la matrice delle variabili.",
   "A questo punto la scheda ha già obiettivo, confini, ruoli, sistemi e rischi.",
  ],None),
  (2,"2.2 Dalla matrice alla rappresentazione",[
   "Dalle variabili si ricavano i KPI e, dalle attività e dai ruoli, il SIPOC e il diagramma a corsie o BPMN.",
   "Il diagramma verifica la coerenza della scheda: se un'attività non ha un ruolo o un esito, la lacuna emerge nel disegno.",
  ],None),
  (1,"3 Output e template aziendale",[
   "Il corso produce un pacchetto di deliverable riusabile come modello interno.",
  ],None),
  (2,"3.1 Il pacchetto di deliverable",[
   "Il pacchetto comprende: mappa gerarchica dei processi, scheda processo sintetica, elenco di attività e Task, matrice delle variabili e delle relazioni, diagramma di rappresentazione.",
   "Insieme descrivono il processo a tutti i livelli utili.",
  ],None),
  (2,"3.2 Riuso come template",[
   "Gli stessi campi e le stesse tabelle si applicano ad altri processi dell'organizzazione. Adottarli come formato standard rende i processi confrontabili e accelera le analisi successive.",
  ],"Le sette schede in <code>esempi-apqc/</code> sono esempi completi del pacchetto di deliverable, uno per dominio funzionale."),
  (1,"4 Laboratorio finale",[
   "Produrre la scheda processo completa di un dominio APQC a scelta: collocazione PCF, elenco attività, una Activity scomposta in Task, matrice delle variabili, due-tre KPI definiti, e il diagramma BPMN aperto in Camunda Modeler con almeno una modifica motivata.",
   "Presentare la scheda in aula in cinque minuti.",
  ],None),
 ],
 kt=[
  "La scheda processo integra in una pagina collocazione, attività, variabili, indicatori e rappresentazione.",
  "La coerenza si verifica quando nome e codice, Activity e Task si corrispondono senza salti.",
  "Il diagramma funziona da controllo: attività senza ruolo o senza esito emergono nel disegno.",
  "Il pacchetto di deliverable del corso è riusabile come template aziendale per confrontare i processi.",
 ]),
}

# ---- template ----------------------------------------------------------------

def esc(s): return html.escape(s, quote=True)

def slug_num(title):
    # "1 Titolo" / "1.1 Titolo" -> "1" / "1-1"
    n = title.split(" ", 1)[0]
    return n.replace(".", "-")

def page(title, body, depth):
    base = "../" * depth
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{base}assets/css/main.css">
<script defer src="{base}assets/js/back-to-top.js"></script>
</head>
<body>
{body}
<a class="back-to-top" href="#top" data-back-to-top aria-hidden="true" tabindex="-1">Torna su</a>
</body>
</html>
"""

def chapter_html(code, full_title, prev_m, next_m, data):
    idx = [m for m in MODULES if m[0] == code][0]
    # nav
    nav = ['<a href="../index.html">Home</a>']
    if prev_m:
        nav.append(f'<a href="chapter-{prev_m[0]}.html">Modulo precedente ({prev_m[1].split(" ")[0]})</a>')
    nav.append(f'<a href="chapter-{code}.html" aria-current="page">{esc(idx[1])}</a>')
    if next_m:
        nav.append(f'<a href="chapter-{next_m[0]}.html">Modulo successivo ({next_m[1].split(" ")[0]})</a>')
    navhtml = "\n   ".join(nav)

    # indice del modulo
    toc_items = []
    sec_html = []
    sid = 0
    for lvl, title, paras, note in data["sections"]:
        sid += 1
        anchor = f"s{sid:02d}"
        indent = "" if lvl == 1 else ' style="margin-left:1.1rem"'
        toc_items.append(f'<li{indent}><a href="#{anchor}">{esc(title)}</a></li>')
        LAB_ANCHOR[code] = anchor  # l'ultima sezione resta l'esercitazione
        tag = "h2" if lvl == 1 else "h3"
        parts = [f'<section class="study-section" id="{anchor}">',
                 f"  <{tag}>{esc(title)}</{tag}>"]
        for p in paras:
            parts.append(f"  <p>{p if '<code>' in p or '<a ' in p else esc(p)}</p>")
        if note:
            parts.append(f'  <div class="note-box">{note}</div>')
        parts.append("</section>")
        sec_html.append("\n".join(parts))

    kt = "\n".join(f"    <li>{esc(x)}</li>" for x in data["kt"])

    body = f"""<header class="hero" id="top">
 <h1>{esc(idx[1])}</h1>
</header>
<nav class="primary-nav" id="primary-nav" aria-label="Navigazione">
   {navhtml}
</nav>
<main class="content">
 <article>
  <section class="section-toc">
   <h2>Indice del modulo</h2>
   <ul>
    {"".join(toc_items)}
   </ul>
  </section>
{chr(10).join(sec_html)}
  <section class="key-takeaways">
   <h2>Punti chiave</h2>
   <ul>
{kt}
   </ul>
  </section>
 </article>
</main>
<div class="site-footer-note">
 <p>Materiale didattico del corso <strong>{esc(COURSE)}</strong>. I diagrammi BPMN e il laboratorio Camunda servono a visualizzare e discutere gli esempi; il taglio del corso resta metodologico e non tecnico.</p>
</div>"""
    return page(f"{idx[1]}", body, depth=1)

# ---- home ------------------------------------------------------------------

def index_html():
    mod_items = "\n".join(
        f'          <li><a href="chapters/chapter-{c}.html">{esc(t)}</a></li>'
        for c, t in MODULES)

    def a(code): return f"chapters/chapter-{code}.html#{LAB_ANCHOR[code]}"
    labs = [
        ("Laboratorio M01 - Confini di un processo", a("01"),
         "Redigere la scheda sintetica di un processo reale: obiettivo, eventi di innesco e fine, input, output, cliente."),
        ("Laboratorio M02 - Collocazione nel PCF", a("02"),
         "Collocare un processo aziendale nei primi tre livelli del Process Classification Framework di APQC."),
        ("Laboratorio M03 - Dalla Activity ai Task", a("03"),
         "Scomporre una Activity di un dominio APQC in quattro-sei Task con esecutore ed esito verificabile."),
        ("Laboratorio M04 - Matrice delle variabili", a("04"),
         "Costruire la matrice delle variabili con almeno un collo di bottiglia e una relazione causa-effetto."),
        ("Laboratorio M05 - Definire i KPI", a("05"),
         "Definire due-tre KPI con formula, unità, frequenza, fonte del dato e target motivato."),
        ("Laboratorio M06 - Visualizzare in Camunda", a("06"),
         "Aprire due esempi .bpmn in Camunda Modeler, leggerne corsie ed eventi, aggiungere un ramo di eccezione."),
        ("Laboratorio M07 - Scheda processo completa", a("07"),
         "Produrre il pacchetto completo di deliverable per un dominio APQC e presentarlo in aula."),
        ("Guida - BPMN con Camunda e assistente MCP", "lab-camunda-mcp.html",
         "Annesso opzionale: allestire l'ambiente (Claude, plugin MCP del Modeler, Camunda 8 in Docker) per generare le bozze BPMN dai prompt."),
        ("Esempi di processo APQC", "../esempi-apqc/",
         "Sette processi reali, uno per dominio: scheda in processo.md e diagramma in processo.bpmn."),
    ]
    lab_cards = "\n".join(
        f'''          <a class="lab-card" href="{esc(href)}">
            <h3>{esc(t)}</h3>
            <p>{esc(d)}</p>
          </a>''' for t, href, d in labs)

    siti = [
        ("APQC — Process Classification Framework", "https://www.apqc.org/process-frameworks"),
        ("APQC — Cross Industry PCF (PDF 8.0)", "https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-pdf-8"),
        ("Object Management Group — BPMN", "https://www.omg.org/spec/BPMN/"),
        ("BPMN.org — risorse introduttive", "https://www.bpmn.org/"),
        ("Camunda — BPMN tutorial e process modeling", "https://camunda.com/bpmn/"),
        ("Lucidchart — process mapping e swimlane", "https://www.lucidchart.com/pages/process-mapping"),
        ("Kaizen Institute — SIPOC e process optimization", "https://kaizen.com/insights/sipoc-process-optimization/"),
    ]
    siti_html = "\n".join(f'          <li><a href="{u}" target="_blank" rel="noopener noreferrer">{esc(n)}</a></li>' for n, u in siti)

    libri = [
        "Giampio Bracchi, Gianmario Motta, <em>Processi aziendali e sistemi informativi</em>, FrancoAngeli.",
        "Giampio Bracchi, Chiara Francalanci, Gianmario Motta, <em>Sistemi informativi e aziende in rete</em>, McGraw-Hill Education.",
        "Giampio Bracchi, Chiara Francalanci, Gianmario Motta, <em>Sistemi informativi d'impresa</em>, McGraw-Hill Education.",
        "Hans-Erik Eriksson, Magnus Penker, <em>Business Modeling with UML: Business Patterns at Work</em>, OMG Press / Wiley.",
    ]
    libri_html = "\n".join(f"          <li>{x}</li>" for x in libri)

    strumenti = [
        ('Camunda Modeler (desktop, gratuito)', 'https://camunda.com/download/modeler/'),
        ('Model Context Protocol — specifica', 'https://modelcontextprotocol.io/'),
        ('Camunda 8 — documentazione Self-Managed e Docker Compose', 'https://docs.camunda.io/docs/self-managed/quickstart/developer-quickstart/docker-compose/'),
        ('Plugin camunda-mcp per il Desktop Modeler', 'https://github.com/JesseLeresche/Camunda-mcp'),
    ]
    strum_html = "\n".join(f'          <li><a href="{u}" target="_blank" rel="noopener noreferrer">{esc(n)}</a></li>' for n, u in strumenti)

    kw = ("Process Classification Framework, Business Process Management, process mapping, SIPOC, "
          "swimlane, Business Process Model and Notation, Category, Process Group, Process, Activity, "
          "Task, input, output, key performance indicator, process owner, variabile, dipendenza, "
          "collo di bottiglia, miglioramento continuo, Camunda Modeler, Model Context Protocol.")

    body = f"""<header id="top" class="hero">
 <h1>{esc(COURSE)}</h1>
</header>
<nav id="primary-nav" class="primary-nav" aria-label="Navigazione">
 <a href="index.html" aria-current="page">Home</a>
 <a href="#moduli">Moduli</a>
 <a href="#caso-studio">Caso di studio</a>
 <a href="#laboratori">Laboratori</a>
 <a href="#riferimenti">Riferimenti</a>
</nav>
<main class="content">
 <section id="presentazione">
  <h2>Presentazione</h2>
  <p>Il corso introduce una metodologia pratica per descrivere, classificare e documentare i processi industriali. Il lavoro parte dai macro-processi aziendali e arriva fino ai task operativi. La classificazione produce una vista ordinata dei processi, utile per analisi organizzative, miglioramento continuo, benchmarking, digitalizzazione, automazione e definizione di responsabilità e indicatori.</p>
  <p>La rappresentazione BPMN e il laboratorio con Camunda Modeler servono a <strong>visualizzare gli esempi</strong> e a discuterli in aula, evitando che il percorso resti troppo teorico. Non è previsto alcun motore di esecuzione: l'uso è di sola modellazione.</p>
  <h3>Obiettivi</h3>
  <ul class="study-bullets">
   <li>Comprendere il significato di processo aziendale e di classificazione cross-industry.</li>
   <li>Applicare una struttura gerarchica a cinque livelli: Category, Process Group, Process, Activity e Task.</li>
   <li>Raggruppare i processi per aree funzionali omogenee.</li>
   <li>Scomporre le attività in task operativi e verificabili.</li>
   <li>Individuare variabili di processo, input, output, vincoli, indicatori e relazioni.</li>
   <li>Produrre documentazione sintetica e modelli di rappresentazione leggibili.</li>
  </ul>
  <h3>Informazioni</h3>
  <ul class="study-bullets">
   <li><strong>Modalità di erogazione</strong>: in aula o Live Virtual Classroom.</li>
   <li><strong>Durata</strong>: 2 giorni.</li>
   <li><strong>Prerequisiti</strong>: nessuno. È utile una conoscenza generale dell'organizzazione aziendale e dei principali flussi operativi.</li>
   <li><strong>Destinatari</strong>: analisti funzionali, referenti di processo, consulenti, project manager, figure di organizzazione, qualità, operations e trasformazione digitale.</li>
  </ul>
  <div class="note-box">Il corso non richiede competenze tecniche di programmazione. Il focus è metodologico e funzionale: capire come descrivere un processo, come scomporlo, come rappresentarlo e come renderlo confrontabile, misurabile e migliorabile.</div>
 </section>

 <section id="moduli">
  <h2>Moduli</h2>
  <p>Sette moduli tematici derivati dai blocchi principali del programma. I moduli 6 e 7 usano i diagrammi BPMN e Camunda Modeler come laboratorio di visualizzazione sugli esempi APQC.</p>
  <ul class="chapter-list">
{mod_items}
  </ul>
 </section>

 <section id="caso-studio">
  <h2>Caso di studio — SAEM S.p.A.</h2>
  <p>Un caso aziendale reale, usato come filo conduttore per rendere concreti tre dei sette esempi APQC. SAEM S.p.A. è un distributore italiano di prodotti industriali che, all'inizio degli anni 2000, ha reingegnerizzato il proprio processo di gestione ordini introducendo un portale di e-commerce B2B, per risolvere criticità sistematiche legate a doppia codifica degli articoli e conversione delle unità di misura tra cliente e fornitore.</p>
  <p>Le versioni astratte degli esempi APQC restano il riferimento primario del corso; le versioni SAEM, parallele e più ricche, servono a discutere ruoli, sistemi e rischi reali sullo stesso schema di analisi.</p>
  <a class="lab-card" href="caso-studio-saem.html">
    <h3>Caso di studio completo — SAEM S.p.A.</h3>
    <p>Profilo azienda, problema che ha innescato il progetto, tabella dei processi mappati su APQC e link alle tre schede arricchite (acquisti, customer service, finance).</p>
  </a>
 </section>

 <section id="laboratori">
  <h2>Laboratori</h2>
  <p>Ogni modulo si chiude con un'esercitazione a esito verificabile. La guida su Camunda e assistente MCP è un annesso opzionale per chi vuole provare la generazione assistita dei diagrammi.</p>
  <div class="labs-grid">
{lab_cards}
  </div>
 </section>

 <section id="riferimenti">
  <h2>Riferimenti per lo studio</h2>
  <h3>Framework e siti</h3>
  <ul class="reference-list">
{siti_html}
  </ul>
  <h3>Libri consigliati</h3>
  <ul class="reference-list">
{libri_html}
  </ul>
  <h3>Strumenti</h3>
  <ul class="reference-list">
{strum_html}
  </ul>
  <h3>Parole chiave da conoscere</h3>
  <p>{esc(kw)}</p>
 </section>
</main>
<div class="site-footer-note">
 <p>Sito del corso <strong>{esc(COURSE)}</strong>. Struttura dei moduli e componenti di navigazione ripresi dalle convenzioni della skill di produzione corsi <em>claude-course-builder</em>; contenuti in italiano, coerenti con <code>sillabo_processi_MOCI06.docx</code>.</p>
</div>"""
    return page(f"{COURSE}", body, depth=0)

# ---- guida di laboratorio (annesso, ex-MOCI07) ----------------------------

def lab_html():
    body = f"""<header class="hero" id="top">
 <h1>Laboratorio BPMN con Camunda e assistente MCP</h1>
</header>
<nav class="primary-nav" id="primary-nav" aria-label="Navigazione">
 <a href="index.html">Home</a>
 <a href="chapters/chapter-06.html">Modulo 6</a>
 <a href="lab-camunda-mcp.html" aria-current="page">Guida di laboratorio</a>
</nav>
<main class="content">
 <article>
  <section class="section-toc">
   <h2>Indice</h2>
   <ul>
    <li><a href="#s01">1 A cosa serve questa guida</a></li>
    <li><a href="#s02">2 Architettura: i tre componenti</a></li>
    <li><a href="#s03">3 Prerequisiti</a></li>
    <li><a href="#s04">4 Motore Camunda 8 in Docker</a></li>
    <li><a href="#s05">5 Camunda Desktop Modeler e plugin MCP</a></li>
    <li><a href="#s06">6 Collegare Claude e primo diagramma</a></li>
    <li><a href="#s07">7 Rete su WSL2</a></li>
    <li><a href="#s08">8 Troubleshooting</a></li>
   </ul>
  </section>

  <section class="study-section" id="s01">
   <h2>1 A cosa serve questa guida</h2>
   <p>Questo è un <strong>annesso opzionale</strong> al Modulo 6: non fa parte del programma d'aula e non è un sillabo. Serve a chi, dopo aver visto i diagrammi BPMN degli esempi APQC, vuole provare a generarne una bozza a partire da una scheda processo, coordinandosi con i prompt.</p>
   <p>Lo strumento è un assistente (Claude) collegato al Camunda Desktop Modeler tramite un server MCP. La generazione produce una prima stesura; la revisione del diagramma resta sempre compito dell'analista.</p>
   <div class="note-box">Il taglio del corso non cambia: la modellazione BPMN qui è un supporto alla visualizzazione e alla discussione, non un obiettivo tecnico.</div>
  </section>

  <section class="study-section" id="s02">
   <h2>2 Architettura: i tre componenti</h2>
   <p><strong>Claude Code</strong> — il client che chiama i tool via MCP. Gira dove lo si avvia, anche dentro WSL.</p>
   <p><strong>Camunda Desktop Modeler + plugin <code>camunda-mcp</code></strong> — applicazione desktop. Il plugin espone un server MCP HTTP su <code>localhost:3100/mcp</code> con cui l'assistente crea e modifica il diagramma visibile a schermo. Non è containerizzabile: richiede un ambiente grafico.</p>
   <p><strong>Motore Camunda 8</strong> — runtime che esegue i processi distribuiti. Questo componente gira in Docker ed è il bersaglio del tool <code>deploy_process</code>. È opzionale se serve solo produrre il file <code>.bpmn</code>.</p>
  </section>

  <section class="study-section" id="s03">
   <h2>3 Prerequisiti</h2>
   <ul class="study-bullets">
    <li>Docker Desktop con backend WSL2 — <code>docker</code> &ge; 20.10.16, <code>docker compose</code> &ge; 2.24.</li>
    <li>Node.js &ge; 20 e npm &ge; 9 (solo per la build del plugin dai sorgenti).</li>
    <li>Camunda Desktop Modeler 5.x — da <a href="https://camunda.com/download/modeler/" target="_blank" rel="noopener noreferrer">camunda.com/download/modeler</a>.</li>
    <li>Claude Code, oppure Claude Desktop con transport MCP HTTP.</li>
    <li>Circa 4–6 GB di RAM liberi per lo stack Camunda 8.</li>
   </ul>
  </section>

  <section class="study-section" id="s04">
   <h2>4 Motore Camunda 8 in Docker</h2>
   <p>Scaricare e avviare il Docker Compose ufficiale per la versione 8.9.</p>
   <div class="code-label">bash — WSL</div>
   <pre><code>curl -L -o docker-compose-8.9.zip \\
  https://github.com/camunda/camunda-distributions/releases/download/docker-compose-8.9/docker-compose-8.9.zip
unzip docker-compose-8.9.zip
cd docker-compose-8.9
docker compose up -d
docker compose ps
docker compose logs -f orchestration connectors</code></pre>
   <ul class="study-bullets">
    <li>REST API del cluster e Zeebe: <code>http://localhost:8080</code>; gateway gRPC: <code>localhost:26500</code>.</li>
    <li>Operate: <code>http://localhost:8080/operate</code> &middot; Tasklist: <code>http://localhost:8080/tasklist</code>.</li>
    <li>Login di default: <code>demo</code> / <code>demo</code>.</li>
    <li>Stop: <code>docker compose down</code> (mantiene i dati) oppure <code>docker compose down -v</code> (cancella tutto).</li>
   </ul>
   <div class="note-box">Il nome della cartella estratta e la mappa delle porte possono variare per patch: verificare il <code>README</code> del pacchetto compose.</div>
  </section>

  <section class="study-section" id="s05">
   <h2>5 Camunda Desktop Modeler e plugin MCP</h2>
   <p>Installare il Modeler 5.x, poi il plugin <code>camunda-mcp</code> (<a href="https://github.com/JesseLeresche/Camunda-mcp" target="_blank" rel="noopener noreferrer">repository</a>, licenza MIT).</p>
   <div class="code-label">bash — build dai sorgenti</div>
   <pre><code>git clone https://github.com/JesseLeresche/Camunda-mcp.git
cd Camunda-mcp
npm install
npm run build
ln -s "$(pwd)" ~/.config/camunda-modeler/resources/plugins/camunda-mcp</code></pre>
   <ul class="study-bullets">
    <li>Cartella plugin: Linux/WSLg <code>~/.config/camunda-modeler/resources/plugins/</code>; macOS <code>~/Library/Application Support/camunda-modeler/resources/plugins/</code>; Windows <code>%APPDATA%\\camunda-modeler\\resources\\plugins\\</code>.</li>
    <li>Variabili d'ambiente (prima di avviare il Modeler): <code>MCP_PORT</code> (default 3100), <code>MCP_API_KEY</code>, <code>ZEEBE_ADDRESS=localhost:26500</code>.</li>
    <li>Verifica: nel menu <strong>Plugins</strong> deve comparire &laquo;MCP Server: Running (port 3100)&raquo;.</li>
   </ul>
   <div class="code-label">verifica — il server risponde</div>
   <pre><code>curl -s -X POST http://localhost:3100/mcp \\
  -H 'Content-Type: application/json' \\
  -H 'Accept: application/json, text/event-stream' \\
  -d '{{"jsonrpc":"2.0","method":"tools/list","id":1}}'</code></pre>
  </section>

  <section class="study-section" id="s06">
   <h2>6 Collegare Claude e primo diagramma</h2>
   <div class="code-label">bash</div>
   <pre><code>claude mcp add --transport http camunda-modeler http://localhost:3100/mcp</code></pre>
   <p>In alternativa, in <code>.mcp.json</code> nella cartella di progetto:</p>
   <div class="code-label">.mcp.json</div>
   <pre><code>{{
  "mcpServers": {{
    "camunda-modeler": {{ "type": "http", "url": "http://localhost:3100/mcp" }}
  }}
}}</code></pre>
   <p>Lanciare <code>/mcp</code> in Claude Code, confermare che <code>camunda-modeler</code> è connesso e approvare il server. Con il Modeler aperto, un prompt di prova:</p>
   <div class="note-box">Nel Camunda Modeler crea un nuovo diagramma <code>leave-request</code>: start event &laquo;Richiesta inviata&raquo; &rarr; user task &laquo;Valuta richiesta&raquo; &rarr; gateway esclusivo &laquo;Approvata?&raquo;; sul ramo sì un service task &laquo;Notifica approvazione&raquo;, sul ramo no un service task &laquo;Notifica rifiuto&raquo;; entrambi confluiscono in un end event &laquo;Richiesta chiusa&raquo;. Disponi il layout da sinistra a destra e valida.</div>
   <p>L'assistente chiama in sequenza i tool <code>manage_diagram</code>, <code>build_process</code> o <code>add_element</code> più <code>connect</code>, <code>layout</code>, <code>query_diagram</code>. Il diagramma compare nella finestra del Modeler. Per distribuirlo: &laquo;Salva il diagramma, poi distribuiscilo sul Camunda 8 locale con <code>deploy_process</code>&raquo; (serve <code>ZEEBE_ADDRESS</code> raggiungibile).</p>
  </section>

  <section class="study-section" id="s07">
   <h2>7 Rete su WSL2</h2>
   <ul class="study-bullets">
    <li>Consigliato: eseguire il Modeler dentro WSL via WSLg, così Modeler, plugin e client vedono <code>localhost:3100</code> nativamente.</li>
    <li>Modeler su Windows e client in WSL: abilitare il mirrored networking in <code>%USERPROFILE%\\.wslconfig</code> con <code>[wsl2]</code> e <code>networkingMode=mirrored</code>, poi <code>wsl --shutdown</code>; in alternativa usare l'IP dell'host Windows al posto di <code>localhost</code>.</li>
    <li>Docker Desktop con backend WSL2: le porte pubblicate dai container compaiono su <code>localhost</code> dentro WSL.</li>
   </ul>
  </section>

  <section class="study-section" id="s08">
   <h2>8 Troubleshooting</h2>
   <ul class="study-bullets">
    <li><strong>Il menu Plugins non mostra il server</strong>: cartella plugin errata o build assente; verificare il percorso per il sistema operativo e la presenza di <code>dist/</code>, poi riavviare il Modeler.</li>
    <li><strong><code>/mcp</code> in stato failed</strong>: Modeler non avviato oppure porta 3100 non raggiungibile dal client (caso Windows&harr;WSL: vedi sezione 7). Provare prima il <code>curl</code> di verifica.</li>
    <li><strong><code>deploy_process</code> fallisce</strong>: <code>ZEEBE_ADDRESS</code> non impostato prima dell'avvio del Modeler, gateway 26500 non esposto, oppure autenticazione del cluster attiva senza credenziali.</li>
    <li><strong>Porta 3100 occupata</strong>: il server ripiega su 3101–3102; aggiornare l'URL in <code>.mcp.json</code> o fissare <code>MCP_PORT</code>.</li>
   </ul>
   <div class="note-box">Nomi degli asset di release e mappa delle porte 8.9 vanno confermati sulle pagine ufficiali: <a href="https://github.com/JesseLeresche/Camunda-mcp" target="_blank" rel="noopener noreferrer">repository del plugin</a> e <a href="https://docs.camunda.io/docs/self-managed/quickstart/developer-quickstart/docker-compose/install-start/" target="_blank" rel="noopener noreferrer">quickstart Docker Compose di Camunda</a>.</div>
  </section>
 </article>
</main>
<div class="site-footer-note">
 <p>Annesso di laboratorio del corso <strong>{esc(COURSE)}</strong>. Contenuto opzionale, non incluso nel programma d'aula.</p>
</div>"""
    return page("Laboratorio BPMN con Camunda e assistente MCP", body, depth=0)

# ---- caso di studio: SAEM S.p.A. ------------------------------------------

def caso_studio_html():
    body = f"""<header class="hero" id="top">
 <h1>Caso di studio — SAEM S.p.A.</h1>
</header>
<nav class="primary-nav" id="primary-nav" aria-label="Navigazione">
 <a href="index.html">Home</a>
 <a href="caso-studio-saem.html" aria-current="page">Caso di studio</a>
</nav>
<main class="content">
 <article>
  <section class="section-toc">
   <h2>Indice</h2>
   <ul>
    <li><a href="#s01">1 Perché questo caso di studio</a></li>
    <li><a href="#s02">2 L'azienda SAEM S.p.A.</a></li>
    <li><a href="#s03">3 Il problema che ha innescato il progetto</a></li>
    <li><a href="#s04">4 I tre processi già sviluppati sul caso</a></li>
    <li><a href="#s05">5 Altri processi SAEM (candidati non ancora sviluppati)</a></li>
    <li><a href="#s06">6 Come usarlo in aula</a></li>
    <li><a href="#s07">7 Fonti</a></li>
   </ul>
  </section>

  <section class="study-section" id="s01">
   <h2>1 Perché questo caso di studio</h2>
   <p>Gli esempi APQC del corso (<code>esempi-apqc/</code>) sono volutamente astratti: gerarchia PCF corretta, ma azienda e ruoli generici. SAEM S.p.A. è un caso aziendale reale (tesi di laurea, Politecnico di Milano, A.A. 2004-2005) che permette di ripetere lo stesso esercizio di classificazione e mappatura su un'organizzazione con ruoli, sistemi e criticità documentati.</p>
   <p>Le versioni SAEM non sostituiscono gli esempi astratti: li affiancano, sotto <code>caso-saem/esempi-apqc/</code>, come varianti più ricche sulla stessa gerarchia PCF e lo stesso Process.</p>
  </section>

  <section class="study-section" id="s02">
   <h2>2 L'azienda SAEM S.p.A.</h2>
   <p>Fondata nel 1904, SAEM è un <strong>distributore</strong> italiano di prodotti industriali ad alto contenuto tecnologico (adesivi e sigillanti, lubrificanti speciali, macchine utensili, componenti per automazione): non produce, importa e distribuisce prodotti di case produttrici internazionali di cui è rappresentante esclusivo.</p>
   <ul class="study-bullets">
    <li><strong>Fatturato</strong>: 12,5-25 milioni di euro; <strong>organico</strong>: ~57 dipendenti + 16 agenti + rete di ~340 distributori.</li>
    <li><strong>Clienti</strong>: oltre 3.500 attivi, in 25 settori industriali. <strong>Fornitori</strong>: oltre 100 case produttrici.</li>
    <li><strong>Struttura</strong>: funzionale al primo livello, 4 divisioni (Chimica, Macchine, Componenti, Hi-Tech); organizzazione vendite a matrice (Responsabili Prodotto, Industria, Area).</li>
    <li><strong>Certificazioni</strong>: ISO 9001 e ISO 14001. <strong>Posizionamento competitivo</strong>: la tecnologia non basta più a differenziare — contano tempestività, personalizzazione e assistenza pre/post vendita.</li>
    <li><strong>Sistemi storici</strong>: Pragma (Client/Server a caratteri, DOS) e MaxGestCS (Java + PostgreSQL), sincronizzati ogni notte.</li>
   </ul>
   <div class="note-box">Ruoli citati nei processi: DIRV (Direttore Vendite), FC (Funzionario Commerciale), RGC (Responsabile Gestione Commerciale), RTRAF (Responsabile Traffico), RMAG/SMAG (Responsabile/Segretario Magazzino), RCONT (Responsabile Contabilità).</div>
  </section>

  <section class="study-section" id="s03">
   <h2>3 Il problema che ha innescato il progetto</h2>
   <p>Il processo di gestione ordini (offerta &rarr; ordine &rarr; evasione &rarr; fatturazione), interamente manuale, generava due criticità sistematiche:</p>
   <ol class="study-bullets">
    <li><strong>Conversione delle unità di misura</strong>: i clienti ordinano in unità proprie (es. grammi), SAEM vende in confezioni indivisibili (fusti, cartucce) &rarr; conversione manuale a rischio d'errore.</li>
    <li><strong>Doppia codifica articolo</strong>: ogni cliente usa un proprio codice interno diverso da quello SAEM &rarr; l'operatore deve tradurre a mano dalla descrizione.</li>
   </ol>
   <p>Questi errori generavano costi di gestione resi, ritardi di consegna e un peggioramento del servizio percepito — da cui la decisione della direzione di reingegnerizzare il processo introducendo un portale di inserimento ordini diretto da parte del cliente (progetto "Maxnet").</p>
  </section>

  <section class="study-section" id="s04">
   <h2>4 I tre processi già sviluppati sul caso</h2>
   <ul class="study-bullets">
    <li><strong>Selezione e qualifica fornitori</strong> &mdash; 4.0 &rarr; 4.2.3 Select suppliers and develop/maintain contracts &mdash; <a href="../caso-saem/esempi-apqc/03-acquisti/processo.md">processo.md</a> / <a href="../caso-saem/esempi-apqc/03-acquisti/processo.bpmn">processo.bpmn</a></li>
    <li><strong>Ritiro prodotti, resi e riparazione deceleratori</strong> &mdash; 6.0 &rarr; 6.2.2 Manage customer service problems, requests, and inquiries &mdash; <a href="../caso-saem/esempi-apqc/05-customer-service/processo.md">processo.md</a> / <a href="../caso-saem/esempi-apqc/05-customer-service/processo.bpmn">processo.bpmn</a></li>
    <li><strong>Fatturazione settimanale</strong> &mdash; 9.0 &rarr; 9.2.2 Invoice customer &mdash; <a href="../caso-saem/esempi-apqc/07-finance/processo.md">processo.md</a> / <a href="../caso-saem/esempi-apqc/07-finance/processo.bpmn">processo.bpmn</a></li>
   </ul>
   <p>Ogni scheda ripete la stessa struttura degli esempi astratti (collocazione PCF, Activity, scomposizione in Task, SIPOC, matrice delle variabili, scheda sintetica, BPMN) ma con scenario, ruoli e flusso presi dal caso reale — i diagrammi BPMN qui includono anche gateway che nella versione astratta non c'erano (es. esito del vendor rating, tipo di richiesta reso/riparazione, canale di fatturazione).</p>
  </section>

  <section class="study-section" id="s05">
   <h2>5 Altri processi SAEM (candidati non ancora sviluppati)</h2>
   <p>Il caso ne descrive molti altri, con un match APQC meno diretto o non ancora verificato sul PCF completo: programmazione ordini a fornitore, controllo qualità in ingresso, gestione reso a fornitore, preparazione offerta al cliente, selezione spedizioniere, generazione bolle/carico veicolo, gestione sistema informativo legacy, progetto di reengineering/e-commerce, posizionamento strategico, sistema qualità/ambiente. Sono candidati per estensioni future del materiale, se il corso vorrà arricchire anche i domini Vendite, Vision&amp;Strategy o IT con questo stesso caso.</p>
  </section>

  <section class="study-section" id="s06">
   <h2>6 Come usarlo in aula</h2>
   <p>Per ciascuno dei tre processi si può ripetere l'esercizio già impostato per gli esempi APQC astratti: individuare Category/Process Group/Process/Activity nel PCF, scomporre in Task, costruire SIPOC e matrice delle variabili, leggere il BPMN con le corsie per ruolo. A differenza degli esempi puri, qui i partecipanti lavorano su un caso con <strong>criticità reali già documentate</strong> (doppia codifica articoli, autorizzazioni di prezzo/reso, shelf life breve) da usare come base per la discussione su rischi e colli di bottiglia.</p>
  </section>

  <section class="study-section" id="s07">
   <h2>7 Fonti</h2>
   <ul class="reference-list">
    <li>C. Bozzoli, <em>"Reengineering del sistema di gestione ordini in ottica e-commerce: il caso SAEM S.p.A."</em>, tesi di laurea, Politecnico di Milano, A.A. 2004-2005 (relatore Prof. Ing. T. Barbieri) — <a href="../resources/casoSAEM.pdf">PDF completo</a>.</li>
    <li><a href="../caso-saem/caso-saem-compresso.md">Versione compressa del caso</a> (azienda, organizzazione, i quattro processi principali) usata come base per le schede.</li>
   </ul>
  </section>
 </article>
</main>
<div class="site-footer-note">
 <p>Caso di studio del corso <strong>{esc(COURSE)}</strong>. Affianca, senza sostituire, gli esempi APQC astratti.</p>
</div>"""
    return page("Caso di studio — SAEM S.p.A.", body, depth=0)

# ---- scrittura ------------------------------------------------------------

# prima i moduli (popolano LAB_ANCHOR), poi la home che li referenzia
for i, (code, title) in enumerate(MODULES):
    prev_m = MODULES[i-1] if i > 0 else None
    next_m = MODULES[i+1] if i < len(MODULES)-1 else None
    (CH / f"chapter-{code}.html").write_text(
        chapter_html(code, title, prev_m, next_m, CONTENT[code]), encoding="utf-8")
(ROOT / "index.html").write_text(index_html(), encoding="utf-8")
(ROOT / "lab-camunda-mcp.html").write_text(lab_html(), encoding="utf-8")
(ROOT / "caso-studio-saem.html").write_text(caso_studio_html(), encoding="utf-8")

print("scritti:")
for p in sorted(ROOT.rglob("*.html")):
    print("  ", p.relative_to(ROOT), p.stat().st_size, "byte")
