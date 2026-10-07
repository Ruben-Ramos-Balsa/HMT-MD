#!/usr/bin/env python3
"""Conserva un corte de trabajo de VI sin declararlo entrega ni compilación.

Sólo escribe dentro del Artículo VI. La copia contiene fuentes, datos,
programas y estados técnicos. Las huellas comprueban identidad documental,
no la verdad de los resultados. Un corte existente nunca se sobrescribe.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
TECH = ROOT / "technical"
READINESS = TECH / "DEPENDENCIAS_PRECOMPILACION_VI.json"
CUTS = TECH / "cortes"
PLACEMENTS = [
    ("VI_NUCLEO_COMUN", "sections/nucleo.tex", "núcleo formal común; identidad de seis fuentes en NUCLEO_COMUN_RECIBO.json"),
    ("VI_GENERACION_REGIONAL", "sections/14_generacion_regional.tex", "condiciones iniciales, censo, selección regional y prolongación"),
    ("VI_CENSO_REGIONAL", "sections/14_apendice_censo_regional.tex", "tablas completas de firmas y órbitas"),
    ("VI_ARITMETICA_HISTORIAS", "sections/15_aritmetica_historias.tex", "vi:hist:seccion-principal"),
    ("VI_DEPENDENCIAS_ANTERIORES", "sections/09_dependencias_anteriores.tex", "vi:dep:seccion; alcance E108 diferenciado en el expediente"),
    ("VI_PARTICULA", "sections/02_particula_persistencia.tex", "vi:sec:particula"),
    ("VI_CONJUGACION_MOBIUS", "sections/03_conjugacion_mobius.tex", "vi:sec:conjugacion"),
    ("VI_ATLAS", "sections/04_atlas_familias.tex", "atlas y clasificación; figura atlas_clasificacion"),
    ("VI_OPERADOR_MASA", "sections/05_registro_operador_masa.tex", "registro, firma, carácter, torres y unidades"),
    ("VI_FOCK_PAULI", "sections/13_fock_pauli_composicion.tex", "vi:sec:fock-pauli"),
    ("VI_FAMILIAS_COMPUESTOS", "sections/08_familias_y_compuestos.tex", "familias, sectores, selección y realizaciones con sus condiciones"),
    ("VI_SECTORES_TOPOLOGICOS", "sections/10_sectores_topologicos.tex", "sectores de fusión y conjugación neutral"),
    ("VI_KEPLER_SOMMERFELD", "sections/06_kepler_sommerfeld.tex", "vi:sec:kepler"),
    ("VI_METROLOGIA", "sections/07_contraste_metrologico.tex", "comparación y condiciones de interpretación de registros"),
    ("VI_CATALOGO_ESTRUCTURAL", "sections/11_apendices_catalogo.tex", "13 multisecciones, 56 familias, 23 tipos públicos"),
    ("VI_DATOS_COMPANEROS", "sections/12_catalogo_datos_companero.tex", "324 rutas de 65 campos; 471 masas y 384 anchuras"),
    ("VI_BIBLIOGRAFIA", "sections/99_bibliografia.tex", "fuentes primarias y antecedentes documentales"),
]


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_readiness():
    old = json.loads(READINESS.read_text(encoding="utf-8"))
    if old.get("status") == "DEPENDENCIAS_DOCUMENTALES_REUNIDAS":
        raise RuntimeError("Un corte posterior declaró cierre: revisar manualmente, no degradarlo ni sobreescribirlo.")
    rows = []
    for identifier, name, locator in PLACEMENTS:
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("Residencia ausente o simbólica: " + name)
        rows.append({"dependency_id": identifier, "path": name,
                     "sha256": digest(path), "locator": locator,
                     "meaning": "Cuerpo reunido; la presencia no certifica cierre de todas sus dependencias."})
    write_json(READINESS, {
        "schema_version": "hmt-vi-editorial-dependency-readiness-v1",
        "status": "MANUSCRITO_INTEGRADO_AUTONOMIA_NO_CERRADA",
        "reviewed_by_editor": False,
        "reviewed_by_editor_meaning": "No se ha aceptado el cierre integral de las dependencias; no significa que las secciones no se hayan leído.",
        "open_dependencies": [
            {"dependency_id": "VI_PRODUCTOR_CANONICO_E108",
             "description": "Reunir la selección y producción del libro canónico de visitas, trazas y multiplicidades desde el estado terminal anterior a su evaluación incidencial.",
             "source": "technical/CONTRASTE_E108_CON_ARTICULO_II.md",
             "disposition": "BUSQUEDA_FOCAL_Y_COMPOSICION_EFECTIVA_SIN_RECONSTRUCCION_DESDE_K"},
            {"dependency_id": "VI_ALCANCE_REALIZACIONES_SECTORIALES",
             "description": "Conciliar las realizaciones por familias con los resultados anunciados y conservar sus condiciones efectivas; la presencia de las tablas no convierte sus observaciones en predicciones.",
             "source": "technical/PROCEDENCIA_FAMILIAS_Y_COMPUESTOS.md",
             "disposition": "CIERRE_POR_RESULTADO_Y_DEPENDENCIAS_TRANSITIVAS"},
        ],
        "placements": rows,
        "pending_editorial_operations": ["preflight integral", "compilación", "inspección visual y corrección de la maquetación"],
        "scope": "Estado de trabajo y residencias documentales; no certificado científico ni autorización de compilación.",
        "compiled_pdf": False,
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "editor_action_when_ready": "Cerrar las dependencias reales y revisar el conjunto antes de modificar este estado; no vaciar las pendientes para eludir el preflight."
    })


def files_to_preserve():
    files = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        parts = relative.parts
        if parts[:2] == ("technical", "cortes") or any(part in {"__pycache__", ".git", "build", "build_lectura", "output", "qa"} for part in parts) or any(part.startswith('qa_') for part in parts[:-1]):
            continue
        if path.is_symlink():
            raise RuntimeError("Enlace simbólico no archivado: " + str(relative))
        if path.is_file():
            files.append((path, relative))
    return sorted(files, key=lambda pair: str(pair[1]))


def check_cut(directory):
    document = json.loads((directory / "MANIFIESTO.json").read_text(encoding="utf-8"))
    for row in document["files"]:
        path = directory / "fuentes" / row["path"]
        if not path.is_file() or path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            raise RuntimeError("El corte no conserva la identidad de " + row["path"])
    print(json.dumps({"status": "CORTE_DOCUMENTAL_VERIFICADO_NO_ENTREGA",
                      "path": str(directory), "files": len(document["files"]),
                      "compiled_pdf": False, "scientific_autonomy_certified": False}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", help="Identificador nuevo, por ejemplo 20260910_01")
    parser.add_argument("--check", type=Path)
    parser.add_argument("--update-readiness", action="store_true")
    args = parser.parse_args()
    if args.check:
        check_cut(args.check.resolve())
        return
    if args.update_readiness:
        update_readiness()
    if not args.snapshot:
        return
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.snapshot):
        raise RuntimeError("Identificador de corte no válido.")
    directory = CUTS / args.snapshot
    if directory.exists():
        raise RuntimeError("El corte existe: no se sobrescribe.")
    files = files_to_preserve()
    directory.mkdir(parents=True)
    rows = []
    for source, relative in files:
        destination = directory / "fuentes" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        rows.append({"path": relative.as_posix(), "sha256": digest(source),
                     "bytes": source.stat().st_size})
    write_json(directory / "MANIFIESTO.json", {
        "schema": "hmt_vi_corte_de_trabajo_v1", "cut": args.snapshot,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "TRABAJO_CONSERVADO_NO_ENTREGA",
        "compiled_pdf": False, "scientific_autonomy_certified": False,
        "scope": "Copia de continuidad de fuentes, datos y pruebas; no sustituye las puertas científicas o editoriales.",
        "files": rows,
    })
    check_cut(directory)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError) as error:
        sys.stderr.write(str(error) + "\n")
        raise SystemExit(1)
