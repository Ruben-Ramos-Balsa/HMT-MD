#!/usr/bin/env python3
"""Reproduce el lote local nuevo; no certifica RH ni compila un PDF cerrado."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    reports = []
    for stem, script, isolated in (
        ("PARTES_FINITAS", "fuente/pruebas/python/verificar_partes_finitas.py", False),
        ("IDENTIDADES_CONTINUO", "fuente/pruebas/python/verificar_identidades_continuo.py", True),
        ("CAPITULO_03", "gestion/VERIFICAR_CAPITULO_03.py", True),
        ("COLA_Y_PLIEGUE", "fuente/pruebas/python/verificar_cola_y_pliegue.py", True),
        ("GRAM_NUEVE_VENTANAS", "fuente/pruebas/python/verificar_gram_nueve_ventanas.py", False),
        ("COERCIVIDAD_NUEVE_INTERVALOS", "fuente/pruebas/python/verificar_nueve_intervalos_coercividad.py", False),
    ):
        pair = []
        for optimized in (False, True):
            suffix = "_OPTIMIZADO" if optimized else ""
            receipt = ROOT/"fuente/certificados"/("CONTROL_" + stem + suffix + ".json")
            flags = (["-I", "-S"] if isolated else []) + (["-O"] if optimized else [])
            command = [sys.executable, *flags, str(ROOT/script), "--receipt", str(receipt)]
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            if run.returncode:
                raise RuntimeError("No superado: " + script + "\n" + run.stdout + run.stderr)
            item = json.loads(receipt.read_text())
            if not item["status"].startswith("PASS"):
                raise RuntimeError("Estado no positivo en " + str(receipt))
            pair.append(item)
            reports.append({"script":script, "script_sha256":digest(ROOT/script),
                            "optimized":optimized, "receipt":str(receipt.relative_to(ROOT)),
                            "status":item["status"]})
        for value in pair:
            value.pop("optimization_level", None)
            value.pop("optimized", None)
            value.pop("python_optimized", None)
        if pair[0] != pair[1]:
            raise RuntimeError("Resultados distintos entre ejecución normal y optimizada: " + stem)
    run = subprocess.run([sys.executable, "-I", "-S", str(ROOT/"gestion/convertir_manuscrito.py")],
                         cwd=ROOT, capture_output=True, text=True)
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    conversion = json.loads(run.stdout)
    result = {"status":"PASS_REPRODUCCION_LOCAL_LOTE_REANUDACION",
              "scope":"Seis verificadores locales, dos ejecuciones por verificador y conversión literal de ecuaciones. La compilación de lectura se registra por separado.",
              "whole_article_closed":False, "pdf_compiled":False,
              "executions":reports, "conversion":conversion}
    target = ROOT/"gestion/CONTROL_REPRODUCCION_LOTE.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status":result["status"], "executions":len(reports),
                      "manuscripts":len(conversion["files"]),
                      "display_equations_preserved":sum(f["display_equations_preserved"] for f in conversion["files"]),
                      "whole_article_closed":False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
