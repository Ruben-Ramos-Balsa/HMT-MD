"""Finite exploratory check of the classical cyclic binary realization.

This is not a proof imported into Lean. The Lean module constructs the same
rows and proves its own finite assertions. Coordinates are zero-based.
"""
from collections import Counter

GENERATOR = 0xAE3  # 1+x+x^5+x^6+x^7+x^9+x^11


def encode(message):
    word = 0
    for i in range(12):
        if message >> i & 1:
            word ^= GENERATOR << i
    return word | ((bin(word).count("1") % 2) << 23)


def support(word):
    return [j for j in range(24) if word >> j & 1]


if __name__ == "__main__":
    words = [encode(m) for m in range(4096)]
    weights = Counter(bin(w).count("1") for w in words)
    assert len(set(words)) == 4096
    assert weights == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    first = next(m for m, w in enumerate(words) if bin(w).count("1") == 12)
    print("PASS_CLASSICAL_BINARY_GOLAY_EXPLORATION")
    print("generator=", GENERATOR, "weights=", dict(sorted(weights.items())))
    print("dodecad_message=", first, "support=", support(words[first]))
