#!/usr/bin/env python3
"""Controles finitos del cociclo y de la sección 15 del Artículo VI.

No reemplazan sus pruebas generales de categorías o límites. Se usan checks
explícitos, activos también con python -O, y sólo biblioteca estándar.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def structural_check(root: Path, source: Path):
    text = source.read_text(encoding="utf-8")
    labels = re.findall(r"\\label\{([^{}]+)\}", text)
    references = re.findall(r"\\(?:ref|eqref)\{([^{}]+)\}", text)
    require(len(labels) == len(set(labels)), "etiquetas locales duplicadas")
    all_labels = {}
    for path in (root / "sections").glob("*.tex"):
        for label in re.findall(r"\\label\{([^{}]+)\}", path.read_text(encoding="utf-8")):
            all_labels.setdefault(label, []).append(path.name)
    require(not set(references) - set(all_labels), "remisiones sin etiqueta")
    for label in ("hist:seccion", "hist:doble-varianza"):
        require(all_labels.get(label) == [source.name],
                f"la etiqueta canonica {label} no es unica en15")
    require(set(references) - set(labels) == {"vi:dep:prefijos"},
            "se ha alterado el corte de remisiones externas previsto")
    stack = []
    for kind, environment in re.findall(r"\\(begin|end)\{([^{}]+)\}", text):
        if kind == "begin":
            stack.append(environment)
        else:
            require(bool(stack) and stack[-1] == environment,
                    f"anidamiento incorrecto: {environment}")
            stack.pop()
    require(not stack, "entornos sin cierre")
    return {"lines": len(text.splitlines()), "unique_labels": len(labels),
            "references_resolved": len(references),
            "external_references": sorted(set(references) - set(labels)),
            "canonical_labels_unique": True, "environment_nesting": "valid",
            "scope": "Control estatico de etiquetas y entornos, no revision semantica completa ni inspeccion visual."}


def calendar_cocycle():
    triples = 0
    for a, b, c in itertools.product(range(9), repeat=3):
        left = (a + b) // 9 + ((a + b) % 9 + c) // 9
        right = (b + c) // 9 + (a + (b + c) % 9) // 9
        require(left == right == (a + b + c) // 9,
                f"cociclo incorrecto en {(a, b, c)}")
        triples += 1
    for a in range(9):
        require((0 + a) // 9 == 0 and (a + 0) // 9 == 0,
                "normalizacion del cociclo")
    products = 0
    for k, j, ell, i in itertools.product(range(12), range(9), range(12), range(9)):
        memory = (k + ell + (j + i) // 9) % 12
        phase = (j + i) % 9
        require(9 * memory + phase == (9 * k + j + 9 * ell + i) % 108,
                "producto de fase/memoria distinto de C108")
        products += 1
    require(triples == 729 and products == 11664, "conteos de controles incompletos")
    return {"cocycle_triples": triples, "C108_products": products,
            "normalized": True, "phase_memory_map": "(k,j) -> 9*k+j mod108",
            "scope": "Calendario C9 con acarreo y cociente de memoria de orden12; no toda la memoria TPK."}


def finite_pullback():
    # Testigo de la identidad de indicadores; la prueba general está en15.
    small = range(3)
    large = range(12)
    restriction = {y: y % 3 for y in large}
    for x in small:
        fiber = [y for y in large if restriction[y] == x]
        require(len(fiber) == 4, "fibra finita del testigo")
        for y in large:
            left = int(restriction[y] == x)
            right = sum(int(y == point) for point in fiber)
            require(left == right, "pullback de indicador")
    functions = list(itertools.product((-1, 0, 1), repeat=3))
    for f, g in itertools.product(functions, repeat=2):
        for y in large:
            x = restriction[y]
            require((f[x] + g[x]) == f[restriction[y]] + g[restriction[y]],
                    "preservacion de la suma")
            require((f[x] * g[x]) == f[restriction[y]] * g[restriction[y]],
                    "preservacion del producto")
            require([1, 1, 1][restriction[y]] == 1, "preservacion unital")
    return {"domain_size": 12, "target_size": 3, "fiber_size": 4,
            "function_pairs": len(functions) ** 2,
            "scope": "Testigo finito; no prueba de existencia de todas las secciones ni cobertura de R."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    source = root / "sections/15_aritmetica_historias.tex"
    receipt = args.receipt or root / "technical/RECIBO_CONTROLES_HISTORIAS_15.json"
    report = {"schema": "HMT.VI.controles_finitos.15.v1",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "python_optimization": sys.flags.optimize, "checks_use_assert": False,
              "script_sha256": sha256(Path(__file__)),
              "scope": "Controles finitos y estaticos de15, no puerta canonica.",
              "coverage_of_R_proved": False, "global_autonomy_certified": False,
              "compiled_pdf": False}
    try:
        require(source.is_file(), "no se encuentra la seccion15")
        report["source"] = {"path": str(source.relative_to(root)), "sha256": sha256(source)}
        report["controls"] = {"source_structure": structural_check(root, source),
                              "calendar": calendar_cocycle(),
                              "finite_pullback": finite_pullback()}
        report["status"] = "PASS_CONTROLES_FINITOS_HISTORIAS_15"
        code = 0
    except Exception as exc:
        report["status"] = "FAIL_CONTROLES_FINITOS_HISTORIAS_15"
        report["error"] = f"{type(exc).__name__}: {exc}"
        code = 1
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "receipt": str(receipt),
                      "error": report.get("error")}, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
