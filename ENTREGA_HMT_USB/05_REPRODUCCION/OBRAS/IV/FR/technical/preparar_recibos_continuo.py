#!/usr/bin/env python3
"""Vinculación focal de la ampliación local, sin otorgar autorización editorial.

La plantilla universal se conserva como contexto tipado. El resultado propio
es la composición local efectivamente expuesta en continuo_conjunto.tex; no se
hereda una afirmación de que REV02 ya hubiera integrado sus cinco operaciones.
No ejecuta puertas ni escribe en el registro canónico. Cada fuente compuesta
tiene un directorio por hash y conserva sus recibos anteriores.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.with_name('ARTICULO_IV_REV02_EDICION_INTEGRADA_20260910')
PROJECT = ROOT.parents[1]

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def spec(path, lines=None):
    result = {'path': str(path), 'sha256': sha(path)}
    if lines:
        result['lines'] = lines
    return result

def save_once(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if path.exists() and path.read_text(encoding='utf-8') != text:
        raise RuntimeError('Recibo de corte ya existente con otro contenido: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def main():
    module_spec = importlib.util.spec_from_file_location('iv_continuo_graph', ROOT/'technical/compilar_iv.py')
    compiler = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(compiler)
    graph = compiler.source_graph()
    if graph['errors']:
        raise RuntimeError(str(graph['errors']))

    def expand(path, stack=()):
        if path in stack:
            raise RuntimeError('Inclusión circular: ' + str(path))
        source = compiler.strip_comments(path.read_text(encoding='utf-8'))
        def replace(match):
            child = compiler.resolve_tex(path, match.group(1), match.group(2))
            return '\n' + expand(child, stack+(path,)) + '\n'
        return re.sub(r'\\(input|include)\s*\{([^{}]+)\}', replace, source)

    combined = expand(ROOT/'main.tex') + '\n'
    source_cut = hashlib.sha256(combined.encode('utf-8')).hexdigest()[:16]
    cut = source_cut + '_' + sha(Path(__file__))[:8]
    out = ROOT/'technical/recepcion_20260911'/cut
    out.mkdir(parents=True, exist_ok=True)
    artifact = out/'FUENTE_COMPUESTA.tex.txt'
    if artifact.exists() and artifact.read_text(encoding='utf-8') != combined:
        raise RuntimeError('Colisión de fuente compuesta')
    artifact.write_text(combined, encoding='utf-8')

    inherited_current = load(OLD/'technical/recepcion_rev02/CORTE_ACTUAL.json')
    inherited_path = Path(inherited_current['genealogy_receipt']['path'])
    inherited = load(inherited_path)
    template = load(PROJECT/'tools/plantillas/RECIBO_GENEALOGIA_UNICA_APP_TRIT_TPK.json')
    receipt = template
    receipt['receipt_id'] = 'IV_CONTINUO_LOCAL_20260911_' + cut
    receipt['scope_kind'] = 'DERIVATION'
    receipt['formal_kernel'] = copy.deepcopy(inherited['formal_kernel'])
    receipt['foundation'] = copy.deepcopy(inherited['foundation'])
    receipt['artifact'] = {**spec(artifact), 'kind':'DERIVATION', 'anchors':[]}
    anchor_texts = [
        ('APP', 'Evaluación aritmética levantada'),
        ('TRIT', 'Firma ternaria y levantamiento local'),
        ('TPK', 'Actualización del TPK'),
        ('ESTADO_ENRIQUECIDO', 'La igualdad de fase y el incremento de memoria son compatibles'),
        ('ESTRUCTURA_DISCRETA_CONTINUO', 'Construcción correlativa del continuo: historias, transporte, incidencia y terminal'),
        ('HMT_OUTPUT', 'En cada residencia, el complejo local libre'),
        ('CONVENTIONAL', 'Unicidad con carácter central primitivo fijado'),
    ]
    position = 0
    for stage, text in anchor_texts:
        pattern = r'\s+'.join(map(re.escape, text.split()))
        match = re.search(pattern, combined[position:])
        if match is None:
            raise RuntimeError('Ancla no localizada después de su antecedente: ' + stage)
        start = position + match.start()
        receipt['artifact']['anchors'].append({'stage':stage, 'text':match.group(),
            'line':combined.count('\n',0,start)+1})
        position += match.end()

    body = ROOT/'sections/continuo_conjunto.tex'
    owner = spec(body, '1-'+str(len(body.read_text(encoding='utf-8').splitlines())))
    receipt['stages'] = copy.deepcopy(inherited['stages'])
    for stage in receipt['stages'][:2]:
        stage['owner'] = spec(ROOT/'sections/nucleo.tex', '1-258')
    receipt['stages'][3]['owner'] = owner
    receipt['stages'][3]['inheritance'] = {
        'mode':'RESULTADO_RECUPERADO',
        'manuscript_status':'HISTORIAS_LEVANTADAS_Y_MEMORIA_AFIN_EXPLICITAS_EN_LA_SUCESORA'}
    stage = receipt['stages'][-1]
    stage['codomain'] = 'JointLocalHistoryConstruction'
    stage['output_object'] = 'C_cont_local'
    formula = ('h -> U_k e_h=sum_epsilon sqrt(p(epsilon|h))e_(h epsilon); '
        'A=Pprime U P+Qprime U Q; eta=Qprime U P+Pprime U Q; '
        'kappa(u,v)_ij=u_i-v_j; delta(w)_ij=w_ij-w_i0-w_0j+w_00; '
        'd f=3c e+b,d e=g,d b=-3c g,d r=0; '
        'B_(q,r)=sum_paths W(nu_q) tensor Gamma_r(nu_0); '
        'D=d_bar+(-1)^q d_Gamma; Det(Tot B)=tensor_(q,r) Det(B_(q,r))^((-1)^(q+r))')
    stage['map'] = {'name':'Operaciones conjuntas sobre las mismas historias levantadas', 'formula':formula}
    stage['action_on_generators'] = {
        'generators':['historias levantadas con hoja actual y prefijo completo',
                      'puertos etiquetados de ambas hojas', 'f,e,b,r,g y caminos terminales'],
        'formula':formula,
        'effect':'Construye transporte, cancelación, incidencia, complejo de memoria y línea determinante conjunta; conserva terminal y condiciones del límite.'}
    stage['owner'] = owner
    stage['inheritance'] = {
        'mode':'RESULTADO_RECUPERADO_Y_FORMALIZACION_EXPLICITA',
        'manuscript_status':'OPERACIONES_CONJUNTAS_LOCALES_REUNIDAS_CON_PRUEBAS_CONTIGUAS',
        'scope':'Esta residencia es de la sucesora, no una atribución retrospectiva a REV02 ni una prueba de Weil.'}
    receipt['trit_constraints'] = copy.deepcopy(inherited['trit_constraints'])
    receipt['tpk_constraints'] = copy.deepcopy(inherited['tpk_constraints'])
    receipt['target'] = {
        'statement':'Componer las operaciones conjuntas locales del continuo sobre el árbol de historias APP–TRIT–TPK, con pruebas de cociclo, isometría, balance, incidencia, naturalidad y ensamblaje terminal.',
        'domain':'JointLocalHistoryConstruction',
        'codomain':'LocalIdentitiesAndCompatibleHistoryPublications',
        'closure_criterion':'Identidades locales del capítulo continuo_conjunto, sobre sus dominios y condiciones explícitos; no identificación con la forma completa de Weil.',
        'result_id':'IV_CONTINUO_LOCAL', 'target_family':'POST_CONTINUUM_HMT',
        'causal_cutoff':'ESTRUCTURA_DISCRETA_CONTINUO',
        'causal_cutoff_reason':'Las identidades pertenecen al ensamblaje producido sobre historias enriquecidas; sus lecturas posteriores no seleccionan las emisiones.',
        'forbidden_generator_inputs':['CODATA','TARGET_ALPHA','TARGET_WEIL_POSITIVITY','ZEROS_OF_ZETA','TARGET_MASS']}
    receipt['result_maps'] = [{
        'id':'IV_CONTINUO_LOCAL', 'statement':receipt['target']['statement'],
        'input_object':'C_cont_local', 'domain':'JointLocalHistoryConstruction',
        'codomain':'LocalIdentitiesAndCompatibleHistoryPublications',
        'output_object':'JointLocalIdentities',
        'map':'Composición afín; transporte isométrico por historias; esperanza condicional; secuencia rectangular exacta; complejo de memoria y bar total; evaluación terminal y líneas determinantes.',
        'generator_inputs':['C_cont_local'], 'source_family':'HMT', 'proof_locator':owner,
        'falsifier':'Un cruce de hojas omitido en el Gram, pérdida de prefijo, uso de pesos uniformes sin hipótesis, falta de naturalidad de puertos o extinción terminal no demostrada.'}]
    receipt['conventional_uses'] = [{
        'name':'Representación de formas acotadas, extensión de medida cilíndrica y compacidad',
        'role':'PROOF_LANGUAGE', 'locator':owner,
        'occurs_after_hmt_output':True, 'selects_hmt_state':False, 'selects_route':False,
        'sets_generators':False, 'sets_coefficients':False, 'target_value_used_as_input':False}]
    receipt['proof_layers'] = {
        'finite':'Pruebas contiguas por generadores y cálculo exacto; los controles numéricos acompañan, no sustituyen, las pruebas generales.',
        'compatibility':'Concatenación afín, supresión de prefijos y precomposición de puertos marcados; reducción modular y transporte Psi; diferencial total cuadrado cero.',
        'limit':{'required':True,
            'finite_levels':'Historias de longitud k y coeficientes Z/3^N, sobre árboles finitamente ramificados sin hojas terminales cuando se afirma no vacuidad.',
            'bonding_maps':'Supresión de la última emisión y reducción modular, conservando hojas y puertos marcados compatibles.',
            'compatibility_identity':'E_k J_k=I; L_k kappa_k=kappa_(k+1)L_k; L_k delta_k=delta_(k+1)L_k; d Psi=Psi d.',
            'limit_object':'Medida de historias, límite fuerte positivo T_infty y publicaciones de cilindros anidados bajo las condiciones indicadas.',
            'proof':'Normalización por fibras, monotonía positiva y compacidad cilíndrica, demostradas en el capítulo. No se deduce T_infty=0 en general.',
            'status':'LOCAL_LIMITS_WITH_EXPLICIT_CONDITIONS'},
        'recognition':'El uso de lenguaje hilbertiano y de líneas determinantes realiza estructuras ya construidas; no se certifica una realización global de Weil o teoría M.'}
    receipt['provenance'] = 'RESULTADO_RECUPERADO'
    receipt['proof_strength'] = 'EXACTO_INTERNO'
    receipt['conclusion_status'] = 'CLOSED_IN_HMT_DOMAIN'
    receipt['residual_if_any'] = None
    receipt['global_falsifier'] = receipt['result_maps'][0]['falsifier']
    receipt['normative_context_semantics'] = (
        'universal_genealogy es el contrato tipado heredado, no la afirmación de que este PDF transcriba íntegramente los resultados del corpus. '
        'El resultado cerrado de este recibo es exclusivamente IV_CONTINUO_LOCAL y sus condiciones explícitas. '
        'No certifica positividad global de Weil, RH, catálogo de masas ni clausura física de teoría M.')
    receipt['previous_receipt_provenance_only'] = spec(inherited_path)
    receipt['new_incorporation'] = {'source':owner, 'predecessor_contained_this_chapter':False,
        'technical_review':'Revisión focal de raíz y del revisor independiente; no validación científica autoral por una aprobación editorial.'}
    save_once(out/'RECIBO_GENEALOGICO_CONTINUO_LOCAL.json', receipt)

    causal_path = Path(inherited_current['constants_receipt']['path'])
    causal = load(causal_path)
    causal['schema_version'] = '1.1'
    causal['artifact'] = str(artifact)
    causal['result_id'] = 'IV_CONTINUO_LOCAL_20260911'
    causal['genealogy']['source_locators'] = [str(ROOT/row['path']) for row in graph['tex']]
    causal['editorial_revision'] = {'predecessor_receipt':spec(causal_path),
        'scope':'Vinculación focal de las fuentes vigentes; campos de constantes heredados con su causalidad, no nueva certificación de todos sus productores.',
        'new_joint_continuum_residence':owner,
        'no_global_Weil_or_physical_closure':True}
    causal['focal_provenance'] = {'status':'RESULTADO_RECUPERADO_Y_FORMALIZACION_EXPLICITA', 'body':[str(body)]}
    causal['limits'] = [
        'Este control causal no prueba por sí mismo los teoremas.',
        'Las operaciones conjuntas locales se incorporan ahora con sus dominios, condiciones y pruebas; no se atribuye su transcripción a REV02.',
        'No se identifica la forma completa de Weil ni se demuestra RH mediante estas identidades.',
        'Los teoremas físicos conservan las condiciones expresas de sus capítulos; el radio normalizado no se convierte en un dato metrológico generador.']
    save_once(out/'RECIBO_CAUSAL_CONTINUO_LOCAL.json', causal)
    save_once(out/'GRAFO_FUENTES_ACTIVAS.json', graph)
    current = {'cut':cut, 'directory':str(out), 'scope':'FOCAL_LOCAL_CONTINUUM_ONLY',
        'composed_source':spec(artifact),
        'genealogy_receipt':spec(out/'RECIBO_GENEALOGICO_CONTINUO_LOCAL.json'),
        'constants_receipt':spec(out/'RECIBO_CAUSAL_CONTINUO_LOCAL.json'),
        'active_sources':len(graph['tex']), 'approval_or_gate_generated':False,
        'receipt_generator':spec(Path(__file__))}
    (out.parent/'CORTE_ACTUAL.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(current,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
