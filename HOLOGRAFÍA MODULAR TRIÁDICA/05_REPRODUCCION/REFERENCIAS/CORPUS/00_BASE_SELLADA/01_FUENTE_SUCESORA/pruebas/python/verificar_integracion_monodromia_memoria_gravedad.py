#!/usr/bin/env python3
"""Verifica la integración pública del delta monodromía--memoria--gravedad.

La puerta coteja la matriz editorial 30/30 con sus residencias activas,
recalcula los censos finitos principales y emite un certificado
determinista. No utiliza ``assert`` para conservar todas las comprobaciones
bajo ``python -O``.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = (
    ROOT
    / "auditoria"
    / "MATRIZ_INTEGRACION_MONODROMIA_MEMORIA_GRAVEDAD_30_30.tsv"
)
CERTIFICATE = (
    ROOT
    / "certificados"
    / "integracion_monodromia_memoria_gravedad.json"
)

EXPECTED_COLUMNS = (
    "id",
    "residencia_destino",
    "localizador_lineas",
    "formulacion_integrada",
    "dominio_codominio",
    "hipotesis_premisas",
    "prueba_o_certificado",
    "estatuto_procedencia",
    "fuerza_probatoria",
    "falsador_control_negativo",
    "fuente_sustituida_o_remision",
    "accion_editorial",
    "duplicacion_evitable",
    "no_regresion",
    "estado",
)

FOCAL_RANGES = {
    "MON-001": "317-388",
    "MON-002": "330-354",
    "MON-003": "390-417",
    "SPEC-001": "182-300",
    "CM-002": "126-183",
    "CM-003": "185-219",
    "GRAV-004": "146-300",
    "GRAV-005": "350-383",
    "COS-001": "86-117",
    "COS-002": "118-200",
    "COS-003": "202-268",
}

NO_CHANGE_IDS = {
    "CAR-001",
    "MEM-001",
    "CM-001",
    "D54-001",
    "D54-002",
    "D54-003",
    "D54-004",
    "WAV-001",
    "WAV-002",
    "WAV-003",
    "GRAV-001",
    "GRAV-002",
    "GRAV-003",
    "GRAV-005",
}

SOURCE_PATHS = (
    "manuscrito/main.tex",
    "manuscrito/sections/hmt/05_tpk_numero_medicion.tex",
    "manuscrito/sections/hmt/09b_algebras_cuadraticas.tex",
    "manuscrito/sections/hmt/17_sintesis.tex",
    "manuscrito/sections/md/06c_sectores_topologicos_no_omision.tex",
    "manuscrito/sections/md/10c_puente_retorno_holonomia_cartan.tex",
    "manuscrito/sections/md/11b_gravedad_sin_graviton_fundamental.tex",
    "manuscrito/sections/md/11c_transductor_gravitatorio_G.tex",
    "manuscrito/sections/md/11g_perspectivas_cosmologicas_frontera.tex",
    "manuscrito/sections/md/12_sintesis.tex",
    "manuscrito/backmatter/C_huecos_reales.tex",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_range(value: str) -> tuple[int, int]:
    parts = value.split("-", maxsplit=1)
    require(len(parts) == 2, f"rango inválido: {value}")
    start, end = (int(part) for part in parts)
    require(1 <= start <= end, f"rango no ordenado: {value}")
    return start, end


def source_span(row: dict[str, str]) -> str:
    path = ROOT / row["residencia_destino"]
    require(path.is_file(), f"residencia inexistente: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    start, end = parse_range(row["localizador_lineas"])
    require(end <= len(lines), f"rango fuera de archivo: {row['id']}")
    return "\n".join(lines[start - 1 : end])


def cm(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((-value) % 3 for value in reversed(word))


def rotate_six(word: tuple[int, ...]) -> tuple[int, ...]:
    return word[-6:] + word[:-6]


def route_counters(start: int, length: int) -> tuple[int, int]:
    modes = ("S", "P", "P", "S", "P", "P", "S", "P", "P")
    turns = 0
    switches = 0
    for offset in range(length):
        tick = (start + offset) % 108
        if (tick + 1) % 27 == 0:
            turns += 1
        if modes[tick % 9] != modes[(tick + 1) % 9]:
            switches += 1
    return turns, switches


def multiply_mod3(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    size = len(left)
    return tuple(
        tuple(
            sum(
                left[row][index] * right[index][column]
                for index in range(size)
            )
            % 3
            for column in range(size)
        )
        for row in range(size)
    )


def main() -> int:
    require(MATRIX.is_file(), "falta la matriz integrada 30/30")
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        require(tuple(reader.fieldnames or ()) == EXPECTED_COLUMNS, "15 columnas")
        rows = list(reader)

    require(len(rows) == 30, "la matriz no contiene treinta filas")
    by_id = {row["id"]: row for row in rows}
    require(len(by_id) == 30, "identificadores duplicados")
    require(
        {
            row["id"]
            for row in rows
            if row["estado"] == "NO_CAMBIO_VERIFICADO"
        }
        == NO_CHANGE_IDS,
        "inventario de catorce NO_CAMBIO",
    )
    require(
        all(
            row["estado"]
            in {
                "INTEGRADO",
                "NO_CAMBIO_VERIFICADO",
                "REMISION_SIN_DUPLICAR",
                "BLOQUEADO_CON_MOTIVO",
            }
            for row in rows
        ),
        "estado editorial desconocido",
    )
    require(
        not any(row["estado"] == "BLOQUEADO_CON_MOTIVO" for row in rows),
        "persisten filas bloqueadas",
    )

    spans = {row["id"]: source_span(row) for row in rows}
    for identifier, expected in FOCAL_RANGES.items():
        require(
            by_id[identifier]["localizador_lineas"] == expected,
            f"localizador desfasado: {identifier}",
        )

    require(
        r"c:\operatorname{Mor}(\mathcal P)\longrightarrow M" in spans["MON-001"],
        "tipo del cociclo sobre flechas",
    )
    require(
        r"c(\operatorname{id}_x)=0" in spans["MON-001"],
        "identidad del cociclo",
    )
    require(
        "isomorfismo lineal" in spans["CM-002"]
        and r"-1\longmapsto2" in spans["CM-002"],
        "estructura vectorial del estrato fijo",
    )
    require(
        r"W_{27}\hookrightarrow\operatorname{Fix}(C_M)" in spans["CM-003"],
        "inclusión canónica W27",
    )
    require(
        r"\emph{finito}" in spans["SPEC-001"]
        and "autoadjunta analítica" in spans["SPEC-001"],
        "hipótesis funcionales del control espectral",
    )
    require(
        "EXACTO_INTERNO" in by_id["SPEC-001"]["fuerza_probatoria"]
        and "PROGRAMA_ABIERTO" in by_id["SPEC-001"]["fuerza_probatoria"],
        "doble estatuto de SPEC-001",
    )
    require(
        "si U es unitario, la norma se conserva"
        in by_id["WAV-001"]["formulacion_integrada"],
        "suficiencia de unitariedad en WAV-001",
    )
    require(
        "Hamiltoniano espectral" in by_id["WAV-003"]["hipotesis_premisas"]
        and "energía y número" in by_id["WAV-003"]["hipotesis_premisas"],
        "premisas térmicas de WAV-003",
    )

    hmt_synthesis = (
        ROOT / "manuscrito/sections/hmt/17_sintesis.tex"
    ).read_text(encoding="utf-8")
    require(
        "Suma de alternativas, producto de transportes y gravedad"
        in hmt_synthesis
        and "homomorfismo de semianillos" in hmt_synthesis,
        "control suma/producto--gravedad",
    )

    gravitation = (
        ROOT / "manuscrito/sections/md/11c_transductor_gravitatorio_G.tex"
    ).read_text(encoding="utf-8")
    require(
        gravitation.find(r"\label{eq:fraccion-angular-orientada-G}")
        < gravitation.find(r"\theta_G^{\rm spec}"),
        "delta_theta debe preceder a la plantilla",
    )
    cosmology = (
        ROOT
        / "manuscrito/sections/md/11g_perspectivas_cosmologicas_frontera.tex"
    ).read_text(encoding="utf-8")
    require(r"\textsc{programa abierto}" in cosmology, "estatuto cosmológico")
    require(
        r"\label{prop:tres-foliaciones-de-sitter}" in cosmology
        and "teorema clásico exacto" in cosmology,
        "separación del teorema clásico de de Sitter",
    )
    program_start = cosmology.find(r"\section{Universo con frontera}")
    require(program_start >= 0, "falta el inicio del programa cosmológico")
    program_region = cosmology[program_start:]
    require(
        not any(
            token in program_region
            for token in (
                r"\begin{theorem}",
                r"\begin{lemma}",
                r"\begin{proposition}",
                r"\begin{corollary}",
            )
        ),
        "el programa cosmológico no puede promoverse a teorema cerrado",
    )

    for phase in range(108):
        orbit = tuple((phase + 27 * power) % 108 for power in range(5))
        require(len(set(orbit[:4])) == 4, "orden observable inferior a cuatro")
        require(orbit[4] == phase, "K27 no cierra a la cuarta")
        require(route_counters(phase, 27) == (1, 18), "contador K27")
        require(route_counters(phase, 108) == (4, 72), "contador C108")

    fixed = 0
    fixed_period_six = 0
    for word in itertools.product(range(3), repeat=12):
        if cm(word) == word:
            fixed += 1
            if rotate_six(word) == word:
                fixed_period_six += 1
    require(fixed == 729, "censo Fix(C_M)")
    require(fixed_period_six == 27, "censo W27")

    minus_identity = tuple(
        tuple(2 if row == column else 0 for column in range(3))
        for row in range(3)
    )
    roots_dimension_three = 0
    for entries in itertools.product(range(3), repeat=9):
        candidate = tuple(
            tuple(entries[3 * row + column] for column in range(3))
            for row in range(3)
        )
        if multiply_mod3(candidate, candidate) == minus_identity:
            roots_dimension_three += 1
    require(roots_dimension_three == 0, "obstrucción impar de W27")

    additive = sum(
        (value % 9 if value % 9 else 9)
        for value in (i + j for i in range(1, 10) for j in range(1, 10))
    )
    multiplicative = sum(
        (value % 9 if value % 9 else 9)
        for value in (i * j for i in range(1, 10) for j in range(1, 10))
    )
    require((additive, multiplicative) == (405, 459), "censos APP")
    require(multiplicative - additive == 54, "defecto APP 54")
    require(54 * (5 * 729 + 1) == 196_884, "factor Moonshine")
    require(315 + 271 + 161 - 3 == 744 == 729 + 15, "normalización 744")

    source_hashes = {
        relative: digest(ROOT / relative)
        for relative in SOURCE_PATHS
    }
    payload = {
        "schema": "hmt.integracion_monodromia_memoria_gravedad.v1",
        "status": "PASS_INTEGRACION_MONODROMIA_MEMORIA_GRAVEDAD",
        "matrix": MATRIX.relative_to(ROOT).as_posix(),
        "matrix_sha256": digest(MATRIX),
        "rows": len(rows),
        "columns": len(EXPECTED_COLUMNS),
        "no_change": len(NO_CHANGE_IDS),
        "focal_ranges": FOCAL_RANGES,
        "fixed_cm": fixed,
        "fixed_cm_period_six": fixed_period_six,
        "roots_minus_one_dimension_three": roots_dimension_three,
        "source_sha256": source_hashes,
        "assert_nodes": 0,
        "optimization_invariant": True,
    }
    encoded = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(encoded)
    print(
        "PASS_INTEGRACION_MONODROMIA_MEMORIA_GRAVEDAD "
        f"rows={len(rows)} fixed={fixed} fixed_per6={fixed_period_six}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
