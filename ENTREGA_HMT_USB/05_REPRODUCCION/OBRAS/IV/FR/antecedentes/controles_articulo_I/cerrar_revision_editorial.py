"""Registra la inspección visual humana y verifica los artefactos correspondientes.

No compila ni altera demostraciones. Requiere --visual-reviewed después de
examinar las hojas de contacto y las ampliaciones descritas en el informe.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
from pypdf import PdfReader

D = Path(__file__).resolve().parent.parent
W = Path('/Users/ruben/Documents/New project')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--visual-reviewed', action='store_true', required=True)
    parser.parse_args()
    manifest_path = D/'COMPROBACION_EDITORIAL.json'
    manifest = json.loads(manifest_path.read_text())
    for artifact in manifest['artifacts']:
        assert digest(Path(artifact['path'])) == artifact['sha256']
        assert digest(Path(artifact['text'])) == artifact['text_sha256']
    for path, value in manifest['source_files'].items():
        assert digest(D/path) == value, path
    main_artifact, supplement = manifest['artifacts']
    assert main_artifact['pages'] == 62
    assert supplement['pages'] == 337
    assert supplement['newly_composed_pages'] == 13
    assembled = PdfReader(supplement['path'])
    seed_path = Path(supplement['seed_appendix']['path'])
    assert digest(seed_path) == supplement['seed_appendix']['sha256']
    seeds = PdfReader(seed_path)
    for index, source in enumerate(seeds.pages):
        target = assembled.pages[index + 13]
        assert source.get_contents().get_data() == target.get_contents().get_data(), index
        assert tuple(source.mediabox) == tuple(target.mediabox), index
    commands = [
        [sys.executable, '-I', '-S', str(D/'technical/preparar_recibo_genealogico.py'), '--bind'],
        [sys.executable, '-I', '-S', str(W/'tools/verificar_genealogia_unica_hmt.py'), '--receipt', str(D/'technical/RECIBO_GENEALOGICO_ARTICULO.json')],
    ]
    gate = Path('/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py')
    for artifact in manifest['artifacts']:
        commands.append([sys.executable, '-I', '-S', str(gate), '--audit', artifact['text'], '--receipt', artifact['causal_receipt']])
    controls = []
    for command in commands:
        run = subprocess.run(command, cwd=D, text=True, capture_output=True)
        controls.append({'command': command, 'returncode': run.returncode,
                         'stdout': run.stdout, 'stderr': run.stderr})
        if run.returncode:
            raise RuntimeError(run.stdout + run.stderr)
    report = {
        'status': 'EDITORIAL_REVIEW_COMPLETED_FOR_WORKING_DRAFT',
        'mathematical_autonomy_claimed': False,
        'main_contact_review': {'pages': 62, 'directory': str(D/'qa/articulo_final'),
                                'final_text_sha256_unchanged': main_artifact['text_sha256']},
        'main_enlargements': [1, 7, 20, 52],
        'supplement_contact_review': {'pages': 13, 'directory': str(D/'qa/suplemento_entrega')},
        'supplement_enlargements': [13],
        'seed_census_review': {'all_324_page_streams_identical': True,
                               'visual_samples_preexisting': [1, 2, 81, 162, 324],
                               'visual_sample_rechecked': 1},
        'layout_corrections': ['APP grid repositioned between digits',
                               'Removed isolated continuation page in supplement',
                               'Census presentation consolidated without deleting content'],
        'receipt_parser_note': ('The first genealogy check matched TODO inside Spanish todos/todo, '
                                'and /RUTA/ inside a slash-separated list of conserved quantities. '
                                'Receipt wording was made equivalent and unambiguous without changing '
                                'the verifier, proof status, residual dependencies or mathematical scope.'),
        'controls': controls,
        'remaining_expository_dependencies': [
            'E108: executable action on effective ledger incidence generators',
            'E21/22: autonomous coefficient rule at degrees >=10 and uniform tail estimates',
            'Exceptional incidence: explicit transport of charts, frames and binary lift'],
        'arithmetic_question_not_closed': 'Rationality, irrationality or transcendence of alpha and pi+e',
    }
    report_path = D/'technical/CONTROLES_CIERRE_EDITORIAL.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    manifest['visual_review'] = report['status']
    manifest['visual_review_report'] = str(report_path)
    manifest['seed_stream_integrity'] = '324/324 identical to existing census'
    manifest['autonomous_monograph_complete'] = False
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps({'status': report['status'], 'pages': [62, 337],
                      'seed_pages_identical': 324, 'controls_passed': len(controls)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
