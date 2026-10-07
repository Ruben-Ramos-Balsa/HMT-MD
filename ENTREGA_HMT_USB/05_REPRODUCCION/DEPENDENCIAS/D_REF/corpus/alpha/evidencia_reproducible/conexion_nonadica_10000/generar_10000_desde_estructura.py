#!/usr/bin/env python3
"""Testigo exacto de 10.000 cifras de la generación HMT de pi, e y phi.

Este archivo está causalmente aislado de los prefijos publicados y de los
archivos de referencia decimal. El único archivo documental que abre es el
catálogo finito TPK de 468 emisiones. Usa además las primitivas declaradas
L0 y L1, embebidas aquí y no cargadas desde archivos externos. A partir de
esa estructura explícita:

1. reconstruye el censo 104976 -> 468 -> 243;
2. selecciona las órbitas D3 de clausura, propagación y autoescala;
3. conserva las cinco regiones de la microfibra de clausura;
4. construye lectores racionales exactos para los tres caracteres;
5. poda algebraicamente los 729 elementos de la fibra ambiente en cada nivel;
6. publica 10.000 cifras sólo desde el cilindro ternario superviviente;
7. levanta cada sexteto a su sombra Paley--Witt (q, q A_W).

No importa ``math``, ``decimal``, ``mpmath``, ``sympy`` ni ``numpy``. No
contiene cifras objetivo de pi, e o phi y no abre ningún ledger de bloques.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import csv
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
CATALOGUE = HERE / "inputs" / "TPK_U_catalog_468.json"
OUTPUT_DIR = HERE / "salidas"
CERTIFICATE = HERE / "certificado_generacion_estructural_10000.json"
REFINEMENT_LEDGER = OUTPUT_DIR / "ledger_10000_cifras.csv"

DECIMAL_DIGITS = 10_000
BLOCK_SIZE = 6
NONAD = 9


def minimal_nonadic_blocks(decimal_digits: int) -> int:
    """Menor múltiplo de nueve B con 3^(6B) > 10^decimal_digits."""
    decimal_scale = 10**decimal_digits
    ternary_scale = 1
    blocks = 0
    nonad_scale = 3 ** (BLOCK_SIZE * NONAD)
    while ternary_scale <= decimal_scale:
        blocks += NONAD
        ternary_scale *= nonad_scale
    return blocks


TOTAL_BLOCKS = minimal_nonadic_blocks(DECIMAL_DIGITS)
TOTAL_TRITS = TOTAL_BLOCKS * BLOCK_SIZE
AMBIENT_WORDS = 3**BLOCK_SIZE
BOUND_GUARD_TRITS = 2 * NONAD * BLOCK_SIZE

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

R_PERMUTATION = (2, 0, 1, 4, 5, 3)
S_PERMUTATION = (3, 4, 5, 0, 1, 2)

AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)

L0 = (
    (2, 2, 2, 1, 2, 1),
    (2, 1, 2, 2, 1, 1),
    (1, 0, 0, 1, 0, 2),
    (0, 0, 1, 1, 1, 0),
    (2, 2, 2, 0, 2, 1),
    (2, 1, 2, 1, 0, 0),
)

L1 = (
    (2, 1, 2, 0, 2, 2),
    (1, 2, 1, 1, 2, 0),
    (1, 2, 1, 1, 1, 2),
    (0, 1, 0, 0, 2, 1),
    (2, 0, 2, 1, 0, 1),
    (0, 2, 2, 2, 1, 1),
)

FINITE_CALENDAR = (L0, L0, L1, L1)

PI_TRANSVERSAL_U6 = (501, 614, 498, 169, 272, 272)
PI_TRANSVERSAL_ESIG = "555555"
PI_NEGATIVE_U6 = (870, 923, 810, 418, 674, 521)
PI_NEGATIVE_ESIG = "933717"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def int_fingerprint(value: int) -> dict[str, object]:
    sign = b"-" if value < 0 else b"+"
    magnitude = abs(value)
    raw = magnitude.to_bytes(max(1, (magnitude.bit_length() + 7) // 8), "big")
    return {
        "sign": sign.decode("ascii"),
        "bits": magnitude.bit_length(),
        "sha256_binary": hashlib.sha256(sign + raw).hexdigest(),
    }


def fraction_fingerprint(value: Fraction) -> dict[str, object]:
    return {
        "numerator": int_fingerprint(value.numerator),
        "denominator": int_fingerprint(value.denominator),
    }


def parse_u6(value: str) -> tuple[int, ...]:
    result = tuple(int(item) for item in value.split("|"))
    require(len(result) == 6, f"U6 no tiene seis coordenadas: {value}")
    require(all(0 <= item < 1000 for item in result), f"U6 fuera de base mil: {value}")
    return result


def serialize_u6(u6: Sequence[int]) -> str:
    return "|".join(str(item) for item in u6)


def compact_esig(value: object) -> str:
    compact = "".join(character for character in str(value) if character.isdigit())
    require(len(compact) == 6, f"Esig no tiene seis dígitos: {value}")
    return compact


def psi(u6: Sequence[int]) -> str:
    return "".join(str((-item) % 3) for item in u6)


def permute(values: Sequence[object], permutation: Sequence[int]) -> tuple[object, ...]:
    return tuple(values[index] for index in permutation)


def permute_word(word: str, permutation: Sequence[int]) -> str:
    return "".join(word[index] for index in permutation)


def rotate_word(word: str) -> str:
    return permute_word(word, R_PERMUTATION)


def swap_word(word: str) -> str:
    return permute_word(word, S_PERMUTATION)


def word_orbit(word: str) -> tuple[str, ...]:
    orbit: set[str] = set()
    current = word
    for _ in range(3):
        orbit.add(current)
        orbit.add(swap_word(current))
        current = rotate_word(current)
    return tuple(sorted(orbit))


def trit_census(word: str) -> tuple[int, int, int]:
    return tuple(word.count(str(digit)) for digit in range(3))  # type: ignore[return-value]


def same_census(orbit: Iterable[str]) -> tuple[int, int, int]:
    values = {trit_census(word) for word in orbit}
    require(len(values) == 1, "el censo trítico no es constante en la órbita")
    return next(iter(values))


def select_structural_orbits() -> dict[str, object]:
    raw = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    require(isinstance(raw, list) and len(raw) == 468, "catálogo TPK distinto de 468")

    required_fields = {"U6", "count", "diag_c", "hplus_type", "Esig"}
    rows: list[dict[str, object]] = []
    by_u6: dict[tuple[int, ...], dict[str, object]] = {}
    fibers: dict[str, list[dict[str, object]]] = defaultdict(list)
    for position, item in enumerate(raw):
        require(isinstance(item, dict), f"fila {position} no es un objeto")
        require(required_fields <= set(item), f"fila {position} incompleta")
        u6 = parse_u6(str(item["U6"]))
        require(u6 not in by_u6, f"U6 duplicado: {serialize_u6(u6)}")
        count = int(item["count"])
        row = {
            **item,
            "u6_tuple": u6,
            "count_int": count,
            "diag_c_int": int(item["diag_c"]),
            "word": psi(u6),
        }
        rows.append(row)
        by_u6[u6] = row
        fibers[str(row["word"])].append(row)

    require(len(rows) == 468, "número de emisiones")
    require(len(fibers) == 243, "número de palabras visibles")
    require(sum(int(row["count_int"]) for row in rows) == 104_976, "censo de semillas")

    # La acción D3 se audita sobre las 468 emisiones, no sólo sobre tres palabras.
    for row in rows:
        u6 = row["u6_tuple"]
        require(isinstance(u6, tuple), "U6 interno mal tipado")
        r_u6 = permute(u6, R_PERMUTATION)
        s_u6 = permute(u6, S_PERMUTATION)
        require(r_u6 in by_u6 and s_u6 in by_u6, "D3 no cierra en U6")
        require(
            int(by_u6[r_u6]["count_int"]) == int(row["count_int"])
            and int(by_u6[s_u6]["count_int"]) == int(row["count_int"]),
            "D3 no preserva multiplicidad",
        )
        require(psi(r_u6) == rotate_word(str(row["word"])), "Psi no es r-equivariante")
        require(psi(s_u6) == swap_word(str(row["word"])), "Psi no es s-equivariante")

    orbits = sorted({word_orbit(word) for word in fibers})
    require(len(orbits) == 43, "el cociente W6/D3 no tiene 43 órbitas")
    require(Counter(len(orbit) for orbit in orbits) == Counter({6: 38, 3: 5}),
            "histograma de órbitas D3")

    def fiber_size(word: str) -> int:
        return len(fibers[word])

    def seed_mass(word: str) -> int:
        return sum(int(row["count_int"]) for row in fibers[word])

    def simple_minimal_orbit(orbit: Sequence[str]) -> bool:
        return len(orbit) == 6 and all(
            fiber_size(word) == 1 and int(fibers[word][0]["count_int"]) == 144
            for word in orbit
        )

    def diagonal_support(orbit: Sequence[str]) -> set[int]:
        return {
            int(row["diag_c_int"])
            for word in orbit
            for row in fibers[word]
        }

    closure_candidates = [
        orbit
        for orbit in orbits
        if len(orbit) == 6
        and all(
            fiber_size(word) == 5
            and seed_mass(word) == 1008
            and sorted(int(row["count_int"]) for row in fibers[word])
            == [144, 144, 144, 144, 432]
            for word in orbit
        )
    ]
    require(len(closure_candidates) == 1, "la órbita de clausura no es única")
    closure_orbit = closure_candidates[0]
    closure_census = same_census(closure_orbit)

    radical_singletons = [
        orbit
        for orbit in orbits
        if simple_minimal_orbit(orbit) and diagonal_support(orbit) == {0, 3, 6}
    ]
    require(len(radical_singletons) == 6, "sector radical singleton")

    propagation_candidates = [
        orbit for orbit in radical_singletons if same_census(orbit) == closure_census
    ]
    autoscale_candidates = [
        orbit for orbit in radical_singletons if same_census(orbit) == (2, 2, 2)
    ]
    require(len(propagation_candidates) == 1, "órbita de propagación no única")
    require(len(autoscale_candidates) == 1, "órbita de autoescala no única")
    propagation_orbit = propagation_candidates[0]
    autoscale_orbit = autoscale_candidates[0]

    def orient(orbit: Sequence[str]) -> str:
        matches = [
            word
            for word in orbit
            if any(
                int(row["diag_c_int"]) == 6 and str(row["hplus_type"]) == "ES"
                for row in fibers[word]
            )
        ]
        require(len(matches) == 1, "el gauge no orienta de modo único")
        return matches[0]

    words = {
        "pi": orient(closure_orbit),
        "e": orient(propagation_orbit),
        "phi": orient(autoscale_orbit),
    }
    pi_rows = sorted(fibers[words["pi"]], key=lambda row: row["u6_tuple"])
    require(len(pi_rows) == 5, "la microfibra de clausura no tiene cinco regiones")
    require(sum(int(row["count_int"]) for row in pi_rows) == 1008, "masa de clausura")
    require(
        sorted(int(row["count_int"]) for row in pi_rows) == [144, 144, 144, 144, 432],
        "patrón 432+4*144",
    )
    anchor = [row for row in pi_rows if int(row["count_int"]) == 432]
    companions = [row for row in pi_rows if int(row["count_int"]) == 144]
    require(len(anchor) == 1 and len(companions) == 4, "descomposición 1+4")

    tail_histogram = Counter(
        tuple(row["u6_tuple"][3:])  # type: ignore[index]
        for row in pi_rows
    )
    require(
        sorted(tail_histogram.values()) == [1, 4],
        "la microfibra no presenta cola común 4+1",
    )
    common_tail = tail_histogram.most_common(1)[0][0]
    positive = [
        row for row in pi_rows
        if str(row["hplus_type"]) == "ES"
    ]
    transversal = [
        row for row in pi_rows
        if row["u6_tuple"] == PI_TRANSVERSAL_U6
        and compact_esig(row["Esig"]) == PI_TRANSVERSAL_ESIG
        and int(row["count_int"]) == 432
        and str(row["hplus_type"]) == "NO"
        and tuple(row["u6_tuple"][3:]) == common_tail  # type: ignore[index]
    ]
    negative = [
        row for row in pi_rows
        if row["u6_tuple"] == PI_NEGATIVE_U6
        and compact_esig(row["Esig"]) == PI_NEGATIVE_ESIG
        and int(row["count_int"]) == 144
        and str(row["hplus_type"]) == "NO"
        and tuple(row["u6_tuple"][3:]) != common_tail  # type: ignore[index]
    ]
    require(
        (len(positive), len(negative), len(transversal)) == (3, 1, 1),
        "roles regionales distintos de 3++ + 1-- + 1 transversal",
    )

    role_by_u6 = {
        **{row["u6_tuple"]: "++" for row in positive},
        **{row["u6_tuple"]: "--" for row in negative},
        **{row["u6_tuple"]: "transversal" for row in transversal},
    }
    require(
        role_by_u6[PI_TRANSVERSAL_U6] == "transversal"
        and role_by_u6[PI_NEGATIVE_U6] == "--",
        "identidad canónica de los papeles transversal y retorno mutado",
    )

    regions = [
        {
            "U6": serialize_u6(row["u6_tuple"]),  # type: ignore[arg-type]
            "multiplicity": int(row["count_int"]),
            "Esig": compact_esig(row["Esig"]),
            "diag_c": int(row["diag_c_int"]),
            "hplus_type": str(row["hplus_type"]),
            "role": role_by_u6[row["u6_tuple"]],
        }
        for row in pi_rows
    ]
    regional_payload = json.dumps(regions, sort_keys=True, separators=(",", ":")).encode()

    return {
        "rows": rows,
        "fibers": fibers,
        "words": words,
        "orbits": {
            "pi": list(closure_orbit),
            "e": list(propagation_orbit),
            "phi": list(autoscale_orbit),
        },
        "pi_regions": regions,
        "pi_region_fingerprint": hashlib.sha256(regional_payload).hexdigest(),
        "anchor_regions": len(anchor),
        "companion_regions": len(companions),
        "pi_role_census": {
            "++": len(positive),
            "--": len(negative),
            "transversal": len(transversal),
        },
    }


def tan_add(left: Fraction, right: Fraction) -> Fraction:
    denominator = 1 - left * right
    require(denominator != 0, "suma tangencial singular")
    return (left + right) / denominator


def derive_closure_parameters(region_count: int, companion_count: int) -> dict[str, object]:
    require(region_count > 1 and companion_count > 0, "parámetros de clausura")
    primitive_slope = Fraction(1, region_count)
    accumulated = Fraction(0)
    for _ in range(companion_count):
        accumulated = tan_add(accumulated, primitive_slope)
    require(accumulated > 1, "la rama periférica no cruza la pendiente unidad")

    # Si tan(A)=t, la condición tan(A-arctan(1/q))=1 fuerza
    # q=(1+t)/(t-1). El compensador no se introduce como literal.
    compensator = (1 + accumulated) / (accumulated - 1)
    require(compensator.denominator == 1 and compensator > 1,
            "el compensador de clausura no es entero positivo")
    q = compensator.numerator
    compensator_slope = Fraction(1, q)
    unit_tangent = (
        (accumulated - compensator_slope)
        / (1 + accumulated * compensator_slope)
    )
    require(unit_tangent == 1, "el compensador no devuelve la pendiente unidad")
    return {
        "region_count": region_count,
        "companion_count": companion_count,
        "primitive_slope": primitive_slope,
        "companion_tangent": accumulated,
        "closure_compensator_denominator": q,
        "unit_tangent": unit_tangent,
    }


def closure_pi_bounds(
    region_count: int,
    companion_count: int,
    target_scale: int,
) -> tuple[Fraction, Fraction, dict[str, object]]:
    parameters = derive_closure_parameters(region_count, companion_count)
    q = int(parameters["closure_compensator_denominator"])

    def gcd_int(left: int, right: int) -> int:
        while right:
            left, right = right, left % right
        return abs(left)

    def lcm_of_odds(last_odd: int) -> int:
        value = 1
        for odd in range(1, last_odd + 1, 2):
            value = value // gcd_int(value, odd) * odd
        return value

    def even_term_count(denominator: int, weight: int) -> int:
        # Con N términos (N par), el ancho de la horquilla alternada es el
        # término de índice N. Se reserva la mitad del presupuesto a cada
        # arctangente de la identidad de clausura.
        count = 2
        odd_power = denominator**5
        step = denominator**4
        while 2 * weight * target_scale >= (2 * count + 1) * odd_power:
            count += 2
            odd_power *= step
        return count

    def atan_bounds(denominator: int, terms: int) -> tuple[Fraction, Fraction]:
        require(terms % 2 == 0 and terms >= 2, "truncación alternada no par")
        x = denominator * denominator
        common_odd = lcm_of_odds(2 * terms + 1)

        # Horner evalúa de una vez N+1 términos sobre el denominador común
        # q*lcm(1,3,...,2N+1)*(q^2)^N. Evita miles de reducciones Fraction
        # sin alterar una sola desigualdad de la serie alternada.
        numerator_upper = 0
        for index in range(terms + 1):
            coefficient = common_odd // (2 * index + 1)
            if index % 2:
                coefficient = -coefficient
            numerator_upper = numerator_upper * x + coefficient
        common_denominator = denominator * common_odd * x**terms
        next_numerator = common_odd // (2 * terms + 1)
        lower = Fraction(numerator_upper - next_numerator, common_denominator)
        upper = Fraction(numerator_upper, common_denominator)
        require(lower < upper, "horquilla de arctangente invertida")
        return lower, upper

    primary_terms = even_term_count(
        region_count, 4 * companion_count
    )
    mirror_terms = even_term_count(q, 4)
    primary_lower, primary_upper = atan_bounds(region_count, primary_terms)
    mirror_lower, mirror_upper = atan_bounds(q, mirror_terms)
    lower = 4 * (companion_count * primary_lower - mirror_upper)
    upper = 4 * (companion_count * primary_upper - mirror_lower)
    require(lower < upper, "cotas de clausura invertidas")
    require((upper - lower) * target_scale < 1, "precisión de clausura insuficiente")
    return lower, upper, {
        **parameters,
        "primary_alternating_terms": primary_terms,
        "mirror_alternating_terms": mirror_terms,
        "exact_acceleration": "odd-lcm common denominator and integer Horner",
        "formula": (
            "4*(r*atan(1/p)-atan(1/q)); "
            "p=#regiones, r=#acompañantes, q forzado por tan=1"
        ),
    }


def propagation_e_bounds(target_scale: int) -> tuple[Fraction, Fraction, dict[str, object]]:
    factorial = 1
    partial_numerator = 1
    for n in itertools.count(1):
        factorial *= n
        partial_numerator = n * partial_numerator + 1
        # Para la cola posterior a n:
        # R_n < [1/(n+1)!] / [1-1/(n+2)].
        tail_numerator = n + 2
        tail_denominator = (n + 1) * (n + 1) * factorial
        if tail_numerator * target_scale < tail_denominator:
            lower = Fraction(partial_numerator, factorial)
            upper = lower + Fraction(tail_numerator, tail_denominator)
            return lower, upper, {
                "last_factorial_index": n,
                "coefficient_law": "a_0=1; (n+1)*a_(n+1)=a_n",
                "normalization": "f(0)=1 and f'=f",
                "exact_acceleration": "P_n=n*P_(n-1)+1 over n!",
            }
    raise AssertionError("bucle de propagación inalcanzable")


def autoscale_phi_bounds(target_scale: int) -> tuple[Fraction, Fraction, dict[str, object]]:
    f_n = 1
    f_next = 1
    n = 1
    while target_scale >= f_n * f_next:
        f_n, f_next = f_next, f_n + f_next
        n += 1
    ratio_a = Fraction(f_next, f_n)
    ratio_b = Fraction(f_n + f_next, f_next)
    lower = min(ratio_a, ratio_b)
    upper = max(ratio_a, ratio_b)
    require((upper - lower) * target_scale < 1, "precisión de autoescala")
    polynomial_lower = lower * lower - lower - 1
    polynomial_upper = upper * upper - upper - 1
    require(polynomial_lower < 0 < polynomial_upper,
            "los cocientes no encierran el autovalor de Perron")
    return lower, upper, {
        "F_av": [[0, 1], [1, 1]],
        "fibonacci_index": n,
        "fixed_point_equation": "x=1+1/x",
        "characteristic_equation": "x^2-x-1=0, x>0",
        "exact_acceleration": "Cassini width=1/(F_n*F_(n+1))",
    }


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def base3_word(value: int, width: int = BLOCK_SIZE) -> str:
    digits = []
    current = value
    for _ in range(width):
        digits.append(str(current % 3))
        current //= 3
    require(current == 0, "entero fuera de F3^6")
    return "".join(reversed(digits))


def row_times_matrix_mod3(
    row: Sequence[int], matrix: Sequence[Sequence[int]]
) -> tuple[int, ...]:
    return tuple(
        sum(int(row[i]) * int(matrix[i][j]) for i in range(len(row))) % 3
        for j in range(len(matrix[0]))
    )


def witt_codeword(word: str) -> tuple[int, ...]:
    q = tuple(int(character) for character in word)
    return q + row_times_matrix_mod3(q, AW)


def finite_w30_from_tpk_lifts(words: dict[str, str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for channel in ("pi", "e", "phi"):
        current = tuple(int(character) for character in words[channel])
        blocks = [words[channel]]
        for matrix in FINITE_CALENDAR:
            current = row_times_matrix_mod3(current, matrix)
            blocks.append("".join(str(value) for value in current))
        result[channel] = blocks
    return result


def verify_exceptional_729() -> dict[str, object]:
    square = tuple(
        tuple(
            sum(AW[i][k] * AW[k][j] for k in range(6)) % 3
            for j in range(6)
        )
        for i in range(6)
    )
    expected = tuple(
        tuple(2 if i == j else 0 for j in range(6))
        for i in range(6)
    )
    require(square == expected, "A_W^2 no es -I")

    weights: Counter[int] = Counter()
    codewords: set[tuple[int, ...]] = set()
    for q in itertools.product(range(3), repeat=6):
        word = "".join(str(value) for value in q)
        code = witt_codeword(word)
        codewords.add(code)
        weights[sum(value != 0 for value in code)] += 1
    require(len(codewords) == 729, "el código gráfico no tiene 729 palabras")
    require(weights == Counter({0: 1, 6: 264, 9: 440, 12: 24}),
            "enumerador de pesos Paley--Witt")
    require(54 * (5 * 729 + 1) == 196_884, "identidad APP--Moonshine")
    return {
        "A_W_squared": "2*I=-I over F3",
        "message_space": "F3^6",
        "message_count": 729,
        "same_cardinal_as": "F9^3",
        "graph_code": "(q,q*A_W)",
        "weight_enumerator": {
            str(weight): count for weight, count in sorted(weights.items())
        },
        "moonshine_arithmetic_bridge": "196884=54*(5*729+1)",
        "scope": (
            "sombra excepcional paralela de cada nivel; "
            "no selecciona las cifras arquimedianas"
        ),
    }


def fractional_bounds(
    lower: Fraction, upper: Fraction
) -> tuple[int, Fraction, Fraction]:
    integer_lower = floor_fraction(lower)
    integer_upper = floor_fraction(upper)
    require(integer_lower == integer_upper, "parte entera no fijada")
    frac_lower = lower - integer_lower
    frac_upper = upper - integer_lower
    require(0 < frac_lower < frac_upper < 1, "cotas fraccionarias inválidas")
    return integer_lower, frac_lower, frac_upper


def generate_refinement_channel(
    channel: str,
    lower: Fraction,
    upper: Fraction,
    blocks_count: int,
) -> dict[str, object]:
    integer_part, frac_lower, frac_upper = fractional_bounds(lower, upper)
    prefix = 0
    denominator = 1
    lower_floor = 0
    lower_remainder = frac_lower.numerator
    lower_denominator = frac_lower.denominator
    upper_floor = 0
    upper_remainder = frac_upper.numerator
    upper_denominator = frac_upper.denominator
    rows: list[dict[str, object]] = []
    blocks: list[str] = []
    stream_weights: Counter[int] = Counter()

    for k in range(blocks_count):
        new_denominator = denominator * AMBIENT_WORDS
        base = prefix * AMBIENT_WORDS

        # Los 729 elementos de la fibra ambiente están totalmente ordenados.
        # cuentan exhaustivamente los muertos anteriores, el intervalo de
        # supervivientes y los muertos posteriores. La expansión se actualiza
        # por restos en base 729; no se reconstruyen fracciones gigantes en
        # cada nivel de la conexión conjunta.
        lower_floor = lower_floor * AMBIENT_WORDS
        lower_digit, lower_remainder = divmod(
            lower_remainder * AMBIENT_WORDS, lower_denominator
        )
        lower_floor += lower_digit
        upper_floor = upper_floor * AMBIENT_WORDS
        upper_digit, upper_remainder = divmod(
            upper_remainder * AMBIENT_WORDS, upper_denominator
        )
        upper_floor += upper_digit
        global_first = lower_floor
        global_last = upper_floor if upper_remainder else upper_floor - 1
        first = max(base, global_first)
        last = min(base + AMBIENT_WORDS - 1, global_last)
        require(first <= last, f"{channel}: ninguna prolongación en K={k}")
        survivor_count = last - first + 1
        require(survivor_count == 1,
                f"{channel}: {survivor_count} supervivientes en K={k}")

        candidate = first - base
        word = base3_word(candidate)
        code = witt_codeword(word)
        weight = sum(value != 0 for value in code)
        stream_weights[weight] += 1

        prefix = first
        denominator = new_denominator
        phase = 9 if k % 9 == 0 else k % 9
        prefix_mark = int_fingerprint(prefix)
        rows.append(
            {
                "channel": channel,
                "K": k,
                "phase9": phase,
                "ambient_candidates": AMBIENT_WORDS,
                "survivors": survivor_count,
                "killed_before": candidate,
                "killed_after": AMBIENT_WORDS - candidate - 1,
                "candidate_index": candidate,
                "block": word,
                "prefix_trits": (k + 1) * BLOCK_SIZE,
                "prefix_bits": prefix_mark["bits"],
                "prefix_sha256": prefix_mark["sha256_binary"],
                "witt_right": "".join(str(value) for value in code[6:]),
                "witt_weight": weight,
            }
        )
        blocks.append(word)

    require(all(int(row["survivors"]) == 1 for row in rows), "poda no unitaria")
    require(all(
        int(row["killed_before"]) + int(row["survivors"]) + int(row["killed_after"])
        == AMBIENT_WORDS
        for row in rows
    ), "partición de 729 incompleta")

    phase_returns = []
    local_visible_repeat_pairs: list[list[int]] = []
    for k in range(blocks_count - NONAD):
        before = rows[k]
        after = rows[k + NONAD]
        require(before["phase9"] == after["phase9"], "la fase no retorna")
        require(
            (before["prefix_trits"], before["prefix_sha256"])
            != (after["prefix_trits"], after["prefix_sha256"]),
            "el estado completo se reinició",
        )
        local_changed = (
            before["block"],
            before["candidate_index"],
            before["witt_right"],
            before["witt_weight"],
        ) != (
            after["block"],
            after["candidate_index"],
            after["witt_right"],
            after["witt_weight"],
        )
        if not local_changed:
            local_visible_repeat_pairs.append([k, k + NONAD])
        phase_returns.append((k, k + NONAD))

    phase_nine_returns = [
        (k, k + NONAD)
        for k in range(0, blocks_count - NONAD, NONAD)
    ]
    require(
        len(phase_nine_returns) == blocks_count // NONAD - 1,
        "número de vueltas nonádicas",
    )

    decimal_scale = 10**DECIMAL_DIGITS
    decimal_low = (prefix * decimal_scale) // denominator
    decimal_high = ((prefix + 1) * decimal_scale - 1) // denominator
    decimal_cell_fixed = decimal_low == decimal_high
    fractional_digits = (
        f"{decimal_low:0{DECIMAL_DIGITS}d}" if decimal_cell_fixed else ""
    )
    if decimal_cell_fixed:
        require(len(fractional_digits) == DECIMAL_DIGITS, "longitud decimal")

    return {
        "integer_part": integer_part,
        "fractional_digits": fractional_digits,
        "decimal_cell_fixed": decimal_cell_fixed,
        "blocks": blocks,
        "rows": rows,
        "final_prefix": prefix,
        "final_denominator": denominator,
        "phase_return_pairs": len(phase_returns),
        "phase_nine_complete_returns": len(phase_nine_returns),
        "local_visible_repeat_pairs_after_nine": local_visible_repeat_pairs,
        "stream_witt_weight_histogram": {
            str(weight): count for weight, count in sorted(stream_weights.items())
        },
        "reader_interval": {
            "lower": fraction_fingerprint(lower),
            "upper": fraction_fingerprint(upper),
            "width": fraction_fingerprint(upper - lower),
        },
    }


def write_outputs(
    channels: dict[str, dict[str, object]], blocks_count: int
) -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_meta: dict[str, object] = {}
    for channel, result in channels.items():
        decimal_path = OUTPUT_DIR / f"{channel}_{DECIMAL_DIGITS}_decimales.txt"
        blocks_path = OUTPUT_DIR / f"{channel}_{blocks_count}_bloques_ternarios.txt"
        decimal_path.write_text(
            f"{result['integer_part']}.{result['fractional_digits']}\n",
            encoding="ascii",
        )
        blocks_path.write_text(
            "|".join(result["blocks"]) + "\n",  # type: ignore[arg-type]
            encoding="ascii",
        )
        output_meta[channel] = {
            "decimal_path": decimal_path.relative_to(HERE).as_posix(),
            "decimal_sha256": sha256_file(decimal_path),
            "blocks_path": blocks_path.relative_to(HERE).as_posix(),
            "blocks_sha256": sha256_file(blocks_path),
            "integer_part": result["integer_part"],
            "decimal_digits_after_point": DECIMAL_DIGITS,
            "ternary_blocks": blocks_count,
            "ternary_trits": blocks_count * BLOCK_SIZE,
            "first_block_generated": result["blocks"][0],  # type: ignore[index]
            "first_five_blocks_generated": result["blocks"][:5],  # type: ignore[index]
            "sixth_block_generated": result["blocks"][5],  # type: ignore[index]
            "final_prefix": int_fingerprint(int(result["final_prefix"])),
            "final_denominator": int_fingerprint(int(result["final_denominator"])),
            "phase_return_pairs": result["phase_return_pairs"],
            "phase_nine_complete_returns": result["phase_nine_complete_returns"],
            "local_visible_repeat_pairs_after_nine": result[
                "local_visible_repeat_pairs_after_nine"
            ],
            "stream_witt_weight_histogram": result["stream_witt_weight_histogram"],
        }

    fieldnames = [
        "channel",
        "K",
        "phase9",
        "ambient_candidates",
        "survivors",
        "killed_before",
        "killed_after",
        "candidate_index",
        "block",
        "prefix_trits",
        "prefix_bits",
        "prefix_sha256",
        "witt_right",
        "witt_weight",
    ]
    with REFINEMENT_LEDGER.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for channel in ("pi", "e", "phi"):
            writer.writerows(channels[channel]["rows"])  # type: ignore[arg-type]
    output_meta["refinement_ledger"] = {
        "path": REFINEMENT_LEDGER.relative_to(HERE).as_posix(),
        "sha256": sha256_file(REFINEMENT_LEDGER),
        "rows": 3 * blocks_count,
    }
    return output_meta


def main() -> None:
    started = time.perf_counter()
    require(CATALOGUE.is_file(), f"falta el catálogo {CATALOGUE}")
    selection = select_structural_orbits()
    after_selection = time.perf_counter()
    target_scale = 3 ** (TOTAL_TRITS + BOUND_GUARD_TRITS)

    pi_lower, pi_upper, pi_reader = closure_pi_bounds(
        region_count=len(selection["pi_regions"]),  # type: ignore[arg-type]
        companion_count=int(selection["companion_regions"]),
        target_scale=target_scale,
    )
    e_lower, e_upper, e_reader = propagation_e_bounds(target_scale)
    phi_lower, phi_upper, phi_reader = autoscale_phi_bounds(target_scale)
    after_readers = time.perf_counter()

    bounds = {
        "pi": (pi_lower, pi_upper),
        "e": (e_lower, e_upper),
        "phi": (phi_lower, phi_upper),
    }
    blocks_count = TOTAL_BLOCKS
    while True:
        channels = {
            channel: generate_refinement_channel(channel, lower, upper, blocks_count)
            for channel, (lower, upper) in bounds.items()
        }
        if all(bool(channels[channel]["decimal_cell_fixed"]) for channel in bounds):
            break
        blocks_count += NONAD
        require(
            blocks_count * BLOCK_SIZE <= TOTAL_TRITS + BOUND_GUARD_TRITS,
            "las dos nonadas de guarda no fijan la celda decimal",
        )
    after_refinement = time.perf_counter()

    finite_w30 = finite_w30_from_tpk_lifts(selection["words"])  # type: ignore[arg-type]

    # Estas igualdades enlazan el selector exhaustivo, el tramo finito
    # w6->w30 y el comienzo de la sección coinductiva. Ninguno de los
    # bloques esperados está codificado como palabra objetivo.
    for channel in ("pi", "e", "phi"):
        require(
            channels[channel]["blocks"][0] == selection["words"][channel],  # type: ignore[index]
            f"{channel}: el lector no prolonga la palabra seleccionada por el catálogo",
        )
        require(
            channels[channel]["blocks"][:5] == finite_w30[channel],  # type: ignore[index]
            f"{channel}: el lector no prolonga el w30 producido por L0,L0,L1,L1",
        )

    exceptional = verify_exceptional_729()
    outputs = write_outputs(channels, blocks_count)
    after_outputs = time.perf_counter()
    certificate = {
        "schema": "HMT.conexion-nonadica-conjunta.generacion-estructural-10000.v1",
        "status": "PASS_GENERACION_ESTRUCTURAL_10000_DECIMALES",
        "logical_profile": "HMT_FULL_INTERNAL",
        "force": "DEMOSTRADO_CON_ESTRUCTURA_DE_PARTIDA_EXPLICITA",
        "declared_starting_structure": [
            "catálogo TPK activo de 468 emisiones y multiplicidades",
            "proyección Psi(U)=(-U mod 3) y acción D3 de coordenadas 3+3",
            "gauge de orientación diag_c=6, hplus_type=ES",
            "lifts TPK-full L0,L0,L1,L1 para w6->w30",
            "lector de clausura pentafibra con compensador tangencial unitario",
            "lector de propagación f(0)=1, f'=f",
            "lector de autoescala F_av=[[0,1],[1,1]]",
            "cilindros ternarios de seis trits y supervivencia coinductiva",
            "fase g(K)=K mod 9 con 0 escrito como 9",
            "lift excepcional (q,q*A_W)",
        ],
        "only_documentary_input": {
            "path": CATALOGUE.relative_to(HERE).as_posix(),
            "sha256": sha256_file(CATALOGUE),
        },
        "catalogue": {
            "weighted_seeds": 104_976,
            "emissions": 468,
            "visible_words": 243,
            "ambient_F3_6_words": 729,
            "D3_orbits": 43,
            "selected_orbits": selection["orbits"],
            "oriented_words_generated_by_selector": selection["words"],
            "pi_microfiber": {
                "regions": selection["pi_regions"],
                "region_count": len(selection["pi_regions"]),  # type: ignore[arg-type]
                "total_multiplicity": sum(
                    int(row["multiplicity"])
                    for row in selection["pi_regions"]  # type: ignore[union-attr]
                ),
                "decomposition": "432+4*144=1008",
                "role_census": selection["pi_role_census"],
                "role_decomposition": "3++ + 1-- + 1 transversal",
                "canonical_role_assertions": {
                    "transversal": {
                        "U6": serialize_u6(PI_TRANSVERSAL_U6),
                        "Esig": PI_TRANSVERSAL_ESIG,
                        "multiplicity": 432,
                    },
                    "negative_mutated_return": {
                        "U6": serialize_u6(PI_NEGATIVE_U6),
                        "Esig": PI_NEGATIVE_ESIG,
                        "multiplicity": 144,
                    },
                },
                "regional_state_sha256": selection["pi_region_fingerprint"],
                "interpretation": (
                    "las cinco genealogías se conservan; "
                    "la proyección visible comparte una sola palabra"
                ),
            },
        },
        "finite_chain": {
            "map": "w6 -> w30 -> R36 -> G9",
            "calendar": ["L0", "L0", "L1", "L1"],
            "w30_generated_from_selected_words": finite_w30,
            "R36_first_coinductive_blocks": {
                channel: channels[channel]["blocks"][5]  # type: ignore[index]
                for channel in ("pi", "e", "phi")
            },
            "status": (
                "w30 se deriva por los lifts finitos; R36 abre la "
                "prolongación cilíndrica y no termina la rama"
            ),
        },
        "readers": {
            "pi_closure": {
                **{
                    key: (
                        f"{value.numerator}/{value.denominator}"
                        if isinstance(value, Fraction)
                        else value
                    )
                    for key, value in pi_reader.items()
                },
                "provenance": "FORMALIZACION_NUEVA_DE_ARQUITECTURA_AUTORAL_PREEXISTENTE",
            },
            "e_propagation": {
                **e_reader,
                "provenance": "RESULTADO_RECUPERADO_Y_CERTIFICADO_NUEVO",
            },
            "phi_autoscale": {
                **phi_reader,
                "provenance": "RESULTADO_RECUPERADO_Y_CERTIFICADO_NUEVO",
            },
        },
        "joint_nonadic_connection": {
            "block_alphabet": "F3^6",
            "ambient_fiber_elements_per_level": 729,
            "minimal_nonadic_blocks_for_requested_precision": TOTAL_BLOCKS,
            "blocks_per_channel": blocks_count,
            "trits_per_channel": blocks_count * BLOCK_SIZE,
            "phase_law": "g(K+9)=g(K), 0 represented as 9",
            "phase_return_pairs_verified_per_channel": channels["pi"]["phase_return_pairs"],
            "complete_phase9_returns_verified_per_channel": channels["pi"][
                "phase_nine_complete_returns"
            ],
            "memory_law": (
                "la fase retorna; el prefijo, la profundidad y el cilindro se "
                "prolongan. Una eventual repetición de la proyección local "
                "(bloque, índice, sombra Witt) no reinicia el estado completo"
            ),
            "all_partitions": "killed_before + 1 survivor + killed_after = 729",
            "all_refinement_levels_have_unique_compatible_extension": all(
                all(int(row["survivors"]) == 1 for row in channels[channel]["rows"])  # type: ignore[union-attr]
                for channel in ("pi", "e", "phi")
            ),
            "inverse_limit_statement": (
                "la sección coinductiva infinita es el objeto matemático; "
                "10.000 cifras son un truncamiento certificado de la misma "
                "rama, no el límite de la ley"
            ),
        },
        "exceptional_shadow": exceptional,
        "outputs": outputs,
        "causal_isolation": {
            "not_read": [
                "prefijos decimales o ternarios publicados",
                "ledger de veinte bloques",
                "archivos de referencia decimal",
                "archivos externos de L0 o L1",
                "estados Hensel reconstruidos desde las constantes",
                "alpha o CODATA",
                "bibliotecas numéricas de constantes",
            ],
            "declared_primitives_used_not_loaded_from_external_files": [
                "L0",
                "L1",
            ],
            "decimal_publication_rule": (
                "las 10.000 cifras se calculan únicamente cuando el cilindro "
                "ternario final completo yace en una sola celda decimal"
            ),
        },
        "provenance": {
            "architecture": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "catalogue_and_orbits": "RESULTADO_RECUPERADO",
            "exact_executable_readers": "FORMALIZACION_NUEVA",
            "10000_digit_truncation_run": "CERTIFICADO_NUEVO",
            "constant_values": "NO_SE_ROTULAN_COMO_RESULTADO_NUEVO",
        },
        "generator_sha256": sha256_file(Path(__file__).resolve()),
    }
    CERTIFICATE.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PASS_GENERACION_ESTRUCTURAL_10000_DECIMALES")
    print(
        json.dumps(
            {
                "decimal_digits": DECIMAL_DIGITS,
                "blocks_per_channel": blocks_count,
                "trits_per_channel": blocks_count * BLOCK_SIZE,
                "complete_nonads_per_channel": blocks_count // NONAD - 1,
                "phase_pairs_per_channel": blocks_count - NONAD,
                "seconds": after_outputs - started,
            },
            sort_keys=True,
        )
    )
    print(CERTIFICATE)


if __name__ == "__main__":
    main()
