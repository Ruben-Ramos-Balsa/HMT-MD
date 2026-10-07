#!/usr/bin/env python3
"""Verify the two involution/fixed-space modules against frozen base279+coherence17.

No predecessor source or object, locality module, translation module, selector or
Mathlib dependency is recompiled. Every public declaration of the two new sources
is queried. A PASS certifies these declarations, not the twisted orbifold or FLM.
"""

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True

HELPER_SHA = 'f022db4decca339ed0873c08508b9a9a93b66a9ce711a3785526896870219939'
AUTH_HELPER_SHA = 'c16c63bfe0f9c95f7a5e767e8f8be5b1f67524496259f1618f9fe1043ece82a3'
COHERENCE_SHA = '620583b804d93d031a8abcdf94606ab20c3d7bf1c213cac5c3e7890c571098b8'
EXPECTED_MODULES = {'LatticeStateFieldParity', 'LatticeEvenVertexFields'}
ORDINARY_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def load(path, name, expected):
    import hashlib
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Helper changed: ' + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    here = Path(__file__).resolve().parent
    previous = here.parent / 'state_field'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=here)
    parser.add_argument('--report-dir', type=Path, default=here / 'involution_closed_results')
    parser.add_argument('--base', type=Path)
    parser.add_argument('--coherence-root', type=Path, default=previous)
    parser.add_argument('--coherence-report-dir', type=Path,
                        default=previous / 'normal_coherence_results')
    parser.add_argument('--helper', type=Path, default=previous / 'verify_state_field.py')
    parser.add_argument('--auth-helper', type=Path, default=here.parent /
                        'descendant_locality/verify_descendant_locality.py')
    parser.add_argument('--lean', type=Path, default=Path.home() /
                        '.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
    parser.add_argument('--mathlib', type=Path, default=Path('/Users/ruben/Documents/'
                        'ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4'))
    parser.add_argument('--timeout', type=int, default=900)
    args = parser.parse_args()
    for key in ('source_root', 'report_dir', 'coherence_root', 'coherence_report_dir',
                'helper', 'auth_helper'):
        setattr(args, key, getattr(args, key).expanduser().resolve())
    report = dict(schema='hmt.lean.involution.coherence.v1', status='RUNNING',
                  started_at_utc=datetime.now(timezone.utc).isoformat(), invocation=sys.argv,
                  predecessors_modified=False, predecessors_recompiled=False,
                  mathlib_rebuilt=False, selector_repeated=False, compiler_invoked=False,
                  scope='Full state-field parity equivariance and untwisted fixed-space restriction; '
                        'no twisted sector, orbifold or FLM assertion.',
                  allowed_delta_axioms=sorted(ORDINARY_AXIOMS), modules=[])
    writable = False
    helper = None
    try:
        if args.timeout <= 0:
            raise RuntimeError('Timeout must be positive')
        helper = load(args.helper, 'frozen_state_field_helpers', HELPER_SHA)
        auth = load(args.auth_helper, 'frozen_delta_authentication', AUTH_HELPER_SHA)
        report['runner_sha256'] = helper.sha(Path(__file__))
        coherence_path = args.coherence_report_dir / 'VERIFICATION.json'
        if helper.sha(coherence_path) != COHERENCE_SHA:
            raise RuntimeError('The coherence receipt is not the frozen successful cut')
        coherence_hint = json.loads(coherence_path.read_text())
        base = (args.base or Path(coherence_hint['base'])).expanduser().resolve()
        for protected in (base, args.coherence_report_dir):
            if (args.report_dir.is_relative_to(protected)
                    or protected.is_relative_to(args.report_dir)):
                raise RuntimeError('Report directory overlaps a predecessor')
        if args.report_dir.exists() and any(args.report_dir.iterdir()):
            raise RuntimeError('Use a fresh report directory; existing results are preserved')
        args.report_dir.mkdir(parents=True, exist_ok=True)
        writable = True
        verifier, old, base_sources, _, base_build = helper.authenticate_base(base)
        tracked = {args.helper: HELPER_SHA, args.auth_helper: AUTH_HELPER_SHA,
                   Path(__file__).resolve(): report['runner_sha256']}
        coherence, c_sources, _, c_build = auth.authenticate_delta(
            helper, verifier, coherence_path, COHERENCE_SHA, args.coherence_root,
            17, base_sources, tracked)
        inherited = {**base_sources, **c_sources}
        nodes, order, external, old_imports = auth.source_plan(verifier,
            [args.source_root], ['LatticeEvenVertexFields'], inherited)
        if set(nodes) != EXPECTED_MODULES:
            raise RuntimeError('Unexpected delta closure: ' + ', '.join(nodes))
        report.update(base=str(base), base_manifest_sha256=helper.BASE_MANIFEST_SHA,
                      base_receipt_sha256=helper.BASE_RECEIPT_SHA,
                      coherence_receipt_sha256=COHERENCE_SHA,
                      inherited_module_count=len(inherited), sources=nodes,
                      dependency_order=order, direct_inherited_imports=old_imports,
                      helper_sha256=HELPER_SHA, auth_helper_sha256=AUTH_HELPER_SHA)
        lean, mathlib, paths, compiler = helper.external_paths(args, old)
        report['compiler'] = compiler
        report['external_objects'] = {}
        external_names = set(external) | set(old['external_objects']) | set(coherence['external_objects'])
        for name in sorted(external_names):
            path = helper.object_for(name, paths)
            digest = helper.sha(path)
            for receipt in (old, coherence):
                witness = receipt['external_objects'].get(name)
                if witness and digest != witness.get('sha256', witness.get('object_sha256')):
                    raise RuntimeError('Inherited external object changed: ' + name)
            tracked[path] = digest
            report['external_objects'][name] = dict(path=str(path), sha256=digest)
        build = args.report_dir / 'build'
        build.mkdir()
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str,
            [build, c_build, base_build, *paths])))
        report['lean_path'] = env['LEAN_PATH']
        for name in order:
            node = nodes[name]
            source = Path(node['path'])
            if helper.sha(source) != node['sha256']:
                raise RuntimeError('Source changed before use: ' + name)
            snapshot, target = build / (name + '.lean'), build / (name + '.olean')
            snapshot.write_bytes(source.read_bytes())
            command = [str(lean), '-DwarningAsError=true', '--root=' + str(build),
                       '-o', str(target), str(snapshot)]
            print(name + ': compiling focal delta', flush=True)
            code, output = helper.run(command, mathlib, args.timeout, env=env)
            report['compiler_invoked'] = True
            (build / (name + '.log')).write_text(output, encoding='utf-8')
            row = dict(module=name, command=command, exit_code=code,
                       source_sha256=node['sha256'], output=output)
            report['modules'].append(row)
            if code:
                raise RuntimeError(f'Compilation failed for {name} ({code})\n{output}')
            if helper.sha(snapshot) != node['sha256'] or helper.sha(source) != node['sha256']:
                raise RuntimeError('Source changed during compilation: ' + name)
            row['object_sha256'] = helper.sha(target)
        queries = [q for n in order for q in nodes[n]['public_declarations']]
        if not queries or len(queries) != len(set(queries)):
            raise RuntimeError('Empty or duplicate public declarations')
        probe = ''.join('import ' + n + '\n' for n in order)
        probe += ''.join('#print axioms ' + q + '\n' for q in queries)
        (args.report_dir / 'axiom_probe.lean').write_text(probe, encoding='utf-8')
        code, output = helper.run([str(lean), '--stdin'], mathlib, args.timeout,
                                  env=env, stdin=probe)
        axioms = verifier.axiom_reports(output)
        report['axiom_probe'] = dict(exit_code=code, output=output, declarations=axioms)
        if code or set(axioms) != set(queries):
            raise RuntimeError('The public declaration probe is incomplete')
        if any(not set(values) <= ORDINARY_AXIOMS for values in axioms.values()):
            raise RuntimeError('Nonordinary axiom in the new delta')
        helper.authenticate_base(base)
        if any(helper.sha(path) != digest for path, digest in tracked.items()):
            raise RuntimeError('An inherited source, receipt or object changed')
        after, after_order, _, _ = auth.source_plan(verifier,
            [args.source_root], ['LatticeEvenVertexFields'], inherited)
        if nodes != after or order != after_order:
            raise RuntimeError('The focal source closure changed')
        if any(helper.sha(build / (row['module'] + '.olean')) != row['object_sha256']
               for row in report['modules']):
            raise RuntimeError('A focal compiled object changed')
        if helper.sha(lean) != helper.LEAN_SHA:
            raise RuntimeError('The compiler changed')
        report.update(status='PASS_INVOLUTION_COHERENCE_DELTA',
                      public_declaration_count=len(queries),
                      theorem_names=[q for n in order for q in nodes[n]['theorem_names']],
                      axioms=sorted({a for values in axioms.values() for a in values}),
                      predecessor_sources_objects_unchanged=True)
        exit_code = 0
    except Exception as error:
        report.update(status='FAIL_INVOLUTION_COHERENCE_DELTA',
                      error_type=type(error).__name__, error=str(error))
        exit_code = 1
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    receipt_path = args.report_dir / 'VERIFICATION.json'
    if writable:
        helper.write_json(receipt_path, report)
    print(json.dumps(dict(status=report['status'],
        receipt=str(receipt_path) if writable else None,
        compiled_modules=[r['module'] for r in report['modules']],
        public_declarations=report.get('public_declaration_count'),
        error=report.get('error')), indent=2, ensure_ascii=False))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
