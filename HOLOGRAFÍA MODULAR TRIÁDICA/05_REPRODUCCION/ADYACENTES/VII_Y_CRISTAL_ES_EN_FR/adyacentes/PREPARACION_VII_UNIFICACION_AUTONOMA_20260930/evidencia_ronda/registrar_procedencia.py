"""Genera metadatos mecánicos focales; no promueve claims ni modifica el corpus."""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PROJECT = Path('/Users/ruben/Documents/New project')
NOTE = ROOT / 'INTEGRACION_MATEMATICA.md'
BASE_G = PROJECT / 'output/INVESTIGACION_PI_MEDIO_20260929/enlace_fase_accion/tu_contribucion/RECIBO_GENEALOGIA.json'
BASE_C = PROJECT / 'output/ACUMULACION_ACCION_HOLOGRAFIA_20260929/RECIBO_CONSTANTES_NARRATIVA.json'


def loc(path):
    p = Path(path)
    data = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(data).hexdigest(),
            'lines': '1-' + str(len(data.splitlines()))}


proof = loc(NOTE)
rid = 'COMPOSICION-CUATRO-SECTORES-FOCAL-20260929'
statement = 'Componer los lectores de vacío, calibre, Higgs y respuesta gravitatoria, y demostrar la compatibilidad matricial color-mezcla en la realización declarada.'
g = copy.deepcopy(json.loads(BASE_G.read_text()))
g['receipt_id'] = rid
g['artifact'] = {**proof, 'kind': 'DERIVATION', 'anchors': [
    {'stage': s, 'text': t} for s, t in [
        ('APP', 'APP →'), ('TRIT', 'TRIT →'), ('TPK', 'TPK →'),
        ('ESTADO_ENRIQUECIDO', 'estado enriquecido →'),
        ('ESTRUCTURA_DISCRETA_CONTINUO', 'estructura discreta conjunta del continuo.'),
        ('HMT_OUTPUT', '**Proposición 1.**'),
        ('CONVENTIONAL', 'El reconocimiento convencional posterior conserva')]]}
g['target'].update(statement=statement, domain='C_CONT_DISC',
    codomain='COMPOSICION_LECTORES_Y_REPRESENTACION_FINITA', result_id=rid,
    closure_criterion='Proposiciones 1-5 en sus dominios explícitos y realización variacional quiral del sector quark; la composición contiene antecedentes cuánticos y no se clasifica globalmente como clásica. No demuestra aún el cierre conjunto de todas las interacciones.',
    causal_cutoff_reason='Los canales y representaciones recibidos son salidas posteriores al continuo; la nota prueba la composición de estos lectores.')
g['target']['forbidden_generator_inputs'] = ['CODATA_target', 'PDG_target', 'unification_verdict', 'measured_masses_as_selectors']
g['result_maps'] = [{
    'id': rid, 'statement': statement, 'input_object': 'c_cont_disc',
    'domain': 'C_CONT_DISC', 'codomain': 'COMPOSICION_LECTORES_Y_REPRESENTACION_FINITA',
    'output_object': 'lectores_compuestos_y_representacion_color_mezcla',
    'map': 'T->(D,Xi)->s_plus_minus->respuesta y gamma; alpha,L*,hbar,c->G y accion; V_CKM unitario y color->J_i,C_a y cambio de base; conexiones->producto tensorial vectorial.',
    'generator_inputs': ['c_cont_disc'], 'source_family': 'HMT', 'proof_locator': proof,
    'falsifier': 'No unitariedad rompe el conmutador; perder orientación invierte gamma; composición quiral requiere equivariancia del mapa Higgs; no se afirma un cierre cuántico global.'}]
g['conventional_uses'][0].update(name='Cálculo funcional, álgebra de bloques y conexiones tensoriales como lenguaje de prueba posterior.', locator=proof)
g['proof_layers'] = {
    'finite': 'Proposiciones 1-5 y corolario fuerte-gravitatorio con pruebas algebraicas en el texto; 171 controles focales, no equivalentes a prueba de unificación física.',
    'compatibility': 'Amplificación por identidad, trazas normalizadas y transporte simultáneo de masa y corrientes; cotetrada y representación geométrica comunes cuando se acopla.',
    'limit': {'required': False, 'reason': 'Composición de lectores y representación finita; no se afirma un nuevo límite cuántico acoplado.', 'typing_falsifier': 'Promover la amplificación matricial a teoría cuántica de campos completa sin prueba.'},
    'recognition': 'Realizaciones electrodébiles de árbol, constitutiva y geométrica conservan las condiciones de sus propietarios.'}
g['inheritance_note'] = 'Núcleo común heredado sin cambios; cinco proposiciones focales de composición, no revalidación integral.'
g['scope_boundaries'] = ['No cierre cuántico conjunto de cuatro interacciones.', 'No nueva derivación de etiquetas de carga.', 'No selección numérica nueva del acoplamiento fuerte.', 'No nueva prueba del teorema Yang-Mills completo.', 'Sin modificación de PDF, claims globales ni archivos Lean.']
g['global_falsifier'] = 'Confluencia de parámetros y conmutación de representaciones no implican por sí solas existencia cuántica ni cancelación de anomalías del sistema acoplado.'
g['inherited_receipt'] = loc(BASE_G)

