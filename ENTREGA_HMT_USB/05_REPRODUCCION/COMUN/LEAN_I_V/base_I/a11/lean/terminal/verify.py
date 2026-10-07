#!/usr/bin/env python3
"""Incrementally verify the finite terminal selector and its alpha composition.

Only the six focal modules and their reachable article/regional dependencies
are compiled. Mathlib's existing objects are reused, never rebuilt. A cache
entry is trusted only when source/dependency/compiler fingerprints and the
resulting object hash match. Existing objects without this receipt are not
silently adopted, so the first run can compile the local dependency closure.

`native_decide` uses `Lean.ofReduceBool`: that axiom is recorded and explicitly
allowed alongside Lean's ordinary foundational axioms. Local `axiom`, `sorry`,
`admit`, and `sorryAx` are rejected. The regional bridge proves the panel and
N69 rows and W24 from the already generated regional prefixes. S8 remains
an explicit input: its provenance is not claimed by this verifier.

Optional --check-python PATH compares all 100 rows and every atlas key/mask
with the original verificar_selector_orbital_etiquetado.py. It is a diagnostic
parity test, not another proof of an HMT theorem.
"""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


HERE = Path(__file__).resolve().parent
DEFAULT_ARTICLE_LIBRARY = Path(
    '/Users/ruben/Documents/New project/output/'
    'AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/delivery/'
    'HMT_ARTICULO_I_FUENTES_Y_PRUEBAS_ES_EN_REV04B/lean'
)
DEFAULT_REGIONAL_LIBRARY = (
    HERE / 'regional' if (HERE / 'regional').is_dir() else
    Path('/Users/ruben/Documents/New project/output/IMPLEMENTACION_N69_REGIONAL_20260918')
)
FOCAL_MODULES = (
    'TerminalReaders', 'TerminalInputs', 'TerminalOrbitalSelection',
    'SelectedTerminalAlpha', 'RegionalPanelBridge', 'SelectedFromRegionalInputs',
)
EXPECTED_DECLARATIONS = (
    'HMT.I.TerminalSelector.terminal_selection',
    'HMT.I.TerminalSelector.terminal_selection_unique',
    'HMT.I.TerminalSelector.selected_register_digits',
    'HMT.I.TerminalSelector.selected_register_recovery',
    'HMT.I.TerminalSelector.selected_terminal_alpha',
    'HMT.I.TerminalSelector.regionalPanel_eq',
    'HMT.I.TerminalSelector.regional_terminal_alpha',
    'HMT.I.RegionalW24.regionalW24_eq_input',
)
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}
MODULE_NAME = re.compile(r'[A-Za-z_][A-Za-z_0-9\']*(?:\.[A-Za-z_][A-Za-z_0-9\']*)*\Z')
CACHE_FORMAT = 1


def sha256(path):
    with Path(path).open('rb') as handle:
        digest = hashlib.sha256()
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
        return digest.hexdigest()


def json_digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(payload).hexdigest()


def write_json(path, value):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def mask_comments_and_strings(text):
    """Keep code positions/newlines; mask nested Lean comments and strings."""
    result = list(text)
    index, depth, line_comment, string = 0, 0, False, False
    while index < len(text):
        pair = text[index:index + 2]
        char = text[index]
        if line_comment:
            if char == '\n':
                line_comment = False
            else:
                result[index] = ' '
        elif depth:
            if pair == '/-':
                result[index:index + 2] = [' ', ' ']
                depth += 1
                index += 1
            elif pair == '-/':
                result[index:index + 2] = [' ', ' ']
                depth -= 1
                index += 1
            elif char != '\n':
                result[index] = ' '
        elif string:
            if char == '\\' and index + 1 < len(text):
                result[index:index + 2] = [' ', '\n' if text[index + 1] == '\n' else ' ']
                index += 1
            elif char == '"':
                result[index] = ' '
                string = False
            elif char != '\n':
                result[index] = ' '
        elif pair == '--':
            result[index:index + 2] = [' ', ' ']
            line_comment = True
            index += 1
        elif pair == '/-':
            result[index:index + 2] = [' ', ' ']
            depth = 1
            index += 1
        elif char == '"':
            result[index] = ' '
            string = True
        index += 1
    if depth or string:
        raise RuntimeError('Unterminated Lean block comment or string')
    return ''.join(result)


