#!/usr/bin/env python3
"""Exact controls for mass_bridge.tex; Python standard library only.

The controls distinguish ordinary and generalized spectrum under congruence,
the information retained by the K projector, and regular versus singular
Legendre transformations. They do not certify an unconstructed physical
intertwiner between the K flow and the route-mass flow.
"""

from fractions import Fraction


def require(condition, description):
    if not condition:
        raise RuntimeError("FAIL_MASS_BRIDGE: " + description)


def add(left, right):
    result = dict(left)
    for exponent, coefficient in right.items():
        result[exponent] = result.get(exponent, Fraction(0)) + coefficient
        if not result[exponent]:
            del result[exponent]
    return result


def scale(poly, factor):
    return {power: coefficient * factor for power, coefficient in poly.items()
            if coefficient * factor}


def multiply(left, right):
    result = {}
    for first, c_first in left.items():
        for second, c_second in right.items():
            power = tuple(x + y for x, y in zip(first, second))
            result[power] = result.get(power, Fraction(0)) + c_first * c_second
    return {power: coefficient for power, coefficient in result.items()
            if coefficient}


def variable(index, exponent=1):
    powers = [0] * 5
    powers[index] = exponent
    return {tuple(powers): Fraction(1)}


def derivative(poly, index):
    result = {}
    for power, coefficient in poly.items():
        if power[index]:
            new_power = list(power)
            new_power[index] -= 1
            result[tuple(new_power)] = coefficient * power[index]
    return result


def main():
    # Rational non-isospectral congruence, even with determinant-one D.
    diagonal = (Fraction(2), Fraction(1, 2))
    mass = (Fraction(1), Fraction(1))
    transformed = tuple(d * d * m for d, m in zip(diagonal, mass))
    metric = tuple(d * d for d in diagonal)
    require(diagonal[0] * diagonal[1] == 1, "det D = 1")
    require(transformed == (Fraction(4), Fraction(1, 4)),
            "ordinary spectrum changes")
    require(transformed != mass, "ordinary spectra are distinct")
    require(all(value > 0 for value in transformed), "positivity preserved")
    require(tuple(m / g for m, g in zip(transformed, metric)) == mass,
            "generalized spectrum preserved with transported metric")

    # A second control preserves the unordered spectrum but changes route labels.
    route_mass = (Fraction(1), Fraction(4))
    route_transformed = tuple(d * d * m
                              for d, m in zip(diagonal, route_mass))
    require(route_transformed == (Fraction(4), Fraction(1)),
            "route-labelled masses transform by their own diagonal weights")

    # Uniform shift changes positional closure by an exactly rational amount.
    base = 1000
    length = 12
    K = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
    require(sum(K) == 6263, "K charge")
    number = sum(k * base ** (length - j - 1) for j, k in enumerate(K))
    require(number == 234543140729659824621058914794146601,
            "ordered base-one-thousand word")
    shifted_number = sum((k + 1) * base ** (length - j - 1)
                         for j, k in enumerate(K))
    shift = Fraction(shifted_number - number, base ** length - 1)
    require(shift == Fraction(1, 999), "exact uniform-shift falsifier")
    mean = Fraction(sum(K), length)
    shifted_mean = Fraction(sum(k + 1 for k in K), length)
    require(tuple(Fraction(k) - mean for k in K)
            == tuple(Fraction(k + 1) - shifted_mean for k in K),
            "centred vector invariant under uniform shift")

    # Symbolic Laurent-polynomial proof, exact in Q[a,b,b^-1,c,q,v].
    # b = omega*exp(eta), c = omega*exp(-eta), a = eta_dot/2.
    a, b, c, q, v = (variable(index) for index in range(5))
    inverse_b = variable(1, -1)
    velocity_shift = add(v, scale(multiply(a, q), -1))
    momentum = multiply(velocity_shift, inverse_b)
    hamiltonian = add(
        add(scale(multiply(b, multiply(momentum, momentum)), Fraction(1, 2)),
            multiply(multiply(a, q), momentum)),
        scale(multiply(c, multiply(q, q)), Fraction(1, 2)))
    legendre = add(multiply(momentum, v), scale(hamiltonian, -1))
    lagrangian = add(
        scale(multiply(multiply(velocity_shift, velocity_shift), inverse_b),
              Fraction(1, 2)),
        scale(multiply(c, multiply(q, q)), Fraction(-1, 2)))
    require(legendre == lagrangian, "symbolic Legendre identity")
    require(derivative(lagrangian, 4) == momentum,
            "momentum recovered from velocity derivative")
    require(derivative(derivative(lagrangian, 4), 4) == inverse_b,
            "regular velocity Hessian is b^-1")

    # p plays the role of v here; H_linear = p*a*q is linear in that variable.
    linear_hamiltonian = multiply(v, multiply(a, q))
    require(derivative(derivative(linear_hamiltonian, 4), 4) == {},
            "cotangent linear Hamiltonian has zero momentum Hessian")

    print("PASS_EXACT_MASS_BRIDGE_CONTROLS")
    print("ordinary_spectrum=4,1/4 generalized_spectrum=1,1")
    print("uniform_K_shift=1/999 centred_K_invariant=true")
    print("legendre_identity=exact_laurent_polynomial regular_hessian=1/b")
    print("linear_cotangent_hessian=0 physical_intertwiner_not_assumed=true")


if __name__ == "__main__":
    main()
