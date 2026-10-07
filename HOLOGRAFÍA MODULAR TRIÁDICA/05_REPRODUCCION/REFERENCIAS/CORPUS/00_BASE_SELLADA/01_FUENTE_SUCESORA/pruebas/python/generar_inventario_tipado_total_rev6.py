#!/usr/bin/env python3
"""Genera la comparación íntegra de masas y anchuras del catálogo PDG 2026.

Cada fila conserva el observable externo y lo sitúa en su dominio estructural
HMT--MD. La clasificación distingue secciones simples, multisecciones quark,
registros compuestos mesónicos y bariónicos, sectores nulos y el registro
gravitatorio externo. Masa y anchura permanecen como lectores diferentes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = SOURCE_ROOT / "datos" / "catalogo_externo_pdg_2026"
DEFAULT_CATALOG = CATALOG_DIR / "catalogo_externo_pdg_2026.csv"
DEFAULT_METADATA = CATALOG_DIR / "catalogo_externo_pdg_2026.json"
DEFAULT_OUTPUT = (
    SOURCE_ROOT
    / "manuscrito"
    / "sections"
    / "md"
    / "generated"
    / "A4_inventario_tipado_total_rev6_rows.tex"
)

FAMILY_ORDER = ("S", "Q", "M", "B", "G")
FAMILY_TITLES = {
    "S": "Familia general S de las tablas-resumen PDG",
    "Q": "Quarks (familia Q)",
    "M": "Mesones (familia M)",
    "B": "Bariones (familia B)",
    "G": "Registro gravitatorio externo (familia G)",
}
OBSERVABLE_LABELS = {"MASS": "masa", "WIDTH": "anchura"}
UNAVAILABLE = {"UNAVAILABLE", "UNAVAILABLE_IN_SNAPSHOT", "NOT_APPLICABLE", ""}

# La familia S del catálogo PDG mezcla partículas elementales y compuestos.
# Estas listas deshacen esa mezcla para que la última columna describa el
# objeto HMT--MD y no la carpeta de procedencia de la fila.
S_ELEMENTARY = {"S003", "S004", "S035", "S043", "S044", "S126"}
S_NULL = {"S000"}
S_MESONIC = {
    "S008",
    "S009",
    "S010",
    "S011",
    "S014",
    "S031",
    "S032",
    "S034",
    "S041",
    "S042",
    "S074",
    "S085",
    "S086",
    "S087",
    "S091",
}

STRUCTURAL_CODES = {
    "E": "sección simple o representación elemental",
    "N": "sector nulo o gauge",
    "Q": "multisección quark orientada por generación y color",
    "M": "registro compuesto de tipo mesónico o exótico bosónico",
    "B": "registro compuesto de tipo bariónico o exótico fermiónico",
    "G": "registro gravitatorio externo; no gravitón elemental HMT",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def latex(text: str) -> str:
    """Escapa texto plano para una celda LaTeX sin alterar su contenido."""

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    return "".join(replacements.get(char, char) for char in normalized(text))


def load_rows(catalog: Path) -> list[dict[str, str]]:
    with catalog.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(
    rows: list[dict[str, str]],
    metadata: dict[str, object],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    counts = metadata.get("counts")
    require(isinstance(counts, dict), "El JSON no contiene el bloque counts")

    required_count_keys = (
        "rows_total",
        "particle_entries",
        "particle_groups",
        "summary_observables",
        "mass_observables",
        "width_observables",
    )
    for key in required_count_keys:
        require(isinstance(counts.get(key), int), f"Falta el recuento entero {key}")

    require(len(rows) == counts["rows_total"], "No coincide rows_total")
    require(
        len({row["output_id"] for row in rows}) == len(rows),
        "Hay output_id duplicados",
    )

    identities = [
        row for row in rows if row["record_kind"] == "PARTICLE_IDENTITY"
    ]
    observables = [
        row for row in rows if row["record_kind"] == "SUMMARY_TABLE_OBSERVABLE"
    ]
    require(
        len(identities) == counts["particle_entries"],
        "No coincide particle_entries",
    )
    require(
        len(observables) == counts["summary_observables"],
        "No coincide summary_observables",
    )
    require(
        len({row["particle_group_pdgid"] for row in rows})
        == counts["particle_groups"],
        "No coincide particle_groups",
    )
    require(
        sum(row["observable_kind"] == "MASS" for row in observables)
        == counts["mass_observables"],
        "No coincide mass_observables",
    )
    require(
        sum(row["observable_kind"] == "WIDTH" for row in observables)
        == counts["width_observables"],
        "No coincide width_observables",
    )

    required_fields = (
        "output_id",
        "particle_group_pdgid",
        "particle_names",
        "object_name",
        "property_data_id",
        "observable_kind",
        "observable_description",
        "display_value",
        "unit",
        "scheme",
        "scale",
        "value_type",
        "limit_type",
        "source",
        "source_edition",
        "coverage_state",
        "hmt_mapping_status",
        "hmt_mapping",
    )
    for row in observables:
        for field in required_fields:
            require(row.get(field, "") != "", f"{row['output_id']}: falta {field}")
        require(
            row["observable_kind"] in OBSERVABLE_LABELS,
            f"{row['output_id']}: observable no tipado",
        )
        require(
            row["statute"] == "RECONOCIMIENTO_EXTERNO",
            f"{row['output_id']}: estatuto externo alterado",
        )
        require(
            row["particle_group_pdgid"][:1] in FAMILY_ORDER,
            f"{row['output_id']}: familia PDG desconocida",
        )

    observed = {
        "rows_total": len(rows),
        "particle_entries": len(identities),
        "particle_groups": len(
            {row["particle_group_pdgid"] for row in rows}
        ),
        "summary_observables": len(observables),
        "mass_observables": sum(
            row["observable_kind"] == "MASS" for row in observables
        ),
        "width_observables": sum(
            row["observable_kind"] == "WIDTH" for row in observables
        ),
        "observable_groups": len(
            {row["particle_group_pdgid"] for row in observables}
        ),
    }
    observed["identity_only_groups"] = (
        observed["particle_groups"] - observed["observable_groups"]
    )
    return observables, observed


def short_owner(mapping: str) -> str:
    if mapping.startswith("escala electrónica calibrada"):
        return "electrón central (5,5)"
    if ":" in mapping:
        return normalized(mapping.split(":", 1)[1])
    return normalized(mapping)


def structural_class(row: dict[str, str]) -> str:
    group = row["particle_group_pdgid"]
    prefix = group[0]
    if prefix == "Q":
        return "Q"
    if prefix == "M":
        return "M"
    if prefix == "B":
        return "B"
    if prefix == "G":
        return "G"
    require(prefix == "S", f"{row['output_id']}: prefijo estructural desconocido")
    if group in S_NULL:
        return "N"
    if group in S_ELEMENTARY:
        return "E"
    if group in S_MESONIC:
        return "M"
    return "B"


def structural_cell(row: dict[str, str]) -> str:
    """Código del objeto y del lector; A/H sólo matiza la comparación."""

    object_code = structural_class(row)
    reader = "m" if row["observable_kind"] == "MASS" else r"\Gamma"
    coverage = row["coverage_state"]
    comparison = ""
    if coverage == "ACTIVE":
        comparison = r"^{\mathrm A}"
    elif coverage == "HISTORICAL":
        comparison = r"^{\mathrm H}"
    else:
        require(
            coverage == "ABSENT",
            f"{row['output_id']}: cobertura externa desconocida {coverage}",
        )
    result = (
        r"\(\mathsf{" + object_code + "}_{" + reader + "}" + comparison + r"\)"
    )
    if coverage in {"ACTIVE", "HISTORICAL"}:
        result += rf"\newline {latex(short_owner(row['hmt_mapping']))}"
    return result


def uncertainty_cell(row: dict[str, str]) -> str:
    kinds = {
        "SYMMETRIC": "simétrica",
        "ASYMMETRIC": "asimétrica",
        "NOT_APPLICABLE_LIMIT": "no aplicable",
        "UNAVAILABLE": "no consignada",
    }
    kind = kinds.get(row["uncertainty_kind"], latex(row["uncertainty_kind"]))
    result = (
        rf"\textbf{{inc.:}} {kind}; "
        rf"\textbf{{tipo:}} \texttt{{{latex(row['value_type'])}}}; "
        rf"\textbf{{límite:}} \texttt{{{latex(row['limit_type'])}}}"
    )
    if row["confidence_level"] not in UNAVAILABLE:
        result += rf"; \textbf{{CL:}} {latex(row['confidence_level'])}\%"
    return result


def row_tex(row: dict[str, str]) -> str:
    observable = OBSERVABLE_LABELS[row["observable_kind"]]
    object_name = re.sub(r"\bMASS\b", "masa", row["object_name"])
    object_name = re.sub(r"\bWIDTH\b", "anchura", object_name)
    return (
        rf"\textbf{{{latex(object_name)}}}\newline "
        rf"\texttt{{{latex(row['particle_group_pdgid'])}; "
        rf"prop.\ {latex(row['property_data_id'])}}}\newline "
        rf"\emph{{Especies:}} {latex(row['particle_names'])}"
        " & "
        rf"\textbf{{{observable}}}\newline "
        rf"\texttt{{{latex(row['property_pdgid'])}}}"
        " & "
        rf"{latex(row['display_value'])}\,{latex(row['unit'])}"
        + " & "
        + uncertainty_cell(row)
        + " & "
        + structural_cell(row)
        + r"\\"
    )


def counted(number: int, singular: str, plural: str) -> str:
    noun = singular if number == 1 else plural
    return f"{number} {noun}"


def family_table(prefix: str, rows: list[dict[str, str]]) -> list[str]:
    masses = sum(row["observable_kind"] == "MASS" for row in rows)
    widths = sum(row["observable_kind"] == "WIDTH" for row in rows)
    groups = len({row["particle_group_pdgid"] for row in rows})
    label = prefix.lower()
    lines = [
        rf"\subsection{{{FAMILY_TITLES[prefix]}}}",
        "",
        r"{\scriptsize",
        r"\setlength{\tabcolsep}{2pt}",
        r"\renewcommand{\arraystretch}{1.08}",
        (
            r"\begin{longtable}{@{}"
            r"L{0.34\textwidth}L{0.10\textwidth}L{0.17\textwidth}"
            r"L{0.20\textwidth}L{0.09\textwidth}@{}}"
        ),
        (
            rf"\caption{{Inventario íntegro PDG--{prefix}: "
            rf"{counted(len(rows), 'observable', 'observables')} en "
            rf"{counted(groups, 'grupo', 'grupos')} "
            rf"({counted(masses, 'masa', 'masas')} y "
            rf"{counted(widths, 'anchura', 'anchuras')}).}}"
        ),
        rf"\label{{tab:inventario-tipado-pdg-{label}-rev6}}\\",
        r"\toprule",
        (
            r"Grupo, objeto y especies & Observable & Valor y unidad & "
            r"Incertidumbre, tipo y límite & Objeto\newline lector\\"
        ),
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        (
            r"Grupo, objeto y especies & Observable & Valor y unidad & "
            r"Incertidumbre, tipo y límite & Objeto\newline lector\\"
        ),
        r"\midrule",
        r"\endhead",
        r"\midrule",
        r"\multicolumn{5}{r}{\emph{continúa en la página siguiente}}\\",
        r"\endfoot",
        r"\bottomrule",
        r"\endlastfoot",
    ]
    lines.extend(row_tex(row) for row in rows)
    lines.extend([r"\end{longtable}", r"}", ""])
    return lines


def generate(
    observables: list[dict[str, str]],
    counts: dict[str, int],
    catalog_digest: str,
) -> str:
    order = {prefix: index for index, prefix in enumerate(FAMILY_ORDER)}
    observables = sorted(
        observables,
        key=lambda row: (
            order[row["particle_group_pdgid"][0]],
            row["particle_group_pdgid"],
            0 if row["observable_kind"] == "MASS" else 1,
            row["object_name"],
            row["property_data_id"],
        ),
    )

    coverage = Counter(row["coverage_state"] for row in observables)
    structural = Counter(structural_class(row) for row in observables)
    lines = [
        "% GENERADO MECÁNICAMENTE: no editar a mano.",
        "% Fuente: catalogo_externo_pdg_2026.csv",
        f"% SHA-256 fuente: {catalog_digest}",
        (
            "% Recuentos: "
            f"{counts['summary_observables']} observables; "
            f"{counts['mass_observables']} masas; "
            f"{counts['width_observables']} anchuras; "
            f"{coverage['ACTIVE']} ACTIVE; "
            f"{coverage['HISTORICAL']} HISTORICAL; "
            + "; ".join(
                f"{structural[code]} {code}" for code in STRUCTURAL_CODES
            )
            + "."
        ),
        "",
    ]
    for prefix in FAMILY_ORDER:
        family = [
            row
            for row in observables
            if row["particle_group_pdgid"].startswith(prefix)
        ]
        require(family, f"No hay filas para la familia {prefix}")
        lines.extend(family_table(prefix, family))
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera las 855 filas LaTeX de masa/anchura para REV.6."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    require(args.catalog.is_file(), f"No existe el catálogo: {args.catalog}")
    require(args.metadata.is_file(), f"No existen metadatos: {args.metadata}")

    rows = load_rows(args.catalog)
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    observables, counts = validate(rows, metadata)
    output = generate(observables, counts, sha256(args.catalog))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(output)

    coverage = Counter(row["coverage_state"] for row in observables)
    print(
        "PASS_INVENTARIO_TIPADO_TOTAL_REV6 "
        f"rows={counts['rows_total']} "
        f"identities={counts['particle_entries']} "
        f"groups={counts['particle_groups']} "
        f"observable_groups={counts['observable_groups']} "
        f"identity_only_groups={counts['identity_only_groups']} "
        f"observables={counts['summary_observables']} "
        f"masses={counts['mass_observables']} "
        f"widths={counts['width_observables']} "
        f"active={coverage['ACTIVE']} "
        f"historical={coverage['HISTORICAL']} "
        f"external_comparison_only={coverage['ABSENT']} "
        f"output_sha256={hashlib.sha256(output.encode('utf-8')).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"FAIL_INVENTARIO_TIPADO_TOTAL_REV6: {error}", file=sys.stderr)
        raise SystemExit(1)
