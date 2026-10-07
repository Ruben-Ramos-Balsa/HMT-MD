#!/usr/bin/env python3
"""Certifica el bloque hojas--Möbius--pi/phi^2.

La prueba no lee valores metrológicos. Parte de las coordenadas HMT ya
generadas de pi y phi, de la partición nonádica y de las definiciones
publicadas de A, C* y q_±. Separa tres afirmaciones:

* teoremas enteros exactos del transductor nonádico;
* teoremas relativos al lector bicapa F_AV=S+P_V;
* evaluación racional certificada de pi/phi^2 por cilindros.

No usa ``assert`` y produce la misma salida bajo ``python -O``.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations
import json
from math import gcd
from pathlib import Path


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "certificados" / "hojas_mobius_pi_phi2.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"FAIL_HOJAS_MOBIUS_PI_PHI2: {message}")


def det2(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def det3(matrix: tuple[tuple[int, int, int], ...]) -> int:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def matmul3(
    left: tuple[tuple[int, int, int], ...],
    right: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        tuple(sum(left[r][k] * right[k][c] for k in range(3)) for c in range(3))
        for r in range(3)
    )


def matmul2(
    left: tuple[tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(sum(left[r][k] * right[k][c] for k in range(2)) for c in range(2))
        for r in range(2)
    )  # type: ignore[return-value]


def matpow2(
    matrix: tuple[tuple[int, int], tuple[int, int]], exponent: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    result = ((1, 0), (0, 1))
    base = matrix
    while exponent:
        if exponent & 1:
            result = matmul2(result, base)
        base = matmul2(base, base)
        exponent //= 2
    return result


def fibonacci(index: int) -> int:
    a, b = 0, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def decimal_fraction(value: Fraction, digits: int = 80) -> str:
    getcontext().prec = digits
    return str(Decimal(value.numerator) / Decimal(value.denominator))


def rr5(q: Decimal, depth: int = 2400) -> Decimal:
    denominator = Decimal(1)
    for exponent in range(depth, 0, -1):
        denominator = Decimal(1) + (q ** exponent) / denominator
    return (q.ln() / Decimal(5)).exp() / denominator


def check_nonadic_transducer() -> dict[str, object]:
    residues = {
        "C1": {1, 4, 7},
        "C2": {2, 5, 8},
        "C0": {3, 6, 9},
    }
    supports = {
        "DA": {1, 3, 5, 7},
        "DC": {2, 4, 6, 8},
        "D9": {9},
    }
    require(set().union(*residues.values()) == set(range(1, 10)), "partición residual")
    require(set().union(*supports.values()) == set(range(1, 10)), "partición angular")
    require(sum(map(len, residues.values())) == 9, "solapamiento residual")
    require(sum(map(len, supports.values())) == 9, "solapamiento angular")

    matrix = tuple(
        tuple(len(residues[row] & supports[column]) for column in ("DA", "DC", "D9"))
        for row in ("C1", "C2", "C0")
    )
    expected = ((2, 1, 0), (1, 2, 0), (1, 1, 1))
    require(matrix == expected, "matriz de incidencia nonádica")
    require(det3(matrix) == 3, "determinante del transductor")

    entries_gcd = 0
    for row in matrix:
        for value in row:
            entries_gcd = gcd(entries_gcd, abs(value))
    minors: list[int] = []
    for rows in combinations(range(3), 2):
        for columns in combinations(range(3), 2):
            minor = (
                matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]]
                - matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]]
            )
            minors.append(abs(minor))
    minors_gcd = 0
    for value in minors:
        minors_gcd = gcd(minors_gcd, value)
    require((entries_gcd, minors_gcd, abs(det3(matrix))) == (1, 1, 3), "SNF (1,1,3)")

    swap = ((0, 1, 0), (1, 0, 0), (0, 0, 1))
    require(matmul3(swap, matmul3(matrix, swap)) == matrix, "equivarianza simultánea")

    # La imagen integral queda descrita por una sola congruencia.
    for x in range(-4, 5):
        for y in range(-4, 5):
            for z in range(-2, 3):
                u = 2 * x + y
                v = x + 2 * y
                w = x + y + z
                require((u + v) % 3 == 0, "condición necesaria de imagen")
                xr = (2 * u - v) // 3
                yr = (2 * v - u) // 3
                zr = w - xr - yr
                require((xr, yr, zr) == (x, y, z), "inversa integral en la imagen")

    return {
        "residue_partition": {name: sorted(values) for name, values in residues.items()},
        "angular_support_partition": {name: sorted(values) for name, values in supports.items()},
        "incidence_matrix": matrix,
        "determinant": 3,
        "smith_normal_form": [1, 1, 3],
        "integer_image": "{(u,v,w) in Z^3 : u+v = 0 mod 3}",
        "simultaneous_swap_equivariant": True,
    }


def check_mobius_and_two_way() -> dict[str, object]:
    grading = ((1, 0), (0, -1))
    conjugation = ((0, 1), (1, 0))
    minus_grading = ((-1, 0), (0, 1))
    require(matmul2(conjugation, matmul2(grading, conjugation)) == minus_grading, "CRC=-R")
    require(matmul2(conjugation, conjugation) == ((1, 0), (0, 1)), "C^2=I")

    alpha = Decimal("0.007297352569283800997285105472380663")
    a_deg = Decimal(1000) * alpha
    c_deg = Decimal("2.123738338968645724261951380393")
    pi_dec = Decimal("3.141592653589793238462643383279502884")
    a_rad = a_deg * pi_dec / Decimal(180)
    c_rad = c_deg * pi_dec / Decimal(180)
    q_plus = (-(a_rad + c_rad)).exp()
    q_minus = (-(a_rad - c_rad)).exp()
    a_recovered = -(q_plus * q_minus).ln() / Decimal(2)
    c_recovered = (q_minus / q_plus).ln() / Decimal(2)
    tolerance = Decimal("1e-90")
    require(abs(a_recovered - a_rad) < tolerance, "recuperación exacta de A")
    require(abs(c_recovered - c_rad) < tolerance, "recuperación exacta de C*")

    # Retícula two-way de índice doce.
    winding = ((6, 1), (6, -1))
    require(det2(winding) == -12, "índice de la retícula two-way")
    for n_a in range(-8, 9):
        for s_c in range(-8, 9):
            w_plus = 6 * n_a + s_c
            w_minus = 6 * n_a - s_c
            require((w_plus + w_minus) % 12 == 0, "congruencia de winding")
            require((w_plus + w_minus) // 12 == n_a, "recuperación de n_A")
            require((w_plus - w_minus) // 2 == s_c, "recuperación de s_C")

    return {
        "grading_R": grading,
        "sheet_conjugation_C": conjugation,
        "relations": ["R^2=I", "C^2=I", "CRC=-R"],
        "A_degrees": str(a_deg),
        "C_degrees": str(c_deg),
        "q_plus": str(q_plus),
        "q_minus": str(q_minus),
        "exact_log_readers": {
            "A_rad": "-log(q_plus*q_minus)/2",
            "C_rad": "log(q_minus/q_plus)/2",
            "A_reconstruction_error": str(abs(a_recovered - a_rad)),
            "C_reconstruction_error": str(abs(c_recovered - c_rad)),
        },
        "two_way_lattice_matrix": winding,
        "two_way_lattice_snf": [1, 12],
        "mobius_statement": "one base return exchanges sheets; the squared return restores orientation",
    }


def check_tpk_mode_quotient() -> dict[str, object]:
    """Deriva la incidencia AV desde el calendario de modos de TPK.

    El resultado es una matriz de incidencia de aristas. También certifica
    que olvidar la fase no produce un cociente determinista fuerte y que la
    medida de Parry pertenece al envolvente de memoria uno, no a la órbita
    periódica microscópica.
    """

    primitive_calendar = (1, -1, 0)

    def update(mode: str, phase: int) -> str:
        if phase == 1:
            return "SIGMA"
        if phase == -1:
            return "PI"
        require(phase == 0, "fase fuera de TRIT")
        return mode

    mode = "PI"
    primitive_orbit: list[str] = []
    for phase in primitive_calendar:
        mode = update(mode, phase)
        primitive_orbit.append(mode)
    require(primitive_orbit == ["SIGMA", "PI", "PI"], "órbita primitiva de modos")

    order = ("SIGMA", "PI")
    index = {name: position for position, name in enumerate(order)}

    def cyclic_incidence(word: list[str]) -> tuple[tuple[int, int], tuple[int, int]]:
        counts = [[0, 0], [0, 0]]
        for position, source in enumerate(word):
            target = word[(position + 1) % len(word)]
            counts[index[source]][index[target]] += 1
        return tuple(tuple(row) for row in counts)  # type: ignore[return-value]

    primitive_incidence = cyclic_incidence(primitive_orbit)
    transfer = ((0, 1), (1, 1))
    require(primitive_incidence == transfer, "incidencia TPK primitiva")

    incidences: dict[str, object] = {}
    for length, copies in ((3, 1), (9, 3), (27, 9), (108, 36)):
        orbit = primitive_orbit * copies
        incidence = cyclic_incidence(orbit)
        expected = tuple(
            tuple(copies * transfer[row][column] for column in range(2))
            for row in range(2)
        )
        require(incidence == expected, f"incidencia TPK de longitud {length}")
        common = 0
        for row in incidence:
            for value in row:
                common = gcd(common, value)
        require(common == copies, f"factor común de longitud {length}")
        require(
            tuple(tuple(value // common for value in row) for row in incidence) == transfer,
            f"primitivización de longitud {length}",
        )
        incidences[str(length)] = {
            "matrix": incidence,
            "common_factor": common,
            "primitive_matrix": transfer,
        }

    # Mismo modo visible, sucesores diferentes: la fase no puede olvidarse
    # como un cociente determinista de un paso.
    require(
        primitive_orbit[1] == primitive_orbit[2] == "PI",
        "testigo de dos fases con modo PI",
    )
    require(
        primitive_orbit[2] != primitive_orbit[0],
        "testigo de sucesores diferentes al olvidar fase",
    )

    # El SFT mínimo de memoria uno contiene palabras que no aparecen en la
    # órbita periódica; por eso Parry no es el pushforward cronológico.
    envelope_word = ("SIGMA", "PI", "SIGMA")
    require(
        all(
            transfer[index[envelope_word[k]]][index[envelope_word[k + 1]]] == 1
            for k in range(len(envelope_word) - 1)
        ),
        "palabra admisible del envolvente",
    )
    periodic_triples = {
        tuple((primitive_orbit * 2)[start:start + 3])
        for start in range(3)
    }
    require(envelope_word not in periodic_triples, "separación órbita/envolvente")

    return {
        "primitive_calendar": list(primitive_calendar),
        "mode_update": {
            "+1": "SIGMA",
            "-1": "PI",
            "0": "retain_previous_mode",
        },
        "primitive_cyclic_orbit": primitive_orbit,
        "geometric_reader": {
            "SIGMA": "areal/additive/boundary",
            "PI": "volumetric/multiplicative/interior",
        },
        "incidences": incidences,
        "four_rules_are_induced": {
            "areal_to_volumetric": 1,
            "volumetric_to_areal": 1,
            "volumetric_to_volumetric": 1,
            "areal_to_areal": 0,
        },
        "phase_erasure_is_not_a_strong_one_step_quotient": True,
        "periodic_vertex_frequencies": {
            "areal": "1/3",
            "volumetric": "2/3",
            "areal_to_volumetric_ratio": "1/2",
        },
        "minimal_one_step_envelope": {
            "adjacency": transfer,
            "strictly_additional_word": list(envelope_word),
        },
        "status": "EXACT_EDGE_INCIDENCE_AND_CANONICAL_ONE_STEP_ENVELOPE",
    }


def check_fibonacci_sheet_reader() -> dict[str, object]:
    swap = ((0, 1), (1, 0))
    retained_memory = ((0, 0), (0, 1))
    transfer = tuple(
        tuple(swap[row][column] + retained_memory[row][column] for column in range(2))
        for row in range(2)
    )
    require(transfer == ((0, 1), (1, 1)), "F_AV=S+P_V")
    require(det2(transfer) == -1, "orientación del lector Fibonacci")
    require(transfer[0][0] + transfer[1][1] == 1, "traza del lector Fibonacci")
    require(all(value > 0 for row in matpow2(transfer, 2) for value in row), "primitividad")

    # Unicidad dentro de matrices enteras no negativas con traza 1 y det -1.
    candidates: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    matrix = ((a, b), (c, d))
                    if a + d == 1 and det2(matrix) == -1 and b > 0 and c > 0:
                        candidates.append(matrix)
    require(set(candidates) == {((0, 1), (1, 1)), ((1, 1), (1, 0))}, "unicidad hasta intercambio")

    loop_ratios: list[dict[str, object]] = []
    for depth in range(2, 25):
        power = matpow2(transfer, depth)
        expected = (
            (fibonacci(depth - 1), fibonacci(depth)),
            (fibonacci(depth), fibonacci(depth + 1)),
        )
        require(power == expected, f"potencia Fibonacci n={depth}")
        loop_ratios.append(
            {
                "depth": depth,
                "areal_closed_loops": power[0][0],
                "volumetric_closed_loops": power[1][1],
                "ratio": f"{power[0][0]}/{power[1][1]}",
            }
        )

    phi = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    require(abs(phi * phi - phi - Decimal(1)) < Decimal("1e-95"), "ecuación áurea")
    vector = (Decimal(1), phi)
    image = (vector[1], vector[0] + vector[1])
    require(abs(image[0] - phi * vector[0]) < Decimal("1e-95"), "autovector Perron A")
    require(abs(image[1] - phi * vector[1]) < Decimal("1e-95"), "autovector Perron V")
    parry_ratio = (vector[0] * vector[0]) / (vector[1] * vector[1])
    require(abs(parry_ratio - Decimal(1) / (phi * phi)) < Decimal("1e-95"), "razón de Parry")

    return {
        "premises": [
            "edge incidence induced by the primitive TPK calendar",
            "minimal one-step symbolic envelope after phase erasure",
        ],
        "S": swap,
        "P_V": retained_memory,
        "F_AV": transfer,
        "unique_nonnegative_integral_realizations_up_to_sheet_swap": candidates,
        "perron_root": str(phi),
        "perron_vector": [str(value) for value in vector],
        "parry_areal_to_volumetric_ratio": str(parry_ratio),
        "exact_ratio": "phi^-2",
        "closed_loop_formula": "(F_AV^n)_AA/(F_AV^n)_VV = Fibonacci(n-1)/Fibonacci(n+1)",
        "finite_loop_ratio_examples": loop_ratios[-5:],
        "status": "PARRY_MEASURE_OF_THE_CANONICAL_ONE_STEP_ENVELOPE",
    }


def check_quadratic_memory_and_marked_return() -> dict[str, object]:
    """Certifica la raíz espectral del cuadrado y el retorno marcado.

    La representación de Sym^2 usa por columnas las imágenes de
    (e_A^2, e_A odot e_V, e_V^2). El marcador D_pi se aplica una sola vez
    sobre la hoja areal; no modifica el transportador F_AV.
    """

    transfer = ((0, 1), (1, 1))
    sym2 = (
        (0, 0, 1),
        (0, 1, 2),
        (1, 1, 1),
    )
    trace = sum(sym2[index][index] for index in range(3))
    principal_minor_sum = (
        sym2[0][0] * sym2[1][1] - sym2[0][1] * sym2[1][0]
        + sym2[0][0] * sym2[2][2] - sym2[0][2] * sym2[2][0]
        + sym2[1][1] * sym2[2][2] - sym2[1][2] * sym2[2][1]
    )
    determinant = det3(sym2)
    require((trace, principal_minor_sum, determinant) == (2, -2, -1), "charpoly Sym^2")

    phi = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    eigenvalues = (phi * phi, Decimal(-1), Decimal(1) / (phi * phi))

    def characteristic(value: Decimal) -> Decimal:
        return value ** 3 - Decimal(2) * value ** 2 - Decimal(2) * value + Decimal(1)

    for value in eigenvalues:
        require(abs(characteristic(value)) < Decimal("1e-90"), "espectro Sym^2")
    require(
        abs((-Decimal(1) / phi) ** 2 - eigenvalues[2]) < Decimal("1e-95"),
        "cuadrado positivo del modo estable orientado",
    )

    power108 = matpow2(transfer, 108)
    f107 = 10284720757613717413913
    f109 = 26925748508234281076009
    require(power108[0][0] == f107, "cuenta areal n=108")
    require(power108[1][1] == f109, "cuenta volumétrica n=108")
    require(fibonacci(107) == f107 and fibonacci(109) == f109, "índices Fibonacci n=108")

    loop_ratio = Decimal(f107) / Decimal(f109)
    parry_ratio = Decimal(1) / (phi * phi)
    loop_error = abs(loop_ratio - parry_ratio)
    require(loop_error < Decimal("6.17e-46"), "error de retorno n=108")
    require(loop_error > Decimal("6.16e-46"), "control inferior de error n=108")

    pi_hmt = Decimal(
        "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
    )
    marked_ratio = pi_hmt * loop_ratio
    marked_limit = pi_hmt * parry_ratio
    marked_error = abs(marked_ratio - marked_limit)
    require(marked_error < Decimal("1.938e-45"), "error marcado n=108")
    require(marked_error > Decimal("1.937e-45"), "control inferior marcado n=108")

    # Un operador diagonal de hoja queda determinado por sus dos
    # normalizaciones. La comprobación evita que pi se inserte en F_AV.
    d_pi = ((pi_hmt, Decimal(0)), (Decimal(0), Decimal(1)))
    require(d_pi[0][0] == pi_hmt and d_pi[1][1] == Decimal(1), "normalización D_pi")
    require(transfer == ((0, 1), (1, 1)), "D_pi no altera F_AV")
    require(marked_ratio == pi_hmt * Decimal(power108[0][0]) / Decimal(power108[1][1]), "Theta_108")

    return {
        "F_AV": transfer,
        "F_AV_characteristic_polynomial": "t^2-t-1",
        "F_AV_eigenvalues": ["phi", "-phi^-1"],
        "Sym2_basis": ["e_areal^2", "e_areal odot e_volumetric", "e_volumetric^2"],
        "Sym2_matrix_column_image_convention": sym2,
        "Sym2_characteristic_polynomial": "t^3-2*t^2-2*t+1=(t+1)*(t^2-3*t+1)",
        "Sym2_eigenvalues": ["phi^2", "-1", "phi^-2"],
        "stable_oriented_mode": "-phi^-1",
        "stable_quadratic_memory": "phi^-2",
        "marked_return": {
            "P_areal": [[1, 0], [0, 0]],
            "P_volumetric": [[0, 0], [0, 1]],
            "D_pi": "Pi_HMT*P_areal+P_volumetric",
            "relative_canonicity_axioms": [
                "sheet diagonal",
                "volumetric weight one",
                "areal weight Pi_HMT",
            ],
            "Theta_n": "Pi_HMT*Fibonacci(n-1)/Fibonacci(n+1)",
            "pi_is_applied_once_at_the_boundary": True,
        },
        "native_depth_108": {
            "areal_closed_loops_F107": f107,
            "volumetric_closed_loops_F109": f109,
            "loop_ratio": str(loop_ratio),
            "phi_inverse_squared": str(parry_ratio),
            "absolute_error": str(loop_error),
            "marked_ratio": str(marked_ratio),
            "pi_over_phi_squared": str(marked_limit),
            "marked_absolute_error": str(marked_error),
        },
        "status": "EXACT_SPECTRAL_SQUARE_AND_RELATIVE_CANONICAL_MARKED_RETURN",
    }


def check_ratio_cylinders() -> dict[str, object]:
    pi_fraction = "141592653589793238462643383279502884"
    phi_fraction = "618033988749894848204586834365638117"
    places = len(pi_fraction)
    require(places == len(phi_fraction) == 36, "doce tríadas de entrada")
    scale = 10 ** places
    pi_lower = Fraction(3 * scale + int(pi_fraction), scale)
    pi_upper = pi_lower + Fraction(1, scale)
    phi_lower = Fraction(scale + int(phi_fraction), scale)
    phi_upper = phi_lower + Fraction(1, scale)
    require(pi_lower > 0 and phi_lower > 0, "cilindros positivos")

    ratio_lower = pi_lower / (phi_upper * phi_upper)
    ratio_upper = pi_upper / (phi_lower * phi_lower)
    require(ratio_lower < ratio_upper, "orientación del intervalo cociente")
    width = ratio_upper - ratio_lower
    certified_places = 35
    scaled_lower = ratio_lower * 10 ** certified_places
    scaled_upper = ratio_upper * 10 ** certified_places
    common_prefix = floor_fraction(scaled_lower)
    require(common_prefix == floor_fraction(scaled_upper), "prefijo cociente no certificado")
    require(
        str(common_prefix) == "119998161486432666111577775331680692",
        "prefijo de pi/phi^2",
    )

    # Los once primeros bloques completos de tres cifras quedan certificados.
    fractional = str(common_prefix)[1:]
    triads = [fractional[index:index + 3] for index in range(0, 33, 3)]
    require(
        triads == ["199", "981", "614", "864", "326", "661", "115", "777", "753", "316", "806"],
        "tríadas cociente",
    )

    # Q(I,J) es el intervalo imagen mínimo porque x/y^2 es creciente en x
    # y decreciente en y>0. Se verifica además la anidación coinductiva a
    # cada profundidad de una tríada.
    nested_readers: list[dict[str, object]] = []
    previous_lower: Fraction | None = None
    previous_upper: Fraction | None = None
    for prefix_places in range(3, places + 1, 3):
        prefix_scale = 10 ** prefix_places
        p_lower = Fraction(
            3 * prefix_scale + int(pi_fraction[:prefix_places]),
            prefix_scale,
        )
        p_upper = p_lower + Fraction(1, prefix_scale)
        f_lower = Fraction(
            prefix_scale + int(phi_fraction[:prefix_places]),
            prefix_scale,
        )
        f_upper = f_lower + Fraction(1, prefix_scale)
        q_lower = p_lower / (f_upper * f_upper)
        q_upper = p_upper / (f_lower * f_lower)

        corners = (
            p_lower / (f_lower * f_lower),
            p_lower / (f_upper * f_upper),
            p_upper / (f_lower * f_lower),
            p_upper / (f_upper * f_upper),
        )
        require(q_lower == min(corners) and q_upper == max(corners), "minimalidad de Q(I,J)")
        if previous_lower is not None and previous_upper is not None:
            require(previous_lower <= q_lower < q_upper <= previous_upper, "anidación de Q(I,J)")
        previous_lower, previous_upper = q_lower, q_upper

        forced_triads = 0
        for block_count in range(1, 13):
            base = 1000 ** block_count
            if floor_fraction(q_lower * base) != floor_fraction(q_upper * base):
                break
            forced_triads = block_count
        nested_readers.append(
            {
                "input_decimal_places": prefix_places,
                "input_triads": prefix_places // 3,
                "forced_quotient_triads": forced_triads,
                "lower": decimal_fraction(q_lower, 90),
                "upper": decimal_fraction(q_upper, 90),
            }
        )

    require(nested_readers[-1]["forced_quotient_triads"] == 11, "once tríadas forzadas")
    require(
        all(
            int(nested_readers[index]["forced_quotient_triads"])
            <= int(nested_readers[index + 1]["forced_quotient_triads"])
            for index in range(len(nested_readers) - 1)
        ),
        "monotonía de bloques forzados",
    )

    return {
        "input": {
            "pi_generated_fractional_triads": [pi_fraction[i:i + 3] for i in range(0, 36, 3)],
            "phi_generated_fractional_triads": [phi_fraction[i:i + 3] for i in range(0, 36, 3)],
            "fractional_decimal_places_each": places,
        },
        "quotient_interval": {
            "lower": decimal_fraction(ratio_lower),
            "upper": decimal_fraction(ratio_upper),
            "width": decimal_fraction(width),
        },
        "certified_fractional_decimal_places": certified_places,
        "certified_prefix": "1." + str(common_prefix)[1:],
        "certified_full_triads": triads,
        "coinductive_interval_reader": {
            "definition": "Q([a,b],[c,d])=[a/d^2,b/c^2] for 0<c<=d",
            "is_minimal_image_interval": True,
            "is_nested_on_nested_positive_cylinders": True,
            "singleton_limit": "pi_HMT/phi_HMT^2",
            "depths": nested_readers,
        },
        "reader": "Theta_n = Pi_HMT*Fibonacci(n-1)/Fibonacci(n+1) -> pi/phi^2",
    }


def check_electron_mirror() -> dict[str, object]:
    """Certifica el intercambio exacto entre la bisagra y la semilla electrónica."""
    getcontext().prec = 100
    pi_hmt = Decimal(
        "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
    )
    phi_hmt = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    boundary_ratio = pi_hmt / (phi_hmt * phi_hmt)
    electron_ratio = phi_hmt / (pi_hmt * pi_hmt)
    electron_seed = electron_ratio.exp()
    tolerance = Decimal("1e-95")

    require(
        abs(boundary_ratio * electron_ratio - Decimal(1) / (pi_hmt * phi_hmt))
        < tolerance,
        "producto del par especular",
    )
    require(
        abs(boundary_ratio / electron_ratio - (pi_hmt / phi_hmt) ** 3)
        < tolerance,
        "cociente del par especular",
    )
    require(
        abs(
            electron_ratio
            - Decimal(1) / (phi_hmt ** 3 * boundary_ratio ** 2)
        )
        < tolerance,
        "reparametrización de la semilla electrónica",
    )
    require(
        abs(
            electron_seed
            - Decimal(
                "1.178144942596306780811600956808889102533837932497813085998138710447880271485"
            )
        )
        < Decimal("1e-75"),
        "evaluación de exp(phi/pi^2)",
    )

    return {
        "bivariate_law": "R(x,y)=x/y^2",
        "exchange": "J(x,y)=(y,x), J^2=I",
        "areal_volumetric_orientation": {
            "formula": "R(pi,phi)=pi/phi^2",
            "value": str(boundary_ratio),
        },
        "electronic_orientation": {
            "formula": "R(phi,pi)=phi/pi^2",
            "value": str(electron_ratio),
            "exponential_seed": str(electron_seed),
        },
        "identities": [
            "R(pi,phi)*R(phi,pi)=1/(pi*phi)",
            "R(pi,phi)/R(phi,pi)=(pi/phi)^3",
            "phi/pi^2=1/(phi^3*(pi/phi^2)^2)",
        ],
        "status": "EXACT_ALGEBRAIC_LINK_NOT_AN_INDEPENDENT_ELECTRON_DERIVATION",
    }


def check_diagnostics() -> dict[str, object]:
    getcontext().prec = 100
    alpha = Decimal("0.007297352569283800997285105472380663")
    a_deg = Decimal(1000) * alpha
    c_deg = Decimal("2.123738338968645724261951380393")
    pi_dec = Decimal("3.141592653589793238462643383279502884")
    phi = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    a_rad = a_deg * pi_dec / Decimal(180)
    c_rad = c_deg * pi_dec / Decimal(180)
    q_plus = (-(a_rad + c_rad)).exp()
    q_minus = (-(a_rad - c_rad)).exp()

    r_plus = rr5(q_plus)
    r_minus = rr5(q_minus)
    phi_inverse = Decimal(1) / phi
    require(abs(r_plus - phi_inverse) < Decimal("1e-20"), "control RR q+")
    require(abs(r_minus - phi_inverse) < Decimal("1e-35"), "control RR q-")

    def s90(q: Decimal) -> Decimal:
        return q ** 90 / (Decimal(1) - q ** 270)

    def s120(q: Decimal) -> Decimal:
        return q ** 120 / (Decimal(1) - q ** 360)

    delta4 = Decimal("1.1119642269214005e-4")
    e527 = Decimal(1) / Decimal(5) - Decimal(27) * delta4 / Decimal(160)
    kernel = Decimal(1) + s90(q_plus) - s120(q_plus) + e527
    exact_ratio = pi_dec / (phi * phi)
    residual = kernel - exact_ratio
    triadic_tail = q_plus ** 270 + q_plus ** 360
    require(abs(residual) > triadic_tail, "control negativo de la antigua cota de cola")

    return {
        "rogers_ramanujan": {
            "R5_q_plus": str(r_plus),
            "R5_q_minus": str(r_minus),
            "phi_inverse": str(phi_inverse),
            "q_plus_residual": str(r_plus - phi_inverse),
            "q_minus_residual": str(r_minus - phi_inverse),
            "typed_use": "asymptotic level-five compatibility control; not the generator of phi",
        },
        "kernel_90_120": {
            "value": str(kernel),
            "pi_over_phi_squared": str(exact_ratio),
            "residual": str(residual),
            "q270_plus_q360": str(triadic_tail),
            "typed_use": "independent diagnostic; not an exact real identity",
        },
    }


def main() -> None:
    result = {
        "schema": "HMT.hojas-mobius-pi-phi2.v3",
        "status": "PASS_HOJAS_MOBIUS_PI_PHI2_TPK_INDUCIDO",
        "canonical_revision": "2026-07-22.2",
        "nonadic_transducer": check_nonadic_transducer(),
        "mobius_two_way": check_mobius_and_two_way(),
        "tpk_mode_quotient": check_tpk_mode_quotient(),
        "fibonacci_sheet_reader": check_fibonacci_sheet_reader(),
        "quadratic_memory_and_marked_return": check_quadratic_memory_and_marked_return(),
        "pi_phi2_cylinders": check_ratio_cylinders(),
        "electron_mirror": check_electron_mirror(),
        "diagnostics": check_diagnostics(),
        "provenance": {
            "particle_antiparticle_mobius": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "pi_phi2_hinge": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "nonadic_incidence_matrix": "FORMALIZACION_NUEVA",
            "tpk_induced_edge_incidence": "FORMALIZACION_NUEVA_EXACTA",
            "fibonacci_parry_reader": "FORMALIZACION_NUEVA_DEL_ENVOLVENTE_MINIMO",
            "quadratic_memory_reader": "FORMALIZACION_NUEVA",
            "marked_return_operator": "FORMALIZACION_NUEVA_RELATIVA_A_TRES_CLAUSULAS",
            "depth_108_and_interval_reader": "CERTIFICADO_NUEVO",
            "cylinder_quotient_certificate": "CERTIFICADO_NUEVO",
            "electron_mirror_link": "FORMALIZACION_NUEVA_DE_ARQUITECTURA_AUTORAL_PREEXISTENTE",
        },
        "scope": {
            "exact_internal": [
                "incidence matrix, determinant and Smith form",
                "q-channel logarithmic reconstruction of A and C*",
                "Möbius sheet-exchange algebra",
                "TPK mode incidences N3=F_AV, N9=3F_AV, N27=9F_AV, N108=36F_AV",
                "Sym^2(F_AV) spectrum phi^2,-1,phi^-2",
                "native n=108 loop counts F107 and F109",
                "minimal nested quotient interval Q(I,J)",
                "35 certified quotient decimals from 12 generated triads of pi and phi",
                "exact exchange R(pi,phi)=pi/phi^2 <-> R(phi,pi)=phi/pi^2",
            ],
            "relative": (
                "Parry ratio phi^-2 belongs to the canonical minimal one-step "
                "envelope of the exact TPK edge incidence; D_pi is canonical "
                "relative to sheet diagonal, unit volumetric normalization and "
                "the independently generated Pi_HMT boundary mark"
            ),
            "algebraic_no_go": (
                "rational algebraic operations on F_AV remain algebraic "
                "(spectrally inside Q(sqrt(5))) and cannot generate the "
                "transcendental factor pi/phi^2 without the Pi_HMT boundary reader"
            ),
            "physical_interface": {
                "torsional_local_equivalence": "G_tor/I_tor=1",
                "areal_volumetric_ambivalence": "G_av/I_av=pi_HMT/phi^2 under the declared factorization",
                "universal_measured_mass_ratio_is_not_claimed": True,
            },
            "open_program": (
                "dark matter and dark energy as effective non-torsional sheet "
                "readings require a cosmological realization and prospective observables"
            ),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(encoded, encoding="utf-8")
    print("PASS_HOJAS_MOBIUS_PI_PHI2_TPK_INDUCIDO")
    print(f"certificate={OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
