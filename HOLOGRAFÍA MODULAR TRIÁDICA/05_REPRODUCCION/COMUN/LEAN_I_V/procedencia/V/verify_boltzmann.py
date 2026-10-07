#!/usr/bin/env python3
"""Verify only the selected II -> III -> V thermal composition."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CORE = HERE.parent / 'II_CENTRAL'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def main():
    v_receipt = HERE / 'VERIFICATION.json'
    ii_receipt = CORE / 'verification_action_gravity_thermal/VERIFICATION.json'
    v = json.loads(v_receipt.read_text())
    ii = json.loads(ii_receipt.read_text())
    require(v['status'] == 'PASS_SELECTED_V_THERMAL_PUBLICATION', 'V receipt')
    require(ii['status'] == 'PASS_SELECTED_ACTION_GRAVITY_THERMAL', 'II receipt')
    inputs = {
        str(v_receipt): sha(v_receipt), str(ii_receipt): sha(ii_receipt),
        str(HERE / 'SelectedThermalPublication.lean'): v['source_sha256'],
        str(HERE / 'SelectedThermalPublication.olean'): v['object_sha256'],
        str(CORE / 'SelectedActionGravityThermal.lean'): ii['source_sha256'],
        str(CORE / 'verification_action_gravity_thermal/SelectedActionGravityThermal.olean'):
            ii['object_sha256'],
    }
    require(all(sha(p) == h for p, h in inputs.items()), 'changed imported source/object')
    require(sha(LEAN) == v['compiler']['binary_sha256'], 'compiler changed')
    source = HERE / 'SelectedBoltzmannRadiation.lean'
    source_sha = sha(source)
    roots = [str(CORE / 'verification_action_gravity_thermal')] + v['lean_path']
    command = [str(LEAN), '-DwarningAsError=true', '--root=' + str(HERE),
               '-o', str(HERE / 'SelectedBoltzmannRadiation.olean'), str(source)]
    run = subprocess.run(command, cwd=HERE,
        env=dict(os.environ, LEAN_PATH=os.pathsep.join(roots)), text=True, capture_output=True)
    output = run.stdout + run.stderr
    (HERE / 'SelectedBoltzmannRadiation.log').write_text(output)
    axioms = {name: [item.strip() for item in names.split(',') if item.strip()]
        for name, names in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output)}
    allowed = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}
    passed = (run.returncode == 0 and len(axioms) == 4 and
        all(set(names) <= allowed for names in axioms.values()) and
        sha(source) == source_sha and all(sha(p) == h for p, h in inputs.items()))
    receipt = dict(status='PASS_SELECTED_BOLTZMANN_RADIATION' if passed else
        'FAIL_SELECTED_BOLTZMANN_RADIATION', exit_code=run.returncode,
        source=str(source), source_sha256=source_sha, command=command,
        object_sha256=sha(HERE / 'SelectedBoltzmannRadiation.olean') if run.returncode == 0 else None,
        log_sha256=sha(HERE / 'SelectedBoltzmannRadiation.log'), axioms=axioms,
        imported_inputs=inputs, verifier_sha256=sha(__file__),
        scope='Selected II thermal coefficient, same returned action, III constitutive speed, V two-polarization occupation and Stefan flux.',
        explicit_parameters=['positive action unit U', 'positive velocity unit C',
            'positive clock unit t0', 'positive thermal section Theta', 'positive temperature T'],
        external_boltzmann_value_supplied=False, full_articles_I_V_claimed=False,
        antecedents_recompiled=False, validation_uses_optimization_sensitive_asserts=False)
    (HERE / 'VERIFICATION_BOLTZMANN.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(output)
    print(receipt['status'])
    require(passed, 'Selected Boltzmann composition failed')
    causal = json.loads((HERE / 'CAUSAL.json').read_text())
    causal.update(artifact=str(source), artifact_sha256=source_sha,
        result_id='SELECTED_II_III_V_BOLTZMANN_RADIATION', scope=receipt['scope'],
        explicit_posterior_inputs=receipt['explicit_parameters'],
        selected_thermal_coefficient='HMT.II.SelectedActionGravityThermal.thermalCoefficient U t0 Theta .pre',
        verification_receipt=str(HERE / 'VERIFICATION_BOLTZMANN.json'))
    causal['genealogy']['source_locators'] += [
        str(CORE / 'SelectedActionGravityThermal.lean') +
            ':thermalCoefficient_pos,return_preserves_transducer,unique_positive_transducer',
        str(source) + ':same_returned_action,selected_transducer_unique,selected_II_III_V_thermal_chain']
    causal['genealogy']['tpk']['action'] += (
        ' The radiation consumer now also specializes beta to the unique generated '
        'energy-temperature transducer of II and its positive thermodynamic temperature; '
        'the returned action is definitionally the same section in II and V.')
    causal_path = HERE / 'CAUSAL_BOLTZMANN.json'
    causal_path.write_text(json.dumps(causal, ensure_ascii=False, indent=2) + '\n')
    gate = subprocess.run([sys.executable, '-I', '-S',
        '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit', str(source), '--receipt', str(causal_path)], text=True, capture_output=True)
    print(gate.stdout, end='')
    require(gate.returncode == 0 and 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' in gate.stdout,
        gate.stdout + gate.stderr)

if __name__ == '__main__':
    main()
