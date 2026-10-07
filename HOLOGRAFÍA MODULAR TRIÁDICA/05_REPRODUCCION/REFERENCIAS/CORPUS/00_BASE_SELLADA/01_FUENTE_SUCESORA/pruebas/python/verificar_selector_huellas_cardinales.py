#!/usr/bin/env python3
"""Audita selectores de huellas cardinales hacia firmas de especies.

La auditoría no usa masas. Contrasta dos codominios de estatuto distinto:

1. los pares (n_A,s_C) de doce especies, conservados como decodificación
   inversa dependiente de objetivos, que se usan únicamente como prueba de
   consistencia algebraica;
2. las firmas enteras vigentes de cinco coordenadas, restringidas a las
   especies que también aparecen en la tabla cardinal histórica.

Se estudian mapas afines sobre Q y sobre cuerpos finitos, pruebas
leave-one-out y el espacio cuadrático de grado a lo sumo dos. El programa no
modifica manuscritos ni fuentes activas.
"""

from __future__ import annotations

from collections import Counter
import csv
from fractions import Fraction
import hashlib
import itertools
import json
from math import gcd, lcm
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MD = ROOT
FOOTPRINTS = MD / "datos/cierre_rutas_masas/rutas_NS_EW_historicas.csv"
INVERSE_PAIRS = MD / "datos/decodificacion_inversa_12_especies.csv"
CURRENT_SIGNATURES = MD / "datos/firmas_enteras_diez_especies.csv"
OUTPUT = ROOT / "certificados/selector_huellas_cardinales.json"

FEATURE_NAMES_FULL = ("1", "turns", "switches", "N", "E", "S", "O", "leaf369", "res5", "axis")
# O=108-N-E-S en las doce huellas; se elimina para trabajar en una base.
FEATURE_NAMES = ("1", "turns", "switches", "N", "E", "S", "leaf369", "res5", "axis")
VARIABLE_NAMES = FEATURE_NAMES[1:]
TARGET_PAIR_NAMES = ("nA", "sC")
TARGET_SIGNATURE_NAMES = ("nA", "sC", "k_D4", "nu120", "nu270")
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 101, 1009)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("SELECTOR_HUELLAS FAIL: " + message)


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.is_file(), "falta " + str(path))
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def transpose(matrix: list[list[object]]) -> list[list[object]]:
    return [list(column) for column in zip(*matrix)] if matrix else []


