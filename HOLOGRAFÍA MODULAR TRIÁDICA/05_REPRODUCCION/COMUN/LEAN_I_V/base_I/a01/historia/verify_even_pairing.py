#!/usr/bin/env python3
"""Focal compilation and public-declaration axiom check for the even pairing.

Only the five contribution modules are compiled.  Predecessor and Fock objects
are authenticated and reused, never rebuilt.  Run only after the editor has
frozen the five Lean sources.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
TWISTED = Path('/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/exceptional/twisted_fields')
FOCK = Path('/Users/ruben/Documents/New project/output/ARTICLE_I_TT_FOCK_PAIRING_20260922')
RECEIPT = TWISTED / 'terminal_te_duality_results_20260922/VERIFICATION.json'
RECEIPT_SHA = 'dd5561e11cb0a019ec4d63f0ca0239e068509ab92d7dd22197b88947fc14f647'
NAMES = [
    'GradedPairingRepresentability',
    'LatticeChargePairing',
    'LatticeIntegerPairingWeights',
    'LatticeUntwistedPairing',
    'LatticeEvenPairingRepresentability',
]
ORDINARY = {'Classical.choice', 'Quot.sound', 'propext'}
INHERITED = [
    (FOCK, 'WeightedBasisPairing',
     'f1f0cf162e1d88ddd9a0b121153d8bac90d48e9172898eefb90db971e66fd3a0',
     '82682e919bff4bf30d487ba03ea1f32ee8abcbc94c4f54267041907983d32ce5'),
    (FOCK, 'LatticeFactorialPairing',
     '7fe98a4d9dfec0144ab044727703645ac0c2c17f490d9678c248d84b2c973a49',
     'd97440509a8c0365f52de7b18e5b975d8af4d7e0e2f59fed92dabf167dfd9a79'),
    (FOCK, 'LatticeHalfGramTransport',
     '14c892ca757fcf25ed20b68b340ae62b45803b49b23cded32013d41603da1e18',
     'a4e72768e1681870c640ba5d42015a7c093bd8fa5293e23d5ed41cffa89f43dd'),
    (TWISTED, 'LatticeIntegerFockPairing',
     '8edcd7156446723731f444904d5c3edd670f6eb175bf5c54370cd1d3de66f2c6',
     '416319f3dcdd0f288778a961d4b62fd887caf17a1911323033af2e12d59f60fd'),
]
DECL = re.compile(
    r'^[ \t]*(?:@\[[^\]\n]*\][ \t]*)*'
    r'(?:(?:noncomputable|protected)[ \t]+)*'
    r'(?:def|theorem|lemma|abbrev|structure|class|opaque|inductive)[ \t]+'
    r"([\w']+)", re.M)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def without_comments(text):
    """Remove nested Lean comments, preserving line breaks and string literals."""
    result, i, depth, quoted = [], 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1
                result.append('  ')
                i += 2
            elif text.startswith('-/', i):
                depth -= 1
                result.append('  ')
                i += 2
            else:
                result.append('\n' if text[i] == '\n' else ' ')
                i += 1
        elif quoted:
            result.append(text[i])
            if text[i] == '\\' and i + 1 < len(text):
                result.append(text[i + 1])
                i += 2
            else:
                if text[i] == '"':
                    quoted = False
                i += 1
        elif text.startswith('/-', i):
            depth = 1
            result.append('  ')
            i += 2
        elif text.startswith('--', i):
            end = text.find('\n', i)
            if end == -1:
                end = len(text)
            result.append(' ' * (end - i))
            i = end
        else:
            quoted = text[i] == '"'
            result.append(text[i])
            i += 1
    require(depth == 0 and not quoted, 'Unclosed source comment or string')
    return ''.join(result)


def public_declarations(name, content):
    clean = without_comments(content)
    require(not re.search(r'\b(?:sorry|admit|axiom)\b', clean),
            name + ': forbidden proof placeholder or axiom declaration')
    namespaces = re.findall(r'^\s*namespace\s+(\S+)', clean, re.M)
    expected = 'HMT.IV.' + name
    require(namespaces == [expected], name + ': unsupported namespace layout')
    public = DECL.findall(clean)
    require(public and len(public) == len(set(public)),
            name + ': missing or duplicated public declarations')
    require(not re.search(r'^\s*(?:@\[[^\]\n]*\]\s*)*(?:noncomputable\s+)?instance\b',
                          clean, re.M), name + ': instance needs an explicit probe name')
    return [expected + '.' + declaration for declaration in public]


def resolve_object(name, paths):
    relative = Path(*name.split('.')).with_suffix('.olean')
    for path in paths:
        candidate = Path(path) / relative
        if candidate.is_file():
            return candidate.resolve()
    raise RuntimeError('Unresolved import object: ' + name)


def unchanged(tracked):
    for path, expected in tracked.items():
        require(sha(path) == expected, 'Artifact changed: ' + path)


def main():
    started = time.monotonic()
    require(sha(RECEIPT) == RECEIPT_SHA, 'Predecessor receipt changed')
    prior = json.loads(RECEIPT.read_text())
    require(prior['status'] == 'PASS_TWISTED_TERMINAL_DELTA', 'Wrong predecessor status')
    require(len(prior['modules']) == 8, 'Expected eight predecessor module pairs')
    compiler = prior['compiler']
    tracked = {str(RECEIPT): RECEIPT_SHA,
               compiler['executable']: compiler['binary_sha256'],
               str(Path(__file__).resolve()): sha(__file__)}
    for item in prior['modules']:
        for suffix, key in [('.lean', 'source_sha256'), ('.olean', 'object_sha256')]:
            artifact = RECEIPT.parent / 'build' / (item['module'] + suffix)
            tracked[str(artifact)] = item[key]
    inherited = []
    for folder, name, source_hash, object_hash in INHERITED:
        source, obj = folder / (name + '.lean'), folder / (name + '.olean')
        tracked[str(source)], tracked[str(obj)] = source_hash, object_hash
        inherited.append(dict(module=name, source=str(source), source_sha256=source_hash,
                              object=str(obj), object_sha256=object_hash))
    unchanged(tracked)
    paths = [str(HERE), *prior['lean_path'].split(os.pathsep), str(FOCK), str(TWISTED)]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(paths))
    for entry in inherited:
        require(resolve_object(entry['module'], paths) == Path(entry['object']).resolve(),
                'Pinned inherited object is shadowed: ' + entry['module'])
    contents, declarations = {}, []
    for name in NAMES:
        source = HERE / (name + '.lean')
        contents[name] = source.read_text()
        tracked[str(source)] = sha(source)
        declarations.extend(public_declarations(name, contents[name]))
    require(len(declarations) == len(set(declarations)), 'Repeated qualified declaration')
    out = HERE / 'resultados'
    out.mkdir(exist_ok=True)
    report = dict(status='RUNNING_UNTWISTED_EVEN_WEIGHT_PAIRING', compiler=compiler,
                  predecessor_receipt=str(RECEIPT), predecessor_receipt_sha256=RECEIPT_SHA,
                  inherited_modules_recompiled=False, pdfs_changed=False,
                  inherited_fock_modules=inherited, lean_path=env['LEAN_PATH'], modules=[],
                  runner_sha256=sha(__file__), public_declarations=declarations,
                  public_declaration_count=len(declarations),
                  scope='Concrete untwisted/even bilinear pairing, nondegeneracy, weight '
                        'orthogonality and unique representability on finite weight spaces. '
                        'This does not assert full vertex invariance or construction of TT.')
    receipt_out = out / 'VERIFICATION.json'

    def save():
        receipt_out.write_text(json.dumps(report, indent=2) + '\n')

    save()
    try:
        for name in NAMES:
            source = HERE / (name + '.lean')
            require(sha(source) == tracked[str(source)], 'Contribution source changed: ' + name)
            imports = re.findall(r'^import\s+(\S+)', without_comments(contents[name]), re.M)
            dependencies = []
            for imported in imports:
                obj = resolve_object(imported, paths)
                digest = sha(obj)
                if str(obj) in tracked:
                    require(tracked[str(obj)] == digest, 'Import changed: ' + imported)
                else:
                    tracked[str(obj)] = digest
                dependencies.append(dict(module=imported, object=str(obj), object_sha256=digest))
            command = [compiler['executable'], '-DwarningAsError=true', '--root=' + str(HERE),
                       '-o', str(HERE / (name + '.olean')), str(source)]
            run_started = time.monotonic()
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=300)
            log = out / (name + '.log')
            log.write_text(result.stdout + result.stderr)
            entry = dict(module=name, source=str(source), source_sha256=tracked[str(source)],
                         object=str(HERE / (name + '.olean')), imports=imports,
                         dependencies=dependencies, command=command, exit_code=result.returncode,
                         elapsed_seconds=round(time.monotonic() - run_started, 3),
                         log=str(log), log_sha256=sha(log))
            report['modules'].append(entry)
            save()
            require(result.returncode == 0, log.read_text())
            entry['object_sha256'] = sha(entry['object'])
            tracked[entry['object']] = entry['object_sha256']
            require(sha(source) == tracked[str(source)], 'Source changed during compilation: ' + name)
            save()
            print('COMPILED', name, flush=True)
        probe = out / 'axiom_probe.lean'
        probe.write_text('\n'.join('import ' + name for name in NAMES) + '\n' +
                         '\n'.join('#print axioms ' + name for name in declarations) + '\n')
        command = [compiler['executable'], '-DwarningAsError=true', str(probe)]
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr
        log = out / 'axiom_probe.log'
        log.write_text(output)
        report.update(axiom_probe_command=command, axiom_probe_exit_code=result.returncode,
                      axiom_probe_sha256=sha(probe), axiom_log_sha256=sha(log))
        require(result.returncode == 0, output)
        found = {}
        for match in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output):
            found[match.group(1)] = [a.strip() for a in match.group(2).split(',') if a.strip()]
        for match in re.finditer(r"'([^']+)' does not depend on any axioms", output):
            found[match.group(1)] = []
        require(set(found) == set(declarations), 'Incomplete public declaration probe')
        require(all(set(axioms) <= ORDINARY for axioms in found.values()), 'Unexpected axiom')
        unchanged(tracked)
        report.update(status='PASS_UNTWISTED_EVEN_WEIGHT_PAIRING', axioms=found,
                      ordinary_axioms_allowed=sorted(ORDINARY),
                      authenticated_and_unchanged_artifacts=tracked,
                      elapsed_seconds=round(time.monotonic() - started, 3))
        save()
        print(report['status'], len(NAMES), 'modules;', len(declarations), 'public declarations')
    except Exception as error:
        report.update(status='FAIL_UNTWISTED_EVEN_WEIGHT_PAIRING', error=str(error),
                      elapsed_seconds=round(time.monotonic() - started, 3))
        save()
        raise


if __name__ == '__main__':
    main()
