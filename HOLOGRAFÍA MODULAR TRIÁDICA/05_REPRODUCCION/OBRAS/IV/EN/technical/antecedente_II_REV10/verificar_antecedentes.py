#!/usr/bin/env python3
"""Conservación y verificación binaria focal de siete fuentes de II REV10.

Sin argumentos: verifica las copias respecto del inventario local, sin acceder
a las rutas originales. --copy-from SECTIONS conserva las fuentes íntegras y
crea el inventario; nunca sobrescribe un contenido distinto ya existente.
No verifica teoremas, compilación ni clausura global de dependencias.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys


OWNERS = {
    "05_accion.tex": {
        "locators": ["1--195"],
        "destination": "sections/iv_accion_antecedente.tex",
        "content": "H4, Smith, cociente de 16 hojas, norma y década; H5, transferencia, continuación, positividad y secciones de acción.",
    },
    "revision_planck.tex": {
        "locators": ["13--93"],
        "destination": "sections/iv_accion_antecedente.tex",
        "content": "Procedencia y asignación de coeficientes, renovación formal, primer peso unitario y secciones por retorno.",
    },
    "05b_coordenadas_angulares.tex": {
        "locators": ["1--125"],
        "destination": "sections/iv_angulos_antecedente.tex",
        "content": "Publicación angular, base mil, grados y radianes, acción por vuelta y reversión de canales.",
    },
    "07_elipse.tex": {
        "locators": ["1--61"],
        "destination": "sections/iv_elipse_radio.tex",
        "content": "Elipse etiquetada, radio de forma y distinción entre transporte simpléctico y antisimpléctico.",
    },
    "07b_geometria_elipse.tex": {
        "locators": ["41--70", "73--115", "144--158"],
        "destination": "sections/iv_elipse_radio.tex",
        "content": "Radio polar, fase paramétrica, ley areal, signo de la acción cerrada y reciprocidad.",
    },
    "12_dualidad_t.tex": {
        "locators": ["27--107", "265--346"],
        "destination": "sections/iv_elipse_radio.tex; sections/02_dualidad_t.tex",
        "content": "Determinación de R0, recuperación angular, matriz de semiejes; condiciones de la normalización dimensional y transporte de momento-enrollamiento.",
    },
    "definicion_planck_rev06.tex": {
        "locators": ["4--34"],
        "destination": "sections/iv_accion_antecedente.tex",
        "content": "Par de secciones de acción y relación entre valoración, carácter, continuación y acción por vuelta.",
    },
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def preserve(source, here):
    source = source.resolve(strict=True)
    manifest_path = here / "REGISTRO_PROCEDENCIA.json"
    require(not manifest_path.exists(), "El registro ya existe; usar la verificación local.")
    records = []
    for name, use in OWNERS.items():
        original = source / name
        require(original.is_file(), "Fuente ausente: " + str(original))
        copied = here / name
        if copied.exists():
            require(copied.read_bytes() == original.read_bytes(),
                    "Copia existente distinta; se conserva intacta: " + name)
        else:
            shutil.copy2(original, copied)
        require(copied.read_bytes() == original.read_bytes(),
                "Diferencia binaria tras la copia: " + name)
        records.append({
            "file": name,
            "original_path": str(original),
            "source_sha256": digest(original),
            "copy_sha256": digest(copied),
            "bytes": copied.stat().st_size,
            "copy_scope": "ARCHIVO_COMPLETO_SIN_EDICION",
            "copy_identical_at_preservation": True,
            "selection_in_article_IV": use,
        })
    package = source.parent.parent
    pdf = package / "output/pdf/ARTICULO_II_REVISION_10.pdf"
    pdf_record = None
    if pdf.is_file():
        pdf_record = {"path": str(pdf), "sha256": digest(pdf)}
    record = {
        "schema": "HMT_FOCAL_SOURCE_PRESERVATION_1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_edition": "ARTICULO_II_REV10_EDICION_INTEGRADA_20260910",
        "source_sections": str(source),
        "source_pdf_identity_only": pdf_record,
        "destination_edition": "ARTICULO_IV_REV02_EDICION_INTEGRADA_20260910",
        "provenance_status": "RESULTADO_RECUPERADO",
        "scope": "Conservación íntegra por identidad binaria de siete propietarios. Los fragmentos públicos de IV reúnen las dependencias seleccionadas; la copia histórica no sustituye su demostración en el artículo.",
        "conditions_preserved": [
            "Norma local sobre G_H y aplicación única de la autoescala.",
            "Asignación de los coeficientes de H5 a sus grados y signos como parte del carácter declarado.",
            "Normalización unitaria del primer peso y regla de concatenación de la continuación regional.",
            "Secciones anterior y posterior diferenciadas, con base de acción positiva común.",
            "Ambos ángulos en una misma unidad; radio de forma adimensional y semiejes con unidad de raíz de acción.",
            "Escala dimensional alpha-prima distinta de alpha; la determinación de R0 no fija por sí sola la escala de cuerda.",
        ],
        "editorial_additions_in_IV": [
            "Explicación de la cota H5<2 y comprobación de 0<C*<A mediante desigualdades racionales.",
            "Sustitución algebraica Rstar^4=(499 alpha-eta_ret)/(501 alpha+eta_ret).",
            "Especialización a la familia de dos radios recíprocos; no confundirla con una sola fibra estable.",
        ],
        "not_certified_by_this_record": [
            "Validez matemática global de HMT o de los artículos.",
            "Clausura completa de las dependencias del artículo IV.",
            "Compilación o incorporación de cada archivo histórico entero al PDF.",
            "Identidad entre la realización reticular y toda una teoría física.",
        ],
        "files": records,
        "portable_verification": "python3 -I -S verificar_antecedentes.py",
    }
    with manifest_path.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def verify(here):
    record = json.loads((here / "REGISTRO_PROCEDENCIA.json").read_text(encoding="utf-8"))
    rows = record["files"]
    require(len(rows) == 7 and {r["file"] for r in rows} == set(OWNERS),
            "El inventario no contiene exactamente los siete propietarios.")
    for row in rows:
        copied = here / row["file"]
        require(copied.is_file(), "Copia ausente: " + row["file"])
        require(copied.stat().st_size == row["bytes"], "Tamaño distinto: " + row["file"])
        require(digest(copied) == row["copy_sha256"] == row["source_sha256"],
                "Huella distinta: " + row["file"])
    print("PASS_CONSERVACION_FOCAL_II_REV10 files=7 binary_hashes=7 "
          "scope=source_integrity_only original_paths_required=false")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--copy-from", type=Path, help="Directorio sections de II REV10.")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    try:
        if args.copy_from is not None:
            preserve(args.copy_from, here)
        verify(here)
    except (OSError, ValueError, KeyError) as error:
        print("FAIL_CONSERVACION_FOCAL_II_REV10: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
