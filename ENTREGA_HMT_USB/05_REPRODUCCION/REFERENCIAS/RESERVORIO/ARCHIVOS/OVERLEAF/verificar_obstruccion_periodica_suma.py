#!/usr/bin/env python3
"""Exact tests for the three-state carry-difference criterion.

This is an arithmetic test of the local criterion, not an irrationality
certificate for e+pi. No new constant digits, target constants or external
packages are used. Existing certified prefixes may be inspected read-only.
"""
from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def transitions(base: int) -> dict[int, tuple[int, int]]:
    if base < 3:
        raise ValueError("The unique-label criterion requires base >= 3.")
    table = {base * h - j: (h, j)
             for h in (-1, 0, 1) for j in (-1, 0, 1)}
    assert len(table) == 9
    return table


def path_result(labels: list[int], base: int,
                table: dict[int, tuple[int, int]] | None = None) -> dict:
    table = transitions(base) if table is None else table
    previous_end = None
    states = []
    for i, d in enumerate(labels):
        edge = table.get(d)
        if edge is None:
            return {"accepted_prefix": False, "index": i,
                    "reason": "label", "difference": d}
        h, j = edge
        if previous_end is not None and h != previous_end:
            return {"accepted_prefix": False, "index": i,
                    "reason": "concatenation", "previous_end": previous_end,
                    "required_start": h, "difference": d}
        if i == 0:
            states.append(h)
        states.append(j)
        previous_end = j
    return {"accepted_prefix": True, "states": states,
            "scope": "finite_prefix_only"}


def aggregate_return_transitions(base: int = 1000) -> dict[int, tuple[int, int]]:
    """Carry-compensated returns of t=P+E-Phi, not a return-time theorem."""
    if base <= 6:
        raise ValueError("Unique seven-state labels require base > 6.")
    bound = 3 * (base - 1)
    table = {base * h - j: (h, j)
             for h in range(-3, 4) for j in range(-3, 4)
             if abs(base * h - j) <= bound}
    assert len(table) == 37
    return table


def aggregate_return_self_check() -> dict:
    """Check telescopy and complete periodic examples with exact fractions."""
    base = 1000
    table = aggregate_return_transitions(base)
    paths = 0
    for states in itertools.product(range(-3, 4), repeat=5):
        labels = [base * states[k] - states[k + 1] for k in range(4)]
        if any(abs(d) > 3 * (base - 1) for d in labels):
            continue
        result = path_result(labels, base, table)
        assert result["states"] == list(states)
        value = sum((Fraction(d, base ** (k + 1))
                     for k, d in enumerate(labels)), Fraction(0))
        assert value - states[0] == -Fraction(states[-1], base ** len(labels))
        paths += 1
    assert path_result([1, 1], base, table)["reason"] == "concatenation"
    # Nonzero raw differences may be removed by a bounded carry: exact 2-cycle.
    labels = (base + 1, -base - 1)
    assert periodic_value(labels, base) == 1
    assert path_result(list(labels) * 3, base, table)["accepted_prefix"]
    # Canonical residual dynamics of three already-specified rational sections.
    cases = 0
    for xp, xe, xf in itertools.product(
            (Fraction(1, 7), Fraction(2, 9), Fraction(3, 11)), repeat=3):
        p, e, f = xp, xe, xf
        for _ in range(20):
            residual = p + e - f
            h = residual.numerator // residual.denominator
            assert h in (-1, 0, 1)
            y = residual - h
            dp, pn = digit(p, base)
            de, en = digit(e, base)
            df, fn = digit(f, base)
            next_residual = pn + en - fn
            hn = next_residual.numerator // next_residual.denominator
            emitted = dp + de - df
            assert emitted == base * residual - next_residual
            canonical, yn = digit(y, base)
            assert canonical == emitted + hn - base * h
            assert yn == next_residual - hn
            p, e, f = pn, en, fn
        cases += 1
    return {"status": "PASS_AGGREGATE_RETURN_TRANSDUCER",
            "states": 7, "admissible_edges": len(table),
            "exact_telescoping_paths": paths,
            "rational_triple_orbits": cases,
            "raw_equality_required": False,
            "scope": "identities_and_finite_tests_not_irrationality"}


