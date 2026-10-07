#!/usr/bin/env python3
"""Verifica el inventario de la entrega actual. No modifica el paquete."""
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parent

def verify():
    manifest=json.loads((ROOT/"metadata/MANIFIESTO_PUBLICACION.json").read_text())
    errors=[]
    for entry in manifest["files"]:
        path=(ROOT/entry["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            errors.append("Ausente o exterior: "+entry["path"])
            continue
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=entry["sha256"]:
            errors.append("Huella distinta: "+entry["path"])
    return {"status":"PASS_INTEGRIDAD_PUBLICACION" if not errors else "FAIL_INTEGRIDAD_PUBLICACION",
            "files_checked":len(manifest["files"]),"errors":errors,
            "scope":"Integridad de los archivos inventariados; no sustituye las pruebas matemáticas ni la reproducción."}

if __name__=="__main__":
    try:
        result=verify()
    except (OSError,ValueError,KeyError) as exc:
        result={"status":"FAIL_INTEGRIDAD_PUBLICACION","errors":[str(exc)]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if result["status"].startswith("PASS") else 1)
