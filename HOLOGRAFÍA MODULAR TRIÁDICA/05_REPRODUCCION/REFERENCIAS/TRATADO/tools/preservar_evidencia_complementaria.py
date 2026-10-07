#!/usr/bin/env python3
"""Conserva inventarios, productores y suplementos de las derivaciones incluidas."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[2]
SOURCES=(
 ('output/INVENTARIO_GENEALOGICO_HMT_20260919','inventario_genealogico'),
 ('output/REVISION_EDITORIAL_HMT_MD_20260905/03_PRUEBAS','integral_pruebas'),
 ('03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados','certificados_generativos'),
 ('16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA','lectura_dodecafasica'),
 ('output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/supplement','suplemento_conservacion'),
)
records=[]
for relative,name in SOURCES:
    source=PROJECT/relative;target=ROOT/'evidencia/complementaria'/name
    if not target.exists():shutil.copytree(source,target,symlinks=True)
    rows=[]
    for p in sorted(source.rglob('*')):
        if not p.is_file():continue
        q=target/p.relative_to(source)
        digest=hashlib.sha256(p.read_bytes()).hexdigest()
        if not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest()!=digest:
            raise ValueError(('Diferencia material',p,q))
        rows.append({'path':str(p.relative_to(source)),'sha256':digest,'bytes':p.stat().st_size})
    records.append({'source':str(source),'copy':str(target.relative_to(ROOT)),'files':rows})
csv=ROOT/'datos/GENERACION/G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/HMT_N69_ley_transicion_o_axioma_cilindrico_v1/N69_signatures_t0_t99.csv'
shutil.copy2(csv,ROOT/'datos/N69_signatures_t0_t99.csv')
shutil.copy2(ROOT/'incoming/verificar_incidencias_repertorio.py',ROOT/'tools/verificar_incidencias_repertorio.py')
(ROOT/'metadata/EVIDENCIA_COMPLEMENTARIA_PRESERVADA.json').write_text(json.dumps({
 'scope':'Copia íntegra de evidencia y productores; las rutas históricas de ejecución se conservan y no equivalen a reproducción portable.',
 'records':records},ensure_ascii=False,indent=2)+'\n')
print('Suplementos conservados:',len(records),'archivos:',sum(len(r['files']) for r in records))
