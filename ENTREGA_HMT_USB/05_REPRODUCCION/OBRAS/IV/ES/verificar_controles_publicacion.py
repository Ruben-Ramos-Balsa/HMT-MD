#!/usr/bin/env python3
"""Ejecuta controles finitos activos. Cada salida conserva su alcance."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
PROFILES={
"IV":["technical/verificar_imagen_firmada.py","technical/verificar_weyl_orientado_rev04.py"],
"V":["colaboracion_fuentes/verificar_ocupacion_microcanonica.py",
     "colaboracion_radiacion_termica_20260910/verificar_radiacion_termica.py",
     "colaboracion_accion_termica_20260910/verificar_recuperacion.py",
     "gestion/verificar_transporte_fock_rev02.py",
     "colaboracion_velocidad_III_V_20260910/verificar_enlace_velocidad.py"]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--articulo",choices=PROFILES,required=True)
    parser.add_argument("--lean-bin")
    parser.add_argument("--recibo",type=Path)
    args=parser.parse_args()
    records=[]
    errors=[]
    targets=PROFILES[args.articulo]+["suplemento/verificar_acoplamiento.py",
        "suplemento/verificar_aislamiento_jet.py",
        "suplemento/censo_terminal/verificar_censo.py",
        "suplemento/alpha/technical/verificar_lector_analitico_alpha.py"]
    for relative in targets:
        path=ROOT/relative
        if not path.is_file():
            errors.append("Falta "+relative)
            continue
        variants=[False] if path.name=="verificar_imagen_firmada.py" else [False,True]
        outputs=[]
        for optimized in variants:
            command=[sys.executable,"-I","-S","-B"]+(["-O"] if optimized else [])+[str(path)]
            p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=180)
            records.append({"file":relative,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                "optimized":optimized,"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr})
            outputs.append(p.stdout)
            if p.returncode:
                errors.append(relative+(" -O" if optimized else "")+": ejecución fallida")
        if len(outputs)==2 and outputs[0]!=outputs[1]:
            errors.append(relative+": cambia salida entre normal y -O")
    if args.lean_bin:
        p=subprocess.run([sys.executable,"-I","-S","-B",
            str(ROOT/"suplemento/lean/verificar_lean.py"),"--article",args.articulo,
            "--lean-bin",args.lean_bin,"--negative-controls"],cwd=ROOT,
            capture_output=True,text=True,timeout=240)
        records.append({"file":"suplemento/lean/verificar_lean.py","returncode":p.returncode,
            "stdout":p.stdout,"stderr":p.stderr})
        if p.returncode:
            errors.append("Falló Lean")
    result={"status":"PASS_CONTROLES_PUBLICACION" if not errors else "FAIL_CONTROLES_PUBLICACION",
        "article":args.articulo,"lean_checked":bool(args.lean_bin),"executions":records,"errors":errors,
        "scope":"Controles reproducidos de las identidades y dominios indicados por cada programa. No formalización global de los artículos."}
    if args.recibo:
        with args.recibo.open("x",encoding="utf-8") as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({"status":result["status"],"executions":len(records),
        "lean_checked":result["lean_checked"],"errors":errors},ensure_ascii=False,indent=2))
    return bool(errors)

if __name__=="__main__":
    raise SystemExit(main())
