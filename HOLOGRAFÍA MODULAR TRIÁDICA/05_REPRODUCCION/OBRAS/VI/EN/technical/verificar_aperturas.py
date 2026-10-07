#!/usr/bin/env python3
"""Verificación editorial focal de aperturas; no certifica resultados científicos."""
from pathlib import Path
import hashlib
import json
import re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parents[1] / 'PRESENTACION_ACADEMICA_SERIE_20260911' / ROOT.name
PREVIOUS = ROOT.parents[1] / 'APERTURAS_PAPER_RESTAURADAS_20260911_REV02' / ROOT.name
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

changed = {'sections/00_portada.tex', 'sections/00_resumen.tex', 'main_catalogo.tex', 'main.tex'}
preserved = []
for source in sorted(OLD.rglob('*.tex')):
    rel = source.relative_to(OLD)
    if any(x.startswith('build') or x == 'tmp' for x in rel.parts):
        continue
    dest = ROOT / rel
    if str(rel) not in changed:
        assert dest.is_file() and sha(source) == sha(dest), str(rel)
        preserved.append({'path': str(rel), 'sha256': sha(source)})

old_summary = (OLD / 'sections/00_resumen.tex').read_text()
new_summary = (ROOT / 'sections/00_resumen.tex').read_text()
old_body = old_summary.split('\n\n', 1)[1].strip()
new_body = new_summary.split('\\noindent\n', 1)[1].rsplit('\\par\\endgroup', 1)[0].strip()
assert old_body == new_body
old_cat = (OLD / 'main_catalogo.tex').read_text()
new_cat = (ROOT / 'main_catalogo.tex').read_text()
def presentation(s):
    return s.split('\\begin{minipage}{\\textwidth}', 1)[1].split('\\end{minipage}', 1)[0]
assert presentation(old_cat) == presentation(new_cat)
assert '\\begin{titlepage}' not in new_cat
assert '\\begin{titlepage}' not in (ROOT / 'sections/00_portada.tex').read_text()

pdfs = []
for name, prefix in [
    ('PARTICULAS_PERSISTENCIA_Y_ESPECTRO_DE_MASAS.pdf', 'vi'),
    ('CATALOGOS_ESTRUCTURALES_Y_METROLOGICOS.pdf', 'catalogo'),
]:
    path = ROOT / 'output/pdf' / name
    reader = PdfReader(path)
    previous = PdfReader(PREVIOUS / 'output/pdf' / name)
    assert len(reader.pages) == len(previous.pages)
    assert all(a.extract_text() == b.extract_text()
               for a, b in zip(reader.pages[1:], previous.pages[1:])), name
    text = reader.pages[0].extract_text()
    assert 'Oumar Haidara Fall' in text
    assert 'Rubén Ramos Balsa' in text
    assert 'Manuscrito de recopilación para transferencia académica' in text
    assert 'Coautoría sin prelación de contribución' in text
    assert 'Integración y recopilación documental generadas por ChatGPT - Astra.' in text
    assert text.count('Integración y recopilación documental generadas por ChatGPT - Astra.') == 1
    assert ('Resumen' if prefix == 'vi' else 'Presentación') in text
    if prefix == 'vi':
        assert 'Palabras clave' in text
        assert 'especificado en cada sección' in text
        assert 'Identidad estructural y magnitud de masa' in reader.pages[1].extract_text()
    pdfs.append({'pdf': str(path), 'sha256': sha(path), 'pages': len(reader.pages),
                 'first_page_png': str(ROOT / 'technical/QA_APERTURA' / (prefix + '-001.png')),
                 'all_pages_after_opening_text_identical_to_rev02': True,
                 'rendered_and_visually_reviewed_pages': [1, 2, 3]})

logs = []
for path in sorted((ROOT / 'build_lectura').glob('*.log')):
    text = path.read_text(errors='replace')
    logs.append({'path': str(path.relative_to(ROOT)),
                 'overfull_count': len(re.findall(r'Overfull \\[hv]box', text)),
                 'missing_glyph_count': text.count('Missing character:'),
                 'undefined_reference_count': text.count('undefined references')})
report = {'status': 'PASS_APERTURAS_Y_PRESERVACION_FOCAL',
          'scope': 'Sólo apertura y maquetación inicial. Sin revisión matemática ni alteración del cuerpo.',
          'original_unchanged': str(OLD), 'changed_sources': sorted(changed),
          'unchanged_tex_count': len(preserved), 'unchanged_tex': preserved,
          'summary_preserved_exactly': True, 'catalogue_presentation_preserved_exactly': True,
          'pdfs': pdfs, 'compilation_logs': logs,
          'visual_notes': ['Título, autores y resumen/presentación en el mismo folio, sin portada separada.',
                           'VI: resumen íntegro y palabras clave caben en primera página a 10,5 puntos.',
                           'Catálogo: presentación íntegra; índice comienza en página 2.',
                           'La paginación del cuerpo y sus tablas cambia; sus fuentes permanecen idénticas.',
                           'Secciones principales en página nueva; subsecciones con reserva de espacio, sin salto forzado.',
                           'Penalización de partición reforzada para evitar fragmentos de una o dos líneas al inicio o final de página.']}
(ROOT / 'technical/QA_APERTURAS_RESTAURADAS.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ['status', 'unchanged_tex_count', 'pdfs', 'compilation_logs']}, ensure_ascii=False, indent=2))