def inspect_aggregate_returns(prefix_root: Path) -> dict:
    """Apply the composed reader to existing prefixes, with no new digits."""
    streams = [read_existing_prefix(prefix_root / (name + "_1000_decimales.txt"))
               for name in ("pi", "e", "phi")]
    n = min(map(len, streams))
    t = [streams[0][k] + streams[1][k] - streams[2][k] for k in range(n)]
    table = aggregate_return_transitions()
    best = None
    best_exact = None
    candidates = accepted = 0
    # r is the number of preceding decimal blocks; s is a decimal displacement.
    for s in range(12, n, 12):
        for r in range(n - s):
            labels = [t[r + s + k] - t[r + k] for k in range(n - r - s)]
            result = path_result(labels, 1000, table)
            ell = len(labels) if result["accepted_prefix"] else result["index"]
            exact = next((k for k, d in enumerate(labels) if d), len(labels))
            candidates += 1
            accepted += bool(ell)
            candidate = {"r": r, "s": s, "ell": ell,
                         "ell_minus_r_minus_s": ell - r - s}
            if ell and (best is None or ell - r - s > best["ell_minus_r_minus_s"]):
                best = candidate
            if exact and (best_exact is None or
                          exact - r - s > best_exact["ell_minus_r_minus_s"]):
                best_exact = {"r": r, "s": s, "ell": exact,
                              "ell_minus_r_minus_s": exact - r - s}
    # Capacity K_j is determined with integer powers, not floating logarithms.
    boundaries = [0]
    power = 729
    k = 0
    while k < n:
        power *= 729
        while 1000 ** (k + 1) <= power:
            k += 1
        boundaries.append(k)
    clocks, decorated = [], []
    for j in range(len(boundaries) - 1):
        current, following = boundaries[j:j + 2]
        delta = following - current
        assert delta in (0, 1)
        clocks.append((current % 12, delta))
        decorated.append(t[following - 1] if delta else None)
    groups = {}
    clock_counterexample = None
    for j, (clock, output) in enumerate(zip(clocks, decorated)):
        if clock in groups and groups[clock][1] != output:
            first_j, first_output = groups[clock]
            clock_counterexample = {
                "first_step": first_j, "second_step": j,
                "clock": list(clock), "first_output": first_output,
                "second_output": output,
                "scope": "excludes_only_memoryless_t_output_from_this_clock"}
            break
        groups.setdefault(clock, (j, output))
    assert clock_counterexample is not None
    return {"blocks_per_channel": n, "new_digits_computed": 0,
            "decimal_displacements_tested": "positive multiples of 12 below prefix length",
            "candidate_windows": candidates,
            "nonempty_compensated_matches": accepted,
            "best_compensated_excess": best,
            "best_raw_equality_excess": best_exact,
            "actual_clock_counterexample": clock_counterexample,
            "scope": "finite_existing_prefix_only",
            "irrationality_proved": False,
            "asymptotic_return_regime_disproved": False}


