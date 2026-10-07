#!/usr/bin/env python3
"""Genera censos APP y controles finitos mediante aritmética entera.

Alcance: soporte APP de 81 posiciones, seis evaluaciones y controles focales.
Las comprobaciones por muestreo de enteros complementan las demostraciones
universales del capítulo; su alcance se declara expresamente en el recibo.
"""

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[2]
INVENTORY = (
    PROJECT / "output/INVENTARIO_GENEALOGICO_HMT_20260919/REV02_ARBOL/"
    "11_APP_CELDAS_COMPLETAS.json"
)
GENERATED = ROOT / "source/generated"
RECEIPT = ROOT / "metadata/CONTROLES_APP_EXACTOS.json"
D9 = tuple(range(1, 10))
Z9 = tuple(range(9))


def rho(n):
    if not isinstance(n, int) or n <= 0:
        raise ValueError("rho está definida aquí sobre enteros positivos")
    return 1 + (n - 1) % 9


def quotient(n):
    return (n - rho(n)) // 9


def section(a):
    return a % 9 or 9


def cocycle(a, b):
    return (section(a) + section(b) - section(a + b)) // 9


def cocycle_zero(a, b):
    return ((a % 9) + (b % 9) - ((a + b) % 9)) // 9


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def matrix_table(name, caption, values):
    lines = [
        "% Generado reproduciblemente por tools/generar_tablas_app.py.",
        r"\begin{tablacompleta}[htbp]",
        "\\caption{" + caption + "}",
        "\\label{tab:app-" + name + "}",
        r"\begin{tabular}{r*{9}{r}}",
        r"\toprule",
        "$i\\backslash j$ & " + " & ".join(map(str, D9)) + r" \\",
        r"\midrule",
    ]
    for i, row in zip(D9, values):
        lines.append(str(i) + " & " + " & ".join(map(str, row)) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{tablacompleta}", ""])
    return "\n".join(lines)


def row_totals_table(row_totals):
    lines = [
        "% Generado reproduciblemente por tools/generar_tablas_app.py.",
        r"\begin{tablacompleta}[htbp]",
        r"\caption{Evaluaciones acumuladas por fila del soporte APP.}",
        r"\label{tab:app-totales_filas}",
        r"\begin{tabular}{r*{6}{r}}",
        r"\toprule",
        r"$i$ & $\sum_j S$ & $\sum_j\Sigma$ & $\sum_j q_+$ & $\sum_j P$ & $\sum_j\Pi$ & $\sum_j q_\times$ \\",
        r"\midrule",
    ]
    for i, row in zip(D9, row_totals):
        lines.append(str(i) + " & " + " & ".join(map(str, row)) + r" \\")
    total = [sum(row[k] for row in row_totals) for k in range(6)]
    lines.extend([
        r"\midrule",
        "Total & " + " & ".join(map(str, total)) + r" \\",
        r"\bottomrule", r"\end{tabular}", r"\end{tablacompleta}", "",
    ])
    return "\n".join(lines)


def main():
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = {(r["i"], r["j"]): r for r in inventory["records"]}
    require(len(records) == 81, "El inventario debe contener 81 posiciones distintas")
    require(set(records) == set(product(D9, repeat=2)), "Soporte incompleto")

    matrices = {
        "suma": [[i + j for j in D9] for i in D9],
        "producto": [[i * j for j in D9] for i in D9],
        "residuo_suma": [[rho(i + j) for j in D9] for i in D9],
        "residuo_producto": [[rho(i * j) for j in D9] for i in D9],
        "cociente_suma": [[quotient(i + j) for j in D9] for i in D9],
        "cociente_producto": [[quotient(i * j) for j in D9] for i in D9],
    }
    expected_totals = {
        "suma": 810, "producto": 2025, "residuo_suma": 405,
        "residuo_producto": 459, "cociente_suma": 45, "cociente_producto": 174,
    }
    totals = {name: sum(map(sum, data)) for name, data in matrices.items()}
    require(totals == expected_totals, "Totales APP distintos de los esperados")
    compared_fields = 0
    for (i, j), row in records.items():
        for operation, n in (("additive", i + j), ("multiplicative", i * j)):
            expected = {
                "raw": n,
                "residue_positive_mod9": rho(n),
                "quotient_positive_mod9": quotient(n),
                "usual_remainder_mod9": n % 9,
                "remainder_mod1000": n % 1000,
                "quotient_mod1000": n // 1000,
            }
            require(row[operation] == expected, f"Diferencia en {i},{j}/{operation}")
            compared_fields += len(expected)
            require(n == rho(n) + 9 * quotient(n), f"Reconstrucción fallida: {n}")
    for operation, names in (
        ("additive", ("suma", "residuo_suma", "cociente_suma")),
        ("multiplicative", ("producto", "residuo_producto", "cociente_producto")),
    ):
        for key, name in zip(("raw", "residue_positive_mod9", "quotient_positive_mod9"), names):
            require(inventory["totals"][operation + "_" + key] == totals[name], "Total discrepante con inventario")

    require([rho(10), quotient(10), rho(25), quotient(25)] == [1, 1, 7, 2], "Centro APP")
    central_fixed = [(i, j) for i, j in product(D9, repeat=2) if (i, j) == (10 - i, 10 - j)]
    require(central_fixed == [(5, 5)], "Punto fijo de la inversión central")
    transpose_fixed = [(i, j) for i, j in product(D9, repeat=2) if i == j]
    require(len(transpose_fixed) == 9, "Puntos fijos de transposición")

    for a, b, c in product(Z9, repeat=3):
        require(cocycle(a, b) + cocycle(a + b, c) == cocycle(b, c) + cocycle(a, b + c), "Identidad de cociclo")
    for a, b in product(Z9, repeat=2):
        delta = int(a == 0) + int(b == 0) - int((a + b) % 9 == 0)
        require(cocycle(a, b) == cocycle_zero(a, b) + delta, "Cambio de sección")
    require(all(cocycle(0, a) == 1 for a in Z9), "Normalización de sección positiva")

    vertices = set(product(Z9, repeat=2))
    steps = ((-1, 0), (0, 1), (1, 0), (0, -1))
    directed = {((i, j), ((i + di) % 9, (j + dj) % 9)) for i, j in vertices for di, dj in steps}
    undirected = {tuple(sorted(edge)) for edge in directed}
    require(len(directed) == 324 and len(undirected) == 162, "Censo del grafo")
    require(all((b, a) in directed for a, b in directed), "Inversión de aristas")
    require(all(sum(a == v for a, b in directed) == 4 for v in vertices), "Valencia de salida")

    radical = {0, 3, 6}
    require({3 * x % 9 for x in Z9} == radical, "Imagen de multiplicación por tres")
    require({x for x in Z9 if 3 * x % 9 == 0} == radical, "Núcleo de multiplicación por tres")
    require({a * b % 9 for a, b in product(radical, repeat=2)} == {0}, "Cuadrado del radical")
    units = [a for a in Z9 if any(a * b % 9 == 1 for b in Z9)]
    require(units == [1, 2, 4, 5, 7, 8], "Unidades del anillo")
    row_images = {str(i): sorted({i * j % 9 for j in Z9}) for i in D9}
    require([len(row_images[str(i)]) for i in D9] == [9, 9, 3, 9, 9, 3, 9, 9, 1], "Rangos de filas multiplicativas")
    row_counts = {str(i): dict(sorted(Counter(i * j % 9 for j in Z9).items())) for i in D9}
    require(row_counts["3"] == {0: 3, 3: 3, 6: 3} and row_counts["6"] == {0: 3, 3: 3, 6: 3}, "Multiplicidades del radical")
    require(row_counts["9"] == {0: 9}, "Fila nula del cociente")

    sum_counts = Counter(i + j for i, j in product(D9, repeat=2))
    require(all(sum_counts[k] == (k - 1 if k <= 10 else 19 - k) for k in range(2, 19)), "Multiplicidades de suma")

    # Control finito: todos los enteros hasta 250000 y todos los bloques para
    # una selección determinista de cocientes, incluidos cocientes muy grandes.
    sampled = set(range(1, 250001))
    selected_quotients = [0, 1, 8, 9, 10, 110, 111, 112, 728, 729, 999, 1000, 10**6, 10**12, 10**30, 10**100]
    for q in selected_quotients:
        sampled.update(1000 * q + b for b in range(1000) if 1000 * q + b > 0)
    for n in sampled:
        q, b = divmod(n, 1000)
        require(rho(n) == rho(q + b), "Compatibilidad del residuo 9/1000")
        require(quotient(n) == 111 * q + quotient(q + b), "Compatibilidad del cociente 9/1000")

    GENERATED.mkdir(parents=True, exist_ok=True)
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    captions = {
        "suma": r"Evaluación aditiva entera: $S(i,j)=i+j$.",
        "producto": r"Evaluación multiplicativa entera: $P(i,j)=ij$.",
        "residuo_suma": r"Representantes positivos de la evaluación aditiva: $\Sigma(i,j)=\rho_9(i+j)$.",
        "residuo_producto": r"Matriz principal de APP: multiplicación reducida por raíz digital positiva, $\Pi(i,j)=\rho_9(ij)$.",
        "cociente_suma": r"Cocientes de la evaluación aditiva: $q_+(i,j)=q_9(i+j)$.",
        "cociente_producto": r"Cocientes de la evaluación multiplicativa: $q_\times(i,j)=q_9(ij)$.",
    }
    outputs = []
    for name, data in matrices.items():
        path = GENERATED / (name + ".tex")
        path.write_text(matrix_table(name, captions[name], data), encoding="utf-8")
        outputs.append(path)
    row_order = ("suma", "residuo_suma", "cociente_suma", "producto", "residuo_producto", "cociente_producto")
    row_totals = [[sum(matrices[name][i]) for name in row_order] for i in range(9)]
    totals_path = GENERATED / "totales_filas.tex"
    totals_path.write_text(row_totals_table(row_totals), encoding="utf-8")
    outputs.append(totals_path)

    receipt = {
        "schema_version": "1.0",
        "status": "PASS_APP_EXACTO_FOCAL",
        "result_id": "APP_TABLAS_ENTERAS_Y_CONTROLES_REV02",
        "scope": "APP_INTERNAL",
        "causal_cutoff": "APP",
        "provenance_status": "CERTIFICADO_NUEVO",
        "evidence_type": "ENUMERACION_EXHAUSTIVA_FINITA_Y_CONTROLES_ENTEROS_MUESTREADOS",
        "external_constant_inputs": [],
        "inventory": {"path": str(INVENTORY), "sha256": digest(INVENTORY)},
        "script": {"path": str(Path(__file__).resolve()), "sha256": digest(Path(__file__))},
        "checks": {
            "cells_against_inventory": 81,
            "scalar_fields_compared": compared_fields,
            "totals": totals,
            "cell_reconstructions": 162,
            "central_fixed_points": central_fixed,
            "transpose_fixed_points": len(transpose_fixed),
            "transpose_nonfixed_pairs": 36,
            "cocycle_triples_exhaustive": 729,
            "section_change_pairs_exhaustive": 81,
            "graph": {"vertices": 81, "directed_edges": len(directed), "undirected_edges": len(undirected), "outdegree": 4},
            "radical": {"elements": sorted(radical), "square": [0], "kernel_multiply_three": sorted(radical), "image_multiply_three": sorted(radical)},
            "units": units,
            "multiplicative_row_images": row_images,
            "multiplicative_row_multiplicities": row_counts,
            "additive_value_multiplicities": dict(sorted(sum_counts.items())),
            "base1000": {
                "kind": "FINITE_SAMPLE_COMPLEMENT_TO_SYMBOLIC_PROOF",
                "sample_count": len(sampled),
                "consecutive_positive_range": [1, 250000],
                "additional_quotients_all_1000_blocks": selected_quotients,
                "max_sample": max(sampled),
                "identities": ["rho9(N)=rho9(Q+B)", "q9(N)=111Q+q9(Q+B)"],
                "hypotheses": "N>0, N=1000Q+B, Q>=0, 0<=B<1000",
                "universal_proof_claimed_by_sample": False,
            },
        },
        "generated_tables": [{"path": str(p), "sha256": digest(p)} for p in outputs],
        "global_HMT_results_verified_here": False,
        "proof_residence": "source/chapters/01_app.tex; las pruebas universales pertenecen al capítulo, no al muestreo",
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS_APP_EXACTO_FOCAL tables={len(outputs)} cells=81 cocycle=729 section_change=81 base1000_samples={len(sampled)}")
    print(str(RECEIPT))


if __name__ == "__main__":
    main()
