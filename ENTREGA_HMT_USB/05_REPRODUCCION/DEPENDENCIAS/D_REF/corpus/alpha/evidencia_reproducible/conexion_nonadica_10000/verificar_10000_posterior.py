#!/usr/bin/env python3
"""Verificación posterior de la conexión nonádica conjunta y de G9->T1.

Este programa se abre sólo después de que ambos generadores hayan escrito sus
salidas. Compara pi/e/phi con algoritmos Decimal independientes y con la ventana
canónica de 1.000 cifras; para alpha recompone el autómata de carry, verifica la
independencia de la frontera remota y sólo entonces abre un control local
de 3.000 cifras, que no participa en la generación.
"""

from __future__ import annotations

import ast
import csv
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import re
import sys
import time


HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "salidas"
GENERATOR = HERE / "generar_10000_desde_estructura.py"
ALPHA_GENERATOR = HERE / "generar_alpha_T1_10000.py"
GEN_CERT = HERE / "certificado_generacion_estructural_10000.json"
ALPHA_CERT = HERE / "certificado_composicion_G9_T1_alpha_10000.json"
K_INPUT = HERE / "inputs" / "K_R12_DECLARADO.json"
REFINEMENT_LEDGER = OUTPUT_DIR / "ledger_10000_cifras.csv"
ALPHA_LEDGER = OUTPUT_DIR / "ledger_alpha_T1_3340_triados_guardia.csv"
OUTPUT = HERE / "certificado_verificacion_independiente_10000.json"

CURRENT_AUTHORITY = HERE / "inputs" / "CURRENT_AUTHORITY_SNAPSHOT.json"
PREFIX_CONTROL_DIR = HERE / "controles_corpus"
ALPHA_REFERENCE = PREFIX_CONTROL_DIR / "alpha_3000_reference_digits.txt"

CHANNELS = ("pi", "e", "phi")
DIGITS = 10_000
BLOCKS = 3501
BLOCK_SIZE = 6
NONAD = 9
AMBIENT = 729
GUARD_DIGITS = 10_020
TERMINAL_CARRIES = (-2, -1, 0, 1, 2)
FORBIDDEN_IMPORTS = {"math", "decimal", "mpmath", "sympy", "numpy"}

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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def source_isolation(path: Path, forbid_numeric_libraries: bool) -> dict[str, object]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    imports: set[str] = set()
    long_literals: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            long_literals.extend(re.findall(r"(?<![A-Za-z])\d{25,}(?![A-Za-z])", node.value))
        elif isinstance(node, ast.Constant) and isinstance(node.value, int):
            rendered = str(abs(node.value))
            if len(rendered) >= 25:
                long_literals.append(rendered)
    if forbid_numeric_libraries:
        require(not (imports & FORBIDDEN_IMPORTS), f"{path.name}: biblioteca prohibida")
    require(not long_literals, f"{path.name}: literal numérico largo")
    target_prefixes = ("1415926535", "7182818284", "6180339887", "0072973525")
    require(not any(prefix in source for prefix in target_prefixes), f"{path.name}: prefijo objetivo")
    return {
        "path": path.name,
        "sha256": sha256_file(path),
        "imports": sorted(imports),
        "long_numeric_literals": 0,
        "known_target_prefixes_absent": list(target_prefixes),
    }


def decimal_output(channel: str) -> tuple[int, str]:
    text = (OUTPUT_DIR / f"{channel}_{DIGITS}_decimales.txt").read_text(
        encoding="ascii"
    ).strip()
    integer, fractional = text.split(".")
    require(len(fractional) == DIGITS and fractional.isdigit(), f"{channel}: decimal")
    return int(integer), fractional


def generated_blocks(channel: str) -> list[str]:
    blocks = (
        OUTPUT_DIR / f"{channel}_{BLOCKS}_bloques_ternarios.txt"
    ).read_text(encoding="ascii").strip().split("|")
    require(len(blocks) == BLOCKS, f"{channel}: bloques")
    require(
        all(len(block) == BLOCK_SIZE and set(block) <= {"0", "1", "2"} for block in blocks),
        f"{channel}: alfabeto ternario",
    )
    return blocks