def carry_cancellation_control() -> dict:
    """Universal finite telescopy for the clock-derived control of section 24.

    All binary input words are tested; neither HMT regional stream is replaced
    in the research data. The infinite statement is proved in the manuscript.
    """
    cases = 0
    for base in (4, 10, 1000):
        a, half = (base - 2) // 2, base // 2
        for n in range(1, 11):
            for h in itertools.product((0, 1), repeat=n + 1):
                ps = [a + half * h[k] for k in range(n)]
                es = [a + half * h[k] - h[k + 1] for k in range(n)]
                assert all(0 <= d < base for d in ps + es)
                raw = [p + e for p, e in zip(ps, es)]
                assert all(raw[k] + h[k + 1] - base * h[k] == base - 2
                           for k in range(n))
                # The unnormalized aggregate recovers the input letter.
                assert all(int(raw[k] >= base) == h[k] for k in range(n))
                value = sum((Fraction(d, base ** (k + 1))
                             for k, d in enumerate(raw)), Fraction(0))
                expected = (Fraction(base - 2, base - 1)
                            * (1 - Fraction(1, base ** n))
                            + h[0] - Fraction(h[-1], base ** n))
                assert value == expected
                cases += 1
    # Bounded additive coboundaries are not automatically weighted carries.
    table = aggregate_return_transitions()
    for d in (-1, 1):
        for following in (-1, 0, 1):
            result = path_result([d, following], 1000, table)
            assert not result["accepted_prefix"]
            assert result["reason"] == "concatenation"
    return {"status": "PASS_EXACT_CARRY_CANCELLATION_CONTROL",
            "bases_tested": [4, 10, 1000],
            "exhaustive_binary_prefix_cases": cases,
            "max_prefix_length": 10,
            "nonzero_additive_coboundary_pairs_rejected": 6,
            "actual_regional_streams_replaced": False,
            "irrationality_of_e_plus_pi_proved": False,
            "irrationality_of_e_plus_pi_refuted": False,
            "scope": "control_of_general_transfer_not_a_model_of_full_HMT"}


def fractional(q: Fraction) -> Fraction:
    return q - q.numerator // q.denominator


