#!/usr/bin/env python3
"""Portable source verifier for the consolidated HMT Lean package.

--plan checks the manifested local source closure without invoking a compiler.
The plan and compilation write receipts only in resultados/lean_unificado/.
Mathlib and its existing compiled dependencies are external prerequisites;
they are not rebuilt. No unreceipted local .olean is adopted as a cache hit.

The finite terminal selector uses native_decide/Lean.ofReduceBool. This trust
boundary is recorded explicitly; the verifier does not claim axiom-free
proofs, generation of every upstream input, or formalization of an entire PDF.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


LEAN_VERSION = '4.21.0'
MATHLIB_COMMIT = '308445d7985027f538e281e18df29ca16ede2ba3'
CACHE_VERSION = 1
MANDATORY_MODULES = (
    'TerminalReaders', 'TerminalInputs', 'TerminalOrbitalSelection',
    'SelectedTerminalAlpha', 'RegionalPanelBridge', 'SelectedFromRegionalInputs',
    'RegionalSixHundred', 'N69RegionalSignature', 'GeneratedN69Rows', 'RegionalW24',
    'GeneratedMarkedIncidence', 'WeightedIncidenceRecovery',
)
OPTIONAL_MODULE = 'SelectedRegionalIncidence'
SOURCE_ROOTS = ('lean/terminal', 'lean/regional', 'lean/incidencia', 'lean/biblioteca')
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}
EXTERNAL_PREFIXES = {'Mathlib', 'Lean', 'Init', 'Std', 'Batteries', 'Aesop', 'Qq',
                     'Plausible', 'ProofWidgets', 'ImportGraph', 'LeanSearchClient'}
MODULE_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9']*(?:\.[A-Za-z_][A-Za-z_0-9']*)*\Z")
PROBE_DECLARATIONS = (
    'HMT.I.TerminalSelector.terminal_selection',
    'HMT.I.TerminalSelector.terminal_selection_unique',
    'HMT.I.TerminalSelector.selected_register_recovery',
    'HMT.I.TerminalSelector.selected_terminal_alpha',
    'HMT.I.TerminalSelector.regionalPanel_eq',
    'HMT.I.TerminalSelector.regional_terminal_alpha',
    'HMT.I.RegionalW24.regionalW24_eq_input',
    'HMT.I.GeneratedMarkedIncidence.native_seed_incidence_lattice_composition',
    'HMT.KWeightedIncidenceRecovery.full_hexad_reading_injective',
    'HMT.KWeightedIncidenceRecovery.unique_recovered_register',
)
OPTIONAL_PROBE = 'HMT.I.SelectedRegionalIncidence.arithmetic_and_incidence_of_same_register'


def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha_file(path):
    with Path(path).open('rb') as handle:
        digest = hashlib.sha256()
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def digest_json(value):
    return sha_bytes(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def write_json(path, data):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def mask_comments_strings(text):
    """Preserve line positions while masking nested comments and strings."""
    output = list(text)
    i, depth, line, string = 0, 0, False, False
    while i < len(text):
        pair, char = text[i:i + 2], text[i]
        if line:
            if char == '\n':
                line = False
            else:
                output[i] = ' '
        elif depth:
            if pair == '/-':
                output[i:i + 2] = [' ', ' ']
                depth += 1
                i += 1
            elif pair == '-/':
                output[i:i + 2] = [' ', ' ']
                depth -= 1
                i += 1
            elif char != '\n':
                output[i] = ' '
        elif string:
            if char == '\\' and i + 1 < len(text):
                output[i:i + 2] = [' ', '\n' if text[i + 1] == '\n' else ' ']
                i += 1
            elif char == '"':
                output[i] = ' '
                string = False
            elif char != '\n':
                output[i] = ' '
        elif pair == '--':
            output[i:i + 2] = [' ', ' ']
            line = True
            i += 1
        elif pair == '/-':
            output[i:i + 2] = [' ', ' ']
            depth = 1
            i += 1
        elif char == '"':
            output[i] = ' '
            string = True
        i += 1
    if depth or string:
        raise RuntimeError('Unterminated Lean block comment or string')
    return ''.join(output)


def inspect_source(data, label):
    code = mask_comments_strings(data.decode('utf-8'))
    forbidden = re.search(r'\b(?:axiom|sorry|admit|sorryAx)\b', code)
    if forbidden:
        line = code.count('\n', 0, forbidden.start()) + 1
        raise RuntimeError(f'Forbidden local axiom/placeholder at {label}:{line}: {forbidden.group()}')
    imports = []
    for match in re.finditer(r'^\s*(?:public\s+)?import[ \t]+([^\n]+)', code, re.M):
        for name in match.group(1).split():
            if not MODULE_RE.fullmatch(name):
                raise RuntimeError(f'Unsupported import syntax in {label}: {name!r}')
            if name not in imports:
                imports.append(name)
    return imports, len(re.findall(r'#print\s+axioms\s+', code))


def axiom_reports(output):
    reports = {}
    pattern = r"'([^'\r\n]+)'\s+depends\s+on\s+axioms:\s*\[([^\]]*)\]"
    for match in re.finditer(pattern, output):
        reports[match.group(1)] = sorted(x.strip() for x in match.group(2).split(',') if x.strip())
    for match in re.finditer(r"'([^'\r\n]+)'\s+does not depend on any axioms", output):
        reports[match.group(1)] = []
    if re.search(r'\bsorryAx\b', output):
        raise RuntimeError('Lean output depends on sorryAx')
    unexpected = {a for values in reports.values() for a in values} - ALLOWED_AXIOMS
    if unexpected:
        raise RuntimeError('Unexpected proof axioms: ' + ', '.join(sorted(unexpected)))
    return reports


def load_plan(root):
    manifest_path = root / 'MANIFIESTO.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    entries = {}
    for record in manifest['files']:
        relative = Path(record['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise RuntimeError('Unsafe manifest path: ' + str(relative))
        key = relative.as_posix()
        if key in entries:
            raise RuntimeError('Duplicate manifest path: ' + key)
        entries[key] = record
    available, ignored = {}, []
    for source_root in SOURCE_ROOTS:
        directory = root / source_root
        if not directory.is_dir():
            raise RuntimeError('Missing package source directory: ' + source_root)
        for file in sorted(directory.rglob('*.lean')):
            if not file.resolve().is_relative_to(root):
                raise RuntimeError('Source resolves outside package: ' + str(file))
            relative = file.relative_to(root).as_posix()
            module = '.'.join(file.relative_to(directory).with_suffix('').parts)
            if relative not in entries:
                if module == OPTIONAL_MODULE:
                    ignored.append(relative)
                    continue
                raise RuntimeError('Unmanifested Lean source: ' + relative)
            raw = file.read_bytes()
            digest = sha_bytes(raw)
            if digest != entries[relative]['sha256']:
                raise RuntimeError('Manifest/source mismatch: ' + relative)
            imports, queries = inspect_source(raw, relative)
            node = dict(source=file, path=relative, sha256=digest, imports=imports,
                        query_count=queries, size=len(raw))
            if module in available:
                if available[module]['sha256'] != digest:
                    raise RuntimeError('Conflicting definitions of module: ' + module)
            else:
                available[module] = node
    focal = list(MANDATORY_MODULES)
    if OPTIONAL_MODULE in available:
        focal.append(OPTIONAL_MODULE)
    graph, order, visiting, external = {}, [], set(), set()

    def visit(name):
        if name in graph:
            return
        if name in visiting:
            raise RuntimeError('Cyclic local import: ' + name)
        if name not in available:
            raise RuntimeError('Missing local source: ' + name)
        visiting.add(name)
        node = available[name]
        for dependency in node['imports']:
            if dependency in available:
                visit(dependency)
            elif dependency.split('.')[0] in EXTERNAL_PREFIXES:
                external.add(dependency)
            else:
                raise RuntimeError(f'Missing local import {dependency} required by {name}')
        visiting.remove(name)
        graph[name] = node
        order.append(name)

    for module in focal:
        visit(module)
    return dict(root=str(root), manifest_sha256=sha_bytes(manifest_bytes),
                focal_modules=focal, optional_unmanifested_ignored=ignored,
                compile_order=order, graph=graph, external_modules=sorted(external))


def run(command, *, cwd, env=None, timeout=900, stdin=None):
    try:
        result = subprocess.run(command, cwd=cwd, env=env, input=stdin, text=True,
                                capture_output=True, timeout=timeout)
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired as error:
        def decoded(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else (value or '')
        return 124, decoded(error.stdout) + decoded(error.stderr) + f'\nTIMEOUT ({timeout}s)\n'


def checked(command, *, cwd, timeout):
    code, output = run(command, cwd=cwd, timeout=timeout)
    if code:
        raise RuntimeError(f'Command failed ({code}): {command!r}\n{output}')
    return output.strip()


def compile_plan(plan, args, receipt, report_dir):
    root = Path(plan['root'])
    if args.mathlib is None:
        raise RuntimeError('--mathlib is required for compilation, but not for --plan')
    mathlib = args.mathlib.expanduser().resolve()
    if not mathlib.is_dir():
        raise RuntimeError('--mathlib must identify an existing checkout with compiled dependencies')
    lean_found = shutil.which(args.lean)
    if lean_found is None:
        raise RuntimeError('Lean executable not found: ' + args.lean)
    initial_lean = str(Path(lean_found).resolve())
    prefix = Path(checked([initial_lean, '--print-prefix'], cwd=mathlib, timeout=args.timeout))
    actual_lean = prefix / 'bin' / 'lean'
    lean = str(actual_lean.resolve() if actual_lean.is_file() else Path(initial_lean))
    version = checked([lean, '--version'], cwd=mathlib, timeout=args.timeout)
    if f'version {LEAN_VERSION},' not in version:
        raise RuntimeError('Expected Lean ' + LEAN_VERSION + '; found ' + version)
    commit = checked(['git', 'rev-parse', 'HEAD'], cwd=mathlib, timeout=args.timeout)
    if commit != MATHLIB_COMMIT:
        raise RuntimeError('Expected Mathlib commit ' + MATHLIB_COMMIT + '; found ' + commit)
    lake = prefix / 'bin' / 'lake'
    lake_executable = str(lake) if lake.is_file() else shutil.which('lake')
    if lake_executable is None:
        raise RuntimeError('Lake executable not found')
    raw_paths = checked([lake_executable, 'env', 'printenv', 'LEAN_PATH'],
                        cwd=mathlib, timeout=args.timeout)
    library_paths = [(mathlib / item).resolve() for item in raw_paths.split(os.pathsep) if item]
    library_paths.append(prefix / 'lib' / 'lean')
    build = report_dir / 'build'
    build.mkdir(exist_ok=True)
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [build, *library_paths])))
    compiler = dict(version=version, executable=lean, binary_sha256=sha_file(lean),
                    mathlib_commit=commit, verifier_sha256=sha_file(Path(__file__)),
                    cache_version=CACHE_VERSION)
    receipt.update(compiler=compiler, mathlib=str(mathlib), lean_path=env['LEAN_PATH'])
    external = {}
    for module in plan['external_modules']:
        relative = Path(*module.split('.')).with_suffix('.olean')
        file = next((base / relative for base in library_paths if (base / relative).is_file()), None)
        if file is None:
            raise RuntimeError('Missing precompiled external dependency: ' + module)
        external[module] = dict(path=str(file), object_sha256=sha_file(file))
    receipt['external_objects'] = external
    cache_path = report_dir / 'CACHE.json'
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    if cache.get('format') != CACHE_VERSION:
        cache = dict(format=CACHE_VERSION, modules={})
    cache.setdefault('modules', {})
    completed = {}
    receipt['modules'] = []
    for module in plan['compile_order']:
        node = plan['graph'][module]
        dependency_hashes = {
            name: (dict(fingerprint=completed[name]['fingerprint'],
                        object_sha256=completed[name]['object_sha256'])
                   if name in completed else external[name]) for name in node['imports']}
        fingerprint = digest_json(dict(source_sha256=node['sha256'],
                                       dependencies=dependency_hashes, compiler=compiler))
        relative = Path(*module.split('.'))
        target = (build / relative).with_suffix('.olean')
        snapshot = (build / relative).with_suffix('.lean')
        log = (build / relative).with_suffix('.log')
        previous = cache['modules'].get(module, {})
        hit = (previous.get('fingerprint') == fingerprint and previous.get('exit_code') == 0
               and target.is_file() and previous.get('object_sha256') == sha_file(target))
        command = [lean, '-DwarningAsError=true', '--root=' + str(build),
                   '-o', str(target), str(snapshot)]
        record = dict(module=module, source=node['path'], source_sha256=node['sha256'],
                      dependencies=dependency_hashes, fingerprint=fingerprint,
                      command=command, cache_hit=hit)
        receipt['modules'].append(record)
        raw = node['source'].read_bytes()
        if sha_bytes(raw) != node['sha256']:
            raise RuntimeError('Source changed before verification: ' + module)
        if hit:
            code, output = 0, previous.get('output', '')
            print(module + ': verified cache hit', flush=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_bytes(raw)
            print(module + ': compiling source', flush=True)
            code, output = run(command, cwd=mathlib, env=env, timeout=args.timeout)
            log.write_text(output, encoding='utf-8')
        record.update(exit_code=code, output=output)
        record['axioms'] = axiom_reports(output)
        if code:
            raise RuntimeError(f'Lean compilation failed: {module} ({code})\n{output}')
        if len(record['axioms']) < node['query_count']:
            raise RuntimeError('Missing axiom reports requested by source: ' + module)
        if not target.is_file() or sha_file(node['source']) != node['sha256']:
            raise RuntimeError('Object absent or source changed after compilation: ' + module)
        record['object_sha256'] = sha_file(target)
        completed[module] = record
        cache['modules'][module] = record
        write_json(cache_path, cache)
    probe_declarations = list(PROBE_DECLARATIONS)
    if OPTIONAL_MODULE in plan['focal_modules']:
        probe_declarations.append(OPTIONAL_PROBE)
    probe = '\n'.join('import ' + name for name in plan['focal_modules']) + '\n'
    probe += ''.join('#print axioms ' + name + '\n' for name in probe_declarations)
    code, output = run([lean, '--stdin'], cwd=mathlib, env=env,
                       timeout=args.timeout, stdin=probe)
    reports = axiom_reports(output)
    receipt['axiom_probe'] = dict(source=probe, exit_code=code, output=output, declarations=reports)
    if code or set(reports) != set(probe_declarations):
        raise RuntimeError('Final theorem/axiom probe failed or omitted a declaration')
    for node in plan['graph'].values():
        if sha_file(node['source']) != node['sha256']:
            raise RuntimeError('Source changed during verification: ' + node['path'])
    if sha_file(root / 'MANIFIESTO.json') != plan['manifest_sha256']:
        raise RuntimeError('Manifest changed during verification')
    for value in external.values():
        if sha_file(value['path']) != value['object_sha256']:
            raise RuntimeError('External object changed during verification: ' + value['path'])
    for module, record in completed.items():
        target = (build / Path(*module.split('.'))).with_suffix('.olean')
        if sha_file(target) != record['object_sha256']:
            raise RuntimeError('Local object changed during verification: ' + module)
    if sha_file(lean) != compiler['binary_sha256']:
        raise RuntimeError('Compiler changed during verification')
    receipt['axioms'] = sorted({a for r in receipt['modules'] for aa in r['axioms'].values() for a in aa}
                              | {a for aa in reports.values() for a in aa})
    receipt.update(status='PASS_PORTABLE_LEAN_SOURCE_CLOSURE',
                   compiled_modules=[r['module'] for r in receipt['modules'] if not r['cache_hit']],
                   cached_modules=[r['module'] for r in receipt['modules'] if r['cache_hit']])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--root', type=Path, required=True, help='Root of the manifested portable package')
    parser.add_argument('--mathlib', type=Path, help='External Mathlib checkout, with compiled cache')
    parser.add_argument('--lean', default='lean', help='Lean executable, version 4.21.0')
    parser.add_argument('--plan', action='store_true', help='Check sources/imports without compiling; save PLAN.json')
    parser.add_argument('--timeout', type=int, default=900, help='Maximum seconds for each command')
    args = parser.parse_args()
    receipt = dict(schema='hmt.portable.lean.source.closure.v1', status='RUNNING',
                   started_at_utc=datetime.now(timezone.utc).isoformat(),
                   invocation=sys.argv, mathlib_rebuilt=False,
                   allowed_axioms=sorted(ALLOWED_AXIOMS),
                   native_evaluation='Finite selector permits Lean.ofReduceBool; not kernel-only reduction.',
                   whole_pdf_formalized=False,
                   source_files_modified=False,
                   scope='Compile the manifested source closure and check named declarations; preserve stated theorem hypotheses.')
    report_dir = None
    try:
        if args.timeout <= 0:
            raise RuntimeError('--timeout must be positive')
        root = args.root.expanduser().resolve()
        if not root.is_dir():
            raise RuntimeError('--root must identify an existing package directory')
        report_dir = root / 'resultados' / 'lean_unificado'
        report_dir.mkdir(parents=True, exist_ok=True)
        plan = load_plan(root)
        receipt.update(root=str(root), manifest_sha256=plan['manifest_sha256'],
                       focal_modules=plan['focal_modules'],
                       optional_unmanifested_ignored=plan['optional_unmanifested_ignored'],
                       local_module_count=len(plan['compile_order']),
                       compile_order=plan['compile_order'], external_modules=plan['external_modules'],
                       sources=[dict(module=n, path=plan['graph'][n]['path'],
                                     sha256=plan['graph'][n]['sha256'],
                                     imports=plan['graph'][n]['imports']) for n in plan['compile_order']])
        if args.plan:
            receipt.update(status='PASS_LOCAL_SOURCE_PLAN_NOT_COMPILED', compiler_invoked=False)
        else:
            compile_plan(plan, args, receipt, report_dir)
        code = 0
    except Exception as error:
        receipt.update(status='FAIL', error_type=type(error).__name__, error=str(error))
        code = 1
    receipt['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    if report_dir is not None:
        write_json(report_dir / ('PLAN.json' if args.plan else 'VERIFICATION.json'), receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2), flush=True)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
