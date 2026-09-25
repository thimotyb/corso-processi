#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera il sito del corso processi-MOCI06 (home + 8 moduli + guida di laboratorio).

Riusa CSS/JS del corso datamesh (skill claude-course-builder): albero struttura a
due livelli, evidenziazione sezione attiva, pulsante di stampa, foglio di stile per
la stampa. Contenuti in italiano per coerenza con sillabo_processi_MOCI06.docx.
"""
import html
import pathlib
import re
from pypdf import PdfReader

ROOT = pathlib.Path("/home/thimoty/git/corso-processi/site")
CH = ROOT / "chapters"
RESOURCES = ROOT.parent / "resources"

COURSE = "processi-MOCI06 — Classificazione e analisi dei processi industriali"
REPO_BLOB = "https://github.com/thimotyb/corso-processi/blob/main/"
REPO_TREE = "https://github.com/thimotyb/corso-processi/tree/main/"

MODULES = [
    ("01", "M01 - Classificazione e architettura dei processi"),
    ("02", "M02 - Raccolta e documentazione dei requisiti"),
    ("03", "M03 - APQC PCF: Category, Process Group, Process"),
    ("04", "M04 - Dalla Activity al Task"),
    ("05", "M05 - Variabili di processo e relazioni"),
    ("06", "M06 - Rappresentazione: SIPOC, process map, swimlane, BPMN"),
    ("07", "M07 - Indicatori e misurazione"),
    ("08", "M08 - Scheda processo completa (laboratorio integrato)"),
]

# id dell'ultima sezione (esercitazione) di ogni modulo — calcolato dal contenuto
LAB_ANCHOR = {}

PCF_CATEGORIES = [
    ("1.0", "Develop Vision and Strategy", "Definisce il concetto d'impresa, la visione di lungo periodo, la strategia e le iniziative necessarie per attuarla."),
    ("2.0", "Develop and Manage Products and Services", "Governa il portafoglio e lo sviluppo di prodotti e servizi, dall'idea fino alla preparazione del rilascio."),
    ("3.0", "Market and Sell Products and Services", "Comprende l'analisi di mercati e clienti, il marketing, la strategia commerciale e la gestione delle vendite."),
    ("4.0", "Manage Supply Chain for Physical Products", "Pianifica e gestisce approvvigionamento, produzione, logistica e magazzino dei prodotti fisici."),
    ("5.0", "Deliver Services", "Definisce la governance, prepara le risorse e gestisce l'erogazione dei servizi ai clienti."),
    ("6.0", "Manage Customer Service", "Governa assistenza post-vendita, richieste, reclami, richiami di prodotto e soddisfazione del cliente."),
    ("7.0", "Develop and Manage Human Resources", "Pianifica e gestisce l'intero ciclo di vita delle persone, dalla selezione fino alla mobilità e all'uscita."),
    ("8.0", "Manage Information Technology (IT)", "Allinea l'IT al business e gestisce informazioni, rischi, soluzioni, distribuzione e supporto tecnologico."),
    ("9.0", "Manage Financial Resources", "Gestisce pianificazione economica, contabilità, ricavi, pagamenti, tesoreria, controlli e fiscalità."),
    ("10.0", "Acquire, Construct, and Manage Assets", "Governa pianificazione, acquisizione, costruzione, manutenzione e fine vita degli asset aziendali."),
    ("11.0", "Manage Enterprise Risk, Compliance, Remediation, and Resiliency", "Gestisce rischi d'impresa, conformità, azioni correttive e capacità di continuità e ripresa."),
    ("12.0", "Manage External Relationships", "Cura le relazioni con investitori, autorità, settore, consiglio di amministrazione, comunità e media."),
    ("13.0", "Develop and Manage Business Capabilities", "Sviluppa capacità trasversali per processi, progetti, qualità, cambiamento, conoscenza, dati, sicurezza e sostenibilità."),
]

PCF_PROCESS_GROUPS = {
    "1.0": [
        ("1.1", "Define the business concept and long-term vision", "Analizza contesto e capacità interne per chiarire identità, finalità e visione futura dell'organizzazione."),
        ("1.2", "Develop business strategy", "Traduce visione e missione in opzioni, obiettivi e scelte strategiche coordinate."),
        ("1.3", "Develop and measure strategic initiatives", "Seleziona, attua e misura le iniziative con cui realizzare la strategia."),
        ("1.4", "Develop and maintain business models", "Definisce, governa e aggiorna il modo in cui l'organizzazione crea e sostiene valore."),
    ],
    "2.0": [
        ("2.1", "Govern and manage product/service development program", "Governa portafoglio, ciclo di vita, proprietà intellettuale e dati principali di prodotti e servizi."),
        ("2.2", "Generate and define new product/service ideas", "Raccoglie opportunità e bisogni e li trasforma in idee e requisiti per nuove offerte."),
        ("2.3", "Develop products and services", "Progetta, prototipa, prova e prepara alla produzione o all'erogazione le nuove offerte."),
    ],
    "3.0": [
        ("3.1", "Understand markets, customers, and capabilities", "Analizza mercato, clienti, concorrenti e capacità interne per individuare opportunità praticabili."),
        ("3.2", "Develop marketing strategy", "Definisce proposta di valore, posizionamento, marchio, prezzi e canali di marketing."),
        ("3.3", "Develop and manage marketing plans", "Pianifica ed esegue campagne, promozioni, contenuti e attività di relazione con il mercato."),
        ("3.4", "Develop sales strategy", "Definisce segmenti, canali, obiettivi, modelli organizzativi e politiche della funzione vendite."),
        ("3.5", "Develop and manage sales plans", "Gestisce previsioni, opportunità, proposte, ordini, partner commerciali e risultati di vendita."),
    ],
    "4.0": [
        ("4.1", "Plan for and align supply chain resources", "Prevede domanda e capacità e coordina le risorse necessarie alla supply chain."),
        ("4.2", "Procure materials and services", "Seleziona fonti e fornitori e gestisce ordini, ricezione e prestazioni degli approvvigionamenti."),
        ("4.3", "Produce/Assemble/Test product", "Programma, produce, assembla, collauda e rilascia i prodotti secondo requisiti di qualità."),
        ("4.4", "Manage logistics and warehousing", "Gestisce magazzino, trasporti, distribuzione, consegne e logistica inversa."),
    ],
    "5.0": [
        ("5.1", "Establish service delivery governance and strategies", "Definisce regole, obiettivi e strategie con cui governare l'erogazione dei servizi."),
        ("5.2", "Manage service delivery resources", "Prevede la domanda e pianifica, assegna e prepara persone e risorse di servizio."),
        ("5.3", "Manage and Operate Service Delivery System", "Pianifica, avvia, conduce e controlla il sistema operativo di erogazione."),
        ("5.4", "Deliver service to customer", "Avvia, esegue e conclude il servizio concordato, verificandone esito e completezza."),
    ],
    "6.0": [
        ("6.1", "Develop customer service strategy", "Definisce requisiti, esperienza attesa, politiche, procedure e livelli di servizio."),
        ("6.2", "Plan and manage customer service contacts", "Pianifica la forza lavoro e gestisce richieste, problemi, informazioni e reclami dei clienti."),
        ("6.3", "Service products after sales", "Registra i prodotti e gestisce garanzie, riparazioni, resi e altri interventi post-vendita."),
        ("6.4", "Manage product recalls and regulatory audits", "Pianifica ed esegue richiami di prodotto e supporta verifiche e audit regolamentari."),
        ("6.5", "Evaluate customer service operations and customer satisfaction", "Misura prestazioni dell'assistenza, soddisfazione, garanzie e risultati dei richiami."),
    ],
    "7.0": [
        ("7.1", "Develop and manage human resources planning, policies, and strategies", "Definisce strategia, piani, politiche, struttura e costi delle risorse umane."),
        ("7.2", "Recruit, source, and select employees", "Pianifica il fabbisogno e ricerca, valuta, seleziona e assume le persone."),
        ("7.3", "Manage employee onboarding, training, and development", "Inserisce le persone e ne sviluppa competenze, prestazioni e percorsi professionali."),
        ("7.4", "Manage employee relations", "Gestisce relazioni di lavoro, istanze, benessere, sicurezza e rapporti con le rappresentanze."),
        ("7.5", "Reward and retain employees", "Amministra retribuzione, benefit, riconoscimenti e iniziative di fidelizzazione."),
        ("7.6", "Redeploy and retire employees", "Gestisce mobilità, riassegnazioni, pensionamenti, dimissioni e cessazioni."),
        ("7.7", "Manage employee information and analytics", "Amministra dati e documenti del personale e produce analisi per le decisioni HR."),
        ("7.8", "Manage employee communication", "Pianifica e realizza la comunicazione interna rivolta alle persone."),
    ],
    "8.0": [
        ("8.1", "Develop and manage IT customer relationships", "Comprende bisogni degli utenti interni e concorda servizi, trasformazioni e livelli di servizio IT."),
        ("8.2", "Develop and manage IT business strategy", "Allinea strategia, architettura, portafoglio e modello operativo IT alle priorità aziendali."),
        ("8.3", "Develop and manage IT resilience and risk", "Gestisce continuità, sicurezza, privacy, rischi, controlli e identità digitali."),
        ("8.4", "Manage information", "Definisce strategia, architettura, ciclo di vita e amministrazione delle informazioni aziendali."),
        ("8.5", "Develop and manage services/solutions", "Progetta, sviluppa, integra, prova e governa il ciclo di vita delle soluzioni IT."),
        ("8.6", "Deploy services/solutions", "Pianifica e realizza il rilascio delle soluzioni, il cambiamento e il passaggio in esercizio."),
        ("8.7", "Create and manage support services/solutions", "Gestisce infrastrutture, esercizio, assistenza utenti e supporto continuativo ai servizi IT."),
    ],
    "9.0": [
        ("9.1", "Perform planning and management accounting", "Svolge pianificazione, budgeting, forecasting, contabilità gestionale e analisi delle prestazioni."),
        ("9.2", "Perform revenue accounting", "Gestisce credito, fatturazione, crediti verso clienti, incassi e rettifiche dei ricavi."),
        ("9.3", "Perform general accounting and reporting", "Registra operazioni, chiude i conti, consolida e produce rendiconti finanziari e gestionali."),
        ("9.4", "Manage fixed-asset project accounting", "Contabilizza progetti e costi connessi alla creazione o modifica di immobilizzazioni."),
        ("9.5", "Process payroll", "Calcola retribuzioni, trattenute, versamenti e registrazioni collegate alle paghe."),
        ("9.6", "Process accounts payable and expense reimbursements", "Gestisce debiti verso fornitori, fatture passive e rimborsi spese."),
        ("9.7", "Manage treasury operations", "Governa liquidità, finanziamenti, investimenti, rischi finanziari e rapporti bancari."),
        ("9.8", "Manage internal controls", "Definisce, applica, verifica e corregge i controlli interni di natura finanziaria."),
        ("9.9", "Manage taxes", "Pianifica e amministra adempimenti, dichiarazioni, pagamenti e controversie fiscali."),
        ("9.10", "Manage international funds/consolidation", "Gestisce movimenti finanziari internazionali, cambi e consolidamento tra entità del gruppo."),
        ("9.11", "Perform global trade services", "Supporta operazioni commerciali internazionali, strumenti di pagamento e finanziamento degli scambi."),
    ],
    "10.0": [
        ("10.1", "Plan and acquire assets", "Definisce fabbisogni, investimenti e modalità di acquisizione degli asset."),
        ("10.2", "Design and construct assets", "Progetta e realizza asset e infrastrutture controllando tempi, costi, qualità e conformità."),
        ("10.3", "Maintain assets", "Pianifica ed esegue manutenzione preventiva, correttiva e predittiva degli asset."),
        ("10.4", "Manage asset end-of-life", "Gestisce dismissione, vendita, riciclo o sostituzione degli asset a fine vita."),
    ],
    "11.0": [
        ("11.1", "Manage enterprise risk", "Definisce il quadro di enterprise risk management e identifica, valuta e tratta i rischi."),
        ("11.2", "Manage compliance", "Individua obblighi, definisce controlli e verifica il rispetto di norme e politiche."),
        ("11.3", "Manage remediation efforts", "Analizza non conformità e incidenti e governa azioni correttive e preventive."),
        ("11.4", "Manage business resiliency", "Prepara continuità operativa, risposta alle crisi, disaster recovery e ripristino."),
    ],
    "12.0": [
        ("12.1", "Build investor relationships", "Gestisce comunicazioni, informazioni e rapporti con investitori e comunità finanziaria."),
        ("12.2", "Manage government and industry relationships", "Cura rapporti con istituzioni, regolatori, associazioni e organismi di settore."),
        ("12.3", "Manage relations with board of directors", "Supporta il consiglio di amministrazione con governance, informazioni e adempimenti."),
        ("12.4", "Manage legal and ethical issues", "Gestisce questioni legali, proprietà intellettuale, contenzioso ed etica aziendale."),
        ("12.5", "Manage public relations program", "Pianifica relazioni pubbliche, comunicazioni esterne, media e gestione della reputazione."),
    ],
    "13.0": [
        ("13.1", "Manage business processes", "Governa, definisce, misura e migliora i processi aziendali."),
        ("13.2", "Manage portfolio, program, and project", "Seleziona e governa portafogli, programmi e progetti fino alla loro chiusura."),
        ("13.3", "Manage enterprise quality", "Definisce piani, controlli e miglioramenti per garantire la qualità a livello aziendale."),
        ("13.4", "Manage change", "Prepara, attua e consolida cambiamenti organizzativi e comportamentali."),
        ("13.5", "Develop and manage enterprise-wide knowledge management (KM) capability", "Costruisce e mantiene capacità, governance e pratiche di gestione della conoscenza."),
        ("13.6", "Manage Content", "Governa creazione, classificazione, conservazione, distribuzione e controllo dei contenuti."),
        ("13.7", "Measure and benchmark", "Definisce sistemi di misurazione e confronta prestazioni interne ed esterne."),
        ("13.8", "Develop, manage, and deliver analytics", "Trasforma dati e analisi in informazioni utilizzabili per decisioni e prestazioni."),
        ("13.9", "Manage environmental health and safety (EHS)", "Gestisce ambiente, salute e sicurezza attraverso politiche, controlli e prevenzione."),
        ("13.10", "Manage sustainability", "Integra obiettivi ambientali, sociali ed economici e ne misura i risultati."),
    ],
}

# URL ufficiali delle schede APQC incluse nella raccolta PCF 8.0. Gli slug
# pubblicati non sono uniformi: mantenerli espliciti evita di generare link
# errati concatenando codice e nome della Category.
PCF_CATEGORY_LINKS = {
    "1.0": "https://www.apqc.org/resource-library/resource-listing/10-develop-vision-and-strategy-definitions-pcf-version-80",
    "2.0": "https://www.apqc.org/resource-library/resource-listing/20-develop-and-manage-products-and-services-definitions-and-key-3",
    "3.0": "https://www.apqc.org/resource-library/resource-listing/30-market-and-sell-products-and-services-definitions-and-key-3",
    "4.0": "https://www.apqc.org/resource-library/resource-listing/40-manage-supply-chain-physical-products-definitions-and-key",
    "5.0": "https://www.apqc.org/resource-library/resource-listing/50-deliver-services-key-definitions-pcf-version-80",
    "6.0": "https://www.apqc.org/resource-library/resource-listing/60-manage-customer-service-definitions-and-key-measures-pcf-0",
    "7.0": "https://www.apqc.org/resource-library/resource-listing/70-develop-and-manage-human-resources-definitions-and-key",
    "8.0": "https://www.apqc.org/resource-library/resource-listing/80-manage-information-technology-it-definitions-and-key-1",
    "9.0": "https://www.apqc.org/resource-library/resource-listing/90-manage-financial-resources-definitions-and-key-measures-pcf-1",
    "10.0": "https://www.apqc.org/resource-library/resource-listing/100-acquire-construct-and-manage-assets-definitions-and-key-1",
    "11.0": "https://www.apqc.org/resource-library/resource-listing/110-manage-enterprise-risk-compliance-remediation-and-0",
    "12.0": "https://www.apqc.org/resource-library/resource-listing/120-manage-external-relationships-key-definitions-pcf-version-80",
    "13.0": "https://www.apqc.org/resource-library/resource-listing/130-develop-and-manage-business-capabilities-definitions-and-1",
}

def pcf_category_table():
    rows = "".join(
        f"<tr><td><code>{code}</code></td><td><strong>{name}</strong></td><td>{description}</td></tr>"
        for code, name, description in PCF_CATEGORIES
    )
    return f'<div class="table-wrap"><table class="pcf-table"><thead><tr><th>Category</th><th>Nome</th><th>Spiegazione</th></tr></thead><tbody>{rows}</tbody></table></div>'

def pcf_process_group_tables():
    blocks = []
    for code, category, _ in PCF_CATEGORIES:
        rows = "".join(
            f"<tr><td><code>{group_code}</code></td><td><strong>{name}</strong></td><td>{description}</td></tr>"
            for group_code, name, description in PCF_PROCESS_GROUPS[code]
        )
        blocks.append(
            f'<div class="pcf-group-block"><h4>{code} {category}</h4>'
            f'<p><a href="{PCF_CATEGORY_LINKS[code]}" target="_blank" rel="noopener noreferrer">Apri la scheda APQC e scarica il PDF della Category {code}</a> '
            f'(nella scheda della raccolta 8.0 scegliere <em>View Now</em>).</p>'
            f'<div class="table-wrap"><table class="pcf-table"><thead><tr><th>Process Group</th><th>Nome</th><th>Spiegazione</th></tr></thead><tbody>{rows}</tbody></table></div></div>'
        )
    return "".join(blocks)

def pcf_support_categories_list():
    items = "".join(
        f"<li><code>{code}</code> <strong>{category}</strong></li>"
        for code, category, _ in PCF_CATEGORIES[6:]
    )
    return f'<ul class="study-bullets">{items}</ul>'

PCF_DOMAIN_REPOSITORIES = [
    ("Visione e strategia", "01-vision-strategy"),
    ("Vendite", "02-vendite"),
    ("Acquisti", "03-acquisti"),
    ("Servizi", "04-servizi"),
    ("Customer service", "05-customer-service"),
    ("IT", "06-it"),
    ("Finance", "07-finance"),
]

def pcf_domain_links():
    items = "".join(
        f'<li><strong>{label}</strong> — '
        f'<a href="{REPO_BLOB}esempi-apqc/{slug}/processo.md">scheda processo.md</a> · '
        f'<a href="{REPO_BLOB}esempi-apqc/{slug}/processo.bpmn">diagramma processo.bpmn</a> '
        f'(apribile con Camunda Modeler)</li>'
        for label, slug in PCF_DOMAIN_REPOSITORIES
    )
    return f'<ul class="study-bullets">{items}</ul>'

KPI_CATEGORIES = ("1.0", "3.0", "4.0", "5.0", "6.0", "8.0", "9.0")

def kpi_description(name):
    lower = name.lower()
    if "cycle time" in lower or "average time" in lower:
        return "Misura il tempo necessario per completare l'operazione indicata."
    if "total cost" in lower or "cost per" in lower or "cost to perform" in lower:
        return "Misura il costo sostenuto, normalizzato rispetto al volume indicato."
    if "number of ftes" in lower:
        return "Misura il personale equivalente a tempo pieno impiegato nel processo rispetto al volume indicato."
    if " per fte" in lower:
        return "Misura la produttività rapportando il volume elaborato a ogni addetto equivalente a tempo pieno."
    if "percentage" in lower:
        return "Misura la quota percentuale del fenomeno indicato rispetto al totale osservato."
    if "rate" in lower:
        return "Misura il tasso con cui si verifica il fenomeno indicato."
    if "budget" in lower:
        return "Misura l'entità del budget rispetto ai ricavi o alle risorse professionali indicate."
    if "days sales outstanding" in lower:
        return "Misura i giorni medi necessari per trasformare i crediti commerciali in incassi."
    if "schedule adherence" in lower:
        return "Misura quanto gli operatori rispettano la pianificazione assegnata."
    if "utilization" in lower:
        return "Misura il livello di utilizzo della capacità disponibile."
    if "speed of answer" in lower or "handling time" in lower:
        return "Misura la rapidità con cui i contatti dei clienti vengono presi in carico o gestiti."
    if "forecast accuracy" in lower:
        return "Misura la precisione della previsione rispetto al risultato effettivo."
    if "downtime" in lower or "outages" in lower:
        return "Misura l'indisponibilità non pianificata di impianti o servizi."
    if "return on investment" in lower:
        return "Misura il rendimento ottenuto rispetto al ritorno sull'investimento pianificato."
    return "Misura la prestazione descritta dal KPI nel perimetro del Process Group."

def extract_process_group_kpis():
    """Estrae i KPI APQC dalle sette Category usate negli esempi di M03."""
    pdfs = {}
    for path in RESOURCES.glob("*Definitions*8.0*.pdf"):
        match = re.search(r"_(\d+)\.0 ", path.name)
        if match:
            pdfs[f"{match.group(1)}.0"] = path

    result = {}
    for category_code in KPI_CATEGORIES:
        source = pdfs.get(category_code)
        if source is None:
            raise FileNotFoundError(f"PDF APQC mancante per la Category {category_code}")
        text = "\n".join(page.extract_text() or "" for page in PdfReader(source).pages)
        groups = PCF_PROCESS_GROUPS[category_code]
        for position, (group_code, group_name, _) in enumerate(groups):
            heading = re.compile(
                rf"(?m)^\s*{re.escape(group_code)}\s+{re.escape(group_name)}\s*\(\d+\)"
            )
            matches = list(heading.finditer(text))
            if not matches:
                raise ValueError(f"Process Group {group_code} non trovato in {source.name}")
            start = matches[-1].start()
            if position + 1 < len(groups):
                next_code, next_name, _ = groups[position + 1]
                next_heading = re.compile(
                    rf"(?m)^\s*{re.escape(next_code)}\s+{re.escape(next_name)}\s*\(\d+\)"
                )
                following = [item for item in next_heading.finditer(text) if item.start() > start]
                end = following[0].start() if following else len(text)
            else:
                end = len(text)
            segment = text[start:end]
            subgroup = re.search(rf"(?m)^\s*{re.escape(group_code)}\.\d+\s", segment)
            group_intro = segment[:subgroup.start()] if subgroup else segment
            table = re.search(
                r"Suggested KPI(?:s)?\s*\n\s*Metric ID\s+KPI\s*\n(.*)",
                group_intro,
                re.S,
            )
            kpis = []
            if table:
                flattened = " ".join(line.strip() for line in table.group(1).splitlines())
                for item in re.split(r"(?=\b\d{6}\s)", flattened):
                    metric = re.match(r"(\d{6})\s+(.+)", item.strip())
                    if metric:
                        name = re.sub(
                            r"\s+K\d+\s+\d+\s+©\d{4}\s+APQC\s+ALL RIGHTS RESERVED.*$",
                            "",
                            metric.group(2).strip(),
                        )
                        kpis.append((metric.group(1), name))
            result[group_code] = kpis
    return result

def pcf_kpi_table():
    kpis_by_group = extract_process_group_kpis()
    rows = []
    for category_code in KPI_CATEGORIES:
        category_name = next(name for code, name, _ in PCF_CATEGORIES if code == category_code)
        for group_code, group_name, _ in PCF_PROCESS_GROUPS[category_code]:
            kpis = kpis_by_group[group_code]
            if not kpis:
                rows.append(
                    f'<tr><td><code>{category_code}</code> {category_name}</td>'
                    f'<td><code>{group_code}</code> {group_name}</td>'
                    '<td colspan="2"><em>Nessun KPI proposto da APQC al livello del Process Group.</em></td></tr>'
                )
                continue
            for metric_id, kpi_name in kpis:
                rows.append(
                    f'<tr><td><code>{category_code}</code> {category_name}</td>'
                    f'<td><code>{group_code}</code> {group_name}</td>'
                    f'<td><code>{metric_id}</code> {html.escape(kpi_name)}</td>'
                    f'<td>{kpi_description(kpi_name)}</td></tr>'
                )
    return (
        '<div class="table-wrap"><table class="pcf-table pcf-kpi-table">'
        '<thead><tr><th>Category</th><th>Process Group</th><th>KPI APQC proposto</th><th>Descrizione</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )

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
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/saem-fasi-inserimento-ordine.png\" alt=\"Fasi dell'inserimento dell'ordine in SAEM: arrivo dell'ordine, smistamento, verifica e inserimento a sistema, invio della conferma\" data-caption=\"Fasi dell'inserimento dell'ordine in SAEM.\"><figcaption>Fasi dell'inserimento dell'ordine in SAEM.</figcaption></figure>",
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
   "Quando il requisito coinvolge dati persistenti, la fonte deve consentire anche di motivare le operazioni sui dati. La notazione <strong>CRUD</strong> distingue quattro operazioni: <strong>C - Create</strong>, creazione di una nuova istanza; <strong>R - Read</strong>, lettura senza modifica; <strong>U - Update</strong>, aggiornamento di un'istanza esistente; <strong>D - Delete</strong>, eliminazione di un'istanza. Una stessa attività può compiere più operazioni sulla stessa entità.",
   "Il codice CRUD da solo non costituisce un requisito completo. Per ogni cella occorre indicare <strong>perché</strong> l'attività accede al dato, quale ruolo avvia l'operazione, quale condizione la rende necessaria e quale risultato deve essere verificabile.",
  ],None),
  (2,"4.2 Confini e livelli di dettaglio",[
   "La raccolta deve mantenere il collegamento tra il requisito e il livello a cui si riferisce. Un obiettivo riguarda il processo nel suo insieme; una regola può riguardare una specifica attività; un requisito informativo può riguardare un singolo dato o una singola interazione con il sistema.",
   "Un requisito troppo generale non è verificabile; uno troppo dettagliato può anticipare inutilmente una soluzione tecnica. Il livello corretto è quello che consente di comprendere il comportamento atteso, assegnare una responsabilità, verificare l'esito e mantenere aperte le scelte progettuali ancora non decise.",
   "La <strong>matrice CRUD</strong> rende esplicito questo livello di dettaglio: dispone le entità o gli archivi sulle righe, le attività sulle colonne e registra nelle celle le operazioni compiute. Si legge sia per colonna, per controllare tutti i dati richiesti da un'attività, sia per riga, per verificare il ciclo di vita di ogni entità.",
   "Nell'esempio SAEM dell'ordine telematico, la matrice deriva dall'Assembly Line e dalle prove dei moduli sul database di sviluppo. Mostra, per esempio, che la ricerca di un articolo legge <code>Articoli</code>, <code>Articoli_storico</code>, <code>Scadmag</code> e i listini, mentre la conferma crea movimenti e messaggi e legge, aggiorna o elimina dati del carrello. Le lettere descrivono operazioni del sistema TO-BE, non attività storiche dell'AS-IS.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch02/tavola-crud-d2a-ordine-telematico.png\" alt=\"Tavola CRUD SAEM D.2A: entità del database sulle righe, attività dell'ordine telematico sulle colonne e operazioni C, R, U e D nelle celle\" data-caption=\"Tavola CRUD dell'ordine telematico SAEM.\"><figcaption>Tavola CRUD D.2A dell'ordine telematico: la matrice sintetizza le operazioni compiute dalle attività sulle tabelle del sistema TO-BE.</figcaption></figure>",
  ],None),
  (1,"5 Dalle attività alle entità informative",[
   "Dopo aver scelto quali attività del processo possono essere supportate da un sistema IT nello scenario TO-BE, si passa dall'analisi di business alla mappatura dei requisiti informativi. Il passaggio è un processo di <strong>selezione</strong>: dal modello di business si individuano soltanto attività e informazioni pertinenti al sistema da progettare.",
   "Le <strong>entità informative candidate</strong> sono strutture dati o unità informative la cui presenza appare significativa o probabile nel sistema di supporto. Possono essere un cliente, un ordine, una riga d'ordine, un articolo, un'autorizzazione o un messaggio. Sono candidate perché l'analisi successiva può confermarle, trasformarle, accorparle o eliminarle.",
   "L'<strong>Assembly Line</strong> mette in relazione i due livelli. La parte superiore contiene la porzione del processo di business; la parte inferiore dispone le linee associate agli elementi informativi; la fascia intermedia collega le attività alle entità mediante relazioni dirette di lettura e scrittura. Le relazioni selezionate permettono poi di derivare i casi d'uso e i requisiti del sistema dal punto di vista dell'utente.",
   "Nel caso SAEM le entità non sono semplici candidate: il progetto conserva il DBMS Emaxgest5 e il diagramma usa le tabelle effettivamente individuate nel database PostgreSQL. Questa precisazione riguarda il sistema TO-BE di MaxNet III e non autorizza ad attribuire retroattivamente le stesse tabelle alle attività storiche AS-IS.",
  ],None),
  (2,"5.1 Letture, scritture e responsabilità",[
   "Nell'Assembly Line una relazione di <strong>lettura</strong> indica che l'attività usa un'informazione già presente; una relazione di <strong>scrittura</strong> indica che crea o modifica un'informazione resa disponibile alle attività successive. I collegamenti non vanno aggiunti per semplice vicinanza grafica: ognuno deve corrispondere a un'interazione documentata.",
   "La parte superiore della figura seguente mostra il flusso di inserimento dell'offerta; gli ovali centrali sono i casi d'uso candidati; le linee inferiori rappresentano le tabelle del database. I cerchi sulle intersezioni rendono visibile dove una funzione legge o scrive. La disposizione orizzontale facilita la lettura delle relazioni.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch02/assembly-line-d1-inserimento-offerta.png\" alt=\"Assembly Line SAEM D.1 ruotata in orizzontale: processo di inserimento offerta, casi d'uso candidati e tabelle collegate da letture e scritture\" data-caption=\"Assembly Line D.1 per l'inserimento dell'offerta.\"><figcaption>Assembly Line D.1 per l'inserimento dell'offerta: dal processo di business ai casi d'uso e alle tabelle del sistema TO-BE.</figcaption></figure>",
   "Per interpretare il disegno si segue una singola attività dall'alto verso il basso: si identifica il caso d'uso che la supporta, quindi si osservano le entità raggiunte e il tipo di accesso. L'annotazione va infine completata con il <strong>ruolo</strong>, lo scopo dell'operazione e la fonte. Leggere i dati del cliente per autenticare l'utente è infatti un requisito diverso dal leggerli per compilare la testata di un'offerta.",
  ],None),
  (2,"5.2 La matrice attività–informazioni",[
   "Una matrice attività–informazioni mette in riga le attività e in colonna le entità o gli archivi. Nelle celle si annotano le operazioni compiute. La matrice fornisce una vista sintetica e consente di verificare che ogni informazione prodotta abbia un destinatario e che ogni informazione letta sia giustificata da un'attività.",
   "Quando l'archivio è persistente, la matrice può essere dettagliata con la notazione <strong>CRUD</strong>: Create, Read, Update e Delete. La matrice non sostituisce la descrizione testuale, ma la integra e aiuta a validare la coerenza tra modello del processo e modello dei dati.",
   "La tavola D.1 mostra il passaggio dall'Assembly Line alla vista CRUD per l'inserimento dell'offerta. Le righe identificano le tabelle del sistema TO-BE, mentre le colonne rappresentano le attività applicative. Una cella può contenere più lettere quando la stessa attività compie operazioni diverse sulla medesima tabella.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch02/tavola-crud-d1-inserimento-offerta.png\" alt=\"Tavola CRUD SAEM D.1: tabelle sulle righe, attività di inserimento dell'offerta sulle colonne e operazioni C, R, U e D nelle celle\" data-caption=\"Tavola CRUD D.1 per l'inserimento dell'offerta.\"><figcaption>Tavola CRUD D.1 per l'inserimento dell'offerta: sintesi delle operazioni sulle tabelle del sistema TO-BE.</figcaption></figure>",
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
   "L'analisi collega ciascuna attività alle informazioni utilizzate e prodotte. Per l'ordine telematico, per esempio, la creazione del carrello legge cliente, condizioni di consegna e parametri IVA; la conferma legge e verifica testata e righe; l'esito positivo crea l'ordine effettivo e trasferisce le righe.",
   "Le operazioni sono poi formalizzate nelle Assembly Line e nelle tavole CRUD. Da queste relazioni vengono derivati i casi d'uso e le relative specifiche testuali, con attori, flussi, alternative, eccezioni, precondizioni, postcondizioni, frequenza e criticità.",
  ],None),
  (2,"7.1 Esempio: gestione dell'ordine telematico",[
   "L'attore cliente crea la testata del carrello, inserisce gli articoli, verifica disponibilità e condizioni, quindi conferma l'ordine. Il sistema legge le informazioni necessarie, segnala le righe non disponibili, ricalcola i dati economici e, se le verifiche hanno esito positivo, trasforma il carrello in ordine.",
   "Le entità informative coinvolte includono cliente, condizioni di consegna, tabella IVA, carrello, righe del carrello, articoli, storico articoli, scadenze di magazzino, listini, ordine e messaggi. La loro presenza nel modello deve essere collegata all'attività che le legge o le scrive e alla fonte che documenta l'interazione.",
   "L'esempio D.2A permette di seguire la trasformazione completa dal processo ai requisiti. L'<strong>Assembly Line</strong> collega le attività alle tabelle e individua i casi d'uso candidati; il <strong>diagramma dei casi d'uso</strong> mostra attori e relazioni; la <strong>scheda testuale</strong> specifica comportamento, alternative e condizioni di un singolo caso d'uso.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch02/assembly-line-d2a-ordine-telematico.png\" alt=\"Assembly Line SAEM D.2A ruotata in orizzontale: attività di inserimento dell'ordine telematico, casi d'uso e tabelle collegate da letture e scritture\" data-caption=\"Assembly Line D.2A per l'inserimento dell'ordine telematico.\"><figcaption>Assembly Line D.2A: dalle attività di inserimento dell'ordine telematico ai casi d'uso candidati e alle tabelle del sistema TO-BE.</figcaption></figure>",
   "Il diagramma derivato contiene sette casi d'uso. <strong>Crea nuovo carrello</strong>, <strong>Aggiungi articolo in carrello</strong> e <strong>Conferma ordine</strong> costituiscono il percorso principale; richiesta di offerta, modifica della riga e trasformazione del carrello intervengono come estensioni o varianti. Gli attori sono il Cliente, che avvia il processo via Internet, e il Sistema EDP.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch02/diagramma-casi-uso-d2a-ordine-telematico.png\" alt=\"Diagramma dei casi d'uso SAEM D.2A per l'ordine telematico con gli attori Cliente e Sistema EDP e sette casi d'uso collegati\" data-caption=\"Diagramma dei casi d'uso D.2A per l'inserimento dell'ordine telematico.\"><figcaption>Diagramma dei casi d'uso D.2A: attori, casi principali ed estensioni della gestione dell'ordine telematico.</figcaption></figure>",
   "Come esempio di specifica testuale, il <strong>caso d'uso 11 - Conferma ordine</strong> descrive l'azione del Cliente e le verifiche del Sistema EDP: controllo degli scaduti, validità dell'offerta, disponibilità e importo minimo; in caso positivo il sistema aggiorna le disponibilità, salva il carrello come ordine, elimina il carrello e comunica il numero assegnato. La scheda registra anche alternative, precondizioni, postcondizioni, eccezioni, frequenza e criticità.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch02/scheda-caso-uso-11-conferma-ordine.png\" alt=\"Scheda SAEM del caso d'uso 11 Conferma ordine con attori, flusso degli eventi, alternative, condizioni, eccezioni, frequenza e criticità\" data-caption=\"Scheda del caso d'uso 11: Conferma ordine.\"><figcaption>Scheda del caso d'uso 11 - Conferma ordine: specifica testuale del comportamento mostrato nel diagramma D.2A.</figcaption></figure>",
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
   "APQC sviluppa strumenti e conoscenze per il benchmarking, la gestione dei processi e il miglioramento delle prestazioni. Il <strong>Process Classification Framework</strong>, sviluppato a partire dal 1992, offre un linguaggio comune per discutere, organizzare e confrontare il lavoro svolto dalle organizzazioni.",
   "Il PCF è un <strong>elenco gerarchico di processi aziendali</strong>, non la sequenza con cui il lavoro deve essere eseguito. La versione cross-industry organizza il lavoro in tredici Category di alto livello, progressivamente articolate in Process Group, Process, Activity e Task. Ogni elemento possiede un identificativo stabile che permette di mantenere il riferimento anche quando nomi e formulazioni vengono adattati.",
   "Un vocabolario condiviso riduce le ambiguità tra funzioni, sedi e organizzazioni. Lo stesso processo può infatti essere chiamato in modi diversi oppure essere distribuito tra reparti differenti: il PCF consente di descriverlo a partire dal risultato prodotto, senza dipendere dall'organigramma locale.",
   "Le applicazioni principali sono il <strong>benchmarking</strong>, perché definizioni comuni rendono confrontabili misure e prestazioni; la <strong>gestione dei processi</strong>, perché il framework aiuta a costruire l'inventario dei processi e a definirne i confini; e la <strong>gestione dei contenuti</strong>, perché procedure, indicatori, rischi e documenti possono essere classificati secondo una struttura coerente.",
   "<div class=\"note-box\"><strong>Approfondimenti APQC:</strong><ul class=\"study-bullets\"><li><a href=\"https://www.apqc.org/resource-library/resource-listing/introduction-apqcs-process-classification-framework-pcf\" target=\"_blank\" rel=\"noopener noreferrer\">Introduction to APQC's Process Classification Framework (PCF)</a></li><li><a href=\"https://www.apqc.org/process-frameworks\" target=\"_blank\" rel=\"noopener noreferrer\">Process Frameworks</a></li><li><a href=\"https://www.apqc.org/blog/what-are-different-types-process-models\" target=\"_blank\" rel=\"noopener noreferrer\">What are the different types of process models?</a></li><li><a href=\"https://www.apqc.org/process-frameworks/pcf-faqs\" target=\"_blank\" rel=\"noopener noreferrer\">PCF Frequently Asked Questions</a></li></ul></div>",
  ],None),
  (2,"1.2 La versione Cross-Industry 8.0",[
   "La versione <strong>Cross-Industry</strong> è il modello più generale: può essere applicata a organizzazioni di qualsiasi settore e copre sia i processi operativi sia quelli di gestione e supporto. Le versioni <strong>industry-specific</strong> conservano la struttura di base e gli identificativi di riferimento, ma approfondiscono i processi caratteristici di uno specifico comparto.",
   "La struttura comune permette di confrontarsi anche con organizzazioni di settori diversi; il dettaglio settoriale consente invece confronti più precisi con i propri pari. Il framework resta un punto di partenza da adattare: alcune voci possono non essere applicabili, mentre altre possono richiedere un'estensione locale mantenendo la tracciabilità verso il PCF.",
   "APQC distribuisce il PCF in formato <strong>PDF</strong> ed <strong>Excel</strong>. Il PDF rende immediatamente leggibile la gerarchia ed è utile per presentare il framework e costruire consenso; il foglio Excel contiene definizioni in linea più complete ed è più adatto all'indicizzazione, all'integrazione e alla costruzione di modelli aziendali.",
   "<div class=\"note-box\"><strong>Scarica il PCF Cross-Industry 8.0:</strong><ul class=\"study-bullets\"><li><a href=\"https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-pdf-13\" target=\"_blank\" rel=\"noopener noreferrer\">Versione PDF</a> - apre la scheda APQC con il comando <em>View Now</em>.</li><li><a href=\"https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-excel-12\" target=\"_blank\" rel=\"noopener noreferrer\">Versione Excel</a> - apre la scheda APQC con il comando <em>View Now</em>.</li></ul></div>",
  ],None),
  (1,"2 I livelli della gerarchia",[
   "Il PCF scompone il lavoro in cinque livelli: <strong>Category</strong>, <strong>Process Group</strong>, <strong>Process</strong>, <strong>Activity</strong> e <strong>Task</strong>. Ogni passaggio restringe il campo: dalla grande area di lavoro si arriva agli eventi chiave e alle azioni operative.",
   "I primi tre livelli costituiscono l'ossatura con cui classificare i processi dell'organizzazione. Activity e Task aggiungono il dettaglio esecutivo e saranno approfonditi nel modulo successivo.",
   "La gerarchia non implica che tutti gli elementi abbiano lo stesso peso. Il PCF non è <strong>uniformemente livellato</strong>: task collocati in rami diversi possono richiedere quantità di lavoro differenti e, quando serve, possono essere ulteriormente scomposti in sotto-task.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch03/livelli-pcf.png\" alt=\"Gerarchia APQC PCF articolata nei cinque livelli Category, Process Group, Process, Activity e Task\" data-caption=\"I cinque livelli gerarchici del Process Classification Framework.\"><figcaption>I cinque livelli del PCF: dalla Category al Task, con dettaglio progressivamente maggiore.</figcaption></figure>",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch03/esempio-gerarchia-processi.png\" alt=\"Esempio di gerarchia APQC con Category, Process Group, Process, Activity e Task, illustrata attraverso i codici 11.0, 11.1, 11.1.3, 11.1.3.3 e 11.1.3.3.1\" data-caption=\"Esempio di gerarchia dei cinque livelli del PCF.\"><figcaption>Esempio di gerarchia PCF: la Category 11.0 viene progressivamente scomposta in Process Group, Process, Activity e Task.</figcaption></figure>",
   "Il diagramma seguente applica i primi tre livelli a un ramo reale. La Category <code>6.0 Manage Customer Service</code> si divide in Process Group; ciascun Process Group contiene a sua volta i Process che ne specificano il perimetro.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch03/pcf-primi-tre-livelli.svg\" alt=\"Diagramma ad albero dei primi tre livelli APQC PCF per la Category 6.0 Manage Customer Service, con Process Group e Process\" data-caption=\"Albero dei primi tre livelli del PCF applicato al Customer Service.\"><figcaption>Albero Mermaid dei primi tre livelli: Category, Process Group e Process nel ramo Customer Service.</figcaption></figure>",
  ],None),
  (2,"2.1 Category (livello 1)",[
   "La <strong>Category</strong> rappresenta il livello più alto del PCF e identifica una grande area di lavoro, per esempio «Develop Vision and Strategy» o «Manage Customer Service». Le tredici Category della versione cross-industry forniscono una vista complessiva dell'organizzazione.",
   "Le Category operative descrivono la catena del valore; quelle di gestione e supporto descrivono le funzioni abilitanti.",
   "La Category non coincide necessariamente con un reparto. Una stessa area di lavoro può attraversare più unità organizzative e coinvolgere ruoli differenti.",
   "<div class=\"pcf-category-list\"><ol><li><strong>1.0 Develop Vision and Strategy</strong> - definisce il concetto d'impresa, la visione, la strategia e le iniziative strategiche.<ul><li><code>1.1</code> Define the business concept and long-term vision</li><li><code>1.2</code> Develop business strategy</li><li><code>1.3</code> Develop and measure strategic initiatives</li><li><code>1.4</code> Develop and maintain business models</li></ul></li><li><strong>2.0 Develop and Manage Products and Services</strong> - governa il portafoglio e il ciclo di sviluppo di prodotti e servizi, dall'idea alla preparazione del rilascio.<ul><li><code>2.1</code> Govern and manage product/service development program</li><li><code>2.2</code> Generate and define new product/service ideas</li><li><code>2.3</code> Develop products and services</li></ul></li><li><strong>3.0 Market and Sell Products and Services</strong> - comprende conoscenza del mercato, strategia e pianificazione di marketing e vendite.<ul><li><code>3.1</code> Understand markets, customers, and capabilities</li><li><code>3.2</code> Develop marketing strategy</li><li><code>3.3</code> Develop and manage marketing plans</li><li><code>3.4</code> Develop sales strategy</li><li><code>3.5</code> Develop and manage sales plans</li></ul></li><li><strong>4.0 Manage Supply Chain for Physical Products</strong> - pianifica e gestisce approvvigionamento, produzione, logistica e magazzino dei prodotti fisici.<ul><li><code>4.1</code> Plan for and align supply chain resources</li><li><code>4.2</code> Procure materials and services</li><li><code>4.3</code> Produce/Assemble/Test product</li><li><code>4.4</code> Manage logistics and warehousing</li></ul></li><li><strong>5.0 Deliver Services</strong> - definisce la governance, prepara le risorse e gestisce l'erogazione del servizio al cliente.<ul><li><code>5.1</code> Establish service delivery governance and strategies</li><li><code>5.2</code> Manage service delivery resources</li><li><code>5.3</code> Manage and Operate Service Delivery System</li><li><code>5.4</code> Deliver service to customer</li></ul></li><li><strong>6.0 Manage Customer Service</strong> - governa le interazioni successive alla vendita, le richieste, i reclami, l'assistenza e la soddisfazione del cliente.<ul><li><code>6.1</code> Develop customer service strategy</li><li><code>6.2</code> Plan and manage customer service contacts</li><li><code>6.3</code> Service products after sales</li><li><code>6.4</code> Manage product recalls and regulatory audits</li><li><code>6.5</code> Evaluate customer service operations and customer satisfaction</li></ul></li><li><strong>7.0 Develop and Manage Human Resources</strong> - pianifica e gestisce l'intero ciclo di vita delle persone, dalla selezione all'uscita.<ul><li><code>7.1</code> Develop and manage human resources planning, policies, and strategies</li><li><code>7.2</code> Recruit, source, and select employees</li><li><code>7.3</code> Manage employee onboarding, training, and development</li><li><code>7.4</code> Manage employee relations</li><li><code>7.5</code> Reward and retain employees</li><li><code>7.6</code> Redeploy and retire employees</li><li><code>7.7</code> Manage employee information and analytics</li><li><code>7.8</code> Manage employee communication</li></ul></li><li><strong>8.0 Manage Information Technology (IT)</strong> - allinea l'IT al business e gestisce informazioni, soluzioni, distribuzione e supporto tecnologico.<ul><li><code>8.1</code> Develop and manage IT customer relationships</li><li><code>8.2</code> Develop and manage IT business strategy</li><li><code>8.3</code> Develop and manage IT resilience and risk</li><li><code>8.4</code> Manage information</li><li><code>8.5</code> Develop and manage services/solutions</li><li><code>8.6</code> Deploy services/solutions</li><li><code>8.7</code> Create and manage support services/solutions</li></ul></li><li><strong>9.0 Manage Financial Resources</strong> - comprende pianificazione e contabilità, ricavi, pagamenti, tesoreria, controlli e fiscalità.<ul><li><code>9.1</code> Perform planning and management accounting</li><li><code>9.2</code> Perform revenue accounting</li><li><code>9.3</code> Perform general accounting and reporting</li><li><code>9.4</code> Manage fixed-asset project accounting</li><li><code>9.5</code> Process payroll</li><li><code>9.6</code> Process accounts payable and expense reimbursements</li><li><code>9.7</code> Manage treasury operations</li><li><code>9.8</code> Manage internal controls</li><li><code>9.9</code> Manage taxes</li><li><code>9.10</code> Manage international funds/consolidation</li><li><code>9.11</code> Perform global trade services</li></ul></li><li><strong>10.0 Acquire, Construct, and Manage Assets</strong> - governa pianificazione, acquisizione, costruzione, manutenzione e fine vita degli asset.<ul><li><code>10.1</code> Plan and acquire assets</li><li><code>10.2</code> Design and construct assets</li><li><code>10.3</code> Maintain assets</li><li><code>10.4</code> Manage asset end-of-life</li></ul></li><li><strong>11.0 Manage Enterprise Risk, Compliance, Remediation, and Resiliency</strong> - gestisce rischi, conformità, azioni correttive e continuità operativa.<ul><li><code>11.1</code> Manage enterprise risk</li><li><code>11.2</code> Manage compliance</li><li><code>11.3</code> Manage remediation efforts</li><li><code>11.4</code> Manage business resiliency</li></ul></li><li><strong>12.0 Manage External Relationships</strong> - cura le relazioni con investitori, autorità, settore, consiglio di amministrazione, comunità e media.<ul><li><code>12.1</code> Build investor relationships</li><li><code>12.2</code> Manage government and industry relationships</li><li><code>12.3</code> Manage relations with board of directors</li><li><code>12.4</code> Manage legal and ethical issues</li><li><code>12.5</code> Manage public relations program</li></ul></li><li><strong>13.0 Develop and Manage Business Capabilities</strong> - sviluppa capacità trasversali per processi, progetti, qualità, cambiamento, conoscenza, contenuti, misurazione, analytics, sicurezza e sostenibilità.<ul><li><code>13.1</code> Manage business processes</li><li><code>13.2</code> Manage portfolio, program, and project</li><li><code>13.3</code> Manage enterprise quality</li><li><code>13.4</code> Manage change</li><li><code>13.5</code> Develop and manage enterprise-wide knowledge management (KM) capability</li><li><code>13.6</code> Manage Content</li><li><code>13.7</code> Measure and benchmark</li><li><code>13.8</code> Develop, manage, and deliver analytics</li><li><code>13.9</code> Manage environmental health and safety (EHS)</li><li><code>13.10</code> Manage sustainability</li></ul></li></ol></div>",
  ],None),
  (2,"2.2 Process Group (livello 2)",[
   "Il <strong>Process Group</strong> è un insieme coerente di processi appartenenti alla stessa Category. Dentro «Manage Customer Service» si trova, per esempio, «Plan and manage customer service contacts».",
   "Questo livello rende navigabile una Category e delimita un dominio gestionale abbastanza omogeneo da associare a responsabilità, indicatori e iniziative di miglioramento, senza entrare ancora nel dettaglio operativo delle singole attività.",
  ],None),
  (2,"2.3 Process (livello 3)",[
   "Il <strong>Process</strong> è l'unità di analisi principale: riunisce gli elementi fondamentali necessari per conseguire un risultato e può comprendere varianti, controlli e rilavorazioni. «Manage customer service problems, requests, and inquiries» è un esempio di Process.",
   "È a questo livello che normalmente si definiscono obiettivo, confini, input, output, responsabile e indicatori e si costruiscono scheda processo, SIPOC e diagramma.",
   "Ogni elemento PCF possiede componenti standard: un <strong>identificativo numerico univoco</strong>, il titolo, una frase in corsivo che ne descrive il dominio, una descrizione dettagliata, eventuali riferimenti incrociati ad altri elementi e un <strong>codice gerarchico</strong> che ne indica la posizione, per esempio <code>4.3.1</code>. L'identificativo univoco sostiene il benchmarking anche quando nomi e definizioni vengono adattati.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch03/formato-elemento-pcf.png\" alt=\"Formato standard di un elemento PCF con identificativo univoco, titolo, dominio, descrizione e riferimenti incrociati\" data-caption=\"Componenti standard di un elemento del PCF.\"><figcaption>Come leggere un elemento PCF: identificativo stabile, titolo, dominio, descrizione e riferimenti ad altri elementi.</figcaption></figure>",
  ],None),
  (1,"3 Identificare le Category in azienda",[
   "Collocare i processi reali nel PCF richiede di partire dalle finalità, non dai reparti. Si individuano prima le Category presenti, poi i Process Group pertinenti, infine i Process effettivamente eseguiti.",
   "Il PCF descrive <strong>che cosa</strong> fa l'organizzazione, ma non rappresenta il flusso con cui il lavoro viene eseguito. Non è quindi una process map, un flow chart o un diagramma a corsie; fornisce invece la struttura comune dalla quale questi modelli possono essere derivati e collegati.",
   "La stessa struttura può collegare modelli diversi. Nell'enterprise architecture, per esempio, consente di chiedere quali sistemi sostengono un determinato processo e, in senso inverso, quali processi dipendono da uno specifico sistema. Questo rende più leggibili gli impatti di una modifica organizzativa o tecnologica.",
  ],None),
  (2,"3.1 Processi operativi, di gestione e di supporto",[
   "I processi operativi generano direttamente valore per il cliente esterno: sviluppare prodotti, vendere, consegnare. I processi di gestione e supporto rendono possibile l'operatività: gestire IT, risorse umane, risorse finanziarie.",
   "La distinzione orienta le priorità di analisi e la scelta degli indicatori.",
  ],None),
  (2,"3.2 Esempi per dominio",[
   "Gli esempi del corso coprono sette domini: visione e strategia, vendite, acquisti, servizi, customer service, IT, finance. Ciascuno è collocato nei primi tre livelli PCF e poi sviluppato fino alla Activity.",
   "Per ciascuna delle tredici Category, APQC pubblica un documento <strong>Process Definitions and Key Measures</strong>. Questi documenti affiancano alla gerarchia le definizioni degli elementi e gli indicatori suggeriti, con un identificativo per ogni metrica.",
   "Nell'esempio seguente, il Process Group <code>4.3 Produce/Assemble/Test product</code> è accompagnato da una definizione e da KPI relativi al costo e ai fermi macchina; subito sotto compare la definizione del Process <code>4.3.1 Schedule production</code>. La lettura combinata di gerarchia, definizione e misure aiuta a verificare che il processo aziendale sia collocato nel ramo corretto.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch03/definitions-key-measures.png\" alt=\"Esempio APQC di Process Definitions and Key Measures con definizione del Process Group 4.3, KPI suggeriti e definizione del Process 4.3.1\" data-caption=\"Esempio di definizioni e misure collegate alla gerarchia PCF.\"><figcaption>Definitions and Key Measures: definizione, KPI suggeriti e processo di livello inferiore nello stesso ramo della gerarchia.</figcaption></figure>",
   "I dati comparativi associati ai KPI possono essere consultati negli strumenti di benchmarking APQC. Il codice del processo e l'identificativo della metrica garantiscono che organizzazioni diverse confrontino lo stesso perimetro di lavoro.",
  ],f"Per ogni dominio, <code>esempi-apqc/&lt;dominio&gt;/processo.md</code> riporta la collocazione PCF completa (Category → Process Group → Process → Activity) con i codici numerici originali. I collegamenti interni aprono la scheda Markdown e il diagramma BPMN del dominio:<br>{pcf_domain_links()}<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch03/camunda-process-customer-service.png\" alt=\"Camunda Modeler con il processo APQC 6.2.2 Manage customer service problems, requests, and inquiries aperto e selezionato\" data-caption=\"Figura M03.06 — Processo APQC aperto in Camunda Modeler.\"><figcaption>Figura M03.06 — Esempio di processo APQC caricato e visualizzato in Camunda Modeler.</figcaption></figure>"),
  (1,"4 Laboratorio",[
   "Scegliere un processo della propria organizzazione e collocarlo nei primi tre livelli del PCF, usando la tabella dei sette domini come riferimento. Motivare la scelta della Category e del Process Group in due righe.",
   "Registrare sia il codice gerarchico sia l'identificativo univoco del Process scelto. Consultare quindi il documento Definitions and Key Measures della Category per confrontare la definizione ufficiale con il perimetro del processo aziendale e selezionare almeno un KPI pertinente.",
  ],None),
 ],
 kt=[
  "Il PCF è una tassonomia gerarchica di processi con codici stabili, pensata per confronto e miglioramento.",
  "I cinque livelli sono Category, Process Group, Process, Activity e Task; il Process è l'unità di analisi principale.",
  "Il PCF descrive che cosa fa l'organizzazione, ma non sostituisce una process map o un diagramma del flusso.",
  "Identificativo univoco e codice gerarchico hanno funzioni diverse: il primo mantiene stabile il riferimento, il secondo indica la posizione nel modello.",
  "La versione cross-industry favorisce confronti trasversali; le versioni settoriali approfondiscono il lavoro caratteristico di un'industria.",
  "La collocazione parte dalle finalità del processo, non dai reparti che lo eseguono.",
  "Definitions and Key Measures collega gerarchia, definizioni e KPI per rendere confrontabile il perimetro misurato.",
 ]),

"03": dict(
 sections=[
  (1,"1 Il livello Activity",[
   "Nel Process Classification Framework di APQC, l'<strong>Activity</strong> è il quarto livello della gerarchia: descrive un'area di lavoro concreta che contribuisce a completare un Process e produce un risultato intermedio riconoscibile. La gerarchia va dalla Category al Process Group, al Process e infine alle Activity; il livello Task, quando serve per descrivere l'esecuzione locale, viene definito dall'organizzazione. Questa distinzione è coerente con l'<a href=\"https://www.apqc.org/resource-library/resource-listing/introduction-apqcs-process-classification-framework-pcf\" target=\"_blank\" rel=\"noopener noreferrer\">Introduzione APQC al PCF</a> e con le <a href=\"https://www.apqc.org/process-frameworks/pcf-faqs\" target=\"_blank\" rel=\"noopener noreferrer\">FAQ sul PCF</a>.",
   "Un'Activity risponde alla domanda <em>quale risultato operativo deve essere prodotto per completare il processo?</em>, senza descrivere ancora ogni clic, controllo o gesto dell'operatore. Per esempio, nel Process APQC 6.2.2 <em>Manage customer service problems, requests, and inquiries</em>, «Analyze problems, requests, and inquiries» identifica il lavoro di analisi della richiesta; classificazione, verifica dello storico, controllo dello SLA e assegnazione sono possibili Task locali che rendono eseguibile quell'Activity.",
   "Il nome dell'Activity usa di norma un verbo e un oggetto: il verbo indica l'azione o il risultato atteso, l'oggetto delimita ciò su cui si interviene. Il nome non va confuso con una procedura aziendale: organizzazioni diverse possono svolgere la stessa Activity con ruoli, sistemi, documenti e livelli di automazione differenti. L'<a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN Reference di Camunda</a> aiuta a rappresentare poi questi passi in un diagramma, ma la classificazione APQC e il modello BPMN hanno scopi diversi.",
   "La relazione tra i livelli può essere letta come una progressiva riduzione del perimetro: la Category raggruppa un dominio, il Process Group raccoglie processi affini, il Process delimita un risultato end-to-end, l'Activity identifica un blocco di lavoro e i Task descrivono le azioni osservabili necessarie per completarlo.",
  ],None),
  (2,"1.1 Definizione secondo il PCF",[
   "Ogni Process del PCF è scomposto in un insieme di Activity correlate. L'elenco APQC è un <strong>modello di classificazione e confronto</strong>, non una procedura obbligatoria né una sequenza BPMN già pronta: l'organizzazione può eseguire le Activity in un ordine diverso, accorparne alcune, introdurre attività locali o non applicare quelle non pertinenti, mantenendo il riferimento al codice originale.",
   "Per descrivere correttamente un'Activity conviene documentare almeno: <strong>perimetro</strong> (dove inizia e dove termina), <strong>risultato</strong> prodotto, <strong>input</strong> necessari, <strong>ruolo o sistema</strong> responsabile, principali <strong>regole e decisioni</strong>, output consegnato all'Activity successiva e condizioni di eccezione. Questi campi trasformano un'etichetta tassonomica in una base utile per la successiva analisi del lavoro.",
   "L'Activity non implica necessariamente un singolo rettangolo BPMN. Può essere rappresentata da una sequenza di Task, da un sotto-processo o da un gruppo di elementi distribuiti tra più corsie. In BPMN un <em>task</em> è un'attività atomica del diagramma, mentre un <em>sub-process</em> contiene un dettaglio ulteriore: la corrispondenza tra Activity APQC e costrutti BPMN va quindi decisa in base al livello di dettaglio richiesto.",
   "Nel metamodel BPMN, <strong>Activity</strong> è il termine generale per un lavoro eseguito nel flusso. Le principali specializzazioni sono <strong>Task</strong> (unità di lavoro atomica), <strong>Sub-Process</strong> (attività composta da un flusso interno), <strong>Call Activity</strong> (invocazione di un processo o di un global task riusabile) e <strong>Transaction</strong>. La Transaction non è un quarto contenitore indipendente: è un Sub-Process con protocollo transazionale e doppio bordo, usato quando le attività devono concludersi con accordo completo oppure essere annullate. La BPMN Reference di Camunda elenca inoltre l'<strong>Event Sub-Process</strong> come variante attivata da un evento.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch04/bpmn-activity-hierarchy.svg\" alt=\"Schema Mermaid della gerarchia BPMN: Activity al vertice, con Task, Sub-Process e Call Activity; dal Sub-Process derivano Transaction ed Event Sub-Process\" data-caption=\"Gerarchia concettuale BPMN delle Activities.\"><figcaption>In BPMN Activity è il concetto generale; Transaction ed Event Sub-Process sono varianti del Sub-Process.</figcaption></figure>",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Tipo BPMN</th><th>Icona dalla <a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN Reference</a></th><th>Uso principale</th></tr></thead><tbody><tr><td><strong>Task</strong></td><td><img class=\"zoomable\" src=\"../assets/images/ch04/bpmn-activity-task.svg\" alt=\"Icona BPMN Task\" style=\"max-width:180px;max-height:90px\"></td><td>Unità atomica di lavoro svolta da una persona, da un'applicazione o da entrambi.</td></tr><tr><td><strong>Sub-Process</strong></td><td><img class=\"zoomable\" src=\"../assets/images/ch04/bpmn-activity-subprocess.svg\" alt=\"Icona BPMN Sub-Process\" style=\"max-width:180px;max-height:90px\"></td><td>Raggruppa un flusso interno e consente di nascondere o espandere il dettaglio.</td></tr><tr><td><strong>Call Activity</strong></td><td><img class=\"zoomable\" src=\"../assets/images/ch04/bpmn-activity-call-activity.svg\" alt=\"Icona BPMN Call Activity\" style=\"max-width:180px;max-height:90px\"></td><td>Richiama un processo o un global task definito e riusabile.</td></tr><tr><td><strong>Transaction</strong></td><td><img class=\"zoomable\" src=\"../assets/images/ch04/bpmn-activity-transaction.svg\" alt=\"Icona BPMN Transaction\" style=\"max-width:180px;max-height:90px\"></td><td>Sub-Process con protocollo di accordo o annullamento tra le parti.</td></tr><tr><td><strong>Event Sub-Process</strong></td><td><img class=\"zoomable\" src=\"../assets/images/ch04/bpmn-activity-event-subprocess.svg\" alt=\"Icona BPMN Event Sub-Process\" style=\"max-width:180px;max-height:90px\"></td><td>Flusso interno attivato da un evento, eventualmente in modalità interrupting o non-interrupting.</td></tr></tbody></table></div>",
   "Una traccia operativa è: (1) leggere il verbo e l'oggetto APQC; (2) verificare l'output che chiude l'Activity; (3) individuare chi la esegue e quali sistemi usa; (4) elencare i Task osservabili; (5) modellare il flusso con eventi, gateway, corsie e Task BPMN; (6) controllare che il diagramma non allarghi il perimetro del codice PCF.",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Livello</th><th>Domanda</th><th>Output della descrizione</th></tr></thead><tbody><tr><td><strong>Process</strong></td><td>Quale risultato end-to-end deve essere ottenuto?</td><td>Confine del processo, cliente e risultato complessivo.</td></tr><tr><td><strong>Activity</strong></td><td>Quale blocco di lavoro contribuisce al risultato?</td><td>Risultato intermedio, input/output e responsabilità principale.</td></tr><tr><td><strong>Task</strong></td><td>Quale azione osservabile viene eseguita?</td><td>Passo operativo con esecutore, regola ed esito verificabile.</td></tr></tbody></table></div>",
   "Per la terminologia grafica e la distinzione tra attività atomiche e sotto-processi si può consultare la <a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN Reference</a>; per la costruzione del primo diagramma online è disponibile la guida Camunda <a href=\"https://docs.camunda.io/docs/components/modeler/web-modeler/modeling/model-your-first-diagram/\" target=\"_blank\" rel=\"noopener noreferrer\">Model your first diagram</a>.",
  ],None),
  (2,"1.2 SIPOC: fornitori, input, processo, output e clienti",[
   "Poiché input e output aiutano a delimitare un'Activity, è utile introdurre il <strong>SIPOC</strong>, acronimo di <em>Suppliers, Inputs, Process, Outputs, Customers</em>. Secondo la definizione dell'<a href=\"https://asq.org/quality-resources/sipoc\" target=\"_blank\" rel=\"noopener noreferrer\">American Society for Quality (ASQ)</a>, è uno strumento di raccolta dati che offre una vista ad alto livello dei fornitori, degli ingressi, delle macro-fasi, dei risultati e dei destinatari di un processo. Si compila dopo aver fissato i confini — evento di avvio e risultato finale — e prima di costruire il flusso dettagliato: il Process contiene in genere poche macro-fasi, non l'elenco dei Task.",
   "Un SIPOC consente di verificare che ogni input abbia un fornitore, che ogni output abbia un cliente e che il perimetro del processo sia condiviso dagli stakeholder. Supplier e Customer possono essere interni o esterni; Input e Output possono essere materiali, documenti, dati, decisioni o servizi. Non sostituisce la scheda Activity né il diagramma BPMN: li prepara, rendendo espliciti gli scambi ai bordi del processo.",
   "<strong>Esempio dalla scheda APQC Category 6.0 — Manage Customer Service.</strong> Per il Process <code>6.2.2</code> <em>Manage customer service problems, requests, and inquiries</em>, la scheda già preparata identifica il trigger nella ricezione di una richiesta, problema o quesito del cliente e l'output nella risposta fornita, con eventuale opportunità di upsell trasmessa alle vendite:",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch04/sipoc-customer-service.svg\" alt=\"Diagramma SIPOC del processo APQC 6.2.2 con le colonne Supplier, Input, Process, Output e Customer\" data-caption=\"Diagramma SIPOC del customer service APQC 6.2.2.\"><figcaption>Diagramma SIPOC costruito sulla scheda del processo APQC Category 6.0: le cinque colonne mostrano gli scambi end-to-end prima del dettaglio dei Task.</figcaption></figure>",
  ],None),
  (2,"1.3 Leggere codice e identificativo",[
   "Una voce APQC può presentarsi come «<code>6.2.2.2</code> Analyze problems, requests, and inquiries (<code>13482</code>)». Il codice gerarchico <code>6.2.2.2</code> si legge da sinistra a destra: <code>6.0</code> Category <em>Manage Customer Service</em>, <code>6.2</code> Process Group <em>Plan and manage customer service contacts</em>, <code>6.2.2</code> Process <em>Manage customer service problems, requests, and inquiries</em>, <code>6.2.2.2</code> Activity. Il codice descrive quindi la <strong>posizione</strong> nell'albero.",
   "Il numero tra parentesi, <code>13482</code>, è l'<strong>identificativo univoco APQC</strong>. Non è un livello aggiuntivo e non sostituisce il codice gerarchico: serve a citare la stessa voce in documenti, fogli Excel, strumenti di benchmarking e versioni del framework anche quando il testo o la posizione vengono aggiornati. Nei materiali conviene riportare sempre entrambi, per esempio <code>6.2.2.2 (13482)</code>.",
   "Codice gerarchico e identificativo hanno quindi funzioni diverse:",
   "<ul class=\"study-bullets\"><li><strong>codice gerarchico</strong>: mostra il ramo e il livello della voce; permette di capire da quale Category, Process Group e Process discende;</li><li><strong>identificativo univoco</strong>: fornisce un riferimento stabile alla definizione APQC e facilita ricerca, confronto e tracciabilità;</li><li><strong>nome</strong>: rende leggibile il contenuto, ma può essere tradotto o adattato senza perdere il riferimento numerico.</li></ul>",
   "Il codice PCF non è un identificativo BPMN. Nel diagramma Camunda ogni elemento ha un proprio ID tecnico XML e un nome visualizzato; l'ID BPMN serve al motore e agli strumenti di modellazione, mentre il codice APQC serve a classificare il lavoro. È buona pratica riportare il codice APQC nel nome, nella documentazione o nelle proprietà del modello, senza confondere i due sistemi di identificazione.",
   "La lettura del codice consente infine di controllare la coerenza del modello: un Task locale dovrebbe essere collegato a una Activity, l'Activity a un Process e il Process al ramo PCF corretto. Se un diagramma contiene attività che non possono essere ricondotte al perimetro di <code>6.2.2.2</code>, occorre dichiarare se si tratta di un'eccezione, di un'attività di supporto o di un altro Process.",
  ],None),
  (1,"2 Il livello Task",[
   "Il <strong>Task</strong> è un'unità di lavoro elementare: descrive un'azione che può essere assegnata a un esecutore, osservata e conclusa con un risultato verificabile. Nel PCF APQC il Task è il dettaglio operativo che l'organizzazione aggiunge sotto una Activity; in BPMN è anche un elemento grafico e semantico del diagramma, rappresentato da un rettangolo arrotondato.",
   "Un Task deve chiarire almeno <strong>chi o che cosa</strong> esegue il lavoro, <strong>quale input</strong> utilizza, <strong>quale trasformazione</strong> compie e <strong>quale output</strong> rende disponibile. L'esecutore può essere una persona, un'applicazione o una combinazione dei due. Il termine italiano <em>attività</em> è quindi ambiguo: nel PCF indica il livello tassonomico Activity, mentre in BPMN Activity è la super-classe che comprende Task e Sub-Process.",
   "La BPMN Reference distingue i Task generici dai Task tipizzati. Il tipo non serve a rendere il disegno più dettagliato in modo ornamentale: comunica il meccanismo previsto per eseguire o coordinare il lavoro. Per esempio, una richiesta di approvazione svolta da una persona è un <em>User Task</em>; l'invio automatico di una notifica è un <em>Service Task</em> o un <em>Send Task</em>, a seconda che si rappresenti l'elaborazione automatica o l'atto di invio del messaggio.",
   "Il PCF e BPMN restano complementari: il codice APQC collega il Task locale all'Activity e al Process; il tipo BPMN descrive come quel passo entra nel flusso e chi lo esegue. Un'Activity APQC può quindi essere scomposta in più Task BPMN, anche di tipi diversi, senza pretendere una corrispondenza uno-a-uno.",
  ],None),
  (2,"2.1 Perché il PCF si ferma alla Activity",[
   "Sotto la Activity la variabilità tra organizzazioni diventa troppo alta per una tassonomia cross-industry. La stessa Activity può essere svolta manualmente, con un ERP, con un portale self-service, con un servizio integrato o con una combinazione di questi strumenti. Può inoltre cambiare il ruolo responsabile, la sequenza dei controlli, il livello di autorizzazione e la granularità dei passi.",
   "Fissare i Task nel PCF renderebbe il framework rigido e poco riusabile: APQC manterrebbe una procedura locale al posto di un riferimento comune. La separazione mantiene stabile la parte condivisa e lascia all'organizzazione la definizione delle azioni, delle regole, delle eccezioni, dei sistemi e delle evidenze da registrare.",
   "La tipizzazione BPMN non contraddice questa scelta. Un <em>User Task</em> o un <em>Service Task</em> è una decisione di modellazione della soluzione corrente, non una nuova voce APQC. Se la soluzione cambia — per esempio un'approvazione passa da un operatore a una regola automatica — il codice Activity può restare lo stesso, mentre cambia il tipo BPMN e cambiano ruoli, dati e KPI da verificare.",
   "Per mantenere la tracciabilità, la scheda dovrebbe riportare il codice e il nome dell'Activity APQC, l'elenco dei Task locali, il tipo BPMN scelto, l'esecutore, l'output e la motivazione della scomposizione. In questo modo il dettaglio operativo può evolvere senza perdere il collegamento al framework.",
  ],None),
  (2,"2.2 Criteri per individuare Task elementari",[
   "Un Task è ben definito quando ha un <strong>esecutore prevalente</strong>, un <strong>input riconoscibile</strong>, un <strong>esito verificabile</strong> e una durata breve rispetto alla Activity. La sua formulazione dovrebbe iniziare con un verbo osservabile — ricevere, validare, classificare, approvare, inviare, registrare — e indicare l'oggetto su cui si interviene.",
   "Per testare la granularità si possono porre sei domande: (1) il passo ha un solo responsabile o un sistema chiaramente identificato? (2) produce un risultato che può essere controllato? (3) richiede una sola decisione principale? (4) usa un insieme coerente di input e strumenti? (5) può essere misurato con un tempo, un esito o un errore? (6) l'eventuale eccezione ha un punto di uscita riconoscibile? Se le risposte sono negative, il passo è probabilmente troppo grande o troppo vago.",
   "Se un presunto Task richiede più ruoli, più decisioni indipendenti o due risultati distinti, va scomposto ulteriormente. Se due passi si eseguono sempre insieme, con lo stesso esecutore e senza un controllo intermedio utile, possono essere accorpati. La scomposizione non deve però arrivare al gesto fisico o al clic sullo schermo: il livello corretto è quello che rende il lavoro assegnabile, misurabile e modellabile.",
   "La scelta del tipo BPMN va fatta dopo aver definito il lavoro: <strong>human</strong> indica un lavoro affidato a una persona e in BPMN corrisponde normalmente a <em>User Task</em>; <strong>manuale</strong> indica un lavoro umano non gestito dal motore e corrisponde a <em>Manual Task</em>; <strong>automatico</strong> è un termine descrittivo, non un tipo unico, e può essere rappresentato da <em>Service Task</em>, <em>Script Task</em> o <em>Business Rule Task</em>.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch04/bpmn-task-types.svg\" alt=\"Tavola ufficiale Camunda dei tipi di BPMN Task: undefined, manual, user, receive, send, script, service e business rule\" data-caption=\"Tipi BPMN di Task.\"><figcaption>Tipi di Task nella <a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN Reference di Camunda</a>: la tavola ufficiale raccoglie i simboli per lavoro manuale, umano, messaggi, script, servizi e regole.</figcaption></figure>",
   "<div class=\"table-wrap\"><table class=\"pcf-table task-types-table\"><thead><tr><th>Tipo BPMN</th><th>Significato operativo</th><th>Esempio nel customer service</th></tr></thead><tbody><tr><td><strong>Task generico</strong></td><td>Unità di lavoro non ancora tipizzata; utile nelle fasi iniziali o quando il meccanismo di esecuzione non è deciso.</td><td>Valutare la richiesta, prima di decidere se sarà svolta da operatore o sistema.</td></tr><tr><td><strong>User Task / human task</strong></td><td>Lavoro eseguito da una persona, normalmente attraverso una lista di lavoro o una form; in Camunda può essere collegato a una form di approvazione o raccolta dati.</td><td>Classificare la richiesta e approvare un'eventuale escalation.</td></tr><tr><td><strong>Manual Task</strong></td><td>Lavoro umano svolto fuori dal motore e senza una gestione automatica della worklist; serve a documentare un passaggio fisico o organizzativo.</td><td>Contattare telefonicamente il cliente e annotare l'esito in un sistema esterno.</td></tr><tr><td><strong>Service Task / automatico</strong></td><td>Invoca un servizio, connettore o job worker per eseguire un'operazione automatica.</td><td>Creare o aggiornare il ticket nel CRM e recuperare lo storico cliente.</td></tr><tr><td><strong>Script Task</strong></td><td>Esegue uno script definito nel processo per una trasformazione o una piccola elaborazione.</td><td>Normalizzare il codice della richiesta o calcolare una priorità tecnica.</td></tr><tr><td><strong>Business Rule Task</strong></td><td>Valuta una regola o una decisione, spesso tramite una decision table DMN.</td><td>Determinare se la richiesta rientra nello SLA o richiede escalation.</td></tr><tr><td><strong>Send Task</strong></td><td>Invia un messaggio a un partecipante o sistema esterno.</td><td>Inviare al cliente la risposta oppure trasmettere il lead al team Vendite.</td></tr><tr><td><strong>Receive Task</strong></td><td>Attende la ricezione di un messaggio; il processo resta in attesa fino all'evento previsto.</td><td>Attendere la risposta del cliente o la conferma del team Vendite.</td></tr></tbody></table></div>",
   "La distinzione tra User Task e Manual Task è importante: entrambi coinvolgono una persona, ma solo il primo è normalmente gestito come lavoro assegnabile nel motore e può essere associato a una form. Send e Receive Task modellano invece la comunicazione; Service, Script e Business Rule Task modellano forme diverse di automazione. La scelta deve riflettere il comportamento reale e non soltanto l'aspetto grafico del diagramma.",
   "Nel caso di un <strong>human task</strong>, la form è l'interfaccia con cui l'utente legge le istruzioni, inserisce o modifica dati e comunica l'esito del lavoro. In un flusso di approvazione può contenere, per esempio, un campo decisione <em>approvato/rifiutato</em>, commenti e allegati: la sottomissione della form completa il User Task, registra le variabili di processo e consente al gateway o al passo successivo di avanzare sul ramo corretto. Finché l'utente non completa il task, l'istanza resta in attesa.",
   "Un esempio ufficiale è la user task <em>Configure</em> della documentazione Camunda: la task viene collegata a una Camunda Form tramite un <code>formId</code>, può essere assegnata a un utente o a un gruppo e, una volta completata in Tasklist, restituisce i dati al processo. Si può consultare l'esempio XML nella guida <a href=\"https://docs.camunda.io/docs/components/modeler/bpmn/user-tasks/\" target=\"_blank\" rel=\"noopener noreferrer\">User tasks</a> e la guida alla <a href=\"https://docs.camunda.io/docs/components/modeler/forms/utilizing-forms/\" target=\"_blank\" rel=\"noopener noreferrer\">creazione di Camunda Forms</a>. La form può essere collegata al modello e visualizzata in Tasklist oppure gestita da un'applicazione personalizzata.",
  ],None),
  (1,"3 Orchestrare task automatici e human task",[
   "Quando un processo alterna attività automatiche e lavoro umano, il problema non è soltanto disegnare la sequenza: occorre coordinare tempi, assegnazioni, dati, attese, esiti ed eccezioni. Un motore di workflow deve avviare il task automatico, fermarsi quando serve l'intervento umano, rendere disponibile il lavoro alla persona corretta e riprendere il flusso con i dati restituiti.",
   "Il caso Salesforce Flow Orchestration mostra una soluzione concreta. Una <strong>orchestration</strong> coordina fasi e passi: gli <em>interactive steps</em> richiedono intervento dell'utente e generano un work item, mentre i <em>background steps</em> eseguono flow automatici senza interazione. I passi possono essere sequenziali o concorrenti; le fasi raggruppano i passi e definiscono quando una fase è completata.",
   "Salesforce espone due viste operative distinte. <strong>Orchestration Runs</strong> serve al supervisore per monitorare le istanze in corso, lo stato, la data e l'autore; da una run in corso è possibile intervenire, per esempio annullando o eseguendo il debug. <strong>Orchestration Work Items</strong> raccoglie invece i lavori assegnati agli utenti, con stato, record di contesto, passo e assegnatario. La distinzione separa il controllo dell'istanza end-to-end dal lavoro da svolgere su un singolo passo.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch04/salesforce-orchestration-runs.png\" alt=\"Salesforce Flow Orchestration Runs: elenco delle istanze con nome, stato, autore, data di creazione e ultima modifica\" data-caption=\"Salesforce Flow Orchestration Runs.\"><figcaption>Salesforce Flow Orchestration — vista <em>Orchestration Runs</em>: monitoraggio delle istanze dell'orchestrazione. Fonte: <a href=\"https://trailhead.salesforce.com/content/learn/modules/orchestrator-basics/get-to-know-orchestrator\" target=\"_blank\" rel=\"noopener noreferrer\">Trailhead, Get to Know Flow Orchestration</a>.</figcaption></figure>",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch04/salesforce-orchestration-work-items.png\" alt=\"Salesforce Flow Orchestration Work Items: elenco dei lavori con data, nome, stato, record di contesto, passo e assegnatario\" data-caption=\"Salesforce Flow Orchestration Work Items.\"><figcaption>Salesforce Flow Orchestration — vista <em>Orchestration Work Items</em>: lavori assegnati agli utenti. Fonte: <a href=\"https://trailhead.salesforce.com/content/learn/modules/orchestrator-basics/get-to-know-orchestrator\" target=\"_blank\" rel=\"noopener noreferrer\">Trailhead, Get to Know Flow Orchestration</a>.</figcaption></figure>",
   "Il <strong>Work Guide</strong> Salesforce è il punto di lavoro dell'utente: un componente inserito nella pagina del record mostra il lavoro interattivo e consente di completarlo senza cambiare strumento. È concettualmente simile alla Camunda Form collegata a un User Task: entrambi raccolgono dati e un esito umano, aggiornano le variabili e fanno avanzare il processo; cambiano però il prodotto, il modello di assegnazione e il contesto applicativo.",
   "La lezione progettuale è separare tre responsabilità: l'orchestratore controlla lo stato dell'istanza e le dipendenze; il task automatico esegue una trasformazione o integrazione; il work item/human task raccoglie una decisione o un dato dalla persona. Un modello è completo quando esplicita anche timeout, riassegnazione, errore, rifiuto e percorso di compensazione.",
  ],None),
  (1,"4 Schede di processo PCF completate",[
   "Le sette schede di processo APQC già sviluppate applicano lo stesso percorso: collocazione Category → Process Group → Process → Activity, scomposizione didattica in Task, SIPOC, matrice delle variabili, KPI e diagramma BPMN.",
   "<ul class=\"study-bullets\"><li><a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/01-vision-strategy/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\"><strong>Visione e strategia</strong> — Assess the external environment (1.1.1)</a> (<a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/01-vision-strategy/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN</a>)</li><li><a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/02-vendite/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\"><strong>Vendite</strong> — Develop sales forecast (3.4.1)</a> (<a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/02-vendite/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN</a>)</li><li><a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/03-acquisti/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\"><strong>Acquisti</strong> — Select suppliers and develop/maintain contracts (4.2.3)</a> (<a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/03-acquisti/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN</a>)</li><li><a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/04-servizi/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\"><strong>Servizi</strong> — Create and manage resource plan (5.2.2)</a> (<a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/04-servizi/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN</a>)</li><li><a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/05-customer-service/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\"><strong>Customer Service</strong> — Manage customer service problems, requests, and inquiries (6.2.2)</a> (<a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/05-customer-service/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN</a>)</li><li><a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/06-it/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\"><strong>IT</strong> — Operate IT user support (8.7.8)</a> (<a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/06-it/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN</a>)</li><li><a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/07-finance/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\"><strong>Finance</strong> — Invoice customer (9.2.2)</a> (<a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/07-finance/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN</a>)</li></ul>",
   "Le schede Markdown sono il riferimento testuale; i file BPMN sono diagrammi di rappresentazione, apribili con Camunda Modeler e non configurati per l'esecuzione.",
  ],None),
  (1,"5 Caso SAEM: schede e materiali risolti",[
   "Il caso SAEM applica lo stesso schema a processi reali, con ruoli, sistemi, criticità e dati documentati. La pagina del <a href=\"../caso-studio-saem.html\">caso di studio SAEM</a> raccoglie il quadro aziendale, la mappatura APQC, le fonti e lo stato delle elaborazioni.",
   "<ul class=\"study-bullets\"><li><strong>Gestione ordine telematico</strong> — <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/esempi-apqc/02-gestione-ordine/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\">scheda processo</a>, <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/esempi-apqc/02-gestione-ordine/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">diagramma BPMN</a> e <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/ROADMAP-DIAGRAMMI.md\" target=\"_blank\" rel=\"noopener noreferrer\">roadmap dei diagrammi</a>;</li><li><strong>Selezione e qualifica fornitori</strong> — <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/esempi-apqc/03-acquisti/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\">scheda processo</a> e <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/esempi-apqc/03-acquisti/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">diagramma BPMN</a>;</li><li><strong>Customer service: ritiro, resi e riparazione</strong> — <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/esempi-apqc/05-customer-service/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\">scheda processo</a> e <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/esempi-apqc/05-customer-service/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">diagramma BPMN</a>;</li><li><strong>Fatturazione settimanale</strong> — <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/esempi-apqc/07-finance/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\">scheda processo</a> e <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/esempi-apqc/07-finance/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">diagramma BPMN</a>.</li></ul>",
   "Per seguire l'evoluzione dei requisiti e delle fonti sono disponibili anche la <a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/caso-saem-compresso.md\" target=\"_blank\" rel=\"noopener noreferrer\">sintesi didattica del caso</a> e l'<a href=\"https://github.com/thimotyb/corso-processi/blob/main/caso-saem/ROADMAP-DIAGRAMMI.md\" target=\"_blank\" rel=\"noopener noreferrer\">inventario/roadmap dei diagrammi</a>.",
  ],None),
  (1,"6 Laboratorio",[
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
   "Le variabili di processo sono le grandezze osservabili che descrivono come un processo trasforma un input in un output. Rendono espliciti il perimetro del lavoro, le risorse assorbite, le condizioni operative e i risultati ottenuti. Servono a caratterizzare il processo, confrontarlo nel tempo o tra unità diverse e individuare interventi di miglioramento basati su evidenze.",
   "L'approccio per processi di <a href=\"https://www.iso.org/iso/iso9001_2015_process_approach.pdf\" target=\"_blank\" rel=\"noopener noreferrer\">ISO 9001</a> invita a identificare input, output, sequenza e interazioni, criteri di controllo, risorse, responsabilità, rischi e opportunità. La prospettiva di <em>Business Modeling with UML</em> di Eriksson e Penker aggiunge la lettura del processo come trasformazione orientata a un obiettivo e sottoposta a vincoli e controlli.",
   "Nel corso la tassonomia è una sintesi operativa: non è una classificazione ufficiale APQC, ma una griglia comune per leggere le schede dei processi e collegare descrizione, analisi e misurazione.",
  ],None),
  (2,"1.1 Input e output",[
   "Gli <strong>input</strong> sono gli elementi necessari per avviare o svolgere il processo: dati, documenti, richieste, materiali, autorizzazioni, disponibilità di una risorsa o risultato di un processo precedente. Per ogni input è utile indicare il fornitore, il formato, il momento di disponibilità e i controlli di completezza o qualità.",
   "Gli <strong>output</strong> sono i risultati prodotti e consegnati a un cliente interno o esterno: una risposta, un ordine confermato, una decisione, un documento, un servizio o un'opportunità commerciale. Un output è descritto bene quando sono chiari destinatario, contenuto, criterio di accettazione e momento di consegna.",
   "La distinzione input/output deve essere osservata dal punto di vista del processo analizzato: lo stesso oggetto può essere output di un processo e input di quello successivo. Il collegamento tra i due estremi permette di verificare se il processo risponde davvero al bisogno del cliente e costituisce la base per SIPOC, KPI e analisi delle interazioni.",
  ],None),
  (2,"1.2 Tempi, costi, volumi",[
   "Il <strong>tempo</strong> va distinto almeno in tempo di attraversamento (dall'innesco alla chiusura), tempo di lavorazione e tempo di attesa. La distinzione rende visibili code, passaggi autorizzativi e dipendenze esterne: un'attività che richiede dieci minuti può produrre un lead time di un giorno se l'output resta in attesa di stampa, firma o disponibilità.",
   "Il <strong>costo</strong> comprende le risorse direttamente impiegate e, quando rilevante, una quota dei costi indiretti: ore delle persone, sistemi e licenze, materiali, rilavorazioni, trasferte ed errori. È importante dichiarare il perimetro del calcolo e distinguere costo per istanza da costo del periodo.",
   "Il <strong>volume</strong> indica quante istanze, richieste, righe o transazioni vengono gestite in un intervallo. Va associato a una frequenza e, se necessario, alla distribuzione nel tempo: la media mensile può nascondere picchi giornalieri che generano sovraccarico e tempi di attesa.",
   "Tempo, costo e volume si interpretano insieme: un aumento dei volumi può ridurre il costo unitario grazie alle economie di scala, ma può anche aumentare il lead time se la capacità non cresce; una rilavorazione aumenta contemporaneamente costo e tempo senza produrre valore per il cliente.",
  ],None),
  (2,"1.3 Ruoli, sistemi, vincoli, rischi",[
   "I <strong>ruoli</strong> identificano chi esegue, approva, fornisce informazioni o riceve l'output. È utile distinguere ruolo organizzativo, persona o team, responsabilità decisionale e responsabilità operativa; una matrice RACI può dettagliare la relazione tra attività e attori.",
   "I <strong>sistemi</strong> sono applicativi, archivi, canali e strumenti che registrano dati o supportano l'esecuzione: CRM, ticketing, ERP, posta elettronica, portali e knowledge base. Per ciascun sistema si osservano dati inseriti, dati letti, integrazioni e passaggi manuali.",
   "I <strong>vincoli</strong> sono condizioni da rispettare: SLA, normative, privacy, autorizzazioni, finestre temporali, budget, capacità, regole commerciali o dipendenze da fornitori. Un vincolo può introdurre un controllo necessario, ma anche un'attesa o un costo aggiuntivo.",
   "I <strong>rischi</strong> sono eventi o condizioni che possono ridurre qualità, puntualità, conformità o continuità. Vanno collegati alla causa, all'effetto, alla probabilità e alla misura di prevenzione o rilevazione. Un collo di bottiglia è un caso particolare in cui capacità insufficiente o dipendenza da una risorsa concentra la variabilità e crea accumulo.",
  ],None),
  (1,"2 La matrice delle variabili",[
   "La matrice delle variabili traduce la scheda di processo in un quadro compatto e verificabile. Ogni riga rappresenta una famiglia; le colonne distinguono la definizione, il dato osservato, la fonte, il responsabile della rilevazione e le note su rischi o qualità del dato. In questo modo la descrizione narrativa diventa confrontabile tra processi e può alimentare la definizione dei KPI.",
   "La matrice non sostituisce il diagramma BPMN o la scheda: li completa. Il diagramma mostra sequenza e responsabilità, mentre la matrice esplicita condizioni, risorse, grandezze e punti di misura.",
  ],None),
  (2,"2.1 Struttura della matrice",[
   "Le righe minime sono: input, output, tempi, costi, volumi, ruoli, sistemi, vincoli e rischi/colli di bottiglia. Le colonne possono contenere la descrizione, l'esempio concreto, l'unità di misura, la fonte del dato e il proprietario dell'informazione. Per una prima analisi didattica bastano tre colonne: variabile, significato ed evidenza nel processo.",
   "La qualità della matrice dipende dalla granularità: tutte le righe devono riferirsi allo stesso confine di processo, usare termini osservabili e distinguere fatti da ipotesi. Se un valore non è disponibile, si annota esplicitamente \"da rilevare\" invece di inventare una stima.",
  ],None),
  (2,"2.2 Compilazione a partire dalla scheda processo",[
   "La compilazione parte dai confini della scheda: evento di innesco, output finale, ruoli, sistemi, vincoli e rischi. Si leggono poi Activity e Task per ricavare tempi di lavorazione, attese, volumi e punti in cui nasce o si perde un'informazione. Infine si verifica che ogni riga sia sostenuta da una fonte: sistema informativo, documento, intervista, osservazione o dato storico.",
   "L'esempio seguente riprende la matrice già preparata per la Category 6.0 <em>Manage Customer Service</em>, Process 6.2.2 <em>Manage customer service problems, requests, and inquiries</em>. La tabella mostra come una singola scheda APQC venga arricchita con ipotesi operative controllabili e collegamenti a rischi, ruoli e sistemi.",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Variabile</th><th>Descrizione</th><th>Esempio nella Category 6.0 — Manage Customer Service</th></tr></thead><tbody><tr><td><strong>Input</strong></td><td>Dati necessari ad avviare il processo.</td><td>Richiesta, problema o quesito del cliente; storico dei contatti; SLA contrattuali.</td></tr><tr><td><strong>Output</strong></td><td>Risultato consegnato dal processo.</td><td>Richiesta risolta e risposta al cliente; eventuale opportunità di upsell/cross-sell trasmessa alle vendite.</td></tr><tr><td><strong>Tempi</strong></td><td>Durata di lavorazione, attesa e attraversamento.</td><td>Da pochi minuti per una chat a più giorni per problemi complessi, nel rispetto dello SLA.</td></tr><tr><td><strong>Costi</strong></td><td>Risorse economiche assorbite per istanza o periodo.</td><td>Costo per contatto: ore dell'operatore, costo del canale e delle eventuali escalation.</td></tr><tr><td><strong>Volumi</strong></td><td>Quantità e frequenza delle istanze.</td><td>Centinaia o migliaia di contatti al mese, con possibili picchi per canale o periodo.</td></tr><tr><td><strong>Ruoli</strong></td><td>Attori che eseguono, approvano o ricevono il risultato.</td><td>Customer Service Representative; team Vendite per le opportunità commerciali.</td></tr><tr><td><strong>Sistemi</strong></td><td>Applicativi e strumenti che supportano il flusso.</td><td>CRM/ticketing, telefonia o chat, knowledge base.</td></tr><tr><td><strong>Vincoli</strong></td><td>Limiti operativi, contrattuali o normativi.</td><td>SLA, privacy, regole di gestione dei reclami e disponibilità degli specialisti.</td></tr><tr><td><strong>Rischi / colli di bottiglia</strong></td><td>Eventi o punti di accumulo che degradano il risultato.</td><td>Errata classificazione, escalation tardiva, mancato rispetto dello SLA, opportunità non trasmesse alle vendite.</td></tr></tbody></table></div>",
   "La matrice evidenzia anche le lacune: per esempio, \"centinaia o migliaia\" è una descrizione iniziale, non ancora un dato misurato. Il passo successivo è definire fonte, periodo e unità, ad esempio numero di ticket per giorno e percentuale risolta entro SLA.",
  ],None),
  (1,"3 Relazioni tra variabili",[
   "Le variabili non sono indipendenti: cambiare capacità, regole, canali o sistemi modifica tempi, costi, volumi gestibili e qualità degli output. L'analisi delle relazioni consente di formulare ipotesi causa-effetto e di scegliere quali dati osservare prima e dopo un intervento.",
   "Nel caso SAEM, per esempio, la gestione telematica dell'ordine modifica l'attività di inserimento, riduce i passaggi manuali e può ridurre il lead time; l'effetto deve però essere verificato anche su errori di imputazione, carico degli operatori e qualità della conferma.",
  ],None),
  (2,"3.1 Dipendenze, cause, effetti",[
   "Le dipendenze si possono esprimere come catene: <em>causa → variabile intermedia → effetto osservabile</em>. Un aumento dei volumi allunga le code se la capacità resta invariata; un nuovo controllo normativo aumenta il tempo di attraversamento e il costo per istanza; una classificazione errata a monte genera riassegnazioni, escalation e ritardi a valle.",
   "Per rendere la relazione verificabile si indicano almeno il verso atteso, la misura coinvolta e il perimetro temporale. Un'ipotesi come \"più richieste fanno aumentare il tempo\" diventa analizzabile se si confrontano volume giornaliero, coda media e percentile del lead time a parità di canale e SLA.",
  ],None),
  (2,"3.2 Eccezioni e colli di bottiglia",[
   "Le eccezioni sono percorsi alternativi attivati da condizioni specifiche: richiesta incompleta, cliente prioritario, escalation tecnica, opportunità commerciale o indisponibilità di un sistema. Vanno descritte con trigger, ruolo responsabile, output atteso e criterio di rientro nel flusso principale.",
   "Un collo di bottiglia è un punto in cui la capacità disponibile è inferiore alla domanda o dipende da una risorsa difficile da sostituire. I segnali sono coda crescente, tempo di attesa elevato, rilavorazioni e attività che restano bloccate prima di un'approvazione o di un'escalation. Nella Category 6, una classificazione errata o un'escalation tardiva può accumulare ticket e compromettere lo SLA.",
   "La scheda di ogni dominio in <code>esempi-apqc/</code> contiene una matrice già compilata. La si può usare come punto di partenza, aggiungendo poi fonte del dato, frequenza di rilevazione e responsabile della misura.",
  ],None),
  (1,"4 Laboratorio",[
   "Costruire la matrice delle variabili per la Activity scomposta nel Modulo 4. Per ogni riga indicare almeno una fonte del dato e distinguere ciò che è osservato da ciò che deve ancora essere rilevato.",
   "Aggiungere un collo di bottiglia, descriverne causa ed effetto e formulare una relazione tra due variabili. Infine proporre una modifica operativa e specificare quali misure confronterebbero situazione AS-IS e TO-BE.",
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
   "Misurare serve a sapere se il processo raggiunge il suo obiettivo, a confrontarne le prestazioni nel tempo e a decidere dove intervenire con dati anziché con impressioni. Senza misura, il miglioramento non è verificabile: non si distingue un risultato occasionale da una prestazione stabile e non si può controllare se una modifica abbia prodotto l'effetto atteso.",
   "Secondo <a href=\"https://www.apqc.org/blog/what-are-key-performance-indicators-kpis\" target=\"_blank\" rel=\"noopener noreferrer\">APQC</a>, un KPI è una misura specifica che valuta una componente quantificabile della prestazione a livello di organizzazione, funzione, processo o attività. Il KPI deve essere collegato a un obiettivo o a un fattore critico di successo: un numero isolato non è ancora un indicatore utile alla gestione.",
  ],None),
  (2,"1.1 Controllo, confronto, miglioramento",[
   "Il <strong>controllo</strong> verifica che il processo resti entro limiti attesi; il <strong>confronto</strong> mette a paragone periodi, sedi, prodotti o organizzazioni; il <strong>miglioramento</strong> usa la misura come riferimento prima e dopo un intervento. La stessa metrica può quindi servire al controllo operativo e alla valutazione direzionale, purché il perimetro resti esplicito.",
   "Gli indicatori devono essere stabili, definiti in modo univoco e accompagnati da contesto: periodo, volume, popolazione osservata, fonte e soglia. APQC raccomanda di privilegiare misure affidabili, rilevanti per gli obiettivi, osservabili nel tempo, accessibili e familiari agli utilizzatori.",
  ],None),
  (2,"1.2 Efficienza ed efficacia",[
   "L'<strong>efficacia</strong> misura quanto l'output raggiunge il risultato atteso e soddisfa il cliente: tempestività, qualità, completezza, rispetto dello SLA. L'<strong>efficienza</strong> misura quante risorse servono per produrlo: costo unitario, tempo di lavorazione, produttività, automazione e rilavorazioni.",
   "Un processo può essere efficace ma inefficiente, per esempio quando risolve ogni richiesta ma impiega troppe ore; oppure efficiente ma inefficace, quando chiude rapidamente casi senza risolvere il problema. Un set equilibrato deve quindi includere indicatori di risultato e indicatori diagnostici, evitando di ottimizzare una dimensione a scapito dell'altra.",
   "<a href=\"https://www.apqc.org/What-Are-the-Best-Metrics-to-Measure-Process-Performance\" target=\"_blank\" rel=\"noopener noreferrer\">APQC</a> raggruppa le misure di processo in quattro famiglie: efficacia dei costi, produttività del personale, efficienza del processo e tempo di ciclo. La scelta va adattata all'obiettivo e ai confini del processo.",
  ],None),
  (1,"2 Definire un KPI",[
   "Un KPI è una misura scelta perché rappresentativa di un obiettivo importante del processo. Va definito in modo che due persone diverse, con gli stessi dati e lo stesso perimetro, ottengano lo stesso valore e sappiano quale decisione supporta.",
   "È utile distinguere tre termini: una <strong>misura</strong> è l'osservazione definita della prestazione; una <strong>metrica</strong> è il risultato quantificato della misura, normalmente espresso come numero, percentuale o rapporto; un <strong>KPI</strong> è una misura di rilievo strategico o gestionale scelta per seguire un obiettivo. La distinzione è illustrata da <a href=\"https://www.apqc.org/blog/ask-us-answered-whats-difference-between-kpi-measure-and-metric\" target=\"_blank\" rel=\"noopener noreferrer\">APQC</a>.",
   "La misura deve avere un proprietario, una fonte, una regola di calcolo, una frequenza e una decisione associata. Se nessuno agisce quando il valore cambia, l'indicatore è probabilmente descrittivo ma non ancora un KPI di gestione.",
  ],None),
  (2,"2.1 Formula, unità, frequenza, fonte del dato",[
   "La scheda di un KPI comprende almeno: nome, obiettivo collegato, formula, numeratore e denominatore, unità di misura, perimetro, frequenza, periodo di riferimento, fonte del dato, responsabile, direzione desiderata e regola per i valori mancanti.",
   "La definizione deve chiarire se il tempo è di lavorazione o di attraversamento, se il costo è totale o unitario e se la percentuale usa tutte le istanze o solo quelle chiuse. <a href=\"https://www.iso.org/standard/56847.html\" target=\"_blank\" rel=\"noopener noreferrer\">ISO 22400-1</a> fornisce un quadro terminologico per definire e utilizzare KPI; è orientata alle operations manifatturiere, ma i criteri di chiarezza e composizione sono riutilizzabili come riferimento metodologico.",
   "Senza formula, unità, frequenza e fonte l'indicatore è ambiguo e non confrontabile. Una definizione corretta permette di ricostruire il valore, verificarne la qualità e confrontare AS-IS e TO-BE sullo stesso perimetro.",
  ],None),
  (2,"2.2 Target e soglie",[
   "Il <strong>target</strong> è il valore atteso; le <strong>soglie</strong> delimitano le fasce di attenzione e di allarme. Target e soglie vanno fissati con un riferimento — storico interno, benchmark esterno, requisito contrattuale, SLA o obiettivo strategico — e riesaminati periodicamente.",
   "La direzione desiderata dipende dall'indicatore: per il tasso di risoluzione più alto è normalmente migliore, mentre per il tempo di attesa o il tasso di errore è migliore un valore più basso. Le soglie devono generare un'azione: analisi della causa, riassegnazione di capacità, escalation o revisione del processo.",
  ],None),
  (2,"2.3 Dal KPI al cruscotto direzionale",[
   "Un cruscotto direzionale è una vista sintetica che permette di monitorare lo stato dell'organizzazione o di un processo e di decidere dove approfondire. Non è il deposito di tutti i dati: mostra pochi indicatori prioritari, il valore corrente, il confronto con il target, il trend e un collegamento al dettaglio.",
   "Le <a href=\"https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips\" target=\"_blank\" rel=\"noopener noreferrer\">linee guida Microsoft per i dashboard</a> raccomandano di considerare il pubblico, raccontare la situazione in una schermata, mettere in evidenza le informazioni più importanti e scegliere la visualizzazione in funzione della domanda. Il <a href=\"https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards\" target=\"_blank\" rel=\"noopener noreferrer\">dashboard Power BI</a> è descritto come una sintesi collegata a report e modelli sottostanti: il cruscotto segnala, il report consente di diagnosticare.",
   "Una struttura didattica efficace comprende: intestazione con periodo e perimetro; schede KPI con valore, target, scostamento e trend; semaforo o soglia per lo stato; grafico di andamento; filtro per dominio o responsabile; link alla scheda processo e alla fonte del dato. L'uso del colore deve essere coerente e non l'unico modo per comunicare lo stato.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch07/power-bi-marketing-sample-dashboard.png\" alt=\"Esempio di dashboard direzionale Power BI Marketing con schede KPI, grafici, filtri e indicatori di andamento\" data-caption=\"Esempio di dashboard direzionale Power BI.\"><figcaption>Esempio di dashboard direzionale Power BI: schede sintetiche, grafici e filtri organizzano indicatori diversi in una vista unica. <a href=\"https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips\" target=\"_blank\" rel=\"noopener noreferrer\">Documentazione Microsoft sui suggerimenti di progettazione</a>.</figcaption></figure>",
   "Il visual KPI di Power BI richiede un valore, un obiettivo e un asse temporale o di trend. La <a href=\"https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-kpi\" target=\"_blank\" rel=\"noopener noreferrer\">documentazione Microsoft sui KPI visuali</a> è un esempio concreto di questa relazione tra valore attuale, target, direzione e distanza dall'obiettivo.",
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
  (2,"3.3 Balanced Scorecard e allineamento strategico",[
   "La <strong>Balanced Scorecard</strong> collega strategia, obiettivi, indicatori, target e iniziative. Il modello di Kaplan e Norton nasce per superare la lettura della performance basata soltanto sui risultati finanziari e propone una vista bilanciata delle dimensioni che creano valore.",
   "Le quattro prospettive tradizionali sono: <strong>finanziaria</strong> (risultati economici e uso delle risorse), <strong>cliente/stakeholder</strong> (valore percepito, soddisfazione, fidelizzazione), <strong>processi interni</strong> (qualità, efficienza, innovazione e tempi) e <strong>apprendimento e crescita</strong> (competenze, persone, tecnologia e capacità organizzativa). Il <a href=\"https://balancedscorecard.org/staging/bsc-basics/articles-videos/the-four-perspectives-of-the-balanced-scorecard/\" target=\"_blank\" rel=\"noopener noreferrer\">Balanced Scorecard Institute</a> descrive le prospettive come lenti complementari per leggere l'organizzazione come sistema.",
   "Per costruire una scorecard si parte da missione e strategia, si definiscono obiettivi per prospettiva, si scelgono pochi KPI, si assegnano target e iniziative e si rendono esplicite le relazioni causa-effetto. Un KPI operativo deve poter risalire a un obiettivo di processo e, quando rilevante, a un obiettivo strategico.",
   "La fonte originaria è l'articolo di <a href=\"https://hbr.org/2005/07/the-balanced-scorecard-measures-that-drive-performance\" target=\"_blank\" rel=\"noopener noreferrer\">Kaplan e Norton su Harvard Business Review</a>. La Balanced Scorecard non sostituisce il cruscotto: definisce la logica strategica e le prospettive; il dashboard presenta in modo operativo i valori e gli scostamenti.",
  ],None),
  (2,"3.4 Il caso SAEM: dall'albero delle determinanti ai KPI",[
   "Nel caso SAEM i KPI non sono scelti come un elenco isolato. Partono da un <strong>albero delle determinanti</strong> che collega la profittabilità di lungo periodo ai risultati strategici, ai fattori critici di successo e infine alle leve operative. A ogni driver vengono associati indicatori capaci di misurarne lo stato e le variazioni. La metrica deve essere intuitiva, comprensibile e calcolabile in modo stabile da chi ne cura la rilevazione.",
   "Il cruscotto aziendale comprendeva già <strong>29 indicatori monitorati periodicamente</strong>. Per analizzare la ridefinizione della gestione ordini sono stati messi in evidenza due indicatori ulteriori, <strong>lead time offerta</strong> e <strong>lead time ordine</strong>, da leggere insieme alla percentuale di errori di imputazione già presente nel sistema qualità. In questo modo la misura collega la strategia del servizio al cliente alle attività concrete di preparazione dell'offerta, inserimento dell'ordine e invio della conferma.",
   "Il primo ramo mostra come gli indicatori economici e commerciali scendano dalla profittabilità verso Market Share, Qualità, Servizio al cliente e Innovatività. Il <strong>ROI</strong> (<em>Return on Investment</em>) misura il rendimento del capitale investito, rapportando il risultato operativo agli investimenti impiegati; il <strong>ROE</strong> (<em>Return on Equity</em>) misura il rendimento del capitale proprio, rapportando l'utile netto al patrimonio netto; il <strong>ROS</strong> (<em>Return on Sales</em>) misura la redditività delle vendite, rapportando il risultato operativo ai ricavi. Insieme descrivono dimensioni diverse della profittabilità; nuovi clienti, clienti persi e quota di mercato osservano il risultato commerciale; reclami, non conformità e valutazioni dei clienti rendono misurabili qualità e servizio.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch07/saem-albero-kpi-parte-1.png\" alt=\"Prima parte dell'albero KPI SAEM: profittabilità, Market Share, gestione magazzino, qualità, servizio al cliente e innovatività con i relativi indicatori\" data-caption=\"Albero delle determinanti e KPI del caso SAEM, parte 1.\"><figcaption>Albero delle determinanti e KPI del caso SAEM, parte 1: dagli obiettivi strategici agli indicatori di mercato, qualità, servizio e innovazione.</figcaption></figure>",
   "Il secondo ramo porta il <strong>Servizio al cliente</strong> ai driver Tempestività e Competenza. La Tempestività viene osservata attraverso l'efficienza dell'evasione ordini, la gestione dei flussi informativi, gli approvvigionamenti e la velocità di gestione delle non conformità. La Competenza viene invece collegata alla formazione. Il disegno mostra quindi che un KPI appartiene a una leva precisa: per esempio, il tempo di risposta alle richieste di informazioni misura la gestione dei flussi informativi, mentre le ore di formazione misurano la capacità che sostiene il servizio.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch07/saem-albero-kpi-parte-2.png\" alt=\"Seconda parte dell'albero KPI SAEM: servizio al cliente, tempestività, competenza, evasione ordini, flussi informativi, approvvigionamenti, non conformità e formazione\" data-caption=\"Albero delle determinanti e KPI del caso SAEM, parte 2.\"><figcaption>Albero delle determinanti e KPI del caso SAEM, parte 2: gli indicatori che misurano tempestività, competenza e attività operative collegate al servizio al cliente.</figcaption></figure>",
   "Il terzo ramo riguarda l'<strong>efficacia della gestione del magazzino</strong>. Rotazione delle scorte ed errori di magazzino misurano il risultato del processo; puntualità delle consegne in entrata e quota di ordini a fornitore in ritardo misurano la logistica in ingresso; non conformità aperte e voto ponderato sugli acquisti supportano rispettivamente la selezione e il monitoraggio dei fornitori.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch07/saem-albero-kpi-parte-3.png\" alt=\"Terza parte dell'albero KPI SAEM: gestione del magazzino, logistica in ingresso, manutenzione, selezione e monitoraggio dei fornitori con i relativi indicatori\" data-caption=\"Albero delle determinanti e KPI del caso SAEM, parte 3.\"><figcaption>Albero delle determinanti e KPI del caso SAEM, parte 3: misure per magazzino, logistica in ingresso e gestione dei fornitori.</figcaption></figure>",
   "L'applicazione dei KPI può essere letta su tre livelli:",
   "<ul class=\"study-bullets\"><li><strong>Attività</strong>: il dato nasce durante un'operazione osservabile, come inserire una riga d'ordine, inviare un'offerta, confermare un ordine o rispondere a una richiesta.</li><li><strong>Processo</strong>: i valori delle singole istanze vengono aggregati per valutare l'efficienza del sottoprocesso di inserimento ordini o del processo di evasione.</li><li><strong>Obiettivo</strong>: il risultato di processo viene ricondotto a tempestività, servizio al cliente, quota di mercato e profittabilità. Il KPI permette quindi di verificare se una modifica operativa produce l'effetto strategico atteso.</li></ul>",
   "<div class=\"table-wrap\"><table class=\"pcf-table saem-kpi-table\"><thead><tr><th>KPI</th><th>Definizione operativa</th><th>Applicazione nel caso SAEM</th></tr></thead><tbody><tr><td><strong>% errori di imputazione ordini</strong></td><td><code>numero errori di imputazione / numero righe delle bolle</code>, espresso in percentuale e rilevato trimestralmente. Target: <code>0%</code>.</td><td>Misura la qualità dell'attività manuale di inserimento delle righe e, per aggregazione, l'efficienza dell'ufficio commerciale. Gli errori riguardano soprattutto quantità e codici articolo; le conversioni manuali delle unità di misura possono generare correzioni, ricircoli e costi. Il valore osservato più recente è <code>0,10%</code>, superiore al livello ottimale dello <code>0,05%</code>.</td></tr><tr><td><strong>Lead time offerta</strong></td><td>Media del tempo fra l'inizio della quotazione e l'invio dell'offerta, espressa in ore e rilevata trimestralmente. Target: risposta immediata.</td><td>Attraversa inserimento degli articoli, eventuale autorizzazione del Direttore Vendite e invio al cliente. Consente di distinguere il tempo di lavorazione dal tempo di attesa: un'offerta media richiede circa dieci minuti di inserimento, ma la stampa e l'invio differiti possono portare il tempo complessivo fino a un giorno.</td></tr><tr><td><strong>Lead time ordine</strong></td><td>Media del tempo fra ricevimento dell'ordine e invio della conferma, espressa in giorni e rilevata trimestralmente sugli ordini che prevedono conferma. Target: risposta immediata.</td><td>Misura end-to-end ricezione, smistamento, verifica, inserimento e conferma. Nel processo AS-IS varia indicativamente da <code>1,5</code> a <code>5 giorni</code>, anche per le attese legate alla disponibilità e alle date comunicate dai fornitori. Nel TO-BE telematico il cliente inserisce direttamente l'ordine e il sistema restituisce subito il codice: per un ordine medio il tempo stimato scende a circa <code>20 minuti</code>.</td></tr></tbody></table></div>",
   "Il confronto mostra perché un KPI deve avere <strong>confini coerenti con il processo</strong>. Il lead time ordine non misura soltanto la digitazione: comprende anche code, passaggi organizzativi, verifiche di disponibilità e conferma. La percentuale di errori, invece, nasce a livello di riga ma valuta l'affidabilità dell'intero sottoprocesso. Nel TO-BE la tecnologia modifica attività, responsabilità e tempi; perciò il miglioramento atteso deve essere verificato mantenendo stabile la definizione dell'indicatore e confrontando AS-IS e TO-BE sullo stesso perimetro.",
  ],None),
  (1,"4 Laboratorio",[
   "Definire due o tre KPI per il processo in analisi. Per ciascuno specificare formula, unità, frequenza, fonte del dato e un target motivato.",
  ],None),
 ],
 kt=[
  "La misura rende il miglioramento verificabile e sostituisce le impressioni con i dati.",
  "Efficacia ed efficienza sono dimensioni distinte: un processo può eccellere in una e non nell'altra.",
  "Un KPI è definito solo se ha formula, unità, frequenza, fonte del dato, proprietario e decisione associata; target e soglie richiedono un riferimento.",
  "Un cruscotto direzionale sintetizza pochi indicatori con valore, target, scostamento e trend e rimanda al dettaglio per la diagnosi.",
  "La Balanced Scorecard collega KPI e obiettivi attraverso le prospettive finanziaria, cliente, processi interni e apprendimento/crescita.",
  "Gli indicatori più utili nascono dalle variabili critiche e dai colli di bottiglia della matrice.",
  "Nel caso SAEM l'albero delle determinanti collega KPI operativi, risultati di processo e obiettivi strategici; il confronto AS-IS/TO-BE mantiene stabile il perimetro della misura.",
 ]),

"06": dict(
 sections=[
  (1,"1 Rappresentazioni sintetiche",[
   "Rappresentare un processo significa renderlo leggibile a colpo d'occhio. Le forme sintetiche precedono i diagrammi e ne preparano i contenuti.",
  ],None),
  (2,"1.1 Tabelle e matrici",[
   "Tabelle e matrici organizzano in righe e colonne gli elementi del processo: attività e responsabili, dati gestiti, variabili e valori, rischi e contromisure. Sono rapide da compilare e confrontare, non richiedono strumenti grafici e costituiscono una buona verifica preliminare prima di disegnare una process map o un diagramma BPMN.",
   "Una <strong>matrice CRUD</strong> mette in relazione le attività con gli oggetti informativi che il processo crea, legge, aggiorna o elimina. CRUD è l'acronimo di <em>Create</em> (creare), <em>Read</em> (leggere o consultare), <em>Update</em> (modificare) e <em>Delete</em> (eliminare). La matrice aiuta a scoprire dati non gestiti, duplicazioni, aggiornamenti senza responsabile e cancellazioni che richiedono una regola di conservazione. Una stessa attività può avere più lettere sullo stesso oggetto, per esempio <code>CR</code> quando crea un ticket e ne legge contestualmente i dati di contatto.",
   "Esempio CRUD sul processo APQC 6.2.2 <em>Manage customer service problems, requests, and inquiries</em>:",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Activity</th><th>Ticket / richiesta</th><th>Storico cliente</th><th>Articolo knowledge base</th><th>Esito / risposta</th><th>Opportunità commerciale</th></tr></thead><tbody><tr><td><strong>6.2.2.1 Ricevere</strong></td><td>C</td><td>R</td><td>—</td><td>—</td><td>—</td></tr><tr><td><strong>6.2.2.2 Analizzare</strong></td><td>RU</td><td>R</td><td>R</td><td>U</td><td>—</td></tr><tr><td><strong>6.2.2.3 Risolvere</strong></td><td>U</td><td>R</td><td>R</td><td>C/U</td><td>—</td></tr><tr><td><strong>6.2.2.4 Rispondere</strong></td><td>R</td><td>—</td><td>R</td><td>U</td><td>—</td></tr><tr><td><strong>6.2.2.5 Identificare upsell/cross-sell</strong></td><td>R</td><td>R</td><td>—</td><td>R</td><td>C</td></tr><tr><td><strong>6.2.2.6 Consegnare alle vendite</strong></td><td>R</td><td>—</td><td>—</td><td>R</td><td>CU</td></tr></tbody></table></div>",
   "La matrice <strong>RACI</strong> risponde invece alla domanda \"chi fa che cosa?\". Per ogni attività si incrociano i ruoli e si assegna una delle quattro responsabilità: <strong>R — Responsible</strong>, esegue il lavoro; <strong>A — Accountable</strong>, risponde del risultato finale e approva; <strong>C — Consulted</strong>, viene consultato prima della decisione; <strong>I — Informed</strong>, riceve aggiornamenti o l'esito. È buona pratica avere almeno un R e un solo A per attività, salvo una scelta organizzativa esplicita. R e A possono coincidere quando chi esegue è anche il titolare del risultato.",
   "La guida in italiano di <a href=\"https://learn.microsoft.com/it-it/power-platform/guidance/adoption/roles\" target=\"_blank\" rel=\"noopener noreferrer\">Microsoft Learn — Definire ruoli e responsabilità</a> presenta la procedura per costruire una RACI e un esempio concreto. La tabella seguente applica la stessa logica, come esempio didattico, al customer service APQC.",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Activity</th><th>Customer Service Representative</th><th>Customer Service Manager</th><th>Specialista tecnico</th><th>Team Vendite</th><th>Cliente</th></tr></thead><tbody><tr><td><strong>Ricevere la richiesta</strong></td><td>R</td><td>A</td><td>I</td><td>I</td><td>C</td></tr><tr><td><strong>Analizzare problema o quesito</strong></td><td>R</td><td>A</td><td>C</td><td>I</td><td>C</td></tr><tr><td><strong>Risolvere la richiesta</strong></td><td>R</td><td>A</td><td>C/R</td><td>I</td><td>C</td></tr><tr><td><strong>Rispondere al cliente</strong></td><td>R</td><td>A</td><td>C</td><td>I</td><td>I</td></tr><tr><td><strong>Identificare opportunità upsell/cross-sell</strong></td><td>R</td><td>A</td><td>C</td><td>C</td><td>I</td></tr><tr><td><strong>Trasmettere opportunità alle vendite</strong></td><td>R</td><td>A</td><td>I</td><td>C/R</td><td>I</td></tr></tbody></table></div>",
   "La CRUD e la RACI descrivono due aspetti diversi e complementari: la prima segue il ciclo di vita delle informazioni, la seconda assegna responsabilità organizzative. Se la RACI mostra un'attività senza R, il lavoro non ha esecutore; se la CRUD mostra un oggetto senza C o U, il dato potrebbe non avere un punto di creazione o aggiornamento. Le due matrici possono quindi essere usate insieme per controllare completezza e coerenza della scheda di processo.",
  ],None),
  (2,"1.2 SIPOC: struttura e uso",[
   "Il <strong>SIPOC</strong> è una vista ad alto livello del processo articolata in cinque colonne: <em>Suppliers</em> (fornitori), <em>Inputs</em> (ingressi), <em>Process</em> (macro-fasi), <em>Outputs</em> (risultati) e <em>Customers</em> (clienti o destinatari). La definizione e l'uso didattico riprendono la descrizione dell'<a href=\"https://asq.org/quality-resources/sipoc\" target=\"_blank\" rel=\"noopener noreferrer\">American Society for Quality</a>: il SIPOC si compila dopo aver fissato evento di avvio e risultato finale, prima del dettaglio di Activity e Task.",
   "La colonna Process contiene poche macro-fasi, normalmente cinque-sette, e non l'elenco dei Task. Il modello permette di verificare che ogni input abbia un fornitore, ogni output abbia un cliente e che il perimetro sia condiviso dagli stakeholder. Supplier e Customer possono essere interni o esterni; input e output possono essere dati, documenti, materiali, decisioni o servizi.",
   "La stessa tabella usata per l'esempio APQC della Category 6.0 — <em>Manage Customer Service</em> — viene riportata qui come modello completo per la lettura di un SIPOC:",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Supplier</th><th>Input</th><th>Process (macro-fasi)</th><th>Output</th><th>Customer</th></tr></thead><tbody><tr><td>Cliente; canali di contatto (telefono, email, chat, portale)</td><td>Richiesta, problema o quesito; storico cliente; SLA contrattuali</td><td>Ricevere la richiesta → analizzarla → risolverla (o identificare upsell) → rispondere al cliente → trasmettere l'opportunità alle vendite</td><td>Richiesta risolta e risposta al cliente; eventuale lead commerciale</td><td>Cliente finale; team Vendite per le opportunità identificate</td></tr></tbody></table></div>",
   "Il SIPOC non sostituisce la scheda processo o il diagramma BPMN: li prepara, rendendo espliciti gli scambi ai bordi del processo. Dalla tabella si può poi passare alla process map, distribuire le macro-fasi nelle corsie e dettagliare le eccezioni con gateway ed eventi.",
  ],None),
  (1,"2 Process map e swimlane",[
   "I diagrammi di flusso mostrano la sequenza delle attività e le decisioni. Le corsie aggiungono la dimensione della responsabilità.",
  ],None),
  (2,"2.1 Mappa di processo per fasi",[
   "La process map dispone le attività nell'ordine di esecuzione, con i punti di decisione, gli input e gli esiti. Evidenzia ripetizioni, attese e passaggi di consegna ed è la base per discutere semplificazioni. Nel caso SAEM la stessa area di processo può essere letta con due prospettive complementari: la rappresentazione SCOR dei macro-processi di consegna e la rappresentazione UML/Eriksson–Penker del flusso organizzativo e informativo.",
   "La tavola SCOR mostra <strong>D1 — Deliver Stocked Product</strong> e <strong>D2 — Deliver Make-to-Order Product</strong> come una catena di elementi D.1–D.11: valutazione e risposta al cliente, ricezione e validazione dell'ordine, impegno delle scorte, selezione del corriere, generazione dei documenti, prelievo, carico/spedizione, aggiornamento della partenza e fatturazione. Le frecce e i dati ai bordi rendono visibili le dipendenze con piani, disponibilità, cliente e magazzino.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch06/saem-scor-d1-d2-process-map.png\" alt=\"Process map SCOR del caso SAEM per D1 Deliver Stocked Product e D2 Deliver Make-to-Order Product, con gli elementi D.1-D.11 e i relativi flussi informativi\" data-caption=\"Process map SCOR D1 e D2 del caso SAEM.\"><figcaption>Process map in formato SCOR: D1 <em>Deliver Stocked Product</em> e D2 <em>Deliver Make-to-Order Product</em>. La figura evidenzia attività, flussi informativi e dipendenze end-to-end.</figcaption></figure>",
   "La tavola UML/Eriksson–Penker dettaglia invece la preparazione dell'offerta D.1 attraverso corsie organizzative, oggetti informativi, attività, decisioni e flussi. È orientata in orizzontale per rendere leggibili le corsie e i nomi degli oggetti.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch06/saem-eriksson-penker-d1-process-map.png\" alt=\"Process map UML Eriksson-Penker del caso SAEM per la preparazione dell'offerta D.1, ruotata in orizzontale, con corsie Sistema EDP, RGC/FC, DIRV, Servizi e centralinista\" data-caption=\"Process map UML/Eriksson–Penker D.1 del caso SAEM.\"><figcaption>Process map UML/Eriksson–Penker per D.1 <em>Preparazione offerta</em>, orientata in orizzontale: le corsie collegano ruoli, attività, oggetti informativi e decisioni.</figcaption></figure>",
   "Il confronto è utile perché SCOR fornisce una vista standardizzata e comparabile del processo end-to-end, mentre UML/Eriksson–Penker rende più espliciti ruoli, oggetti e regole locali. Le due mappe non sono concorrenti: la prima aiuta a collocare il processo nella catena di fornitura, la seconda aiuta a progettare o verificare il flusso operativo.",
  ],None),
  (1,"3 Cenni a BPMN",[
   "<a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN (Business Process Model and Notation)</a> è lo standard OMG per rappresentare i processi in modo formale, con un insieme di simboli condiviso. La <a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN Reference ufficiale di Camunda</a> presenta gli elementi principali della notazione e il loro significato.",
  ],None),
  (2,"3.1 Elementi di base",[
   "La <a href=\"https://camunda.com/bpmn/reference/\" target=\"_blank\" rel=\"noopener noreferrer\">BPMN Reference di Camunda</a> distingue gli elementi di flusso in eventi, attività e gateway. Gli eventi indicano qualcosa che accade, le attività indicano lavoro da svolgere e i gateway controllano la convergenza o la divergenza dei percorsi. Le corsie aggiungono la responsabilità, ma non cambiano il significato dell'elemento.",
   "<strong>Eventi.</strong> Il bordo del cerchio e il simbolo interno precisano il comportamento: un evento di <em>start</em> crea una nuova istanza o avvia un sotto-processo; un evento intermedio può attendere (catch) o generare (throw) un accadimento mentre il flusso è attivo; un evento <em>end</em> conclude un percorso. Un bordo pieno identifica normalmente un evento interrupting, mentre un bordo tratteggiato indica un evento non-interrupting che apre un ramo lasciando proseguire l'attività principale.",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Famiglia / icona</th><th>Significato</th><th>Uso tipico nel modello</th></tr></thead><tbody><tr><td><img src=\"../assets/images/ch06/bpmn-reference/event-start.svg\" alt=\"Evento di inizio BPMN\" style=\"max-width:70px\"><br><strong>Start none</strong></td><td>Avvio senza trigger esterno esplicito.</td><td>Usarlo quando il diagramma parte da una condizione già assunta, per esempio l'apertura giornaliera del lavoro.</td></tr><tr><td><img src=\"../assets/images/ch06/bpmn-reference/event-message-start.svg\" alt=\"Evento di inizio messaggio BPMN\" style=\"max-width:70px\"><br><strong>Start message</strong></td><td>Un messaggio ricevuto avvia l'istanza.</td><td>Ricezione di una richiesta cliente o di un ordine da un canale esterno.</td></tr><tr><td><img src=\"../assets/images/ch06/bpmn-reference/event-timer-intermediate.svg\" alt=\"Evento intermedio timer BPMN\" style=\"max-width:70px\"><br><strong>Intermediate catch</strong></td><td>Il processo attende un evento, come messaggio, timer o condizione.</td><td>Attendere la risposta del cliente, la scadenza di uno SLA o una data di consegna.</td></tr><tr><td><img src=\"../assets/images/ch06/bpmn-reference/event-escalation-throw.svg\" alt=\"Evento intermedio di escalation BPMN\" style=\"max-width:70px\"><br><strong>Intermediate throw</strong></td><td>Il processo genera un'escalation verso un gestore o un processo padre.</td><td>Segnalare un caso oltre soglia senza trattarlo automaticamente come errore.</td></tr><tr><td><img src=\"../assets/images/ch06/bpmn-reference/event-error-boundary.svg\" alt=\"Evento di errore sul bordo di un'attività BPMN\" style=\"max-width:70px\"><br><strong>Boundary error</strong></td><td>Rileva un errore durante l'attività a cui è attaccato e devia il flusso.</td><td>Gestire un pagamento rifiutato o un'integrazione indisponibile mentre il Task è in esecuzione.</td></tr><tr><td><img src=\"../assets/images/ch06/bpmn-reference/event-end.svg\" alt=\"Evento di fine messaggio BPMN\" style=\"max-width:70px\"><br><strong>End</strong></td><td>Chiude il percorso; il simbolo interno può indicare messaggio, errore, escalation o terminazione.</td><td>Concludere con risposta al cliente, fatturazione o comunicazione di esito.</td></tr></tbody></table></div>",
   "<strong>Attività.</strong> Il rettangolo arrotondato rappresenta lavoro. Un Task è atomico; un Sub-Process contiene un flusso dettagliato e può essere collassato; una Call Activity richiama un processo globale riusabile. I tipi di Task (user, manual, service, send, receive, business rule e script) specificano chi o che cosa esegue il lavoro e sono approfonditi nel Modulo 4.",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Attività / icona</th><th>Spiegazione</th><th>Esempio</th></tr></thead><tbody><tr><td><img src=\"../assets/images/ch04/bpmn-activity-task.svg\" alt=\"Icona BPMN Task\" style=\"max-width:100px\"><br><strong>Task</strong></td><td>Unità atomica di lavoro con un esito osservabile.</td><td>Classificare la richiesta cliente.</td></tr><tr><td><img src=\"../assets/images/ch04/bpmn-activity-subprocess.svg\" alt=\"Icona BPMN Sub-Process\" style=\"max-width:100px\"><br><strong>Sub-Process</strong></td><td>Raggruppa un flusso interno per nascondere o espandere il dettaglio.</td><td>Gestire l'escalation tecnica con più passi.</td></tr><tr><td><img src=\"../assets/images/ch04/bpmn-activity-call-activity.svg\" alt=\"Icona BPMN Call Activity\" style=\"max-width:100px\"><br><strong>Call Activity</strong></td><td>Richiama un processo globale riusabile da più processi.</td><td>Richiamare il processo condiviso di verifica cliente.</td></tr></tbody></table></div>",
   "<strong>Gateway.</strong> Il rombo non esegue lavoro: valuta o sincronizza il flusso. XOR segue una sola alternativa; AND apre o ricongiunge tutti i rami paralleli; OR segue una o più alternative in base alle condizioni; il gateway event-based attende il primo evento disponibile. La decisione deve essere preparata da un Task o da dati già disponibili, e le condizioni vanno scritte sui flussi in uscita.",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Gateway / icona</th><th>Spiegazione</th><th>Esempio</th></tr></thead><tbody><tr><td><img src=\"../assets/images/ch06/bpmn-reference/gateway-xor.svg\" alt=\"Gateway esclusivo XOR BPMN\" style=\"max-width:70px\"><br><strong>XOR</strong></td><td>Seleziona esattamente un percorso.</td><td>Richiesta completa oppure richiesta da integrare.</td></tr><tr><td><img src=\"../assets/images/ch06/bpmn-reference/gateway-and.svg\" alt=\"Gateway parallelo AND BPMN\" style=\"max-width:70px\"><br><strong>AND</strong></td><td>Avvia tutti i rami e li sincronizza al ricongiungimento.</td><td>Verifica tecnica e verifica contrattuale in parallelo.</td></tr><tr><td><img src=\"../assets/images/ch06/bpmn-reference/gateway-or.svg\" alt=\"Gateway inclusivo OR BPMN\" style=\"max-width:70px\"><br><strong>OR</strong></td><td>Avvia una o più alternative compatibili.</td><td>Inviare risposta standard e, quando necessario, attivare anche il team vendite.</td></tr><tr><td><img src=\"../assets/images/ch06/bpmn-reference/gateway-event.svg\" alt=\"Gateway basato su eventi BPMN\" style=\"max-width:70px\"><br><strong>Event-based</strong></td><td>Il primo evento che si verifica determina il percorso; gli altri vengono scartati.</td><td>Attendere risposta cliente oppure scadenza dello SLA.</td></tr></tbody></table></div>",
   "<strong>Flussi e frecce.</strong> Il flusso di sequenza collega elementi dello stesso pool e indica l'ordine di esecuzione. Un flusso condizionale esplicita una condizione in uscita da un'attività; il flusso di default identifica il ramo scelto quando nessuna condizione è vera. Il flusso di messaggio collega pool diversi e non va usato per sostituire un normale passaggio tra corsie dello stesso pool. L'associazione tratteggiata collega annotazioni o dati senza controllare la sequenza.",
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Tipo di collegamento</th><th>Icona</th><th>Significato</th></tr></thead><tbody><tr><td><strong>Sequence flow</strong></td><td><img src=\"../assets/images/ch06/bpmn-reference/flow-sequence.svg\" alt=\"Freccia di flusso di sequenza BPMN\" style=\"max-width:180px\"></td><td>Ordine normale di esecuzione nello stesso pool.</td></tr><tr><td><strong>Conditional flow</strong></td><td><img src=\"../assets/images/ch06/bpmn-reference/flow-conditional.svg\" alt=\"Freccia di flusso condizionale BPMN\" style=\"max-width:180px\"></td><td>Ramo percorso quando la condizione associata è vera.</td></tr><tr><td><strong>Default flow</strong></td><td><img src=\"../assets/images/ch06/bpmn-reference/flow-default.svg\" alt=\"Freccia di flusso di default BPMN\" style=\"max-width:180px\"></td><td>Ramo di fallback quando nessuna condizione precedente si applica.</td></tr><tr><td><strong>Message flow</strong></td><td><img src=\"../assets/images/ch06/bpmn-reference/flow-message.svg\" alt=\"Freccia di flusso di messaggio BPMN\" style=\"max-width:180px\"></td><td>Messaggio tra partecipanti o pool distinti; non rappresenta la sequenza interna.</td></tr></tbody></table></div>",
   "<strong>Usare gli eventi come raccordo.</strong> Un evento non è una decorazione: va collegato con un flusso coerente con il suo comportamento. Per un <strong>trigger</strong>, si può usare un <em>Message Start Event</em> «Richiesta cliente ricevuta» collegato direttamente al Task «Registrare richiesta»; se il processo è già attivo e deve attendere una risposta, si usa invece un <em>Intermediate Message Catch Event</em> dopo un Task di invio o in un gateway event-based. Per un <strong>escalation</strong>, si può collegare un <em>Escalation Throw Event</em> a un Sub-Process o a un'attività e riceverlo con un <em>Escalation Boundary Event</em> o con un Event Sub-Process nel processo padre: il ramo di escalation può interrompere l'attività oppure, con bordo tratteggiato non-interrupting, avviare una gestione parallela lasciando proseguire il lavoro principale.",
   "La differenza tra evento di avvio e evento di raccolta è quindi temporale e semantica: lo Start Event crea il token iniziale, il Catch Event attende un evento durante un percorso già aperto, il Throw Event lo produce e l'End Event chiude il percorso. Questa regola evita di usare un gateway o un Task come sostituto improprio di un evento.",
  ],None),
  (2,"3.2 Quando serve una notazione formale",[
   "Una notazione formale conviene quando il diagramma deve essere interpretato senza ambiguità da persone diverse, quando descrive percorsi alternativi e condizioni, o quando è il punto di partenza per l'automazione.",
   "Per una panoramica rapida, SIPOC e process map restano più economici.",
  ],None),
  (1,"4 Visualizzare gli esempi con Camunda",[
   "I file <code>esempi-apqc/&lt;dominio&gt;/processo.bpmn</code> contengono i sette processi in notazione BPMN 2.0 con corsie per ruolo, pensati per essere proiettati e discussi in aula. Si aprono con Camunda Modeler, gratuito, senza alcun motore di esecuzione collegato.",
   "Per la demo con <strong>Camunda Web Modeler</strong> usare come traccia la guida ufficiale <a href=\"https://docs.camunda.io/docs/components/modeler/web-modeler/modeling/model-your-first-diagram/\" target=\"_blank\" rel=\"noopener noreferrer\">Model your first diagram</a>: creare il diagramma online, aggiungere evento iniziale, attività, evento finale e collegamenti, quindi confrontare il risultato con uno dei processi BPMN del repository.",
   "Come esempio avanzato e <strong>blueprint da caricare nel Web Modeler</strong> usare <a href=\"https://marketplace.camunda.com/en-US/apps/449510/credit-card-fraud-dispute-handling\" target=\"_blank\" rel=\"noopener noreferrer\">Credit Card Fraud Dispute Handling</a> del Camunda Marketplace. Il modello mostra l'orchestrazione di attività automatiche e manuali nella gestione di una contestazione per frode; il file BPMN è disponibile anche come <a href=\"https://raw.githubusercontent.com/camunda/camunda-platform-tutorials/main/solutions/bank-customer-complaint-dispute-handling/Bank_customer_complaint_dispute_handling.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">download BPMN</a> da importare nel Web Modeler.",
   "Un secondo esempio e <strong>blueprint da caricare nel Web Modeler</strong> è <a href=\"https://marketplace.camunda.com/en-US/apps/450143/loan-origination-and-processing\" target=\"_blank\" rel=\"noopener noreferrer\">Loan Origination and Processing</a>. Il modello rappresenta l'iter digitale di istruttoria e concessione di un prestito, con l'obiettivo di ridurre i tempi di approvazione e i passaggi manuali; il relativo <a href=\"https://raw.githubusercontent.com/camunda/camunda-platform-tutorials/main/solutions/bank-loan-origination-and-processing/bank-loan-origination-and-processing.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">file BPMN</a> può essere importato nel Web Modeler.",
   "In aula: aprire due esempi — tra cui customer service o IT, che includono un gateway esclusivo — e leggere insieme corsie, eventi e diramazioni; poi chiedere ai partecipanti di aggiungere un ramo di eccezione o un ruolo mancante.",
   "Per chi vuole approfondire, un assistente AI collegato a Camunda tramite MCP può generare la prima bozza del diagramma da una scheda processo. La revisione del diagramma resta sempre a carico dell'analista.",
  ],"La guida <a href=\"../lab-camunda-mcp.html\">Laboratorio BPMN con Camunda e assistente MCP</a> raccoglie prerequisiti, installazione e primo esempio per chi vuole provare la generazione assistita."),
  (1,"5 Laboratorio",[
   "Aprire due esempi APQC in Camunda Modeler. Per ciascuno: identificare corsie, evento di innesco, evento finale e gateway. Aggiungere un ramo di eccezione plausibile e salvarne una copia.",
  ],None),
  (1,"6 Esercizio ulteriore: Salesforce Flow",[
   "Dopo aver creato e modificato i processi in Camunda, ripetere l'esercizio con uno strumento applicativo diverso: <strong>Salesforce Flow</strong>. L'obiettivo non è sostituire BPMN, ma confrontare una rappresentazione standard del processo con una configurazione concreta di automazione.",
   "Aprire una Developer Edition o un Playground seguendo il percorso Trailhead <a href=\"https://trailhead.salesforce.com/content/learn/modules/flow-troubleshooting/review-flow-terminology-and-sign-up-for-a-special-org\" target=\"_blank\" rel=\"noopener noreferrer\">Flow Troubleshooting</a>. Analizzare nei Flow predisposti il trigger, le attività, le decisioni, i dati letti o scritti e l'esito restituito. Trailhead parla di Developer Edition o Playground, non di una Sandbox Salesforce tradizionale.",
   "Come esempio di implementazione osservare il Flow Salesforce <strong>Create New Customer</strong>: il processo business parte dalla raccolta delle informazioni del cliente, mentre il sistema esegue in sequenza la creazione di Account, Contact e Opportunity e restituisce una conferma. Confrontare il Flow con la scheda processo e con il diagramma BPMN: evidenziare quali passaggi sono attività di processo, quali sono operazioni sui dati e dove sono modellate le decisioni.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/salesforce-flow-create-new-customer.png\" alt=\"Salesforce Flow Builder: il flusso Create New Customer raccoglie le informazioni e crea Account, Contact e Opportunity prima di mostrare una conferma\" data-caption=\"Esercizio Salesforce Flow: Create New Customer.\"><figcaption>Esempio di implementazione Salesforce Flow: il processo business di acquisizione di un nuovo cliente interagisce con il sistema creando Account, Contact e Opportunity.</figcaption></figure>",
   "Consegna: produrre una breve tabella di confronto Camunda/Salesforce con trigger, attività, decisioni, oggetti dati, responsabilità e output. Indicare almeno una differenza tra il modello BPMN e l'implementazione applicativa.",
  ],None),
 ],
 kt=[
  "SIPOC e tabelle fissano confini e scambi prima del dettaglio grafico.",
  "La process map mostra sequenza e decisioni; le corsie aggiungono la responsabilità e rendono visibili gli handoff.",
  "BPMN è lo standard OMG: evento, attività, gateway, flusso di sequenza e corsie sono gli elementi di base.",
  "I file .bpmn del corso servono a visualizzare e discutere gli esempi; un assistente AI via MCP può produrre una bozza, ma la revisione è dell'analista.",
  "Salesforce Flow offre un esercizio complementare: confrontare il modello BPMN con un'automazione applicativa che esegue attività, decisioni e operazioni sui dati.",
 ]),

"07": dict(
 sections=[
  (1,"1 Costruire la scheda processo: percorso guidato",[
   "La scheda processo viene costruita per passi, usando come esempio la scheda completa della Category 6.0 <em>Manage Customer Service</em>, disponibile nel repository alla voce <a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/05-customer-service/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\">05-customer-service/processo.md</a>.",
   "Ogni passo aggiunge un'informazione verificabile e prepara quello successivo: prima si fissa il perimetro, poi si scelgono le Activity, si dettagliano i Task, si analizzano scambi e variabili, si sintetizza il processo e infine lo si rappresenta in BPMN.",
  ],None),
  (2,"1.1 Passo 1 — Collocazione nella gerarchia PCF",[
   "Si riportano Category, Process Group e Process con codice e nome ufficiale. La collocazione impedisce di descrivere un processo senza contesto e collega la scheda alla tassonomia APQC.",
   "Per Category 6.0 la sequenza è: <code>6.0 Manage Customer Service</code> → <code>6.2 Plan and manage customer service contacts</code> → <code>6.2.2 Manage customer service problems, requests, and inquiries</code>. Si annotano inoltre trigger e output finale, che delimitano il processo.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch08/m08-step-01-collocazione.svg\" alt=\"Estratto della scheda processo con Category 6.0, Process Group 6.2 e Process 6.2.2\" data-caption=\"Passo 1: collocazione PCF.\"><figcaption>Estratto della scheda: i tre livelli PCF definiscono l'identità e il perimetro gerarchico del processo.</figcaption></figure>",
  ],None),
  (2,"1.2 Passo 2 — Scelta delle Activity dal PCF",[
   "Si selezionano le Activity che realizzano il Process, mantenendo codice, nome e identificativo APQC. La scelta deve coprire il percorso end-to-end senza aggiungere attività estranee al perimetro.",
   "Nel caso 6.2.2 le Activity vanno da <em>Receive</em> ad <em>Deliver opportunity to sales team</em>. L'elenco costituisce l'indice operativo del processo e diventa la base per Task, SIPOC e BPMN.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch08/m08-step-02-activity.svg\" alt=\"Estratto della scheda con l'elenco delle sei Activity APQC del processo 6.2.2\" data-caption=\"Passo 2: Activity del processo.\"><figcaption>Estratto della scheda: elenco delle Activity selezionate dal ramo PCF 6.2.2.</figcaption></figure>",
  ],None),
  (2,"1.3 Passo 3 — Scomposizione in Task e requisiti IT",[
   "Si sceglie almeno una Activity e la si scompone in Task osservabili, ciascuno con esecutore ed esito verificabile. Nel nostro esempio l'Activity <em>Analyze problems, requests, and inquiries</em> diventa classificare la richiesta, verificare storico e SLA, decidere l'escalation e assegnare il caso.",
   "La scomposizione si collega ai requisiti IT del <a href=\"chapter-02.html\">Modulo 2</a>: per ogni Task si annotano ruolo, input/output, dati letti o scritti, operazioni CRUD, regole, eccezioni e criteri di verifica. Il PCF definisce Activity, mentre Task e requisiti IT dipendono dal contesto organizzativo e applicativo.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch08/m08-step-03-task-requirements.svg\" alt=\"Estratto della scheda con la scomposizione dell'Activity Analyze in quattro Task e i requisiti IT da verificare\" data-caption=\"Passo 3: Task e requisiti IT.\"><figcaption>Estratto didattico: i Task operativi sono collegati a dati, ruoli, regole ed eccezioni da documentare nei requisiti IT.</figcaption></figure>",
  ],None),
  (2,"1.4 Passo 4 — Analisi SIPOC",[
   "Si compilano Supplier, Input, Process, Output e Customer per fissare gli scambi ai bordi del processo. La colonna Process contiene macro-fasi, non tutti i Task; ogni input deve avere un fornitore e ogni output un destinatario.",
   "Per il customer service i fornitori sono il cliente e i canali di contatto; gli input sono richiesta, storico e SLA; le macro-fasi seguono le Activity; gli output sono risposta, richiesta risolta ed eventuale lead; i clienti sono cliente finale e team Vendite.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch08/m08-step-04-sipoc.svg\" alt=\"Estratto della scheda con il SIPOC del processo APQC 6.2.2\" data-caption=\"Passo 4: SIPOC.\"><figcaption>Estratto della scheda: il SIPOC delimita il processo e rende espliciti fornitori, scambi e destinatari.</figcaption></figure>",
  ],None),
  (2,"1.5 Passo 5 — Matrice delle variabili",[
   "Si traducono nella matrice le grandezze che descrivono il processo: input, output, tempi, costi, volumi, ruoli, sistemi, vincoli e rischi/colli di bottiglia. Ogni riga deve riferirsi allo stesso perimetro e distinguere dato osservato da valore ancora da rilevare.",
   "Nel caso 6.2.2 la matrice collega la richiesta e lo storico ai sistemi CRM/ticketing, agli SLA, ai ruoli Customer Service e Vendite e ai rischi di classificazione errata, escalation tardiva e perdita di opportunità.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch08/m08-step-05-variabili.svg\" alt=\"Estratto della scheda con la matrice delle variabili del customer service\" data-caption=\"Passo 5: matrice delle variabili.\"><figcaption>Estratto della scheda: la matrice rende confrontabili risorse, condizioni operative, risultati e rischi.</figcaption></figure>",
  ],None),
  (2,"1.6 Passo 6 — Scheda sintetica del processo",[
   "Si ricompongono in una pagina le informazioni utili a governare il processo: nome e codice, owner, obiettivo, confini, ruoli, sistemi, KPI e rischi. La scheda sintetica non sostituisce i dettagli precedenti: li indicizza e li rende consultabili.",
   "Per 6.2.2 l'owner è il Customer Service Manager; l'obiettivo è gestire richieste, problemi e reclami. I KPI includono il tempo medio di risoluzione, la <strong>FCR — First Contact Resolution</strong> (percentuale di richieste risolte al primo contatto), la <strong>CSAT — Customer Satisfaction Score</strong> (punteggio di soddisfazione del cliente) e il numero di lead trasmessi alle vendite.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/ch08/m08-step-06-scheda-sintetica.svg\" alt=\"Estratto della scheda sintetica del processo APQC 6.2.2 con owner, obiettivo, confini, sistemi, KPI e rischi\" data-caption=\"Passo 6: scheda processo sintetica.\"><figcaption>Estratto della scheda sintetica: i campi essenziali riassumono il processo per lettura e governo.</figcaption></figure>",
  ],None),
  (2,"1.7 Passo 7 — Disegno BPMN",[
   "Si rappresentano trigger, Activity/Task, gateway, corsie, eventi finali e flussi. Il diagramma deve rispettare il perimetro della scheda e rendere visibili responsabilità, percorso principale ed eccezioni.",
   "Nel modello 6.2.2 il gateway distingue la risoluzione diretta dal ramo upsell/cross-sell; le corsie separano Customer Service Representative e Team Vendite. Il file completo è disponibile come <a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/05-customer-service/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">processo.bpmn</a>.",
   "<figure class=\"chapter-figure\"><img class=\"zoomable\" src=\"../assets/images/apqc-customer-service-process.png\" alt=\"Diagramma BPMN del processo APQC 6.2.2 con corsie Customer Service Representative e Team Vendite\" data-caption=\"Passo 7: diagramma BPMN.\"><figcaption>Rappresentazione BPMN del customer service: il diagramma verifica sequenza, ruoli, gateway e output del processo.</figcaption></figure>",
  ],None),
  (1,"2 Il deliverable completo",[
   "La scheda finale non è un documento isolato: è un pacchetto coerente di viste, ciascuna con una funzione diversa. La scheda completa di riferimento è disponibile nel repository: <a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/05-customer-service/processo.md\" target=\"_blank\" rel=\"noopener noreferrer\">aprire 05-customer-service/processo.md</a>.",
   "Il diagramma BPMN collegato alla scheda è disponibile in <a href=\"https://github.com/thimotyb/corso-processi/blob/main/esempi-apqc/05-customer-service/processo.bpmn\" target=\"_blank\" rel=\"noopener noreferrer\">processo.bpmn</a>.",
  ],None),
  (2,"2.1 Elementi del pacchetto e funzione",[
   "<div class=\"table-wrap\"><table class=\"pcf-table\"><thead><tr><th>Elemento</th><th>Cosa contiene</th><th>A cosa serve</th><th>Collegamento nel caso 6.2.2</th></tr></thead><tbody><tr><td><strong>Mappa gerarchica dei processi</strong></td><td>Category, Process Group, Process, Activity e codici.</td><td>Colloca il processo e ne stabilisce il perimetro.</td><td>6.0 → 6.2 → 6.2.2 → Activity 6.2.2.1–6.2.2.6.</td></tr><tr><td><strong>Scheda processo sintetica</strong></td><td>Owner, obiettivo, confini, ruoli, sistemi, KPI e rischi.</td><td>Permette una lettura rapida e supporta il governo.</td><td>Customer Service Manager, SLA, CRM/ticketing, FCR (risoluzione al primo contatto) e CSAT (soddisfazione del cliente).</td></tr><tr><td><strong>Elenco di Activity e Task</strong></td><td>Activity PCF e scomposizione operativa con esecutore ed esito.</td><td>Collega classificazione, lavoro reale e requisiti IT.</td><td>Analyze → classificare, verificare, decidere escalation, assegnare.</td></tr><tr><td><strong>Matrice delle variabili e relazioni</strong></td><td>Input, output, tempi, costi, volumi, ruoli, sistemi, vincoli, rischi e dipendenze.</td><td>Rende confrontabili i processi e prepara KPI e miglioramento.</td><td>Tempi secondo SLA, sistemi CRM, rischi di classificazione ed escalation.</td></tr><tr><td><strong>Diagramma di rappresentazione</strong></td><td>Process map o BPMN con eventi, attività, gateway, corsie e flussi.</td><td>Verifica sequenza, responsabilità, eccezioni e handoff.</td><td>Gateway upsell/cross-sell e corsie Customer Service/Vendite.</td></tr></tbody></table></div>",
  ],None),
  (2,"2.2 Riuso come template",[
   "Gli stessi sette passi e gli stessi campi si applicano agli altri domini APQC. Cambiano codici, ruoli, dati, KPI e diagrammi, ma resta costante la sequenza di costruzione. Le sette schede in <code>esempi-apqc/</code> sono esempi completi del pacchetto.",
  ],None),
  (1,"3 Laboratorio finale",[
   "Scegliere un dominio APQC diverso da Customer Service e replicare i sette passi: collocazione, Activity, Task e requisiti IT, SIPOC, matrice delle variabili, scheda sintetica e BPMN.",
   "Consegnare la scheda in formato Markdown, il diagramma BPMN e una breve nota sulle decisioni progettuali. Usare il modello Category 6 come riferimento e verificare che ogni elemento della tabella finale abbia un corrispondente nella scheda.",
  ],None),
 ],
 kt=[
  "La scheda processo si costruisce in sette passi progressivi, dalla collocazione PCF al diagramma BPMN.",
  "Activity e Task hanno livelli diversi: le Activity vengono dal PCF, i Task sono scomposti dall'analista e collegati ai requisiti IT.",
  "SIPOC e matrice delle variabili rendono espliciti scambi, risorse, condizioni e rischi.",
  "La scheda sintetica indicizza il lavoro, mentre il BPMN verifica sequenza, ruoli, gateway ed eccezioni.",
  "Il pacchetto di deliverable è riusabile come template per confrontare processi diversi.",
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

# Nel percorso didattico corrente la rappresentazione precede la misurazione:
# M06 tratta SIPOC/BPMN, mentre M07 è il modulo dedicato ai KPI.
CONTENT["06"], CONTENT["07"] = CONTENT["07"], CONTENT["06"]

# Le Category e i Process Group di M03 sono mantenuti come dati strutturati
# sopra, così le due sezioni possono essere aggiornate senza duplicare HTML.
for index, (level, title, paragraphs, note) in enumerate(CONTENT["03"]["sections"]):
    if title.startswith("2.1 "):
        CONTENT["03"]["sections"][index] = (
            level,
            title,
            [
                "La <strong>Category</strong> è il livello più alto del PCF e identifica una grande area di lavoro. Le tredici Category offrono una vista complessiva dell'organizzazione e non coincidono necessariamente con i reparti.",
                pcf_category_table(),
            ],
            note,
        )
    elif title.startswith("2.2 "):
        CONTENT["03"]["sections"][index] = (
            level,
            title,
            [
                "Il <strong>Process Group</strong> riunisce processi coerenti che contribuiscono all'esecuzione di una Category. Le tabelle riportano numero gerarchico, nome ufficiale e una spiegazione sintetica in italiano.",
                "I collegamenti aprono la ricerca della singola Category nella Resource Library ufficiale APQC; dalla scheda della versione 8.0 il comando <em>View Now</em> consente di scaricare il PDF con definizioni e misure.",
                pcf_process_group_tables(),
            ],
            note,
        )
    elif title.startswith("3.1 "):
        CONTENT["03"]["sections"][index] = (
            level,
            "3.1 Processi di gestione e supporto nel PCF",
            [
                "APQC divide il framework in due blocchi: le Category <strong>1.0-6.0</strong> rappresentano gli <strong>Operating Processes</strong>; le Category <strong>7.0-13.0</strong> costituiscono i <strong>Management and Support Services</strong>. Queste ultime forniscono persone, tecnologie, risorse, controlli e capacità necessarie ai processi operativi.",
                "Le Category di gestione e supporto sono:",
                pcf_support_categories_list(),
                "Queste Category abilitano, governano, proteggono e migliorano il lavoro operativo. Il dettaglio dei rispettivi Process Group è già riportato nella sezione 2.2.",
            ],
            note,
        )

# La tabella delle misure APQC appartiene al modulo KPI, non al modulo PCF.
for index, (level, title, paragraphs, note) in enumerate(CONTENT["07"]["sections"]):
    if title.startswith("3.2 "):
        CONTENT["07"]["sections"][index] = (
            level,
            title,
            [
                *paragraphs,
                "La tabella seguente raccoglie, per ciascun Process Group disponibile nei documenti APQC caricati nelle risorse del corso, i KPI proposti e una breve descrizione in italiano.",
                pcf_kpi_table(),
            ],
            note,
        )

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
        ("Laboratori M06 - Camunda e Salesforce Flow", a("06"),
         "Creare e modificare processi in Camunda, poi confrontare il modello BPMN con un esercizio di automazione in Salesforce Flow."),
        ("Laboratorio M07 - Definire i KPI", a("07"),
         "Definire due-tre KPI con formula, unità, frequenza, fonte del dato e target motivato."),
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
        ("APQC — Introduction to the Process Classification Framework", "https://www.apqc.org/resource-library/resource-listing/introduction-apqcs-process-classification-framework-pcf"),
        ("APQC — Types of process models", "https://www.apqc.org/blog/what-are-different-types-process-models"),
        ("APQC — Process Classification Framework FAQ", "https://www.apqc.org/process-frameworks/pcf-faqs"),
        ("APQC — What are Key Performance Indicators?", "https://www.apqc.org/blog/what-are-key-performance-indicators-kpis"),
        ("APQC — Difference between KPI, measure, and metric", "https://www.apqc.org/blog/ask-us-answered-whats-difference-between-kpi-measure-and-metric"),
        ("APQC — Best metrics to measure process performance", "https://www.apqc.org/What-Are-the-Best-Metrics-to-Measure-Process-Performance"),
        ("APQC — PCF Process Definitions and Key Measures collection", "https://www.apqc.org/resource-library/resource-collection/pcf-version-80-process-definitions-and-key-measures-collection"),
        ("APQC — Cross-Industry PCF (PDF 8.0)", "https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-pdf-13"),
        ("APQC — Cross-Industry PCF (Excel 8.0)", "https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-excel-12"),
        ("ASCM — SCOR Digital Standard (supply chain)", "https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/"),
        ("Object Management Group — BPMN", "https://www.omg.org/spec/BPMN/"),
        ("BPMN.org — risorse introduttive", "https://www.bpmn.org/"),
        ("ASQ — SIPOC+CM Diagram", "https://asq.org/quality-resources/sipoc"),
        ("ISO — ISO 22400-1 KPI terminology and concepts", "https://www.iso.org/standard/56847.html"),
        ("Harvard Business Review — The Balanced Scorecard", "https://hbr.org/2005/07/the-balanced-scorecard-measures-that-drive-performance"),
        ("Balanced Scorecard Institute — Four perspectives", "https://balancedscorecard.org/staging/bsc-basics/articles-videos/the-four-perspectives-of-the-balanced-scorecard/"),
        ("Balanced Scorecard Institute — Basics", "https://balancedscorecard.org/bsc-basics-overview/"),
        ("Microsoft Learn — Power BI dashboard design tips", "https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips"),
        ("Microsoft Learn — Introduction to Power BI dashboards", "https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards"),
        ("Microsoft Learn — KPI visualizations in Power BI", "https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-kpi"),
        ("Camunda — BPMN tutorial e process modeling", "https://camunda.com/bpmn/"),
        ("Camunda — BPMN Reference", "https://camunda.com/bpmn/reference/"),
        ("Camunda Docs — User tasks e Camunda Forms", "https://docs.camunda.io/docs/components/modeler/bpmn/user-tasks/"),
        ("Camunda Docs — Build forms with Modeler", "https://docs.camunda.io/docs/components/modeler/forms/utilizing-forms/"),
        ("Salesforce Trailhead — Get to Know Flow Orchestration", "https://trailhead.salesforce.com/content/learn/modules/orchestrator-basics/get-to-know-orchestrator"),
        ("Camunda Docs — Model your first diagram (Web Modeler)", "https://docs.camunda.io/docs/components/modeler/web-modeler/modeling/model-your-first-diagram/"),
        ("Camunda Marketplace — Credit Card Fraud Dispute Handling", "https://marketplace.camunda.com/en-US/apps/449510/credit-card-fraud-dispute-handling"),
        ("Camunda Marketplace — Loan Origination and Processing", "https://marketplace.camunda.com/en-US/apps/450143/loan-origination-and-processing"),
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
   <p>Gli esempi APQC del corso (<code>esempi-apqc/</code>) sono volutamente astratti: gerarchia PCF corretta, ma azienda e ruoli generici. SAEM S.p.A. è un caso aziendale reale che permette di ripetere lo stesso esercizio di classificazione e mappatura su un'organizzazione con ruoli, sistemi e criticità documentati.</p>
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
   <p>Per confronto, il modello <strong>SCOR (Supply Chain Operations Reference)</strong> è specializzato sui processi di supply chain (pianificazione, approvvigionamento, produzione, evasione ordini, logistica, resi), mentre l'APQC PCF è una tassonomia generica cross-industry che copre anche le funzioni non di supply chain (vendite, HR, IT, finance...).</p>
   <p>SCOR è mantenuto oggi dalla <strong>Association for Supply Chain Management (ASCM)</strong>, sotto il nome di <strong>SCOR Digital Standard (SCOR-DS)</strong>. Il modello attuale organizza i processi su un livello Orchestrate e sei processi di primo livello: <strong>Plan, Order, Source, Transform, Fulfill, Return</strong>.</p>
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
