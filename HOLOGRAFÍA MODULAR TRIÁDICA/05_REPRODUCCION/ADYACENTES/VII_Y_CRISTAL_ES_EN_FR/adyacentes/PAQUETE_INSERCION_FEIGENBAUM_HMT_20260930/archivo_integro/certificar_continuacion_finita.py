#!/usr/bin/env python3
"""Bounded interval exclusion between successive HMT superstable roots.

Read-only unless --output is supplied. Reuses the rational interval backend in
certificar_raices.py. A PASS proves exactly two zeros of S_n on a covered
closed interval: the inherited period-2^(n-1) zero and the new period-2^n zero.
It does not assume global kneading monotonicity or certify an infinite limit.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from math import factorial
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("hmt_finite_roots", HERE / "certificar_raices.py")
base = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = base
spec.loader.exec_module(base)
I, SCALE = base.Interval, base.SCALE


def magnitude(x):
    return max(abs(x.lo), abs(x.hi))


class PolynomialFamily(base.Family):
    """Exact moment polynomial; global tail and |u''|<=2 centered extension."""

    def __init__(self, terms=32):
        super().__init__()
        self.terms = terms
        # omega_k^2 = 4 k^2 / 899 exactly; pi already cancelled in s0 phi_k.
        self.moments = [Fraction(sum(k ** (2*j) for k in base.K), 12)
                        * Fraction(4, 899) ** j for j in range(terms + 2)]
        self.coefficients = [I.rational((-1) ** (j+1) * self.moments[j]
                                      / factorial(2*j)) for j in range(1, terms+1)]
        self.gradient = [coefficient * (2*j) for j, coefficient
                         in enumerate(self.coefficients, 1)]
        self.max_frequency_squared = Fraction(4 * max(base.K)**2, 899)
        # 0 < omega_k < 3 < pi: u is even and strictly increasing on (0,1].
        # Thus 0 < lambda <= 2/u(1) gives f_lambda([-1,1]) subset [-1,1].
        assert self.max_frequency_squared < 9
        self.tail_coefficient = self.moments[terms+1] / factorial(2*terms+2)
        self.gradient_tail_coefficient = self.moments[terms+1] / factorial(2*terms+1)
        radius = Fraction(3, 2)
        ratio = self.max_frequency_squared * radius**2 / ((2*terms+3)*(2*terms+4))
        derivative_ratio = self.max_frequency_squared * radius**2 / ((2*terms+2)*(2*terms+3))
        assert 0 <= ratio < 1 and 0 <= derivative_ratio < 1
        tail = self.tail_coefficient * radius**(2*terms+2) / (1-ratio)
        gradient_tail = self.gradient_tail_coefficient * radius**(2*terms+1) / (1-derivative_ratio)
        self.tail_error = base.ceildiv(tail.numerator*SCALE, tail.denominator)
        self.gradient_tail_error = base.ceildiv(gradient_tail.numerator*SCALE, gradient_tail.denominator)
        self.point_cache = {}

    def point(self, scaled_x):
        if scaled_x in self.point_cache:
            return self.point_cache[scaled_x]
        if abs(scaled_x) > 3*SCALE//2:
            raise ValueError("Point outside the declared |x|<=3/2 polynomial domain")
        x = I.scaled_point(scaled_x)
        if not scaled_x:
            result = I.rational(0), I.rational(0)
        else:
            square = x.square()
            value, derivative = self.coefficients[-1], self.gradient[-1]
            for coefficient, gradient in zip(reversed(self.coefficients[:-1]),
                                             reversed(self.gradient[:-1])):
                value = value * square + coefficient
                derivative = derivative * square + gradient
            value, derivative = value * square, derivative * x
            value = value.expand(self.tail_error)
            derivative = derivative.expand(self.gradient_tail_error)
            result = value, derivative
        # The cache is an optimization of identical integer arguments only.
        if len(self.point_cache) < 20000:
            self.point_cache[scaled_x] = result
        return result

    def potential(self, x):
        self.evaluations += 1
        middle, radius = x.radius_bound()
        value, derivative = self.point(middle)
        value = (value + derivative*(x-I.scaled_point(middle))).expand(
            base.ceildiv(radius*radius, SCALE))
        derivative = derivative.expand(2*radius)
        return value, derivative

    def orbit(self, parameter, level, with_derivative=True, record_trace=False):
        x, derivative = I.rational(0), I.rational(0)
        powers, trajectory = {}, []
        for step in range(1, 2**level+1):
            potential, slope = self.potential(x)
            if with_derivative:
                derivative = -potential-parameter*slope*derivative
            x = 1-parameter*potential
            # Valid only after certify_level has proved global self-map bounds.
            x = I(max(-SCALE, x.lo), min(SCALE, x.hi))
            if record_trace:
                trajectory.append(x)
            if step & (step-1) == 0:
                powers[step.bit_length()-1] = x
        return x, derivative, powers, trajectory


def read_box(record):
    left, right = I.rational(record["lower"]), I.rational(record["upper"])
    return I(left.lo, right.hi)


def disjoint(a, b):
    return a.hi < b.lo or b.hi < a.lo


def certify_level(family, level, roots, upper, deadline, max_boxes):
    start = time.monotonic()
    inherited, target = roots[level-1], roots[level]
    full = I(inherited.lo, upper.hi)
    u1, _ = family.potential(I.rational(1))
    assert full.lo > 0 and (full*u1).hi < 2*SCALE
    # Recheck both local boxes for the equation S_n, including inherited root.
    anchors = []
    for name, box in (("inherited", inherited), ("new", target)):
        left = family.orbit(I.scaled_point(box.lo), level, False)[0]
        right = family.orbit(I.scaled_point(box.hi), level, False)[0]
        derivative = family.orbit(box, level)[1]
        if left.sign()*right.sign() != -1 or derivative.contains_zero():
            return dict(level=level, status="LOCAL_ANCHOR_UNRESOLVED", anchor=name)
        anchors.append(dict(name=name, box=box, derivative=derivative))

    # A piece adjacent to an anchor can be absorbed by monotonicity on their hull.
    stack = [(I(inherited.hi, target.lo), "between"),
             (I(target.hi, upper.hi), "right")]
    counts = {"range_exclusion":0, "monotone_exclusion":0,
              "anchor_hull":0, "subdivisions":0}
    leaves, processed = [], 0
    while stack:
        if processed >= max_boxes or time.monotonic() > deadline:
            return dict(level=level, status="INCOMPLETE_BUDGET", processed=processed,
                        counts=counts, pending_boxes=len(stack),
                        pending=[box.record() for box, _ in stack],
                        elapsed_seconds=time.monotonic()-start,
                        certified_leaves=leaves)
        box, side = stack.pop()
        processed += 1
        value, derivative, _, _ = family.orbit(box, level)
        method = None
        if not value.contains_zero():
            method = "range_exclusion"
        elif not derivative.contains_zero():
            left = family.orbit(I.scaled_point(box.lo), level, False)[0]
            right = family.orbit(I.scaled_point(box.hi), level, False)[0]
            if left.sign() and left.sign() == right.sign():
                method = "monotone_exclusion"
        if method is None:
            for anchor in anchors:
                abox = anchor["box"]
                if box.lo == abox.hi or box.hi == abox.lo:
                    hull = I(min(box.lo, abox.lo), max(box.hi, abox.hi))
                    slope = family.orbit(hull, level)[1]
                    if not slope.contains_zero():
                        method = "anchor_hull"
                        break
        if method is not None:
            counts[method] += 1
            leaves.append(dict(interval=box.record(), method=method))
            continue
        midpoint = (box.lo+box.hi)//2
        if midpoint in (box.lo, box.hi):
            return dict(level=level, status="UNRESOLVED_AT_ARITHMETIC_SCALE",
                        box=box.record(), processed=processed, counts=counts)
        counts["subdivisions"] += 1
        stack.extend(((I(midpoint, box.hi), side), (I(box.lo, midpoint), side)))
    # Exact integer endpoint tiling: includes the two certified root anchors.
    pieces = [inherited, target] + [read_box(leaf["interval"]) for leaf in leaves]
    pieces.sort(key=lambda box: box.lo)
    assert pieces[0].lo == full.lo and pieces[-1].hi == full.hi
    assert all(a.hi == b.lo for a,b in zip(pieces, pieces[1:]))
    return dict(level=level, status="PASS_EXACTLY_TWO_ROOTS_ON_COVERED_INTERVAL",
                interval=full.record(), known_roots=[a["box"].record() for a in anchors],
                processed=processed, counts=counts, certified_leaves=leaves,
                elapsed_seconds=time.monotonic()-start,
                conclusion="Only inherited lambda_(n-1) and new lambda_n; no other S_n zero")


def self_test(family):
    reference = base.Family()
    for rational in ("-1", "-3/4", "-1/5", "0", "1/3", "1"):
        box = I.rational(rational)
        actual, actual_d = family.potential(box)
        expected, expected_d = reference.potential(box)
        assert not disjoint(actual, expected) and not disjoint(actual_d, expected_d)
    return "PASS_POLYNOMIAL_AND_TRIGONOMETRIC_ENCLOSURES_OVERLAP"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate",type=Path, default=HERE/"CERTIFICADO_RAICES_INTERVALOS.json")
    parser.add_argument("--levels",type=int,nargs="+",default=[2,3,4,5,6,7,8])
    parser.add_argument("--upper",default="1.874039")
    parser.add_argument("--seconds",type=float,default=20)
    parser.add_argument("--max-boxes",type=int,default=400)
    parser.add_argument("--terms",type=int,default=32)
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if any(n not in range(2,9) for n in args.levels) or args.terms<24:
        parser.error("Choose levels 2..8 and terms >=24")
    family=PolynomialFamily(args.terms)
    raw=args.certificate.read_bytes()
    data=json.loads(raw)
    roots={r["level"]:read_box(r["root_interval"]) for r in data["root_certificates"]}
    upper=I.rational(args.upper)
    tests=self_test(family) if args.self_test else "NOT_RUN"
    deadline=time.monotonic()+args.seconds
    reports=[]
    for level in args.levels:
        report=certify_level(family,level,roots,upper,deadline,args.max_boxes)
        reports.append(report)
        print(json.dumps({k:v for k,v in report.items()
                          if k not in ("certified_leaves","pending")}),flush=True)
        if report["status"] != "PASS_EXACTLY_TWO_ROOTS_ON_COVERED_INTERVAL":
            break
    complete = len(reports)==len(args.levels) and all(
        r["status"] == "PASS_EXACTLY_TWO_ROOTS_ON_COVERED_INTERVAL" for r in reports)
    result=dict(schema="hmt.feigenbaum.finite_root_exclusion.v1", reports=reports,
                status="PASS_FINITE_ROOT_CONTINUATION" if complete else "INCOMPLETE_FINITE_ROOT_CONTINUATION",
                requested_levels=args.levels,
                self_test=tests, backend="Exact integer outward rational intervals and moment Taylor tails",
                polynomial=dict(terms=family.terms, point_domain="|x|<=3/2",
                                exact_moment="M_j=(4/899)^j sum_(k in {2,5,...,35}) k^(2j)/12",
                                potential_uniform_tail=base.fixed_decimal(family.tail_error),
                                derivative_uniform_tail=base.fixed_decimal(family.gradient_tail_error),
                                centered_extension="|u''|<=sum omega_k^2/12=2"),
                base_level=dict(level=1, proof="S_1(lambda)=1-lambda*u(1), u(1)>0; exactly one zero 1/u(1)"),
                source_certificate_sha256=hashlib.sha256(raw).hexdigest(),
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                exclusions="No claim of infinite cascade, renormalization basin, parameter universality or asymptotic tail")
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    main()