def inspect_source(path):
    code = mask_comments_and_strings(path.read_text(encoding='utf-8'))
    forbidden = re.search(r'\b(?:axiom|sorry|admit|sorryAx)\b', code)
    if forbidden:
        line = code.count('\n', 0, forbidden.start()) + 1
        raise RuntimeError(f'Forbidden local axiom/placeholder at {path}:{line}: {forbidden.group()}')
    imports = []
    for match in re.finditer(r'^\s*(?:public\s+)?import[ \t]+([^\n]+)', code, re.M):
        for name in match.group(1).split():
            if not MODULE_NAME.fullmatch(name):
                raise RuntimeError(f'Unsupported import syntax in {path}: {name!r}')
            if name not in imports:
                imports.append(name)
    return imports


def axiom_reports(output):
    reports = {}
    for match in re.finditer(r"'([^'\r\n]+)'\s+depends\s+on\s+axioms:\s*\[([^\]]*)\]", output):
        reports[match.group(1)] = sorted(a.strip() for a in match.group(2).split(',') if a.strip())
    for match in re.finditer(r"'([^'\r\n]+)'\s+does not depend on any axioms", output):
        reports[match.group(1)] = []
    if re.search(r'\bsorryAx\b', output):
        raise RuntimeError('Lean output depends on sorryAx')
    unexpected = {axiom for values in reports.values() for axiom in values} - ALLOWED_AXIOMS
    if unexpected:
        raise RuntimeError('Unexpected proof axioms: ' + ', '.join(sorted(unexpected)))
    return reports


