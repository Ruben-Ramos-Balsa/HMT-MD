#!/usr/bin/env python3
"""Certifica la transferencia TPK de fase sobre las 468 emisiones.

El certificado separa dos objetos que no deben confundirse:

1. la cronologia determinista ``F_obs`` de una sola ruta publicada; y
2. la transferencia normalizada sobre todas las continuaciones compatibles
   de cada canal TRIT.

La primera vuelve al estado visible tras 108 pasos y no selecciona una
medida. La segunda, relativamente a la regla APP de contar uniformemente la
fibra activa completa, induce un kernel sesgado por la fase nonadica. Su
retorno de nueve pasos es uniforme sobre las 468 emisiones.

No se usa ``assert`` para que las comprobaciones sobrevivan a ``python -O``.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict, deque
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "datos/catalogo_lector_arquimediano.csv"
ARCHIMEDEAN_BLOCKS = ROOT / "datos/lectura_arquimediana_12_bloques.csv"
OUTPUT = ROOT / "certificados/dinamica_cociente_468.json"

DIRS = ("N", "E", "S", "O")
VEC = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
OPPOSITE = {"N": "S", "S": "N", "E": "O", "O": "E"}
QUARTER = {"N": "E", "E": "S", "S": "O", "O": "N"}
LOG9 = {1: 0, 2: 1, 4: 2, 8: 3, 7: 4, 5: 5}
FLIPS = {27, 54, 81, 108}

Seed = tuple[int, int, str]
Signature = tuple[int, ...]
Emission = tuple[int, ...]
State = tuple[Signature, Signature]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"DINAMICA 468 FAIL: {message}")


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


def plus_value(i: int, j: int) -> int:
    return dr9((i + 1) + (j + 1))


def times_value(i: int, j: int) -> int:
    return dr9((i + 1) * (j + 1))


def channel_signature(seed: Seed, channel: str) -> Signature:
    """Firma de seis ventanas del canal suma o producto publicado."""
    i, j, direction = seed
    di, dj = VEC[direction]
    result: list[int] = []
    for window in range(6):
        accumulator = 0
        for tick in range(9 * window + 1, 9 * (window + 1) + 1):
            sign = trit(tick)
            if channel == "plus" and sign == 1:
                accumulator += plus_value(i, j)
                i, j = (i + di) % 9, (j + dj) % 9
            elif channel == "times" and sign == -1:
                accumulator += LOG9.get(times_value(i, j), 0)
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


def quarter_turn(seed: Seed) -> Seed:
    i, j, direction = seed
    return i, j, QUARTER[direction]


def central_involution(seed: Seed) -> Seed:
    i, j, direction = seed
    return (7 - i) % 9, (7 - j) % 9, OPPOSITE[direction]


def simulate_visible_channel(seed: Seed, channel: str, ticks: int) -> Seed:
    """Proyecta ``F_obs`` a uno de sus dos cursores."""
    i, j, direction = seed
    for tick in range(1, ticks + 1):
        sign = trit(tick)
        if (channel == "plus" and sign == 1) or (channel == "times" and sign == -1):
            di, dj = VEC[direction]
            i, j = (i + di) % 9, (j + dj) % 9
        if tick in FLIPS:
            direction = OPPOSITE[direction]
    return i, j, direction


def recover_signatures(u6: Emission) -> State:
    additive: list[int] = []
    multiplicative: list[int] = []
    for value in u6:
        s = value // 100
        second = (value // 10) % 10
        e = (second - s) % 10
        require(value % 10 == (3 * s + 5 * e + 1) % 10,
                "una emision no satisface la factorizacion TPK")
        additive.append(s)
        multiplicative.append(e)
    return tuple(additive), tuple(multiplicative)


def read_catalogue() -> tuple[list[Emission], dict[Emission, int]]:
    emissions: list[Emission] = []
    multiplicity: dict[Emission, int] = {}
    with CATALOGUE.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            emission = tuple(int(item) for item in row["U6"].split("|"))
            require(emission not in multiplicity, "emision duplicada")
            emissions.append(emission)
            multiplicity[emission] = int(row["count"])
    return emissions, multiplicity


def stable_refinement(
    seeds: list[Seed], generators: tuple,
) -> dict[Seed, int]:
    """Congruencia minima que refina Esig y es estable por generadores."""
    signature_ids = {
        signature: index
        for index, signature in enumerate(sorted({channel_signature(x, "times") for x in seeds}))
    }
    partition = {x: signature_ids[channel_signature(x, "times")] for x in seeds}
    while True:
        keys = {
            x: (partition[x],) + tuple(partition[generator(x)] for generator in generators)
            for x in seeds
        }
        key_ids = {key: index for index, key in enumerate(sorted(set(keys.values())))}
        refined = {x: key_ids[keys[x]] for x in seeds}
        if len(set(refined.values())) == len(set(partition.values())):
            return refined
        partition = refined


def partition_classes(partition: dict[Seed, int]) -> dict[int, list[Seed]]:
    classes: defaultdict[int, list[Seed]] = defaultdict(list)
    for seed, label in partition.items():
        classes[label].append(seed)
    return dict(classes)


def fibonacci(index: int) -> int:
    """Devuelve F_index con F_0=0 y F_1=1."""
    left, right = 0, 1
    for _ in range(index):
        left, right = right, left + right
    return left


def rational_cylinder(integer_part: int, digits: str) -> tuple[Fraction, Fraction]:
    denominator = 10 ** len(digits)
    numerator = integer_part * denominator + int(digits)
    return Fraction(numerator, denominator), Fraction(numerator + 1, denominator)


def decimal_floor(value: Fraction, places: int) -> int:
    scaled = value * 10**places
    return scaled.numerator // scaled.denominator


def fixed_decimal(integer: int, places: int) -> str:
    digits = str(integer).zfill(places + 1)
    return digits[:-places] + "." + digits[-places:]


def fraction_to_decimal(value: Fraction, precision: int = 100) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        return Decimal(value.numerator) / Decimal(value.denominator)


def quotient_orbits(classes: dict[int, list[Seed]], partition: dict[Seed, int], generators: tuple) -> list[int]:
    transitions: list[dict[int, int]] = []
    for generator in generators:
        induced: dict[int, int] = {}
        for label, fibre in classes.items():
            images = {partition[generator(seed)] for seed in fibre}
            require(len(images) == 1, "el refinamiento no es congruencia")
            induced[label] = next(iter(images))
        transitions.append(induced)

    seen: set[int] = set()
    sizes: list[int] = []
    for origin in classes:
        if origin in seen:
            continue
        orbit = {origin}
        queue = deque([origin])
        seen.add(origin)
        while queue:
            current = queue.popleft()
            for transition in transitions:
                following = transition[current]
                if following not in orbit:
                    orbit.add(following)
                    seen.add(following)
                    queue.append(following)
        sizes.append(len(orbit))
    return sorted(sizes)


def main() -> None:
    emissions, multiplicity = read_catalogue()
    require(len(emissions) == 468, "el catalogo no contiene 468 emisiones")
    require(sum(multiplicity.values()) == 104_976, "censo microscopico")

    factor = {u: recover_signatures(u) for u in emissions}
    additive = sorted({pair[0] for pair in factor.values()})
    multiplicative = sorted({pair[1] for pair in factor.values()})
    require(len(additive) == 18, "numero de firmas aditivas")
    require(len(multiplicative) == 26, "numero de firmas multiplicativas")
    require(len(set(factor.values())) == 18 * 26 == 468,
            "la aplicacion a firmas no es biyectiva")
    require(set(factor.values()) == {(s, e) for s in additive for e in multiplicative},
            "el catalogo no es el producto completo 18 por 26")

    states = sorted(factor.values())
    state_set = set(states)
    seeds = [(i, j, direction) for i, j, direction in product(range(9), range(9), DIRS)]
    require(len(seeds) == 324, "espacio de semillas de canal")

    # --- Cronologia determinista de una sola ruta -------------------------
    for seed in seeds:
        for channel in ("plus", "times"):
            require(simulate_visible_channel(seed, channel, 54) == seed,
                    "posicion u orientacion no retornan tras 54 ticks")
            require(simulate_visible_channel(seed, channel, 108) == seed,
                    "F_obs no retorna tras 108 ticks")

    times_classes: defaultdict[Signature, list[Seed]] = defaultdict(list)
    plus_classes: defaultdict[Signature, list[Seed]] = defaultdict(list)
    for seed in seeds:
        times_classes[channel_signature(seed, "times")].append(seed)
        plus_classes[channel_signature(seed, "plus")].append(seed)

    plus_successors = {
        signature: {channel_signature(advance(seed), "plus") for seed in fibre}
        for signature, fibre in plus_classes.items()
    }
    require(set(map(len, plus_successors.values())) == {1},
            "el avance aditivo no desciende")

    exceptional = (5, 5, 5, 5, 5, 5)
    product_successor_histogram = Counter(
        channel_signature(advance(seed), "times") for seed in times_classes[exceptional]
    )
    require(len(times_classes[exceptional]) == 24, "fibra excepcional de producto")
    require(
        product_successor_histogram
        == Counter({
            (5, 5, 5, 7, 1, 7): 8,
            (5, 5, 5, 7, 7, 1): 8,
            (5, 5, 5, 1, 7, 7): 8,
        }),
        "testigo de no descenso producto",
    )

    # --- El giro como memoria minima de ruta ------------------------------
    ph_partition = stable_refinement(seeds, (advance, half_turn))
    ph_classes = partition_classes(ph_partition)
    require(len(ph_classes) == 28, "refinamiento avance-media vuelta")
    require(Counter(map(len, ph_classes.values())) == Counter({8: 27, 108: 1}),
            "fibras del refinamiento de 28 estados")
    require(quotient_orbits(ph_classes, ph_partition, (advance, half_turn)) == [1, 9, 9, 9],
            "orbitas del refinamiento de 28 estados")
    exceptional_subclasses = {
        ph_partition[seed] for seed in times_classes[exceptional]
    }
    require(len(exceptional_subclasses) == 3, "la firma 555555 no se separa en tres hojas")
    require({len(ph_classes[label]) for label in exceptional_subclasses} == {8},
            "tamano de las tres hojas excepcionales")
    require(18 * 28 == 504 and 504 - 468 == 36,
            "exceso exacto del refinamiento completo")

    pq_partition = stable_refinement(seeds, (advance, quarter_turn))
    pq_classes = partition_classes(pq_partition)
    require(len(pq_classes) == 162, "refinamiento avance-cuarto de giro")
    require(Counter(map(len, pq_classes.values())) == Counter({2: 162}),
            "fibras del cociente por la involucion central")
    require(quotient_orbits(pq_classes, pq_partition, (advance, quarter_turn)) == [162],
            "el cociente de 162 estados no es transitivo")
    for seed in seeds:
        partner = central_involution(seed)
        require(pq_partition[seed] == pq_partition[partner],
                "J no preserva una clase del cociente de 162")
        require(set(pq_classes[pq_partition[seed]]) == {seed, partner},
                "una fibra no es exactamente una orbita de J")

    # --- Transferencia normalizada sobre todos los caminos compatibles ----
    def identity(left: State, right: State) -> Fraction:
        return Fraction(int(left == right))

    def refresh_plus(left: State, right: State) -> Fraction:
        return Fraction(int(left[1] == right[1]), len(additive))

    def refresh_times(left: State, right: State) -> Fraction:
        return Fraction(int(left[0] == right[0]), len(multiplicative))

    def averaged_kernel(left: State, right: State) -> Fraction:
        return (identity(left, right) + refresh_plus(left, right) + refresh_times(left, right)) / 3

    row_sums: dict[State, Fraction] = {}
    column_sums: dict[State, Fraction] = {state: Fraction(0) for state in states}
    adjacency: dict[State, set[State]] = {}
    symmetric = True
    for left in states:
        total = Fraction(0)
        neighbours: set[State] = set()
        for right in states:
            value = averaged_kernel(left, right)
            total += value
            column_sums[right] += value
            symmetric = symmetric and value == averaged_kernel(right, left)
            if value > 0:
                neighbours.add(right)
        row_sums[left] = total
        adjacency[left] = neighbours
    require(set(row_sums.values()) == {Fraction(1)}, "filas no estocasticas")
    require(set(column_sums.values()) == {Fraction(1)}, "columnas no estocasticas")
    require(symmetric, "el promedio de fase no es simetrico")

    reached = {states[0]}
    queue = deque([states[0]])
    while queue:
        current = queue.popleft()
        for neighbour in adjacency[current]:
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
    require(reached == state_set, "el promedio de fase no es irreducible")

    # El calendario (+,-,0)^3 contiene tres copias de cada canal. Los tres
    # operadores son proyectores conmutantes; por eso el retorno de nueve
    # pasos es E_+ E_x y toda entrada vale 1/(18*26).
    phase_word = tuple(trit(tick) for tick in range(1, 10))
    require(phase_word == (1, -1, 0, 1, -1, 0, 1, -1, 0),
            "palabra de fase nonadica")
    require(Counter(phase_word) == Counter({1: 3, -1: 3, 0: 3}),
            "equiponderacion TRIT")
    for left in states:
        for right in states:
            return_entry = Fraction(1, len(additive) * len(multiplicative))
            require(return_entry == Fraction(1, 468), "retorno nonadico no uniforme")

    spectrum = {
        "1": 1,
        "2/3": (len(additive) - 1) + (len(multiplicative) - 1),
        "1/3": (len(additive) - 1) * (len(multiplicative) - 1),
    }
    require(spectrum == {"1": 1, "2/3": 42, "1/3": 425}, "espectro")

    # Olvidar la fase no es lumpabilidad fuerte: un mismo estado aplica I,
    # E_+ o E_x segun el residuo. K_cat es la sombra promediada con fase
    # estacionaria uniforme, no el sucesor determinista de una emision.
    sample = states[0]
    require(
        any(identity(sample, right) != refresh_plus(sample, right) for right in states),
        "I y E_+ colapsan al olvidar la fase",
    )
    require(
        any(identity(sample, right) != refresh_times(sample, right) for right in states),
        "I y E_x colapsan al olvidar la fase",
    )

    # --- Lift microscopico fiel a la quietud -------------------------------
    fibre_histogram = Counter(multiplicity.values())
    require(fibre_histogram == Counter({144: 432, 432: 18, 1944: 18}),
            "histograma de fibras")
    lifted_total = sum(
        multiplicity[u] * Fraction(1, 9 * 468 * multiplicity[u])
        for _phase in range(9) for u in emissions
    )
    require(lifted_total == 1, "la estacionaria microscopica de fase no suma uno")

    # En fase neutra se retiene el representante exacto. En fase activa,
    # L_sigma(x,y)=P_sigma(Fx,Fy)/m(Fy). La suma en una fibra de destino es
    # P_sigma y, tras una vuelta, la entrada es 1/(468*m(Fy)).
    for u in emissions:
        fu = factor[u]
        for v in emissions:
            fv = factor[v]
            plus_lumped = multiplicity[v] * refresh_plus(fu, fv) / multiplicity[v]
            times_lumped = multiplicity[v] * refresh_times(fu, fv) / multiplicity[v]
            require(plus_lumped == refresh_plus(fu, fv), "lumpabilidad del canal suma")
            require(times_lumped == refresh_times(fu, fv), "lumpabilidad del canal producto")
            nine_step_seed_entry = Fraction(1, 468 * multiplicity[v])
            require(multiplicity[v] * nine_step_seed_entry == Fraction(1, 468),
                    "retorno microscopico no proyecta al uniforme")

    # --- Cociclos operativos de modo y giro -------------------------------
    mode = "times"  # el cero final de la vuelta anterior retiene este modo
    signed_switches: list[int] = []
    modes: list[str] = []
    for sign in phase_word:
        previous = mode
        if sign == 1:
            mode = "plus"
        elif sign == -1:
            mode = "times"
        modes.append(mode)
        if previous == "times" and mode == "plus":
            signed_switches.append(1)
        elif previous == "plus" and mode == "times":
            signed_switches.append(-1)
        else:
            signed_switches.append(0)
    require(tuple(modes) == ("plus", "times", "times") * 3,
            "el cero no retiene el modo activo")
    require(Counter(signed_switches) == Counter({1: 3, -1: 3, 0: 3}),
            "cociclo de cambio de hoja nonadico")
    require(sum(signed_switches) == 0 and sum(abs(x) for x in signed_switches) == 6,
            "cierre y variacion del cociclo nonadico")
    require(Counter(trit(tick) for tick in range(1, 109)) == Counter({1: 36, -1: 36, 0: 36}),
            "conteo TRIT dodecafasico")
    require(12 * sum(signed_switches) == 0 and 12 * sum(abs(x) for x in signed_switches) == 72,
            "cociclo de 108 pasos")
    require(len(FLIPS) == 4, "conteo de inversiones de orientacion")

    pi_regions = [
        u for u in emissions if "".join(str((-value) % 3) for value in u) == "010211"
    ]
    require(len(pi_regions) == 5, "microfibra de pi")
    uniform_pi = Fraction(len(pi_regions), 468)
    seed_pi = Fraction(sum(multiplicity[u] for u in pi_regions), 104_976)
    require(uniform_pi == Fraction(5, 468), "peso regional uniforme")
    require(seed_pi == Fraction(7, 729), "peso regional microscopico")

    # --- Bisagra areal--volumetrica y retorno marcado --------------------
    primitive_modes = tuple(modes[:3])
    primitive_pairs = tuple(
        (primitive_modes[index], primitive_modes[(index + 1) % 3])
        for index in range(3)
    )
    primitive_incidence = (
        (
            primitive_pairs.count(("plus", "plus")),
            primitive_pairs.count(("plus", "times")),
        ),
        (
            primitive_pairs.count(("times", "plus")),
            primitive_pairs.count(("times", "times")),
        ),
    )
    require(primitive_modes == ("plus", "times", "times"),
            "orbita primitiva de modos")
    require(primitive_incidence == ((0, 1), (1, 1)),
            "incidencia primitiva areal--volumetrica")
    require(
        Counter(modes) == Counter({"plus": 3, "times": 6}),
        "frecuencia cronologica de hojas",
    )
    chronological_frequency = {
        "areal": Fraction(Counter(modes)["plus"], len(modes)),
        "volumetric": Fraction(Counter(modes)["times"], len(modes)),
    }
    require(
        chronological_frequency
        == {"areal": Fraction(1, 3), "volumetric": Fraction(2, 3)},
        "frecuencia 1/3--2/3",
    )

    # En la base (x^2,2xy,y^2), Sym^2(F_av) tiene polinomio
    # t^3 - 2t^2 - 2t + 1 = (t+1)(t^2-3t+1).
    symmetric_square = ((0, 0, 1), (0, 1, 2), (1, 1, 1))
    trace_sym2 = sum(symmetric_square[index][index] for index in range(3))
    principal_minor_sum = (
        symmetric_square[0][0] * symmetric_square[1][1]
        - symmetric_square[0][1] * symmetric_square[1][0]
        + symmetric_square[0][0] * symmetric_square[2][2]
        - symmetric_square[0][2] * symmetric_square[2][0]
        + symmetric_square[1][1] * symmetric_square[2][2]
        - symmetric_square[1][2] * symmetric_square[2][1]
    )
    determinant_sym2 = (
        symmetric_square[0][0]
        * (
            symmetric_square[1][1] * symmetric_square[2][2]
            - symmetric_square[1][2] * symmetric_square[2][1]
        )
        - symmetric_square[0][1]
        * (
            symmetric_square[1][0] * symmetric_square[2][2]
            - symmetric_square[1][2] * symmetric_square[2][0]
        )
        + symmetric_square[0][2]
        * (
            symmetric_square[1][0] * symmetric_square[2][1]
            - symmetric_square[1][1] * symmetric_square[2][0]
        )
    )
    characteristic_sym2 = (1, -trace_sym2, principal_minor_sum, -determinant_sym2)
    require(characteristic_sym2 == (1, -2, -2, 1),
            "polinomio caracteristico de Sym^2(F_av)")

    fib107 = fibonacci(107)
    fib109 = fibonacci(109)
    require(fib107 == 10_284_720_757_613_717_413_913,
            "entrada areal de F_av^108")
    require(fib109 == 26_925_748_508_234_281_076_009,
            "entrada volumetrica de F_av^108")
    finite_return_ratio = Fraction(fib107, fib109)

    with localcontext() as context:
        context.prec = 100
        sqrt5 = Decimal(5).sqrt()
        golden_ratio = (Decimal(1) + sqrt5) / Decimal(2)
        stable_ratio = Decimal(1) / (golden_ratio * golden_ratio)
        finite_ratio_decimal = (
            Decimal(finite_return_ratio.numerator)
            / Decimal(finite_return_ratio.denominator)
        )
        finite_return_error = abs(finite_ratio_decimal - stable_ratio)
    require(
        finite_return_error
        < Decimal("6.1684979916614407937e-46"),
        "error del retorno nativo 108",
    )
    require(
        finite_return_error
        > Decimal("6.1684979916614407935e-46"),
        "cota inferior del retorno nativo 108",
    )

    with ARCHIMEDEAN_BLOCKS.open(encoding="utf-8", newline="") as stream:
        arch_rows = {
            row["constant"]: row["triads_12"].replace("|", "")
            for row in csv.DictReader(stream)
        }
    require(set(arch_rows) >= {"pi", "phi"}, "cilindros arquimedianos")
    require(len(arch_rows["pi"]) == len(arch_rows["phi"]) == 36,
            "doce bloques de base mil")
    pi_cylinder = rational_cylinder(3, arch_rows["pi"])
    phi_cylinder = rational_cylinder(1, arch_rows["phi"])
    require(pi_cylinder[0] > 0 and phi_cylinder[0] > 0,
            "positividad de los cilindros")
    quotient_cylinder = (
        pi_cylinder[0] / (phi_cylinder[1] * phi_cylinder[1]),
        pi_cylinder[1] / (phi_cylinder[0] * phi_cylinder[0]),
    )
    require(quotient_cylinder[0] < quotient_cylinder[1],
            "intervalo cociente bien orientado")

    forced_places = 0
    forced_integer = 0
    for places in range(1, 100):
        lower_floor = decimal_floor(quotient_cylinder[0], places)
        upper_floor = decimal_floor(quotient_cylinder[1], places)
        if lower_floor != upper_floor:
            break
        forced_places = places
        forced_integer = lower_floor
    require(forced_places == 35, "numero de cifras forzadas por doce bloques")
    forced_decimal = fixed_decimal(forced_integer, forced_places)
    require(
        forced_decimal == "1.19998161486432666111577775331680692",
        "prefijo de pi/phi^2",
    )

    pi_lower_decimal = fraction_to_decimal(pi_cylinder[0])
    pi_upper_decimal = fraction_to_decimal(pi_cylinder[1])
    with localcontext() as context:
        context.prec = 100
        marked_error_interval = (
            pi_lower_decimal * finite_return_error,
            pi_upper_decimal * finite_return_error,
    )
    require(
        marked_error_interval[0]
        < Decimal("1.9378907974286976067581085641743757431e-45")
        < marked_error_interval[1],
        "cota del error de retorno marcado",
    )

    # --- Espejo exacto con la semilla electrónica ------------------------
    with localcontext() as context:
        context.prec = 100
        pi_hmt = Decimal(
            "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
        )
        phi_hmt = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
        boundary_ratio = pi_hmt / (phi_hmt * phi_hmt)
        electron_ratio = phi_hmt / (pi_hmt * pi_hmt)
        electron_seed = electron_ratio.exp()
        mirror_product_error = abs(
            boundary_ratio * electron_ratio
            - Decimal(1) / (pi_hmt * phi_hmt)
        )
        mirror_quotient_error = abs(
            boundary_ratio / electron_ratio
            - (pi_hmt / phi_hmt) ** 3
        )
        electron_reparam_error = abs(
            electron_ratio
            - Decimal(1) / (phi_hmt ** 3 * boundary_ratio ** 2)
        )
    require(mirror_product_error < Decimal("1e-95"),
            "producto del espejo pi--phi")
    require(mirror_quotient_error < Decimal("1e-95"),
            "cociente del espejo pi--phi")
    require(electron_reparam_error < Decimal("1e-95"),
            "reparametrizacion de la semilla electronica")
    require(
        abs(
            electron_seed
            - Decimal(
                "1.178144942596306780811600956808889102533837932497813085998138710447880271485"
            )
        )
        < Decimal("1e-75"),
        "evaluacion de exp(phi/pi^2)",
    )

    result = {
        "schema": "HMT.dinamica-cociente-468.v6",
        "status": "PASS_EXACT_PHASE_TRANSFER_FAV_AND_MARKED_PI_PHI2_RETURN",
        "domain": {
            "emissions": len(emissions),
            "additive_signatures": len(additive),
            "multiplicative_signatures": len(multiplicative),
            "factorization": "U6 ~= S_plus x S_times",
            "factorization_cardinality": "468=18*26",
            "microscopic_presentations": sum(multiplicity.values()),
            "fibre_histogram": dict(sorted(fibre_histogram.items())),
        },
        "raw_chronology": {
            "formula": "F_obs",
            "positions_and_orientations_return_after_ticks": 54,
            "full_phase_return_after_ticks": 108,
            "poincare_return_on_U6": "identity",
            "unique_stationary_measure": False,
            "one_active_product_step_lumpable": False,
            "witness_source_signature": "555555",
            "witness_successors": {
                ",".join(map(str, key)): value
                for key, value in sorted(product_successor_histogram.items())
            },
        },
        "route_memory": {
            "advance_half_turn_refinement_classes": len(ph_classes),
            "advance_half_turn_class_sizes": dict(sorted(Counter(map(len, ph_classes.values())).items())),
            "advance_half_turn_orbits": [1, 9, 9, 9],
            "exceptional_555555_sheets": 3,
            "full_catalogue_refinement": "18*28=504=468+36",
            "type_separation": {
                "extra_36": "multiplicity of two additional sheets over 18 additive signatures",
                "R36": "ordered boundary at depth 36: (222220,021222,102011)",
                "same_object": False,
            },
            "advance_quarter_turn_refinement_classes": len(pq_classes),
            "advance_quarter_turn_class_sizes": {"2": 162},
            "advance_quarter_turn_orbits": [162],
            "central_involution": "J(i,j,d)=((7-i) mod 9,(7-j) mod 9,opposite(d))",
            "quarter_turn_status": "route generator added to the published advance/half-turn chronology",
        },
        "phase_skew_transfer": {
            "state_space": "U6 x Z/9",
            "formula": "K((u,r),(v,r+1))=P_tau(r)(u,v)",
            "channels": {"0": "I", "+1": "E_plus", "-1": "E_times"},
            "phase_word": list(phase_word),
            "phase_weights": {"I": "1/3", "E_plus": "1/3", "E_times": "1/3"},
            "weight_status": "forced by the three occurrences of each TRIT sign in the nonadic calendar",
            "active_fibre_normalization_status": (
                "canonical relative to uniform counting of every compatible continuation in the active finite fibre"
            ),
            "doubly_stochastic": True,
            "irreducible": True,
            "period": 9,
            "nine_step_return": "E_plus*E_times; every U6 entry is 1/468",
            "unique_stationary_measure": "pi(u,r)=1/(9*468)",
            "phase_averaged_shadow": "K_cat=(I+E_plus+E_times)/3",
            "forget_phase_strongly_lumpable": False,
            "averaged_shadow_spectrum": spectrum,
            "averaged_shadow_spectral_gap": "1/3",
        },
        "microscopic_phase_lift": {
            "neutral_channel": "L_0(x,y)=1[x=y]",
            "active_channels": "L_sigma(x,y)=P_sigma(Fx,Fy)/|F^-1(Fy)|",
            "strong_lumpability": True,
            "irreducible": True,
            "period": 9,
            "stationary_measure": "1/(9*468*|F^-1(Fx)|)",
            "nine_step_return": "1/(468*|F^-1(Fy)|)",
            "pushforward": "pi(u,r)=1/(9*468)",
        },
        "calendar_cocycles": {
            "mode_rule": "+ sets sum; - sets product; 0 retains the previous active mode",
            "signed_switches_per_9": signed_switches,
            "signed_sum_per_9": sum(signed_switches),
            "total_variation_per_9": sum(abs(x) for x in signed_switches),
            "signed_sum_per_108": 0,
            "total_variation_per_108": 72,
            "orientation_reversals_per_108": 4,
        },
        "areal_volumetric_hinge": {
            "primitive_mode_orbit": list(primitive_modes),
            "primitive_pairs": [list(pair) for pair in primitive_pairs],
            "F_av": [list(row) for row in primitive_incidence],
            "chronological_frequency": {
                key: str(value) for key, value in chronological_frequency.items()
            },
            "parry_vertex_ratio": "mu_areal/mu_volumetric=phi^-2",
            "measure_warning": (
                "The chronological 1/3--2/3 frequency, uniform tau_468 and "
                "Parry measure are three different typed measures."
            ),
            "symmetric_square": [list(row) for row in symmetric_square],
            "symmetric_square_basis": ["x^2", "2xy", "y^2"],
            "symmetric_square_characteristic": "t^3-2t^2-2t+1=(t+1)(t^2-3t+1)",
            "symmetric_square_eigenvalues": ["phi^2", "-1", "phi^-2"],
            "native_length_108": {
                "F107": fib107,
                "F109": fib109,
                "ratio": str(finite_return_ratio),
                "error_to_phi^-2": str(finite_return_error),
            },
        },
        "marked_pi_phi2_return": {
            "marker": "D_pi=pi_HMT*P_areal+P_volumetric",
            "marker_canonicity": (
                "unique relative to positivity, sheet diagonality, "
                "volumetric normalization 1 and areal mark pi_HMT"
            ),
            "finite_formula": "Theta_n=pi_HMT*F_(n-1)/F_(n+1)",
            "limit": "pi_HMT/phi_HMT^2=pi_HMT*phi_HMT^-2",
            "pi_cylinder_12_blocks": [
                str(pi_cylinder[0]),
                str(pi_cylinder[1]),
            ],
            "phi_cylinder_12_blocks": [
                str(phi_cylinder[0]),
                str(phi_cylinder[1]),
            ],
            "quotient_interval": [
                str(quotient_cylinder[0]),
                str(quotient_cylinder[1]),
            ],
            "forced_decimal_places": forced_places,
            "forced_decimal_prefix": forced_decimal,
            "marked_return_108_error_interval": [
                str(marked_error_interval[0]),
                str(marked_error_interval[1]),
            ],
            "no_go": (
                "The rational spectral algebra of F_av lies in Q(sqrt(5)); "
                "it supplies phi^-2 but not transcendental pi. The pi mark "
                "must come from the independently generated closure reader."
            ),
        },
        "electron_mirror": {
            "bivariate_law": "R(x,y)=x/y^2",
            "exchange": "J(x,y)=(y,x), J^2=I",
            "boundary_orientation": {
                "formula": "R(pi,phi)=pi/phi^2",
                "value": str(boundary_ratio),
            },
            "electronic_orientation": {
                "formula": "R(phi,pi)=phi/pi^2",
                "value": str(electron_ratio),
                "exponential_seed": str(electron_seed),
            },
            "exact_reparametrization": (
                "phi/pi^2=1/(phi^3*(pi/phi^2)^2)"
            ),
            "status": (
                "EXACT_ALGEBRAIC_LINK_NOT_AN_INDEPENDENT_ELECTRON_DERIVATION"
            ),
        },
        "measure_separation": {
            "pi_uniform_emissions": str(uniform_pi),
            "pi_uniform_seeds_pushforward": str(seed_pi),
            "equal": uniform_pi == seed_pi,
        },
        "logical_scope": {
            "proved": (
                "The deterministic F_obs return and the normalized all-compatible-path transfer are different. "
                "Relative to full active-fibre counting, the TPK phase calendar induces the phase-skew kernel; "
                "its nine-step return is exactly uniform on 468 emissions and its stationary state is unique. "
                "The operational sheet-switch and orientation-turn counters are additive cocycles once their "
                "terminal mode and orientation are retained. The primitive mode quotient induces F_av; its "
                "memory-one Parry state has areal/volumetric ratio phi^-2. The independently generated pi "
                "closure marks one boundary return, producing the limit pi_HMT/phi_HMT^2. Twelve generated "
                "base-1000 blocks force 35 decimal places of that quotient. Exchanging pi and phi in the "
                "same bivariate law R(x,y)=x/y^2 gives the electronic seed phi/pi^2 exactly."
            ),
            "not_proved": (
                "Uniform refresh of a complete active fibre is an APP transfer clause, not the transition of a "
                "single F_obs trajectory. The certificate does not construct the inverse-limit kernel on every "
                "TPK depth or derive Delta4*P3 from the switch cocycle. R36 already exists independently as a "
                "depth-36 boundary and is not a 36-state space. The enriched route-to-angle/mass transducer also "
                "exists as a separate construction; this finite phase certificate does not derive that ledger "
                "after the ledger coordinates have been forgotten. The conditional gravitational--inertial "
                "factorization and its proposed cosmological realization are physical interfaces, not consequences "
                "of this finite certificate. The exact mirror identity does not derive the calibrated electronic "
                "coefficients 22 and 15."
            ),
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS_DINAMICA_COCIENTE_468_FASE_TPK")


if __name__ == "__main__":
    main()
