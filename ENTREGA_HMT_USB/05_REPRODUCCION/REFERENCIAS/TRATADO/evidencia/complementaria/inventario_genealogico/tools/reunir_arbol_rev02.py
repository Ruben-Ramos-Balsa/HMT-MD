#!/usr/bin/env python3
"""Reúne REV01 íntegra y las ampliaciones REV02, con control documental."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREE = ROOT / 'REV02_ARBOL'
PROJECT = Path('/Users/ruben/Documents/New project')
PARTS = [
    '10_CRITERIO_DE_DESCOMPOSICION.md',
    '15_ALCANCE_GLOBAL_Y_CONTINUIDAD.md',
    '11_APP_ARBOL_ELEMENTAL.md',
    '12_LECTURA_RAPIDA_Y_GENERACION.md',
    '13_ESTRUCTURA_DISCRETA_ARBOL.md',
    '14_NUCLEO_COMUN_Y_CARTOGRAFIAS_PREVIAS.md',
    '17_CONCORDANCIA_REGISTRO_K_SERIE_Y_DELTAS.md',
]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def save_new(path, data):
    raw = data.encode() if isinstance(data, str) else data
    if path.exists():
        assert path.read_bytes() == raw, f'Revisión ya sellada distinta: {path}'
    else:
        path.write_bytes(raw)

def main():
    old_manifest = json.loads((ROOT/'MANIFIESTO_REV01.json').read_text())
    for item in old_manifest['parts']:
        assert sha(Path(item['path']).read_bytes()) == item['sha256'], item['path']
    old = ROOT/'INVENTARIO_ACUMULATIVO_REV01.md'
    assert sha(old.read_bytes()) == old_manifest['artifact_sha256']
    roots = []
    for part in old_manifest['parts']:
        path = Path(part['path'])
        for line, content in enumerate(path.read_text().splitlines(),1):
            match = re.match(r'^#{2,3}\s+((?:APP|TRIT|TPK|SR|CG|KA)-\d{3})\s+—\s+(.+)', content)
            if match:
                roots.append({'id':match[1], 'title':match[2], 'source':str(path),'line':line,
                              'status':'FICHA_REV01_CONSERVADA', 'kind':'DOCUMENTARY_ROOT'})
    assert len(roots)==113
    app = json.loads((TREE/'11_APP_ARBOL_ELEMENTAL.json').read_text())
    by_parent = {}
    for n in app['nodes']:
        by_parent.setdefault(n['parent'],[]).append(n)
    nav = [
        '# Árbol maestro de consulta — revisión 02\n',
        'Este índice enlaza todas las fichas de REV01 y sus primeras ampliaciones. No es un árbol cerrado ni una certificación de exhaustividad. Las ramas aún no subdivididas conservan íntegros sus textos y sus pendientes.\n',
        'El perímetro es el corpus global: integral de 2.249 páginas, síntesis, cadena compacta, reservorio, serie, narración y desarrollos posteriores. Las dos canteras antiguas tienen una función auxiliar y no determinan qué puede incorporarse.\n',
        f'Lectura reunida: [inventario acumulativo REV02](<{ROOT / "INVENTARIO_ACUMULATIVO_REV02.md"}>).\n',
        '## Todas las fichas de partida y sus descendientes APP\n',
    ]
    def render_children(parent, depth):
        for node in by_parent.get(parent,[]):
            nav.append('  '*depth + f"- {node['id']} — {node['title']}")
            render_children(node['id'],depth+1)
    for root in roots:
        nav.append(f"- [{root['id']} — {root['title']}](<{root['source']}:{root['line']}>)")
        render_children(root['id'],1)
    nav += ['\n## Ampliaciones y concordancias\n']
    for name in PARTS:
        path=TREE/name
        nav.append(f'- [{name}](<{path}>)')
    nav += [
        '\nLas extracciones de fuentes de generación y de continuo contienen sus propios IDs y localizadores, además de los vínculos a SR/CG/KA. No se suman mecánicamente a los IDs APP como si fueran resultados disjuntos. La futura concordancia será muchos-a-muchos cuando una operación tenga varios propietarios.\n',
        '## Pendientes preservados\n',
        f'[P01–P10 íntegros](<{ROOT/"05_PENDIENTES_DE_INTEGRACION.md"}>) y [actualización de alcance y tareas](<{TREE/"15_ALCANCE_GLOBAL_Y_CONTINUIDAD.md"}>).\n',
    ]
    save_new(TREE/'16_ARBOL_MAESTRO.md','\n'.join(nav)+'\n')
    source_tree_payloads = {}
    for name in ('12_LECTURA_RAPIDA_Y_GENERACION.json','13_ESTRUCTURA_DISCRETA_ARBOL.json'):
        path = TREE/name
        if path.exists():
            source_tree_payloads[name] = json.loads(path.read_text())
    index={'root_fichas_preserved':roots, 'app_descendants':app['nodes'],
           'source_tree_payloads_preserved':source_tree_payloads,
           'additional_source_trees':[str(TREE/x) for x in PARTS if x.startswith(('12_','13_'))],
           'global_source_roots':json.loads((ROOT/'censo/RAICES.json').read_text()),
           'all_dependencies_validated':False,
           'scope':'EXPOSITIVE_INDEX_NOT_COMPLETE_CAUSAL_PROOF_GRAPH'}
    save_new(TREE/'16_ARBOL_MAESTRO.json',json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    intro = (
        '# Inventario genealógico HMT — revisión acumulativa 02\n\n'
        '19 de septiembre de 2026. REV01 se conserva literalmente a continuación, seguida '
        'por las ampliaciones de REV02. No se ha sustituido ni resumido ninguna pieza previa.\n\n'
        'La revisión amplía la granularidad y las concordancias; no declara terminada la lectura '
        'del corpus completo. Los dos antecedentes históricos son cantera, no perímetro.\n\n'
        f'Índice de navegación: [árbol maestro](<{TREE/"16_ARBOL_MAESTRO.md"}>).\n\n'
    )
    records=[]
    contents=[]
    for path in [old]+[TREE/x for x in PARTS]:
        raw=path.read_bytes()
        body=raw.decode()
        records.append({'path':str(path),'sha256':sha(raw),'bytes':len(raw),'lines':len(body.splitlines())})
        contents.append(f'\n<!-- BEGIN INTEGRAL {path.name}; SHA256={sha(raw)} -->\n\n'+body+f'\n<!-- END INTEGRAL {path.name} -->\n')
    artifact=ROOT/'INVENTARIO_ACUMULATIVO_REV02.md'
    whole=intro+'\n'.join(contents)
    assert old.read_text() in whole
    links=re.findall(r'\]\(<(/[^>]+)>\)',whole)
    missing=[]
    for ref in links:
        target=re.sub(r':\d+(?:-\d+)?$','',ref)
        if not Path(target).exists() and Path(target)!=artifact:
            missing.append(ref)
    assert not missing, missing
    save_new(artifact,whole)
    manifest={
        'artifact':str(artifact),'artifact_sha256':sha(whole.encode()),'parts':records,
        'rev01_preserved_verbatim':True,'rev01_source_parts_hashes_unchanged':True,
        'global_source_roots_preserved':len(index['global_source_roots']),
        'initial_fichas_preserved':len(roots),'app_descendants':len(app['nodes']),
        'local_links_checked':len(links),'missing_local_links':[],
        'all_dependencies_validated':False,'mathematical_completeness_certified':False,
        'source_files_modified':[],'pdfs_modified':[],'new_lean_compilation':False,
    }
    save_new(ROOT/'MANIFIESTO_REV02.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    receipt=json.loads((ROOT/'RECIBO_CAUSAL_REV01.json').read_text())
    receipt.update({
        'artifact':str(artifact),'artifact_sha256':manifest['artifact_sha256'],
        'result_id':'INVENTARIO_DOCUMENTAL_GENERATIVO_HMT_20260919_REV02',
        'scope_note':'Ampliación documental: conservación literal de REV01, subinventario APP, canteras y variantes de núcleo. No certifica todo el corpus ni la completitud del grafo.',
        'current_source_map':str(TREE/'15_ALCANCE_GLOBAL_Y_CONTINUIDAD.md'),
        'inherited_receipt':{'path':str(ROOT/'RECIBO_CAUSAL_REV01.json'),'sha256':sha((ROOT/'RECIBO_CAUSAL_REV01.json').read_bytes())},
    })
    receipt['genealogy']['source_locators']=[f"{x['path']}:1-{x['lines']} sha256={x['sha256']}" for x in records]
    receipt['result_boundary']['work_performed']=[
        'Conservación literal de REV01 y de sus 113 fichas',
        'Descomposición elemental de APP con 121 descendientes editoriales',
        'Cálculo focal de las 81 celdas y del cociclo',
        'Cotejo documental del bloque común y variantes de la serie',
        'Extracción parcial de detalles de canteras históricas sin restringir el corpus global',
    ]
    save_new(ROOT/'RECIBO_CAUSAL_REV02.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    refs=subprocess.check_output(['python3','-I','-S',str(PROJECT/'PUBLICACION_HMT/SERIE_ARTICULOS_HMT/herramientas/render_referencias_serie.py')],text=True,cwd=PROJECT)
    save_new(ROOT/'REFERENCIAS_SERIE_REV02.md',refs)
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
