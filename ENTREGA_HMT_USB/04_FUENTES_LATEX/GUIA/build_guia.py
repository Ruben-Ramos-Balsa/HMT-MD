#!/usr/bin/env python3
"""Portable, explicit rendering of the frozen ES/EN/FR guide sources.

The original builders remain byte-identical. This entrypoint uses their drawing
functions and sequence with explicit font configuration and output paths.
No PDF is created without --render.
"""
from pathlib import Path
import argparse
import ast
import copy
import hashlib
import importlib.metadata
import json
import os
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
LANGUAGES = ('ES', 'EN', 'FR')
FONT_ALIASES = ('Serif', 'SerifB', 'SerifI', 'Sans', 'SansB', 'Math')
MANIFEST = 'INTEGRIDAD_FUENTES.json'
PACKAGES = ('reportlab', 'matplotlib', 'svglib', 'Pillow', 'pypdf')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree_digest(node):
    return hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()


def verify_files(root=ROOT):
    manifest = json.loads((root / MANIFEST).read_text(encoding='utf-8'))
    require(manifest['schema'] == 'GUIDE_PORTABLE_SOURCE_SNAPSHOT_V1', 'Unknown source snapshot')
    expected = set()
    for item in manifest['files']:
        relative = Path(item['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'Invalid relative source path')
        path = root / relative
        require(path.is_file() and not path.is_symlink(), 'Missing or redirected source: ' + str(relative))
        require(path.resolve().is_relative_to(root.resolve()), 'Source leaves package')
        require(path.stat().st_size == item['bytes'] and sha(path) == item['sha256'],
                'Source changed since snapshot: ' + str(relative))
        expected.add(relative.as_posix())
    # Ignore Python caches, but never accept unregistered content in source/shared.
    actual = set()
    for directory in [root / lang / 'source' for lang in LANGUAGES] + [root / 'shared']:
        for path in directory.rglob('*'):
            if '__pycache__' in path.parts or path.name in ('.DS_Store',):
                continue
            require(not path.is_symlink(), 'Redirected package item: ' + str(path))
            if path.is_file():
                actual.add(path.relative_to(root).as_posix())
    expected_sources = {p for p in expected if p.split('/')[0] in (*LANGUAGES, 'shared')}
    require(actual == expected_sources, 'Source inventory differs from the frozen selection')
    return manifest


def is_call(node, name):
    return isinstance(node, ast.Call) and ast.unparse(node.func) == name


def portable_tree(language, root=ROOT):
    """Keep the drawing AST exactly; replace only I/O, font paths and dispatch."""
    path = root / language / 'source' / 'build_dossier.py'
    original = ast.parse(path.read_bytes(), filename=str(path))
    functions = {n.name: n for n in original.body if isinstance(n, ast.FunctionDef)}
    require('main' in functions and 'check_final_document_reception' in functions, 'Builder structure changed')
    main = functions['main']
    starts = [i for i, n in enumerate(main.body) if isinstance(n, ast.Assign)
              and is_call(n.value, 'canvas.Canvas')]
    ends = [i for i, n in enumerate(main.body) if isinstance(n, ast.Expr) and is_call(n.value, 'c.save')]
    require(len(starts) == len(ends) == 1 and starts[0] < ends[0], 'Ambiguous drawing sequence')
    drawing = copy.deepcopy(main.body[starts[0]:ends[0] + 1])
    helpers = [n for n in original.body if isinstance(n, ast.FunctionDef)
               and n.name not in ('main', 'check_final_document_reception')]
    prefix = []
    removed = []
    for node in original.body:
        if isinstance(node, (ast.FunctionDef, ast.If)):
            continue
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'FONT' for t in node.targets):
            removed.append('FONT')
            continue
        if isinstance(node, ast.For):
            require('pdfmetrics.registerFont' in ast.unparse(node), 'Unexpected module loop')
            removed.append('registerFont loop')
            continue
        prefix.append(copy.deepcopy(node))
    require(removed == ['FONT', 'registerFont loop'], 'Unexpected font initialization')
    render = copy.deepcopy(main)
    render.name = 'render_portable'
    render.args = ast.arguments(posonlyargs=[], args=[ast.arg(arg='target'), ast.arg(arg='data')],
                                vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])
    render.body = ast.parse("docs = data['documents']").body + drawing
    tree = ast.fix_missing_locations(ast.Module(body=prefix + copy.deepcopy(helpers) + [render], type_ignores=[]))
    transformed = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    require(all(tree_digest(transformed[n.name]) == tree_digest(n) for n in helpers), 'Drawing helper changed')
    require(all(tree_digest(a) == tree_digest(b) for a, b in zip(drawing, render.body[1:])), 'Drawing sequence changed')
    # Original EN wrapper currently checks the already-corrected literal; it does not rewrite it.
    if language == 'EN':
        wrapper_path = path.with_name('build_dossier_final.py')
        wrapper = ast.parse(wrapper_path.read_bytes(), filename=str(wrapper_path))
        constants = {n.targets[0].id: n.value.value for n in wrapper.body
                     if isinstance(n, ast.Assign) and len(n.targets) == 1
                     and isinstance(n.targets[0], ast.Name) and isinstance(n.value, ast.Constant)}
        require(constants.get('BASE_SHA256') == sha(path), 'English frozen-builder hash mismatch')
        corrected = next(n for n in wrapper.body if isinstance(n, ast.FunctionDef) and n.name == 'corrected_tree')
        require(not any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Attribute) and t.attr == 'value'
                    for t in n.targets) for n in ast.walk(corrected)), 'English correction wrapper changed: review needed')
        require(sum(isinstance(n, ast.Constant) and n.value == '.<br/>Conservation'
                    for n in ast.walk(functions['fiches'])) == 1, 'English fiche correction is missing')
    compile(tree, str(path), 'exec')  # Syntax validation only; this never imports or draws.
    report = {
        'language': language,
        'unchanged_helpers': [n.name for n in helpers],
        'drawing_sequence_ast_sha256': tree_digest(ast.Module(body=drawing, type_ignores=[])),
        'drawing_statements': len(drawing),
        'drawing_helpers_ast_equal': True,
        'drawing_sequence_ast_equal': True,
        'replaced_environment': ['font registration from explicit fontmap', 'UTF-8 content loading',
                                 'relative snapshot integrity', 'explicit destination and new build report'],
        'source_integrity': 'SHA256_RELATIVE_MANIFEST',
    }
    return tree, report