def rref_fraction(matrix: list[list[int | Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    if not matrix:
        return [], []
    work = [[Fraction(value) for value in row] for row in matrix]
    rows, columns = len(work), len(work[0])
    pivot_row = 0
    pivots: list[int] = []
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivots


def rank_fraction(matrix: list[list[int | Fraction]]) -> int:
    return len(rref_fraction(matrix)[1])


def solve_fraction(
    matrix: list[list[int | Fraction]], vector: list[int | Fraction]
) -> dict[str, object]:
    require(len(matrix) == len(vector), "dimensiones del sistema racional")
    rows = [list(row) + [value] for row, value in zip(matrix, vector)]
    rank_matrix = rank_fraction(matrix)
    reduced, pivots_augmented = rref_fraction(rows)
    rank_augmented = len(pivots_augmented)
    variables = len(matrix[0])
    inconsistent = any(
        all(row[column] == 0 for column in range(variables)) and row[-1] != 0
        for row in reduced
    )
    solution = [Fraction(0) for _ in range(variables)]
    if not inconsistent:
        for row_index, pivot in enumerate(pivots_augmented):
            if pivot < variables:
                solution[pivot] = reduced[row_index][-1]
    return {
        "consistent": not inconsistent,
        "rank": rank_matrix,
        "augmented_rank": rank_augmented,
        "nullity": variables - rank_matrix,
        "solution": solution if not inconsistent else None,
    }


def nullspace_fraction(matrix: list[list[int | Fraction]]) -> list[list[Fraction]]:
    if not matrix:
        return []
    reduced, pivots = rref_fraction(matrix)
    columns = len(matrix[0])
    free = [column for column in range(columns) if column not in pivots]
    basis: list[list[Fraction]] = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free_column] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(vector)
    return basis


def primitive_integer(vector: list[Fraction]) -> list[int]:
    denominator = 1
    for value in vector:
        denominator = lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in vector]
    common = 0
    for value in integers:
        common = gcd(common, abs(value))
    if common:
        integers = [value // common for value in integers]
    first = next((value for value in integers if value), 1)
    if first < 0:
        integers = [-value for value in integers]
    return integers


def dot(left: Iterable[int | Fraction], right: Iterable[int | Fraction]) -> Fraction:
    return sum((Fraction(a) * Fraction(b) for a, b in zip(left, right)), Fraction(0))


def short_left_obstruction(matrix: list[list[int]], target: list[int]) -> dict[str, object]:
    basis = nullspace_fraction(transpose(matrix))
    require(basis, "el espacio de obstrucciones izquierdo es trivial")
    candidates: list[tuple[tuple[int, int, int], list[int], int]] = []
    # La nulidad izquierda es tres. Un barrido simétrico algo más amplio
    # permite escoger un certificado entero más legible sin cambiar la prueba.
    for coefficients in itertools.product(range(-12, 13), repeat=len(basis)):
        if not any(coefficients):
            continue
        vector = [
            sum(Fraction(coefficients[j]) * basis[j][i] for j in range(len(basis)))
            for i in range(len(matrix))
        ]
        integers = primitive_integer(vector)
        violation = int(dot(integers, target))
        if violation:
            score = (
                sum(value != 0 for value in integers),
                max(abs(value) for value in integers),
                sum(abs(value) for value in integers),
            )
            candidates.append((score, integers, violation))
    require(candidates, "no se encontró testigo de inconsistencia")
    _, witness, violation = min(candidates, key=lambda item: item[0])
    require(all(dot(witness, column) == 0 for column in transpose(matrix)), "testigo izquierdo")
    return {
        "coefficients_by_row": witness,
        "feature_relation_value": 0,
        "target_relation_value": violation,
        "support": sum(value != 0 for value in witness),
    }


def rank_mod_prime(matrix: list[list[int]], prime: int) -> int:
    if not matrix:
        return 0
    work = [[value % prime for value in row] for row in matrix]
    rows, columns = len(work), len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [(value * inverse) % prime for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def modular_audit(matrix: list[list[int]], targets: list[list[int]]) -> dict[str, object]:
    report: dict[str, object] = {}
    for prime in PRIMES:
        rank = rank_mod_prime(matrix, prime)
        target_report = {}
        joint = True
        for name, target in zip(TARGET_PAIR_NAMES, targets):
            augmented = [row + [value] for row, value in zip(matrix, target)]
            augmented_rank = rank_mod_prime(augmented, prime)
            consistent = augmented_rank == rank
            joint = joint and consistent
            target_report[name] = {
                "consistent": consistent,
                "rank": rank,
                "augmented_rank": augmented_rank,
            }
        report[str(prime)] = {
            "rank": rank,
            "nullity": len(matrix[0]) - rank,
            "targets": target_report,
            "joint_selector_exists": joint,
            "joint_solution_count_if_consistent": (
                f"{prime}^{2 * (len(matrix[0]) - rank)}" if joint else "0"
            ),
        }
    return report


def leave_one_out(matrix: list[list[int]], targets: list[list[int]], labels: list[str]) -> dict[str, object]:
    rows = []
    for omitted in range(len(matrix)):
        train_matrix = [row for index, row in enumerate(matrix) if index != omitted]
        train_targets = [
            [value for index, value in enumerate(target) if index != omitted]
            for target in targets
        ]
        solutions = [solve_fraction(train_matrix, target) for target in train_targets]
        consistent = all(bool(solution["consistent"]) for solution in solutions)
        determined = (
            consistent
            and rank_fraction(train_matrix + [matrix[omitted]]) == rank_fraction(train_matrix)
        )
        prediction = None
        correct = False
        if determined:
            prediction = [
                str(dot(matrix[omitted], solution["solution"]))  # type: ignore[arg-type]
                for solution in solutions
            ]
            correct = all(
                Fraction(prediction[index]) == targets[index][omitted]
                for index in range(len(targets))
            )
        rows.append(
            {
                "omitted": labels[omitted],
                "training_consistent": consistent,
                "heldout_determined": determined,
                "prediction": prediction,
                "correct": correct,
            }
        )
    return {
        "rows": rows,
        "training_consistent_count": sum(row["training_consistent"] for row in rows),
        "heldout_determined_count": sum(row["heldout_determined"] for row in rows),
        "correct_prediction_count": sum(row["correct"] for row in rows),
    }


def quadratic_design(base_variables: list[list[int]]) -> tuple[list[str], list[list[int]]]:
    names = ["1", *VARIABLE_NAMES]
    columns = [[1 for _ in base_variables]]
    for index, _name in enumerate(VARIABLE_NAMES):
        columns.append([row[index] for row in base_variables])
    for left in range(len(VARIABLE_NAMES)):
        for right in range(left, len(VARIABLE_NAMES)):
            names.append(f"{VARIABLE_NAMES[left]}*{VARIABLE_NAMES[right]}")
            columns.append([row[left] * row[right] for row in base_variables])
    # La primera ampliación anterior ya añadió los nombres lineales al crear
    # names; no debe duplicarlos en el bucle. Comprobación explícita.
    require(len(names) == len(columns) == 45, "base cuadrática de 45 monomios")
    return names, transpose(columns)  # type: ignore[arg-type]


def greedy_interpolation_basis(design: list[list[int]]) -> list[int]:
    selected: list[int] = []
    current_rank = 0
    for column in range(len(design[0])):
        candidate = [[row[index] for index in selected + [column]] for row in design]
        rank = rank_fraction(candidate)
        if rank > current_rank:
            selected.append(column)
            current_rank = rank
        if current_rank == len(design):
            break
    require(current_rank == len(design), "la base cuadrática no interpola las doce filas")
    return selected


def sparse_quadratic_search(
    design: list[list[int]], targets: list[list[int]], maximum_terms: int = 4
) -> dict[str, object]:
    columns = len(design[0])
    tested = 0
    first_joint = None
    first_individual: dict[int, tuple[int, ...] | None] = {index: None for index in range(len(targets))}
    for size in range(1, maximum_terms + 1):
        for subset in itertools.combinations(range(columns), size):
            tested += 1
            submatrix = [[row[column] for column in subset] for row in design]
            base_rank = rank_mod_prime(submatrix, 1009)
            individual = []
            for index, target in enumerate(targets):
                augmented = [row + [value] for row, value in zip(submatrix, target)]
                possible = rank_mod_prime(augmented, 1009) == base_rank
                if possible:
                    possible = bool(solve_fraction(submatrix, target)["consistent"])
                individual.append(possible)
                if possible and first_individual[index] is None:
                    first_individual[index] = subset
            if all(individual):
                first_joint = subset
                break
        if first_joint is not None:
            break
    return {
        "maximum_terms": maximum_terms,
        "supports_tested": tested,
        "joint_support_found": list(first_joint) if first_joint is not None else None,
        "first_individual_supports": {
            TARGET_PAIR_NAMES[index]: (list(subset) if subset is not None else None)
            for index, subset in first_individual.items()
        },
    }


def footprint_vector(row: dict[str, str], full: bool = False) -> list[int]:
    axis = 1 if row["axis"] == "N-S" else -1
    values = [
        1,
        int(row["turns"]),
        int(row["switches"]),
        int(row["N"]),
        int(row["E"]),
        int(row["S"]),
    ]
    if full:
        values.append(int(row["O"]))
    values.extend((int(row["leaf369"]), int(row["res5"]), axis))
    return values


def audit() -> dict[str, object]:
    footprints = read_csv(FOOTPRINTS)
    inverse = read_csv(INVERSE_PAIRS)
    current = read_csv(CURRENT_SIGNATURES)
    require(len(footprints) == len(inverse) == 12, "doce especies")
    require(all(row["epistemic_role"] == "INVERSE_TARGET_DEPENDENT" for row in inverse), "tipo de los pares")

    route_labels = [row["object"] for row in footprints]
    require(route_labels == [row["species"] for row in inverse], "orden de las doce especies")
    for row in footprints:
        require(sum(int(row[key]) for key in ("N", "E", "S", "O")) == 108, "longitud cardinal 108")

    full_matrix = [footprint_vector(row, full=True) for row in footprints]
    matrix = [footprint_vector(row, full=False) for row in footprints]
    pair_targets = [
        [int(row[name]) for row in inverse]
        for name in TARGET_PAIR_NAMES
    ]
    rank_full = rank_fraction(full_matrix)
    rank_basis = rank_fraction(matrix)
    require(rank_full == rank_basis, "O no era redundante")

    pair_solutions = {
        name: solve_fraction(matrix, target)
        for name, target in zip(TARGET_PAIR_NAMES, pair_targets)
    }
    require(not any(solution["consistent"] for solution in pair_solutions.values()), "apareció un mapa afín racional")
    obstructions = {
        name: short_left_obstruction(matrix, target)
        for name, target in zip(TARGET_PAIR_NAMES, pair_targets)
    }

    modular = modular_audit(matrix, pair_targets)
    loo = leave_one_out(matrix, pair_targets, route_labels)

    base_variables = [row[1:] for row in matrix]
    quadratic_names, quadratic = quadratic_design(base_variables)
    quadratic_rank = rank_fraction(quadratic)
    require(quadratic_rank == 12, "el espacio cuadrático no tiene rango fila completo")
    interpolation_basis = greedy_interpolation_basis(quadratic)
    interpolation_matrix = [[row[index] for index in interpolation_basis] for row in quadratic]
    interpolation = {}
    for name, target in zip(TARGET_PAIR_NAMES, pair_targets):
        solution = solve_fraction(interpolation_matrix, target)
        require(solution["consistent"] and solution["nullity"] == 0, "interpolación cuadrática")
        coefficients: list[Fraction] = solution["solution"]  # type: ignore[assignment]
        interpolation[name] = {
            "coefficients": [str(value) for value in coefficients],
            "maximum_numerator_absolute": max(abs(value.numerator) for value in coefficients),
            "maximum_denominator": max(value.denominator for value in coefficients),
        }
    quadratic_loo = leave_one_out(quadratic, pair_targets, route_labels)
    sparse = sparse_quadratic_search(quadratic, pair_targets, maximum_terms=4)

    current_by_species = {
        row["species"]: [int(row[name]) for name in TARGET_SIGNATURE_NAMES]
        for row in current
    }
    strict_overlap = [label for label in route_labels if label in current_by_species]
    require(strict_overlap == ["mu", "tau", "W", "Z"], "intersección con firmas vigentes")
    route_by_species = {row["object"]: row for row in footprints}
    overlap_matrix = [footprint_vector(route_by_species[label], full=False) for label in strict_overlap]
    overlap_targets = [
        [current_by_species[label][coordinate] for label in strict_overlap]
        for coordinate in range(5)
    ]
    overlap_rank = rank_fraction(overlap_matrix)
    require(overlap_rank == 4, "las cuatro huellas coincidentes no son independientes")
    overlap_solutions = [solve_fraction(overlap_matrix, target) for target in overlap_targets]
    require(all(solution["consistent"] for solution in overlap_solutions), "una firma coincidente no interpola")
    require(all(solution["nullity"] == 5 for solution in overlap_solutions), "nulidad de la intersección")
    overlap_loo = leave_one_out(overlap_matrix, overlap_targets, strict_overlap)

    # El electrón puede añadirse como origen nulo sólo mediante una convención
    # externa a la tabla vigente de diez firmas; se audita por separado.
    augmented_labels = ["e", *strict_overlap]
    augmented_matrix = [footprint_vector(route_by_species[label], full=False) for label in augmented_labels]
    augmented_targets = [
        [0, *target]
        for target in overlap_targets
    ]
    augmented_rank = rank_fraction(augmented_matrix)
    augmented_solutions = [solve_fraction(augmented_matrix, target) for target in augmented_targets]
    require(augmented_rank == 5 and all(solution["consistent"] for solution in augmented_solutions), "origen electrónico")

    return {
        "schema": "HMT.MD.cardinal-footprints.selector-audit.v1",
        "status": "PASS_NO_IDENTIFIABLE_LOW_COMPLEXITY_SELECTOR",
        "source_hashes_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (FOOTPRINTS, INVERSE_PAIRS, CURRENT_SIGNATURES)
        },
        "input_typing": {
            "historical_cardinal_footprints": {
                "rows": len(footprints),
                "species": route_labels,
                "fields": list(FEATURE_NAMES_FULL[1:]),
                "exact_identity": "N+E+S+O=108",
            },
            "twelve_pair_table": {
                "fields": list(TARGET_PAIR_NAMES),
                "epistemic_role": "INVERSE_TARGET_DEPENDENT",
                "use_in_this_audit": "algebraic stress test only; no masses are read",
            },
            "current_five_coordinate_signatures": {
                "fields": list(TARGET_SIGNATURE_NAMES),
                "strict_species_overlap": strict_overlap,
            },
        },
        "affine_rational_audit_on_twelve_pairs": {
            "feature_columns_full": list(FEATURE_NAMES_FULL),
            "full_column_count": len(FEATURE_NAMES_FULL),
            "rank_full": rank_full,
            "independent_spanning_columns": list(FEATURE_NAMES),
            "basis_column_count": len(FEATURE_NAMES),
            "rank_basis": rank_basis,
            "left_constraint_dimension": len(matrix) - rank_basis,
            "targets": {
                name: {
                    "consistent": bool(solution["consistent"]),
                    "rank": int(solution["rank"]),
                    "augmented_rank": int(solution["augmented_rank"]),
                    "obstruction": obstructions[name],
                }
                for name, solution in pair_solutions.items()
            },
            "integer_affine_selector_exists": False,
            "reason": "Both target coordinates fail necessary rational affine consistency, hence also integer consistency.",
        },
        "modular_affine_audit_on_twelve_pairs": {
            "prime_fields": modular,
            "composite_consequence": (
                "Inconsistency modulo 3 rules out affine selectors modulo 9, 27 and 108; "
                "inconsistency modulo 2 and modulo 5 rules out one modulo 1000. More generally, "
                "failure after reduction modulo a prime divisor rules out a selector over the "
                "corresponding composite residue ring."
            ),
            "hmt_relevant_moduli_ruled_out": [9, 27, 108, 1000],
        },
        "leave_one_out_affine_on_twelve_pairs": loo,
        "quadratic_interpolation_audit": {
            "monomial_degree": 2,
            "monomial_count": len(quadratic_names),
            "row_rank": quadratic_rank,
            "solution_dimension_per_target": len(quadratic_names) - quadratic_rank,
            "one_greedy_interpolation_basis": [quadratic_names[index] for index in interpolation_basis],
            "one_interpolation": interpolation,
            "leave_one_out": quadratic_loo,
            "sparse_joint_search": {
                **sparse,
                "monomial_names_for_found_support": (
                    [quadratic_names[index] for index in sparse["joint_support_found"]]
                    if sparse["joint_support_found"] is not None
                    else None
                ),
            },
            "interpretation": (
                "Degree-two features have full row rank and can interpolate arbitrary labels on the twelve rows. "
                "The held-out value is therefore unconstrained; exact fit is not an identified selector."
            ),
        },
        "current_five_coordinate_overlap": {
            "strict_overlap_species": strict_overlap,
            "sample_count": len(strict_overlap),
            "feature_rank": overlap_rank,
            "coefficient_count_per_coordinate": len(FEATURE_NAMES),
            "solution_dimension_per_coordinate": [int(solution["nullity"]) for solution in overlap_solutions],
            "all_five_coordinates_interpolable": True,
            "unique_rule": False,
            "leave_one_out": overlap_loo,
            "electron_origin_extension": {
                "status": "additional convention; electron has no row in the current ten-signature table",
                "sample_count": len(augmented_labels),
                "feature_rank": augmented_rank,
                "solution_dimension_per_coordinate": [int(solution["nullity"]) for solution in augmented_solutions],
                "unique_rule": False,
            },
        },
        "conclusion": {
            "exact": (
                "The twelve historical footprints do not admit a rational, hence not an integer, affine map "
                "to either coordinate of the twelve inverse pair table. On the four species shared with the "
                "current five-coordinate signature table, every output can be interpolated but the coefficient "
                "space has dimension five per coordinate, so no rule is identifiable and leave-one-out values "
                "are not forced. Quadratic degree-two fitting has full row rank and is pure interpolation."
            ),
            "selector_status": "NO_INTERNAL_UNIQUE_LOW_COMPLEXITY_SELECTOR_FOUND",
            "what_would_change_the_status": (
                "A predeclared formula or symmetry reducing the coefficient space before viewing the labels, "
                "followed by successful held-out prediction on species not used to choose it."
            ),
        },
    }


def main() -> None:
    result = audit()
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_SELECTOR_HUELLAS_CARDINALES_NO_IDENTIFICABLE")


if __name__ == "__main__":
    main()
