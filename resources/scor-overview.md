# Il modello SCOR (Supply Chain Operations Reference)

*Sintesi ad uso didattico. Fonte primaria: ASCM, "SCOR Digital Standard — Quick Reference Guide", © 2025, CC BY-NC-ND 4.0 — [`resources/scor-ds-digital-guide_final.pdf`](scor-ds-digital-guide_final.pdf). Framework completo e interattivo: [scor.ascm.org](https://scor.ascm.org).*

## Cos'è e chi lo mantiene

SCOR è un framework di riferimento per la gestione della supply chain, dal fornitore del fornitore al cliente del cliente. Nasce nel 1996 per iniziativa del **Supply-Chain Council (SCC)**, un consorzio di aziende che volevano un linguaggio comune per descrivere, confrontare e migliorare i processi logistico-produttivi. Nel 2014 il SCC è confluito in **APICS**, a sua volta parte dal 2018 dell'**Association for Supply Chain Management (ASCM)**, che oggi mantiene e aggiorna il modello sotto il nome di **SCOR Digital Standard (SCOR-DS)**.

A differenza dell'APQC PCF — tassonomia generica, cross-industry, che copre *tutti* i processi di un'azienda (vendite, HR, IT, finance...) — SCOR è **specializzato sulla supply chain fisica**: pianificazione, approvvigionamento, produzione, evasione ordini, logistica e resi. È quindi il framework più naturale per un'azienda manifatturiera o distributiva, mentre l'APQC PCF resta preferibile quando si vuole classificare l'intera organizzazione con un unico schema.

> **Nota storica per il caso SAEM**: la tesi originale (2004-2005) su cui è basato `caso-saem/` usava proprio SCOR (nella versione "classica" dell'epoca, precedente al restyling Digital Standard) insieme a diagrammi UML, per lo stesso motivo — SAEM è un distributore fisico, e SCOR mappa i suoi processi di supply chain meglio di una tassonomia generica. La versione compressa del caso usata nel corso omette SCOR/UML a favore dell'APQC PCF, per coerenza con il resto del materiale; questo documento recupera SCOR come framework di confronto.

## Le quattro componenti del modello

1. **Processes** — la tassonomia dei processi (vedi sotto).
2. **Performance** — metriche di misurazione, organizzate in 8 *performance attribute*: Reliability (RL), Responsiveness (RS), Agility (AG), Cost (CO), Profit (PR), Asset management (AM), Environmental (EV), Social (SC). Tre livelli di metriche (L1 = KPI strategici, L2 = diagnostici di L1, L3 = diagnostici di L2); oltre 300 metriche definite.
3. **Practices** — configurazioni/pratiche ricorrenti di un processo (automazione, tecnologia, sequenza, modalità di collaborazione tra organizzazioni), organizzate in 4 *pillar*: Analytics, Technology, Process, Organization.
4. **People** — competenze (skill) richieste per eseguire i processi, con esperienza e formazione associate.

## Gerarchia dei processi (Level 0 → Level 3)

- **Level 0 — Orchestrate**: le attività che connettono la supply chain a fornitori, clienti e stakeholder interni (strategia, regole di business, dati/tecnologia, contratti, rischio, ESG...). Sono i tredici **Orchestration Enabler (OE1-OE13)**, trasversali a tutti gli altri processi.
- **Level 1 — i sei processi macro**: Plan, Order, Source, Transform, Fulfill, Return (dettaglio sotto).
- **Level 2 — categorie di processo**: varianti del Level 1 (es. *Source stocked product* vs *Source make-to-order product*).
- **Level 3 — elementi di processo**: le attività elementari, con input/output e metriche associate (es. `S1.9 Analyze Offers and Select Suppliers`).

Il modello si ferma al Level 3: il Level 4 (esecuzione operativa, specifica per singola azienda/ERP) non è standardizzato — esattamente come l'APQC PCF si ferma alle Activity e lascia i Task/le procedure alla singola organizzazione.

## I sei processi di Level 1 (e le categorie di Level 2)

| Processo | Descrizione | Categorie di Level 2 |
|---|---|---|
| **Plan** | Bilancia domanda e offerta aggregate, sviluppa i piani tattici per Order, Source, Transform, Fulfill e Return. | P1 Plan Supply Chain · P2 Plan Order · P3 Plan Source · P4 Plan Transform · P5 Plan Fulfill · P6 Plan Return |
| **Order** | Gestisce il ciclo dell'ordine cliente: cattura, validazione, pagamento, conferma. | O1 Order B2C · O2 Order B2B · O3 Order Intra-company |
| **Source** | Approvvigiona beni e servizi per soddisfare la domanda pianificata o effettiva. | S1 Strategic Source · S2 Direct Procure · S3 Indirect Procure · S4 Source Return |
| **Transform** | Trasforma il prodotto/servizio nello stato finito (ex "Make"): produzione, erogazione di un servizio, manutenzione/riparazione. | T1 Transform Product · T2 Transform Service · T3 Transform MRO (Maintenance, Repair, Overhaul) |
| **Fulfill** | Consegna il prodotto/servizio finito al cliente: prelievo, imballo, spedizione, installazione, fatturazione. | F1 Fulfill B2C · F2 Fulfill B2B · F3 Fulfill Intra-company |
| **Return** | Gestisce il flusso inverso — resi dal cliente o verso il fornitore, diagnosi, disposizione, eventuale rilavorazione. | R1 Return Product · R2 Return Service · R3 Return MRO |

*(Il modello "classico" pre-2022, quello presumibilmente noto alla tesi SAEM, aveva 5 processi macro — Plan, Source, Make, Deliver, Return — poi arricchiti con "Enable" come sesto. SCOR-DS li ha riorganizzati separando l'Order dal Deliver/Fulfill e rinominando Make in Transform, oltre ad aggiungere il livello Orchestrate.)*

## Esempi di Level 3 (elementi di processo)

Per dare concretezza, alcuni elementi di Level 3 rilevanti per un distributore come SAEM:

- `S1.6` Prequalify Suppliers · `S1.9` Analyze Offers and Select Suppliers · `S1.10` Negotiate and Award Contract
- `S2.2` Schedule Product Delivery · `S2.5` Inspect and Verify · `S2.7` Authorize Supplier Payment
- `S4.1`-`S4.5` (Source Return): Initiate a Source Return → Request Authorize Product Return → Identify Product Condition/Return Reason → Schedule Product Shipment → Close or Adjust Return Order
- `O2.1` Process Inquiry and Quote · `O2.3` Confirm Inventory Availability and Delivery Date · `O2.6` Process Payment
- `F2.3`-`F2.9` (Fulfill B2B): Pick Product → Pack and/or Kit Product → Stage Product → Schedule Transportation → Notify and Confirm Dock Appointment → Load Vehicle and Generate Shipping Document → Invoice
- `R1.1`-`R1.5` (Return Product): Initiate/Authorize/Schedule/Verify Product Return → Receive Product → RMA Close or Adjust Return Order → Diagnose and/or Test → Disposition Product
- `T3.1`-`T3.12` (Transform MRO): dal ricevimento del pezzo guasto (`T3.1`) alla diagnosi (`T3.2`), riparazione (`T3.7`), collaudo (`T3.8`) e restituzione — il percorso seguito nel caso SAEM per la riparazione dei deceleratori.

## Mappatura di prima approssimazione: processi SAEM → SCOR

| Processo SAEM | Processo/elemento SCOR candidato | Confidenza |
|---|---|---|
| Selezione e qualifica fornitori | **S1** Strategic Source (S1.6 Prequalify Suppliers, S1.9 Analyze Offers and Select Suppliers) | Alta |
| Gestione ordine cliente (offerta → ordine → evasione) | **O2** Order B2B + **F2** Fulfill B2B (per i clienti/distributori) | Alta |
| Preparazione offerta al cliente | **O2.1** Process Inquiry and Quote | Alta |
| Selezione spedizioniere, generazione bolle, carico veicolo | **F2.6**-**F2.8** Schedule Transportation / Load Vehicle and Generate Shipping Document | Alta |
| Ritiro e gestione resi (incl. riparazione deceleratori) | **R1** Return Product (reso cliente) + **T3** Transform MRO (riparazione) | Alta |
| Fatturazione | **O2.6/F2.9** Process Payment / Invoice — SCOR non ha un processo di fatturazione dedicato come l'APQC 9.2.2: è distribuito dentro Order/Fulfill | Media |
| Programmazione ordini a fornitore | **S2.1**-**S2.2** Direct Procure (Establish Order Signal, Schedule Product Delivery) | Alta |
| Controllo qualità in ingresso | **S2.5** Inspect and Verify | Alta |
| Gestione reso a fornitore | **S4** Source Return | Alta |
| Sistema qualità/ambiente (ISO 9001/14001), posizionamento strategico | **OE1** Supply Chain Strategy, **OE8** Regulatory and Compliance (Orchestration Enabler) | Media |

Da confrontare con la mappatura sullo stesso caso verso l'APQC PCF, in [`caso-saem/caso-saem-compresso.md`](../caso-saem/caso-saem-compresso.md) e nella pagina "Caso di studio" del sito del corso.

## Come usarlo in aula

Un esercizio efficace è far ripetere ai partecipanti la classificazione di uno o due processi SAEM **sia su APQC PCF sia su SCOR**, confrontando i due risultati: dove i due framework isolano lo stesso confine di processo, dove no, e perché SCOR (specializzato, granulare sulle attività fisiche di supply chain) risulta più naturale di un framework generico come l'APQC PCF per un'azienda come SAEM — un distributore fisico — mentre l'APQC resta più adatto a coprire anche le funzioni non di supply chain (vendite, IT, finance, HR) con lo stesso schema.
