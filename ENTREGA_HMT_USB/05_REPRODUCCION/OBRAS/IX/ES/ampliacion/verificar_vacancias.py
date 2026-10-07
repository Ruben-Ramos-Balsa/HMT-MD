#!/usr/bin/env python3
"""Certificado racional del calendario de vacancias APP--TRIT--TPK.

Se verifica la publicación de capacidad que compara 3**6=729 con
10**3=1000. No se evalúan pi, phi, e o alpha ni se consultan cifras objetivo.
Los logaritmos se encierran mediante series racionales y cotas de resto.
Los controles finitos complementan las pruebas universales del manuscrito.
Ejemplo: python3 -I -S ampliacion/verificar_vacancias.py --receipt recibo.json
"""

from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


def log_bounds(x, n):
    """S_n < log(x) < S_n+R_n, x>1, indices de suma 0,...,n."""
    z = (x - 1) / (x + 1)
    if not (F(0) < z < F(1)):
        raise ValueError("La carta requiere x>1.")
    partial = 2 * sum((z ** (2*k + 1) / (2*k + 1)
                       for k in range(n + 1)), F(0))
    rest = 2 * z ** (2*n + 3) / ((2*n + 3) * (1 - z*z))
    return partial, partial + rest


def delta_bounds(n):
    a0, a1 = log_bounds(F(10, 9), n)
    b0, b1 = log_bounds(F(2), n)
    c0, c1 = log_bounds(F(5, 4), n)
    # log(10) = 3 log(2) + log(5/4).
    return a0 / (3*b1 + c1), a1 / (3*b0 + c0)


def floor_interval(lo, hi):
    a, b = lo.numerator // lo.denominator, hi.numerator // hi.denominator
    if a != b:
        raise ArithmeticError("Intervalo insuficiente para decidir una parte entera.")
    return a


