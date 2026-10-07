#!/usr/bin/env python3
"""Verifica el delta de maquetación y la integridad de las fuentes del cuerpo."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
old = root.parents[1] / 'APERTURAS_PAPER_RESTAURADAS_20260911_REV02/VII_GRAVITACION'
allowed = {'00_portada.tex', 'preambulo.tex'}
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
changes, identical = [], []
for source in sorted((old / 'manuscrito').rglob('*.tex')):
    relative = source.relative_to(old / 'manuscrito')
    destination = root / 'manuscrito' / relative
    assert destination.is_file(), str(relative)
    if sha(source) == sha(destination):
        identical.append(str(relative))
    else:
        changes.append(str(relative))
assert set(changes) == allowed, changes
before = (old / 'manuscrito/00_apertura.tex').read_text()
after = (root / 'manuscrito/00_apertura.tex').read_text()
original_summary = before.split('\\noindent\n', 1)[1].split('\\par\\endgroup', 1)[0]
new_summary = after.split('\\noindent\n', 1)[1].split('\\par\\endgroup', 1)[0]
assert original_summary == new_summary, 'Resumen no idéntico'
assert before.split('\\section{Introducción}', 1)[1] == after.split('\\section{Introducción}', 1)[1], 'Introducción no idéntica'
old_body = (old / 'manuscrito/cuerpo_en_desarrollo.tex').read_text()
new_body = (root / 'manuscrito/cuerpo_en_desarrollo.tex').read_text()
assert old_body == new_body
old_main = (old / 'manuscrito/main.tex').read_text()
new_main = (root / 'manuscrito/main.tex').read_text()
assert old_main == new_main
pdf = root / 'output/pdf/GRAVITACION_TORSION_DINAMICA_COSMOLOGICA.pdf'
reader = PdfReader(pdf)
old_pdf_reader = PdfReader(old / 'output/pdf/GRAVITACION_TORSION_DINAMICA_COSMOLOGICA.pdf')
assert len(reader.pages) == len(old_pdf_reader.pages)
assert all(new_page.extract_text() == old_page.extract_text()
           for new_page, old_page in zip(reader.pages[1:], old_pdf_reader.pages[1:])), 'Cambió texto maquetado después de primera página'
opening = reader.pages[0].extract_text()
assert 'Resumen' in opening and 'compatibilidad en la frontera.' in opening
assert '10 de septiembre de 2026' not in opening
assert 'Manuscrito de recopilación para transferencia académica' not in opening
assert 'Integración y recopilación documental generadas por ChatGPT - Astra.' not in opening
assert 'completitud geodésica causal' in opening
assert 'De la memoria orientada' not in opening
assert 'La asistencia de inteligencia artificial se utiliza' not in opening
assert 'Introducción' in reader.pages[1].extract_text()
result = {'status': 'PASS_APERTURA_CON_CUERPO_CONSERVADO',
          'scope': 'Restauración de apertura, no revisión matemática',
          'pdf': str(pdf), 'pdf_sha256': sha(pdf), 'pages': len(reader.pages),
          'source': str(old), 'changed_tex': changes, 'identical_tex': identical,
          'identical_tex_count': len(identical),
          'summary_verbatim': True, 'introduction_verbatim': True,
          'title_summary_same_page': True, 'introduction_page': 2,
          'pdf_text_pages_2_to_end_identical': True}
(root / 'gestion/CONTROL_APERTURA.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
(root / 'gestion/TEXTO_PRIMERAS_PAGINAS.txt').write_text('\n\n'.join(p.extract_text() for p in reader.pages[:3]))
print(json.dumps({k: v for k, v in result.items() if k != 'identical_tex'}, ensure_ascii=False, indent=2))
