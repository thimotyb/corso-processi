# 4.0 Manage Supply Chain for Physical Products — versione SAEM S.p.A.
*Versione arricchita, radicata nel caso SAEM (vedi `caso-saem/caso-saem-compresso.md` e `resources/casoSAEM.pdf`), della scheda astratta [`esempi-apqc/03-acquisti/processo.md`](../../../esempi-apqc/03-acquisti/processo.md) — stessa gerarchia APQC PCF v8.0, stesso Process, narrazione e ruoli reali del caso.*
## 0. Scenario
SAEM S.p.A. è un distributore (non produce) e deve garantire un parco di oltre 100 fornitori (case produttrici di adesivi, lubrificanti, macchine utensili, componenti) affidabili e certificati. Il Direttore Vendite (DIRV) avvia la ricerca quando emerge un fabbisogno di una nuova linea di prodotto o quando un fornitore già qualificato deve essere valutato per una nuova gamma. Per orientarsi, SAEM sfrutta anche un consorzio europeo di aziende distributrici simili, che condivide informazioni sui possibili candidati prima di avviare una ricerca di mercato autonoma.
## 1. Collocazione nella gerarchia PCF
| Livello | Codice | Nome |
|---|---|---|
| Category | 4.0 | Manage Supply Chain for Physical Products |
| Process Group | 4.2 | Procure materials and services (10216) |
| Process | 4.2.3 | Select suppliers and develop/maintain contracts (10278) |

**Evento di innesco (trigger):** Il DIRV individua il fabbisogno di un nuovo fornitore o di una nuova linea prodotti da un fornitore già rappresentato
**Evento finale / output di processo:** Il fornitore è qualificato, l'anagrafica fornitore/prodotto è creata a sistema e il contratto è attivo

## 2. Activity del processo (dal PCF, istanziate sul caso SAEM)
| Codice | Activity | Come si manifesta in SAEM |
|---|---|---|
| 4.2.3.1 | Select suppliers (10288) | Ricerca candidati anche tramite il consorzio europeo di aziende consociate, prima di una ricerca di mercato autonoma |
| 4.2.3.2 | Certify and validate suppliers (10289) | Questionario di prevalutazione (anagrafica, organizzazione, sistema qualità) + eventuale visita con rapporto + vendor rating su 5 parametri pesati |
| 4.2.3.3 | Negotiate and establish contracts (10290) | Negoziazione delle condizioni; caso reale citato nel documento: accordo di distribuzione con Petrol per i lubrificanti speciali |
| 4.2.3.4 | Manage contracts (10291) | Creazione dell'anagrafica fornitore/prodotto a sistema; rivalutazione semestrale sui 5 parametri; eventuali azioni correttive o rimozione dalla lista |

## 3. Scomposizione in Task (esempio SAEM)
Esempio di scomposizione dell'Activity **"Certify and validate suppliers (10289)"**, così come descritta nel caso:

1. Inviare al candidato il questionario di prevalutazione (anagrafica, organizzazione, sistema qualità)
2. Effettuare, se necessario, una visita presso la casa produttrice e redigere il rapporto di visita
3. Raccogliere listini, schede tecniche e schede di sicurezza dei prodotti
4. Applicare la tecnica di vendor rating sui 5 parametri pesati previsti dall'azienda

## 4. SIPOC
| Supplier | Input | Process (macro-fasi) | Output | Customer |
|---|---|---|---|---|
| Casa produttrice candidata, consorzio europeo di aziende consociate | Questionario di prevalutazione compilato, rapporto di visita, listini, schede tecniche e di sicurezza | Selezionare candidati (anche via consorzio) → Certificare (questionario + visita + vendor rating) → Negoziare le condizioni → Creare l'anagrafica e gestire il contratto nel tempo (rivalutazione semestrale) | Fornitore qualificato e attivo a sistema, con anagrafica fornitore/prodotto creata; oppure fornitore scartato/rimosso dalla lista | Ufficio Traffico/Acquisti (emette gli ordini al fornitore), Magazzino (riceve la merce) |

## 5. Matrice delle variabili di processo
| Variabile | Descrizione | Esempio nel caso SAEM |
|---|---|---|
| Input | Dati necessari ad avviare il processo | Fabbisogno di nuova linea prodotti, questionario di prevalutazione, rapporto di visita |
| Output | Risultato prodotto dal processo | Anagrafica fornitore/prodotto creata a sistema, contratto attivo |
| Tempi | Durata tipica del processo | Da alcune settimane (fornitore già noto tramite consorzio) a alcuni mesi (nuova ricerca di mercato + visita) |
| Costi | Risorse economiche assorbite | Ore DIRV, eventuale trasferta per la visita, costi di test in laboratorio SAEM |
| Volumi | Quantità/frequenza di esecuzione | Oltre 100 fornitori attivi; rivalutazione di ciascuno ogni 6 mesi |
| Ruoli | Attori coinvolti | Direttore Vendite (DIRV), consorzio europeo, fornitore candidato |
| Sistemi | Applicativi/strumenti a supporto | MaxGestCS (anagrafica fornitore/prodotto), archivio documentale (questionari, rapporti di visita) |
| Vincoli | Limiti operativi o normativi | Certificazioni ISO 9001/14001 di SAEM da mantenere lungo tutta la filiera fornitori |
| Rischi / colli di bottiglia | Punti critici del processo | Dipendenza da fornitore unico per una categoria (es. Petrol per i lubrificanti); fornitore che non supera la rivalutazione semestrale e va sostituito senza interrompere le consegne |

## 6. Scheda processo sintetica
- **Nome processo:** 4.2.3 Select suppliers and develop/maintain contracts (10278)
- **Process owner:** Direttore Vendite (DIRV)
- **Obiettivo:** Garantire un parco fornitori affidabile, certificato e coerente con gli standard di qualità ISO 9001/14001 di SAEM
- **Confini:** da "Il DIRV individua il fabbisogno di un nuovo fornitore o di una nuova linea prodotti da un fornitore già rappresentato" a "Il fornitore è qualificato, l'anagrafica fornitore/prodotto è creata a sistema e il contratto è attivo"
- **Ruoli coinvolti:** DIRV, consorzio europeo di aziende consociate, fornitore candidato
- **Sistemi coinvolti:** MaxGestCS (anagrafiche), archivio documentale qualità
- **KPI:** Tempo medio di qualifica di un nuovo fornitore; % fornitori che superano la rivalutazione semestrale; numero di azioni correttive aperte
- **Rischi / colli di bottiglia:** Dipendenza da fornitore unico su categorie strategiche; ritardo nella rivalutazione semestrale con conseguente rischio su qualità/continuità delle consegne

## 7. Rappresentazione BPMN
Vedi file allegato `processo.bpmn` — importabile in [Camunda Modeler](https://camunda.com/download/modeler/). Rispetto alla versione astratta, questo diagramma introduce un gateway di esito del vendor rating (fornitore idoneo / scartato), assente nella versione astratta.
Corsie (lane): Direttore Vendite (DIRV), Sistema Informativo / Anagrafiche.
