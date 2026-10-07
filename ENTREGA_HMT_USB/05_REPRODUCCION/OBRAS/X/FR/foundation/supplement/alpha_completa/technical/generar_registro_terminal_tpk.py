#!/usr/bin/env python3
"""Comprueba auxiliarmente la carta modular downstream desde ``C_term``.

La prueba interna usa ``TPKFullState`` y su carta
``SignedDodecaphaseState``; no usa ``CT108RawProjection`` como dominio. Este helper recibe
la coordenada publicada ``C_term=(b90,b120,Q_TPK)`` y calcula únicamente
``C_term -> Pi_H -> U_term -> H4_inverse -> K -> Dig10 -> (D3,D4,Q)``. No
reconstruye el ledger después de una proyección que lo haya olvidado. Ni ``U_term`` ni ``K``
ni alfa ni una magnitud metrológica aparecen en la entrada. La integración del
grafo de Cayley comprueba que el registro obtenido por Hadamard es la única
preimagen de la coordenada publicada.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "metadata" / "semilla-registro-terminal.json"

HADAMARD_4 = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)


def fail(message: str) -> None:
    raise SystemExit("FAIL_VERIFICACION_AUXILIAR_REGISTRO_TERMINAL_TPK_REV13 " + message)


def cyclic_difference(values: tuple[int, ...], step: int) -> tuple[int, ...]:
    return tuple(
        values[index] - values[(index + step) % len(values)]
        for index in range(len(values))
    )


def orbit_sums(values: tuple[int, ...], classes: int) -> tuple[int, ...]:
    return tuple(sum(values[residue::classes]) for residue in range(classes))


def load_terminal_channel_state() -> tuple[tuple[int, ...], tuple[int, ...], int]:
    try:
        data = json.loads(SEED.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail("terminal_seed=" + str(error))
    if data.get("schema") != "HMT.CH.published-terminal-channel-coordinate.v3":
        fail("terminal_seed_schema")
    if data.get("causal_role") != "published_internal_terminal_channel_coordinate_for_auxiliary_downstream_verification":
        fail("terminal_seed_causal_role")
    if data.get("state_constructor") != "TPK_FULL_DECLARED_ENRICHED_STATE":
        fail("terminal_seed_state_constructor")
    if data.get("channel_map_status") != "FULL_STATE_TYPED_INTERNAL_CLOSURE":
        fail("terminal_seed_channel_map")
    if data.get("mathematical_proof_status") != "EXACTO_INTERNO":
        fail("terminal_seed_mathematical_proof_status")
    if data.get("recovery_receipt") != "metadata/recuperacion-procedencia-terminal.json":
        fail("terminal_seed_recovery_receipt")
    if data.get("downstream_chain_status") != "EXACT_AND_REPRODUCIBLE_FROM_PUBLISHED_TERMINAL_COORDINATE":
        fail("terminal_seed_downstream_status")
    if data.get("auxiliary_replay_scope") != "CTERM_TO_RETURN_ONLY":
        fail("terminal_seed_auxiliary_replay_scope")
    if data.get("visit_by_visit_replay_included") is not False:
        fail("terminal_seed_visit_by_visit_replay")
    if data.get("python_generates_upstream") is not False:
        fail("terminal_seed_python_upstream")
    if data.get("mathematical_proof_limited_by_auxiliary_replay_scope") is not False:
        fail("terminal_seed_proof_scope")
    if data.get("terminal_channel_coordinate_input") is not True:
        fail("terminal_seed_channel_input_disclosure")
    if data.get("equivalent_terminal_coordinate_input") is not True:
        fail("terminal_seed_equivalent_input_disclosure")
    for flag in (
        "signed_terminal_coordinate_input",
        "terminal_register_K_input",
        "external_physical_input",
        "conventional_alpha_input",
        "terminal_residual_table_input",
    ):
        if data.get(flag) is not False:
            fail("terminal_seed_scope=" + flag)
    owner = data.get("source_owner")
    if not isinstance(owner, dict):
        fail("terminal_seed_source_owner")
    if owner.get("owner_id") != "U016":
        fail("terminal_seed_source_owner_id")
    if owner.get("sha256") != "40449cd4913dc6867b7784f7338afc63706ea4a5467c6efdad97b6d7d365de96":
        fail("terminal_seed_source_owner_sha256")
    if owner.get("line_ranges") != [
        "7-24", "61-77", "270-350", "352-382", "442-476", "523-583", "630-663"
    ]:
        fail("terminal_seed_source_owner_lines")
    if owner.get("provenance_status") != "TPK_FULL_STATE_OWNER":
        fail("terminal_seed_source_owner_provenance")
    if owner.get("formalization_status") != "FULL_STATE_TYPED_INTERNAL_CLOSURE":
        fail("terminal_seed_source_owner_formalization")
    b90 = data.get("b90")
    b120 = data.get("b120")
    total = data.get("Q_TPK")
    for name, vector in (("b90", b90), ("b120", b120)):
        if (
            not isinstance(vector, list)
            or len(vector) != 12
            or any(type(value) is not int for value in vector)
        ):
            fail("terminal_seed_" + name)
    if type(total) is not int:
        fail("terminal_seed_Q_TPK")
    return tuple(b90), tuple(b120), total


def validate_channel_state(
    b90: tuple[int, ...], b120: tuple[int, ...], total: int
) -> None:
    if len(b90) != 12 or len(b120) != 12:
        fail("channel_length")
    if orbit_sums(b90, 3) != (0, 0, 0):
        fail("b90_not_closed")
    if orbit_sums(b120, 4) != (0, 0, 0, 0):
        fail("b120_not_closed")
    if cyclic_difference(b90, 4) != cyclic_difference(b120, 3):
        fail("channel_square_not_commutative")
    sums_120 = orbit_sums(b120, 3)
    numerators = (
        total + 2 * sums_120[0] + sums_120[1],
        total - sums_120[0] + sums_120[1],
        total - sums_120[0] - 2 * sums_120[1],
    )
    if any(value % 3 for value in numerators):
        fail("channel_orbit_nonintegral")


def harmonic_signed_coordinate(
    b90: tuple[int, ...], b120: tuple[int, ...], total: int
) -> tuple[tuple[int, ...], list[list[int]]]:
    """Calcula ``Pi_H(b90,b120,Q)`` sin recibir ``U`` ni ``K``."""
    validate_channel_state(b90, b120, total)
    sums_120 = orbit_sums(b120, 3)
    scalar = (
        (total + 2 * sums_120[0] + sums_120[1]) // 3,
        (total - sums_120[0] + sums_120[1]) // 3,
        (total - sums_120[0] - 2 * sums_120[1]) // 3,
    )
    blocks: list[list[int]] = []
    for residue in range(3):
        d0, d1, d2, d3 = (b90[residue + 3 * column] for column in range(4))
        blocks.append([scalar[residue], d1 - d3, d0 + d2, d0 - d2])
    signed = tuple(
        blocks[residue][column]
        for column in range(4)
        for residue in range(3)
    )
    return signed, blocks


def inverse_hadamard(block: tuple[int, int, int, int] | list[int]) -> list[int]:
    products = [
        sum(row[index] * block[index] for index in range(4))
        for row in HADAMARD_4
    ]
    if any(value % 4 for value in products):
        fail("nonintegral_terminal_chart")
    return [value // 4 for value in products]


def integrate_channel_state(
    b90: tuple[int, ...], b120: tuple[int, ...], total: int
) -> tuple[int, ...]:
    """Integra D3 y D4; Q fija la única constante restante."""
    validate_channel_state(b90, b120, total)
    values: list[int | None] = [None] * 12
    values[0] = 0
    pending = [0]
    while pending:
        index = pending.pop()
        current = values[index]
        if current is None:
            fail("channel_integration_internal")
        for step, edges in ((3, b90), (4, b120)):
            neighbour = (index + step) % 12
            candidate = current - edges[index]
            if values[neighbour] is None:
                values[neighbour] = candidate
                pending.append(neighbour)
            elif values[neighbour] != candidate:
                fail("channel_does_not_integrate")
    if any(value is None for value in values):
        fail("channel_graph_not_connected")
    base = tuple(int(value) for value in values if value is not None)
    displacement = Fraction(total - sum(base), 12)
    if displacement.denominator != 1:
        fail("channel_total_nonintegral")
    return tuple(value + displacement.numerator for value in base)


def compute_downstream_terminal_chart(
    channel_state: tuple[tuple[int, ...], tuple[int, ...], int] | None = None,
) -> dict[str, object]:
    if channel_state is None:
        channel_state = load_terminal_channel_state()
    b90, b120, total = channel_state
    signed_coordinate, orbit_blocks = harmonic_signed_coordinate(b90, b120, total)
    phase_blocks = [inverse_hadamard(block) for block in orbit_blocks]
    register = tuple(
        phase_blocks[residue][column]
        for column in range(4)
        for residue in range(3)
    )
    integrated_register = integrate_channel_state(b90, b120, total)
    if register != integrated_register:
        fail("hadamard_channel_concordance")
    if cyclic_difference(register, 3) != b90:
        fail("b90_return")
    if cyclic_difference(register, 4) != b120:
        fail("b120_return")
    if sum(register) != total:
        fail("Q_return")
    if any(not 0 <= value <= 999 for value in register):
        fail("register_outside_decimal_chart")
    rows = [
        {
            "window": window,
            "digit_A": value // 100,
            "digit_C": (value // 10) % 10,
            "digit_V": value % 10,
            "K_block": value,
        }
        for window, value in enumerate(register, start=1)
    ]
    return {
        "schema": "HMT.CH.auxiliary-downstream-terminal-chart.v4",
        "causal_role": "auxiliary_downstream_publication_from_published_terminal_channel_coordinate",
        "computed_by": [
            "published_internal_terminal_channel_coordinate_C_term",
            "Pi_H",
            "H4_inverse_on_three_orbits",
            "Euclidean_Dig10",
        ],
        "seed_artifact": "metadata/semilla-registro-terminal.json",
        "terminal_channel_state": {
            "b90": list(b90),
            "b120": list(b120),
            "Q_TPK": total,
        },
        "signed_terminal_coordinate": list(signed_coordinate),
        "orbit_blocks": orbit_blocks,
        "phase_blocks": phase_blocks,
        "terminal_family": rows,
        "derived_dodecaphase_register_K": list(register),
        "independent_integrated_register": list(integrated_register),
        "returned_terminal_channel_state": {
            "b90": list(cyclic_difference(register, 3)),
            "b120": list(cyclic_difference(register, 4)),
            "Q_TPK": sum(register),
        },
        "concordance": {
            "Pi_H_then_H4_inverse_equals_Cayley_integration": True,
            "D3_D4_Q_return_equals_seed_channel_state": True,
        },
        "mathematical_provenance_status": "TPK_FULL_STATE_OWNER",
        "formalization_status": "FULL_STATE_TYPED_INTERNAL_CLOSURE",
        "auxiliary_replay_scope": "CTERM_TO_RETURN_ONLY",
        "visit_by_visit_replay_included": False,
        "python_generates_upstream": False,
        "mathematical_proof_limited_by_auxiliary_replay_scope": False,
        "terminal_channel_coordinate_input": True,
        "equivalent_terminal_coordinate_input": True,
        "external_physical_input": False,
        "conventional_alpha_input": False,
        "signed_terminal_coordinate_input": False,
        "terminal_register_K_input": False,
    }


def main() -> None:
    result = compute_downstream_terminal_chart()
    if sys.argv[1:] == ["--emit-json"]:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return
    if sys.argv[1:]:
        fail("usage")
    print(
        "PASS_REGISTRO_TERMINAL_DOWNSTREAM_REV13 "
        "input=published_internal_C_term channels=25 Pi_H=U_term H4_inverse=K "
        "Cayley_integration=concordant windows=12 residues=36 "
        "mathematical_proof=FULL_STATE_TYPED_INTERNAL_CLOSURE "
        "auxiliary_replay_scope=CTERM_TO_RETURN_ONLY visit_by_visit_replay_included=false "
        "python_generates_upstream=false mathematical_proof_limited=false "
        "terminal_channel_coordinate_input=true "
        "signed_terminal_coordinate_input=false terminal_register_K_input=false "
        "external_physical_input=false conventional_alpha_input=false"
    )


if __name__ == "__main__":
    main()
