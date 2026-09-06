"""Estrazione riproducibile; consultare gli output conservati prima di rieseguirla."""
from pathlib import Path
import hashlib
import json
import pdfplumber
from pypdf import PdfReader

base = Path(__file__).resolve().parent
source = base.parent.parent / 'resources' / 'casoSAEM.pdf'
pages = sorted(set([3, 4, 5, 6, 32, 51, 55] + list(range(35, 44)) + list(range(72, 76)) + list(range(88, 135))))
figures = [72, 73, 74, 75, 95, 96, 97, 98, 99, 106, 107, 108, 109, 110, 113, 118, 120]
reader = PdfReader(source)
text = ['# Testo delle pagine SAEM consultate\n', 'Estratto di lavoro. Le figure richiedono il controllo dei rendering in `pagine/`.\n']
for number in pages:
    printed = str(number - 12) if number >= 32 else 'indice preliminare'
    text.append(f'\n## PDF {number} / pagina stampata {printed}\n\n')
    text.append(reader.pages[number - 1].extract_text() or '[Pagina senza testo estraibile]')
    text.append('\n')
(base / 'testo-pagine.md').write_text(''.join(text), encoding='utf-8')
(base / 'pagine').mkdir(exist_ok=True)
with pdfplumber.open(source) as pdf:
    for number in figures:
        pdf.pages[number - 1].to_image(resolution=150).save(base / 'pagine' / f'pdf-{number:03d}.png')
manifest = {
    'source': 'resources/casoSAEM.pdf',
    'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'extracted_on': '2026-09-06',
    'total_pdf_pages': len(reader.pages),
    'text_pages_pdf_1_based': pages,
    'rendered_pages_pdf_1_based': figures,
    'render_dpi': 150,
    'note': 'Le inferenze BPMN sono annotate separatamente in estrazione-ordine.json e processo.md.'
}
(base / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Archiviate {len(pages)} pagine testuali e {len(figures)} figure.')