def pi_chudnovsky(ndigits: int) -> Decimal:
    with localcontext() as context:
        context.prec = ndigits + 90
        constant = Decimal(426880) * context.sqrt(Decimal(10005))
        k = 0
        multiplier = 1
        linear = 13591409
        power = 1
        auxiliary = 6
        series = Decimal(linear)
        threshold = Decimal(10) ** (-(ndigits + 60))
        while True:
            k += 1
            multiplier = (multiplier * (auxiliary**3 - 16 * auxiliary)) // (k**3)
            linear += 545140134
            power *= -262537412640768000
            term = Decimal(multiplier * linear) / power
            series += term
            auxiliary += 12
            if abs(term) < threshold:
                break
        return +(constant / series)


def independent_values(ndigits: int) -> dict[str, Decimal]:
    with localcontext() as context:
        context.prec = ndigits + 90
        return {
            "pi": pi_chudnovsky(ndigits),
            "e": +context.exp(Decimal(1)),
            "phi": +(Decimal(1) + context.sqrt(Decimal(5))) / 2,
        }


def decimal_parts(value: Decimal, ndigits: int) -> tuple[int, str]:
    rendered = format(value, "f")
    integer, fractional = rendered.split(".")
    fractional = (fractional + "0" * ndigits)[:ndigits]
    return int(integer), fractional


def verify_independent_decimals() -> dict[str, object]:
    references = independent_values(DIGITS)
    result: dict[str, object] = {}
    for channel in CHANNELS:
        generated_integer, generated_fractional = decimal_output(channel)
        reference_integer, reference_fractional = decimal_parts(references[channel], DIGITS)
        require(
            (generated_integer, generated_fractional)
            == (reference_integer, reference_fractional),
            f"{channel}: no coincide con cálculo independiente",
        )
        canonical = (HERE / "controles_corpus" / f"{channel}_1000_reference_digits.txt")
        canonical_text = canonical.read_text(encoding="ascii").strip()
        generated_head = f"{generated_integer}.{generated_fractional[:1000]}"
        require(generated_head == canonical_text, f"{channel}: ventana canónica 1000")
        result[channel] = {
            "match_independent_10000": True,
            "independent_algorithm": (
                "Chudnovsky Decimal" if channel == "pi" else
                "Decimal exp" if channel == "e" else "Decimal sqrt(5)"
            ),
            "match_canonical_1000_window": True,
            "canonical_control_sha256": sha256_file(canonical),
            "generated_sha256": sha256_file(
                OUTPUT_DIR / f"{channel}_{DIGITS}_decimales.txt"
            ),
        }
    return result


def verify_joint_connection() -> dict[str, object]:
    rows = read_csv(REFINEMENT_LEDGER)
    require(len(rows) == 3 * BLOCKS, "filas del ledger G9")
    local_repeats: dict[str, int] = {}
    for channel in CHANNELS:
        channel_rows = [row for row in rows if row["channel"] == channel]
        require(len(channel_rows) == BLOCKS, f"{channel}: ledger incompleto")
        require(all(int(row["ambient_candidates"]) == AMBIENT for row in channel_rows), "ambiente")
        require(all(int(row["survivors"]) == 1 for row in channel_rows), "poda no unitaria")
        require(
            all(
                int(row["killed_before"])
                + int(row["survivors"])
                + int(row["killed_after"])
                == AMBIENT
                for row in channel_rows
            ),
            "partición no exhaustiva",
        )
        repeats = 0
        for index in range(BLOCKS - NONAD):
            before = channel_rows[index]
            after = channel_rows[index + NONAD]
            require(before["phase9"] == after["phase9"], "retorno de fase")
            require(before["prefix_sha256"] != after["prefix_sha256"], "estado reiniciado")
            local_before = (
                before["block"], before["candidate_index"],
                before["witt_right"], before["witt_weight"],
            )
            local_after = (
                after["block"], after["candidate_index"],
                after["witt_right"], after["witt_weight"],
            )
            repeats += local_before == local_after
        local_repeats[channel] = repeats

        canonical_blocks = (
            PREFIX_CONTROL_DIR / f"{channel}_396_bloques_ternarios.txt"
        ).read_text(encoding="ascii").strip().split("|")
        require(generated_blocks(channel)[:396] == canonical_blocks, f"{channel}: regresión 1000")

    return {
        "rows": len(rows),
        "levels_per_channel": BLOCKS,
        "trits_per_channel": BLOCKS * BLOCK_SIZE,
        "phase_pairs_per_channel": BLOCKS - NONAD,
        "complete_nonads_per_channel": BLOCKS // NONAD - 1,
        "partitions_729_to_1": True,
        "full_state_never_resets": True,
        "local_projection_repeats_after_nine": local_repeats,
        "canonical_396_block_prefix_preserved": True,
    }


