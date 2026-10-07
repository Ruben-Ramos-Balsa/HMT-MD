#!/usr/bin/env python3
"""Bind the recovered genealogy to the direct generated-record theorem."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / 'PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def locator(path):
    return dict(path=str(path), sha256=digest(path),
                lines='1-' + str(len(path.read_text().splitlines())))


def main():
    source = ROOT / 'deltas/integracion/GeneratedTransitionRecords.lean'
    frontier = ROOT / 'deltas/integracion/JointRegionalFrontier.lean'
    readme = ROOT / 'README.md'
    receipt = json.loads((HERE / 'RECIBO_REGISTROS_GENEALOGICO.json').read_text())
    old_scope = receipt['scope_note']
    scope = ('Lectura directa de las publicaciones regionales a profundidad arbitraria y '
             'construcción de cuatro registros y dos elevaciones únicas. La genealogía '
             'APP–TRIT–TPK y el continuo conjunto se conservan como antecedentes; este '
             'recibo no recertifica todas sus fibras ni identifica recordGenerated con nueve U.')
    rid = 'GENERATED_TRANSITION_RECORDS_20260919'
    statement = ('Los registros se construyen con bloques de la publicación regional a '
                 'profundidad time+1; coinciden con las lecturas finitas y determinan '
                 'un único par de elevaciones ternarias bajo sus ecuaciones de transición.')
    receipt['receipt_id'] = rid
    receipt['artifact'] = dict(**locator(readme), kind='MODULE', anchors=[
        dict(stage='APP', text='APP →'), dict(stage='TRIT', text='TRIT →'),
        dict(stage='TPK', text='TPK →'),
        dict(stage='ESTADO_ENRIQUECIDO', text='estado\nenriquecido →'),
        dict(stage='ESTRUCTURA_DISCRETA_CONTINUO', text='estructura discreta conjunta'),
        dict(stage='HMT_OUTPUT', text='## Lo que se incorpora'),
        dict(stage='CONVENTIONAL', text='Se requiere Python 3, Lean 4.21.0')])
    receipt['foundation']['inheritance_boundary'] = scope
    receipt['target'].update(statement=statement, result_id=rid,
        causal_cutoff_reason=scope,
        actual_lean_domain='Productor regional racional ya formalizado; profundidad natural arbitraria; palabras y matrices ternarias.',
        closure_criterion='Once teoremas comprobados para el constructor directo y sus dos elevaciones; dependencia de los lectores regionales heredados explícita.')
    result = receipt['result_maps'][0]
    result.update(id=rid, statement=statement, output_object=rid,
        map='publish → blockGenerated → bandsGenerated → wordGenerated → recordGenerated → solveMatrix',
        proof_locator=locator(source), scope=scope,
        premises=['Productor regional y búsqueda por cotas racionales heredados.',
                  'Orden de tres canales y pares time/time+1 conservado.',
                  'Unicidad entre matrices ternarias bajo las ecuaciones de transición.'])
    receipt['conventional_uses'][0]['locator'] = locator(source)
    receipt['proof_layers'].update(
        finite='Cuatro registros evaluados; comparación con los anteriores y dos elevaciones únicas.',
        compatibility='Cada bloque procede de publish a profundidad arbitraria. La igualdad con los 600 trits sólo se usa como teorema de comparación.',
        limit=dict(required=False, reason='El resultado focal recupera cuatro registros; la prolongación y compatibilidad arbitrarias se importan de JointRegionalFrontier y RegionalPublicationComposition.',
                   typing_falsifier='Usar600trits como entrada estructural o afirmar identidad9U sin una prueba de todas las fibras.'))
    record = receipt['effective_result_record']
    record['3_tpk_operator_domain_codomain_action'] = scope + ' La acción comprobada es publish→bloque→banda→registro→elevación.'
    record['4_coefficient_origin'] = 'Bases3 y729=3^6; seis residuos por palabra y tres canales regionales. time0,1,2,3 son las lecturas que se comparan con los registros publicados. No hay entradasX/Y/L ni600trits en recordGenerated.'
    record['5_conservation'] = 'Se conservan canal, orden de tiempos y seis residuos. JointRegionalFrontier conserva firma y acarreo para toda profundidad; el presente resultado focal conserva la igualdad de los registros con esas palabras.'
    record['6_enriched_state_and_continuum_residence'] = scope
    record['7_hmt_output_before_recognition'] = statement
    record['8_posterior_recognition_and_falsifier'] = 'La igualdad con los registros publicados se prueba después de construirlos. El control semántico es documental; las once pruebas Lean y sus imports tienen su recibo independiente.'
    record['9_material_owners'] = [locator(source), locator(frontier)] + record['9_material_owners']
    receipt['scope_note'] = scope
    receipt['local_proof_owners'] = [locator(source), locator(frontier)] + receipt['local_proof_owners']
    receipt['lean_build_receipt'] = locator(HERE / 'mixed_enriched_delta_build/VERIFICATION.json')
    receipt['producer_dependency_audit']['scope_note'] = 'Esta auditoría conservada corresponde a los cuatro constructores regionales anteriores; no se presenta como una nueva ejecución sobre recordGenerated.'
    receipt['provenance_details'] = 'Formalización reunida del constructor directo desde publicaciones ya existentes, sin atribuir prioridad nueva a la arquitectura autoral.'
    receipt['previous_scope_preserved'] = old_scope
    output = HERE / 'RECIBO_GENERATED_RECORDS_GENEALOGICO.json'
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    command = [sys.executable, '-I', '-S',
        str(HERE.parents[1] / 'tools/verificar_genealogia_unica_hmt.py'), '--receipt', str(output)]
    p = subprocess.run(command, text=True, capture_output=True)
    result = dict(exit_code=p.returncode, command=command, output=p.stdout + p.stderr,
                  artifact_sha256=digest(readme), receipt_sha256=digest(output),
                  metadata_not_a_mathematical_proof=True)
    (HERE / 'GENERATED_RECORDS_GENEALOGY_CHECK.json').write_text(json.dumps(result, indent=2) + '\n')
    print(p.stdout + p.stderr)
    return p.returncode


if __name__ == '__main__':
    sys.exit(main())
