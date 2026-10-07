"""Reproduce a concrete Paley-Witt to binary-Golay dodecad chart.

Finite exploration/certificate only; no result is imported as a Lean axiom.
All coordinates are zero-based. The encoding of n in Fin 729 is little-endian:
    w(i) = (n // 3**i) % 3, 0 <= i < 6.
Binary messages are little-endian coefficients of the degree <= 11 polynomial.
"""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "lean/base"
ARTICLE = ROOT / "documentation/excepcional.tex"

SOURCES = [
    (BASE / "CoxeterNeighbor.lean", "324-347: paleyWitt, encode, wittCode"),
    (BASE / "SectorIncidenceData.lean", "31-32: wordSupport"),
    (BASE / "PaleyCharacterConstruction.lean", "51-69, 90-104: generated encoder and supports"),
    (ARTICLE, "521-566: binary Golay realization and incidence chart ell"),
    (Path(__file__).resolve().parent.parent / "binary/check_golay.py", "0xAE3 binary encoder, dodecad message 9"),
]

AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)
GENERATOR = 0xAE3
DODECAD_MESSAGE = 9
LOCAL_CHART = (0, 1, 2, 3, 4, 5, 10, 6, 11, 7, 9, 8)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binary_encode(message):
    value = 0
    for i in range(12):
        if message >> i & 1:
            value ^= GENERATOR << i
    return value | ((bin(value).count("1") % 2) << 23)


def binary_support(word):
    return frozenset(i for i in range(24) if word >> i & 1)


def ternary_digits(n):
    return tuple((n // (3 ** i)) % 3 for i in range(6))


def ternary_encode(n):
    w = ternary_digits(n)
    return w + tuple(sum(w[i] * AW[i][j] for i in range(6)) % 3 for j in range(6))


def ternary_support(n):
    return frozenset(i for i, digit in enumerate(ternary_encode(n)) if digit)


def certificate():
    all_binary = [binary_support(binary_encode(m)) for m in range(4096)]
    assert len(set(all_binary)) == 4096
    dodecad = all_binary[DODECAD_MESSAGE]
    assert len(dodecad) == 12
    dcoords = sorted(dodecad)
    assert dcoords == [0, 1, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14]
    assert sorted(LOCAL_CHART) == list(range(12))
    ambient_chart = tuple(dcoords[i] for i in LOCAL_CHART)

    residual_to_message = {}
    for m, support in enumerate(all_binary):
        intersection = support & dodecad
        if len(support) == 8 and len(intersection) == 6:
            assert intersection not in residual_to_message, "Octad lift is not unique"
            residual_to_message[intersection] = m

    ternary_hexads = {}
    for n in range(729):
        support = ternary_support(n)
        if len(support) == 6:
            ternary_hexads.setdefault(support, []).append(n)

    assert len(ternary_hexads) == 132
    assert len(residual_to_message) == 132
    assert sum(map(len, ternary_hexads.values())) == 264
    assert all(len(ns) == 2 for ns in ternary_hexads.values())
    mapped = {frozenset(ambient_chart[i] for i in support) for support in ternary_hexads}
    assert mapped == set(residual_to_message), "Full 132-to-132 support equality failed"

    table = []
    witnesses = [0] * 729  # 0 only for inputs whose support does not have weight six.
    for support, ns in sorted(ternary_hexads.items(), key=lambda item: sorted(item[0])):
        image = frozenset(ambient_chart[i] for i in support)
        m = residual_to_message[image]
        for n in ns:
            witnesses[n] = m
            assert all_binary[m] & dodecad == image
        table.append({
            "ternary_support": sorted(support),
            "ternary_message_indices": ns,
            "image_support": sorted(image),
            "binary_message": m,
            "binary_word_integer": binary_encode(m),
            "binary_octad_support": sorted(all_binary[m]),
        })

    # Stress checks distinguish this chart from an arbitrary bijection.
    wrong = list(ambient_chart)
    wrong[0], wrong[1] = wrong[1], wrong[0]
    wrong_images = {frozenset(wrong[i] for i in s) for s in ternary_hexads}
    assert wrong_images != set(residual_to_message)
    changed = sum(1 for n in range(729)
                  if len(ternary_support(n)) == 6 and
                  frozenset(ambient_chart[i] for i in ternary_support(n)) !=
                  (all_binary[(witnesses[n] + 1) % 4096] & dodecad))
    assert changed > 0

    return {
        "status": "PASS_EXPLICIT_132_HEXAD_DODECAD_CHART",
        "classification": "CERTIFICADO_NUEVO of an existing manuscript realization chart",
        "scope": "Exact finite enumeration, not a Lean kernel proof or an FLM/Moonshine theorem",
        "sources": [{"path": str(p), "sha256": sha256(p), "lines": loc} for p, loc in SOURCES],
        "generator_script_sha256": sha256(Path(__file__)),
        "ternary_index_encoding": "w(i) = (n // 3**i) % 3, i=0..5; word=(w,w*AW mod 3)",
        "ternary_matrix": AW,
        "binary_generator_hex": hex(GENERATOR),
        "binary_encoding": "XOR_i bit_i(message)*(0xAE3 << i), parity appended at coordinate 23",
        "dodecad_message": DODECAD_MESSAGE,
        "dodecad_support": dcoords,
        "local_chart": LOCAL_CHART,
        "ambient_chart": ambient_chart,
        "ternary_words": 729,
        "ternary_weight_six_words": 264,
        "distinct_ternary_hexads": 132,
        "distinct_binary_residual_hexads": 132,
        "full_support_set_equality": True,
        "unique_binary_octad_lift_per_hexad": True,
        "wrong_chart_falsified": True,
        "wrong_witness_falsified_on_count": changed,
        "witness_729_nonhexad_sentinel": 0,
        "binary_message_witnesses_729": witnesses,
        "hexad_table": table,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = certificate()
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
        path = args.output / "incidence_chart_132.json"
        path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        witnesses = result["binary_message_witnesses_729"]
        literal = "![\n" + ",\n".join(
            "  " + ", ".join(map(str, witnesses[i:i + 18]))
            for i in range(0, len(witnesses), 18)) + "]\n"
        (args.output / "binary_witnesses_729.lean-fragment.txt").write_text(literal, encoding="utf-8")
        print("certificate_sha256=" + sha256(path))
    print(result["status"])
    print("132 source hexads = 132 residual hexads; all 264 signed hexad words lifted")
    print("ambient_chart=" + str(result["ambient_chart"]))


if __name__ == "__main__":
    main()
