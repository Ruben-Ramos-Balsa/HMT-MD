#!/usr/bin/env python3
"""Auditor independiente del producto nativo sobre palabras nonádicas."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CERTIFICATE = ROOT / "certificados/producto_nativo_generador.json"
OUT = ROOT / "certificados/producto_nativo_auditoria.json"


def load_module_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"no se puede cargar el módulo {name} desde {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


a9_native = load_module_from_path("a9_native", HERE / "a9_native.py")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"AUDITORÍA DEL PRODUCTO NATIVO FAIL: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def function_node(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise RuntimeError(f"funcion ausente: {name}")


def calls_in(node: ast.AST) -> set[str]:
    calls: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name):
                calls.add(child.func.id)
            elif isinstance(child.func, ast.Attribute):
                calls.add(child.func.attr)
    return calls


def independent_bijective9(value: int) -> tuple[int, ...]:
    digits: list[int] = []
    while value:
        value, residue = divmod(value - 1, 9)
        digits.append(residue + 1)
    return tuple(digits)


def is_prime_external(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audita el producto nativo sin modificar el árbol por defecto."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="escribe explícitamente el certificado de auditoría canónico",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_path = HERE / "a9_native.py"
    generator_path = HERE / "generar_certificado_producto_nativo.py"
    source_tree = ast.parse(source_path.read_text(encoding="utf-8"))
    generator_tree = ast.parse(generator_path.read_text(encoding="utf-8"))

    product_node = function_node(source_tree, "native_product_words")
    product_calls = calls_in(product_node)
    forbidden_product_calls = {
        "word_value",
        "encode_bijective9",
        "native_product",
        "factorization",
        "isprime",
        "zeta",
    }
    require(
        not product_calls.intersection(forbidden_product_calls),
        "el producto nativo consulta su evaluacion o un oraculo externo",
    )
    require(
        not any(isinstance(node, ast.Mult) for node in ast.walk(product_node)),
        "el cuerpo del producto multiplica evaluaciones en vez de usar Horner A9#",
    )

    imported_modules = {
        alias.name
        for node in ast.walk(generator_tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    require(
        not imported_modules.intersection(
            {"sympy", "sage", "mpmath", "numpy", "primesieve", "zeta"}
        ),
        "el generador importa datos o algebra externos no declarados",
    )

    with tempfile.TemporaryDirectory(prefix="hmt-producto-nativo-") as tmp_name:
        tmp_root = Path(tmp_name)
        tmp_python = tmp_root / "pruebas" / "python"
        tmp_certificates = tmp_root / "certificados"
        tmp_python.mkdir(parents=True)
        tmp_certificates.mkdir(parents=True)
        shutil.copy2(source_path, tmp_python / source_path.name)
        shutil.copy2(generator_path, tmp_python / generator_path.name)
        completed = subprocess.run(
            [
                sys.executable,
                "-O",
                "-S",
                str(tmp_python / generator_path.name),
            ],
            cwd=tmp_root,
            check=False,
            capture_output=True,
            text=True,
        )
        require(completed.returncode == 0, "el generador falla bajo python -O")
        generated_certificate = (
            tmp_certificates / "producto_nativo_generador.json"
        )
        require(generated_certificate.exists(), "el generador no produjo certificado")
        data = json.loads(generated_certificate.read_text(encoding="utf-8"))

    active_data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(
        active_data == data,
        "el certificado activo no coincide con la regeneración temporal",
    )
    require(data["status"] == "PASS", "certificado generador no PASS")
    require(
        data["declared_premise"] == "extensión aritmética local A9# sobre D9={1,...,9}",
        "premisa local declarada",
    )

    expected_cells = []
    expected_tables = {
        "R_plus": [],
        "Q_plus": [],
        "R_times": [],
        "Q_times": [],
    }
    for operation in ("plus", "times"):
        for left in range(1, 10):
            residue_row: list[int] = []
            quotient_row: list[int] = []
            for right in range(1, 10):
                total = left + right if operation == "plus" else left * right
                residue = total % 9 or 9
                quotient = (total - residue) // 9
                cell = a9_native.lifted_cell(operation, left, right)
                require(
                    (cell.residue, cell.quotient) == (residue, quotient),
                    f"celda local incorrecta {operation}({left},{right})",
                )
                expected_cells.append((operation, left, right, residue, quotient))
                residue_row.append(residue)
                quotient_row.append(quotient)
            expected_tables[f"R_{operation}"].append(residue_row)
            expected_tables[f"Q_{operation}"].append(quotient_row)
    require(data["cell_tables"] == expected_tables, "las cuatro tablas A9# no coinciden")

    cocycle_errors = {
        "additive_associativity": 0,
        "multiplicative_associativity": 0,
        "lifted_distributivity": 0,
    }
    for left in range(1, 10):
        for middle in range(1, 10):
            for right in range(1, 10):
                rp_lm, qp_lm = a9_native.a9_add(left, middle)
                rp_mr, qp_mr = a9_native.a9_add(middle, right)
                cocycle_errors["additive_associativity"] += (
                    qp_lm + a9_native.a9_add(rp_lm, right)[1]
                    != qp_mr + a9_native.a9_add(left, rp_mr)[1]
                )

                rx_lm, qx_lm = a9_native.a9_multiply(left, middle)
                rx_mr, qx_mr = a9_native.a9_multiply(middle, right)
                cocycle_errors["multiplicative_associativity"] += (
                    a9_native.a9_multiply(rx_lm, right)[1] + right * qx_lm
                    != a9_native.a9_multiply(left, rx_mr)[1] + left * qx_mr
                )

                rx_lr, qx_lr = a9_native.a9_multiply(left, right)
                cocycle_errors["lifted_distributivity"] += (
                    a9_native.a9_multiply(left, rp_mr)[1] + left * qp_mr
                    != a9_native.a9_add(rx_lm, rx_lr)[1] + qx_lm + qx_lr
                )
    require(not any(cocycle_errors.values()), "fallo en cociclos locales")

    roundtrip_limit = 20000
    for value in range(roundtrip_limit + 1):
        word = a9_native.encode_bijective9(value)
        require(word == independent_bijective9(value), "codificacion no independiente")
        require(a9_native.word_value(word) == value, "roundtrip base nueve")

    pair_limit = 512
    pair_checks = 0
    for left in range(pair_limit + 1):
        for right in range(pair_limit + 1):
            actual = a9_native.native_product(left, right)
            require(actual == left * right, f"entrelazador falla en {left},{right}")
            pair_checks += 1

    add_limit = 500
    for left in range(add_limit + 1):
        for right in range(add_limit + 1):
            word = a9_native.add_words(
                a9_native.encode_bijective9(left),
                a9_native.encode_bijective9(right),
            )
            require(a9_native.word_value(word) == left + right, "hoja aditiva global")

    factor_limit = data["native_coproduct"]["limit"]
    native_irreducibles = tuple(data["native_coproduct"]["irreducibles"])
    external_irreducibles = tuple(
        value for value in range(2, factor_limit + 1) if is_prime_external(value)
    )
    require(
        native_irreducibles == external_irreducibles,
        "el selector nativo no coincide con el control externo",
    )

    visible_failure = data["negative_controls"]["visible_only"]
    require(visible_failure["left"] == 2 and visible_failure["right"] == 5,
            "control visible inesperado")
    require(visible_failure["visible_only"] == 1, "resto del control visible")
    require(visible_failure["exact"] == 10, "valor exacto del control visible")
    perturbation = data["negative_controls"]["perturb_Q_times_9_9_minus_one"]
    require(
        (perturbation["canonical"], perturbation["perturbed"], perturbation["defect"])
        == (81, 72, -9),
        "la ablacion de memoria no detecta el borde 9x9",
    )

    require(data["native_source_sha256"] == sha256(source_path), "hash fuente nativa")

    audit = {
        "schema": "HMT.producto-nativo-A9.auditoria.v1",
        "status": "PASS",
        "generator_exit_under_O": completed.returncode,
        "native_source_sha256": sha256(source_path),
        "generator_source_sha256": sha256(generator_path),
        "local_cells_recomputed": len(expected_cells),
        "local_cocycle_triples_recomputed_each": 9**3,
        "local_cocycle_errors": cocycle_errors,
        "roundtrips_recomputed": roundtrip_limit + 1,
        "intertwiner_pairs_recomputed": pair_checks,
        "additive_pairs_recomputed": (add_limit + 1) ** 2,
        "native_irreducibles_checked": len(native_irreducibles),
        "static_gate": {
            "product_calls": sorted(product_calls),
            "forbidden_product_calls_found": sorted(
                product_calls.intersection(forbidden_product_calls)
            ),
            "external_arithmetic_inside_product_body": False,
            "forbidden_generator_imports_found": [],
        },
        "scope": {
            "positive_sector_unitary_only": True,
            "zero_requires_adjoined_vacuum": True,
            "K_radix_not_yet_full_K_APP_history": True,
            "global_EF_G9_compatibility": "NOT_PROVED",
        },
    }
    rendered = json.dumps(audit, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
