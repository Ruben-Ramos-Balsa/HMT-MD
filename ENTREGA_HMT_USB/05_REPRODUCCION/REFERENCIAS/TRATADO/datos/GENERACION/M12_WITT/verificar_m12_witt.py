#!/usr/bin/env python3
"""Recalcula W12, sus estrellas y el grupo generado, sin usar el JSON legado."""

from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path


AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)

IDENTITY = tuple(range(12))


def codeword(q: tuple[int, ...]) -> tuple[int, ...]:
    right = tuple(
        sum(q[i] * AW[i][j] for i in range(6)) % 3 for j in range(6)
    )
    return q + right


def witt_hexads() -> set[frozenset[int]]:
    supports: set[frozenset[int]] = set()
    weight_enumerator: dict[int, int] = {}
    for q in itertools.product(range(3), repeat=6):
        w = codeword(q)
        support = frozenset(i for i, x in enumerate(w) if x)
        weight_enumerator[len(support)] = weight_enumerator.get(len(support), 0) + 1
        if len(support) == 6:
            supports.add(support)
    assert weight_enumerator == {0: 1, 6: 264, 9: 440, 12: 24}
    assert len(supports) == 132
    return supports


def star_involution(
    face: frozenset[int], hexads: set[frozenset[int]]
) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]]:
    containing = [h for h in hexads if face <= h]
    assert len(containing) == 4
    pairs = tuple(tuple(sorted(h - face)) for h in containing)
    assert all(len(pair) == 2 for pair in pairs)
    assert set().union(*(set(pair) for pair in pairs)) == set(range(12)) - set(face)
    p = list(IDENTITY)
    for a, b in pairs:
        p[a], p[b] = b, a
    return tuple(p), tuple(sorted(pairs))


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """p after q."""
    return tuple(p[q[i]] for i in range(12))


def closure(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    group = {IDENTITY}
    queue: deque[tuple[int, ...]] = deque([IDENTITY])
    while queue:
        h = queue.popleft()
        for g in generators:
            gh = compose(g, h)
            if gh not in group:
                group.add(gh)
                queue.append(gh)
        if len(group) > 95040:
            raise AssertionError("El grupo excede el orden de Aut(W12).")
    return group


def image_set(p: tuple[int, ...], s: frozenset[int]) -> frozenset[int]:
    return frozenset(p[i] for i in s)


def one_based(items: frozenset[int] | tuple[int, ...]) -> list[int]:
    return [i + 1 for i in sorted(items)]


def audit() -> dict[str, object]:
    hexads = witt_hexads()

    expected_channel_supports = {
        "P_pi": frozenset(i - 1 for i in (2, 4, 5, 6, 7, 8, 9, 10, 11)),
        "H_e": frozenset(i - 1 for i in (1, 3, 4, 6, 9, 10)),
        "H_phi": frozenset(i - 1 for i in (1, 2, 3, 4, 7, 9)),
        "H_APP": frozenset(i - 1 for i in (2, 3, 5, 10, 11, 12)),
    }
    channel_words = {
        "P_pi": (0, 1, 0, 2, 1, 1),
        "H_e": (2, 0, 1, 1, 0, 1),
        "H_phi": (1, 2, 1, 2, 0, 0),
        "H_APP": (0, 2, 2, 0, 2, 0),
    }
    for name, q in channel_words.items():
        observed = frozenset(i for i, x in enumerate(codeword(q)) if x)
        assert observed == expected_channel_supports[name]
    stars: list[tuple[frozenset[int], tuple[int, ...], tuple[tuple[int, int], ...]]] = []
    for raw_face in itertools.combinations(range(12), 4):
        face = frozenset(raw_face)
        sigma, pairs = star_involution(face, hexads)
        assert all(image_set(sigma, h) in hexads for h in hexads)
        stars.append((face, sigma, pairs))

    generators: list[tuple[int, ...]] = []
    generator_faces: list[list[int]] = []
    group: set[tuple[int, ...]] = {IDENTITY}
    order_chain = [1]
    for face, sigma, _pairs in stars:
        if sigma not in group:
            generators.append(sigma)
            generator_faces.append(one_based(face))
            group = closure(generators)
            order_chain.append(len(group))

    assert len(stars) == 495
    assert all(sigma in group for _face, sigma, _pairs in stars)
    assert len(group) == 95040

    h_alpha = frozenset(i - 1 for i in (4, 5, 6, 7, 9, 10))
    h_e = frozenset(i - 1 for i in (1, 3, 4, 6, 9, 10))
    h_phi = frozenset(i - 1 for i in (1, 2, 3, 4, 7, 9))
    h_app = frozenset(i - 1 for i in (2, 3, 5, 10, 11, 12))
    frame = (h_alpha, h_e, h_phi, h_app)
    assert all(h in hexads for h in frame)
    b_k = frozenset(i - 1 for i in (4, 6, 9, 10))
    assert b_k == h_e & expected_channel_supports["P_pi"]
    assert h_alpha == b_k | frozenset(i - 1 for i in (5, 7))
    frame_stabilizer = [
        p for p in group if all(image_set(p, h) == h for h in frame)
    ]
    assert len(frame_stabilizer) == 1

    sigma_bk, pairs_bk = star_involution(b_k, hexads)
    assert sigma_bk in group

    return {
        "schema": "HMT.M12_Witt.repro.v2",
        "status": "PASS",
        "weight_6_supports": len(hexads),
        "four_faces": len(stars),
        "all_star_involutions_preserve_W12": True,
        "generated_group_order": len(group),
        "classical_identification": "Aut(S(5,6,12)) is M12",
        "small_generating_set_size": len(generators),
        "small_generating_faces_1based": generator_faces,
        "order_chain": order_chain,
        "HMT_selected_face_BK_1based": one_based(b_k),
        "HMT_selected_star_pairs_1based": [
            [a + 1, b + 1] for a, b in pairs_bk
        ],
        "ordered_HMT_frame_stabilizer": len(frame_stabilizer),
        "exact_contacts": {
            "B_K_equals_H_e_intersection_P_pi": True,
            "H_alpha_equals_B_K_union_negative_pair": True,
        },
        "channel_supports_1based": {
            name: one_based(support) for name, support in expected_channel_supports.items()
        },
        "logical_scope": (
            "The global field of all 495 Witt stars generates M12; "
            "HMT selects one star and an ordered frame."
        ),
    }


if __name__ == "__main__":
    result = audit()
    target = Path(__file__).with_name("verificacion_m12_witt.json")
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
