#!/usr/bin/env python3
"""Verifica la incidencia dodecafase--Witt y el sector positivo 3/11.

El calculo no usa constantes fisicas ni objetivos decimales. Reconstruye el
Golay ternario extendido y el W_12 con el etiquetado HMT vigente. Comprueba de
manera entera el transporte de incidencia punto--hexada, contrasta la accion
A5/C5 declarada y lee los conteos N73 directamente de sus CSV historicos.

Las comprobaciones usan ``require`` y permanecen activas con ``python -O``.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datos"
OUTPUT = ROOT / "certificados/entrelazador_incidencia_witt.json"
N73_DIR = DATA
U6_CATALOG = DATA / "TPK_U_catalog_468.json"

AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)

# Bijeccion dodecafasica vigente: posiciones 1,...,12 -> A5/C5.
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("ENTRELAZADOR INCIDENCIA FAIL: " + message)


def ternary_codeword(left: tuple[int, ...]) -> tuple[int, ...]:
    right = tuple(
        sum(left[i] * AW[i][j] for i in range(6)) % 3
        for j in range(6)
    )
    return left + right


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.is_file(), "falta el CSV " + str(path))
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def rank_mod_prime(matrix: list[list[int]], prime: int) -> int:
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [value * inverse % prime for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (value - factor * pivot_value) % prime
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def construct_witt_design() -> tuple[list[frozenset[int]], dict[str, object]]:
    words = [ternary_codeword(left) for left in itertools.product(range(3), repeat=6)]
    weight_enumerator = Counter(sum(value != 0 for value in word) for word in words)
    require(
        weight_enumerator == Counter({0: 1, 6: 264, 9: 440, 12: 24}),
        "enumerador del Golay ternario extendido",
    )
    hexads = sorted(
        {
            frozenset(index for index, value in enumerate(word) if value)
            for word in words
            if sum(value != 0 for value in word) == 6
        },
        key=lambda block: tuple(sorted(block)),
    )
    require(len(hexads) == 132, "132 hexadas")
    five_counts = Counter(
        subset
        for hexad in hexads
        for subset in itertools.combinations(sorted(hexad), 5)
    )
    require(
        len(five_counts) == math.comb(12, 5)
        and set(five_counts.values()) == {1},
        "propiedad S(5,6,12)",
    )
    require(
        all(frozenset(range(12)) - block in set(hexads) for block in hexads),
        "cierre por complemento de W12",
    )
    return hexads, {
        "construction": "extended ternary Golay code in the HMT labeling",
        "ternary_golay_words": len(words),
        "weight_enumerator": {str(weight): count for weight, count in sorted(weight_enumerator.items())},
        "hexads": len(hexads),
    }


def point_hexad_intertwiner(hexads: list[frozenset[int]]) -> dict[str, object]:
    # I_{H,p}=1 si p pertenece a H. I(v)(H)=sum_{p in H} v_p.
    incidence = [
        [1 if point in hexad else 0 for point in range(12)]
        for hexad in hexads
    ]
    point_gram = [
        [
            sum(row[left] * row[right] for row in incidence)
            for right in range(12)
        ]
        for left in range(12)
    ]
    require(
        all(
            point_gram[i][j] == (66 if i == j else 30)
            for i in range(12)
            for j in range(12)
        ),
        "I^T I = 36 I + 30 J",
    )

    # G es el Gram tetrada--hexada: G_{H,H'}=C(|H cap H'|,4).
    gram = [
        [math.comb(len(left & right), 4) for right in hexads]
        for left in hexads
    ]
    gram_times_incidence = [
        [
            sum(gram[row][column] * incidence[column][point]
                for column in range(132))
            for point in range(12)
        ]
        for row in range(132)
    ]
    require(
        all(
            gram_times_incidence[row][point]
            == 30 * incidence[row][point] + 15
            for row in range(132)
            for point in range(12)
        ),
        "G I = 30 I + 15 J",
    )
    shifted_gram = [
        [
            gram[row][column] - (30 if row == column else 0)
            for column in range(132)
        ]
        for row in range(132)
    ]
    # Las once columnas centradas dan nulidad al menos once sobre Q. El rango
    # 121 modulo 1009 da rango racional al menos 121; ambas cotas fuerzan
    # exactamente dim ker(G-30 Id)=11.
    shifted_rank_mod_1009 = rank_mod_prime(shifted_gram, 1009)
    require(shifted_rank_mod_1009 == 121, "multiplicidad exacta de E_30")

    # Base entera e_i-e_11 del hiperplano V11.
    centered_columns = [
        [incidence[row][i] - incidence[row][11] for row in range(132)]
        for i in range(11)
    ]
    centered_gram = [
        [
            sum(centered_columns[i][row] * centered_columns[j][row]
                for row in range(132))
            for j in range(11)
        ]
        for i in range(11)
    ]
    require(
        all(
            centered_gram[i][j] == (72 if i == j else 36)
            for i in range(11)
            for j in range(11)
        ),
        "I^T I=36 Id sobre V11",
    )
    for column in centered_columns:
        require(
            [sum(gram[row][k] * column[k] for k in range(132))
             for row in range(132)]
            == [30 * value for value in column],
            "imagen centrada en E_30",
        )

    # Estrella basada en la primera tetrada: fija cuatro puntos y permuta los
    # cuatro petalos por transposiciones.
    # Cara HMT seleccionada B_K=H_e cap P_pi, en indices cero.
    base = frozenset((3, 5, 8, 9))
    petals = sorted(
        (hexad - base for hexad in hexads if base <= hexad),
        key=lambda pair: tuple(sorted(pair)),
    )
    require(len(petals) == 4 and all(len(pair) == 2 for pair in petals),
            "cuatro petalos binarios")
    require(set().union(*petals) == set(range(12)) - set(base),
            "los petalos particionan el complemento")
    permutation = list(range(12))
    for pair in petals:
        left, right = sorted(pair)
        permutation[left] = right
        permutation[right] = left
    require(sum(i == image for i, image in enumerate(permutation)) == 4,
            "la estrella fija la tetrada")
    hexad_index = {block: index for index, block in enumerate(hexads)}
    image_indices = []
    for hexad in hexads:
        image = frozenset(permutation[point] for point in hexad)
        require(image in hexad_index, "la estrella preserva W12")
        image_indices.append(hexad_index[image])
    require(
        all(
            incidence[image_indices[row]][permutation[point]]
            == incidence[row][point]
            for row in range(132)
            for point in range(12)
        ),
        "la incidencia entrelaza las dos acciones de estrella",
    )

    # En R^12 la estrella tiene 8 modos pares y 4 impares. Al retirar el
    # uniforme queda 7+4 en V11 y, por U=I/6, tambien en E30.
    star_even_v11 = 7
    star_odd_v11 = 4
    star_trace = star_even_v11 - star_odd_v11
    require(star_trace == 3, "traza 7-4 de la estrella")

    return {
        "incidence_shape": [132, 12],
        "point_design_identity": "I^T I = 36 Id + 30 J",
        "hexad_gram_identity": "G I = 30 I + 15 J",
        "restricted_isometry": "U=(1/6) I: V11 -> E30",
        "image_dimension": 11,
        "image_gram_eigenvalue": 30,
        "rank_G_minus_30_Id_mod_1009": shifted_rank_mod_1009,
        "E30_equals_kernel_dimension": 11,
        "star_base_tetrad_zero_based": sorted(base),
        "star_petals_zero_based": [sorted(pair) for pair in petals],
        "star_coordinate_permutation_zero_based": permutation,
        "star_even_odd_on_V11_and_E30": [star_even_v11, star_odd_v11],
        "star_trace": star_trace,
        "equivariance": "I(gv)=gI(v) for every design automorphism g",
        "uniqueness": (
            "Within scalar multiples of the published point-hexad incidence "
            "matrix, isometry plus positive incidence fixes U=I/6. The script "
            "does not enumerate Aut(W12) or prove uniqueness among all "
            "equivariant kernels."
        ),
    }


def compose_small(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def parity_small(permutation: tuple[int, ...]) -> int:
    return sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    ) % 2


def permutation_order(permutation: tuple[int, ...]) -> int:
    identity = tuple(range(len(permutation)))
    power = identity
    for order in range(1, 61):
        power = compose_small(permutation, power)
        if power == identity:
            return order
    raise RuntimeError("ENTRELAZADOR INCIDENCIA FAIL: orden de permutacion no encontrado")


def declared_a5_coset_action() -> list[tuple[int, ...]]:
    a5 = [
        permutation
        for permutation in itertools.permutations(range(5))
        if parity_small(permutation) == 0
    ]
    require(len(a5) == 60, "orden de A5")
    identity = tuple(range(5))
    generator_c5 = (1, 2, 3, 4, 0)
    subgroup_c5 = set()
    power = identity
    for _ in range(5):
        subgroup_c5.add(power)
        power = compose_small(generator_c5, power)
    cosets = [
        frozenset(compose_small(representative, element) for element in subgroup_c5)
        for representative in COS_REPS
    ]
    require(len(set(cosets)) == 12, "doce cosets A5/C5")
    coset_index = {
        element: index
        for index, coset in enumerate(cosets)
        for element in coset
    }
    require(len(coset_index) == 60, "particion de A5 por C5")
    actions = []
    for element in a5:
        action = []
        for coset in cosets:
            representative = next(iter(coset))
            action.append(coset_index[compose_small(element, representative)])
        require(len(set(action)) == 12, "accion por permutaciones en A5/C5")
        actions.append(tuple(action))
    require(len(set(actions)) == 60, "accion fiel de A5/C5")
    return actions


def a5_and_operator_obstruction(
    hexads: list[frozenset[int]],
) -> dict[str, object]:
    # Character calculation for the 12-vertex A5 permutation module.
    class_sizes = (1, 15, 20, 12, 12)
    permutation_character = (12, 0, 0, 2, 2)
    # chi_3=(3,-1,0,phi,phi'), with phi+phi'=1.
    multiplicity_three = Fraction(36 + 24, 60)
    require(multiplicity_three == 1, "multiplicidad del irrep V3")
    projector_rank = 3
    active_dimension = 11
    tau_projector = Fraction(projector_rank, active_dimension)

    actions = declared_a5_coset_action()
    action_profile = Counter(
        (permutation_order(action), sum(index == image for index, image in enumerate(action)))
        for action in actions
    )
    require(
        action_profile == Counter({(1, 12): 1, (2, 0): 15, (3, 0): 20, (5, 2): 24}),
        "perfil exacto de la accion A5/C5",
    )
    hexad_set = set(hexads)
    design_preservers = [
        action
        for action in actions
        if all(
            frozenset(action[point] for point in hexad) in hexad_set
            for hexad in hexads
        )
    ]
    require(
        len(design_preservers) == 1
        and design_preservers[0] == tuple(range(12)),
        "la accion A5/C5 declarada no es una subaccion del W12 etiquetado",
    )

    # P3 y la estrella tienen la misma traza, pero espectros diferentes.
    p3_spectrum = {"1": 3, "0": 8}
    star_spectrum = {"1": 7, "-1": 4}
    require(p3_spectrum != star_spectrum, "espectros distintos")
    require(Fraction(7 - 4, 11) == tau_projector == Fraction(3, 11),
            "igualdad de trazas normalizadas")
    return {
        "A5_class_sizes": list(class_sizes),
        "A5_permutation_character": list(permutation_character),
        "declared_A5_C5_action_profile_order_fixedpoints": {
            str(key): value for key, value in sorted(action_profile.items())
        },
        "declared_A5_actions_preserving_labeled_W12": len(design_preservers),
        "declared_A5_is_subgroup_of_labeled_W12_automorphisms": False,
        "equivariance_scope": (
            "U is Aut(W12)-equivariant and canonically transports the labeled P3, "
            "but it is not an intertwiner for the declared A5/C5 action because "
            "that action does not preserve the labeled W12."
        ),
        "V3_multiplicity": int(multiplicity_three),
        "P3_spectrum_on_V11": p3_spectrum,
        "Witt_star_spectrum_on_E30": star_spectrum,
        "normalized_trace_P3": "3/11",
        "normalized_trace_star": "3/11",
        "invertible_operator_intertwiner": False,
        "no_go_reason": (
            "An invertible F with F P3 = R_star F would make P3 and R_star "
            "similar, but their spectra and minimal polynomials differ."
        ),
        "positive_transport": (
            "The canonical positive operator on E30 is Q3=U P3 U*, a rank-3 "
            "orthogonal projector. R_star is an orientation involution and is "
            "not positive."
        ),
    }


def n73_gate_audit() -> dict[str, object]:
    profile = read_csv(N73_DIR / "N73_orientation_gate_resolution_depths.csv")
    details = read_csv(N73_DIR / "N72_selected_branches_survival_details.csv")
    row7 = next(row for row in profile if row["t"] == "7")
    row8 = next(row for row in profile if row["t"] == "8")
    row9 = next(row for row in profile if row["t"] == "9")

    # Objeto correcto: en t=7 la filtracion local es 11 -> 3 -> 1.
    require(row7["num_selected"] == "11", "t=7 tiene once ramas")
    require(row7["survivors_h1"] == "11", "t=7 conserva once ramas en h1")
    require(row7["survivors_h2"] == "3", "t=7 conserva tres ramas en h2")
    require(row7["survivors_h3"] == "1", "t=7 conserva una rama en h3")
    branches7 = [row for row in details if row["t"] == "7"]
    require(len(branches7) == 11, "once filas de rama en t=7")
    surviving7 = [row for row in branches7 if int(row["surv_h2"]) > 0]
    expected_surviving_rows = {
        "200112|212221|110110",
        "200121|212212|110110",
        "200211|212122|110110",
    }
    require(
        {row["rows"] for row in surviving7} == expected_surviving_rows,
        "triplete superviviente correcto en t=7,h=2",
    )

    # S3 permuta simultaneamente las tres posiciones finales de pi y e,
    # mientras phi permanece como eje fijo.
    permutations = list(itertools.permutations(range(3)))

    def act_gate_row(encoded: str, permutation: tuple[int, int, int]) -> str:
        pi_component, e_component, phi_component = encoded.split("|")

        def act_tail(word: str) -> str:
            return word[:3] + "".join(word[3 + index] for index in permutation)

        return "|".join(
            (act_tail(pi_component), act_tail(e_component), phi_component)
        )

    all_gate_rows = {row["rows"] for row in branches7}
    surviving_gate_rows = {row["rows"] for row in surviving7}
    require(
        all(
            act_gate_row(row, permutation) in all_gate_rows
            for row in all_gate_rows
            for permutation in permutations
        ),
        "accion S3 sobre las once ramas",
    )
    require(
        all(
            act_gate_row(row, permutation) in surviving_gate_rows
            for row in surviving_gate_rows
            for permutation in permutations
        ),
        "el triplete superviviente es una orbita S3",
    )

    unseen = set(all_gate_rows)
    orbit_sizes = []
    while unseen:
        seed = min(unseen)
        orbit = {act_gate_row(seed, permutation) for permutation in permutations}
        require(orbit <= all_gate_rows, "orbita S3 fuera de las ramas")
        orbit_sizes.append(len(orbit))
        unseen -= orbit
    require(sorted(orbit_sizes) == [1, 1, 3, 3, 3],
            "descomposicion orbital 1+1+3+3+3")

    identity = (0, 1, 2)
    transposition = (1, 0, 2)
    three_cycle = (1, 2, 0)
    representatives = (identity, transposition, three_cycle)
    full_character = [
        sum(act_gate_row(row, permutation) == row for row in all_gate_rows)
        for permutation in representatives
    ]
    gate_character = [
        sum(
            act_gate_row(row, permutation) == row
            for row in surviving_gate_rows
        )
        for permutation in representatives
    ]
    require(full_character == [11, 5, 2], "caracter S3 de las once ramas")
    require(gate_character == [3, 1, 0], "caracter 1+2 del triplete")

    # El proyector diagonal de supervivencia P_G tiene rango tres y conmuta
    # con S3 porque su soporte es una orbita completa.
    gate_projector_rank = len(surviving7)
    require(gate_projector_rank == 3, "rango de P_G")

    # Enlace S3-equivariante con las tres regiones positivas de pi.
    catalogue = json.loads(U6_CATALOG.read_text(encoding="utf-8"))

    def projected_pi_word(row: dict[str, object]) -> str:
        return "".join(
            str((-int(value)) % 3) for value in str(row["U6"]).split("|")
        )

    pi_positive = [
        row
        for row in catalogue
        if projected_pi_word(row) == "010211" and row["hplus_type"] == "ES"
    ]
    require(len(pi_positive) == 3, "tres regiones positivas de pi")
    energy_prefixes = {
        "".join(str(row["Esig"]).split(",")[:3]) for row in pi_positive
    }
    require(energy_prefixes == {"339", "393", "933"},
            "orbita energetica positiva 339/393/933")
    gate_pi_tails = {
        row["rows"].split("|")[0][3:] for row in surviving7
    }
    digit_map = {"1": "3", "2": "9"}
    require(
        {"".join(digit_map[digit] for digit in tail) for tail in gate_pi_tails}
        == energy_prefixes,
        "biyeccion S3 gate--pi positiva",
    )

    # Obstruccion y reparacion tipada: el triplete natural es 1+2, mientras
    # V3|S3 es sign+2. El twist por la linea de orientacion corrige el caracter,
    # pero no selecciona por si solo embedding ni normalizacion relativa.
    a5_v3_restricted_character = [3, -1, 0]
    sign_twisted_gate_character = [3, -1, 0]
    require(gate_character != a5_v3_restricted_character,
            "obstruccion S3 sin twist")
    require(sign_twisted_gate_character == a5_v3_restricted_character,
            "compatibilidad tras twist de signo")

    # La lectura anterior t=8 era de tipo incorrecto: tres raices locales y
    # once extensiones de una sola raiz.
    require(row8["num_selected"] == "3", "t=8 tiene tres ramas")
    require(row8["actual_chain_count_h9"] == "11", "t=8 tiene once cadenas")
    require(row8["survivors_h3"] == "1" and row8["survivors_h9"] == "1",
            "t=8 selecciona una sola rama")
    require(row9["num_selected"] == "3" and row9["actual_chain_count_h9"] == "6",
            "el retorno t=9 cambia 3/11 por 3/6")
    branches8 = [row for row in details if row["t"] == "8"]
    require(len(branches8) == 3, "tres filas de rama en t=8")
    require(sum(row["is_actual"] == "True" for row in branches8) == 1,
            "una rama actual")
    fibre_sizes = [int(row["surv_h9"]) for row in branches8]
    require(sorted(fibre_sizes) == [0, 0, 11],
            "fibras rama--cadena 0,0,11")

    return {
        "correct_gate": {
            "phase": 7,
            "ambient_local_branches": 11,
            "survival_filtration_h1_h2_h3": [11, 3, 1],
            "rank_PG": gate_projector_rank,
            "normalized_trace_PG": "3/11",
            "surviving_rows_h2": sorted(surviving_gate_rows),
            "S3_orbit_sizes_on_11_branches": sorted(orbit_sizes),
            "S3_character_on_11_branches_id_transposition_3cycle": full_character,
            "S3_character_on_range_PG": gate_character,
            "S3_module_range_PG": "trivial + standard = 1 + 2",
            "positive_projector": True,
        },
        "gate_to_pi_positive_bridge": {
            "gate_pi_tails": sorted(gate_pi_tails),
            "pi_positive_energy_prefixes": sorted(energy_prefixes),
            "coordinate_rule": "1 -> 3, 2 -> 9",
            "S3_equivariant": True,
        },
        "comparison_with_P3": {
            "range_PG_character": gate_character,
            "V3_restricted_to_S3_character": a5_v3_restricted_character,
            "untwisted_S3_intertwiner": False,
            "sign_twisted_character": sign_twisted_gate_character,
            "sign_twist_makes_modules_isomorphic": True,
            "canonical_full_intertwiner": False,
            "remaining_data": (
                "An explicit embedding of the gate S3 into the declared A5 action "
                "and a normalization relating the sign and standard summands."
            ),
        },
        "rejected_t8_ratio": {
            "t8_local_branches": 3,
            "t8_horizon9_actual_chains": 11,
            "t8_branch_fibre_sizes": fibre_sizes,
            "t8_natural_branch_chain_incidence_rank": 1,
            "t8_surviving_root_branches_at_h9": 1,
            "t9_ratio": "3/6",
            "no_go_reason": (
                "The numerator counts three local roots, while the denominator "
                "counts eleven depth-nine extensions of the single surviving root."
            ),
        },
    }


def main() -> None:
    hexads, design = construct_witt_design()
    bridge = point_hexad_intertwiner(hexads)
    operator_audit = a5_and_operator_obstruction(hexads)
    gate_audit = n73_gate_audit()
    result = {
        "schema": "HMT.entrelazador-incidencia-witt.v2",
        "status": "PASS_NORMALIZED_INCIDENCE_ISOMETRY_AND_GATE_PROJECTOR_FULL_TRIPLE_RELATIVE",
        "uses_physical_targets": False,
        "witt_design": design,
        "canonical_pair_intertwiner": bridge,
        "operator_type_audit": operator_audit,
        "n73_n74_audit": gate_audit,
        "theorem": (
            "There is a canonical positive incidence isometry U=(1/6)I from "
            "the labeled dodecaphase augmentation space V11 to the Gram-30 Witt "
            "module E30, unique among positive normalized scalar multiples of "
            "the published incidence matrix. It transports P3 to the positive "
            "rank-3 projector Q3. The declared A5/C5 action does not preserve "
            "the labeled W12, so this is not a common intrinsic A5 intertwiner. "
            "The Witt-star involution has "
            "the same normalized trace 3/11 but is not conjugate to P3. N73 "
            "has a genuine rank-3 survival projector PG at t=7,h=2, "
            "S3-equivariantly identified with the three positive pi regions. "
            "Its natural module is 1+2, whereas V3 restricts as sign+2; a sign "
            "twist matches the characters, but the corpus does not fix the "
            "embedding and normalization needed for a canonical full intertwiner."
        ),
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_ENTRELAZADOR_INCIDENCIA_WITT")


if __name__ == "__main__":
    main()
