#!/usr/bin/env python3
"""Pruebas de sensibilidad del verificador en copias temporales aisladas."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    base = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location('integration', base / 'pruebas/verificar_integracion_20260926.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    manifest = json.loads((base / module.MANIFEST).read_text())
    checks = []

    def record(name, success):
        checks.append({'test': name, 'passed': bool(success)})

    with tempfile.TemporaryDirectory(prefix='hmt_integration_falsifiers_') as directory:
        temporary = Path(directory)
        paths = {module.MANIFEST}
        for group in ('current_files', 'baseline_files', 'evidence_files', 'control_files'):
            paths.update(x['path'] for x in manifest[group])
        for relative in sorted(paths):
            destination = temporary / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(base / relative, destination)

        record('unmodified_portable_copy_passes', module.verify(temporary)['status'].startswith('PASS_'))

        baseline = temporary / manifest['baseline_files'][0]['path']
        data = baseline.read_bytes()
        baseline.unlink()
        result = module.verify(temporary)
        record('missing_baseline_snapshot_fails', result['status'].startswith('FAIL_') and
               any(x.get('hash_mismatch') == str(baseline.relative_to(temporary)) for x in result['errors']))
        baseline.write_bytes(data)

        proof_source = temporary / 'manuscrito/29_retorno_y_memoria_traslacional.tex'
        original = proof_source.read_text()
        modified = original.replace(r'\begin{proof}', r'\begin{proof} ALTERACION_DE_PRUEBA ', 1)
        proof_source.write_text(modified)
        result = module.verify(temporary)
        record('unrecorded_proof_change_fails', result['status'].startswith('FAIL_') and
               any('antecedent_proof_changed' in x for x in result['errors']))
        proof_source.write_text(original)

        body = temporary / 'manuscrito/cuerpo_en_desarrollo.tex'
        original = body.read_text()
        body.write_text(original + '\n' + r'\ref{FALSADOR_REFERENCIA_AUSENTE}' + '\n')
        result = module.verify(temporary)
        record('active_unresolved_reference_fails', result['status'].startswith('FAIL_') and
               any(x['label'] == 'FALSADOR_REFERENCIA_AUSENTE' for x in result['unresolved_references']))

        body.write_text(original + '\n' + r'\label{v:ant:sec:gravity}' + '\n')
        result = module.verify(temporary)
        record('active_duplicate_label_fails', result['status'].startswith('FAIL_') and
               'v:ant:sec:gravity' in result['duplicate_labels'])

        body.write_text(original + '\n' + r'\iffalse\label{v:ant:sec:gravity}\ref{FALSADOR_REFERENCIA_AUSENTE}\fi' + '\n')
        graph = module.scan(temporary / 'manuscrito')
        record('false_branch_is_preserved_but_inactive', not graph['errors'] and
               not graph['duplicate_labels'] and not graph['unresolved_references'])
        body.write_text(original)

        errors = []
        module.active_text(r'\ifnum1=1\input{unknown}\fi', 'fixture.tex', errors, [], [])
        record('unevaluated_structural_condition_fails', any('unevaluated_structural_condition' in x for x in errors))

        errors = []
        text = module.active_text(r'\iffalse A\iftrue B\else C\fi\else D\fi', 'fixture.tex', errors, [], [])
        record('nested_boolean_conditionals_and_else', not errors and text.strip() == 'D')

    result = {'schema': 'hmt.viii.documentary_checker_sensitivity.20260926.v1',
              'status': 'PASS_SENSIBILIDAD_CONTROL_DOCUMENTAL_VIII_20260926' if all(x['passed'] for x in checks)
                        else 'FAIL_SENSIBILIDAD_CONTROL_DOCUMENTAL_VIII_20260926',
              'checks': checks, 'check_count': len(checks), 'originals_modified': False,
              'scope': 'Sensibilidad del control documental en copias temporales; no certificación de teoremas.'}
    if args.receipt:
        args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    sys.exit(main())
