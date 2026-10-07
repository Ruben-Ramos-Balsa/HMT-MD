"""Exact rational interface for an already generated regional interval producer.

The constructor takes a callable producing rational enclosures, never a real
constant or a target digit string. Universal termination requires a valid
shrinking enclosure producer and avoidance of the queried radix boundaries;
those hypotheses cannot be inferred from a finite test. The executable tests
exercise arithmetic compatibility on independently generated geometric names.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable
import argparse
import json

Bounds = tuple[Fraction, Fraction]
Producer = Callable[[int], Bounds]


def floor_q(x: Fraction) -> int:
    return x.numerator // x.denominator


def ceil_q(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


class SearchLimit(RuntimeError):
    """A requested finite execution budget ended; not a nonexistence proof."""


class EnclosureCache:
    def __init__(self, producer: Producer):
        self.producer = producer
        self.cache: list[Bounds] = []

    def enclosure(self, j: int) -> Bounds:
        if j < 0:
            raise ValueError("The approximation index is nonnegative")
        while len(self.cache) <= j:
            lo, hi = self.producer(len(self.cache))
            if not isinstance(lo, Fraction) or not isinstance(hi, Fraction):
                raise TypeError("The producer must return exact Fractions")
            if lo > hi:
                raise ValueError("Reversed input enclosure")
            if self.cache:
                a, z = self.cache[-1]
                lo, hi = max(a, lo), min(z, hi)
            if lo > hi:
                raise ValueError("The accumulated rational enclosures are disjoint")
            self.cache.append((lo, hi))
        return self.cache[j]


def publish_prefix(oracle: EnclosureCache, base: int, depth: int,
                   max_queries: int | None = None) -> tuple[int, int]:
    if base < 2 or depth < 0:
        raise ValueError("Require base >= 2 and depth >= 0")
    scale = base ** depth
    j = 0
    while True:
        if max_queries is not None and j >= max_queries:
            raise SearchLimit("No separated cell within the requested budget")
        lo, hi = oracle.enclosure(j)
        first, last = floor_q(scale * lo), ceil_q(scale * hi) - 1
        if first == last:
            return j, first
        j += 1


@dataclass(frozen=True)
class Emission:
    depth_before: int
    prefix_before: int
    index: int
    digit: int
    prefix_after: int
    residual_before: Bounds
    residual_after: Bounds


class ResidualReader:
    def __init__(self, oracle: EnclosureCache, base: int, initial_depth: int,
                 max_queries: int | None = None):
        self.oracle = oracle
        self.base = base
        self.depth = initial_depth
        self.index, self.prefix = publish_prefix(
            oracle, base, initial_depth, max_queries)
        self.initial_depth = initial_depth
        self.initial_prefix = self.prefix
        self.history: list[Emission] = []
        self._check_unit_interval(self.residual_interval())

    @staticmethod
    def _check_unit_interval(interval: Bounds) -> None:
        lo, hi = interval
        if not (0 <= lo <= hi <= 1):
            raise ValueError("Residual enclosure is outside the normalized cell")

    def residual_interval(self, j: int | None = None) -> Bounds:
        if j is None:
            j = self.index
        if j < self.index:
            raise ValueError("Residual name starts at the current certified index")
        lo, hi = self.oracle.enclosure(j)
        scale = self.base ** self.depth
        return scale * lo - self.prefix, scale * hi - self.prefix

    def step(self, max_queries: int | None = None) -> Emission:
        j = self.index
        queried = 0
        while True:
            if max_queries is not None and queried >= max_queries:
                raise SearchLimit("Residual cell not separated within execution budget")
            before = self.residual_interval(j)
            first = floor_q(self.base * before[0])
            last = ceil_q(self.base * before[1]) - 1
            queried += 1
            if first == last:
                break
            j += 1
        digit = first
        if not 0 <= digit < self.base:
            raise ValueError("The emitted block is outside the declared radix")
        new_prefix = self.base * self.prefix + digit
        after = (self.base * before[0] - digit,
                 self.base * before[1] - digit)
        self._check_unit_interval(after)
        event = Emission(self.depth, self.prefix, j, digit,
                         new_prefix, before, after)
        self.prefix = new_prefix
        self.depth += 1
        self.index = j
        self.history.append(event)
        if self.residual_interval() != after:
            raise AssertionError("Affine residual update disagrees with the source name")
        if new_prefix // self.base != event.prefix_before:
            raise AssertionError("Prefix truncation failed")
        if tuple((x + digit) / self.base for x in after) != before:
            raise AssertionError("Residual interval recovery failed")
        return event

    def approximate(self, width: Fraction,
                    max_queries: int | None = None) -> tuple[int, Bounds]:
        if width <= 0:
            raise ValueError("The requested width must be positive")
        j, queried = self.index, 0
        while True:
            if max_queries is not None and queried >= max_queries:
                raise SearchLimit("Requested enclosure width not reached in budget")
            interval = self.residual_interval(j)
            queried += 1
            if interval[1] - interval[0] <= width:
                self.index = j
                return j, interval
            j += 1


def geometric_name(offset: int = 0, weight: int = 1) -> Producer:
    """Test producer: finite sums of a generated geometric series.

    Its input is the recurrence ratio 1/8, offset, and integer weight.
    The exact limit is used only by the tests after the interface executes.
    """
    if weight <= 0:
        raise ValueError("Positive test weights only")

    def bounds(j: int) -> Bounds:
        ratio = Fraction(1, 8)
        term = ratio
        partial = Fraction(offset)
        for _ in range(j + 1):
            partial += weight * term
            term *= ratio
        tail_bound = 2 * weight * term / (1 - ratio)
        return partial, partial + tail_bound
    return bounds


def self_test() -> dict[str, object]:
    comparisons = 0
    recoveries = 0
    cases = []
    for base in (2, 3, 729, 1000):
        for initial_depth in (0, 1, 6):
            for offset, weight in ((0, 1), (2, 1), (0, 3)):
                producer = geometric_name(offset, weight)
                reader = ResidualReader(EnclosureCache(producer), base,
                                        initial_depth, max_queries=2000)
                # This exact value is a posterior test oracle, not a constructor input.
                expected_value = Fraction(offset) + Fraction(weight, 7)
                assert reader.prefix == floor_q(base ** initial_depth * expected_value)
                for _ in range(12):
                    event = reader.step(max_queries=2000)
                    _, direct = publish_prefix(EnclosureCache(producer), base,
                                               reader.depth, max_queries=2000)
                    assert reader.prefix == direct
                    assert direct == floor_q(base ** reader.depth * expected_value)
                    lo, hi = reader.residual_interval()
                    residual = base ** reader.depth * expected_value - direct
                    assert lo <= residual <= hi
                    assert reader.prefix % base == event.digit
                    assert ((event.prefix_after - event.digit) // base
                            == event.prefix_before)
                    comparisons += 1
                    recoveries += 1
                _, refined = reader.approximate(Fraction(1, 10 ** 10), 2000)
                assert refined[1] - refined[0] <= Fraction(1, 10 ** 10)
                assert reader.prefix // base ** 12 == reader.initial_prefix
                cases.append({"base": base, "initial_depth": initial_depth,
                              "offset": offset, "weight": weight,
                              "emissions": len(reader.history), "index": reader.index})
    producer = geometric_name()
    for n in range(1, 9):
        assert publish_prefix(EnclosureCache(producer), 729, n)[1] == \
               publish_prefix(EnclosureCache(producer), 3, 6 * n)[1]
        assert publish_prefix(EnclosureCache(producer), 1000, n)[1] == \
               publish_prefix(EnclosureCache(producer), 10, 3 * n)[1]
    # A boundary input is outside the strict-separation theorem.
    try:
        publish_prefix(EnclosureCache(lambda _: (Fraction(1), Fraction(1))),
                       1000, 1, max_queries=4)
        raise AssertionError("A boundary was incorrectly declared separated")
    except SearchLimit:
        pass
    # Invalid producer evidence is detected, not patched into a value.
    try:
        invalid = EnclosureCache(lambda j: (Fraction(j), Fraction(j)))
        invalid.enclosure(1)
        raise AssertionError("Disjoint enclosures were accepted")
    except ValueError:
        pass
    return {"status": "PASS_RESIDUAL_RATIONAL_INTERFACE",
            "scope": "Exact finite tests of a parametric interface; universal proof is in LaTeX",
            "target_constant_inputs": False,
            "full_enriched_transition_equivalence": False,
            "cases": cases, "prefix_comparisons": comparisons,
            "recovery_checks": recoveries,
            "radix_grouping_checks": 16,
            "boundary_rejection": True, "invalid_producer_rejection": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2, ensure_ascii=False))
    else:
        parser.error("Import the parametric interface or request --self-test")
