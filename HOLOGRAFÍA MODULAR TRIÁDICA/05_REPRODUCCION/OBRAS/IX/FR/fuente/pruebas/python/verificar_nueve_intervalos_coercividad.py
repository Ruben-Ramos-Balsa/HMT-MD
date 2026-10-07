#!/usr/bin/env python3
"""Cotas intervalares de coercividad sobre nueve intervalos de soporte.

Dominio: f=sum(f_j), f_j en C_c^infty(I_j^o), con
I_j=[j*L-epsilon/2,j*L+epsilon/2], L=log(2), epsilon=1/1000, j=0,...,8.
El dominio es infinito-dimensional. No es C_c^infty de toda la envolvente
convexa: los ocho huecos entre intervalos permanecen fuera del soporte.

Dependencias operativas: producto de las hojas A9# -> irreducibles nativos ->
potencias nativas; publicación interna autenticada de pi; gamma de la parte
finita racional sobre el sucesor nativo; evaluación intervalar posterior.
No se introducen tablas de primos ni constantes de biblioteca como entradas.

Prueba analítica cuyas constantes se certifican aquí:
1. La forma COMPLETA es invariante por traslación (no cada puerto polar por
   separado). Centrar cada intervalo permite usar
     W(f_j,f_j) >= delta*||f_j||_2^2,
     delta=2*M_Gamma(epsilon)+c_Gamma-beta_epsilon,
     beta_epsilon=2*sinh(epsilon/2)-epsilon.
   Para a>=epsilon los soportes son disjuntos y el canal gamma aporta
   2*M_Gamma(epsilon)||f_j||^2. Los relojes primos no cruzan una sola celda,
   pues epsilon<log(2). El término polar es |b_+|^2-|b_-|^2 >= -beta*||f_j||^2.

2. Para i!=j y d=|i-j|, el cruce gamma tiene kernel -mu(|x-y|), donde
   mu(a)=exp(-a/2)/(1-exp(-2*a)) es decreciente. Así su norma está acotada por
   epsilon*mu(d*L-epsilon), usando ||f_j||_1<=sqrt(epsilon)||f_j||_2.
   No aparece un factor 2 adicional en gamma: las correlaciones orientadas
   tienen soportes de signo opuesto y reúnen un único kernel sobre I_i x I_j.
   El polar tiene kernel 2*cosh((x-y)/2), con cota
   2*epsilon*cosh((d*L+epsilon)/2). El término c_Gamma no cruza soportes disjuntos.

3. El censo nativo comprueba que |k*log(p)-d*L|<epsilon solamente permite
   p=2,k=d. También se certifica prospectivamente
     2^d-1 < 2^d*exp(-epsilon) < 2^d*exp(epsilon) < 2^d+1.
   Por ello el único peso primo es w_d=L/sqrt(2^d). Resulta
     |W(f_i,f_j)| <= rho_d ||f_i|| ||f_j||,
     rho_d=w_d+epsilon*mu(d*L-epsilon)
                 +2*epsilon*cosh((d*L+epsilon)/2).

4. Poniendo v_j=||f_j||, 2*v_i*v_j<=v_i^2+v_j^2 da
     W(f,f) >= sum_i (delta-sum_{j!=i}rho_|i-j|)*||f_i||^2.
   El script certifica que cada coeficiente supera 1. Como los soportes son
   disjuntos, W(f,f)>=||f||_2^2 en el dominio declarado, para todos los
   coeficientes complejos y todas las funciones de ese dominio, no por muestreo
   de funciones. Cualquier refinamiento interno que mantenga el mismo soporte
   y recomposición de f satisface la misma cota.

M_Gamma(h)=atanh(t)+atan(t), t=exp(-h/2). Se evalúa atan(t) mediante
pi/4-atan((1-t)/(1+t)); esta última arctangente usa 8 términos alternados con
cota racional de la cola. La pi empleada es la publicación interna copiada.

Alcance: certificado intervalar de los coeficientes de la prueba anterior.
No prueba positividad sobre todos los soportes, RH ni la selección canónica
TPK de estos nueve intervalos. No modifica otros programas ni manuscritos.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

import partes_finitas_exactas as partes
import a9_native as native
import verificar_gram_nueve_ventanas as shared
import mpmath
from mpmath import iv


def run():
    iv.dps = 45
    checks = shared.Checks()
    irreducibles, native_rows = shared.native_prime_powers(checks)
    polar_identity = shared.check_polar_identity(checks)
    pi, pi_provenance = shared.published_pi(checks)
    gamma_bounds = partes.gamma_interval(81, 8, 120)
    checks.require(gamma_bounds[0] < gamma_bounds[1], "unordered exact gamma enclosure")
    gamma = shared.enclose_rationals(*gamma_bounds)
    log2_bounds = partes.log_ratio_interval(Fraction(2), 120)
    L = shared.enclose_rationals(*log2_bounds)
    epsilon = shared.rational_iv(Fraction(1, 1000))
    c_gamma = -gamma - pi / 2 - 3 * L - iv.log(pi)
    checks.require(epsilon.b < L.a, "the support intervals are not disjoint")
    checks.require((8 * L + epsilon).b < iv.log(shared.LIMIT).a,
                   "native prime-power census does not cover all possible crosses")

    # The only possible integer in each prime-power window is obtained first
    # by native multiplication, and then compared with interval bounds.
    powers_two = []
    power = 1
    for _ in range(8):
        power = native.native_product(power, 2)
        powers_two.append(power)
    rows_with_lengths = [(p, k, value, k * iv.log(p))
                         for p, k, value in native_rows]
    census_windows = []
    for d, power in enumerate(powers_two, 1):
        lower_real = power * iv.exp(-epsilon)
        upper_real = power * iv.exp(epsilon)
        lower_margin = lower_real - (power - 1)
        upper_margin = (power + 1) - upper_real
        checks.require(lower_margin.a > 0, "lower integer-window inclusion failed")
        checks.require(upper_margin.a > 0, "upper integer-window inclusion failed")
        inside = []
        for p, k, value, ell in rows_with_lengths:
            distance = abs(ell - d * L)
            certainly_inside = distance.b < epsilon.a
            certainly_outside = distance.a >= epsilon.b
            checks.require(certainly_inside or certainly_outside,
                           "unresolved boundary in a native prime-power window")
            if certainly_inside:
                inside.append((p, k, value))
        checks.require(inside == [(2, d, power)],
                       "more or fewer than the announced prime-power crosses")
        census_windows.append({
            "distance_index": d,
            "native_integer": power,
            "inside": [{"p": p, "k": k, "value": value} for p, k, value in inside],
            "lower_integer_margin": shared.publish(lower_margin),
            "upper_integer_margin": shared.publish(upper_margin),
        })

    # Shifted arctangent: a very small positive argument makes eight terms
    # sufficient, instead of applying a slow alternating series at t near 1.
    t = iv.exp(-epsilon / 2)
    z = (1 - t) / (1 + t)
    checks.require(z.a > 0 and z.b < 1, "shifted arctangent argument outside (0,1)")
    atan_terms = 8
    zero = iv.mpf(0)
    atan_partial = sum(((-1 if n % 2 else 1) * z ** (2 * n + 1) / (2 * n + 1)
                        for n in range(atan_terms)), zero)
    atan_next = z ** (2 * atan_terms + 1) / (2 * atan_terms + 1)
    atan_z = atan_partial + iv.mpf([0, atan_next.b])
    atan_t = pi / 4 - atan_z
    atanh_t = iv.log((1 + t) / (1 - t)) / 2
    M_gamma = atanh_t + atan_t
    beta = iv.exp(epsilon / 2) - iv.exp(-epsilon / 2) - epsilon
    delta = 2 * M_gamma + c_gamma - beta
    checks.require(delta.a > 0, "diagonal coercivity coefficient is not positive")

    rho = []
    cross_components = []
    for d, power in enumerate(powers_two, 1):
        lower_distance = d * L - epsilon
        checks.require(lower_distance.a > 0, "gamma cross touches the singular diagonal")
        weight = L / iv.sqrt(power)
        mu = iv.exp(-lower_distance / 2) / (1 - iv.exp(-2 * lower_distance))
        gamma_cross = epsilon * mu
        far = d * L + epsilon
        polar_cross = epsilon * (iv.exp(far / 2) + iv.exp(-far / 2))
        bound = weight + gamma_cross + polar_cross
        checks.require(bound.a > 0, "nonpositive cross bound")
        rho.append(bound)
        cross_components.append({
            "distance_index": d,
            "prime": shared.publish(weight),
            "gamma": shared.publish(gamma_cross),
            "polar": shared.publish(polar_cross),
            "rho": shared.publish(bound),
        })

    row_sums = []
    margins = []
    for i in range(9):
        total = sum((rho[abs(i - j) - 1] for j in range(9) if j != i), zero)
        margin = delta - total
        checks.require(margin.a > 1, "the declared coercivity constant 1 was not certified")
        row_sums.append(total)
        margins.append(margin)

    # This minimum is taken over exact rational LOWER endpoints. No central
    # floating approximation is used to choose or publish the lower bound.
    certified_minimum = min(shared.exact_endpoint(x) for x in margins)
    checks.require(certified_minimum > 1, "exact endpoint does not establish the bound")
    files = [Path(__file__).resolve(), HERE / "verificar_gram_nueve_ventanas.py",
             HERE / "a9_native.py", HERE / "partes_finitas_exactas.py",
             ROOT / "antecedentes/nonadica/pi_1000_decimales.txt",
             ROOT / "antecedentes/nonadica/certificado_generacion_estructural.json",
             ROOT / "antecedentes/nonadica/SHA256SUMS"]
    return {
        "status": "PASS",
        "certificate": "NINE_INTERVALS_COMPLETE_FORM_COERCIVITY",
        "optimization_level": sys.flags.optimize,
        "checks": checks.count,
        "scope": "Interval certification of the explicit analytic coercivity criterion on all smooth compactly supported functions in the declared nine-interval union",
        "dimension_of_function_domain": "infinite",
        "not_certified": ["positivity on the convex hull including its gaps",
                          "positivity on every support", "Riemann hypothesis",
                          "canonical TPK selection of these nine centres"],
        "causal_order": ["APP two-sheet native product", "native irreducibles and native prime powers",
                         "internal pi publication and native rational finite-part gamma evaluation",
                         "downstream interval analytic evaluation", "coercivity coefficients"],
        "domain": {"epsilon": "1/1000", "centres": "j*log(2), j=0,...,8",
                   "functions": "f=sum(f_j), f_j in C_c^infty((j*L-epsilon/2,j*L+epsilon/2))",
                   "internal_refinements": "covered when support and recomposition remain inside the same nine-interval union",
                   "support_gaps_preserved": True},
        "arithmetic": {"interval_engine": "mpmath.iv", "version": mpmath.__version__,
                       "decimal_precision": iv.dps, "float_inputs_used": False,
                       "library_pi_or_euler_used": False},
        "native_census": {"limit": shared.LIMIT, "irreducibles": list(irreducibles),
                          "prime_power_count": len(native_rows),
                          "prime_powers": [{"p": p, "k": k, "value": value}
                                           for p, k, value in native_rows],
                          "windows": census_windows},
        "pi_publication": pi_provenance,
        "Euler_Mascheroni": {"producer": "partes_finitas_exactas.gamma_interval(81,8,120)",
                             "exact_lower": str(gamma_bounds[0]), "exact_upper": str(gamma_bounds[1])},
        "log2": {"producer": "partes_finitas_exactas.log_ratio_interval(2,120)",
                 "exact_lower": str(log2_bounds[0]), "exact_upper": str(log2_bounds[1])},
        "polar_identity": {"exact_Laurent_equality": polar_identity,
                           "meaning": "the complete polar kernel is 2*cosh((x-y)/2), not a function of x+y"},
        "gamma_tail_evaluation": {"formula": "M_Gamma(epsilon)=atanh(t)+pi/4-atan((1-t)/(1+t)), t=exp(-epsilon/2)",
                                  "atan_alternating_terms": atan_terms,
                                  "atan_small_argument": shared.publish(z),
                                  "atan_next_term_bound": shared.publish(atan_next),
                                  "M_Gamma": shared.publish(M_gamma)},
        "diagonal": {"c_Gamma": shared.publish(c_gamma), "beta_epsilon": shared.publish(beta),
                     "delta_epsilon": shared.publish(delta)},
        "cross_bounds": cross_components,
        "row_cross_sums": [shared.publish(x) for x in row_sums],
        "coercivity_margins": [shared.publish(x) for x in margins],
        "minimum_lower_endpoint_exact": str(certified_minimum),
        "minimum_lower_endpoint_decimal_directed": partes.decimal_bound(certified_minimum, 35),
        "certified_rational_coercivity_constant": "1",
        "conclusion": "W(f,f)>=||f||_2^2 for every f in the declared domain, by the analytic norm bounds stated in this source",
        "provenance": "Extension of the recovered local gamma-tail estimate to a declared disconnected support; new interval coefficient certificate; no claim of a new underlying HMT architecture",
        "files": [{"path": str(path.relative_to(ROOT)),
                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in files],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        report = run()
        exit_code = 0
    except Exception as exc:
        report = {"status": "FAIL", "certificate": "NINE_INTERVALS_COMPLETE_FORM_COERCIVITY",
                  "optimization_level": sys.flags.optimize,
                  "scope": "only the declared analytic coefficient criterion",
                  "error": type(exc).__name__ + ": " + str(exc)}
        exit_code = 1
    if args.receipt is not None:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {key: report[key] for key in ("status", "certificate", "optimization_level")}
    if exit_code == 0:
        summary.update({"checks": report["checks"],
                        "native_prime_power_rows": report["native_census"]["prime_power_count"],
                        "certified_coercivity_constant": "1",
                        "minimum_lower_endpoint": report["minimum_lower_endpoint_decimal_directed"],
                        "scope": report["scope"]})
    else:
        summary["error"] = report["error"]
    if args.receipt is not None:
        summary["receipt"] = str(args.receipt.resolve())
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
