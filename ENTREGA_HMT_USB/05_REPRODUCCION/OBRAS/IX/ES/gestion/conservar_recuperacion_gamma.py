#!/usr/bin/env python3
"""Copia literal de los propietarios de la integración gamma; no los reescribe."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DOCS = Path('/Users/ruben/Documents')
BASE = 'excelencia academica/ARTICULOS_CIENTIFICOS_HMT_MD_2026-08-14/RIEMANN_REDHEFFER_WEIL/manuscrito/secciones/'
SOURCES = [
    (BASE+'02b_conector_cola_gamma.tex', 'cola_gamma', 'RESULTADO_RECUPERADO'),
    (BASE+'02_factorizacion_basal.tex', 'dominio_basal', 'RESULTADO_RECUPERADO'),
    (BASE+'03_conector_global.tex', 'equivalencia_contraccion_dilatacion', 'PROCEDENCIA_Y_ALCANCE'),
    (BASE+'02c_lector_superviviente_dos_rutas.tex', 'gram_y_densidad', 'RESULTADO_RECUPERADO'),
    ('excelencia academica/RECONSTRUCCION_CONSTRUCTIVA_RH_NS_YM_HMT_MD_REV4_2026-08-14/deltas/rh/08_factorizacion_source_first_fibra_gamma_refinamiento.tex', 'pliegue_previo', 'RESULTADO_RECUPERADO'),
    ('excelencia academica/CONSTRUCTOR_TRES_FLECHAS_HMT_MD_2026-08-15/01_riemann_weil_contraccion_cofinal.md', 'traslacion_y_ensamble', 'RESULTADO_RECUPERADO'),
    ('excelencia academica/output/CONSTANTES_ESTRUCTURA_REALIDAD_LIENZO_ACUMULATIVO_20260909/CONSTANTES_ESTRUCTURA_Y_REALIDAD_FISICA_RECOPILACION_INTEGRA.md', 'narrativa_205_paginas', 'CONSULTA_FOCAL_NO_LECTURA_INTEGRAL'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows = []
    for relative, role, status in SOURCES:
        source = DOCS/relative
        target = ROOT/'antecedentes/recuperacion_gamma'/role/source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and sha(target) != sha(source):
            raise RuntimeError('Copia conservada distinta; requiere nueva versión: '+str(target))
        shutil.copy2(source, target)
        if sha(source) != sha(target):
            raise RuntimeError('Huella distinta tras copia: '+str(target))
        rows.append({'source':str(source), 'copy':str(target.relative_to(ROOT)),
                     'sha256':sha(source), 'bytes':source.stat().st_size,
                     'role':role, 'status':status})
    report = {'status':'PASS_COPIAS_LITERALES_RECUPERACION_GAMMA',
              'scope':'Conservación documental; no certifica la positividad global ni la lectura íntegra de la narrativa.',
              'source_files':rows}
    target = ROOT/'gestion/MANIFIESTO_RECUPERACION_GAMMA.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'], 'copies':len(rows)},ensure_ascii=False))


if __name__ == '__main__':
    main()
