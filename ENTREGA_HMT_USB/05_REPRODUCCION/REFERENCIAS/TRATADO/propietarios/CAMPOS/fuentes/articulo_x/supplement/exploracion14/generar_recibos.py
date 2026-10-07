#!/usr/bin/env python3
"""Recibos focales del registro archivado: vista previa por defecto.

--seal escribe sólo en esta carpeta, después de controles y puertas focales.
--expected-snapshot exige la huella que devuelve la vista previa. No modifica
fuentes, PDF, propietarios, recibos antecedentes ni registros globales.
Los antecedentes se heredan literalmente; estos controles NO reejecutan la
generación desde semillas, ni validan globalmente física, cardinalidad o prioridad.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
OLD = PROJECT / "output/INVESTIGACION_CONSERVACION_ESTRUCTURAL_HMT_20260911"
PAPER = PROJECT / "output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source"
CG = Path('/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py')
GG = PROJECT / 'tools/verificar_genealogia_unica_hmt.py'
PARENTS = {
    'constants': (OLD / 'RECIBO_CONSTANTES_RECONSTRUCCION_DIMENSIONAL_20260912.json',
                  'bba91bfa41753977f2338ae3cf8e380fc7d391714b247ddc94ffd8cb3f585cf3'),
    'genealogy': (OLD / 'RECIBO_GENEALOGIA_RECONSTRUCCION_DIMENSIONAL_20260912.json',
                  '95c1d22be7ec46cbeea34d07a66c0129fb93c55b5797e43c72446e2f3dda9221'),
}
NOTES = ['EXPLORACION.md', 'APORTE_INCIDENCIA.md', 'APORTE_TRANSPORTE.md']
CONTROLS = ['verificar_exploracion.py', 'RESULTADOS_EXACTOS.json', 'RESULTADOS_EXACTOS_OPT.json']
SOURCE_NAMES = [
    'sections/registro_k.tex', 'sections/registro_imagen_integral.tex',
    'sections/k_direccion_dimensional.tex', 'sections/excepcional.tex',
    'sections/alpha.tex', 'sections/k_reversibilidad.tex',
    'nuclear/05.tex', 'nuclear/10.tex', 'nuclear/11.tex',
]
ANCHORS = {
    'EXPLORACION.md': [
        'Los dos ejes nonádicos producen mediante APP',
        'TRIT conserva orientación, régimen y memoria local.',
        'operaciones de selección, transporte y actualización del TPK',
        'estado\nenriquecido', 'la estructura discreta conjunta del continuo',
        'El registro utilizado como testigo publicado es',
        'Trabajamos en la realización lineal posterior',
    ],
    'APORTE_INCIDENCIA.md': [
        'APP aporta las dos hojas', 'TRIT conserva régimen, orientación y acarreo',
        'TPK compone selección, transporte y actualización',
        'El estado enriquecido', 'la construcción conjunta del continuo',
        'La salida nueva es un decodificador', 'La terminología de red discreta',
    ],
    'APORTE_TRANSPORTE.md': [
        'las hojas aditiva y multiplicativa mantienen residuo y cociente',
        'TRIT conserva régimen y orientación',
        'la selección, el transporte y la actualización TPK',
        'del mismo estado enriquecido', 'de su estructura discreta conjunta del continuo',
        'la inversión orbital de Hadamard produce K',
        'Las realizaciones lineales y los caracteres de incidencia actúan después',
    ],
}
# id, section heading, statement, effective formula, falsifier, provenance.
RESULTS = {
    'EXPLORACION.md': [
        ('CLAUSURA_INVERSA', '## 2.',
         'La diferencia exacta de las lecturas a y alfa_A recupera los doce bloques, con carta y origen fijados.',
         'N=(1000^12-1)(a-alpha_A); K=divmod_1000^12(N)',
         'Confundir esta inversa posterior con un generador causal alimentado por alfa.', 'RESULTADO_RECUPERADO'),
        ('ORBITA_COMPLETA', '## 3.',
         'La órbita del registro archivado es base con cotas exactas 589609 y 39225169.',
         'O_K=(K,SK,...,S^11K); 589609 I <= O_K*O_K <= 39225169 I',
         'Promover la ausencia de periodo propio a independencia sin calcular los modos del Gram.', 'FORMALIZACION_NUEVA'),
        ('OPERADOR_RESPUESTAS', '## 4.',
         'Las doce respuestas recuperan H; una respuesta basta cuando HS=SH.',
         'H=(HK,HSK,...,HS^11K)O_K^-1; HS=SH implies H=O_(HK)O_K^-1',
         'Un operador no nulo que anula K refuta la recuperación desde una respuesta sin conmutación.', 'FORMALIZACION_NUEVA'),
        ('HOLONOMIA_RELATIVA', '### 4.1.',
         'Una respuesta vectorial completa del complemento determina la holonomía relativa con referencia invertible conocida y conmutación declarada.',
         'HB^-1 HC=I+(9/sqrt(8)) HB^-1 O_y O_K^-1; y=D_gamma K; D_gamma=sqrt(8)(HC-HB)/9',
         'Omitir la referencia HB, la conmutación o las doce componentes de la respuesta.', 'FORMALIZACION_NUEVA'),
        ('GRAM_TRANSPORTADO', '## 5.',
         'La isometría completa conserva el Gram y las cotas de la órbita en su imagen.',
         '(V O_K)*(V O_K)=O_K*O_K; V*V=I',
         'Omitir el terminal positivo o identificar la imagen con el ambiente completo.', 'FORMALIZACION_NUEVA'),
        ('COMPOSICION_INCIDENCIA_MEMORIA', '## 6.',
         'Se componen recuperación entera, incidencia, proyector transportado y carga de la acción auxiliar.',
         'Dec_q(MK+e)=K for ||e||<4sqrt(73)/81; Q^V=VQV*; J_n=p_n*A_n q_n',
         'Tratar perturbaciones de lectura como historias admisibles o como incertidumbre física.', 'FORMALIZACION_NUEVA'),
    ],
    'APORTE_INCIDENCIA.md': [
        ('GRAM_MEMORIAS', '## 2.',
         'El Gram de las dos memorias tiene la forma circulante exacta indicada.',
         '6561 M*M=2336I-520(S3+S4+S8+S9)-64(S+S5+S7+S11)',
         'Cambiar orden de las dos lecturas o normalización sqrt(8).', 'FORMALIZACION_NUEVA'),
        ('SEPARACION_ENTERA', '## 3.',
         'Las distancias mínimas cuadradas son 2336/6561 sin carga y 4672/6561 con carga.',
         'min_(h notin Z1)||Mh||^2=2336/6561; min_(sum h=0,h!=0)||Mh||^2=4672/6561',
         'Confundir la enumeración de cortes con la prueba sobre la red entera por niveles y paridad.', 'FORMALIZACION_NUEVA'),
        ('DECODIFICACION', '## 4.',
         'La decodificación más cercana recupera el registro centrado o completo dentro de los radios estrictos.',
         'r0=2sqrt(146)/81; rq=4sqrt(73)/81; Dec_q(MK+e)=K if ||e||<rq',
         'Admitir igualdad en el radio o suministrar K al decodificador.', 'FORMALIZACION_NUEVA'),
        ('SELECCION_RESTITUIDA', '## 5.',
         'La restitución entera previa conserva el selector 729; la lectura continua directa no tiene radio positivo.',
         'B_Dec_q(y)={4,6,9,10}; K_t=K-t P e4 gives (K_t)_4<729 for t>0',
         'Corregir K no corrige errores independientes de las otras marcas de la bandera.', 'FORMALIZACION_NUEVA'),
        ('DECODIFICACION_COVARIANTE', '## 6.',
         'Las distancias y los decodificadores se transportan por la isometría incidencial y la red transportada.',
         'M_inc=(F directsum F)M; ||M_inc h||=||Mh||; M_R R=(R directsum R)M',
         'Redondear en Z12 fija tras cambiar la carta ortogonal sin transportar la red.', 'FORMALIZACION_NUEVA'),
    ],
    'APORTE_TRANSPORTE.md': [
        ('DESCOMPOSICION_K', '## 2.',
         'El registro centrado se descompone ortogonalmente en la dirección seleccionada y su complemento.',
         'k=Pi K; u=P3 k; Q=Pi-uu*/||u||^2; k=u+Qk',
         'Identificar el proyector de rango uno con P3 o omitir u!=0.', 'RESULTADO_RECUPERADO'),
        ('TRANSPORTE_PROYECTOR', '## 3.',
         'La isometría completa conserva dirección, proyector y descriptor en su imagen.',
         'Q^V=VQV*=V Pi V*-(Vu)(Vu)*/||u||^2; eta^V=eta',
         'Usar identidad ambiente en lugar de VV* sobre la imagen.', 'FORMALIZACION_NUEVA'),
        ('ESTABILIDAD_COMPLETA', '## 4.',
         'La inversa completa tiene norma uno; el proyector y eta admiten las cotas focales con las condiciones dadas.',
         '||V*(VK+delta)-K||<=epsilon; ||Q_hat-Q||<=epsilon/||u||; |eta_hat-eta|<=epsilon/||k||',
         'Omitir epsilon<||u|| o epsilon<||k||, o descartar las correlaciones entre bloques.', 'FORMALIZACION_NUEVA'),
        ('REFINAMIENTO_COVARIANTE', '## 5.',
         'El proyector transportado entrelaza el refinamiento; cambiar sólo K no conserva eta en carta fija.',
         'Q_(n+1) R_n=R_n Q_n; R_n*Q_(n+1)R_n=Q_n',
         'Mantener P3 fijo al cambiar K por S3K o S4K y anunciar invariancia.', 'FORMALIZACION_NUEVA'),
        ('CARGA_TRANSPORTE', '## 6.',
         'La acción auxiliar cotangente conserva J_n y su lectura mediante registros isométricos.',
         'L_n=p_(n+1)*(q_(n+1)-U_n q_n); A_(n+1)U_n=U_n A_n; J_n=p_n*A_nq_n=J_0',
         'Identificar esta acción auxiliar con una acción física no especificada.', 'FORMALIZACION_NUEVA'),
    ],
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def locator(path, lines=None):
    path = Path(path).resolve()
    return {'path': str(path), 'sha256': digest(path),
            'lines': lines or f'1-{len(path.read_text().splitlines())}'}


def section(path, heading):
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith(heading)]
    require(len(starts) == 1, f'Ancla de sección inequívoca requerida: {path.name}: {heading}')
    start = starts[0]
    end = next((i for i in range(start+1, len(lines)) if lines[i].startswith('## ')), len(lines))
    return locator(path, f'{start+1}-{end}')


def check_locators(value):
    """No refresca silenciosamente ninguna huella de antecedentes heredados."""
    if isinstance(value, dict):
        if 'path' in value and 'sha256' in value:
            p = Path(value['path'])
            require(p.is_file() and digest(p) == value['sha256'], f'Antecedente cambiado: {p}')
        for item in value.values():
            check_locators(item)
    elif isinstance(value, list):
        for item in value:
            check_locators(item)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def build(checked=False):
    old = {}
    for kind, (path, sha) in PARENTS.items():
        require(digest(path) == sha, f'Recibo antecedente cambió: {path}')
        old[kind] = json.loads(path.read_text())
    base = old['genealogy']
    inherited_keys = ['schema_version', 'scope_kind', 'formal_kernel', 'universal_genealogy',
                      'foundation', 'stage_order', 'stages', 'trit_constraints',
                      'tpk_constraints', 'non_regression']
    inherited = {key: copy.deepcopy(base[key]) for key in inherited_keys}
    check_locators(inherited)
    sources = [locator(PAPER / name) for name in SOURCE_NAMES]
    controls = [dict(locator(HERE/name), kind='EXACT_FINITE_CONTROL_OR_REPORT') for name in CONTROLS]
    all_notes = [locator(HERE/name) for name in NOTES]
    outputs = {}
    base_stage = base['stages'][-1]
    reg_domain = 'Registro entero dodecafásico ya generado, con carga, origen, orientación y lectores posteriores tipados'
    register_owner = locator(PAPER/'sections/registro_k.tex', '213-296,315-387')
    for name in NOTES:
        p = HERE/name
        stem = p.stem
        rid = f'EXPLORACION_REGISTRO_{stem}_20260914'
        gen = copy.deepcopy(inherited)
        gen.update(receipt_id=rid, provenance='FORMALIZACION_NUEVA',
                   proof_strength='DEMOSTRADO_CON_ESTRUCTURA_DE_PARTIDA_EXPLICITA',
                   conclusion_status='CLOSED_IN_HMT_DOMAIN', residual_if_any=None)
        gen['foundation']['inherited_receipt'] = locator(PARENTS['genealogy'][0])
        gen['foundation']['inheritance_is_new_global_reproof'] = False
        gen['artifact'] = dict(locator(p), kind='DERIVATION')
        gen['artifact']['anchors'] = []
        text = p.read_text()
        position = -1
        for stage, anchor in zip(gen['stage_order']+['HMT_OUTPUT','CONVENTIONAL'], ANCHORS[name]):
            position = text.find(anchor, position+1)
            require(position >= 0, f'Ancla causal ausente: {name}: {anchor}')
            gen['artifact']['anchors'].append({'stage':stage, 'text':anchor,
                                               'line':text.count('\n', 0, position)+1})
        gen['scope'] = {
            'included': 'Lectores posteriores del registro archivado: '+stem,
            'global_corpus_revalidated': False, 'empirical_validation': False,
            'constant_digits_recomputed': False, 'seed_generator_reexecuted': False,
            'cardinality_audited': False, 'CH_certified': False,
            'priority_globally_established': False, 'particular_physical_trajectory_selected': False,
            'PDF_or_sources_modified': False, 'global_records_modified': False,
            'finite_checks_performed_by_this_execution': checked,
            'focal_proofs_in_notes_not_replaced_by_gates': True,
            'inherited_catalogue_claims_are_not_newly_revalidated': True,
        }
        gen['inherited_evidence'] = [locator(path) for path, _ in PARENTS.values()]
        gen['source_evidence'] = sources
        gen['associated_artifacts'] = all_notes + controls
        gen['result_maps'] = [{
            'id':'REGISTRO_ARCHIVADO', 'statement':'El lector firmado y su inversión producen el registro usado como antecedente archivado.',
            'input_object':base_stage['output_object'], 'domain':base_stage['codomain'],
            'codomain':reg_domain, 'output_object':'REGISTRO_ARCHIVADO_K',
            'map':'R_sgn=Pi_H o E108^(90,120) o R12; K=H12 R_sgn(x_term)/4',
            'generator_inputs':[base_stage['output_object']], 'source_family':'HMT',
            'proof_locator':register_owner, 'falsifier':'Introducir K o alfa como objetivo del extractor firmado.',
            'provenance':'RESULTADO_RECUPERADO', 'execution_scope':'INHERITED_NOT_REEXECUTED',
        }]
        register_nine = copy.deepcopy(base['result_maps'][0]['genealogical_nine_fields'])
        register_nine.update(
            coefficient_origins='Canales anteriores al registro, tres órbitas y H4^2=4I; la división por cuatro procede de la inversión de Hadamard.',
            hmt_output=gen['result_maps'][0]['statement'],
            recognition_and_falsifier={'recognition':'Coordenatización integral posterior del registro firmado.',
                                      'falsifier':gen['result_maps'][0]['falsifier']},
            owners_and_locators=[register_owner, locator(PARENTS['genealogy'][0])],
        )
        gen['result_maps'][0]['genealogical_nine_fields'] = register_nine
        for ident, heading, statement, formula, falsifier, provenance in RESULTS[name]:
            proof = section(p, heading)
            nine = copy.deepcopy(base['result_maps'][0]['genealogical_nine_fields'])
            nine.update(coefficient_origins='Registro firmado archivado y lectores S3/S4; partición nonádica8+1. Coeficientes espectrales y radios deducidos de los operadores, no elegidos como objetivos.',
                        preserved_information='Antecedentes completos heredados; en el lector focal se conservan los datos que explicita la prueba. K no reemplaza la historia completa. La carga se distingue de la componente centrada.',
                        hmt_output=statement,
                        recognition_and_falsifier={'recognition':'Álgebra lineal y análisis funcional como lenguaje posterior de prueba.', 'falsifier':falsifier},
                        owners_and_locators=[register_owner, proof]+sources)
            gen['result_maps'].append({
                'id':ident, 'statement':statement, 'input_object':'REGISTRO_ARCHIVADO_K',
                'domain':reg_domain, 'codomain':'Realización focal: '+ident,
                'output_object':'SALIDA_'+ident, 'map':formula,
                'generator_inputs':['REGISTRO_ARCHIVADO_K'], 'source_family':'HMT',
                'proof_locator':proof, 'falsifier':falsifier, 'provenance':provenance,
                'hypotheses_are_those_of_bound_proof':True, 'genealogical_nine_fields':nine,
            })
        selected = gen['result_maps'][-1]
        gen['target'] = {
            'statement':selected['statement'], 'domain':selected['domain'], 'codomain':selected['codomain'],
            'closure_criterion':'Pruebas y condiciones de las secciones enlazadas; controles focales separados de las pruebas generales.',
            'result_id':selected['id'], 'target_family':'POST_CONTINUUM_HMT',
            'causal_cutoff':'ESTRUCTURA_DISCRETA_CONTINUO',
            'causal_cutoff_reason':'Aplicación posterior al registro firmado; se heredan, no reejecutan, las etapas generadoras.',
            'forbidden_generator_inputs':base['target']['forbidden_generator_inputs'],
        }
        gen['conventional_uses'] = [{
            'name':'Álgebra lineal, distancias y transporte funcional como lenguaje de prueba posterior',
            'role':'PROOF_LANGUAGE', 'locator':section(p, '## 2.'),
            'occurs_after_hmt_output':True, 'selects_hmt_state':False,
            'selects_route':False, 'sets_generators':False, 'sets_coefficients':False,
            'target_value_used_as_input':False,
        }]
        limit = name != 'APORTE_INCIDENCIA.md'
        gen['proof_layers'] = {
            'finite':'Pruebas escritas y controles enteros/racionales vinculados; 4094 cortes y132 raíces son comprobaciones finitas, no prueba por enumeración de toda la red.',
            'compatibility':'Los lectores, carta, métrica, red y proyectores se transportan conjuntamente, con carga cuando procede.',
            'recognition':'Realizaciones posteriores y acción auxiliar; sin identificación física por el solo rango o escalar.',
            'limit': ({'required':True,
                       'finite_levels':'V_N=(P_N,D_0,...,D_(N-1)P_(N-1))',
                       'bonding_maps':'Identidad telescópica I=P_N*P_N+sum P_n*D_n*D_nP_n',
                       'compatibility_identity':'V*V=I y conjugación de los observables en im(V)',
                       'limit_object':'V_infty=(A_infty^(1/2),(D_nP_n)_n)',
                       'proof':'Balance monótono de Grams y polarización heredados de nuclear/10; aplicación en la nota enlazada.'}
                      if limit else {'required':False,
                       'reason':'Separación y decodificación de una red finita dimensional con lector fijo de doce posiciones.',
                       'typing_falsifier':'Extender radios a otras ventanas, métricas o generadores sin nueva prueba.'}),
        }
        gen['global_falsifier'] = 'Usar los controles como nueva generación de semillas, certificación CH/física global, sustituto de hipótesis o prioridad; confundir registro, estado completo y lecturas.'
        gen['seal_state'] = 'FOCAL_GATES_PASSED_FOR_BOUND_ARTIFACTS' if checked else 'PREPARED_UNSEALED'
        gen_name = f'RECIBO_GENEALOGIA_{stem}.json'
        const = {
            'schema_version':'1.1', 'artifact':str(p), 'artifact_sha256':digest(p), 'result_id':rid,
            'genealogy':copy.deepcopy(old['constants']['genealogy']),
            'inherited_receipt':locator(PARENTS['constants'][0]),
            'genealogy_receipt':str(HERE/gen_name), 'associated_artifacts':all_notes+controls,
            'scope':copy.deepcopy(gen['scope']), 'seal_state':gen['seal_state'],
        }
        const['genealogy']['focal_constant_roles'] = {
            'K':'Publicación firmada archivada, entrada legítima de lectores posteriores; no semilla primaria ni objetivo metrológico.',
            'pi_phi_e_alpha':'Salidas correlacionadas heredadas; sin nuevo cálculo de cifras ni fusión de las dos vías de alfa.',
            'spectral_bounds_decoding_radii':'Consecuencias exactas de operadores y dominios declarados, no nuevas constantes físicas por denominación.',
            'whole_catalogue_revalidated':False, 'seed_generator_reexecuted':False,
        }
        const['genealogy']['source_locators'] += [x['path']+':'+x['lines'] for x in sources+all_notes]
        const['inherited_scope_semantics'] = 'El catálogo del recibo previo conserva su significado antecedente; las puertas focales no lo vuelven a demostrar.'
        outputs[gen_name] = gen
        outputs[f'RECIBO_CONSTANTES_{stem}.json'] = const
    return outputs


def snapshot(outputs):
    paths = {Path(__file__).resolve(), GG, CG}
    def collect(obj):
        if isinstance(obj, dict):
            if isinstance(obj.get('path'), str) and obj.get('sha256'):
                paths.add(Path(obj['path']))
            for val in obj.values():
                collect(val)
        elif isinstance(obj, list):
            for val in obj:
                collect(val)
    collect(outputs)
    mapping = {str(p):digest(p) for p in sorted(paths)}
    sha = hashlib.sha256(json.dumps(mapping,sort_keys=True).encode()).hexdigest()
    return sha, mapping


def validate_memory(outputs):
    gg, cg = module(GG, 'hmt_genealogy_focal'), module(CG, 'hmt_constants_focal')
    failures = []
    for name, obj in outputs.items():
        if name.startswith('RECIBO_GENEALOGIA'):
            issues = gg.validate_receipt(obj)
            failures += [name+': '+issue.code+' '+issue.path+' '+issue.message for issue in issues]
        else:
            original_reader = cg.read_json
            cg.read_json = lambda path, data=obj: data
            try:
                failures += [name+': '+issue for issue in cg.validate_receipt(HERE/name, Path(obj['artifact']))]
                failures += [name+': '+issue for issue in cg.scan_text(Path(obj['artifact']))]
            finally:
                cg.read_json = original_reader
    return failures


def run(command):
    proc = subprocess.run(command, cwd=PROJECT, text=True, capture_output=True, timeout=60)
    require(proc.returncode == 0, f'Control falló: {command}\n{proc.stdout}\n{proc.stderr}')
    return {'command':command, 'returncode':proc.returncode,
            'stdout':proc.stdout.strip(), 'stderr':proc.stderr.strip()}


def exact_controls():
    script = HERE/CONTROLS[0]
    records = []
    normal = json.loads((HERE/CONTROLS[1]).read_text())
    optimized = json.loads((HERE/CONTROLS[2]).read_text())
    require(normal == optimized, 'Las dos salidas exactas guardadas no coinciden.')
    for options in (['-I','-S'], ['-I','-S','-O']):
        rec = run([sys.executable]+options+[str(script)])
        actual = json.loads(rec['stdout'])
        expected = {k:v for k,v in normal.items() if k != 'integer_inverse_numerator'}
        require(actual == expected, 'La salida guardada no corresponde al control actual.')
        records.append({'command':rec['command'], 'returncode':0,
                        'matches_archived_report':True,
                        'stdout_sha256':hashlib.sha256(rec['stdout'].encode()).hexdigest()})
    require(normal['two_memory_decoding']['target_not_received_by_decoder'] is True,
            'El decodificador debe ser independiente del registro objetivo.')
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seal', action='store_true')
    parser.add_argument('--expected-snapshot')
    args = parser.parse_args()
    outputs = build(checked=args.seal)
    sha, mapping = snapshot(outputs)
    errors = validate_memory(outputs)
    report = {'mode':'SEAL' if args.seal else 'READ_ONLY_PREVIEW', 'snapshot_sha256':sha,
              'bound_files':len(mapping), 'receipt_files':list(outputs), 'issues':errors,
              'seeds_reexecuted':False, 'global_validation':False, 'files_written':False}
    if errors or not args.seal:
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 1 if errors else 0
    require(args.expected_snapshot == sha, 'Se exige la huella de vista previa actual mediante --expected-snapshot.')
    checks = exact_controls()
    require(snapshot(outputs)[0] == sha, 'Cambió una dependencia durante los controles; no se sella.')
    # Las puertas trabajan sobre recibos temporales; sólo tras todas ellas se publican.
    gates = []
    with tempfile.TemporaryDirectory(prefix='.recibos-', dir=HERE) as tmp:
        staging = Path(tmp)
        for name, obj in outputs.items():
            path = staging/name
            path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
            if name.startswith('RECIBO_GENEALOGIA'):
                rec = run([sys.executable,'-I','-S',str(GG),'--receipt',str(path)])
                require(rec['stdout'].startswith('PASS_GENEALOGIA_UNICA_APP_TRIT_TPK'), 'Salida inesperada de genealogía.')
            else:
                rec = run([sys.executable,'-I','-S',str(CG),'--audit',obj['artifact'],'--receipt',str(path)])
                require(rec['stdout'] == 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY', 'Salida inesperada de constantes.')
            rec['receipt_final_path'] = str(HERE/name)
            gates.append(rec)
        require(snapshot(outputs)[0] == sha, 'Cambió una dependencia durante las puertas; no se sella.')
        for name in outputs:
            dest = HERE/name
            require(not dest.exists(), f'No se sobreescribe un recibo existente: {dest}')
        manifest_name = 'SELLO_FOCAL_20260914.json'
        require(not (HERE/manifest_name).exists(), 'Ya existe un sello; crear una revisión explícita.')
        manifest = {'status':'FOCAL_GATES_PASSED_FOR_BOUND_ARTIFACTS', 'snapshot_sha256':sha,
                    'bindings':mapping, 'receipts':[dict(locator(staging/name),path=str(HERE/name)) for name in outputs],
                    'exact_controls':checks, 'gates':gates,
                    'scope':'Trazabilidad causal y controles de lectores posteriores del registro archivado; no certificación global ni generación desde semillas.',
                    'notes_are_research_not_pdf_integration':True}
        (staging/manifest_name).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        for name in list(outputs)+[manifest_name]:
            os.replace(staging/name,HERE/name)
    report.update(files_written=True, issues=[], gates_passed=len(gates),
                  manifest=str(HERE/manifest_name), exact_controls_modes=['normal','-O'])
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({'status':'FOCAL_RECEIPT_ERROR','message':str(exc)},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(1)
