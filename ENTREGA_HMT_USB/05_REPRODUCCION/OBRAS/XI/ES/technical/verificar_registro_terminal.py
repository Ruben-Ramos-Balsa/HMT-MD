#!/usr/bin/env python3
"""REV13: verifica auxiliarmente la cadena downstream desde ``C_term``.

El cierre interno usa ``TPKFullState`` y su carta firmada; no sustituye ese
dominio por ``CT108RawProjection``. Este programa sólo reproduce la carta
downstream desde ``C_term``.
"""

from __future__ import annotations

import json
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "metadata" / "certificado-registro-terminal.json"
GENERATOR = ROOT / "technical" / "generar_registro_terminal_tpk.py"
SEED = ROOT / "metadata" / "semilla-registro-terminal.json"


def fail(message: str) -> None:
    raise SystemExit("FAIL_REGISTRO_TERMINAL_DOWNSTREAM_REV13 " + message)


def cyclic_difference(values: list[int], step: int) -> list[int]:
    size = len(values)
    return [
        values[index] - values[(index + step) % size]
        for index in range(size)
    ]


def hadamard_inverse(block: list[int]) -> list[int]:
    matrix = (
        (1, 1, 1, 1),
        (1, 1, -1, -1),
        (1, -1, 1, -1),
        (1, -1, -1, 1),
    )
    products = [
        sum(row[index] * block[index] for index in range(4))
        for row in matrix
    ]
    if any(value % 4 for value in products):
        fail("hadamard_nonintegral")
    return [value // 4 for value in products]


def main() -> None:
    namespace = runpy.run_path(str(GENERATOR), run_name="hmt_terminal_generator")
    generated = namespace["compute_downstream_terminal_chart"]()
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    if data.get("schema") != "HMT.CH.terminal-incidence-certificate.v5":
        fail("schema")
    if generated.get("terminal_family") != data.get("generated_terminal_family"):
        fail("generated_family_receipt_mismatch")
    channel_state = generated.get("terminal_channel_state")
    if channel_state != data.get("seed", {}).get("terminal_channel_state"):
        fail("channel_seed_receipt_mismatch")
    if channel_state != {
        "b90": seed.get("b90"),
        "b120": seed.get("b120"),
        "Q_TPK": seed.get("Q_TPK"),
    }:
        fail("channel_seed_artifact_mismatch")
    if generated.get("seed_artifact") != "metadata/semilla-registro-terminal.json":
        fail("seed_artifact")
    upstream = data.get("upstream_provenance", {})
    if upstream.get("status") != "CIERRE_INTERNO_TIPADO_ESTADO_TPK_PLENO":
        fail("upstream_status")
    if upstream.get("formalization_status") != "RECTIFICACION_DE_DOMINIO_Y_CIERRE_EXACTO":
        fail("upstream_formalization_status")
    if upstream.get("recovery_receipt") != "metadata/recuperacion-procedencia-terminal.json":
        fail("upstream_recovery_receipt")
    owner = upstream.get("owner", {})
    if owner.get("id") != "U016":
        fail("upstream_owner_id")
    if owner.get("sha256") != "40449cd4913dc6867b7784f7338afc63706ea4a5467c6efdad97b6d7d365de96":
        fail("upstream_owner_sha256")
    if owner.get("line_ranges") != [
        "7-24", "61-77", "270-350", "352-382", "442-476", "523-583", "630-663"
    ]:
        fail("upstream_owner_lines")
    if generated.get("mathematical_provenance_status") != "TPK_FULL_STATE_OWNER":
        fail("generated_mathematical_provenance")
    if generated.get("formalization_status") != "FULL_STATE_TYPED_INTERNAL_CLOSURE":
        fail("generated_formalization")
    if generated.get("auxiliary_replay_scope") != "CTERM_TO_RETURN_ONLY":
        fail("generated_auxiliary_replay_scope")
    if generated.get("visit_by_visit_replay_included") is not False:
        fail("generated_visit_by_visit_replay")
    if generated.get("python_generates_upstream") is not False:
        fail("generated_python_upstream")
    if generated.get("mathematical_proof_limited_by_auxiliary_replay_scope") is not False:
        fail("generated_mathematical_proof_scope")
    if generated.get("terminal_channel_coordinate_input") is not True:
        fail("generated_channel_input_disclosure")
    if generated.get("equivalent_terminal_coordinate_input") is not True:
        fail("generated_equivalent_input_disclosure")

    rows = generated["terminal_family"]
    if not isinstance(rows, list) or len(rows) != 12:
        fail("terminal_family")
    values: list[int] = []
    for expected_window, row in enumerate(rows, start=1):
        if row.get("window") != expected_window:
            fail("window_order")
        digits = [row.get(name) for name in ("digit_A", "digit_C", "digit_V")]
        if any(not isinstance(value, int) or not 0 <= value <= 9 for value in digits):
            fail("residue_digit")
        value = 100 * digits[0] + 10 * digits[1] + digits[2]
        if row.get("K_block") != value:
            fail("decimal_formation")
        values.append(value)

    coordinates = data.get("coordinates", {})
    b90 = cyclic_difference(values, 3)
    b120 = cyclic_difference(values, 4)
    total = sum(values)
    if b90 != coordinates.get("b90_D3"):
        fail("D3")
    if b120 != coordinates.get("b120_D4"):
        fail("D4")
    if total != coordinates.get("Q"):
        fail("Q")
    if channel_state != {"b90": b90, "b120": b120, "Q_TPK": total}:
        fail("channel_state_return")

    orbit_sums = [
        sum(b120[residue + 3 * index] for index in range(4))
        for residue in range(3)
    ]
    numerator = total + 2 * orbit_sums[0] + orbit_sums[1]
    if numerator % 3:
        fail("orbit_integrality")
    s1 = numerator // 3
    scalar = [s1, s1 - orbit_sums[0], s1 - orbit_sums[0] - orbit_sums[1]]
    blocks: list[list[int]] = []
    for residue in range(3):
        difference = [b90[residue + 3 * index] for index in range(4)]
        blocks.append([
            scalar[residue],
            difference[1] - difference[3],
            difference[0] + difference[2],
            difference[0] - difference[2],
        ])
    signed_vector = [
        blocks[residue][column]
        for column in range(4)
        for residue in range(3)
    ]
    if signed_vector != data.get("derived_signed_vector_U"):
        fail("signed_vector_U")

    hadamard_blocks = [hadamard_inverse(block) for block in blocks]
    register = [
        hadamard_blocks[residue][column]
        for column in range(4)
        for residue in range(3)
    ]
    if register != data.get("derived_dodecaphase_register_K"):
        fail("register_K")
    if generated.get("derived_dodecaphase_register_K") != register:
        fail("generated_register_K")
    if register != values:
        fail("reversibility")

    expected_return = {
        "b90": b90,
        "b120": b120,
        "Q_TPK": total,
    }
    if generated.get("returned_terminal_channel_state") != expected_return:
        fail("generated_channel_return")
    if data.get("returned_terminal_channel_state") != expected_return:
        fail("certificate_channel_return")
    expected_concordance = {
        "Pi_H_then_H4_inverse_equals_Cayley_integration": True,
        "D3_D4_Q_return_equals_seed_channel_state": True,
    }
    if generated.get("concordance") != expected_concordance:
        fail("generated_concordance")
    if data.get("concordance") != expected_concordance:
        fail("certificate_concordance")

    original_b90 = tuple(channel_state["b90"])
    original_b120 = tuple(channel_state["b120"])
    original_total = channel_state["Q_TPK"]
    mutations = [
        ((original_b90[0] + 1,) + original_b90[1:], original_b120, original_total),
        (original_b90[3:] + original_b90[:3], original_b120[3:] + original_b120[:3], original_total),
    ]
    for mutation in mutations:
        try:
            altered = namespace["compute_downstream_terminal_chart"](mutation)
        except SystemExit:
            continue
        if altered["terminal_family"] == rows:
            fail("negative_mutation_not_detected")

    scope = data.get("scope", {})
    if scope.get("external_physical_input") is not False:
        fail("causal_scope")
    if scope.get("conventional_alpha_input") is not False:
        fail("alpha_scope")
    if scope.get("signed_terminal_coordinate_input") is not False:
        fail("signed_coordinate_scope")
    if scope.get("terminal_register_K_input") is not False:
        fail("terminal_register_scope")
    if scope.get("terminal_channel_coordinate_input") is not True:
        fail("terminal_channel_scope")
    if scope.get("auxiliary_replay_scope") != "CTERM_TO_RETURN_ONLY":
        fail("auxiliary_replay_scope")
    if scope.get("visit_by_visit_replay_included") is not False:
        fail("visit_by_visit_replay_scope")
    if scope.get("python_generates_upstream") is not False:
        fail("python_upstream_scope")
    if scope.get("mathematical_proof_limited_by_auxiliary_replay_scope") is not False:
        fail("mathematical_proof_scope")

    print(
        "PASS_REGISTRO_TERMINAL_DOWNSTREAM_REV13 "
        "input=published_internal_C_term channels=25 Pi_H=U12 H4_inverse=K12 "
        "Cayley_integration=concordant reversible=true mutations=2 "
        "mathematical_proof=FULL_STATE_TYPED_INTERNAL_CLOSURE "
        "auxiliary_replay_scope=CTERM_TO_RETURN_ONLY visit_by_visit_replay_included=false "
        "python_generates_upstream=false mathematical_proof_limited=false "
        "terminal_channel_coordinate_input=true "
        "signed_terminal_coordinate_input=false terminal_register_K_input=false "
        "external_physical_input=false"
    )


if __name__ == "__main__":
    main()
