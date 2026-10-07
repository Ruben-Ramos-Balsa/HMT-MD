#!/usr/bin/env python3
"""Composición causal G9 -> T1 para un truncamiento de 10.000 cifras de alpha.

El programa abre exclusivamente las tres ramas ternarias ya generadas por G9,
su certificado y la coordenada declarada K_R12. Reconstruye 10.020 cifras de
guarda directamente de los cilindros ternarios y aplica, de derecha a izquierda,

    s_k = P_k + E_k - Phi_k - K_(k mod 12) + c_(k+1),
    A_k = s_k mod 1000,
    c_k = floor(s_k/1000).

No fija un carry terminal particular. Propaga los cinco estados terminales del
intervalo invariante {-2,-1,0,1,2} y sólo publica el prefijo que es idéntico en
todas las prolongaciones. No abre alpha, alphaInv, CODATA ni un prefijo objetivo.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "salidas"
GEN_CERT = HERE / "certificado_generacion_estructural_10000.json"
K_INPUT = HERE / "inputs" / "K_R12_DECLARADO.json"
CERTIFICATE = HERE / "certificado_composicion_G9_T1_alpha_10000.json"
LEDGER = OUTPUT_DIR / "ledger_alpha_T1_3340_triados_guardia.csv"
OUTPUT_DECIMAL = OUTPUT_DIR / "alpha_T1_10000_decimales.txt"
OUTPUT_STABLE_TRIADS = OUTPUT_DIR / "alpha_T1_3339_triados_estables.txt"

OUTPUT_DIGITS = 10_000
GUARD_DIGITS = 10_020
BLOCKS = 3501
BLOCK_SIZE = 6
BASE = 1000
TERMINAL_CARRY_STATES = (-2, -1, 0, 1, 2)
CHANNELS = ("pi", "e", "phi")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def blocks_path(channel: str) -> Path:
    return OUTPUT_DIR / f"{channel}_{BLOCKS}_bloques_ternarios.txt"


def read_blocks(channel: str) -> list[str]:
    path = blocks_path(channel)
    blocks = path.read_text(encoding="ascii").strip().split("|")
    require(len(blocks) == BLOCKS, f"{channel}: número de bloques")
    require(
        all(len(block) == BLOCK_SIZE and set(block) <= {"0", "1", "2"} for block in blocks),
        f"{channel}: bloque ternario inválido",
    )
    return blocks


def digits_from_complete_cylinder(channel: str) -> str:
    blocks = read_blocks(channel)
    prefix = int("".join(blocks), 3)
    denominator = 3 ** (BLOCK_SIZE * len(blocks))
    scale = 10**GUARD_DIGITS
    lower_cell = prefix * scale // denominator
    upper_cell = ((prefix + 1) * scale - 1) // denominator
    require(lower_cell == upper_cell, f"{channel}: cilindro sin {GUARD_DIGITS} cifras")
    digits = f"{lower_cell:0{GUARD_DIGITS}d}"
    require(len(digits) == GUARD_DIGITS, f"{channel}: longitud de guarda")
    return digits


def triads(digits: str) -> list[int]:
    require(len(digits) % 3 == 0, "la guarda no se divide en tríadas")
    return [int(digits[index:index + 3]) for index in range(0, len(digits), 3)]


def propagate_branch(
    pi: list[int],
    euler: list[int],
    phi: list[int],
    seal: list[int],
    terminal_carry: int,
) -> tuple[list[int], list[int]]:
    length = len(pi)
    require(len(euler) == len(phi) == length, "canales de longitudes distintas")
    output = [0] * length
    carries = [0] * (length + 1)
    carries[length] = terminal_carry
    carry = terminal_carry
    for index in range(length - 1, -1, -1):
        total = pi[index] + euler[index] - phi[index] - seal[index % 12] + carry
        output[index] = total % BASE
        carry = total // BASE
        carries[index] = carry
    return output, carries


def main() -> None:
    started = time.perf_counter()
    require(GEN_CERT.is_file() and K_INPUT.is_file(), "faltan entradas certificadas")
    generation = json.loads(GEN_CERT.read_text(encoding="utf-8"))
    require(
        generation["status"] == "PASS_GENERACION_ESTRUCTURAL_10000_DECIMALES",
        "la generación G9 no está certificada",
    )
    seal_payload = json.loads(K_INPUT.read_text(encoding="utf-8"))
    seal = [int(value) for value in seal_payload["coordinates"]]
    require(len(seal) == 12 and all(0 <= value < BASE for value in seal), "K_R12")

    decimal_guard = {channel: digits_from_complete_cylinder(channel) for channel in CHANNELS}
    inputs = {channel: triads(decimal_guard[channel]) for channel in CHANNELS}
    length = len(inputs["pi"])
    require(length == GUARD_DIGITS // 3, "número de tríadas de guarda")

    # [-2,2] es invariante para todas las entradas concretas y cubre el rango
    # general inducido por cuatro dígitos base mil. Esta verificación no fija
    # una condición terminal: prueba todas las condiciones admisibles.
    raw_terms = [
        inputs["pi"][index]
        + inputs["e"][index]
        - inputs["phi"][index]
        - seal[index % 12]
        for index in range(length)
    ]
    require(
        all(
            (raw + carry) // BASE in TERMINAL_CARRY_STATES
            for raw in raw_terms
            for carry in TERMINAL_CARRY_STATES
        ),
        "el intervalo de carries no es invariante",
    )

    branches = [
        propagate_branch(
            inputs["pi"], inputs["e"], inputs["phi"], seal, terminal
        )
        for terminal in TERMINAL_CARRY_STATES
    ]
    branch_outputs = [branch[0] for branch in branches]
    branch_carries = [branch[1] for branch in branches]

    common_prefix_triads = 0
    for index in range(length):
        if len({output[index] for output in branch_outputs}) != 1:
            break
        common_prefix_triads += 1
    required_triads = (OUTPUT_DIGITS + 2) // 3
    require(
        common_prefix_triads >= required_triads,
        "el carry remoto no fija las 10.000 cifras solicitadas",
    )
    stable_triads = branch_outputs[0][:common_prefix_triads]
    stable_word = "".join(f"{value:03d}" for value in stable_triads)
    output_digits = stable_word[:OUTPUT_DIGITS]
    require(len(output_digits) == OUTPUT_DIGITS, "longitud alpha")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DECIMAL.write_text(f"0.{output_digits}\n", encoding="ascii")
    OUTPUT_STABLE_TRIADS.write_text(stable_word + "\n", encoding="ascii")

    fieldnames = [
        "k",
        "pi",
        "e",
        "phi",
        "K_R12",
        "carry_next_options",
        "alpha_options",
        "carry_current_options",
        "stable_output",
    ]
    with LEDGER.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(length):
            alpha_options = sorted({output[index] for output in branch_outputs})
            carry_next = sorted({carries[index + 1] for carries in branch_carries})
            carry_current = sorted({carries[index] for carries in branch_carries})
            writer.writerow(
                {
                    "k": index + 1,
                    "pi": f"{inputs['pi'][index]:03d}",
                    "e": f"{inputs['e'][index]:03d}",
                    "phi": f"{inputs['phi'][index]:03d}",
                    "K_R12": f"{seal[index % 12]:03d}",
                    "carry_next_options": "|".join(str(value) for value in carry_next),
                    "alpha_options": "|".join(f"{value:03d}" for value in alpha_options),
                    "carry_current_options": "|".join(str(value) for value in carry_current),
                    "stable_output": len(alpha_options) == 1,
                }
            )

    elapsed = time.perf_counter() - started
    certificate = {
        "schema": "HMT.G9-T1.alpha-10000.rev9.v1",
        "status": "PASS_COMPOSICION_G9_T1_ALPHA_10000",
        "recurrence": {
            "s_k": "P_k+E_k-Phi_k-K_(k mod 12)+c_(k+1)",
            "A_k": "s_k mod 1000",
            "c_k": "floor(s_k/1000)",
        },
        "boundary_convention": {
            "guard_triads": length,
            "terminal_carry_set": list(TERMINAL_CARRY_STATES),
            "method": (
                "se propagan todas las condiciones terminales del intervalo "
                "invariante; sólo se publica su prefijo común"
            ),
            "common_prefix_triads": common_prefix_triads,
            "common_prefix_digits": 3 * common_prefix_triads,
            "requested_output_digits": OUTPUT_DIGITS,
            "target_terminal_carry_used": False,
        },
        "input_origins": {
            "G9_generation_certificate": {
                "path": GEN_CERT.name,
                "sha256": sha256_file(GEN_CERT),
            },
            "K_R12_declared_coordinate": {
                "path": K_INPUT.relative_to(HERE).as_posix(),
                "sha256": sha256_file(K_INPUT),
                "authority_locator": seal_payload["authority_locator"],
            },
            "ternary_channels": {
                channel: {
                    "path": blocks_path(channel).relative_to(HERE).as_posix(),
                    "sha256": sha256_file(blocks_path(channel)),
                    "blocks": BLOCKS,
                    "trits": BLOCKS * BLOCK_SIZE,
                }
                for channel in CHANNELS
            },
        },
        "causal_isolation": {
            "not_read": [
                "alpha decimal",
                "alphaInv",
                "CODATA",
                "control decimal externo",
                "metrological target",
            ],
            "published_only_after_remote_carry_coalescence": True,
        },
        "outputs": {
            "alpha_decimal": {
                "path": OUTPUT_DECIMAL.relative_to(HERE).as_posix(),
                "sha256": sha256_file(OUTPUT_DECIMAL),
                "digits_after_point": OUTPUT_DIGITS,
            },
            "stable_triads": {
                "path": OUTPUT_STABLE_TRIADS.relative_to(HERE).as_posix(),
                "sha256": sha256_file(OUTPUT_STABLE_TRIADS),
                "triads": common_prefix_triads,
            },
            "remote_carry_ledger": {
                "path": LEDGER.relative_to(HERE).as_posix(),
                "sha256": sha256_file(LEDGER),
                "rows": length,
            },
        },
        "provenance": {
            "T1_rule": "RESULTADO_RECUPERADO",
            "G9_to_T1_composition": "FORMALIZACION_NUEVA",
            "remote_carry_and_10000_digit_run": "CERTIFICADO_NUEVO",
            "alpha_value": "NO_SE_ROTULA_COMO_RESULTADO_NUEVO",
        },
        "generator_sha256": sha256_file(Path(__file__).resolve()),
    }
    CERTIFICATE.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PASS_COMPOSICION_G9_T1_ALPHA_10000")
    print(
        json.dumps(
            {
                "guard_triads": length,
                "common_prefix_triads": common_prefix_triads,
                "common_prefix_digits": 3 * common_prefix_triads,
                "published_digits": OUTPUT_DIGITS,
                "seconds": elapsed,
            },
            sort_keys=True,
        )
    )
    print(CERTIFICATE)


if __name__ == "__main__":
    main()