source_root = Path('/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes')
owners = [source_root/p for p in [
    'III_ES/manuscrito/sections/04_respuesta_constitutiva.tex',
    'III_ES/manuscrito/sections/06_pell_barbero.tex',
    'VII_ES/manuscrito/ampliacion_composicion/higgs.tex',
    'VII_ES/manuscrito/ampliacion_composicion/electroweak.tex',
    'VI_ES/sections/08_familias_y_compuestos.tex',
    'VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex',
    'VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex',
    'VIII_ES/manuscrito/90_conclusiones.tex',
    'X_ES/sections/ym_complete.tex', 'X_ES/sections/ym_scale.tex']]
g['focal_owners'] = [loc(p) for p in owners]

c = copy.deepcopy(json.loads(BASE_C.read_text()))
c.update(artifact=str(NOTE), artifact_sha256=proof['sha256'], result_id=rid,
    scope_note='Cinco proposiciones focales y una realización variacional quiral dentro de una composición que incluye antecedentes cuánticos; condiciones de los propietarios conservadas; no certifica unificación física completa.',
    audited_text_scope=proof, focal_claim_locator=proof,
    focal_material_owners=g['focal_owners'], prior_receipt_provenance=loc(BASE_C),
    declared_realization_assumptions={'domain': 'x>y>0; tree electroweak; labeled sheets; unitary CKM; strong monoidal realization; vectorial spin coupling; chiral equivariance declared separately.'})
c['genealogy']['tpk'].update(
    operator='Transporte angular e incidencia hexada-octada heredados; lector CKM y representación cromática posteriores.',
    domain='Estado HMT completo y sus lectores anteriores a esta composición.',
    codomain='Confluencia de lectores y compatibilidad representacional en los dominios probados.',
    action='Componer los lectores espectrales sin invertir su origen; preservar etiquetas, refinamiento y cambio de base simultáneo.')
c['genealogy']['source_locators'] = [str(p) for p in owners]
gpath = ROOT / 'RECIBO_GENEALOGIA.json'
gpath.write_text(json.dumps(g, ensure_ascii=False, indent=2)+'\n')
c['focal_genealogy_receipts'] = [loc(gpath)]
(ROOT/'RECIBO_CONSTANTES.json').write_text(json.dumps(c, ensure_ascii=False, indent=2)+'\n')
(ROOT/'MANIFIESTO.json').write_text(json.dumps({
    'scope': 'Mathematical composition note, not publication acceptance',
    'artifact': proof, 'owners': g['focal_owners'], 'verifier': loc(ROOT/'verificar_composicion.py'),
    'focal_extensions': [loc(p) for p in sorted((ROOT/'quantum').glob('*'))
                         if p.is_file() and p.suffix in ('.md', '.py')],
    'manuscripts_modified': False, 'global_claims_promoted': False}, ensure_ascii=False, indent=2)+'\n')
print('Metadatos focales generados; ningún teorema certificado por este script.')

