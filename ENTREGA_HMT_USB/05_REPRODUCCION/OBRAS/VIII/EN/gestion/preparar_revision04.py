#!/usr/bin/env python3
"""PROPUESTA no ejecutada: corte VII REV04; nunca emite PASS de preflight.

Sólo crea una carpeta nueva de propuesta y preservación dentro de VII.
No modifica manuscritos, verificadores históricos, claims.json ni evidence.json.
El alta la revisa/aplica el editor; el recibo lo produce precompile_hmt_md.py.
"""
import argparse
import copy
import difflib
import hashlib
import json
from pathlib import Path
import re
import runpy
import shutil
import sys

sys.dont_write_bytecode = True
WORKSPACE = Path('/Users/ruben/Documents/New project')
BASELINE = WORKSPACE / 'output/APERTURAS_PAPER_RESTAURADAS_20260911_REV03/VII_GRAVITACION'
SUCCESSOR = WORKSPACE / 'output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/VII_GRAVITACION'
TRUNK = Path('/Users/ruben/Documents/excelencia academica/HMT_SCIENTIFIC_TRUNK')
CLAIM = 'HMT-VII-S0-FUNCIONAL-CLIFFORD-CARTAN-20260910'
CONTEXT = 'HMT-APPLICATION-EJE-TRANSVERSAL-READERS'
READER_FILE = '80_observador_y_respuesta_relacional.tex'
# Único reemplazo no aditivo autorizado en 80: se fija su literal exacto.
# La reversión de este párrafo y las dos inserciones debe recuperar REV03.
READER_OPENING_BEFORE = r'''Los lectores areal y volumétrico, denotados aquí
\(A_\partial,V_\partial:B_{\rm ef}\to(0,\infty)\), y el reloj
energético \(Q:B_{\rm ef}\to(0,\infty)\) conservan su construcción
anterior en el estado HMT. La memoria permanece como coordenada
\(\mathsf M_\partial(\beta)\) de la frontera. La bisagra de
ambivalencia proporciona las dos orientaciones
'''
READER_OPENING_AFTER = r'''Para la fórmula general consideramos lectores positivos
\(A_\partial,V_\partial\) y un lector energético \(Q\)
definidos sobre el dominio efectivo de frontera declarado.
A continuación se explicita una realización sobre
\(B_{\rm av}\subseteq B_{\rm ef}\). La memoria permanece como coordenada
\(\mathsf M_\partial(\beta)\) de la frontera. La bisagra de
ambivalencia proporciona las dos orientaciones
'''
# Cinco deltas leídos: identidad exacta de los dos cortes, no permiso genérico.
EDITORIAL_HASHES = {
 '00_apertura.tex': ('b3c5c771a6a1141344aae0f1944024b4a510a1ea429d5b2c03dc406caef7246a', 'b3157a4200a969e9e1e365186994aecbdf8bb0d4c18771292166ac19a425dac1'),
 '30_pantalla_y_respuesta.tex': ('05dba05b444b0796a04b6b1cd43f7957de0d99bef411e7a47b6868500815f0c8', '7062cb026287a6a077e4b5d003d115f0d00956899b7c88e1550da40664e86507'),
 '50_dilucion_y_rebote.tex': ('a96969bbf92a4fddb82581fb4eaf9bf99f6d3bcb1408c1ba6b4702afe2213957', '7af9ce6ff3915922b0afae5a639bd8f17faf908f95d59e1faafff5abcd348cd8'),
 '90_conclusiones.tex': ('c8fb435cc3ce36af8c86860f2385d95ac5f2809ae1f19c8e1c01a6c2b5f87062', 'aa979f20b1f113fbbeb18f7615ef6cd53eafc81ed6a76ba8eb45d9febf871048'),
 'sections/extension.tex': ('5cf12c8dfdb158b99cf252b64af07df2fd1c20502821be9967c317d682b4e9b6', 'f5a1fe57baacdb8ac00d7c6507cf12fe6d5c390276e49acea2f7df56826e6a79'),
}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def read(path):
    return json.loads(Path(path).read_text())


def spec(path):
    return {'path': str(Path(path).resolve()), 'sha256': sha(path)}


def verified(item):
    path = Path(item['path']).resolve()
    require(path.is_file() and not path.is_symlink() and sha(path) == item['sha256'], 'Referencia alterada: ' + str(path))
    return path


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.exists(), 'No sobrescribir: ' + str(path))
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def exactly_once(text, old, new=''):
    require(text.count(old) == 1, 'Literal no único para comparación: ' + old)
    return text.replace(old, new, 1)


