#!/usr/bin/env python3
"""Exact algebra of the signed-channel image; not an upstream E108 generator.

No alpha value, decimal target, metrology or constant recognizer is read.
The source fixture is isolated inside test_reference(), after the general
identities have been established by basis and finite exact tests.
"""
from fractions import Fraction
from itertools import product
import json

N = 12
H4 = ((1, 1, 1, 1), (1, 1, -1, -1),
      (1, -1, 1, -1), (1, -1, -1, 1))


def vector12(values):
    values = tuple(values)
    if len(values) != N:
        raise ValueError("Expected twelve coordinates")
    return values


def shift(values, count=1):
    values = vector12(values)
    return tuple(values[(i + count) % N] for i in range(N))


def difference(values, step):
    values = vector12(values)
    return tuple(values[i] - values[(i + step) % N] for i in range(N))


def transversal(values):
    values = vector12(values)
    return difference(values, 3), difference(values, 4), sum(values)


def prefixes(w):
    w = vector12(w)
    out, total = [], 0
    for value in w:
        out.append(total)
        total += value
    return tuple(out), total


def edge_charge_check(w, charge):
    w = vector12(w)
    if any(type(x) is not int for x in w) or type(charge) is not int:
        raise ValueError("The integral image requires integer coordinates")
    p, closure = prefixes(w)
    if closure:
        raise ValueError("Nonzero cyclic edge sum")
    if (charge + sum(p)) % N:
        raise ValueError("Charge congruence modulo twelve fails")
    return p


def channels_from_edges(w, charge):
    """Materializes compatible channels from independently supplied edge data.

    This function does not produce w or charge from a TPK ledger.
    """
    w = vector12(w)
    edge_charge_check(w, charge)
    b = tuple(sum(w[(i + j) % N] for j in range(3)) for i in range(N))
    c = tuple(sum(w[(i + j) % N] for j in range(4)) for i in range(N))
    return b, c, charge


def image_residuals(b, c):
    b, c = vector12(b), vector12(c)
    w = tuple(c[i] - b[(i + 1) % N] for i in range(N))
    residual = tuple(b[i] - sum(w[(i + j) % N] for j in range(3))
                     for i in range(N))
    return w, residual + (sum(w),)


def reconstruct_channels(b, c, charge):
    """Unique reconstruction on the proved image, rejecting off-image data."""
    b, c = vector12(b), vector12(c)
    if any(type(x) is not int for x in b + c):
        raise ValueError("The integral image requires integer coordinates")
    w, residual = image_residuals(b, c)
    if any(residual):
        raise ValueError("Linear channel compatibility fails")
    p = edge_charge_check(w, charge)
    first = (charge + sum(p)) // N
    return tuple(first - x for x in p)


def hadamard12(values):
    values = vector12(values)
    out = [0] * N
    for r in range(3):
        block = [values[r + 3 * j] for j in range(4)]
        for j in range(4):
            out[r + 3 * j] = sum(H4[j][a] * block[a] for a in range(4))
    return tuple(out)


def pi_h(b, c, charge):
    """The U016 rational formula, independent of the expected fixture."""
    b, c = vector12(b), vector12(c)
    sums = [sum(c[r + 3 * j] for j in range(4)) for r in range(3)]
    first = Fraction(charge + 2 * sums[0] + sums[1], 3)
    orbital = (first, first - sums[0], first - sums[0] - sums[1])
    out = [Fraction(0)] * N
    for r in range(3):
        d = [b[r + 3 * j] for j in range(4)]
        block = (orbital[r], d[1] - d[3], d[0] + d[2], d[0] - d[2])
        for j in range(4):
            out[r + 3 * j] = block[j]
    return tuple(out)


def inverse_hadamard(u):
    inverse = tuple(Fraction(x, 4) for x in hadamard12(u))
    if any(x.denominator != 1 for x in inverse):
        raise ValueError("Hadamard image congruence fails")
    return tuple(x.numerator for x in inverse)


