#!/usr/bin/env python3
"""Comprobación exhaustiva focal de la memoria de la firma producto 555555.

Reúne las definiciones y el refinamiento del propietario:
  pruebas/python/verificar_dinamica_cociente_468.py, líneas 33--171 y 253--315
  SHA256 1cd7d2789777c53f3cf33f603dfd0bb439e8421a27ce1c6261c0e95b83697292
del integral EL_CIERRE_HOLOGRAFICO_DEL_INFINITO_SUCESOR_102_CAPITULOS_2026-08-28_EN_TRABAJO.
Exposición: manuscrito/sections/hmt/05b_extensiones_dinamica_cociente.tex,
líneas 409--426 y 741--816, teorema thm:congruencias-avance-giro.

Alcance: enumeración de 324 rutas producto, firmas de seis ventanas,
congruencia mínima estable bajo avance y media vuelta, escisión 3 x 8.
No certifica identidad de esta firma con la celda electrónica (5,5), ni
identifica la proyección finita con la memoria ilimitada del estado.

Sin argumentos escribe el informe en stdout y no modifica archivos.
--receipt RUTA escribe además el mismo informe JSON en esa ruta.
Sólo bibliotecas estándar; no recibe constantes físicas ni catálogos.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from itertools import product
import json
from pathlib import Path


DIRS = ("N", "E", "S", "O")
VEC = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
OPPOSITE = {"N": "S", "S": "N", "E": "O", "O": "E"}
LOG9 = {1: 0, 2: 1, 4: 2, 8: 3, 7: 4, 5: 5}
FLIPS = {27, 54, 81, 108}
Seed = tuple[int, int, str]
Signature = tuple[int, ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("FAIL_MEMORIA_555555: " + message)


def trit(tick: int) -> int:
    residue = (tick - 1) % 9 + 1
    if residue in (1, 4, 7):
        return 1
    if residue in (2, 5, 8):
        return -1
    return 0


def dr9(value: int) -> int:
    residue = value % 9
    return 9 if residue == 0 else residue


def channel_signature(seed: Seed) -> Signature:
    """Firma E_m mod 10 del canal producto; coordenadas internas 0,...,8."""
    i, j, direction = seed
    di, dj = VEC[direction]
    result: list[int] = []
    for window in range(6):
        accumulator = 0
        for tick in range(9 * window + 1, 9 * (window + 1) + 1):
            if trit(tick) == -1:
                value = dr9((i + 1) * (j + 1))
                accumulator += LOG9.get(value, 0)
                i, j = (i + di) % 9, (j + dj) % 9
            if tick in FLIPS:
                di, dj = (-di) % 9, (-dj) % 9
        result.append(accumulator % 10)
    return tuple(result)


def advance(seed: Seed) -> Seed:
    i, j, direction = seed
    di, dj = VEC[direction]
    return (i + di) % 9, (j + dj) % 9, direction


def half_turn(seed: Seed) -> Seed:
    i, j, direction = seed
    return i, j, OPPOSITE[direction]


def stable_refinement(seeds: list[Seed], signatures: dict[Seed, Signature]):
    signature_ids = {
        signature: index
        for index, signature in enumerate(sorted(set(signatures.values())))
    }
    partition = {x: signature_ids[signatures[x]] for x in seeds}
    counts = [len(signature_ids)]
    while True:
        keys = {
            x: (partition[x], partition[advance(x)], partition[half_turn(x)])
            for x in seeds
        }
        key_ids = {key: index for index, key in enumerate(sorted(set(keys.values())))}
        refined = {x: key_ids[keys[x]] for x in seeds}
        counts.append(len(key_ids))
        if len(key_ids) == len(set(partition.values())):
            return refined, counts
        partition = refined


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    seeds = list(product(range(9), range(9), DIRS))
    require(len(seeds) == 324, "dominio de rutas")
    signatures = {seed: channel_signature(seed) for seed in seeds}
    require(len(set(signatures.values())) == 26, "26 firmas producto")
    exceptional = (5,) * 6
    fibre = [seed for seed in seeds if signatures[seed] == exceptional]
    successors = Counter(signatures[advance(seed)] for seed in fibre)
    require(len(fibre) == 24, "24 representantes de 555555")
    require(successors == Counter({
        (5, 5, 5, 7, 1, 7): 8,
        (5, 5, 5, 7, 7, 1): 8,
        (5, 5, 5, 1, 7, 7): 8,
    }), "tres imágenes distintas, ocho representantes por imagen")

    partition, iteration_counts = stable_refinement(seeds, signatures)
    classes: dict[int, list[Seed]] = defaultdict(list)
    for seed in seeds:
        classes[partition[seed]].append(seed)
    require(len(classes) == 28, "28 clases de memoria")
    require(Counter(map(len, classes.values())) == Counter({8: 27, 108: 1}),
            "histograma 27 x 8 + 1 x 108")

    transitions = []
    for operator in (advance, half_turn):
        induced = {}
        for label, members in classes.items():
            require(len({signatures[s] for s in members}) == 1,
                    "el refinamiento no puede fusionar firmas")
            destinations = {partition[operator(s)] for s in members}
            require(len(destinations) == 1, "estabilidad por cada operador")
            induced[label] = next(iter(destinations))
        transitions.append(induced)
    seen = set()
    orbit_sizes = []
    for start in classes:
        if start in seen:
            continue
        queue, orbit = deque([start]), {start}
        while queue:
            current = queue.popleft()
            for transition in transitions:
                destination = transition[current]
                if destination not in orbit:
                    orbit.add(destination)
                    queue.append(destination)
        seen.update(orbit)
        orbit_sizes.append(len(orbit))
    require(sorted(orbit_sizes) == [1, 9, 9, 9], "órbitas del cociente")
    sheets = sorted({partition[s] for s in fibre})
    require(len(sheets) == 3, "tres hojas sobre 555555")
    require(all(len(classes[label]) == 8 for label in sheets), "ocho rutas por hoja")
    split_signatures = {
        sig for sig in set(signatures.values())
        if len({partition[s] for s in seeds if signatures[s] == sig}) > 1
    }
    require(split_signatures == {exceptional}, "única firma escindida")

    report = {
        "status": "PASS_MEMORIA_555555_324_RUTAS",
        "scope": "Verificación combinatoria exhaustiva finita de P y H",
        "source_sha256": "1cd7d2789777c53f3cf33f603dfd0bb439e8421a27ce1c6261c0e95b83697292",
        "state_count": len(seeds),
        "product_signature_count": len(set(signatures.values())),
        "refinement_class_counts": iteration_counts,
        "stable_class_count": len(classes),
        "class_size_histogram": dict(sorted(Counter(map(len, classes.values())).items())),
        "quotient_orbit_sizes": sorted(orbit_sizes),
        "exceptional_signature": exceptional,
        "exceptional_fibre_size": len(fibre),
        "successor_histogram": {"".join(map(str, s)): n for s, n in sorted(successors.items())},
        "sheets": [{
            "sheet_index": n,
            "states_zero_based": sorted(classes[label]),
            "states_one_based": [(i + 1, j + 1, d) for i, j, d in sorted(classes[label])],
            "successor_signature": signatures[advance(classes[label][0])],
        } for n, label in enumerate(sheets)],
        "negative_control": {
            "forgetting_sheet_prevents_single_valued_advance": len(successors) == 3,
            "explanation": "Los 24 estados tienen la misma firma, pero P produce tres firmas distintas.",
        },
    }
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.receipt is not None:
        args.receipt.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
