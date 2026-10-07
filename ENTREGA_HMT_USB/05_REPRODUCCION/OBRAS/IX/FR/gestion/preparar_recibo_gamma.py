#!/usr/bin/env python3
"""Registra el delta gamma con contexto heredado y alcance local explícito."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]


def loc(path):
    return {'path':str(path), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'lines':'1-'+str(len(path.read_text().splitlines()))}


def main():
    inherited = ROOT/'gestion/recibo_partes_finitas/RECIBO_GENEALOGIA_PARTES_FINITAS.json'
    r = json.loads(inherited.read_text())
    source = ROOT/'manuscrito/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.md'
    producer = ROOT/'fuente/pruebas/python/verificar_gram_nueve_ventanas.py'
    previous = copy.deepcopy(r['result_maps'][0])
    target = 'VIII_GAMMA_CONNECTOR_NINE_INTERVAL_COERCIVITY_AND_FIXED_WINDOW_DETAILS'
    statement = ('Sobre los modos y pesos primo-potencia ya publicados, la cola gamma tiene inversa izquierda; '
                 'C_R=J_- L_R es acotado y satisface C_R J_+=J_- para cada ventana finita. '
                 'La norma explícita prueba contractividad basal. La forma completa tiene el núcleo '
                 'de intervalos trasladados de la proposición16; su Gram de nueve ventanas declaradas '
                 'es estrictamente positivo. El ensamblaje de nueve intervalos de anchura 1/1000 '
                 'es coercivo para cada funcion del dominio y cada refinamiento interno; '
                 'en cualquier ventana fijada los detalles de media nula tienen un umbral '
                 'explicito de coercividad y el indice negativo es finito. '
                 'No se afirma contractividad global ni RH.')
    falsifier = ('Borrar los cruces entre rutas, usar sólo el signo del vector uniforme, omitir la cola '
                 'gamma o un reloj primo-potencia pertinente, confundir el dominio basal con todas las '
                 'ventanas, o importar cifras objetivo para obtener el signo.')
    purpose = ('Delta de resultados recuperados, formalizacion analitica reunida y evaluación posterior finita. El núcleo y el continuo '
               'se heredan del recibo previo, no se demuestran globalmente mediante este cálculo. '
               'No certifica autonomía científica completa del VIII ni autoriza compilar una prueba de RH.')
    r.update(receipt_id=target, receipt_purpose=purpose, normative_context_semantics=purpose,
             provenance='RESULTADO_RECUPERADO', global_falsifier=falsifier,
             whole_article_closed=False, pdf_compilation_authorized_by_this_receipt=False)
    r['target'].update(statement=statement, result_id=target,
        domain='PublishedPositiveIntegerModes', codomain='FiniteWindowGammaConnectorsAndGram',
        closure_criterion='Resultados12–24, dominios declarados, pruebas operatorias y certificados intervalares de nueve ventanas e intervalos.',
        forbidden_generator_inputs=['TARGET_WEIL_SIGN','RIEMANN_ZEROS','EXTERNAL_PRIME_SELECTION'])
    result = {'id':target,'statement':statement,'input_object':'native_positive_modes',
        'domain':'PublishedPositiveIntegerModes','codomain':'FiniteWindowGammaConnectorsAndGram',
        'output_object':'gamma_local_results','source_family':'HMT',
        'generator_inputs':['native_positive_modes'],
        'map':'Pesos publicados -> columnas completas -> cola B_R -> L_R=a_R^-1 B_R* pi_tail -> C_R=J_- L_R; correlación triangular -> Gram completo y resto intervalar.',
        'proof_locator':loc(source),'falsifier':falsifier}
    r['result_maps'] = [previous,result]
    r['source_manifest']['GAMMA_DELTA_PROOF'] = loc(source)
    r['source_manifest']['GAMMA_INTERVAL_CONTROL'] = loc(producer)
    r['source_manifest']['GAMMA_COERCIVITY_CONTROL'] = loc(ROOT/'fuente/pruebas/python/verificar_nueve_intervalos_coercividad.py')
    recovery = json.loads((ROOT/'gestion/MANIFIESTO_RECUPERACION_GAMMA.json').read_text())
    for i,row in enumerate(recovery['source_files']):
        r['source_manifest']['RECOVERED_OWNER_'+str(i)] = loc(ROOT/row['copy'])
    r['source_manifest']['PI_INTERNAL_PUBLICATION'] = loc(ROOT/'antecedentes/nonadica/pi_1000_decimales.txt')
    r['conventional_uses'] = [{'name':'Formas de Hilbert, convolución, criterio de Schur y aritmética intervalar',
        'role':'PROOF_LANGUAGE','locator':loc(source),'occurs_after_hmt_output':True,
        'selects_hmt_state':False,'selects_route':False,'sets_generators':False,
        'sets_coefficients':False,'target_value_used_as_input':False,
        'scope_note':'Se analizan lectores sobre modos previamente publicados; las nueve ventanas son pruebas declaradas, no un selector del TPK.'}]
    r['proof_layers'] = {'finite':'Adjuntos y pliegue con Fraction; Gram completo de nueve pruebas con colas intervalares; margen uniforme de interacciones.',
        'compatibility':'F_(q+1)=F_q A_q; Gram_padre=V* Gram_hijos V, conservando cruces; Gram_n y Schur_n >= eta I sobre la union de nueve intervalos.',
        'limit':{'required':True,'statement':'La serie gamma converge con resto explícito y las regularizaciones convergen en la norma conjunta de los lectores.',
            'proof_locator':loc(source),'formula':'0<=F(x)-F_N(x)<=exp(-lambda_N*x)*(lambda_N^-2+(2*lambda_N)^-1)',
            'finite_levels':'Sumas gamma de N términos sobre cada uno de los nueve desplazamientos; regularizaciones de indicadores en ventana fija.',
            'bonding_maps':'Añadir términos gamma y restar su contribución de la cola; regularizar por convolución con una identidad aproximada.',
            'compatibility_identity':'F_N+tail_N=F_(N+1)+tail_(N+1); D_Gamma(rho_delta*b)=rho_delta*(D_Gamma b).',
            'limit_object':'Lectores acotados de cola; coercividad de la forma en la union de nueve intervalos y de sus refinamientos; detalles de media nula en ventana fija; no un certificado cofinal de signo.',
            'proof':'Monotonía de los sumandos e integral de (2u+1/2)^-2 acotan la cola; en norma gamma se domina por 4 sigma_Gamma |b_hat|^2 integrable. Los canales restantes son acotados en la ventana fija.'},
        'recognition':'La prueba compara los lectores completados; no presupone el signo de Weil para toda función.'}
    out = ROOT/'gestion/recibo_gamma'
    out.mkdir(exist_ok=True)
    parts, anchors = [],[]
    for stage in r['stages']:
        anchor = 'RESIDENCIA HEREDADA '+stage['id']
        anchors.append({'stage':stage['id'],'text':anchor})
        parts.extend([anchor,Path(stage['owner']['path']).read_text()])
    for stage,path in [('HMT_OUTPUT',ROOT/'manuscrito/01_CONSTRUCCION_ARITMETICA.md'),('CONVENTIONAL',source)]:
        anchor = 'RESIDENCIA FOCAL '+stage
        anchors.append({'stage':stage,'text':anchor})
        parts.extend([anchor,path.read_text()])
    composite = out/'FUENTE_COMPUESTA.txt'
    composite.write_text('\n\n'.join(parts))
    r['artifact'] = {'path':str(composite),'sha256':loc(composite)['sha256'],'kind':'MODULE','anchors':anchors,
                    'binding_note':'Instantánea de herencia y delta; no es un PDF cerrado ni una nueva prueba global.'}
    fields = r['genealogical_nine_fields']
    fields['4_coefficient_origins'] = ('Pesos log(p)/sqrt(p^k) desde irreducibles y producto nativos; mu desde la forma completada previa. '
        'c_Gamma usa pi publicado por la conexión nonádica y gamma del productor racional de capítulo04. '
        'epsilon=1/100,N=1024 y nueve traslaciones j log2 fijan el dominio de un control; epsilon=1/1000 fija el dominio del ensamblaje funcional. N=floor(1/h) fija la cota analitica de detalles. No fijan un valor objetivo.')
    fields['5_information_preservation'] = 'Cola con ambas orientaciones, filas primas completas, polar y gamma, productos cruzados completos y residuos de refinamiento; la evaluación no reconstruye la historia TPK íntegra.'
    fields['7_hmt_output_before_realization'] = previous
    fields['8_posterior_realization_and_falsifier'] = {'realization':result,'falsifier':falsifier}
    fields['9_material_owners'] = r['source_manifest']
    path = out/'RECIBO_GENEALOGIA_GAMMA.json'
    path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    run = subprocess.run([sys.executable,'-I','-S',str(PROJECT/'tools/verificar_genealogia_unica_hmt.py'),'--receipt',str(path)],capture_output=True,text=True)
    (out/'RESULTADO_VALIDACION.txt').write_text(run.stdout+run.stderr)
    print(run.stdout+run.stderr)
    if run.returncode:
        raise SystemExit(run.returncode)
    c = json.loads((ROOT/'gestion/recibo_partes_finitas/RECIBO_CONSTANTES_04.json').read_text())
    c.update(artifact=str(source),local_artifact_sha256=loc(source)['sha256'],result_id=target,
             focal_genealogical_receipt=loc(path),control_scope=purpose,
             local_results=[{'causal_role':'POST_PUBLICATION_READER_OR_LOCAL_IDENTITY',
               'proof_owner':loc(source),'whole_article_closed':False,
               'global_weil_positivity_certified':False,'target_values_used_as_inputs':False}])
    c['genealogy']['source_locators'] += [str(source),str(producer),str(ROOT/'antecedentes/nonadica/pi_1000_decimales.txt')]
    cp = out/'RECIBO_CONSTANTES_GAMMA.json'
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    gate = Path('/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py')
    check = subprocess.run([sys.executable,'-I','-S',str(gate),'--audit',str(source),'--receipt',str(cp)],capture_output=True,text=True)
    (out/'RESULTADO_CONSTANTES.txt').write_text(check.stdout+check.stderr)
    print(check.stdout+check.stderr)
    if check.returncode:
        raise SystemExit(check.returncode)


if __name__ == '__main__':
    main()
