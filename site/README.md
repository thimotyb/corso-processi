# Sito del corso processi-MOCI06

Sito statico di studio per il corso **processi-MOCI06 — Classificazione e analisi dei
processi industriali**. I moduli sono derivati dai blocchi principali del sillabo
(`../sillabo_processi_MOCI06.docx`); BPMN e Camunda Modeler sono usati come
laboratorio di visualizzazione sugli esempi APQC (`../esempi-apqc/`), non come
argomento tecnico a sé.

## Struttura

| File | Contenuto |
|---|---|
| `index.html` | Home: presentazione, obiettivi, informazioni, elenco moduli, laboratori, riferimenti |
| `chapters/chapter-01.html` … `chapter-07.html` | 7 moduli tematici, struttura a due livelli (1 / 1.1), punti chiave a fine modulo |
| `lab-camunda-mcp.html` | Annesso **opzionale** al Modulo 6: ambiente Claude + plugin MCP del Modeler + Camunda 8 in Docker per generare bozze BPMN dai prompt. Non fa parte del programma d'aula |
| `assets/css/main.css`, `assets/js/back-to-top.js` | Stili e comportamento (albero struttura, evidenziazione sezione attiva, pulsante di stampa, foglio di stile per la stampa) — ripresi dal course-kit datamesh |

## Moduli

1. M01 — Classificazione e architettura dei processi
2. M02 — APQC PCF: Category, Process Group, Process
3. M03 — Dalla Activity al Task
4. M04 — Variabili di processo e relazioni
5. M05 — Indicatori e misurazione
6. M06 — Rappresentazione: SIPOC, process map, swimlane, BPMN
7. M07 — Scheda processo completa (laboratorio integrato)

## Uso

Server locale + browser:

```
./start-site.sh          # porta 8080, apre il browser sulla home
./start-site.sh 9000     # porta a scelta
NO_OPEN=1 ./start-site.sh # solo server, senza browser
```

In alternativa aprire `index.html` direttamente in un browser. Nessuna dipendenza
esterna, nessun build: il sito è servibile come file statici (anche via GitHub Pages).

All'avvio `start-site.sh` esegue automaticamente `check_links.py`, che verifica i
collegamenti locali e gli ancoraggi tra le pagine HTML.

## Rigenerazione

I contenuti HTML sono prodotti dallo script `build_site.py` (in questa cartella):

```
python3 site/build_site.py
```

Lo script riscrive `index.html`, `chapters/*.html` e `lab-camunda-mcp.html`; CSS e JS
sono copiati una tantum dal course-kit datamesh e non vengono toccati. Convenzioni
riprese dalla skill `claude-course-builder`; lingua italiana per coerenza con il
sillabo MOCI06.
