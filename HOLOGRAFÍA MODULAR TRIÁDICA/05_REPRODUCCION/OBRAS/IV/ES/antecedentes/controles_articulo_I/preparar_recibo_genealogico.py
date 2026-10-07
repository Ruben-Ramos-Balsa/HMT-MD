#!/usr/bin/env python3
"""Prepara el recibo editorial v4; --bind lo vincula al texto final existente.

No compila, no extrae texto, no ejecuta puertas y no modifica fuentes.
Sin --bind deja artifact.sha256=null deliberadamente: no es un recibo aceptado.
Cada ejecución recalcula las huellas y los localizadores de las fuentes actuales.
El esquema normativo procede de la plantilla real, no del recibo de investigación.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

PROJECT = Path('/Users/ruben/Documents/New project')
D = Path(__file__).resolve().parent.parent
O = D.parent
I = O / 'fuentes/integral'
B = Path('/Users/ruben/Documents/HMT2/EL_CIERRE_HOLOGRAFICO_DEL_INFINITO_SUCESOR_102_CAPITULOS_2026-08-28_EN_TRABAJO')
S = PROJECT / ('output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/'
               'New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente')
KERNEL = PROJECT / 'PUBLICACION_HMT/REGISTRO_DE_CONTINUIDAD_ACADEMICA/NUCLEO_FORMAL_HMT_PERMANENTE'
TEMPLATE = PROJECT / 'tools/plantillas/RECIBO_GENEALOGIA_UNICA_APP_TRIT_TPK.json'
OUT = D / 'technical/RECIBO_GENEALOGICO_ARTICULO.json'
CORE_DIR = I / ('manuscrito/reconstruccion_quirurgica_20260822/'
                'parte_ii_estructura_discreta/editor_ready/sources/core')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locator(path: Path, lines: str | None = None) -> dict:
    content = path.read_text(encoding='utf-8')
    count = len(content.splitlines())
    if lines is None:
        lines = f'1-{count}'
    for item in lines.split(','):
        bounds = [int(n) for n in item.split('-')]
        start, end = bounds[0], bounds[-1]
        if not 1 <= start <= end <= count:
            raise ValueError(f'Localizador fuera de rango: {path}:{item}; total={count}')
    return {'path': str(path), 'sha256': digest(path), 'lines': lines}


def source_catalog() -> dict:
    entries = {
        'CORE_CANONICAL': (KERNEL / 'CORE_HMT.json', '24-35'),
        'APP_TRIT_STATE': (CORE_DIR / '04b1_estado_arbol_medida_comun.tex', '15-170,172-249,366-551,1238-1277'),
        'CONTINUUM_OPERATIONS': (CORE_DIR / '04b2_operaciones_intrinsecas_correlativas.tex', '872-1205'),
        'CONTINUUM_TERMINAL': (CORE_DIR / '04b3_terminal_naturalidad_limite.tex', '1047-1118'),
        'TPK_INVENTORY': (I / 'manuscrito/propietarios_exactos/tpk/U006F_inventario_operatorio_completo_tpk.tex', None),
        'C27_COINDUCTION': (I / 'manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex', '218-319,399-474,642-674'),
        'CALENDAR_108': (I / 'manuscrito/propietarios_exactos/tpk/U006D_registro_dodecafasico_integral.tex', '13-282'),
        'SIGNED_REGISTER': (I / 'manuscrito/propietarios_exactos/tpk/U016_registro_dodecafasico_hadamard_k.tex', '165-613'),
        'ALPHA_CARRIES': (I / 'colaboracion/partes_i_ii/source/base_residencias/base_c10_sin_encabezado.tex', '787-1155'),
        'ALPHA_FULL_READER': (I / 'manuscrito/sucesor_102/deltas_ley9/c31_dos_vias_alpha_y_prolongacion_nonadica.tex', None),
        'ALPHA_MARKED_JET': (O / 'fuentes/investigacion/DESARROLLO_MATEMATICO.md', '4738-5190'),
        'B001_ELECTRON': (I / 'manuscrito/integracion_83/parte_iv/body/B001_ch48_electron_primera_realizacion_a3f11d97b332_06f_biografia_electron_rev6.tex', '23-51,80-120,281-336,367-491,677-751,763-853'),
        'B002_ELECTRON': (I / 'manuscrito/integracion_83/parte_iv/body/B002_ch48_electron_primera_realizacion_5326d609ca60_06k_electron_two_way_rev11.tex', '14-146'),
        'MASS_10J': (I / 'manuscrito/sucesor_102/deltas_masas/10j_prueba_ley_general_masas_propietario_20260903.tex', '158-161,200-294'),
        'ACTION_READERS': (O / 'fuentes/investigacion/DESARROLLO_MATEMATICO.md', '9471-9541'),
        'MASS_CODE': (PROJECT / 'PUBLICACION_HMT/PAQUETE_RECTOR_LEY_GENERAL_MASAS_HMT_MD_2026-08-06/procedencia/generador_tabla_rev_acumulativa_original.py', '112-128,277-295'),
        'MASS_AUTHORITY': (PROJECT / 'PUBLICACION_HMT/PAQUETE_RECTOR_LEY_GENERAL_MASAS_HMT_MD_2026-08-06/RESULTADO_RECTOR.md', None),
        'EXCEPTIONAL_PALEY': (S / 'colaboracion/partes_i_ii/source/base_residencias/base_c11_sin_encabezado.tex', '5-36'),
        'EXCEPTIONAL_FRAMES': (S / 'colaboracion/partes_i_ii/source/base_residencias/base_c17_sin_encabezado.tex', '268-484,565-824'),
        'EXCEPTIONAL_FLAG': (I / 'manuscrito/sections/hmt/15_bandera_y_rama_excepcional.tex', '21-474'),
        'EXCEPTIONAL_INTERTWINER': (I / 'manuscrito/sections/hmt/delta_297/16c_entrelazador_dodecafase_witt.tex', '96-236,269-316'),
        'EXCEPTIONAL_VOA': (I / 'colaboracion/partes_i_ii/source/public/residencias/capitulo_22_voa_leech_moonshine.tex', None),
        'ELECTRON_PROVENANCE': (D / 'PROCEDENCIA_ELECTRON.md', None),
        'ALPHA_PROVENANCE': (D / 'technical/procedencia_alpha.md', None),
        'EXCEPTIONAL_PROVENANCE': (D / 'technical/procedencia_excepcional.md', None),
        'ELECTRON_CONTROL': (D / 'pruebas/CONTROL_ELECTRON.json', None),
        'ALPHA_CONTROL': (D / 'technical/CONTROL_REGISTRO_ALPHA.json', None),
        'TRIT_TEMPORAL_SOURCE': (B / 'manuscrito/sections/hmt/02_trit_geometrias.tex', '127-196'),
        'EULER_TRIT_SOURCE': (B / 'manuscrito/sections/hmt/09b_algebras_cuadraticas.tex', '289-516'),
        'CYCLOTOMIC_SOURCE': (B / 'manuscrito/sections/hmt/03d_esqueleto_ciclotomico_app.tex', '13-47,145-246'),
        'PRIME_PRODUCT_SOURCE': (B / 'manuscrito/sections/hmt/10_producto_nativo.tex', '1-736'),
        'PRIME_CLOCK_SOURCE': (B / 'colaboracion/parte_iii/source/public_final/base_83/c44_body.tex', '358-420'),
        'VACANCY_ZETA_SOURCE': (B / 'manuscrito/sections/hmt/19b_zeta_vacancias_primos_rev11.tex', None),
        'HOLONOMY_VACANCY_SOURCE': (PROJECT / 'output/INVESTIGACION_HOLONOMIA_NONADICA_CRISTAL_APERIODICO_20260903/DESARROLLO_MATEMATICO.md', '3058-3290,4035-4137'),
        'EULER_ALGEBRA_SOURCE': (PROJECT / 'output/INVESTIGACION_HOLONOMIA_NONADICA_CRISTAL_APERIODICO_20260903/ALGEBRA_HOLONOMICA_UNIVERSAL_Y_EULER_TRITICO.md', None),
    }
    for section in ('nucleo', 'extension', 'generacion', 'registro_k', 'alpha',
                    'electron', 'excepcional', 'comparacion', 'conclusiones', 'bibliografia',
                    'geometria_modular', 'aritmetica_historias', 'k_reversibilidad',
                    'realizacion_electromagnetica', 'trit_desarrollo', 'alpha_dependencias',
                    'electron_articulacion', 'incidencia_articulacion', 'temporalidad_trit',
                    'euler_trit_articulacion', 'vacancias_capacidad', 'primos_retornos'):
        entries['BODY_' + section.upper()] = (D / f'sections/{section}.tex', None)
    return {key: locator(*value) for key, value in entries.items()}


def stage(stage_id, input_object, domain, codomain, output, name, formula,
          generators, effect, owner, evidence, status):
    return {
        'id': stage_id, 'input_object': input_object, 'domain': domain,
        'codomain': codomain, 'output_object': output,
        'map': {'name': name, 'formula': formula},
        'action_on_generators': {'generators': generators, 'formula': formula, 'effect': effect},
        'generator_inputs': [input_object], 'source_family': 'HMT', 'owner': owner,
        'inheritance': {'mode': 'INHERITED', 'source_ids': evidence,
                        'manuscript_status': status},
    }


def result(result_id, statement, codomain, output, formula, inputs, proof,
           falsifier, sources, proved, inherited, residual=None):
    return {
        'id': result_id, 'statement': statement,
        'input_object': 'C_cont_generated', 'domain': 'C_cont^disc',
        'codomain': codomain, 'output_object': output, 'map': formula,
        'generator_inputs': inputs, 'source_family': 'HMT',
        'proof_locator': proof, 'falsifier': falsifier,
        'inheritance': {'source_ids': sources, 'proved_in_manuscript': proved,
                        'received_from_sources': inherited,
                        'autonomous_transcription_residual': residual},
    }


def ordered_anchors(text: str) -> list[dict]:
    # Las anclas sólo vinculan pasajes materiales. No convierten el orden de
    # lectura ni una mención del continuo en prueba de sus teoremas heredados.
    phrases = [
        ('APP', 'Evaluación aritmética levantada'),
        ('TRIT', 'Firma ternaria y levantamiento local'),
        ('TPK', 'Actualización del TPK'),
        ('ESTADO_ENRIQUECIDO', 'La igualdad de fase y el incremento de memoria son compatibles'),
        ('ESTRUCTURA_DISCRETA_CONTINUO', 'Desde la estructura discreta conjunta del continuo'),
        ('HMT_OUTPUT', 'Coordenada alfa de la clausura'),
        ('CONVENTIONAL', 'Comparación con los ajustes de constantes fundamentales'),
    ]
    anchors, pos = [], 0
    for key, phrase in phrases:
        pattern = r'\s+'.join(re.escape(word) for word in phrase.split())
        match = re.search(pattern, text[pos:])
        if match is None:
            raise ValueError(f'Ancla ausente o fuera de orden: {key}: {phrase}')
        literal = match.group(0)
        absolute = pos + match.start()
        anchors.append({'stage': key, 'text': literal,
                        'line': text.count('\n', 0, absolute) + 1})
        pos += match.end()
    return anchors


def prepare(bind: bool, artifact: Path) -> dict:
    receipt = json.loads(TEMPLATE.read_text(encoding='utf-8'))
    src = source_catalog()
    graph = KERNEL / 'TPK_GRAFO_OPERATORIO_TIPADO.json'
    core = json.loads((KERNEL / 'CORE_HMT.json').read_text(encoding='utf-8'))
    canonical_statement = ' -> '.join(core['canonical_chain'])
    receipt.update({
        'receipt_id': 'ARTICULO_AMPLIACION_PI_PHI_E_ALPHA_ELECTRON_20260908',
        'scope_kind': 'MANUSCRIPT',
        'binding_status': 'BOUND_TO_CURRENT_FINAL_TEXT' if bind else 'PENDING_FINAL_BIND',
        'receipt_purpose': ('Procedencia causal y alcance de un manuscrito de trabajo. '
                            'No es una certificación nueva de clausura global, de autosuficiencia '
                            'de la totalidad de productores, de precisión experimental ni de prioridad.'),
        'template_binding': locator(TEMPLATE),
        'source_manifest': src,
        'normative_context_semantics': (
            'universal_genealogy reproduce el contrato rector de la plantilla. '
            'Sus declaraciones de alcance integral describen la arquitectura heredada, '
            'no afirman que este artículo transcriba el catálogo entero de masas, '
            'los cinco resultados terminales ni todas las pruebas del continuo. '
            'El alcance acreditado para el manuscrito está en target, result_maps, '
            'proof_layers y residual_if_any. Un pase de procedencia no sustituye esas pruebas.'),
        'formal_kernel': {
            'typed_operator_graph': {'path': str(graph), 'sha256': digest(graph)},
            'typed_operator_graph_schema': 'HMT_TPK_TYPED_OPERATOR_GRAPH_V2',
            'definition_independent_of_any_pdf': True,
        },
        'artifact': {
            'path': str(artifact), 'sha256': digest(artifact) if bind else None,
            'kind': 'MANUSCRIPT',
            'anchors': ordered_anchors(artifact.read_text(encoding='utf-8')) if bind else [],
            'binding_note': ('Huella y anclas calculadas del archivo material existente; '
                             'regenerar si cambia el texto o cualquiera de las fuentes.') if bind else
                            'Enlace pendiente a la extracción final; no ejecutar la puerta con este borrador.',
        },
        'target': {
            'statement': ('Reunir en un manuscrito causal APP–TRIT–TPK la generación regional, '
                          'el registro K, las dos vías de alfa, la composición electrónica y '
                          'la prolongación excepcional, con comparación metrológica posterior '
                          'y dependencias autónomas expresamente delimitadas.'),
            'domain': 'C_cont^disc',
            'codomain': 'ManuscriptClaimsWithExplicitInheritedMapsAndResiduals',
            'closure_criterion': ('No se solicita clausura matemática global: cada familia conserva '
                                  'sus mapas, condiciones, prueba reproducida, dependencia heredada '
                                  'y falsador; las obligaciones de transcripción se mantienen abiertas.'),
            'result_id': 'MANUSCRIPT_CAUSAL_ASSEMBLY',
            'target_family': 'POST_CONTINUUM_HMT',
            'causal_cutoff': 'ESTRUCTURA_DISCRETA_CONTINUO',
            'causal_cutoff_reason': ('El electrón y las lecturas excepcionales son posteriores '
                                    'al estado aritmético y al continuo discreto conjunto; '
                                    'la herencia de ese constructor no se sustituye por sus lectores.'),
            'forbidden_generator_inputs': ['CONVENTIONAL_PI_E_PHI', 'CODATA_2018', 'CODATA_2022',
                                            'TARGET_ALPHA', 'TARGET_ELECTRON_MASS', 'TARGET_DECIMAL_PREFIX',
                                            'BARBERO_IMMIRZI', 'EXTERNAL_METROLOGICAL_SCALE'],
        },
        'foundation': {
            'claim_id': 'HMT-FOUNDATION-APP-TRIT-TPK', 'mode': 'INHERITED',
            'claim_statement': canonical_statement,
            'claim_statement_sha256': hashlib.sha256(canonical_statement.encode('utf-8')).hexdigest(),
            'claim_statement_origin': 'CORE_HMT.json $.canonical_chain, unión literal mediante " -> "',
            'evidence_ids': ['CORE_CANONICAL', 'APP_TRIT_STATE', 'CONTINUUM_OPERATIONS', 'CONTINUUM_TERMINAL'],
            'inheritance_is_new_global_reproof': False,
        },
    })
    receipt['stages'] = [
        stage('APP', 'DiscreteSeeds_D9_TwoCursors', 'D9^2 x Directions x D9^2 x Directions',
              'APP_LiftedEvaluations', 'APP_two_leaves', 'A9 with positive Euclidean lift',
              '(i,j) -> ((rho9(i+j),q9(i+j)),(rho9(ij),q9(ij))); n=rho9(n)+9q9(n)',
              ['1,...,9', 'horizontal/vertical positions', 'sum/product operations', 'cardinal directions'],
              'Construye las dos hojas y conserva enteros, residuos, cocientes y origen; no recibe números reales objetivo.',
              src['BODY_NUCLEO'], ['CORE_CANONICAL', 'APP_TRIT_STATE'], 'FINITE_RULE_AND_PROOF_TRANSCRIBED'),
        stage('TRIT', 'APP_two_leaves', 'APP_LiftedEvaluations', 'APP_TritOrientedEmissions',
              'TRIT_oriented_emissions', 'rho3_or and carry lift',
              'Delta(epsilon)=or(epsilon)+3*kappa(epsilon); 0->0,1->+1,2->-1; J_tau^2=-tau I',
              ['APP divisions', 'oriented emission incidence'],
              'Distingue régimen, orientación y acarreo sin sustituirlos por el signo visible.',
              src['BODY_NUCLEO'], ['CORE_CANONICAL', 'APP_TRIT_STATE'], 'FINITE_RULE_AND_PROOF_TRANSCRIBED'),
        stage('TPK', 'TRIT_oriented_emissions', 'APP_TritOrientedEmissions', 'TPK_TransportedHistories',
              'TPK_histories', 'U_t and typed route concatenation',
              'U_t=Upd_t o Tra_t o Sel_t; x->T_d(x); m->C_epsilon*m+kappa(epsilon); '
              'sigma9(w,r)=(w+floor((r+1)/9),r+1 mod9); Gamma9=U_(t+8)...U_t',
              ['M_ph', 'cardinal translations T_d', 'Euclidean carry', 'ordered route extensions'],
              'Selecciona hoja, transporta posiciones y frontera, concatena ruta y actualiza fase, memoria y cilindro; '
              'la realización finita T_min se distingue del transporte de extensiones completas.',
              src['TPK_INVENTORY'], ['CORE_CANONICAL', 'APP_TRIT_STATE', 'BODY_NUCLEO', 'BODY_EXTENSION'],
              'FINITE_TWO_CURSOR_RULE_TRANSCRIBED_FULL_ARCHITECTURE_INHERITED'),
        stage('ESTADO_ENRIQUECIDO', 'TPK_histories', 'TPK_TransportedHistories', 'X_chi',
              'x_chi_generated', 'Ordered ledger and compatible prefix state',
              'Led(gamma)=(lambda(epsilon1),...,lambda(epsilonk)); '
              'lambda=(source,target,resSigma,quoSigma,resPi,quoPi,or,kappa,boundary,Qminus,Qplus); '
              'v_K=(B_K,delta_K,x_K,C_K,Sigma_K,omega_K,ell_K,g(K),Lambda_K)',
              ['transported emissions', 'surviving prefixes', 'both leaves and phase/memory endpoints'],
              'Ensambla el registro producido conservando hoja, fibra, frontera, supervivencia y terminal; '
              'el lector visible no se declara inversible sobre toda la historia.',
              src['APP_TRIT_STATE'], ['APP_TRIT_STATE', 'BODY_EXTENSION', 'C27_COINDUCTION'],
              'STATE_AND_MEMORY_DISTINCTION_TRANSCRIBED_FULL_COMPATIBILITY_INHERITED'),
        stage('ESTRUCTURA_DISCRETA_CONTINUO', 'x_chi_generated', 'X_chi', 'C_cont^disc',
              'C_cont_generated', 'G_cont: common intrinsic constructor and terminal inverse system',
              'G_cont(x) uses D_(k,N)(x) with O(epsilon)=<O_sp,O_sol,O_gau,O_coh,O_det;Cpl_epsilon>; '
              'u_(l,Nprime),(k,N) D_(l,Nprime)(x_l)=D_(k,N)(tau_(l,k)x_l); '
              'terminal=lim_inverse Term_(k,N), retaining all histories and extension witnesses',
              ['same surviving enriched emissions', 'complete terminal multisections', 'common refinement maps'],
              'Las cinco operaciones consustanciales se producen sobre la misma emisión con sus relaciones; '
              'no son ramas independientes ni se generan copiando la entrada como primera coordenada.',
              src['CONTINUUM_OPERATIONS'], ['APP_TRIT_STATE', 'CONTINUUM_OPERATIONS', 'CONTINUUM_TERMINAL'],
              'INHERITED_JOINT_CONSTRUCTION_NOT_REPROVED_BY_MANUSCRIPT_OR_THIS_RECEIPT'),
    ]
    receipt['tpk_constraints']['forward_map'] = {
        'name': 'Typed affine memory transport and phase odometer',
        'formula': '(x,m,w,r)->(T_d(x),C_epsilon*m+kappa(epsilon),w+chi9(r),r+1 mod9)',
    }
    receipt['tpk_constraints']['inverse_map'] = {
        'name': 'Reversal on reversible routes and recorded predecessor on a prefix fibre',
        'formula': '(xprime,mprime)->(T_(-d)(xprime),C_epsilon^(-1)*(mprime-kappa(epsilon))); '
                   'kappa(rev epsilon)=-C_epsilon^(-1)*kappa(epsilon), '
                   'on the declared reversible domain; no inverse of a many-to-one visible projection',
    }
    receipt['tpk_constraints']['preserves'] += ['sheet', 'fibre', 'winding', 'terminal', 'reader']
    residual_e108 = (
        'Transcribir y evaluar E108^{90,120} sobre los generadores efectivos de las incidencias del ledger '
        'para producir sus 25 coordenadas sin cargarlas como literales. El tipo, composición y naturalidad '
        'se heredan; Pi_H y la inversión U<->K están probadas. No es ausencia global de U ni entrada convencional.')
    residual_alpha = (
        'Transcribir una regla evaluable de cada coeficiente de E21/22 de grados >=10, sus cuadrados '
        'de truncamiento y las cotas necesarias de cola/derivada. La familia compatible y la igualdad '
        'de sus límites se reciben de c27/c31; el jet P9 no se promueve a operador completo. '
        'No se afirma racionalidad, irracionalidad ni trascendencia de alfa o e+pi.')
    residual_exceptional = (
        'Conservar explícita la carta de incidencia, los marcos y su transporte, el lift binario y '
        'el orden marcado de las tres regiones positivas. La enumeración Paley y el entrelazador I/6 '
        'no reproducen por sí solos íntegramente el productor de esas cartas ni una acción monstruosa sobre '
        'dígitos o rutas. Métrica A2, cámara positiva, vecino y VOA tienen sus dominios propios; '
        'FLM y Moonshine se usan como teoremas posteriores, no como coeficientes del generador.')
    receipt['result_maps'] = [
        result('REGIONAL_GENERATION', 'Lectores regionales y prolongación coinductiva conjunta anterior al contraste.',
               'CompatibleRegionalCylindersAndReadouts', 'regional_readouts',
               'w6->w12->w18->w24->w30->R36->G9; on regional fibres apply closure/propagation/autoscale readers '
               'and compatible cylinder limits; recognition of pi,e,phi is downstream.',
               ['C_cont_generated', 'regional seed fibres', 'oriented TRIT mode calendar', 'Gamma9'],
               src['BODY_GENERACION'],
               'Introducir prefijos objetivo, sustituir el estado por K_ph, identificar 243 con 729 o fase con memoria.',
               ['C27_COINDUCTION', 'BODY_EXTENSION', 'BODY_GENERACION'],
               'Reglas finitas, lectores, pruebas algebraicas y encierros descritos en el cuerpo.',
               'Sistema coinductivo completo y su compatibilidad desde las fuentes focales; no nueva ejecución por este recibo.'),
        result('SIGNED_K', 'Registro firmado, transformación de Hadamard y lectores racionales distintos.',
               'SignedRegister_U12_K_WithBoundary', 'signed_K_readout',
               'R_sgn=Pi_H o E108^{90,120} o R12; K=H12^(-1)U; '
               'kappa36=N_K/1000^12, kappaper=N_K/(1000^12-1)',
               ['C_cont_generated', 'terminal state', 'calendar and transported incidences'],
               src['BODY_REGISTRO_K'], 'Seleccionar K restando alfa objetivo o equiparar U con la carta local de eventos sin mapa.',
               ['CALENDAR_108', 'SIGNED_REGISTER', 'ALPHA_PROVENANCE'],
               'Carta 1+5+6, Pi_H, Hadamard, extractor transversal y diferencia entre lecturas racionales.',
               'Origen tipado de la evaluación E108 y sus canales antes de alfa.', residual_e108),
        result('ALPHA_TWO_ROUTES', 'Coordenada alfa por acarreo completo y segundo lector compatible, sin fusionar sus obligaciones.',
               'AlphaCoordinateWithCarryAndGradedReader', 'alpha_readout',
               'A_j=P_j+E_j-F_j-K_j+c_(j+1)-1000*c_j; '
               'alpha=sum A_j*1000^(-j)=pi+e-phi-4-kappaper; '
               'alpha_B is the positive root of inherited full E21/22, compared via common compatible cylinders.',
               ['C_cont_generated', 'regional HMT coordinates', 'signed_K_readout', 'compatible carry boundaries', 'graded HMT invariants'],
               src['BODY_ALPHA'], 'Confundir c13=0 y c13=-1, kappa36 y kappaper, o inferir la cola de E21/22 del jet P9.',
               ['ALPHA_CARRIES', 'C27_COINDUCTION', 'ALPHA_FULL_READER', 'ALPHA_MARKED_JET', 'ALPHA_PROVENANCE'],
               'Telescopado, normalización, jet/resolvente y equivalencia de límites bajo compatibilidad. La clasificación aritmética se conserva fuera del artículo por instrucción autoral.',
               'Productor E108 y sistema completo de truncamientos de la segunda vía.', residual_alpha),
        result('ELECTRON_ACTION', 'Escalar basal, razón de acción y beta en una carta dimensional declarada.',
               'ElectronScalarsAndActionLineWithDeclaredChart', 'electron_readout',
               'Delta4=((pi-e*log(pi))/270)*(1+pi/729); '
               'b0=(sqrt(3)/4)*(exp(phi/pi^2)-22*alpha^3)*(1+15*Delta4); '
               'b_beta=b0*(H5/eta)^(80-54*alpha+6*Delta4); '
               'Sigma_H=phi*alpha^16 selects decade -34 on the action line, not an extra factor in b_beta.',
               ['C_cont_generated', 'APP joint table', 'regional_readouts', 'alpha_readout',
                'central TPK route', 'H4 cokernel', 'declared H5 and eta readers'],
               src['BODY_ELECTRON'], 'Omitir 1+pi/729, mezclar Delta4, introducir -22 dentro de exp, duplicar -34 '
               'o identificar el escalar con masa o con cuanto cronológico sin carta.',
               ['B001_ELECTRON', 'B002_ELECTRON', 'MASS_10J', 'ACTION_READERS', 'MASS_CODE', 'MASS_AUTHORITY', 'ELECTRON_PROVENANCE'],
               'Prefactor APP, retorno tipado, coeficientes regionales, vacancia posterior a alfa, triple80/54/6, '
               'cotas de década, reconciliación documental Delta4 y composición algebraica.',
               'Lectores H5/eta y calibre regional recibidos con fuentes; la dimensión requiere una base de acción/energía declarada.',
               'No se afirma unicidad de cualquier funcional posible, identificación física independiente de la carta, '
               'ni derivación completa nueva de toda la ley de masas.'),
        result('EXCEPTIONAL_READOUT', 'Incidencia y realización excepcional del mismo origen con cartas y niveles distintos.',
               'TransportedCodesFlagsLatticesVOA', 'exceptional_readout',
               'Q_n(x)=((f_j,(w_j,w_j*A_j)))_(j<=n), f_(j+1)=g_j(x)f_j; '
               'in Paley chart C_W={(w,w*A_W)}, I^t I=36I+30J, U_W=I/6 on V11; '
               '(K,s0,frame)->flag->A2^12 glue->rootless neighbour->VOA, then recognition.',
               ['C_cont_generated', 'regional words and transported frames', 'signed_K_readout',
                'precarry signed state', 'declared incidence chart and A2 metric'],
               src['BODY_EXCEPCIONAL'], 'Confundir proyección de soporte con inversa del estado, GL6 con isometría Hamming, '
               'una estrella con M12, norma54 fuera de cámara o acción VOA con acción sobre dígitos.',
               ['C27_COINDUCTION', 'EXCEPTIONAL_PALEY', 'EXCEPTIONAL_FRAMES', 'EXCEPTIONAL_FLAG',
                'EXCEPTIONAL_INTERTWINER', 'EXCEPTIONAL_VOA', 'EXCEPTIONAL_PROVENANCE'],
               'Código/incidencia finitos, bandera, isometría I/6, estrella y argumentos reticulares con hipótesis explícitas.',
               'Transporte de cartas y lift incidencial de fuentes; teoremas externos de reconocimiento en sus dominios.',
               residual_exceptional),
        result('TRIT_EXPONENTIAL_REALIZATIONS',
               'Tres generadores concretos y resolución polinómica de sus regímenes, posteriores a las coordenadas regionales.',
               'DirectSumOfThreeQuadraticRepresentations', 'trit_exponential_readout',
               'APP multiplication by4 gives C; local nilpotent N; TPK mode incidence Fav gives A=Fav^2; '
               'Je=(2C+I)/sqrt3, Jp=N, Jh=(2A-3I)/sqrt5; Jtotal^6=Jtotal^2.',
               ['C_cont_generated', 'APP unit orbits and additive/multiplicative sheets',
                'TRIT quadratic type', 'TPK mode calendar', 'regional_readouts'],
               src['BODY_EULER_TRIT_ARTICULACION'],
               'Fallo de (2C+I)^2=-3I, N^2=0 o (2Fav^2-3I)^2=5I; '
               'uso de un valor objetivo para seleccionar C o Fav; una transición atribuida a la suma directa sin mapa TPK.',
               ['CYCLOTOMIC_SOURCE', 'EULER_TRIT_SOURCE', 'EULER_ALGEBRA_SOURCE', 'BODY_EULER_TRIT_ARTICULACION'],
               'Matrices, relaciones cuadráticas, tres evaluaciones exponenciales y proyectores con pruebas contiguas.',
               'Origen APP del ciclo y origen modal Fav conservados; no una teoría dinámica física de cristal temporal.'),
        result('CAPACITY_VACANCY_TRIT',
               'Complementariedad exacta de capacidad y vacancias; selección trítica inducida por los eventos.',
               'TypedCapacityEventClockAndMemory', 'capacity_vacancy_readout',
               'rho=log_1000(729); delta=1-rho; C_t=floor((t+1)rho); '
               'C_t-C_(t-1)=1-z_t; p_j=floor(j/delta),v_j=p_j-j; '
               'v_(j+1)-v_j=h_j-1; [v_(j+1)]_3=[v_j-(22-h_j)]_3; tau=Mph(1+[v_j]_9).',
               ['C_cont_generated', 'APP cubic completion729/1000', 'TRIT phase selector',
                'TPK block clock and compatible refinement'], src['BODY_VACANCIAS_CAPACIDAD'],
               'Confundir contador de bloques y capacidad, perder el origen de índice, o identificar vacancia temporal con partícula sin mapa.',
               ['HOLONOMY_VACANCY_SOURCE', 'TRIT_TEMPORAL_SOURCE', 'BODY_TEMPORALIDAD_TRIT', 'BODY_VACANCIAS_CAPACIDAD'],
               'Identidad telescópica y régimen módulo3 probados; control racional100000pasos y4096huecos adjunto.',
               'Parametrización de trayectorias y lectura temporal +1/0/-1 heredadas con operadores de memoria.'),
        result('NATIVE_PRIMES_AND_VACANCY_READOUTS',
               'Producto nativo, selector de irreducibles, órdenes de retorno y dos observables de vacancias.',
               'NativeMultiplicativeMonoidAndDirichletReadouts', 'native_prime_readout',
               'APP cells -> native sum and scalar transducer -> Horner product; '
               'DeltaRed counts nonunit factorizations; P_irr=(I-P_unit)1_{0}(DeltaRed*DeltaRed); '
               'tau_n=ord_n10; ZvacPlus=delta*zeta+H on Re(s)>1 with H holomorphic Re(s)>0; '
               'Euler product over selected primes has only claimed domain Re(s)>1.',
               ['C_cont_generated', 'APP local residue/quotient sheets', 'TRIT labels and preserved regime',
                'TPK transport memory', 'capacity_vacancy_readout'], src['BODY_PRIMOS_RETORNOS'],
               'Seleccionar primos por período decimal, identificar formas normales con todas las historias, '
               'o trasladar discrepancia acotada sobre enteros a una estimación no probada sobre primos.',
               ['PRIME_PRODUCT_SOURCE', 'PRIME_CLOCK_SOURCE', 'VACANCY_ZETA_SOURCE', 'BODY_PRIMOS_RETORNOS'],
               'Operaciones, entrelazamiento, selector con dominio de clausura, mcm de órdenes y sumación de Abel expuestos.',
               'No se incorpora ni se certifica la demostración global de RH en este artículo.'),
        result('MANUSCRIPT_CAUSAL_ASSEMBLY',
               'Ensamblaje expositivo de las familias anteriores con sus hipótesis y residuos, no otro generador del continuo.',
               'ManuscriptClaimsWithExplicitInheritedMapsAndResiduals', 'manuscript_claims',
               'Compose the declared regional, signed, carry, electronic and incidence readers '
               'from G_cont; record each typed claim with its proof or explicit inherited dependency. '
               'This is an editorial dependency map, not a replacement definition of G_cont.',
               ['C_cont_generated', 'regional_readouts', 'signed_K_readout', 'alpha_readout',
                'electron_readout', 'exceptional_readout'], src['BODY_CONCLUSIONES'],
               'Promover una transcripción parcial, un checksum o un acuerdo decimal a clausura global o igualdad experimental.',
               ['BODY_NUCLEO', 'BODY_EXTENSION', 'BODY_GENERACION', 'ALPHA_PROVENANCE',
                'ELECTRON_PROVENANCE', 'EXCEPTIONAL_PROVENANCE', 'BODY_COMPARACION'],
               'Composiciones y pruebas que efectivamente constan en el cuerpo; se preserva el alcance por familias.',
               'Construcción conjunta y fuentes focales expresamente individualizadas.',
               'Artículo en curso de autosuficiencia: E108, lector E21/22 completo e incidencias marcadas no se borran del alcance.'),
    ]
    receipt['result_families'] = {
        'APP': {'stage_refs': ['APP'], 'source_ids': ['BODY_NUCLEO', 'BODY_EXTENSION']},
        'TRIT': {'stage_refs': ['TRIT'], 'source_ids': ['BODY_NUCLEO', 'BODY_TRIT_DESARROLLO']},
        'TPK': {'stage_refs': ['TPK', 'ESTADO_ENRIQUECIDO', 'ESTRUCTURA_DISCRETA_CONTINUO'],
                'source_ids': ['TPK_INVENTORY', 'APP_TRIT_STATE', 'CONTINUUM_OPERATIONS', 'CONTINUUM_TERMINAL']},
        'GENERACION': {'result_refs': ['REGIONAL_GENERATION', 'TRIT_EXPONENTIAL_REALIZATIONS', 'CAPACITY_VACANCY_TRIT']},
        'PRIMOS': {'result_refs': ['NATIVE_PRIMES_AND_VACANCY_READOUTS']},
        'K': {'result_refs': ['SIGNED_K']},
        'ALPHA': {'result_refs': ['ALPHA_TWO_ROUTES'], 'source_ids': ['BODY_ALPHA_DEPENDENCIAS']},
        'ELECTRON': {'result_refs': ['ELECTRON_ACTION'], 'source_ids': ['BODY_ELECTRON_ARTICULACION']},
        'EXCEPCIONAL': {'result_refs': ['EXCEPTIONAL_READOUT'], 'source_ids': ['BODY_INCIDENCIA_ARTICULACION']},
        'COMPARACION': {'role': 'COMPARISON_ONLY_NOT_HMT_GENERATOR',
                       'source_ids': ['BODY_COMPARACION', 'BODY_BIBLIOGRAFIA'],
                       'map': 'After HMT evaluation and dimensional chart, z=(x_HMT-x_ref)/u_ref; '
                              'CODATA values are comparison arguments only, never generator_inputs.',
                       'verified_rounded_z': {'alpha2018': '-0.01473', 'alpha2022': '4.53073',
                                              'electron2018': '4.60001', 'electron2022': '0.00000505'},
                       'limits': 'No igualdad experimental exacta; ajustes no independientes; coincidencias de redondeo distintas.'},
    }
    receipt['conventional_uses'] = []
    for name, role, source_id in [
        ('Lenguaje de realización posterior a los objetos discretos: álgebra lineal, series y cilindros', 'PROOF_LANGUAGE', 'BODY_GENERACION'),
        ('Planck reducido h/(2pi) y cartas dimensionales posteriores a la recta de acción', 'TRANSLATION', 'BODY_ELECTRON'),
        ('Reconocimiento código/diseño/Leech/VOA/FLM/Moonshine en los dominios demostrados', 'RECOGNITION', 'BODY_EXCEPCIONAL'),
        ('CODATA 2018 y 2022, diferencias respecto de incertidumbres tabuladas', 'COMPARISON', 'BODY_COMPARACION'),
        ('Pauli: conferencia Nobel de 13 de diciembre de 1946, contexto histórico sin aprobación retrospectiva', 'TRANSLATION', 'BODY_BIBLIOGRAFIA'),
    ]:
        receipt['conventional_uses'].append({
            'name': name, 'role': role, 'locator': src[source_id],
            'occurs_after_hmt_output': True, 'selects_hmt_state': False,
            'selects_route': False, 'sets_generators': False, 'sets_coefficients': False,
            'target_value_used_as_input': False,
        })
    receipt['proof_layers'] = {
        'finite': ('APP, emisor de dos cursores, identidades de transporte y acarreo, registro y Hadamard, '
                   'jet P9, control electrónico racional y bloque finito excepcional. Las comprobaciones '
                   'reproducidas se distinguen de las entradas HMT heredadas; Decimal reevalúa fórmulas '
                   'posteriores y no ejecuta la genealogía completa de pi/e/phi.'),
        'compatibility': ('Naturalidad del constructor conjunto recibida de sus fuentes completas; '
                          'cilindros regionales y familia E21/22 recibidos de c27/c31; pruebas locales '
                          'de telescopado, truncación y transporte reproducidas donde se indican.'),
        'limit': {
            'required': True,
            'finite_levels': 'Estados de prefijo y terminales finitos; cilindros regionales y truncamientos de lectores por profundidad.',
            'bonding_maps': 'Borrado del último refinamiento, reducción de coeficientes, precomposición de puertos y transporte de marcos.',
            'compatibility_identity': 'u D_(l,Nprime)=D_(k,N) tau; rho I_(n+1)=I_n; '
                                      'las vías A/B se reciben en los mismos cilindros compatibles.',
            'limit_object': 'Terminal inverso conjunto y coordenadas únicas de cilindros de diámetro tendente a cero.',
            'proof': ('La prueba conjunta se hereda de CONTINUUM_OPERATIONS y CONTINUUM_TERMINAL; '
                      'la consecuencia mismos cilindros -> mismo valor está probada en el cuerpo. '
                      'No se acredita aquí una transcripción nueva de cada grado de E21/22.'),
            'status': 'INHERITED_LIMIT_THEOREMS_WITH_EXPLICIT_MANUSCRIPT_RESIDUALS',
        },
        'recognition': ('Nombres convencionales y metrología se aplican después de los objetos HMT; '
                        'ningún reconocimiento fija semilla, ruta, coeficiente o prefijo objetivo.'),
    }
    receipt['provenance'] = 'RESULTADO_RECUPERADO'
    receipt['proof_strength'] = 'DEMOSTRADO_CON_ESTRUCTURA_DE_PARTIDA_EXPLICITA'
    receipt['conclusion_status'] = 'APPLICATION_IN_PROGRESS'
    receipt['residual_if_any'] = {
        'E108_producer_transcription': residual_e108,
        'E21_22_full_reader_transcription': residual_alpha,
        'exceptional_incidence_and_recognition_domains': residual_exceptional,
        'dimensional_and_metrological_boundary': ('La carta de acción/energía es explícita, no impuesta '
                                                'por una coincidencia decimal. No se certifica igualdad '
                                                'experimental exacta ni se ajustan coeficientes a CODATA.'),
    }
    receipt['global_falsifier'] = (
        'Una arista causal invertida desde valores convencionales, una omisión de residuo, cociente, ruta o memoria, '
        'una disgregación del constructor conjunto heredado, una identificación de fase con estado, '
        'la promoción de E108/P9/cartas a productores autónomos no transcritos, mezclar Delta4, '
        'o declarar clausura global o igualdad experimental mediante esta vinculación material.')
    # No quedan valores de sustitución de la plantilla; null sólo expresa vínculo pendiente.
    if 'REEMPLAZAR' in json.dumps(receipt, ensure_ascii=False):
        raise ValueError('Subsiste un valor de plantilla sin especificar')
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bind', action='store_true', help='Vincular al texto final ya extraído; no ejecuta la puerta.')
    parser.add_argument('--artifact', type=Path, default=D / 'TEXTO_ARTICULO.txt')
    parser.add_argument('--check-plan', action='store_true', help='Construir y comprobar localizadores sin escribir.')
    args = parser.parse_args()
    artifact = args.artifact.expanduser().resolve()
    if args.bind and not artifact.is_file():
        parser.error('No existe el texto final; no se inventará una huella.')
    receipt = prepare(args.bind, artifact)
    if not args.check_plan:
        OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': receipt['binding_status'], 'receipt': str(OUT),
                      'scope_kind': receipt['scope_kind'], 'conclusion_status': receipt['conclusion_status'],
                      'source_count': len(receipt['source_manifest']),
                      'result_map_count': len(receipt['result_maps']),
                      'artifact_sha256': receipt['artifact']['sha256'],
                      'written': not args.check_plan, 'gate_executed': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
