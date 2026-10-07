#!/usr/bin/env python3
"""Read-only delivery inputs; portable path bindings; external outputs only.

--plan authenticates source/data files without importing any scientific module.
Execution requires a fresh --output-dir outside the delivery. No source is
rewritten, no formula or model is replaced, and no Lean compiler is invoked.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import shutil
import sys

K = '05_REPRODUCCION/COMUN/CERTIFICADOS_K/lectura_conjunta'
R15 = ('05_REPRODUCCION/REFERENCIAS/TRATADO/verificaciones/R15/'
       'EL_CIERRE_HOLOGRAFICO_DEL_INFINITO_HMT_MD_2026-07-22/'
       '01_HOLOGRAFIA_MODULAR_TRIADICA/certificados/selector_orbital_constantes.json')

UNITS = {
    'regional': {
        'source': (K + '/python/lectores_regionales.py',
                   '50249c422bec1f3614bacc3982d8cc9ec096bd2f089a5a0ef6d0fab22d2835c6'),
        'inputs': {
            'ROOT_CERTIFICATE': (R15, 'e0777bb5d1aeba5ce60799f5bf678b9e0bf2cf0137349103117548892f9c8a25'),
            'FINITE_R36_CONTROL': (
                '05_REPRODUCCION/COMUN/CERTIFICADOS_K/entradas_selector/CERTIFICADO_SELECTOR_INTERNO.json',
                'ea0f8f335f60cc23d07dcfcbbf58c88675b819c8f2c5f65c87d7a0654e819e44'),
        },
        'outputs': ['CERTIFICADO_SELECTOR_GLOBAL.json'],
        'scope': 'Original regional-reader main, including its finite posterior R36 control. No Lean or new global mathematical claim.',
    },
    'n69': {
        'source': (K + '/python/regenerate_n69_original.py',
                   '93f7eb9183ff8f3d8b9757640c0fda8d6be0924579b5dd2590cebdb65450e4ef'),
        'inputs': {
            'READER': (K + '/python/lectores_regionales.py',
                       '50249c422bec1f3614bacc3982d8cc9ec096bd2f089a5a0ef6d0fab22d2835c6'),
            'SIGNATURE_OWNER': (
                '05_REPRODUCCION/REFERENCIAS/TRATADO/datos/GENERACION/G9_MONODROMIA/hmt_puerta_ley01_taxonomia_ciclos.py',
                'd6e6574b0b7e91a1105865e0e082e5390dffaf281692d9564f84c926d79d8652'),
            'REFERENCE': (K + '/datos/N69_TESTIGO_POSTERIOR.csv',
                          '4f022ee0f1cf43b38e49f026607dc0bdb08a98d210d2b255fad265c2099011f7'),
        },
        'outputs': ['N69_REGENERATED.csv', 'N69_REGENERATION.json'],
        'scope': 'Original N69 finite generator/comparison. The reference table is read only after generation, as in the unchanged source.',
    },
    'refinamiento_carta': {
        'source': (
            '05_REPRODUCCION/REFERENCIAS/TRATADO/evidencia/complementaria/inventario_genealogico/REV03_PASOS_Y_CONTRATOS/22_verificar_refinamiento_cambio_carta.py',
            'bf61698e9f9da60bf7507a0edac877530026196798bcaf8649cc1deabf7fd68f'),
        'inputs': {
            'OWNER': ('05_REPRODUCCION/COMUN/REFINAMIENTO_CARTA/construir_libro_pleno.py',
                      'daa14f6551652dce0b6f352ae5c2736e8d033e0f88a23465c821735238ce2776'),
        },
        'outputs': ['REFINAMIENTO_CAMBIO_CARTA.json'],
        'scope': 'Original focal run(): integer identities/inverses, half-open intervals and explicit rational fixtures. The original consumer extracts only require/encode_trits/Cylinder by AST; it does not execute the owner campaign or certify global selection.',
    },
    'rombo': {
        'source': (
            '05_REPRODUCCION/REFERENCIAS/TRATADO/evidencia/complementaria/lectura_dodecafasica/rombo_nueve_fases/verificar_rombo_nueve_fases.py',
            '4efdfb6bee82d4c437c695457335b52739f9fa332f32c70c564896b0c68d4a23'),
        'input_manifest': (
            '05_REPRODUCCION/COMUN/ROMBO_HISTORICO/ENTRADAS.json',
            '9a949635cd377bc43c80ac893580e0f212ea87dc968839ccb8e35ebb9cc0e89f'),
        'stored_certificate': (
            '05_REPRODUCCION/REFERENCIAS/TRATADO/evidencia/complementaria/lectura_dodecafasica/rombo_nueve_fases/CERTIFICADO_ROMBO_NUEVE_FASES.json',
            '0d9c4466a410109dc297558a8b97376a668964ace26f987f1aa44692c55f8403'),
        'outputs': ['CERTIFICADO_ROMBO_NUEVE_FASES.json'],
        'scope': 'Historical cited rombo control with its frozen CURRENT 2026-07-22.2. Not a current HMT generator, authority change or new mathematical validation. Original finite, primitive-conditioned and posterior-recognition layers remain unchanged.',
    },
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def locate_root(explicit: Path | None) -> Path:
    if explicit is not None:
        root = explicit.expanduser().resolve()
        if not (root / '06_VERIFICACION/MANIFIESTO.json').is_file():
            raise ValueError('--usb-root must identify the delivery root with 06_VERIFICACION/MANIFIESTO.json')
        return root
    for root in Path(__file__).resolve().parents:
        if (root / '06_VERIFICACION/MANIFIESTO.json').is_file():
            return root
    raise ValueError('Delivery not found. Provide --usb-root /path/to/ENTREGA_HMT_USB')


class HistoricalInputPath(type(Path())):
    """Native file access; historical provenance keys always use forward slashes."""

    def relative_to(self, *other):
        return PurePosixPath(super().relative_to(*other).as_posix())


class HistoricalCertificatePath(type(Path())):
    """Keep the preserved JSON's LF line endings on every operating system."""

    def write_text(self, data, encoding=None, errors=None, newline=None):
        with self.open('w', encoding=encoding, errors=errors, newline='\n') as handle:
            return handle.write(data)


