#!/usr/bin/env python3
"""Authenticate a portable package and replay its explicitly selected Lean entries.

Default: reuse authenticated predecessor objects and recompile selected terminal
entries (including terminal entries required transitively by another article).
--from-sources: rebuild the complete local source closure of the selected entries.
No network access, installation, extraction, or automatic execution is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import time

ROOT = Path(__file__).absolute().parent
ARTICLES = ('I', 'II', 'III', 'IV', 'V')
ALLOWED_AXIOMS = {'propext', 'Quot.sound', 'Classical.choice', 'Lean.ofReduceBool'}
MODULE_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*\Z")
DIGEST = re.compile(r'[0-9a-f]{64}\Z')


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def safe_relative(value):
    require(isinstance(value, str) and bool(value), 'A relative path must be nonempty text')
    require('\\' not in value and ':' not in value and '\x00' not in value,
            'Unsupported or unsafe relative path: ' + repr(value))
    p = PurePosixPath(value)
    require(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts,
            'Path traversal is forbidden: ' + value)
    require(p.as_posix() == value, 'Noncanonical relative path: ' + value)
    require(bool(p.parts), 'Empty relative path')
    return p


def regular_file(path):
    mode = path.lstat().st_mode
    require(stat.S_ISREG(mode), 'Nonregular file or symlink: ' + str(path))


def inventory():
    require(not ROOT.is_symlink(), 'Package root must not be a symlink')
    files = {}
    for directory, dirs, names in os.walk(ROOT, followlinks=False):
        for name in dirs:
            p = Path(directory) / name
            require(not p.is_symlink(), 'Directory symlink is forbidden: ' + str(p))
        for name in names:
            p = Path(directory) / name
            regular_file(p)
            rel = p.relative_to(ROOT).as_posix()
            safe_relative(rel)
            files[rel] = sha(p)
    return files


def authenticate_package():
    manifest_path = ROOT / 'MANIFIESTO.json'
    regular_file(manifest_path)
    manifest = read_json(manifest_path)
    require(isinstance(manifest, dict) and isinstance(manifest.get('files'), dict),
            'MANIFIESTO.json requires a files object')
    expected = manifest['files']
    require('MANIFIESTO.json' not in expected,
            'Manifest must exclude its own self-referential hash')
    folded = set()
    for name, digest in expected.items():
        safe_relative(name)
        require(name.casefold() not in folded, 'Case-insensitive path collision: ' + name)
        folded.add(name.casefold())
        require(isinstance(digest, str) and DIGEST.fullmatch(digest), 'Invalid SHA-256 for ' + name)
    observed = inventory()
    manifest_digest = observed.pop('MANIFIESTO.json', None)
    missing, extra = set(expected) - set(observed), set(observed) - set(expected)
    require(not missing and not extra,
            f'Inventory mismatch: missing={sorted(missing)}, extra={sorted(extra)}')
    changed = [name for name in expected if expected[name] != observed[name]]
    require(not changed, 'Changed package files: ' + ', '.join(changed))
    require('REGISTRO_UNIFICADO.json' in expected, 'Registry is not bound by the manifest')
    require(Path(__file__).name in expected, 'Reproducer is not bound by the manifest')
    return expected, manifest_digest


def remove_comments(text):
    """Preserve line breaks while removing nested Lean block/line comments."""
    result, index, depth, quoted = [], 0, 0, False
    while index < len(text):
        pair = text[index:index + 2]
        ch = text[index]
        if depth:
            if pair == '/-':
                depth += 1
                result.extend('  ')
                index += 2
            elif pair == '-/':
                depth -= 1
                result.extend('  ')
                index += 2
            else:
                result.append('\n' if ch == '\n' else ' ')
                index += 1
        elif quoted:
            result.append(ch)
            index += 1
            if ch == '\\' and index < len(text):
                result.append(text[index])
                index += 1
            elif ch == '"':
                quoted = False
        elif ch == '"':
            quoted = True
            result.append(ch)
            index += 1
        elif pair == '/-':
            depth = 1
            result.extend('  ')
            index += 2
        elif pair == '--':
            end = text.find('\n', index)
            end = len(text) if end == -1 else end
            result.extend(' ' * (end - index))
            index = end
        else:
            result.append(ch)
            index += 1
    require(depth == 0, 'Unclosed Lean block comment in a registered source')
    return ''.join(result)


def source_imports(text, name):
    cleaned = remove_comments(text)
    imports = []
    for match in re.finditer(r'^\s*(?:(?:public|private)\s+)?import\s+([^\n]+)', cleaned, re.M):
        for token in match.group(1).split():
            require(MODULE_NAME.fullmatch(token), f'Unsupported import syntax in {name}: {token!r}')
            imports.append(token)
    require(len(imports) == len(set(imports)), 'Duplicate source import in ' + name)
    return imports, cleaned


def validate_registry(expected):
    registry = read_json(ROOT / 'REGISTRO_UNIFICADO.json')
    require(isinstance(registry, dict), 'Registry must be an object')
    modules, targets, compiler = (registry.get(k) for k in ('modules', 'targets', 'compiler'))
    require(isinstance(modules, dict) and bool(modules), 'Nonempty modules registry required')
    require(isinstance(targets, dict) and set(targets) == set(ARTICLES),
            'Targets must contain exactly I, II, III, IV and V')
    require(isinstance(compiler, dict), 'Compiler pin is required')
    for key in ('version', 'binary_sha256', 'mathlib_commit'):
        require(isinstance(compiler.get(key), str) and compiler[key], 'Missing compiler pin: ' + key)
    require(DIGEST.fullmatch(compiler['binary_sha256']), 'Invalid compiler binary hash')
    external_objects = registry.get('external_objects', {})
    require(isinstance(external_objects, dict), 'external_objects must be an object when present')
    for name, row in external_objects.items():
        require(MODULE_NAME.fullmatch(name), 'Invalid external module name: ' + repr(name))
        digest = row.get('sha256') if isinstance(row, dict) else row
        require(isinstance(digest, str) and DIGEST.fullmatch(digest),
                'Invalid pinned external object hash: ' + name)
    names_folded, sources, graph = set(), {}, {}
    for name, row in modules.items():
        require(MODULE_NAME.fullmatch(name), 'Unsupported local module name: ' + repr(name))
        require(name.casefold() not in names_folded, 'Case-insensitive module collision: ' + name)
        names_folded.add(name.casefold())
        require(isinstance(row, dict), 'Invalid module row: ' + name)
        for field, suffix in (('source', '.lean'), ('object', '.olean')):
            path = row.get(field)
            safe_relative(path)
            require(path.endswith(suffix), f'Wrong {field} extension for {name}')
            require(path in expected, f'{name} {field} is absent from manifest')
            require(row.get(field + '_sha256') == expected[path], f'{name} {field} hash disagrees with manifest')
        declared = row.get('imports')
        require(isinstance(declared, list) and all(isinstance(n, str) and MODULE_NAME.fullmatch(n) for n in declared),
                'Invalid imports list for ' + name)
        require(len(declared) == len(set(declared)), 'Duplicate registered imports for ' + name)
        actual, cleaned = source_imports((ROOT / row['source']).read_text(encoding='utf-8'), name)
        local_actual = set(actual) & set(modules)
        local_declared = set(declared) & set(modules)
        require(local_actual == local_declared,
                f'Incomplete or incorrect local imports for {name}: source={sorted(local_actual)}, registry={sorted(local_declared)}')
        # A registry may list only local imports or also include external imports.
        require(set(declared) <= set(actual), 'Registry declares nonexistent imports for ' + name)
        sources[name] = dict(imports=actual, clean_text=cleaned)
        graph[name] = local_actual
    for article, entries in targets.items():
        require(isinstance(entries, list) and entries and len(entries) == len(set(entries)),
                'Nonempty unique target list required for ' + article)
        require(all(isinstance(n, str) and n in modules for n in entries), 'Unregistered target in ' + article)
    indegree = {name: len(deps) for name, deps in graph.items()}
    dependents = {name: [] for name in modules}
    for name, dependencies in graph.items():
        for dep in dependencies:
            dependents[dep].append(name)
    ready = [name for name, count in indegree.items() if count == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        name = heapq.heappop(ready)
        order.append(name)
        for child in dependents[name]:
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(ready, child)
    require(len(order) == len(modules),
            'Local import cycle: ' + ', '.join(sorted(n for n, count in indegree.items() if count)))
    return registry, sources, graph, order


def closure(entries, graph):
    found, pending = set(), list(entries)
    while pending:
        name = pending.pop()
        if name not in found:
            found.add(name)
            pending.extend(graph[name])
    return found


def run_command(command, *, cwd=None, env=None, timeout=60):
    return subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                          text=True, timeout=timeout, check=False)


def lean_version(text):
    match = re.search(r'(?:version\s+)?(\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.]+)?)', text)
    require(match is not None, 'Could not parse Lean version: ' + text)
    return match.group(1)


def authenticate_runtime(args, compiler):
    lean, mathlib = args.lean.expanduser().resolve(), args.mathlib_root.expanduser().resolve()
    require(lean.is_file(), 'Lean executable not found')
    binary_hash = sha(lean)
    if not args.portable_toolchain:
        require(binary_hash == compiler['binary_sha256'], 'Lean executable hash mismatch')
    proc = run_command([str(lean), '--version'])
    require(proc.returncode == 0, 'lean --version failed: ' + proc.stderr)
    version = (proc.stdout + proc.stderr).strip()
    require(lean_version(version) == lean_version(compiler['version']), 'Lean version mismatch: ' + version)
    commit = run_command(['git', '-C', str(mathlib), 'rev-parse', 'HEAD'])
    require(commit.returncode == 0, 'Cannot read Mathlib git commit: ' + commit.stderr)
    require(commit.stdout.strip() == compiler['mathlib_commit'], 'Mathlib commit mismatch')
    roots = [mathlib / '.lake/build/lib/lean']
    roots += sorted((mathlib / '.lake/packages').glob('*/.lake/build/lib/lean'))
    roots += [lean.parent.parent / 'lib/lean']
    require(all(p.is_dir() for p in roots), 'Missing Mathlib or Lean object directory')
    return lean, roots, dict(executable=str(lean), binary_sha256=binary_hash,
        version=version, mathlib_root=str(mathlib), mathlib_commit=commit.stdout.strip(),
        binary_pin_enforced=not args.portable_toolchain)


def module_path(name, suffix):
    return Path(*name.split('.')).with_suffix(suffix)


def external_dependencies(selected_closure, sources, modules, roots, external_objects, enforce_pins):
    fingerprints, pin_checks = {}, {}
    for name in selected_closure:
        for imported in sources[name]['imports']:
            if imported in modules:
                continue
            relative = module_path(imported, '.olean')
            matches = [root / relative for root in roots if (root / relative).is_file()]
            require(matches, f'Import {imported} of {name} is neither registered nor available externally')
            # Reject differing objects for one import in separate search roots.
            digests = {sha(p) for p in matches}
            require(len(digests) == 1, 'Ambiguous external import: ' + imported)
            path = matches[0]
            actual_hash = sha(path)
            fingerprints[str(path)] = actual_hash
            row = external_objects.get(imported)
            pinned_hash = row.get('sha256') if isinstance(row, dict) else row
            if pinned_hash is not None and enforce_pins:
                require(actual_hash == pinned_hash, 'Pinned external object changed: ' + imported)
            pin_checks[imported] = dict(path=str(path), actual_sha256=actual_hash,
                pinned_sha256=pinned_hash,
                status=('MATCHED_PIN' if enforce_pins else 'PIN_SKIPPED_PORTABLE_SOURCE_BUILD')
                    if pinned_hash is not None else 'NO_REGISTERED_PIN')
    return fingerprints, pin_checks


def match_axiom_queries(expected, found, module):
    """One-to-one matching allows Lean to qualify a query inside a namespace."""
    require(len(expected) == len(found), 'Axiom-query count mismatch in ' + module)
    options = []
    for requested in expected:
        compatible = [i for i, (qualified, _) in enumerate(found)
                      if qualified == requested or qualified.endswith('.' + requested)]
        compatible.sort(key=lambda i: (found[i][0] != requested, i))
        options.append(compatible)
    matched_output = {}

    def assign(query, visited):
        for output in options[query]:
            if output in visited:
                continue
            visited.add(output)
            if output not in matched_output or assign(matched_output[output], visited):
                matched_output[output] = query
                return True
        return False

    for query in range(len(expected)):
        require(assign(query, set()),
                'Axiom-query output has no one-to-one qualified match in ' + module)
    query_output = {query: output for output, query in matched_output.items()}
    return [dict(requested=requested, resolved=found[query_output[i]][0])
            for i, requested in enumerate(expected)]


def axiom_report(cleaned_source, log, module):
    # The permitted foundational axioms belong to Lean's existing environment,
    # not to new declarations hidden in an unqueried local module.
    require(not re.search(r'^\s*(?:(?:private|protected|noncomputable|unsafe)\s+)*axioms?\b',
                          cleaned_source, re.M),
            'A registered compiled source declares a new axiom: ' + module)
    expected = re.findall(r"#print\s+axioms\s+([A-Za-z_][A-Za-z0-9_'.]*)", cleaned_source)
    commands = len(re.findall(r'#print\s+axioms\b', cleaned_source))
    require(commands == len(expected), 'Unsupported #print axioms target syntax in ' + module)
    found = []
    for match in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", log):
        names = [name.strip() for name in match.group(2).split(',') if name.strip()]
        found.append((match.group(1), names))
    for match in re.finditer(r"'([^']+)' does not depend on any axioms", log):
        found.append((match.group(1), []))
    matched_queries = match_axiom_queries(expected, found, module)
    for declaration, axioms in found:
        extra = set(axioms) - ALLOWED_AXIOMS
        require(not extra, f'Unapproved axioms in {declaration}: {sorted(extra)}')
    return dict(status='CHECKED_EXPLICIT_QUERIES' if expected else 'NOT_QUERIED',
        full_module_axiom_coverage_claimed=False,
        queries=matched_queries,
        declarations=[dict(name=name, axioms=axioms) for name, axioms in found],
        computational_dependency_present=any('Lean.ofReduceBool' in axioms for _, axioms in found))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true', help='Integrity/import checks only; do not invoke Lean')
    parser.add_argument('--article', choices=(*ARTICLES, 'all'), default='all')
    parser.add_argument('--from-sources', action='store_true', help='Compile the entire local target dependency closure')
    parser.add_argument('--portable-toolchain', action='store_true',
                        help='With --from-sources, require Lean version and Mathlib commit but not the platform-specific binary hash')
    parser.add_argument('--lean', type=Path)
    parser.add_argument('--mathlib-root', type=Path)
    parser.add_argument('--report-dir', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=600, help='Maximum seconds per Lean module')
    args = parser.parse_args()
    require(not args.portable_toolchain or args.from_sources,
            '--portable-toolchain requires --from-sources')
    require(args.timeout > 0, '--timeout must be positive')
    require(args.verify_only or (args.lean is not None and args.mathlib_root is not None),
            'Compilation requires --lean and --mathlib-root')
    out = args.report_dir.expanduser().resolve()
    require(not out.exists() and not out.is_relative_to(ROOT.resolve()),
            'Choose a fresh report directory outside the package')
    out.mkdir(parents=True)
    report = dict(status='RUNNING', article=args.article, from_sources=args.from_sources,
        verify_only=args.verify_only, compiler_invoked=False, modules=[],
        whole_manuscript_formalization_claimed=False, report_directory=str(out))
    started = time.time()
    try:
        expected, manifest_hash = authenticate_package()
        registry, sources, graph, order = validate_registry(expected)
        articles = ARTICLES if args.article == 'all' else (args.article,)
        selected = {n for article in articles for n in registry['targets'][article]}
        needed = closure(selected, graph)
        all_targets = {n for values in registry['targets'].values() for n in values}
        compile_set = needed if args.from_sources else needed & all_targets
        compile_order = [n for n in order if n in compile_set]
        report.update(manifest_sha256=manifest_hash, authenticated_files=len(expected),
            registered_modules=len(registry['modules']), selected_targets=sorted(selected),
            dependency_closure=sorted(needed), planned_compile_order=compile_order,
            reused_local_objects=sorted(needed - compile_set),
            compilation_policy='full_local_source_closure' if args.from_sources else 'terminal_entries_only')
        if not args.verify_only:
            lean, external_roots, runtime = authenticate_runtime(args, registry['compiler'])
            external_hashes, external_pins = external_dependencies(
                needed, sources, registry['modules'], external_roots,
                registry.get('external_objects', {}), not args.portable_toolchain)
            report.update(runtime=runtime, external_direct_import_objects=external_hashes,
                external_direct_import_pin_checks=external_pins,
                external_direct_import_pin_coverage_complete=all(
                    row['status'] == 'MATCHED_PIN' for row in external_pins.values()),
                external_transitive_object_hash_coverage_claimed=False)
            build, logs = out / 'build', out / 'logs'
            build.mkdir(); logs.mkdir()
            for name in sorted(needed - compile_set):
                row = registry['modules'][name]
                dest = build / module_path(name, '.olean')
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / row['object'], dest)
                require(sha(dest) == row['object_sha256'], 'Copied object changed: ' + name)
            environment = dict(os.environ)
            environment['LEAN_PATH'] = os.pathsep.join(map(str, [build] + external_roots))
            for name in compile_order:
                row = registry['modules'][name]
                source = build / module_path(name, '.lean')
                obj = build / module_path(name, '.olean')
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / row['source'], source)
                require(sha(source) == row['source_sha256'], 'Copied source changed: ' + name)
                require(not obj.exists(), 'Unexpected object before compilation: ' + name)
                command = [str(lean), '-DwarningAsError=true', '--root=' + str(build),
                           '-o', str(obj), str(source)]
                print('COMPILE', name, flush=True)
                report['compiler_invoked'] = True
                try:
                    proc = run_command(command, cwd=build, env=environment, timeout=args.timeout)
                except subprocess.TimeoutExpired as error:
                    def decoded(value):
                        return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value or ''
                    log_path = logs / (name + '.log')
                    log_path.write_text(decoded(error.stdout) + decoded(error.stderr), encoding='utf-8')
                    report['modules'].append(dict(module=name, command=command, exit_code=None,
                        timeout_seconds=args.timeout, log=str(log_path.relative_to(out)),
                        log_sha256=sha(log_path), source_sha256=sha(source)))
                    raise VerificationError('Lean compilation timed out for ' + name) from error
                log = proc.stdout + proc.stderr
                log_path = logs / (name + '.log')
                log_path.write_text(log, encoding='utf-8')
                item = dict(module=name, command=command, exit_code=proc.returncode,
                    source_sha256=sha(source), log=str(log_path.relative_to(out)), log_sha256=sha(log_path),
                    object=str(obj.relative_to(out)), object_sha256=sha(obj) if obj.exists() else None)
                report['modules'].append(item)
                require(proc.returncode == 0 and obj.is_file(), 'Lean compilation failed for ' + name)
                require(sha(source) == row['source_sha256'], 'Source changed during compilation: ' + name)
                item['axiom_scope'] = axiom_report(sources[name]['clean_text'], log, name)
                write_json(out / 'PROGRESS.json', report)
            require(sha(lean) == runtime['binary_sha256'], 'Lean binary changed during execution')
            commit_after = run_command(['git', '-C', runtime['mathlib_root'], 'rev-parse', 'HEAD'])
            require(commit_after.returncode == 0 and commit_after.stdout.strip() == runtime['mathlib_commit'],
                    'Mathlib commit changed during execution')
            changed_external = [p for p, digest in external_hashes.items() if sha(p) != digest]
            require(not changed_external, 'External objects changed during execution: ' + ', '.join(changed_external))
            # Authenticate build objects too: no later compilation may silently
            # modify a previously produced or copied dependency.
            for name in needed - compile_set:
                require(sha(build / module_path(name, '.olean')) == registry['modules'][name]['object_sha256'],
                        'Reused build object changed: ' + name)
            for item in report['modules']:
                require(sha(out / item['object']) == item['object_sha256'],
                        'Produced object changed after compilation: ' + item['module'])
        final_expected, final_manifest_hash = authenticate_package()
        require(final_expected == expected and final_manifest_hash == manifest_hash,
                'Package changed during execution')
        report.update(status='PASS_PACKAGE_INTEGRITY' if args.verify_only else 'PASS_SELECTED_LEAN_REPRODUCTION',
            package_unchanged=True, full_export_axiom_coverage_claimed=False,
            allowed_axioms=sorted(ALLOWED_AXIOMS),
            elapsed_seconds=round(time.time() - started, 3))
    except Exception as error:
        report.update(status='FAIL_PACKAGE_REPRODUCTION', error_type=type(error).__name__,
            error=str(error), elapsed_seconds=round(time.time() - started, 3))
        write_json(out / 'VERIFICATION.json', report)
        print(report['status'] + ': ' + str(error), file=sys.stderr)
        return 1
    write_json(out / 'VERIFICATION.json', report)
    print(report['status'], flush=True)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except VerificationError as error:
        print('FAIL_PACKAGE_REPRODUCTION: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