def comparison_copy(name, text):
    if name == '30_pantalla_y_respuesta.tex':
        require(text.count(r'q_{\mathrm{vis}}') == 3, 'Se esperan tres usos de q_vis, exclusivamente de compresión.')
        text = text.replace(r'q_{\mathrm{vis}}', 'q_9')
        # Tres menciones explicativas añadidas en el párrafo exacto de origen.
        # No retirar q_9(n) del manuscrito: sólo de esta copia de comparación.
        for literal in (r'\(5/9\)', r'\(B_c/9\)', r'\(q_9(n)\)'):
            text = exactly_once(text, literal)
    elif name == '50_dilucion_y_rebote.tex':
        added = (' La densidad ordinaria\n'
                 '\\(\\rho_0>0\\) y su ley barotrópica se especifican adicionalmente en la\n'
                 'sección~\\ref{vii:sec:umbral-rebote}: el testigo de positividad de la\n'
                 'amplitud no evalúa por sí mismo esa densidad material.')
        text = exactly_once(text, added)
    return text


def inspect_added_reader(before, after, review_spec, after_hash, root):
    review = read(verified(review_spec))
    require(review.get('reviewed_source_sha256') == after_hash, 'La revisión de 80 no liga el archivo final.')
    require(review.get('approved_for_manuscript_inclusion') is True, 'Falta revisión explícita de inclusión del añadido de 80.')
    require(review.get('technical_review_by') == 'root', 'La revisión del añadido debe identificar al editor root.')
    require(isinstance(review.get('scope'), str) and review['scope'].strip(), 'Falta alcance de la revisión del añadido.')
    require(review.get('whole_article_mathematical_certification') is False, 'El recibo debe distinguir revisión focal de certificación global.')
    require(before.count(READER_OPENING_BEFORE) == 1, 'Arranque original de 80 distinto o no único.')
    require(after.count(READER_OPENING_AFTER) == 1, 'Reemplazo inicial de 80 distinto al literal autorizado o no único.')
    literal_recovery = after
    snippets, additions = [], []
    for name in ('revision04_lectores.tex', 'revision04_pesos.tex'):
        path = root / 'gestion' / name
        # read_bytes().decode() conserva CR/LF; no strip ni normalización global.
        literal = path.read_bytes().decode('utf-8') + '\n\n'
        require(literal.strip(), 'Inserción vacía en 80: ' + name)
        require(after.count(literal) == 1, 'Inserción literal no única en 80: ' + name)
        start = after.index(literal)
        additions.append({'after_line_from_1': after.count('\n', 0, start) + 1,
                          'after_line_to_1': after.count('\n', 0, start + len(literal)),
                          'text': literal, 'sha256': hashlib.sha256(literal.encode('utf-8')).hexdigest()})
        literal_recovery = exactly_once(literal_recovery, literal)
        snippets.append({**spec(path), 'inserted_suffix_exact': '\n\n'})
    literal_recovery = exactly_once(literal_recovery, READER_OPENING_AFTER, READER_OPENING_BEFORE)
    require(literal_recovery.encode('utf-8') == before.encode('utf-8'),
            'Revertir el único arranque autorizado y las dos inserciones exactas no recupera REV03 byte por byte.')
    opening = {'before_text': READER_OPENING_BEFORE, 'after_text': READER_OPENING_AFTER,
               'before_sha256': hashlib.sha256(READER_OPENING_BEFORE.encode('utf-8')).hexdigest(),
               'after_sha256': hashlib.sha256(READER_OPENING_AFTER.encode('utf-8')).hexdigest(),
               'before_line_from_1': before.count('\n', 0, before.index(READER_OPENING_BEFORE)) + 1,
               'after_line_from_1': after.count('\n', 0, after.index(READER_OPENING_AFTER)) + 1,
               'scope': 'Formulación general de lectores y realización explícita en B_av; único reemplazo heredado autorizado.'}
    return {'prior_source_recovered_exactly': True, 'additions': additions, 'review': review_spec,
            'sole_authorized_initial_replacement': opening,
            'literal_source_snippets': snippets,
            'new_reader_proofs_certified_by_s0': False,
            'scope': 'Dos inserciones y un reemplazo inicial exactos, con revisión focal ligada al archivo; el certificado S0 conserva su dominio propio.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=SUCCESSOR)
    parser.add_argument('--baseline', type=Path, default=BASELINE)
    parser.add_argument('--declaration', type=Path, required=True)
    parser.add_argument('--run-name', default='editorial_cientifica_rev04')
    parser.add_argument('--pdf-name', default='GRAVITACION_TORSION_DINAMICA_COSMOLOGICA.pdf')
    args = parser.parse_args()
    root, baseline = args.root.resolve(), args.baseline.resolve()
    require(root == SUCCESSOR.resolve() and baseline == BASELINE.resolve(), 'Revisar el script antes de cambiar las raíces autorizadas.')
    require(re.fullmatch(r'[A-Za-z0-9_-]+', args.run_name), 'Nombre de run inválido.')
    require(Path(args.pdf_name).name == args.pdf_name and args.pdf_name.endswith('.pdf'), 'Nombre PDF inválido.')
    here = root / 'gestion/preflight_s0'
    previous = here / 'runs/editorial_rev07'
    run = here / 'runs' / args.run_name
    require(not run.exists(), 'El corte ya existe: preservar y seleccionar otro run-name.')
    declaration = read(args.declaration)
    require(declaration.get('technical_review_by') == 'root', 'Se requiere declaración del editor principal.')
    require(declaration.get('purpose') == 'BORRADOR_PARA_REVISION_AUTORAL', 'Alcance no reconocido.')
    require(declaration.get('author_review_of_exact_matrix_or_hashes') is False, 'No atribuir revisión de hashes al autor.')
    require(isinstance(declaration.get('reviewed_at_utc'), str) and
            re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', declaration['reviewed_at_utc']),
            'reviewed_at_utc debe ser fecha real de la revisión en formato UTC.')
    verified(declaration['authorial_authorization'])
    historical_checks = read(verified(declaration['historical_control_report']))
    reader_certificate = declaration['reader_certificate']
    program = verified(reader_certificate['program'])
    require(program == root / 'pruebas/verificar_lectores_frontera_rev04.py', 'Programa focal de lectores distinto.')
    normal = read(verified(reader_certificate['normal_result']))
    optimized = read(verified(reader_certificate['optimized_result']))
    require(normal == optimized, 'Resultados normal y optimizado de lectores distintos.')
    require(normal.get('status') == 'PASS_LECTORES_FRONTERA_REV04' and normal.get('exact_checks') == 60
            and normal.get('negative_controls') == 10 and normal.get('general_boundary_identification') is False
            and normal.get('new_global_physical_certificate') is False, 'Recibo focal de lectores inesperado.')
    helpers = runpy.run_path(str(here / 'preparar_expediente_s0.py'), run_name='readonly_helpers')
    blocks = runpy.run_path(str(here / 'refrescar_corte_documental.py'), run_name='readonly_blocks')['mathematical_blocks']
    files, edges = helpers['active_sources']()
    records = [{'path': str(p.relative_to(root / 'manuscrito')), 'sha256': sha(p)} for p in files]
    before_records = []
    for item in records:
        old = baseline / 'manuscrito' / item['path']
        require(old.is_file() and not old.is_symlink(), 'Fuente sin antecedente REV03: ' + item['path'])
        before_records.append({'path': item['path'], 'sha256': sha(old)})
    # El grafo completo previo se reconstruye: no confiar sólo en el ledger antiguo.
    old_helpers = runpy.run_path(str(baseline / 'gestion/preflight_s0/preparar_expediente_s0.py'), run_name='readonly_baseline')
    old_files, _ = old_helpers['active_sources']()
    require({str(p.relative_to(baseline / 'manuscrito')) for p in old_files} == {r['path'] for r in records}, 'Fuentes activas ganadas o perdidas: integración distinta a la autorizada.')
    before_hashes = {r['path']: r['sha256'] for r in before_records}
    after_hashes = {r['path']: r['sha256'] for r in records}
    changed = {p for p in before_hashes if before_hashes[p] != after_hashes[p]}
    expected = set(EDITORIAL_HASHES) | {READER_FILE}
    require(changed == expected, 'Se esperan los cinco deltas editoriales más el añadido de 80; diferencias: ' + repr(sorted(changed ^ expected)))
    declared = {r['path']: r for r in declaration['changes']}
    require(len(declared) == len(declaration['changes']) and set(declared) == changed, 'Declaración incompleta o duplicada.')
    changes = []
    for name in sorted(changed):
        item = declared[name]
        require((item['before_sha256'], item['after_sha256']) == (before_hashes[name], after_hashes[name]), 'Hashes declarados distintos: ' + name)
        require(isinstance(item.get('reason'), str) and item['reason'].strip(), 'Falta motivo: ' + name)
        before = (baseline / 'manuscrito' / name).read_bytes().decode('utf-8')
        after = (root / 'manuscrito' / name).read_bytes().decode('utf-8')
        if name == READER_FILE:
            require(before_hashes[name] == '8436a66f7bb661cd63e1cdc7503df46b91e638ca983a2920eec99cba3d23aec5', 'El antecedente 80 de REV03 cambió.')
            detail = inspect_added_reader(before, after, item['addition_review'], after_hashes[name], root)
        else:
            require(EDITORIAL_HASHES[name] == (before_hashes[name], after_hashes[name]), 'Delta editorial no coincide con los cinco archivos leídos: ' + name)
            require(blocks(before) == blocks(comparison_copy(name, after)), 'Bloques matemáticos anteriores alterados fuera de las equivalencias locales: ' + name)
            old_labels = re.findall(r'\\label\{([^}]+)\}', before)
            new_labels = re.findall(r'\\label\{([^}]+)\}', after)
            if name == 'sections/extension.tex':
                require(new_labels.count('vii:sec:bloque-compresion') == 1, 'Etiqueta focal no única.')
                new_labels.remove('vii:sec:bloque-compresion')
            require(old_labels == new_labels, 'Etiquetas previas alteradas: ' + name)
            detail = {'prior_mathematical_blocks_preserved_under_enumerated_local_comparison': True,
                      'notation_scope': 'Tres usos q_vis de compresión; q_9(n) no se cambia en el manuscrito.' if name.startswith('30_') else None}
        changes.append({**item, 'detail': detail,
            'diff': ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='REV03/'+name, tofile='REV04/'+name))})
    tests = runpy.run_path(str(root / 'pruebas/verificar_paquete_local.py'), run_name='readonly_test_list')['TESTS']
    require(len(tests) == 13, 'Censo de verificadores histórico distinto.')
    test_hashes = []
    for name, _ in tests:
        relative = 'pruebas/' + name
        require(sha(root / relative) == sha(baseline / relative), 'Verificador histórico modificado: ' + relative)
        test_hashes.append({'path': relative, 'sha256': sha(root / relative)})
    for name in ('31_corriente_y_respuesta_cartan.tex', '33_corriente_espinorial_y_densidad.tex'):
        require(before_hashes[name] == after_hashes[name], 'Prueba focal S0 modificada: requiere revisión propia.')
    contract = read(previous / 'CONTRATO_PRECOMPILACION.json')
    for key in ('application_dossier', 'physical_certificate_manifest'):
        verified(contract[key])
    for item in contract['evidence']:
        verified(item)
    for certificate in contract['certificates']:
        verified(certificate['program'])
        for item in certificate['inputs']:
            verified(item)
    scientific_gate_hashes = {name: spec(verified(item)) for name, item in contract['gates'].items()}
    authority_before = {name: sha(TRUNK / name) for name in ('claims.json', 'evidence.json', 'causal_graph.json')}
    # No se escribe nada hasta superar los controles de preparación anteriores.
    run.mkdir(parents=True)
    preserved = run / 'preservacion_rev03'
    for name in sorted(changed):
        destination = preserved / 'manuscrito' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(baseline / 'manuscrito' / name, destination)
        require(sha(destination) == before_hashes[name], 'Copia previa divergente: ' + name)
    declaration_record = {'schema': 'hmt.vii.rev04.documentary_and_exact_reader_delta.v2',
        'status': 'PREPARACION_DOCUMENTAL_CON_DELTAS_EXACTOS', 'baseline': str(baseline),
        'source_root': str(root / 'manuscrito'), 'declaration': spec(args.declaration),
        'changes': changes, 'active_source_count': len(records),
        'unchanged_active_sources': len(records)-len(changed), 'verifiers_preserved': test_hashes,
        'historical_verifiers_executed_by_this_preparer': False,
        'historical_integration_failure_not_relabelled_PASS': True,
        'historical_control_report': declaration['historical_control_report'],
        'historical_control_status': historical_checks.get('status'),
        'historical_control_failures_preserved': historical_checks.get('failures'),
        'reader_certificate': {**reader_certificate, 'normal_optimized_results_equal': True,
            'execution_repeated_by_this_preparer': False, 'result': normal,
            'provenance': 'CERTIFICADO_NUEVO', 'included_in_s0_certificate': False},
        'reader_provenance': {
            'Q_and_L_ar_L_vol_factorization': 'RESULTADO_RECUPERADO',
            'explicit_normalization_on_B_av_and_weight_substitution': 'FORMALIZACION_NUEVA',
            'new_test': 'CERTIFICADO_NUEVO',
            'scope': 'Sector de amplitud común y condición explícita de descenso; no identificación física universal.',
            'model_discovery_claim': False},
        'scientific_claim_statement_changed': False, 'whole_article_mathematical_certification': False,
        'new_readers_covered_by_s0_certificate': False}
    write(run / 'DECLARACION_Y_DIFERENCIAS.json', declaration_record)
    write(run / 'GRAFO_FUENTES.json', {'sources': records, 'imports': edges, 'source_merkle_sha256': hashlib.sha256(canon(records)).hexdigest()})
    matrix = read(previous / 'MATRIZ_RECTORA.json')
    ledger = read(previous / 'LEDGER_MANUSCRITO.json')
    canvas = read(previous / 'LIENZO_APROBADO_PROPUESTO.json')
    for row in matrix['results']:
        row['source_blocks'] = [helpers['block'](root / 'manuscrito' / row['residence'], 'proof' if row['result_id'] == CLAIM else 'documentary_residence')]
    ledger['results'] = copy.deepcopy(matrix['results'])
    ledger['source_files'] = records
    canvas['results'] = copy.deepcopy(matrix['results'])
    write(run / 'MATRIZ_RECTORA.json', matrix)
    write(run / 'LEDGER_MANUSCRITO.json', ledger)
    write(run / 'MANIFIESTO_MANUSCRITO.json', read(previous / 'MANIFIESTO_MANUSCRITO.json'))
    fingerprint = hashlib.sha256(canon({'sources': records, 'declaration': spec(args.declaration), 'producer': spec(__file__)})).hexdigest()[:16].upper()
    canvas_id = 'EV-VII-REV04-CANVAS-DOCUMENTAL-' + fingerprint
    canvas.update({'approval_evidence_id': canvas_id, 'matrix_sha256': sha(run / 'MATRIZ_RECTORA.json'),
        'approved_matrix_sha256': sha(run / 'MATRIZ_RECTORA.json'),
        'technical_revision_declaration': spec(run / 'DECLARACION_Y_DIFERENCIAS.json'),
        'prior_canvas': spec(previous / 'LIENZO_APROBADO_PROPUESTO.json'),
        'editorial_authorization': declaration['authorial_authorization'],
        'technical_review_by': 'root', 'author_review_of_exact_matrix_or_hashes': False,
        'author_scientific_approval_of_new_source_hashes': False, 'publication_approved': False,
        'artifact_stage': 'BORRADOR_PARA_REVISION_AUTORAL', 'new_readers_covered_by_s0_certificate': False})
    write(run / 'LIENZO_APROBADO_PROPUESTO.json', canvas)
    physical = read(previous / 'EXPEDIENTE_FISICO.json')
    physical['editorial_handoff'] = {'is_pdf_task': True,
        'rector_matrix': spec(run / 'MATRIZ_RECTORA.json'), 'approved_canvas_record': spec(run / 'LIENZO_APROBADO_PROPUESTO.json'),
        'export_claim_ledger': spec(run / 'LEDGER_MANUSCRITO.json'), 'manuscript_manifest': spec(run / 'MANIFIESTO_MANUSCRITO.json')}
    bridge = helpers['module']('physical_bridge_gate_v2.py')
    require(bridge['dossier_binding'](physical) == matrix['dossier_binding_sha256'], 'Binding científico cambiado.')
    write(run / 'EXPEDIENTE_FISICO.json', physical)
    contract['artifact']['source_root'] = str(root / 'manuscrito')
    contract['artifact']['entrypoint'] = 'main.tex'
    contract['artifact']['output_pdf'] = str(root / 'output/pdf' / args.pdf_name)
    contract['separation']['central_root'] = str(root / 'manuscrito')
    for field, filename in [('physical_dossier','EXPEDIENTE_FISICO.json'), ('rector_matrix','MATRIZ_RECTORA.json'),
                            ('approved_canvas','LIENZO_APROBADO_PROPUESTO.json'), ('manuscript_ledger','LEDGER_MANUSCRITO.json'),
                            ('manuscript_manifest','MANIFIESTO_MANUSCRITO.json')]:
        contract[field] = spec(run / filename)
    contract['claims_registry'] = spec(TRUNK / 'claims.json')
    contract['physical_evidence_registry'] = spec(TRUNK / 'evidence.json')
    contract['gates'] = scientific_gate_hashes
    contract['proposal_status'] = 'REV04_SUCCESSOR_PENDING_CANONICAL_CANVAS_REGISTRATION'
    write(run / 'CONTRATO_PRECOMPILACION_PROPUESTO.json', contract)
    claims, evidence = read(TRUNK / 'claims.json'), read(TRUNK / 'evidence.json')
    old_claim = next(x for x in claims['claims'] if x['id'] == CLAIM)
    updated_claim = copy.deepcopy(old_claim)
    require(canvas_id not in updated_claim['evidence_ids'], 'Lienzo ya registrado.')
    updated_claim['evidence_ids'].append(canvas_id)
    new_evidence = {'id': canvas_id, **spec(run / 'LIENZO_APROBADO_PROPUESTO.json'),
        'claim_ids': [CLAIM, CONTEXT], 'status': 'VERIFIED', 'source': 'workspace_corpus',
        'kind': 'DOCUMENTARY_SUCCESSOR_CANVAS_UNDER_EXISTING_AUTHORIAL_SCOPE',
        'verification_history': [{'result': 'pass', 'timestamp': declaration['reviewed_at_utc'],
            'verifier': 'Control de deltas exactos y revisión focal del añadido declarada por root',
            'certificate_receipt': {'program': str(Path(__file__).resolve()), 'program_sha256': sha(__file__),
                'scope': 'Control documental, dos inserciones y un reemplazo inicial exacto; no aprobación científica global ni certificado nuevo de lectores',
                'declaration': spec(run / 'DECLARACION_Y_DIFERENCIAS.json')}}]}
    additions = {'status': 'PROPOSED_NOT_APPLIED', 'claims': [], 'evidence': [new_evidence],
        'claim_updates': [{'before': old_claim, 'after': updated_claim}],
        'old_claims_sha256': authority_before['claims.json'], 'old_evidence_sha256': authority_before['evidence.json'],
        'old_causal_graph_sha256': authority_before['causal_graph.json'], 'causal_graph_additions': {'nodes': [], 'edges': []},
        'scientific_binding_preserved': matrix['dossier_binding_sha256']}
    write(run / 'ALTAS_PROPUESTAS.json', additions)
    proposed_claims, proposed_evidence = copy.deepcopy(claims), copy.deepcopy(evidence)
    proposed_claims['claims'] = [updated_claim if x['id'] == CLAIM else x for x in claims['claims']]
    proposed_evidence['items'].append(new_evidence)
    lines = ['*** Begin Patch']
    for path, data in [(TRUNK / 'claims.json', proposed_claims), (TRUNK / 'evidence.json', proposed_evidence)]:
        diff = list(difflib.unified_diff(path.read_text().splitlines(), (json.dumps(data, ensure_ascii=False, indent=2)+'\n').splitlines(), n=3))
        lines.append('*** Update File: ' + str(path))
        lines.extend('@@' if line.startswith('@@') else line for line in diff[2:])
    lines.append('*** End Patch')
    (run / 'PROPUESTA_ALTA_ADITIVA.patch').write_text('\n'.join(lines)+'\n')
    require(all(sha(TRUNK/name) == value for name, value in authority_before.items()), 'El registro cambió durante la preparación: revisar propuesta.')
    require(all(sha(root/'manuscrito'/r['path']) == r['sha256'] for r in records), 'Las fuentes cambiaron durante la preparación: no registrar este corte.')
    print(json.dumps({'status':'PROPUESTA_REV04_PREPARADA_NO_APLICADA','run':str(run),'sources':len(records),
        'changed_sources':sorted(changed),'canonical_registry_modified':False,'preflight_receipt_issued':False,
        'compilation_authorized':False},ensure_ascii=False))


if __name__ == '__main__':
    main()
