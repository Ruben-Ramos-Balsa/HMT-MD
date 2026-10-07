#!/usr/bin/env python3
"""Reconstruye de forma exhaustiva el emisor APP mínimo y sus fibras."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARCHIMEDEAN_CATALOG = ROOT / "datos/catalogo_lector_arquimediano.csv"
OUTPUT = ROOT / "certificados/catalogo_app_exhaustivo.json"

DIRS = ("N", "E", "S", "O")
VEC = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
LOG9 = {1: 0, 2: 1, 4: 2, 8: 3, 7: 4, 5: 5}
FLIPS = {27, 54, 81, 108}
PI_WORD = "010211"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"CATALOGO APP FAIL: {message}")


def dr9(n: int) -> int:
    residue = n % 9
    return 9 if residue == 0 else residue


def sign(t: int) -> int:
    residue = (t - 1) % 9 + 1
    if residue in (1, 4, 7):
        return 1
    if residue in (2, 5, 8):
        return -1
    return 0


def plus_value(i: int, j: int) -> int:
    return dr9((i + 1) + (j + 1))


def times_value(i: int, j: int) -> int:
    return dr9((i + 1) * (j + 1))


def channel_signature(seed: tuple[int, int, str], channel: str) -> tuple[int, ...]:
    """Calcula S_m mod 10 o E_m mod 10 durante las seis ventanas."""
    i, j, direction = seed
    di, dj = VEC[direction]
    result: list[int] = []
    for window in range(6):
        accumulator = 0
        for t in range(9 * window + 1, 9 * (window + 1) + 1):
            movement = sign(t)
            if channel == "plus" and movement == 1:
                accumulator += plus_value(i, j)
                i, j = (i + di) % 9, (j + dj) % 9
            elif channel == "times" and movement == -1:
                accumulator += LOG9.get(times_value(i, j), 0)
                i, j = (i + di) % 9, (j + dj) % 9
            if t in FLIPS:
                di, dj = (-di) % 9, (-dj) % 9
        result.append(accumulator % 10)
    return tuple(result)


def direct_u6(
    seed_plus: tuple[int, int, str], seed_times: tuple[int, int, str]
) -> tuple[int, ...]:
    """Segunda implementación independiente de la factorización por firmas."""
    pi, pj, pd = seed_plus
    ti, tj, td = seed_times
    pdi, pdj = VEC[pd]
    tdi, tdj = VEC[td]
    output: list[int] = []
    for window in range(6):
        s_total = e_total = neutral = 0
        for tick in range(9 * window + 1, 9 * (window + 1) + 1):
            movement = sign(tick)
            if movement == 1:
                s_total += plus_value(pi, pj)
                pi, pj = (pi + pdi) % 9, (pj + pdj) % 9
            elif movement == -1:
                e_total += LOG9.get(times_value(ti, tj), 0)
                ti, tj = (ti + tdi) % 9, (tj + tdj) % 9
            else:
                neutral += 1
            if tick in FLIPS:
                pdi, pdj = (-pdi) % 9, (-pdj) % 9
                tdi, tdj = (-tdi) % 9, (-tdj) % 9
        digits = (
            s_total % 10,
            (s_total + e_total) % 10,
            (3 * s_total + 5 * e_total + 7 * neutral) % 10,
        )
        output.append(100 * digits[0] + 10 * digits[1] + digits[2])
    return tuple(output)


def combine(s_signature: tuple[int, ...], e_signature: tuple[int, ...]) -> tuple[int, ...]:
    check(len(s_signature) == len(e_signature) == 6, "firmas mal tipadas")
    return tuple(
        100 * s + 10 * ((s + e) % 10) + ((3 * s + 5 * e + 1) % 10)
        for s, e in zip(s_signature, e_signature)
    )


def recover_signatures(u6: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    s_values: list[int] = []
    e_values: list[int] = []
    for value in u6:
        s = value // 100
        second = (value // 10) % 10
        e = (second - s) % 10
        check(value % 10 == (3 * s + 5 * e + 1) % 10, "U no pertenece a la imagen")
        s_values.append(s)
        e_values.append(e)
    return tuple(s_values), tuple(e_values)


def w6(u6: tuple[int, ...]) -> str:
    return "".join(str((-value) % 3) for value in u6)


def read_catalog() -> dict[tuple[int, ...], int]:
    result: dict[tuple[int, ...], int] = {}
    row_count = 0
    total_multiplicity = 0
    with ARCHIMEDEAN_CATALOG.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = tuple(int(item) for item in row["U6"].split("|"))
            check(row["w6"] == w6(key), "sombra w6 inconsistente en el CSV")
            check(key not in result, "fila U6 duplicada en el CSV")
            multiplicity = int(row["count"])
            result[key] = multiplicity
            row_count += 1
            total_multiplicity += multiplicity
    check(row_count == len(result) == 468, "numero de filas del catalogo")
    check(total_multiplicity == 104_976, "multiplicidad total del catalogo")
    return result


def coordinate_ablations(
    records: set[tuple[tuple[int, int, str], tuple[int, int, str]]]
) -> dict[str, object]:
    columns = ("pi", "pj", "ti", "tj")
    counters = {pair: Counter() for pair in combinations(range(4), 2)}
    loops = Counter()
    for plus_seed, times_seed in records:
        values = plus_seed[:2] + times_seed[:2]
        for pair, counter in counters.items():
            a, b = values[pair[0]], values[pair[1]]
            name = f"{columns[pair[0]]}_{columns[pair[1]]}"
            if a == b:
                loops[name] += 1
            else:
                counter[tuple(sorted((a, b)))] += 1
    report: dict[str, object] = {}
    for pair, counter in counters.items():
        name = f"{columns[pair[0]]}_{columns[pair[1]]}"
        check(not (len(counter) == 36 and set(counter.values()) == {28}),
              f"la ablacion {name} seria ya un cociente uniforme")
        report[name] = {
            "loops_discarded": loops[name],
            "distinct_unordered_pairs": len(counter),
            "fibre_histogram": dict(sorted(Counter(counter.values()).items())),
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-certificate",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help=(
            "Escribe el JSON determinista; sin argumento usa la residencia "
            "canónica. Por defecto la verificación es de sólo lectura."
        ),
    )
    args = parser.parse_args()
    seeds = [(i, j, d) for i, j, d in product(range(9), range(9), DIRS)]
    check(len(seeds) == 324, "espacio de semillas distinto de 324")

    plus_classes: defaultdict[tuple[int, ...], set[tuple[int, int, str]]] = defaultdict(set)
    times_classes: defaultdict[tuple[int, ...], set[tuple[int, int, str]]] = defaultdict(set)
    plus_by_key: defaultdict[tuple[int, int], set[tuple[int, ...]]] = defaultdict(set)
    for seed in seeds:
        s_signature = channel_signature(seed, "plus")
        e_signature = channel_signature(seed, "times")
        plus_classes[s_signature].add(seed)
        times_classes[e_signature].add(seed)
        orientation = 1 if seed[2] in ("E", "S") else -1
        plus_by_key[((seed[0] + seed[1]) % 9, orientation)].add(s_signature)

    check(len(plus_classes) == 18, "numero de clases suma")
    check(set(map(len, plus_classes.values())) == {18}, "fibras suma no uniformes")
    check(len(plus_by_key) == 18 and set(map(len, plus_by_key.values())) == {1},
          "la parametrizacion suma (i+j,orientacion) no es funcional")
    check(len({next(iter(value)) for value in plus_by_key.values()}) == 18,
          "la parametrizacion suma no es inyectiva")

    times_size_histogram = Counter(map(len, times_classes.values()))
    check(len(times_classes) == 26, "numero de clases producto")
    check(times_size_histogram == Counter({8: 24, 24: 1, 108: 1}),
          "histograma de clases producto")
    check(len(times_classes[(0, 0, 0, 0, 0, 0)]) == 108, "clase producto nula")
    check(len(times_classes[(5, 5, 5, 5, 5, 5)]) == 24, "clase producto constante 5")

    uid_count: Counter[tuple[int, ...]] = Counter()
    pi_records: set[tuple[tuple[int, int, str], tuple[int, int, str]]] = set()
    pi_by_u: defaultdict[
        tuple[int, ...], set[tuple[tuple[int, int, str], tuple[int, int, str]]]
    ] = defaultdict(set)
    for plus_seed in seeds:
        s_signature = channel_signature(plus_seed, "plus")
        for times_seed in seeds:
            e_signature = channel_signature(times_seed, "times")
            factored = combine(s_signature, e_signature)
            check(direct_u6(plus_seed, times_seed) == factored, "fallo de factorizacion")
            uid_count[factored] += 1
            if w6(factored) == PI_WORD:
                record = (plus_seed, times_seed)
                pi_records.add(record)
                pi_by_u[factored].add(record)

    check(sum(uid_count.values()) == 104_976, "conteo total")
    check(len(uid_count) == 18 * 26 == 468, "imagen U6")
    check(uid_count == Counter(read_catalog()), "el catálogo arquimediano no se regenera exactamente")
    fibre_histogram = Counter(uid_count.values())
    check(fibre_histogram == Counter({144: 432, 432: 18, 1944: 18}),
          "histograma global U6")

    expected_cells = [
        ((501, 614, 498, 169, 272, 272), 432,
         (5, 6, 4, 1, 2, 2), (5, 5, 5, 5, 5, 5)),
        ((810, 923, 870, 169, 272, 272), 144,
         (8, 9, 8, 1, 2, 2), (3, 3, 9, 5, 5, 5)),
        ((810, 983, 810, 169, 272, 272), 144,
         (8, 9, 8, 1, 2, 2), (3, 9, 3, 5, 5, 5)),
        ((870, 923, 810, 169, 272, 272), 144,
         (8, 9, 8, 1, 2, 2), (9, 3, 3, 5, 5, 5)),
        ((870, 923, 810, 418, 674, 521), 144,
         (8, 9, 8, 4, 6, 5), (9, 3, 3, 7, 1, 7)),
    ]
    check(len(pi_records) == 1008 and len(pi_by_u) == 5, "microfibra de la palabra 010211")
    plus_sets: list[set[tuple[int, int, str]]] = []
    times_sets: list[set[tuple[int, int, str]]] = []
    for u6, count, s_signature, e_signature in expected_cells:
        check(recover_signatures(u6) == (s_signature, e_signature), "firmas de celda pi")
        p_set = plus_classes[s_signature]
        t_set = times_classes[e_signature]
        rectangle = {(p, t) for p in p_set for t in t_set}
        check(pi_by_u[u6] == rectangle, "una celda pi no es producto cartesiano")
        check(len(rectangle) == count == uid_count[u6], "tamano de celda pi")
        plus_sets.append(p_set)
        times_sets.append(t_set)

    check(plus_sets[1] == plus_sets[2] == plus_sets[3], "las tres regiones ++ no comparten P")
    check(plus_sets[0].isdisjoint(plus_sets[1]) and plus_sets[0].isdisjoint(plus_sets[4]),
          "interseccion inesperada con P perpendicular")
    check(plus_sets[1].isdisjoint(plus_sets[4]), "interseccion inesperada P+ con P-")
    check(all(times_sets[i].isdisjoint(times_sets[j]) for i, j in combinations(range(5), 2)),
          "las cinco clases T no son disjuntas")

    p_neighbours: defaultdict[tuple[int, int, str], set[tuple[int, int, str]]] = defaultdict(set)
    t_neighbours: defaultdict[tuple[int, int, str], set[tuple[int, int, str]]] = defaultdict(set)
    for plus_seed, times_seed in pi_records:
        p_neighbours[plus_seed].add(times_seed)
        t_neighbours[times_seed].add(plus_seed)
    check(len(p_neighbours) == 54, "semillas P incidentes")
    check(Counter(map(len, p_neighbours.values())) == Counter({24: 36, 8: 18}),
          "grados de semillas P")
    check(len(t_neighbours) == 56 and set(map(len, t_neighbours.values())) == {18},
          "grados de semillas T")

    report = {
        "schema": "HMT.catalogo_app.v1",
        "status": "PASS",
        "global_factorization": {
            "plus_signatures": len(plus_classes),
            "plus_class_sizes": dict(sorted(Counter(map(len, plus_classes.values())).items())),
            "times_signatures": len(times_classes),
            "times_class_sizes": dict(sorted(times_size_histogram.items())),
            "unique_U6": len(uid_count),
            "U6_fibre_histogram": dict(sorted(fibre_histogram.items())),
        },
        "pi_microfibre": {
            "word": PI_WORD,
            "raw_routes": len(pi_records),
            "rectangles": [
                {"U6": list(u6), "plus": len(plus_sets[index]),
                 "times": len(times_sets[index]), "routes": count}
                for index, (u6, count, _, _) in enumerate(expected_cells)
            ],
            "plus_seed_degree_histogram": dict(sorted(Counter(map(len, p_neighbours.values())).items())),
            "times_seed_degree_histogram": dict(sorted(Counter(map(len, t_neighbours.values())).items())),
        },
        "coordinate_pair_ablations": coordinate_ablations(pi_records),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write_certificate is not None:
        args.write_certificate.parent.mkdir(parents=True, exist_ok=True)
        args.write_certificate.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print("PASS_CATALOGO_APP_EXACTO")


if __name__ == "__main__":
    main()
