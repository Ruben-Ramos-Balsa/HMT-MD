#!/usr/bin/env python3
"""Prepare fresh documentary metadata from accepted incremental Lean receipts.

Read-only on every antecedent. This script neither compiles Lean nor runs gates,
packages files or manufactures a PASS. It records successful supplied receipts,
checks their focal evidence, and leaves acceptance to the real documentary gates.
Normalization, continuation and descendants are required; a terminal receipt is
optional when the last conformal/descent modules were compiled in a later delta.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = next(p for p in HERE.parents if (p/'tools/verificar_genealogia_unica_hmt.py').is_file())
OLD_DIR = HERE/'metadata_cierre_20260922_02'
OLD_V4_SHA = 'f816a8a0c92395c6e3ebaa99eacc7dbab4bfa07e803935cc9e9e5560b652766d'
OLD_CAUSAL_SHA = '35f862bd697fdabed40477ab4430464062fe7337fcdf839b6b7eff8ee3d87a4c'
FIELD_SHA = 'a40c091b74b9cc38ef28888437fbd96f07d8fbf8e84b05d7940202206e16980e'
ORDINARY = {'propext', 'Classical.choice', 'Quot.sound'}
PRESERVED = ('formal_kernel', 'universal_genealogy', 'foundation', 'stage_order',
             'stages', 'trit_constraints', 'tpk_constraints', 'non_regression',
             'continuum_inheritance', 'antecedent_context', 'documentary_contract_continuity')
TARGET = 'TWISTED_ALL_STATE_FIELDS_POSITIVE_ET_AND_CONFORMAL_COMPATIBILITY'
SUMMARY = ('Asignación torcida corregida sobre cada estado del portador reticular heredado: '
    'normalización de cargas, reordenación operatoria, productos normales derivados, '
    'independencia de palabra, corrección exponencial e inversa, involución, descenso '
    'positivo ET, acción par sobre ambos sectores y coincidencia del campo conforme con los modos construidos.')
EXCLUSIONS = [
    'Identidad de Jacobi torcida completa y sus identidades de módulo',
    'Construcción completa de los productos TE y TT y compatibilidades mixtas del orbifold',
    'Teorema íntegro FLM, carácter J=j-744, Aut(Vnatural)=Monster y género cero de Moonshine',
    'Unicidad del prefactor de carga deducida solamente de covarianza energética',
    'Nueva selección de K o nueva formalización íntegra de la genealogía HMT por este incremento',
]

# Each group names actual owners, not a fresh theorem inferred from file counts.
GROUPS = [
    ('NORMALIZATION', ('LatticeTwistedChargeNormalization',),
     'positiveSector o y cargas del mismo Lattice o',
     'chargeField o x con prefactor reticular, truncación, identidad de carga cero y covarianza energética',
     'Definir el prefactor desde halfnormNat y demostrar sus identidades sobre el campo heredado; no deducir su unicidad de la covarianza.', ()),
    ('NORMAL_ORDER', ('LatticeHalfNormalOrderClosed',),
     'Coeficientes creadores y aniquiladores efectivos en HalfFock o',
     'Igualdad operatoria universal de reordenación con el factor de contracción calculado',
     'Componer la recurrencia de reordenación con la convolución finita de exponenciales y el factor formal, para cada par de grados.', ()),
    ('NORMAL_PRODUCTS', ('LatticeTwistedNormalDerivative', 'LatticeTwistedNormalTerms',
       'LatticeTwistedNormalBounds', 'LatticeTwistedNormalCommutation'),
     'Campos Laurent sobre Carrier o y modos semienteros heredados',
     'Productos normales de derivadas divididas en z=t² con conmutación demostrada',
     'Separar creadores y aniquiladores por modo, demostrar soporte rectangular puntual y después intercambiar las cuatro sumas.', ()),
    ('RAW_STATE_MAP', ('LatticeTwistedRawStateField', 'LatticeTwistedWordCoherence'),
     'LatticeCarrier o con su base de ocupación y carga existente',
     'rawStateField o lineal, independiente de palabra y compatible con creación en cada estado',
     'Evaluar palabras por productos normales derivados, extender por la base y eliminar la elección de representante mediante List.Perm.', ('NORMAL_PRODUCTS',)),
    ('CORRECTION', ('LatticeTwistedCorrection', 'TwistedCorrectionScalarKernel',
       'LatticeTwistedCorrectionPreservation', 'LatticeTwistedCorrectionInverse'),
     'LatticeCarrier o con modos no negativos y matriz de Gram inversa heredados',
     'Delta, exponencial e inversa puntualmente polinomiales con identidad de composición y conservación de paridad',
     'Obtener los coeficientes de la ecuación logarítmica bivariada, contraer los modos con Gram inversa y usar el descenso de energía para cada estado.', ()),
    ('CORRECTED_STATE_MAP', ('LatticeTwistedCorrectedStateField', 'LatticeTwistedStateField'),
     'La asignación rawStateField o y la corrección exponencial efectiva',
     'twistedStateField o = W(exp(Delta)u), lineal y Laurent, con vacío, cargas y equivariancia de involución',
     'Sumar los coeficientes W(E_d u) en k+2d usando finitud en d y componer la asignación concreta, no un campo final recibido.', ('RAW_STATE_MAP', 'CORRECTION')),
    ('POSITIVE_ET', ('LatticeTwistedStateDescent', 'LatticeTwistedPositiveStateDescent'),
     'evenSpace o y positiveSector o del mismo retículo y del tensor torcido heredado',
     'positiveDescendedAssignment o: evenSpace o -> campos sobre positiveSector o, bloque ET concreto en z',
     'Anular coeficientes impares, leer los pares, restringir al subespacio positivo y demostrar conmutación con la inclusión y recuperación de chargeField.', ('CORRECTED_STATE_MAP', 'NORMALIZATION')),
    ('CONFORMAL_FIELD', ('LatticeTwistedCorrectionConformal', 'LatticeTwistedRawConformal',
       'LatticeTwistedStateConformal'),
     'Estado conforme heredado y twistedStateField o ya construido',
     'Coeficiente en -2m-4 igual a conformalMode o m, con corrección rank/16 derivada',
     'Evaluar exp(Delta) sobre omega en grados 0 y 2, identificar el campo crudo con el modo cuadrático y reunir el término de vacío sólo en m=0.', ('CORRECTED_STATE_MAP',)),
    ('POSITIVE_CONFORMAL', ('LatticeTwistedPositiveConformal', 'LatticePositiveDescendedConformal'),
     'El estado conforme par y la asignación torcida positiva descendida en z',
     'Coeficiente de grado -m-2 igual al modo conforme positivo heredado',
     'Transportar la igualdad conforme por inclusión de subespacio y descenso z=t², sin modificar normalizaciones.', ('POSITIVE_ET','CONFORMAL_FIELD')),
    ('DIAGONAL_EVEN_ACTION', ('LatticeOrbifoldEvenAction','LatticeOrbifoldEvenConformal'),
     'evenSpace o y la suma Space o=evenSpace o por positiveSector o',
     'Acción de estados pares por campos concretos sobre ambos sectores, con vacío, creación, inyectividad y compatibilidad conforme',
     'Componer por prodMap los campos pares y ET ya construidos; demostrar truncación, inclusiones e igualdad con los modos conformes y consumir sus relaciones de Virasoro.', ('POSITIVE_ET','POSITIVE_CONFORMAL')),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pinned(path, digest):
    if not digest or sha(path) != digest:
        raise RuntimeError('Huella divergente: '+str(path))
    return json.loads(Path(path).read_text())


def locator(path):
    p = Path(path).resolve()
    return {'path':str(p), 'sha256':sha(p), 'lines':f'1-{len(p.read_text().splitlines())}'}


def write_new(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def check_hash(path, expected):
    if sha(path) != expected:
        raise RuntimeError('Evidencia focal modificada: '+str(path))


def read_receipt(path, digest, role, source_dir):
    """Authenticate the exact focal evidence; do not rebuild its inherited cut."""
    r = pinned(path, digest)
    expected = {'normalization':'PASS_CHARGE_NORMALIZATION_DELTA',
        'continuation':'PASS_TWISTED_CONTINUATION_DELTA',
        'descendants':'PASS_TWISTED_DESCENDANTS_DELTA'}
    if role in expected and r['status'] != expected[role]:
        raise RuntimeError('Recibo no integrado de '+role)
    if not r['status'].startswith('PASS_') or not r['status'].endswith('_DELTA'):
        raise RuntimeError('Se exige un recibo de compilación, no un plan')
    if not r.get('authenticated_inputs_unchanged') or any(r.get(k) for k in
            ('predecessors_modified', 'predecessors_recompiled', 'mathlib_rebuilt')):
        raise RuntimeError('La continuidad incremental no quedó registrada')
    root, inventory = path.parent, []
    single = 'sources' not in r and 'source' in r
    if single:
        node = r['source']; name = Path(node['path']).stem
        nodes, order = {name:node}, [name]
        rows = {name:dict(module=name, source_sha256=r['source_sha256'],
            object_sha256=r['object_sha256'], log_sha256=r['log_sha256'],
            exit_code=r['exit_code'], output=r['output'])}
        queries = r['axiom_queries']
    else:
        nodes, order = r['sources'], r['dependency_order']
        rows = {v['module']:v for v in r['modules']}
        if len(rows) != len(r['modules']) or set(rows) != set(nodes) or set(order) != set(nodes) or len(order) != len(nodes):
            raise RuntimeError('Inventario de módulos incompleto')
        probe = r['axiom_probe']; queries = probe['declarations']
        if probe['exit_code']:
            raise RuntimeError('Consulta de axiomas fallida')
        check_hash(root/'axiom_probe.lean', probe['source_sha256'])
        check_hash(root/'axiom_probe.log', probe['output_sha256'])
        publics = [q for n in order for q in nodes[n]['public_declarations']]
        expected_probe = ''.join('import '+n+'\n' for n in order)+''.join('#print axioms '+q+'\n' for q in publics)
        if (root/'axiom_probe.lean').read_text() != expected_probe or (root/'axiom_probe.log').read_text() != probe['output']:
            raise RuntimeError('Sondeo público o transcripción divergente')
        if r['public_declaration_count'] != len(publics):
            raise RuntimeError('Recuento público divergente')
    owners = {}
    for name in order:
        node, row = nodes[name], rows[name]
        source = source_dir/(name+'.lean')
        if row['exit_code'] or row['source_sha256'] != node['sha256']:
            raise RuntimeError('Módulo no compilado satisfactoriamente: '+name)
        log = root/'compile.log' if single else root/'build'/(name+'.log')
        for item,h in ((source,node['sha256']), (root/'build'/(name+'.lean'),node['sha256']),
                (root/'build'/(name+'.olean'),row['object_sha256']), (log,row['log_sha256'])):
            check_hash(item,h)
        if log.read_text() != row['output']:
            raise RuntimeError('Transcripción de compilación divergente: '+name)
        for q in node['public_declarations']:
            if q in owners:
                raise RuntimeError('Declaración duplicada: '+q)
            owners[q] = name
        inventory.append(dict(module=name, source=locator(source), receipt_role=role,
            delivery_path=f'lean/{role}/{name}.lean', public_declarations=node['public_declarations'],
            theorem_names=node['theorem_names'], verification_receipt=locator(path),
            verification_status=r['status']))
    if set(queries) != set(owners) or any(not set(ax) <= ORDINARY for ax in queries.values()):
        raise RuntimeError('Consulta incompleta o axiomas no ordinarios')
    if not single and r['public_declaration_owners'] != owners:
        raise RuntimeError('Propietarios públicos divergentes')
    if r['theorem_names'] != [q for item in inventory for q in item['theorem_names']]:
        raise RuntimeError('Inventario de teoremas divergente')
    return r, inventory


def make_maps(old, inventory):
    by_name = {r['module']:r for r in inventory}
    maps, made = copy.deepcopy(old['result_maps']), []
    parent = old['target']['result_id']
    for suffix, names, domain, codomain, action, dependencies in GROUPS:
        absent = set(names)-set(by_name)
        if absent:
            raise RuntimeError('El alcance del README no está en los recibos: '+', '.join(sorted(absent)))
        rows = [by_name[n] for n in names]
        result_id = 'STATE_FIELDS_'+suffix
        maps.append(dict(id=result_id, statement=action, input_object=parent,
            domain=old['target']['codomain'], actual_lean_domain=domain,
            input_projection='Se usa el retículo, portador y familia de campos que contiene el antecedente tipado; el dominio de cada enunciado Lean está registrado por separado, sin identificarlo con el resumen del contexto.',
            codomain=codomain, output_object=result_id, map=action,
            generator_inputs=[parent]+['STATE_FIELDS_'+d for d in dependencies], source_family='HMT',
            proof_locator=rows[0]['source'], additional_proofs=[r['source'] for r in rows[1:]],
            lean_declarations=[q for r in rows for q in r['public_declarations']],
            falsifier='Usar la conclusión como hipótesis, cambiar el portador heredado o atribuir al resultado una identidad de Jacobi no enunciada.',
            causal_role='POSTERIOR_REALIZATION_ON_INHERITED_LATTICE', provenance='CERTIFICADO_NUEVO',
            verification_receipts=[r['verification_receipt'] for r in rows]))
        made.append(result_id)
    maps.append(dict(id=TARGET, statement=SUMMARY, input_object=parent,
        domain=old['target']['codomain'], codomain=SUMMARY, output_object=TARGET,
        map='Reunir documentalmente los resultados focales y sus propietarios sin añadir un teorema Lean conjunto.',
        generator_inputs=[parent]+made, source_family='HMT', proof_locator=by_name['LatticeTwistedStateField']['source'],
        additional_proofs=[r['source'] for r in inventory], lean_declarations=[],
        aggregate_of_result_maps=made, independent_joint_lean_theorem_claimed=False,
        falsifier='Interpretar el resumen documental o sus controles de esquema como prueba del orbifold completo.',
        causal_role='DOCUMENTARY_ASSEMBLY_OF_PROVED_POSTERIOR_REALIZATIONS', provenance='CERTIFICADO_NUEVO'))
    return maps


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for role in ('normalization','continuation','descendants'):
        p.add_argument('--'+role+'-verification', type=Path, required=True)
        p.add_argument('--'+role+'-sha256', required=True)
    p.add_argument('--terminal-verification', type=Path)
    p.add_argument('--terminal-sha256')
    p.add_argument('--readme', type=Path, default=HERE/'README_CAMPOS_ESTADOS.md')
    p.add_argument('--readme-sha256', required=True)
    p.add_argument('--source-dir', type=Path, default=HERE)
    p.add_argument('--destination', type=Path, default=PROJECT/'output/PAQUETE_ARTICULO_I_CAMPOS_DE_ESTADOS_20260922')
    p.add_argument('--output-dir', type=Path, required=True)
    args = p.parse_args()
    for key,value in vars(args).items():
        if isinstance(value,Path): setattr(args,key,value.expanduser().resolve())
    if bool(args.terminal_verification) != bool(args.terminal_sha256):
        raise RuntimeError('El recibo terminal y su SHA se proporcionan juntos')
    if args.output_dir.exists() or args.readme.is_relative_to(args.output_dir) or args.source_dir.is_relative_to(args.output_dir):
        raise RuntimeError('Se requiere una carpeta nueva de metadatos sin fuentes dentro')
    gp0,cp0 = OLD_DIR/'RECIBO_GENEALOGICO_CAMPOS_TORCIDOS.json',OLD_DIR/'CAUSAL_CAMPOS_TORCIDOS.json'
    old, oldc = pinned(gp0,OLD_V4_SHA),pinned(cp0,OLD_CAUSAL_SHA)
    check_hash(args.readme,args.readme_sha256)
    receipts, inventory, receipt_paths = {}, [], {}
    for role in ('normalization','continuation','descendants','terminal'):
        path = getattr(args,role+'_verification',None)
        if path is None: continue
        receipt_paths[role] = path
        r,rows = read_receipt(path,getattr(args,role+'_sha256'),role,args.source_dir)
        receipts[role] = r; inventory.extend(rows)
    if len({r['module'] for r in inventory}) != len(inventory):
        raise RuntimeError('Un módulo se ha contado en más de un incremento')
    all_publics = [q for item in inventory for q in item['public_declarations']]
    if len(set(all_publics)) != len(all_publics):
        raise RuntimeError('Una declaración pública se ha contado en más de un incremento')
    nr,cr,dr = [receipts[k] for k in ('normalization','continuation','descendants')]
    if (nr['predecessor_receipt_sha256'] != FIELD_SHA or cr['field_receipt_sha256'] != FIELD_SHA
            or dr['field_receipt_sha256'] != FIELD_SHA
            or cr['normalization_receipt_sha256'] != args.normalization_sha256
            or dr['normalization_receipt_sha256'] != args.normalization_sha256
            or dr['continuation_receipt_sha256'] != args.continuation_sha256):
        raise RuntimeError('Cadena de recibos inconsecuente')
    cut = 406
    for role,r in receipts.items():
        inherited = r.get('inherited_module_count',r.get('authenticated_predecessor_modules'))
        if inherited != cut: raise RuntimeError('Corte antecedente incorrecto: '+role)
        cut += sum(item['receipt_role']==role for item in inventory)
    totals = dict(compiled_modules=len(inventory), public_declarations=sum(len(r['public_declarations']) for r in inventory),
        theorem_lemma_count=sum(len(r['theorem_names']) for r in inventory), inherited_modules=406, resulting_modules=cut)
    evidence = {role:dict(**locator(path), status=receipts[role]['status'],
        delivery_path='recibos/'+{'normalization':'normalizacion','continuation':'continuacion','descendants':'descendientes','terminal':'terminal'}[role]+'/VERIFICATION.json')
        for role,path in receipt_paths.items()}
    d = copy.deepcopy(old)
    d['inherited_context'] = dict(source=locator(gp0), previous_current_fields={k:copy.deepcopy(old[k]) for k in
        ('target','scope_exclusions','later_operations_not_claimed','integrated_lean_evidence','scope_note','source_review_testimony') if k in old},
        historical_result_map_ids=[r['id'] for r in old['result_maps']],
        scope='Los mapas anteriores se conservan literalmente como evidencia histórica; sus reservas no sustituyen el alcance vigente de este sucesor.')
    d['result_maps'] = make_maps(old,inventory)
    d['receipt_id'] = 'CAMPOS_ESTADOS_CONTINUIDAD_20260922'
    d['artifact'] = dict(**locator(args.readme),kind='MODULE',anchors=[
        dict(stage=s,text=t) for s,t in [('APP','APP–'),('TRIT','TRIT–'),('TPK','TPK →'),
        ('ESTADO_ENRIQUECIDO','estado enriquecido →'),('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
        ('HMT_OUTPUT','Construcciones efectivas añadidas'),('CONVENTIONAL','No se atribuye una nueva prioridad al álgebra de operadores de vértice')]])
    d['target'] = dict(statement=SUMMARY, domain=old['target']['codomain'],codomain=SUMMARY,
        closure_criterion='Cada propietario focal debe figurar en los recibos integrados suministrados, con fuentes, objetos y consulta pública íntegra; el documento no ejecuta ni reemplaza Lean.',
        result_id=TARGET,target_family='POST_CONTINUUM_HMT',causal_cutoff='ESTRUCTURA_DISCRETA_CONTINUO',
        causal_cutoff_reason='Realización posterior sobre el retículo, cociclo y portadores heredados; los operadores de campo no se renombran TPK.',
        forbidden_generator_inputs=['NUEVA_SELECCION_K','JACOBI_COMO_HIPOTESIS','PRODUCTO_TE_TT_SUPUESTO','MONSTER_COMO_ENTRADA'],
        actual_lean_domain='LatticeCarrier o -> campos en Carrier o; restricción evenSpace o -> campos en positiveSector o. ET está construido como asignación; no se declara probado el sistema íntegro de identidades mixtas.')
    d['inherited_receipt'] = locator(gp0)
    d['previous_lean_build_receipt'] = copy.deepcopy(old['lean_build_receipt'])
    d['lean_build_receipt'] = locator(next(reversed(receipt_paths.values())))
    d['integrated_lean_evidence'] = dict(receipts=evidence,**totals,axioms=sorted(ORDINARY),
        evidence_role='Recibos independientes de Lean registrados, no resultados producidos por estas comprobaciones documentales.')
    d['focal_source_inventory'] = inventory
    d['scope_exclusions'] = '; '.join(EXCLUSIONS)
    d['later_operations_not_claimed'] = EXCLUSIONS
    d['conclusion_status'],d['residual_if_any'] = 'CLOSED_IN_HMT_DOMAIN',None
    d['scope_note'] = SUMMARY+' La reunión terminal es documental, no un nuevo teorema de FLM.'
    d['global_falsifier'] = 'Reclasificar corrección, descendientes o ET como datos no construidos; asumir Jacobi o productos TE/TT; confundir conservación documental y formalización íntegra de HMT o Moonshine.'
    d['proof_layers'] = dict(finite='Cada coeficiente y cada aplicación al estado usa soporte finito demostrado.',
        compatibility='Mismo retículo y cociclo; involución, descenso, inclusión positiva, vacío, cargas y modos conformes.',
        limit=dict(required=False,reason='Series formales con truncación Laurent puntual; no se afirma convergencia analítica.',typing_falsifier='Confundir series formales con una afirmación de convergencia analítica.'),
        recognition='Los campos de vértice son realización posterior; no seleccionan el origen HMT.')
    d['source_review_testimony'] = dict(kind='LECTURA_FOCAL_SIN_COMPILACION',
        report=locator(HERE/'REVISION_MATEMATICA_CAMPOS_ESTADOS_20260922.md'),replaces_integrated_lean_receipt=False)
    d['inherited_sections_policy'] = dict(preserved_literal_keys=list(PRESERVED),
        all_previous_result_maps_preserved_literal=True,previous_result_map_count=len(old['result_maps']))
    d['delivery_status'] = dict(documentary_gates_run=False,packaging_executed_by_this_receipt=False,
        lean_compilation_executed_by_this_script=False,planned_delivery=str(args.destination))
    c = copy.deepcopy(oldc)
    c['inherited_context'] = dict(source=locator(cp0),previous_context=copy.deepcopy(oldc['inherited_context']),
        previous_scope=copy.deepcopy(oldc['formalization_scope']),
        scope='Contexto anterior literal; los mapas nuevos son realizaciones posteriores, no una nueva prueba del origen HMT.')
    paths = [r['delivery_path'] for r in inventory]
    c.update(artifact=str(args.destination/'README.md'),artifact_sha256=args.readme_sha256,result_id=TARGET,
        verification_receipts=evidence,compiled_modules=totals['compiled_modules'],public_declarations=totals['public_declarations'],
        theorem_lemma_count=totals['theorem_lemma_count'],reused_authenticated_modules=406,authenticated_predecessor_modules=406,
        verification_receipt=list(evidence.values())[-1]['delivery_path'],verification_receipt_sha256=list(evidence.values())[-1]['sha256'],
        added_source_modules=[r['module'] for r in inventory])
    c['genealogy']['source_locators'] = [s if Path(s.split(':')[0]).is_absolute() else 'antecedente/'+s for s in oldc['genealogy']['source_locators']]+paths
    focal = c['focal_genealogical_receipt']
    focal['4_coefficient_origins'] = 'La norma reticular determina el prefactor de carga; los modos semienteros y z=t² determinan los factores divididos binom(e/2,n). El núcleo logarítmico bivariado y Gram inversa determinan Delta. Su evaluación conforme da rank/16 sin objetivo impuesto.'
    focal['5_conserved_information'] = 'Se conservan origen, retículo marcado, cociclo, portadores, paridad y graduaciones. El cambio de palabra preserva ocupación; la corrección tiene inversa; el descenso usa coeficientes pares después de demostrar que los impares se anulan.'
    focal['7_produced_output'] = SUMMARY+f" El inventario aceptado reúne {totals['compiled_modules']} módulos y {totals['public_declarations']} declaraciones públicas nuevas respecto del corte 406."
    focal['8_posterior_recognition_and_falsifier'] = 'La realización usa lenguaje de Fock y campos de vértice después del origen HMT. ET es una asignación concreta, no un argumento libre del resultado final. Sería falso usar estos metadatos como demostración de Jacobi, TE/TT completos o Aut(Vnatural)=Monster.'
    focal['9_material_owners'] = paths
    d['focal_genealogical_receipt'] = copy.deepcopy(focal)
    c['formalization_scope'] = dict(context_fields_are_not_new_theorem_claims=True,new_result=SUMMARY,
        same_carrier_as_predecessor=True,same_marked_lattice_as_predecessor=True,new_K_selection=False,
        new_native_evaluation=False,ordinary_modules_axioms=sorted(ORDINARY),not_claimed=EXCLUSIONS,
        causal_gate_is_not_a_lean_proof_checker=True,actual_EE_block=True,actual_ET_assignment=True,
        ET_module_Jacobi_claimed=False,explicit_mixed_block_arguments=['TE','TT'],
        native_inventory_scope='Los axiomas ordinarios corresponden al incremento; las especializaciones nativas históricas mantienen sus propios recibos.')
    c['posterior_realization'] = dict(operator='Productos normales derivados y corrección exponencial sobre el retículo heredado.',
        action=SUMMARY,owners=paths,source_hashes={r['module']:r['source']['sha256'] for r in inventory})
    c['documentary_contract_continuity']['receipt'] = 'antecedente/'+oldc['documentary_contract_continuity']['receipt']
    for key in PRESERVED:
        if d[key] != old[key]: raise RuntimeError('Alteración de fundamento heredado: '+key)
    if d['result_maps'][:len(old['result_maps'])] != old['result_maps']:
        raise RuntimeError('Alteración de mapas antecedentes')
    for key in ('1_app_object_domain_sheets_operation','2_trit_state_regime_orientation',
                '3_tpk_effective_composition','6_enriched_state_and_residence'):
        if focal[key] != oldc['focal_genealogical_receipt'][key]:
            raise RuntimeError('Alteración del contexto focal heredado: '+key)
    args.output_dir.mkdir(parents=True,exist_ok=False)
    gp,cp = args.output_dir/'RECIBO_GENEALOGICO.json',args.output_dir/'CAUSAL.json'
    write_new(gp,d)
    c['genealogy_v4_source'] = dict(**locator(gp),purpose='Recibo documental separado; no sustituye las pruebas Lean.')
    write_new(cp,c)
    source_causal = copy.deepcopy(c)
    source_causal['artifact'] = str(args.readme)
    source_cp = args.output_dir/'CAUSAL_AUDITORIA_FUENTE.json'
    write_new(source_cp,source_causal)
    check_hash(args.readme,args.readme_sha256)
    for role,path in receipt_paths.items(): check_hash(path,getattr(args,role+'_sha256'))
    write_new(args.output_dir/'MANIFIESTO_METADATA.json',dict(status='METADATA_PREPARED_GATES_NOT_RUN',
        generated_at_utc=datetime.now(timezone.utc).isoformat(),script=locator(__file__),
        readme=locator(args.readme),inherited_v4=locator(gp0),inherited_causal=locator(cp0),
        receipts=evidence,inventory_summary=totals,no_lean_compilation=True,no_packaging=True,
        no_new_pass_emitted=True,legacy_arranque_not_promoted_to_pass=True,
        files={gp.name:sha(gp),cp.name:sha(cp),source_cp.name:sha(source_cp)}))
    print(json.dumps(dict(status='METADATA_PREPARED_GATES_NOT_RUN',directory=str(args.output_dir)),ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