def input_path(root: Path, relative: str, overlay: Path | None = None) -> Path:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or '..' in rel.parts or '\\' in relative or ':' in relative:
        raise ValueError('Unsafe relative input path: ' + relative)
    path = root / relative
    # Staging is a plan-only fallback, never a substitute for existing delivery
    # bytes and never available to execution.
    if not path.exists() and overlay is not None:
        return overlay / relative
    return path


def unit_spec(root: Path, unit: str, overlay: Path | None = None) -> dict:
    spec = dict(UNITS[unit])
    if unit == 'rombo':
        relative, expected = spec['input_manifest']
        manifest_path = input_path(root, relative, overlay)
        if not manifest_path.is_file() or digest(manifest_path) != expected:
            raise ValueError('Rombo path manifest missing or SHA-256 mismatch: ' + str(manifest_path))
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        entries = manifest['entries']
        if manifest['schema'] != 'hmt-historical-rombo-path-bindings-v1' or len(entries) != 16:
            raise ValueError('Unexpected rombo input manifest')
        spec['inputs'] = {name: (row['path'], row['sha256']) for name, row in entries.items()}
        spec['historical_paths'] = {name: row['historical_path'] for name, row in entries.items()}
        for relative in spec['historical_paths'].values():
            input_path(root, relative)  # Reject non-relative and traversal paths.
    return spec


