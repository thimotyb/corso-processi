#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera il sito del corso processi-MOCI06 (home + 8 moduli + guida di laboratorio).

Riusa CSS/JS del corso datamesh (skill claude-course-builder): albero struttura a
due livelli, evidenziazione sezione attiva, pulsante di stampa, foglio di stile per
la stampa. Contenuti in italiano per coerenza con sillabo_processi_MOCI06.docx.
"""
import html
import pathlib

ROOT = pathlib.Path("/home/thimoty/git/corso-processi/site")
CH = ROOT / "chapters"

COURSE = "processi-MOCI06 — Classificazione e analisi dei processi industriali"
REPO_BLOB = "https://github.com/thimotyb/corso-processi/blob/main/"
REPO_TREE = "https://github.com/thimotyb/corso-processi/tree/main/"

MODULES = [
    ("01", "M01 - Classificazione e architettura dei processi"),
    ("02", "M02 - Raccolta e documentazione dei requisiti"),
    ("03", "M03 - APQC PCF: Category, Process Group, Process"),
    ("04", "M04 - Dalla Activity al Task"),
    ("05", "M05 - Variabili di processo e relazioni"),
    ("06", "M06 - Indicatori e misurazione"),
    ("07", "M07 - Rappresentazione: SIPOC, process map, swimlane, BPMN"),
    ("08", "M08 - Scheda processo completa (laboratorio integrato)"),
]

# id dell'ultima sezione (esercitazione) di ogni modulo — calcolato dal contenuto
LAB_ANCHOR = {}

# ---- contenuto dei moduli -------------------------------------------------------
# ogni modulo: lista di sezioni (livello, "numero titolo", [paragrafi], nota|None)
# livello 1 -> <h2>, livello 2 -> <h3>
CONTENT = {
"01": dict(
 sections=[
  (1,"1 Il processo aziendale",[
   "Un <strong>processo aziendale</strong> è una sequenza strutturata e ripetibile di attività che consente all'organizzazione di raggiungere un obiettivo. Non è soltanto un elenco di operazioni: è un insieme coordinato di azioni, decisioni e passaggi che porta da una situazione iniziale a un risultato atteso.",
   "Un processo può essere eseguito da <strong>persone</strong>, <strong>sistemi informativi</strong> o <strong>macchinari</strong> e, nella maggior parte dei casi, combina questi diversi esecutori. La sua utilità consiste nel rendere comprensibile come il lavoro viene svolto e in che modo le singole attività contribuiscono al risultato complessivo.",
   "Ogni processo riceve uno o più <strong>input</strong> e li trasforma in <strong>output</strong>. Gli input possono essere dati, informazioni, documenti, materiali, richieste, autorizzazioni o altre risorse necessarie per iniziare e completare il lavoro. Gli output sono i risultati prodotti dal processo: un bene, un servizio, una decisione, un documento, una registrazione o un'informazione destinata a un altro soggetto.",
   "Un output non è necessariamente il prodotto venduto al cliente finale. Può essere anche un <strong>risultato intermedio</strong> che alimenta un processo successivo. Per esempio, l'ordine registrato dall'ufficio vendite può diventare l'input per la verifica amministrativa, per la preparazione della merce e per la pianificazione della consegna.",
   "Il processo è orientato a uno <strong>scopo</strong>. Le sue componenti principali possono essere osservate attraverso queste domande:",
   "<ul class=\"study-bullets\"><li><strong>Obiettivo</strong>: perché il processo esiste e quale risultato deve rendere possibile?</li><li><strong>Attività</strong>: che cosa deve essere fatto per raggiungere il risultato?</li><li><strong>Ruoli</strong>: chi è responsabile delle diverse parti del lavoro?</li><li><strong>Regole</strong>: quali condizioni, vincoli o criteri devono essere rispettati?</li><li><strong>Indicatori</strong>: come si verifica se il risultato è raggiunto con tempi, costi e qualità accettabili?</li></ul>",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/eriksson-penker-process.svg\" alt=\"Schema di processo aziendale: input a sinistra, processo e attività al centro, output a destra, obiettivo sopra e controlli sotto\" data-caption=\"Schema didattico originale ispirato alla prospettiva di processo Eriksson-Penker.\"><figcaption>Schema didattico originale ispirato alla prospettiva di processo Eriksson-Penker: gli input alimentano il processo, le attività li trasformano e gli output vengono consegnati al cliente.</figcaption></figure>",
   "Un esempio concreto è il processo APQC <strong>Manage customer service problems, requests, and inquiries</strong>. Il diagramma seguente mostra come un processo reale possa essere scomposto in attività successive, ruoli, decisioni e risultati: la richiesta viene ricevuta, analizzata e risolta oppure indirizzata verso un'opportunità commerciale. In questo modo il modello rende visibile il passaggio dal processo generale alle attività che lo compongono.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/apqc-customer-service-process.png\" alt=\"Diagramma BPMN del processo APQC Manage customer service problems, requests, and inquiries\" data-caption=\"Esempio di processo APQC modellato in BPMN: Manage customer service problems, requests, and inquiries.\"><figcaption>Esempio di processo APQC modellato in BPMN: <em>Manage customer service problems, requests, and inquiries</em> (6.2.2). Diagramma prodotto con Camunda Modeler per il corso.</figcaption></figure>",
   "Per analizzare un processo è necessario considerarlo come un <strong>percorso completo</strong>. Si individua l'evento o la condizione che lo avvia, si descrivono le attività e le decisioni che trasformano gli input, e si definiscono uno o più risultati di conclusione. I <strong>confini</strong> stabiliscono che cosa appartiene al processo e che cosa invece resta all'esterno.",
   "La prospettiva <strong>end-to-end</strong> segue il risultato dall'innesco fino alla consegna al destinatario, anche quando il lavoro attraversa reparti, funzioni, sedi e applicazioni differenti. Per esempio, la gestione di un ordine cliente può coinvolgere vendite, amministrazione, magazzino, logistica e sistemi informativi. Osservare il processo completo permette di riconoscere attese, passaggi ridondanti, informazioni mancanti, responsabilità poco chiare e punti in cui il risultato può degradarsi.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/saem-fasi-inserimento-ordine.png\" alt=\"Fasi dell'inserimento dell'ordine in SAEM: arrivo dell'ordine, smistamento, verifica e inserimento a sistema, invio della conferma\" data-caption=\"Fasi dell'inserimento dell'ordine in SAEM. Fonte: C. Bozzoli, Reengineering del sistema di gestione ordini in ottica e-commerce: il caso SAEM S.p.A., figura 5.8, p. 76.\"><figcaption>Fasi dell'inserimento dell'ordine in SAEM. Fonte: C. Bozzoli, <em>Reengineering del sistema di gestione ordini in ottica e-commerce: il caso SAEM S.p.A.</em>, figura 5.8, p. 76.</figcaption></figure>",
   "I processi non sono importanti soltanto perché descrivono il lavoro quotidiano. Se vengono progettati, documentati e migliorati con continuità, diventano una leva per la competitività e per la capacità dell'organizzazione di crescere senza perdere controllo:",
   "<ul class=\"study-bullets\"><li><strong>Vantaggio competitivo</strong>: processi chiari e fluidi aumentano l'efficienza, riducono i tempi di risposta e possono migliorare qualità del prodotto, servizio al cliente ed eccellenza operativa.</li><li><strong>Efficienza dei costi</strong>: la revisione periodica mette in evidenza ridondanze, attese e attività che consumano risorse senza creare valore. Le risorse liberate possono essere riallocate dove producono un beneficio maggiore.</li><li><strong>Scalabilità</strong>: un processo ben progettato può gestire l'aumento dei volumi o della complessità senza dipendere soltanto dalla memoria o dall'esperienza di singole persone. Le attività manuali non strutturate tendono invece a diventare un limite quando l'organizzazione cresce.</li><li><strong>Conformità e gestione del rischio</strong>: regole, controlli e responsabilità esplicite aiutano a rispettare obblighi normativi, policy interne e standard di qualità, riducendo errori, violazioni e rischi operativi.</li><li><strong>Soddisfazione del cliente</strong>: un processo orientato al cliente rende più semplice acquistare, ricevere assistenza, ottenere una risposta o risolvere un problema. La qualità percepita dipende anche dalla continuità e dalla prevedibilità del percorso.</li><li><strong>Coinvolgimento e produttività delle persone</strong>: ruoli e responsabilità chiari riducono confusione, sovrapposizioni e rilavorazioni. Le persone possono concentrarsi sulle attività che richiedono competenza e giudizio, invece di ricostruire ogni volta come procedere.</li><li><strong>Innovazione e adattamento</strong>: un processo conosciuto e misurato è più facile da modificare quando cambiano tecnologie, mercato, prodotti o aspettative dei clienti. La standardizzazione non significa immobilità: crea una base dalla quale sperimentare miglioramenti.</li><li><strong>Gestione delle informazioni</strong>: un processo definisce quali dati servono, chi li produce, dove vengono registrati e come vengono utilizzati. Informazioni coerenti, tempestive e protette rendono più affidabili le decisioni e i controlli.</li></ul>",
   "Questi benefici dipendono dal <strong>miglioramento continuo</strong>. Un processo non dovrebbe essere documentato una volta e poi dimenticato: deve essere osservato, misurato e aggiornato quando cambiano obiettivi, strumenti, vincoli o condizioni del contesto. La documentazione, i controlli e il feedback trasformano l'esperienza operativa in conoscenza riutilizzabile e rendono possibile intervenire prima che un problema diventi strutturale.",
  ],"<strong>Il processo e la qualità secondo ISO 9001.</strong> Nel vocabolario ISO, la qualità riguarda il grado con cui le caratteristiche di un prodotto, servizio o processo soddisfano i requisiti. La norma collega questo concetto all'<strong>approccio per processi</strong>: l'organizzazione individua i processi, i loro input e output, le interazioni, i rischi, i controlli e i criteri di misurazione. Le <strong>informazioni documentate</strong> sostengono il funzionamento dei processi e forniscono evidenza che quanto pianificato è stato effettivamente svolto. La documentazione può assumere forme diverse, in funzione delle dimensioni dell'organizzazione, della complessità dei processi, dei rischi e delle competenze disponibili. In questo modo, il sistema di gestione consente di ottenere risultati conformi in modo controllato, verificabile e migliorabile nel tempo. Riferimenti: <a href=\"https://www.iso.org/standard/62085.html?iframeView=true\" target=\"_blank\" rel=\"noopener noreferrer\">ISO 9001 — Quality management systems</a>, <a href=\"https://www.iso.org/iso/iso9001_2015_process_approach.pdf\" target=\"_blank\" rel=\"noopener noreferrer\">ISO — The process approach in ISO 9001</a> e <a href=\"https://www.iso.org/files/live/sites/isoorg/files/standards/docs/en/iso_9001_2015_guidance_documented_information.pdf\" target=\"_blank\" rel=\"noopener noreferrer\">ISO — Guidance on documented information</a>.",
  ),
  (2,"1.1 Obiettivi, confini, input e output",[
   "La descrizione di un processo comincia dall'<strong>obiettivo</strong>: quale risultato deve produrre il processo e per quale esigenza organizzativa o del cliente? Un obiettivo ben formulato non coincide con l'elenco delle attività. Esprime il cambiamento atteso, per esempio consegnare un ordine completo entro una certa data, autorizzare una richiesta conforme ai criteri stabiliti o risolvere un problema del cliente.",
   "L'obiettivo permette di valutare la coerenza del processo. Ogni attività dovrebbe contribuire al risultato oppure fornire un controllo necessario. Se un passaggio non ha una funzione riconoscibile, può essere una duplicazione, un'attesa o una consuetudine non più utile. L'obiettivo diventa quindi il riferimento per progettare il flusso, assegnare le responsabilità e scegliere le misure di prestazione.",
   "I <strong>confini</strong> stabiliscono dove il processo comincia e dove termina. L'inizio può essere identificato da una richiesta del cliente, da un ordine ricevuto, da una scadenza, da un evento tecnico o dalla disponibilità di un input. La fine coincide con la consegna dell'output previsto, con la comunicazione dell'esito o con la registrazione della decisione. Definire i confini evita di estendere l'analisi senza limite e rende chiaro quali attività, ruoli e sistemi appartengono al processo.",
   "Per delimitare correttamente un processo è utile indicare anche ciò che resta fuori. La progettazione del prodotto, per esempio, può essere un processo distinto dalla gestione dell'ordine; la manutenzione del sistema informativo può essere un servizio di supporto e non una fase interna alla vendita. La scelta dipende dall'obiettivo dell'analisi e dal livello di dettaglio richiesto, ma deve essere esplicita e coerente.",
   "Gli <strong>input</strong> sono ciò che il processo riceve, consuma o utilizza per poter operare. Possono essere materiali, dati, documenti, informazioni, richieste, autorizzazioni, risorse economiche o capacità produttiva. Per ogni input è utile chiedersi da chi proviene, in quale formato arriva, se è completo e quali requisiti deve rispettare prima di essere utilizzato.",
   "Gli <strong>output</strong> sono i risultati ottenuti al termine del processo o di una sua parte. Possono essere prodotti fisici, servizi erogati, decisioni, autorizzazioni, rapporti, comunicazioni, registrazioni o dati aggiornati. Un output deve essere descritto dal punto di vista del destinatario: deve essere chiaro che cosa viene consegnato, a chi, con quale livello di completezza, accuratezza, tempestività e conformità.",
   "La relazione tra input e output può essere rappresentata come una trasformazione controllata:",
   "<ul class=\"study-bullets\"><li><strong>Input</strong>: ciò che alimenta il processo.</li><li><strong>Attività e decisioni</strong>: il lavoro che trasforma, verifica o instrada gli input.</li><li><strong>Controlli</strong>: verifiche che prevengono errori o individuano risultati non conformi.</li><li><strong>Output</strong>: il risultato prodotto e consegnato al destinatario.</li><li><strong>Feedback</strong>: informazioni usate per correggere il processo e migliorarne le prestazioni.</li></ul>",
   "Non è sufficiente elencare input e output: occorre definire i <strong>requisiti</strong> che li rendono utilizzabili. Un input incompleto può impedire l'avvio del lavoro; un output consegnato in ritardo o con dati errati può generare rilavorazioni, reclami o rischi. Per questo l'analisi deve considerare anche gli output indesiderati e le condizioni che possono compromettere la conformità del prodotto, del servizio o della decisione.",
   "Infine, il processo deve essere osservabile e misurabile. A seconda del caso, si possono controllare tempi di attraversamento e di attesa, puntualità delle consegne, tasso di errore, scarti e rilavorazioni, costi, frequenza degli incidenti, soddisfazione dei destinatari e prestazioni dei fornitori. Le misure non servono soltanto a giudicare il risultato finale: aiutano a capire in quale punto del processo si genera la variabilità e dove conviene intervenire.",
  ],None),
  (2,"1.2 Clienti interni ed esterni",[
   "Il <strong>cliente del processo</strong> è il soggetto che riceve, utilizza o valuta l'output. Il cliente non coincide necessariamente con chi acquista il prodotto o con chi compare nel contratto commerciale: può essere una persona, un ufficio, un altro processo, un'organizzazione partner o il destinatario finale del servizio.",
   "Il <strong>cliente esterno</strong> si trova fuori dall'organizzazione che esegue il processo. Può essere un acquirente, un cittadino, un paziente, un'azienda cliente, un ente o un altro soggetto destinatario del prodotto o del servizio. Le sue aspettative riguardano normalmente il risultato finale, ma possono riguardare anche il modo in cui il processo viene svolto: tempi di risposta, facilità di accesso, comunicazioni, trasparenza e gestione delle anomalie.",
   "Il <strong>cliente interno</strong> è una persona, una funzione o un processo appartenente alla stessa organizzazione e destinatario di un output intermedio. Per esempio, l'amministrazione può essere cliente interno delle vendite quando riceve un ordine completo; il magazzino può essere cliente interno dell'amministrazione quando riceve l'autorizzazione a preparare la spedizione; la logistica può essere cliente interno del magazzino quando riceve merce e documenti pronti per la consegna.",
   "La distinzione è importante perché molti processi attraversano più funzioni. L'output prodotto da una funzione diventa spesso l'input della funzione successiva: ogni passaggio può quindi essere letto come una relazione tra un <strong>fornitore</strong> e un <strong>cliente</strong>. Se il passaggio interno è incompleto, errato o tardivo, il problema si propaga nel flusso e può arrivare fino al cliente esterno.",
   "Il cliente interno non è un destinatario di seconda importanza. La qualità del risultato finale dipende dalla qualità degli output intermedi. Un processo che consegna informazioni incomplete al processo successivo può sembrare efficiente nel proprio segmento, ma trasferisce lavoro, attese e rischi a valle. L'analisi deve quindi rendere visibili anche le esigenze dei clienti interni e gli accordi di servizio tra funzioni.",
   "Per identificare il cliente di un processo è utile rispondere a queste domande:",
   "<ul class=\"study-bullets\"><li><strong>Chi riceve l'output?</strong> Individuare il destinatario diretto e, se necessario, anche chi utilizza il risultato in una fase successiva.</li><li><strong>Che cosa si aspetta?</strong> Descrivere il risultato richiesto, non soltanto l'attività svolta dall'organizzazione.</li><li><strong>Quali requisiti deve rispettare l'output?</strong> Considerare completezza, accuratezza, formato, tempi, quantità, sicurezza e conformità.</li><li><strong>Come viene verificato il risultato?</strong> Individuare criteri di accettazione, controlli, reclami, richieste di correzione o indicatori di soddisfazione.</li><li><strong>Che cosa accade se l'output non è conforme?</strong> Tracciare rilavorazioni, rifiuti, escalation, ritardi e impatti sui processi successivi.</li></ul>",
   "Un processo può avere più clienti e ciascuno può attribuire valore a caratteristiche diverse dello stesso output. Un ordine, per esempio, deve essere utile al cliente esterno che riceverà la merce, ma anche all'amministrazione che deve fatturare, al magazzino che deve preparare i colli e al vettore che deve organizzare la consegna. La scheda processo dovrebbe esplicitare questi destinatari quando hanno requisiti differenti o quando la loro mancata soddisfazione crea un rischio.",
   "La prospettiva del cliente orienta la definizione delle <strong>misure di qualità</strong>. Non basta sapere quante attività sono state eseguite: occorre verificare se l'output è arrivato al destinatario giusto, nel momento concordato, nel formato utilizzabile e senza errori. Tempi di risposta, puntualità, completezza, accuratezza, numero di reclami e tasso di rilavorazione sono esempi di misure che collegano il funzionamento interno al valore percepito dal cliente.",
  ],None),
  (1,"2 Funzione, processo, attività e task",[
   "<strong>Funzione, processo, attività e task</strong> descrivono aspetti diversi del lavoro organizzativo e non sono sinonimi. La funzione identifica una responsabilità o una capacità organizzativa relativamente stabile, spesso associata a un'unità, a un reparto o a una competenza. Il processo, invece, descrive il modo in cui il lavoro attraversa l'organizzazione per ottenere un risultato utile. Le attività e i task rappresentano livelli progressivamente più concreti di questo lavoro.",
   "Un <strong>processo aziendale</strong> è una sequenza strutturata e ripetibile di attività progettata per raggiungere un obiettivo specifico. Non coincide semplicemente con l'elenco delle operazioni svolte da un reparto: comprende l'insieme delle attività, delle decisioni, delle responsabilità e delle regole necessarie per trasformare determinati input in output destinati a uno o più clienti o destinatari. Per questa ragione un processo può iniziare in una funzione, proseguire in altre funzioni e concludersi presso un cliente interno o esterno.",
   "Ogni processo dovrebbe rendere espliciti il proprio <strong>obiettivo</strong>, gli <strong>input</strong> necessari, gli <strong>output</strong> prodotti, i ruoli coinvolti, le regole applicabili e i criteri con cui si valuta il risultato. L'obiettivo chiarisce perché il processo esiste e quale valore deve generare. Gli input possono essere dati, richieste, documenti, materiali, autorizzazioni o eventi; gli output possono essere prodotti, servizi, decisioni, comunicazioni o informazioni utilizzate dal passaggio successivo.",
   "Le <strong>attività</strong> sono unità di lavoro riconoscibili all'interno del processo. Un'attività può consistere in un'operazione semplice, come inviare una comunicazione, oppure comprendere più passaggi collegati, controlli e decisioni. La sequenza delle attività costituisce il <strong>flusso di lavoro</strong>: mostra l'ordine normale delle operazioni, ma anche le alternative, le diramazioni, le esecuzioni parallele, i ritorni e le condizioni che determinano il percorso effettivo di ogni istanza del processo.",
   "Il <strong>task</strong> è l'azione elementare che, al livello di dettaglio scelto, può essere assegnata a un ruolo ed eseguita o verificata come unità operativa. Il confine tra attività e task dipende dalla finalità del modello: se occorre comprendere il processo nel suo insieme, un gruppo di azioni può essere rappresentato come una singola attività; se occorre organizzare l'esecuzione o automatizzare il lavoro, la stessa attività può essere scomposta in task più dettagliati. Il livello di dettaglio deve quindi essere sufficiente per comprendere, assegnare e controllare il lavoro, senza rendere il modello inutilmente complesso.",
   "Un processo è comprensibile anche attraverso le sue <strong>responsabilità</strong>. Ogni attività o task dovrebbe avere un esecutore, un responsabile o un ruolo chiaramente identificabile. La distinzione dei ruoli riduce sovrapposizioni e omissioni, facilita il passaggio di consegne e rende possibile verificare chi deve agire, chi deve approvare e chi deve essere informato. Il processo può inoltre utilizzare risorse, sistemi informativi e strumenti diversi, che devono essere coerenti con le attività da svolgere.",
   "Le <strong>regole e gli standard</strong> definiscono i vincoli entro cui il processo deve operare: criteri di accettazione, autorizzazioni, obblighi normativi, livelli di servizio e condizioni per proseguire o deviare dal flusso. La <strong>documentazione</strong> rende il processo ripetibile e verificabile, mentre i controlli e i meccanismi di feedback permettono di rilevare errori, eccezioni e scostamenti. Un processo ben descritto non mostra quindi soltanto che cosa viene fatto, ma anche in quali condizioni, con quali strumenti e secondo quali criteri.",
   "Infine, <strong>metriche e indicatori</strong> collegano l'esecuzione del processo al risultato atteso. Tempi di attraversamento, costi, qualità dell'output, puntualità, errori, rilavorazioni e soddisfazione del cliente sono esempi di aspetti misurabili. La loro osservazione consente di capire se il processo raggiunge il proprio obiettivo e di individuare opportunità di miglioramento.",
   "In sintesi, la funzione descrive una responsabilità organizzativa, il processo coordina il lavoro verso un risultato, l'attività rappresenta un'unità significativa di lavoro e il task rende operativa un'azione concreta. Questa distinzione consente di passare dalla struttura organizzativa al flusso end-to-end e, quando serve, dal flusso generale al dettaglio necessario per l'esecuzione e il controllo.",
   "Per leggere correttamente un processo è utile osservare insieme questi elementi:",
   "<ul class=\"study-bullets\"><li><strong>Obiettivo</strong>: il risultato che il processo deve raggiungere.</li><li><strong>Input e output</strong>: ciò che il processo riceve, trasforma e consegna.</li><li><strong>Attività e task</strong>: il lavoro da svolgere e il livello di dettaglio con cui lo si rappresenta.</li><li><strong>Flusso</strong>: l'ordine, le condizioni, le alternative e le eventuali attività parallele.</li><li><strong>Ruoli e risorse</strong>: chi esegue, approva, controlla o supporta il lavoro.</li><li><strong>Regole, documentazione e controlli</strong>: i vincoli e le evidenze che rendono il processo ripetibile.</li><li><strong>Metriche e feedback</strong>: come si verifica il risultato e come si orienta il miglioramento.</li></ul>",
  ],None),
  (2,"2.1 Distinguere i livelli per estrarre i requisiti",[
   "La distinzione tra funzione, processo, attività e task non serve soltanto a ordinare il vocabolario. Serve a capire <strong>a quale livello porre ogni domanda</strong> durante la raccolta dei requisiti. La funzione chiarisce chi possiede una responsabilità; il processo chiarisce quale risultato deve essere ottenuto; l'attività chiarisce quale parte del lavoro è necessaria; il task chiarisce quale azione concreta deve essere eseguita e verificata.",
   "A livello di <strong>processo</strong> si raccolgono obiettivo, cliente, confini, input, output, vincoli e indicatori. A livello di <strong>attività</strong> si individuano attore, precondizioni, informazioni utilizzate, risultato intermedio e regole applicate. A livello di <strong>task</strong> si precisano l'azione, l'esito osservabile, l'eventuale interazione con un sistema e il dato creato o modificato.",
   "Una funzione può partecipare a più processi e un processo può attraversare più funzioni. Per questo il requisito deve essere collegato sia al risultato end-to-end sia all'attività e al ruolo che lo rendono possibile. La distinzione dei livelli evita di confondere una responsabilità organizzativa con un'attività, oppure una funzione del sistema con l'intero processo aziendale.",
   "Nel caso SAEM, per esempio, «gestire l'ordine cliente» è il processo; «creare la testata del carrello» è un'attività; «leggere i dati del cliente», «verificare l'IVA» o «confermare la testata» sono task o passi operativi. Questa scomposizione permette di collegare ogni requisito alle informazioni lette o scritte e al ruolo che esegue l'azione.",
   "La distinzione dei livelli è quindi il punto di partenza; la raccolta completa richiede poi di documentare fonti, flussi alternativi, eccezioni, entità informative, operazioni CRUD e criteri di verifica.",
  ],None),
  (1,"3 Classificazione cross-industry",[
   "Una classificazione <strong>cross-industry</strong> organizza i processi aziendali in una struttura comune, utilizzabile da organizzazioni diverse per settore, dimensione e localizzazione. L'obiettivo non è sostenere che tutte le aziende lavorino nello stesso modo, ma offrire un punto di confronto per riconoscere processi con finalità simili anche quando sono eseguiti con ruoli, strumenti e procedure differenti.",
   "Una tassonomia di processo funziona come una <strong>mappa condivisa</strong>. Permette di passare dai nomi locali e dalle descrizioni operative a categorie, gruppi e processi riconoscibili. La mappa aiuta a vedere l'organizzazione nel suo insieme, a individuare aree coperte o scoperte e a collegare le attività quotidiane a risultati più ampi.",
   "Un modello comune è particolarmente utile quando si devono confrontare prestazioni, progettare miglioramenti, definire responsabilità, valutare sistemi informativi o discutere processi tra persone che provengono da funzioni diverse. Senza un vocabolario condiviso, la stessa parola può indicare attività diverse e attività equivalenti possono essere descritte con parole diverse.",
   "Nessuna tassonomia sostituisce l'analisi dell'organizzazione. Un framework fornisce una struttura di riferimento; l'azienda deve poi adattarla ai propri prodotti, clienti, vincoli, ruoli, sistemi e livelli di dettaglio. La classificazione è quindi un modello di orientamento e confronto, non una fotografia completa delle procedure locali.",
   "La necessità di scegliere un modello dipende dal <strong>perimetro dell'analisi</strong>. Un'organizzazione che vuole rappresentare l'intero patrimonio dei processi ha bisogno di uno schema ampio e trasversale. Un'organizzazione che studia soprattutto la movimentazione fisica dei prodotti può preferire un framework specializzato nella supply chain, come <strong>SCOR</strong>. I due approcci possono essere confrontati, ma non hanno lo stesso campo di applicazione.",
   "<div class=\"note-box\"><strong>Framework generale: APQC Process Classification Framework.</strong> È una tassonomia cross-industry e cross-funzionale pensata per descrivere i processi dell'intera organizzazione e renderne possibile il confronto. La struttura procede dal livello più ampio delle <strong>Category</strong> ai <strong>Process Group</strong>, ai <strong>Process</strong> e alle <strong>Activity</strong>. I livelli superiori aiutano a leggere il portafoglio complessivo; i livelli inferiori descrivono progressivamente il lavoro. I task e le procedure operative restano invece dipendenti dall'organizzazione e dal contesto in cui il processo viene eseguito.</div>",
   "<div class=\"note-box\"><strong>Framework specializzato: SCOR.</strong> È orientato alla supply chain e segue i processi con cui un'organizzazione pianifica, gestisce gli ordini, approvvigiona, trasforma, consegna e gestisce i resi. La struttura comprende macro-processi, categorie ed elementi di processo, insieme a prospettive su <strong>performance</strong>, <strong>practices</strong> e <strong>people</strong>. È quindi particolarmente adatto a imprese manifatturiere e distributive; non ha lo stesso perimetro generale di un modello che copre anche vendite, risorse umane, IT e finanza.</div>",
   "Le suite gestionali rendono concreto il rapporto tra <strong>standardizzazione</strong> e <strong>automazione</strong>. Non si limitano a registrare dati: propongono ruoli, stati, controlli, transazioni e passaggi collegati. La standardizzazione definisce il percorso; la configurazione della piattaforma stabilisce come quel percorso viene eseguito e quali aggiornamenti possono avvenire automaticamente.",
   "Un esempio è il processo <strong>Order to Cash</strong> documentato per Oracle NetSuite: l'ordine cliente alimenta l'evasione e la fatturazione; il sistema aggiorna lo stato dell'ordine, invia la fattura e genera la registrazione contabile. <a href=\"https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4750146419.html\" target=\"_blank\" rel=\"noopener noreferrer\">La pagina ufficiale Oracle descrive questi controlli e automatismi</a>.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/netsuite-order-to-cash.svg\" alt=\"Schema didattico del processo Oracle NetSuite Order to Cash: ordine cliente, evasione, fatturazione, aggiornamento dello stato e registrazione contabile\" data-caption=\"Schema didattico ricostruito dalla documentazione ufficiale Oracle NetSuite sul processo Order to Cash.\"><figcaption>Schema didattico ricostruito dalla <a href=\"https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4750146419.html\" target=\"_blank\" rel=\"noopener noreferrer\">documentazione ufficiale Oracle NetSuite</a>: Order to Cash.</figcaption></figure>",
   "Un esempio analogo è il processo <strong>Procure to Pay</strong> documentato da SAP: la richiesta di acquisto porta all'assegnazione della fonte, all'ordine al fornitore, alla ricezione, alla verifica della fattura e al pagamento. Le regole configurabili possono selezionare richieste, fonti di approvvigionamento e ordini, anche con esecuzione pianificata. <a href=\"https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/af9ef57f504840d2b81be8667206d485/852a52a67c2c442ead085aa07b9fe8d4.html\" target=\"_blank\" rel=\"noopener noreferrer\">La documentazione SAP sulle regole di automazione descrive questo scenario</a>.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/sap-procure-to-pay.svg\" alt=\"Schema didattico del processo SAP Procure to Pay: richiesta di acquisto, fonte, ordine al fornitore, ricezione, verifica della fattura e pagamento\" data-caption=\"Schema didattico ricostruito dalla documentazione ufficiale SAP sul processo Procure to Pay.\"><figcaption>Schema didattico ricostruito dalla <a href=\"https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/af9ef57f504840d2b81be8667206d485/852a52a67c2c442ead085aa07b9fe8d4.html\" target=\"_blank\" rel=\"noopener noreferrer\">documentazione ufficiale SAP</a>: Procure to Pay.</figcaption></figure>",
  ],None),
  (2,"3.1 Tassonomie e vocabolario comune",[
   "Una <strong>tassonomia</strong> è una classificazione organizzata secondo categorie e relazioni gerarchiche. Nel caso dei processi, la gerarchia consente di leggere lo stesso oggetto a livelli diversi: una vista generale mostra grandi aree dell'organizzazione; livelli successivi raggruppano processi omogenei; livelli più dettagliati descrivono attività e, quando necessario, passi operativi specifici.",
   "La gerarchia non serve soltanto a ordinare un elenco. Stabilisce il rapporto tra un elemento e il contesto più ampio a cui appartiene. Un processo può quindi essere identificato sia per il proprio nome e risultato sia per la posizione che occupa nella struttura complessiva. Questa posizione facilita la navigazione, il confronto e la tracciabilità delle analisi.",
   "Il <strong>vocabolario comune</strong> riduce le ambiguità tra funzioni, sedi e organizzazioni. Per ottenere questo risultato, i nomi devono descrivere il risultato o la finalità del processo, non soltanto il reparto che lo esegue. Il reparto può cambiare, mentre il processo può rimanere necessario e attraversare più unità organizzative.",
   "Un buon nome di processo tende a contenere un verbo e un oggetto: per esempio <em>gestire gli ordini cliente</em>, <em>selezionare i fornitori</em> o <em>emettere la fattura al cliente</em>. La denominazione deve essere accompagnata da una definizione e da un confine, perché il solo nome non è sufficiente a stabilire quali attività siano incluse.",
   "Per confrontare due processi occorre verificare almeno quattro elementi:",
   "<ul class=\"study-bullets\"><li><strong>finalità</strong>: quale bisogno o risultato condividono;</li><li><strong>confini</strong>: da quale evento partono e dove terminano;</li><li><strong>livello</strong>: se il confronto riguarda categorie, processi, attività o task;</li><li><strong>definizione</strong>: quali attività e risultati sono effettivamente compresi.</li></ul>",
  ],None),
  (2,"3.2 Perché classificare i processi",[
   "Classificare i processi serve innanzitutto a costruire una <strong>vista completa e leggibile dell'organizzazione</strong>. La tassonomia aiuta a individuare quali processi esistono, come sono raggruppati, quali risultati producono e quali collegamenti hanno con altre aree dell'azienda.",
   "La classificazione sostiene il <strong>confronto delle prestazioni</strong>. Se due organizzazioni usano definizioni compatibili, possono confrontare tempi, costi, qualità, volumi o livelli di servizio riferiti a processi con uno scopo simile. Il confronto non elimina le differenze di contesto: le rende esplicite e permette di capire quali risultati dipendano dall'organizzazione, dal mercato o dai vincoli specifici.",
   "Una struttura comune facilita il <strong>miglioramento continuo</strong>. Permette di assegnare un responsabile, collegare indicatori al processo, individuare sovrapposizioni e lacune, confrontare lo stato attuale con quello desiderato e selezionare le aree in cui intervenire per prime.",
   "La classificazione è utile anche nei progetti di <strong>digitalizzazione e automazione</strong>. Prima di scegliere un'applicazione o automatizzare un'attività, occorre sapere a quale processo appartiene, quale risultato deve sostenere, quali ruoli coinvolge e quali informazioni attraversano il flusso. Una tassonomia evita che l'analisi si riduca a un insieme di funzioni applicative scollegate.",
   "Infine, la classificazione rende più stabile la comunicazione tra direzione, responsabili di processo, analisti, tecnici e auditor. Un riferimento comune facilita la definizione di responsabilità e indicatori, la gestione del portafoglio dei processi, la documentazione dei rischi e il riuso delle conoscenze tra progetti diversi.",
   "I benefici principali possono essere riassunti così:",
   "<ul class=\"study-bullets\"><li><strong>visibilità</strong>: rende leggibile l'insieme dei processi aziendali;</li><li><strong>confrontabilità</strong>: permette di confrontare processi omogenei tra funzioni o organizzazioni;</li><li><strong>governance</strong>: aiuta ad assegnare responsabilità, obiettivi e indicatori;</li><li><strong>miglioramento</strong>: sostiene benchmarking, analisi delle lacune e priorità di intervento;</li><li><strong>digitalizzazione</strong>: collega processi, dati e sistemi prima di automatizzare;</li><li><strong>riuso</strong>: crea un linguaggio e una struttura riutilizzabili in analisi successive.</li></ul>",
   "La classificazione deve però essere riesaminata quando cambiano strategia, prodotti, tecnologie, organizzazione o vincoli esterni. Un modello utile non è immutabile: resta abbastanza stabile da consentire il confronto, ma può evolvere quando cambiano le modalità con cui l'organizzazione crea valore.",
  ],None),
  (1,"4 Dal processo ai requisiti",[
   "La descrizione di un processo non si esaurisce nella rappresentazione del flusso. Per poterlo migliorare, digitalizzare o supportare con un sistema informativo è necessario esplicitare <strong>che cosa deve accadere</strong>, <strong>per chi</strong>, <strong>in quali condizioni</strong> e <strong>con quali risultati verificabili</strong>. Queste informazioni costituiscono la base per la raccolta dei requisiti.",
   "Un requisito nasce da un'esigenza osservata o dichiarata e descrive una condizione che il processo o il sistema deve rispettare. Può riguardare il risultato del processo, una regola di business, un'informazione da conservare, un controllo, un'autorizzazione, un tempo di risposta oppure un comportamento che il sistema deve rendere possibile.",
   "La raccolta parte dal <strong>modello di business</strong>: obiettivi, clienti, attività, ruoli, input, output, vincoli ed eccezioni. Solo dopo si selezionano le parti che devono essere supportate da applicazioni o archivi. In questo modo il sistema informativo resta al servizio del processo e non diventa il punto di partenza dell'analisi.",
   "È utile distinguere due livelli collegati: i <strong>requisiti del processo</strong>, che descrivono il lavoro e il risultato atteso, e i <strong>requisiti informativi o IT</strong>, che descrivono le funzioni del sistema e i dati necessari. Il secondo livello deriva dal primo attraverso un passaggio di selezione e di dettaglio progressivo.",
   "Per avviare la raccolta dei requisiti occorre chiedersi:",
   "<ul class=\"study-bullets\"><li><strong>Quale esigenza</strong> ha dato origine al processo o alla modifica?</li><li><strong>Quale risultato</strong> deve essere ottenuto e da chi sarà utilizzato?</li><li><strong>Quali regole e vincoli</strong> devono essere rispettati?</li><li><strong>Quali informazioni</strong> servono per eseguire, controllare e concludere il lavoro?</li><li><strong>Quali errori, alternative ed eccezioni</strong> devono essere gestiti?</li><li><strong>Come si verificherà</strong> che il requisito sia stato soddisfatto?</li></ul>",
  ],None),
  (2,"4.1 Esigenze, vincoli e fonti dei requisiti",[
   "I requisiti possono essere esplicitamente dichiarati dal cliente o dagli utenti, ma possono anche derivare da esigenze note, requisiti cogenti, policy aziendali, accordi di servizio, rischi, errori ricorrenti e caratteristiche tecniche del prodotto o del servizio.",
   "Una raccolta completa considera sia ciò che il cliente chiede sia ciò che è necessario per l'uso previsto. Nel caso di un ordine, per esempio, non basta registrare il prodotto richiesto: possono essere necessari dati sul cliente, condizioni di consegna, disponibilità, IVA, autorizzazioni, limiti di prezzo e modalità di evasione.",
   "Ogni requisito dovrebbe avere una <strong>fonte</strong>: una richiesta, un documento, una regola, un'intervista, un'osservazione del lavoro, un indicatore di prestazione o un elemento del sistema esistente. La fonte permette di riesaminare la decisione e di distinguere ciò che è documentato da ciò che è stato inferito durante l'analisi.",
  ],None),
  (2,"4.2 Confini e livelli di dettaglio",[
   "La raccolta deve mantenere il collegamento tra il requisito e il livello a cui si riferisce. Un obiettivo riguarda il processo nel suo insieme; una regola può riguardare una specifica attività; un requisito informativo può riguardare un singolo dato o una singola interazione con il sistema.",
   "Un requisito troppo generale non è verificabile; uno troppo dettagliato può anticipare inutilmente una soluzione tecnica. Il livello corretto è quello che consente di comprendere il comportamento atteso, assegnare una responsabilità, verificare l'esito e mantenere aperte le scelte progettuali ancora non decise.",
  ],None),
  (1,"5 Dalle attività alle entità informative",[
   "Dopo aver individuato le attività da analizzare, si osservano le informazioni che esse utilizzano e producono. Un'attività può leggere dati già disponibili, crearne di nuovi, aggiornarli, eliminarli o usarli per generare un documento, una comunicazione o una decisione.",
   "Le <strong>entità informative</strong> rappresentano strutture dati o unità informative significative per il processo. Possono essere un cliente, un ordine, una riga d'ordine, un articolo, un'autorizzazione, un messaggio o un documento. In una prima analisi sono entità candidate: solo il successivo approfondimento stabilisce se saranno confermate, modificate, accorpate o eliminate.",
   "Il collegamento tra attività ed entità rende visibile il rapporto tra lavoro e informazioni. Per ogni attività è possibile chiedere: quali dati deve leggere? quali dati produce? quali dati modifica? quali informazioni devono restare disponibili per il passaggio successivo o per un controllo successivo?",
   "Questa analisi aiuta a evitare due errori opposti: descrivere attività senza sapere quali informazioni le rendono possibili oppure partire dalle tabelle esistenti senza comprendere quale bisogno del processo soddisfino.",
  ],None),
  (2,"5.1 Letture, scritture e responsabilità",[
   "Le relazioni tra attività ed entità possono essere annotate come operazioni di lettura e scrittura. La lettura indica che l'attività usa informazioni già presenti; la scrittura indica che l'attività crea o modifica un'informazione che diventa disponibile per altri soggetti o attività.",
   "L'annotazione deve essere accompagnata dal <strong>ruolo</strong> che esegue l'operazione e dallo scopo della lettura o della scrittura. Leggere i dati del cliente per autenticare l'utente è un requisito diverso dal leggerli per calcolare il prezzo o compilare la testata di un ordine.",
  ],None),
  (2,"5.2 La matrice attività–informazioni",[
   "Una matrice attività–informazioni mette in riga le attività e in colonna le entità o gli archivi. Nelle celle si annotano le operazioni compiute. La matrice fornisce una vista sintetica e consente di verificare che ogni informazione prodotta abbia un destinatario e che ogni informazione letta sia giustificata da un'attività.",
   "Quando l'archivio è persistente, la matrice può essere dettagliata con la notazione <strong>CRUD</strong>: Create, Read, Update e Delete. La matrice non sostituisce la descrizione testuale, ma la integra e aiuta a validare la coerenza tra modello del processo e modello dei dati.",
  ],None),
  (1,"6 Dalle entità ai requisiti funzionali",[
   "Le relazioni tra attività ed entità permettono di derivare i <strong>casi d'uso</strong>. Un caso d'uso descrive una funzionalità visibile dall'esterno, attivata da un attore e realizzata attraverso interazioni con il sistema e con le informazioni che il sistema gestisce.",
   "Il caso d'uso traduce il processo in una domanda operativa: che cosa deve poter fare l'attore e quale risultato deve ottenere? La descrizione non deve limitarsi al nome della funzione, ma deve rendere espliciti il flusso normale, le condizioni iniziali, il risultato finale e i percorsi alternativi.",
   "La specifica testuale dei requisiti può essere organizzata in asserzioni numerate. La numerazione deve seguire una struttura stabile e mantenere la distinzione tra categorie di requisito. Questo rende possibile riferirsi a un requisito durante progettazione, sviluppo, test e gestione delle modifiche.",
  ],None),
  (2,"6.1 Flusso principale e flussi alternativi",[
   "Il <strong>flusso principale</strong> descrive il percorso atteso quando i dati sono corretti e le condizioni sono soddisfatte. I <strong>flussi alternativi</strong> descrivono variazioni legittime del percorso, mentre le <strong>eccezioni</strong> descrivono errori, indisponibilità o condizioni che impediscono la conclusione normale.",
   "Per ogni alternativa è utile indicare il punto del flusso in cui si attiva, il dato o la condizione che la determina, l'azione da compiere e il risultato prodotto. Questa struttura consente di trasformare le eccezioni in percorsi analizzabili invece di lasciarle come conoscenza implicita degli operatori.",
  ],None),
  (2,"6.2 Precondizioni, postcondizioni e verificabilità",[
   "Le <strong>precondizioni</strong> indicano ciò che deve essere vero prima dell'avvio, per esempio utente autenticato, cliente attivo o dati disponibili. Le <strong>postcondizioni</strong> descrivono lo stato che deve risultare al termine, per esempio ordine registrato, messaggio inviato o autorizzazione aggiornata.",
   "Un requisito è utile quando può essere verificato. Frequenza, criticità, tempi attesi, completezza dei dati e criteri di accettazione aiutano a stabilire la priorità e a progettare controlli e test. La documentazione deve poter rispondere alla domanda: come sapremo che il requisito è stato soddisfatto?",
  ],None),
  (1,"7 Caso SAEM: dalla criticità alla specifica",[
   "Nel caso SAEM la raccolta dei requisiti parte dall'analisi del processo reale di gestione degli ordini. L'analisi evidenzia problemi nelle unità di misura, nella corrispondenza tra codici cliente e codici interni, nei tempi di evasione, nei resi e nelle modifiche telefoniche agli ordini.",
   "Queste criticità vengono trasformate in esigenze del nuovo processo: rendere visibili le specifiche dell'ordine, cercare e selezionare l'articolo corretto, verificare la disponibilità, controllare i parametri economici, gestire l'evasione unica o parziale e ridurre gli errori di imputazione.",
   "La tesi non si limita a elencare le funzionalità. Collega ciascuna attività alle informazioni utilizzate e prodotte. Per l'ordine telematico, per esempio, la creazione del carrello legge cliente, condizioni di consegna e parametri IVA; la conferma legge e verifica testata e righe; l'esito positivo crea l'ordine effettivo e trasferisce le righe.",
   "Le operazioni sono poi formalizzate nelle Assembly Line e nelle tavole CRUD. Da queste relazioni vengono derivati i casi d'uso e le relative specifiche testuali, con attori, flussi, alternative, eccezioni, precondizioni, postcondizioni, frequenza e criticità.",
  ],None),
  (2,"7.1 Esempio: gestione dell'ordine telematico",[
   "L'attore cliente crea la testata del carrello, inserisce gli articoli, verifica disponibilità e condizioni, quindi conferma l'ordine. Il sistema legge le informazioni necessarie, segnala le righe non disponibili, ricalcola i dati economici e, se le verifiche hanno esito positivo, trasforma il carrello in ordine.",
   "Le entità informative coinvolte includono cliente, condizioni di consegna, tabella IVA, carrello, righe del carrello, articoli, storico articoli, scadenze di magazzino, listini, ordine e messaggi. La loro presenza nel modello deve essere collegata all'attività che le legge o le scrive e alla fonte che documenta l'interazione.",
  ],None),
  (2,"7.2 Iterazione e gestione delle varianti",[
   "La documentazione dei requisiti evolve durante lo sviluppo. Una prima descrizione può essere breve; in seguito vengono aggiunti i dettagli delle interazioni, delle entità e degli scenari alternativi. Il confronto tra tavole CRUD e soluzioni diverse permette inoltre di rendere visibili le varianti progettuali.",
   "Nel caso SAEM la modifica dell'ordine presenta alternative tra la soluzione sviluppata dai tecnici e quella proposta nell'analisi. Le differenze vengono evidenziate nella tavola CRUD e non devono essere confuse con requisiti già definitivamente approvati.",
  ],None),
  (1,"8 Laboratorio: costruire una scheda dei requisiti",[
   "Scegliere un processo semplice, come la gestione di una richiesta cliente o di un ordine. Descrivere prima l'obiettivo, i confini, gli attori, gli input e gli output; poi individuare le attività e le condizioni che modificano il flusso.",
   "Per ogni attività compilare una scheda con: requisito, fonte, ruolo, input, output, entità lette, entità create o modificate, regola applicata, flusso alternativo, eccezione e criterio di verifica. Assegnare un identificativo stabile a ogni requisito.",
   "Infine costruire una matrice attività–informazioni e confrontarla con la descrizione testuale. Ogni lettura o scrittura deve essere motivata da un'esigenza del processo; ogni output informativo deve avere un destinatario o un uso documentato.",
  ],None),
 ],
  kt=[
  "Un processo trasforma input in output per un cliente e ha obiettivo, confini, evento di avvio e risultato atteso.",
  "Funzione, processo, attività e task sono livelli distinti: il processo esprime il risultato, il task l'azione elementare.",
  "Una tassonomia cross-industry fornisce un linguaggio comune per confrontare processi con finalità simili in organizzazioni diverse.",
  "La scelta del framework dipende dal perimetro: un modello generale copre l'organizzazione, mentre SCOR è specializzato nella supply chain.",
  "La raccolta dei requisiti parte dall'analisi del business e distingue requisiti di processo da requisiti informativi e IT.",
  "Le Assembly Line collegano attività ed entità informative attraverso relazioni di lettura e scrittura.",
  "La matrice CRUD valida la coerenza tra attività, dati e comportamento del sistema.",
  "I casi d'uso documentano attori, flussi, alternative, eccezioni, precondizioni e postcondizioni.",
  "Nel caso SAEM i requisiti evolvono iterativamente e sono collegati a fonti, dati e varianti progettuali.",
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
   "Costruire la matrice delle variabili per la Activity scomposta nel Modulo 4. Aggiungere una riga con almeno un collo di bottiglia e indicare una relazione causa-effetto tra due variabili.",
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
   "<a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN (Business Process Model and Notation)</a> è lo standard OMG per rappresentare i processi in modo formale, con un insieme di simboli condiviso. La <a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN Reference</a> presenta gli elementi principali della notazione e il loro significato.",
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
   "Come estensione facoltativa, aprire una Developer Edition speciale del percorso Trailhead <a href=\"https://trailhead.salesforce.com/content/learn/modules/flow-troubleshooting/review-flow-terminology-and-sign-up-for-a-special-org\" target=\"_blank\" rel=\"noopener noreferrer\">Flow Troubleshooting</a>. L'organizzazione contiene alcuni Flow già predisposti: analizzarne trigger, attività, decisioni e dati, quindi confrontare l'implementazione con la scheda processo e con il diagramma BPMN. Trailhead parla di Developer Edition o Playground, non di una Sandbox Salesforce tradizionale.",
   "Come esempio di implementazione, osservare il Flow Salesforce <strong>Create New Customer</strong>: il processo business parte dalla raccolta delle informazioni del cliente, mentre il sistema esegue in sequenza la creazione di Account, Contact e Opportunity e restituisce una conferma. La figura rende visibili le interazioni tra attività del processo e operazioni sui dati del sistema.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/salesforce-flow-create-new-customer.png\" alt=\"Salesforce Flow Builder: il flusso Create New Customer raccoglie le informazioni e crea Account, Contact e Opportunity prima di mostrare una conferma\" data-caption=\"Esempio di implementazione Salesforce Flow: Create New Customer.\"><figcaption>Esempio di implementazione Salesforce Flow: il processo business di acquisizione di un nuovo cliente interagisce con il sistema creando Account, Contact e Opportunity.</figcaption></figure>",
  ],None),
 ],
 kt=[
  "La scheda processo integra in una pagina collocazione, attività, variabili, indicatori e rappresentazione.",
  "La coerenza si verifica quando nome e codice, Activity e Task si corrispondono senza salti.",
  "Il diagramma funziona da controllo: attività senza ruolo o senza esito emergono nel disegno.",
  "Il pacchetto di deliverable del corso è riusabile come template aziendale per confrontare i processi.",
 ]),
}

# ---- riorganizzazione didattica dei moduli --------------------------------
# M01 termina alla sezione 3. Le sezioni dedicate alla requisitazione diventano
# il nuovo M02; i moduli già esistenti scalano di una posizione.
requirements_sections = CONTENT["01"]["sections"][8:]
CONTENT["01"]["sections"] = CONTENT["01"]["sections"][:8]
requirement_section_numbers = {
    "4": "1", "4.1": "1.1", "4.2": "1.2",
    "5": "2", "5.1": "2.1", "5.2": "2.2",
    "6": "3", "6.1": "3.1", "6.2": "3.2",
    "7": "4", "7.1": "4.1", "7.2": "4.2",
    "8": "5",
}
requirements_sections = [
    (
        level,
        requirement_section_numbers.get(title.split(" ", 1)[0], title.split(" ", 1)[0])
        + title[len(title.split(" ", 1)[0]):],
        paragraphs,
        note,
    )
    for level, title, paragraphs, note in requirements_sections
]
CONTENT["01"]["kt"] = [
    "Un processo trasforma input in output per un cliente e ha obiettivo, confini, evento di avvio e risultato atteso.",
    "Funzione, processo, attività e task sono livelli distinti: il processo esprime il risultato, il task l'azione elementare.",
    "Una tassonomia cross-industry fornisce un linguaggio comune per confrontare processi con finalità simili in organizzazioni diverse.",
    "La scelta del framework dipende dal perimetro: un modello generale copre l'organizzazione, mentre SCOR è specializzato nella supply chain.",
]
requirements_kt = [
    "La raccolta dei requisiti parte dall'analisi del business e distingue requisiti di processo da requisiti informativi e IT.",
    "Le Assembly Line collegano attività ed entità informative attraverso relazioni di lettura e scrittura.",
    "La matrice CRUD valida la coerenza tra attività, dati e comportamento del sistema.",
    "I casi d'uso documentano attori, flussi, alternative, eccezioni, precondizioni e postcondizioni.",
    "Nel caso SAEM i requisiti evolvono iterativamente e sono collegati a fonti, dati e varianti progettuali.",
]
for old, new in reversed([
    ("02", "03"), ("03", "04"), ("04", "05"),
    ("05", "06"), ("06", "07"), ("07", "08"),
]):
    CONTENT[new] = CONTENT.pop(old)
CONTENT["02"] = dict(sections=requirements_sections, kt=requirements_kt)

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
<button class="print-page" type="button" data-print-page aria-label="Stampa la pagina">Stampa</button>
<a class="back-to-top" href="#top" data-back-to-top aria-hidden="true" tabindex="-1">Torna su</a>
<div class="lightbox" id="lightbox" aria-hidden="true">
 <figure class="lightbox-inner">
  <img id="lightbox-image" alt="">
  <figcaption id="lightbox-caption"></figcaption>
 </figure>
</div>
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
    figure_number = 0
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
            if p.lstrip().startswith("<figure"):
                figure_number += 1
                figure_label = f"Figura M{code}.{figure_number:02d} — "
                p = p.replace('data-caption="', f'data-caption="{figure_label}', 1)
                p = p.replace("<figcaption>", f"<figcaption>{figure_label}", 1)
            is_raw = any(marker in p for marker in ('<code>', '<a ', '<strong>', '<em>', '<ul', '<ol', '<div', '<figure'))
            if p.lstrip().startswith(('<ul', '<ol', '<div', '<figure')):
                parts.append(f"  {p}")
            else:
                parts.append(f"  <p>{p if is_raw else esc(p)}</p>")
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
        ("Laboratorio M01 - Classificazione dei processi", a("01"),
         "Consolidare concetti di processo, livelli e classificazione cross-industry."),
        ("Laboratorio M02 - Scheda dei requisiti", a("02"),
         "Descrivere un processo, collegare attività ed entità informative e costruire una prima matrice attività–informazioni con requisiti verificabili."),
        ("Laboratorio M03 - Collocazione nel PCF", a("03"),
         "Collocare un processo aziendale nei primi tre livelli del Process Classification Framework di APQC."),
        ("Laboratorio M04 - Dalla Activity ai Task", a("04"),
         "Scomporre una Activity di un dominio APQC in quattro-sei Task con esecutore ed esito verificabile."),
        ("Laboratorio M05 - Matrice delle variabili", a("05"),
         "Costruire la matrice delle variabili con almeno un collo di bottiglia e una relazione causa-effetto."),
        ("Laboratorio M06 - Definire i KPI", a("06"),
         "Definire due-tre KPI con formula, unità, frequenza, fonte del dato e target motivato."),
        ("Laboratorio M07 - Visualizzare in Camunda", a("07"),
         "Aprire due esempi .bpmn in Camunda Modeler, leggerne corsie ed eventi, aggiungere un ramo di eccezione."),
        ("Laboratorio M08 - Scheda processo completa", a("08"),
         "Produrre il pacchetto completo di deliverable per un dominio APQC e presentarlo in aula."),
        ("Guida - BPMN con Camunda e assistente MCP", "lab-camunda-mcp.html",
         "Annesso opzionale: allestire l'ambiente (Claude, plugin MCP del Modeler, Camunda 8 in Docker) per generare le bozze BPMN dai prompt."),
        ("Esempi di processo APQC", REPO_TREE + "esempi-apqc/",
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
        ("ASCM — SCOR Digital Standard (supply chain)", "https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/"),
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
  <p>Otto moduli tematici derivati dai blocchi principali del programma. I moduli 7 e 8 usano i diagrammi BPMN e Camunda Modeler come laboratorio di visualizzazione sugli esempi APQC.</p>
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
 <a href="chapters/chapter-07.html">Modulo 7</a>
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
   <p>Questo è un <strong>annesso opzionale</strong> al Modulo 7: non fa parte del programma d'aula e non è un sillabo. Serve a chi, dopo aver visto i diagrammi BPMN degli esempi APQC, vuole provare a generarne una bozza a partire da una scheda processo, coordinandosi con i prompt.</p>
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
    <li><a href="#s06">6 SCOR: il framework usato dal caso originale</a></li>
    <li><a href="#s07">7 Come usarlo in aula</a></li>
    <li><a href="#s08">8 Fonti</a></li>
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
    <li><strong>Selezione e qualifica fornitori</strong> &mdash; 4.0 &rarr; 4.2.3 Select suppliers and develop/maintain contracts &mdash; <a href="{REPO_BLOB}caso-saem/esempi-apqc/03-acquisti/processo.md">processo.md</a> / <a href="{REPO_BLOB}caso-saem/esempi-apqc/03-acquisti/processo.bpmn">processo.bpmn</a></li>
    <li><strong>Ritiro prodotti, resi e riparazione deceleratori</strong> &mdash; 6.0 &rarr; 6.2.2 Manage customer service problems, requests, and inquiries &mdash; <a href="{REPO_BLOB}caso-saem/esempi-apqc/05-customer-service/processo.md">processo.md</a> / <a href="{REPO_BLOB}caso-saem/esempi-apqc/05-customer-service/processo.bpmn">processo.bpmn</a></li>
    <li><strong>Fatturazione settimanale</strong> &mdash; 9.0 &rarr; 9.2.2 Invoice customer &mdash; <a href="{REPO_BLOB}caso-saem/esempi-apqc/07-finance/processo.md">processo.md</a> / <a href="{REPO_BLOB}caso-saem/esempi-apqc/07-finance/processo.bpmn">processo.bpmn</a></li>
   </ul>
   <p>Ogni scheda ripete la stessa struttura degli esempi astratti (collocazione PCF, Activity, scomposizione in Task, SIPOC, matrice delle variabili, scheda sintetica, BPMN) ma con scenario, ruoli e flusso presi dal caso reale — i diagrammi BPMN qui includono anche gateway che nella versione astratta non c'erano (es. esito del vendor rating, tipo di richiesta reso/riparazione, canale di fatturazione).</p>
  </section>

  <section class="study-section" id="s05">
   <h2>5 Altri processi SAEM (candidati non ancora sviluppati)</h2>
   <p>Il caso ne descrive molti altri. Per ciascuno, un'ipotesi di collocazione sull'APQC PCF (con livello di confidenza) e, per confronto, sul modello SCOR — più nativo per un'azienda distributrice di prodotti fisici come SAEM (v. sezione 6).</p>
   <div class="data-table-wrap">
    <table class="data-table">
     <caption>Processi SAEM non ancora sviluppati come scheda/BPMN completa</caption>
     <thead>
      <tr><th>Processo SAEM</th><th>Process APQC candidato</th><th>Confidenza</th><th>Processo SCOR candidato</th></tr>
     </thead>
     <tbody>
      <tr><td>Programmazione ordini a fornitore</td><td>4.2.4 Order materials and services (4.2.4.4 Create/Distribute purchase orders)</td><td>Alta</td><td>S2.1&ndash;S2.2 Direct Procure</td></tr>
      <tr><td>Controllo qualità in ingresso</td><td>4.4.3.2 Receive, inspect, and store inbound deliveries</td><td>Alta</td><td>S2.5 Inspect and Verify</td></tr>
      <tr><td>Gestione reso a fornitore</td><td>4.4.2.4&ndash;4.4.2.5 Manage flow/disposition of returned products</td><td>Alta</td><td>S4 Source Return</td></tr>
      <tr><td>Preparazione offerta al cliente</td><td>3.5.3 Develop and manage sales proposals, bids, and quotes</td><td>Alta</td><td>O2.1 Process Inquiry and Quote</td></tr>
      <tr><td>Selezione spedizioniere, generazione bolle/carico veicolo</td><td>4.4.4.1 Plan, transport, and deliver outbound product</td><td>Alta</td><td>F2.6&ndash;F2.8 Schedule Transportation / Load Vehicle and Generate Shipping Document</td></tr>
      <tr><td>Gestione sistema informativo legacy (Pragma/MaxGestCS)</td><td>8.5/8.6 Develop and manage / Deploy services-solutions (categoria, non verificata a livello Process)</td><td>Media</td><td>&mdash; (SCOR non copre l'IT interno)</td></tr>
      <tr><td>Progetto di reengineering/e-commerce (Maxnet)</td><td>13.0 Develop and Manage Business Capabilities (categoria, non verificata)</td><td>Bassa</td><td>&mdash;</td></tr>
      <tr><td>Posizionamento strategico competitivo</td><td>1.2.2 Define and evaluate strategic options to achieve the mission</td><td>Media</td><td>OE1 Supply Chain Strategy (Orchestration Enabler)</td></tr>
      <tr><td>Sistema qualità/ambiente (ISO 9001/14001)</td><td>11.0 Manage Enterprise Risk, Compliance, Remediation and Resiliency (categoria, non verificata)</td><td>Bassa</td><td>OE8 Regulatory and Compliance (Orchestration Enabler)</td></tr>
     </tbody>
    </table>
   </div>
   <p>Sono candidati per estensioni future del materiale, se il corso vorrà arricchire anche i domini Vendite, Vision&amp;Strategy o IT con questo stesso caso. Le confidenze "Media"/"Bassa" segnalano codici verificati solo a livello di Category/Process Group sul PCF completo (K016809), non ancora a livello di Activity con i PDF "Definitions and Key Measures" corrispondenti (non tutti disponibili in <code>resources/</code>).</p>
  </section>

  <section class="study-section" id="s06">
   <h2>6 SCOR: il framework usato dal caso originale</h2>
   <p>La tesi originale su cui è basato questo caso (Bozzoli, 2004-2005) non usava l'APQC PCF, ma il modello <strong>SCOR (Supply Chain Operations Reference)</strong> insieme a diagrammi UML — scelta naturale per un distributore di prodotti fisici, dato che SCOR è specializzato sui processi di supply chain (pianificazione, approvvigionamento, produzione, evasione ordini, logistica, resi), mentre l'APQC PCF è una tassonomia generica cross-industry che copre anche le funzioni non di supply chain (vendite, HR, IT, finance...).</p>
   <p>SCOR è mantenuto oggi dalla <strong>Association for Supply Chain Management (ASCM)</strong>, erede del Supply-Chain Council che lo creò nel 1996, sotto il nome di <strong>SCOR Digital Standard (SCOR-DS)</strong>. Il modello attuale organizza i processi su un livello Orchestrate (le tredici funzioni trasversali di governo della supply chain) e sei processi di primo livello: <strong>Plan, Order, Source, Transform, Fulfill, Return</strong> — la versione "classica" nota alla tesi del 2004-2005 aveva invece cinque processi macro (Plan, Source, Make, Deliver, Return).</p>
   <p>Una sintesi completa dei processi SCOR-DS (livelli, categorie, elementi di processo) e una mappatura di prima approssimazione dei processi SAEM sui processi SCOR sono in <a href="{REPO_BLOB}resources/scor-overview.md">resources/scor-overview.md</a>.</p>
  </section>

  <section class="study-section" id="s07">
   <h2>7 Come usarlo in aula</h2>
   <p>Per ciascuno dei tre processi si può ripetere l'esercizio già impostato per gli esempi APQC astratti: individuare Category/Process Group/Process/Activity nel PCF, scomporre in Task, costruire SIPOC e matrice delle variabili, leggere il BPMN con le corsie per ruolo. A differenza degli esempi puri, qui i partecipanti lavorano su un caso con <strong>criticità reali già documentate</strong> (doppia codifica articoli, autorizzazioni di prezzo/reso, shelf life breve) da usare come base per la discussione su rischi e colli di bottiglia.</p>
   <p>Esercizio di confronto tra framework: far classificare uno o due processi SAEM sia su APQC PCF sia su SCOR (v. sezione 6), discutendo dove i due framework isolano lo stesso confine di processo e dove no, e perché.</p>
  </section>

  <section class="study-section" id="s08">
   <h2>8 Fonti</h2>
   <ul class="reference-list">
    <li>C. Bozzoli, <em>"Reengineering del sistema di gestione ordini in ottica e-commerce: il caso SAEM S.p.A."</em>, tesi di laurea, Politecnico di Milano, A.A. 2004-2005 (relatore Prof. Ing. T. Barbieri) — <a href="{REPO_BLOB}resources/casoSAEM.pdf">PDF completo</a>.</li>
    <li><a href="{REPO_BLOB}caso-saem/caso-saem-compresso.md">Versione compressa del caso</a> (azienda, organizzazione, i quattro processi principali) usata come base per le schede.</li>
    <li>ASCM, <em>"SCOR Digital Standard — Quick Reference Guide"</em>, © 2025, CC BY-NC-ND 4.0 — <a href="{REPO_BLOB}resources/scor-ds-digital-guide_final.pdf">PDF completo</a>. Framework interattivo: <a href="https://scor.ascm.org" target="_blank" rel="noopener noreferrer">scor.ascm.org</a>.</li>
    <li><a href="{REPO_BLOB}resources/scor-overview.md">Sintesi SCOR ad uso didattico</a> (gerarchia dei processi, mappatura SAEM &rarr; SCOR).</li>
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