def inspect_sources(root=ROOT):
    reports = []
    for language in LANGUAGES:
        _, report = portable_tree(language, root)
        reports.append(report)
        content = json.loads((root / language / 'source' / 'contenido.json').read_text(encoding='utf-8'))
        docs = content['documents']
        require(len(docs) == 17 and len({d['id'] for d in docs}) == 17, 'Document inventory mismatch')
        for doc in docs:
            cover = root / language / 'source' / doc['cover']
            require(cover.resolve().is_relative_to((root / language / 'source').resolve()) and cover.is_file(),
                    'Missing or redirected cover: ' + doc['id'])
    return reports


def register_fonts(fontmap_path):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    fontmap_path = fontmap_path.resolve(strict=True)
    config = json.loads(fontmap_path.read_text(encoding='utf-8'))
    require(config['schema'] == 'GUIDE_FONTMAP_V1', 'Unknown fontmap schema')
    require(set(config['fonts']) == set(FONT_ALIASES), 'Exactly six font aliases are required')
    result = {}
    for alias in FONT_ALIASES:
        entry = config['fonts'][alias]
        path = Path(entry['path']).expanduser()
        if not path.is_absolute():
            path = fontmap_path.parent / path
        require(path.is_file(), 'Install the licensed font or correct fontmap: ' + alias + ' / ' + str(path))
        digest = sha(path)
        if entry.get('sha256'):
            require(digest == entry['sha256'], 'Font hash mismatch: ' + alias)
        font = TTFont(alias, str(path))
        name = font.face.name.decode('utf-8', errors='replace') if isinstance(font.face.name, bytes) else str(font.face.name)
        require(name == entry['postscript_name'], 'Unexpected font identity: ' + alias + ' / ' + name)
        pdfmetrics.registerFont(font)
        # Use only a filename in the portable report; no personal path is exported.
        result[alias] = {'file': path.name, 'postscript_name': name, 'sha256': digest}
    return result


