#!/usr/bin/env python3
"""Verifica los deltas finitos recuperados del corpus de mayo de 2024.

La prueba distingue tres objetos: la clasificación Witt de 56 familias, la
taxonomía externa de 114 expresiones y la trazabilidad tipada —no biyectiva—
entre los inventarios TPK de 87 y 34 entradas.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from ast import literal_eval
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

# Matriz generadora activa del codigo de Golay ternario extendido, con el
# etiquetado dodecafasico vigente. Es la misma matriz A_W usada por el
# verificador de incidencia Witt del corpus.
AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path, *, delimiter: str = ",") -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def ternary_codeword(left: tuple[int, ...]) -> tuple[int, ...]:
    right = tuple(
        sum(left[row] * AW[row][column] for row in range(6)) % 3
        for column in range(6)
    )
    return left + right


def construct_witt_design() -> set[frozenset[int]]:
    words = [
        ternary_codeword(left)
        for left in itertools.product(range(3), repeat=6)
    ]
    require(len(words) == 729, "W12 debe reconstruirse desde 729 palabras")
    weight_enumerator = Counter(
        sum(value != 0 for value in word) for word in words
    )
    require(
        weight_enumerator == Counter({0: 1, 6: 264, 9: 440, 12: 24}),
        "enumerador de pesos del Golay ternario extendido incorrecto",
    )

    hexads = {
        frozenset(index + 1 for index, value in enumerate(word) if value)
        for word in words
        if sum(value != 0 for value in word) == 6
    }
    require(len(hexads) == 132, "W12 debe contener 132 hexadas")
    five_counts = Counter(
        subset
        for hexad in hexads
        for subset in itertools.combinations(sorted(hexad), 5)
    )
    require(
        len(five_counts) == math.comb(12, 5)
        and set(five_counts.values()) == {1},
        "las hexadas reconstruidas no satisfacen S(5,6,12)",
    )
    universe = frozenset(range(1, 13))
    require(
        all(universe - hexad in hexads for hexad in hexads),
        "W12 no es cerrado por complemento",
    )
    return hexads


def parse_support(value: str, *, field: str) -> frozenset[int]:
    try:
        parsed = literal_eval(value)
    except (SyntaxError, ValueError) as exc:
        raise RuntimeError(f"soporte invalido en {field}: {value!r}") from exc
    require(isinstance(parsed, (tuple, list)), f"{field} no es una sucesion")
    require(
        all(isinstance(point, int) and 1 <= point <= 12 for point in parsed),
        f"{field} contiene una posicion fuera de 1,...,12",
    )
    support = frozenset(parsed)
    require(len(support) == len(parsed), f"{field} contiene posiciones repetidas")
    return support


def parse_bool(value: str, *, field: str) -> bool:
    require(value in {"True", "False"}, f"booleano invalido en {field}")
    return value == "True"


def supports_from_tau(tau: str) -> dict[str, frozenset[int]]:
    require(len(tau) == 12, "tau12 debe tener doce fases")
    require(set(tau) <= {"+", "-", "0"}, "tau12 usa un simbolo no tritico")
    positive = frozenset(index + 1 for index, value in enumerate(tau) if value == "+")
    negative = frozenset(index + 1 for index, value in enumerate(tau) if value == "-")
    active = positive | negative
    require(not (positive & negative), "los soportes positivo y negativo se solapan")
    return {"active": active, "neg": negative, "pos": positive}


def classify_witt_support(
    support: frozenset[int],
    completions: int,
    is_hexad: bool,
) -> str:
    if len(support) > 6 and completions == 0 and not is_hexad:
        return "overfull support / obstruction (>6)"
    if len(support) == 6 and completions == 0 and not is_hexad:
        return "6-set non-Witt / obstruction"
    if len(support) == 6 and completions == 1 and is_hexad:
        return "Witt hexad"
    if len(support) == 4 and completions == 4 and not is_hexad:
        return "4-face -> star of 4 hexads"
    raise RuntimeError(
        "clase Witt no contemplada: "
        f"size={len(support)} completions={completions} is_hexad={is_hexad}"
    )


def verify_witt() -> None:
    raw = (
        ROOT
        / "datos"
        / "procedencia_corpus_may24"
        / "CT108_all_56_families_with_antisection_tests.csv"
    )
    require(raw.is_file(), "falta el catálogo Witt de 56 familias")
    require(
        digest(raw)
        == "a584dde6a7b120dc3412ce4d6b8e54c0b847e8460427d484bf0256410070a991",
        "el catálogo Witt no es byte-idéntico al testigo recibido",
    )
    rows = read_csv(raw)
    require(len(rows) == 56, "el dominio Witt debe contener 56 familias")
    require(
        len(
            {
                (row["tau12"], row["mult"], row["rep_r0"], row["rep_c0"])
                for row in rows
            }
        )
        == 56,
        "el catalogo contiene familias duplicadas",
    )

    hexads = construct_witt_design()
    recomputed_classes: dict[str, Counter[str]] = {
        side: Counter() for side in ("active", "neg", "pos")
    }
    for row_number, row in enumerate(rows, start=2):
        supports = supports_from_tau(row["tau12"])
        for side, support in supports.items():
            prefix = f"fila {row_number}, {side}"
            stored_support = parse_support(
                row[f"{side}_support"], field=f"{prefix}_support"
            )
            require(
                stored_support == support,
                f"{prefix}: el soporte no coincide con tau12",
            )
            require(
                int(row[f"{side}_size"]) == len(support),
                f"{prefix}: cardinal de soporte incorrecto",
            )

            completions = sum(support <= hexad for hexad in hexads)
            is_hexad = support in hexads
            computed_class = classify_witt_support(
                support, completions, is_hexad
            )
            require(
                int(row[f"{side}_witt_completions"]) == completions,
                f"{prefix}: numero de completaciones Witt incorrecto",
            )
            require(
                parse_bool(row[f"{side}_is_hexad"], field=f"{prefix}_is_hexad")
                == is_hexad,
                f"{prefix}: indicador de hexada incorrecto",
            )
            require(
                row[f"{side}_witt_class"] == computed_class,
                f"{prefix}: clase Witt incorrecta",
            )
            recomputed_classes[side][computed_class] += 1

    negative = recomputed_classes["neg"]
    positive = recomputed_classes["pos"]
    require(
        negative
        == Counter(
            {
                "6-set non-Witt / obstruction": 50,
                "4-face -> star of 4 hexads": 6,
            }
        ),
        "censo Witt negativo distinto de 50+6",
    )
    require(
        positive
        == Counter(
            {
                "6-set non-Witt / obstruction": 36,
                "4-face -> star of 4 hexads": 20,
            }
        ),
        "censo Witt positivo distinto de 36+20",
    )
    require(
        recomputed_classes["active"]
        == Counter({"overfull support / obstruction (>6)": 56}),
        "el censo del soporte activo no contiene 56 obstrucciones por sobre-soporte",
    )


def verify_taxonomy() -> None:
    path = ROOT / "datos" / "atlas_taxonomico_114_constantes_rev11.csv"
    rows = read_csv(path)
    require(rows[-1]["family"] == "TOTAL", "falta la fila total del atlas")
    require(int(rows[-1]["count"]) == 114, "el atlas no totaliza 114 entradas")
    require(
        rows[-1]["unique_readings_role"] == "106_distinct_triadic_readings",
        "el atlas no conserva las 106 lecturas distintas",
    )
    require(
        sum(int(row["count"]) for row in rows[:-1]) == 114,
        "las nueve familias taxonómicas no suman 114",
    )
    require(
        all(row["status"] == "EXTERNAL_VALUES_TAXONOMY" for row in rows),
        "una fila del atlas promueve indebidamente taxonomía a generación",
    )


def verify_tpk_traceability() -> None:
    matrix = ROOT / "gestion" / "MATRIZ_TRAZABILIDAD_TPK_87_34_REV11.tsv"
    certificate = ROOT / "certificados" / "trazabilidad_tpk_87_34_rev11.json"
    payload = json.loads(certificate.read_text(encoding="utf-8"))
    rows = read_csv(matrix, delimiter="\t")
    require(len(rows) == 87, "la matriz TPK debe conservar 87 filas históricas")
    require(
        [row["historical_id"] for row in rows]
        == [f"TPK-{number:03d}" for number in range(1, 88)],
        "los identificadores TPK históricos no son completos o están desordenados",
    )
    explicit = sum(bool(row["canonical_ids"].strip()) for row in rows)
    require(explicit == 25, "el número de relaciones canónicas explícitas no es 25")
    require(
        payload["rows_preserved_without_forced_equivalence"] == 62,
        "el certificado no conserva las 62 filas sin equivalencia forzada",
    )
    require(
        payload["canonical_operator_rows"] == 34,
        "el registro canónico no declara 34 operadores",
    )
    require(payload["matrix_sha256"] == digest(matrix), "hash de matriz TPK inválido")
    require(
        payload["status"] == "PASS_TPK_TRACEABILITY_TYPED_NONBIJECTIVE",
        "estatuto de trazabilidad TPK inválido",
    )


def main() -> int:
    verify_witt()
    verify_taxonomy()
    verify_tpk_traceability()
    print("PASS_DELTAS_CORPUS_MAY24_REV11")
    print("w12_words=729 weight_enumerator=1+264z^6+440z^9+24z^12 hexads=132")
    print("witt_families=56 negative=50+6 positive=36+20")
    print("taxonomy_entries=114 distinct_readings=106")
    print("tpk_historical=87 canonical=34 explicit_relations=25 forced_equivalences=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
