#!/usr/bin/env python3
"""Control independiente posterior; mpmath se usa sólo en el testigo final."""
import argparse
import ast
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("finite_parts", HERE/"partes_finitas_exactas.py")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def expect_rejection(function, *args):
    try:
        function(*args)
    except (ValueError, TypeError):
        check(True, "rechazo")
    else:
        check(False, "Se aceptó un dominio no admisible")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    # Se producen todas las salidas antes de cargar el comparador externo.
    gamma_runs = [(n, p, producer.gamma_interval(n, p, 120))
                  for n in (1, 2, 3, 9, 27, 81) for p in (1, 2, 4, 8)]
    zeta_runs = [(s, n, p, producer.zeta_positive_integer_interval(s, n, p))
                 for s in (2, 3, 5, 7) for n in (1, 3, 9, 27, 81)
                 for p in (1, 2, 4, 8)]
    logs = [(F(a,b), producer.log_ratio_interval(F(a,b), 120))
            for a in (1, 2, 3, 9, 81, 1000) for b in (1, 2, 7)]
    b = producer.bernoulli(20)
    for m in range(1, 21):
        check(sum((F(producer.binomial(m+1,k))*b[k] for k in range(m+1)), F()) == 0,
              "Recurrencia de Bernoulli")
    for n in range(1, 109):
        check(producer.regularized_minus_one(n) == F(-1,12), "Independencia de N en -1")
    words = list(producer.native_initial_segment(729))
    check([value for _,value in words] == list(range(1,730)), "Sucesor nativo")
    check(words[80][0] == (9,8), "Forma de 81")
    check(words[728][0] == (9,8,8), "Forma de 729")
    for val in (F(1,3), F(-1,3), F(0), F(-7,2), F(17,8)):
        for digits in (0, 1, 3, 12):
            lo = F(producer.decimal_bound(val, digits))
            hi = F(producer.decimal_bound(val, digits, upper=True))
            check(lo <= val <= hi, "Redondeo dirigido")
            check(hi-lo <= F(1,10**digits), "Anchura de redondeo")
    for value in (0, -1, True, 1.5):
        expect_rejection(producer.gamma_interval, value)
        expect_rejection(producer.gamma_interval, 9, value)
    expect_rejection(producer.log_ratio_interval, 0)
    expect_rejection(producer.log_ratio_interval, -1)
    expect_rejection(producer.zeta_positive_integer_interval, 1)
    expect_rejection(producer.zeta_positive_integer_interval, 1.5)

    # No hay importaciones de evaluadores de constantes en el productor.
    tree = ast.parse((HERE/"partes_finitas_exactas.py").read_text())
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(a.name.split('.')[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append((node.module or '').split('.')[0])
    check(not set(imported) & {"mpmath", "numpy", "scipy", "sympy", "requests"},
          "Contaminación del productor por evaluador externo")

    import mpmath as mp
    # Algunas cotas racionales del logaritmo son mucho más estrechas que 1e-110.
    # Se aumenta la precisión del testigo, no se ensancha el intervalo productor.
    mp.mp.dps = 400

    def real(frac):
        return mp.mpf(frac.numerator)/frac.denominator

    for n,p,(lo,hi) in gamma_runs:
        check(real(lo) < mp.euler < real(hi), "Parte finita fuera del intervalo")
    for s,n,p,(lo,hi) in zeta_runs:
        check(real(lo) < mp.zeta(s) < real(hi), "Zeta fuera del intervalo")
    for x,(lo,hi) in logs:
        target = mp.log(real(x))
        if x == 1:
            check(lo == hi == 0, "log(1)")
        else:
            check(real(lo) <= target <= real(hi), "Logaritmo fuera del intervalo")

    # Controles negativos: una cota cero y retirar un término indispensable.
    glo,ghi = producer.gamma_interval()
    wrong = (glo+ghi)/2+F(1,162)
    check(abs(real(wrong)-mp.euler) > real(ghi-glo), "No detecta retirar frontera 1/(2N)")
    check(producer.regularized_minus_one()+F(1,12) != F(-1,12), "No detecta retirar Bernoulli")
    check(producer.bernoulli(2)[2] != -F(1,6), "No detecta invertir B2")
    check(ghi-glo < F(1,10**30), "Precisión racional gamma")
    alo,ahi = producer.zeta_positive_integer_interval()
    check(ahi-alo < F(1,10**32), "Precisión racional Apery")
    report = {"status": "PASS_FOCAL_PARTES_FINITAS", "checks": checks,
              "scope": "Exact interval formulas and independent numerical comparison, not RH or full HMT autonomy",
              "external_comparison_loaded_after_generation": True,
              "python_optimized": not __debug__,
              "producer_sha256": hashlib.sha256((HERE/"partes_finitas_exactas.py").read_bytes()).hexdigest(),
              "gamma": producer.publish((glo,ghi)), "Apery": producer.publish((alo,ahi))}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("gamma","Apery")},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
