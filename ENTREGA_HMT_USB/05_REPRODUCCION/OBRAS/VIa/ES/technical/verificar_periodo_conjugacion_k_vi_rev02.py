#!/usr/bin/env python3
"""Control exacto focal: período de K y conjugación incidencial de VI REV02.

Evalúa un testigo publicado y las identidades finitas indicadas. No genera el
libro terminal ni acredita por sí solo la genealogía completa del registro.
Los controles explícitos permanecen activos con python -O.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import re


def require(condition, name):
    if not condition:
        raise RuntimeError("FAIL: " + name)


def block(a, c, v):
    return 100 * (a % 10) + 10 * (c % 10) + v % 10


def reverse_counts(rows):
    return [(a, -c, v) for a, c, v in reversed(rows)]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent
    source = root / "sections/09_dependencias_anteriores.tex"
    raw = source.read_bytes()
    match = re.search(r"K=\(([\d,\s]+)\)\.\s*\\label\{vi:dep:K-testigo\}", raw.decode("utf-8"))
    require(match is not None, "localización del testigo K en fuente activa")
    k = tuple(int(x.strip()) for x in match.group(1).split(","))
    require(len(k) == 12 and all(0 <= x < 1000 for x in k), "doce bloques base mil")
    require(len(set(k)) == 12, "distinción de los doce bloques")
    block_periods = [d for d in range(1, 13) if all(k[i] == k[(i + d) % 12] for i in range(12))]
    require(block_periods == [12], "período mínimo de bloques")
    digits = "".join(f"{x:03d}" for x in k)
    decimal_periods = [d for d in range(1, 37) if all(digits[i] == digits[(i + d) % 36] for i in range(36))]
    require(decimal_periods == [36], "período mínimo de cifras")
    q = Fraction(int(digits), 10 ** 36 - 1)
    require(all(pow(10, d, q.denominator) != 1 for d in range(1, 36)), "ningún período racional menor")
    require(pow(10, 36, q.denominator) == 1, "retorno racional tras 36 cifras")
    require(q != Fraction(int(digits), 10 ** 36), "distinguir lectura finita de periódica")

    scalar_cases = 0
    for a in range(10):
        for v in range(10):
            for c in range(-31, 32):
                u = c % 10
                require((-c) % 10 == 10 * int(u != 0) - u, "residuo conjugado")
                require((-c) // 10 == -(c // 10) - int(u != 0), "cociente conjugado")
                require(block(a, -c, v) == block(a, c, v) + 100 * int(u != 0) - 20 * u, "bloque conjugado")
                scalar_cases += 1
    rows = [(m + 10, (-1) ** m * (19 * m + 7), 3 * m - 8) for m in range(12)]
    flipped = reverse_counts(rows)
    require(reverse_counts(flipped) == rows, "involutividad de recuentos")
    for m, row in enumerate(flipped):
        a, c, v = rows[11 - m]
        require(block(*row) == block(a, c, v) + 100 * int(c % 10 != 0) - 20 * (c % 10), "reversión de las doce ventanas")

    boundary_cases = 0
    closed_cases = 0
    for length in range(1, 7):
        for values in product((-1, 0, 2), repeat=length):
            forward = sum(values[:-1])
            backward = sum(values[:0:-1])
            require(backward == forward + values[-1] - values[0], "frontera de ruta inversa")
            if values[0] == values[-1]:
                require(backward == forward, "frontera cerrada nula")
                closed_cases += 1
            boundary_cases += 1
    require(sum((0, 1)[1:]) != sum((0, 1)[:-1]), "control negativo: omitir extremos altera ventana abierta")
    require(block(0, 1, 0) != block(0, 0, 0), "control negativo: frontera puede alterar bloque decimal")

    result = {
        "status": "PASS_CONTROL_EXACTO_PERIODO_CONJUGACION_K_VI_REV02",
        "scope": "Período exacto del testigo K publicado; reducción decimal conjugada; identidad de frontera en casos finitos. Las pruebas generales están en la sección 09. No reproduce la selección del libro terminal.",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source": str(source.relative_to(root)),
        "period_block": min(block_periods),
        "period_decimal": min(decimal_periods),
        "conjugation_scalar_cases": scalar_cases,
        "conjugation_window_cases": 12,
        "boundary_cases": boundary_cases,
        "closed_boundary_cases": closed_cases,
        "negative_controls": ["finite_vs_periodic", "open_boundary_not_omissible", "boundary_changes_decimal_block"],
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
