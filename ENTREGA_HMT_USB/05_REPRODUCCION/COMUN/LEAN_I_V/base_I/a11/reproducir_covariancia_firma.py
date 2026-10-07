#!/usr/bin/env python3
"""Replay the inherited closure and probe every new public declaration."""
from pathlib import Path
import contextlib
import importlib.util
import json
import re
import subprocess
import sys

sys.dont_write_bytecode = True
SECTION = 'causal_covariance_successor'
DELTA = 'deltas/covariancia_firma'
ORDINARY_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
SECTIONS = [
    ('vacuum_products_successor', 'deltas/productos'),
    ('charged_locality_successor', 'deltas/localidad'),
    ('generated_enrichment_mixed_successor', 'deltas/integracion'),
    ('survival_register_successor', 'deltas/supervivencia'),
    ('iterated_selector_signature_successor', 'deltas/selector'),
    ('joint_reading_transport_successor', 'deltas/lectura_conjunta'),
    ('incidence_orientation_successor', 'deltas/incidencias_orientaciones'),
    (SECTION, DELTA),
]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def declaration_queries(verifier, sources):
    """A fixed namespace per source; private helpers are checked transitively."""
    queries, inventory = [], {}
    pattern = re.compile(
        r'^\s*(?:(noncomputable|unsafe)\s+)?'
        r'(theorem|lemma|def|abbrev|structure|inductive|instance)\s+'
        r'([A-Za-z_][\w\']*)', re.M)
    for name, row in sources.items():
        raw = Path(row['path']).read_bytes()
        verifier.inspect_source(raw, str(row['path']))
        code = verifier.mask_comments_strings(raw.decode('utf-8'))
        namespaces = re.findall(r'^\s*namespace\s+([\w.]+)', code, re.M)
        if namespaces != [row['namespace']]:
            raise RuntimeError('Review changed namespace nesting: ' + name)
        found = []
        for match in pattern.finditer(code):
            if match.group(1) == 'unsafe':
                raise RuntimeError('Unsafe declaration in new proof module: ' + name)
            found.append(row['namespace'] + '.' + match.group(3))
        if not found or len(found) != len(set(found)):
            raise RuntimeError('Missing or duplicate declaration names: ' + name)
        inventory[name] = {
            'namespace': row['namespace'], 'public_declarations': found,
            'private_helpers_checked_transitively': len(re.findall(
                r'^\s*private\s+(?:theorem|lemma|def)\s+', code, re.M)),
        }
        queries.extend(found)
    return sorted(queries), inventory


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFIESTO.json').read_text())
    section = manifest[SECTION]
    if '--plan' not in sys.argv:
        result = subprocess.run([sys.executable, '-I', '-S',
                                 str(root / 'comprobar_datos_incidencia.py')])
        if result.returncode:
            return result.returncode
    chain = load_module('covariance_chain_runner', root / 'reproducir_cadena.py')
    verifier = chain.configure(root)
    for key, directory in SECTIONS:
        verifier.SOURCE_ROOTS += (directory,)
        verifier.MANDATORY_MODULES += tuple(manifest[key]['modules'])
    sources = {name: dict(path=root / DELTA / (name + '.lean'),
                         namespace=section['source_metadata'][name]['namespace'])
               for name in section['modules']}
    queries, inventory = declaration_queries(verifier, sources)
    if queries != section['axiom_queries']:
        raise RuntimeError('New declaration inventory differs from the manifest')
    # Retain the previous entry probes and inspect ALL new public declarations.
    verifier.PROBE_DECLARATIONS = tuple(dict.fromkeys([
        *manifest['incidence_orientation_successor']['integration_queries'],
        *section['activated_axiom_queries'], *queries]))
    sys.argv = [sys.argv[0], '--root', str(root), *sys.argv[1:]]
    log = root / 'resultados/covariancia_firma.log'
    log.parent.mkdir(exist_ok=True)
    with log.open('w') as stream, contextlib.redirect_stdout(stream):
        code = verifier.main()
    receipt = root / 'resultados/lean_unificado' / (
        'PLAN.json' if '--plan' in sys.argv else 'VERIFICATION.json')
    data = json.loads(receipt.read_text())
    if not code and '--plan' not in sys.argv:
        reports = data.get('axiom_probe', {}).get('declarations', {})
        bad = {q: reports.get(q) for q in [*queries, *section['activated_axiom_queries']]
               if q not in reports or not set(reports[q]) <= ORDINARY_AXIOMS}
        if data.get('local_module_count') != section['expected_module_count'] or bad:
            code = 1
            data['status'] = 'FAIL_CAUSAL_COVARIANCE_JOINT_PROBE'
            data['error'] = dict(expected_modules=section['expected_module_count'],
                                 failed_new_declarations=bad)
        data['causal_covariance_probe'] = {
            'all_new_public_declarations': queries, 'inventory': inventory,
            'new_axioms_allowed': sorted(ORDINARY_AXIOMS),
            'private_helpers_are_transitive_dependencies': True,
        }
        receipt.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(status=data['status'], returncode=code,
        modules=data.get('local_module_count'), new_declarations=len(queries),
        compiled=len(data.get('compiled_modules', [])),
        cached=len(data.get('cached_modules', [])), error=data.get('error'),
        receipt=str(receipt), log=str(log)), indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
