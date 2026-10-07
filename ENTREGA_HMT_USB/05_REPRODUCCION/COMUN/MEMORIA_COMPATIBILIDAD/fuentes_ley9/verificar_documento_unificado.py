"""Verifica conservación documental, no corrección matemática.

Uso: python3 -I -S verificar_documento_unificado.py
     python3 -I -S verificar_documento_unificado.py --embedded-only

No ejecuta los programas incorporados ni escribe archivos.
"""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFIESTO_DOCUMENTO_UNIFICADO.json").read_text(encoding="utf-8"))
document = (root / manifest["document"]["name"]).read_bytes()
digest = lambda data: hashlib.sha256(data).hexdigest()
errors = []
if digest(document) != manifest["document"]["sha256"]:
    errors.append("La huella del documento no coincide.")
if len(document) != manifest["document"]["bytes"]:
    errors.append("El tamaño del documento no coincide.")
entries = manifest["entries"]
if len(entries) != manifest["source_count"] or len({r["name"] for r in entries}) != len(entries):
    errors.append("El censo contiene una omisión o duplicación.")
counts = {"markdown": 0, "python": 0, "json": 0}
type_map = {".md": "markdown", ".py": "python", ".json": "json"}
checked_originals = 0
previous_end = 0
for row in entries:
    start, end = row["byte_start"], row["byte_end"]
    if not (previous_end <= start < end <= len(document)):
        errors.append("Intervalo inválido: " + row["name"])
    previous_end = end
    embedded = document[start:end]
    if len(embedded) != row["bytes"] or digest(embedded) != row["sha256"]:
        errors.append("Contenido incorporado alterado: " + row["name"])
    if not document[:start].endswith(b"\n"):
        errors.append("Inicio de fuente mal delimitado: " + row["name"])
    counts[type_map[Path(row["name"]).suffix]] += 1
    if "--embedded-only" not in sys.argv:
        original = root / row["name"]
        if not original.exists() or original.read_bytes() != embedded:
            errors.append("Original ausente o cambiado: " + row["name"])
        else:
            checked_originals += 1
if counts != manifest["counts"]:
    errors.append("El reparto de tipos no coincide.")
if sum(r["bytes"] for r in entries) != manifest["original_bytes"]:
    errors.append("El volumen de originales no coincide.")
required = {"NARRATIVA_APROBADA_Y_MANDATO_DESARROLLO.md",
            "NARRATIVA_CONTINUACION_COMPATIBILIDAD.md",
            "COMPATIBILIDAD_HOLONOMIA_E_INFORMACION.md",
            "HIBRIDACION_ACCION_MASA_PROPAGACION.md",
            "CONTRAANGULO_ELECTRON_BARBERO_CATALAN.md"}
if not required.issubset({r["name"] for r in entries}):
    errors.append("Falta una narrativa o desarrollo principal.")
result = {
    "status": "PASS_CONSERVACION_DOCUMENTAL_39_DE_39" if not errors else "FAIL_CONSERVACION_DOCUMENTAL",
    "sources_embedded": len(entries),
    "originals_unchanged": checked_originals if "--embedded-only" not in sys.argv else "not_checked",
    "counts": counts,
    "original_bytes": manifest["original_bytes"],
    "document_bytes": len(document),
    "document_sha256": digest(document),
    "scope": "Identidad y cobertura documental del corte registrado; no certificación matemática ni física.",
    "errors": errors,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(bool(errors))

