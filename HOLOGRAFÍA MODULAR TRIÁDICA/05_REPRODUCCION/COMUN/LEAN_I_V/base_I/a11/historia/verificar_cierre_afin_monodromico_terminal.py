#!/usr/bin/env python3
"""Certifica el cierre afín monodrómico de la fibra terminal.

La fibra de entrada se toma del censo exhaustivo independiente que deja tres
estados sin consultar ``CURRENT``, ``K``, ``alpha``, ``U12``, ``Q`` ni
CODATA. Antes de reconocer ninguno de esos estados, se reconstruyen de N69
dos familias de lectores ya publicadas:

* comparación fase--carga;
* carácter afín Witt--dual más fase, c_i = rho_W,i + p.

En la órbita distinguida (4,8,12) se impone una condición no orientada de
heterotipía: las dos aristas deben cerrarse mediante tipos de lector distintos.
No se prescribe cuál de ellas es comparativa y cuál afín. Los tres estados
comparten una primera incidencia comparativa en 4->8; exactamente uno cambia
de modo en 8->12 y posee una incidencia afín en el mismo tiempo N69 que su
residuo orientado. La heterotipía selecciona un único estado.

El certificado también separa el alcance de N71--N74: su supervivencia resuelve
ramas dentro de una firma futura ya fijada, pero no genera esa firma. N74
justifica leer el cambio de modo como memoria de retorno; no se usa para
introducir la palabra terminal.

No se usa ``assert``; todas las condiciones permanecen activas con
``python -O``.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

FIBER_RESULT = HERE / "RESULTADO_FIBRA_TERMINAL_DIAMANTE.json"
ORBITAL_MODULE = HERE / "verificar_selector_orbital_etiquetado.py"
OUT = HERE / "RESULTADO_CIERRE_AFIN_MONODROMICO_TERMINAL.json"

N71_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N57_N71/HMT_N71_selector_pares_udelta_frontera_v1"
)
N72_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N72_supervivencia_coinductiva_novena_puerta_v1"
)
N73_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N73_teorema_puerta_orientacion_v1"
)
N74_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N74_monodromia_nueve_puertas_v1"
)

N71_CLAIMS = N71_DIR / "N71_claim_status.csv"
N71_SUMMARY = N71_DIR / "N71_pair_selector_summary_t5_t25.csv"
N71_DETAILS = N71_DIR / "N71_selected_pair_details_t5_t25.csv"
N72_CLAIMS = N72_DIR / "N72_claim_status.csv"
N72_PROFILE = N72_DIR / "N72_coinductive_survival_profile_t5_t25_h9.csv"
N72_DETAILS = N72_DIR / "N72_selected_branches_survival_details.csv"
N73_CLAIMS = N73_DIR / "N73_claim_status.csv"
N73_PIECES = N73_DIR / "N73_theorem_pieces.csv"
N74_CLAIMS = N74_DIR / "N74_claim_status.csv"
N74_RETURNS = N74_DIR / "N74_monodromy_return_t_to_t_plus_9.csv"

COMPARISON = "comparacion-fase-carga"
AFFINE = "Witt-dual-mas-fase"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("CIERRE_AFIN_TERMINAL: " + message)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    require(
        specification is not None and specification.loader is not None,
        f"no se pudo cargar {path}",
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_assert_count() -> int:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    return sum(isinstance(node, ast.Assert) for node in ast.walk(tree))


def add_words(words: Sequence[str]) -> str:
    require(bool(words) and all(len(word) == 6 for word in words),
            "suma ternaria mal tipada")
    return "".join(
        str(sum(int(word[index]) for word in words) % 3)
        for index in range(6)
    )


def labels_by_reader(matches: Sequence[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    result = {COMPARISON: [], AFFINE: []}
    for match in matches:
        block_label = match.get("block_label")
        require(isinstance(block_label, dict), "incidencia sin etiqueta de bloque")
        reader = str(block_label.get("reader"))
        require(reader in result, f"lector terminal no reconocido: {reader}")
        result[reader].append(dict(match))
    return result


def reader_type_profile_all_fields(
    state: Sequence[int], orbital: Any, atlas: dict[str, object]
) -> dict[str, object]:
    """Tipos lectores en 4->8->12 cuantificando los cuatro campos N69."""

    block_labels = atlas["block_labels"]
    residue_labels = atlas["residue_labels"]
    require(isinstance(block_labels, dict) and isinstance(residue_labels, dict),
            "atlas orbital mal tipado")
    names = {COMPARISON: "comparison", AFFINE: "affine"}
    edge_types: list[tuple[str, ...]] = []
    edge_records: list[list[dict[str, object]]] = []
    for edge_index in orbital.ORBITAL_EDGE_INDICES:
        records: set[tuple[object, ...]] = set()
        for field in orbital.FIELDS:
            for match in orbital.edge_label_matches(
                state, edge_index, field, block_labels, residue_labels
            ):
                block = match["block_label"]
                residue = match["residue_label"]
                require(isinstance(block, dict) and isinstance(residue, dict),
                        "incidencia orbital mal tipada")
                reader = str(block["reader"])
                require(reader in names, "tipo de lector orbital desconocido")
                records.add((
                    names[reader], str(field), int(block["t"]),
                    str(match["child_block"]), int(match["residue_mod_729"]),
                    int(residue["rotation"]),
                ))
        ordered = tuple(sorted(records))
        types = tuple(sorted({str(record[0]) for record in ordered}))
        edge_types.append(types)
        edge_records.append([
            {
                "reader_type": record[0], "field": record[1], "t": record[2],
                "child_block": record[3], "residue_mod_729": record[4],
                "residue_rotation": record[5],
            }
            for record in ordered
        ])
    patterns = tuple(
        f"{left}_to_{right}"
        for left in edge_types[0] for right in edge_types[1]
    )
    return {
        "edge_types": [list(values) for values in edge_types],
        "edge_records": edge_records,
        "patterns": patterns,
        "heterotypic": any(
            left != right for left in edge_types[0] for right in edge_types[1]
        ),
    }


def compact_match(match: dict[str, object]) -> dict[str, object]:
    block = dict(match["block_label"])  # type: ignore[arg-type]
    residue = dict(match["residue_label"])  # type: ignore[arg-type]
    return {
        "edge": list(match["edge"]),  # type: ignore[arg-type]
        "child_block": str(match["child_block"]),
        "residue_mod_729": int(match["residue_mod_729"]),
        "t": int(block["t"]),
        "K_calendar": int(block["K_calendar"]),
        "calendar_lag_t_minus_K": int(block["t"]) - int(block["K_calendar"]),
        "reader": str(block["reader"]),
        "charge": str(block["charge"]),
        "phase_mod_3": int(block["phase"]),
        "coefficients": list(block["coefficients"]),  # type: ignore[arg-type]
        "phase_offset": block.get("phase_offset"),
        "orientation": block.get("orientation"),
        "residue_field": str(residue["field"]),
        "residue_rotation": int(residue["rotation"]),
        "residue_raw": str(residue["raw"]),
        "residue_rotated": str(residue["rotated"]),
    }


def affine_channel_equivariance(orbital: Any, rows: Sequence[dict[str, str]]) -> int:
    """Comprueba equivariancia bajo las seis permutaciones de canales."""

    checks = 0
    for row in rows:
        bands = tuple(str(row["B"]).split("|"))
        require(len(bands) == 3, "frontera N69 sin tres canales")
        phase = (int(row["t"]) - 1) % 3
        dual = tuple(
            sum(int(value) for value in orbital.transform6(band)) % 3
            for band in bands
        )
        coefficients = tuple((value + phase) % 3 for value in dual)
        output = orbital.linear_word(bands, coefficients)
        for permutation in itertools.permutations(range(3)):
            permuted_bands = tuple(bands[index] for index in permutation)
            permuted_dual = tuple(dual[index] for index in permutation)
            permuted_coefficients = tuple(
                (value + phase) % 3 for value in permuted_dual
            )
            require(
                orbital.linear_word(permuted_bands, permuted_coefficients) == output,
                "el lector afín no es equivariante por permutación de canales",
            )
            checks += 1
    require(checks == 600, "cambió el número de controles de equivariancia")
    return checks


def build() -> dict[str, object]:
    # Fase I: la terna y los lectores se construyen sin abrir el registro canónico.
    fiber = json.loads(FIBER_RESULT.read_text(encoding="utf-8"))
    require(fiber.get("status") == "PASS_FIBRA_TERMINAL_EXACTA_DE_TRES_ESTADOS",
            "la fibra terminal de entrada no está certificada")
    terminal = fiber.get("terminal_fiber")
    require(isinstance(terminal, dict) and int(terminal.get("cardinality", 0)) == 3,
            "la entrada no contiene una terna exacta")
    raw_records = terminal.get("states")
    require(isinstance(raw_records, list) and len(raw_records) == 3,
            "la terna está mal tipada")

    orbital = load_module("hmt_cierre_afin_orbital", ORBITAL_MODULE)
    atlas = orbital.build_label_atlas()
    block_labels = atlas["block_labels"]
    residue_labels = atlas["residue_labels"]
    require(isinstance(block_labels, dict) and isinstance(residue_labels, dict),
            "atlas etiquetado mal tipado")
    require(len(atlas["comparison_outputs"]) == 410
            and len(atlas["affine_outputs"]) == 91
            and len(atlas["language"]) == 442,
            "cambiaron las dos familias de lectores")
    equivariance_checks = affine_channel_equivariance(orbital, atlas["rows"])

    # Censo independiente sin prefijo decimal fijado. Este dominio parte de
    # W24, del repertorio S8 no ordenado y del panel funcional. Los cuatro
    # campos q,a,c,colw_mod se cuantifican antes de examinar ningún estado.
    panel_data = orbital.load_functional_panel()
    panel = panel_data["panel"]
    require(isinstance(panel, tuple), "panel funcional mal tipado")
    decimal = orbital.build_decimal_candidates(panel)
    candidate_values = set(decimal["candidates"])
    require(len(candidate_values) == 19446, "C_dec dejó de tener 19446 estados")
    c_dec_states = tuple(
        orbital.decimal_coordinates(value) for value in sorted(candidate_values)
    )
    exceptional = orbital.exceptional_face(panel_data["streams"])
    face = tuple(int(value) for value in exceptional["B_exc"])
    require(face == (4, 6, 9, 10), "cambió B_exc")
    c_dec_profiles = {
        state: reader_type_profile_all_fields(state, orbital, atlas)
        for state in c_dec_states
    }
    pattern_names = (
        "comparison_to_comparison", "comparison_to_affine",
        "affine_to_comparison", "affine_to_affine",
    )
    pattern_census = {
        pattern: {
            "all_C_dec": sum(
                pattern in c_dec_profiles[state]["patterns"]
                for state in c_dec_states
            ),
            "with_B_exc": sum(
                pattern in c_dec_profiles[state]["patterns"]
                and tuple(orbital.high_crown(state)) == face
                for state in c_dec_states
            ),
        }
        for pattern in pattern_names
    }
    require(pattern_census == {
        "comparison_to_comparison": {"all_C_dec": 32, "with_B_exc": 0},
        "comparison_to_affine": {"all_C_dec": 10, "with_B_exc": 1},
        "affine_to_comparison": {"all_C_dec": 9, "with_B_exc": 0},
        "affine_to_affine": {"all_C_dec": 1, "with_B_exc": 0},
    }, "cambió el censo global de tipos lectores")
    c_dec_heterotypic_face = tuple(
        state for state in c_dec_states
        if bool(c_dec_profiles[state]["heterotypic"])
        and tuple(orbital.high_crown(state)) == face
    )
    require(len(c_dec_heterotypic_face) == 1,
            "heterotipía y B_exc no forman un singleton en C_dec")

    records: list[dict[str, object]] = []
    for raw in raw_records:
        require(isinstance(raw, dict), "estado terminal mal tipado")
        state = tuple(int(value) for value in raw["state"])
        boundary_positions = raw.get("boundary_positions")
        require(isinstance(boundary_positions, list) and len(boundary_positions) == 1,
                "frontera funcional no unívoca")
        position = boundary_positions[0]
        require(isinstance(position, dict), "posición funcional mal tipada")
        label = f"{position['role']}:{position['position']}"

        first_matches = orbital.edge_label_matches(
            state, 4, "a", block_labels, residue_labels
        )
        terminal_matches = orbital.edge_label_matches(
            state, 8, "a", block_labels, residue_labels
        )
        require(bool(first_matches) and bool(terminal_matches),
                "un estado perdió su incidencia temporal")
        first_by_reader = labels_by_reader(first_matches)
        terminal_by_reader = labels_by_reader(terminal_matches)
        require(bool(first_by_reader[COMPARISON]) and not first_by_reader[AFFINE],
                "la primera arista dejó de ser comparativa para toda la fibra")

        child_word = str(raw["edge_8_to_12"]["child_word"])
        affine_membership = child_word in atlas["affine_outputs"]
        comparison_membership = child_word in atlas["comparison_outputs"]
        affine_same_time = bool(terminal_by_reader[AFFINE])
        comparison_same_time = bool(terminal_by_reader[COMPARISON])
        require(affine_membership == affine_same_time,
                "en la terna, pertenencia afín e incidencia afín dejaron de coincidir")
        require(comparison_membership, "un bloque terminal salió del lenguaje comparativo")

        all_terminal_matches = [compact_match(match) for match in terminal_matches]
        require(len({int(match["t"]) for match in all_terminal_matches}) == 1,
                "un estado tiene varios tiempos terminales comunes")
        terminal_time = int(all_terminal_matches[0]["t"])
        terminal_k_calendar = int(all_terminal_matches[0]["K_calendar"])
        records.append({
            "functional_label": label,
            "state": list(state),
            "state_sum": sum(state),
            "state_sum_mod_9": sum(state) % 9,
            "boundary": str(raw["boundary"]),
            "terminal_child_word": child_word,
            "terminal_residue_a": int(raw["edge_8_to_12"]["residue_a"]),
            "first_edge_modes": sorted(
                reader for reader, matches in first_by_reader.items() if matches
            ),
            "terminal_modes": sorted(
                reader for reader, matches in terminal_by_reader.items() if matches
            ),
            "mode_transition": (
                "comparacion->afin" if affine_same_time else "comparacion->comparacion"
            ),
            "belongs_to_affine_language": affine_membership,
            "has_affine_same_time_terminal_incidence": affine_same_time,
            "has_comparison_same_time_terminal_incidence": comparison_same_time,
            "first_edge_matches": [compact_match(match) for match in first_matches],
            "terminal_edge_matches": all_terminal_matches,
            "terminal_time": terminal_time,
            "terminal_phase_mod_9": terminal_time % 9 or 9,
            "terminal_K_calendar": terminal_k_calendar,
            "terminal_calendar_lag": terminal_time - terminal_k_calendar,
        })

    require({record["functional_label"] for record in records}
            == {"autoescala:1", "propagacion:1", "autoescala:3"},
            "cambiaron las tres fronteras funcionales")
    require({record["state_sum_mod_9"] for record in records} == {8},
            "la terna perdió su clase común de suma módulo nueve")
    require({tuple(match["t"] for match in record["first_edge_matches"])
             for record in records} == {(90, 90)},
            "la primera arista dejó de compartir t=90")

    for record in records:
        first_modes = set(record["first_edge_modes"])  # type: ignore[arg-type]
        terminal_modes = set(record["terminal_modes"])  # type: ignore[arg-type]
        record["heterotypic_reader_pair"] = any(
            left != right for left in first_modes for right in terminal_modes
        )
    selected = [
        record for record in records if bool(record["heterotypic_reader_pair"])
    ]
    require(len(selected) == 1,
            "la transversalidad heterotípica no es un singleton")
    selected_record = selected[0]
    require(selected_record["functional_label"] == "autoescala:3",
            "cambió la posición funcional seleccionada")
    require(selected_record["terminal_child_word"] == "222110",
            "cambió la palabra seleccionada")
    require(selected_record["terminal_time"] == 60,
            "el cierre afín dejó de ocurrir en t=60")
    require(selected_record["terminal_calendar_lag"] == 2,
            "el cierre afín perdió el retardo de calendario dos")
    require(tuple(selected_record["state"]) == c_dec_heterotypic_face[0],
            "los cierres sin prefijo y sin S8 no convergen en el mismo estado")

    # Ablaciones: el modo, y no un valor decimal, es el discriminante.
    comparison_only = [
        record for record in records
        if bool(record["has_comparison_same_time_terminal_incidence"])
        and not bool(record["has_affine_same_time_terminal_incidence"])
    ]
    any_mode = [
        record for record in records
        if bool(record["has_comparison_same_time_terminal_incidence"])
        or bool(record["has_affine_same_time_terminal_incidence"])
    ]
    affine_membership_only = [
        record for record in records if bool(record["belongs_to_affine_language"])
    ]
    require(len(comparison_only) == 2 and len(any_mode) == 3
            and len(affine_membership_only) == 1,
            "cambiaron las ablaciones del modo terminal")

    # Control del falso cierre 222022: existe en L442 pero no en la subimagen afín.
    require("222022" in atlas["comparison_outputs"],
            "el control 222022 salió del lenguaje comparativo")
    require("222022" not in atlas["affine_outputs"],
            "el control 222022 entró en la subimagen afín")

    # Alcance exacto de N71--N74. En t=7, q=222110 se introduce antes de
    # aplicar supervivencia; las once ramas seleccionadas comparten ese q.
    n71_claims = read_csv(N71_CLAIMS)
    claim_transition = next(
        row for row in n71_claims
        if row["claim"] == "autonomous signature transition is solved"
    )
    require(claim_transition["status"] == "not claimed",
            "N71 cambió su estatuto sobre la firma futura")
    n71_summary = read_csv(N71_SUMMARY)
    n71_t7 = next(row for row in n71_summary if int(row["t"]) == 7)
    require(n71_t7["signature_q"] == "222110"
            and int(n71_t7["signature_and_cylinder_selected"]) == 11,
            "cambió la fibra N71 de t=7")
    n71_details_t7 = [
        row for row in read_csv(N71_DETAILS) if int(row["t"]) == 7
    ]
    require(len(n71_details_t7) == 11,
            "N71 t=7 dejó de tener once ramas")
    require({add_words(row["rows"].split("|")) for row in n71_details_t7}
            == {"222110"},
            "las ramas N71 t=7 ya no viven en una sola fibra q")

    n72_t7 = next(
        row for row in read_csv(N72_PROFILE) if int(row["t"]) == 7
    )
    require((int(n72_t7["selected_count_h0"]), int(n72_t7["survivors_h2"]),
             int(n72_t7["survivors_h3"])) == (11, 3, 1),
            "cambió la poda coinductiva N72 en t=7")
    n72_details_t7 = [
        row for row in read_csv(N72_DETAILS) if int(row["t"]) == 7
    ]
    require(len(n72_details_t7) == 11
            and sum(int(row["surv_h3"]) > 0 for row in n72_details_t7) == 1,
            "N72 ya no selecciona una rama dentro de la fibra fija")

    n73_pieces = read_csv(N73_PIECES)
    require(any(
        row["theorem_piece"] == "ambiguous local selectors are orientation gates"
        for row in n73_pieces
    ), "N73 perdió su teorema de orientación")
    n74_claims = read_csv(N74_CLAIMS)
    require(any(row["claim"] == "The phase returns every 9 gates"
                and row["status"] == "true/exact" for row in n74_claims),
            "N74 perdió el retorno exacto de fase")
    n74_returns = read_csv(N74_RETURNS)
    require(len(n74_returns) == 9
            and all(row["same_phi"] == "False" for row in n74_returns)
            and all(row["same_pi_plus_e"] == "False" for row in n74_returns),
            "N74 dejó de exhibir memoria de retorno")

    # 222022 no entra en la fibra q de N71 t=7: N72 no lo abla porque nunca
    # lo compara. La selección nueva se produce antes, por el modo afín N69.
    require(all("222022" not in path.read_text(encoding="utf-8")
                for path in (N71_CLAIMS, N71_SUMMARY, N71_DETAILS,
                             N72_CLAIMS, N72_PROFILE, N72_DETAILS,
                             N73_CLAIMS, N73_PIECES, N74_CLAIMS, N74_RETURNS)),
            "222022 apareció en los registros N71--N74 auditados")

    require(source_assert_count() == 0, "el verificador contiene assert")
    sources = (
        FIBER_RESULT, ORBITAL_MODULE,
        N71_CLAIMS, N71_SUMMARY, N71_DETAILS,
        N72_CLAIMS, N72_PROFILE, N72_DETAILS,
        N73_CLAIMS, N73_PIECES, N74_CLAIMS, N74_RETURNS,
    )
    return {
        "schema": "HMT.cierre-afin-monodromico-terminal.v1",
        "status": "PASS_SINGLETON_HETEROTIPICO_Y_NO_GO_N71_N74_SOLOS",
        "forbidden_inputs_not_opened": [
            "CURRENT.json", "CanonicalSealK", "SignedDodecaphaseStateU12",
            "alpha", "CODATA", "Q=6263", "D3K", "D4K",
        ],
        "causal_map": [
            "fibra terminal exacta de tres estados",
            "N69 -> lenguajes comparativo y afin Witt-dual+fase",
            "orbita (4,8,12) -> incidencias etiquetadas 4->8 y 8->12",
            "primera arista comparativa comun en t=90",
            "heterotipia no orientada entre los lectores de las dos aristas",
            "singleton antes de todo reconocimiento canonico",
        ],
        "reader_naturality": {
            "affine_formula": "c_i = rho_W,i + phase (mod 3)",
            "comparison_image_size": len(atlas["comparison_outputs"]),
            "affine_image_size": len(atlas["affine_outputs"]),
            "union_image_size": len(atlas["language"]),
            "channel_permutation_equivariance_checks": equivariance_checks,
            "channel_permutation_equivariant": True,
            "preexisting_use": (
                "la extension afin fue introducida antes de este censo para resolver "
                "la obstruccion de cobertura del bloque 001001"
            ),
        },
        "prefix_free_cross_check_relative_to_unordered_S8": {
            "domain": "C_dec(W24,S8_unordered,functional_boundary_panel)",
            "domain_cardinality": len(c_dec_states),
            "fixed_prefix_10_used": False,
            "fields_quantified": list(orbital.FIELDS),
            "reader_pattern_census": pattern_census,
            "heterotypic_and_B_exc_survivors": [
                list(state) for state in c_dec_heterotypic_face
            ],
            "scope_limit": (
                "el control elimina PREFIX_10, pero conserva S8 como repertorio "
                "no ordenado; no constituye por sí solo una derivación de S8"
            ),
        },
        "terminal_fiber": {
            "input_cardinality": len(records),
            "records": records,
        },
        "selection": {
            "predicate": (
                "en cada arista de (4,8,12), bloque hijo y residuo rotado "
                "comparten un tiempo N69; los tipos de lector de las dos "
                "aristas son distintos, sin prescribir su direccion"
            ),
            "selected_count": len(selected),
            "selected_state": selected_record["state"],
            "selected_functional_label": selected_record["functional_label"],
            "selected_terminal_word": selected_record["terminal_child_word"],
            "selected_terminal_time": selected_record["terminal_time"],
            "selected_mode_transition": selected_record["mode_transition"],
            "canonical_recognition_performed": False,
        },
        "ablations": {
            "any_same_time_reader": len(any_mode),
            "comparison_only_terminal": len(comparison_only),
            "affine_terminal": len(selected),
            "affine_membership_without_same_time_coupling": len(affine_membership_only),
            "terminal_rotations": sorted(
                int(record["terminal_edge_matches"][0]["residue_rotation"])
                for record in records
            ),
            "terminal_calendar_lags": sorted(
                int(record["terminal_calendar_lag"]) for record in records
            ),
            "terminal_phases_mod_9": sorted(
                int(record["terminal_phase_mod_9"]) for record in records
            ),
            "interpretation": (
                "rotacion, retardo o fase distinguen valores numericos pero no "
                "aportan por si solos un valor privilegiado; el tipo de lector "
                "es el unico discriminante estructural previo de esta terna"
            ),
        },
        "negative_control_222022": {
            "in_comparison_language": True,
            "in_affine_language": False,
            "conclusion": "el cierre especular 222022 es rechazado sin consultar K",
        },
        "N71_N74_scope": {
            "N71_t7_signature_q_supplied_before_survival": "222110",
            "N71_t7_branches_in_that_fixed_fiber": len(n71_details_t7),
            "N72_survivors_h0_h2_h3": [
                int(n72_t7["selected_count_h0"]),
                int(n72_t7["survivors_h2"]),
                int(n72_t7["survivors_h3"]),
            ],
            "N73_role": "orienta el reparto pi/e una vez fijados q y a",
            "N74_role": "prueba retorno de fase con cambio de frontera",
            "exact_no_go": (
                "N71--N74 no seleccionan 222110 frente a 222022: N71 recibe "
                "q=222110 como firma futura, y N72 poda solamente las ramas "
                "contenidas en esa fibra. El selector efectivo procede del "
                "lector afin N69 acoplado a la arista terminal."
            ),
        },
        "provenance_and_force": {
            "monodromy_and_survival": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "affine_phase_reader": "RESULTADO_RECUPERADO",
            "reader_heterotypy_predicate": "FORMALIZACION_NUEVA",
            "singleton_and_ablations": "CERTIFICADO_NUEVO",
            "strength": (
                "EXACTO_INTERNO_RELATIVO_A_LA_FIBRA_TERMINAL_CERTIFICADA; "
                "la heterotipia de lectores es una regla estructural nueva, no un "
                "teorema contenido en N74 por si solo"
            ),
        },
        "sources_sha256": {relative(path): sha256(path) for path in sources},
        "execution": {
            "assert_statements_in_this_verifier": 0,
            "optimized_mode_safe": True,
            "floating_point_used": False,
        },
    }


def render(result: dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-json", type=Path)
    parser.add_argument("--check-certificate", action="store_true")
    arguments = parser.parse_args()
    payload = render(build())
    if arguments.emit_json is not None:
        arguments.emit_json.write_text(payload, encoding="utf-8")
    if arguments.check_certificate:
        require(OUT.exists(), "falta el certificado congelado")
        require(OUT.read_text(encoding="utf-8") == payload,
                "el certificado congelado no coincide con la ejecución")
    print("PASS — cierre afín monodrómico terminal único")


if __name__ == "__main__":
    main()