# Cada extensión conserva un recibo propio: el hash de la nota principal no
# puede certificar documentos nuevos. Se hereda la genealogía anterior, no un
# supuesto cierre físico global.
extensions = [
    ('MEMORIA_DOMINIO_Y_ALGEBRA.md', 'MEMORIA',
     'Conservar la composición y el álgebra de operadores al incluir explícitamente lectura y memoria; demostrar el dominio autoadjunto de la dilatación 8:1.',
     'TRANSPORTE_OPERATORIO_CON_MEMORIA',
     [('APP', 'APP →'), ('TRIT', 'TRIT →'), ('TPK', 'TPK →'),
      ('ESTADO_ENRIQUECIDO', 'estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO', 'estructura\ndiscreta conjunta del continuo'),
      ('HMT_OUTPUT', 'La escala positiva de acción que aparece abajo es una salida ya publicada'),
      ('CONVENTIONAL', '## 2. Identidad exacta del defecto de compresión')],
     'La dilatación transporta un álgebra ya demostrada; no obtiene las restricciones gravitatorias a partir de operadores abstractos. No confundir defecto de compresión con anomalía quiral.'),
    ('COMPATIBILIDAD_QUIRAL_Y_ANOMALIAS.md', 'QUIRAL',
     'Comprobar la cancelación de anomalías de la representación quiral declarada al componer los lectores recibidos de carga, color y sabor con quarks y leptones.',
     'COMPATIBILIDAD_REPRESENTACION_QUIRAL',
     [('APP', 'APP–'), ('TRIT', 'TRIT–'), ('TPK', 'TPK,'),
      ('ESTADO_ENRIQUECIDO', 'estado enriquecido y'),
      ('ESTRUCTURA_DISCRETA_CONTINUO', 'estructura discreta del continuo.'),
      ('HMT_OUTPUT', 'Las cargas eléctricas utilizadas son las etiquetas recibidas'),
      ('CONVENTIONAL', '## Representación y resultado exacto')],
     'La elección de representación débil se declara; las cargas son lectores recibidos, no una generación nueva. La cancelación no construye por sí sola la medida quiral ni un cierre gravitatorio.'),
    ('ACOPLAMIENTO_GRAVITATORIO_MEMORIA_20260929.md', 'ACOPLAMIENTO',
     'Construir un operador común con registro geométrico cuántico, materia y transporte interno, demostrar covariancia Gauss y conservación del resolvente bajo eliminación de memoria.',
     'EVOLUCION_ACOPLADA_EN_CARTA_FINITA',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta\nconjunta del continuo.'),
      ('HMT_OUTPUT','Las constantes y normalizaciones'),
      ('CONVENTIONAL','Se trabaja en una carta celular finita')],
     'Conserva Gauss interna y memoria; no identifica su densidad de respuesta con todas las restricciones Hamiltonianas PCH.'),
    ('HAMILTONIANO_FINITO_HIGGS_FOCK.md', 'HIGGS_FOCK',
     'Componer Higgs, Yukawa, Fock y torsión reducida con el operador geométrico-interno; demostrar hermiticidad, covariancia, reducción gauge y positividad temporal finita en la carta declarada.',
     'ACOPLAMIENTO_HIGGS_FOCK_TORSION_FINITO',
     [('APP','APP–'), ('TRIT','TRIT–'), ('TPK','TPK se'),
      ('ESTADO_ENRIQUECIDO','estados enriquecidos supervivientes'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','Los coeficientes de acción, los acoplamientos'),
      ('CONVENTIONAL','## 2. Espacio común y transformación gauge')],
     'La torsión se usa en la carta reducida explícita sin doble contabilizar contorsión; no demuestra el límite quiral ni todas las restricciones gravitatorias.'),
    ('REFINAMIENTO_DINAMICO_NONADICO.md', 'REFINAMIENTO',
     'Demostrar energía, norma temporal, Schur exacto y límite de resolventes en una realización covariante de ruta con refinamiento nonádico.',
     'LIMITE_DINAMICO_RUTA_COVARIANTE',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo.'),
      ('HMT_OUTPUT','La escala de acción positiva'),
      ('CONVENTIONAL','El reconocimiento convencional posterior')],
     'El límite es de una ruta o grafo métrico con fibra finita y condiciones conformes; no es el límite de una teoría completa en espacio-tiempo.'),
    ('EVOLUCION_ACOPLADA_Y_LIMITE.md', 'EVOLUCION',
     'Retirar el corte de amplitud y excitación escalar en una carta espacial y geométrica fija; construir forma cerrada interactuante, evolución unitaria, reducción gauge y límite Galerkin.',
     'EVOLUCION_INTERACTUANTE_SIN_CORTE_ESCALAR',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','La escala de acción, los canales angulares'),
      ('CONVENTIONAL','El reconocimiento convencional posterior')],
     'Células, registro geométrico y modos fermiónicos siguen finitos; no se promueve el límite Galerkin escalar a cierre espacial-quiral-gravitatorio completo.'),
    ('ACCION_MEMORIA_TRES_REGIMENES.md', 'ACCION_TRIT',
     'Construir propagadores exactos en los tres regímenes TRIT, demostrar convergencia temporal L1 y metapléctica, transportar la memoria con sus unidades y demostrar covarianza conjunta acción-masa-gravedad.',
     'EVOLUCION_TRIT_MEMORIA_Y_ESCALA',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','Las secciones de acción y las constantes se reciben como salidas internas anteriores.'),
      ('CONVENTIONAL','El reconocimiento convencional posterior')],
     'Realización canónica recibida y parámetros L1 locales; no se identifica el cambio discreto de régimen con conjugación ni la covarianza de escalas con cancelación de anomalías.'),
    ('TRIT_CURVATURAS_Y_DEFORMACIONES.md', 'TRIT_GEOMETRIA',
     'Componer las tres conexiones de Cartan, variación de transporte, deformaciones normales y naturalidad del corchete con memoria y cambio de rango; representar momentos en semidensidades de configuraciones finitas.',
     'ALGEBRA_COVARIANTE_Y_DEFORMACIONES',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo.'),
      ('HMT_OUTPUT','salidas de esa cadena.'),
      ('CONVENTIONAL','## 2. Las tres realizaciones')],
     'Conmutadores geométricos exactos y representación finidimensional; no identifica por su nombre el momento de embeddings con la restricción dinámica PCH.'),
    ('LIMITE_MATERIA_MEMORIA.md', 'HISTORIAS_COMPLETAS',
     'Retirar el corte de historias en la evolución interactuante, componer el retorno reversible y demostrar límite de lectores de masas, Yukawa y torsión y archivo isométrico infinito.',
     'EVOLUCION_INTERACTUANTE_HISTORIAS_COMPLETAS',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta\nconjunta del continuo'),
      ('HMT_OUTPUT','Los valores de los\nlectores son salidas'),
      ('CONVENTIONAL','## 2. La masa conserva')],
     'Historias completas en sector reversible y realizaciones de carta; celularización espacial y modos fermiónicos fijados. No se intercambian los índices de memoria, precisión y espacio.'),
    ('SUSPENSION_RELOJ_INTERACTUANTE.md', 'SUSPENSION',
     'Construir la suspensión autoadjunta del retorno interactuante, su dominio de frontera, monodromía, conservación de Gauss y límite fuerte, sin elegir logaritmo del retorno.',
     'EVOLUCION_CONTINUA_RETORNO_INTERACTUANTE',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','Las constantes son salidas anteriores'),
      ('CONVENTIONAL','La operación de suspensión es\nuna construcción operatoria estándar')],
     'Suspensión de un reloj recibido y del retorno interactuante; no se identifica su generador con todas las restricciones PCH espaciales ni se afirma energía global acotada inferiormente.'),
    ('ACCION_GRAVEDAD_AREA_TORSION.md', 'AREA_TORSION',
     'Componer las ecuaciones de acción, gravedad, reloj y Barbero con el operador de área y la interacción torsional de corriente total; obtener el coeficiente de fase normalizado y su covarianza de sección.',
     'IDENTIDAD_OPERATORIA_AREA_TORSION_ACCION',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','son salidas HMT anteriores'),
      ('CONVENTIONAL','El reconocimiento convencional posterior')],
     'Misma sección de acción y mismos lectores; área, corriente y lapse no se identifican; relación de coeficientes no sustituye el cálculo de restricciones espaciales.'),
    ('LEGENDRE_PCH_Y_RELOJ_PARAMETRIZADO.md', 'LEGENDRE_RELOJ',
     'Derivar el cargo Noether-Legendre de la acción PCH recibida y la restricción autoadjunta de parametrización del mismo reloj interactuante; demostrar álgebra de semidensidades y equivalencia por densidad para lapsos positivos.',
     'CARGO_VARIACIONAL_Y_RESTRICCION_RELOJ',
     [('APP','APP produce'), ('TRIT','TRIT conserva'), ('TPK','TPK transporta'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido con'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del\ncontinuo'),
      ('HMT_OUTPUT','lectores de acción ya generados'),
      ('CONVENTIONAL','La transformación de\nLegendre')],
     'Carga de la acción PCH y restricción del reloj probadas en sus realizaciones; identificar los dos Hamiltonianos sin entrelazador no está demostrado. El control negativo C_N Psi = -i hbar Nprime Psi/2 impide imponer la familia de semidensidades como restricciones simultáneas.'),
    ('CONMUTADOR_ESPACIAL_ESPINORIAL.md', 'CONMUTADOR_ESPACIAL',
     'Calcular el conmutador de dos lapsos espaciales suaves en la realización espinorial recibida, con masa y Yukawa anticommutantes; demostrar transporte tangencial, término de espín y elevación a Fock algebraico.',
     'ALGEBRA_LOCAL_ESPINORIAL_CON_LAPSOS',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta\nconjunta del continuo.'),
      ('HMT_OUTPUT','son salidas HMT anteriores'),
      ('CONVENTIONAL','El reconocimiento\nconvencional posterior')],
     'Conexión intrínseca Clifford compatible, contorsión eliminada separadamente, núcleo suave; el bloque cuártico no es un potencial de un cuerpo. No se identifica el operador de materia con la restricción geométrica total.'),
    ('DEFORMACIONES_ESPACIALES_Y_QUIRALIDAD.md', 'DEFORMACIONES_ESPACIALES',
     'Demostrar naturalidad del cinético espinorial y su graduación, cotransporte de métrica y conexión, límite de cortes espectrales y convergencia de conmutadores de lapsos suaves en núcleo común.',
     'LIMITE_ESPACIAL_COVARIANTE_EN_HOJA_SPIN',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta\ndel continuo.'),
      ('HMT_OUTPUT','Las constantes de acción y velocidad\nson las secciones ya generadas.'),
      ('CONVENTIONAL','## 2. El transporte es entre fibras geométricas')],
     'Hoja compacta suave no degenerada sin borde, lift spin y datos cotransportados; regulador espectral posterior distinto del refinamiento TPK. No prueba uniformidad en lapsos con derivadas sin cota ni cierre de restricciones de geometría dinámica.'),
    ('LIMITE_ESPACIAL_QUIRAL_FUENTES.md', 'LIMITE_ESPACIAL_QUIRAL',
     'Reunir el límite espacial Yang-Mills recibido con la fibra quiral, prolongar graduaciones y CAR y transportar palabras de operadores en núcleos inductivos compatibles; calcular el flujo de detalle omitido por una compresión.',
     'LIMITE_GRADUADO_Y_TRANSPORTE_DE_ALGEBRAS',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del\ncontinuo'),
      ('HMT_OUTPUT','no seleccionan retroactivamente semillas ni constantes.'),
      ('CONVENTIONAL','### 1.1. Entrelazamiento fuerte del propietario Yang–Mills')],
     'El entrelazamiento fuerte se exige por operador y dominio, no se infiere de compresión de formas. Los controles de corte no son anomalías atribuidas al regulador HMT; no se afirma cierre global de restricciones normales.'),
    ('CURVATURA_TOTAL_MEMORIA_Y_LIMITE.md', 'CURVATURA_MEMORIA',
     'Calcular la curvatura de una lectura isométrica móvil con su complemento de memoria, aplicar exactamente la dilatación nonádica 8:1 y demostrar el transporte de la identidad de calibre por inclusiones covariantemente compatibles.',
     'CURVATURA_COMPLETA_Y_LIMITE_COVARIANTE',
     [('APP','APP produce'), ('TRIT','TRIT\nconserva'), ('TPK','TPK transporta'),
      ('ESTADO_ENRIQUECIDO','el estado enriquecido'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','La estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','Los coeficientes de acción son salidas HMT anteriores.'),
      ('CONVENTIONAL','El reconocimiento convencional posterior')],
     'La memoria restaura la curvatura completa, no la anula por definición. El límite exige la identidad covariante de inclusiones móviles y núcleos; no se identifica holonomía central con una restricción gauge sin su representación.'),
    ('CURVATURA_TPK_Y_REFINAMIENTO.md', 'CURVATURA_TPK',
     'Comparar rutas afines completas, calcular el Hessiano de energía de memoria y su cancelación covariante, conservar productos cruzados y construir una diagonal nonádica de precisión con error menor que el área infinitesimal.',
     'SEGUNDA_VARIACION_Y_LIMITE_DE_CURVATURA',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura\ndiscreta conjunta del continuo'),
      ('HMT_OUTPUT','las constantes, incluidos los lectores de acción, se reciben como salidas'),
      ('CONVENTIONAL','## 3. Segunda variación completa')],
     'La simetría del Hessiano no impone curvatura cero. La tasa nonádica se aplica a productos de lectores que satisfacen la cota recibida; no se promociona a límite espacial cuántico total ni se confunde Ward de expectativas con anulación de operadores.'),
    ('CURVATURA_DEFORMACIONES_PCH.md', 'CURVATURA_DIRAC',
     'Derivar el generador de deformación de gráficas de Cauchy a partir de la corriente de la misma acción espinorial, calcular sus variaciones y probar curvatura nula conservando masa, Yukawa, conexión, norma de flujo y graduación.',
     'CURVATURA_DE_EVOLUCION_ESPINORIAL_ENTRE_SUPERFICIES',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','las secciones de acción'),
      ('CONVENTIONAL','## 2. Corriente y operador')],
     'Problema de Dirac lineal sobre geometría y campos suaves declarados, globalmente hiperbólico y sin flujo de borde no especificado; no se convierte el término cuártico ni la métrica cuántica en un potencial externo. No certifica el cierre cuántico total.'),
    ('GRAVEDAD_EN_EL_SISTEMA_CONJUNTO.md', 'GRAVEDAD_CONJUNTA',
     'Reunir la incorporación gravitatoria en su realización declarada: identidad operatoria energia-masa-radio, memoria dinamica, retroaccion en el operador conjunto y fuentes de la misma accion; probar la identidad adimensional y su covarianza.',
     'INCORPORACION_GRAVITATORIA_EN_REALIZACION_CONJUNTA',
     [('APP','APP produce'), ('TRIT','TRIT conserva'), ('TPK','TPK transporta'),
      ('ESTADO_ENRIQUECIDO','El estado enriquecido'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','son salidas HMT anteriores'),
      ('CONVENTIONAL','El reconocimiento convencional posterior')],
     'Se conservan R1-R8 del lector radial y los dominios de la forma acoplada y la accion PCH. No se iguala cualquier Hamiltoniano con H_X ni se acredita curvatura cuantica total cero para deformaciones normales arbitrarias.'),
    ('AUTOINERCIA_ACOPLAMIENTO.md', 'AUTOINERCIA',
     'Componer el lector autoinercial con energia, masa y gravedad del mismo caracter; extenderlo por calculo espectral y demostrar naturalidad de su reduccion con memoria y de su refinamiento.',
     'LECTOR_AUTOINERCIAL_DEL_CARACTER_RADIAL',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','son salidas de sus lectores HMT'),
      ('CONVENTIONAL','reconocimiento gravitatorio externo')],
     'Lector en el sector de amplitud comun, con descenso del reloj y caracter positivo declarados. No se identifica el lector con una ley de fuerza ni con la curvatura cuantica total.'),
    ('RETROACCION_PCH_Y_RESTRICCIONES_VARIACIONALES.md', 'RETROACCION_RESTRICCIONES',
     'Reunir accion PCH con materia y metricas dinamicas; reducir contorsion, recuperar Legendre y demostrar propagacion de restricciones iniciales sobre las soluciones regulares con fuente total.',
     'COMPATIBILIDAD_VARIACIONAL_CON_RETROACCION',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
      ('HMT_OUTPUT','son salidas recibidas'),
      ('CONVENTIONAL','## 2. Misma acción')],
     'Sector regular de la accion recibida, coframe no degenerado, variaciones interiores y eliminacion consistente de segunda clase; propagacion durante existencia regular. No afirma existencia global ni identifica Poisson con conmutador cuantico.'),
    ('CIERRE_CANONICO_TOTAL_Y_REPRESENTACION.md', 'CURVATURA_CANONICA',
     'Calcular la curvatura de la conexion del potencial canonico total y su anulacion sobre las direcciones caracteristicas de la superficie regular de restricciones; demostrar la identidad precuantica y distinguir su representacion del Hamiltoniano interactuante anterior.',
     'CONEXION_CANONICA_TOTAL_SOBRE_SUPERFICIE_DE_RESTRICCIONES',
     [('APP','APP →'), ('TRIT','TRIT →'), ('TPK','TPK →'),
      ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
      ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo.'),
      ('HMT_OUTPUT','La escala de acción y los acoplamientos son salidas HMT'),
      ('CONVENTIONAL','El reconocimiento convencional posterior')],
     'Carta regular y parametros interiores de la accion total. No se identifica la conexion precuantica con el Hamiltoniano cuantico interactuante previo, ni planitud con holonomia global trivial. El limite hacia otra representacion exige entrelazamiento efectivo de conexiones, no solo archivo reversible.')]
