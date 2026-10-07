"""Genera y comprueba exclusivamente los dos recibos focales de esta carpeta.

Uso:
  python3 -I -S sellar_recibos_focales.py --seal --expected-main-sha SHA256
  python3 -I -S sellar_recibos_focales.py --check

--seal requiere autorización editorial previa para la huella indicada. No modifica
los cuatro desarrollos, propietarios, índices, certificados heredados ni PDF.
--check no escribe. No sustituye la semántica por un escaneo de palabras.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/ruben/Documents/New project')
FORMAL = ROOT / 'PUBLICACION_HMT/REGISTRO_DE_CONTINUIDAD_ACADEMICA/NUCLEO_FORMAL_HMT_PERMANENTE'
GATE = ROOT / 'tools/verificar_genealogia_unica_hmt.py'
CGATE = Path('/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py')
BASE_DIR = ROOT / 'output/REVISION_CIENTIFICA_EDITORIAL_SERIE_20260911_REV04/VII_GRAVITACION/gestion/genealogia_s0_rev04'
BASE_G = BASE_DIR / 'RECIBO_GENEALOGIA_S0.json'
BASE_C = BASE_DIR / 'RECIBO_CONSTANTES_S0.json'
BASE_G_SHA = '7537da0bd708fdd5027b21ea84a539c8206f0d2af105fd32af9ac313e69f2282'
BASE_C_SHA = '5fecb67a3c1f6a03dcd33d45e07cb1db1b895e7a59ae54581d1d45d8f85e6a7d'
SOURCE = ROOT / 'output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente'
CORE_S = SOURCE / 'manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core'
F1 = CORE_S / '04b1_estado_arbol_medida_comun.tex'
F2 = CORE_S / '04b2_operaciones_intrinsecas_correlativas.tex'
F3 = CORE_S / '04b3_terminal_naturalidad_limite.tex'
F4 = SOURCE / 'colaboracion/partes_i_ii/source/base_residencias/base_c17_sin_encabezado.tex'
FILES = ['CONSERVACION_ESTRUCTURAL.md', 'REFINAMIENTO.md', 'EXCEPCIONAL.md', 'ACCION.md']
GOUT = HERE / 'RECIBO_GENEALOGIA.json'
COUT = HERE / 'RECIBO_CONSTANTES.json'
STAGES = ['APP', 'TRIT', 'TPK', 'ESTADO_ENRIQUECIDO', 'ESTRUCTURA_DISCRETA_CONTINUO']
BASE_OBJECT = 'CONTINUO_CONJUNTO_HMT'
BASE_DOMAIN = 'Estructura discreta conjunta con historias, medida, cinco operaciones y lectores tipados'
NINE = ['app', 'trit', 'tpk', 'coefficient_origins', 'preserved_information', 'enriched_state_and_continuum', 'hmt_output', 'recognition_and_falsifier', 'owners_and_locators']


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def locator(path, lines=None):
    path = Path(path).resolve()
    count = len(path.read_text(encoding='utf-8').splitlines())
    return {'path': str(path), 'sha256': digest(path), 'lines': lines or f'1-{count}'}


def section(path, heading):
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    start = lines.index(heading)
    stop = next((i for i in range(start+1, len(lines)) if lines[i].startswith('## ')), len(lines))
    return locator(path, f'{start+1}-{stop}')


def run(command, marker):
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    require(result.returncode == 0 and marker in result.stdout,
            'Puerta fallida: ' + ' '.join(map(str, command)))
    return {'command': list(map(str, command)), 'exit_code': result.returncode, 'stdout': result.stdout.strip()}


def inherited_checks():
    for path, expected in [(BASE_G, BASE_G_SHA), (BASE_C, BASE_C_SHA)]:
        require(digest(path) == expected,
                f'Herencia modificada: {path}; actual={digest(path)} esperado={expected}')
    g, c = load(BASE_G), load(BASE_C)
    inherited = g['foundation']['inherited_receipt']
    require(digest(inherited['path']) == inherited['sha256'],
            'Huella del antecedente fundacional V modificada: ' + inherited['path'])
    core = load(FORMAL / 'CORE_HMT.json')
    statement = ' -> '.join(core['canonical_chain'])
    require(statement == g['foundation']['claim_statement'], 'Enunciado fundacional cambiado')
    require(hashlib.sha256(statement.encode()).hexdigest() == g['foundation']['claim_statement_sha256'],
            'Huella del enunciado fundacional incompatible')
    require(digest(FORMAL / 'TPK_GRAFO_OPERATORIO_TIPADO.json') == g['formal_kernel']['typed_operator_graph']['sha256'],
            'Grafo tipado distinto de la herencia; no se reescribe el antecedente')
    records = [
        run([sys.executable, '-I', '-S', str(FORMAL/'hmt_formal_kernel.py'), '--verify'], 'PASS_NUCLEO_FORMAL_HMT_PERMANENTE'),
        run([sys.executable, '-I', '-S', str(GATE), '--receipt', str(BASE_G)], 'PASS_GENEALOGIA_UNICA_APP_TRIT_TPK'),
        run([sys.executable, '-I', '-S', str(CGATE), '--self-check'], 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY'),
        run([sys.executable, '-I', '-S', str(CGATE), '--audit', c['artifact'], '--receipt', str(BASE_C)], 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY'),
    ]
    return g, c, records


def make_receipts(base, constants_base, inheritance_validation):
    main = HERE / FILES[0]
    text = main.read_text(encoding='utf-8')
    anchors = [
        'La construcción parte de las dos hojas operatorias de APP.',
        'La orientación TRIT discrimina los residuos',
        'El TPK compone selección, transporte y actualización',
        'actúa sobre ese estado enriquecido.',
        'Las construcciones espectral, solenoidal, de calibre, cohomológica y determinantal',
        'son salidas, con sus operadores y orden constructivo propio.',
        'Los espacios de Hilbert y el teorema espectral intervienen como lenguaje de realización y demostración posterior.',
    ]
    position = -1
    bound_anchors = []
    for stage, anchor in zip(STAGES + ['HMT_OUTPUT', 'CONVENTIONAL'], anchors):
        position = text.find(anchor, position+1)
        require(position >= 0, 'Ancla causal ausente o reordenada: ' + anchor)
        bound_anchors.append({'stage': stage, 'text': anchor, 'line': text[:position].count('\n')+1})
    g = {
        'schema_version': 'hmt-genealogia-unica-v4',
        'receipt_id': 'CONSERVACION_ESTRUCTURAL_FOCAL_HMT_20260911',
        'scope_kind': 'DERIVATION',
        'formal_kernel': copy.deepcopy(base['formal_kernel']),
        'universal_genealogy': copy.deepcopy(base['universal_genealogy']),
        'foundation': {k: copy.deepcopy(v) for k, v in base['foundation'].items() if k != 'inherited_receipt'},
        'artifact': dict(locator(main), kind='DERIVATION', anchors=bound_anchors),
        'stage_order': STAGES,
        'trit_constraints': copy.deepcopy(base['trit_constraints']),
        'non_regression': copy.deepcopy(base['non_regression']),
        'provenance': 'FORMALIZACION_NUEVA',
        'proof_strength': 'DEMOSTRADO_CON_ESTRUCTURA_DE_PARTIDA_EXPLICITA',
        'conclusion_status': 'CLOSED_IN_HMT_DOMAIN',
        'residual_if_any': None,
        'scope': {
            'included': 'Balance de observables; limite fuerte T^N a Pfix; covariancia; refinamiento; incidencia y accion con forma variable.',
            'global_corpus_revalidated': False, 'empirical_validation': False,
            'constant_digits_recomputed': False, 'cardinality_audited': False,
            'unbounded_quantization_claimed': False,
            'historical_2084_does_not_replace_selected_2249': True,
        },
        'associated_artifacts': [locator(HERE/name) for name in FILES[1:]],
        'finite_check_script': locator(HERE/'verificar_balances_exactos.py'),
        'inherited_evidence': [locator(BASE_G), locator(BASE_C), locator(FORMAL/'CORE_HMT.json'), locator(FORMAL/'TPK_GRAFO_OPERATORIO_TIPADO.json')],
        'inheritance_validation': inheritance_validation,
        'seal_state': 'AWAITING_FOCAL_GATE_RESULTS',
    }
    g['foundation']['inherited_receipt'] = locator(BASE_G)
    g['universal_genealogy']['scope_semantics'] = {
        'mode': 'INHERITED_NORMATIVE_CONTEXT', 'source_receipt': locator(BASE_G),
        'catalogue_or_terminal_proof_by_local_checks': False,
        'meaning': 'Se conserva el alcance autoral heredado; los balances focales no revalidan catalogos ni problemas terminales.'}
    stage_specs = [
        ('SEMILLAS_APP', 'D9 horizontal x D9 vertical', 'HOJAS_APP', 'Hojas APP con residuos y cocientes',
         'Evaluacion aditiva y multiplicativa', '(i,j)->(i+j,ij); delta^diamond=res^diamond+9quo^diamond', '15-95'),
        ('HOJAS_APP', 'Hojas APP con residuos y cocientes', 'EMISIONES_TRIT', 'Emisiones orientadas y acarreo',
         'Levantamiento TRIT', 'Delta(epsilon)=or(epsilon)+3kappa(epsilon); or in {-1,0,1}', '97-174'),
        ('EMISIONES_TRIT', 'Emisiones orientadas y acarreo', 'RUTAS_TPK', 'Rutas transportadas con memoria',
         'Actualizacion TPK', 'U_t=Upd_t o Tra_t o Sel_t; m->C_epsilon m+kappa(epsilon); U_gamma=U_last...U_first', '176-219,358-446'),
        ('RUTAS_TPK', 'Rutas transportadas con memoria', 'HISTORIAS_ENRIQUECIDAS', 'Sistema de prefijos enriquecidos completos',
         'Generacion del estado y ledger', 'gamma->xhat_k(gamma); rho(xhat_(k+1))=xhat_k; Led(gamma)=(lambda(epsilon_j))_j', '449-487,730-834'),
        ('HISTORIAS_ENRIQUECIDAS', 'Sistema de prefijos enriquecidos completos', BASE_OBJECT, BASE_DOMAIN,
         'Constructor conjunto y limite', 'e_epsilon->O(e_epsilon); uD_fine=D_coarse tau; Cdisc=lim D_joint', '1028-1118,1169-1205'),
    ]
    g['stages'] = []
    for ident, spec in zip(STAGES, stage_specs):
        inp, domain, out, codomain, name, formula, lines = spec
        g['stages'].append({
            'id': ident, 'input_object': inp, 'domain': domain, 'codomain': codomain,
            'map': {'name': name, 'formula': formula},
            'action_on_generators': {'generators': [inp], 'formula': formula,
                'effect': 'Produce la etapa siguiente conservando ambas hojas, procedencia y las relaciones registradas, sin entradas objetivo.'},
            'generator_inputs': [inp], 'output_object': out, 'source_family': 'HMT',
            'owner': locator(F2 if ident == STAGES[-1] else F1, lines)})
    g['tpk_constraints'] = {
        'forward_map': {'name': 'Emision enriquecida', 'formula': 'gamma->gamma epsilon; m->C_epsilon m+kappa(epsilon)'},
        'inverse_map': {'name': 'Recuperacion del prefijo y reversion tipada', 'formula': 'rho(gamma epsilon)=gamma; on reversible arrows m->C_epsilon^{-1}(m-kappa(epsilon))'},
        'phase_return': {'identity': 'g(k+9)=g(k)', 'state_return': False},
        'preserves': ['residue','quotient','orientation','carry','boundary','route','memory','survival','sheet','ledger','multisection'],
    }
    result_specs = [
        ('BALANCE_OBSERVABLE', main, '## 2. Balance de un observable conservado',
         'Descomposicion exacta A=T*AT+eta*Atilde eta bajo U*Atilde U=Atilde y [Atilde,JJ*]=0.',
         'UJ=JT+eta; expansion de la forma sesquilineal; los terminos cruzados se anulan por reduccion.',
         'J normalizado; 1/3 procede de nueve copias; 8/81 de (64+8)/729, no de ajuste.',
         'Omitir reduccion del observable puede conservar terminos cruzados; omitir invariancia altera el balance.'),
        ('LIMITE_COMPRESION', main, '## 4. Sector terminal y registro a profundidad ilimitada',
         'Para C unitario, T=(8I+C)/9 satisface s-lim T^N=Pfix y conserva la carga en Pfix y el registro infinito.',
         't(z)=(8+z)/9; convergencia dominada espectral; telescopia de las formas acotadas.',
         '8 y 9 son las componentes de la costura; Pfix procede de ker(I-C), no se fija como cero por definicion.',
         'Un ciclo finito tiene sector fijo; eliminarlo falsifica la identidad. Convergencia fuerte no implica tasa uniforme.'),
        ('COVARIANCIA_INCIDENCIA', main, '## 5. Conservación de simetría y transporte de carta',
         'Conjugacion covariante de T, eta y Pfix; transporte isometrico del registro K completo mediante media e incidencia.',
         'Cprime=RCR*; Tprime R=RT; F(k)=(media,I P0 k/6), F^{-1}(mu,y)=mu 1+P0 I*y/6.',
         'H12^2=4I; Gram de incidencia 36I+30 11*; 1/2,1/4,1/6 conservan sus roles distintos. La composicion C3 fija-libre da g_c+g_c*=-I, T3*T3=19/27 I y eta3*eta3=8/27 I por expansion, sin identificar g_c con Gamma9.',
         'Omitir la media pierde una coordenada; confundir H/4 con H/2 altera la norma; no se identifica C3 con Gamma9 por orden.'),
        ('REFINAMIENTO_CONJUNTO', HERE/'REFINAMIENTO.md', '## 7. Teorema de paso al límite para la carga observable/memoria',
         'La medida proyectiva produce refinamiento isometrico; los cuadrados J,P,U,A preservan balance y memoria al limite.',
         'R delta_h=sum_e sqrt(p_h(e))delta_he; Pnext S=SP; naturalidad de T y eta; extension por densidad y cotas uniformes.',
         'p_h(e)=1/#Out(h) cuenta todas las emisiones con multiplicidades; las raices son normalizacion Hilbert posterior.',
         'Sin Gram, proyeccion natural o cota uniforme no se afirma la promocion analitica correspondiente.'),
        ('ACCION_FORMA_VARIABLE', HERE/'ACCION.md', '## 3. Cambio de forma: transporte y conexión determinados',
         'El transporte M_eta_prime exp(-theta J2) M_eta^{-1} conserva la accion; su realizacion C1 produce Htr=omega I_eta+etadot QP/2.',
         'Diferenciar el transporte; dot M M^{-1}; cancelacion de d_t I_eta y corchete con el termino de conexion.',
         'eta procede de las salidas angulares HMT; omega del reloj declarado; hbar es salida anterior de accion. 1/2 procede de derivar exp(+-eta/2).',
         'Omitir el termino de conexion en forma variable deja dI/dt no nula. No se asigna una interpolacion fisica unica a cada ruta.'),
        ('TRANSPORTE_EXCEPCIONAL', HERE/'EXCEPCIONAL.md', '## 3. Corolario ensamblable: transporte K–Witt de normas, operadores y balances',
         'Composicion Hadamard-Witt equivarante sobre el sector centrado; accion C3 generada y refinamiento de energia en sus dominios.',
         'B=U_W J_H; B rho_hat=rho_hex B; conjugacion de transportes, pesos y diferencias conserva el balance.',
         'Normalizadores determinados por H12^2 y Gram incidencial; grupo C3 y sus marcas proceden del propietario integral.',
         'Una simetria de marco fijo requiere estabilizador y conmutacion especifica; un entrelazador finito no representa por si toda holonomia.'),
    ]
    maps = []
    for ident, path, heading, statement, formula, coefficients, falsifier in result_specs:
        proof = section(path, heading)
        maps.append({
            'id': ident, 'statement': statement, 'input_object': BASE_OBJECT,
            'domain': BASE_DOMAIN, 'codomain': 'Realizacion focal tipada: '+ident,
            'output_object': 'SALIDA_'+ident, 'map': formula,
            'generator_inputs': [BASE_OBJECT], 'source_family': 'HMT',
            'proof_locator': proof, 'falsifier': falsifier,
            'genealogical_nine_fields': {
                'app': {'stage': 'APP', 'owner': locator(F1,'15-95'), 'action': stage_specs[0][5]},
                'trit': {'stage': 'TRIT', 'owner': locator(F1,'97-174'), 'action': stage_specs[1][5]},
                'tpk': {'stage': 'TPK', 'owner': locator(F1,'176-219,358-446'), 'action': stage_specs[2][5]},
                'coefficient_origins': coefficients,
                'preserved_information': 'Hojas, residuo, cociente, orientacion, carry, frontera, ruta, ledger, memoria, supervivencia y retorno permanecen en la base; cada lector declara su proyeccion.',
                'enriched_state_and_continuum': {'state': locator(F1,'730-834'), 'joint_constructor': locator(F2,'1028-1118,1169-1205'), 'joint_limit': locator(F3,'898-945')},
                'hmt_output': statement,
                'recognition_and_falsifier': {'recognition': 'Lenguaje posterior de Hilbert, representaciones o variacion; no selecciona entradas HMT.', 'falsifier': falsifier},
                'owners_and_locators': [proof, locator(F2,'1028-1118'), locator(F3,'898-945')],
            }})
    # La lectura de todos los desarrollos queda ligada por huellas completas,
    # aunque cada resultado tenga un localizador probatorio focal.
    maps.append({
        'id':'CONSERVACION_FOCAL_CONJUNTA', 'statement':'Composicion tipada de los seis resultados focales, con sus hipotesis y dominios explicitos conservados.',
        'input_object':BASE_OBJECT, 'domain':BASE_DOMAIN,
        'codomain':'Balance, limite, covariancia, refinamiento e interfaz de accion documentados',
        'output_object':'CONSERVACION_FOCAL_HMT', 'map':'Componer las realizaciones anteriores mediante sus cuadrados; ninguna identifica por nombre dominios distintos.',
        'generator_inputs':[BASE_OBJECT], 'source_family':'HMT', 'proof_locator':locator(main),
        'falsifier':'Omitir una hipotesis de una realizacion o disgregar el constructor comun invalida esa composicion.',
        'genealogical_nine_fields': copy.deepcopy(maps[0]['genealogical_nine_fields'])})
    maps[-1]['genealogical_nine_fields']['hmt_output'] = maps[-1]['statement']
    maps[-1]['genealogical_nine_fields']['coefficient_origins'] = 'Los coeficientes se heredan exclusivamente de los seis mapas focales anteriores, con sus propietarios y sin entradas objetivo.'
    maps[-1]['genealogical_nine_fields']['owners_and_locators'] = [locator(HERE/name) for name in FILES]
    g['result_maps'] = maps
    g['target'] = {
        'statement':maps[-1]['statement'], 'domain':BASE_DOMAIN, 'codomain':maps[-1]['codomain'],
        'closure_criterion':'Identidades (1)-(7) del principal y cuadrados de refinamiento; cada limite tiene su prueba escrita.',
        'result_id':maps[-1]['id'], 'target_family':'POST_CONTINUUM_HMT',
        'causal_cutoff':'ESTRUCTURA_DISCRETA_CONTINUO',
        'causal_cutoff_reason':'Los transportes, medidas, incidencias y salidas de accion realizados proceden del continuo conjunto previamente generado.',
        'forbidden_generator_inputs':['CONVENTIONAL_PI_E_PHI','CODATA_TARGET','TARGET_ENERGY','TARGET_MASS','ASSUMED_GLOBAL_SYMMETRY'],
    }
    g['conventional_uses'] = [{
        'name':'Espacios de Hilbert, teorema espectral y calculo variacional como demostracion posterior',
        'role':'PROOF_LANGUAGE', 'locator':locator(main),
        'occurs_after_hmt_output':True, 'selects_hmt_state':False,'selects_route':False,
        'sets_generators':False,'sets_coefficients':False,'target_value_used_as_input':False}]
    g['proof_layers'] = {
        'finite':'Expansion ortogonal; identidad Gram; conteo de hijos; conjugacion y diferenciacion del transporte; pruebas escritas y casos racionales focales.',
        'compatibility':'Naturalidad conjunta F2; prefijos y coeficientes; proyecciones y transportes analiticos compatibles.',
        'limit':{'required':True, 'finite_levels':'Horizontes completos H_n y realizaciones analiticas declaradas',
            'bonding_maps':'rho_n en estados; R_n y S_n isometricos en observables',
            'compatibility_identity':'Jnext R=SJ; Pnext S=SP; Unext S=SU; Atilde_next S=SAtilde',
            'limit_object':'Limite inverso de historias y limite inductivo Hilbert; por separado, s-lim T^N=Pfix',
            'proof':'Consistencia de cilindros y densidad; cotas uniformes para operadores; convergencia dominada de t(z)^N y telescopia para memoria.'},
        'recognition':'Noether reconoce la carga de una accion ya realizada; los grupos excepcionales mantienen sus dominios y marcos.'}
    g['global_falsifier'] = 'Promover el resultado focal a revalidacion global, omitir memoria o hipotesis, usar constantes objetivo, o separar las cinco construcciones cambia el enunciado autorizado.'
    g['no_disaggregation'] = {
        'aspects':['sp','sol','gau','coh','det'], 'joint':True, 'same_emission':True,
        'generation_and_nonemptiness':locator(F2,'14-61,1169-1205'),
        'single_naturality':locator(F2,'1028-1118'),
        'simultaneous_limit':locator(F3,'898-945'),
        'local_exposition':section(HERE/'REFINAMIENTO.md','## 4. Las cinco operaciones se prolongan dentro de ese mismo sistema'),
        'claim':'Se heredan construccion, no vacuidad y naturalidad sobre la misma emision; el refinamiento focal no selecciona cinco historias.',
        'new_global_proof':False,
    }
    c = {'schema_version':'1.1','artifact':str(main),'artifact_sha256':digest(main),
         'result_id':'CONSERVACION_ESTRUCTURAL_FOCAL_HMT_20260911',
         'genealogy':copy.deepcopy(constants_base['genealogy']),
         'associated_artifacts':copy.deepcopy(g['associated_artifacts']),
         'scope':copy.deepcopy(g['scope']), 'inherited_receipt':locator(BASE_C),
         'genealogy_receipt':str(GOUT), 'seal_state':'AWAITING_FOCAL_GATE_RESULTS'}
    c['genealogy']['app']['operation'] = stage_specs[0][5]
    c['genealogy']['trit'] = {'local_state':'Emision APP orientada con carry', 'regime':'Los tres regimenes TRIT se conservan; la accion eliptica es una realizacion posterior declarada.', 'orientation':'0->0,1->+1,2->-1; retornos y fronteras conservan su signo.'}
    c['genealogy']['tpk'] = {'operator':stage_specs[2][5], 'domain':stage_specs[2][1], 'codomain':BASE_DOMAIN,
        'action':'Genera la historia y su medida; los lectores de memoria, incidencia y accion se componen despues sin cambiar la genealogia.'}
    c['genealogy']['source_locators'] = [str(F1)+':15-95,97-174,358-446,730-834,1277-1433', str(F2)+':1028-1118,1169-1205', str(F3)+':898-945', str(F4)+':668-748,898-995', *[str(HERE/name) for name in FILES]]
    c['genealogy']['focal_constant_roles'] = {
        'pi_phi_e_alpha':'Salidas heredadas del generador; no recalculadas ni usadas como valores convencionales objetivo.',
        'hbar_A_Cstar':'Publicaciones HMT anteriores recibidas por el lector de accion; no calibracion de la prueba.',
        'rational_factors':'Conteo de fases, normalizacion, Gram de incidencia y derivacion del cambio de forma.',
        'whole_catalogue_revalidated':False}
    return g, c


def all_locators(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            yield value
        for child in value.values():
            yield from all_locators(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_locators(child)


def local_semantic_checks(g, c):
    for item in all_locators([g,c]):
        require(digest(item['path']) == item['sha256'], 'Huella focal o heredada cambiada: '+item['path'])
    require(digest(c['artifact']) == c['artifact_sha256'], 'Artefacto del recibo causal de constantes cambiado')
    require({Path(x['path']).name for x in g['associated_artifacts']} == set(FILES[1:]), 'Los tres desarrollos deben estar vinculados')
    for result in g['result_maps']:
        fields = result['genealogical_nine_fields']
        require(set(fields) == set(NINE) and all(fields[k] for k in NINE), 'Nueve campos incompletos: '+result['id'])
    joint = g['no_disaggregation']
    require(joint['aspects'] == ['sp','sol','gau','coh','det'] and joint['joint'] and joint['same_emission'], 'Disgregacion del constructor')
    require('\\label{thm:pdfv2-cor-totalidad-naturalidad}' in F2.read_text(encoding='utf-8'), 'Teorema de totalidad no localizado')
    require('\\label{eq:pdfv2-cor-naturalidad-unica}' in F2.read_text(encoding='utf-8'), 'Naturalidad unica no localizada')
    require('\\label{cor:pdfv2-terminal-limite-cinco-desarrollos}' in F3.read_text(encoding='utf-8'), 'Persistencia simultanea no localizada')
    # Alarma textual complementaria; la semantica ya esta ligada por los nueve
    # campos, las premisas, los mapas, las pruebas y sus huellas. No es --scan.
    spec = importlib.util.spec_from_file_location('hmt_constants_focal', CGATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in FILES:
        errors = module.scan_text(HERE/name)
        require(not errors, 'Alarma causal en '+name+': '+repr(errors))
    print('PASS_NO_DISGREGACION_CINCO_CONSTRUCCIONES_CONTINUO scope=focal inherited_F2_F3=true global_reproof=false')
    print('PASS_NUEVE_CAMPOS_CAUSALES_FOCALES results='+str(len(g['result_maps']))+' artifacts=4')


def validate(g, c):
    local_semantic_checks(g,c)
    results = [
        run([sys.executable,'-I','-S',str(GATE),'--receipt',str(GOUT)], 'PASS_GENEALOGIA_UNICA_APP_TRIT_TPK'),
        run([sys.executable,'-I','-S',str(CGATE),'--audit',str(HERE/FILES[0]),'--receipt',str(COUT)], 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY'),
        run([sys.executable,'-I','-S',str(HERE/'verificar_balances_exactos.py')], 'PASS_BALANCES_RACIONALES_EXACTOS'),
    ]
    # El control finito acompana, pero no sustituye, el teorema espectral.
    local_semantic_checks(g,c)
    return results


def save(path, data):
    require(path in (GOUT,COUT), 'Destino de escritura no autorizado')
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--seal',action='store_true')
    mode.add_argument('--check',action='store_true')
    parser.add_argument('--expected-main-sha')
    args = parser.parse_args()
    if args.seal:
        require(args.expected_main_sha is not None, '--seal exige --expected-main-sha autorizado')
        require(digest(HERE/FILES[0]) == args.expected_main_sha, 'El principal cambió antes del sellado')
        base, constants_base, checks = inherited_checks()
        g,c = make_receipts(base,constants_base,checks)
        local_semantic_checks(g,c)
        save(GOUT,g)
        save(COUT,c)
        results = validate(g,c)
        g['seal_state'] = c['seal_state'] = 'FOCAL_GATES_PASSED_FOR_BOUND_ARTIFACTS'
        g['focal_validation'] = c['focal_validation'] = results
        save(GOUT,g)
        save(COUT,c)
        # Comprobar lo realmente entregado, no solo los objetos en memoria.
        validate(load(GOUT),load(COUT))
        print('PASS_SELLADO_CAUSAL_FOCAL artifacts=4 main_sha256='+args.expected_main_sha)
    else:
        g,c = load(GOUT),load(COUT)
        require(g['seal_state'] == c['seal_state'] == 'FOCAL_GATES_PASSED_FOR_BOUND_ARTIFACTS', 'Recibos no sellados')
        validate(g,c)
        print('PASS_COMPROBACION_RECIBOS_FOCALES artifacts=4')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL_RECIBOS_CAUSALES_FOCALES: '+str(exc), file=sys.stderr)
        raise SystemExit(1)