def execute(command, *, cwd, env, timeout, input_text=None):
    try:
        process = subprocess.run(command, cwd=cwd, env=env, text=True,
                                 input=input_text, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        def as_text(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else (value or '')
        return 124, as_text(error.stdout) + as_text(error.stderr) + f'\nTIMEOUT after {timeout} seconds\n'
    return process.returncode, process.stdout + process.stderr


def python_parity(owner_path, lean, build, mathlib, env, timeout, record):
    checker = HERE / 'CheckReaders.lean'
    inspect_source(checker)
    command = [lean, '--run', str(checker)]
    record.update(command=command, checker_sha256=sha256(checker),
                  python_owner=str(owner_path), python_owner_sha256=sha256(owner_path))
    code, output = execute(command, cwd=mathlib, env=env, timeout=timeout)
    record['exit_code'] = code
    if code:
        record['output'] = output
        raise RuntimeError('Lean reader diagnostic failed')
    actual, actual_rows, metadata = {}, [], None
    for line in output.splitlines():
        tag, *values = line.split(',')
        if tag == 'PAIR':
            key, mask = map(int, values)
            if key in actual:
                raise RuntimeError('Duplicate exported atlas key')
            actual[key] = mask
        elif tag == 'ROW':
            actual_rows.append(tuple(map(int, values)))
        elif tag == 'META':
            metadata = values
        else:
            raise RuntimeError('Unexpected Lean diagnostic output: ' + line)
    # The original module is loaded without creating a __pycache__ beside it.
    previous_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location('terminal_selector_parity_owner', owner_path)
        if spec is None or spec.loader is None:
            raise RuntimeError('Cannot load Python selector owner')
        orbital = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(orbital)
        reference = orbital.build_label_atlas()
    finally:
        sys.dont_write_bytecode = previous_bytecode
    expected_rows = [
        (int(row['t']), *[int(word, 3) for word in row['B'].split('|')],
         *[int(row[field], 3) for field in orbital.FIELDS])
        for row in reference['rows']
    ]
    if actual_rows != expected_rows or metadata != ['100', 'true', 'true']:
        raise RuntimeError('N69 rows, row validity, or uniqueness of time differ')
    residues_by_time = defaultdict(set)
    for field in orbital.FIELDS:
        for residue, labels in reference['residue_labels'][field].items():
            for label in labels:
                residues_by_time[int(label['t'])].add(int(residue))
    expected = {}
    reader_bits = {'comparacion-fase-carga': 1, 'Witt-dual-mas-fase': 2}
    for word, labels in reference['block_labels'].items():
        child = int(word, 3)
        for label in labels:
            bit = reader_bits[str(label['reader'])]
            for residue in residues_by_time[int(label['t'])]:
                key = child * 729 + residue
                expected[key] = expected.get(key, 0) | bit
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    wrong = [key for key in actual.keys() & expected.keys() if actual[key] != expected[key]]
    record.update(missing=len(missing), extra=len(extra), wrong_masks=len(wrong))
    if missing or extra or wrong:
        record['examples'] = dict(missing=missing[:10], extra=extra[:10], wrong=sorted(wrong)[:10])
        raise RuntimeError('Python/Lean reader-atlas parity failed')
    canonical = ''.join(f'{key},{mask}\n' for key, mask in sorted(actual.items())).encode()
    record.update(
        status='PASS_ALL_ROWS_AND_ATLAS_PAIRS', rows_match_csv=len(actual_rows),
        all_rows_valid=True, times_unique=True,
        same_row_equals_same_time_for_this_input=True,
        atlas_pairs=len(actual), bitmask_histogram=dict(sorted(Counter(actual.values()).items())),
        comparison_words=len(reference['comparison_outputs']),
        affine_words=len(reference['affine_outputs']), union_words=len(reference['language']),
        canonical_pair_csv_sha256=hashlib.sha256(canonical).hexdigest(),
        canonical_serialization='ascending key; decimal key,mask followed by LF; no header',
        n69_csv=str(orbital.N69), n69_csv_sha256=sha256(orbital.N69),
        diagnostic_only=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--mathlib', type=Path, required=True, help='Existing Mathlib checkout with compiled cache')
    parser.add_argument('--lean', default='lean', help='Lean executable (default: lean on PATH; must be 4.21.0)')
    parser.add_argument('--article-library', type=Path, default=DEFAULT_ARTICLE_LIBRARY)
    parser.add_argument('--regional-library', type=Path, default=DEFAULT_REGIONAL_LIBRARY,
                        help='Regional source library (default: bundled regional/ when present)')
    parser.add_argument('--check-python', type=Path, metavar='SELECTOR_PY', help='Optional exact atlas parity diagnostic')
    parser.add_argument('--timeout', type=int, default=900, help='Seconds per compiler/diagnostic command (default: 900)')
    args = parser.parse_args()
    receipt = dict(
        status='RUNNING', verified_at_utc=datetime.now(timezone.utc).isoformat(),
        invocation=sys.argv, verifier_sha256=sha256(Path(__file__)), modules=[],
        native_decide_trust='Lean.ofReduceBool is explicitly allowed and reported; it is not an axiom-free proof.',
        allowed_axioms=sorted(ALLOWED_AXIOMS), mathlib_rebuilt=False,
        input_provenance_proved={
            'panel_from_generated_regional_prefixes': False,
            'N69_from_generated_regional_prefixes': False,
            'W24': False, 'S8': False,
        },
        whole_article_I_formalized=False,
        scope='Finite selector and alpha composition from generated regional panel/N69/W24, with S8 still an explicit input.',
    )
    report_path = HERE / 'VERIFICATION.json'
    try:
        mathlib, article = args.mathlib.expanduser().resolve(), args.article_library.expanduser().resolve()
        regional = args.regional_library.expanduser().resolve()
        if not mathlib.is_dir() or not article.is_dir() or not regional.is_dir():
            raise RuntimeError('--mathlib, --article-library and --regional-library must be existing directories')
        if args.timeout <= 0:
            raise RuntimeError('--timeout must be positive')
        lean = shutil.which(args.lean)
        if lean is None:
            raise RuntimeError('Lean executable not found: ' + args.lean)
        lean = str(Path(lean).absolute())
        version = subprocess.check_output([lean, '--version'], cwd=mathlib, text=True).strip()
        if 'version 4.21.0,' not in version:
            raise RuntimeError('Expected Lean 4.21.0; found ' + version)
        raw_paths = subprocess.check_output(['lake', 'env', 'printenv', 'LEAN_PATH'], cwd=mathlib, text=True).strip()
        library_paths = [(mathlib / item).resolve() for item in raw_paths.split(os.pathsep) if item]
        prefix = subprocess.check_output([lean, '--print-prefix'], cwd=mathlib, text=True).strip()
        library_paths.append(Path(prefix) / 'lib' / 'lean')
        commit_run = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=mathlib, text=True, capture_output=True)
        commit = commit_run.stdout.strip() if commit_run.returncode == 0 else None
        build = HERE / 'build'
        build.mkdir(exist_ok=True)
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, [build, *library_paths])))
        receipt.update(lean_version=version, lean_executable=lean, mathlib=str(mathlib),
                       mathlib_commit=commit, article_library=str(article),
                       regional_library=str(regional), lean_path=env['LEAN_PATH'])
        cache_path = build / 'VERIFICATION_CACHE.json'
        cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
        if cache.get('format') != CACHE_FORMAT:
            cache = {'format': CACHE_FORMAT, 'modules': {}}
        cache.setdefault('modules', {})
        graph, order, visiting = {}, [], set()
        external = {}

        def source_for(name):
            relative = Path(*name.split('.')).with_suffix('.lean')
            if name in FOCAL_MODULES:
                return HERE / relative
            return next((root / relative for root in (article, regional)
                         if (root / relative).is_file()), None)

        def external_object(name):
            if name not in external:
                relative = Path(*name.split('.')).with_suffix('.olean')
                path = next((root / relative for root in library_paths if (root / relative).is_file()), None)
                if path is None:
                    raise RuntimeError(f'Missing precompiled dependency {name}; Mathlib will not be rebuilt')
                external[name] = {'path': str(path), 'object_sha256': sha256(path)}
            return external[name]

        def visit(name):
            if name in graph:
                return
            if name in visiting:
                raise RuntimeError('Cyclic local imports at ' + name)
            source = source_for(name)
            if source is None or not source.is_file():
                raise RuntimeError('Missing local source ' + name)
            visiting.add(name)
            imports = inspect_source(source)
            for dependency in imports:
                if source_for(dependency) is not None:
                    visit(dependency)
                else:
                    external_object(dependency)
            visiting.remove(name)
            graph[name] = {'source': source, 'source_sha256': sha256(source), 'imports': imports}
            order.append(name)

        for module in FOCAL_MODULES:
            visit(module)
        receipt['local_compile_order'] = order
        receipt['external_objects'] = external
        completed = {}
        for module in order:
            node = graph[module]
            dependency_hashes = {
                name: ({'fingerprint': completed[name]['fingerprint'],
                        'object_sha256': completed[name]['object_sha256']}
                       if name in completed else external[name])
                for name in node['imports']
            }
            fingerprint = json_digest(dict(
                source_sha256=node['source_sha256'], dependencies=dependency_hashes,
                lean_version=version, mathlib_commit=commit,
                verifier_sha256=receipt['verifier_sha256'], cache_format=CACHE_FORMAT,
            ))
            relative = Path(*module.split('.'))
            target = (build / relative).with_suffix('.olean')
            copied_source = (build / relative).with_suffix('.lean')
            log_path = (build / relative).with_suffix('.log')
            command = [lean, '-DwarningAsError=true', '--root=' + str(build),
                       '-o', str(target), str(copied_source)]
            prior = cache['modules'].get(module, {})
            hit = (prior.get('fingerprint') == fingerprint and prior.get('exit_code') == 0
                   and target.is_file() and prior.get('object_sha256') == sha256(target))
            record = dict(module=module, source=str(node['source']), source_sha256=node['source_sha256'],
                          dependencies=dependency_hashes, fingerprint=fingerprint,
                          command=command, cache_hit=hit, object=str(target))
            receipt['modules'].append(record)
            if hit:
                code, output = 0, prior.get('output', '')
                print(module + ': verified cache hit', flush=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(node['source'], copied_source)
                if sha256(copied_source) != node['source_sha256']:
                    raise RuntimeError('Source changed before compilation: ' + module)
                print(module + ': compiling source', flush=True)
                code, output = execute(command, cwd=mathlib, env=env, timeout=args.timeout)
                log_path.write_text(output, encoding='utf-8')
            record.update(exit_code=code, output=output)
            record['axioms'] = axiom_reports(output)
            if code:
                print(output, end='', flush=True)
                raise RuntimeError(f'Lean compilation failed: {module}, exit {code}')
            if sha256(node['source']) != node['source_sha256'] or not target.is_file():
                raise RuntimeError('Source changed or object missing after compilation: ' + module)
            record['object_sha256'] = sha256(target)
            completed[module] = record
            cache['modules'][module] = record
            write_json(cache_path, cache)

        probe = 'import SelectedFromRegionalInputs\n' + ''.join(
            '#print axioms ' + name + '\n' for name in EXPECTED_DECLARATIONS)
        command = [lean, '--stdin']
        receipt['axiom_probe'] = {'command': command, 'source': probe}
        code, output = execute(command, cwd=mathlib, env=env, timeout=args.timeout, input_text=probe)
        receipt['axiom_probe'].update(exit_code=code, output=output)
        reports = axiom_reports(output)
        receipt['axiom_probe']['declarations'] = reports
        if code or set(reports) != set(EXPECTED_DECLARATIONS):
            raise RuntimeError('Final theorem/axiom probe failed or omitted a declaration')
        receipt['axioms'] = sorted({axiom for values in reports.values() for axiom in values})
        receipt['input_provenance_proved'].update(
            panel_from_generated_regional_prefixes=True,
            N69_from_generated_regional_prefixes=True,
        )
        receipt['input_provenance_proved']['W24'] = True
        receipt['input_provenance_remaining'] = ['S8']
        if args.check_python is not None:
            receipt['python_parity'] = {'status': 'RUNNING'}
            python_parity(args.check_python.expanduser().resolve(), lean, build, mathlib,
                          env, args.timeout, receipt['python_parity'])
        else:
            receipt['python_parity'] = {'status': 'NOT_REQUESTED'}
        for name, node in graph.items():
            if sha256(node['source']) != node['source_sha256']:
                raise RuntimeError('Source changed during verification: ' + name)
        receipt.update(status='PASS_TERMINAL_SELECTOR_AND_ALPHA',
                       compiled_modules=[r['module'] for r in receipt['modules'] if not r['cache_hit']],
                       cached_modules=[r['module'] for r in receipt['modules'] if r['cache_hit']],
                       result='All seven selector/recovery/alpha/regional-bridge results loaded and axiom-checked.')
        return_code = 0
    except Exception as error:
        receipt.update(status='FAIL', error_type=type(error).__name__, error=str(error))
        print(f'FAIL: {error}', file=sys.stderr, flush=True)
        return_code = 1
    receipt['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    write_json(report_path, receipt)
    print(receipt['status'], flush=True)
    print(str(report_path), flush=True)
    return return_code


if __name__ == '__main__':
    raise SystemExit(main())
