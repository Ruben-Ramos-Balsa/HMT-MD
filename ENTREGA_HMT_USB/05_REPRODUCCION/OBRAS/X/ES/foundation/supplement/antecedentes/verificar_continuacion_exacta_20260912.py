"""Controles finitos exactos de la continuación; los límites se prueban en el texto.

Sólo biblioteca estándar. Conserva inmutable el verificador precedente.
Los ejemplos racionales comprueban identidades, no seleccionan datos HMT.
"""
from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = spec_from_file_location("balances", HERE / "verificar_balances_exactos.py")
b = module_from_spec(spec)
spec.loader.exec_module(b)
eye, tr, mm, plus, minus, scale = b.eye, b.tr, b.mm, b.plus, b.minus, b.scale


def determinant2(a):
    return a[0][0]*a[1][1] - a[0][1]*a[1][0]


def transpose_congruence(t, g):
    return mm(mm(tr(t), g), t)


def main():
    passed = []

    def check(name, condition):
        if not condition:
            raise RuntimeError(name)
        passed.append(name)

    for size in (3, 5):
        c = b.cyclic(size)
        _, _, _, t, eta = b.setup(c)
        identity = eye(size)
        pf = [[F(1, size) for _ in range(size)] for _ in range(size)]
        check(f"C_recuperado_{size}", minus(scale(9, t), scale(8, identity)) == c)
        check(f"terminal_fijo_{size}", mm(pf, c) == pf)
        power = identity
        accumulated = scale(0, identity)
        for n in range(9):
            record = mm(eta, power)
            check(f"dinamica_en_bloque_{size}_{n}",
                  mm(record, c) == minus(scale(9, mm(record, t)), scale(8, record)))
            accumulated = plus(accumulated, mm(tr(record), record))
            power = mm(t, power)
            remainder = mm(tr(power), power)
            check(f"reconstruccion_finita_{size}_{n+1}", plus(remainder, accumulated) == identity)
            partial = plus(pf, accumulated)
            check(f"error_reconstruccion_{size}_{n+1}",
                  minus(identity, partial) == mm(remainder, minus(identity, pf)))

    # Registro bilateral: polinomios de soporte finito, sin cierre cíclico.
    coefficients = [F(1)]
    previous_total = F(0)
    for n in range(65):
        an = sum((x*x for x in coefficients), F(0))
        closed = F(sum(comb(n, k)**2 * 64**(n-k) for k in range(n+1)), 81**n)
        check(f"bilateral_binomio_{n}", an == closed)
        difference = [-coefficients[0]]
        difference += [coefficients[k-1]-coefficients[k] for k in range(1, len(coefficients))]
        difference += [coefficients[-1]]
        bn = F(8, 81) * sum((x*x for x in difference), F(0))
        following = [F(0)] * (len(coefficients)+1)
        for k, x in enumerate(coefficients):
            following[k] += F(8, 9)*x
            following[k+1] += F(1, 9)*x
        an1 = sum((x*x for x in following), F(0))
        check(f"bilateral_balance_{n}", an-an1 == bn and bn > 0)
        previous_total += bn
        check(f"bilateral_acumulacion_{n}", previous_total + an1 == 1)
        coefficients = following

    omega = [[F(0), F(1)], [F(-1), F(0)]]
    examples = {
        "eliptico_Coxeter_A2": [[F(0), F(-1)], [F(1), F(-1)]],
        "parabolico_unipotente": [[F(1), F(1)], [F(0), F(1)]],
        "hiperbolico_Fav2": [[F(1), F(1)], [F(1), F(2)]],
    }
    for name, c in examples.items():
        t = scale(F(1, 9), plus(scale(8, eye(2)), c))
        delta = minus(c, eye(2))
        check(name+"_area_preservada", transpose_congruence(c, omega) == omega)
        memory_form = scale(F(8, 81), transpose_congruence(delta, omega))
        check(name+"_balance_area", plus(transpose_congruence(t, omega), memory_form) == omega)
        check(name+"_determinantes", determinant2(t) + F(8, 81)*determinant2(delta) == 1)
    check("parabolico_memoria_no_nula_area_cero",
          minus(examples["parabolico_unipotente"], eye(2)) != scale(0, eye(2))
          and determinant2(minus(examples["parabolico_unipotente"], eye(2))) == 0)
    check("hiperbolico_memoria_orientacion_negativa",
          determinant2(minus(examples["hiperbolico_Fav2"], eye(2))) < 0)

    # Forma variable: exp(eta/2)=a se representa con escalas racionales.
    def diag(x, y):
        return [[F(x), F(0)], [F(0), F(y)]]

    m0, m1 = diag(2, F(1, 2)), diag(3, F(1, 3))
    m0i, m1i = diag(F(1, 2), 2), diag(F(1, 3), 3)
    g0, g1 = mm(tr(m0i), m0i), mm(tr(m1i), m1i)
    rotation = [[F(3, 5), F(4, 5)], [F(-4, 5), F(3, 5)]]
    base = mm(m1, m0i)
    costura = mm(mm(m1, rotation), m0i)
    tv = scale(F(1, 9), plus(scale(8, base), costura))
    dv = minus(costura, base)
    check("forma_variable_balance_positivo",
          plus(transpose_congruence(tv, g1), scale(F(8, 81), transpose_congruence(dv, g1))) == g0)
    check("forma_variable_balance_simplectico",
          plus(transpose_congruence(tv, omega), scale(F(8, 81), transpose_congruence(dv, omega))) == omega)
    wrong_tv = scale(F(1, 9), plus(scale(8, eye(2)), costura))
    wrong_d = minus(costura, eye(2))
    check("omitir_transporte_forma_detectado",
          plus(transpose_congruence(wrong_tv, g1), scale(F(8, 81), transpose_congruence(wrong_d, g1))) != g0)

    print(json.dumps({"status": "PASS_CONTINUACION_EXACTA_20260912", "checks": len(passed),
                      "scope": "Identidades racionales finitas; tasas y reconstruccion ilimitada tienen pruebas escritas.",
                      "names": passed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
