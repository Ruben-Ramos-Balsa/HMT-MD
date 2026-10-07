#!/usr/bin/env python3
"""Conservación documental portátil REV06→REV07. No invoca TeX ni skills."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {'00_apertura.tex', '33_corriente_espinorial_y_densidad.tex', 'cuerpo_en_desarrollo.tex'}

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    delta = read(ROOT / 'gestion/revision07/DELTA_EDITORIAL.json')
    baseline_path = ROOT / 'preservacion/revision06/gestion/MANIFIESTO_ENTREGA_VII.json'
    require(sha(baseline_path) == delta['baseline_manifest']['sha256'], 'Manifiesto previo alterado.')
    baseline = read(baseline_path)
    preserved = []
    for row in baseline['files']:
        current = ROOT / row['path']
        prior = ROOT / 'preservacion/revision06' / row['path']
        if current.is_file() and sha(current) == row['sha256']:
            continue
        require(prior.is_file() and sha(prior) == row['sha256'], 'Archivo previo no conservado: ' + row['path'])
        preserved.append(row['path'])
    rows = {r['path']: r for r in delta['changes']}
    require(set(rows) == EXPECTED, 'El delta debe contener exactamente las tres fuentes autorizadas.')
    environment_counts = {}
    for name, row in rows.items():
        before_path = ROOT / row['preserved_before']
        after_path = ROOT / 'manuscrito' / name
        require(sha(before_path) == row['before_sha256'] and sha(after_path) == row['after_sha256'], 'Fuente cambiada: ' + name)
        before, after = before_path.read_text(), after_path.read_text()
        detail = row['exact_delta']
        if name.startswith('33_'):
            inserted = detail['inserted_text']
            require(after.count(inserted) == 1 and after.replace(inserted, '') == before, 'Párrafo33 no es la única adición.')
        elif name == '00_apertura.tex':
            expected = before
            require(len(detail['replacements']) == 3, 'Tres precisiones declaradas en apertura.')
            for change in detail['replacements']:
                require(expected.count(change['before']) == 1, 'Reemplazo ambiguo.')
                expected = expected.replace(change['before'], change['after'])
            require(expected == after, 'Apertura no corresponde al delta exacto.')
        else:
            reduced = after.replace('revisión de integración 07.', 'revisión de integración 06.')
            require(len(detail['movements']) == 3, 'Tres movimientos requeridos.')
            for title in detail['movements']:
                inserted = '\\part*{'+title+'}\n\\addcontentsline{toc}{part}{'+title+'}\n'
                require(reduced.count(inserted) == 1, 'Movimiento no único.')
                reduced = reduced.replace(inserted, '')
            require(reduced == before, 'La secuencia de inclusiones cambió.')
        pattern = r'\\begin\{(theorem|lemma|proposition|corollary|definition|proof)\*?\}(.*?)\\end\{\1\*?\}'
        old_blocks = re.findall(pattern, before, re.S)
        require(old_blocks == re.findall(pattern, after, re.S), 'Enunciado/prueba cambiado: ' + name)
        environment_counts[name] = len(old_blocks)
        require(re.findall(r'\\label\{([^}]+)\}', before) == re.findall(r'\\label\{([^}]+)\}', after), 'Etiqueta cambiada: ' + name)
    ledger = read(ROOT / 'gestion/preflight_s0/runs/editorial_rev07/LEDGER_MANUSCRITO.json')
    for row in ledger['source_files']:
        require(sha(ROOT / 'manuscrito' / row['path']) == row['sha256'], 'Ledger desactualizado: ' + row['path'])
    require(len(delta['verifiers_preserved']) == 13, 'Trece verificadores requeridos.')
    for row in delta['verifiers_preserved']:
        require(sha(ROOT / row['path']) == row['sha256'], 'Verificador modificado: ' + row['path'])
    driver = runpy.run_path(str(ROOT / 'gestion/compilar_portable_VII.py'), run_name='portable_binding_only')
    graph = driver['source_graph']()
    require(not graph['errors'] and not graph['duplicate_labels_in_sources'], 'Grafo inválido.')
    preflight = ROOT / 'gestion/preflight_s0/runs/editorial_rev07/RECIBO_PRECOMPILACION.json'
    binding = driver['verify_preflight'](preflight, graph)
    report = {'schema': 'hmt.vii.editorial_conservation.v1', 'status': 'PASS_CONSERVACION_EDITORIAL_VII_REV07',
        'baseline_files_preserved': len(baseline['files']), 'preserved_in_historical_location': preserved,
        'changed_manuscript_sources': sorted(EXPECTED), 'active_sources': len(ledger['source_files']),
        'environments_preserved_in_changed_files': environment_counts, 'verifiers_preserved': 13,
        'preflight_payload_and_local_bindings_valid': True, 'source_merkle_sha256': binding['source_merkle_sha256'],
        'scientific_claims_unchanged': True, 'whole_article_mathematical_certification': False,
        'scope': 'Conservación documental, tres deltas exactos y enlace real a preflight previo. No certificación matemática global.'}
    if args.receipt:
        args.receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