def hensel_window_self_check() -> dict:
    """Finite identities in the documented integer Hensel chart.

    Test states are synthetic integer vectors, not HMT constant sections.
    No continuation beyond the documented chart is asserted.
    """
    matrix = ((2, 2, 2, 1, 2, 1), (2, 1, 2, 2, 1, 1),
              (1, 0, 0, 1, 0, 2), (0, 0, 1, 1, 1, 0),
              (2, 2, 2, 0, 2, 1), (2, 1, 2, 1, 0, 0))
    work = [[Fraction(x) for x in row]
            + [Fraction(i == j) for j in range(6)]
            for i, row in enumerate(matrix)]
    for col in range(6):
        pivot = next(i for i in range(col, 6) if work[i][col])
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for i in range(6):
            if i != col:
                scale = work[i][col]
                work[i] = [x - scale * y
                           for x, y in zip(work[i], work[col])]
    assert all(x.denominator == 1 for row in work for x in row[6:])
    inverse = tuple(tuple(int(x) for x in row[6:]) for row in work)

    def mul(row, mat):
        return tuple(sum(row[i] * mat[i][j] for i in range(6))
                     for j in range(6))

    def reconstruct(words, terminal):
        state = terminal
        for word in reversed(words):
            state = mul(tuple(u + 3 * x for u, x in zip(word, state)), inverse)
        return state

    seeds = ((0,) * 6, (1, 2, 3, 4, 5, 6),
             (-7, 11, -13, 17, -19, 23), (729, -271, 1, 0, 81, -9))
    windows = perturbations = frame_corrections_required = 0
    for seed in seeds:
        assert mul(mul(seed, matrix), inverse) == seed
        state, words = seed, []
        for length in range(1, 9):
            y = mul(state, matrix)
            word = tuple(x % 3 for x in y)
            state = tuple((x - u) // 3 for x, u in zip(y, word))
            words.append(word)
            assert reconstruct(words, state) == seed
            residue = reconstruct(words, (0,) * 6)
            assert all((x - y) % (3 ** length) == 0
                       for x, y in zip(seed, residue))
            frame_words = [tuple(x % 3 for x in mul(w, matrix)) for w in words]
            inverse_lifts = [mul(v, inverse) for v in frame_words]
            decoded = [tuple(x % 3 for x in w) for w in inverse_lifts]
            assert decoded == words
            assert reconstruct(decoded, (0,) * 6) == residue
            unnormalized = reconstruct(inverse_lifts, (0,) * 6)
            frame_corrections_required += any(
                (x - y) % (3 ** length) for x, y in zip(seed, unnormalized))
            for coordinate in range(6):
                changed = list(word)
                changed[coordinate] = (changed[coordinate] + 1) % 3
                invalid = reconstruct(words[:-1] + [tuple(changed)], (0,) * 6)
                assert any((x - y) % (3 ** length)
                           for x, y in zip(seed, invalid))
                perturbations += 1
            windows += 1
    # An aggregate congruence does not preserve the two fixed source states.
    left = reconstruct([(1, 0, 0, 0, 0, 0)], (0,) * 6)
    right = reconstruct([(2, 0, 0, 0, 0, 0)], (0,) * 6)
    assert all((x + y) % 3 == 0 for x, y in zip(left, right))
    assert any(x % 3 for x in left) and any(x % 3 for x in right)
    assert frame_corrections_required > 0
    return {"status": "PASS_EXACT_HENSEL_WINDOW_LIFT",
            "integer_test_windows": windows,
            "altered_windows_rejected": perturbations,
            "windows_requiring_integer_frame_correction": frame_corrections_required,
            "aggregate_only_false_positive_rejected": True,
            "new_constant_digits_computed": 0,
            "scope": "finite_chart_identity_not_global_survival_or_irrationality"}


def digit(q: Fraction, base: int) -> tuple[int, Fraction]:
    scaled = q * base
    a = scaled.numerator // scaled.denominator
    return a, scaled - a


def periodic_value(word: tuple[int, ...], base: int) -> Fraction:
    n = 0
    for d in word:
        n = base * n + d
    return Fraction(n, base ** len(word) - 1)


def check_exact_rational_case(x: Fraction, y: Fraction,
                              base: int, period: int, count: int,
                              common_cycle: int) -> None:
    """Test one entire periodic input cycle, including its closing edge.

    Finite path acceptance is equivalent to infinite acceptance here only
    because pure input periodicity and cycle coverage are verified first.
    """
    if base < 3 or period < 1 or common_cycle < 1:
        raise ValueError("Positive periods and base >= 3 are required.")
    if not (0 <= x < 1 and 0 <= y < 1):
        raise ValueError("Inputs must be fractional parts.")
    if any(fractional(base ** common_cycle * q) != q for q in (x, y)):
        raise ValueError("Inputs must be purely periodic with this cycle.")
    if count < common_cycle + 1:
        raise ValueError("The complete cycle and its closing edge are required.")
    u, v = x, y
    ps, es, zs, cs, ss = [], [], [], [], []
    for _ in range(count + period + 2):
        zs.append(u + v)
        cs.append((u + v).numerator // (u + v).denominator)
        sd, _ = digit(fractional(u + v), base)
        ss.append(sd)
        p, u = digit(u, base)
        e, v = digit(v, base)
        ps.append(p)
        es.append(e)
    ts = [p + e for p, e in zip(ps, es)]
    for k in range(count + period):
        assert ss[k] == ts[k] + cs[k + 1] - base * cs[k]
        assert base * zs[k] == ts[k] + zs[k + 1]
    ds = [ts[k + period] - ts[k] for k in range(count)]
    hs = [zs[k + period] - zs[k] for k in range(count + 1)]
    for k in range(count):
        assert ds[k] == base * hs[k] - hs[k + 1]
    # Purely periodic input streams are traversed through a full common cycle.
    same = fractional(zs[period]) == fractional(zs[0])
    result = path_result(ds, base)
    assert same == result["accepted_prefix"], (x, y, base, period)
    if same:
        assert all(h.denominator == 1 and -1 <= h <= 1 for h in hs)
        assert result["states"] == [int(h) for h in hs]


def self_check() -> dict:
    assert path_result([1, 1], 1000)["reason"] == "concatenation"
    assert path_result([2], 1000)["reason"] == "label"
    for base in (3, 10, 729, 1000):
        tab = transitions(base)
        for states in itertools.product((-1, 0, 1), repeat=5):
            labels = [base * states[k] - states[k + 1] for k in range(4)]
            assert path_result(labels, base)["states"] == list(states)
        for a, b in itertools.product(tab, repeat=2):
            result = path_result([a, b], base)
            assert result["accepted_prefix"] == (tab[a][1] == tab[b][0])
    cases = 0
    base = 3
    for length in (1, 2):
        words = list(itertools.product(range(base), repeat=length))
        # The all-(base-1) word represents 1, outside the fractional domain.
        words = [w for w in words if any(d != base - 1 for d in w)]
        for a, b in itertools.product(words, repeat=2):
            for period in range(1, 2 * length + 1):
                check_exact_rational_case(periodic_value(a, base),
                                          periodic_value(b, base),
                                          base, period, count=4 * length + 2,
                                          common_cycle=length)
                cases += 1
    try:
        check_exact_rational_case(Fraction(1, 1000), Fraction(0),
                                  3, 1, count=2, common_cycle=1)
    except ValueError:
        pass
    else:
        raise AssertionError("A finite prefix must not certify tail equality.")
    pairs = (("101222", "112221"),
             ("102221", "111222"),
             ("111221", "102222"))
    values = [(int(a, 3), int(b, 3)) for a, b in pairs]
    assert values == [(296, 403), (322, 377), (376, 323)]
    assert {a + b for a, b in values} == {699}
    assert values[1][0] - values[0][0] == 26
    assert values[1][1] - values[0][1] == -26
    return {"status": "PASS_LOCAL_THREE_STATE_CARRY_CRITERION",
            "exact_rational_cases": cases,
            "bases_tested": [3, 10, 729, 1000],
            "native_orientation_pairs": values,
            "scope": "algebraic_criterion_and_tests_not_irrationality"}


def read_existing_prefix(path: Path) -> list[int]:
    text = path.read_text(encoding="ascii").strip()
    tail = text.split(".", 1)[1]
    if not tail.isdigit():
        raise ValueError("Expected one existing decimal expansion.")
    return [int(tail[i:i + 3]) for i in range(0, len(tail) - 2, 3)]


def inspect_prefix(pi_path: Path, e_path: Path, max_period: int) -> dict:
    pi = read_existing_prefix(pi_path)
    e = read_existing_prefix(e_path)
    n = min(len(pi), len(e))
    t = [a + b for a, b in zip(pi[:n], e[:n])]
    result = []
    for p in range(1, min(max_period, n - 2) + 1):
        ds = [t[k + p] - t[k] for k in range(n - p)]
        test = path_result(ds, 1000)
        result.append({"period": p, "start_index": 1, **test})
    return {"scope": "finite_prefix_only_from_start_index_1",
            "irrationality_proved": False,
            "eventual_periodicity_excluded": False,
            "blocks_read_per_channel": n,
            "new_digits_computed": 0,
            "checks": result}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix-root", type=Path)
    parser.add_argument("--max-period", type=int, default=108)
    parser.add_argument("--aggregate-returns", action="store_true",
                        help="Test the seven-state composed aggregate reader.")
    parser.add_argument("--carry-control", action="store_true",
                        help="Check the exact clock-derived cancellation control.")
    parser.add_argument("--hensel-window", action="store_true",
                        help="Check exact finite Hensel window reconstruction.")
    args = parser.parse_args()
    out = {"self_check": self_check()}
    if args.carry_control:
        out["carry_cancellation_control"] = carry_cancellation_control()
    if args.hensel_window:
        out["hensel_window"] = hensel_window_self_check()
    if args.aggregate_returns:
        out["aggregate_return_self_check"] = aggregate_return_self_check()
        if args.prefix_root:
            out["aggregate_returns"] = inspect_aggregate_returns(args.prefix_root)
    if args.prefix_root:
        if not args.aggregate_returns:
            out["existing_prefix"] = inspect_prefix(
                args.prefix_root / "pi_1000_decimales.txt",
                args.prefix_root / "e_1000_decimales.txt", args.max_period)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
