#!/usr/bin/env python3
"""Control intervalar de la forma completa sobre nueve ventanas de prueba.

Orden de evaluación:
  hojas APP de A9# -> producto nativo -> irreducibles -> potencias nativas;
  sucesor nativo -> parte finita racional de Euler--Mascheroni;
  publicación nonádica autenticada de pi -> intervalo racional publicado;
  evaluación posterior exp/log -> Gram gamma--primo--escalar--polar.

No es un productor alternativo de constantes. Consume una publicación interna
de pi, sin regenerar aquí su cadena APP--TRIT--TPK. Los nueve centros j*log(2)
son pruebas analíticas del reloj irreducible 2; no se identifican por su número
con nueve hijos canónicos del estado TPK. No certifica positividad global de
Weil, RH, un codificador universal ni la autonomía científica del artículo.

Para b[e,t]=e**(-1/2)*1_[t-e/2,t+e/2], tau_e(x)=(1-|x|/e)_+ y
F(x)=sum(exp(-(2*n+1/2)*x)/(2*n+1/2)**2), la entrada completa es

 K_e(d) = 2*a_e**2*cosh(d/2) + c_Gamma*tau_e(d)
          +(2*F(|d|)-F(|d-e|)-F(|d+e|))/e
          -sum(w*(tau_e(d-ell)+tau_e(d+ell))),

donde a_e=4*sinh(e/4)/sqrt(e), ell=k*log(p), w=log(p)/sqrt(p**k).
La última suma incluye todos los p**k < exp(|d|+e).

Prueba del término gamma: la integración de la correlación triangular en sus
tramos da, para lambda>0,

 integral_0^inf exp(-lambda*a)*(2*tau(d)-tau(d-a)-tau(d+a)) da
 = (2*exp(-lambda*|d|)-exp(-lambda*|d-e|)
    -exp(-lambda*|d+e|))/(e*lambda**2).

La suma es absolutamente convergente. Para N términos se añade la cola
 0 <= F(x)-F_N(x) <= exp(-lambda_N*x)
                       *(lambda_N**(-2)+(2*lambda_N)**(-1)),
obtenida por sumatorio decreciente e integral. Se conservan errores de cola
y de redondeo de TODOS los términos; no se usa una estimación central sola.

Polarización: si X=exp(s/2), Y=exp(t/2), los dos funcionales son
a_e*(X+X**-1)/sqrt(2) y a_e*(X-X**-1)/sqrt(2). Su diferencia de Grams es
a_e**2*(X/Y+Y/X). Por tanto depende de s-t, aunque cada funcional por separado
depende del centro absoluto. La identidad se comprueba también exactamente
como igualdad de polinomios de Laurent.

Requiere mpmath (evaluación intervalar posterior). Sin assertions eliminables
por -O. Sólo escribe el recibo solicitado mediante --receipt.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

import a9_native
import partes_finitas_exactas as partes
import mpmath
from mpmath import iv


PI_SHA256 = "e898fea26734a6d3af5396b9f4c60ae5dcc88fc40944d835911a9ee8a672ea1b"
CERT_SHA256 = "c0888059e747bd200996a0945c95bb368f0d4d8cc46df0da985377077c1db2ef"
MANIFEST_SHA256 = "a6f7fe6d66140a0e88518c2b62c69e1ac23b26a165e6dc494caf1dd174ec8996"
PRECISION = 45
TERMS = 1024
LIMIT = 259


class VerificationFailure(RuntimeError):
    pass


class Checks:
    def __init__(self):
        self.count = 0

    def require(self, condition, message):
        self.count += 1
        if not condition:
            raise VerificationFailure(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational_iv(value):
    value = Fraction(value)
    return iv.mpf(value.numerator) / iv.mpf(value.denominator)


def enclose_rationals(lower, upper):
    return iv.mpf([rational_iv(lower).a, rational_iv(upper).b])


def exact_endpoint(value, upper=False):
    """Converts an mpmath binary endpoint to an exact fraction, without float."""
    sign, mantissa, exponent, _ = value._mpi_[1 if upper else 0]
    if not isinstance(exponent, int):
        raise VerificationFailure("non-finite interval endpoint")
    numerator = -mantissa if sign else mantissa
    if exponent >= 0:
        return Fraction(numerator * (1 << exponent))
    return Fraction(numerator, 1 << (-exponent))


def publish(interval):
    lower = exact_endpoint(interval)
    upper = exact_endpoint(interval, upper=True)
    return {
        "lower": partes.decimal_bound(lower, 35),
        "upper": partes.decimal_bound(upper, 35, upper=True),
        "lower_exact": str(lower),
        "upper_exact": str(upper),
    }


def published_pi(checks):
    folder = ROOT / "antecedentes" / "nonadica"
    pi_path = folder / "pi_1000_decimales.txt"
    cert_path = folder / "certificado_generacion_estructural.json"
    manifest_path = folder / "SHA256SUMS"
    for path, expected in ((pi_path, PI_SHA256), (cert_path, CERT_SHA256),
                           (manifest_path, MANIFEST_SHA256)):
        checks.require(path.is_file(), "missing copied antecedent: " + str(path))
        checks.require(sha256(path) == expected, "antecedent hash mismatch: " + str(path))
    certificate = json.loads(cert_path.read_text(encoding="utf-8"))
    entry = certificate["outputs"]["pi"]
    checks.require(entry["decimal_sha256"] == PI_SHA256,
                   "pi hash does not match its generating receipt")
    checks.require(entry["decimal_digits_after_point"] == 1000,
                   "unexpected precision of the nonadic publication")
    manifest = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        digest, name = line.split(None, 1)
        manifest[name.strip()] = digest
    checks.require(manifest["salidas/pi_1000_decimales.txt"] == PI_SHA256,
                   "pi does not match the preserved source manifest")
    checks.require(manifest["certificado_generacion_estructural.json"] == CERT_SHA256,
                   "source certificate does not match its manifest")
    text = pi_path.read_text(encoding="ascii").strip()
    checks.require(re.fullmatch(r"[0-9]+\.[0-9]{1000}", text) is not None,
                   "pi publication is not an exact 1000-digit decimal prefix")
    integer, tail = text.split(".")
    denominator = 10 ** len(tail)
    lower = Fraction(int(integer + tail), denominator)
    upper = lower + Fraction(1, denominator)
    checks.require(lower > 0, "nonpositive pi publication")
    # The generating certificate publishes a decimal CELL containing the
    # complete compatible cylinder, rather than an unbounded rounded value.
    return enclose_rationals(lower, upper), {
        "original_path": "/Users/ruben/Documents/New project/certificados/ley_nueve_puertas_2026-07-30/salidas/pi_1000_decimales.txt",
        "copied_path": str(pi_path.relative_to(ROOT)),
        "sha256": PI_SHA256,
        "source_certificate_sha256": CERT_SHA256,
        "source_manifest_sha256": MANIFEST_SHA256,
        "inherited_status": certificate["status"],
        "inherited_status_recomputed_by_this_script": False,
        "publication_role": "internal nonadic output used downstream in the completed form",
        "exact_lower": str(lower),
        "exact_upper": str(upper),
        "interval_convention": "closed enclosure of the published half-open decimal cell",
    }


def laurent_product(left, right):
    out = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            key = (a + c, b + d)
            out[key] = out.get(key, Fraction()) + x * y
    return {key: value for key, value in out.items() if value}


def check_polar_identity(checks):
    xp = {(1, 0): Fraction(1), (-1, 0): Fraction(1)}
    xm = {(1, 0): Fraction(1), (-1, 0): Fraction(-1)}
    yp = {(0, 1): Fraction(1), (0, -1): Fraction(1)}
    ym = {(0, 1): Fraction(1), (0, -1): Fraction(-1)}
    plus = laurent_product(xp, yp)
    minus = laurent_product(xm, ym)
    result = {key: (plus.get(key, Fraction()) - minus.get(key, Fraction())) / 2
              for key in set(plus) | set(minus)}
    result = {key: value for key, value in result.items() if value}
    checks.require(result == {(1, -1): Fraction(1), (-1, 1): Fraction(1)},
                   "polar Laurent identity is false")
    checks.require(all(a + b == 0 for a, b in result),
                   "polar Gram is not invariant under a common translation")
    return "((X+X^-1)(Y+Y^-1)-(X-X^-1)(Y-Y^-1))/2 = X/Y+Y/X"


def native_prime_powers(checks):
    irreducibles = a9_native.irreducibles_native(LIMIT)
    checks.require(len(irreducibles) == len(set(irreducibles)),
                   "duplicate native irreducibles")
    rows = []
    for p in irreducibles:
        k, power = 1, p
        while power <= LIMIT:
            rows.append((p, k, power))
            successor = a9_native.native_product(power, p)
            checks.require(successor > power, "native prime-power progression did not advance")
            k, power = k + 1, successor
    checks.require(len({power for _, _, power in rows}) == len(rows),
                   "duplicate native prime-power publication")
    return irreducibles, rows


def run():
    iv.dps = PRECISION
    checks = Checks()
    irreducibles, native_rows = native_prime_powers(checks)
    polar_identity = check_polar_identity(checks)
    pi, pi_provenance = published_pi(checks)
    gamma_bounds = partes.gamma_interval(81, 8, 120)
    checks.require(gamma_bounds[0] < gamma_bounds[1],
                   "unordered Euler--Mascheroni rational enclosure")
    gamma_euler = enclose_rationals(*gamma_bounds)
    log2_bounds = partes.log_ratio_interval(Fraction(2), 120)
    log2 = enclose_rationals(*log2_bounds)
    epsilon = rational_iv(Fraction(1, 100))
    zero = iv.mpf(0)
    c_gamma = -gamma_euler - pi / 2 - 3 * log2 - iv.log(pi)
    a = 2 * (iv.exp(epsilon / 4) - iv.exp(-epsilon / 4)) / iv.sqrt(epsilon)

    # Independent basal check, using the recovered tail formula, not a new
    # connector. atan(t) is enclosed by its alternating series; atanh(t)
    # is evaluated by the logarithmic identity, so no library constant is used.
    h = rational_iv(Fraction(1, 16))
    t = iv.exp(-h / 2)
    checks.require(t.a > 0 and t.b < 1, "basal alternating series outside (0,1)")
    atan_terms = 512
    atan_partial = sum(((-1 if k % 2 else 1) * t ** (2 * k + 1) / (2 * k + 1)
                        for k in range(atan_terms)), zero)
    atan_error = t ** (2 * atan_terms + 1) / (2 * atan_terms + 1)
    atan_interval = atan_partial + iv.mpf([0, atan_error.b])
    atanh_interval = iv.log((1 + t) / (1 - t)) / 2
    twice_tail = 2 * (atanh_interval + atan_interval)
    basal_rhs = -c_gamma + iv.exp(h / 2) - iv.exp(-h / 2) - h
    basal_margin = twice_tail - basal_rhs
    checks.require(basal_margin.a > 0, "the recovered basal contraction bound is not certified")
    checks.require((8 * log2 + epsilon).b < iv.log(LIMIT).a,
                   "the native prime-power census does not cover the support")
    checks.require(log2.a > epsilon.b, "test boxes are not disjoint")
    prime_rows = [(p, k, power, k * iv.log(p), iv.log(p) / iv.sqrt(power))
                  for p, k, power in native_rows]

    def positive_part(x):
        if x.b <= 0:
            return zero
        if x.a >= 0:
            return x
        return iv.mpf([0, x.b])

    def tent(x):
        return positive_part(1 - abs(x) / epsilon)

    def gamma_primitive(x):
        checks.require(x.a >= 0, "negative argument of gamma primitive")
        total = zero
        for n in range(TERMS):
            lam = iv.mpf(2 * n) + rational_iv(Fraction(1, 2))
            total += iv.exp(-lam * x) / (lam * lam)
        lam = iv.mpf(2 * TERMS) + rational_iv(Fraction(1, 2))
        upper = iv.exp(-lam * x) * (1 / (lam * lam) + 1 / (2 * lam))
        return total + iv.mpf([0, upper.b])

    def kernel(distance):
        gamma = (2 * gamma_primitive(abs(distance))
                 - gamma_primitive(abs(distance - epsilon))
                 - gamma_primitive(abs(distance + epsilon))) / epsilon
        prime = sum((weight * (tent(distance - ell) + tent(distance + ell))
                     for _, _, _, ell, weight in prime_rows), zero)
        polar = a * a * (iv.exp(distance / 2) + iv.exp(-distance / 2))
        return polar + c_gamma * tent(distance) + gamma - prime

    first_row = [kernel(j * log2) for j in range(9)]
    matrix = [[first_row[abs(i - j)] for j in range(9)] for i in range(9)]
    d = first_row[0]
    margins = []
    for i in range(9):
        margin = d - sum((abs(matrix[i][j]) for j in range(9) if j != i), zero)
        margins.append(margin)
        checks.require(margin.a > rational_iv(Fraction(8479, 10000)).b,
                       "Gershgorin does not certify the announced finite lower bound")

    # Independent evaluation of the two polar functionals before subtracting
    # their Grams; the exact Laurent proof above is the algebraic justification.
    sqrt2 = iv.sqrt(2)
    polar_functions = []
    for j in range(9):
        centre = j * log2
        forward, backward = iv.exp(centre / 2), iv.exp(-centre / 2)
        polar_functions.append((a * (forward + backward) / sqrt2,
                                a * (forward - backward) / sqrt2))
    for i in range(9):
        for j in range(9):
            plus_i, minus_i = polar_functions[i]
            plus_j, minus_j = polar_functions[j]
            direct = plus_i * plus_j - minus_i * minus_j
            distance = (i - j) * log2
            relative = a * a * (iv.exp(distance / 2) + iv.exp(-distance / 2))
            residual = direct - relative
            checks.require(residual.a <= 0 <= residual.b,
                           "polarization does not match the difference kernel")
            checks.require((residual.b - residual.a).b < rational_iv(Fraction(1, 10**35)).a,
                           "polarization interval is too wide")

    # These are consequences on the two stated two-dimensional spans only.
    separation_one_fifth = kernel(rational_iv(Fraction(1, 5)))
    two_box_eigenvalues = {
        "L=1/5": [d + separation_one_fifth, d - separation_one_fifth],
        "L=log(2)": [d + first_row[1], d - first_row[1]],
    }
    for values in two_box_eigenvalues.values():
        for value in values:
            checks.require(value.a > 0, "a two-box Gram is not certified positive")
    checks.require(first_row[1].b < first_row[8].a,
                   "the stated non-circulant witness was not separated")

    files = [Path(__file__).resolve(), HERE / "a9_native.py",
             HERE / "partes_finitas_exactas.py",
             ROOT / "antecedentes/nonadica/pi_1000_decimales.txt",
             ROOT / "antecedentes/nonadica/certificado_generacion_estructural.json",
             ROOT / "antecedentes/nonadica/SHA256SUMS"]
    return {
        "status": "PASS",
        "certificate": "FINITE_NINE_BOX_COMPLETE_GRAM_INTERVALS",
        "scope": "Complete gamma-prime-scalar-polar form restricted to nine normalized test boxes; all complex coefficients",
        "not_certified": ["global Weil positivity", "Riemann hypothesis",
                          "a universal TPK-to-Weil encoder", "canonical TPK selection of these nine centres"],
        "optimization_level": sys.flags.optimize,
        "checks": checks.count,
        "arithmetic": {"interval_engine": "mpmath.iv", "version": mpmath.__version__,
                       "decimal_precision": PRECISION, "gamma_series_terms": TERMS,
                       "library_pi_or_euler_used": False, "float_inputs_used": False},
        "causal_order": ["APP two-sheet A9# product", "native irreducibles and native prime powers",
                         "internal nonadic pi publication and rational finite-part gamma evaluation",
                         "downstream exponential/logarithmic evaluation", "finite complete Gram"],
        "test_domain": {"epsilon": "1/100", "centres": "j*log(2), j=0,...,8",
                        "dimension": 9, "orthonormal_in_L2": True,
                        "interpretation": "analytic test family of the irreducible clock 2; not an inferred canonical nonadic fibre"},
        "native_census": {"limit": LIMIT, "irreducibles": list(irreducibles),
                          "prime_power_count": len(native_rows),
                          "prime_powers": [{"p": p, "k": k, "value": power}
                                           for p, k, power in native_rows]},
        "pi_publication": pi_provenance,
        "Euler_Mascheroni": {"producer": "partes_finitas_exactas.gamma_interval(81,8,120)",
                             "exact_lower": str(gamma_bounds[0]), "exact_upper": str(gamma_bounds[1]),
                             "interval": publish(gamma_euler)},
        "log2": {"producer": "partes_finitas_exactas.log_ratio_interval(2,120)",
                 "exact_lower": str(log2_bounds[0]), "exact_upper": str(log2_bounds[1])},
        "polar_identity": {"exact_Laurent_equality": polar_identity,
                           "common_translation_invariance": True,
                           "separate_interval_crosschecks": 81},
        "tail_bound": "0<=F-F_N<=exp(-lambda_N*x)*(1/lambda_N^2+1/(2*lambda_N)), lambda_N=2*N+1/2",
        "basal_control": {"h": "1/16", "atan_alternating_terms": atan_terms,
                          "inequality": "2*M_Gamma(h) >= -c_Gamma+2*sinh(h/2)-h",
                          "tail_formula": "M_Gamma(h)=atanh(exp(-h/2))+atan(exp(-h/2))",
                          "left_side": publish(twice_tail), "right_side": publish(basal_rhs),
                          "strict_margin": publish(basal_margin),
                          "scope": "interval verification of the recovered local contraction estimate"},
        "gram_first_row": [publish(value) for value in first_row],
        "gram_matrix": [[publish(value) for value in row] for row in matrix],
        "gershgorin_margins": [publish(value) for value in margins],
        "certified_form_lower_bound": "8479/10000 times the squared L2 norm on this nine-dimensional span",
        "two_box_gram_eigenvalues": {name: [publish(value) for value in values]
                                    for name, values in two_box_eigenvalues.items()},
        "non_circulant_witness": "K_e(log(2)) < K_e(8*log(2)); phase return does not erase memory of displacement",
        "provenance": "Recovered complete columns and source-first folding; new finite interval control. No priority claim for the underlying architecture or connector.",
        "files": [{"path": str(path.relative_to(ROOT)), "sha256": sha256(path)} for path in files],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, help="write the actually executed finite-control JSON")
    args = parser.parse_args()
    try:
        report = run()
        exit_code = 0
    except Exception as exc:
        report = {"status": "FAIL", "certificate": "FINITE_NINE_BOX_COMPLETE_GRAM_INTERVALS",
                  "optimization_level": sys.flags.optimize,
                  "scope": "finite control only; no global mathematical verdict",
                  "error": type(exc).__name__ + ": " + str(exc)}
        exit_code = 1
    if args.receipt is not None:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {key: report[key] for key in ("status", "certificate", "optimization_level")}
    if exit_code == 0:
        summary.update({"checks": report["checks"], "prime_power_rows": report["native_census"]["prime_power_count"],
                        "certified_lower_bound": "0.8479", "scope": report["scope"]})
    else:
        summary["error"] = report["error"]
    if args.receipt is not None:
        summary["receipt"] = str(args.receipt.resolve())
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
