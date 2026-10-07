#!/usr/bin/env python3
"""Certifica el alcance exacto de N69--N74 respecto de los ocho bloques.

Las familias de lectura se construyen antes de introducir el conjunto de
contraste. El programa no abre W72, K, U12, alpha ni CODATA. El conjunto de
ocho palabras sólo se usa al final para medir cobertura y nunca para definir
un lector, elegir un tiempo o filtrar una rama.

No se usa ``assert``; todas las condiciones siguen activas bajo ``python -O``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

N69 = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/"
    "HMT_N69_ley_transicion_o_axioma_cilindrico_v1/"
    "N69_signatures_t0_t99.csv"
)
N72 = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N72_supervivencia_coinductiva_novena_puerta_v1/"
    "N72_coinductive_survival_profile_t5_t25_h9.csv"
)
N74 = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N74_monodromia_nueve_puertas_v1/"
    "N74_monodromy_return_t_to_t_plus_9.csv"
)
COINDUCTIVE_READERS = ROOT / (
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/01_SELECTOR_CONSTANTES/"
    "CERTIFICADO_SELECTOR_GLOBAL.json"
)
OUT = HERE / "RESULTADO_NO_GO_S8_N71_N72.json"

FIELDS = ("cierre", "propagacion", "autoescala")

# Matriz de Paley--Witt usada por los registros N69--N74.
A_W = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def witt(word: str) -> str:
    require(len(word) == 6 and set(word) <= {"0", "1", "2"},
            "palabra ternaria mal formada")
    vector = tuple(int(value) for value in word)
    return "".join(
        str(sum(vector[i] * A_W[i][j] for i in range(6)) % 3)
        for j in range(6)
    )


def linear_word(bands: Sequence[str], coefficients: Sequence[int]) -> str:
    require(len(bands) == len(coefficients) == 3, "lector lineal mal tipado")
    return "".join(
        str(sum(int(coefficients[i]) * int(bands[i][j]) for i in range(3)) % 3)
        for j in range(6)
    )


def charge(bands: Sequence[str], dual: bool) -> tuple[int, int, int]:
    words = tuple(witt(word) if dual else word for word in bands)
    return tuple(sum(int(value) for value in word) % 3 for word in words)  # type: ignore[return-value]


def row_readers(row: dict[str, str]) -> dict[str, set[str]]:
    bands = tuple(row["B"].split("|"))
    require(len(bands) == 3, "frontera N69 mal formada")
    phase = (int(row["t"]) - 1) % 3
    comparison = {"visible": set(), "dual": set()}
    for name, dual in (("visible", False), ("dual", True)):
        rho = charge(bands, dual)
        for offset in range(3):
            selected = (phase + offset) % 3
            for orientation in (1, 2):
                coefficients = tuple(
                    orientation * (1 if value == selected else -1) % 3
                    for value in rho
                )
                comparison[name].add(linear_word(bands, coefficients))

    rho_dual = charge(bands, True)
    affine_dual = {
        linear_word(bands, tuple((value + phase) % 3 for value in rho_dual))
    }
    return {
        "bands": set(bands),
        "comparison_visible": comparison["visible"],
        "comparison_dual": comparison["dual"],
        "affine_dual": affine_dual,
    }


def all_n69_families(rows: list[dict[str, str]]) -> dict[str, object]:
    visible: set[str] = set()
    dual: set[str] = set()
    affine: set[str] = set()
    indexed: dict[str, dict[str, set[int]]] = {}
    for row in rows:
        outputs = row_readers(row)
        visible.update(outputs["comparison_visible"])
        dual.update(outputs["comparison_dual"])
        affine.update(outputs["affine_dual"])
        for family in ("comparison_visible", "comparison_dual", "affine_dual"):
            for word in outputs[family]:
                indexed.setdefault(word, {}).setdefault(family, set()).add(int(row["t"]))
    comparison = visible | dual
    total = comparison | affine
    require((len(visible), len(dual), len(comparison), len(affine), len(total))
            == (330, 318, 410, 91, 442),
            "cambiaron los cardinales de las familias N69")
    return {
        "visible": visible,
        "dual": dual,
        "comparison": comparison,
        "affine": affine,
        "total": total,
        "indexed": indexed,
    }


def first_word_at_least(entry: dict[str, object], length: int) -> str:
    cylinders = entry.get("cilindros_ternarios")
    require(isinstance(cylinders, list), "lector coinductivo sin cilindros")
    words = [
        str(item["palabra"])
        for item in cylinders
        if isinstance(item, dict) and int(item["longitud"]) >= length
    ]
    require(bool(words), f"el lector no publica {length} trits")
    return min(words, key=len)


def rank_mod3(words: Iterable[str]) -> int:
    matrix = [[int(value) for value in word] for word in words]
    rank = 0
    for column in range(6):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column] % 3),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = 1 if matrix[rank][column] % 3 == 1 else 2
        matrix[rank] = [(inverse * value) % 3 for value in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column] % 3:
                factor = matrix[row][column] % 3
                matrix[row] = [
                    (value - factor * pivot_value) % 3
                    for value, pivot_value in zip(matrix[row], matrix[rank])
                ]
        rank += 1
    return rank


def panel_of_readers() -> dict[str, object]:
    certificate = json.loads(COINDUCTIVE_READERS.read_text(encoding="utf-8"))
    result = certificate.get("resultado")
    require(isinstance(result, dict), "certificado de lectores mal formado")
    indexed: list[dict[str, object]] = []
    for role in FIELDS:
        entry = result.get(role)
        require(isinstance(entry, dict), f"falta el lector {role}")
        word = first_word_at_least(entry, 360)
        for position in range(3):
            indexed.append({
                "reader": role,
                "position": position + 1,
                "word": word[6 * position:6 * (position + 1)],
            })
    panel = {str(item["word"]) for item in indexed}
    require(len(indexed) == 9 and len(panel) == 8, "cambió el panel 9/8")

    cyclic = {
        word[offset:] + word[:offset]
        for word in panel for offset in range(6)
    }
    witt_orbit: set[str] = set()
    combined: set[str] = set()
    for word in panel:
        current = word
        for _power in range(4):
            witt_orbit.add(current)
            current = witt(current)
    for word in cyclic:
        current = word
        for _power in range(4):
            combined.add(current)
            current = witt(current)
    require(rank_mod3(panel) == 6, "el panel dejó de generar F3^6")
    return {
        "indexed": indexed,
        "panel": panel,
        "cyclic": cyclic,
        "witt": witt_orbit,
        "combined": combined,
        "rank": 6,
    }


def n72_window(
    n69_rows: list[dict[str, str]], n72_rows: list[dict[str, str]]
) -> dict[str, object]:
    actual_words: set[str] = set()
    comparison: set[str] = set()
    affine: set[str] = set()
    times: list[int] = []
    for profile in n72_rows:
        time = int(profile["t"])
        times.append(time)
        # Convención publicada: la salida de la puerta t está en la frontera
        # B de la fila N69 t+1.
        row = n69_rows[time + 1]
        require(int(row["t"]) == time + 1, "índice N69 no consecutivo")
        require(row["B"] == profile["actual_rows"],
                "N69 y N72 dejaron de compartir la misma rama")
        outputs = row_readers(row)
        actual_words.update(outputs["bands"])
        comparison.update(outputs["comparison_visible"])
        comparison.update(outputs["comparison_dual"])
        affine.update(outputs["affine_dual"])
    require(times == list(range(5, 26)), "la ventana N72 dejó de ser t=5,...,25")
    total = actual_words | comparison | affine
    require((len(actual_words), len(comparison), len(affine), len(total))
            == (61, 114, 21, 172), "cambió la imagen total de la ventana N72")
    return {
        "times": times,
        "actual_words": actual_words,
        "comparison": comparison,
        "affine": affine,
        "total": total,
    }


def build_result() -> dict[str, object]:
    # 1. Todas las familias se construyen sin introducir el conjunto buscado.
    n69_rows = read_csv(N69)
    n72_rows = read_csv(N72)
    n74_rows = read_csv(N74)
    require(len(n69_rows) == 100, "N69 ya no contiene cien estados")
    require(len(n72_rows) == 21, "N72 ya no contiene veintiún puertas")
    require(len(n74_rows) == 9, "N74 ya no contiene nueve retornos")
    n69 = all_n69_families(n69_rows)
    n72 = n72_window(n69_rows, n72_rows)
    panel = panel_of_readers()

    # 2. N74 prueba que la fase no determina el estado de frontera.
    require(all(row["same_phi"] == "False" for row in n74_rows),
            "algún retorno N74 conservó inesperadamente phi")
    require(all(row["same_pi_plus_e"] == "False" for row in n74_rows),
            "algún retorno N74 conservó inesperadamente pi+e")
    require(all(int(row["t_plus_9"]) - int(row["t"]) == 9 for row in n74_rows),
            "N74 dejó de describir retornos de nueve pasos")

    # 3. Sólo ahora se introduce S8 como contraste posterior. No participa en
    # la definición de ninguna familia ni en la elección de ningún tiempo.
    target = {
        "002001", "020111", "200110", "121012",
        "010122", "001001", "221110", "222110",
    }
    require(len(target) == 8, "el contraste no contiene ocho palabras")
    total69 = n69["total"]
    require(isinstance(total69, set) and target <= total69,
            "N69 dejó de contener los ocho bloques")
    comparison69 = n69["comparison"]
    affine69 = n69["affine"]
    require(isinstance(comparison69, set) and isinstance(affine69, set),
            "familias N69 mal tipadas")
    require(target - comparison69 == {"001001"},
            "cambió la única obstrucción del lector comparativo")
    require(target & affine69 == {"001001", "222110"},
            "cambió la incidencia de la extensión afín")

    indexed = n69["indexed"]
    require(isinstance(indexed, dict), "índice N69 mal tipado")
    target_occurrences = {
        word: {
            family: sorted(times)
            for family, times in indexed[word].items()
        }
        for word in sorted(target)
    }

    n72_total = n72["total"]
    require(isinstance(n72_total, set), "imagen N72 mal tipada")
    n72_intersection = target & n72_total
    n72_missing = target - n72_total
    require(n72_intersection == {"010122", "020111", "221110", "222110"},
            "cambió la intersección N72--S8")
    require(n72_missing == {"001001", "002001", "121012", "200110"},
            "cambió la obstrucción de dominio N72")

    panel_set = panel["panel"]
    cyclic = panel["cyclic"]
    witt_set = panel["witt"]
    combined = panel["combined"]
    require(all(isinstance(item, set) for item in (panel_set, cyclic, witt_set, combined)),
            "órbitas del panel mal tipadas")
    require(target & panel_set == set(), "el panel pasó a contener un bloque S8")
    require(target & cyclic == {"020111"}, "cambió la órbita cíclica del panel")
    require(target & witt_set == set(), "cambió la órbita Witt del panel")
    require(target & combined == {"020111"}, "cambió la órbita combinada del panel")

    ambiguity = math.comb(len(total69), 8)
    require(ambiguity == 33899151336985935, "cambió la ambigüedad combinatoria")

    return {
        "schema": "HMT.no-go-S8-N71-N72.v1",
        "status": "PASS_NO_GO_N71_N72_COMO_SELECTOR_INTRINSECO_DE_S8",
        "construction_without_targets": {
            "families_built_before_target_contrast": True,
            "files_not_opened": [
                "W72",
                "CanonicalSealK",
                "SignedDodecaphaseStateU12",
                "alpha",
                "CODATA",
            ],
            "target_used_only_for_posterior_coverage_test": True,
        },
        "N69_reader_universe": {
            "comparison_visible_distinct": len(n69["visible"]),  # type: ignore[arg-type]
            "comparison_Witt_dual_distinct": len(n69["dual"]),  # type: ignore[arg-type]
            "comparison_union_distinct": len(comparison69),
            "affine_Witt_dual_plus_phase_distinct": len(affine69),
            "total_distinct": len(total69),
            "S8_is_contained": True,
            "comparison_missing_from_S8": sorted(target - comparison69),
            "affine_incidence_with_S8": sorted(target & affine69),
            "target_occurrences_after_family_construction": target_occurrences,
            "eight_subsets_left_by_membership_alone": ambiguity,
            "minimum_binary_label_length_for_an_arbitrary_eight_subset":
                math.ceil(math.log2(ambiguity)),
        },
        "N72_domain_obstruction": {
            "audited_times": n72["times"],
            "alignment": "la salida de la puerta t coincide con B_(t+1) de N69",
            "actual_branch_words_distinct": len(n72["actual_words"]),  # type: ignore[arg-type]
            "comparison_outputs_distinct": len(n72["comparison"]),  # type: ignore[arg-type]
            "affine_outputs_distinct": len(n72["affine"]),  # type: ignore[arg-type]
            "total_available_words_distinct": len(n72_total),
            "S8_intersection": sorted(n72_intersection),
            "S8_absent_from_entire_N72_image": sorted(n72_missing),
            "exact_no_go": (
                "todo selector construido únicamente restringiendo tiempos, fases, "
                "profundidades de resolución o ramas de la ventana N72 tiene imagen "
                "contenida en estas 172 palabras; no puede producir las cuatro "
                "palabras ausentes y, por tanto, no puede seleccionar S8"
            ),
        },
        "N74_monodromy_obstruction": {
            "returns_tested": len(n74_rows),
            "phase_returns_after_nine": True,
            "all_return_pairs_change_phi": True,
            "all_return_pairs_change_pi_plus_e": True,
            "conclusion": (
                "la clase de fase módulo nueve no determina la frontera; no es lícito "
                "prolongar N72 repitiendo su perfil por periodicidad"
            ),
        },
        "coinductive_reader_panel": {
            "indexed_entries": panel["indexed"],
            "distinct_words": len(panel_set),
            "rank_over_F3": panel["rank"],
            "linear_span_size": 3 ** int(panel["rank"]),
            "direct_intersection_with_S8": sorted(target & panel_set),
            "cyclic_orbit_size": len(cyclic),
            "cyclic_intersection_with_S8": sorted(target & cyclic),
            "Witt_orbit_size": len(witt_set),
            "Witt_intersection_with_S8": sorted(target & witt_set),
            "cyclic_Witt_orbit_size": len(combined),
            "cyclic_Witt_intersection_with_S8": sorted(target & combined),
            "conclusion": (
                "el panel fija las fronteras funcionales posteriores, pero ni su "
                "pertenencia, ni sus rotaciones, ni su órbita Witt seleccionan S8; "
                "su envolvente lineal es todo F3^6"
            ),
        },
        "minimal_additional_object": {
            "type": "sección coinductiva monodrómica sensible a la memoria",
            "domain": "estados TPK enriquecidos con frontera, fase, acarreo, hoja y orientación",
            "codomain": "incidencias indexadas de los lectores N69",
            "required_properties": [
                "prolongar el selector de supervivencia más allá de t=25",
                "distinguir estados con la misma fase y distinta memoria de retorno",
                "seleccionar ocho incidencias sin leer W72, K ni sus cifras",
                "conservar la posición de cada incidencia para el ensamblaje dodecafásico",
            ],
            "why_a_plain_set_is_insufficient": (
                "la corona excepcional y el bosque actúan sobre posiciones; un "
                "multiconjunto sin mapa de incidencia no puede acoplarse a ellos"
            ),
        },
        "proof_strength": {
            "N69_cardinalities": "EXACTO_INTERNO relativo al ledger N69 publicado",
            "N72_domain_no_go": "EXACTO_INTERNO relativo a la ventana publicada t=5,...,25",
            "N74_nonperiodicity": "EXACTO_INTERNO para los nueve retornos publicados",
            "global_infinite_selector": "no construido por estos archivos",
        },
        "provenance": {
            "architecture": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "N69_and_N72_recovery": "RESULTADO_RECUPERADO",
            "typed_domain_no_go": "FORMALIZACION_NUEVA",
            "exhaustive_counts": "CERTIFICADO_NUEVO",
        },
        "sources_sha256": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in (N69, N72, N74, COINDUCTIVE_READERS)
        },
        "execution": {
            "assert_statements_in_this_verifier": 0,
            "optimized_mode_safe": True,
        },
    }


def render(result: dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-json", type=Path)
    parser.add_argument("--check-certificate", action="store_true")
    args = parser.parse_args()
    payload = render(build_result())
    if args.emit_json is not None:
        args.emit_json.write_text(payload, encoding="utf-8")
    if args.check_certificate:
        require(OUT.exists(), "no existe el certificado congelado")
        require(OUT.read_text(encoding="utf-8") == payload,
                "el certificado no es reproducible")
    print("PASS — N71/N72 no seleccionan intrínsecamente los ocho bloques")


if __name__ == "__main__":
    main()
