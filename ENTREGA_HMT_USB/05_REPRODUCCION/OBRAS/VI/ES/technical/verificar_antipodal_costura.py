#!/usr/bin/env python3
"""Pruebas exactas de cancelación antipodal y costura 108->1080."""

import itertools
import random


def sgn(value: int) -> int:
    return (value > 0) - (value < 0)


def j2(digit: int) -> int:
    if digit == 9:
        return 0
    if digit in (2, 4, 6, 8):
        return 1
    if digit in (1, 3, 5, 7):
        return -1
    raise ValueError(digit)


def antipodal(first_half: tuple[int, ...]) -> tuple[int, ...]:
    return first_half + tuple(-value for value in first_half)


def shift(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    amount %= len(values)
    return values[amount:] + values[:amount]


def scalar_readers(events: tuple[int, ...]) -> tuple[int, int]:
    blocks = [sum(events[(a + 4 * r) % 12] for r in range(3)) for a in range(4)]
    b120 = sum(sgn(value) for value in blocks)
    tau = [sgn(value) for value in events]
    bzeta = sum(tau[m] * tau[(m + 3) % 12] for m in range(12))
    return b120, bzeta


def tz(word: list[int]) -> int:
    return sum(j2(word[index - 1]) for index, digit in enumerate(word) if digit == 9)


def cz(word: list[int]) -> int:
    return sum(j2(word[index - 1]) for index in range(26, len(word), 27) if word[index] == 9)


def seam_formula(blocks: list[list[int]]) -> int:
    first = [block[0] for block in blocks]
    last = [block[-1] for block in blocks]
    return sum(
        j2(last[(b - 1) % len(blocks)]) - j2(last[b])
        for b in range(len(blocks))
        if first[b] == 9
    )


def verify_antipodal() -> None:
    for first_half in itertools.product(range(-2, 3), repeat=6):
        events = antipodal(first_half)
        assert all(events[(m + 6) % 12] == -events[m] for m in range(12))
        assert scalar_readers(events) == (0, 0)

        # A_3^2=A_6=-I on the anti-invariant sector.
        shifted_six = shift(events, 6)
        shifted_three_twice = shift(shift(events, 3), 3)
        assert shifted_six == tuple(-value for value in events)
        assert shifted_three_twice == shifted_six


def verify_seams() -> None:
    rng = random.Random(1080)
    for _ in range(250):
        blocks = [[rng.randrange(1, 10) for _ in range(108)] for _ in range(10)]
        concatenated = [digit for block in blocks for digit in block]
        delta_t = tz(concatenated) - sum(tz(block) for block in blocks)
        delta_c = cz(concatenated) - sum(cz(block) for block in blocks)
        assert delta_t == seam_formula(blocks)
        assert delta_c == 0

    blocks = [[1] * 108 for _ in range(10)]
    blocks[1][0] = 9
    blocks[1][-1] = 2
    concatenated = [digit for block in blocks for digit in block]
    delta_t = tz(concatenated) - sum(tz(block) for block in blocks)
    assert delta_t == seam_formula(blocks) == -2
    assert cz(concatenated) - sum(cz(block) for block in blocks) == 0


def main() -> None:
    verify_antipodal()
    verify_seams()
    print("PASS_VI_ANTIPODAL_SEAM_108_1080")


if __name__ == "__main__":
    main()
