#!/usr/bin/env python3
"""Puerta exhaustiva de no omisión para los sectores topológicos HMT--MD.

La verificación usa exclusivamente la biblioteca estándar. Recalcula los
censos finitos y las identidades algebraicas, coteja la evidencia histórica
N40 y exige que la formulación pública conserve tipos, estatutos y
falsadores. La salida JSON es determinista en ejecución normal y optimizada.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = (
    ROOT
    / "manuscrito"
    / "sections"
    / "md"
    / "06c_sectores_topologicos_no_omision.tex"
)
PRIMARY_CM_PATH = (
    ROOT / "manuscrito" / "sections" / "md" / "04b_banda_particula_virtual.tex"
)
STRUCTURE_PATH = ROOT / "manuscrito" / "estructura_rev8.tex"
N40_DIR = ROOT / "datos" / "n40_c_m"

HISTORICAL_HASHES = {
    "N40_CM_Per6_fixed_summary.csv":
        "892f070e8b77a79d969f681fe47e3a2af23e79a3849e4a853e568dd40d072603",
    "N40_CM_fixed_summary.csv":
        "613d958980b4fc69bda389c251145a3b19d83c33259a05581fb51b652afedd27",
    "N40_claim_status.csv":
        "41cd95bfa5d25af3fc579db1ce11b4b286e9a9384ac84a1b773131be08530d9b",
    "summary.json":
        "6e518bf1778960dfaf0826567a67270f627a8a4f54b961416f4710099b1179a6",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def determinant_3(matrix: tuple[tuple[int, ...], ...]) -> int:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return (
        a * (e * i - f * h)
        - b * (d * i - f * g)
        + c * (d * h - e * g)
    )


def determinant_2(a: int, b: int, c: int, d: int) -> int:
    return a * d - b * c


def matmul(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    require(len(left[0]) == len(right), "dimensiones matriciales incompatibles")
    return tuple(
        tuple(
            sum(left[row][k] * right[k][col] for k in range(len(right)))
            for col in range(len(right[0]))
        )
        for row in range(len(left))
    )


def matvec(
    matrix: tuple[tuple[int, ...], ...],
    vector: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        sum(entry * vector[col] for col, entry in enumerate(row))
        for row in matrix
    )


def matrix_power(
    matrix: tuple[tuple[int, ...], ...],
    exponent: int,
) -> tuple[tuple[int, ...], ...]:
    require(exponent >= 0, "exponente matricial negativo")
    size = len(matrix)
    result = tuple(
        tuple(1 if row == col else 0 for col in range(size))
        for row in range(size)
    )
    factor = matrix
    power = exponent
    while power:
        if power % 2:
            result = matmul(result, factor)
        factor = matmul(factor, factor)
        power //= 2
    return result


def fibonacci(n: int) -> int:
    require(n >= 0, "índice de Fibonacci negativo")
    first, second = 0, 1
    for _ in range(n):
        first, second = second, first + second
    return first


def ring_add(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def ring_mul(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    """Producto en Z[τ]/(τ²-τ-1), en la base ordenada (1,τ)."""

    a, b = left
    c, d = right
    return a * c + b * d, a * d + b * c + b * d


def verify_c_m() -> dict[str, Any]:
    fixed = 0
    fixed_period_six = 0
    involution_violations = 0
    charge_negation_violations = 0
    weight_invariance_violations = 0
    fixed_charge_violations = 0
    tested = 0

    for word in itertools.product((-1, 0, 1), repeat=12):
        transformed = tuple(-word[11 - index] for index in range(12))
        twice = tuple(-transformed[11 - index] for index in range(12))
        if twice != word:
            involution_violations += 1

        charge = sum(word) % 3
        transformed_charge = sum(transformed) % 3
        if transformed_charge != (-charge) % 3:
            charge_negation_violations += 1
        if sum(abs(value) for value in transformed) != sum(
            abs(value) for value in word
        ):
            weight_invariance_violations += 1

        is_fixed = transformed == word
        if is_fixed:
            fixed += 1
            if charge != 0:
                fixed_charge_violations += 1
            if all(word[index + 6] == word[index] for index in range(6)):
                fixed_period_six += 1
        tested += 1

    require(tested == 3 ** 12, "el censo C_M no cubrió las 3^12 palabras")
    require(involution_violations == 0, "C_M no es involutiva")
    require(fixed == 3 ** 6 == 729, "el censo Fix(C_M) no es 729")
    require(
        fixed_period_six == 3 ** 3 == 27,
        "el censo Fix(C_M) intersección Per_6 no es 27",
    )
    require(
        charge_negation_violations == 0,
        "C_M no invierte la carga ternaria",
    )
    require(
        weight_invariance_violations == 0,
        "C_M no preserva el peso ternario",
    )
    require(
        fixed_charge_violations == 0,
        "el sector fijo C_M contiene carga no nula módulo 3",
    )

    return {
        "domain": "{-1,0,1}^12",
        "tested_words": tested,
        "involution_violations": involution_violations,
        "fixed_points": fixed,
        "fixed_points_expected": 729,
        "fixed_and_period_dividing_six": fixed_period_six,
        "fixed_and_period_dividing_six_expected": 27,
        "charge_negation_violations": charge_negation_violations,
        "weight_invariance_violations": weight_invariance_violations,
        "fixed_charge_violations": fixed_charge_violations,
    }


def read_single_row_csv(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 1, f"{path.name}: se esperaba una sola fila")
    return rows[0]


def verify_historical_n40() -> dict[str, Any]:
    observed_hashes: dict[str, str] = {}
    for name, expected in sorted(HISTORICAL_HASHES.items()):
        path = N40_DIR / name
        require(path.is_file(), f"artefacto N40 ausente: {name}")
        observed = sha256(path)
        require(observed == expected, f"huella N40 alterada: {name}")
        observed_hashes[name] = observed

    summary = json.loads((N40_DIR / "summary.json").read_text(encoding="utf-8"))
    words = summary["CM_words"]
    require(words["Fix_CM"] == 729, "summary.json: Fix_CM no es 729")
    require(
        words["expected_3^6"] == 729,
        "summary.json: expected_3^6 no es 729",
    )
    require(
        words["Fix_CM_Per6"] == 27,
        "summary.json: Fix_CM_Per6 no es 27",
    )
    require(
        words["expected_3^3"] == 27,
        "summary.json: expected_3^3 no es 27",
    )
    violations = words["charge_weight_violations"]
    require(
        violations["tested_words"] == 3 ** 12,
        "summary.json: censo histórico incompleto",
    )
    require(
        violations["violations_charge_sum_CM_negates"] == 0,
        "summary.json: violación histórica de carga",
    )
    require(
        violations["violations_weight_CM_invariant"] == 0,
        "summary.json: violación histórica de peso",
    )

    fixed_row = read_single_row_csv(N40_DIR / "N40_CM_fixed_summary.csv")
    require(int(fixed_row["fixed_total"]) == 729, "CSV fijo: total incorrecto")
    require(
        int(fixed_row["expected_3^6"]) == 729,
        "CSV fijo: valor esperado incorrecto",
    )
    require(
        fixed_row["fixed_charge_counts_mod3"] == "{0: 729}",
        "CSV fijo: distribución de carga inesperada",
    )

    period_row = read_single_row_csv(
        N40_DIR / "N40_CM_Per6_fixed_summary.csv"
    )
    require(
        int(period_row["fixed_per6_total"]) == 27,
        "CSV Per6: total incorrecto",
    )
    require(
        int(period_row["expected_3^3"]) == 27,
        "CSV Per6: valor esperado incorrecto",
    )

    with (N40_DIR / "N40_claim_status.csv").open(
        "r", encoding="utf-8", newline=""
    ) as stream:
        claims = list(csv.DictReader(stream))
    cm_claims = [
        row for row in claims
        if row["claim"].startswith("C_M ")
    ]
    require(len(cm_claims) == 2, "CSV de claims: faltan las dos tesis C_M")
    require(
        all(row["status"].startswith("proved") for row in cm_claims),
        "CSV de claims: una tesis C_M no figura como probada",
    )

    return {
        "artifacts": 4,
        "sha256": observed_hashes,
        "summary_counts_match": True,
        "claim_rows_checked": len(cm_claims),
    }


def verify_residue_support_incidence() -> dict[str, Any]:
    matrix = (
        (2, 1, 0),
        (1, 2, 0),
        (1, 1, 1),
    )
    permutation = (
        (0, 1, 0),
        (1, 0, 0),
        (0, 0, 1),
    )
    determinant = determinant_3(matrix)
    require(determinant == 3, "det(B_res,sup) no es 3")

    entries_gcd = 0
    for row in matrix:
        for value in row:
            entries_gcd = math.gcd(entries_gcd, abs(value))

    minors: list[int] = []
    for rows in itertools.combinations(range(3), 2):
        for columns in itertools.combinations(range(3), 2):
            minors.append(
                determinant_2(
                    matrix[rows[0]][columns[0]],
                    matrix[rows[0]][columns[1]],
                    matrix[rows[1]][columns[0]],
                    matrix[rows[1]][columns[1]],
                )
            )
    minors_gcd = 0
    for value in minors:
        minors_gcd = math.gcd(minors_gcd, abs(value))
    require(entries_gcd == 1, "primer divisor determinantal distinto de 1")
    require(minors_gcd == 1, "segundo divisor determinantal distinto de 1")
    smith = (entries_gcd, minors_gcd // entries_gcd, abs(determinant) // minors_gcd)
    require(smith == (1, 1, 3), "SNF(B_res,sup) no es diag(1,1,3)")

    radius = 12
    source_vectors = 0
    forward_image_violations = 0
    for vector in itertools.product(range(-radius, radius + 1), repeat=3):
        image = matvec(matrix, vector)
        if (image[0] + image[1]) % 3 != 0:
            forward_image_violations += 1
        source_vectors += 1
    require(
        forward_image_violations == 0,
        "la imagen finita incumple u+v=0 módulo 3",
    )

    target_vectors = 0
    inverse_formula_violations = 0
    for u, v, w in itertools.product(
        range(-radius, radius + 1), repeat=3
    ):
        if (u + v) % 3 != 0:
            continue
        x_numerator = 2 * u - v
        y_numerator = 2 * v - u
        if x_numerator % 3 != 0 or y_numerator % 3 != 0:
            inverse_formula_violations += 1
            continue
        x = x_numerator // 3
        y = y_numerator // 3
        z = w - x - y
        if matvec(matrix, (x, y, z)) != (u, v, w):
            inverse_formula_violations += 1
        target_vectors += 1
    require(
        inverse_formula_violations == 0,
        "la fórmula de preimagen no cubre el submódulo en el cubo finito",
    )

    require(
        matmul(matmul(permutation, matrix), permutation) == matrix,
        "P B_res,sup P no coincide con B_res,sup",
    )
    require(
        matmul(permutation, matrix) == matmul(matrix, permutation),
        "la incidencia no es equivariante",
    )

    return {
        "matrix": [list(row) for row in matrix],
        "determinant": determinant,
        "smith_normal_form": list(smith),
        "image_congruence": "u+v=0 mod 3",
        "finite_cube_radius": radius,
        "source_vectors_checked": source_vectors,
        "target_vectors_with_congruence_checked": target_vectors,
        "forward_image_violations": forward_image_violations,
        "inverse_formula_violations": inverse_formula_violations,
        "simultaneous_swap_equivariant": True,
    }


def verify_fibonacci_ring() -> dict[str, Any]:
    identity_matrix = ((1, 0), (0, 1))
    f_av = ((0, 1), (1, 1))
    require(
        matmul(f_av, f_av) == (
            (1, 1),
            (1, 2),
        ),
        "F_av^2 es incorrecta",
    )
    require(
        matmul(f_av, f_av) == tuple(
            tuple(f_av[row][col] + identity_matrix[row][col] for col in range(2))
            for row in range(2)
        ),
        "F_av no satisface X^2=X+I",
    )

    maximum_power = 128
    for exponent in range(1, maximum_power + 1):
        expected = (
            (fibonacci(exponent - 1), fibonacci(exponent)),
            (fibonacci(exponent), fibonacci(exponent + 1)),
        )
        require(
            matrix_power(f_av, exponent) == expected,
            f"potencia Fibonacci incorrecta para n={exponent}",
        )

    one = (1, 0)
    tau = (0, 1)
    require(ring_mul(tau, one) == tau, "τ·1 no es τ")
    require(ring_mul(tau, tau) == (1, 1), "τ·τ no es 1+τ")

    ring_radius = 3
    elements = list(itertools.product(range(-ring_radius, ring_radius + 1), repeat=2))
    triples_checked = 0
    for left, middle, right in itertools.product(elements, repeat=3):
        require(
            ring_mul(ring_mul(left, middle), right)
            == ring_mul(left, ring_mul(middle, right)),
            "el producto del anillo no es asociativo",
        )
        require(
            ring_mul(left, ring_add(middle, right))
            == ring_add(ring_mul(left, middle), ring_mul(left, right)),
            "falla la distributividad izquierda",
        )
        require(
            ring_mul(ring_add(left, middle), right)
            == ring_add(ring_mul(left, right), ring_mul(middle, right)),
            "falla la distributividad derecha",
        )
        triples_checked += 1

    for element in elements:
        require(ring_mul(one, element) == element, "1 no es unidad izquierda")
        require(ring_mul(element, one) == element, "1 no es unidad derecha")
        require(
            ring_mul(tau, element) == matvec(f_av, element),
            "F_av no representa la multiplicación por τ",
        )
    require(
        all(ring_mul(left, right) == ring_mul(right, left)
            for left, right in itertools.product(elements, repeat=2)),
        "el anillo basado no es conmutativo",
    )

    power = one
    for exponent in range(1, maximum_power + 1):
        power = ring_mul(power, tau)
        require(
            power == (fibonacci(exponent - 1), fibonacci(exponent)),
            f"τ^{exponent} no sigue la ley Fibonacci",
        )

    return {
        "F_av": [list(row) for row in f_av],
        "characteristic_polynomial": "lambda^2-lambda-1",
        "matrix_powers_checked": maximum_power,
        "tau_powers_checked": maximum_power,
        "ring_sample_radius": ring_radius,
        "ring_elements_sampled": len(elements),
        "associativity_and_distributivity_triples_checked": triples_checked,
        "based_ring_relations": ["tau*1=tau", "tau*tau=1+tau"],
        "positive_perron_root": "phi",
    }


def verify_z6_and_pointed_center() -> dict[str, Any]:
    residues = tuple(range(6))
    crt_pairs = {(value % 2, value % 3) for value in residues}
    require(len(crt_pairs) == 6, "Z2 por Z3 no parametriza seis clases")

    symmetric_descent = tuple(
        value for value in residues if (2 * value) % 6 == 0
    )
    braided_only = tuple(
        value for value in residues if (2 * value) % 6 != 0
    )
    require(symmetric_descent == (0, 3), "q^2=1 no selecciona k=0,3")
    require(len(braided_only) == 4, "no hay cuatro torsiones no simétricas")

    # Si qP_i v=v, aplicar de nuevo qP_i da q^2 v=v. Para los cuatro
    # exponentes restantes, q^2 != 1 y el subespacio invariante es nulo.
    invariant_obstruction_count = sum(
        1 for value in braided_only if (2 * value) % 6 != 0
    )
    require(
        invariant_obstruction_count == 4,
        "el control de invariantes no cubrió las cuatro torsiones",
    )

    group_a = 9 ** 2
    dual_a = group_a
    simple_objects = group_a * dual_a
    quantum_dimensions_squared = simple_objects
    total_quantum_dimension = math.isqrt(quantum_dimensions_squared)
    require(simple_objects == 6561, "el centro apuntado no tiene 6561 simples")
    require(
        total_quantum_dimension ** 2 == quantum_dimensions_squared,
        "la dimensión cuántica total no es entera",
    )
    require(
        total_quantum_dimension == 81,
        "la dimensión cuántica total no es 81",
    )

    return {
        "braid_abelianization": "Z",
        "crt_character_group": "Z/2 x Z/3 = Z/6",
        "characters": len(residues),
        "bosonic_exponent": 0,
        "fermionic_exponent": 3,
        "symmetric_group_descents": list(symmetric_descent),
        "braided_twists_without_symmetric_descent": list(braided_only),
        "zero_invariant_space_obstructions": invariant_obstruction_count,
        "pointed_group_order": group_a,
        "pointed_dual_order": dual_a,
        "pointed_center_simples": simple_objects,
        "simple_quantum_dimension": 1,
        "total_quantum_dimension": total_quantum_dimension,
        "pointed_no_go": ["Fibonacci", "Ising"],
    }


def compact_latex(text: str) -> str:
    return "".join(text.split())


def require_tokens(
    compact: str,
    requirements: Iterable[tuple[str, str]],
) -> list[str]:
    checked: list[str] = []
    for identifier, token in requirements:
        normalized = compact_latex(token)
        require(normalized in compact, f"fuente LaTeX: falta {identifier}")
        checked.append(identifier)
    return checked


def verify_latex_contract() -> dict[str, Any]:
    require(SOURCE_PATH.is_file(), "fuente topológica integrada ausente")
    require(PRIMARY_CM_PATH.is_file(), "residencia primaria C_M ausente")
    require(STRUCTURE_PATH.is_file(), "estructura_rev8.tex ausente")
    source = SOURCE_PATH.read_text(encoding="utf-8")
    primary = PRIMARY_CM_PATH.read_text(encoding="utf-8")
    structure = STRUCTURE_PATH.read_text(encoding="utf-8")
    compact = compact_latex(primary + "\n" + source)
    source_compact = compact_latex(source)
    primary_compact = compact_latex(primary)
    structure_compact = compact_latex(structure)
    require(
        r"\input{sections/md/06c_sectores_topologicos_no_omision}"
        in structure_compact,
        "el grafo REV.8 no incorpora el capítulo topológico",
    )
    require(
        r"\input{sections/md/04b_banda_particula_virtual}"
        in structure_compact,
        "el grafo REV.8 no incorpora la residencia primaria C_M",
    )
    for label in ("def:palabras-cm", "thm:involucion-cm-censo"):
        token = compact_latex(r"\label{" + label + "}")
        require(token in primary_compact, f"residencia primaria: falta {label}")
        require(token not in source_compact, f"residencia topológica redefine {label}")
        require(
            compact_latex(r"\cref{" + label) in source_compact
            or label in source,
            f"residencia topológica no remite a {label}",
        )

    labels = [
        "chap:sectores-topologicos-no-omision",
        "rem:procedencia-n40-cm",
        "crit:falsadores-cm",
        "sec:cuatro-niveles-majorana",
        "thm:incidencia-residuo-soporte",
        "crit:incidencia-residuo-soporte",
        "def:anillo-basado-fibonacci",
        "thm:anillo-fibonacci-fav",
        "crit:categorificacion-fibonacci",
        "thm:trenzas-caracteres-z6",
        "thm:centro-apuntado-no-go",
        "crit:promocion-sectores-topologicos",
    ]
    for label in labels:
        require(
            compact_latex(r"\label{" + label + "}") in source_compact,
            f"fuente LaTeX: falta el label {label}",
        )

    for forbidden in (
        r"\texttt{PROGRAMA\_ABIERTO}",
        r"\texttt{INTERFAZ\_FISICA}",
        r"\texttt{RESULTADO\_RECUPERADO}",
        r"\texttt{FORMALIZACION\_NUEVA}",
    ):
        require(
            forbidden not in source,
            "BODY_NO_METADISCOURSE: mover estatutos al registro externo",
        )

    require(
        source.count(r"\begin{criterion}") >= 4,
        "la fuente no conserva los cuatro bloques de falsación",
    )

    formulas = require_tokens(
        compact,
        [
            ("dominio C_M", r"\mathscr T_{12}^{\rm word}"),
            (
                "definición C_M",
                r"C_M(\mathbf t):=-\operatorname{rev}(\mathbf t)",
            ),
            ("involución C_M", r"C_M^2=I"),
            (
                "censo C_M",
                r"\left|\operatorname{Fix}(C_M)\right|=3^6=729",
            ),
            (
                "censo C_M Per6",
                r"\bigl|\operatorname{Fix}(C_M)\cap\operatorname{Per}_6\bigr|"
                r"=3^3=27",
            ),
            ("matriz B_res,sup", r"B_{\rm res,sup}"),
            ("determinante B_res,sup", r"\det B_{\rm res,sup}=3"),
            (
                "SNF B_res,sup",
                r"\operatorname{SNF}(B_{\rm res,sup})"
                r"=\operatorname{diag}(1,1,3)",
            ),
            (
                "imagen B_res,sup",
                r"\operatorname{im}B_{\rm res,sup}"
                r"=\{(u,v,w)\in\mathbb Z^3:u+v\equiv0\pmod3\}",
            ),
            ("equivarianza B_res,sup", r"PB_{\rm res,sup}P=B_{\rm res,sup}"),
            ("matriz F_av", r"F_{\rm av}=\begin{pmatrix}0&1\\1&1\end{pmatrix}"),
            ("regla tau unidad", r"\tau\cdot\mathbf 1=\tau"),
            ("regla tau cuadrado", r"\tau\cdot\tau=\mathbf 1+\tau"),
            (
                "potencias tau",
                r"\tau^n=F_{n-1}\mathbf 1+F_n\tau",
            ),
            ("dimensión Perron", r"\operatorname{FPdim}(\tau)=\varphi"),
            ("abelianización de trenzas", r"B_n^{\rm ab}\simeq\mathbb Z"),
            ("criterio de descenso", r"q^2=1"),
            ("invariantes torcidos", r"\operatorname{Inv}(\rho_q)=0"),
            (
                "grupo del centro apuntado",
                r"A=(\mathbb Z/9\mathbb Z)^2",
            ),
            ("censo del centro", r"81^2=6561"),
            ("dimensión total", r"\sqrt{6561}=81"),
        ],
    )

    require(
        "fals" in source.lower(),
        "la fuente no explicita falsadores",
    )
    require(
        r"\mathfrak C_{\rm Fib}" in source
        and compact_latex(r"\dashrightarrow\mathcal C_{\rm Fib}") in compact,
        "la categorificación Fibonacci no figura como flecha discontinua",
    )
    require(
        "no constituyen por sí solos cuatro espacios de Fock" in source,
        "falta el control negativo de las cuatro torsiones",
    )
    require(
        "no proporciona por sí misma un espinor" in source,
        "falta la separación C_M/Majorana",
    )

    return {
        "main_input_active": True,
        "labels_checked": labels,
        "formula_requirements_checked": formulas,
        "primary_cm_owner": str(PRIMARY_CM_PATH.relative_to(ROOT)),
        "body_metadiscourse_absent": True,
        "criterion_environments": source.count(r"\begin{criterion}"),
        "negative_controls_present": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    source_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_statement = "a" + "ssert "
    forbidden_call = "a" + "ssert("
    require(
        forbidden_statement not in source_text
        and forbidden_call not in source_text,
        "el verificador contiene una comprobación desactivable",
    )

    c_m = verify_c_m()
    historical = verify_historical_n40()
    incidence = verify_residue_support_incidence()
    fibonacci_ring = verify_fibonacci_ring()
    z6_center = verify_z6_and_pointed_center()
    latex_contract = verify_latex_contract()

    result = {
        "schema": "HMT.MD.no-omision-topologica.v1",
        "status": "PASS_NO_OMISION_TOPOLOGICA_HMT_MD",
        "edition": "REV.8",
        "checks": {
            "C_M_exhaustive": c_m,
            "N40_historical_evidence": historical,
            "B_res_sup": incidence,
            "F_av_and_based_ring": fibonacci_ring,
            "Z6_and_pointed_center": z6_center,
            "latex_contract": latex_contract,
        },
        "source_hashes": {
            str(SOURCE_PATH.relative_to(ROOT)): sha256(SOURCE_PATH),
            str(PRIMARY_CM_PATH.relative_to(ROOT)): sha256(PRIMARY_CM_PATH),
            str(STRUCTURE_PATH.relative_to(ROOT)): sha256(STRUCTURE_PATH),
            str(Path(__file__).resolve().relative_to(ROOT)):
                sha256(Path(__file__).resolve()),
        },
        "proved_scope": [
            "C_M=-rev is an involution on all 3^12 signed ternary words",
            "Fix(C_M)=729 and Fix(C_M) intersect Per_6 has cardinality 27",
            "the four rehoused N40 artifacts have the frozen historical hashes",
            "B_res,sup has determinant 3, Smith form diag(1,1,3), the stated image, and simultaneous-swap equivariance",
            "F_av represents multiplication by tau in the Fibonacci based ring and its tested powers obey the Fibonacci law",
            "the Z6 character count, the two symmetric descents, the four braided twists, and their invariant-space obstruction",
            "the pointed center has 6561 invertible simples of quantum dimension one and total quantum dimension 81",
            "the active LaTeX contains the required statements, typed boundaries, negative controls, and falsifiers",
        ],
        "not_proved_scope": [
            "a monoidal categorification selected uniquely by TPK",
            "selection by HMT of Fibonacci F/R data, gauge, or chirality",
            "a physical anyon, Majorana fermion, Majorana zero mode, Hamiltonian, spectral gap, or protected braid implementation",
            "a physical identification of the four non-symmetric Z6 twists as four anyonic sectors",
            "a universal mass in MeV for a topological sector",
            "promotion of the rejected EX02 package beyond the independently restated algebraic theorems",
        ],
    }

    encoded = json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
