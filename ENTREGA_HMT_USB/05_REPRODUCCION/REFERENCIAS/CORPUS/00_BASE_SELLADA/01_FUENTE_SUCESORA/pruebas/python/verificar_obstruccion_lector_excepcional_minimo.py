#!/usr/bin/env python3
"""Certifica la obstrucción de factorización del lector excepcional mínimo.

El cálculo usa el catálogo normativo de 468 estados regionales. Reconstruye
la palabra ternaria visible, la codifica mediante la matriz de Paley--Witt y
compara exactamente las fibras del lector visible con las de su producto
diagonal junto al soporte excepcional. Todas las comprobaciones permanecen
activas bajo ``python -O``.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "datos/TPK_U_catalog_468.json"
FIBRE_TABLE = ROOT / "datos/obstruccion_lector_excepcional_minimo_fibras.csv"
OUTPUT = ROOT / "certificados/obstruccion_lector_excepcional_minimo.json"

AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)
PI_WORD = "010211"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("OBSTRUCCION_LECTOR_MINIMO FAIL: " + message)


def codeword(word: str) -> tuple[int, ...]:
    left = tuple(int(value) for value in word)
    require(len(left) == 6 and set(left) <= {0, 1, 2}, "palabra fuera de F3^6")
    right = tuple(
        sum(left[row] * AW[row][column] for row in range(6)) % 3
        for column in range(6)
    )
    return left + right


def support(word: str) -> tuple[int, ...]:
    return tuple(index + 1 for index, value in enumerate(codeword(word)) if value)


def visible_word(row: dict[str, Any]) -> str:
    return "".join(str((-int(value)) % 3) for value in str(row["U6"]).split("|"))


def histogram(fibres: dict[Any, list[str]]) -> dict[str, int]:
    return {
        str(size): count
        for size, count in sorted(Counter(len(values) for values in fibres.values()).items())
    }


def build_certificate() -> tuple[dict[str, Any], list[dict[str, int]]]:
    require(CATALOGUE.is_file(), "falta el catálogo de 468 estados")
    rows = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    require(isinstance(rows, list) and len(rows) == 468, "cardinal del catálogo")
    require(sum(int(row["count"]) for row in rows) == 104_976, "peso total de semillas")

    visible_fibres: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        visible_fibres[visible_word(row)].append(str(row["U6"]))
    require(len(visible_fibres) == 243, "imagen visible")

    supports = {word: support(word) for word in visible_fibres}
    support_fibres: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for word, incidence in supports.items():
        support_fibres[incidence].append(word)

    diagonal_fibres: dict[tuple[str, tuple[int, ...]], list[str]] = defaultdict(list)
    for row in rows:
        word = visible_word(row)
        diagonal_fibres[(word, supports[word])].append(str(row["U6"]))

    visible_partition = sorted(sorted(values) for values in visible_fibres.values())
    diagonal_partition = sorted(sorted(values) for values in diagonal_fibres.values())
    require(diagonal_partition == visible_partition, "igualdad exacta de particiones")

    expected_histogram = {"1": 132, "2": 66, "3": 18, "4": 3, "5": 6, "6": 18}
    visible_histogram = histogram(visible_fibres)
    diagonal_histogram = histogram(diagonal_fibres)
    require(visible_histogram == expected_histogram, "histograma visible")
    require(diagonal_histogram == expected_histogram, "histograma diagonal")

    support_histogram = histogram(support_fibres)
    require(len(support_fibres) == 213, "número de soportes excepcionales")
    require(support_histogram == {"1": 185, "2": 27, "4": 1}, "histograma de soportes")

    pi_regions = sorted(visible_fibres[PI_WORD])
    require(len(pi_regions) == 5, "microfibra de pi")
    require(supports[PI_WORD] == (2, 4, 5, 6, 7, 8, 9, 10, 11), "soporte de pi")

    table: list[dict[str, int]] = []
    sizes = sorted({int(size) for size in expected_histogram} | {int(size) for size in support_histogram})
    for size in sizes:
        table.append(
            {
                "tamano_fibra": size,
                "fibras_lector_visible": int(visible_histogram.get(str(size), 0)),
                "fibras_lector_diagonal": int(diagonal_histogram.get(str(size), 0)),
                "fibras_soporte_sobre_palabras": int(support_histogram.get(str(size), 0)),
            }
        )

    certificate = {
        "schema": "HMT.obstruccion-factorizacion-lector-excepcional-minimo.v1",
        "status": "PASS_EXACT_MINIMAL_EXCEPTIONAL_READER_OBSTRUCTION",
        "uses_physical_targets": False,
        "domain_states": len(rows),
        "seed_weighted_total": sum(int(row["count"]) for row in rows),
        "visible_words": len(visible_fibres),
        "exceptional_supports": len(support_fibres),
        "factorization": "Q_min=Supp o c o Psi",
        "equivalence_relation_identity": "Eq(Psi,Q_min)=Eq(Psi)",
        "kernel_shorthand_identity": "ker(Psi,Q_min)=ker(Psi)",
        "visible_fibre_histogram": visible_histogram,
        "diagonal_fibre_histogram": diagonal_histogram,
        "support_fibre_histogram_on_visible_words": support_histogram,
        "pi_word": PI_WORD,
        "pi_regions_U6": pi_regions,
        "pi_common_exceptional_support": list(supports[PI_WORD]),
        "joint_faithfulness_on_468_states": False,
        "scope": (
            "The obstruction applies exactly to every exceptional reader that factors "
            "through the visible word Psi. It does not apply to a reader of orientation, "
            "sheet, signature, return or other pre-quotient fields of the enriched state."
        ),
    }
    return certificate, table


def main() -> None:
    certificate, table = build_certificate()
    FIBRE_TABLE.parent.mkdir(parents=True, exist_ok=True)
    with FIBRE_TABLE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]))
        writer.writeheader()
        writer.writerows(table)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(certificate, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_OBSTRUCCION_LECTOR_EXCEPCIONAL_MINIMO")


if __name__ == "__main__":
    main()
