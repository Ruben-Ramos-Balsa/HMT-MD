#!/usr/bin/env python3
"""Certifica una recalibración del diseño de Witt compatible con el S3 HMT.

El cálculo reconstruye W12 desde el Golay ternario, genera M12 mediante seis
estrellas, localiza un S3 semirregular (dos órbitas regulares de seis puntos)
y construye una permutación de calibre que conjuga con él el S3 seleccionado
en la acción A5/C5 de la dodecafase. No usa constantes físicas ni espectros
de Yang--Mills.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path


AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)
COS_REPS = (
    (3, 2, 4, 1, 0),
    (3, 1, 0, 2, 4),
    (0, 1, 3, 4, 2),
    (1, 4, 2, 3, 0),
    (3, 2, 0, 4, 1),
    (4, 0, 1, 2, 3),
    (4, 3, 2, 1, 0),
    (0, 2, 3, 1, 4),
    (3, 1, 2, 4, 0),
    (2, 1, 4, 3, 0),
    (3, 4, 1, 2, 0),
    (4, 2, 1, 3, 0),
)
IDENTITY_12 = tuple(range(12))
IDENTITY_5 = tuple(range(5))
GENERATOR_FACES = (
    (0, 1, 2, 3),
    (0, 1, 2, 4),
    (0, 1, 2, 5),
    (0, 1, 3, 4),
    (0, 2, 3, 4),
    (1, 2, 3, 4),
)
C_STAR_5 = (0, 1, 3, 4, 2)
R_STAR_5 = (1, 0, 4, 3, 2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("S3--WITT FAIL: " + message)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Devuelve left after right."""
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def order(permutation: tuple[int, ...]) -> int:
    identity = tuple(range(len(permutation)))
    power = identity
    for candidate in range(1, 13):
        power = compose(permutation, power)
        if power == identity:
            return candidate
    raise RuntimeError("S3--WITT FAIL: orden no encontrado")


def parity(permutation: tuple[int, ...]) -> int:
    return sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    ) % 2


def codeword(left: tuple[int, ...]) -> tuple[int, ...]:
    right = tuple(
        sum(left[i] * AW[i][j] for i in range(6)) % 3
        for j in range(6)
    )
    return left + right


def witt_hexads() -> set[frozenset[int]]:
    words = [codeword(left) for left in itertools.product(range(3), repeat=6)]
    hexads = {
        frozenset(i for i, value in enumerate(word) if value)
        for word in words
        if sum(value != 0 for value in word) == 6
    }
    require(len(hexads) == 132, "deben reconstruirse 132 hexadas")
    counts: dict[tuple[int, ...], int] = {}
    for hexad in hexads:
        for subset in itertools.combinations(sorted(hexad), 5):
            counts[subset] = counts.get(subset, 0) + 1
    require(len(counts) == 792 and set(counts.values()) == {1}, "S(5,6,12)")
    return hexads


def star(face: tuple[int, ...], hexads: set[frozenset[int]]) -> tuple[int, ...]:
    fixed = frozenset(face)
    containing = [hexad for hexad in hexads if fixed <= hexad]
    require(len(containing) == 4, "cada tetrada debe abrir cuatro hexadas")
    permutation = list(IDENTITY_12)
    petals = []
    for hexad in containing:
        pair = tuple(sorted(hexad - fixed))
        require(len(pair) == 2, "pétalo binario")
        petals.append(pair)
        a, b = pair
        permutation[a] = b
        permutation[b] = a
    require(set().union(*(set(pair) for pair in petals)) == set(range(12)) - set(fixed), "partición por pétalos")
    result = tuple(permutation)
    require(all(frozenset(result[i] for i in h) in hexads for h in hexads), "la estrella preserva W12")
    return result


def closure(generators: tuple[tuple[int, ...], ...]) -> set[tuple[int, ...]]:
    group = {IDENTITY_12}
    queue: deque[tuple[int, ...]] = deque([IDENTITY_12])
    while queue:
        current = queue.popleft()
        for generator in generators:
            candidate = compose(generator, current)
            if candidate not in group:
                group.add(candidate)
                queue.append(candidate)
    return group


