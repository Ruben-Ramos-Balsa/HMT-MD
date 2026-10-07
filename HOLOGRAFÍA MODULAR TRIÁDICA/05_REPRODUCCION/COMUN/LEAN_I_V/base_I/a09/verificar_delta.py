#!/usr/bin/env python3
"""Compile the local state-field delta against the authenticated 279-module base.

No base source or object is modified, no terminal census is repeated, and no
Mathlib dependency is rebuilt. Every new public declaration is queried with
``#print axioms``. A successful receipt certifies exactly the recorded Lean
declarations, not an unlisted reconstruction or Moonshine theorem.

Dependencies can be relocated with --base, --mathlib and --lean. The frozen
binary objects require the exact compiler binary used for the sealed base;
otherwise rebuild that base from its own sources before making a new receipt.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True

BASE_NAME = 'PAQUETE_ARTICULO_I_COVARIANCIA_Y_FIRMA_20260920'
BASE_MANIFEST_SHA = 'f8b246dd18a35a60c4e02c31f7f3e9a4cc6a08a7f812f5ceddc87743300bd7ee'
BASE_RECEIPT_SHA = '019297aa9975b55fd817d51b4460558cfbaa2a058783f103c052fc8fb6d20f4d'
BASE_VERIFIER_SHA = '92cbae6c42d918a2b4b61c6cc9771a0af031d78cb5a916fcf99785b4d8fb539e'
BASE_RECEIPT = 'recibos/covariancia_firma/LEAN_CONJUNTO.json'
LEAN_SHA = 'c89073b8a577a5914ead7b740d2ad996af1ad5ad5b4bfc2825e0bce2f01b6aa4'
MATHLIB_COMMIT = '308445d7985027f538e281e18df29ca16ede2ba3'
ORDINARY_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
SELECTED_NAMESPACE = 'HMT.I.SelectedStateField'
DEFAULT_MATHLIB = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/'
                       'FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4')
DEFAULT_LEAN = Path.home() / '.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean'


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n',
                         encoding='utf-8')
    temporary.replace(path)


def run(command, cwd, timeout, env=None, stdin=None):
    try:
        result = subprocess.run(command, cwd=cwd, env=env, input=stdin,
                                capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else (value or '')
        return 124, decode(error.stdout) + decode(error.stderr) + '\nCOMMAND TIMEOUT\n'


def checked(command, cwd, timeout):
    code, output = run(command, cwd, timeout)
    if code:
        raise RuntimeError(f'Command failed ({code}): {command!r}\n{output}')
    return output.strip()


def relative_file(root, value):
    path = Path(value)
    if path.is_absolute() or '..' in path.parts:
        raise RuntimeError('Unsafe relative source path: ' + value)
    result = root / path
    if not result.resolve().is_relative_to(root.resolve()):
        raise RuntimeError('Source escapes root: ' + value)
    return result


def authenticate_base(base):
    for relative, expected in [('MANIFIESTO.json', BASE_MANIFEST_SHA),
                               (BASE_RECEIPT, BASE_RECEIPT_SHA),
                               ('verificar_lean.py', BASE_VERIFIER_SHA)]:
        if sha(base / relative) != expected:
            raise RuntimeError('Sealed base changed: ' + relative)
    manifest = json.loads((base / 'MANIFIESTO.json').read_text())
    receipt = json.loads((base / BASE_RECEIPT).read_text())
    if receipt['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE':
        raise RuntimeError('Base receipt is not a successful source closure')
    records = {row['module']: row for row in receipt['modules']}
    sources = {row['module']: row for row in receipt['sources']}
    if len(records) != 279 or len(sources) != 279 or records.keys() != sources.keys():
        raise RuntimeError('Base is not the complete sealed 279-module closure')
    entries = {row['path']: row for row in manifest['files']}
    spec = importlib.util.spec_from_file_location('sealed_state_field_verifier',
                                                 base / 'verificar_lean.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    build = base / 'resultados/lean_unificado/build'
    for name, source in sources.items():
        path = relative_file(base, source['path'])
        digest = sha(path)
        row = records[name]
        if (digest != source['sha256'] or digest != row['source_sha256']
                or entries.get(source['path'], {}).get('sha256') != digest):
            raise RuntimeError('Base source/manifest/receipt mismatch: ' + name)
        imports, _ = verifier.inspect_source(path.read_bytes(), str(path))
        if imports != source['imports'] or set(imports) != set(row['dependencies']):
            raise RuntimeError('Base import graph mismatch: ' + name)
        snapshot = (build / Path(*name.split('.'))).with_suffix('.lean')
        object_file = snapshot.with_suffix('.olean')
        if sha(snapshot) != digest or row['exit_code'] != 0:
            raise RuntimeError('Base snapshot is not its successful source: ' + name)
        if sha(object_file) != row['object_sha256']:
            raise RuntimeError('Base object mismatch: ' + name)
        for dependency, witness in row['dependencies'].items():
            if dependency in records:
                if (witness.get('object_sha256') != records[dependency]['object_sha256']
                        or witness.get('fingerprint') != records[dependency]['fingerprint']):
                    raise RuntimeError('Base dependency witness mismatch: ' + name)
            elif dependency not in receipt['external_objects']:
                raise RuntimeError('Base import has no external witness: ' + dependency)
    return verifier, receipt, sources, records, build


def inventory(verifier, root, base_sources):
    """A single explicit namespace per file keeps names unambiguous and auditable."""
    nodes = {}
    pattern = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)*(?:(noncomputable|unsafe)\s+)?'
                         r'(theorem|lemma|def|abbrev|structure|inductive|instance)\s+'
                         r'([A-Za-z_][\w\']*)', re.M)
    for path in sorted(root.glob('*.lean')):
        name = path.stem
        if name in base_sources:
            raise RuntimeError('A new module shadows a sealed module: ' + name)
        raw = path.read_bytes()
        imports, _ = verifier.inspect_source(raw, str(path))
        code = verifier.mask_comments_strings(raw.decode('utf-8'))
        if re.search(r'\bunsafe\s+(?:def|abbrev|instance|opaque)\b', code):
            raise RuntimeError('Unsafe declaration in new source: ' + name)
        namespaces = re.findall(r'^\s*namespace\s+([\w.]+)', code, re.M)
        if len(namespaces) != 1:
            raise RuntimeError('Use one explicit namespace per new module: ' + name)
        if re.search(r'\b(?:native_decide|ofReduceBool|ofReduceNat)\b', code):
            raise RuntimeError('New native-evaluation proof is not allowed in this delta: ' + name)
        if name == 'SelectedStateField' or namespaces[0] == SELECTED_NAMESPACE:
            if (name != 'SelectedStateField' or namespaces[0] != SELECTED_NAMESPACE
                    or set(imports) != {'LatticeStateFieldMap', 'SelectedMixedFieldLocality'}):
                raise RuntimeError('Selected-origin axiom exception requires its exact inherited imports')
        declarations, theorems = [], []
        for match in pattern.finditer(code):
            if match.group(1) == 'unsafe':
                raise RuntimeError('Unsafe declaration: ' + name)
            full_name = namespaces[0] + '.' + match.group(3)
            declarations.append(full_name)
            if match.group(2) in ('theorem', 'lemma'):
                theorems.append(full_name)
        if len(declarations) != len(set(declarations)):
            raise RuntimeError('Duplicate public declaration in module: ' + name)
        nodes[name] = dict(path=path.name, sha256=hashlib.sha256(raw).hexdigest(),
                           bytes=len(raw), imports=imports, namespace=namespaces[0],
                           public_declarations=declarations, theorem_names=theorems)
    if not nodes:
        raise RuntimeError('No local *.lean modules yet; no compilation claimed')
    order, active, seen, inherited, external = [], set(), set(), set(), set()

    def visit(name):
        if name in seen:
            return
        if name in active:
            raise RuntimeError('Cyclic delta imports: ' + name)
        active.add(name)
        for dependency in nodes[name]['imports']:
            if dependency in nodes:
                visit(dependency)
            elif dependency in base_sources:
                inherited.add(dependency)
            elif dependency.split('.')[0] in verifier.EXTERNAL_PREFIXES:
                external.add(dependency)
            else:
                raise RuntimeError(f'Unresolved import {dependency} in {name}')
        active.remove(name)
        seen.add(name)
        order.append(name)

    for name in nodes:
        visit(name)
    return nodes, order, sorted(inherited), sorted(external)


def external_paths(args, base_receipt):
    lean = args.lean.expanduser().resolve()
    mathlib = args.mathlib.expanduser().resolve()
    if sha(lean) != LEAN_SHA or sha(lean) != base_receipt['compiler']['binary_sha256']:
        raise RuntimeError('Compiler differs from the authenticated base object compiler')
    version = checked([str(lean), '--version'], mathlib, args.timeout)
    if 'version 4.21.0,' not in version:
        raise RuntimeError('Expected Lean 4.21.0; found ' + version)
    commit = checked(['git', 'rev-parse', 'HEAD'], mathlib, args.timeout)
    if commit != MATHLIB_COMMIT:
        raise RuntimeError('Mathlib revision differs from the authenticated base')
    prefix = Path(checked([str(lean), '--print-prefix'], mathlib, args.timeout))
    raw = checked([str(prefix / 'bin/lake'), 'env', 'printenv', 'LEAN_PATH'],
                  mathlib, args.timeout)
    paths = list(dict.fromkeys((mathlib / p).resolve() for p in raw.split(os.pathsep) if p))
    paths.append(prefix / 'lib/lean')
    return lean, mathlib, paths, dict(version=version, binary_sha256=sha(lean),
                                     executable=str(lean), mathlib_commit=commit)


def object_for(module, paths):
    relative = Path(*module.split('.')).with_suffix('.olean')
    file = next((p / relative for p in paths if (p / relative).is_file()), None)
    if file is None:
        raise RuntimeError('External object not found: ' + module)
    return file


def main():
    script_root = Path(__file__).resolve().parent
    outputs = next((p for p in script_root.parents if p.name == 'output'), None)
    default_base = (script_root / 'antecedente' if (script_root / 'antecedente').is_dir()
                    else (outputs / BASE_NAME if outputs else None))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=default_base)
    parser.add_argument('--source-root', type=Path,
                        default=(script_root / 'lean' if (script_root / 'lean').is_dir()
                                 else script_root))
    parser.add_argument('--report-dir', type=Path, default=script_root / 'resultados')
    parser.add_argument('--mathlib', type=Path, default=DEFAULT_MATHLIB)
    parser.add_argument('--lean', type=Path, default=DEFAULT_LEAN)
    parser.add_argument('--timeout', type=int, default=900)
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    root = args.source_root.expanduser().resolve()
    report_dir = args.report_dir.expanduser().resolve()
    report_dir.mkdir(parents=True, exist_ok=True)
    report = dict(schema='hmt.lean.state.field.delta.v1', status='RUNNING',
                  started_at_utc=datetime.now(timezone.utc).isoformat(), invocation=sys.argv,
                  base_modified=False, base_recompiled=False, mathlib_rebuilt=False,
                  declared_scope='Exact new declarations listed in this receipt; no implicit theorem promotion.',
                  allowed_new_axioms=sorted(ORDINARY_AXIOMS),
                  inherited_axiom_exception=dict(namespace=SELECTED_NAMESPACE,
                      extra_axioms=['Lean.ofReduceBool'],
                      reason='Inherited selected origin; no new native evaluation is permitted.'),
                  runner_sha256=sha(Path(__file__)), modules=[])
    try:
        if args.base is None or args.timeout <= 0:
            raise RuntimeError('--base and a positive --timeout are required')
        base = args.base.expanduser().resolve()
        verifier, old, sources, records, base_build = authenticate_base(base)
        nodes, order, inherited, extra_external = inventory(verifier, root, sources)
        report.update(base=str(base), source_root=str(root), base_manifest_sha256=BASE_MANIFEST_SHA,
                      base_receipt_sha256=BASE_RECEIPT_SHA, authenticated_base_modules=279,
                      sources=nodes, compile_order=order, direct_inherited_imports=inherited)
        if args.plan:
            report.update(status='PASS_STATE_FIELD_SOURCE_PLAN_NOT_COMPILED', compiler_invoked=False)
        else:
            lean, mathlib, paths, compiler = external_paths(args, old)
            report['compiler'] = compiler
            report['external_objects'] = {}
            for name in sorted(set(old['external_objects']) | set(extra_external)):
                path = object_for(name, paths)
                digest = sha(path)
                if name in old['external_objects'] and digest != old['external_objects'][name]['object_sha256']:
                    raise RuntimeError('External object changed since base verification: ' + name)
                report['external_objects'][name] = dict(path=str(path), sha256=digest)
            build = report_dir / 'build'
            build.mkdir(exist_ok=True)
            env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [build, base_build, *paths])))
            report['lean_path'] = env['LEAN_PATH']
            for name in order:
                node = nodes[name]
                source = root / node['path']
                if sha(source) != node['sha256']:
                    raise RuntimeError('Delta source changed before compilation: ' + name)
                snapshot = build / (name + '.lean')
                target = build / (name + '.olean')
                snapshot.write_bytes(source.read_bytes())
                command = [str(lean), '-DwarningAsError=true', '--root=' + str(build),
                           '-o', str(target), str(snapshot)]
                print(name + ': compiling new source', flush=True)
                code, output = run(command, mathlib, args.timeout, env=env)
                (build / (name + '.log')).write_text(output, encoding='utf-8')
                row = dict(module=name, source_sha256=node['sha256'], command=command,
                           exit_code=code, output=output, source_axiom_reports=verifier.axiom_reports(output))
                report['modules'].append(row)
                if code:
                    raise RuntimeError(f'Compilation failed for {name} ({code})\n{output}')
                if sha(source) != node['sha256'] or sha(snapshot) != node['sha256']:
                    raise RuntimeError('Delta source changed during compilation: ' + name)
                row['object_sha256'] = sha(target)
            queries = [q for name in order for q in nodes[name]['public_declarations']]
            if not queries or len(queries) != len(set(queries)):
                raise RuntimeError('Empty or conflicting public declaration inventory')
            probe = ''.join('import ' + name + '\n' for name in order)
            probe += ''.join('#print axioms ' + query + '\n' for query in queries)
            (report_dir / 'axiom_probe.lean').write_text(probe, encoding='utf-8')
            code, output = run([str(lean), '--stdin'], mathlib, args.timeout, env=env, stdin=probe)
            reports = verifier.axiom_reports(output)
            report['axiom_probe'] = dict(exit_code=code, output=output, declarations=reports)
            if code or set(reports) != set(queries):
                raise RuntimeError('Axiom probe failed or omitted a public declaration')
            bad = {q: values for q, values in reports.items()
                   if not set(values) <= (ORDINARY_AXIOMS | {'Lean.ofReduceBool'}
                       if q.startswith(SELECTED_NAMESPACE + '.') else ORDINARY_AXIOMS)}
            if bad:
                raise RuntimeError('Nonordinary axioms in new declarations: ' + json.dumps(bad))
            # Final immutability checks catch concurrent edits, not just stale snapshots.
            authenticate_base(base)
            final_nodes, final_order, _, _ = inventory(verifier, root, sources)
            if final_nodes != nodes or final_order != order:
                raise RuntimeError('The local source inventory changed during verification')
            for name, node in nodes.items():
                if sha(root / node['path']) != node['sha256']:
                    raise RuntimeError('Source changed while another module compiled: ' + name)
            for row in report['modules']:
                if sha(build / (row['module'] + '.olean')) != row['object_sha256']:
                    raise RuntimeError('Compiled delta object changed: ' + row['module'])
            for row in report['external_objects'].values():
                if sha(row['path']) != row['sha256']:
                    raise RuntimeError('External object changed during compilation: ' + row['path'])
            if sha(lean) != LEAN_SHA:
                raise RuntimeError('Compiler changed during compilation')
            report.update(status='PASS_STATE_FIELD_DELTA', compiler_invoked=True,
                          public_declaration_count=len(queries),
                          theorem_names=[q for name in order for q in nodes[name]['theorem_names']],
                          axioms=sorted({a for values in reports.values() for a in values}))
        exit_code = 0
    except Exception as error:
        report.update(status='FAIL_STATE_FIELD_DELTA', error_type=type(error).__name__, error=str(error))
        exit_code = 1
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    path = report_dir / ('PLAN.json' if args.plan else 'VERIFICATION.json')
    write_json(path, report)
    print(json.dumps(dict(status=report['status'], receipt=str(path),
                         compiled_modules=[r['module'] for r in report['modules']],
                         public_declarations=report.get('public_declaration_count'),
                         error=report.get('error')), indent=2, ensure_ascii=False))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