def evaluate_signed_channels(b, c, charge):
    """Checks the full channel domain before evaluating the signed readout.

    Input coordinates must have been produced independently. This API proves
    neither their origin in an event ledger nor the generation of E108.
    The deliberately unchecked rational formula pi_h remains available only
    as an algebraic formula, e.g. for off-image negative controls.
    """
    b, c = vector12(b), vector12(c)
    reconstructed = reconstruct_channels(b, c, charge)
    signed = pi_h(b, c, charge)
    if any(x.denominator != 1 for x in signed):
        raise ValueError("Compatible integral channels produced a fractional readout")
    signed = tuple(x.numerator for x in signed)
    inverted = inverse_hadamard(signed)
    if reconstructed != inverted:
        raise ValueError("Channel and Hadamard inversions disagree")
    return {"b90": b, "b120": c, "charge": charge,
            "signed": signed, "register": inverted}


def signed_shift(u):
    return hadamard12(shift(inverse_hadamard(u)))


def rank(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    rows, columns = len(a), len(a[0])
    pivot = 0
    for column in range(columns):
        candidate = next((i for i in range(pivot, rows) if a[i][column]), None)
        if candidate is None:
            continue
        a[pivot], a[candidate] = a[candidate], a[pivot]
        scale = a[pivot][column]
        a[pivot] = [x / scale for x in a[pivot]]
        for i in range(rows):
            if i != pivot and a[i][column]:
                scale = a[i][column]
                a[i] = [x - scale * y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == rows:
            break
    return pivot


def determinant(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    result = Fraction(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            result = -result
        diag = a[j][j]
        result *= diag
        for i in range(j + 1, len(a)):
            factor = a[i][j] / diag
            for k in range(j + 1, len(a)):
                a[i][k] -= factor * a[j][k]
            a[i][j] = 0
    return result


def basis(n, i):
    return tuple(int(j == i) for j in range(n))


def expected_rejection(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Negative control was accepted")


def test_general():
    for i in range(N):
        k = basis(N, i)
        b, c, q = transversal(k)
        assert reconstruct_channels(b, c, q) == k
        assert pi_h(b, c, q) == hadamard12(k)
        assert inverse_hadamard(pi_h(b, c, q)) == k
        assert evaluate_signed_channels(b, c, q)["register"] == k
        assert signed_shift(hadamard12(k)) == hadamard12(shift(k))

    # Rational rank and an explicit maximal minor of absolute value twelve.
    cols = [transversal(basis(N, i)) for i in range(N)]
    e = [[(cols[j][0] + cols[j][1] + (cols[j][2],))[i]
          for j in range(N)] for i in range(25)]
    assert rank(e) == N
    tree_charge = [[int(j == i) - int(j == i + 1) for j in range(N)]
                   for i in range(N - 1)] + [[1] * N]
    assert abs(determinant(tree_charge)) == N
    relation_cols = []
    for i in range(24):
        x = basis(24, i)
        relation_cols.append(image_residuals(x[:12], x[12:])[1])
    relations = [[relation_cols[j][i] for j in range(24)] for i in range(13)]
    assert rank(relations) == 13

    for k in product((0, 1), repeat=N):
        b, c, q = transversal(k)
        assert reconstruct_channels(b, c, q) == k
        w = difference(k, 1)
        assert channels_from_edges(w, q) == (b, c, q)
        assert pi_h(b, c, q) == hadamard12(k)
        for rotation in (1, 3, 4, 11):
            assert transversal(shift(k, rotation)) == (
                shift(b, rotation), shift(c, rotation), q)

    # Off-image channel invisible to Pi_H, plus failed integrality.
    zero = (0,) * N
    invisible = tuple(int(i == 0) - int(i == 3) for i in range(N))
    assert pi_h(zero, invisible, 0) == zero
    assert inverse_hadamard(pi_h(zero, invisible, 0)) == zero
    expected_rejection(lambda: reconstruct_channels(zero, invisible, 0))
    expected_rejection(lambda: evaluate_signed_channels(zero, invisible, 0))
    expected_rejection(lambda: evaluate_signed_channels(zero, zero, Fraction(0)))
    expected_rejection(lambda: evaluate_signed_channels((False,) + zero[1:], zero, 0))
    expected_rejection(lambda: reconstruct_channels(zero, zero, 1))
    expected_rejection(lambda: channels_from_edges((1,) + (0,) * 11, 0))
    expected_rejection(lambda: inverse_hadamard(basis(N, 0)))

    # Two charge-preserving candidates, independent of the source fixture.
    k0 = tuple(100 + int(i == 0) for i in range(N))
    k1 = tuple(100 + int(i == 1) for i in range(N))
    assert k0 != k1 and sum(k0) == sum(k1) == 1201
    for k in (k0, k1):
        assert reconstruct_channels(*transversal(k)) == k
        assert inverse_hadamard(pi_h(*transversal(k))) == k
        assert all(0 <= x < 1000 for x in k)

    # Period-p stabilizer: fixed vectors, fixed-charge rank p-1.
    periods = (1, 2, 3, 4, 6, 12)
    for p in periods:
        repeating_basis = [tuple(int(i % p == j) for i in range(N))
                           for j in range(p)]
        assert all(shift(v, p) == v for v in repeating_basis)
        assert rank(repeating_basis) == p
        charge_zero_basis = [tuple(a - b for a, b in zip(v, repeating_basis[-1]))
                             for v in repeating_basis[:-1]]
        assert all(sum(v) == 0 for v in charge_zero_basis)
        if charge_zero_basis:
            assert rank(charge_zero_basis) == p - 1
    return {"basis_identities": 12, "binary_records_roundtripped": 4096,
            "extractor_rank": 12, "independent_linear_relations": 13,
            "tree_charge_minor_abs": 12, "negative_controls": 7,
            "signed_api_checks_full_channel_domain": True,
            "stabilizer_periods_checked": list(periods)}


def test_reference():
    """Downstream regression only; literals never feed a ledger producer."""
    k = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
    b = (-495, -116, -684, 108, 601, -90, -173, -88, 313, 560, -397, 461)
    c = (-425, -281, -481, 671, -255, 30, 475, -543, 680, 251, 6, -128)
    q = 6263
    u = (2378, 1406, 2479, -452, 998, -551, -668, -204, -371, -322, -28, -997)
    assert transversal(k) == (b, c, q)
    assert reconstruct_channels(b, c, q) == k
    assert pi_h(b, c, q) == u
    assert inverse_hadamard(u) == k
    w, residuals = image_residuals(b, c)
    p, closure = prefixes(w)
    assert not any(residuals) and closure == 0
    # Same charge and same threshold support do not select the fixture.
    other = tuple(value + int(i == 0) - int(i == 1) for i, value in enumerate(k))
    support = lambda values: tuple(i + 1 for i, x in enumerate(values) if x >= 729)
    assert other != k and sum(other) == q and support(other) == support(k)
    assert reconstruct_channels(*transversal(other)) == other
    assert all(0 <= x < 1000 for x in other)
    return {"source_fixture_used_only_for_regression": True,
            "adjacent_increments": w, "prefix_sum": sum(p),
            "charge_plus_prefix_sum": q + sum(p), "first_coordinate": k[0],
            "same_charge_same_threshold_second_candidate": other,
            "threshold_support": support(k)}


def main():
    if not __debug__:
        raise RuntimeError("This verifier requires enabled assertions; run without -O")
    report = {"status": "PASS_EXACT_SIGNED_IMAGE_ALGEBRA",
              "scope": "Image equations, inverses and covariance of the published maps",
              "upstream_E108_generator_implemented": False,
              "global_HMT_verdict": False,
              "general_checks": test_general(),
              "downstream_regression": test_reference()}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