def load_namespace(language):
    tree, report = portable_tree(language)
    namespace = {'__name__': 'guide_portable_' + language,
                 '__file__': str(ROOT / language / 'source' / 'build_dossier.py')}
    exec(compile(tree, namespace['__file__'], 'exec'), namespace)
    # Import the only shared module used by the guide, even in environment-check mode.
    sys.path.insert(0, str(ROOT / 'shared'))
    import poster_layout
    require(Path(poster_layout.__file__).resolve() == ROOT / 'shared' / 'poster_layout.py', 'Unexpected shared layout')
    return namespace, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check-only', action='store_true', help='stdlib-only integrity and AST checks, no imports or PDF')
    mode.add_argument('--check-environment', action='store_true', help='check dependencies, fonts and imports, no PDF')
    mode.add_argument('--render', action='store_true', help='explicitly render a new local PDF')
    parser.add_argument('--language', choices=LANGUAGES)
    parser.add_argument('--fontmap', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    snapshot = verify_files()
    static = inspect_sources()
    if args.check_only:
        print(json.dumps({'status': 'STATIC_SOURCE_CHECK_OK', 'rendered': False,
                          'files': len(snapshot['files']), 'languages': static}, ensure_ascii=False, indent=2))
        return
    require(args.fontmap is not None, '--fontmap is required')
    require(not args.render or args.language is not None, '--language is required for rendering')
    require(not args.render or args.output is not None, '--output is required for rendering')
    sys.dont_write_bytecode = True
    os.environ['MPLBACKEND'] = 'Agg'
    with tempfile.TemporaryDirectory(prefix='guide-matplotlib-') as cache:
        os.environ['MPLCONFIGDIR'] = cache
        versions = {name: importlib.metadata.version(name) for name in PACKAGES}
        fonts = register_fonts(args.fontmap)
        selected = (args.language,) if args.language else LANGUAGES
        modules = {language: load_namespace(language) for language in selected}
        if args.check_environment:
            print(json.dumps({'status': 'ENVIRONMENT_IMPORT_CHECK_OK', 'rendered': False,
                              'languages': list(selected), 'packages': versions, 'fonts': fonts},
                             ensure_ascii=False, indent=2))
            return
        output = args.output.expanduser().resolve()
        require(output.suffix.lower() == '.pdf', 'Destination must be a PDF filename')
        require(not output.exists(), 'Refusing to overwrite an existing output')
        metrics_path = output.with_suffix('.layout_metrics.json')
        report_path = output.with_suffix('.build.json')
        require(not metrics_path.exists() and not report_path.exists(), 'Output sidecar already exists')
        output.parent.mkdir(parents=True, exist_ok=True)
        namespace, geometry = modules[args.language]
        content = json.loads((ROOT / args.language / 'source' / 'contenido.json').read_text(encoding='utf-8'))
        namespace['render_portable'](output, content)
        from pypdf import PdfReader
        pages = len(PdfReader(str(output)).pages)
        report = {'schema': 'GUIDE_PORTABLE_RENDER_V1', 'status': 'GENERATED_PENDING_VISUAL_QA',
                  'language': args.language, 'pdf': output.name, 'pdf_sha256': sha(output),
                  'pages': pages, 'expected_pages': 20, 'packages': versions, 'fonts': fonts,
                  'source_snapshot_sha256': sha(ROOT / MANIFEST), 'geometry': geometry,
                  'scientific_recalculation': False}
        if pages != 20:
            report['status'] = 'PAGECOUNT_MISMATCH_REVIEW_REQUIRED'
        metrics_path.write_text(json.dumps(namespace['metrics'], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        require(pages == 20, 'PDF generated with unexpected pagination; see ' + report_path.name)
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, ImportError) as exc:
        raise SystemExit(str(exc)) from exc
