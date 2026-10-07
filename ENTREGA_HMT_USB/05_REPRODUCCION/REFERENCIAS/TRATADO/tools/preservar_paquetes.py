#!/usr/bin/env python3
"""Copia propietarios ejecutables íntegros y comprueba igualdad byte a byte."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[2]
NAMES=(
 'PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA',
 'IMPLEMENTACION_K_SEMILLAS_INCIDENCIA_20260918',
 'PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919',
)

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def main():
    rows=[]
    for name in NAMES:
        source=PROJECT/'output'/name
        destination=ROOT/'evidencia/propietarios'/name
        if not destination.exists(): shutil.copytree(source,destination,symlinks=True)
        items=[]
        for path in sorted(source.rglob('*')):
            if not path.is_file(): continue
            relative=path.relative_to(source)
            counterpart=destination/relative
            actual=digest(path)
            if not counterpart.is_file() or digest(counterpart)!=actual:
                raise RuntimeError('Diferencia material: '+str(relative))
            items.append({'path':str(relative),'sha256':actual,'bytes':path.stat().st_size})
        rows.append({'source':str(source),'copy':str(destination.relative_to(ROOT)),
                     'files':items,'scope':'PROCEDENCIA_INTEGRA; NO_RECOMPILACION'})
    source=ROOT.parent/'REV02/lean'
    destination=ROOT/'lean'
    if not destination.exists(): shutil.copytree(source,destination)
    target=ROOT/'metadata/PAQUETES_PRESERVADOS.json'
    target.write_text(json.dumps({'scope':'Identidad material de los propietarios; independiente de la validez matemática y del alcance de Lean.','packages':rows},ensure_ascii=False,indent=2)+'\n')
    print('Paquetes íntegros:',len(rows),'archivos:',sum(len(r['files']) for r in rows))

if __name__=='__main__': main()
