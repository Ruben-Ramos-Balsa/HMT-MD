#!/usr/bin/env python3
"""Compile only the V consumer, reusing existing checked objects."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORKSPACE = Path('/Users/ruben/Documents/New project')
PRINCIPAL = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916')
SEALED_I = WORKSPACE / 'output/PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922'
MATHLIB = PRINCIPAL / 'deps/mathlib4'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
SOURCE = HERE / 'SelectedThermalPublication.lean'
EXPECTED_SYMMETRIC = 'e984a8466c33cd77ef593d0eba010d57c28b24443ad49e3a52e2e2a4c1489cc4'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def require(condition, message):
    """Validation remains active under Python optimization (-O/-OO)."""
    if not condition:
        raise RuntimeError(message)

def main():
    registry_path = SEALED_I / 'REGISTRO_REPRODUCCION.json'
    registry = json.loads(registry_path.read_text())
    require(sha(LEAN) == registry['compiler']['binary_sha256'],
            'Lean compiler binary hash does not match the sealed registry')
    require(subprocess.check_output(['git', '-C', str(MATHLIB), 'rev-parse', 'HEAD'], text=True).strip() == registry['compiler']['mathlib_commit'],
            'Mathlib revision does not match the sealed registry')
    inherited = {str(registry_path): sha(registry_path)}
    i_roots = []
    for module, item in registry['modules'].items():
        obj = SEALED_I / item['object']
        require(sha(obj) == item['object_sha256'],
                'Changed sealed inherited object: ' + module)
        inherited[str(obj)] = item['object_sha256']
        if obj.parent not in i_roots:
            i_roots.append(obj.parent)
    v_roots = [PRINCIPAL / name for name in
        ['V_FockTransport', 'V_FockBridge', 'V_QuantumOccupations',
         'V_Radiation', 'V_BosonicMoments', 'V_ThermodynamicLimit']]
    roots = [HERE, HERE.parent / 'III'] + i_roots + v_roots
    roots += [MATHLIB / '.lake/build/lib/lean']
    roots += sorted((MATHLIB / '.lake/packages').glob('*/.lake/build/lib/lean'))
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, roots)))
    for path in [HERE.parent / 'III' / name for name in
        ['SelectedConstitutivePublication.lean', 'SelectedConstitutivePublication.olean',
         'ElectricQuanta.olean', 'ActionElectricComposition.olean']]:
        inherited[str(path)] = sha(path)
    for directory in v_roots:
        for path in sorted(directory.glob('*.olean')):
            inherited[str(path)] = sha(path)
    symmetric = HERE / 'SymmetricModes.lean'
    original = WORKSPACE / 'output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/contributions/reviewer/V_FockTransport/SymmetricModes.lean'
    require(sha(symmetric) == sha(original) == EXPECTED_SYMMETRIC,
            'SymmetricModes is not the unchanged checked antecedent')
    inherited[str(original)] = EXPECTED_SYMMETRIC
    # The exact preserved theorem source lacked its persistent object.
    # Rebuild only this unchanged local copy when the object is unavailable.
    if not (HERE / 'SymmetricModes.olean').exists():
        cmd = [str(LEAN), '-DwarningAsError=true', '--root=' + str(HERE),
               '-o', str(HERE / 'SymmetricModes.olean'), str(symmetric)]
        run = subprocess.run(cmd, cwd=HERE, env=env, text=True, capture_output=True)
        (HERE / 'SymmetricModes.log').write_text(run.stdout + run.stderr)
        require(run.returncode == 0,
                'SymmetricModes compilation failed:\n' + run.stdout + run.stderr)
    inherited[str(HERE / 'SymmetricModes.olean')] = sha(HERE / 'SymmetricModes.olean')
    inherited[str(symmetric)] = EXPECTED_SYMMETRIC
    source_hash = sha(SOURCE)
    require(not re.search(r'(?m)^\s*(axiom|sorry)\b|\bby\s+sorry\b', SOURCE.read_text()),
            'Consumer source contains a prohibited axiom or sorry declaration')
    command = [str(LEAN), '-DwarningAsError=true', '--root=' + str(HERE),
               '-o', str(HERE / 'SelectedThermalPublication.olean'), str(SOURCE)]
    run = subprocess.run(command, cwd=HERE, env=env, text=True, capture_output=True)
    output = run.stdout + run.stderr
    log = HERE / 'SelectedThermalPublication.log'
    log.write_text(output)
    axioms = {name: [v.strip() for v in values.split(',') if v.strip()]
              for name, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output)}
    allowed = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}
    checks = [run.returncode == 0, len(axioms) == 10,
              all(set(v) <= allowed for v in axioms.values()), sha(SOURCE) == source_hash,
              all(sha(p) == h for p, h in inherited.items())]
    result = {
        'status': 'PASS_SELECTED_V_THERMAL_PUBLICATION' if all(checks) else 'FAIL_SELECTED_V_THERMAL_PUBLICATION',
        'verifier': str(Path(__file__).resolve()), 'verifier_sha256': sha(__file__),
        'validation_uses_optimization_sensitive_asserts': False,
        'source': str(SOURCE), 'source_sha256': source_hash,
        'object': str(HERE / 'SelectedThermalPublication.olean'),
        'object_sha256': sha(HERE / 'SelectedThermalPublication.olean') if run.returncode == 0 else None,
        'compiler': registry['compiler'], 'command': command, 'exit_code': run.returncode,
        'lean_path': list(map(str, roots)), 'axioms': axioms,
        'log': str(log), 'log_sha256': sha(log),
        'inherited_artifacts': inherited,
        'source_manuscripts': [
            '05/ES/source/sections/30_fock_gibbs.tex',
            '05/ES/source/sections/69_enlace_constitutivo_velocidad.tex',
            '05/ES/source/sections/70_radiacion_termica.tex',
            '05/ES/source/sections/71_limite_termodinamico.tex'],
        'same_selected_regional_register': True,
        'parameters': {'hbar': 'SelectedAction.action_domain.hbarRet',
                       'c': 'SelectedConstitutivePublication.speed * positive_velocity_unit',
                       'a': 'beta*hbar*c', 'b': 'hbar*c',
                       'polarizations': 2, 'chemical_potential': 0, 'zero_mode_excluded_before_sum': True},
        'explicit_inputs': ['positive action unit U', 'positive velocity unit C',
                            'positive Gibbs beta', 'positive radial frequency/momentum',
                            'positive thermal transducer and temperature for Stefan specialization'],
        'whole_article_formalized': False, 'new_axioms_or_sorry': False,
        'mathlib_rebuilt': False, 'sealed_sources_changed': False,
        'reused_theorem_source_recompiled': {'SymmetricModes': 'exact hash-identical copy only; missing persistent object'},
        'scope': 'Selected I-III outputs into two explicit orthonormal Fock modes, mu=0 BE occupation; all three periodic nonzero-mode limits, summability, radial integrability, Planck density and Stefan flux. Free homogeneous three-dimensional posterior realization; not an interacting theory or completed Fock trace.'}
    (HERE / 'VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n')
    print(output)
    print(result['status'])
    if not all(checks):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
