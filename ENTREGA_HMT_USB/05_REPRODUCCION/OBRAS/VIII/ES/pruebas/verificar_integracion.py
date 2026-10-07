#!/usr/bin/env python3
"""Integración documental de VII; no certificación de amplitud física.

Comprueba las inclusiones TeX, las etiquetas, los entornos y las huellas
de los antecedentes conservados. Funciona desde cualquier directorio.
No compila ni modifica los artículos ya entregados.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(base):
    manuscript = base / 'manuscrito'
    visited, active = set(), set()
    labels, references, errors, inventory = {}, [], [], []

    def visit(relative):
        if relative in active:
            errors.append({'cycle': relative})
            return
        if relative in visited:
            return
        path = manuscript / relative
        if not path.is_file():
            errors.append({'missing_input': relative})
            return
        visited.add(relative)
        active.add(relative)
        original = path.read_text(encoding='utf-8')
        text = re.sub(r'(?<!\\)%[^\n]*', '', original)
        inventory.append({'file': relative, 'sha256': digest(path),
                          'proofs': text.count('\\begin{proof}')})
        for label in re.findall(r'\\label\{([^}]+)\}', text):
            labels.setdefault(label, []).append(relative)
        for ref in re.findall(r'\\(?:ref|eqref|cref|Cref|pageref|autoref)\{([^}]+)\}', text):
            references.extend((relative, x.strip()) for x in ref.split(','))
        stack = []
        for kind, name in re.findall(r'\\(begin|end)\{([^}]+)\}', text):
            if kind == 'begin':
                stack.append(name)
            elif not stack or stack.pop() != name:
                errors.append({'environment': name, 'file': relative})
        if stack:
            errors.append({'open_environments': stack, 'file': relative})
        for name in re.findall(r'\\(?:input|include)\{([^}]+)\}', text):
            visit(name if name.endswith('.tex') else name + '.tex')
        active.remove(relative)

    visit('cuerpo_en_desarrollo.tex')
    duplicates = {k: v for k, v in labels.items() if len(v) > 1}
    unresolved = [{'file': f, 'label': x} for f, x in references if x not in labels]
    preserved = []
    manifest = json.loads((base / 'MANIFIESTO_ANTECEDENTES_REV05.json').read_text())
    for entry in manifest['files']:
        path = manuscript / entry['destination']
        actual = digest(path) if path.is_file() else None
        preserved.append({'file': entry['destination'], 'sha256': actual,
                          'match': actual == entry['sha256']})
        if actual != entry['sha256']:
            errors.append({'changed_antecedent': entry['destination']})
    previous = json.loads((base / 'versiones/REV04/CONTROL_PROPUESTA.json').read_text())
    previous_proofs = []
    for entry in previous['proof_fragments_in_partial_assembly']:
        relative = entry['file']
        path = base / relative
        key = next((key for key in previous['proof_fragment_hashes']
                    if key.endswith('/' + relative)), None)
        exact = key is not None and digest(path) == previous['proof_fragment_hashes'][key]
        proof_identity = exact
        snapshot = base / 'versiones/REV04' / relative
        if not exact and snapshot.is_file():
            pattern = r'\\begin\{proof\}[\s\S]*?\\end\{proof\}'
            old_blocks = re.findall(pattern, snapshot.read_text())
            new_blocks = re.findall(pattern, path.read_text())
            proof_identity = (len(old_blocks) == entry['proofs']
                              and old_blocks == new_blocks)
        previous_proofs.append({'file': relative, 'proofs': entry['proofs'],
                                'whole_file_identical': exact,
                                'proofs_identical': proof_identity})
        if not proof_identity:
            errors.append({'previous_proof_changed': relative})
    result = {
        'status': 'PASS_INTEGRACION_DOCUMENTAL_VII' if not
                  (errors or duplicates or unresolved) else 'FAIL_INTEGRACION_DOCUMENTAL_VII',
        'scope': 'Incluye fuentes, huellas, referencias y entornos; no verifica por sí solo las pruebas matemáticas.',
        'files': sorted(inventory, key=lambda x: x['file']),
        'file_count': len(visited), 'label_count': len(labels),
        'proof_environment_count': sum(x['proofs'] for x in inventory),
        'preserved_antecedents': preserved, 'errors': errors,
        'preserved_previous_proofs': previous_proofs,
        'duplicate_labels': duplicates, 'unresolved_references': unresolved,
        'pdf_compiled': False, 'physical_amplitude_certified': False,
        'global_mathematical_certification': False,
        'script_sha256': digest(Path(__file__))
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    result = verify(Path(__file__).resolve().parents[1])
    if args.receipt:
        args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in
                     ['status', 'file_count', 'label_count', 'proof_environment_count',
                      'errors', 'duplicate_labels', 'unresolved_references',
                      'pdf_compiled', 'physical_amplitude_certified']}, ensure_ascii=False))
    if result['status'].startswith('FAIL'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
