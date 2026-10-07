#!/usr/bin/env python3
"""Certificación local finita de raíces superestables de la familia HMT eta=0.

Biblioteca estándar exclusivamente. Todos los intervalos son racionales con
denominador decimal fijo. Cada operación redondea sus extremos hacia fuera
mediante división entera; sin/cos usan polinomios de Taylor y resto de Lagrange.
Las semillas históricas proponen cajas, nunca certifican sus raíces. Este
programa no certifica primera raíz global, cascada infinita ni universalidad.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from math import isqrt
from pathlib import Path
import json
import time


SCALE = 10**100
DIGITS = 100
TERMS = 64
DEFAULT_SEEDS = Path(__file__).resolve().parents[1] / (
    "REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/"
    "certificados/vacancias_criticidad.json"
)
K = tuple(3 * m - 1 for m in range(1, 13))
SUM_K2 = sum(k * k for k in K)


def ceildiv(n: int, d: int) -> int:
    assert d > 0
    return -((-n) // d)


@dataclass(frozen=True)
class Interval:
    """Closed interval [lo/SCALE, hi/SCALE], outward-rounded exactly."""

    lo: int
    hi: int

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError("Reversed interval endpoints")

    @staticmethod
    def rational(value: str | int | Fraction) -> Interval:
        q = Fraction(value)
        return Interval(q.numerator * SCALE // q.denominator,
                        ceildiv(q.numerator * SCALE, q.denominator))

    @staticmethod
    def scaled_point(value: int) -> Interval:
        return Interval(value, value)

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __add__(self, other):
        if isinstance(other, int):
            other = Interval.rational(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, int):
            other = Interval.rational(other)
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, int):
            a, b = self.lo * other, self.hi * other
            return Interval(min(a, b), max(a, b))
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        return Interval(min(products) // SCALE, ceildiv(max(products), SCALE))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError
            if other < 0:
                return (-self) / (-other)
            return Interval(self.lo // other, ceildiv(self.hi, other))
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError("Interval denominator contains zero")
        if other.hi < 0:
            return (-self) / (-other)
        reciprocal = Interval(SCALE * SCALE // other.hi,
                              ceildiv(SCALE * SCALE, other.lo))
        return self * reciprocal

    def square(self):
        upper = max(self.lo * self.lo, self.hi * self.hi)
        lower = 0 if self.contains_zero() else min(self.lo * self.lo, self.hi * self.hi)
        return Interval(lower // SCALE, ceildiv(upper, SCALE))

    def contains_zero(self):
        return self.lo <= 0 <= self.hi

    def sign(self):
        return 1 if self.lo > 0 else -1 if self.hi < 0 else 0

    def radius_bound(self):
        midpoint = (self.lo + self.hi) // 2
        return midpoint, max(midpoint - self.lo, self.hi - midpoint)

    def expand(self, error: int):
        assert error >= 0
        return Interval(self.lo - error, self.hi + error)

    def record(self):
        return {"lower": fixed_decimal(self.lo), "upper": fixed_decimal(self.hi),
                "width": fixed_decimal(self.hi - self.lo)}


def fixed_decimal(n: int) -> str:
    sign = "-" if n < 0 else ""
    integer, remainder = divmod(abs(n), SCALE)
    fractional = str(remainder).zfill(DIGITS).rstrip("0")
    return sign + str(integer) + ("." + fractional if fractional else "")


def sqrt_fraction(n: int, d: int) -> Interval:
    """Integer square-root enclosure; no floating-point approximation."""
    lower = isqrt(n * SCALE * SCALE // d)
    exact = lower * lower * d == n * SCALE * SCALE
    upper = lower if exact else lower + 1
    assert lower * lower * d <= n * SCALE * SCALE <= upper * upper * d
    return Interval(lower, upper)


def sin_cos_taylor(x: Interval) -> tuple[Interval, Interval]:
    """Rational Taylor enclosures with rigorous global derivative bound 1.

    Cos uses degree 2*TERMS-1 (last odd coefficient zero), so its
    remainder is <= abs(x)^(2*TERMS)/(2*TERMS)!.
    Sin uses degree 2*TERMS (last even coefficient zero), so its
    remainder is <= abs(x)^(2*TERMS+1)/(2*TERMS+1)!.
    The next recurrence terms enclose these powers divided by factorials.
    """
    if max(abs(x.lo), abs(x.hi)) > 4 * SCALE:
        raise ValueError("Argument outside the chosen finite certificate domain")
    if x.lo == x.hi == 0:
        return Interval.rational(0), Interval.rational(1)
    xx = x.square()
    tc, ts = Interval.rational(1), x
    cosine, sine = tc, ts
    for j in range(1, TERMS):
        tc = -(tc * xx) / ((2 * j - 1) * (2 * j))
        ts = -(ts * xx) / ((2 * j) * (2 * j + 1))
        cosine, sine = cosine + tc, sine + ts
    next_cos = -(tc * xx) / ((2 * TERMS - 1) * (2 * TERMS))
    next_sin = -(ts * xx) / ((2 * TERMS) * (2 * TERMS + 1))
    return (sine.expand(max(abs(next_sin.lo), abs(next_sin.hi))),
            cosine.expand(max(abs(next_cos.lo), abs(next_cos.hi))))


class Family:
    def __init__(self):
        # phi_m = pi*(3m-1)/18 and uniform weights 1/12.
        # s0*phi_m = (3m-1)*sqrt(24/sum_k k^2): pi cancels exactly.
        self.c = sqrt_fraction(24, SUM_K2)
        self.frequencies = tuple(self.c * k for k in K)
        self.evaluations = 0

    def potential(self, x: Interval) -> tuple[Interval, Interval]:
        self.evaluations += 1
        if x.lo == x.hi == 0:
            return Interval.rational(0), Interval.rational(0)
        midpoint, radius = x.radius_bound()
        m = Interval.scaled_point(midpoint)
        value, derivative = Interval.rational(1), Interval.rational(0)
        cosine_sum = Interval.rational(0)
        for frequency in self.frequencies:
            sine, cosine = sin_cos_taylor(frequency * m)
            cosine_sum = cosine_sum + cosine
            derivative = derivative + frequency * sine
        value = value - cosine_sum / 12
        derivative = derivative / 12
        # Exactly sum omega_m^2/12 = 2, so |V''| <= 2 on all R.
        # Taylor's centered form has remainder <= radius^2.
        delta_x = x - m
        remainder = ceildiv(radius * radius, SCALE)
        value = (value + derivative * delta_x).expand(remainder)
        derivative = derivative.expand(2 * radius)
        return value, derivative

    def orbit(self, parameter: Interval, level: int, with_derivative=True,
              record_trace=False):
        x, derivative = Interval.rational(0), Interval.rational(0)
        powers = {}
        trajectory = []
        for j in range(1, 2**level + 1):
            potential, slope = self.potential(x)
            if with_derivative:
                derivative = -potential - parameter * slope * derivative
            x = 1 - parameter * potential
            if record_trace:
                trajectory.append(x)
            if j & (j - 1) == 0:
                powers[j.bit_length() - 1] = x
        return x, derivative, powers, trajectory


class CertificationFailure(ValueError):
    def __init__(self, level: int, conditions: dict):
        self.conditions = conditions
        super().__init__(f"Uncertified box at level {level}: {conditions}")


def certify_box(family: Family, level: int, box: Interval) -> dict:
    left, _, _, _ = family.orbit(Interval.scaled_point(box.lo), level, False)
    right, _, _, _ = family.orbit(Interval.scaled_point(box.hi), level, False)
    whole, derivative, returns, trajectory = family.orbit(box, level, record_trace=True)
    conditions = {
        "opposite_strict_endpoint_signs": left.sign() * right.sign() == -1,
        "derivative_excludes_zero_on_whole_box": not derivative.contains_zero(),
        "whole_return_encloses_zero": whole.contains_zero(),
        "all_proper_power_of_two_returns_exclude_zero":
            all(not returns[k].contains_zero() for k in range(level)),
        "complete_preclosure_itinerary_excludes_zero":
            all(not state.contains_zero() for state in trajectory[:-1]),
        "power_of_two_return_signs_alternate":
            all(returns[k].sign() == (-1)**k for k in range(level)),
    }
    if not all(conditions.values()):
        raise CertificationFailure(level, conditions)
    return {
        "level": level, "period": 2**level,
        "root_interval": box.record(), "endpoint_return_left": left.record(),
        "endpoint_return_right": right.record(),
        "parameter_derivative_on_box": derivative.record(),
        "return_on_whole_box": whole.record(),
        "proper_period_exclusions": {str(2**k): returns[k].record() for k in range(level)},
        "finite_itinerary": {
            "domain": "x_1 through x_(2^n-1), for every parameter in the root interval",
            "sign_word": "".join("+" if state.sign() > 0 else "-"
                                 for state in trajectory[:-1]),
            "states": [{"iteration": j, "sign": state.sign(), "interval": state.record()}
                       for j, state in enumerate(trajectory[:-1], start=1)],
            "power_of_two_signs": {str(2**k): returns[k].sign() for k in range(level)},
            "half_period_coordinate_sign": returns[level - 1].sign(),
            "alternation_rule": "sign(x_(2^j))=(-1)^j for 0<=j<n",
            "parameter_box_uniformly_certified": True,
        },
        "checks": conditions, "existence_and_local_uniqueness": True,
        "minimal_period_exactly": 2**level,
        "first_root_after_previous_globally_certified": False,
    }


def negative_and_arithmetic_tests(family: Family, roots: dict[int, Interval]) -> dict:
    tests = {}
    try:
        Interval(1, 0)
    except ValueError:
        tests["reversed_interval_rejected"] = True
    try:
        Interval.rational(1) / Interval(-1, 1)
    except ZeroDivisionError:
        tests["zero_denominator_rejected"] = True
    tests["zero_derivative_not_unique"] = Interval(-SCALE, SCALE).contains_zero()
    try:
        certify_box(family, 2, Interval.rational(0))
    except CertificationFailure as failure:
        tests["non_root_parameter_rejected"] = not failure.conditions[
            "opposite_strict_endpoint_signs"]
    # A genuine period-2 root is also a root of the period-4 equation;
    # the proper-period check must reject this inherited root.
    try:
        certify_box(family, 2, roots[1])
    except CertificationFailure as failure:
        tests["inherited_lower_period_root_rejected"] = not failure.conditions[
            "all_proper_power_of_two_returns_exclude_zero"]
    for a in (Fraction(-7, 13), Fraction(2, 3), Fraction(11, 7)):
        for b in (Fraction(-3, 5), Fraction(5, 9), Fraction(13, 4)):
            ai, bi = Interval.rational(a), Interval.rational(b)
            for value, interval in ((a+b, ai+bi), (a-b, ai-bi),
                                    (a*b, ai*bi), (a/b, ai/bi)):
                assert Fraction(interval.lo, SCALE) <= value <= Fraction(interval.hi, SCALE)
    tests["signed_rational_arithmetic_enclosures"] = True
    s, c = sin_cos_taylor(Interval.rational(0))
    tests["exact_origin_trigonometry"] = s.lo == s.hi == 0 and c.lo == c.hi == SCALE
    assert len(tests) == 7 and all(tests.values())
    return tests


def main():
    global SCALE, DIGITS, TERMS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=Path, default=DEFAULT_SEEDS)
    parser.add_argument("--max-level", type=int, default=8, choices=range(2, 9))
    parser.add_argument("--digits", type=int, default=100)
    parser.add_argument("--radius-exp", type=int, default=42)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("CERTIFICADO_RAICES_INTERVALOS.json"))
    args = parser.parse_args()
    if args.digits < 80 or args.radius_exp < 25 or args.radius_exp > args.digits - 30:
        parser.error("Use digits>=80 and 25<=radius-exp<=digits-30")
    DIGITS, SCALE = args.digits, 10**args.digits
    TERMS = max(64, DIGITS)
    start = time.monotonic()
    raw = args.seeds.read_bytes()
    # Only root seeds are read; neither historical delta nor alpha_F is accessed.
    seed_strings = json.loads(raw)["dodecaphase_quadratic_criticality"][
        "undeformed_eta_zero"]["superstable_parameters"]
    family = Family()
    radius = SCALE // 10**args.radius_exp
    roots = {0: Interval.rational(0)}
    certificates = []
    for level in range(1, args.max_level + 1):
        center = Interval.rational(seed_strings[str(level)])
        box = Interval(center.lo - radius, center.hi + radius)
        if not box.lo > roots[level - 1].hi:
            raise ValueError("The candidate root intervals are not strictly ordered")
        certificate = certify_box(family, level, box)
        roots[level] = box
        certificates.append(certificate)
        print(f"CERTIFIED_LOCAL_ROOT level={level} period={2**level}", flush=True)
    ratios = {}
    for level in range(2, args.max_level + 1):
        numerator = roots[level - 1] - roots[level - 2]
        denominator = roots[level] - roots[level - 1]
        assert numerator.lo > 0 and denominator.lo > 0
        ratios[str(level)] = (numerator / denominator).record()
    tests = negative_and_arithmetic_tests(family, roots)
    result = {
        "schema": "hmt.feigenbaum.local_superstable_interval_certificate.v1",
        "status": "PASS_LOCAL_FINITE_ROOTS_AND_RATIOS",
        "scope": "Uniform eta=0 dodecaphase family; local finite existence, uniqueness and minimal periods",
        "arithmetic": {
            "backend": "Python arbitrary-precision integers; fixed-denominator rational intervals",
            "decimal_scale_exponent": DIGITS, "directed_rounding": "floor lower, ceil upper",
            "sqrt": "integer isqrt enclosure",
            "sin_cos": "Taylor polynomials with Lagrange remainder |derivative|<=1",
            "terms": TERMS,
            "potential_extension": "centered second-order enclosure; exact |V''|<=2",
        },
        "family": {
            "eta": "0", "weights": "1/12", "k": K, "sum_k_squared": SUM_K2,
            "frequency_rule": "omega_m=(3m-1)*sqrt(24/sum_k_squared)",
            "potential": "V(x)=1-sum_m cos(omega_m*x)/12",
            "map": "f_a(x)=1-a*V(x)", "equation": "F_n(a)=f_a^(2^n)(0)=0",
            "normalization": "V(0)=V'(0)=0, V''(0)=2 exactly",
            "pi_cancellation": "s0*phi_m=(3m-1)*sqrt(24/sum_k_squared) exactly for eta=0",
            "frequency_scale_interval": family.c.record(),
        },
        "provenance": {
            "seed_file": str(args.seeds.resolve()),
            "seed_sha256": hashlib.sha256(raw).hexdigest(),
            "used_json_member": "dodecaphase_quadratic_criticality.undeformed_eta_zero.superstable_parameters",
            "role": "Untrusted numerical proposals; every enclosing box independently checked",
            "Feigenbaum_target_values_used": False,
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "certified_root_levels": [1, args.max_level], "root_certificates": certificates,
        "delta_definition": "(a_(n-1)-a_(n-2))/(a_n-a_(n-1)), with a_0=0 convention",
        "delta_intervals": ratios, "negative_and_arithmetic_tests": tests,
        "not_claimed": ["first root globally after previous level", "infinite cascade",
                        "convergence to universal Feigenbaum delta", "limit error bound",
                        "global uniqueness of each superstable equation"],
        "potential_evaluations": family.evaluations,
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "levels": args.max_level,
                      "delta_last": ratios[str(args.max_level)], "output": str(args.output),
                      "elapsed_seconds": result["elapsed_seconds"]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
