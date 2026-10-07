#!/usr/bin/env python3
"""Seal the exact 461 predecessor, fifteen ordinary modules and a separate selection.

--plan authenticates inputs only. Delivery copies the predecessor exactly once,
then runs only a source/authentication plan from a relocated copy. This builder
never invokes Lean, any documentary gate, or any predecessor compilation.
"""
import argparse
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
import tempfile
import zipfile
import zlib

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent
TF = OUTPUT/'AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/exceptional/twisted_fields'
BASE_SHA = '822524de5672f5453dc4a63cd33d6172ed98527d576f9185647206207a01acad'
TERMINAL_SHA = 'd1911674fa5a59d25d63246ab73cc1057057c02a91439dda92d785c10d91e51d'
HISTORICAL_TE_SHA = 'dd5561e11cb0a019ec4d63f0ca0239e068509ab92d7dd22197b88947fc14f647'
HELPER_SHA = '145accd5aa88f203f648f4e09d3d400122d7e047195cc18b060019c6e9c825a5'
RECEIPT_PINS = {
    'par': 'c34bc4fcbb5638ffda1021702c956d50d156b85696aa60117219d522f454fb0f',
    'reconstruccion': '9a4bf6186475376a3f6330e5fa673c3c9780abf80b027f2116852a82ec2a13f3',
    'soporte': 'cf6aba0dff4a8e524a18abd629e7804e10efd505a6d5746efaf30e67b9b72e73',
    'consumidores': '59491b582d884ba3ba2cc2a2e240a2f61f4e97918b5cb572e79d209b6a29eb6a',
}
ROLE_NAMES = {
    'par': ['GradedPairingRepresentability', 'LatticeChargePairing',
        'LatticeIntegerPairingWeights', 'LatticeUntwistedPairing', 'LatticeEvenPairingRepresentability'],
    'reconstruccion': ['LatticeEvenRestrictedDual'],
    'soporte': ['LatticeTwistedNormalEnergy', 'LatticeTwistedRawEnergy',
        'LatticeTwistedCorrectedEnergy', 'SkewFieldEnergy', 'LatticeTwistedPairingEnergy',
        'LatticeTwistedFullEnergy', 'LatticeContragredientWeightSupport'],
    'consumidores': ['LatticeTwistedPairProduct', 'LatticeOrbifoldFullStateFields'],
    'selected': ['SelectedOrbifoldStateFields'],
}
STATUSES = {'par': 'PASS_UNTWISTED_EVEN_WEIGHT_PAIRING',
    'reconstruccion': 'PASS_RESTRICTED_DUAL_RECONSTRUCTION',
    'soporte': 'PASS_CONTRAGREDIENT_HOMOGENEOUS_WEIGHT_SUPPORT',
    'consumidores': 'PASS_TWISTED_PAIR_PRODUCT',
    'selected': 'PASS_SELECTED_ORBIFOLD_SPECIALIZATION'}
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}
SELECTED_ALLOWED = ORDINARY | {'Lean.ofReduceBool'}


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'Symlink is not a sealed file: '+str(path))
        if path.is_file():
            name = path.relative_to(root).as_posix()
            result[name] = dict(path=name, sha256=sha(path), bytes=path.stat().st_size)
    return result


def axiom_reports(output):
    reports = {}
    pattern = r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, output):
        require(match[1] not in reports, 'Repeated public axiom report: '+match[1])
        reports[match[1]] = [a.strip() for a in (match[2] or '').split(',') if a.strip()]
    return reports


