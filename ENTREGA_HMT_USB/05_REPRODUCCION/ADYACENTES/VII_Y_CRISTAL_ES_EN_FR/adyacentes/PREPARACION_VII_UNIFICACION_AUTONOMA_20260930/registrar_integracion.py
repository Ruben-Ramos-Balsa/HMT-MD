#!/usr/bin/env python3
"""Adaptador documental del generador focal existente; no crea otra puerta."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GENERATOR = ROOT / 'output/COMPOSICION_CUATRO_INTERACCIONES_20260929/quantum/registros_delta_20260930/registrar_delta.py'
OUT = HERE / 'registros_integracion'
PARTS = (
    '01_anuncio_resultado.tex',
    '00_antecedentes_geometricos_materiales.tex',
    '02_color_y_representacion_interna.tex',
    '10_gravedad_energia_autoinercia.tex',
    '20_accion_retroaccion_restricciones.tex',
    '40_conclusion_integracion.tex',
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def actual_anchors(spec: dict, text: str) -> list[dict]:
    candidates = (
        ('APP', ('APP',)),
        ('TRIT', ('TRIT',)),
        ('TPK', ('TPK',)),
        ('ESTADO_ENRIQUECIDO', ('estado enriquecido',)),
        ('ESTRUCTURA_DISCRETA_CONTINUO', ('estructura discreta conjunta del continuo', 'estructura discreta del continuo')),
        ('HMT_OUTPUT', ('salidas HMT', 'salidas de esta genealogía', 'salidas')),
        ('CONVENTIONAL', ('lenguaje', 'realización', '\\subsection')),
    )
    cursor = -1
    result = []
    for stage, choices in candidates:
        hits = [(text.find(token, cursor + 1), token) for token in choices]
        hits = [(pos, token) for pos, token in hits if pos >= 0]
        if not hits:
            raise ValueError(f'Ancla tipada no localizada en el agregado: {stage}')
        cursor, token = min(hits)
        result.append({'stage': stage, 'text': token})
    return result


def main() -> int:
    paths = [HERE / 'copia_vii/integracion_20260930' / name for name in PARTS]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        print('NO_ACEPTADO_DOCUMENTALMENTE: faltan fragmentos materializados', *missing, sep='\n')
        return 2
    OUT.mkdir(exist_ok=True)
    aggregate = OUT / 'AGREGADO_SEIS_FRAGMENTOS.tex'
    header = ('% Agregado documental literal de seis fragmentos para auditoría focal.\n'
              '% No es un documento compilable ni sustituye copia_vii/main.tex.\n'
              '% Orden de lectura: anuncio; antecedentes; color; gravedad; acción; conclusión.\n')
    body = [header]
    markdown = ['# Desarrollo acumulado de la preparación de VII\n\n'
                'Transcripción íntegra de los seis fragmentos incorporados en la copia de preparación. '
                'No agrega enunciados ni sustituye el ensamblador LaTeX; el agregado TeX es exclusivamente documental.\n']
    input_manifest = []
    for path in paths:
        text = path.read_text(encoding='utf-8')
        digest = sha(path)
        rel = path.relative_to(HERE).as_posix()
        body.append(f'\n% BEGIN {rel}\n% SHA256 {digest}\n{text}')
        if not text.endswith('\n'):
            body.append('\n')
        body.append(f'% END {rel}\n')
        fence = '`' * max(3, 1 + max((len(word) for word in text.split() if word and set(word) == {'`'}), default=0))
        markdown.append(f'\n## {path.name}\n\nRuta: `{rel}`\n\nSHA-256: `{digest}`\n\n{fence}latex\n{text}')
        if not text.endswith('\n'):
            markdown.append('\n')
        markdown.append(f'{fence}\n')
        input_manifest.append({'path': str(path), 'relative_path': rel, 'sha256': digest})
    aggregate.write_text(''.join(body), encoding='utf-8')
    md = HERE / 'DESARROLLO_ACUMULADO.md'
    md.write_text(''.join(markdown), encoding='utf-8')

    loader = importlib.util.spec_from_file_location('existing_hmt_delta_generator', GENERATOR)
    module = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(module)
    if sha(module.BASE_G) != module.PIN_G or sha(module.BASE_C) != module.PIN_C:
        raise SystemExit('El antecedente documental cambió de huella; no se hereda silenciosamente')
    module.OUT = OUT
    module.anchors = actual_anchors
    spec = copy.deepcopy(module.SPECS['ENUNCIADO'])
    spec.update({
        'file': str(aggregate),
        'codomain': 'INTEGRACION_VII_ACCION_TOTAL_CON_ANTECEDENTES',
        'statement': 'Integrar materialmente en la preparación de VII los antecedentes geométricos y de color con las pruebas de la acción conjunta, su reducción y restricciones, conservando el alcance variacional y canónico y la planitud característica precuántica.',
        'owners': paths,
        'finite': 'Seis fragmentos íntegros: anuncio, antecedentes geométricos y materiales, construcción residual de color, gravedad y autoinercia, acción y restricciones, conclusión. Se heredan las pruebas localizadas y se registran sus nuevas residencias; las puertas no demuestran las identidades matemáticas.',
        'limit': 'Conservación de los dominios y límites focales expuestos en los fragmentos. No se anuncia un nuevo límite cuántico espacial-quiral ni un cierre operatorio universal; el agregado es documental y no se compila.',
    })
    result = module.produce('INTEGRACION_VII', spec,
                            json.loads(module.BASE_G.read_text(encoding='utf-8')),
                            json.loads(module.BASE_C.read_text(encoding='utf-8')))
    unchanged = all(sha(Path(item['path'])) == item['sha256'] for item in input_manifest)
    report = {'schema': 'VII_SIX_FRAGMENT_DOCUMENTARY_AUDIT_V1',
              'adapter_sha256': sha(Path(__file__)), 'reused_generator': str(GENERATOR),
              'reused_generator_sha256': sha(GENERATOR), 'inputs': input_manifest,
              'aggregate': module.locator(aggregate), 'markdown': module.locator(md),
              'source_fragments_unchanged': unchanged, 'result': result,
              'checks_are_documentary_only': True, 'global_physical_closure_certified': False,
              'pdf_compiled': False, 'aggregate_is_main_tex': False}
    (OUT / 'CONTROL_INTEGRACION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for check in result['checks']:
        print(check['stdout'].strip())
        if check['stderr']:
            print(check['stderr'].strip())
    print('PASS_DOCUMENTAL_INTEGRACION_VII' if result['accepted'] and unchanged else 'FAIL_DOCUMENTAL_INTEGRACION_VII')
    return 0 if result['accepted'] and unchanged else 1


if __name__ == '__main__':
    raise SystemExit(main())