for filename, suffix, claim, codomain, anchors, boundary in extensions:
    path = ROOT/'quantum'/filename
    if not path.is_file():
        continue
    ploc = loc(path)
    identifier = rid+'-'+suffix
    eg = copy.deepcopy(g)
    eg['receipt_id'] = identifier
    eg['artifact'] = {**ploc, 'kind': 'DERIVATION', 'anchors': [
        {'stage': stage, 'text': anchor} for stage, anchor in anchors]}
    eg['target'].update(statement=claim, result_id=identifier, codomain=codomain,
        closure_criterion=claim+' '+boundary)
    eg['result_maps'] = [{**g['result_maps'][0], 'id': identifier,
        'statement': claim, 'codomain': codomain, 'map': claim,
        'output_object': suffix.lower()+'_compatibilidad',
        'proof_locator': ploc, 'falsifier': boundary}]
    eg['conventional_uses'][0].update(
        name='Lenguaje de prueba y reconocimiento posterior de los lectores recibidos.', locator=ploc)
    eg['proof_layers']['finite'] = 'Pruebas explícitas en la nota y controles negativos adjuntos; no prueba de cierre global.'
    eg['proof_layers']['compatibility'] = claim
    eg['proof_layers']['limit'] = {'required': False,
        'reason': 'No se anuncia un nuevo límite acoplado de las cuatro interacciones. Los dominios operatorios se prueban en la nota de memoria.',
        'typing_falsifier': boundary}
    if suffix in ('REFINAMIENTO', 'EVOLUCION'):
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Mallas nonádicas de ruta' if suffix == 'REFINAMIENTO' else 'Subespacios completos Peter-Weyl y Hermite sobre una carta espacial fija',
            'bonding_maps': 'Inclusiones conformes lineales por tramos' if suffix == 'REFINAMIENTO' else 'Inclusiones de subespacios invariantes con proyección ortogonal respecto de la medida recibida',
            'compatibility_identity': 'Igualdad de formas restringidas y norma exacta; ortogonalidad de Galerkin, no entrelazamiento finito supuesto',
            'limit_object': codomain,
            'proof': str(path)+'; prueba de coercividad, densidad del núcleo de forma y convergencia de resolventes. '+boundary}
    if suffix == 'ACCION_TRIT':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Medias por celdas de particiones nonádicas del generador temporal K en L1 local',
            'bonding_maps': 'Refinamiento de particiones y aproximación por medias; no se postula igualdad de soluciones finitas',
            'compatibility_identity': 'Norma L1 de K_n-K tiende a cero; cota (7) de propagadores simplécticos y levantamiento metapléctico desde identidad',
            'limit_object': codomain,
            'proof': str(path)+' §§3–5: serie de integrales iteradas, variación de constantes y recubrimiento metapléctico.'}
    if suffix == 'HISTORIAS_COMPLETAS':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Truncaciones de los lectores sobre el mismo espacio de historias y archivos de memoria con cola residual',
            'bonding_maps': 'Aproximación de coeficientes en dominio de forma común; J_N divide residuo del archivo conservando bloques previos',
            'compatibility_identity': 'Cota de error (2), convergencia de forma por fibra y cota resolvente uniforme; J_N V_N=V_(N+1)',
            'limit_object': codomain,
            'proof': str(path)+' §§3–6: suma directa autoadjunta, convergencia dominada de resolventes, telescopía e inversa del archivo.'}
    if suffix == 'SUSPENSION':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Lectores truncados H_N sobre el mismo portador, con T, hbar y C fijos',
            'bonding_maps': 'Convergencia resolvente fuerte de H_N y productos unitarios de sus evoluciones',
            'compatibility_identity': 'Frontera psi(T)=C^-1 psi(0) conservada, grupos de traslación ponderada convergen fuertemente',
            'limit_object': codomain,
            'proof': str(path)+' §5: convergencia dominada de multiplicadores y traslaciones, transformada de Laplace de los grupos.'}
    if suffix == 'DEFORMACIONES_ESPACIALES':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Cortes espectrales del cinético espacial sobre hoja compacta; en suma de historias son cortes por fibra',
            'bonding_maps': 'Inclusiones espectrales y cotransporte unitario de la misma geometría, espín y conexión',
            'compatibility_identity': 'P_Rprime U_phi = U_phi P_R; convergencia Sobolev controla productos de primer orden en H2',
            'limit_object': codomain,
            'proof': str(path)+' §§2–5: naturalidad, núcleo elíptico, estimación resolvente y convergencia de conmutadores; no uniformidad sobre lapsos de derivadas ilimitadas.'}
    if suffix == 'LIMITE_ESPACIAL_QUIRAL':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Realizaciones espaciales isométricas del propietario Yang-Mills y fibra graduada recibida',
            'bonding_maps': 'J_m y su segunda cuantización exterior, compatibles con graduación',
            'compatibility_identity': 'chi_(m+1) J_m = J_m chi_m y A_(m+1) J_m = J_m A_m sobre núcleos declarados',
            'limit_object': codomain,
            'proof': str(path)+' §§3–5: extensión isométrica, densidad de tensores y palabras finitas de operadores; la compresión no sustituye el entrelazamiento.'}
    if suffix == 'CURVATURA_MEMORIA':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Realizaciones con índices conjuntos de precisión, espacio y modos y núcleos estables declarados',
            'bonding_maps': 'Inclusiones isométricas C2 móviles J_mu_lambda compatibles por composición y graduación',
            'compatibility_identity': 'delta_N J + (i/hbar) H_N^mu J - (i/hbar) J H_N^lambda = 0',
            'limit_object': codomain,
            'proof': str(path)+' §7, teorema 3: curvatura entrelazada en núcleo cilíndrico denso; igualdad de clausuras sólo con condición de núcleo. Identidad (16) para defectos aproximados.'}
    if suffix == 'CURVATURA_TPK':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Productos de lectores nonádicos acotados y bucles de tamaño epsilon_m=9^-m',
            'bonding_maps': 'Transporte exacto y aproximación de lectores con cota r*729^-n',
            'compatibility_identity': 'r*729^-m / epsilon_m^2 = r*9^-m tiende a cero en la clase de productos declarada',
            'limit_object': codomain,
            'proof': str(path)+' §6: cota telescópica de productos, extracción de curvatura con error o(area) y control negativo de intercambio indebido de límites.'}
    if suffix == 'CURVATURA_DIRAC':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Cortes espectrales fijos en la carta de deformaciones y precisión de coeficientes del mismo Dirac',
            'bonding_maps': 'Proyecciones sobre núcleo suave con cotas Sobolev y conservación de graduación',
            'compatibility_identity': 'La variación del flujo Q_f y su raíz S_f define el mismo generador; F_m=0 antes de comprimir y el defecto de corte converge a cero',
            'limit_object': codomain,
            'proof': str(path)+' §§5–6: corriente conservada, problema de Cauchy y convergencia de productos/derivadas sobre núcleo; familias uniformemente espaciales y cotas declaradas.'}
    if suffix == 'AUTOINERCIA':
        eg['proof_layers']['limit'] = {
            'required': True,
            'finite_levels': 'Cortes espectrales acotados del mismo caracter positivo inyectivo Y y sectores areal-volumetrico',
            'bonding_maps': 'Inclusiones espectrales e isometrias efectivas que entrelazan los caracteres Y y los modos W_av',
            'compatibility_identity': 'I_prime (K tensor J)=(K tensor J) I; la cola espectral de Y converge en norma de grafo sobre su dominio',
            'limit_object': codomain,
            'proof': str(path)+' §5: identidad tensorial de refinamiento y convergencia de la integral espectral de lambda^2 en la cola.'}
    extra_owners = {
        'ACCION_TRIT': ['X_ES/sections/hamiltonianos_curvatura.tex', 'II_ES/sections/gravedad_rigidez_20260926.tex', 'VIII_ES/manuscrito/sections/temporalidad_trit.tex'],
        'TRIT_GEOMETRIA': ['VIII_ES/manuscrito/30d_realizacion_geometrica.tex', 'VIII_ES/manuscrito/30c_composicion_corriente_conexion.tex', 'X_ES/sections/hamiltonianos_curvatura.tex'],
        'HISTORIAS_COMPLETAS': ['VI_ES/sections/05b_electron_estados_ley_masas_20260927.tex', 'XII_ES/nuclear/09.tex', 'VI_ES/sections/05_registro_operador_masa.tex'],
        'SUSPENSION': ['XII_ES/nuclear/09.tex', 'II_ES/sections/gravedad_rigidez_20260926.tex'],
        'LEGENDRE_RELOJ': ['VIII_ES/manuscrito/30c_composicion_corriente_conexion.tex', 'VIII_ES/manuscrito/30d_realizacion_geometrica.tex', 'VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex'],
        'CONMUTADOR_ESPACIAL': ['VIII_ES/manuscrito/30d_realizacion_geometrica.tex', 'X_ES/sections/hamiltonianos_curvatura.tex'],
        'DEFORMACIONES_ESPACIALES': ['VIII_ES/manuscrito/30d_realizacion_geometrica.tex', 'X_ES/sections/hamiltonianos_curvatura.tex'],
        'LIMITE_ESPACIAL_QUIRAL': ['VIII_ES/manuscrito/30b_variacion_energia_memoria.tex', 'VIII_ES/manuscrito/30c_composicion_corriente_conexion.tex', 'VI_ES/sections/13_fock_pauli_composicion.tex'],
        'CURVATURA_MEMORIA': ['VII_ES/manuscrito/desarrollos/restitucion_operatoria.tex', 'VIII_ES/manuscrito/30b_variacion_energia_memoria.tex', 'X_ES/supplement/00_MEMORIA_Y_FORMA.md'],
        'CURVATURA_TPK': ['VIII_ES/manuscrito/29_retorno_y_memoria_traslacional.tex', 'VIII_ES/manuscrito/30b_variacion_energia_memoria.tex', 'XII_ES/nuclear/09.tex'],
        'CURVATURA_DIRAC': ['VIII_ES/manuscrito/30d_realizacion_geometrica.tex', 'VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex', 'VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex'],
        'AREA_TORSION': ['II_ES/sections/gravedad_rigidez_20260926.tex', 'VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex', 'VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex'],
        'GRAVEDAD_CONJUNTA': ['II_ES/sections/gravedad_rigidez_20260926.tex', 'VIII_ES/manuscrito/30b_variacion_energia_memoria.tex', 'VIII_ES/manuscrito/80_observador_y_respuesta_relacional.tex'],
        'AUTOINERCIA': ['II_ES/sections/gravedad_rigidez_20260926.tex', 'II_ES/sections/10_gravedad.tex', 'VIII_ES/manuscrito/80_observador_y_respuesta_relacional.tex'],
        'RETROACCION_RESTRICCIONES': ['VIII_ES/manuscrito/30d_realizacion_geometrica.tex', 'VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex', 'VIII_ES/manuscrito/33_corriente_espinorial_y_densidad.tex']}
    eg['focal_owners'] = [*g['focal_owners'], *[loc(source_root/p) for p in extra_owners.get(suffix, [])]]
    if suffix == 'AREA_TORSION':
        eg['focal_owners'].append(loc('/Users/ruben/Documents/excelencia academica/output/AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929/fuentes/V_ES/sections/v_area_informacion.tex'))
    if suffix in ('GRAVEDAD_CONJUNTA', 'AUTOINERCIA'):
        eg['focal_owners'].append(loc('/Users/ruben/Documents/excelencia academica/output/AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929/fuentes/II_ES/sections/gravedad_rigidez_20260926.tex'))
    if suffix in ('LEGENDRE_RELOJ', 'CURVATURA_CANONICA'):
        eg['focal_owners'].append(loc(PROJECT/'output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex'))
    if suffix == 'CURVATURA_CANONICA':
        eg['focal_owners'].extend([
            loc(ROOT/'quantum'/'RETROACCION_PCH_Y_RESTRICCIONES_VARIACIONALES.md'),
            loc(source_root/'XII_ES/nuclear/09.tex')])
        eg['proof_layers']['finite'] = 'Identidades diferenciales (1)-(8) demostradas en la carta regular; no se anuncian nuevos controles computacionales.'
        eg['proof_layers']['limit'] = {
            'required': False,
            'reason': 'El resultado nuevo es la planitud caracteristica de la conexion canonica. No se anuncia un nuevo limite espacial-quiral del Hamiltoniano interactuante; el transporte de una identidad al limite conserva las condiciones del teorema ya escrito.',
            'typing_falsifier': boundary}
    eg['proof_layers']['recognition'] = 'Operadores, formas y resolventes como realización matemática posterior; coeficientes recibidos conservan su origen. '+boundary
    eg['inheritance_note'] = 'Genealogía común y salidas recibidas conservadas; resultado focal declarado en este recibo.'
    eg['scope_boundaries'] = [boundary, 'Sin modificación de manuscritos ni promoción de cierre físico global.']
    eg['global_falsifier'] = boundary
    egpath = ROOT/'quantum'/('RECIBO_GENEALOGIA_'+suffix+'.json')
    egpath.write_text(json.dumps(eg, ensure_ascii=False, indent=2)+'\n')
    ec = copy.deepcopy(c)
    ec.update(artifact=str(path), artifact_sha256=ploc['sha256'], result_id=identifier,
        scope_note=boundary, audited_text_scope=ploc, focal_claim_locator=ploc,
        focal_genealogy_receipts=[loc(egpath)], focal_material_owners=eg['focal_owners'])
    (ROOT/'quantum'/('RECIBO_CONSTANTES_'+suffix+'.json')).write_text(
        json.dumps(ec, ensure_ascii=False, indent=2)+'\n')
