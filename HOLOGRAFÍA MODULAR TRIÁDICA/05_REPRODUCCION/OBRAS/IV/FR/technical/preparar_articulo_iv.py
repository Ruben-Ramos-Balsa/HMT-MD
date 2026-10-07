#!/usr/bin/env python3
"""Enlaza el borrador IV a sus fuentes, recibos y controles de alcance.

No modifica los artículos anteriores ni convierte una validación documental
en demostración. Los JSON y la fuente compuesta son derivados reproducibles.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path('/Users/ruben/Documents/New project')
SERIES = PROJECT / 'PUBLICACION_HMT/SERIE_ARTICULOS_HMT'
OLD = PROJECT / 'output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910'
TECH = ROOT / 'technical'
INPUT = re.compile(r'\\(?:input|include)\s*\{([^{}]+)\}')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def loc(path):
    path = Path(path)
    return {'path': str(path), 'sha256': digest(path),
            'lines': f'1-{len(path.read_text().splitlines())}'}


def active_tree():
    paths, active = [], []
    def expand(path):
        path = path.resolve()
        if path in active:
            raise ValueError('Ciclo de inclusiones: ' + str(path))
        if not path.is_relative_to(ROOT):
            raise ValueError('Dependencia externa compilada: ' + str(path))
        active.append(path)
        paths.append(path)
        text = path.read_text()
        def replace(match):
            name = match.group(1)
            target = ROOT / name
            if not target.suffix:
                target = target.with_suffix('.tex')
            return '\n' + expand(target) + '\n'
        result = INPUT.sub(replace, text)
        active.pop()
        return result
    combined = expand(ROOT / 'main.tex')
    return paths, combined


def prepare():
    paths, combined = active_tree()
    literal = re.sub(r'(?<!\\)%[^\n]*', '', combined)
    labels = re.findall(r'\\label\{([^}]+)\}', literal)
    references = set()
    for group in re.findall(r'\\(?:eqref|ref|cref|Cref)\{([^}]+)\}', literal):
        references.update(group.split(','))
    bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', literal))
    cites = set()
    for group in re.findall(r'\\cite\w*(?:\[[^]]*\])?\{([^}]+)\}', literal):
        cites.update(group.split(','))
    errors = []
    if len(labels) != len(set(labels)):
        errors.append('Etiquetas duplicadas: ' + str(sorted(x for x in set(labels) if labels.count(x) > 1)))
    if references - set(labels):
        errors.append('Referencias sin destino: ' + str(sorted(references - set(labels))))
    if cites - bib:
        errors.append('Citas sin entrada: ' + str(sorted(cites - bib)))
    common = read(SERIES / 'NUCLEO_COMUN_20260910/MANIFIESTO.json')
    common_checks = []
    for row in common['files']:
        actual = digest(ROOT / row['path'])
        common_checks.append({'path': row['path'], 'sha256': actual, 'identical': actual == row['sha256']})
        if actual != row['sha256']:
            errors.append('Núcleo alterado: ' + row['path'])
    preserved = []
    for path in paths:
        relative = path.relative_to(ROOT)
        prior = OLD / relative
        if not prior.is_file():
            continue
        current = path.read_text()
        original = prior.read_text()
        if str(relative) == 'sections/registro_k.tex':
            current = current.replace('\\input{sections/registro_incidencias.tex}\n\n', '')
        if relative.name == 'main.tex':
            continue
        same = current == original
        preserved.append({'path': str(relative), 'identical_after_declared_input': same,
                          'source_sha256': digest(prior), 'copy_sha256': digest(path)})
        if not same:
            errors.append('Cambio no declarado en cuerpo heredado: ' + str(relative))
    report = {'status': 'PASS' if not errors else 'FAIL', 'scope': 'Inclusiones, referencias, citas e identidad documental; no certificación matemática global.',
              'source_count': len(paths), 'labels': len(labels), 'reference_targets': len(references),
              'citations': sorted(cites), 'common_kernel': common_checks,
              'preserved_sources': preserved, 'errors': errors,
              'files': [{'path': str(p.relative_to(ROOT)), 'sha256': digest(p)} for p in paths]}
    write(TECH / 'CONTROL_ENSAMBLE.json', report)
    if errors:
        raise ValueError('\n'.join(errors))
    artifact = TECH / 'FUENTE_COMPUESTA.tex.txt'
    artifact.write_text(combined)

    inherited = TECH / '../antecedentes/controles_articulo_I'
    receipt = read(inherited / 'RECIBO_GENEALOGICO_REVISION.json')
    receipt['receipt_id'] = 'ARTICULO_IV_MOONSHINE_DUALIDAD_20260910'
    receipt['receipt_purpose'] = 'Ensamblaje de trabajo de la prolongación excepcional y dimensional; preserva los alcances heredados y explicita las pruebas propias.'
    receipt['artifact'] = {'path': str(artifact), 'sha256': digest(artifact), 'kind': 'MANUSCRIPT', 'anchors': []}
    phrases = [('APP','Evaluación aritmética levantada'), ('TRIT','Firma ternaria y levantamiento local'),
               ('TPK','Actualización del TPK'), ('ESTADO_ENRIQUECIDO','La igualdad de fase y el incremento de memoria son compatibles'),
               ('ESTRUCTURA_DISCRETA_CONTINUO','Desde la estructura discreta conjunta del continuo'),
               ('HMT_OUTPUT','Coordenada alfa de la clausura'), ('CONVENTIONAL','Unicidad con carácter central primitivo fijado')]
    position = 0
    for stage, phrase in phrases:
        match = re.search(r'\s+'.join(map(re.escape, phrase.split())), combined[position:])
        if match is None:
            raise ValueError('Ancla causal no localizada: ' + phrase)
        absolute = position + match.start()
        receipt['artifact']['anchors'].append({'stage': stage, 'text': match.group(), 'line': combined.count('\n', 0, absolute) + 1})
        position += match.end()
    receipt['target'].update({'statement': 'Reunir la cadena APP–TRIT–TPK, K e incidencia excepcional con la realización hilbertiana, dualidad compacta, pantallas y cociclo de acción, conservando las condiciones de realización física.',
                              'result_id': 'IV_ASSEMBLY', 'codomain': 'WorkingManuscriptWithExplicitMapsDomainsAndProofs',
                              'closure_criterion': 'Cierre de las inclusiones documentales y pruebas de los mapas expuestos; no declaración de clausura global de teoría M.'})
    keep = {'REGIONAL_GENERATION','SIGNED_K','ALPHA_TWO_ROUTES','EXCEPTIONAL_READOUT','TRIT_EXPONENTIAL_REALIZATIONS','CAPACITY_VACANCY_TRIT','NATIVE_PRIMES_AND_VACANCY_READOUTS'}
    receipt['result_maps'] = [r for r in receipt['result_maps'] if r['id'] in keep]
    for row in receipt['result_maps']:
        old_path = Path(row['proof_locator']['path'])
        try:
            local = ROOT / old_path.relative_to(OLD)
        except ValueError:
            continue
        if local in paths:
            row['proof_locator'] = loc(local)
    focal = read(TECH / 'REGISTRO_PROCEDENCIA.json')
    formulas = {
      'IV_H1': 'C9,d -> l2(C9,d); Xf(r)=f(r-1), Zf(r)=omega^r f(r); ZX=omega XZ.',
      'IV_H2': 'a -> a tensor I9; tau_(d+1)(a tensor I9)=tau_d(a); UHF and tracial weak closure.',
      'IV_T1': '(m,w,R0)->(w,m,1/R0); E=m²/R0²+w²R0²; UT H(R0) UT^-1=H(1/R0) with domains.',
      'IV_T2': 'L9=Z(9,-1); min_k q_R(x+k(9,-1)); S transports L9 to SL9.',
      'IV_T3': 'R0=R/sqrt(alpha_prime); N T_alpha_prime=T0 N; iota(R0)=i R0².',
      'IV_P1': 'Channels / relations; puncture C_W at one coordinate; radius2 balls of cardinal243.',
      'IV_P2': 'uK=P3 P11 K; P10=P11-uK uK^t/||uK||²; eplus_perp/Zeplus=Leech.',
      'IV_P3': '([v],d,[y])->((P11v,P10v),d,q24(y)); T acts on the same compact factor.',
      'IV_A1': 'I(gamma)=(sum1_direction_change,sum1_type_change); I(gamma eta)=I(gamma)+I(eta) with boundary.',
      'IV_M1': 'W Qhat=QW and Qhat²=Hhat imply Q²W=HW on D(Hhat), with domain preservation.'}
    for row in focal['results']:
        receipt['result_maps'].append({'id': row['id'], 'statement': row['claim'],
          'input_object': 'C_cont_generated', 'domain': 'C_cont^disc', 'codomain': row['strength'],
          'output_object': row['id'] + '_readout', 'map': formulas[row['id']],
          'generator_inputs': ['C_cont_generated', 'typed phase and incidence readouts', 'declared representation and normalizations'],
          'source_family': 'HMT', 'proof_locator': loc(ROOT / row['destination']),
          'falsifier': 'Failure of the stated identity, domain, preservation or quotient map; promotion beyond the declared realization.',
          'provenance': row['provenance'], 'requires': row['requires'],
          'scope_note': row['strength']})
    receipt['result_maps'].append({'id':'IV_ASSEMBLY','statement':receipt['target']['statement'],
      'input_object':'C_cont_generated','domain':'C_cont^disc','codomain':receipt['target']['codomain'],
      'output_object':'IV_working_manuscript','map':'Compose the explicitly typed readouts; retain each domain, proof and physical realization condition.',
      'generator_inputs':['C_cont_generated','signed_K_readout','exceptional_readout'],
      'source_family':'HMT','proof_locator':loc(ROOT/'sections/iv_conclusiones.tex'),
      'falsifier':'Missing documentary dependency or promotion of an inherited or conditional statement beyond its proof.'})
    receipt['result_families'] = {'IV': {'result_refs': [r['id'] for r in receipt['result_maps']]}}
    receipt['conventional_uses'] = [r for r in receipt['conventional_uses'] if r['role'] in ('PROOF_LANGUAGE','RECOGNITION')]
    receipt['conventional_uses'].append({'name':'Weyl, UHF, dualidad compacta y codominio físico de Polyakov/teoría M', 'role':'TRANSLATION',
      'locator':loc(ROOT/'sections/04_accion_realizacion.tex'),'occurs_after_hmt_output':True,
      'selects_hmt_state':False,'selects_route':False,'sets_generators':False,'sets_coefficients':False,'target_value_used_as_input':False})
    receipt['proof_layers'].update({'finite':'Pruebas matriciales, proyectores, cocientes, 28 controles focales y fuente anterior conservada.',
      'compatibility':'Refinamiento unital, traza, cambios de sección y dominios de operadores se prueban en los cuerpos correspondientes.',
      'recognition':'Realizaciones posteriores de objetos HMT; el parámetro universal R0 de un teorema no es una predicción de radio físico.'})
    receipt['residual_if_any']['physical_theory_M'] = 'Las condiciones de campos, acción, supercarga, tensión, osciladores, amplitudes, anomalías y baja energía permanecen con el alcance explícito de los propietarios; no se declaran resueltas mediante el ensamblaje.'
    receipt['conclusion_status'] = 'APPLICATION_IN_PROGRESS'
    write(TECH / 'RECIBO_GENEALOGICO_IV.json', receipt)

    causal = read(inherited / 'RECIBO_CAUSAL_REVISION.json')
    causal.update({'artifact':str(artifact),'result_id':'ARTICULO_IV_MOONSHINE_DUALIDAD_20260910',
                   'receipt_purpose':'Genealogía de las salidas heredadas y realización posterior de incidencia, fase, dualidad y pantallas.'})
    causal['genealogy']['source_locators'] = [str(p) for p in paths]
    causal['genealogy']['tpk']['codomain'] = 'Registros regionales, registro K, incidencia y realizaciones operatorias con dominios declarados.'
    causal['focal_provenance'] = {'status':'RESULTADO_RECUPERADO','owner':str(TECH/'REGISTRO_PROCEDENCIA.json'),
                                'body':[str(ROOT/r['destination']) for r in focal['results']]}
    causal['limits'] = ['El control causal no prueba por sí mismo los teoremas.',
                         'Se conserva el alcance explícito de alfa y de la realización undecadimensional.',
                         'R0 es un parámetro declarado del teorema universal; no se anuncia aquí una predicción de radio físico.']
    write(TECH / 'RECIBO_CAUSAL_IV.json', causal)
    print(json.dumps({'status':'PREPARED','sources':len(paths),'labels':len(labels),'maps':len(receipt['result_maps']),'errors':errors}, ensure_ascii=False))


def gates():
    commands = [
      [sys.executable,'-I','-S',str(PROJECT/'tools/verificar_genealogia_unica_hmt.py'),'--receipt',str(TECH/'RECIBO_GENEALOGICO_IV.json')],
      [sys.executable,'-I','-S','/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py','--audit',str(TECH/'FUENTE_COMPUESTA.tex.txt'),'--receipt',str(TECH/'RECIBO_CAUSAL_IV.json')]]
    for command in commands:
        subprocess.run(command, check=True)


if __name__ == '__main__':
    if sys.argv[1:] == ['gates']:
        gates()
    else:
        prepare()
