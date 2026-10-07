#!/usr/bin/env python3
"""Verify one frozen normalization module on the portable sealed 406-module base.
The base --plan authenticates 388 ancestors without compiling; its 18 field
objects are added ahead of that relocated LEAN_PATH. Only this new source is
compiled, with its 19 embedded public axiom queries. No loose TF objects,
ancestor rebuild, documentary gate or package is produced.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RECEIPT_SHA = 'a40c091b74b9cc38ef28888437fbd96f07d8fbf8e84b05d7940202206e16980e'
SOURCE_SHA = '326bc7a5c2cfc080e8dcd82816a38254b5d1aa7b205267b5ba5158344db11f2b'
RUNNER_SHA = 'f3363670657b5bf030edf6d193ebadb2c6e822d77fcdcffb8044090feccf9906'
MANIFEST_SHA = '10a5a5de9b53b27d4324135db1e51a8992033a30bbedb501586ac11d2ff7acf9'
NAME = 'LatticeTwistedChargeNormalization'


def sha(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def authenticate(base):
    if sha(base/'MANIFIESTO.json') != MANIFEST_SHA:
        raise RuntimeError('Changed sealed package manifest')
    manifest = json.loads((base/'MANIFIESTO.json').read_text())
    for row in manifest['files']:
        path = (base/row['path']).resolve()
        if not path.is_relative_to(base) or sha(path) != row['sha256']:
            raise RuntimeError('Changed inherited package file: '+row['path'])
    if sha(base/'recibos/incremento/VERIFICATION.json') != RECEIPT_SHA:
        raise RuntimeError('Changed integrated field receipt')
    receipt = json.loads((base/'recibos/incremento/VERIFICATION.json').read_text())
    if {p.stem for p in (base/'recibos/incremento/build').glob('*.olean')} != set(receipt['sources']):
        raise RuntimeError('Unlisted object in the prefixed field build')
    return receipt


def main():
    import importlib.util
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--source', type=Path, default=HERE/(NAME+'.lean'))
    p.add_argument('--report-dir', type=Path, default=HERE/'normalization_results_20260922')
    p.add_argument('--timeout', type=int, default=600)
    args = p.parse_args()
    base, source, report_dir = args.base.resolve(), args.source.resolve(), args.report_dir.resolve()
    if (report_dir.exists() or report_dir.is_relative_to(base) or base.is_relative_to(report_dir)
            or source.is_relative_to(report_dir)):
        raise RuntimeError('Use a fresh report outside the sealed package and source')
    old = authenticate(base)
    runner_path = base/'verificar_campos_torcidos.py'
    if sha(runner_path) != RUNNER_SHA:
        raise RuntimeError('Changed frozen TF runner')
    spec = importlib.util.spec_from_file_location('normalization_frozen_tf', runner_path)
    tf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tf)
    vertex = base/'antecedente/antecedente/antecedente'
    helper = tf.load(vertex/'antecedente/antecedente/antecedente/verificar_delta.py',
        'f022db4decca339ed0873c08508b9a9a93b66a9ce711a3785526896870219939', 'normalization_helper')
    locality = tf.load(vertex/'antecedente/antecedente/verificar_localidad.py',
        'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3', 'normalization_inventory')
    report_dir.mkdir(parents=True)
    report = dict(status='RUNNING', started_at_utc=datetime.now(timezone.utc).isoformat(),
        runner_sha256=sha(__file__), base=str(base), base_manifest_sha256=MANIFEST_SHA,
        predecessor_receipt_sha256=RECEIPT_SHA,
        predecessors_recompiled=False, predecessors_modified=False, mathlib_rebuilt=False)
    try:
        command = [sys.executable, '-I', '-S', str(base/'reproducir.py'),
            '--report-dir', str(report_dir/'antecedent_plan'), '--plan']
        code, output = helper.run(command, base, args.timeout)
        (report_dir/'antecedent_plan.log').write_text(output)
        report['antecedent_plan'] = dict(command=command, exit_code=code, output=output)
        if code:
            raise RuntimeError('Antecedent authentication plan failed')
        plan = json.loads((report_dir/'antecedent_plan/PLAN.json').read_text())
        if plan['status'] != 'PASS_TWISTED_FIELDS_SOURCE_PLAN_NOT_COMPILED':
            raise RuntimeError('Antecedent plan is not successful')
        for key in ('sources', 'dependency_order', 'public_declaration_owners', 'predecessor_receipt_sha256'):
            if plan[key] != old[key]:
                raise RuntimeError('Changed inherited input: '+key)
        if plan['compiler_invoked'] or plan['modules'] or not plan['authenticated_inputs_unchanged']:
            raise RuntimeError('Antecedent authentication rebuilt modules')
        verifier = tf.load(Path(plan['base'])/'verificar_lean.py', helper.BASE_VERIFIER_SHA, 'normalization_parser')
        queries_old = [q for m in old['dependency_order'] for q in old['sources'][m]['public_declarations']]
        probe = old['axiom_probe']
        if (probe['exit_code'] or verifier.axiom_reports(probe['output']) != probe['declarations']
                or set(queries_old) != set(probe['declarations'])
                or any(not set(a) <= tf.ORDINARY for a in probe['declarations'].values())):
            raise RuntimeError('Incomplete inherited public axiom probe')
        for row in old['modules']:
            stem = row['module']; build = base/'recibos/incremento/build'
            if (row['exit_code'] or sha(build/(stem+'.olean')) != row['object_sha256']
                    or sha(build/(stem+'.lean')) != row['source_sha256']
                    or sha(build/(stem+'.log')) != row['log_sha256']):
                raise RuntimeError('Changed inherited object, snapshot or log: '+stem)
        if sha(source) != SOURCE_SHA:
            raise RuntimeError('Changed frozen normalization source')
        node = locality.inspect(verifier, source)
        queries = re.findall(r'^#print axioms\s+(\S+)\s*$', source.read_text(), re.M)
        if (node['public_declarations'] != queries or len(queries) != 19
                or len(node['theorem_names']) != 16
                or set(node['imports']) != {'LatticeTwistedPositiveEnergy', 'LatticeWeightShells'}):
            raise RuntimeError('Unexpected source closure or axiom queries')
        paths = [base/'recibos/incremento/build', *map(Path, plan['lean_path'].split(os.pathsep))]
        lean_path = os.pathsep.join(map(str, paths))
        tracked = {Path(v['path']):v['sha256'] for v in plan['external_objects'].values()}
        lean = Path(plan['compiler']['executable']); tracked[lean] = plan['compiler']['binary_sha256']
        build = report_dir/'build'
        build.mkdir()
        snapshot, obj = build/source.name, build/(NAME+'.olean')
        snapshot.write_bytes(source.read_bytes())
        command = [str(lean), '-DwarningAsError=true', '--root='+str(build), '-o', str(obj), str(snapshot)]
        code, output = helper.run(command, base, args.timeout, env=dict(os.environ, LEAN_PATH=lean_path))
        (report_dir/'compile.log').write_text(output)
        axioms = verifier.axiom_reports(output)
        report.update(command=command, exit_code=code, output=output, lean_path=lean_path,
            source=node, public_declarations=queries, theorem_names=node['theorem_names'],
            axiom_queries=axioms, authenticated_predecessor_modules=388+len(old['modules']))
        if code or set(axioms) != set(queries) or any(not set(a) <= tf.ORDINARY for a in axioms.values()):
            raise RuntimeError('Normalization compilation or complete ordinary axiom query failed')
        authenticate(base)
        if any(sha(f) != h for f,h in tracked.items()) or sha(source) != SOURCE_SHA or sha(snapshot) != SOURCE_SHA:
            raise RuntimeError('Authenticated input changed during focal compilation')
        report.update(status='PASS_CHARGE_NORMALIZATION_DELTA', object_sha256=sha(obj),
            source_sha256=SOURCE_SHA, log_sha256=sha(report_dir/'compile.log'),
            axioms=sorted({a for values in axioms.values() for a in values}), authenticated_inputs_unchanged=True)
    except Exception as error:
        report.update(status='FAIL_CHARGE_NORMALIZATION_DELTA', error=str(error))
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    helper.write_json(report_dir/'VERIFICATION.json', report)
    print(json.dumps(dict(status=report['status'], receipt=str(report_dir/'VERIFICATION.json'), error=report.get('error'))))
    return 0 if report['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
