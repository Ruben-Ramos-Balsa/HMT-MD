#!/usr/bin/env python3
"""Verifica el ZIP y reproduce controles portables en una extracción temporal."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "output/ARTICULO_III_VACIO_ELECTROMAGNETICO_FUENTES_Y_REPRODUCCION.zip"

def run(command, cwd):
    process = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if process.returncode:
        raise RuntimeError(" ".join(command) + "\n" + process.stdout + process.stderr)
    return {"command": command, "returncode": process.returncode,
            "stdout": process.stdout.strip()}

def main():
    results = []
    with zipfile.ZipFile(ZIP) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Integridad ZIP incorrecta")
        manifest = json.loads(archive.read("ARTICULO_III/MANIFIESTO_ENTREGA.json"))
        for item in manifest["files"]:
            data = archive.read("ARTICULO_III/" + item["path"])
            if hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise RuntimeError("Huella incorrecta: " + item["path"])
        with tempfile.TemporaryDirectory(prefix="hmt_iii_rev02_") as folder:
            archive.extractall(folder)
            target = Path(folder) / "ARTICULO_III"
            for command in [
                [sys.executable, "-I", "-S", "technical/reproducibilidad/reproducir.py", "--check-article-copies"],
                [sys.executable, "-I", "-S", "technical/verificar_delta_rev02.py"],
                [sys.executable, "-I", "-S", "technical/propuestas/verificar_vacancias_prefactor.py"],
                [sys.executable, "technical/evaluar_vacio.py"],
            ]:
                results.append(run(command, target))
    report = {"status": "PASS_PAQUETE_REV02_REPRODUCCION_FOCAL",
              "zip_sha256": hashlib.sha256(ZIP.read_bytes()).hexdigest(),
              "manifest_files_verified": len(manifest["files"]),
              "temporary_extraction": True, "commands": results,
              "global_mathematical_autonomy_certified": False,
              "physical_identification_certified": False}
    (ROOT / "output/COMPROBACION_ZIP_REV02.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["status"], "files=" + str(report["manifest_files_verified"]))

if __name__ == "__main__":
    main()
