#!/usr/bin/env python3
"""Ensamblaje aditivo y controles exactos focales; no certificación global."""
from pathlib import Path
from fractions import Fraction as F
from urllib.parse import unquote
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path('/Users/ruben/Documents/New project')
NEW = ROOT / 'REV05_DETALLE_JUSTIFICATIVO'
ATTACHMENT = Path('/Users/ruben/.codex/attachments/cdd9ec9b-cee2-4372-9f10-d0949eb63e45/pasted-text.txt')
PARTS = ['35_DELTAS_DEL_EJEMPLO_CKM.md', '36_MODELO_DE_EXPOSICION_JUSTIFICATIVA.md',
         '37_DECISION_Y_ORDEN_DE_REDACCION.md']

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def record(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': sha(raw), 'bytes': len(raw), 'lines': len(raw.splitlines())}

def save_new(path, value):
    raw = value.encode('utf-8') if isinstance(value, str) else value
    if path.exists():
        assert path.read_bytes() == raw, f'No se sobrescribe {path}'
    else:
        path.write_bytes(raw)

def save_json(path, obj):
    save_new(path, json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def focal_checks():
    for p in range(1, 13):
        pairs = {(i, j) for i in range(p) for j in range(p)}
        orbits = {frozenset({(i, j), (j, i)}) for i, j in pairs}
        weight = sum((F(len(o), 2) for o in orbits), F(0))
        assert len(orbits) == p * (p + 1) // 2
        assert weight == F(p * p, 2)
    M = [[F(2), F(-5), F(28)], [F(0), F(7), F(-25, 2)],
         [F(1), F(-20), F(-2, 3)]]
    row = [1528, 3380, 801]
    assert [sum(row[i] * M[i][j] for i in range(3)) for j in range(3)] == [3857, 0, 0]
    det = sum(M[0][i] * (M[1][(i+1)%3] * M[2][(i+2)%3] -
                        M[1][(i+2)%3] * M[2][(i+1)%3]) for i in range(3))
    assert det == F(-3857, 6)
    for n90 in range(37):
        for n120 in range(37):
            n, d = n90+n120, 90*n90+120*n120
            assert (4*n-F(d, 30), F(d, 30)-3*n) == (n90, n120)
            assert d % 30 == 0 and 90*n <= d <= 120*n
            assert 90*(36-n90)+120*(36-n120) == 7560-d
    return {'status': 'PASS_CONTROLES_EXACTOS_FOCALES_REV05',
            'orbital_support_sizes_checked': list(range(1, 13)),
            'ckm_row_identity_exact': True, 'ckm_determinant': str(det),
            'occupation_pairs_checked': 37*37, 'occupation_inverse_exact': True,
            'scope': 'Comprobaciones racionales finitas; las pruebas generales están en la prosa y las fuentes.',
            'new_lean_compilation': False, 'metrological_targets_used': False}

def main():
    for v in ('01', '02', '03', '04'):
        m = json.loads((ROOT / f'MANIFIESTO_REV{v}.json').read_text())
        assert sha(Path(m['artifact']).read_bytes()) == m['artifact_sha256']
        for r in m['parts']:
            assert sha(Path(r['path']).read_bytes()) == r['sha256'], r['path']
    copy = NEW / 'ADJUNTO_INTEGRO_CKM_20260919.md'
    save_new(copy, ATTACHMENT.read_bytes())
    checks = focal_checks()
    save_json(NEW / 'CONTROLES_EXACTOS_FOCALES.json', checks)
    previous = ROOT / 'INVENTARIO_ACUMULATIVO_REV04.md'
    records = [record(p) for p in [previous] + [NEW/n for n in PARTS] + [copy]]
    body = '# Inventario genealógico HMT — revisión acumulativa 05\n\n'
    body += ('19 de septiembre de 2026. Conserva literalmente REV01–REV04. '
             'Añade el detalle justificativo recuperado del ejemplo CKM, una muestra '
             'de redacción y el orden de trabajo. El adjunto se conserva íntegro como '
             'memoria documental; no se convierte automáticamente en prosa del tratado.\n\n')
    for n in PARTS:
        body += f'- [{n[:-3]}](<{NEW/n}>)\n'
    for r in records:
        p = Path(r['path'])
        body += f'\n<!-- BEGIN INTEGRAL {p.name}; SHA256={r["sha256"]} -->\n\n'
        body += p.read_text() + f'\n<!-- END INTEGRAL {p.name} -->\n'
    for v in ('01', '02', '03', '04'):
        assert (ROOT/f'INVENTARIO_ACUMULATIVO_REV{v}.md').read_text() in body
    assert ATTACHMENT.read_bytes() == copy.read_bytes()
    assert ATTACHMENT.read_text() in body
    missing = []
    links = re.findall(r'\]\(<(/[^>]+)>\)', body)
    for link in links:
        p = Path(unquote(re.sub(r':\d+(?:-\d+)?$', '', link)))
        if not p.exists():
            missing.append(link)
    for n in PARTS:
        for link in re.findall(r'\]\(<(/[^>]+)>\)', (NEW/n).read_text()):
            assert Path(unquote(re.sub(r':\d+(?:-\d+)?$', '', link))).exists(), link
    artifact = ROOT / 'INVENTARIO_ACUMULATIVO_REV05.md'
    save_new(artifact, body)
    manifest = {'artifact': str(artifact), 'artifact_sha256': sha(body.encode()),
                'parts': records, 'support_files': [record(p) for p in sorted(NEW.iterdir()) if p.is_file()],
                'prior_revisions_preserved_verbatim': ['01', '02', '03', '04'],
                'prior_part_hashes_unchanged': True, 'attachment_source': record(ATTACHMENT),
                'attachment_preserved_byte_for_byte': True,
                'local_links_checked': len(links), 'missing_local_links': sorted(set(missing)),
                'focal_checks': checks, 'all_dependencies_validated': False,
                'mathematical_completeness_certified': False, 'new_pdf_compilation': False,
                'new_lean_compilation': False, 'pdfs_modified': [], 'other_threads_messaged': [],
                'documentary_scope': 'INVENTARIO_ADITIVO_Y_MODELO_DE_REDACCION_JUSTIFICATIVA'}
    save_json(ROOT/'MANIFIESTO_REV05.json', manifest)
    rp = ROOT/'RECIBO_CAUSAL_REV04.json'
    receipt = json.loads(rp.read_text())
    receipt.update({'artifact': str(artifact), 'artifact_sha256': manifest['artifact_sha256'],
                    'result_id': 'INVENTARIO_DOCUMENTAL_GENERATIVO_HMT_20260919_REV05',
                    'scope_note': 'Delta documental aditivo, ejemplo de prosa y comprobaciones racionales focales; sin dictamen global ni compilación PDF/Lean.',
                    'current_source_map': str(NEW/PARTS[0]),
                    'inherited_receipt': {'path': str(rp), 'sha256': sha(rp.read_bytes())}})
    receipt['genealogy']['source_locators'] = [f'{r["path"]}:1-{r["lines"]} sha256={r["sha256"]}' for r in records]
    receipt['result_boundary']['work_performed'] = ['Preservación literal REV01–REV04 y adjunto',
        'Seis deltas de incidencia, recuperación y memoria con fuentes',
        'Muestra de prosa justificativa y orden de redacción',
        'Lectura del adaptador CKM desde la base compartida sin recompilación',
        'Controles racionales focales sin valores metrológicos de entrada']
    save_json(ROOT/'RECIBO_CAUSAL_REV05.json', receipt)
    refs = subprocess.check_output(['python3','-I','-S',str(PROJECT/'PUBLICACION_HMT/SERIE_ARTICULOS_HMT/herramientas/render_referencias_serie.py')], cwd=PROJECT, text=True)
    save_new(ROOT/'REFERENCIAS_SERIE_REV05.md', refs)
    print(json.dumps({'artifact': record(artifact), 'preserved': manifest['prior_revisions_preserved_verbatim'],
                      'attachment_byte_exact': True, 'local_links_checked': len(links),
                      'missing_links': manifest['missing_local_links'], 'focal_checks': checks}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
