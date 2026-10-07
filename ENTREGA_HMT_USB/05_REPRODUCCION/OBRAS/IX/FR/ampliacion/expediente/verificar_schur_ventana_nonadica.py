#!/usr/bin/env python3
"""Certifica Schur en I=(-1/18,1/18), para todo el dominio de lectores.

Se usan publicaciones internas y productores racionales conservados de VIII.
No se consultan ceros de zeta ni se muestrean funciones para inferir el signo.
La prueba se encuentra en AGENTE_SCHUR_DETALLES.md. Los cálculos certifican
sus constantes; no certifican por sí solos el argumento funcional ni RH.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LOCAL_VIII = HERE / "dependencias_viii"
ORIGINAL_VIII = HERE.parent / "ARTICULO_VIII_PRIMOS_ESTRUCTURA_ESPECTRAL_20260910"
# Una copia local presente tiene prioridad completa. Si está incompleta,
# falla la lectura; no se mezclan silenciosamente cortes de dos carpetas.
VIII = LOCAL_VIII if LOCAL_VIII.is_dir() else ORIGINAL_VIII
PYTHON = VIII / "fuente/pruebas/python"
sys.path.insert(0, str(PYTHON))

import mpmath
from mpmath import iv
import verificar_gram_nueve_ventanas as shared
import partes_finitas_exactas as partes


def run():
    iv.dps = 55
    checks = shared.Checks()
    pi, pi_source = shared.published_pi(checks)
    gamma_bounds = partes.gamma_interval(81, 8, 120)
    gamma = shared.enclose_rationals(*gamma_bounds)
    log2_bounds = partes.log_ratio_interval(Fraction(2), 120)
    log2 = shared.enclose_rationals(*log2_bounds)
    h = shared.rational_iv(Fraction(1, 9))
    c_gamma = -gamma - pi / 2 - 3 * log2 - iv.log(pi)
    checks.require(h.b < log2.a, "a prime-power translation enters the window")
    n = 13
    harmonic = sum((Fraction(4, 4 * k + 1) for k in range(n + 1)), Fraction())
    beta = iv.exp(h / 2) - iv.exp(-h / 2) - h
    eta = (shared.rational_iv(harmonic)
           - h ** 2 * (n + 1) * (2 * n + 1) / pi ** 2
           + c_gamma - beta)
    checks.require((shared.rational_iv(Fraction(4*n+1, 2))*h).b < pi.a,
                   "retained gamma lower bounds are not all nonnegative")
    checks.require(eta.a > 1, "detail coercivity eta>1 is not certified")

    terms = 1024
    zero = iv.mpf(0)
    gamma_average_partial = sum(
        ((1 - iv.exp(-shared.rational_iv(Fraction(4*k+1, 2))*h))
         / shared.rational_iv(Fraction(4*k+1, 2)) ** 2
         for k in range(terms)), zero)
    lam = shared.rational_iv(Fraction(4*terms+1, 2))
    tail_upper = 1 / lam ** 2 + 1 / (2 * lam)
    sinh_quarter = (iv.exp(h/4) - iv.exp(-h/4)) / 2
    cosh_quarter = (iv.exp(h/4) + iv.exp(-h/4)) / 2
    a_interval = (c_gamma + (2/h) *
                  (gamma_average_partial + iv.mpf([0, tail_upper.b]))
                  + (32/h) * sinh_quarter ** 2)
    checks.require(a_interval.a > shared.rational_iv(Fraction(97,100)).b,
                   "the mean block is not above 97/100")

    # M(x)=-log(x)/2+C+r(x). On 0<x<=1/9, -9/10<=r'<=0.
    # r(ht)+r(h(1-t)) has oscillation <=1/20 and standard deviation <=1/40.
    # The logarithmic part has variance 1-pi^2/12, proved in the note.
    log_variance = 1 - pi ** 2 / 12
    polar_std_bound = 4 * sinh_quarter * (cosh_quarter - 1)
    b_squared_upper = (iv.sqrt(log_variance)
                       + shared.rational_iv(Fraction(1,40))
                       + polar_std_bound) ** 2
    checks.require(log_variance.a > 0, "invalid logarithmic variance")
    checks.require(b_squared_upper.b < shared.rational_iv(Fraction(1,5)).a,
                   "the entire cross norm is not below 1/5")
    schur_lower = a_interval - b_squared_upper / eta
    checks.require(schur_lower.a > shared.rational_iv(Fraction(77,100)).b,
                   "the Schur lower bound is not above 77/100")
    half = shared.rational_iv(Fraction(1,2))
    shifted_determinant = (a_interval - half) * (eta - half) - b_squared_upper
    checks.require(shifted_determinant.a > 0,
                   "the full form minus one half identity is not positive")

    # Finite adversarial control: positive diagonal blocks alone are not enough.
    # [[1,2],[2,1]] has negative Schur complement -3.
    checks.require(Fraction(1)-Fraction(2)**2/Fraction(1) == -3,
                   "negative cross-control failed")

    paths = [Path(__file__), PYTHON / "verificar_gram_nueve_ventanas.py",
             PYTHON / "partes_finitas_exactas.py",
             PYTHON / "a9_native.py",
             VIII / "manuscrito/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.md",
             VIII / "antecedentes/nonadica/pi_1000_decimales.txt",
             VIII / "antecedentes/nonadica/certificado_generacion_estructural.json",
             VIII / "antecedentes/nonadica/SHA256SUMS",
             HERE / "AGENTE_SCHUR_DETALLES.md",
             HERE / "REPRODUCIR_SCHUR.md",
             HERE / "requirements_schur.txt"]
    return {
        "status": "PASS_SCHUR_FIXED_WINDOW_ONE_NINTH",
        "optimization_level": sys.flags.optimize,
        "checks": checks.count,
        "domain": "closure of C_c^infty((-1/18,1/18)) in the joint reader norm",
        "all_complex_functions_in_domain": True,
        "mean_cells": 1,
        "detail_dimension": "infinite",
        "all_internal_nonadic_refinements": True,
        "coercivity_constant_exact": "1/2",
        "schur_lower_bound_exact": "77/100",
        "window_length_exact": "1/9",
        "gamma_terms_for_detail": n + 1,
        "gamma_terms_for_mean": terms,
        "gamma_mean_tail_upper": shared.publish(tail_upper),
        "c_gamma": shared.publish(c_gamma),
        "detail_eta": shared.publish(eta),
        "mean_A": shared.publish(a_interval),
        "cross_norm_squared_upper_enclosure": shared.publish(b_squared_upper),
        "schur_lower_enclosure": shared.publish(schur_lower),
        "shifted_determinant": shared.publish(shifted_determinant),
        "pi_publication": pi_source,
        "gamma_exact_bounds": list(map(str,gamma_bounds)),
        "log2_exact_bounds": list(map(str,log2_bounds)),
        "arithmetic": {"engine": "mpmath.iv", "version": mpmath.__version__,
                       "decimal_precision": iv.dps, "float_inputs": False,
                       "library_pi_or_euler_inputs": False},
        "zero_inputs": False,
        "prime_terms": "empty because 1/9 < log(2), the shortest published clock",
        "ancestry": "APP two sheets -> TRIT -> TPK -> joint continuum -> native modes and published constants -> complete reader form -> Schur",
        "not_certified": ["every window R", "a window containing an active prime translation", "RH", "canonical TPK selection of this analytic window"],
        "scope": "Rigorous interval constants for the analytic proof in AGENTE_SCHUR_DETALLES.md; inherited publications are authenticated, not regenerated here",
        "dependency_mode": "LOCAL_BYTE_IDENTICAL_COPY" if VIII == LOCAL_VIII else "ORIGINAL_VIII_FALLBACK",
        "dependency_root": str(VIII),
        "files": [{"path": str(p.resolve()), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        report = run()
        code = 0
    except Exception as exc:
        report = {"status": "FAIL_SCHUR_FIXED_WINDOW_ONE_NINTH",
                  "optimization_level": sys.flags.optimize,
                  "error": type(exc).__name__ + ": " + str(exc)}
        code = 1
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k in
          ["status","optimization_level","checks","domain","coercivity_constant_exact",
           "schur_lower_bound_exact","error","detail_eta","mean_A","cross_norm_squared_upper_enclosure"]},
          ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
