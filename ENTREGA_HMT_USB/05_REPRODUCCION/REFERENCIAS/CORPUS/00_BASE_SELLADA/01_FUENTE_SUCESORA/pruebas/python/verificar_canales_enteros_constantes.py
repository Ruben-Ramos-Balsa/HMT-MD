#!/usr/bin/env python3
"""Certifica identidades tipadas 729/271/315/161 y el selector orbital.

La prueba no usa cifras decimales de pi, e o phi. Evalua reglas de composicion
declaradas sobre observables APP, realiza 135/270/271/315 como cardinales de
conjuntos relativamente a la particion/origen de fase publicados y recupera
tres orbitas D3 bajo predicados y calibres publicados.
No demuestra que TPK fuerce las reglas, los predicados o el diccionario que
asocia los tipos enteros con las orbitas.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
from math import factorial
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_CERT = ROOT / "certificados/estructura_app.json"
CATALOGUE = ROOT / "datos/TPK_U_catalog_468.json"
OUTPUT = ROOT / "certificados/canales_enteros_constantes.json"

R = (2, 0, 1, 4, 5, 3)
S = (3, 4, 5, 0, 1, 2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("CANALES ENTEROS FAIL: " + message)


def parse_u6(text: str) -> tuple[int, ...]:
    result = tuple(int(item) for item in text.split("|"))
    require(len(result) == 6, "U6 mal tipado")
    return result


def psi(u6: tuple[int, ...]) -> str:
    return "".join(str((-entry) % 3) for entry in u6)


def permute(values: tuple[object, ...], permutation: tuple[int, ...]) -> tuple[object, ...]:
    return tuple(values[index] for index in permutation)


def permute_word(word: str, permutation: tuple[int, ...]) -> str:
    return "".join(word[index] for index in permutation)


def orbit(word: str) -> tuple[str, ...]:
    result: set[str] = set()
    current = word
    for _ in range(3):
        result.add(current)
        result.add(permute_word(current, S))
        current = permute_word(current, R)
    return tuple(sorted(result))


def coordinate_orbit(values: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    result: set[tuple[int, ...]] = set()
    current = values
    for _ in range(3):
        result.add(current)
        result.add(permute(current, S))
        current = permute(current, R)
    return tuple(sorted(result))


def phase_add_three(value: int) -> int:
    return ((value + 2) % 9) + 1


def phase_negate(value: int) -> int:
    residue = (-value) % 9
    return 9 if residue == 0 else residue


def pair_image(pair: tuple[int, int], function: object) -> tuple[int, int]:
    mapped = tuple(sorted((function(pair[0]), function(pair[1]))))  # type: ignore[operator]
    return mapped


def pair_orbit(pair: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    pending = [pair]
    result: set[tuple[int, int]] = set()
    while pending:
        current = pending.pop()
        if current in result:
            continue
        result.add(current)
        pending.append(pair_image(current, phase_add_three))
        pending.append(pair_image(current, phase_negate))
    return tuple(sorted(result))


def census(word: str) -> tuple[int, int, int]:
    return word.count("0"), word.count("1"), word.count("2")


def dr9(value: int) -> int:
    require(value > 0, "dr9 sólo se usa sobre enteros positivos")
    return 9 if value % 9 == 0 else value % 9


def q9_sharp(value: int) -> int:
    return (value - dr9(value)) // 9


def phase_sign(tick: int) -> int:
    phase = (tick - 1) % 9 + 1
    if phase in (1, 4, 7):
        return 1
    if phase in (2, 5, 8):
        return -1
    return 0


def main() -> None:
    app = json.loads(APP_CERT.read_text(encoding="utf-8"))
    sigma_total = int(app["table_sums"]["Sigma"])
    pi_total = int(app["table_sums"]["Pi"])
    additive_quotient = int(app["quotient_sums"]["additive"])
    central = app["central_block"]
    require(central == [[7, 2], [2, 7]], "bloque central APP")

    delta = pi_total - sigma_total
    kappa = delta // 2
    shell = additive_quotient
    theta = 5 * kappa
    c_alpha = kappa * kappa
    c_e = 2 * theta + 1
    c_pi = 2 * theta + shell
    c_phi = theta + kappa - 1

    require((sigma_total, pi_total, delta) == (405, 459, 54), "defecto APP")
    require((shell, kappa, theta) == (45, 27, 135), "invariantes centrales")
    require((c_alpha, c_e, c_pi, c_phi) == (729, 271, 315, 161), "canales")
    require(c_e == 5 * delta + 1 == 10 * 27 + 1, "formas de 271")
    require(c_pi == 5 * delta + shell == 7 * shell, "formas de 315")
    require(c_phi == 3 * delta - 1, "forma de 161")
    require(c_e == 4 * delta + (delta + 1), "rama expansiva")
    require(c_phi == 4 * delta - (delta + 1), "rama equilibrada")
    require(1000 == c_alpha + c_e == 729 + 243 + 27 + 1, "completacion 1000")
    require(c_pi + c_e + c_phi - 3 == 744 == c_alpha + 15, "cierre de canales")

    # Las concatenaciones 72/27 y 77/22 proceden de B_c, no de cifras de
    # constantes. Se conservan como palabras ordenadas de sus entradas.
    word_72 = 10 * central[0][0] + central[0][1]
    word_27 = 10 * central[1][0] + central[1][1]
    word_77 = 10 * central[0][0] + central[1][1]
    word_22 = 10 * central[0][1] + central[1][0]
    require((word_72, word_27, word_77, word_22) == (72, 27, 77, 22), "palabras centrales")
    require(word_72 + word_27 == word_77 + word_22 == 99, "borde 99")
    require(word_72 - word_27 == shell, "determinante 45")
    require(word_77 - word_22 == delta + 1, "defecto apuntado 55")
    require(c_alpha == 10 * word_72 + 9, "canal 729 desde 72|9")
    require(c_e == 10 * word_27 + 1, "canal 271 desde 27|1")

    # Paridad visible y paridad de acarreo. Como 9=1 mod 2, la paridad del
    # entero sin reducir es la suma de ambos bits. Se censan las 81 celdas en
    # las dos hojas APP para registrar que suma y producto distribuyen esos
    # bits de manera diferente.
    parity_tables: dict[str, Counter[tuple[int, int]]] = {}
    for name, operation in (
        ("sum", lambda i, j: i + j),
        ("product", lambda i, j: i * j),
    ):
        table: Counter[tuple[int, int]] = Counter()
        for i in range(1, 10):
            for j in range(1, 10):
                raw = operation(i, j)
                visible_bit = dr9(raw) % 2
                carry_bit = q9_sharp(raw) % 2
                require(raw % 2 == (visible_bit + carry_bit) % 2,
                        "factorización de paridad visible--acarreo")
                table[visible_bit, carry_bit] += 1
        parity_tables[name] = table
    require(
        parity_tables["sum"]
        == Counter({(0, 0): 16, (0, 1): 20, (1, 0): 20, (1, 1): 25}),
        "tabla de paridad aditiva",
    )
    require(
        parity_tables["product"]
        == Counter({(0, 0): 25, (0, 1): 5, (1, 0): 20, (1, 1): 31}),
        "tabla de paridad multiplicativa",
    )

    # Semicorona de fase relativa a la particion de movimiento y al origen de
    # la ventana publicados. El producto cartesiano se construye aqui; este
    # certificado no ejecuta aun la dinamica cronologica de TPK-full.
    phase_clock = tuple(range(1, 10))
    h_plus = tuple(t for t in phase_clock if phase_sign(t) == 1)
    h_minus = tuple(t for t in phase_clock if phase_sign(t) == -1)
    h_zero = tuple(t for t in phase_clock if phase_sign(t) == 0)
    h_active = tuple(sorted(h_plus + h_minus))
    phase_octet = tuple(range(1, 9))
    phase_return = 9
    pairs_active = tuple(combinations(h_active, 2))
    theta_phase = {(tick, pair) for tick in phase_clock for pair in pairs_active}
    f6_phase = {(tick, pair) for tick in h_active for pair in pairs_active}
    f8_phase = {(tick, pair) for tick in phase_octet for pair in pairs_active}
    boundary_phase = {
        (state, orientation) for state in theta_phase for orientation in (-1, 1)
    }
    pointed_phase = set(boundary_phase) | {"infinity"}
    lateral_phase = {(tick, pair) for tick in h_zero for pair in pairs_active}
    closure_phase = set(boundary_phase) | lateral_phase
    require(h_plus == (1, 4, 7), "fases aditivas")
    require(h_minus == (2, 5, 8), "fases multiplicativas")
    require(h_zero == (3, 6, 9), "fases neutras")
    require(h_active == (1, 2, 4, 5, 7, 8), "seis fases activas")
    require(set(h_active) <= set(phase_octet) <= set(phase_clock),
            "cadena 6-8-9 de fase")
    require(phase_clock[-1] == phase_return, "tick de retorno")
    require(len(pairs_active) == 15, "pares de fases activas")
    require((len(f6_phase), len(f8_phase), len(theta_phase)) == (90, 120, 135),
            "semicorona de fase 90-120-135")
    require(len(boundary_phase) == 270 and len(pointed_phase) == 271,
            "retorno orientado de fase")
    require(lateral_phase == theta_phase - f6_phase and len(lateral_phase) == 45,
            "frontera lateral neutral")
    require(len(closure_phase) == 315, "cierre lateral de fase")
    unmarked_chain_isomorphisms = factorial(6) * factorial(2)
    require(unmarked_chain_isomorphisms == 1440, "calibres cadena 6-8-9")

    # Modelo coordinado de la semicorona sobre una inclusion 6->8. La
    # existencia y unicidad de O_H para la hexada publicada se demuestra en
    # el capitulo W12->W24; este script certifica el tipo conjuntista y sus
    # cardinales, no reconstruye de nuevo el alineamiento de Golay.
    h = tuple(range(6))
    o = tuple(range(8))
    pairs_h = tuple(combinations(h, 2))
    o_hat = o + ("return",)
    theta_set = {(point, pair) for point in o_hat for pair in pairs_h}
    f6 = {(point, pair) for point in h for pair in pairs_h}
    f8 = {(point, pair) for point in o for pair in pairs_h}
    boundary = {(state, orientation) for state in theta_set for orientation in (-1, 1)}
    pointed_return = set(boundary) | {"infinity"}
    closure_pi = set(boundary) | (theta_set - f6)
    require(len(pairs_h) == 15, "pares de una hexada")
    require(len(f6) == 90 and len(f8) == 120, "interfaz 90/120")
    require(f6 <= f8 <= theta_set, "cadena de inclusiones")
    require(len(theta_set) == theta == 135, "semicorona")
    require(len(boundary) == 270, "doble orientacion")
    require(len(pointed_return) == c_e == 271, "retorno apuntado")
    require(len(theta_set - f6) == shell == 45, "frontera lateral")
    require(len(closure_pi) == c_pi == 315, "cierre orientado mas lateral")

    raw = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    require(isinstance(raw, list) and len(raw) == 468, "catalogo 468")
    by_u6: dict[tuple[int, ...], dict[str, object]] = {}
    fibers: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for item in raw:
        require(isinstance(item, dict), "fila de catalogo")
        u6 = parse_u6(str(item["U6"]))
        require(u6 not in by_u6, "U6 repetido")
        row = dict(item)
        row["u6"] = u6
        row["word"] = psi(u6)
        by_u6[u6] = row
        fibers[str(row["word"])].append(row)
    require(len(fibers) == 243, "imagen visible 243")

    # La accion D3 debe cerrar antes de aplicar predicados de seleccion.
    for u6, row in by_u6.items():
        for permutation in (R, S):
            image = permute(u6, permutation)
            require(image in by_u6, "D3 no cierra en U6")
            require(int(by_u6[image]["count"]) == int(row["count"]), "D3 no preserva masa")
            require(psi(image) == permute_word(str(row["word"]), permutation), "Psi no equivariante")

    orbits = sorted({orbit(word) for word in fibers})
    require(Counter(map(len, orbits)) == Counter({6: 38, 3: 5}), "orbitas D3")

    def fibre_size(word: str) -> int:
        return len(fibers[word])

    def seed_mass(word: str) -> int:
        return sum(int(row["count"]) for row in fibers[word])

    def diag_support(words: tuple[str, ...]) -> set[int]:
        return {int(row["diag_c"]) for word in words for row in fibers[word]}

    pi_candidates = [
        words for words in orbits
        if len(words) == 6
        and all(
            fibre_size(word) == 5
            and seed_mass(word) == 1008
            and sorted(int(row["count"]) for row in fibers[word]) == [144, 144, 144, 144, 432]
            for word in words
        )
    ]
    require(len(pi_candidates) == 1, "selector orbital de pi")
    orbit_pi = pi_candidates[0]
    require({census(word) for word in orbit_pi} == {(2, 3, 1)}, "censo de pi")

    radical_singletons = [
        words for words in orbits
        if len(words) == 6
        and all(fibre_size(word) == 1 and seed_mass(word) == 144 for word in words)
        and diag_support(words) == {0, 3, 6}
    ]
    require(len(radical_singletons) == 6, "sector singleton radical")
    e_candidates = [words for words in radical_singletons if {census(word) for word in words} == {(2, 3, 1)}]
    phi_candidates = [words for words in radical_singletons if {census(word) for word in words} == {(2, 2, 2)}]
    require(len(e_candidates) == len(phi_candidates) == 1, "selectores de e y phi")
    orbit_e, orbit_phi = e_candidates[0], phi_candidates[0]

    def zero_support(word: str) -> tuple[int, ...]:
        return tuple(index + 1 for index, symbol in enumerate(word) if symbol == "0")

    zero_support_pi = Counter(zero_support(word) for word in orbit_pi)
    zero_support_e = Counter(zero_support(word) for word in orbit_e)
    zero_support_phi = Counter(zero_support(word) for word in orbit_phi)
    intrahalf_pairs = {(1, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 6)}
    antipodal_pairs = {(1, 6), (2, 5), (3, 4)}
    require(set(zero_support_pi) == intrahalf_pairs and set(zero_support_pi.values()) == {1},
            "codificador c0 de pi")
    require(set(zero_support_e) == antipodal_pairs and set(zero_support_e.values()) == {2},
            "codificador c0 de e")
    require(zero_support_phi == zero_support_pi, "codificador c0 de phi")

    # No-go: un selector producto->pares que dependa solo de Esig no puede
    # ser total y D3-equivariante. La fuente tiene dos puntos globalmente
    # fijos; el blanco P2(Hact) no tiene ninguno.
    product_signatures = {
        tuple(int(value) for value in str(row["Esig"]).split(",")) for row in raw
    }
    require(len(product_signatures) == 26, "firmas producto Esig")
    require(all(len(signature) == 6 for signature in product_signatures), "tipo Esig")
    require(all(
        permute(signature, generator) in product_signatures
        for signature in product_signatures for generator in (R, S)
    ), "cierre D3 de Esig")
    product_orbits = {coordinate_orbit(signature) for signature in product_signatures}
    require(Counter(map(len, product_orbits)) == Counter({6: 3, 3: 2, 1: 2}),
            "orbitas D3 de Esig")
    fixed_product = {
        signature for signature in product_signatures
        if permute(signature, R) == signature and permute(signature, S) == signature
    }
    require(fixed_product == {(0, 0, 0, 0, 0, 0), (5, 5, 5, 5, 5, 5)},
            "puntos fijos Esig")
    phase_pair_orbits = {pair_orbit(pair) for pair in pairs_active}
    require(Counter(map(len, phase_pair_orbits)) == Counter({6: 1, 3: 3}),
            "orbitas D3 sobre pares de fase")
    fixed_pairs = {
        pair for pair in pairs_active
        if pair_image(pair, phase_add_three) == pair
        and pair_image(pair, phase_negate) == pair
    }
    require(not fixed_pairs, "el blanco de pares tendria un punto fijo")

    def orient(words: tuple[str, ...]) -> list[str]:
        return [
            word for word in words
            if any(int(row["diag_c"]) == 6 and str(row["hplus_type"]) == "ES" for row in fibers[word])
        ]

    word_pi, word_e, word_phi = orient(orbit_pi), orient(orbit_e), orient(orbit_phi)
    require((word_pi, word_e, word_phi) == (["010211"], ["201101"], ["121200"]),
            "gauge orientado")

    # Ablación exacta: suma, residuo nonádico y paridad de entradas no
    # separan por sí solos e de tres de las cinco regiones de pi.
    def elementary_signature(row: dict[str, object]) -> tuple[int, int, int]:
        u6 = tuple(int(value) for value in row["u6"])
        return sum(u6), sum(u6) % 9, sum(value % 2 == 0 for value in u6)

    oriented_e_rows = [
        row for row in fibers[word_e[0]]
        if int(row["diag_c"]) == 6 and str(row["hplus_type"]) == "ES"
    ]
    oriented_pi_rows = [
        row for row in fibers[word_pi[0]]
        if int(row["diag_c"]) == 6 and str(row["hplus_type"]) == "ES"
    ]
    require(len(oriented_e_rows) == 1 and len(oriented_pi_rows) == 3,
            "testigos de ablación elemental")
    elementary_collision = elementary_signature(oriented_e_rows[0])
    require(elementary_collision == (3316, 4, 4), "firma elemental común")
    require(
        all(elementary_signature(row) == elementary_collision for row in oriented_pi_rows),
        "la colisión elemental e/pi no se reproduce",
    )

    result = {
        "schema": "HMT.canales-enteros-constantes.v3",
        "status": "PASS_EXACT_RELATIVE_PHASE_SEMICORONA_ORBIT_CLASSIFICATION_AND_D3_NO_GO",
        "APP_invariants": {
            "Sigma_total": sigma_total,
            "Pi_total": pi_total,
            "Delta_product_minus_sum": delta,
            "S_1_to_9": shell,
            "kappa": kappa,
            "Theta": theta,
            "central_words": [word_72, word_27, word_77, word_22],
        },
        "parity_carry_factorization": {
            "identity": "raw_parity = visible_dr9_parity + lifted_carry_parity mod 2",
            "sum_counts_by_visible_carry_bits": {
                f"{visible}{carry}": parity_tables["sum"][visible, carry]
                for visible in (0, 1) for carry in (0, 1)
            },
            "product_counts_by_visible_carry_bits": {
                f"{visible}{carry}": parity_tables["product"][visible, carry]
                for visible in (0, 1) for carry in (0, 1)
            },
            "physical_scope": "an exact Z/2 grading of APP readings, not a derivation of Bose/Fermi exchange statistics",
        },
        "integer_channels": {
            "alpha": c_alpha,
            "e": c_e,
            "pi": c_pi,
            "phi": c_phi,
            "completion": "1000=729+271",
        },
        "phase_semicorona": {
            "origin_status": "relative to the published phase partition, origin 1 and terminal return tick 9; origin changes act by C9 translation",
            "dynamical_scope": "the certificate constructs the finite phase product; it does not execute or prove descent from the full chronological TPK state",
            "H_plus": list(h_plus),
            "H_minus": list(h_minus),
            "H_zero": list(h_zero),
            "H_active": list(h_active),
            "phase_octet": list(phase_octet),
            "return_tick": phase_return,
            "P2_H_active": len(pairs_active),
            "F6": len(f6_phase),
            "F8": len(f8_phase),
            "Theta": len(theta_phase),
            "oriented_boundary": len(boundary_phase),
            "pointed_return": len(pointed_phase),
            "neutral_lateral_boundary": len(lateral_phase),
            "closure": len(closure_phase),
            "unmarked_isomorphisms_to_any_fixed_6_in_8_in_9_chain": unmarked_chain_isomorphisms,
        },
        "initial_zero_support_coder": {
            "definition": "c0(w)={positions j with w_j=0}, on the stratum with exactly two zeros",
            "pi_pairs": [list(pair) for pair in sorted(zero_support_pi)],
            "pi_multiplicities": {str(pair): count for pair, count in sorted(zero_support_pi.items())},
            "e_pairs": [list(pair) for pair in sorted(zero_support_e)],
            "e_multiplicities": {str(pair): count for pair, count in sorted(zero_support_e.items())},
            "phi_equals_pi_support_orbit": zero_support_phi == zero_support_pi,
            "scope": "intrinsic D3-equivariant coder at w6 only; not a construction of the deep coders c_k or of a Witt incidence map",
        },
        "product_to_phase_pair_no_go": {
            "source_orbit_sizes": sorted(map(len, product_orbits)),
            "source_fixed_points": [list(signature) for signature in sorted(fixed_product)],
            "target_orbit_sizes": sorted(map(len, phase_pair_orbits)),
            "target_fixed_points": [list(pair) for pair in sorted(fixed_pairs)],
            "conclusion": "no total D3-equivariant function Esig -> P2(H_active) exists; a deep coder must use enriched ledger/phase, a relation, an enlarged target or a gauge",
        },
        "steiner_semicorona": {
            "model_status": "coordinate representative of the separately proved dodecad-relative Steiner hexad-to-octad lift",
            "P2_H": len(pairs_h),
            "F6": len(f6),
            "F8": len(f8),
            "Theta_H": len(theta_set),
            "oriented_boundary": len(boundary),
            "pointed_return_E_H": len(pointed_return),
            "lateral_boundary": len(theta_set - f6),
            "pi_closure": len(closure_pi),
        },
        "finite_selector": {
            "D3_orbits": len(orbits),
            "pi_orbit": list(orbit_pi),
            "e_orbit": list(orbit_e),
            "phi_orbit": list(orbit_phi),
            "oriented_words": {
                "pi": word_pi[0],
                "e": word_e[0],
                "phi": word_phi[0],
            },
            "uses_decimal_reader": False,
        },
        "typed_correspondence": {
            "271": "pointed two-way return; associated with the e orbit only relative to the declared type dictionary, predicates and orientation gauge",
            "315": "two-way boundary plus the 45-state lateral closure; associated with the pi orbit only relative to the declared type dictionary, predicates and orientation gauge",
            "161": "exact integer identity only; no set-theoretic realization or induced map to the phi orbit is constructed here",
            "729": "cubic core; alpha is read only after the dodecaphase closure",
        },
        "ablation": {
            "elementary_signature": {
                "sum_U6": elementary_collision[0],
                "sum_mod_9": elementary_collision[1],
                "even_entries": elementary_collision[2],
            },
            "e_rows": len(oriented_e_rows),
            "pi_rows_with_same_signature": len(oriented_pi_rows),
            "conclusion": (
                "sum, mod 9 and entry parity do not distinguish the e emission "
                "from three pi regions; fibre/orbit structure is necessary"
            ),
        },
        "logical_scope": {
            "proved": (
                "Given the four declared composition rules, the published APP totals and central block evaluate exactly to 729, 271, 315 and 161. "
                "The published TPK phase partition and phase origin realize 90, 120, 135, 270, 271 and 315 as a finite phase semicorona; the dodecad-relative Steiner lift gives a second realization with the same cardinal profile. "
                "Independently, the declared finite D3 predicates and gauges classify unique pi/e/phi catalogue orbits without decimal data."
            ),
            "relative_step": (
                "Identifying the pointed-return type with the e orbit and the boundary-closure type with the pi orbit uses the stated type-preserving channel dictionary."
            ),
            "not_proved": (
                "The script does not execute the chronological TPK-full state or construct an incidence map from the phase 6-in-8-in-9 chain to the dodecad-relative Steiner chain, nor does it prove that TPK forces the four composition rules, the D3 predicates, the orientation gauge or the type dictionary. "
                "It constructs no set-theoretic realization of 161 and no infinite target-free decimal emitter. Consequently the 271-to-e and 315-to-pi associations remain relative rather than upstream target-free readers."
            ),
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS_CANALES_ENTEROS_CONSTANTES")


if __name__ == "__main__":
    main()
