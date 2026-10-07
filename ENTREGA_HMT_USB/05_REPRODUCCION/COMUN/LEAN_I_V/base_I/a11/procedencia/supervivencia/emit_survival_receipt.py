#!/usr/bin/env python3
"""Document the local theorem scope; this metadata is not a Lean proof."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def locator(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'lines': '1-' + str(len(path.read_text().splitlines()))}


def main():
    checked = HERE / 'survival_chain_build/VERIFICATION.json'
    build = json.loads(checked.read_text())
    if build['status'] != 'PASS_CONNECTED_SURVIVAL_CHAIN':
        raise RuntimeError('The connected proof must compile first')
    r = json.loads((HERE / 'RECIBO_GENERATED_RECORDS_GENEALOGICO.json').read_text())
    statement = ('La supervivencia cilíndrica selecciona una única historia regional; '
                 'sus registros determinan las elevaciones y su firma. La trayectoria '
                 'residual posterior a R36 satisface ese criterio sin añadir compatibilidad como premisa.')
    scope = ('Se componen los lectores regionales internos, las desigualdades de cilindros, '
             'la selección por supervivencia y la realización residual posterior a R36. '
             'No se identifica por ello la composición histórica de nueve actualizaciones '
             'pre-R36 sobre todas las fibras enriquecidas, ni se certifica el artículo íntegro.')
    rid = 'CONNECTED_SURVIVAL_CHAIN_20260919'
    owners = [locator(Path(m['source'])) for m in build['modules']]
    readme = HERE / 'README_SUPERVIVENCIA_INTEGRADA.md'
    r['receipt_id'] = rid
    r['artifact'] = dict(**locator(readme), kind='MODULE', anchors=[
        {'stage': 'APP', 'text': 'APP →'}, {'stage': 'TRIT', 'text': 'TRIT →'},
        {'stage': 'TPK', 'text': 'TPK →'},
        {'stage': 'ESTADO_ENRIQUECIDO', 'text': 'estado enriquecido →'},
        {'stage': 'ESTRUCTURA_DISCRETA_CONTINUO', 'text': 'estructura discreta conjunta'},
        {'stage': 'HMT_OUTPUT', 'text': '## Cadena comprobada'},
        {'stage': 'CONVENTIONAL', 'text': 'Se requiere Python 3, Lean 4.21.0'}])
    r['foundation']['inheritance_boundary'] = scope
    r['target'].update(statement=statement, result_id=rid,
        domain='Estructura discreta conjunta con sus lectores finitos de incidencia',
        codomain='Historia superviviente única, registros, elevaciones y firma',
        causal_cutoff_reason=scope,
        actual_lean_domain='Tres canales internos y prefijos en bases729 y1000; estados residuales reales en [0,1).',
        closure_criterion='Compilación conjunta de los seis módulos y examen de sus 48 consultas de axiomas.')
    r['result_maps'][0].update(id=rid, statement=statement, output_object=rid,
        domain=r['target']['domain'], codomain=r['target']['codomain'],
        map='desigualdades cilíndricas → supervivencia → historia única → registros/elevaciones/firma; recurrencia residual → compatibilidad → supervivencia',
        proof_locator=owners[2], scope=scope,
        premises=['Productores regionales internos y separación de fronteras ya formalizados.',
                  'Supervivencia definida por solapamiento; el caso cofinal declara la cofinalidad.',
                  'La trayectoria residual parte de la coordenada real regional a profundidad seis.'])
    r['conventional_uses'][0]['locator'] = owners[2]
    r['proof_layers'].update(
        finite='Los registros finitos y sus elevaciones se obtienen de la historia superviviente.',
        compatibility='Truncación decimal, supervivencia a toda profundidad y observación cofinal.',
        limit={'required': False,
               'reason': 'Cuantificación sobre todas las profundidades naturales; no se añade un nuevo paso al límite topológico al productor regional heredado.',
               'typing_falsifier': 'Sustituir la supervivencia por igualdad al bloque objetivo.'})
    e = r['effective_result_record']
    e['3_tpk_operator_domain_codomain_action'] = scope
    e['4_coefficient_origin'] = 'Bases729=3^6 y1000 ya presentes en los cilindros; profundidad seis corresponde aR36. No se importan tablasX/Y/L como datos generadores.'
    e['5_conservation'] = 'Prefijos por recurrencia y truncación, canales y firma común; la recurrencia conserva el balance N+epsilon bajo multiplicación por729.'
    e['6_enriched_state_and_continuum_residence'] = scope
    e['7_hmt_output_before_recognition'] = statement
    e['8_posterior_recognition_and_falsifier'] = 'Una historia discrepante tiene rechazo finito demostrado. Este recibo documental no sustituye las pruebas Lean compiladas.'
    e['9_material_owners'] = owners
    r['scope_note'] = scope
    r['outside_local_statement'] = 'Identidad pre-R36 con nueve pasos completos y cierre global de FLM/Moonshine.'
    r['local_proof_owners'] = owners
    r['lean_build_receipt'] = locator(checked)
    r['provenance_details'] = 'CERTIFICADO_NUEVO de supervivencia y composición de la arquitectura autoral preexistente; los módulos residuales son aportación coordinada del revisor.'
    r['producer_dependency_audit']['scope_note'] = 'Conservado sólo como antecedente de los lectores; no es auditoría nueva de los seis módulos.'
    r['previous_scope_preserved'] = 'Paquete251 intacto; esta incorporación no modifica ninguna fuente niPDF anterior.'
    dest = HERE / 'RECIBO_SUPERVIVENCIA_GENEALOGICO.json'
    dest.write_text(json.dumps(r, ensure_ascii=False, indent=2) + '\n')
    command = [sys.executable, '-I', '-S', str(HERE.parents[1] / 'tools/verificar_genealogia_unica_hmt.py'),
               '--receipt', str(dest)]
    p = subprocess.run(command, text=True, capture_output=True)
    (HERE / 'SURVIVAL_GENEALOGY_CHECK.json').write_text(json.dumps({
        'exit_code': p.returncode, 'command': command, 'output': p.stdout+p.stderr,
        'receipt': locator(dest), 'metadata_not_a_mathematical_proof': True}, ensure_ascii=False, indent=2)+'\n')
    print(p.stdout+p.stderr)
    if p.returncode:
        return p.returncode
    base = HERE.parent / 'PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919'
    causal = json.loads((base / 'recibos/integracion/RECIBO_CAUSAL.json').read_text())
    causal.update(artifact=str(readme), artifact_sha256=locator(readme)['sha256'],
                  result_id=rid, scope=scope, mathematical_result=statement)
    causal['genealogy']['tpk'].update(
        operator='Criterio de supervivencia cilíndrica y recurrencia residual posterior aR36',
        domain='Lectores regionales internos, historias de bloques y residuos',
        codomain='Historia superviviente, registros, elevaciones y firma',
        action=statement)
    causal['genealogy']['source_locators'] += [x['path'] for x in owners]
    causal['genealogical_result_record'].update(e)
    causal['formalization_scope'] = dict(whole_pdf=False,
        full_U_nine_step_identification=False, full_FLM_Moonshine=False,
        local_claim=statement, allowed_new_axioms=[])
    causal_path = HERE / 'RECIBO_SUPERVIVENCIA_CAUSAL.json'
    causal_path.write_text(json.dumps(causal, ensure_ascii=False, indent=2)+'\n')
    command = [sys.executable, '-I', '-S',
        '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit', str(readme), '--receipt', str(causal_path)]
    p = subprocess.run(command, text=True, capture_output=True)
    (HERE / 'SUPERVIVENCIA_CAUSAL_CHECK.json').write_text(json.dumps({
        'exit_code': p.returncode, 'command': command, 'output': p.stdout+p.stderr,
        'receipt': locator(causal_path), 'metadata_not_a_mathematical_proof': True}, ensure_ascii=False, indent=2)+'\n')
    print(p.stdout+p.stderr)
    return p.returncode


if __name__ == '__main__':
    raise SystemExit(main())