def a5_coset_action(element: tuple[int, ...]) -> tuple[int, ...]:
    c5 = (1, 2, 3, 4, 0)
    subgroup = set()
    power = IDENTITY_5
    for _ in range(5):
        subgroup.add(power)
        power = compose(c5, power)
    cosets = [
        frozenset(compose(representative, h) for h in subgroup)
        for representative in COS_REPS
    ]
    index = {item: i for i, coset in enumerate(cosets) for item in coset}
    return tuple(index[compose(element, next(iter(coset)))] for coset in cosets)


def generated_s3(cycle: tuple[int, ...], reflection: tuple[int, ...]) -> set[tuple[int, ...]]:
    return closure((cycle, reflection))


def orbits(group: set[tuple[int, ...]]) -> list[tuple[int, ...]]:
    unseen = set(range(12))
    result = []
    while unseen:
        base = min(unseen)
        orbit = tuple(sorted({g[base] for g in group}))
        result.append(orbit)
        unseen.difference_update(orbit)
    return sorted(result)


def find_target_s3(group: set[tuple[int, ...]]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    involutions = sorted(
        g for g in group
        if g != IDENTITY_12 and compose(g, g) == IDENTITY_12
        and all(g[i] != i for i in range(12))
    )
    order_three = sorted(
        g for g in group
        if g != IDENTITY_12
        and compose(compose(g, g), g) == IDENTITY_12
        and compose(g, g) != IDENTITY_12
        and all(g[i] != i for i in range(12))
    )
    require(involutions and order_three, "clases semirregulares 2 y 3")
    for reflection in involutions:
        for cycle in order_three:
            if compose(compose(reflection, cycle), reflection) != inverse(cycle):
                continue
            subgroup = generated_s3(cycle, reflection)
            if len(subgroup) == 6 and [len(o) for o in orbits(subgroup)] == [6, 6]:
                return cycle, reflection
    raise RuntimeError("S3--WITT FAIL: no se encontró S3 semirregular")


def group_isomorphism(
    c_source: tuple[int, ...],
    r_source: tuple[int, ...],
    c_target: tuple[int, ...],
    r_target: tuple[int, ...],
) -> dict[tuple[int, ...], tuple[int, ...]]:
    mapping = {IDENTITY_12: IDENTITY_12}
    queue = deque([IDENTITY_12])
    while queue:
        source = queue.popleft()
        target = mapping[source]
        for source_gen, target_gen in ((c_source, c_target), (r_source, r_target)):
            source_next = compose(source_gen, source)
            target_next = compose(target_gen, target)
            if source_next in mapping:
                require(mapping[source_next] == target_next, "homomorfismo S3 bien definido")
            else:
                mapping[source_next] = target_next
                queue.append(source_next)
    require(len(mapping) == 6, "orden seis")
    return mapping


def conjugating_calibre(
    source_group: set[tuple[int, ...]],
    target_group: set[tuple[int, ...]],
    phi: dict[tuple[int, ...], tuple[int, ...]],
) -> tuple[int, ...]:
    source_orbits = orbits(source_group)
    target_orbits = orbits(target_group)
    candidates = []
    for target_order in (target_orbits, list(reversed(target_orbits))):
        for source_bases in itertools.product(*(orbit for orbit in source_orbits)):
            for target_bases in itertools.product(*(orbit for orbit in target_order)):
                sigma = [None] * 12
                valid = True
                for source_base, target_base in zip(source_bases, target_bases):
                    for source_element, target_element in phi.items():
                        source_point = source_element[source_base]
                        target_point = target_element[target_base]
                        if sigma[source_point] not in (None, target_point):
                            valid = False
                            break
                        sigma[source_point] = target_point
                    if not valid:
                        break
                if valid and None not in sigma and len(set(sigma)) == 12:
                    candidate = tuple(int(value) for value in sigma)
                    if all(
                        compose(compose(candidate, source), inverse(candidate)) == phi[source]
                        for source in source_group
                    ):
                        candidates.append(candidate)
    require(candidates, "debe existir un calibre conjugante")
    return min(candidates)


def one_based(permutation: tuple[int, ...]) -> list[int]:
    return [value + 1 for value in permutation]


def audit() -> dict[str, object]:
    hexads = witt_hexads()
    generators = tuple(star(face, hexads) for face in GENERATOR_FACES)
    m12 = closure(generators)
    require(len(m12) == 95040, "orden de M12")

    c_source = a5_coset_action(C_STAR_5)
    r_source = a5_coset_action(R_STAR_5)
    require(compose(compose(r_source, c_source), r_source) == inverse(c_source), "presentación S3 source")
    source_s3 = generated_s3(c_source, r_source)
    require(len(source_s3) == 6 and [len(o) for o in orbits(source_s3)] == [6, 6], "S3 source semirregular")

    c_target, r_target = find_target_s3(m12)
    target_s3 = generated_s3(c_target, r_target)
    phi = group_isomorphism(c_source, r_source, c_target, r_target)
    sigma = conjugating_calibre(source_s3, target_s3, phi)
    sigma_inv = inverse(sigma)

    recalibrated_hexads = {
        frozenset(sigma_inv[point] for point in hexad)
        for hexad in hexads
    }
    require(
        all(
            frozenset(source[point] for point in hexad) in recalibrated_hexads
            for source in source_s3
            for hexad in recalibrated_hexads
        ),
        "el S3 HMT preserva el W12 recalibrado",
    )
    recalibrated_list = sorted(recalibrated_hexads, key=lambda block: tuple(sorted(block)))
    recalibrated_index = {block: index for index, block in enumerate(recalibrated_list)}
    incidence = [
        [1 if point in block else 0 for point in range(12)]
        for block in recalibrated_list
    ]
    for source in source_s3:
        for block_index, block in enumerate(recalibrated_list):
            image = frozenset(source[point] for point in block)
            image_index = recalibrated_index[image]
            for point in range(12):
                require(
                    incidence[image_index][source[point]] == incidence[block_index][point],
                    "equivarianza exacta de la incidencia recalibrada",
                )
    require(
        any(
            frozenset(source[point] for point in hexad) not in hexads
            for source in source_s3 - {IDENTITY_12}
            for hexad in hexads
        ),
        "el calibre original debe conservar su no-go",
    )

    source_profile = Counter(
        (order(g), sum(g[i] == i for i in range(12)))
        for g in source_s3
    )
    target_profile = Counter(
        (order(g), sum(g[i] == i for i in range(12)))
        for g in target_s3
    )
    require(source_profile == target_profile == Counter({(2, 0): 3, (3, 0): 2, (1, 12): 1}), "carácter de permutación común")
    return {
        "schema": "HMT.S3_Witt_recalibration.v1",
        "status": "PASS",
        "m12_order": len(m12),
        "source_s3_order": len(source_s3),
        "target_s3_order": len(target_s3),
        "source_orbits": [list(orbit) for orbit in orbits(source_s3)],
        "target_orbits": [list(orbit) for orbit in orbits(target_s3)],
        "source_action_profile_order_fixedpoints": {
            str(key): value for key, value in sorted(source_profile.items())
        },
        "target_action_profile_order_fixedpoints": {
            str(key): value for key, value in sorted(target_profile.items())
        },
        "target_cycle_1based": one_based(c_target),
        "target_reflection_1based": one_based(r_target),
        "calibre_sigma_1based": one_based(sigma),
        "recalibrated_design_is_source_s3_invariant": True,
        "recalibrated_point_hexad_incidence_is_source_s3_equivariant": True,
        "original_design_is_source_s3_invariant": False,
        "theorem": (
            "The oriented HMT S3 action on the twelve dodecaphase positions is "
            "permutation-isomorphic to a semiregular S3 subgroup of M12. After "
            "transporting the whole Witt calibration by the explicit permutation "
            "sigma, the point--hexad incidence isometry becomes S3-equivariant. "
            "This does not assert equivariance in the original fixed calibration."
        ),
    }


def main() -> None:
    result = audit()
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_RECALIBRACION_S3_WITT")


if __name__ == "__main__":
    main()
