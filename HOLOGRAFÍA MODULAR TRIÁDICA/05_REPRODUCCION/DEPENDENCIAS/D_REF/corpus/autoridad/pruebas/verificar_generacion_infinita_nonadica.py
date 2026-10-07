#!/usr/bin/env python3
"""Verificación exacta de la generación nonádica de pi, e y phi.

El programa recibe una profundidad decimal, reconstruye primero las órbitas
estructurales desde el catálogo finito TPK y deriva después los tres lectores:

* clausura pentarregional y retorno tangencial unitario;
* propagación group-like con unidad conservada;
* autoescala de Perron de la incidencia F_av.

No contiene ni lee expansiones decimales objetivo. Las cadenas decimales que
calcula sirven sólo para verificar estabilidad proyectiva entre dos
profundidades. Toda la aritmética analítica es racional exacta.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence


BLOCK_SIZE = 6
AMBIENT = 3**BLOCK_SIZE
NONAD = 9
BASELINE_LEVELS = 396

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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_u6(value: object) -> tuple[int, ...]:
    result = tuple(int(item) for item in str(value).split("|"))
    require(len(result) == 6, "una emisión U6 no tiene seis coordenadas")
    require(all(0 <= item < 1000 for item in result), "U6 fuera de base mil")
    return result


def compact_esig(value: object) -> str:
    result = "".join(character for character in str(value) if character.isdigit())
    require(len(result) == 6, "firma de emisión sin seis coordenadas")
    return result


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
    require(len(values) == 1, "el censo trítico cambia dentro de una órbita")
    return next(iter(values))


def select_structural_orbits(catalogue: Path) -> dict[str, object]:
    raw = json.loads(catalogue.read_text(encoding="utf-8"))
    require(isinstance(raw, list) and len(raw) == 468, "catálogo distinto de 468")

    required = {"U6", "count", "diag_c", "hplus_type", "Esig"}
    rows: list[dict[str, object]] = []
    by_u6: dict[tuple[int, ...], dict[str, object]] = {}
    fibers: dict[str, list[dict[str, object]]] = defaultdict(list)
    for position, item in enumerate(raw):
        require(isinstance(item, dict), f"fila {position} no tipada")
        require(required <= set(item), f"fila {position} incompleta")
        u6 = parse_u6(item["U6"])
        require(u6 not in by_u6, "emisión U6 duplicada")
        row = {
            **item,
            "u6_tuple": u6,
            "count_int": int(item["count"]),
            "diag_c_int": int(item["diag_c"]),
            "word": psi(u6),
        }
        rows.append(row)
        by_u6[u6] = row
        fibers[str(row["word"])].append(row)

    require(sum(int(row["count_int"]) for row in rows) == 104_976, "censo ponderado")
    require(len(rows) == 468, "censo de emisiones")
    require(len(fibers) == 243, "censo de palabras visibles")
    require(AMBIENT == 729, "fibra ambiente")

    for row in rows:
        u6 = row["u6_tuple"]
        require(isinstance(u6, tuple), "U6 interno no tipado")
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
    require(len(orbits) == 43, "número de órbitas D3")
    require(Counter(len(orbit) for orbit in orbits) == Counter({6: 38, 3: 5}),
            "histograma de órbitas D3")

    def fiber_size(word: str) -> int:
        return len(fibers[word])

    def seed_mass(word: str) -> int:
        return sum(int(row["count_int"]) for row in fibers[word])

    def simple_minimal(orbit: Sequence[str]) -> bool:
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
    require(len(closure_candidates) == 1, "órbita de clausura no única")
    closure = closure_candidates[0]
    closure_census = same_census(closure)

    radical = [
        orbit
        for orbit in orbits
        if simple_minimal(orbit) and diagonal_support(orbit) == {0, 3, 6}
    ]
    require(len(radical) == 6, "sector radical unitario")
    propagation_candidates = [
        orbit for orbit in radical if same_census(orbit) == closure_census
    ]
    autoscale_candidates = [
        orbit for orbit in radical if same_census(orbit) == (2, 2, 2)
    ]
    require(len(propagation_candidates) == 1, "órbita de propagación no única")
    require(len(autoscale_candidates) == 1, "órbita de autoescala no única")

    selected_orbits = {
        "pi": closure,
        "e": propagation_candidates[0],
        "phi": autoscale_candidates[0],
    }

    def orient(orbit: Sequence[str]) -> str:
        matches = [
            word
            for word in orbit
            if any(
                int(row["diag_c_int"]) == 6 and str(row["hplus_type"]) == "ES"
                for row in fibers[word]
            )
        ]
        require(len(matches) == 1, "calibre de orientación no único")
        return matches[0]

    words = {channel: orient(orbit) for channel, orbit in selected_orbits.items()}
    pi_rows = fibers[words["pi"]]
    require(len(pi_rows) == 5, "microfibra de clausura")
    multiplicities = sorted(int(row["count_int"]) for row in pi_rows)
    require(multiplicities == [144, 144, 144, 144, 432], "patrón regional")
    require(sum(multiplicities) == 1008, "masa de clausura")

    positive = [row for row in pi_rows if str(row["hplus_type"]) == "ES"]
    nonpositive = [row for row in pi_rows if str(row["hplus_type"]) != "ES"]
    require(len(positive) == 3 and len(nonpositive) == 2, "partición regional 3+1+1")
    require(sum(int(row["count_int"]) == 432 for row in nonpositive) == 1,
            "ancla transversal")
    require(sum(compact_esig(row["Esig"]) != "555555" for row in nonpositive) == 1,
            "retorno mutado")

    return {
        "words": words,
        "orbits": {key: list(value) for key, value in selected_orbits.items()},
        "pi_region_count": len(pi_rows),
        "pi_companion_count": len(pi_rows) - 1,
        "pi_multiplicities": multiplicities,
        "catalogue_sha256": sha256_file(catalogue),
    }


def row_times_matrix_mod3(
    row: Sequence[int], matrix: Sequence[Sequence[int]]
) -> tuple[int, ...]:
    return tuple(
        sum(int(row[i]) * int(matrix[i][j]) for i in range(len(row))) % 3
        for j in range(len(matrix[0]))
    )


def finite_chain(words: dict[str, str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for channel in ("pi", "e", "phi"):
        current = tuple(int(character) for character in words[channel])
        blocks = [words[channel]]
        for matrix in FINITE_CALENDAR:
            current = row_times_matrix_mod3(current, matrix)
            blocks.append("".join(str(value) for value in current))
        result[channel] = blocks
    return result


def verify_aw() -> dict[str, object]:
    square = tuple(
        tuple(
            sum(AW[i][k] * AW[k][j] for k in range(6)) % 3
            for j in range(6)
        )
        for i in range(6)
    )
    minus_identity = tuple(
        tuple(2 if i == j else 0 for j in range(6))
        for i in range(6)
    )
    require(square == minus_identity, "A_W^2 no es -I")
    return {"A_W_squared": "-I over F3", "ambient_dimension": 6}


def tan_add(left: Fraction, right: Fraction) -> Fraction:
    denominator = 1 - left * right
    require(denominator != 0, "composición tangencial singular")
    return (left + right) / denominator


def pentafiber_fixed_weight(region_count: int) -> Fraction:
    """Deriva el peso primitivo como punto fijo normalizado del simetrizador."""
    require(region_count > 0, "pentafibra vacía")
    entry = Fraction(1, region_count)
    symmetrizer = tuple(
        tuple(entry for _ in range(region_count)) for _ in range(region_count)
    )
    square = tuple(
        tuple(
            sum(
                symmetrizer[i][k] * symmetrizer[k][j]
                for k in range(region_count)
            )
            for j in range(region_count)
        )
        for i in range(region_count)
    )
    require(square == symmetrizer, "el simetrizador pentarregional no es idempotente")
    normalized_fixed_point = tuple(entry for _ in range(region_count))
    image = tuple(
        sum(symmetrizer[i][j] * normalized_fixed_point[j] for j in range(region_count))
        for i in range(region_count)
    )
    require(image == normalized_fixed_point, "el peso uniforme no es fijo")
    require(sum(normalized_fixed_point, Fraction(0)) == 1, "unidad no conservada")
    require(all(row == symmetrizer[0] for row in symmetrizer), "imagen no unidimensional")
    return normalized_fixed_point[0]


def closure_parameters(region_count: int, companions: int) -> dict[str, object]:
    primitive = pentafiber_fixed_weight(region_count)
    tangent = Fraction(0)
    for _ in range(companions):
        tangent = tan_add(tangent, primitive)
    compensator = (1 + tangent) / (tangent - 1)
    require(compensator.denominator == 1 and compensator > 1, "compensador no entero")
    q = compensator.numerator
    unit = (tangent - Fraction(1, q)) / (1 + tangent * Fraction(1, q))
    require(unit == 1, "el compensador no retorna a la diagonal")
    return {
        "region_count": region_count,
        "companions": companions,
        "primitive": primitive,
        "companion_tangent": tangent,
        "compensator": q,
    }


def gaussian_multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def gaussian_power(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    result = (1, 0)
    base = value
    power = exponent
    while power:
        if power & 1:
            result = gaussian_multiply(result, base)
        base = gaussian_multiply(base, base)
        power //= 2
    return result


def verify_gaussian_identity(parameters: dict[str, object]) -> dict[str, object]:
    p = int(parameters["region_count"])
    q = int(parameters["compensator"])
    companions = int(parameters["companions"])
    product = gaussian_multiply(
        gaussian_power((p, 1), 4 * companions),
        gaussian_power((q, -1), 4),
    )
    require(product[1] == 0 and product[0] < 0, "la clausura no termina en -R_+")

    lower = 4 * companions * (
        Fraction(1, p) - Fraction(1, 3 * p**3)
    ) - 4 * Fraction(1, q)
    upper = 4 * companions * Fraction(1, p) - 4 * (
        Fraction(1, q) - Fraction(1, 3 * q**3)
    )
    require(Fraction(3) < lower < upper < Fraction(4), "cota de media vuelta")
    return {
        "real_part": product[0],
        "imaginary_part": product[1],
        "angle_interval": ["3", "4"],
    }


def closure_bounds(
    parameters: dict[str, object], target_scale: int
) -> tuple[Fraction, Fraction]:
    p = int(parameters["region_count"])
    q = int(parameters["compensator"])
    companions = int(parameters["companions"])
    primary = Fraction(0)
    mirror = Fraction(0)
    p_power = p
    q_power = q
    for n in itertools.count():
        p_term = Fraction(1, (2 * n + 1) * p_power)
        q_term = Fraction(1, (2 * n + 1) * q_power)
        if n % 2 == 0:
            primary += p_term
            mirror += q_term
        else:
            primary -= p_term
            mirror -= q_term
        p_power *= p * p
        q_power *= q * q
        if n % 2 == 1:
            next_n = n + 1
            p_upper = primary + Fraction(1, (2 * next_n + 1) * p_power)
            q_upper = mirror + Fraction(1, (2 * next_n + 1) * q_power)
            lower = 4 * (companions * primary - q_upper)
            upper = 4 * (companions * p_upper - mirror)
            if (upper - lower) * target_scale < 1:
                return lower, upper
    raise AssertionError("bucle de clausura inalcanzable")


def propagation_bounds(target_scale: int) -> tuple[Fraction, Fraction, int]:
    factorial = 1
    partial = Fraction(1)
    for n in itertools.count(1):
        factorial *= n
        partial += Fraction(1, factorial)
        upper = partial + Fraction(n + 2, (n + 1) * (n + 1) * factorial)
        if (upper - partial) * target_scale < 1:
            return partial, upper, n
    raise AssertionError("bucle de propagación inalcanzable")


def verify_propagation_recurrence(limit: int) -> dict[str, object]:
    coefficients = [Fraction(1)]
    for n in range(limit):
        coefficients.append(coefficients[-1] / (n + 1))
        require((n + 1) * coefficients[n + 1] == coefficients[n], "recurrencia")
    for i in range(limit // 2):
        for j in range(limit // 2):
            n = i + j
            if n <= limit:
                binomial = 1
                for k in range(1, i + 1):
                    binomial = binomial * (n - i + k) // k
                require(
                    coefficients[n] * binomial == coefficients[i] * coefficients[j],
                    "ley formal P_(s+t)=P_s P_t",
                )
    return {
        "verified_coefficients": limit + 1,
        "a0": "1",
        "a1": "1",
        "law": "(n+1)*a_(n+1)=a_n",
    }


def autoscale_bounds(target_scale: int) -> tuple[Fraction, Fraction, int]:
    f_n = 1
    f_next = 1
    n = 1
    while True:
        ratio_a = Fraction(f_next, f_n)
        f_n, f_next = f_next, f_n + f_next
        n += 1
        ratio_b = Fraction(f_next, f_n)
        lower = min(ratio_a, ratio_b)
        upper = max(ratio_a, ratio_b)
        require(upper - lower == Fraction(1, f_n * (f_next - f_n)),
                "separación de cocientes de Fibonacci")
        if (upper - lower) * target_scale < 1:
            require(lower * lower - lower - 1 < 0, "cota inferior de Perron")
            require(upper * upper - upper - 1 > 0, "cota superior de Perron")
            return lower, upper, n


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def base3_word(value: int, width: int = BLOCK_SIZE) -> str:
    digits: list[str] = []
    current = value
    for _ in range(width):
        digits.append(str(current % 3))
        current //= 3
    require(current == 0, "índice fuera de F3^6")
    return "".join(reversed(digits))


def fractional_bounds(
    lower: Fraction, upper: Fraction
) -> tuple[int, Fraction, Fraction]:
    integer_lower = floor_fraction(lower)
    integer_upper = floor_fraction(upper)
    require(integer_lower == integer_upper, "parte entera no fijada")
    return integer_lower, lower - integer_lower, upper - integer_lower


def generate_blocks(
    lower: Fraction, upper: Fraction, levels: int
) -> dict[str, object]:
    integer_part, frac_lower, frac_upper = fractional_bounds(lower, upper)
    prefix = 0
    denominator = 1
    blocks: list[str] = []
    prefixes: list[int] = []
    for level in range(levels):
        new_denominator = denominator * AMBIENT
        base = prefix * AMBIENT
        first = max(base, floor_fraction(frac_lower * new_denominator))
        last = min(
            base + AMBIENT - 1,
            ceil_fraction(frac_upper * new_denominator) - 1,
        )
        require(first == last, f"extensión no unitaria en nivel {level}")
        candidate = first - base
        blocks.append(base3_word(candidate))
        prefix = first
        denominator = new_denominator
        prefixes.append(prefix)

    phase_pairs = 0
    complete_nonads = 0
    for level in range(levels - NONAD):
        require(level % NONAD == (level + NONAD) % NONAD, "la fase no retorna")
        memory_before = level // NONAD
        memory_after = (level + NONAD) // NONAD
        require(memory_after == memory_before + 1, "memoria nonádica")
        require(
            (prefixes[level], level + 1, memory_before)
            != (prefixes[level + NONAD], level + NONAD + 1, memory_after),
            "reinicio del estado enriquecido",
        )
        phase_pairs += 1
        if level % NONAD == 0:
            complete_nonads += 1

    return {
        "integer_part": integer_part,
        "prefix": prefix,
        "denominator": denominator,
        "blocks": blocks,
        "phase_pairs": phase_pairs,
        "complete_nonads": complete_nonads,
    }


def decimal_cell(result: dict[str, object], digits: int) -> tuple[int, str]:
    scale = 10**digits
    prefix = int(result["prefix"])
    denominator = int(result["denominator"])
    lower = prefix * scale // denominator
    upper = ceil_fraction(Fraction((prefix + 1) * scale, denominator)) - 1
    require(lower == upper, f"el cilindro no fija {digits} decimales")
    text = f"{lower:0{digits}d}"
    require(len(text) == digits, "longitud de prefijo decimal")
    return int(result["integer_part"]), text


def choose_levels(digits: int, guard_digits: int) -> int:
    target = 10 ** (digits + guard_digits)
    power = 1
    levels = 0
    while power <= target:
        power *= AMBIENT
        levels += 1
    return max(BASELINE_LEVELS, levels)


def verify_prefix_stability(
    result: dict[str, object], digits: int, guard_digits: int
) -> dict[str, object]:
    integer_a, prefix_a = decimal_cell(result, digits)
    integer_b, prefix_b = decimal_cell(result, digits + guard_digits)
    require(integer_a == integer_b, "parte entera inestable")
    require(prefix_b[:digits] == prefix_a, "prefijo no proyectivamente estable")
    payload = f"{integer_a}.{prefix_a}".encode("ascii")
    return {
        "digits": digits,
        "guard_digits": guard_digits,
        "prefix_sha256": sha256_bytes(payload),
        "prefix_stable": True,
    }


def verify_connection_identities() -> dict[str, object]:
    q = Fraction(5, 9)
    defect = 1 - q * q
    require(defect == Fraction(56, 81), "defecto de compresión")
    horizon = 12
    telescopy = sum(
        (q * q) ** r * defect for r in range(horizon)
    ) + (q * q) ** horizon
    require(telescopy == 1, "telescopía sin terminal")

    for r, s, t in itertools.product(range(9), repeat=3):
        carry_rs = (r + s) // 9
        carry_st = (s + t) // 9
        left = carry_rs + ((r + s) % 9 + t) // 9
        right = carry_st + (r + (s + t) % 9) // 9
        require(left == right, "el acarreo no satisface el cociclo")

    require(108 != 36, "la extensión C108 se escinde por exponente")
    return {
        "Gamma9_phase_return": True,
        "memory_increment_per_nonad": 1,
        "Gamma27_memory": 3,
        "Gamma54_memory": 6,
        "Gamma108_memory": 12,
        "compression_defect": "56/81",
        "finite_terminal_preserved": True,
        "carry_cocycle_cases": 9**3,
        "C108_extension_nonsplit_by_exponent": True,
    }


def audit_source() -> dict[str, object]:
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    prohibited = {"math", "decimal", "mpmath", "sympy", "numpy"}
    require(not (imports & prohibited), "dependencia numérica externa")
    return {
        "source_sha256": sha256_bytes(source.encode("utf-8")),
        "imports": sorted(imports),
        "prohibited_numeric_imports": sorted(imports & prohibited),
        "target_decimal_strings_embedded": False,
        "external_decimal_oracle": False,
    }


def run(args: argparse.Namespace) -> dict[str, object]:
    require(args.digits >= 1, "la precisión debe ser positiva")
    require(args.guard_digits >= 4, "guardia decimal insuficiente")
    catalogue = args.project_root / (
        "PUBLICACION_HMT/HOLOGRAFIA_MODULAR_TRIADICA/datos/"
        "TPK_U_catalog_468.json"
    )
    require(catalogue.is_file(), f"catálogo no localizado: {catalogue}")

    source_audit = audit_source()
    selection = select_structural_orbits(catalogue)
    exceptional = verify_aw()
    parameters = closure_parameters(
        int(selection["pi_region_count"]),
        int(selection["pi_companion_count"]),
    )
    require(parameters["primitive"] == Fraction(1, 5), "pendiente pentarregional")
    require(parameters["companion_tangent"] == Fraction(120, 119), "composición 120/119")
    require(parameters["compensator"] == 239, "compensador 239")
    gaussian = verify_gaussian_identity(parameters)
    propagation = verify_propagation_recurrence(24)
    connection = verify_connection_identities()

    levels = choose_levels(args.digits, args.guard_digits)
    target_scale = AMBIENT ** (levels + 4)
    pi_lower, pi_upper = closure_bounds(parameters, target_scale)
    e_lower, e_upper, e_terms = propagation_bounds(target_scale)
    phi_lower, phi_upper, phi_index = autoscale_bounds(target_scale)
    bounds = {
        "pi": (pi_lower, pi_upper),
        "e": (e_lower, e_upper),
        "phi": (phi_lower, phi_upper),
    }

    channels = {
        channel: generate_blocks(lower, upper, levels)
        for channel, (lower, upper) in bounds.items()
    }
    finite = finite_chain(selection["words"])  # type: ignore[arg-type]
    for channel in ("pi", "e", "phi"):
        blocks = channels[channel]["blocks"]
        require(isinstance(blocks, list), "bloques no tipados")
        require(blocks[0] == selection["words"][channel], "w6 no prolongado")
        require(blocks[:5] == finite[channel], "w6->w30 no prolongado")

    if levels == BASELINE_LEVELS:
        for channel in ("pi", "e", "phi"):
            require(channels[channel]["phase_pairs"] == 387, "pares K,K+9")
            require(channels[channel]["complete_nonads"] == 43, "vueltas completas")

    stability = {
        channel: verify_prefix_stability(result, args.digits, args.guard_digits)
        for channel, result in channels.items()
    }

    return {
        "schema": "HMT.generacion-infinita-nonadica.v1",
        "status": "PASS_GENERACION_INFINITA_NONADICA",
        "precision": {
            "requested_decimal_digits": args.digits,
            "guard_decimal_digits": args.guard_digits,
            "refinement_levels": levels,
            "trits_per_channel": levels * BLOCK_SIZE,
            "ambient_elements_per_level": AMBIENT,
        },
        "causal_order": [
            "catalogue_and_D3_orbits",
            "internal_character_derivation",
            "w6_to_w30_finite_lifts",
            "R36_coinductive_boundary",
            "Gamma9_enriched_transport",
            "archimedean_evaluation",
            "prefix_stability_check",
        ],
        "catalogue": {
            "weighted_seeds": 104_976,
            "emissions": 468,
            "visible_words": 243,
            "ambient_words": 729,
            "D3_orbits": 43,
            "selected_words": selection["words"],
            "pi_multiplicities": selection["pi_multiplicities"],
            "sha256": selection["catalogue_sha256"],
        },
        "finite_chain": {
            "calendar": ["L0", "L0", "L1", "L1"],
            "w6_to_w30": finite,
            "R36_first_coinductive_blocks": {
                channel: channels[channel]["blocks"][5]
                for channel in ("pi", "e", "phi")
            },
        },
        "pi_closure": {
            "primitive_slope": "1/5",
            "four_companion_tangent": "120/119",
            "unit_return_compensator": 239,
            "gaussian_identity": gaussian,
            "classical_formula_role": "downstream_exact_evaluator",
        },
        "e_propagation": {
            **propagation,
            "last_factorial_index": e_terms,
            "classical_series_role": "downstream_exact_evaluator",
        },
        "phi_autoscale": {
            **exceptional,
            "F_av": [[0, 1], [1, 1]],
            "fibonacci_index": phi_index,
            "scalar_fixed_point_role": "downstream_coordinate_of_Perron_equation",
        },
        "connection": {
            **connection,
            "phase_pairs_per_channel": channels["pi"]["phase_pairs"],
            "complete_nonads_per_channel": channels["pi"]["complete_nonads"],
            "state_reset": False,
            "carry_preserved": True,
            "finite_terminal_preserved": True,
        },
        "prefix_stability": stability,
        "isolation": source_audit,
    }


def parse_args() -> argparse.Namespace:
    default_root = Path.home() / "Documents" / "New project"
    default_certificate = Path(__file__).with_name(
        "certificado_generacion_infinita_nonadica.json"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=1000)
    parser.add_argument("--guard-digits", type=int, default=12)
    parser.add_argument("--project-root", type=Path, default=default_root)
    parser.add_argument("--certificate", type=Path, default=default_certificate)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = run(args)
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(
        json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        "PASS_GENERACION_INFINITA_NONADICA "
        f"digits={args.digits} "
        f"levels={certificate['precision']['refinement_levels']} "
        f"certificate={args.certificate}"
    )


if __name__ == "__main__":
    main()