def replay_wrapper(bundle_hash):
    return '''#!/usr/bin/env python3
"""Explicit ordinary replay; --plan only authenticates the delivered closure."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parent
args = sys.argv[1:]
if any(a == '--package-root' or a.startswith('--package-root=') or
       a == '--bundle-sha256' or a.startswith('--bundle-sha256=') for a in args):
    raise SystemExit('The wrapper binds its own package root and bundle SHA256.')
defaults = []
if not any(a == '--report-dir' or a.startswith('--report-dir=') for a in args):
    defaults = ['--report-dir', str(root.parent/(root.name+'_resultados_nuevos'))]
raise SystemExit(subprocess.call([sys.executable, '-I', '-S',
    str(root/'verificar_incremento.py'), '--package-root', str(root),
    '--bundle-sha256', ''' + repr(bundle_hash) + ''', *defaults, *args]))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=OUTPUT/'PAQUETE_ARTICULO_I_DUALIDAD_DE_ESTADOS_20260922')
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--even-root', type=Path,
        default=Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_ARTICULO_I_20260917/even_pairing'))
    parser.add_argument('--restricted-root', type=Path, default=OUTPUT/'ARTICLE_I_RESTRICTED_DUAL_RECONSTRUCTION_20260922')
    parser.add_argument('--restricted-report-dir', type=Path)
    parser.add_argument('--support-root', type=Path, default=OUTPUT/'ARTICLE_I_CONTRAGREDIENT_WEIGHT_SUPPORT_20260922')
    parser.add_argument('--source-dir', type=Path, default=HERE)
    parser.add_argument('--consumers-report-dir', type=Path, default=HERE/'resultados')
    parser.add_argument('--selected-report-dir', type=Path, required=True)
    for flag in ('even', 'restricted', 'support', 'consumers', 'selected'):
        parser.add_argument('--'+flag+'-receipt-sha256', required=True)
    parser.add_argument('--readme', type=Path, default=HERE/'README_ENTREGA.md')
    parser.add_argument('--readme-sha256', required=True)
    parser.add_argument('--replayer', type=Path, default=HERE/'verify_pair_bundle.py')
    parser.add_argument('--replayer-sha256', required=True)
    for flag in ('genealogy-receipt', 'genealogy-check', 'causal-receipt', 'causal-check'):
        parser.add_argument('--'+flag, type=Path)
        parser.add_argument('--'+flag+'-sha256')
    parser.add_argument('--historical-te-receipt', type=Path,
        default=TF/'terminal_te_duality_results_20260922/VERIFICATION.json')
    parser.add_argument('--lean', type=Path)
    parser.add_argument('--mathlib-root', type=Path)
    parser.add_argument('--timeout', type=int, default=900)
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    for key, value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, key, value.expanduser().resolve())
    args.restricted_report_dir = args.restricted_report_dir or args.restricted_root/'resultados_02'
    require(args.timeout > 0, 'Positive timeout required')
    for key, value in vars(args).items():
        if key.endswith('sha256') and value is not None:
            require(re.fullmatch('[0-9a-f]{64}', value), 'Explicit lowercase SHA256 required: '+key)
    base, dest = args.base, args.destination
    archive = dest.with_suffix('.zip')
    delivery = dest.parent/(dest.name+'_ENTREGA.json')
    zip_report = dest.parent/(dest.name+'_ZIP_VERIFICACION.json')
    roots = {'par': args.even_root, 'reconstruccion': args.restricted_root,
        'soporte': args.support_root, 'consumidores': args.source_dir, 'selected': args.source_dir}
    reports = {'par': args.even_root/'resultados', 'reconstruccion': args.restricted_report_dir,
        'soporte': args.support_root, 'consumidores': args.consumers_report_dir, 'selected': args.selected_report_dir}
    hashes = dict(zip(reports, [args.even_receipt_sha256, args.restricted_receipt_sha256,
        args.support_receipt_sha256, args.consumers_receipt_sha256, args.selected_receipt_sha256]))
    require(all(not path.exists() for path in (dest, archive, delivery, zip_report)), 'Refusing to overwrite a delivery')
    protected = {base, *roots.values(), *reports.values()}
    require(all(not dest.is_relative_to(p) and not p.is_relative_to(dest) for p in protected),
        'Destination overlaps protected inputs')
    require(all(not p.is_relative_to(dest) for p in
        (args.readme, args.replayer, args.historical_te_receipt, Path(__file__).resolve())),
        'Destination would contain protected source files')
    tracked, copies = {}, {}

    def track(path, digest):
        path = Path(path).resolve()
        require(path not in tracked or tracked[path] == digest, 'Conflicting artifact hashes: '+str(path))
        require(sha(path) == digest, 'Changed authenticated artifact: '+str(path))
        tracked[path] = digest
        return path

    def add_copy(path, relative, digest):
        path = track(path, digest)
        rel = Path(relative)
        require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe delivery path')
        key = rel.as_posix()
        require(key not in copies, 'Repeated delivery file: '+key)
        copies[key] = (path, digest)
        return key

    track(base/'MANIFIESTO.json', BASE_SHA)
    manifest = read(base/'MANIFIESTO.json')
    require(manifest['total_authenticated_modules'] == 461, 'Wrong inherited cut')
    before = inventory(base)
    rows = {r['path']: r for r in manifest['files']}
    require(len(rows) == len(manifest['files']) and set(before) == set(rows)|{'MANIFIESTO.json'},
        'Unlisted or duplicate predecessor files')
    require(all(before[p] == row for p, row in rows.items()), 'Changed predecessor inventory')
    terminal_path = track(base/'recibos/terminal/VERIFICATION.json', TERMINAL_SHA)
    terminal = read(terminal_path)
    require(terminal['status'] == 'PASS_TWISTED_TERMINAL_DELTA'
        and terminal['authenticated_inputs_unchanged'], 'Invalid inherited terminal receipt')
    objects = {name: node['sha256'] for name, node in terminal['inherited_objects'].items()}
    for row in terminal['modules']:
        require(row['module'] not in objects and row['exit_code'] == 0, 'Duplicate or failed predecessor module')
        objects[row['module']] = row['object_sha256']
    require(len(objects) == 461, 'Incomplete inherited registry')
    registry = {}
    for name, digest in objects.items():
        candidates = [p for p, row in rows.items() if Path(p).name == name+'.olean' and row['sha256'] == digest]
        require(candidates, 'Predecessor object is absent from the sealed package: '+name)
        obj = min(candidates, key=lambda p: (len(Path(p).parts), p))
        sibling = str(Path(obj).with_suffix('.lean'))
        sources = [sibling] if sibling in rows else [p for p in rows if Path(p).name == name+'.lean']
        require(sources and len({rows[p]['sha256'] for p in sources}) == 1,
            'Missing or ambiguous manifested predecessor source: '+name)
        source = min(sources, key=lambda p: (len(Path(p).parts), p))
        registry[name] = dict(source='antecedente/'+source, source_sha256=rows[source]['sha256'],
            object='antecedente/'+obj, object_sha256=digest)
    helper_path = track(args.even_root/'verify_even_pairing.py', HELPER_SHA)
    spec = importlib.util.spec_from_file_location('pair_bundle_public_inventory', helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    receipt_data, receipt_locators, delta, selected = {}, {}, {}, {}
    for role, root in reports.items():
        digest = hashes[role]
        require(role not in RECEIPT_PINS or digest == RECEIPT_PINS[role], 'Wrong explicit focal receipt: '+role)
        rp = track(root/'VERIFICATION.json', digest)
        receipt = read(rp)
        receipt_data[role] = receipt
        require(receipt['status'] == STATUSES[role], 'Unsuccessful focal receipt: '+role)
        require([row['module'] for row in receipt['modules']] == ROLE_NAMES[role], 'Unexpected contribution modules: '+role)
        if role in ('reconstruccion', 'consumidores', 'selected'):
            require(receipt['authenticated_inputs_unchanged'] and not receipt['inherited_modules_recompiled'],
                'Unverified or rebuilt focal predecessor: '+role)
        target_root = 'especializacion' if role == 'selected' else 'recibos/'+role
        receipt_locators[role] = dict(path=add_copy(rp, target_root+'/VERIFICATION.json', digest), sha256=digest)
        publics, names = [], []
        for row in receipt['modules']:
            name = row['module']
            names.append(name)
            source = track(roots[role]/(name+'.lean'), row['source_sha256'])
            clean = helper.without_comments(source.read_text())
            if role == 'selected':
                policy = receipt['axiom_policy']
                namespace = 'HMT.I.'+name
                require(policy['module'] == name and policy['namespace'] == namespace
                    and set(policy['allowed_axioms']) == SELECTED_ALLOWED
                    and policy['native_decide_in_new_source_allowed'] is False
                    and policy['inherited_native_exception'] == 'Lean.ofReduceBool', 'Changed selected axiom policy')
                require(re.findall(r'^\s*namespace\s+(\S+)', clean, re.M) == [namespace]
                    and not re.search(r'\b(?:sorry|admit|axiom|native_decide|unsafe|run_cmd|elab|macro|initialize)\b', clean),
                    'Unsupported selected declaration source')
                declarations = [namespace+'.'+n for n in helper.DECL.findall(clean)]
            else:
                namespace = 'HMT.IV.'+name
                declarations = helper.public_declarations(name, source.read_text())
            theorem_names = [namespace+'.'+n for n in re.findall(
                r'^\s*(?:@\[[^\]\n]*\]\s*)*(?:theorem|lemma)\s+([\w\x27]+)', clean, re.M)]
            imports = re.findall(r'^import\s+(\S+)', clean, re.M)
            if role == 'selected':
                require(imports == receipt['axiom_policy']['imports'], 'Changed selected imports')
            publics.extend(declarations)
            if role in ('par', 'soporte'):
                obj = roots[role]/(name+'.olean')
            else:
                snapshot = track(root/'build'/(name+'.lean'), row['source_sha256'])
                add_copy(snapshot, target_root+'/build/'+name+'.lean', row['source_sha256'])
                obj = root/'build'/(name+'.olean')
            object_hash = row['olean_sha256'] if role == 'soporte' else row['object_sha256']
            if role != 'soporte':
                require(row['exit_code'] == 0, 'Failed focal compilation: '+name)
                log = root/(name+'.log') if role == 'par' else root/'build'/(name+'.log')
                add_copy(log, target_root+'/build/'+name+'.log', row['log_sha256'])
                if 'output' in row:
                    require(log.read_text() == row['output'], 'Changed focal compilation transcript: '+name)
            source_rel = ('especializacion/lean/' if role == 'selected' else 'lean/incremento/')+name+'.lean'
            node = dict(source=add_copy(source, source_rel, row['source_sha256']),
                source_sha256=row['source_sha256'],
                object=add_copy(obj, target_root+'/build/'+name+'.olean', object_hash),
                object_sha256=object_hash, imports=imports, public_declarations=declarations,
                theorem_names=theorem_names, receipt_role=role)
            require(name not in registry and name not in delta and name not in selected, 'Module collision: '+name)
            if role == 'selected':
                node['allowed_axioms'] = sorted(SELECTED_ALLOWED)
                node['axiom_policy'] = receipt['axiom_policy']
                selected[name] = node
            else:
                delta[name] = node
        if role == 'par':
            probe, log = root/'axiom_probe.lean', root/'axiom_probe.log'
            probe_hash, log_hash = receipt['axiom_probe_sha256'], receipt['axiom_log_sha256']
            recorded = receipt['axioms']
            require(receipt['axiom_probe_exit_code'] == 0, 'Failed even public probe')
        elif role == 'soporte':
            probe, log = root/'WeightSupportAxioms.lean', root/'axioms.log'
            probe_hash, log_hash = sha(probe), receipt['axioms_log_sha256']
            recorded = receipt['declarations']
            add_copy(root/'compile.log', target_root+'/compile.log', receipt['compile_log_sha256'])
        else:
            probe, log = root/'axiom_probe.lean', root/'axiom_probe.log'
            ap = receipt['axiom_probe']
            require(ap['exit_code'] == 0, 'Failed public probe: '+role)
            probe_hash, log_hash, recorded = ap['source_sha256'], ap['output_sha256'], ap['declarations']
            require(log.read_text() == ap['output'], 'Changed public transcript: '+role)
        wanted = ''.join('import '+n+'\n' for n in names)+''.join('#print axioms '+n+'\n' for n in publics)
        require(probe.read_text() == wanted, 'Changed complete public probe source: '+role)
        add_copy(probe, target_root+'/axiom_probe.lean', probe_hash)
        add_copy(log, target_root+'/axiom_probe.log', log_hash)
        found = axiom_reports(log.read_text())
        allowed = SELECTED_ALLOWED if role == 'selected' else ORDINARY
        require(len(publics) == len(set(publics)) and set(found) == set(publics) == set(recorded),
            'Incomplete or duplicate public probe: '+role)
        require(all(set(found[n]) == set(recorded[n]) and set(found[n]) <= allowed for n in publics),
            'Disallowed or changed axioms: '+role)
        if role != 'soporte':
            require(receipt['public_declaration_count'] == len(publics), 'Public count mismatch: '+role)
        if role in ('par', 'reconstruccion', 'selected'):
            require(receipt['public_declarations'] == publics, 'Public inventory mismatch: '+role)
        if role in ('reconstruccion', 'consumidores', 'selected'):
            entries = selected if role == 'selected' else delta
            require(receipt['theorem_names'] == [q for n in names for q in entries[n]['theorem_names']],
                'Theorem inventory mismatch: '+role)
        if role == 'consumidores':
            require(receipt['public_declaration_owners'] == {q: n for n in names for q in delta[n]['public_declarations']},
                'Consumer public owners mismatch')
        if role == 'selected':
            require(len(publics) == 6 and any('Lean.ofReduceBool' in values for values in found.values()),
                'Expected six separately recorded selected declarations with inherited reduction axiom')
    consumers, restricted = receipt_data['consumidores'], receipt_data['reconstruccion']
    require(consumers['restricted_receipt_sha256'] == hashes['reconstruccion']
        and consumers['support_receipt_sha256'] == hashes['soporte']
        and restricted['even_receipt_sha256'] == hashes['par']
        and restricted['terminal_receipt_sha256'] == TERMINAL_SHA
        and receipt_data['soporte']['parent_receipt_sha256'] == TERMINAL_SHA
        and receipt_data['selected']['ordinary_receipt_sha256'] == hashes['consumidores'],
        'Broken focal predecessor chain')
    require(len(delta) == 15 and len(selected) == 1, 'Wrong increment size')
    base_objects = {n: v['object_sha256'] for n, v in registry.items()}
    for role, prior_roles in (('reconstruccion', ('par',)),
            ('consumidores', ('par', 'reconstruccion', 'soporte')),
            ('selected', ('par', 'reconstruccion', 'soporte', 'consumidores'))):
        expected = dict(base_objects)
        expected.update({n: v['object_sha256'] for n, v in delta.items() if v['receipt_role'] in prior_roles})
        actual = {n: v['sha256'] for n, v in receipt_data[role]['inherited_objects'].items()}
        require(actual == expected, 'Focal object registry differs from the actual inherited closure: '+role)
    compiler = consumers['compiler']
    require(compiler == restricted['compiler'] == receipt_data['par']['compiler'] == terminal['compiler'],
        'Compiler identity mismatch')
    require(receipt_data['soporte']['compiler_sha256'] == compiler['binary_sha256'], 'Support compiler mismatch')
    require(receipt_data['selected']['compiler'] == compiler, 'Selected compiler mismatch')
    policy = receipt_data['selected']['axiom_policy']
    inherited_selected = registry[policy['inherited_owner']]
    require(inherited_selected['source_sha256'] == policy['inherited_source_sha256']
        and inherited_selected['object_sha256'] == policy['inherited_object_sha256'], 'Changed inherited selected owner')
    external = {name: dict(path=w['path'], sha256=w['sha256']) for name, w in consumers['resolved_objects'].items()
        if name not in registry and name not in delta}
    for node in delta.values():
        require(all(name in registry or name in delta or name in external for name in node['imports']),
            'Unresolved new ordinary import')
    for node in selected.values():
        require(all(name in registry or name in delta or name in external for name in node['imports']),
            'Unresolved selected import')
    order = list(delta)
    for index, name in enumerate(order):
        require(not (set(delta[name]['imports']) & set(order[index:])),
            'The four focal receipt orders are not a valid dependency order: '+name)
    for node in external.values():
        track(node['path'], node['sha256'])
    track(args.lean or compiler['executable'], compiler['binary_sha256'])
    scripts = [(helper_path, HELPER_SHA), (args.restricted_root/'verify_restricted_dual.py', restricted['runner_sha256']),
        (args.support_root/'verify_weight_support.py', receipt_data['soporte']['verifier_sha256']),
        (args.source_dir/'verify_pair_product.py', consumers['runner_sha256']),
        (args.source_dir/'verify_selected_orbifold.py', receipt_data['selected']['runner_sha256']),
        (Path(__file__).resolve(), sha(__file__))]
    for script, digest in scripts:
        add_copy(script, 'historia/'+script.name, digest)
    add_copy(args.historical_te_receipt, 'historia/TERMINAL_TE_DUALITY_VERIFICATION.json', HISTORICAL_TE_SHA)
    add_copy(args.readme, 'README.md', args.readme_sha256)
    add_copy(args.replayer, 'verificar_incremento.py', args.replayer_sha256)
    documentary = {}
    for flag, filename in (('genealogy_receipt', 'GENEALOGIA_V4.json'), ('genealogy_check', 'CONTROL_GENEALOGIA_V4.json'),
            ('causal_receipt', 'CAUSAL.json'), ('causal_check', 'CONTROL_CAUSAL.json')):
        path, digest = getattr(args, flag), getattr(args, flag+'_sha256')
        require(bool(path) == bool(digest), 'Supply documentary file and SHA256 together: '+flag)
        if path is not None:
            data = read(track(path, digest))
            require(isinstance(data, dict), 'Documentary artifact must be a JSON object: '+flag)
            if flag.endswith('_check'):
                if 'status' in data:
                    require(isinstance(data['status'], str) and data['status'].startswith('PASS_'),
                        'Documentary check is not successful: '+flag)
                else:
                    require(data.get('exit_code') == 0 and re.search(r'\bPASS_[A-Z0-9_]+\b', data.get('stdout', '')),
                        'Documentary check must contain a successful recorded result: '+flag)
            documentary[flag] = dict(path=add_copy(path, 'recibos/'+filename, digest), sha256=digest)
    bundle = dict(schema='hmt.pair_product.bundle.v1', registry461=registry, delta15=delta,
        selected=selected, dependency_order15=order, ordinary_allowed_axioms=sorted(ORDINARY),
        compiler=compiler, external_objects=external, receipts=receipt_locators,
        old_manifest=dict(path='antecedente/MANIFIESTO.json', sha256=BASE_SHA),
        inherited_terminal_receipt=dict(path='antecedente/recibos/terminal/VERIFICATION.json', sha256=TERMINAL_SHA),
        replayer=dict(path='verificar_incremento.py', sha256=args.replayer_sha256),
        inspector=dict(path='historia/verify_even_pairing.py', sha256=HELPER_SHA),
        artifact_files={name: digest for name, (_, digest) in copies.items() if name != 'verificar_incremento.py'},
        documentary_artifacts=documentary,
        copied_artifacts={name: digest for name, (_, digest) in copies.items()},
        ordinary_increment_modules=15, authenticated_modules_after_ordinary=476,
        selected_modules_separate=1, predecessor_copied_exactly_once=True)
    result = dict(status='PASS_PAIR_PRODUCT_PACKAGE_INPUTS', predecessor_modules=461,
        ordinary_increment_modules=15, selected_modules_separate=1,
        destination=str(dest), base_manifest_sha256=BASE_SHA, compilation_repeated=False)
    if args.plan:
        require(inventory(base) == before and all(sha(p) == h for p, h in tracked.items()), 'Inputs changed during plan')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    dest.mkdir(parents=True)
    shutil.copytree(base, dest/'antecedente')
    for relative, (source, digest) in copies.items():
        target = dest/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        require(sha(target) == digest, 'Copied artifact changed: '+relative)
    write_new(dest/'BUNDLE_INPUTS.json', bundle)
    bundle_hash = sha(dest/'BUNDLE_INPUTS.json')
    with (dest/'reproducir.py').open('x') as stream:
        stream.write(replay_wrapper(bundle_hash))
    with tempfile.TemporaryDirectory(prefix='hmt-pair-product-relocation-', dir=dest.parent) as temporary:
        temporary = Path(temporary)
        relocated = temporary/'paquete_relocalizado'
        shutil.copytree(dest, relocated)
        for is_selected in (False, True):
            label = 'selected' if is_selected else 'ordinary'
            plan_dir = temporary/('plan_'+label)
            command = [sys.executable, '-I', '-S', str(relocated/'verificar_incremento.py'),
                '--package-root', str(relocated), '--bundle-sha256', bundle_hash,
                '--report-dir', str(plan_dir), '--plan']
            if is_selected:
                command.append('--selected')
            for flag in ('lean', 'mathlib_root'):
                if getattr(args, flag) is not None:
                    command += ['--'+flag.replace('_', '-'), str(getattr(args, flag))]
            run = subprocess.run(command, cwd=temporary, text=True, capture_output=True, timeout=args.timeout)
            require(run.returncode == 0, 'Relocated authentication failed: '+run.stdout+run.stderr)
            plan_path = plan_dir/'VERIFICATION.json'
            if not plan_path.is_file():
                plan_path = plan_dir/'PLAN.json'
            plan = read(plan_path)
            require(plan.get('status', '').startswith('PASS_') and not plan.get('compiler_invoked', True)
                and plan.get('modules') == [] and plan.get('authenticated_inputs_unchanged') is True,
                'Relocated plan failed, compiled, or did not authenticate unchanged inputs')
            write_new(dest/('recibos/REPRODUCCION_RELOCALIZADA_'+label.upper()+'.json'), dict(command=command,
                exit_code=run.returncode, stdout=run.stdout, stderr=run.stderr,
                plan=plan, plan_sha256=sha(plan_path), is_lean_compilation=False))
    require(inventory(base) == before and inventory(dest/'antecedente') == before, 'Predecessor was changed or incompletely copied')
    require(all(sha(p) == h for p, h in tracked.items()), 'Input changed during packaging')
    write_new(dest/'VERIFICACION_CONSERVACION.json', dict(status='PASS_EXACT_461_PREDECESSOR_COPY',
        predecessor_manifest_sha256=BASE_SHA, predecessor_files=list(before.values()),
        predecessor_copied_exactly_once=True, predecessor_modules_recompiled=False,
        ordinary_increment_modules=15, selected_modules_separate=1))
    write_new(dest/'MANIFIESTO.json', dict(schema='hmt.pair_product.successor.v1',
        generated_at_utc=datetime.now(timezone.utc).isoformat(), predecessor='antecedente',
        previous_manifest_sha256=BASE_SHA, bundle_inputs_sha256=sha(dest/'BUNDLE_INPUTS.json'),
        inherited_modules=461, ordinary_increment_modules=15, authenticated_modules_after_ordinary=476,
        selected_modules_separate=1, files=list(inventory(dest).values())))
    complete = inventory(dest)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
        for name in complete:
            zipped.write(dest/name, dest.name+'/'+name)
    entries = []
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
        require(zipped.testzip() is None and len(names) == len(set(names)) == len(complete), 'ZIP count, duplication or CRC failure')
        require(set(names) == {dest.name+'/'+n for n in complete}, 'Unexpected ZIP entry')
        for name, row in complete.items():
            path = dest.name+'/'+name
            data = zipped.read(path)
            digest, crc = hashlib.sha256(data).hexdigest(), zlib.crc32(data)&0xffffffff
            require(digest == row['sha256'] and len(data) == row['bytes'] and crc == zipped.getinfo(path).CRC,
                'ZIP entry content mismatch: '+name)
            entries.append(dict(path=path, bytes=len(data), sha256=digest, crc32=f'{crc:08x}'))
    write_new(zip_report, dict(status='PASS_ZIP_CRC_AND_SHA256_EVERY_ENTRY', archive=str(archive),
        archive_sha256=sha(archive), entries=entries))
    require(inventory(dest) == complete and inventory(base) == before
        and all(sha(p) == h for p, h in tracked.items()), 'Inputs or delivery changed during sealing')
    result.update(status='PASS_PAIR_PRODUCT_DELIVERY', files=len(complete), manifest_sha256=sha(dest/'MANIFIESTO.json'),
        zip_sha256=sha(archive), zip_verification_sha256=sha(zip_report), relocated_plan_passed=True,
        gates_executed=False, lean_invoked_by_builder=False, selected_axiom_policy_separate=True)
    write_new(delivery, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
