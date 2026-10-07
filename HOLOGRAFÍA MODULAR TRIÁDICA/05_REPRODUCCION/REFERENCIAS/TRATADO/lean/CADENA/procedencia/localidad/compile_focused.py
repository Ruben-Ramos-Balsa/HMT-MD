"""Compile one local module; certify its source, queries and direct imports.

This does not recompile or recertify the entire base closure. Its baseline
receipt is pinned, and every directly imported object is checked before and
after the local compilation. No invocation can reuse an earlier PASS.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = Path('/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_PRODUCTOS_RETICULARES_20260919')
BASE_RECEIPT_SHA256 = 'ca4983392204e75aa444870e027945497115c110534e3f6cee5df27b895beb24'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
MODULE_NAME = r'[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def lean_code(text):
    """Erase nested Lean comments and strings, retaining line boundaries."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i+2]
        if depth:
            if pair == '/-':
                depth += 1
                out.append('  ')
                i += 2
            elif pair == '-/':
                depth -= 1
                out.append('  ')
                i += 2
            else:
                out.append('\n' if text[i] == '\n' else ' ')
                i += 1
        elif string:
            if text[i] == '\\':
                out.append('  ')
                i += 2
            elif text[i] == '"':
                string = False
                out.append(' ')
                i += 1
            else:
                out.append('\n' if text[i] == '\n' else ' ')
                i += 1
        elif pair == '--':
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            out.append(' ' * (end-i))
            i = end
        elif pair == '/-':
            depth = 1
            out.append('  ')
            i += 2
        elif text[i] == '"':
            string = True
            out.append(' ')
            i += 1
        else:
            out.append(text[i])
            i += 1
    if depth or string:
        raise RuntimeError('Unterminated source comment or string')
    return ''.join(out)


def source_contract(text):
    code = lean_code(text)
    forbidden = re.search(r'\b(?:sorry|sorryAx|axiom|constant)\b', code)
    if forbidden:
        raise RuntimeError('Forbidden active Lean token: ' + forbidden.group())
    imports = []
    for tail in re.findall(r'^\s*import\b([^\n]*)', code, re.M):
        names = tail.split()
        if not names or any(not re.fullmatch(MODULE_NAME, n) for n in names):
            raise RuntimeError('Unsupported or incomplete import syntax')
        imports.extend(names)
    queries = []
    for tail in re.findall(r'^\s*#print\s+axioms\b([^\n]*)', code, re.M):
        query = tail.strip()
        if not re.fullmatch(MODULE_NAME, query):
            raise RuntimeError('Expected an explicit qualified axiom-query name')
        queries.append(query.removeprefix('_root_.'))
    if not queries or len(set(queries)) != len(queries):
        raise RuntimeError('At least one distinct explicit #print axioms query is required')
    return list(dict.fromkeys(imports)), queries


def checked_axioms(output, queries):
    pairs = [(n, [a.strip() for a in raw.split(',') if a.strip()])
             for n, raw in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.S)]
    pairs += [(n, []) for n in re.findall(r"'([^']+)' does not depend on any axioms", output)]
    names = [name for name, _ in pairs]
    if len(names) != len(queries) or set(names) != set(queries):
        raise RuntimeError('Missing, duplicated, or unexpected axiom-query output')
    if any(set(values) - ALLOWED_AXIOMS for _, values in pairs):
        raise RuntimeError('Unapproved axiom dependency (including sorryAx)')
    return dict(pairs)


