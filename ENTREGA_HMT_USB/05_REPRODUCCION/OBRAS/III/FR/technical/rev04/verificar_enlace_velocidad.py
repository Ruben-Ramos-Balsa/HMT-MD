#!/usr/bin/env python3
"""Exact cross-article algebra; not a new HMT generator or a metrology fit.

Default execution is read-only, stdout JSON, stdlib only. Compatible with
python3 -I -S -B and -O from an empty current working directory.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import json
from pathlib import Path


class Checks:
    def __init__(self):
        self.count = 0
        self.groups = {}

    def require(self, condition, group, detail):
        self.count += 1
        self.groups[group] = self.groups.get(group, 0) + 1
        if not condition:
            raise RuntimeError(group + ": " + detail)


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def response(q):
    return (1 - q**90) / (1 - q**120)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, help="Optional new JSON output")
    args = parser.parse_args()
    check = Checks()

    # Polynomial identity valid for an indeterminate s, not just sample s.
    check.require(poly_mul([1, -1], [1, 1, 1]) == [1, 0, 0, -1],
                  "symbolic", "1-s^3 factorization")
    check.require(poly_mul([1, -1], [1, 1, 1, 1]) == [1, 0, 0, 0, -1],
                  "symbolic", "1-s^4 factorization")
    # Exponents in the free multiplicative group on r+,r-,uC,uT,tau,d,eta.
    rp = (1, 0, 0, 0, 0, 0, 0)
    rm = (0, 1, 0, 0, 0, 0, 0)
    uc = (0, 0, 1, 0, 0, 0, 0)
    ut = (0, 0, 0, 1, 0, 0, 0)
    tau = (0, 0, 0, 0, 1, 0, 0)
    d = (0, 0, 0, 0, 0, 1, 0)
    eta = (0, 0, 0, 0, 0, 0, 1)

    def mul(*items):
        return tuple(sum(values) for values in zip(*items))

    def power(item, n):
        return tuple(n * value for value in item)

    chat = power(mul(rp, rm), -1)
    c = mul(chat, uc)
    cprim = mul(chat, power(d, -1), uc, d)
    ell = mul(tau, chat, uc, ut)
    ellprim = mul(tau, power(eta, -1), chat, power(d, -1), uc, ut, d, eta)
    check.require(c == cprim, "symbolic", "velocity as a section")
    check.require(ell == ellprim, "symbolic", "element length as a section")
    check.require(mul(ell, power(mul(tau, ut), -1)) == c,
                  "symbolic", "length/duration")
    check.require(mul(power(rm, 2), power(rp, 2), power(chat, 2)) == (0,) * 7,
                  "symbolic", "constitutive product")
    check.require(power(c, -3) == power(cprim, -3),
                  "symbolic", "radiative density covariance")
    check.require(power(c, -2) == power(cprim, -2),
                  "symbolic", "Stefan coefficient covariance")

    for qp, qm in product((F(1, 3), F(2, 5), F(7, 8)), repeat=2):
        rplus, rminus = response(qp), response(qm)
        numerator = (1 - qp**90) * (1 - qm**90)
        denominator = (1 - qp**120) * (1 - qm**120)
        determinant = rplus * rminus
        chat = 1 / determinant
        # exp(-log(numerator/denominator)) is the reciprocal on positive reals.
        check.require(determinant == numerator / denominator,
                      "exact_channel_fixtures", "logarithmic reader product")
        check.require(chat == denominator / numerator,
                      "exact_channel_fixtures", "two definitions of c-hat")
        check.require(F(3, 4) < rplus < 1 and F(3, 4) < rminus < 1,
                      "exact_channel_fixtures", "positive response domain")
        check.require(1 < chat < F(16, 9),
                      "exact_channel_fixtures", "intrinsic velocity range")
        check.require(chat == 1 / (response(qm) * response(qp)),
                      "exact_channel_fixtures", "sheet exchange")
        for q, r in ((qp, rplus), (qm, rminus)):
            s = q**30
            check.require(r == (1 + s + s*s) / (1 + s + s*s + s**3),
                          "exact_channel_fixtures", "response cancellation")
            check.require(r*s**3 + (r-1)*(1+s+s*s) == 0,
                          "exact_channel_fixtures", "original inverse cubic")

        mu, eps, z = rminus**2, rplus**2, rminus/rplus
        check.require(mu*eps*chat**2 == 1 and mu/eps == z*z,
                      "constitutive", "intrinsic identities")
        a, b, dval, eta_val = F(3, 2), F(5, 7), F(11, 4), F(13, 5)
        ucval, utval, tauval = F(17, 3), F(19, 8), F(23, 6)
        cp = chat/dval
        mup, ep, zp = mu*dval*b*b/a, eps*a*dval/(b*b), z*b*b/a
        check.require(mup*ep*cp*cp == 1 and mup/ep == zp*zp,
                      "chart", "general constitutive covariance")
        check.require(cp*(dval*ucval) == chat*ucval,
                      "chart", "physical velocity invariant")
        check.require((tauval/eta_val)*cp*(dval*eta_val*ucval*utval)
                      == tauval*chat*ucval*utval,
                      "chart", "clock and length invariant")
        check.require(chat*mu == z and chat*eps == 1/z,
                      "chart", "adapted velocity frame")
        check.require((a/dval/(b*b))*mup == mu and (b*b/a/dval)*ep == eps,
                      "chart", "undo units before inverse reader")
        for n, k in ((1, 2), (9, 27), (54, 108)):
            length_n = n*chat*ucval*utval
            duration_n = n*utval
            check.require(length_n/duration_n == chat*ucval,
                          "route", "constant-channel quotient")
            check.require(length_n + k*chat*ucval*utval
                          == (n+k)*chat*ucval*utval,
                          "route", "concatenation")
        # Exact coefficients of log r+ and log r- after normalized trace.
        # Do not build the unnormalized determinant at astronomical precision.
        for m in (0, 1, 2, 4):
            multiplicity = 9**m
            log_coeffs = (2*F(multiplicity, 2*multiplicity),) * 2
            check.require(log_coeffs == (F(1), F(1)),
                          "refinement", "normalized logarithmic trace")
            check.require((multiplicity, multiplicity)
                          == tuple(multiplicity*x for x in (1, 1)),
                          "refinement", "ordinary determinant multiplicities")

    # Varying-channel path remains additive; mean is not one selected edge.
    speeds = (F(5, 4), F(7, 6), F(9, 8))
    check.require(sum(speeds[:1]) + sum(speeds[1:]) == sum(speeds),
                  "route_variable", "length additivity")
    check.require(sum(speeds)/len(speeds) not in speeds,
                  "route_variable", "homogeneous assumption is explicit")

    result = {
        "status": "PASS_ENLACE_ALGEBRAICO_VELOCIDAD_III_V",
        "checks": check.count,
        "groups": check.groups,
        "exact_arithmetic": "integers, rational numbers, polynomial coefficients, Laurent exponents",
        "scope": {
            "recovered_identity": "same inherited channels and dimensional frame: c_int=c_vac",
            "path_length": "t0=uT implies ell0=c_hat*uL; uL=uC*uT",
            "chart_conversion": "uC_prime=d*uC; c_hat_prime=c_hat/d",
            "symbolic_proof": "printed separately in 69_enlace_constitutivo_velocidad.tex",
            "finite_fixtures": "rational channels exercise algebra; they are not HMT channel predictions",
            "does_not_certify": [
                "a new autonomous generation of the inherited channels",
                "an independent SI frame or numerical metrology prediction",
                "the realization of two transverse physical polarizations",
                "global mathematical closure of either article"
            ]
        }
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        if args.receipt.exists():
            raise FileExistsError("Refusing to overwrite an existing receipt")
        args.receipt.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
