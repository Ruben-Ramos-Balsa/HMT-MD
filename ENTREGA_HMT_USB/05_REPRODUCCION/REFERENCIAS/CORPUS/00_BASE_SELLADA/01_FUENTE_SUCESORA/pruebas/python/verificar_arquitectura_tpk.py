#!/usr/bin/env python3
"""Verifica la cobertura operatoria APP--TRIT--TPK de la publicación.

La prueba combina tres clases de control: tipos declarados en el registro,
invariantes ejecutables de las rutas y de la monodromía, y presencia causal
de los objetos en el manuscrito. No usa la instrucción assert y produce un
certificado JSON determinista.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datos"
MANUSCRIPT = ROOT / "manuscrito"
OUTPUT = ROOT / "certificados" / "arquitectura_operatoria_tpk.json"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def read_json(path: Path) -> Any:
    require(path.is_file(), f"archivo ausente: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    registry_path = DATA / "registro_operadores_tpk.json"
    route_path = DATA / "rutas_tres_pasos_162_estados.json"
    monodromy_path = DATA / "monodromia_nonadica.json"
    dynamics_path = DATA / "dinamica_cociente_468.json"
    atlas_path = ROOT / "certificados" / "atlas_genealogia_masas.json"

    registry = read_json(registry_path)
    routes = read_json(route_path)
    monodromy = read_json(monodromy_path)
    dynamics = read_json(dynamics_path)
    atlas = read_json(atlas_path)

    require(
        registry.get("canonical_revision") == "2026-07-22.2",
        "revisión canónica incorrecta",
    )
    operators = registry.get("operators")
    require(isinstance(operators, list), "lista de operadores ausente")
    ids = [entry.get("id") for entry in operators]
    require(len(ids) == len(set(ids)), "identificadores de operador repetidos")

    mandatory = {
        "APP_A9",
        "APP_BIVARIATE_PATH_CATEGORY",
        "APP_RHO9_QUOTIENT",
        "TRIT_RHO3",
        "BASE1000_CONCAT",
        "CARDINAL_TRANSLATIONS",
        "TPK_LOCAL_FEEDBACK",
        "OBSERVABLE_TWO_CURSOR_CHRONOLOGY",
        "ROUTE_3_SURJECTIVITY",
        "TPK_MIN_TWO_CURSOR",
        "TPK_SIGNATURE_COMBINER",
        "DECIMAL_TRIAD_ALPHABET",
        "TPK_W6_PROJECTION",
        "TPK_FULL_STATE",
        "ENRICHED_FIBRE_EXTENSION",
        "HENSEL_STATE_TRANSITION",
        "CYLINDER_BASE1000_TRANSITION",
        "BOUNDARY_SIGNATURE",
        "PHASE_BIASED_FIBRE_TRANSFER",
        "SEED_TURN_REFINEMENT",
        "TPK_MODE_ORIENTATION_COCYCLES",
        "EF_G9_EXTENSION_RELATION",
        "NONADIC_MONODROMY",
        "THREE_CHANNEL_TWENTY_BLOCK_EXTENSION",
        "HMT_NUMBER_INVERSE_LIMIT",
        "R12_DODECAPHASE",
        "SIGNED_U12_READOUT",
        "HADAMARD_K_U12",
        "TRANSVERSE_D3_D4_Q",
        "ALPHA_BASE1000_CLOSURE",
        "ROUTE_LEDGER_CHARACTER",
        "INDEX12_TWO_WAY_LATTICE",
        "NONADIC_PARTICLE_FAMILY_ATLAS",
    }
    require(
        mandatory <= set(ids),
        f"operadores obligatorios ausentes: {sorted(mandatory-set(ids))}",
    )
    required_fields = {
        "id",
        "academic_name",
        "symbol",
        "historical_aliases",
        "layer",
        "domain",
        "codomain",
        "transition",
        "invariants",
        "status",
        "sources",
    }
    for entry in operators:
        missing = required_fields - set(entry)
        require(not missing, f"{entry.get('id')}: campos ausentes {sorted(missing)}")
        require(entry["sources"], f"{entry['id']}: sin fuente local")
        require(entry["invariants"], f"{entry['id']}: sin invariantes")

    trace_types = registry.get("trace108_types")
    require(
        isinstance(trace_types, list) and len(trace_types) == 10,
        "no hay diez tipos de traza 108",
    )
    require(
        len({entry["id"] for entry in trace_types}) == 10,
        "tipos de traza 108 repetidos",
    )

    stats = routes["stats"]
    require(stats["num_states"] == 162, "censo cardinal distinto de 162")
    require(
        stats["min_count"] == 8 and stats["max_count"] == 40,
        "rango de testigos incorrecto",
    )
    require(
        stats["all_digits_reachable_from_every_state"] is True,
        "fallo de sobreyectividad local",
    )
    witness = routes["witness"]
    require(len(witness) == 162, "tabla de testigos incompleta")
    for state, targets in witness.items():
        require(set(targets) == {"0", "1", "2"}, f"{state}: faltan trits objetivo")
        for target, item in targets.items():
            route = item["route"]
            require(
                len(route) == 3 and set(route) <= set("NESO"),
                f"{state}/{target}: ruta inválida",
            )
            require(
                8 <= item["count"] <= 40,
                f"{state}/{target}: multiplicidad inválida",
            )

    require(monodromy["status"] == "PASS", "certificado nonádico no pasa")
    recurrence = monodromy["residue_quotient_recurrence"]
    require(recurrence["matrix_determinant"] == 1, "matriz Hensel no unimodular")
    require(
        recurrence["division_identity_verified_steps"] == 60,
        "faltan identidades residuo-cociente",
    )
    require(recurrence["published_blocks_verified"] == 60, "faltan bloques publicados")
    gate = monodromy["gate_9_to_1"]
    require(
        gate["survivors_h1"] == 3 and gate["survivors_h2"] == 1,
        "supervivencia 3->1 incorrecta",
    )
    require(gate["fixed_phi_axis"] == "112002", "eje phi incorrecto")
    require(gate["fixed_pi_plus_e"] == "210110", "agregado pi+e incorrecto")
    require(
        len(monodromy["phase_returns"]["verified_returns"]) == 9,
        "faltan retornos de fase",
    )
    blocks = monodromy["twenty_block_branch"]
    require(
        all(len(blocks[channel]) == 20 for channel in ("pi", "e", "phi")),
        "rama de veinte bloques incompleta",
    )
    reading = monodromy["archimedean_reading"]
    require(
        all(len(reading[channel]["decimal_triads"]) == 12 for channel in ("pi", "e", "phi")),
        "lector de doce tríadas incompleto",
    )
    require(
        monodromy["beatty_calendar"]["gap_set"] == [21, 22],
        "calendario 21/22 incorrecto",
    )

    raw = dynamics["raw_chronology"]
    require(
        raw["positions_and_orientations_return_after_ticks"] == 54,
        "retorno observable de 54 incorrecto",
    )
    require(
        raw["full_phase_return_after_ticks"] == 108,
        "retorno de fase de 108 incorrecto",
    )
    phase = dynamics["phase_skew_transfer"]
    require(
        phase["doubly_stochastic"] is True and phase["irreducible"] is True,
        "transferencia de fase inválida",
    )
    require(phase["period"] == 9, "periodo de transferencia distinto de nueve")
    require(
        phase["nine_step_return"] == "E_plus*E_times; every U6 entry is 1/468",
        "retorno uniforme incorrecto",
    )
    memory = dynamics["route_memory"]
    require(
        memory["advance_half_turn_refinement_classes"] == 28,
        "refinamiento P,H incorrecto",
    )
    require(
        memory["advance_quarter_turn_refinement_classes"] == 162,
        "refinamiento P,Q incorrecto",
    )
    require(
        memory["exceptional_555555_sheets"] == 3,
        "la firma 555555 no tiene tres hojas",
    )
    require(
        memory["type_separation"]["same_object"] is False,
        "se confundió R36 con 504-468",
    )
    cocycles = dynamics["calendar_cocycles"]
    require(cocycles["total_variation_per_108"] == 72, "cociclo de modo incorrecto")
    require(
        cocycles["orientation_reversals_per_108"] == 4,
        "cociclo de orientación incorrecto",
    )
    require(cocycles["signed_sum_per_108"] == 0, "suma firmada incorrecta")

    atlas_data = atlas["atlas"]
    require(
        atlas["status"] == "PASS_TYPED_ATLAS_AND_GENEALOGY_AUDIT",
        "atlas de familias no pasa",
    )
    require(atlas_data["cells"] == 81, "atlas distinto de 81 celdas")
    center = atlas_data["center"]
    require(
        center.get("r") == 5 and center.get("c") == 5,
        "centro electrónico incorrecto",
    )
    sector_counts = atlas_data["sector_counts"]
    require(sum(sector_counts.values()) == 81, "sectores del atlas no suman 81")
    require(
        sorted(atlas_data["quark_color_counts"].values()) == [12, 12, 12],
        "clases de color no uniformes",
    )

    # Orden causal del manuscrito unificado. Los prefijos ``hmt/`` y ``md/``
    # forman parte de la ruta pública y evitan depender de los alias de las
    # ediciones breves anteriores.
    source_order = (
        "hmt/03_app_ortograma",
        "hmt/02_trit_geometrias",
        "hmt/03c_nucleo_transporte",
        "hmt/20_arquitectura_operatoria_tpk_actualizada",
        "hmt/03b_alfabeto_factorizacion",
        "hmt/05_tpk_numero_medicion",
        "hmt/05b_extensiones_dinamica_cociente",
        "hmt/14_numero_heisenberg_y_d108",
        "hmt/08_dodecafase_alpha",
        "md/05b_extension_superviviente_caracter",
        "md/06b_atlas_especies_genealogia_masas",
    )
    main_text = (MANUSCRIPT / "main.tex").read_text(encoding="utf-8")
    positions = []
    manuscript_parts = [main_text]
    for stem in source_order:
        token = f"\\input{{sections/{stem}}}"
        require(token in main_text, f"sección no incluida: {stem}")
        positions.append(main_text.index(token))
        section = MANUSCRIPT / "sections" / f"{stem}.tex"
        require(section.is_file(), f"fuente ausente: {stem}")
        manuscript_parts.append(section.read_text(encoding="utf-8"))
    require(positions == sorted(positions), "orden causal de secciones incorrecto")
    manuscript_text = "\n".join(manuscript_parts)
    anchors = (
        "\\mathsf P_{\\rm APP}^{(2)}",
        "\\Theta_{108}",
        "F_{\\rm obs}^{108}=I",
        "42\\) tríadas",
        "\\operatorname{Ext}_r",
        "\\mathcal K_{\\rm ph}",
        "504=468+36",
        "veinte bloques",
        "\\varprojlim_m",
        "U_{12}^{\\rm sgn}",
        "(D_3K,D_4K,Q)",
        "\\chi_{\\rm mass}",
        "81=25_{\\ell^-}+20_{\\nu}+20_{d\\text{-tipo}}+16_{u\\text{-tipo}}",
    )
    for anchor in anchors:
        require(anchor in manuscript_text, f"ancla semántica ausente: {anchor}")
    forbidden = (
        "upstream",
        "target-free",
        "TPK carece de genealogía",
        "la partícula escoge una ruta",
        "R_{36}=504-468",
    )
    for phrase in forbidden:
        require(phrase not in manuscript_text, f"regresión textual: {phrase}")

    result = {
        "schema": "HMT.tpk.publication_coverage.v1",
        "status": "PASS_ARQUITECTURA_OPERATORIA_TPK",
        "canonical_revision": registry["canonical_revision"],
        "operators_checked": len(operators),
        "mandatory_operators": len(mandatory),
        "trace108_types": len(trace_types),
        "route_states": stats["num_states"],
        "route_target_cases": stats["num_states"] * 3,
        "monodromy_returns": len(monodromy["phase_returns"]["verified_returns"]),
        "published_trit_blocks": recurrence["published_blocks_verified"],
        "particle_atlas_cells": atlas_data["cells"],
        "semantic_anchors": len(anchors),
        "inputs_sha256": {
            path.relative_to(ROOT).as_posix(): digest(path)
            for path in (registry_path, route_path, monodromy_path, dynamics_path, atlas_path)
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
