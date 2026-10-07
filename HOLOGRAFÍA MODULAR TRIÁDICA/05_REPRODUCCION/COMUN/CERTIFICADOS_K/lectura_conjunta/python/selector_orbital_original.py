#!/usr/bin/env python3
"""Selector orbital etiquetado en la orbita 4--8--12.

El certificado construye primero una familia decimal C_dec de 19 446 estados
a partir de W24, el conjunto historico no ordenado S8 y el panel funcional de
nueve fronteras.  No recibe K, U12, alpha, CODATA ni los nueve residuos del
sello.

La traslacion +4 sobre Z/12 se descompone en cuatro orbitas.  Las tres primeras
contienen respectivamente las raices decimales 1, 2 y 3; la cuarta,
(4,8,12), es la unica sin una de esas raices.  En sus dos aristas internas se
impone una condicion de procedencia, no una coincidencia de cifras: el bloque
ternario de la coordenada hija y el residuo orientado de la arista deben tener
una etiqueta con el mismo tiempo t en N69.

Los dieciseis pares de campos (q,a,c,colw_mod)^2 se publican antes de filtrar
los candidatos.  Al intersectar con la cara excepcional calculada desde los
lectores de pi y e, sobrevive exactamente un par regla--estado.  Solo despues
se abre CURRENT.json para reconocer el estado como el sello canonico.

No se usa ``assert``; todas las condiciones siguen activas con ``python -O``.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

CURRENT = ROOT / "03_PAPER/HMT_MACROPAPER_V3/CURRENT.json"
PHASE_COVERAGE = ROOT / (
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/"
    "continuacion_fases/RESULTADO_OBSTRUCCION_Y_DATO_MINIMO_W72.json"
)
GLOBAL_READER = ROOT / (
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/01_SELECTOR_CONSTANTES/"
    "CERTIFICADO_SELECTOR_GLOBAL.json"
)
N69 = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/"
    "HMT_N69_ley_transicion_o_axioma_cilindrico_v1/"
    "N69_signatures_t0_t99.csv"
)
OUT = HERE / "RESULTADO_SELECTOR_ORBITAL_ETIQUETADO.json"

FIELDS = ("q", "a", "c", "colw_mod")

# Entradas tipadas ya certificadas.  S8 se usa como conjunto, nunca con el
# orden canonico.  Su presencia se declara expresamente en el alcance.
W24_INPUT = "020022222111211201021101"
S8_UNORDERED_INPUT = (
    "001001", "002001", "010122", "020111",
    "121012", "200110", "221110", "222110",
)

# Bosque fijado por la geometria Cay(Z/12; +3,+4), antes de leer candidatos.
FOREST = (
    (0, 3, 3),
    (0, 4, 4),
    (1, 5, 4),
    (2, 6, 4),
    (3, 7, 4),
    (4, 8, 4),
    (5, 9, 4),
    (6, 10, 4),
    (7, 11, 4),
)

# Indices de las aristas 4->8 y 8->12 dentro del bosque anterior.
ORBITAL_EDGE_INDICES = (4, 8)

# Matriz Paley--Witt publicada por el cierre activo.
A_W = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(values: Iterable[str]) -> str:
    payload = "".join(value + "\n" for value in values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def assert_count_in_source() -> int:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    return sum(isinstance(node, ast.Assert) for node in ast.walk(tree))


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def cylinder_grid(prefix: str, decimal_places: int = 36) -> tuple[int, int, int]:
    require(prefix and set(prefix) <= {"0", "1", "2"}, "prefijo ternario invalido")
    value = int(prefix, 3)
    denominator = 3 ** len(prefix)
    scale = 10 ** decimal_places
    lower = ceil_div(value * scale, denominator)
    upper = ceil_div((value + 1) * scale, denominator) - 1
    return lower, upper, max(0, upper - lower + 1)


def first_word_at_least(entry: dict[str, object], length: int) -> str:
    cylinders = entry.get("cilindros_ternarios")
    require(isinstance(cylinders, list), "lector global sin cilindros")
    words = [
        str(item["palabra"])
        for item in cylinders
        if isinstance(item, dict) and int(item["longitud"]) >= length
    ]
    require(bool(words), f"el lector no alcanza {length} trits")
    return min(words, key=len)


def load_functional_panel() -> dict[str, object]:
    certificate = json.loads(GLOBAL_READER.read_text(encoding="utf-8"))
    require(str(certificate.get("estado", "")).startswith("PASS"),
            "el lector funcional no esta certificado")
    result = certificate.get("resultado")
    require(isinstance(result, dict), "lector funcional sin resultado")
    streams = {
        role: first_word_at_least(result[role], 360)  # type: ignore[arg-type]
        for role in ("cierre", "propagacion", "autoescala")
    }
    panel = tuple(
        (role, position + 1, stream[6 * position:6 * (position + 1)])
        for role, stream in streams.items()
        for position in range(3)
    )
    require(len(panel) == 9, "el panel no tiene nueve posiciones")
    require(len({word for _role, _position, word in panel}) == 8,
            "el panel no conserva ocho palabras distintas")
    return {"streams": streams, "panel": panel}


def verify_historical_inputs() -> dict[str, object]:
    """Coteja W24 y S8 sin leer los cierres posteriores del mismo artefacto."""

    certificate = json.loads(PHASE_COVERAGE.read_text(encoding="utf-8"))
    interface = certificate.get("minimal_dodecaphase_interface")
    reader = certificate.get("phase_charge_reader")
    require(isinstance(interface, dict) and isinstance(reader, dict),
            "fuente historica de W24/S8 mal formada")
    require(str(interface.get("W24")) == W24_INPUT,
            "W24 historico ya no coincide con la entrada congelada")
    hits = reader.get("hits")
    affine = reader.get("affine_extension")
    require(isinstance(hits, list) and isinstance(affine, dict),
            "fuente historica sin incidencias fase--carga")
    by_position: dict[int, set[str]] = {}
    for hit in hits:
        require(isinstance(hit, dict), "incidencia historica mal formada")
        position = int(hit["position_W72"])
        if 5 <= position <= 12:
            by_position.setdefault(position, set()).add(str(hit["output"]))
    affine_position = int(affine["position_W72"])
    if 5 <= affine_position <= 12:
        by_position.setdefault(affine_position, set()).add(str(affine["output"]))
    require(set(by_position) == set(range(5, 13)),
            "la fuente historica ya no cubre W5,...,W12")
    require(all(len(words) == 1 for words in by_position.values()),
            "una posicion historica ya no es unitaria")
    recovered = tuple(next(iter(by_position[position])) for position in range(5, 13))
    require(set(recovered) == set(S8_UNORDERED_INPUT),
            "S8 historico ya no coincide con la entrada no ordenada")
    return {
        "W24_verified": True,
        "S8_verified": True,
        "historical_order_not_exported_to_selector": True,
    }


def build_decimal_candidates(panel: Sequence[tuple[str, int, str]]) -> dict[str, object]:
    """Construye C_dec sin abrir CURRENT ni recibir K/alpha/residuos."""

    require(len(W24_INPUT) == 24 and set(W24_INPUT) <= {"0", "1", "2"},
            "W24 mal tipado")
    require(len(S8_UNORDERED_INPUT) == 8
            and len(set(S8_UNORDERED_INPUT)) == 8,
            "S8 no contiene ocho palabras distintas")
    require(all(len(word) == 6 and set(word) <= {"0", "1", "2"}
                for word in S8_UNORDERED_INPUT), "S8 mal tipado")

    candidates: set[int] = set()
    indexed_hits = 0
    permutations = 0
    for permutation in itertools.permutations(S8_UNORDERED_INPUT):
        permutations += 1
        w72 = W24_INPUT + "".join(permutation)
        for _role, _position, boundary in panel:
            lower, upper, count = cylinder_grid(w72 + boundary)
            require(count <= 1, "un cilindro W78 contiene mas de un punto")
            indexed_hits += count
            if count:
                require(lower == upper, "la interseccion W78 no es unitaria")
                candidates.add(lower)
    require(permutations == 40320, "no se recorrieron las 8! ordenaciones")
    require(indexed_hits == 21902, "cambio el numero de incidencias W78")
    require(len(candidates) == 19446, "C_dec ya no tiene 19 446 estados")
    roots = {decimal_coordinates(value)[:3] for value in candidates}
    require(roots == {(234, 543, 140)}, "W24 ya no fija las tres raices")
    return {
        "candidates": candidates,
        "indexed_hits": indexed_hits,
        "permutations": permutations,
        "roots": next(iter(roots)),
    }


def decimal_coordinates(numerator: int) -> tuple[int, ...]:
    text = f"{numerator:036d}"
    require(len(text) == 36, "numerador fuera de la carta de doce triadas")
    return tuple(int(text[index:index + 3]) for index in range(0, 36, 3))


def ternary6(value: int) -> str:
    require(0 <= value < 729, "digito base 729 fuera de rango")
    return "".join(
        str((value // (3 ** exponent)) % 3)
        for exponent in range(5, -1, -1)
    )


def ternary_blocks(k: Sequence[int]) -> tuple[str, ...]:
    require(len(k) == 12 and all(0 <= int(value) <= 999 for value in k),
            "estado decimal mal tipado")
    numerator = 0
    for value in k:
        numerator = 1000 * numerator + int(value)
    prefix = numerator * (729 ** 13) // (1000 ** 12)
    digits = tuple(
        (prefix // (729 ** exponent)) % 729
        for exponent in range(12, -1, -1)
    )
    return tuple(ternary6(value) for value in digits)


def forest_residues(k: Sequence[int]) -> tuple[int, ...]:
    require(len(k) == 12, "estado sin doce coordenadas")
    return tuple(
        (int(k[source]) - int(k[target])) % 729
        for source, target, _step in FOREST
    )


def high_crown(k: Sequence[int]) -> tuple[int, ...]:
    return tuple(index + 1 for index, value in enumerate(k) if int(value) >= 729)


def rotations(word: str) -> tuple[str, ...]:
    require(len(word) == 6 and set(word) <= {"0", "1", "2"},
            "palabra N69 invalida")
    return tuple(word[index:] + word[:index] for index in range(6))


def transform6(word: str) -> str:
    vector = tuple(int(value) for value in word)
    return "".join(
        str(sum(vector[i] * A_W[i][j] for i in range(6)) % 3)
        for j in range(6)
    )


def linear_word(rows: Sequence[str], coefficients: Sequence[int]) -> str:
    require(len(rows) == len(coefficients) == 3, "lector lineal mal tipado")
    return "".join(
        str(sum(int(coefficients[i]) * int(rows[i][j]) for i in range(3)) % 3)
        for j in range(6)
    )


def add_label(
    table: dict[str, list[dict[str, object]]],
    word: str,
    label: dict[str, object],
) -> None:
    table.setdefault(word, []).append(label)


def build_label_atlas() -> dict[str, object]:
    with N69.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 100, "N69 ya no contiene cien filas")

    block_labels: dict[str, list[dict[str, object]]] = {}
    residue_labels: dict[str, dict[int, list[dict[str, object]]]] = {
        field: {} for field in FIELDS
    }
    comparison_outputs: set[str] = set()
    affine_outputs: set[str] = set()

    for row in rows:
        time = int(row["t"])
        bands = tuple(str(row["B"]).split("|"))
        require(len(bands) == 3 and all(len(band) == 6 for band in bands),
                "frontera N69 mal formada")
        phase = (time - 1) % 3
        visible = tuple(sum(int(value) for value in band) % 3 for band in bands)
        dual = tuple(
            sum(int(value) for value in transform6(band)) % 3
            for band in bands
        )
        require("".join(map(str, visible)) == str(row["r"]).zfill(3),
                "carga visible inconsistente")
        require("".join(map(str, dual)) == str(row["dual"]).zfill(3),
                "carga Witt-dual inconsistente")

        for charge_name, charge in (("visible", visible), ("Witt-dual", dual)):
            for offset in range(3):
                selected = (phase + offset) % 3
                for orientation in (1, -1):
                    coefficients = tuple(
                        orientation * (1 if value == selected else -1) % 3
                        for value in charge
                    )
                    output = linear_word(bands, coefficients)
                    comparison_outputs.add(output)
                    add_label(block_labels, output, {
                        "reader": "comparacion-fase-carga",
                        "t": time,
                        "K_calendar": int(row["K"]),
                        "charge": charge_name,
                        "phase": phase,
                        "phase_offset": offset,
                        "orientation": orientation,
                        "coefficients": list(coefficients),
                    })

        affine_coefficients = tuple((value + phase) % 3 for value in dual)
        affine_output = linear_word(bands, affine_coefficients)
        affine_outputs.add(affine_output)
        add_label(block_labels, affine_output, {
            "reader": "Witt-dual-mas-fase",
            "t": time,
            "K_calendar": int(row["K"]),
            "charge": "Witt-dual",
            "phase": phase,
            "coefficients": list(affine_coefficients),
        })

        for field in FIELDS:
            raw = str(row[field])
            for rotation, rotated in enumerate(rotations(raw)):
                value = int(rotated, 3)
                residue_labels[field].setdefault(value, []).append({
                    "t": time,
                    "K_calendar": int(row["K"]),
                    "field": field,
                    "rotation": rotation,
                    "raw": raw,
                    "rotated": rotated,
                })

    language = comparison_outputs | affine_outputs
    require(len(comparison_outputs) == 410, "cambio el lenguaje comparativo")
    require(len(affine_outputs) == 91, "cambio el lenguaje afin")
    require(len(language) == 442, "el lenguaje N69 ya no tiene 442 palabras")
    expected_sizes = {"q": 378, "a": 437, "c": 177, "colw_mod": 342}
    require({field: len(labels) for field, labels in residue_labels.items()}
            == expected_sizes, "cambiaron los atlas rotacionales")
    return {
        "rows": rows,
        "block_labels": block_labels,
        "residue_labels": residue_labels,
        "comparison_outputs": comparison_outputs,
        "affine_outputs": affine_outputs,
        "language": language,
    }


def witt_codeword(word: str) -> tuple[int, ...]:
    left = tuple(int(value) for value in word)
    right = tuple(
        sum(left[i] * A_W[i][j] for i in range(6)) % 3
        for j in range(6)
    )
    return left + right


def support(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(index + 1 for index, value in enumerate(word) if value)


def exceptional_face(streams: dict[str, str]) -> dict[str, object]:
    pi_word = streams["cierre"][:6]
    e_word = streams["propagacion"][:6]
    p_pi = support(witt_codeword(pi_word))
    h_e = support(witt_codeword(e_word))
    face = tuple(sorted(set(p_pi) & set(h_e)))
    require(pi_word == "010211" and e_word == "201101",
            "cambiaron los canales pi/e")
    require(face == (4, 6, 9, 10), "cambio la cara excepcional")
    return {"pi_word": pi_word, "e_word": e_word,
            "P_pi": p_pi, "H_e": h_e, "B_exc": face}


def plus4_orbits() -> tuple[tuple[int, ...], ...]:
    remaining = set(range(1, 13))
    orbits: list[tuple[int, ...]] = []
    while remaining:
        start = min(remaining)
        orbit = []
        value = start
        while value not in orbit:
            orbit.append(value)
            remaining.discard(value)
            value = ((value - 1 + 4) % 12) + 1
        orbits.append(tuple(orbit))
    result = tuple(orbits)
    require(result == ((1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)),
            "cambio la descomposicion orbital de +4")
    return result


def edge_label_matches(
    k: Sequence[int],
    edge_index: int,
    field: str,
    block_labels: dict[str, list[dict[str, object]]],
    residue_labels: dict[str, dict[int, list[dict[str, object]]]],
) -> list[dict[str, object]]:
    require(field in FIELDS, "campo fuera de la familia predeclarada")
    source, target, step = FOREST[edge_index]
    blocks = ternary_blocks(k)
    residues = forest_residues(k)
    block_word = blocks[target]
    residue = residues[edge_index]
    matches = []
    for block_label in block_labels.get(block_word, []):
        for residue_label in residue_labels[field].get(residue, []):
            if int(block_label["t"]) == int(residue_label["t"]):
                matches.append({
                    "edge": [source + 1, target + 1],
                    "step": step,
                    "child_block": block_word,
                    "residue_mod_729": residue,
                    "block_label": block_label,
                    "residue_label": residue_label,
                })
    return matches


def build_result() -> dict[str, object]:
    # Fase 1: entradas permitidas y familias completas, sin abrir CURRENT.
    panel_data = load_functional_panel()
    panel = panel_data["panel"]
    require(isinstance(panel, tuple), "panel mal tipado")
    decimal = build_decimal_candidates(panel)
    candidate_values = set(decimal["candidates"])  # type: ignore[arg-type]
    coordinate_map = {
        value: decimal_coordinates(value) for value in candidate_values
    }
    labels = build_label_atlas()
    block_labels = labels["block_labels"]
    residue_labels = labels["residue_labels"]
    require(isinstance(block_labels, dict) and isinstance(residue_labels, dict),
            "atlas de etiquetas mal tipado")
    exceptional = exceptional_face(panel_data["streams"])  # type: ignore[arg-type]
    face = tuple(exceptional["B_exc"])  # type: ignore[arg-type]
    orbits = plus4_orbits()
    roots = {1, 2, 3}
    root_intersections = tuple(len(set(orbit) & roots) for orbit in orbits)
    require(root_intersections == (1, 1, 1, 0),
            "la cuarta orbita ya no es la unica sin raiz decimal")
    require(tuple(FOREST[index] for index in ORBITAL_EDGE_INDICES)
            == ((3, 7, 4), (7, 11, 4)),
            "cambiaron las dos aristas internas de la cuarta orbita")

    crown_candidates = {
        value for value, k in coordinate_map.items() if high_crown(k) == face
    }
    require(len(crown_candidates) == 79, "la cara ya no deja 79 candidatos")

    # Se precalculan las coincidencias etiquetadas para cada estado y campo.
    matching_fields: dict[int, tuple[set[str], set[str]]] = {}
    for value, k in coordinate_map.items():
        fields_by_edge = []
        for edge_index in ORBITAL_EDGE_INDICES:
            fields_by_edge.append({
                field for field in FIELDS
                if edge_label_matches(
                    k, edge_index, field, block_labels, residue_labels  # type: ignore[arg-type]
                )
            })
        matching_fields[value] = (fields_by_edge[0], fields_by_edge[1])

    # Los 16 pares se definen antes del contraste con la cara excepcional.
    rules = tuple(itertools.product(FIELDS, repeat=2))
    require(len(rules) == 16, "la familia no contiene dieciseis pares")
    rule_table = []
    joint_pairs: list[tuple[str, str, int]] = []
    for first_field, second_field in rules:
        survivors = {
            value for value, (first_hits, second_hits) in matching_fields.items()
            if first_field in first_hits and second_field in second_hits
        }
        joint = survivors & crown_candidates
        rule_table.append({
            "field_4_to_8": first_field,
            "field_8_to_12": second_field,
            "orbital_label_survivors": len(survivors),
            "joint_with_exceptional_face": len(joint),
        })
        joint_pairs.extend(
            (first_field, second_field, value) for value in sorted(joint)
        )

    expected_table = {
        ("q", "q"): (6, 0), ("q", "a"): (4, 0),
        ("q", "c"): (4, 0), ("q", "colw_mod"): (5, 0),
        ("a", "q"): (1, 0), ("a", "a"): (8, 1),
        ("a", "c"): (1, 0), ("a", "colw_mod"): (3, 0),
        ("c", "q"): (0, 0), ("c", "a"): (2, 0),
        ("c", "c"): (2, 0), ("c", "colw_mod"): (4, 0),
        ("colw_mod", "q"): (3, 0), ("colw_mod", "a"): (1, 0),
        ("colw_mod", "c"): (4, 0), ("colw_mod", "colw_mod"): (7, 0),
    }
    require({
        (str(row["field_4_to_8"]), str(row["field_8_to_12"])):
        (int(row["orbital_label_survivors"]),
         int(row["joint_with_exceptional_face"]))
        for row in rule_table
    } == expected_table, "cambio la tabla exhaustiva de pares de campos")
    require(sum(row["orbital_label_survivors"] for row in rule_table) == 55,
            "cambio el numero de pares regla--estado antes de la cara")
    distinct_pre_face = {
        value
        for first, second in rules
        for value, (first_hits, second_hits) in matching_fields.items()
        if first in first_hits and second in second_hits
    }
    require(len(distinct_pre_face) == 52,
            "cambio el numero de estados orbitales antes de la cara")
    require(len(joint_pairs) == 1,
            "la seleccion conjunta regla--estado dejo de ser unitaria")
    selected_first, selected_second, selected_value = joint_pairs[0]
    require((selected_first, selected_second) == ("a", "a"),
            "el unico par ya no es (a,a)")
    selected_k = coordinate_map[selected_value]

    # Ablaciones: las dos aristas y la cara son necesarias.
    selected_edge_all = []
    selected_edge_crown = []
    for edge_index in ORBITAL_EDGE_INDICES:
        all_hits = {
            value for value, k in coordinate_map.items()
            if edge_label_matches(
                k, edge_index, "a", block_labels, residue_labels  # type: ignore[arg-type]
            )
        }
        selected_edge_all.append(len(all_hits))
        selected_edge_crown.append(len(all_hits & crown_candidates))
    require(selected_edge_all == [276, 221], "cambio la ablacion por arista")
    require(selected_edge_crown == [2, 2],
            "una arista sola ya no deja dos estados con la cara")

    witness_edges = [
        edge_label_matches(
            selected_k, edge_index, "a", block_labels, residue_labels  # type: ignore[arg-type]
        )
        for edge_index in ORBITAL_EDGE_INDICES
    ]
    require([len(matches) for matches in witness_edges] == [2, 1],
            "cambio la multiplicidad de etiquetas del testigo")
    require({int(item["block_label"]["t"]) for item in witness_edges[0]} == {90},
            "la primera coincidencia ya no vive en t=90")
    require({int(item["block_label"]["t"]) for item in witness_edges[1]} == {60},
            "la segunda coincidencia ya no vive en t=60")
    require({str(item["child_block"]) for item in witness_edges[0]} == {"121012"},
            "cambio el bloque hijo W8")
    require({str(item["child_block"]) for item in witness_edges[1]} == {"222110"},
            "cambio el bloque hijo W12")
    require({int(item["residue_mod_729"]) for item in witness_edges[0]} == {671},
            "cambio el residuo 4->8")
    require({int(item["residue_mod_729"]) for item in witness_edges[1]} == {186},
            "cambio el residuo 8->12")

    # Control negativo sin rotaciones: la segunda arista necesita rotacion 1.
    require(all(
        int(item["residue_label"]["rotation"]) == 0
        for item in witness_edges[0]
    ), "la primera arista ya no usa rotacion cero")
    require({int(item["residue_label"]["rotation"])
             for item in witness_edges[1]} == {1},
            "la segunda arista ya no usa rotacion uno")
    raw_joint = set()
    for value in crown_candidates:
        k = coordinate_map[value]
        raw_matches = []
        for edge_index in ORBITAL_EDGE_INDICES:
            matches = edge_label_matches(
                k, edge_index, "a", block_labels, residue_labels  # type: ignore[arg-type]
            )
            raw_matches.append(any(
                int(item["residue_label"]["rotation"]) == 0
                for item in matches
            ))
        if all(raw_matches):
            raw_joint.add(value)
    require(len(raw_joint) == 0,
            "la ablacion sin rotaciones produjo un estado con la cara")

    # Fase 2: cotejo de procedencia y reconocimiento posterior.  Ni el
    # artefacto historico amplio ni CURRENT participaron en la seleccion.
    historical = verify_historical_inputs()
    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    require(current.get("revision") == "2026-07-22.2",
            "revision canonica inesperada")
    canonical = current.get("state_types", {}).get("CanonicalSealK", {}).get("coordinates")
    require(isinstance(canonical, list) and len(canonical) == 12,
            "CURRENT no publica el sello tipado")
    canonical_k = tuple(int(value) for value in canonical)
    require(selected_k == canonical_k,
            "el unico estado no reconoce el sello canonico")
    source_assert_count = assert_count_in_source()
    require(source_assert_count == 0, "el verificador contiene instrucciones assert")

    candidate_text = sorted(f"{value:036d}" for value in candidate_values)
    pre_face_text = sorted(
        "|".join(f"{coordinate:03d}" for coordinate in coordinate_map[value])
        for value in distinct_pre_face
    )
    return {
        "schema": "HMT.selector-orbital-etiquetado.v1",
        "status": "PASS_SELECTOR_ORBITAL_ETIQUETADO_UNICO",
        "allowed_inputs": {
            "W24": W24_INPUT,
            "S8_unordered_historical": list(S8_UNORDERED_INPUT),
            "S8_order_used": False,
            "functional_boundary_panel": [
                {"role": role, "position": position, "word": word}
                for role, position, word in panel
            ],
            "N69": "cien filas con B, relojes y campos q/a/c/colw_mod",
            "Paley_Witt_reader": "A_W para construir B_exc desde pi/e",
            "forest": [
                {"source": source + 1, "target": target + 1, "step": step}
                for source, target, step in FOREST
            ],
            "historical_input_verification": historical,
        },
        "forbidden_during_selection": [
            "CanonicalSealK",
            "SignedDodecaphaseStateU12",
            "alpha",
            "CODATA",
            "Q=6263",
            "D3K",
            "D4K",
            "los nueve residuos canonicos",
            "el orden canonico de S8",
        ],
        "anti_leakage": {
            "CURRENT_opened_only_after_unique_rule_state_pair": True,
            "PHASE_COVERAGE_opened_only_after_unique_rule_state_pair": True,
            "K_used_only_for_posterior_recognition": True,
            "rule_parameters_enumerated_before_exceptional_contrast": True,
            "candidate_values_not_embedded_in_rule": True,
            "logical_scope": (
                "selector sin objetivo relativo a W24, S8 no ordenado y panel funcional; "
                "no constituye una derivacion de S8 desde N69 bruto"
            ),
        },
        "decimal_family": {
            "suffix_permutations": decimal["permutations"],
            "indexed_cylinder_hits": decimal["indexed_hits"],
            "unique_candidates": len(candidate_values),
            "roots_forced_by_W24": list(decimal["roots"]),  # type: ignore[arg-type]
            "candidate_sha256": sha256_lines(candidate_text),
        },
        "orbital_geometry": {
            "translation": "+4 on Z/12",
            "orbits": [list(orbit) for orbit in orbits],
            "decimal_roots": sorted(roots),
            "root_intersection_cardinalities": list(root_intersections),
            "distinguished_orbit": [4, 8, 12],
            "reason": "unica orbita +4 sin una de las tres raices fijadas por W24",
            "internal_edges": [[4, 8], [8, 12]],
        },
        "labelled_rule": {
            "definition": (
                "en cada arista interna, el bloque ternario de la coordenada hija "
                "y una rotacion del campo elegido para el residuo comparten el mismo t N69"
            ),
            "block_label_fields": [
                "t", "K_calendar", "reader", "charge", "phase",
                "phase_offset", "orientation", "coefficients",
            ],
            "residue_label_fields": [
                "t", "K_calendar", "field", "rotation", "raw", "rotated",
            ],
            "field_pair_family": [list(rule) for rule in rules],
            "field_pair_count": len(rules),
            "field_pair_table": rule_table,
        },
        "exceptional_face": {
            "pi_word": exceptional["pi_word"],
            "e_word": exceptional["e_word"],
            "P_pi": list(exceptional["P_pi"]),  # type: ignore[arg-type]
            "H_e": list(exceptional["H_e"]),  # type: ignore[arg-type]
            "B_exc": list(face),
            "candidates_before_face": len(candidate_values),
            "candidates_after_face": len(crown_candidates),
        },
        "selection": {
            "rule_state_pairs_before_face": 55,
            "distinct_states_before_face": len(distinct_pre_face),
            "rule_state_pairs_after_face": len(joint_pairs),
            "selected_rule": {
                "field_4_to_8": selected_first,
                "field_8_to_12": selected_second,
            },
            "selected_K": list(selected_k),
            "recognized_only_after_selection": True,
            "edge_witnesses": witness_edges,
        },
        "ablations": {
            "a_a_both_edges_without_face": 8,
            "a_only_4_to_8_without_face": selected_edge_all[0],
            "a_only_8_to_12_without_face": selected_edge_all[1],
            "a_only_4_to_8_with_face": selected_edge_crown[0],
            "a_only_8_to_12_with_face": selected_edge_crown[1],
            "a_a_both_edges_with_face": 1,
            "without_rotations_selected_rule": 0,
            "pre_face_state_sha256": sha256_lines(pre_face_text),
        },
        "provenance_and_force": {
            "orbital_architecture": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "labelled_same_time_rule": (
                "FORMALIZACION_NUEVA; procedencia historica pendiente de auditoria"
            ),
            "exhaustive_sixteen_rule_selection": "RESULTADO_NUEVO",
            "machine_certificate": "CERTIFICADO_NUEVO",
            "strength": "EXACTO_INTERNO_RELATIVO_A_C_dec_PRECERTIFICADO",
        },
        "sources_sha256": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in (CURRENT, PHASE_COVERAGE, GLOBAL_READER, N69)
        },
        "execution": {
            "assert_statements_in_this_verifier": source_assert_count,
            "optimized_mode_safe": True,
            "integer_arithmetic_only": True,
        },
    }


def render(result: dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-json", type=Path)
    parser.add_argument("--check-certificate", action="store_true")
    args = parser.parse_args()
    payload = render(build_result())
    if args.emit_json is not None:
        args.emit_json.write_text(payload, encoding="utf-8")
    if args.check_certificate:
        require(OUT.exists(), "no existe el certificado esperado")
        require(OUT.read_text(encoding="utf-8") == payload,
                "el certificado no es reproducible")
    print("PASS — selector orbital etiquetado: unico par (a,a) y unico estado")


if __name__ == "__main__":
    main()
