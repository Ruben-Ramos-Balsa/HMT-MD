#!/usr/bin/env python3
"""Sucesor documental aditivo; las capturas íntegras son anexos de trabajo.

Comprueba integridad y referencias; no demuestra los resultados matemáticos.
"""
from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path('/Users/ruben/Documents/New project')
NEW = ROOT / 'REV04_RELECTURA_Y_JERARQUIA'
PARTS = [
    '30_RELECTURA_RETROSPECTIVA_Y_CORRECCIONES.md',
    '31_MICROINVENTARIO_K_Y_ENLACES.md',
    '32_DELTAS_LEAN_Y_PROCEDENCIA.md',
    '33_JERARQUIA_CAUSAL_Y_REALIZACIONES.md',
    '34_INTEGRACION_Y_CONTRATO_DE_COMPLETITUD.md',
]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def record(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': sha(raw), 'bytes': len(raw), 'lines': len(raw.splitlines())}

def save_new(path, text):
    raw = text.encode('utf-8')
    if path.exists():
        assert path.read_bytes() == raw, f'No se sobrescribe {path}'
    else:
        path.write_bytes(raw)

def main():
    for version in ('01', '02', '03'):
        old = json.loads((ROOT / f'MANIFIESTO_REV{version}.json').read_text())
        assert sha(Path(old['artifact']).read_bytes()) == old['artifact_sha256']
        for item in old['parts']:
            assert sha(Path(item['path']).read_bytes()) == item['sha256'], item['path']

    previous = ROOT / 'INVENTARIO_ACUMULATIVO_REV03.md'
    records = [record(p) for p in [previous] + [NEW / n for n in PARTS]]
    body = '# Inventario genealógico HMT — revisión acumulativa 04\n\n'
    body += ('19 de septiembre de 2026. Conserva literalmente REV03, REV02 y REV01. '
             'Añade la relectura autorizada de radion y Revisar tesis HMT desde cero, '
             'microinventario de K, deltas formales y jerarquía causal. '
             'Las conversaciones públicas completas y sus adjuntos se conservan por separado '
             'como memoria editorial, no como demostraciones.\n\n')
    body += '## Acceso a lo añadido\n\n'
    for name in PARTS:
        body += f'- [{name[:-3]}](<{NEW / name}>)\n'
    body += '\n'
    for r in records:
        path = Path(r['path'])
        text = path.read_text()
        assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', text), path
        body += f'\n<!-- BEGIN INTEGRAL {path.name}; SHA256={r["sha256"]} -->\n\n{text}\n<!-- END INTEGRAL {path.name} -->\n'
    for version in ('01', '02', '03'):
        assert (ROOT / f'INVENTARIO_ACUMULATIVO_REV{version}.md').read_text() in body

    links = re.findall(r'\]\(<(/[^>]+)>\)', body)
    missing = []
    for link in links:
        path = Path(unquote(re.sub(r':\d+(?:-\d+)?$', '', link)))
        if not path.exists():
            missing.append(link)
    assert not missing, missing

    capture = json.loads((NEW / 'conversaciones/MANIFIESTO_CAPTURA_AUTORAL.json').read_text())
    for thread in capture['threads']:
        name = thread['name']
        md = NEW / f'conversaciones/{name}_10_intervenciones_autorales.md'
        jp = NEW / f'conversaciones/{name}_10_intervenciones_autorales.json'
        assert sha(md.read_bytes()) == thread['markdown_sha256']
        assert sha(jp.read_bytes()) == thread['json_sha256']
        payload = json.loads(jp.read_text())
        assert sum(m['role'] == 'user' for m in payload['messages']) == 10
        assert all(m['text'] in md.read_text() for m in payload['messages'])
        for attachment in thread['attachments']:
            assert Path(attachment).read_text() in md.read_text(), attachment

    artifact = ROOT / 'INVENTARIO_ACUMULATIVO_REV04.md'
    save_new(artifact, body)
    supports = [record(p) for p in sorted(NEW.rglob('*')) if p.is_file()]
    manifest = {
        'artifact': str(artifact), 'artifact_sha256': sha(body.encode()), 'parts': records,
        'support_files': supports, 'rev01_preserved_verbatim': True,
        'rev02_preserved_verbatim': True, 'rev03_preserved_verbatim': True,
        'prior_part_hashes_unchanged': True, 'local_links_checked': len(links),
        'missing_local_links': [], 'public_conversation_messages': sum(t['public_messages'] for t in capture['threads']),
        'author_interventions': 20, 'attachments_preserved': 3,
        'other_threads_messaged': [], 'other_thread_files_modified': [],
        'all_dependencies_validated': False, 'mathematical_completeness_certified': False,
        'new_pdf_compilation': False, 'new_lean_compilation': False,
        'pdfs_modified': [], 'documentary_scope': 'INVENTARIO_ADITIVO_PROCEDENCIA_Y_JERARQUIA',
    }
    save_new(ROOT / 'MANIFIESTO_REV04.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

    rp = ROOT / 'RECIBO_CAUSAL_REV03.json'
    receipt = json.loads(rp.read_text())
    receipt.update({
        'artifact': str(artifact), 'artifact_sha256': manifest['artifact_sha256'],
        'result_id': 'INVENTARIO_DOCUMENTAL_GENERATIVO_HMT_20260919_REV04',
        'scope_note': 'Preservación literal REV01–REV03; relectura pública autorizada, productores/consumidores de K, deltas Lean y jerarquía. No es una demostración nueva ni una compilación Lean/PDF.',
        'current_source_map': str(NEW / PARTS[0]),
        'inherited_receipt': {'path': str(rp), 'sha256': sha(rp.read_bytes())},
    })
    receipt['genealogy']['source_locators'] = [f'{r["path"]}:1-{r["lines"]} sha256={r["sha256"]}' for r in records]
    receipt['result_boundary']['work_performed'] = [
        'Conservación literal de tres revisiones y de sus partes',
        'Captura íntegra de veinte intervenciones autorales, respuestas públicas y tres adjuntos',
        'Controles de no regresión derivados de casos concretos',
        'Microinventario de productores, lectores e incidencia de K',
        'Actualización documental de suplementos Lean posteriores sin recompilarlos',
        'Mapa de dependencias físicas, excepcionales y dimensionales',
    ]
    save_new(ROOT / 'RECIBO_CAUSAL_REV04.json', json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    refs = subprocess.check_output(['python3', '-I', '-S', str(PROJECT / 'PUBLICACION_HMT/SERIE_ARTICULOS_HMT/herramientas/render_referencias_serie.py')], cwd=PROJECT, text=True)
    save_new(ROOT / 'REFERENCIAS_SERIE_REV04.md', refs)
    print(json.dumps({k: manifest[k] for k in ('artifact', 'artifact_sha256', 'rev03_preserved_verbatim', 'local_links_checked', 'public_conversation_messages', 'author_interventions', 'attachments_preserved', 'new_pdf_compilation', 'new_lean_compilation')}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
