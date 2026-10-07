#!/usr/bin/env python3
"""Copia sólo los siete antecedentes necesarios, sin modificar originales."""
from pathlib import Path
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
ORIGIN = HERE.parent / "ARTICULO_VIII_PRIMOS_ESTRUCTURA_ESPECTRAL_20260910"
DEST = HERE / "dependencias_viii"
RELATIVE = [
    "fuente/pruebas/python/verificar_gram_nueve_ventanas.py",
    "fuente/pruebas/python/partes_finitas_exactas.py",
    "fuente/pruebas/python/a9_native.py",
    "manuscrito/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.md",
    "antecedentes/nonadica/pi_1000_decimales.txt",
    "antecedentes/nonadica/certificado_generacion_estructural.json",
    "antecedentes/nonadica/SHA256SUMS",
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

records = []
for relative in RELATIVE:
    source, target = ORIGIN / relative, DEST / relative
    if not source.is_file():
        raise FileNotFoundError(source)
    source_hash = digest(source)
    if target.exists():
        if digest(target) != source_hash:
            raise RuntimeError("La copia local difiere; no se sobrescribe: " + str(target))
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    if digest(target) != source_hash:
        raise RuntimeError("Fallo de identidad: " + str(target))
    records.append({"origin": str(source), "local": str(target.relative_to(HERE)),
                    "sha256": source_hash, "bytes": source.stat().st_size})
manifest = {"status": "PASS_SEVEN_DEPENDENCIES_BYTE_IDENTICAL",
            "count": len(records), "scope": "Sólo identidad documental; no prueba matemática",
            "files": records}
(HERE / "MANIFIESTO_DEPENDENCIAS_SCHUR.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": manifest["status"], "count": len(records)}))