def inspect_inputs(root: Path, unit: str, overlay: Path | None = None) -> dict:
    spec = unit_spec(root, unit, overlay)
    rows = []
    items = {'source': spec['source'], **spec['inputs']}
    if unit == 'rombo':
        items.update(input_manifest=spec['input_manifest'], stored_certificate=spec['stored_certificate'])
    for role, (relative, expected) in items.items():
        path = input_path(root, relative, overlay)
        actual = digest(path) if path.is_file() else None
        rows.append({'role': role, 'relative_path': relative, 'path': str(path),
                     'input_origin': 'delivery' if path == root / relative else 'staging',
                     'expected_sha256': expected, 'actual_sha256': actual,
                     'status': 'MATCH' if actual == expected else 'MISSING' if actual is None else 'HASH_MISMATCH'})
    good = all(row['status'] == 'MATCH' for row in rows)
    # Syntax/declared definitions only; no module import or scientific execution.
    syntax = False
    if good:
        tree = ast.parse(input_path(root, spec['source'][0], overlay).read_bytes())
        required = 'run' if unit == 'refinamiento_carta' else 'main'
        syntax = any(isinstance(node, ast.FunctionDef) and node.name == required for node in tree.body)
        if unit == 'refinamiento_carta':
            owner = ast.parse((root / spec['inputs']['OWNER'][0]).read_bytes())
            found = {node.name for node in owner.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
            syntax = syntax and {'require', 'encode_trits', 'Cylinder'} <= found
        if unit == 'rombo':
            definitions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
            syntax = syntax and {'main', 'build_result', 'source_hashes'} <= definitions
            stored = json.loads(input_path(root, spec['stored_certificate'][0], overlay).read_text(encoding='utf-8'))
            planned_keys = {spec['historical_paths'][name]: expected for name, (_, expected) in spec['inputs'].items()}
            syntax = syntax and planned_keys == stored['source_sha256']
            current = json.loads(input_path(root, spec['inputs']['CURRENT'][0], overlay).read_text(encoding='utf-8'))
            syntax = syntax and current['revision'] == '2026-07-22.2'
    report = {'unit': unit, 'status': 'PASS_STATIC_PLAN' if good and syntax else 'DEPENDENCY_OR_SYNTAX_FAILURE',
            'source_and_inputs': rows, 'syntax_and_entrypoint_present': syntax,
            'science_executed': False, 'compiler_invoked': False,
            'scope': spec['scope'], 'planned_output_names': spec['outputs']}
    if unit == 'rombo':
        tail = max(len('i/' + name) for name in spec['historical_paths'].values())
        report.update(historical_provenance_keys_retained=True,
                      maximum_external_historical_tail=tail,
                      maximum_output_root_characters_for_259_path_limit=259 - 1 - tail,
                      preserved_certificate_comparison='Only performed during explicit execution; not --plan')
    return report


def execute(root: Path, unit: str, output: Path, plan: dict) -> dict:
    if sys.flags.optimize:
        raise ValueError('Execution under -O is refused: the intact focal source may use assert checks')
    out = output.expanduser().resolve()
    if out == root or out.is_relative_to(root):
        raise ValueError('--output-dir must be outside the entire delivery')
    if out.exists():
        raise ValueError('--output-dir must be a new, nonexistent directory')
    spec = unit_spec(root, unit)
    if unit == 'rombo':
        longest = max(len(str(out / 'i' / name)) for name in spec['historical_paths'].values())
        if longest > 259:
            raise ValueError('Rombo external historical view exceeds 259 characters; choose a shorter --output-dir')
    source = root / spec['source'][0]
    report = {'unit': unit, 'status': 'RUNNING', 'science_executed': False,
              'compiler_invoked': False, 'scope': spec['scope'], 'plan': plan,
              'output_directory': str(out), 'path_bindings_only': {},
              'original_source_rewritten': False}
    out.mkdir(parents=True, exist_ok=False)
    old_argv, old_bytecode = sys.argv, sys.dont_write_bytecode
    module_name = '_hmt_portable_original_' + unit
    try:
        # Register a normal non-main module so inspect.getmodule/getsource and
        # dataclass metadata continue to use the authenticated original source.
        sys.dont_write_bytecode = True
        module_spec = importlib.util.spec_from_file_location(module_name, source)
        if module_spec is None or module_spec.loader is None:
            raise RuntimeError('Cannot prepare original scientific module')
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        # Compile the authenticated .py bytes in memory, bypassing any existing
        # .pyc cache as well as preventing new cache files on the delivery.
        raw = source.read_bytes()
        if hashlib.sha256(raw).hexdigest() != spec['source'][1]:
            raise RuntimeError('Original source changed after the static plan')
        exec(compile(raw, str(source), 'exec'), module.__dict__)
        historical_root = out / 'i'
        for name, (relative, expected) in spec['inputs'].items():
            if not hasattr(module, name):
                raise RuntimeError('Original path binding absent: ' + name)
            bound = root / relative
            if unit == 'rombo':
                bound = HistoricalInputPath(historical_root / spec['historical_paths'][name])
                bound.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / relative, bound)
                if digest(bound) != expected:
                    raise RuntimeError('External historical input copy mismatch: ' + name)
            setattr(module, name, bound)
            report['path_bindings_only'][name] = str(bound)
        report['science_executed'] = True
        if unit == 'regional':
            module.OUTPUT = out / 'CERTIFICADO_SELECTOR_GLOBAL.json'
            report['path_bindings_only']['OUTPUT'] = str(module.OUTPUT)
            sys.argv = [str(source)]
            module.main()
        elif unit == 'n69':
            sys.argv = [str(source), '--output', str(out)]
            module.main()
        elif unit == 'refinamiento_carta':
            result = module.run()
            (out / 'REFINAMIENTO_CAMBIO_CARTA.json').write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        else:
            module.ROOT = historical_root
            module.HERE = out
            module.CERTIFICATE = HistoricalCertificatePath(out / 'CERTIFICADO_ROMBO_NUEVE_FASES.json')
            report['path_bindings_only'].update(ROOT=str(module.ROOT), HERE=str(out), CERTIFICATE=str(module.CERTIFICATE))
            sys.argv = [str(source), '--write-certificate']
            module.main()
            # Preserve the original's output and compare bytes, not a mutated
            # result dictionary. No current authority is read or rolled back.
            preserved = root / spec['stored_certificate'][0]
            report['preserved_certificate_byte_equal'] = module.CERTIFICATE.read_bytes() == preserved.read_bytes()
            report['external_historical_input_bytes_unchanged'] = all(
                digest(historical_root / spec['historical_paths'][name]) == expected
                for name, (_, expected) in spec['inputs'].items())
            if not report['preserved_certificate_byte_equal'] or not report['external_historical_input_bytes_unchanged']:
                raise RuntimeError('Historical certificate or external input comparison differs; originals remain untouched')
        after = inspect_inputs(root, unit)
        if after['status'] != 'PASS_STATIC_PLAN':
            raise RuntimeError('Authenticated source/input changed during execution')
        report['outputs'] = []
        for name in spec['outputs']:
            path = out / name
            if not path.is_file():
                raise RuntimeError('Expected external output absent: ' + name)
            report['outputs'].append({'name': name, 'sha256': digest(path), 'bytes': path.stat().st_size})
        report['source_and_input_bytes_unchanged'] = True
        report['status'] = 'ORIGINAL_PROGRAM_COMPLETED'
    except Exception as error:
        report.update(status='ADAPTER_OR_ORIGINAL_PROGRAM_FAILED', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        sys.argv, sys.dont_write_bytecode = old_argv, old_bytecode
        sys.modules.pop(module_name, None)
        (out / 'RECIBO_ADAPTADOR.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--unit', choices=[*UNITS, 'all'], required=True,
                        help='all is permitted only with --plan')
    parser.add_argument('--plan', action='store_true', help='Hash/syntax checks only; no science or file writes')
    parser.add_argument('--usb-root', type=Path, help='Delivery root; inferred from this script location when installed')
    parser.add_argument('--output-dir', type=Path, help='Mandatory for execution; fresh directory outside delivery')
    parser.add_argument('--input-overlay', type=Path,
                        help='Plan only: staged delivery-relative files used only when absent from the delivery')
    args = parser.parse_args(argv)
    if args.input_overlay is not None and not args.plan:
        parser.error('--input-overlay is permitted only with --plan; execution reads installed delivery files')
    if not args.plan and (args.output_dir is None or args.unit == 'all'):
        parser.error('Execution requires one --unit and a fresh external --output-dir')
    root = locate_root(args.usb_root)
    names = list(UNITS) if args.unit == 'all' else [args.unit]
    overlay = args.input_overlay.expanduser().resolve() if args.input_overlay is not None else None
    plans = [inspect_inputs(root, name, overlay) for name in names]
    passed = all(plan['status'] == 'PASS_STATIC_PLAN' for plan in plans)
    if args.plan or not passed:
        print(json.dumps({'status': 'PASS_STATIC_PLANS' if passed else 'DEPENDENCY_FAILURE',
                          'delivery_root': str(root), 'science_executed': False,
                          'delivery_written': False, 'plans': plans}, ensure_ascii=False, indent=2))
        return 0 if passed else 2
    result = execute(root, args.unit, args.output_dir, plans[0])
    print(json.dumps({'status': result['status'], 'output_directory': result['output_directory'],
                      'receipt': str(Path(result['output_directory']) / 'RECIBO_ADAPTADOR.json')}, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({'status': 'ADAPTER_ERROR', 'error_type': type(error).__name__, 'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
