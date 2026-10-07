#!/usr/bin/env python3
"""Genera y verifica la matriz tipada entre dos inventarios TPK no biyectivos."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCAL_CATALOG = (
    ROOT / "gestion" / "trazabilidad_tpk"
    / "CATALOGO_FUNCIONAL_APP_TRIT_TPK_171.tsv"
)
CANONICAL = ROOT / "datos" / "registro_operadores_tpk.json"
MATRIX = ROOT / "gestion" / "MATRIZ_TRAZABILIDAD_TPK_87_34_REV11.tsv"
CERTIFICATE = ROOT / "certificados" / "trazabilidad_tpk_87_34_rev11.json"

EXPECTED_CATALOG_SHA256 = (
    "177a15755ddbc8442d8f6a072f7aeaae4b3a822517cad435273d293066d5b90c"
)
EXPECTED_CANONICAL_SHA256 = (
    "04c7a32ac099b5a162cb6e73eec08e745537184f6d60527b208d6b83d512e951"
)

# Correspondencias cuya identidad o relación está sustentada por tipo y
# propietario. El resto conserva su fila histórica sin forzar equivalencia.
SAFE_LINKS = {
    "TPK-003": ("IDENTIDAD", ["TPK_ENRICHED_STATE"]),
    "TPK-005": ("IDENTIDAD", ["CARDINAL_TRANSLATIONS"]),
    "TPK-007": ("COMPONENTE_DE", ["TPK_LOCAL_FEEDBACK"]),
    "TPK-009": ("IDENTIDAD", ["TPK_MIN_TWO_CURSOR"]),
    "TPK-013": ("IDENTIDAD", ["TRIT_RHO3"]),
    "TPK-016": ("IDENTIDAD", ["BASE1000_CONCAT"]),
    "TPK-017": ("IDENTIDAD", ["K27_TRANSPORT_LOOP"]),
    "TPK-020": ("COMPONENTE_DE", ["R12_DODECAPHASE"]),
    "TPK-022": ("COMPONENTE_DE", ["R12_DODECAPHASE"]),
    "TPK-023": ("IDENTIDAD", ["OBSERVABLE_TWO_CURSOR_CHRONOLOGY"]),
    "TPK-047": ("IDENTIDAD", ["EF_G9_EXTENSION_RELATION"]),
    "TPK-050": ("COMPONENTE_DE", ["EF_G9_EXTENSION_RELATION"]),
    "TPK-051": ("TESTIGO_DE", ["EF_G9_EXTENSION_RELATION"]),
    "TPK-052": ("TESTIGO_DE", ["EF_G9_EXTENSION_RELATION"]),
    "TPK-053": ("IDENTIDAD", ["HMT_NUMBER_INVERSE_LIMIT"]),
    "TPK-057": ("COMPONENTE_DE", ["NONADIC_MONODROMY"]),
    "TPK-058": ("IDENTIDAD", ["NONADIC_MONODROMY"]),
    "TPK-059": ("COROLARIO_DE", ["NONADIC_MONODROMY"]),
    "TPK-069": ("IDENTIDAD", ["THREE_CHANNEL_TWENTY_BLOCK_EXTENSION"]),
    "TPK-074": ("COMPONENTE_DE", ["ROUTE_LEDGER_CHARACTER"]),
    "TPK-075": ("TESTIGO_DE", ["NONADIC_PARTICLE_FAMILY_ATLAS"]),
    "TPK-076": ("COMPONENTE_DE", ["NONADIC_PARTICLE_FAMILY_ATLAS"]),
    "TPK-083": ("INTERFAZ", ["ROUTE_LEDGER_CHARACTER"]),
    "TPK-085": ("TESTIGO_DE", ["EF_G9_EXTENSION_RELATION"]),
    "TPK-086": ("TESTIGO_DE", ["EF_G9_EXTENSION_RELATION"]),
}

NO_OPERATOR_IDS = {
    "TPK-001", "TPK-002", "TPK-041", "TPK-045", "TPK-046",
    "TPK-060", "TPK-061", "TPK-062", "TPK-079", "TPK-082",
    "TPK-084", "TPK-087",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def active_residence(identifier: str) -> str:
    number = int(identifier.split("-")[1])
    if number <= 12:
        return "manuscrito/sections/hmt/03h_arbol_operatorio_tpk_rev11.tex"
    if number <= 28:
        return "manuscrito/sections/hmt/03i_inventario_operatorio_tpk_rev11.tex"
    if number <= 34:
        return "manuscrito/sections/hmt/03g_ciclo_dodecafasico_tpk_rev7.tex"
    if number <= 73:
        return "manuscrito/sections/hmt/05_tpk_numero_medicion.tex"
    if number <= 77:
        return "manuscrito/sections/md/05b_extension_superviviente_caracter.tex"
    if number <= 81:
        return "manuscrito/sections/hmt/07_nucleo_hensel_witt.tex"
    if number == 82:
        return "manuscrito/sections/hmt/19a_constantes_torre_triadica_rev6.tex"
    if number == 83:
        return "manuscrito/sections/md/05b_extension_superviviente_caracter.tex"
    if number == 84:
        return "manuscrito/sections/md/11h_hoja_comun_hidrodinamica_yang_mills.tex"
    return (
        "testigos_integracion/ley_masas_hmt_md_2026-07-30/certificados/"
        "ley_nueve_puertas_2026-07-30/PRUEBA_VERIFICABLE.md"
    )


def relation_for(row: dict[str, str]) -> tuple[str, list[str]]:
    identifier = row["id"]
    if identifier in SAFE_LINKS:
        return SAFE_LINKS[identifier]
    if identifier in NO_OPERATOR_IDS:
        return "NO_OPERADOR", []
    if row["familia_funcional"] == "INTERFAZ":
        return "INTERFAZ_SIN_EQUIVALENCIA_UNIVOCA", []
    if row["familia_funcional"] in {
        "CENSO", "CERTIFICADO", "FALSADOR", "HISTORIA", "METODO",
        "PROGRAMA", "PUBLICACION", "TIPADO",
    }:
        return "TESTIGO_O_CONTROL_SIN_EQUIVALENCIA_UNIVOCA", []
    return "SUBOBJETO_TPK_SIN_EQUIVALENCIA_UNIVOCA", []


def load_catalog() -> list[dict[str, str]]:
    with LOCAL_CATALOG.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    return [row for row in rows if row["objeto"] == "TPK"]


def generate() -> dict[str, object]:
    catalog_hash = sha256(LOCAL_CATALOG)
    canonical_hash = sha256(CANONICAL)
    if catalog_hash != EXPECTED_CATALOG_SHA256:
        raise SystemExit(f"SHA catálogo inesperado: {catalog_hash}")
    if canonical_hash != EXPECTED_CANONICAL_SHA256:
        raise SystemExit(f"SHA registro canónico inesperado: {canonical_hash}")

    historical = load_catalog()
    expected_ids = [f"TPK-{number:03d}" for number in range(1, 88)]
    found_ids = [row["id"] for row in historical]
    if found_ids != expected_ids:
        raise SystemExit("El catálogo TPK no contiene TPK-001…TPK-087 en orden.")

    canonical_payload = json.loads(CANONICAL.read_text(encoding="utf-8"))
    canonical_rows = canonical_payload["operators"]
    canonical_by_id = {row["id"]: row for row in canonical_rows}
    if len(canonical_rows) != 34 or len(canonical_by_id) != 34:
        raise SystemExit("El registro canónico no contiene 34 IDs únicos.")

    headers = [
        "historical_id", "parent_path", "historical_name", "relation",
        "canonical_ids", "domain", "codomain", "original_source_ids",
        "original_catalog_sha256", "active_residence_primary",
        "historical_status", "canonical_status", "mapping_basis",
        "disposition",
    ]
    MATRIX.parent.mkdir(parents=True, exist_ok=True)
    linked = 0
    with MATRIX.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers, delimiter="\t")
        writer.writeheader()
        for row in historical:
            relation, canonical_ids = relation_for(row)
            for identifier in canonical_ids:
                if identifier not in canonical_by_id:
                    raise SystemExit(f"ID canónico inexistente: {identifier}")
            residence = active_residence(row["id"])
            if not (ROOT / residence).exists():
                raise SystemExit(f"Residencia activa inexistente: {residence}")
            if canonical_ids:
                linked += 1
                canonical_status = "|".join(
                    canonical_by_id[x]["status"] for x in canonical_ids
                )
                basis = (
                    "correspondencia explícita por nombre funcional, dominio, "
                    "codominio y propietario; sin emparejamiento difuso"
                )
            else:
                canonical_status = "NO_APLICA_O_NO_HAY_ID_CANONICO_UNIVOCO"
                basis = (
                    "fila histórica conservada con su tipo documental; "
                    "no se fuerza una equivalencia con el registro de 34"
                )
            writer.writerow({
                "historical_id": row["id"],
                "parent_path": f"TPK/{row['familia_funcional']}",
                "historical_name": row["nombre_funcional"],
                "relation": relation,
                "canonical_ids": "|".join(canonical_ids),
                "domain": row["dominio_entrada"],
                "codomain": row["salida_o_invariante"],
                "original_source_ids": row["fuentes"],
                "original_catalog_sha256": catalog_hash,
                "active_residence_primary": residence,
                "historical_status": (
                    f"{row['estatuto_en_originales']}|{row['estatuto_actual']}"
                ),
                "canonical_status": canonical_status,
                "mapping_basis": basis,
                "disposition": "CONSERVAR_CON_TIPO_Y_RESIDENCIA",
            })

    certificate = {
        "schema": "HMT_TPK_TRACEABILITY_87_34_REV11_V1",
        "catalog_sha256": catalog_hash,
        "canonical_registry_sha256": canonical_hash,
        "matrix_sha256": sha256(MATRIX),
        "historical_tpk_rows": len(historical),
        "historical_ids": {"first": found_ids[0], "last": found_ids[-1]},
        "canonical_operator_rows": len(canonical_rows),
        "rows_with_explicit_canonical_relation": linked,
        "rows_preserved_without_forced_equivalence": len(historical) - linked,
        "assertion": (
            "Los inventarios 87 y 34 tienen universos distintos; la matriz "
            "declara relaciones tipadas y no presupone biyección ni cociente."
        ),
        "status": "PASS_TPK_TRACEABILITY_TYPED_NONBIJECTIVE",
    }
    CERTIFICATE.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return certificate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ingest-catalog",
        type=Path,
        help="Copia byte a byte el catálogo de 87 filas a la residencia local.",
    )
    args = parser.parse_args()
    if args.ingest_catalog:
        source = args.ingest_catalog.resolve()
        if sha256(source) != EXPECTED_CATALOG_SHA256:
            raise SystemExit("El catálogo de ingesta no posee la huella esperada.")
        LOCAL_CATALOG.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, LOCAL_CATALOG)
    if not LOCAL_CATALOG.exists():
        raise SystemExit("Falta el catálogo local; use --ingest-catalog una vez.")
    certificate = generate()
    print(certificate["status"])
    print(json.dumps(certificate, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
