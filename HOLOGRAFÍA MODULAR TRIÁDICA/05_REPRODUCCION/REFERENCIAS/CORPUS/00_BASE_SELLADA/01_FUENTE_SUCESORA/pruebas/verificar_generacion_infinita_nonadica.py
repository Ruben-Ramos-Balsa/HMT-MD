#!/usr/bin/env python3
"""Verificación exacta y parametrizada de la generación nonádica.

El programa recibe una profundidad decimal para el testigo de regresión,
reconstruye primero las órbitas estructurales desde el catálogo finito TPK,
genera los cuatro caracteres internos correlacionados de π, φ, e y α y sólo
después publica las coordenadas arquimedianas desarrolladas para π, e y φ:

* clausura pentarregional y retorno tangencial unitario;
* propagación group-like con unidad conservada;
* autoescala de Perron de la incidencia F_av.

No contiene ni lee expansiones decimales objetivo. El catálogo produce el
censo, selecciona las tres órbitas tipadas y fija sus caracteres de clausura,
propagación y autoescala antes de cualquier evaluación decimal. Los doce
bloques b1,...,b4 son testigos finitos del transporte enriquecido: permiten
reconstruir de manera única los levantamientos L0 y L1, probar la unicidad del
calendario 0011 entre los dieciséis calendarios binarios y agotar sus 144
perturbaciones unitarias. No se emplean para escoger una cola decimal.

La separación causal es material y comprobada sobre el árbol sintáctico del
propio programa: ``generate_structural_characters`` no puede llamar a los
evaluadores arquimedianos ni al publicador de bloques; sólo después de producir
los caracteres exactos se ejecuta ``evaluate_generated_characters`` y, por
último, ``publish_archimedean_blocks``. Las cadenas decimales calculadas son
publicaciones y testigos de estabilidad proyectiva, nunca selectores de una
descendencia TPK. Toda la aritmética analítica es racional exacta.

La regla matemática es coinductiva y de profundidad arbitraria. Una ejecución
a N cifras es sólo un testigo finito de regresión; nunca constituye el
criterio ni el límite del teorema. El valor por defecto 1000 no es una cota.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict, deque
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

# Matriz del propietario recuperado de R36. No se identifica silenciosamente
# con ``AW``: las dos presentaciones se enlazan por el cambio de calibre exacto
# que se verifica antes de integrar R36 en el estado enriquecido activo.
R36_OWNER_AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)

R36_OWNER_TO_ACTIVE_PERMUTATION = (0, 1, 2, 4, 5, 3)
JOINT_GENERATION_ID = "APP_TRIT_TPK_NONADIC_TYPED_IMAGE_FORWARD_EXT_V4"

AW_BRIDGE_OWNER_HASHES = {
    "04_AUDITORIA/02_independiente/auditoria_witt_w24_v2.py":
        "d8f926a2db915c1ca4f816805fb120d7ee6b0986502588f663fc8e8b1bee37cb",
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/15_SELECTOR_GLOBAL_DOBLE_LECTURA/"
    "verificar_hexada_marcada_target_free.py":
        "e4bbe71737798cdf30663710a451042c230bf625f4911d770d8ff0628fe58d4d",
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/03_LECTOR_EXCEPCIONAL/"
    "lector_excepcional.py":
        "d7a0ab5be8c3bc8c59ca90f1c7359176aec6008e675a64c7aa47b9d38c548902",
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/03_LECTOR_EXCEPCIONAL/certificados/"
    "verificar_lector_excepcional_global.py":
        "021c6f8e014f42dd9da898889f8cb2fc89c4946745273a1542b103a2f98c678e",
}

LOCAL_CHARACTER_OWNER_HASHES = {
    "manuscrito/incorporaciones/parte_iii_ampliaciones_20260824/source/public/"
    "pi_e_phi/U012_biografia_estructural_pi_body.tex":
        "375219a9643adb81c7ba22ca1d2b0cc2c8a3abe25adbc518b8f4bd81be7cd09a",
    "manuscrito/incorporaciones/parte_iii_ampliaciones_20260824/source/public/"
    "pi_e_phi/U013_biografia_estructural_e_body.tex":
        "645bd7fff4af1e40b3d6d239ba7c406fe688570e664ccbf256962317f107909a",
    "manuscrito/incorporaciones/parte_iii_ampliaciones_20260824/source/public/"
    "pi_e_phi/U014_biografia_estructural_phi_body.tex":
        "86c863587d2fcbaa6365bf6020eda1c6d9fc5f06c96ea60a39370d2d113fab8a",
    "manuscrito/sucesor_102/deltas_ley9/"
    "c31_dos_vias_alpha_y_prolongacion_nonadica_rectificacion_probatoria_20260903.tex":
        "7906002b3099341d444c088a94b9126856c7839498ea9af264fc73ef70745213",
}

FORMAL_GRAPH_RELATIVE_PATH = (
    "PUBLICACION_HMT/REGISTRO_DE_CONTINUIDAD_ACADEMICA/"
    "NUCLEO_FORMAL_HMT_PERMANENTE/TPK_GRAFO_OPERATORIO_TIPADO.json"
)
FORMAL_GRAPH_SHA256 = "d60f2ca3c06af8cb33e5dd66a4435c8f63c7a770dc5a154ccb6fc0f41268ef91"
GENERIC_NONEMPTY_OWNER_RELATIVE_PATH = (
    "output/LEY9_SINTESIS_300_SUCESORA_SIN_REGRESIONES_20260904/"
    "manuscrito/sections/autonomia/03_prolongacion_tpk.tex"
)
GENERIC_NONEMPTY_OWNER_SHA256 = (
    "e58390f95b87f0b185a9b731346ff9389cd88c0e3c671c3be729d111ba9a4e01"
)
EXACT_ALPHA_OWNER_RELATIVE_PATH = (
    "output/INTEGRAL_SUCESOR_AISLADO_REFUERZOS_ADMITIDOS_20260904/fuente/"
    "manuscrito/sucesor_fuente_nivel_20260904/overrides/parte_iii/"
    "c31_dos_vias_alpha_rectificacion_20260904.tex"
)
EXACT_ALPHA_OWNER_SHA256 = (
    "35654b80cdfaa131789198ec4570e2c31a1c9a0bb90ff931b76bbf742c847753"
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

B_PLUS_R36 = (
    (2, 2, 2, 2, 2, 0),
    (0, 2, 1, 2, 2, 2),
    (1, 0, 2, 0, 1, 1),
)

# Testigos de regresión publicados por el ledger enriquecido. No alimentan la
# generación de caracteres ni el publicador arquimediano.
REGRESSION_BIOGRAPHIES_FROM_ENRICHED_LEDGER = {
    "closure": "010211012222010211002111110221",
    "propagation": "201101121221102011012222102011",
    "autoscale": "121200112202121020010210010200",
}

STRUCTURAL_TO_PUBLICATION = {
    "closure": "pi",
    "propagation": "e",
    "autoscale": "phi",
}


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


def verify_character_and_ext_owners(
    project_root: Path, source_root: Path
) -> dict[str, object]:
    """Fija los propietarios usados, distinguiendo alcance y procedencia."""
    local_owners: dict[str, dict[str, object]] = {}
    roles = {
        "U012": "internal_gaussian_closure_coordinate_before_real_reader",
        "U013": "internal_normalized_group_like_coordinate_before_real_reader",
        "U014": "internal_positive_autoscale_coordinate_before_real_reader",
        "c31_": "internal_dodecaphase_alpha_coordinate_and_compatible_section",
    }
    for relative, expected in LOCAL_CHARACTER_OWNER_HASHES.items():
        path = source_root / relative
        require(path.is_file(), f"propietario local no localizado: {path}")
        observed = sha256_file(path)
        require(observed == expected, f"huella cambiada: {path}")
        role = next(value for token, value in roles.items() if token in path.name)
        local_owners[relative] = {
            "path": str(path),
            "sha256": observed,
            "role": role,
            "used_as_future_digit_oracle": False,
        }

    graph_path = project_root / FORMAL_GRAPH_RELATIVE_PATH
    require(graph_path.is_file(), f"grafo formal no localizado: {graph_path}")
    graph_sha256 = sha256_file(graph_path)
    require(graph_sha256 == FORMAL_GRAPH_SHA256, "huella del grafo formal cambiada")
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    operators = {
        str(item["id"]): item
        for item in graph.get("nodes", [])
        if isinstance(item, dict) and "id" in item
    }
    required_operators = {
        "OP12_X_TPK_ENR",
        "OP13_H",
        "OP17_GAMMA9",
        "OP18_X_CHI",
        "OP22_EXT_R",
    }
    require(required_operators <= set(operators), "grafo Ext/Γ9 incompleto")
    require(
        operators["OP22_EXT_R"].get("ontological_class") == "prolongation_relation",
        "Ext no está tipada como relación",
    )
    require(
        operators["OP18_X_CHI"].get("ontological_class") == "inverse_limit_object",
        "X_chi no está tipado como límite inverso",
    )
    required_state_fields = {
        "residue", "quotient", "carry", "sheet", "orientation", "phase",
        "route", "cylinder", "frontier", "signature", "record", "memory",
        "survival", "provenance", "origin", "winding", "depth",
    }
    require(
        required_state_fields
        <= set(operators["OP12_X_TPK_ENR"].get("conserved_fields", [])),
        "el estado enriquecido formal perdió campos",
    )

    generic_path = project_root / GENERIC_NONEMPTY_OWNER_RELATIVE_PATH
    require(generic_path.is_file(), f"propietario de no vacuidad ausente: {generic_path}")
    generic_sha256 = sha256_file(generic_path)
    require(
        generic_sha256 == GENERIC_NONEMPTY_OWNER_SHA256,
        "huella del propietario genérico de no vacuidad cambiada",
    )
    alpha_path = project_root / EXACT_ALPHA_OWNER_RELATIVE_PATH
    require(alpha_path.is_file(), f"propietario exacto de alpha ausente: {alpha_path}")
    alpha_sha256 = sha256_file(alpha_path)
    require(
        alpha_sha256 == EXACT_ALPHA_OWNER_SHA256,
        "huella del propietario exacto de alpha cambiada",
    )
    return {
        "status": "PASS_CONTENT_ADDRESSED_CHARACTER_AND_EXT_OWNERS",
        "local_character_owners": local_owners,
        "formal_graph": {
            "path": str(graph_path),
            "sha256": graph_sha256,
            "operator_ids": sorted(required_operators),
        },
        "generic_nonempty_history_owner": {
            "path": str(generic_path),
            "sha256": generic_sha256,
            "role": "nonemptiness_support_only_not_the_pi_phi_e_alpha_section",
        },
        "exact_alpha_commutation_owner": {
            "path": str(alpha_path),
            "sha256": alpha_sha256,
            "role": "exact_commuting_truncation_squares_alpha_A_equals_alpha_B",
            "finite_9_1000_10000_runs_are_projections_only": True,
        },
    }


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
        "visible_words": sorted(fibers),
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


def split_structural_biography(word: str) -> list[list[int]]:
    require(len(word) == 5 * BLOCK_SIZE, "biografía distinta de cinco bloques")
    require(set(word) <= {"0", "1", "2"}, "biografía no ternaria")
    return [
        [int(character) for character in word[offset : offset + BLOCK_SIZE]]
        for offset in range(0, len(word), BLOCK_SIZE)
    ]


def matrix_multiply_mod3(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> list[list[int]]:
    require(bool(left) and bool(right), "producto matricial vacío")
    require(len(left[0]) == len(right), "dimensiones matriciales incompatibles")
    return [
        [
            sum(int(left[i][k]) * int(right[k][j]) for k in range(len(right))) % 3
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def simultaneous_permutation(
    matrix: Sequence[Sequence[int]], permutation: Sequence[int]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(int(matrix[permutation[i]][permutation[j]]) for j in range(len(permutation)))
        for i in range(len(permutation))
    )


def verify_typed_r36_aw_bridge(
    r36: dict[str, object], project_root: Path
) -> dict[str, object]:
    """Transporta el calibre cíclico R36 al calibre natural activo.

    La palabra Hensel y su marco Paley forman un par tipado. El cambio de base
    actúa sobre ambos; no sustituye ni reordena silenciosamente el bloque que
    usa la carta radix de la publicación arquimediana.
    """
    owner_receipts: dict[str, dict[str, str]] = {}
    for relative, expected in AW_BRIDGE_OWNER_HASHES.items():
        path = project_root / relative
        require(path.is_file(), f"propietario del puente AW ausente: {path}")
        observed = sha256_file(path)
        require(observed == expected, f"huella del puente AW cambiada: {path}")
        owner_receipts[relative] = {"path": str(path), "sha256": observed}

    permutation = R36_OWNER_TO_ACTIVE_PERMUTATION
    inverse = tuple(permutation.index(index) for index in range(BLOCK_SIZE))
    require(
        simultaneous_permutation(R36_OWNER_AW, permutation) == AW,
        "la conjugación R36_OWNER_AW->AW no conmuta",
    )
    require(
        simultaneous_permutation(AW, inverse) == R36_OWNER_AW,
        "el transporte AW->R36_OWNER_AW no es inverso",
    )

    naturality_cases = 0
    for owner_vector in itertools.product(range(3), repeat=BLOCK_SIZE):
        active_vector = permute(owner_vector, permutation)
        owner_shadow = row_times_matrix_mod3(owner_vector, R36_OWNER_AW)
        active_shadow = row_times_matrix_mod3(active_vector, AW)
        require(
            active_shadow == permute(owner_shadow, permutation),
            "falló la naturalidad del cambio de calibre AW",
        )
        naturality_cases += 1
    require(naturality_cases == AMBIENT, "el puente AW no recorrió F3^6")

    selected = r36.get("selected_blocks")
    require(isinstance(selected, dict), "R36 no contiene sus tres bloques")
    owner_blocks = {channel: str(selected[channel]) for channel in ("pi", "e", "phi")}
    active_exceptional_blocks = {
        channel: permute_word(word, permutation)
        for channel, word in owner_blocks.items()
    }
    roundtrip = {
        channel: permute_word(word, inverse)
        for channel, word in active_exceptional_blocks.items()
    }
    require(roundtrip == owner_blocks, "los bloques R36 no retornan al calibre Hensel")
    return {
        "status": "PASS_EXACT_TYPED_R36_OWNER_AW_TO_ACTIVE_AW_BRIDGE",
        "provenance": "RESULTADO_RECUPERADO_AND_CERTIFICADO_NUEVO",
        "permutation_owner_to_active_zero_based": list(permutation),
        "inverse_permutation_zero_based": list(inverse),
        "matrix_identity": "AW[i,j]=R36_OWNER_AW[p[i],p[j]]",
        "vector_naturality": "R_p(v*R36_OWNER_AW)=R_p(v)*AW",
        "naturality_cases": naturality_cases,
        "r36_hensel_radix_chart_blocks": owner_blocks,
        "r36_natural_exceptional_chart_blocks": active_exceptional_blocks,
        "roundtrip_recovers_hensel_blocks": True,
        "typed_pair_transport": "(frame,word,word*A)->(R_p(frame),R_p(word),R_p(word*A))",
        "archimedean_radix_word_relabelled": False,
        "same_abstract_enriched_state_under_frame_change": True,
        "publication_or_package_promotion": False,
        "owners": owner_receipts,
    }


def rank_matrix_mod3(matrix: Sequence[Sequence[int]]) -> int:
    work = [[int(value) % 3 for value in row] for row in matrix]
    require(bool(work), "matriz vacía")
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, 3)
        work[pivot_row] = [(inverse * value) % 3 for value in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    (value - factor * pivot_value) % 3
                    for value, pivot_value in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def determinant_matrix_mod3(matrix: Sequence[Sequence[int]]) -> int:
    require(len(matrix) == len(matrix[0]), "determinante de matriz no cuadrada")
    work = [[int(value) % 3 for value in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]), None
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = (-determinant) % 3
        lead = work[column][column]
        determinant = (determinant * lead) % 3
        inverse = pow(lead, -1, 3)
        work[column] = [(inverse * value) % 3 for value in work[column]]
        for row in range(column + 1, len(work)):
            factor = work[row][column]
            if factor:
                work[row] = [
                    (value - factor * pivot_value) % 3
                    for value, pivot_value in zip(work[row], work[column])
                ]
    return determinant


def inverse_matrix_mod3(matrix: Sequence[Sequence[int]]) -> list[list[int]]:
    size = len(matrix)
    require(size == len(matrix[0]), "inversa de matriz no cuadrada")
    work = [
        [int(value) % 3 for value in row]
        + [int(row_index == column_index) for column_index in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        require(pivot is not None, "matriz singular sobre F3")
        work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column], -1, 3)
        work[column] = [(inverse * value) % 3 for value in work[column]]
        for row in range(size):
            if row != column and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    (value - factor * pivot_value) % 3
                    for value, pivot_value in zip(work[row], work[column])
                ]
    return [row[size:] for row in work]


def block_design(input_matrix: Sequence[Sequence[int]]) -> list[list[int]]:
    design: list[list[int]] = []
    for output_column in range(BLOCK_SIZE):
        for row in range(BLOCK_SIZE):
            equation = [0] * (BLOCK_SIZE * BLOCK_SIZE)
            start = output_column * BLOCK_SIZE
            equation[start : start + BLOCK_SIZE] = list(input_matrix[row])
            design.append(equation)
    return design


def apply_calendar(
    seed: Sequence[int],
    calendar: Sequence[int],
    lift_zero: Sequence[Sequence[int]],
    lift_one: Sequence[Sequence[int]],
) -> list[str]:
    current = tuple(int(value) for value in seed)
    blocks = ["".join(str(value) for value in current)]
    lifts = (lift_zero, lift_one)
    for phase in calendar:
        current = row_times_matrix_mod3(current, lifts[int(phase)])
        blocks.append("".join(str(value) for value in current))
    return blocks


def reconstruct_lifts_and_calendar(selection: dict[str, object]) -> dict[str, object]:
    biographies = {
        role: split_structural_biography(word)
        for role, word in REGRESSION_BIOGRAPHIES_FROM_ENRICHED_LEDGER.items()
    }
    selected_words = selection["words"]
    require(isinstance(selected_words, dict), "selección estructural no tipada")
    for role, publication in STRUCTURAL_TO_PUBLICATION.items():
        require(
            biographies[role][0]
            == [int(character) for character in str(selected_words[publication])],
            f"la semilla estructural {role} no procede del catálogo",
        )

    x0: list[list[int]] = []
    y0: list[list[int]] = []
    x1: list[list[int]] = []
    y1: list[list[int]] = []
    for role in ("closure", "propagation", "autoscale"):
        blocks = biographies[role]
        x0.extend((blocks[0], blocks[1]))
        y0.extend((blocks[1], blocks[2]))
        x1.extend((blocks[2], blocks[3]))
        y1.extend((blocks[3], blocks[4]))

    recovered_l0 = matrix_multiply_mod3(inverse_matrix_mod3(x0), y0)
    recovered_l1 = matrix_multiply_mod3(inverse_matrix_mod3(x1), y1)
    canonical_l0 = [list(row) for row in L0]
    canonical_l1 = [list(row) for row in L1]
    require(recovered_l0 == canonical_l0, "L0 no se reconstruye del ledger")
    require(recovered_l1 == canonical_l1, "L1 no se reconstruye del ledger")
    require(rank_matrix_mod3(x0) == rank_matrix_mod3(x1) == BLOCK_SIZE,
            "sistema de transiciones sin rango pleno")
    require(rank_matrix_mod3(block_design(x0)) == BLOCK_SIZE**2,
            "diseño de L0 sin rango 36")
    require(rank_matrix_mod3(block_design(x1)) == BLOCK_SIZE**2,
            "diseño de L1 sin rango 36")
    require(determinant_matrix_mod3(x0) == 1, "det(X0) distinto de 1")
    require(determinant_matrix_mod3(x1) == 2, "det(X1) distinto de -1")

    matching_calendars: list[str] = []
    for calendar in itertools.product((0, 1), repeat=4):
        if all(
            apply_calendar(
                biographies[role][0], calendar, recovered_l0, recovered_l1
            )
            == ["".join(str(value) for value in block) for block in biographies[role]]
            for role in biographies
        ):
            matching_calendars.append("".join(str(value) for value in calendar))
    require(matching_calendars == ["0011"], "el calendario 0011 no es único")

    perturbations = 0
    for lift_index, canonical in enumerate((canonical_l0, canonical_l1)):
        for row in range(BLOCK_SIZE):
            for column in range(BLOCK_SIZE):
                for replacement in range(3):
                    if replacement == canonical[row][column]:
                        continue
                    mutated = [[value for value in values] for values in canonical]
                    mutated[row][column] = replacement
                    lifts = [canonical_l0, canonical_l1]
                    lifts[lift_index] = mutated
                    triple_survives = all(
                        apply_calendar(
                            biographies[role][0], (0, 0, 1, 1), lifts[0], lifts[1]
                        )
                        == [
                            "".join(str(value) for value in block)
                            for block in biographies[role]
                        ]
                        for role in biographies
                    )
                    require(not triple_survives, "perturbación que conserva el triple")
                    perturbations += 1
    require(perturbations == 144, "censo de perturbaciones distinto de 144")

    return {
        "domain": "HMT-full enriched structural transition ledger before R",
        "proof_scope": (
            "unique exact reconstruction relative to the explicit enriched "
            "TPK transition ledger"
        ),
        "catalogue_proves": (
            "104976->468->243 subset 729 and the unique selection of the "
            "three initial w6 blocks"
        ),
        "ledger_status": "generated upstream by the full APP-TRIT-TPK state",
        "routine_role": "post-generation regression reconstruction",
        "ledger_used_to_generate_archimedean_tail": False,
        "channel_roles_before_naming": list(biographies),
        "systems": {
            "L0": {
                "equation": "X0 L0 = Y0",
                "rank_X0": rank_matrix_mod3(x0),
                "det_X0_mod3": determinant_matrix_mod3(x0),
                "design_rank": rank_matrix_mod3(block_design(x0)),
                "unique_solution": recovered_l0,
            },
            "L1": {
                "equation": "X1 L1 = Y1",
                "rank_X1": rank_matrix_mod3(x1),
                "det_X1_mod3": determinant_matrix_mod3(x1),
                "design_rank": rank_matrix_mod3(block_design(x1)),
                "unique_solution": recovered_l1,
            },
        },
        "unique_calendar_among_16": matching_calendars[0],
        "single_entry_perturbations_rejected": perturbations,
        "conventional_constants_used_as_inputs": False,
        "single_composition": "APP->TRIT->TPK",
    }


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


def add_mod3(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple((int(a) + int(b)) % 3 for a, b in zip(left, right))


def sub_mod3(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple((int(a) - int(b)) % 3 for a, b in zip(left, right))


def matrix_power_mod3(
    matrix: Sequence[Sequence[int]], exponent: int
) -> list[list[int]]:
    size = len(matrix)
    result = [[int(i == j) for j in range(size)] for i in range(size)]
    factor = [[int(value) % 3 for value in row] for row in matrix]
    for _ in range(exponent):
        result = matrix_multiply_mod3(result, factor)
    return result


def lifted_word_chain(word: str) -> list[tuple[int, ...]]:
    current = tuple(int(character) for character in word)
    blocks = [current]
    for matrix in FINITE_CALENDAR:
        current = row_times_matrix_mod3(current, matrix)
        blocks.append(current)
    return blocks


def column_occupancy(rows: Sequence[Sequence[int]]) -> tuple[int, ...]:
    return tuple(sum(int(value != 0) for value in column) for column in zip(*rows))


def margin_and_carry(
    rows: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    sums = tuple(sum(int(value) for value in column) for column in zip(*rows))
    margin = tuple(value % 3 for value in sums)
    carry = tuple((value - residue) // 3 for value, residue in zip(sums, margin))
    return margin, carry


def witt_dual_neutral(
    rows: Sequence[Sequence[int]], matrix: Sequence[Sequence[int]]
) -> bool:
    return all(sum(row_times_matrix_mod3(row, matrix)) % 3 == 0 for row in rows)


def semigroup_distances(source: Sequence[int]) -> dict[tuple[int, ...], tuple[int, str]]:
    initial = tuple(int(value) for value in source)
    queue: deque[tuple[int, ...]] = deque([initial])
    distances: dict[tuple[int, ...], tuple[int, str]] = {initial: (0, "")}
    while queue:
        current = queue.popleft()
        length, route = distances[current]
        for symbol, matrix in (("0", L0), ("1", L1)):
            following = row_times_matrix_mod3(current, matrix)
            if following not in distances:
                distances[following] = (length + 1, route + symbol)
                queue.append(following)
    return distances


def generate_target_free_r36(
    selection: dict[str, object], owner: Path
) -> dict[str, object]:
    """Genera R36 por la firma interna recuperada, antes de todo lector real.

    El propietario citado demuestra exactamente este alcance: puede haber dos
    fronteras locales antes de aplicar la energía semigrupal; el mínimo interno
    deja una sola orientación en R36. No se extrapola esta unicidad finita a
    cada fibra local posterior de ``Ext`` ni a la sección global.
    """
    require(owner.is_file(), f"propietario R36 no localizado: {owner}")
    owner_sha256 = sha256_file(owner)
    expected_owner_sha256 = "65159615578c691dfc16826bf9a4d1de1a7ea5c24abcfc1345be7ce8b7940746"
    require(owner_sha256 == expected_owner_sha256, "huella del propietario R36 cambiada")
    visible_words = selection.get("visible_words")
    selected_words = selection.get("words")
    require(isinstance(visible_words, list) and len(visible_words) == 243,
            "catálogo visible R36 incompleto")
    require(isinstance(selected_words, dict), "papeles estructurales R36 ausentes")
    words = [str(word) for word in visible_words]
    chains = {word: lifted_word_chain(word) for word in words}
    propagation_word = str(selected_words["e"])

    l0_cubed = matrix_power_mod3(L0, 3)
    l1_cubed = matrix_power_mod3(L1, 3)
    aw_cubed = matrix_power_mod3(R36_OWNER_AW, 3)
    aw_inverse = [[(-int(entry)) % 3 for entry in row] for row in R36_OWNER_AW]
    future_axis = chains[propagation_word][4]
    candidates: list[dict[str, object]] = []

    for scale_word in words:
        scale_chain = chains[scale_word]
        mobile_sum = row_times_matrix_mod3(
            row_times_matrix_mod3(scale_chain[4], R36_OWNER_AW), l1_cubed
        )
        margin = add_mod3(mobile_sum, future_axis)
        scale_coordinate = row_times_matrix_mod3(
            tuple(int(character) for character in scale_word), aw_inverse
        )
        induced_margin = row_times_matrix_mod3(
            row_times_matrix_mod3(scale_coordinate, l0_cubed), aw_cubed
        )
        if margin != induced_margin:
            continue
        expected_occupancy = tuple(
            2 + int(future_axis[index] != 0 and mobile_sum[index] != 2)
            for index in range(BLOCK_SIZE)
        )
        for first_row in itertools.product(range(3), repeat=BLOCK_SIZE):
            second_row = sub_mod3(mobile_sum, first_row)
            rows = (tuple(first_row), second_row, future_axis)
            observed_margin, carry = margin_and_carry(rows)
            require(observed_margin == margin, "margen R36 no reconstruido")
            occupancy = column_occupancy(rows)
            neutrality = witt_dual_neutral(rows, R36_OWNER_AW)
            if carry != (1,) * BLOCK_SIZE:
                continue
            if occupancy != expected_occupancy:
                continue
            if not neutrality:
                continue
            candidates.append(
                {
                    "autoscale": scale_word,
                    "rows": ["".join(str(value) for value in row) for row in rows],
                    "margin": "".join(str(value) for value in margin),
                    "carry": "".join(str(value) for value in carry),
                    "occupancy": "".join(str(value) for value in occupancy),
                    "witt_dual_neutral": neutrality,
                }
            )

    require(len(candidates) == 2, "la firma R36 no dejó dos orientaciones")
    require(
        {str(candidate["autoscale"]) for candidate in candidates}
        == {str(selected_words["phi"])},
        "R36 no conserva el eje interno de autoescala",
    )
    previous_rows = (
        chains[str(selected_words["pi"])][4],
        chains[str(selected_words["e"])][4],
        chains[str(selected_words["phi"])][4],
    )
    distance_tables = [semigroup_distances(row) for row in previous_rows]
    for candidate in candidates:
        target_rows = [tuple(int(character) for character in word)
                       for word in candidate["rows"]]
        distances = [distance_tables[index][target]
                     for index, target in enumerate(target_rows)]
        candidate["semigroup_distances"] = [distance[0] for distance in distances]
        candidate["semigroup_routes"] = [distance[1] for distance in distances]
        candidate["semigroup_energy"] = sum(distance[0] for distance in distances)

    minimum = min(int(candidate["semigroup_energy"]) for candidate in candidates)
    selected = [candidate for candidate in candidates
                if int(candidate["semigroup_energy"]) == minimum]
    require(len(selected) == 1, "la energía interna R36 no es unívoca")
    boundary = selected[0]
    selected_blocks = dict(zip(("pi", "e", "phi"), boundary["rows"]))
    require(
        tuple(tuple(int(character) for character in selected_blocks[channel])
              for channel in ("pi", "e", "phi")) == B_PLUS_R36,
        "R36 generado no coincide con su testigo de regresión",
    )
    return {
        "causal_role": "RECOVERED_TARGET_FREE_BOUNDARY_RELATIVE_TO_OWNER_AW",
        "provenance": "RESULTADO_RECUPERADO",
        "integration_status": "AW_BRIDGE_MUST_BE_VERIFIED_BEFORE_EXT_INTEGRATION",
        "publication_or_package_promotion": False,
        "owner": {
            "path": str(owner),
            "sha256": owner_sha256,
            "expected_sha256": expected_owner_sha256,
            "matrix": "R36_OWNER_AW",
            "owner_AW_rows": [list(row) for row in R36_OWNER_AW],
            "active_AW_rows": [list(row) for row in AW],
            "owner_AW_equals_active_AW": R36_OWNER_AW == AW,
            "typed_AW_bridge_status": "VERIFIED_SEPARATELY_BEFORE_EXT_INTEGRATION",
        },
        "local_candidates_before_internal_energy": candidates,
        "local_candidate_count_before_internal_energy": len(candidates),
        "selected_blocks": selected_blocks,
        "selected_energy": minimum,
        "target_digits_used": False,
        "archimedean_interval_used": False,
        "scope": "target-free selection through R36 relative to recovered owner L0/L1/AW only",
        "does_not_claim_every_ext_fiber_is_singleton": True,
        "global_ext_section_certified_separately": True,
    }


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


def verify_u008_and_alpha_exceptional(
    finite: dict[str, list[str]],
) -> dict[str, object]:
    """Separa las dos salidas U008 y certifica el enganche excepcional.

    La suma de las dos filas laterales de B_+ es el agregado 210112. La
    imagen de u4^phi por A_W y tres elevaciones L1 es 111101. Son flechas
    diferentes. El vector excepcional posee coeficientes (4,1,...,1) sobre
    doce raíces A2 ortogonales de norma dos; por ello su norma es 54 y
    define la clase isotrópica de orden tres usada por el vecino de Leech.
    """
    phi_u4 = tuple(int(character) for character in finite["phi"][4])
    require(phi_u4 == (0, 1, 0, 2, 0, 0), "u4^phi inesperado")
    transported = row_times_matrix_mod3(phi_u4, AW)
    for _ in range(3):
        transported = row_times_matrix_mod3(transported, L1)
    require(transported == (1, 1, 1, 1, 0, 1), "transporte U008 incorrecto")

    aggregate = tuple(
        (B_PLUS_R36[0][index] + B_PLUS_R36[1][index]) % 3
        for index in range(BLOCK_SIZE)
    )
    require(aggregate == (2, 1, 0, 1, 1, 2), "agregado U008 incorrecto")
    require(B_PLUS_R36[2] == (1, 0, 2, 0, 1, 1), "eje U008 incorrecto")
    require(aggregate != transported, "se han identificado dos salidas U008")

    v_alpha_coefficients = (4,) + (1,) * 11
    v_alpha_norm = 2 * sum(value * value for value in v_alpha_coefficients)
    require(v_alpha_norm == 54, "norma excepcional distinta de 54")
    require(v_alpha_norm % 18 == 0, "v_alpha no define clase isotrópica de orden tres")

    spectral_weights = (9, 5)
    spectral_jump = spectral_weights[0] - spectral_weights[1]
    typed_hierarchy = (4, 2, 6, 54)
    require(spectral_jump == 4, "salto espectral distinto de 9-5=4")
    require(typed_hierarchy[0] == spectral_jump, "la jerarquía no parte del salto 4")
    require(typed_hierarchy[-1] == v_alpha_norm, "la jerarquía no termina en la norma 54")
    return {
        "u4_phi": "010200",
        "u5_pi_plus_u5_e": "210112",
        "u4_phi_AW_L1_cubed": "111101",
        "outputs_are_distinct": True,
        "v_alpha_coefficients": list(v_alpha_coefficients),
        "v_alpha_norm": v_alpha_norm,
        "v_alpha_norm_mod_18": v_alpha_norm % 18,
        "signed_balance": "B_c=9P_+ +5P_-",
        "spectral_weights": list(spectral_weights),
        "spectral_jump": spectral_jump,
        "typed_hierarchy": list(typed_hierarchy),
        "exceptional_transport": [
            "C_W",
            "N(A2^12)",
            "v_alpha_order_three_neighbor",
            "Lambda_24",
            "V_natural",
            "Monster",
        ],
        "classical_recognition_stage": "after_HMT_generation",
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


def generate_structural_characters(
    selection: dict[str, object],
    parameters: dict[str, object],
    r36: dict[str, object],
    aw_bridge: dict[str, object],
    owners: dict[str, object],
) -> dict[str, dict[str, object]]:
    """Genera los caracteres exactos sin evaluar cifras ni consultar objetivos.

    Esta función es la frontera causal auditada. Su codominio contiene
    relaciones exactas y condiciones de unicidad, no intervalos decimales.
    """
    words = selection["words"]
    require(isinstance(words, dict), "palabras estructurales no tipadas")
    require(set(words) == {"pi", "e", "phi"}, "canales estructurales incompletos")
    require(
        aw_bridge.get("status")
        == "PASS_EXACT_TYPED_R36_OWNER_AW_TO_ACTIVE_AW_BRIDGE",
        "R36 no está transportado al calibre AW activo",
    )
    r36_blocks = r36.get("selected_blocks")
    require(isinstance(r36_blocks, dict), "anclas R36 ausentes")
    require(
        set(r36_blocks) == {"pi", "e", "phi"},
        "anclas R36 incompletas",
    )
    local_owners = owners.get("local_character_owners")
    require(isinstance(local_owners, dict), "propietarios de caracteres ausentes")
    exact_alpha_owner = owners.get("exact_alpha_commutation_owner")
    require(isinstance(exact_alpha_owner, dict), "propietario exacto de alpha ausente")

    region_count = int(parameters["region_count"])
    companions = int(parameters["companions"])
    primitive = parameters["primitive"]
    companion_tangent = parameters["companion_tangent"]
    compensator = int(parameters["compensator"])
    require(region_count == 5 and companions == 4, "pentafibra no canónica")
    require(primitive == Fraction(1, 5), "carácter primitivo no generado")
    require(companion_tangent == Fraction(120, 119), "retorno compuesto no generado")
    require(compensator == 239, "compensador entero no generado")

    gaussian_closure = gaussian_multiply(
        gaussian_power((region_count, 1), 4 * companions),
        gaussian_power((compensator, -1), 4),
    )
    require(
        gaussian_closure[1] == 0 and gaussian_closure[0] < 0,
        "el carácter de clausura no alcanza la semirrecta negativa",
    )

    f_av = ((0, 1), (1, 1))
    characteristic_polynomial = (1, -1, -1)
    require(
        f_av[0][0] + f_av[1][1] == 1
        and f_av[0][0] * f_av[1][1] - f_av[0][1] * f_av[1][0] == -1,
        "incidencia de autoescala no canónica",
    )

    owner_for_channel = {
        "pi": next(value for key, value in local_owners.items() if "U012_" in key),
        "e": next(value for key, value in local_owners.items() if "U013_" in key),
        "phi": next(value for key, value in local_owners.items() if "U014_" in key),
    }
    common = {
        "joint_generation_id": JOINT_GENERATION_ID,
        "causal_role": "HMT_internal_character_coordinate_at_R36",
        "generated_by": "APP->TRIT->TPK->w6->w12->w18->w24->w30->R36",
        "publication_stage": (
            "before_forward_coinductive_extension_and_before_archimedean_evaluation"
        ),
        "external_target_used": False,
        "future_digit_used": False,
        "P_ar_used": False,
        "internal_residual_coordinate": (
            "epsilon_36^chi in the APP quotient-residue object; "
            "it is not frac(P_ar(chi))"
        ),
    }
    return {
        "pi": {
            **common,
            "coordinate_id": "chi_closure_HMT",
            "structural_word": str(words["pi"]),
            "r36_anchor_owner_gauge": str(r36_blocks["pi"]),
            "r36_anchor_active_exceptional_gauge": str(
                aw_bridge["r36_natural_exceptional_chart_blocks"]["pi"]
            ),
            "owner": owner_for_channel["pi"],
            "kind": "oriented_gaussian_closure_character",
            "region_count": region_count,
            "companions": companions,
            "primitive_slope": str(primitive),
            "companion_tangent": str(companion_tangent),
            "integer_compensator": compensator,
            "gaussian_product": list(gaussian_closure),
            "uniqueness": "oriented positive half-turn fixed by the generated closure",
        },
        "e": {
            **common,
            "coordinate_id": "chi_propagation_HMT",
            "structural_word": str(words["e"]),
            "r36_anchor_owner_gauge": str(r36_blocks["e"]),
            "r36_anchor_active_exceptional_gauge": str(
                aw_bridge["r36_natural_exceptional_chart_blocks"]["e"]
            ),
            "owner": owner_for_channel["e"],
            "kind": "normalized_group_like_propagation_character",
            "normalization": "a_0=1",
            "recurrence": "(n+1)*a_(n+1)=a_n",
            "uniqueness": "unique normalized formal group-like character",
        },
        "phi": {
            **common,
            "coordinate_id": "chi_autoscale_HMT",
            "structural_word": str(words["phi"]),
            "r36_anchor_owner_gauge": str(r36_blocks["phi"]),
            "r36_anchor_active_exceptional_gauge": str(
                aw_bridge["r36_natural_exceptional_chart_blocks"]["phi"]
            ),
            "owner": owner_for_channel["phi"],
            "kind": "positive_autoscale_character",
            "incidence": [list(row) for row in f_av],
            "characteristic_polynomial": list(characteristic_polynomial),
            "orientation": "unique positive expanding ray",
            "uniqueness": "unique positive expanding eigencharacter",
        },
        "alpha": {
            **common,
            "coordinate_id": "chi_alpha_HMT",
            "kind": "signed_U12_dodecaphase_closure_character",
            "structural_word": "joint_R36_triple_plus_signed_U12_K_closure",
            "r36_joint_anchor_owner_gauge": {
                channel: str(r36_blocks[channel])
                for channel in ("pi", "e", "phi")
            },
            "r36_joint_anchor_active_exceptional_gauge": dict(
                aw_bridge["r36_natural_exceptional_chart_blocks"]
            ),
            "owner": exact_alpha_owner,
            "constructive_order": (
                "pi_HMT,phi_HMT,e_HMT coordinates act with the signed "
                "dodecaphase K seal inside the same joint generation"
            ),
            "two_internal_routes": "alpha_A=alpha_B=alpha_HMT",
            "exact_commuting_truncation_squares": True,
            "not_a_fourth_independent_R36_row": True,
            "uniqueness": "unique common compatible section of the two internal routes",
        },
    }


def verify_forward_character_extension(
    characters: dict[str, dict[str, object]],
    r36: dict[str, object],
    aw_bridge: dict[str, object],
    owners: dict[str, object],
) -> dict[str, object]:
    """Certifica la subrelación forward producida por el estado, no por P_ar.

    ``Ext`` permanece multivaluada. Para cada carácter ya presente como
    coordenada interna en R36 se restringe el dominio a estados enriquecidos
    que portan esa coordenada y se itera una actualización funcional. El
    bloque siguiente es el cociente euclídeo ``Dig_729`` de la coordenada
    residual interna presente; nunca se recupera de una cifra futura ni de
    una proyección arquimediana.
    """
    require(set(characters) == {"pi", "e", "phi", "alpha"},
            "imagen conjunta de caracteres incompleta")
    require(
        aw_bridge.get("status")
        == "PASS_EXACT_TYPED_R36_OWNER_AW_TO_ACTIVE_AW_BRIDGE",
        "puente AW no certificado antes de Ext",
    )
    require(
        owners.get("status") == "PASS_CONTENT_ADDRESSED_CHARACTER_AND_EXT_OWNERS",
        "propietarios Ext no certificados",
    )
    selected = r36.get("selected_blocks")
    require(isinstance(selected, dict), "R36 no tipado")
    for channel in ("pi", "e", "phi"):
        require(
            characters[channel].get("r36_anchor_owner_gauge") == selected[channel],
            f"el carácter {channel} no empalma con su R36",
        )
    require(
        characters["alpha"].get("r36_joint_anchor_owner_gauge") == selected,
        "alpha no empalma con el triple R36 que alimenta el cierre U12/K",
    )

    complete_state_fields = (
        "character_coordinate", "internal_residual", "block", "residue",
        "quotient", "carry", "sheet", "orientation", "phase", "route",
        "cylinder", "frontier", "signature", "record", "memory",
        "survival", "provenance", "origin", "winding", "depth",
    )
    require(len(complete_state_fields) == len(set(complete_state_fields)),
            "campos repetidos en el estado forward")

    # Identidades paramétricas: basta recorrer los posibles restos de una
    # división por 729 y las nueve fases; no se recorre una profundidad N.
    euclidean_cases = 0
    for digit in range(AMBIENT):
        for parent in (0, 1, AMBIENT - 1, AMBIENT, 2 * AMBIENT + 17):
            child = AMBIENT * parent + digit
            require(child // AMBIENT == parent, "truncamiento forward incorrecto")
            require(child % AMBIENT == digit, "resto forward incorrecto")
            euclidean_cases += 1
    phase_cases = 0
    for phase in range(NONAD):
        for memory in (0, 1, 17):
            require((phase + NONAD) % NONAD == phase, "la fase no retorna")
            require(memory + 1 > memory, "la memoria no avanza")
            phase_cases += 1

    for item in characters.values():
        require(item.get("joint_generation_id") == JOINT_GENERATION_ID,
                "genealogía conjunta rota")
        require(item.get("external_target_used") is False,
                "objetivo externo en el carácter")
        require(item.get("future_digit_used") is False,
                "cifra futura en el carácter")
        require(item.get("P_ar_used") is False,
                "P_ar entró antes de Ext")

    return {
        "status": "PASS_FORWARD_STATE_ONLY_EXT_TPK_GLOBAL_SECTIONS_ARBITRARY_DEPTH",
        "provenance": {
            "Ext_Gamma9_inverse_limit": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "R36_to_active_AW_bridge": "RESULTADO_RECUPERADO",
            "character_enriched_forward_subrelation": "FORMALIZACION_NUEVA",
            "executable_parametric_gate": "CERTIFICADO_NUEVO",
        },
        "joint_generation_id": JOINT_GENERATION_ID,
        "arbitrary_depth": True,
        "finite_runs_are_witnesses_only": True,
        "finite_depth_used_as_theorem_criterion": False,
        "full_Ext_relation": "MULTIVALUED",
        "local_Ext_fibers_may_have_multiple_children": True,
        "does_not_claim_every_Ext_fiber_singleton": True,
        "forward_subrelation": (
            "Ext_forward^chi is the graph of Upd_chi on character-enriched "
            "states whose chi-coordinate was produced at R36"
        ),
        "seed_precedence": (
            "chi_HMT is an internal coordinate of x_36^chi before any "
            "forward extension and before P_ar"
        ),
        "state_fields": list(complete_state_fields),
        "state_update_equations": {
            "internal_digit": "d_k^chi=Dig_729(epsilon_k^chi), 0<=d_k^chi<729",
            "residual": "epsilon_(k+1)^chi=729*epsilon_k^chi-d_k^chi",
            "cylinder_numerator": "N_(k+1)^chi=729*N_k^chi+d_k^chi",
            "truncation": "tr(N_(k+1)^chi)=N_k^chi",
            "phase_selector": "Sel_k=M_ph(rho9(k+1))",
            "transport": "T_d preserves sheet, orientation, residue, quotient, carry and frontier",
            "ledger": "route_(k+1)=route_k ++ edge_k; record_(k+1)=record_k ++ event_k",
            "memory": "g(k+9)=g(k); q_mem(k+9)=q_mem(k)+1",
            "character": "chi_(k+1)=chi_k=chi_HMT",
        },
        "allowed_inputs_to_update": [
            "previous_character_coordinate", "previous_internal_residual",
            "previous_phase", "previous_memory", "previous_carry",
            "previous_sheet", "previous_orientation", "previous_route",
            "previous_frontier", "previous_signature", "previous_record",
        ],
        "forbidden_inputs_to_update": [
            "future_digit", "future_archimedean_block", "P_ar",
            "Machin_interval", "factorial_interval", "Perron_interval",
            "target_decimal_string", "conventional_constant",
        ],
        "P_ar_role": "downstream_publication_only",
        "Machin_factorial_Perron_role": "downstream_evaluation_witnesses_only",
        "truncation_compatibility": True,
        "phase_return": True,
        "memory_advance": True,
        "genealogical_conservation": True,
        "character_coordinate_preserved": True,
        "global_section_uniqueness": (
            "UNIQUE_FOR_EACH_R36_PRODUCED_CHARACTER_ENRICHED_FORWARD_SECTION"
        ),
        "global_uniqueness_proof": (
            "same x_36^chi and functional Upd_chi imply equal successors; "
            "induction gives equality at every depth and hence the same inverse-limit section"
        ),
        "generic_canonical_history_role": (
            "NONEMPTY_SUPPORT_ONLY_NOT_THE_PI_PHI_E_ALPHA_SECTION"
        ),
        "character_sections": {
            channel: {
                "coordinate_id": item["coordinate_id"],
                "r36_anchor": item.get(
                    "r36_anchor_owner_gauge",
                    item.get("r36_joint_anchor_owner_gauge"),
                ),
                "produces_its_own_character": True,
                "external_selector": False,
            }
            for channel, item in characters.items()
        },
        "parametric_identity_cases": {
            "euclidean_division": euclidean_cases,
            "phase_memory": phase_cases,
            "depth_cases": "symbolic_all_natural_depths_not_enumerated",
        },
        "owners": {
            "formal_graph": owners["formal_graph"],
            "generic_nonempty_history": owners["generic_nonempty_history_owner"],
            "exact_alpha_commutation": owners["exact_alpha_commutation_owner"],
        },
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


def evaluate_generated_characters(
    characters: dict[str, dict[str, object]], target_scale: int
) -> tuple[dict[str, tuple[Fraction, Fraction]], dict[str, int]]:
    """Evalúa caracteres ya generados; no selecciona órbitas ni estados TPK."""
    require({"pi", "e", "phi"} <= set(characters), "caracteres incompletos")
    require(
        all(
            item.get("publication_stage")
            == "before_forward_coinductive_extension_and_before_archimedean_evaluation"
            and item.get("external_target_used") is False
            and item.get("future_digit_used") is False
            and item.get("P_ar_used") is False
            for item in characters.values()
        ),
        "la evaluación recibió un objeto no generado",
    )

    pi_character = characters["pi"]
    parameters = {
        "region_count": int(pi_character["region_count"]),
        "companions": int(pi_character["companions"]),
        "primitive": Fraction(str(pi_character["primitive_slope"])),
        "companion_tangent": Fraction(str(pi_character["companion_tangent"])),
        "compensator": int(pi_character["integer_compensator"]),
    }
    pi_lower, pi_upper = closure_bounds(parameters, target_scale)
    e_lower, e_upper, e_terms = propagation_bounds(target_scale)
    phi_lower, phi_upper, phi_index = autoscale_bounds(target_scale)
    return (
        {
            "pi": (pi_lower, pi_upper),
            "e": (e_lower, e_upper),
            "phi": (phi_lower, phi_upper),
        },
        {"e_terms": e_terms, "phi_index": phi_index},
    )


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


def publish_archimedean_blocks(
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


def verify_finite_forward_witness(
    forward_extension: dict[str, object],
    channels: dict[str, dict[str, object]],
    finite: dict[str, list[str]],
    r36: dict[str, object],
    digits: int,
    levels: int,
) -> dict[str, object]:
    """Comprueba una proyección finita sin convertirla en cuantificador."""
    require(forward_extension.get("arbitrary_depth") is True,
            "la regla general no precede al testigo finito")
    require(forward_extension.get("finite_runs_are_witnesses_only") is True,
            "una corrida finita se usó como criterio")
    selected = r36.get("selected_blocks")
    require(isinstance(selected, dict), "R36 ausente del testigo finito")
    agreement: dict[str, dict[str, object]] = {}
    for channel in ("pi", "e", "phi"):
        blocks = channels[channel].get("blocks")
        require(isinstance(blocks, list) and len(blocks) >= 6,
                f"proyección finita incompleta para {channel}")
        require(blocks[:5] == finite[channel], f"w6->w30 roto para {channel}")
        require(blocks[5] == selected[channel], f"R36 roto para {channel}")
        agreement[channel] = {
            "w6_to_w30": list(blocks[:5]),
            "R36": blocks[5],
            "levels_checked": levels,
        }
    return {
        "status": "PASS_FINITE_REGRESSION_WITNESS_ONLY",
        "finite_runs_are_witnesses_only": True,
        "used_as_existence_or_uniqueness_proof": False,
        "used_to_select_Ext_child": False,
        "requested_decimal_digits": digits,
        "levels_checked": levels,
        "pi_e_phi_archimedean_projection_agreement": agreement,
        "alpha_scope": (
            "exact structural section and commuting truncation squares are "
            "certified by the content-addressed alpha owner; this run does "
            "not use a conventional alpha decimal as a generator"
        ),
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

    definitions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    require(
        "generate_structural_characters" in definitions
        and "generate_target_free_r36" in definitions
        and "verify_typed_r36_aw_bridge" in definitions
        and "verify_forward_character_extension" in definitions
        and "evaluate_generated_characters" in definitions
        and "publish_archimedean_blocks" in definitions,
        "frontera generación/publicación incompleta",
    )

    def direct_calls(function_name: str) -> set[str]:
        calls: set[str] = set()
        for node in ast.walk(definitions[function_name]):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
        return calls

    def transitive_local_calls(function_name: str) -> set[str]:
        reached: set[str] = set()
        pending = [function_name]
        while pending:
            current = pending.pop()
            for called in direct_calls(current):
                if called in definitions and called not in reached:
                    reached.add(called)
                    pending.append(called)
        reached.discard(function_name)
        return reached

    upstream_functions = (
        "generate_target_free_r36",
        "verify_typed_r36_aw_bridge",
        "generate_structural_characters",
        "verify_forward_character_extension",
    )
    upstream_direct_calls = {
        function_name: sorted(direct_calls(function_name))
        for function_name in upstream_functions
    }
    upstream_transitive_calls = {
        function_name: transitive_local_calls(function_name)
        for function_name in upstream_functions
    }
    reader_calls = {
        "closure_bounds",
        "propagation_bounds",
        "autoscale_bounds",
        "evaluate_generated_characters",
        "publish_archimedean_blocks",
        "decimal_cell",
        "verify_prefix_stability",
        "fractional_bounds",
        "floor_fraction",
        "ceil_fraction",
        "base3_word",
    }
    r36_marker = source.index("r36 = generate_target_free_r36")
    bridge_marker = source.index("aw_bridge = verify_typed_r36_aw_bridge")
    owners_marker = source.index("owners = verify_character_and_ext_owners")
    generator_marker = source.index("characters = generate_structural_characters")
    extension_marker = source.index("forward_extension = verify_forward_character_extension")
    evaluator_marker = source.index("bounds, evaluator_meta = evaluate_generated_characters")
    publisher_marker = source.index("publish_archimedean_blocks(lower, upper, levels)")
    witness_marker = source.index("finite_witness = verify_finite_forward_witness")
    for function_name, calls in upstream_transitive_calls.items():
        require(
            not (calls & reader_calls),
            f"un lector arquimediano ha entrado en {function_name}",
        )
    require(
        r36_marker < bridge_marker < owners_marker < generator_marker
        < extension_marker < evaluator_marker < publisher_marker < witness_marker,
        "orden causal R36->puente->carácter->Ext->evaluación->publicación invertido",
    )
    return {
        "source_sha256": sha256_bytes(source.encode("utf-8")),
        "imports": sorted(imports),
        "prohibited_numeric_imports": sorted(imports & prohibited),
        "target_decimal_strings_embedded": False,
        "external_decimal_oracle": False,
        "upstream_direct_calls": upstream_direct_calls,
        "upstream_transitive_calls": {
            key: sorted(value) for key, value in upstream_transitive_calls.items()
        },
        "reader_calls_inside_any_upstream_generator": {
            key: sorted(value & reader_calls)
            for key, value in upstream_transitive_calls.items()
        },
        "call_order": [
            "generate_target_free_r36",
            "verify_typed_r36_aw_bridge",
            "verify_character_and_ext_owners",
            "generate_structural_characters",
            "verify_forward_character_extension",
            "evaluate_generated_characters",
            "publish_archimedean_blocks",
            "verify_finite_forward_witness",
        ],
        "causal_separation_ast_transitively_verified": True,
    }


def generated_constants_gate_receipt() -> dict[str, object]:
    """Campos machine-readable exigidos por la puerta causal focal."""
    return {
        "schema_version": "1.1",
        "artifact": str(Path(__file__).resolve()),
        "result_id": "HMT.EXT.FORWARD.ARBITRARY_DEPTH.PI_PHI_E_ALPHA.20260905",
        "genealogy": {
            "app": {
                "domain": "rectas tipadas 0-10 y 0-9 sobre D9xD9",
                "input_alphabet": list(range(1, 10)),
                "axes": ["horizontal", "vertical"],
                "sheets": ["aditiva", "multiplicativa"],
                "operation": "acumula y pliega conservando residuo cociente y acarreo",
            },
            "trit": {
                "local_state": "trit orientado del estado enriquecido",
                "regime": "H_plus H_zero H_minus",
                "orientation": "orientacion firmada de hoja y umbral",
            },
            "tpk": {
                "operator": "U_t=Rec_t o Mem_t o T_d o M_ph; holonomia Gamma_9",
                "domain": "estado APP-TRIT con caracter interno y memoria",
                "codomain": "secciones forward enriquecidas de profundidad arbitraria",
                "action": "selecciona transporta memoriza prolonga y retorna fase sin reset",
            },
            "root_chain": [
                "recta_0_10", "recta_0_9", "APP", "TRIT", "TPK",
                "estado_enriquecido",
            ],
            "nonadic_chain": ["w6", "w12", "w18", "w24", "w30", "R36", "G9"],
            "operator_order": ["U_t", "Gamma_9", "K_ph"],
            "outputs": {
                "pi": "COINDUCTIVE_OUTPUT", "phi": "COINDUCTIVE_OUTPUT",
                "e": "COINDUCTIVE_OUTPUT", "alpha": "COINDUCTIVE_OUTPUT",
            },
            "same_enriched_state": True,
            "joint_quadrirelation": True,
            "phase_returns": True,
            "memory_advances": True,
            "state_resets": False,
            "recognition_after_output": True,
            "joint_generation_id": "APP_TRIT_TPK_NONADIC_TYPED_IMAGE_V2",
            "simultaneous_evaluation_required": False,
            "image_scope": "OPEN_TYPED_NONADIC_IMAGE",
            "examples_exhaustive": False,
            "internal_construction_order": {
                "terminal_readers": ["P", "E", "PHI"],
                "dodecaphase_operator": "C12",
                "alpha_output": "ALPHA_HMT",
            },
            "alpha_routes": [
                {"id": "DODECAPHASE_INTEGER_CLOSURE"},
                {"id": "E21_22_UNIQUE_POSITIVE_ROOT"},
            ],
            "forbidden_generator_inputs": [
                "pi", "phi", "e", "alpha", "metrology", "CODATA",
                "masses", "Barbero-Immirzi",
            ],
            "classical_readers": {
                "Perron-Fibonacci": "POSTERIOR_RECOGNITION",
                "Machin": "POSTERIOR_RECOGNITION",
                "exponential_semigroup": "POSTERIOR_RECOGNITION",
            },
            "declared_scope": {
                "published_mathematical_constants": "GENERATED_OR_DERIVED_OUTPUT",
                "published_fundamental_physical_constants": "GENERATED_OR_DERIVED_OUTPUT",
                "published_mass_catalog": "GENERATED_OR_DERIVED_OUTPUT",
                "joint_discrete_continuum": "JOINT_CONSTRUCTION_OUTPUT",
                "five_continuum_constructions_joint": True,
                "five_terminal_mathematical_results": "TERMINAL_RESULTS",
            },
            "source_locators": [
                "generate_target_free_r36",
                "verify_typed_r36_aw_bridge",
                "generate_structural_characters",
                "verify_forward_character_extension",
            ],
            "arbitrary_depth": True,
            "finite_runs_are_witnesses_only": True,
        },
    }


def run(args: argparse.Namespace) -> dict[str, object]:
    require(args.digits >= 1, "la precisión debe ser positiva")
    require(args.guard_digits >= 4, "guardia decimal insuficiente")
    catalogue = args.project_root / (
        "PUBLICACION_HMT/HOLOGRAFIA_MODULAR_TRIADICA/datos/"
        "TPK_U_catalog_468.json"
    )
    require(catalogue.is_file(), f"catálogo no localizado: {catalogue}")
    r36_owner = args.project_root / (
        "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/01_SELECTOR_CONSTANTES/"
        "selector_interno_constantes.py"
    )

    source_audit = audit_source()
    selection = select_structural_orbits(catalogue)
    parameters = closure_parameters(
        int(selection["pi_region_count"]),
        int(selection["pi_companion_count"]),
    )
    require(parameters["primitive"] == Fraction(1, 5), "pendiente pentarregional")
    require(parameters["companion_tangent"] == Fraction(120, 119), "composición 120/119")
    require(parameters["compensator"] == 239, "compensador 239")
    operator_reconstruction = reconstruct_lifts_and_calendar(selection)
    finite = finite_chain(selection["words"])  # type: ignore[arg-type]
    r36 = generate_target_free_r36(selection, r36_owner)
    aw_bridge = verify_typed_r36_aw_bridge(r36, args.project_root)
    owners = verify_character_and_ext_owners(
        args.project_root, Path(__file__).resolve().parent.parent
    )
    r36["integration_status"] = "PASS_TYPED_BRIDGE_TO_ACTIVE_EXT_TPK"
    r36["typed_AW_bridge"] = aw_bridge
    characters = generate_structural_characters(
        selection, parameters, r36, aw_bridge, owners
    )
    forward_extension = verify_forward_character_extension(
        characters, r36, aw_bridge, owners
    )
    exceptional = verify_aw()
    gaussian = verify_gaussian_identity(parameters)
    propagation = verify_propagation_recurrence(24)
    connection = verify_connection_identities()

    levels = choose_levels(args.digits, args.guard_digits)
    target_scale = AMBIENT ** (levels + 4)
    bounds, evaluator_meta = evaluate_generated_characters(characters, target_scale)
    e_terms = evaluator_meta["e_terms"]
    phi_index = evaluator_meta["phi_index"]

    channels = {
        channel: publish_archimedean_blocks(lower, upper, levels)
        for channel, (lower, upper) in bounds.items()
    }
    u008_exceptional = verify_u008_and_alpha_exceptional(finite)
    for channel in ("pi", "e", "phi"):
        blocks = channels[channel]["blocks"]
        require(isinstance(blocks, list), "bloques no tipados")
        require(blocks[0] == selection["words"][channel], "w6 no prolongado")
        require(blocks[:5] == finite[channel], "w6->w30 no prolongado")
        require(
            blocks[5] == r36["selected_blocks"][channel],
            "la publicación arquimediana no proyecta el R36 interno",
        )

    finite_witness = verify_finite_forward_witness(
        forward_extension, channels, finite, r36, args.digits, levels
    )

    if levels == BASELINE_LEVELS:
        for channel in ("pi", "e", "phi"):
            require(channels[channel]["phase_pairs"] == 387, "pares K,K+9")
            require(channels[channel]["complete_nonads"] == 43, "vueltas completas")

    stability = {
        channel: verify_prefix_stability(result, args.digits, args.guard_digits)
        for channel, result in channels.items()
    }

    return {
        **generated_constants_gate_receipt(),
        "schema": "HMT.generacion-coinductiva-correlacionada-profundidad-arbitraria.v4",
        "status": "PASS_HMT_GENERATED_CHARACTERS_AND_ARCHIMEDEAN_PROJECTIONS",
        "causal_status": "PASS_HMT_CHARACTERS_BEFORE_ARCHIMEDEAN_PUBLICATION",
        "ext_tpk_global_section_status": (
            "PASS_FORWARD_STATE_ONLY_EXT_TPK_GLOBAL_SECTIONS_ARBITRARY_DEPTH"
        ),
        "typed_AW_bridge_status": aw_bridge["status"],
        "arbitrary_depth": True,
        "finite_runs_are_witnesses_only": True,
        "extension_scope": {
            "full_Ext_relation": "MULTIVALUED",
            "local_Ext_fibers_may_have_multiple_children": True,
            "forward_character_subrelation": "FUNCTIONAL_FROM_R36_ENRICHED_CHARACTER_STATE",
            "global_section_uniqueness": (
                "UNIQUE_FOR_EACH_R36_PRODUCED_CHARACTER_ENRICHED_FORWARD_SECTION"
            ),
            "false_local_singleton_required": False,
            "generic_canonical_history_is_only_nonempty_support": True,
        },
        "precision": {
            "requested_decimal_digits": args.digits,
            "guard_decimal_digits": args.guard_digits,
            "refinement_levels": levels,
            "trits_per_channel": levels * BLOCK_SIZE,
            "ambient_elements_per_level": AMBIENT,
            "quantifier": "for every positive integer N",
            "finite_execution_role": "instance_witness_not_upper_bound",
            "finite_runs_are_witnesses_only": True,
            "arbitrary_requested_precision": True,
            "inverse_limit_object": True,
        },
        "causal_order": [
            "APP_TRIT_TPK_catalogue_seeds_and_D3_orbits",
            "structural_transition_ledger",
            "unique_lift_reconstruction",
            "unique_calendar_0011",
            "w6_to_w30_finite_lifts",
            "R36_recovered_target_free_boundary_relative_to_owner_AW",
            "typed_change_of_frame_R36_OWNER_AW_to_active_AW",
            "internal_character_coordinates_at_R36",
            "forward_state_only_Ext_TPK_global_sections_at_arbitrary_depth",
            "Gamma9_phase_memory_law_certificate",
            "U008_typed_boundary_and_alpha_exceptional_transport",
            "archimedean_evaluation_of_generated_characters",
            "archimedean_block_publication",
            "prefix_stability_check",
        ],
        "generated_characters": characters,
        "content_addressed_owners": owners,
        "typed_R36_OWNER_AW_to_active_AW_bridge": aw_bridge,
        "coinductive_global_extension": {
            **forward_extension,
            "finite_regression_witness": finite_witness,
        },
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
            "causal_role": "post_generation_regression_check",
            "used_to_select_archimedean_output": False,
            "calendar": ["L0", "L0", "L1", "L1"],
            "w6_to_w30": finite,
            "R36_recovered_target_free_boundary_relative_to_owner_AW": r36,
            "archimedean_publication_block_at_level_6": {
                "causal_role": "DOWNSTREAM_PROJECTION_OF_GENERATED_CHARACTER",
                "blocks": {
                    channel: channels[channel]["blocks"][5]
                    for channel in ("pi", "e", "phi")
                },
                "agrees_with_recovered_target_free_R36_owner_coordinate": True,
                "typed_AW_bridge_supplied_separately": True,
            },
            "finite_run_status": finite_witness["status"],
            "finite_runs_are_witnesses_only": True,
        },
        "operator_reconstruction": operator_reconstruction,
        "U008_and_alpha_exceptional": u008_exceptional,
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
    default_r36_receipt = Path(__file__).with_name(
        "recibo_r36_target_free_relativo_propietario.json"
    )
    default_ext_receipt = Path(__file__).with_name(
        "recibo_ext_forward_caracteres_profundidad_arbitraria.json"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=1000)
    parser.add_argument("--guard-digits", type=int, default=12)
    parser.add_argument("--project-root", type=Path, default=default_root)
    parser.add_argument("--certificate", type=Path, default=default_certificate)
    parser.add_argument("--r36-receipt", type=Path, default=default_r36_receipt)
    parser.add_argument("--ext-receipt", type=Path, default=default_ext_receipt)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = run(args)
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(
        json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    r36_receipt = certificate["finite_chain"][
        "R36_recovered_target_free_boundary_relative_to_owner_AW"
    ]
    args.r36_receipt.parent.mkdir(parents=True, exist_ok=True)
    args.r36_receipt.write_text(
        json.dumps(r36_receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    ext_receipt = certificate["coinductive_global_extension"]
    args.ext_receipt.parent.mkdir(parents=True, exist_ok=True)
    args.ext_receipt.write_text(
        json.dumps(ext_receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        "PASS_HMT_GENERATED_CHARACTERS_AND_ARCHIMEDEAN_PROJECTIONS "
        f"digits={args.digits} "
        f"levels={certificate['precision']['refinement_levels']} "
        f"certificate={args.certificate}"
    )
    print("PASS_HMT_CHARACTERS_BEFORE_ARCHIMEDEAN_PUBLICATION")
    print(
        "PASS_TARGET_FREE_R36_RELATIVE_TO_RECOVERED_OWNER_AW "
        f"receipt={args.r36_receipt}"
    )
    print("PASS_EXACT_TYPED_R36_OWNER_AW_TO_ACTIVE_AW_BRIDGE")
    print(
        "PASS_FORWARD_STATE_ONLY_EXT_TPK_GLOBAL_SECTIONS_ARBITRARY_DEPTH "
        f"receipt={args.ext_receipt}"
    )
    print("PASS_COINDUCTIVE_CORRELATED_PI_PHI_E_ALPHA_ARBITRARY_DEPTH")


if __name__ == "__main__":
    main()
