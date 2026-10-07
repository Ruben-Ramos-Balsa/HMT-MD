#!/usr/bin/env python3
"""Verifica el paquete OBS-02 de 25 de junio sin ejecutar su generador.

El certificado comprueba integridad, asignaciones nominales, evaluación numérica y
la ausencia de fórmulas dentro del XLSX. No certifica que el propio paquete derive
los pares (n_A, s_C) desde las rutas: el catálogo los declara explícitamente.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import math
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
PACKAGE = (
    ROOT
    / "02_LECTURA"
    / "ingesta_usuario_2026-07-18"
    / "__extraido__"
    / "25junio-matema_avanzada_expli"
    / "25junio-matema avanzada expli"
    / "__extraido__"
    / "HMT_MD_OBS_02_package"
)

EXPECTED_SHA256 = {
    "HMT_MD_OBS_02_masses_CKM_muon.xlsx":
        "4616cc745151507d0b2a0649a19732e850c7158d3be2ae7647cbb9b0b76720b2",
    "hmt_md_mass_table.csv":
        "74c917f34b7b4307902c66b64bd40b75b1dfe0e1e67a282132cc42eec3c6e894",
    "hmt_md_ckm_muon.csv":
        "c6b70f0152b92811135fc5e13b85c896df66c6915d96f8cf32822956de13dd37",
    "MD_OBS_02_ventana.tex":
        "bf367139aa903180c640de57d2281231202147733a96d5504a8ef4ac17cb5fe0",
    "build_hmt_obs.py":
        "fb2d87786019591005a02d2dfc043508b5171dcf71d322133bbd5e2f3837de9e",
}

EXPECTED_FLAVORS = {
    "u": (11, 7),
    "d": (17, 8),
    "s": (41, -3),
    "c": (61, 8),
    "b": (71, -5),
    "t": (100, -1),
}

COMPARISON = (
    ROOT
    / "PUBLICACION_HMT"
    / "LEY_DE_MASAS_HMT_MD_2026-07-30"
    / "datos"
    / "TABLA_COMPARATIVA_12_ESPECIES_RECUPERADA_2026-07-30.csv"
)

ROUTE_CATALOG_324 = (
    ROOT
    / "02_LECTURA"
    / "ingesta_usuario_2026-07-19_enero_stale"
    / "EXTRACTED"
    / "2026-01-18"
    / "18-enero-26"
    / "ct108_routes_masses_full_2026-01-19.csv"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def close(actual: float, expected: float, *, atol: float = 1e-12) -> None:
    if not math.isclose(actual, expected, rel_tol=1e-12, abs_tol=atol):
        raise AssertionError(f"{actual!r} != {expected!r}")


def assignments(tree: ast.Module) -> dict[str, ast.AST]:
    result: dict[str, ast.AST] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                result[target.id] = node.value
    return result


def read_ckm_and_muon(path: Path) -> tuple[dict[str, float], dict[str, float]]:
    rows = list(csv.reader(path.open(encoding="utf-8", newline="")))
    divider = rows.index([])
    ckm = {row[0]: float(row[2]) for row in rows[1:divider]}
    muon = {row[0]: float(row[1]) for row in rows[divider + 2 :]}
    return ckm, muon


def workbook_has_formula(path: Path) -> tuple[list[str], bool]:
    with zipfile.ZipFile(path) as archive:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        names = [
            node.attrib["name"]
            for node in workbook.iter()
            if node.tag.endswith("}sheet")
        ]
        formulas = False
        for member in archive.namelist():
            if not member.startswith("xl/worksheets/sheet") or not member.endswith(".xml"):
                continue
            sheet = ET.fromstring(archive.read(member))
            if any(node.tag.endswith("}f") for node in sheet.iter()):
                formulas = True
                break
    return names, formulas


def main() -> None:
    if not PACKAGE.is_dir():
        raise AssertionError(f"No existe el paquete ingerido: {PACKAGE}")

    for name, expected in EXPECTED_SHA256.items():
        actual = sha256(PACKAGE / name)
        if actual != expected:
            raise AssertionError(f"SHA-256 distinto para {name}: {actual}")

    source = (PACKAGE / "build_hmt_obs.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    values = assignments(tree)
    a_deg = float(ast.literal_eval(values["A_DEG"]))
    cstar_deg = float(ast.literal_eval(values["CSTAR_DEG"]))
    delta4_rad = float(ast.literal_eval(values["DELTA4_RAD"]))
    m_e = float(ast.literal_eval(values["M_E"]))
    catalog = ast.literal_eval(values["CATALOG"])

    if len(catalog) != 12:
        raise AssertionError(f"El catálogo no tiene 12 especies: {len(catalog)}")
    for flavor, expected_pair in EXPECTED_FLAVORS.items():
        pair = tuple(catalog[flavor][2:4])
        if pair != expected_pair:
            raise AssertionError(f"Asignación de {flavor}: {pair} != {expected_pair}")

    with (PACKAGE / "hmt_md_mass_table.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        mass_rows = list(csv.DictReader(stream))
    if len(mass_rows) != 12:
        raise AssertionError(f"La tabla no tiene 12 filas: {len(mass_rows)}")

    a_rad = math.radians(a_deg)
    cstar_rad = math.radians(cstar_deg)
    relative_errors: list[float] = []
    seen: set[str] = set()
    for row in mass_rows:
        key = row["key"]
        seen.add(key)
        n_a = int(row["n_A"])
        s_c = int(row["s_C"])
        if (n_a, s_c) != tuple(catalog[key][2:4]):
            raise AssertionError(f"CSV y catálogo discrepan para {key}")
        exponent = n_a * a_rad + (s_c / 6.0) * cstar_rad
        predicted = m_e * math.exp(exponent)
        reference = float(row["ref_MeV"])
        relative_error = abs(predicted - reference) / reference
        close(exponent, float(row["E"]))
        close(predicted, float(row["m_HMT_MeV"]), atol=1e-9)
        close(relative_error, float(row["rel_error"]))
        relative_errors.append(relative_error)

    if seen != set(catalog):
        raise AssertionError("La tabla y el catálogo no contienen las mismas especies")
    if max(relative_errors) >= 0.003:
        raise AssertionError(f"Error relativo máximo >= 0.3 %: {max(relative_errors)}")

    ckm, muon = read_ckm_and_muon(PACKAGE / "hmt_md_ckm_muon.csv")
    h = cstar_deg / 6.0
    delta4_deg = math.degrees(delta4_rad)
    theta12 = 2 * a_deg - 5 * h + 28 * delta4_deg
    theta23 = 7 * h - (25 / 2) * delta4_deg
    theta13 = a_deg - 20 * h - (2 / 3) * delta4_deg
    delta_ckm = 9 * a_deg

    r12, r23, r13, rdelta = map(
        math.radians, (theta12, theta23, theta13, delta_ckm)
    )
    jarlskog = (
        math.cos(r12)
        * math.cos(r23)
        * math.cos(r13) ** 2
        * math.sin(r12)
        * math.sin(r23)
        * math.sin(r13)
        * math.sin(rdelta)
    )
    for key, value in {
        "θ12": theta12,
        "θ23": theta23,
        "θ13": theta13,
        "δ_CKM": delta_ckm,
        "J": jarlskog,
    }.items():
        close(value, ckm[key])

    phi = (1 + math.sqrt(5)) / 2
    alpha = a_deg / 1000.0
    a_mu = (
        alpha / (2 * math.pi)
        + alpha * (phi - 1) / 1000.0
        + alpha**2 / (1000.0 * 55.0)
    )
    sigma = math.sqrt((1.14e-10) ** 2 + (9.1e-11) ** 2)
    for key, value in {
        "a_mu HMT": a_mu,
        "g_mu HMT": 2 * (1 + a_mu),
        "difference": a_mu - muon["a_mu Fermilab 2025"],
        "sigma_exp": sigma,
        "sigma units": (a_mu - muon["a_mu Fermilab 2025"]) / sigma,
    }.items():
        close(value, muon[key], atol=1e-15)

    sheets, has_formula = workbook_has_formula(
        PACKAGE / "HMT_MD_OBS_02_masses_CKM_muon.xlsx"
    )
    if sheets != ["Inputs", "Masses", "CKM_Muon", "Notes"]:
        raise AssertionError(f"Hojas XLSX inesperadas: {sheets}")
    if has_formula:
        raise AssertionError("El XLSX contiene fórmulas; se esperaba una exportación estática")

    with COMPARISON.open(encoding="utf-8", newline="") as stream:
        comparison_rows = list(csv.DictReader(stream))
    if len(comparison_rows) != 12:
        raise AssertionError("La tabla comparativa recuperada no tiene doce filas")
    obs_by_key = {row["key"]: row for row in mass_rows}
    internal_electron = 0.51099892248806607250987087719134943763
    for row in comparison_rows:
        key = row["species"]
        source_row = obs_by_key[key]
        n_a = int(row["n_A"])
        s_c = int(row["s_C"])
        if (n_a, s_c) != (int(source_row["n_A"]), int(source_row["s_C"])):
            raise AssertionError(f"Firma discrepante en la tabla comparativa: {key}")
        if int(row["W_plus"]) != 6 * n_a + s_c:
            raise AssertionError(f"W_plus incorrecto para {key}")
        if int(row["W_minus"]) != 6 * n_a - s_c:
            raise AssertionError(f"W_minus incorrecto para {key}")
        close(
            float(row["m_base_OBS02_ext_anchor_MeV"]),
            float(source_row["m_HMT_MeV"]),
            atol=1e-9,
        )
        internal_mass = internal_electron * math.exp(float(source_row["E"]))
        close(
            float(row["m_base_HMT_internal_scale_MeV"]),
            internal_mass,
            atol=1e-6,
        )
        internal_error = (
            internal_mass - float(row["reference_in_archive_MeV"])
        ) / float(row["reference_in_archive_MeV"])
        close(float(row["signed_rel_error_HMT_internal"]), internal_error)

    with ROUTE_CATALOG_324.open(encoding="utf-8-sig", newline="") as stream:
        route_rows = list(csv.DictReader(stream))
    route_signatures = {
        (
            row["nA"],
            row["sC"],
            row["K"],
            row["nu120"],
            row["nu270_Q3"],
        )
        for row in route_rows
    }
    route_cells = {(row["r"], row["c"]) for row in route_rows}
    if (len(route_rows), len(route_cells), len(route_signatures)) != (324, 81, 53):
        raise AssertionError(
            "Censo del catálogo CT-108 distinto de 324 rutas, 81 celdas y 53 firmas"
        )

    mean_error = sum(relative_errors) / len(relative_errors)
    print("PASS_OBS02_MASAS_SABORES_CKM_G2_2026_07_30")
    print(
        "species=12 flavors=6 "
        f"max_rel_error={max(relative_errors):.12f} "
        f"mean_rel_error={mean_error:.12f} "
        "xlsx_formula_cells=0 routes=324 cells=81 route_signatures=53"
    )


if __name__ == "__main__":
    main()
