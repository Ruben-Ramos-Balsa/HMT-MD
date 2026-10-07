#!/usr/bin/env python3
"""Reubica recibos heredados sobre el corte editorial IV REV02, sin editar TeX.

Conserva íntegros los registros antecedentes. Actualiza exclusivamente el
artefacto compuesto, sus anclas y residencias locales; los campos científicos
heredados no reciben una nueva evaluación. El delta editorial se adjunta como
tal. No ejecuta el scaffolder original ni modifica el registro canónico.
"""
from pathlib import Path
import hashlib
import json
import re
import runpy

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.with_name('ARTICULO_IV_MOONSHINE_DUALIDAD_TEORIA_M_20260910')
OUT = ROOT / 'technical/recepcion_rev02'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def spec(path):
    return {'path': str(path), 'sha256': sha(path)}

def write_once(path, data):
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if path.exists() and path.read_text(encoding='utf-8') != content:
        raise RuntimeError('Corte ya materializado con otro contenido: ' + str(path))
    path.write_text(content, encoding='utf-8')

def main():
    compiler = runpy.run_path(str(ROOT/'technical/compilar_iv.py'), run_name='iv_receipt_graph')
    graph = compiler['source_graph']()
    if graph['errors']:
        raise RuntimeError(str(graph['errors']))
    run = Path(load(ROOT/'technical/preflight_rev02/CORTE_ACTUAL.json')['run'])
    certificate = load(run/'CERTIFICADO_CONTINUIDAD_EDITORIAL.json')
    delta_path = Path(certificate['revision_delta']['path'])
    validator = runpy.run_path(str(ROOT/'technical/preflight_rev02/verificar_continuidad_editorial.py'), run_name='iv_delta')
    validator['verify_revision_delta'](delta_path)
    def expand(path, stack=()):
        if path in stack:
            raise RuntimeError('Inclusión cíclica')
        text = compiler['strip_comments'](path.read_text(encoding='utf-8'))
        def include(match):
            target = compiler['resolve_tex'](path, match.group(1), match.group(2))
            return '\n' + expand(target, stack+(path,)) + '\n'
        return re.sub(r'\\(input|include)\s*\{([^{}]+)\}', include, text)
    combined = expand(ROOT/'main.tex') + '\n'
    cut = hashlib.sha256(combined.encode()).hexdigest()[:16]
    out = OUT/cut
    out.mkdir(parents=True, exist_ok=True)
    artifact = out/'FUENTE_COMPUESTA.tex.txt'
    if artifact.exists() and artifact.read_text(encoding='utf-8') != combined:
        raise RuntimeError('Colisión de corte compuesto')
    artifact.write_text(combined, encoding='utf-8')
    prior_path = OLD/'technical/RECIBO_GENEALOGICO_IV.json'
    prior = load(prior_path)
    inherited_artifact = prior['artifact']
    prior['receipt_id'] = 'ARTICULO_IV_REV02_EDITORIAL_20260910'
    prior['artifact'] = {'path':str(artifact),'sha256':sha(artifact),'kind':'MANUSCRIPT','anchors':[]}
    position = 0
    for anchor in inherited_artifact['anchors']:
        pattern = r'\s+'.join(map(re.escape, anchor['text'].split()))
        match = re.search(pattern, combined[position:])
        if match is None:
            raise RuntimeError('Ancla heredada no localizada: '+anchor['stage'])
        start = position + match.start()
        prior['artifact']['anchors'].append({'stage':anchor['stage'], 'text':match.group(), 'line':combined.count('\n',0,start)+1})
        position += match.end()
    def rebind(value):
        if isinstance(value,dict):
            if isinstance(value.get('path'),str) and value['path'].startswith(str(OLD)+'/'):
                p = ROOT / Path(value['path']).relative_to(OLD)
                if p.is_file() and p.suffix == '.tex':
                    value.update(spec(p))
                    if 'lines' in value:
                        value['lines']='1-'+str(len(p.read_text(encoding='utf-8').splitlines()))
            for child in value.values(): rebind(child)
        elif isinstance(value,list):
            for child in value: rebind(child)
    rebind(prior)
    prior['previous_editorial_revision'] = prior.get('editorial_revision')
    prior['editorial_revision'] = {'scope':'EDITORIAL_REV02_SOURCE_BINDING', 'predecessor_receipt':spec(prior_path),
        'reviewed_delta':spec(delta_path), 'active_source_graph_sha256':graph['active_graph_sha256'],
        'scientific_statements_reassessed':False, 'claims_promoted':False,
        'interpretation':'Los campos científicos y reservas antecedentes se preservan como procedencia, no como dictamen nuevo de ausencia o cierre. Las incorporaciones editoriales y sus condiciones constan en el delta revisado y en las fuentes activas.'}
    prior['receipt_purpose']='Vinculación actual de la genealogía heredada al corte editorial REV02; sin reclasificar resultados ni sustituir sus pruebas.'
    prior['additional_editorial_residences']=[spec(ROOT/'sections'/n) for n in ('iv_accion_antecedente.tex','iv_angulos_antecedente.tex','iv_elipse_radio.tex')]
    write_once(out/'RECIBO_GENEALOGICO_IV_REV02.json', prior)
    causal_path = OLD/'technical/RECIBO_CAUSAL_IV.json'
    causal = load(causal_path)
    causal.update({'artifact':str(artifact),'result_id':'ARTICULO_IV_REV02_20260910'})
    causal['genealogy']['source_locators']=[str(ROOT/row['path']) for row in graph['tex']]
    causal['editorial_revision']={'predecessor_receipt':spec(causal_path),'reviewed_delta':spec(delta_path),
        'scope':'Actualización documental sobre fuentes vigentes; no una nueva certificación científica.',
        'radius_note':'R0 conserva su función de parámetro del teorema universal; la familia elíptica interna {R*,1/R*} aparece ahora como especialización anterior a su realización dimensional. No se identifica α\u2032 con α ni se usa metrología para seleccionar la forma.'}
    write_once(out/'RECIBO_CAUSAL_IV_REV02.json',causal)
    write_once(out/'GRAFO_FUENTES_ACTIVAS.json', graph)
    current={'cut':cut,'directory':str(out),'composed_source':spec(artifact),
        'genealogy_receipt':spec(out/'RECIBO_GENEALOGICO_IV_REV02.json'),
        'constants_receipt':spec(out/'RECIBO_CAUSAL_IV_REV02.json'), 'active_sources':len(graph['tex'])}
    current_path=OUT/'CORTE_ACTUAL.json'
    current_path.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(current,ensure_ascii=False))

if __name__ == '__main__':
    main()