def save_receipt(path, result):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(result, indent=2) + '\n')
    temporary.replace(path)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1 or not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', argv[0]):
        raise SystemExit('Expected one local module name')
    name = argv[0]
    source, obj = HERE / (name + '.lean'), HERE / (name + '.olean')
    receipt, log = HERE / (name + '.receipt.json'), HERE / (name + '.log')
    result = {'status': 'RUNNING', 'schema': 2, 'module': name,
              'source': str(source), 'base_modules_recompiled': 0,
              'object_sha256': None, 'allowed_axioms': sorted(ALLOWED_AXIOMS),
              'scope': 'Local source and direct imports, pinned base receipt; not a fresh base-closure verification.'}
    save_receipt(receipt, result)  # Before every fallible source/base/compiler check.
    output = ''
    try:
        log.write_text('')
        source_hash = sha(source)
        imports, queries = source_contract(source.read_text())
        result.update(source_sha256=source_hash, checked_queries=queries)
        base_receipt = BASE / 'resultados/lean_unificado/VERIFICATION.json'
        if sha(base_receipt) != BASE_RECEIPT_SHA256:
            raise RuntimeError('Base receipt differs from the fixed baseline')
        data = json.loads(base_receipt.read_text())
        if data['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE':
            raise RuntimeError('Base receipt is not PASS')
        lean, mathlib = Path(data['compiler']['executable']), Path(data['mathlib'])
        compiler_hash = sha(lean)
        if compiler_hash != data['compiler']['binary_sha256']:
            raise RuntimeError('Compiler hash differs from the baseline')
        version = subprocess.check_output([str(lean), '--version'], text=True).strip()
        if version != data['compiler']['version']:
            raise RuntimeError('Compiler version differs from the baseline')
        libraries = sorted((mathlib / '.lake/packages').glob('*/.lake/build/lib/lean'))
        build = BASE / 'resultados/lean_unificado/build'
        paths = [HERE, build, *libraries, mathlib / '.lake/build/lib/lean', lean.parent.parent / 'lib/lean']
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
        baseline = {item['module']: item for item in data['modules']}
        external = data['external_objects']
        dependencies = {}
        for imp in imports:
            rel = Path(*imp.split('.')).with_suffix('.olean')
            path = next((p / rel for p in paths if (p / rel).is_file()), None)
            if path is None:
                raise RuntimeError('Missing import ' + imp)
            digest = sha(path)
            dep = {'path': str(path), 'sha256': digest}
            if imp in baseline:
                pinned = baseline[imp]
                if path.resolve() != (build / rel).resolve() or digest != pinned['object_sha256']:
                    raise RuntimeError('Shadowed or altered baseline import ' + imp)
                owner = BASE / pinned['source']
                if sha(owner) != pinned['source_sha256']:
                    raise RuntimeError('Altered baseline source ' + imp)
                dep.update(source=str(owner), source_sha256=sha(owner))
            elif imp in external:
                pinned = external[imp]
                if path.resolve() != Path(pinned['path']).resolve() or digest != pinned['object_sha256']:
                    raise RuntimeError('Shadowed or altered external import ' + imp)
            elif path.parent == HERE:
                owner = HERE / (imp + '.lean')
                local_receipt = HERE / (imp + '.receipt.json')
                prior = json.loads(local_receipt.read_text())
                if prior['status'] != 'PASS_FOCUSED_FIELD_MODULE' or prior['source_sha256'] != sha(owner) or prior['object_sha256'] != digest:
                    raise RuntimeError('Unverified or stale local import ' + imp)
                dep.update(source=str(owner), source_sha256=sha(owner),
                           receipt=str(local_receipt), receipt_sha256=sha(local_receipt))
            dependencies[imp] = dep
        command = [str(lean), '-DwarningAsError=true', '-o', str(obj), str(source)]
        result.update(command=command, dependencies=dependencies,
                      compiler={'executable': str(lean), 'binary_sha256': compiler_hash, 'version': version},
                      mathlib=str(mathlib), lean_path=env['LEAN_PATH'],
                      base_receipt_sha256=BASE_RECEIPT_SHA256)
        save_receipt(receipt, result)
        run = subprocess.run(command, cwd=HERE, env=env, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = run.stdout
        log.write_text(output)
        result['exit_code'] = run.returncode
        if run.returncode != 0:
            raise RuntimeError('Lean compilation failed')
        result['axioms'] = checked_axioms(output, queries)
        if sha(source) != source_hash or sha(lean) != compiler_hash or sha(base_receipt) != BASE_RECEIPT_SHA256:
            raise RuntimeError('Source, compiler or base receipt changed during compilation')
        for imp, dep in dependencies.items():
            if sha(dep['path']) != dep['sha256']:
                raise RuntimeError('Imported object changed during compilation: ' + imp)
            if 'source' in dep and sha(dep['source']) != dep['source_sha256']:
                raise RuntimeError('Imported source changed during compilation: ' + imp)
            if 'receipt' in dep and sha(dep['receipt']) != dep['receipt_sha256']:
                raise RuntimeError('Local dependency receipt changed during compilation: ' + imp)
        result.update(status='PASS_FOCUSED_FIELD_MODULE', object_sha256=sha(obj))
    except (Exception, KeyboardInterrupt) as error:
        result.update(status='FAIL_FOCUSED_FIELD_MODULE', error=str(error), object_sha256=None)
        output += '\nFOCUSED_FAILURE: ' + str(error) + '\n'
        log.write_text(output)
    result.update(log=str(log), log_sha256=sha(log))
    save_receipt(receipt, result)
    print(output, end='')
    print(result['status'])
    return 0 if result['status'] == 'PASS_FOCUSED_FIELD_MODULE' else 1


if __name__ == '__main__':
    raise SystemExit(main())