def pair(interval):
    return [str(interval[0]), str(interval[1])]


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=int, default=512)
    parser.add_argument("--short-events", type=int, default=64)
    parser.add_argument("--series-order", type=int, default=16)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if args.events < 30 or args.short_events < 10 or args.series_order < 4:
        parser.error("Se requieren >=30 eventos, >=10 cortos y orden >=4.")
    counts = Counter()

    def check(name, condition):
        if not condition:
            raise RuntimeError("FAIL_VACANCIAS_RACIONALES: " + name)
        counts[name] += 1

    elementary = delta_bounds(4)
    check("cota_racional_impresa", F(7, 153) < elementary[0]
          < elementary[1] < F(6, 131))
    lo, hi = delta_bounds(args.series_order)
    lam = (1/hi, 1/lo)
    beta = (22-lam[1], 22-lam[0])
    mu = (1/beta[1], 1/beta[0])
    check("intervalo_primario", F(21) < lam[0] < lam[1] < F(22))
    check("pendiente_inducida", F(1, 7) < beta[0] < beta[1] < F(1, 6))
    check("intervalo_secundario", F(6) < mu[0] < mu[1] < F(7))

    def fd(t):
        return floor_interval(t*lo, t*hi)

    def fb(t):
        return floor_interval(t*beta[0], t*beta[1])

    def cap(t):
        return floor_interval((t+1)*(1-hi), (t+1)*(1-lo))

    def z(t):
        return fd(t+1) - fd(t)

    def mph(r):
        if not (1 <= r <= 9):
            raise ValueError("Fase fuera de D9.")
        return (1, -1, 0)[(r-1) % 3]

    p = [None] + [floor_interval(j*lam[0], j*lam[1])
                   for j in range(1, args.events+2)]
    q = [None] + [floor_interval(m*mu[0], m*mu[1])
                   for m in range(1, args.short_events+2)]
    if q[-1] >= args.events:
        parser.error("Aumente --events para cubrir todos los eventos secundarios.")
    tmax = p[args.events]
    vac_positions = []
    previous = cap(0)
    cumulative = 0
    for t in range(1, tmax+1):
        value, event = cap(t), z(t)
        check("vacancia_binaria", event in (0, 1))
        check("complementariedad", value-previous == 1-event)
        cumulative += event
        check("telescopia", value-cap(0)+cumulative == t)
        check("fase_capacidad", (value-previous) % 9 == (1-event) % 9)
        if event:
            vac_positions.append(t)
        previous = value
    check("posiciones_eventos", vac_positions == p[1:args.events+1])

    h, short, v, regime = {}, {}, {}, {}
    for j in range(1, args.events+1):
        h[j] = p[j+1]-p[j]
        short[j] = 22-h[j]
        v[j] = cap(p[j])
        regime[j] = mph(1+v[j] % 9)
        check("huecos_21_22", h[j] in (21, 22))
        check("eventos_cortos", short[j] == fb(j+1)-fb(j))
        check("capacidad_evento", v[j] == p[j]-j)
        vnext = cap(p[j+1])
        check("incremento_evento", vnext-v[j] == 21-short[j])
        check("residuo_mod3", vnext % 3 == (v[j]-short[j]) % 3)
        check("regimen_largo", short[j] != 0 or mph(1+vnext % 9) == regime[j])
        check("regimen_corto", short[j] != 1 or mph(1+vnext % 9) != regime[j])

    short_positions = [j for j in range(1, args.events+1) if short[j]]
    check("posiciones_cortos", short_positions[:args.short_events+1] == q[1:])
    secondary = [q[m+1]-q[m] for m in range(1, args.short_events+1)]
    for gap in secondary:
        check("huecos_6_7", gap in (6, 7))
    for m in range(1, args.short_events+1):
        gap = q[m+1]-q[m]
        check("retorno_bloques_131_153", p[q[m+1]]-p[q[m]] == 22*gap-1)
        check("retorno_capacidad_125_146", v[q[m+1]]-v[q[m]] == 21*gap-1)
    check("no_alternancia_estricta", any(a == b for a, b in zip(secondary, secondary[1:])))

    runs = []
    start = 1
    for j in range(2, args.events+1):
        if v[j] % 3 != v[j-1] % 3:
            runs.append({"desde": start, "hasta": j-1, "longitud": j-start,
                         "clase_mod3": v[start] % 3, "trit": regime[start]})
            start = j
    check("mesetas_iniciales", [r["longitud"] for r in runs[:3]] == [6, 7, 7])
    check("clases_iniciales", [r["clase_mod3"] for r in runs[:3]] == [2, 1, 0])
    for run in runs[1:]:
        check("meseta_completa", run["longitud"] in (6, 7))

    receipt = {
        "status": "PASS_VACANCIAS_RACIONALES_21_22_6_7",
        "scope": "Control finito exacto; las pruebas universales residen en vacancias_21_22_6_7.tex",
        "provenance": "CERTIFICADO_NUEVO de resultados recuperados del Articulo I y monografia775",
        "arithmetic": "fractions.Fraction; series positivas con resto acotado; ninguna aproximacion float",
        "input": {"ternary_block": "3^6=729", "decimal_block": "10^3=1000",
                  "logarithmic_reader": "delta=log(10/9)/log(10)", "target_constants": []},
        "series_order": args.series_order,
        "bounds": {"delta_order4": pair(elementary), "delta": pair((lo, hi)),
                   "lambda": pair(lam), "beta": pair(beta), "mu": pair(mu)},
        "events": args.events, "last_block": tmax,
        "short_events": args.short_events,
        "checks": dict(sorted(counts.items())), "total_checks": sum(counts.values()),
        "primary_sample": [{"j": j, "p_j": p[j], "h_j": h[j], "s_j": short[j],
                            "v_j": v[j], "v_mod3": v[j] % 3, "trit": regime[j]}
                           for j in range(1, 21)],
        "short_sample": [{"m": m, "q_m": q[m], "next_gap": q[m+1]-q[m]}
                         for m in range(1, 11)],
        "plateaus_sample": runs[:8],
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    data = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.write_text(data, encoding="utf-8")
    print(data, end="")


if __name__ == "__main__":
    main()
