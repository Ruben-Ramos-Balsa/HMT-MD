#!/usr/bin/env python3
"""Verificación posterior e independiente de la generación estructural.

Este programa se ejecuta después del generador. Aquí sí se abren los testigos
del corpus y las cadenas de control, pero sólo para comparar una salida que ya
existe en disco. Ninguno de estos archivos participa en la generación.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path
import re
from typing import Sequence


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
GENERATOR = HERE / "generar_desde_estructura.py"
GEN_CERT = HERE / "certificado_generacion_estructural.json"
OUTPUT = HERE / "certificado_verificacion_contra_corpus.json"
OUTPUT_DIR = HERE / "salidas"

ACTIVE_HMT = PROJECT_ROOT / "PUBLICACION_HMT" / "HOLOGRAFIA_MODULAR_TRIADICA"
PUBLISHED_LEDGER = ACTIVE_HMT / "datos" / "monodromia_20_bloques.csv"
PUBLISHED_READING = ACTIVE_HMT / "datos" / "lectura_arquimediana_12_bloques.csv"
PUBLISHED_BRANCHES = ACTIVE_HMT / "datos" / "ramas_frontera_fase9.csv"
PUBLISHED_DETAILS = ACTIVE_HMT / "datos" / "detalles_seleccion_frontera.csv"
ORBIT_CERT = (
    PROJECT_ROOT
    / "PUBLICACION_HMT"
    / "CONSERVACION_HOLOGRAFICA_UNIDAD_2026-07-24"
    / "certificados"
    / "selector_orbital_constantes.json"
)

REFERENCE_FILES = {
    "pi": (
        PROJECT_ROOT
        / "03_PAPER"
        / "HMT_CIERRE_HOLOGRAFICO_V1"
        / "certificados"
        / "G9"
        / "pi_1000_reference_digits.txt"
    ),
    "e": (
        PROJECT_ROOT
        / "03_PAPER"
        / "HMT_CIERRE_HOLOGRAFICO_V1"
        / "certificados"
        / "G9"
        / "e_1000_reference_digits.txt"
    ),
    "phi": (
        PROJECT_ROOT
        / "03_PAPER"
        / "HMT_CIERRE_HOLOGRAFICO_V1"
        / "certificados"
        / "G9"
        / "phi_1000_reference_digits.txt"
    ),
}

CHANNELS = ("pi", "e", "phi")


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


def source_isolation_audit() -> dict[str, object]:
    source = GENERATOR.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(GENERATOR))
    imports: set[str] = set()
    long_digit_strings: list[str] = []
    long_integer_literals: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            for match in re.findall(r"(?<![A-Za-z])\d{25,}(?![A-Za-z])", node.value):
                long_digit_strings.append(match)
        elif isinstance(node, ast.Constant) and isinstance(node.value, int):
            rendered = str(abs(node.value))
            if len(rendered) >= 25:
                long_integer_literals.append(rendered)

    forbidden_imports = {"math", "decimal", "mpmath", "sympy", "numpy"}
    target_prefixes = ("1415926535", "7182818284", "6180339887")
    require(not (imports & forbidden_imports), "el generador importa una biblioteca prohibida")
    require(not long_digit_strings, "el generador contiene una cadena numérica larga")
    require(not long_integer_literals, "el generador contiene un entero literal largo")
    require(not any(prefix in source for prefix in target_prefixes),
            "el generador contiene un prefijo objetivo")
    require("reference_digits" not in source, "el generador menciona un archivo de referencia")
    require("monodromia_20_bloques" not in source, "el generador menciona el ledger publicado")

    return {
        "generator_sha256": sha256_file(GENERATOR),
        "imports": sorted(imports),
        "forbidden_imports_absent": sorted(forbidden_imports),
        "long_numeric_strings": 0,
        "long_integer_literals": 0,
        "known_target_prefixes_absent": list(target_prefixes),
        "published_ledger_path_absent": True,
        "reference_digit_path_absent": True,
    }


def load_generated_blocks() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for channel in CHANNELS:
        path = OUTPUT_DIR / f"{channel}_396_bloques_ternarios.txt"
        blocks = path.read_text(encoding="ascii").strip().split("|")
        require(len(blocks) == 396, f"{channel}: no hay 396 bloques")
        require(all(len(block) == 6 and set(block) <= {"0", "1", "2"} for block in blocks),
                f"{channel}: bloque ternario inválido")
        result[channel] = blocks
    return result


def load_generated_decimal(channel: str) -> tuple[int, str]:
    text = (OUTPUT_DIR / f"{channel}_1000_decimales.txt").read_text(
        encoding="ascii"
    ).strip()
    integer, fractional = text.split(".")
    require(len(fractional) == 1000 and fractional.isdigit(), "salida decimal inválida")
    return int(integer), fractional


def cylinder_intersects(blocks: Sequence[str], triads: Sequence[int]) -> bool:
    word = "".join(blocks)
    length = len(word)
    visible = 0
    power1000 = 1
    bound = 3**length
    while power1000 * 1000 <= bound:
        power1000 *= 1000
        visible += 1
    require(len(triads) >= visible, "faltan tríadas para el cilindro")
    ternary_integer = int(word, 3)
    decimal_integer = 0
    for triad in triads[:visible]:
        decimal_integer = 1000 * decimal_integer + int(triad)
    return (
        ternary_integer * 1000**visible < (decimal_integer + 1) * 3**length
        and (ternary_integer + 1) * 1000**visible > decimal_integer * 3**length
    )


def triads_from_generated(channel: str) -> list[int]:
    _integer, fractional = load_generated_decimal(channel)
    padded = fractional + "00"
    return [int(padded[index:index + 3]) for index in range(0, len(fractional), 3)]


def verify_published_window(
    generated: dict[str, list[str]]
) -> dict[str, object]:
    ledger = read_csv(PUBLISHED_LEDGER)
    require(len(ledger) == 20, "ledger publicado distinto de veinte bloques")
    matches: dict[str, bool] = {}
    for channel in CHANNELS:
        published = [row[f"{channel}_block"] for row in ledger]
        matches[channel] = generated[channel][:20] == published
        require(matches[channel], f"{channel}: no coincide la rama de veinte bloques")

    w30 = {channel: "|".join(generated[channel][:5]) for channel in CHANNELS}
    r36 = {channel: generated[channel][5] for channel in CHANNELS}
    return {
        "twenty_blocks_match": matches,
        "w30_generated": w30,
        "R36_generated": r36,
        "B9_generated": [generated[channel][9] for channel in CHANNELS],
        "B10_generated": [generated[channel][10] for channel in CHANNELS],
        "B11_generated": [generated[channel][11] for channel in CHANNELS],
    }


def verify_twelve_triads(
    generated: dict[str, list[str]]
) -> dict[str, object]:
    published_rows = read_csv(PUBLISHED_READING)
    published = {
        row["constant"]: row["triads_12"].split("|")
        for row in published_rows
    }
    result: dict[str, object] = {}
    for channel in CHANNELS:
        word = "".join(generated[channel][:13])
        ternary_integer = int(word, 3)
        decimal_prefix = 1000**12 * ternary_integer // 3**78
        digits = f"{decimal_prefix:036d}"
        triads = [digits[index:index + 3] for index in range(0, 36, 3)]
        require(triads == published[channel], f"{channel}: doce tríadas distintas")
        result[channel] = triads
    return result


def verify_gate_three_to_one(
    generated: dict[str, list[str]]
) -> dict[str, object]:
    branch_rows = read_csv(PUBLISHED_BRANCHES)
    detail_rows = [
        row for row in read_csv(PUBLISHED_DETAILS) if int(row["t"]) == 9
    ]
    candidates = [tuple(row["rows"].split("|")) for row in branch_rows]
    require(len(candidates) == 3, "la fibra local G9 no tiene tres candidatos")
    require(
        candidates == [tuple(row["rows"].split("|")) for row in detail_rows],
        "N71 y N72 discrepan",
    )

    generated_b10 = tuple(generated[channel][10] for channel in CHANNELS)
    generated_b11 = tuple(generated[channel][11] for channel in CHANNELS)
    require(generated_b10 in candidates, "la salida generada B10 no pertenece a la fibra G9")
    generated_index = candidates.index(generated_b10)

    generated_triads = {
        channel: triads_from_generated(channel)
        for channel in CHANNELS
    }
    checks: list[dict[str, object]] = []
    surviving_branches = 0
    for branch_index, candidate in enumerate(candidates):
        channel_checks: dict[str, object] = {}
        all_next = True
        for channel_index, channel in enumerate(CHANNELS):
            current_delta = int(detail_rows[branch_index][f"delta_options_{channel}"])
            current_blocks = generated[channel][:10] + [candidate[channel_index]]
            current_triads = generated_triads[channel][:9] + [current_delta]
            current_ok = cylinder_intersects(current_blocks, current_triads)
            next_blocks = current_blocks + [generated_b11[channel_index]]
            next_triads = current_triads + [generated_triads[channel][10]]
            next_ok = cylinder_intersects(next_blocks, next_triads)
            require(current_ok, f"G9 rama {branch_index}/{channel} no sobrevive h=1")
            all_next = all_next and next_ok
            channel_checks[channel] = {
                "current_delta": current_delta,
                "survives_h1": current_ok,
                "survives_generated_h2": next_ok,
            }
        if all_next:
            surviving_branches += 1
        checks.append(
            {
                "branch_index": branch_index,
                "candidate": list(candidate),
                "per_channel": channel_checks,
                "survives_all_channels_h2": all_next,
            }
        )

    require(surviving_branches == 1, "la poda generada no da 3->1")
    require(checks[generated_index]["survives_all_channels_h2"] is True,
            "la rama generada no es la superviviente")
    require(len({candidate[2] for candidate in candidates}) == 1, "phi no queda fijo")

    def trit_sum(left: str, right: str) -> str:
        return "".join(
            str((int(a) + int(b)) % 3)
            for a, b in zip(left, right)
        )

    aggregates = {trit_sum(candidate[0], candidate[1]) for candidate in candidates}
    require(len(aggregates) == 1, "pi+e no queda fijo")
    return {
        "input_B9": [generated[channel][9] for channel in CHANNELS],
        "candidate_outputs_B10": [list(candidate) for candidate in candidates],
        "generated_selected_index": generated_index,
        "generated_selected_B10": list(generated_b10),
        "generated_next_B11": list(generated_b11),
        "fixed_phi": candidates[0][2],
        "fixed_pi_plus_e": next(iter(aggregates)),
        "survivors_h1": 3,
        "survivors_h2_all_channels": surviving_branches,
        "checks": checks,
    }


def verify_orbital_certificate(gen_cert: dict[str, object]) -> dict[str, object]:
    orbit = json.loads(ORBIT_CERT.read_text(encoding="utf-8"))
    generated_words = gen_cert["catalogue"]["oriented_words_generated_by_selector"]
    published_words = {
        "pi": orbit["orientation_gauge"]["pi_word"],
        "e": orbit["orientation_gauge"]["e_word"],
        "phi": orbit["orientation_gauge"]["phi_word"],
    }
    require(generated_words == published_words, "selector orbital no coincide")
    generated_regions = gen_cert["catalogue"]["pi_microfiber"]["regions"]
    require(len(generated_regions) == 5, "no se conservaron las cinco regiones")
    require(
        sum(int(row["multiplicity"]) for row in generated_regions) == 1008,
        "las cinco regiones no suman 1008",
    )
    role_census = {
        role: sum(row["role"] == role for row in generated_regions)
        for role in ("++", "--", "transversal")
    }
    require(
        role_census == {"++": 3, "--": 1, "transversal": 1},
        "la microfibra no conserva 3++ + 1-- + 1 transversal",
    )
    expected_regions = {
        "501|614|498|169|272|272": {
            "Esig": "555555",
            "multiplicity": 432,
            "role": "transversal",
        },
        "810|923|870|169|272|272": {
            "Esig": "339555",
            "multiplicity": 144,
            "role": "++",
        },
        "810|983|810|169|272|272": {
            "Esig": "393555",
            "multiplicity": 144,
            "role": "++",
        },
        "870|923|810|169|272|272": {
            "Esig": "933555",
            "multiplicity": 144,
            "role": "++",
        },
        "870|923|810|418|674|521": {
            "Esig": "933717",
            "multiplicity": 144,
            "role": "--",
        },
    }
    observed_regions = {
        row["U6"]: {
            "Esig": row["Esig"],
            "multiplicity": int(row["multiplicity"]),
            "role": row["role"],
        }
        for row in generated_regions
    }
    require(
        observed_regions == expected_regions,
        "la identidad U6+Esig+multiplicidad+papel de pi no es canónica",
    )
    causal_isolation = gen_cert["causal_isolation"]
    require(
        causal_isolation["declared_primitives_used_not_loaded_from_external_files"]
        == ["L0", "L1"],
        "L0/L1 deben constar como primitivas declaradas usadas",
    )
    require(
        "archivos externos de L0 o L1" in causal_isolation["not_read"],
        "la auditoría debe distinguir uso de L0/L1 de lectura externa",
    )
    return {
        "oriented_words_match_active_certificate": True,
        "words": generated_words,
        "pi_regions_preserved": 5,
        "pi_total_multiplicity": 1008,
        "pi_role_census": role_census,
        "pi_region_identity_by_U6_Esig": observed_regions,
        "declared_primitives_used": ["L0", "L1"],
        "L0_L1_loaded_from_external_files": False,
        "active_selector_certificate_sha256": sha256_file(ORBIT_CERT),
    }


def verify_reference_digits() -> dict[str, object]:
    result: dict[str, object] = {}
    for channel in CHANNELS:
        generated_path = OUTPUT_DIR / f"{channel}_1000_decimales.txt"
        generated = generated_path.read_text(encoding="ascii")
        reference = REFERENCE_FILES[channel].read_text(encoding="ascii")
        require(generated == reference, f"{channel}: las 1000 cifras no coinciden")
        result[channel] = {
            "match_1000_digits_after_point": True,
            "generated_sha256": sha256_file(generated_path),
            "reference_sha256": sha256_file(REFERENCE_FILES[channel]),
            "reference_role": "control posterior; no entrada del generador",
        }
    return result


def verify_gate_ledger() -> dict[str, object]:
    rows = read_csv(OUTPUT_DIR / "ledger_396_bloques.csv")
    require(len(rows) == 3 * 396, "ledger generado con número de filas incorrecto")
    require(all(int(row["ambient_candidates"]) == 729 for row in rows),
            "ambiente distinto de 729")
    require(all(int(row["survivors"]) == 1 for row in rows),
            "alguna puerta no es unitaria")
    require(all(
        int(row["killed_before"]) + int(row["survivors"]) + int(row["killed_after"])
        == 729
        for row in rows
    ), "alguna partición no agota 729")

    phase_returns = 0
    complete_nonads = 0
    for channel in CHANNELS:
        channel_rows = [row for row in rows if row["channel"] == channel]
        require(len(channel_rows) == 396, f"{channel}: ledger incompleto")
        for k in range(396 - 9):
            before = channel_rows[k]
            after = channel_rows[k + 9]
            require(before["phase9"] == after["phase9"], "fase no conservada")
            require(before["prefix_sha256"] != after["prefix_sha256"],
                    "memoria reiniciada")
            require(
                (
                    before["block"],
                    before["candidate_index"],
                    before["witt_right"],
                    before["witt_weight"],
                )
                != (
                    after["block"],
                    after["candidate_index"],
                    after["witt_right"],
                    after["witt_weight"],
                ),
                "estado local repetido tras el retorno nonádico",
            )
            phase_returns += 1
        complete_nonads += len(list(range(0, 396 - 9, 9)))
    require(complete_nonads == 3 * 43, "conteo de vueltas nonádicas")
    return {
        "rows": len(rows),
        "ambient_partitions_exhaustive": True,
        "unitary_gates": True,
        "phase_return_pairs_all_channels": phase_returns,
        "complete_nonadic_returns_all_channels": complete_nonads,
        "law": (
            "g(K+9)=g(K); cambian tanto el estado prefijo-cilindro como "
            "el estado local bloque-indice-sombra-Witt"
        ),
    }


def main() -> None:
    required = [
        GENERATOR,
        GEN_CERT,
        PUBLISHED_LEDGER,
        PUBLISHED_READING,
        PUBLISHED_BRANCHES,
        PUBLISHED_DETAILS,
        ORBIT_CERT,
        *REFERENCE_FILES.values(),
    ]
    for path in required:
        require(path.is_file(), f"falta {path}")

    gen_cert = json.loads(GEN_CERT.read_text(encoding="utf-8"))
    require(
        gen_cert["status"] == "PASS_GENERACION_ESTRUCTURAL_1000_DECIMALES",
        "el certificado generador no está en PASS",
    )
    generated = load_generated_blocks()
    isolation = source_isolation_audit()
    require(
        gen_cert["generator_sha256"] == isolation["generator_sha256"],
        "el certificado no corresponde al generador actual",
    )
    finite_w30 = gen_cert["finite_chain"]["w30_generated_from_selected_words"]
    for channel in CHANNELS:
        require(
            finite_w30[channel] == generated[channel][:5],
            f"{channel}: la cadena finita w6->w30 no coincide con la prolongación",
        )
    result = {
        "schema": "HMT.ley-nueve-puertas.verificacion-contra-corpus.v1",
        "status": "PASS_VERIFICACION_INDEPENDIENTE_1000_DECIMALES",
        "causal_order": [
            "generación estructural ya escrita en disco",
            "auditoría estática del generador",
            "comparación con el corpus activo",
            "comparación final con testigos de 1000 cifras",
        ],
        "source_isolation": isolation,
        "orbital_selection": verify_orbital_certificate(gen_cert),
        "gate_ledger": verify_gate_ledger(),
        "published_twenty_block_window": verify_published_window(generated),
        "published_twelve_triads": verify_twelve_triads(generated),
        "gate_9_three_to_one_from_generated_future": verify_gate_three_to_one(generated),
        "reference_control_after_generation": verify_reference_digits(),
        "logical_conclusion": {
            "proved": (
                "el catálogo selecciona las tres biografías; los lectores exactos "
                "prolongan sus palabras; cada una de 396 puertas por canal agota "
                "729 candidatos y deja uno; 43 retornos nonádicos conservan fase "
                "sin reiniciar memoria; el cilindro final fija 1000 cifras"
            ),
            "not_used_as_input": (
                "los ledgers y las cifras de referencia sólo se abren en este "
                "verificador posterior"
            ),
            "exceptional_scope": (
                "cada bloque posee lift Paley--Witt; esta sombra conecta con el "
                "corredor excepcional pero no elige la rama decimal"
            ),
        },
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PASS_VERIFICACION_INDEPENDIENTE_1000_DECIMALES")
    print(OUTPUT)


if __name__ == "__main__":
    main()
