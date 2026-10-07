#!/usr/bin/env python3
"""Focal documentary metadata from two already executed Article II receipts."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
PREVIOUS=PROJECT/'output/ARTICLE_I_PUBLICACION_PRINCIPAL_20260922/metadata'
OUT=HERE/'metadata'
RESULT='II_SELECTED_ACTION_GRAVITY_THERMAL_AND_CKM'
SUMMARY=('Composición documental de dos consumidores comprobados sobre el mismo '
    'SelectedActionDomain: acción seleccionada, selector circular y transductor '
    'térmico con bases positivas explícitas; y publicación CKM sobre las reglas '
    'sectoriales declaradas, con recuperación, unitariedad, Jarlskog positivo y '
    'transporte espectral/conmutador. No se introduce Ledger fabricado ni '
    'PublishedRegister como hipótesis y no se afirma un teorema Lean conjunto adicional.')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def loc(path):
    path=Path(path).resolve()
    return dict(path=str(path),sha256=sha(path),lines=f'1-{len(path.read_text().splitlines())}')


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    if OUT.exists():
        raise RuntimeError('Require fresh metadata directory')
    artifact=HERE/'METADATA_ALCANCE.md'
    a_source=HERE/'SelectedActionGravityThermal.lean'
    c_source=HERE/'SelectedCKMPublication.lean'
    a_path=HERE/'verification_action_gravity_thermal/VERIFICATION.json'
    c_path=HERE/'CKM_VERIFICATION.json'
    a=json.loads(a_path.read_text()); c=json.loads(c_path.read_text())
    assert a['status']=='PASS_SELECTED_ACTION_GRAVITY_THERMAL' and a['exit_code']==0
    assert a['source_sha256']==sha(a_source)
    assert a['hypotheses']==['U > 0','c > 0','t0 > 0','Theta > 0']
    assert c['status']=='PASS_SELECTED_CKM_PUBLICATION'
    assert c['fabricated_ledger'] is False and c['PublishedRegister_assumed'] is False
    row=next(r for r in c['modules'] if r['module']=='SelectedCKMPublication')
    assert row['source_sha256']==sha(c_source) and row['exit_code']==0
    assert len(c['declarations'])==3
    gene_path=PREVIOUS/'RECIBO_GENEALOGICO.json'
    gene=json.loads(gene_path.read_text())
    causal=json.loads((PREVIOUS/'CAUSAL.json').read_text())
    old_target=copy.deepcopy(gene['target'])
    old_contract=copy.deepcopy(gene['documentary_contract_continuity'])
    antecedent=next(r for r in gene['result_maps'] if r['id']==old_target['result_id'])
    groups=[
        ('II_SELECTED_ACTION_GRAVITY_THERMAL',a_source,a_path,
         [a['terminal'],'HMT.II.SelectedActionGravityThermal.thermalCoefficient_pos'],
         'U,c,t0,Theta reales estrictamente positivos; ActionChart pre/ret y coordenadas seleccionadas de I.',
         'Década −34, selector circular único, transductor positivo único, balance del ciclo, invariante areal y retorno recíproco.',
         'Aplicar action_decimal_order al registro seleccionado, conservar sectionAction, construir frequency/radius/cycleEnergy y deducir por identidades algebraicas la caracterización circular y térmica con sus hipótesis.'),
        ('II_SELECTED_CKM',c_source,c_path,[d[0] for d in c['declarations']],
         'Coordenadas angulares seleccionadas y reglas sectoriales declaradas; masas y refases unitarios posteriores; separación espectral no nula sólo para la conclusión de no anulación.',
         'Lector recuperable, matriz CKM unitaria, Jarlskog positivo, obstrucción de refase real, transporte hermítico/espectral y determinante de conmutador.',
         'Evaluar chart y sectorRules sobre direct/conjugate/torsion seleccionados; probar intervalos angulares, reutilizar las identidades unitarias y espectrales sobre esa matriz, sin recibir PublishedRegister ni fabricar Ledger.')]
    maps=[]
    for rid,source,receipt,declarations,domain,codomain,operation in groups:
        maps.append(dict(id=rid,statement=operation,
            input_object=antecedent['output_object'],domain=antecedent['codomain'],
            actual_lean_domain=domain,
            input_projection='El arco documental identifica el contexto común; el tipo concreto queda declarado en actual_lean_domain y en la fuente Lean.',
            codomain=codomain,output_object=rid,map=operation,
            generator_inputs=[antecedent['output_object']],source_family='HMT',
            proof_locator=loc(source),lean_declarations=declarations,
            verification_receipts=[loc(receipt)],causal_role='POSTERIOR_REALIZATION_ON_SELECTED_REGIONAL_ACTION',
            provenance='CERTIFICADO_NUEVO',
            falsifier='Ocultar hipótesis dimensionales o sectoriales, introducir objetivos externos o publicar una conclusión más fuerte que la declaración compilada.'))
    joint=copy.deepcopy(maps[0])
    joint.update(id=RESULT,statement=SUMMARY,output_object=RESULT,codomain=SUMMARY,
        map='Reunir documentalmente los dos consumidores sobre SelectedActionDomain sin inferir una nueva equivalencia entre ellos.',
        generator_inputs=[m['id'] for m in maps],aggregate_of_result_maps=[m['id'] for m in maps],
        independent_joint_lean_theorem_claimed=False,
        additional_proofs=[loc(c_source)],
        lean_declarations=[n for m in maps for n in m['lean_declarations']],
        verification_receipts=[loc(a_path),loc(c_path)])
    gene['result_maps']+=maps+[joint]
    gene['receipt_id']='II_CENTRAL_CONSUMIDORES_SELECCIONADOS_20260922'
    gene['artifact']=dict(**loc(artifact),kind='MODULE',anchors=[dict(stage=s,text=t) for s,t in [
        ('APP','APP →'),('TRIT','TRIT →'),('TPK','TPK →'),
        ('ESTADO_ENRIQUECIDO','estado enriquecido →'),
        ('ESTRUCTURA_DISCRETA_CONTINUO','estructura discreta conjunta del continuo'),
        ('HMT_OUTPUT','publicaciones internas'),('CONVENTIONAL','reconocimiento convencional posterior')]])
    gene['target'].update(statement=SUMMARY,result_id=RESULT,domain=antecedent['codomain'],
        codomain=SUMMARY,actual_lean_domain='; '.join(g[4] for g in groups),
        closure_criterion='Dos recibos Lean ejecutados con fuentes autenticadas; reunión documental sin nuevo teorema agregado.',
        causal_cutoff_reason='La acción/regiones de I alimentan downstream los consumidores de II.',
        forbidden_generator_inputs=['FABRICATED_LEDGER','PublishedRegister_AS_INPUT','CODATA','TARGET_CKM_ANGLES'])
    exclusions=['Selección numérica SI de U,c,t0,Theta no demostrada por estos consumidores',
        'Unicidad de representación CKM más allá de las reglas sectoriales declaradas',
        'Derivación de masas espectrales usadas como parámetros posteriores',
        'Certificación global del corpus o modificación del FAIL histórico de AGENTS.md']
    focal=copy.deepcopy(gene['focal_genealogical_receipt'])
    focal.update({
        '1_app_object_domain_sheets_operation':'Se conserva el soporte y las lecturas regionales de I; el selector central no se sustituye por un Ledger reconstruido a partir de una salida.',
        '2_trit_state_regime_orientation':'Se conservan las orientaciones y datos tríticos heredados. La realización térmica emplea log 3; el lector CKM conserva el alfabeto trítico de cardinal tres y su representación sectorial declarada.',
        '3_tpk_effective_composition':'SelectedActionDomain recibe las coordenadas ya seleccionadas. Las secciones anterior/retorno de la acción alimentan el ciclo, radio y transductor; las coordenadas angulares alimentan el lector sectorial recuperable y luego la matriz CKM. No se presenta la realización matricial convencional como selector TPK.',
        '4_coefficient_origins':'La década −34 procede de action_decimal_order. El ciclo 108 y la fase 2π dan frecuencia 2π/(108 t0), radio (54/π)c t0 y selector circular (54/π)^2. El transductor divide la energía por Theta log3. Los coeficientes CKM pertenecen a las reglas sectoriales declaradas y se conservan, sin convertir valores físicos objetivo en generadores.',
        '5_conserved_information':'Mismo registro regional y acción seleccionada; retorno de acción y temperatura, balances del ciclo, marca/hexada/alfabeto de cardinales4/6/3, recuperación angular, espectro bajo transporte y orientación del invariante de Jarlskog. U,c,t0,Theta positivos permanecen explícitos; los parámetros de masa y refase aparecen sólo downstream.',
        '6_enriched_state_and_residence':'Los consumidores se especializan al mismo SelectedActionDomain heredado de I; no crean otro estado, registro o selección. Su realización posterior conserva el origen declarado sin afirmar una nueva reconstrucción completa de la historia.',
        '7_produced_output':SUMMARY,
        '8_posterior_recognition_and_falsifier':'Matriz unitaria CKM, espectro y conmutador son realizaciones posteriores. No se promueven masas, refases o valores SI a entradas de la selección. Falsadores: borrar positividad, cambiar Gm/c² por otro radio, omitir las reglas sectoriales, afirmar no anulación sin separaciones espectrales o declarar un PASS global documental.',
        '9_material_owners':[str(a_source),str(c_source),str(a_path),str(c_path),str(gene_path)]})
    gene['focal_genealogical_receipt']=focal
    gene['scope_note']=SUMMARY+' Los gates documentales no sustituyen Lean.'
    gene['scope_exclusions']='; '.join(exclusions)
    gene['later_operations_not_claimed']=exclusions
    gene['previous_receipt_context']=dict(receipt=loc(gene_path),target=old_target,
        scope='Artículo I inalterado, contexto heredado reutilizado sin reauditoría.')
    gene['lean_build_receipt']=loc(a_path)
    gene['integrated_lean_evidence']=dict(receipts={'action_gravity_thermal':loc(a_path),'ckm':loc(c_path)},
        focal_modules=['SelectedActionGravityThermal','SelectedCKMPublication'],
        ckm_dependency_modules=[r['module'] for r in c['modules']],
        focal_declaration_count=5,
        inherited_axioms=['propext','Classical.choice','Quot.sound','Lean.ofReduceBool'],
        evidence_role='Recibos de ejecución existente autenticados; este generador documental no compila Lean.')
    gene['proof_layers'].update(finite='Cálculos exactos de las reglas y matrices, con las cotas angulares demostradas.',
        compatibility='Especialización común al SelectedActionDomain heredado; hipótesis dimensionales y representación sectorial conservadas.',
        recognition='Realización circular/térmica y matricial/espectral posterior; no se usa metrología para escoger el generador.')
    gene['proof_layers']['limit']=dict(required=False,reason='Delta focal sin paso al límite nuevo.',
        typing_falsifier='Promover este control focal a nueva prueba de la coinducción completa.')
    gene['global_falsifier']=focal['8_posterior_recognition_and_falsifier']
    gene['successor_documentation']=dict(generator=loc(__file__),predecessor=loc(gene_path),
        delta=SUMMARY,preservation='No se edita I, el corpus, los skills ni recibos sellados.')
    gene['delivery_status']=dict(documentary_gates_run=False,
        packaging_executed_by_this_receipt=False,lean_compilation_executed_by_this_script=False)
    assert gene['documentary_contract_continuity']==old_contract
    causal.update(artifact=str(artifact),artifact_sha256=sha(artifact),result_id=RESULT,
        genealogy_v4_source=loc(gene_path),focal_genealogical_receipt=focal,
        compiled_modules=len(c['modules'])+1,
        added_source_modules=['SelectedActionGravityThermal','SelectedCKMPublication'],
        public_declarations=5,verification_receipt=str(a_path),verification_receipt_sha256=sha(a_path),
        verification_receipts=gene['integrated_lean_evidence']['receipts'],
        successor_documentation=gene['successor_documentation'])
    causal.pop('authenticated_predecessor_modules',None)
    causal.pop('reused_authenticated_modules',None)
    causal['formalization_scope']=dict(new_result=SUMMARY,not_claimed=exclusions,
        positive_dimensional_parameters=['U','c','t0','Theta'],
        declared_sector_representation_preserved=True,
        later_spectral_masses_and_unit_rephasings=True,
        fabricated_ledger=False,PublishedRegister_assumed=False,
        independent_joint_lean_theorem_claimed=False,
        selected_specialization_inherits=['Lean.ofReduceBool'])
    causal['posterior_realization']=dict(operator=RESULT,action=SUMMARY,
        owners=[str(a_source),str(c_source)],source_hashes={p.name:sha(p) for p in [a_source,c_source]})
    OUT.mkdir()
    write(OUT/'RECIBO_GENEALOGICO.json',gene)
    write(OUT/'CAUSAL.json',causal)
    checks=[
        ('CONTROL_GENEALOGIA.json',[sys.executable,'-I','-S',str(PROJECT/'tools/verificar_genealogia_unica_hmt.py'),'--receipt',str(OUT/'RECIBO_GENEALOGICO.json')],'PASS_GENEALOGIA_UNICA_APP_TRIT_TPK'),
        ('CONTROL_CAUSAL.json',[sys.executable,'-I','-S','/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py','--audit',str(artifact),'--receipt',str(OUT/'CAUSAL.json')],'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY')]
    failed=False
    for name,command,expected in checks:
        done=subprocess.run(command,capture_output=True,text=True)
        ok=done.returncode==0 and expected in done.stdout
        write(OUT/name,dict(command=command,exit_code=done.returncode,stdout=done.stdout,
                           stderr=done.stderr,expected=expected,passed=ok))
        print(name,done.stdout.strip(),done.stderr.strip())
        failed |= not ok
    write(OUT/'MANIFIESTO_METADATA.json',dict(generator=loc(__file__),artifact=loc(artifact),
        receipts={'action_gravity_thermal':loc(a_path),'ckm':loc(c_path)},predecessor=loc(gene_path),
        outputs={p.name:sha(p) for p in OUT.iterdir() if p.is_file()},
        gates_executed=True,all_focal_gates_passed=not failed,
        lean_executed_by_this_script=False,global_pass_claimed=False,
        historical_contract_failure_preserved=old_contract))
    if failed:
        raise SystemExit(1)


if __name__=='__main__':
    main()