def guard_triads_from_blocks(channel: str) -> list[int]:
    blocks = generated_blocks(channel)
    prefix = int("".join(blocks), 3)
    denominator = 3 ** (BLOCK_SIZE * len(blocks))
    scale = 10**GUARD_DIGITS
    lower = prefix * scale // denominator
    upper = ((prefix + 1) * scale - 1) // denominator
    require(lower == upper, f"{channel}: guarda decimal")
    digits = f"{lower:0{GUARD_DIGITS}d}"
    return [int(digits[index:index + 3]) for index in range(0, GUARD_DIGITS, 3)]


def t1_branch(
    inputs: dict[str, list[int]], seal: list[int], terminal: int
) -> tuple[list[int], list[int]]:
    length = len(inputs["pi"])
    output = [0] * length
    carries = [0] * (length + 1)
    carries[length] = terminal
    carry = terminal
    for index in range(length - 1, -1, -1):
        total = (
            inputs["pi"][index] + inputs["e"][index]
            - inputs["phi"][index] - seal[index % 12] + carry
        )
        output[index] = total % 1000
        carry = total // 1000
        carries[index] = carry
    return output, carries


def verify_alpha_composition() -> dict[str, object]:
    local_k = json.loads(K_INPUT.read_text(encoding="utf-8"))["coordinates"]
    authority = json.loads(CURRENT_AUTHORITY.read_text(encoding="utf-8"))
    authority_k = authority["state_types"]["CanonicalSealK"]["coordinates"]
    require(local_k == authority_k, "K_R12 no coincide con CURRENT")
    seal = [int(value) for value in local_k]

    inputs = {channel: guard_triads_from_blocks(channel) for channel in CHANNELS}
    raw = [
        inputs["pi"][index] + inputs["e"][index]
        - inputs["phi"][index] - seal[index % 12]
        for index in range(len(inputs["pi"]))
    ]
    require(
        all((value + carry) // 1000 in TERMINAL_CARRIES for value in raw for carry in TERMINAL_CARRIES),
        "rango de carry no invariante",
    )
    branches = [t1_branch(inputs, seal, terminal) for terminal in TERMINAL_CARRIES]
    outputs = [branch[0] for branch in branches]
    common = 0
    for index in range(len(outputs[0])):
        if len({output[index] for output in outputs}) != 1:
            break
        common += 1
    require(common == 3339, "longitud de coalescencia remota")
    stable = "".join(f"{value:03d}" for value in outputs[0][:common])
    generated_alpha = (OUTPUT_DIR / "alpha_T1_10000_decimales.txt").read_text(
        encoding="ascii"
    ).strip()
    require(generated_alpha == "0." + stable[:DIGITS], "salida alpha no recompuesta")
    reference = ALPHA_REFERENCE.read_text(encoding="ascii").strip()
    require(stable[:len(reference)] == reference, "ventana local T1")

    ledger = read_csv(ALPHA_LEDGER)
    require(len(ledger) == GUARD_DIGITS // 3, "ledger alpha")
    require(all(row["stable_output"] == "True" for row in ledger[:common]), "prefijo no estable")

    return {
        "K_R12_matches_CURRENT": True,
        "terminal_carry_states_exhausted": list(TERMINAL_CARRIES),
        "carry_interval_invariant": True,
        "guard_triads": len(inputs["pi"]),
        "common_prefix_triads": common,
        "common_prefix_digits": 3 * common,
        "published_digits": DIGITS,
        "match_local_3000_digit_reference_window": True,
        "reference_role": "control posterior; no entrada de la composición",
        "reference_sha256": sha256_file(ALPHA_REFERENCE),
        "alpha_output_sha256": sha256_file(OUTPUT_DIR / "alpha_T1_10000_decimales.txt"),
    }


def main() -> None:
    started = time.perf_counter()
    required = [
        GENERATOR, ALPHA_GENERATOR, GEN_CERT, ALPHA_CERT, K_INPUT,
        REFINEMENT_LEDGER, ALPHA_LEDGER, CURRENT_AUTHORITY, ALPHA_REFERENCE,
    ]
    for channel in CHANNELS:
        required.extend(
            [
                OUTPUT_DIR / f"{channel}_{DIGITS}_decimales.txt",
                OUTPUT_DIR / f"{channel}_{BLOCKS}_bloques_ternarios.txt",
                HERE / "controles_corpus" / f"{channel}_1000_reference_digits.txt",
            ]
        )
    for path in required:
        require(path.is_file(), f"falta {path}")

    generation = json.loads(GEN_CERT.read_text(encoding="utf-8"))
    alpha = json.loads(ALPHA_CERT.read_text(encoding="utf-8"))
    require(generation["status"] == "PASS_GENERACION_ESTRUCTURAL_10000_DECIMALES", "G9")
    require(alpha["status"] == "PASS_COMPOSICION_G9_T1_ALPHA_10000", "T1")

    source_checks = {
        "G9_generator": source_isolation(GENERATOR, True),
        "alpha_T1_generator": source_isolation(ALPHA_GENERATOR, True),
    }
    require(generation["generator_sha256"] == source_checks["G9_generator"]["sha256"], "hash G9")
    require(alpha["generator_sha256"] == source_checks["alpha_T1_generator"]["sha256"], "hash T1")

    result = {
        "schema": "HMT.conexion-nonadica-conjunta-10000.verificacion-posterior.v1",
        "status": "PASS_VERIFICACION_INDEPENDIENTE_10000",
        "causal_order": [
            "generación G9 ya escrita",
            "composición T1 y coalescencia de carry ya escritas",
            "auditoría estática",
            "cálculo decimal independiente",
            "comparación posterior con ventanas canónicas",
        ],
        "source_isolation": source_checks,
        "joint_nonadic_connection": verify_joint_connection(),
        "independent_decimal_control": verify_independent_decimals(),
        "alpha_G9_T1": verify_alpha_composition(),
        "provenance": {
            "infinite_section_and_T1": "ARQUITECTURA_AUTORAL_PREEXISTENTE_Y_RESULTADO_RECUPERADO",
            "optimized_exact_readers_and_composition": "FORMALIZACION_NUEVA",
            "10000_digit_runs_and_remote_carry_proof": "CERTIFICADO_NUEVO",
            "values": "RECONOCIMIENTO_POSTERIOR_NO_RESULTADO_NUEVO",
        },
    }
    elapsed = time.perf_counter() - started
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS_VERIFICACION_INDEPENDIENTE_10000")
    print(
        json.dumps(
            {
                "digits_pi_e_phi": DIGITS,
                "digits_alpha": DIGITS,
                "levels_per_channel": BLOCKS,
                "complete_nonads_per_channel": BLOCKS // NONAD - 1,
                "alpha_common_prefix_digits": result["alpha_G9_T1"]["common_prefix_digits"],
                "seconds": elapsed,
            },
            sort_keys=True,
        )
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
