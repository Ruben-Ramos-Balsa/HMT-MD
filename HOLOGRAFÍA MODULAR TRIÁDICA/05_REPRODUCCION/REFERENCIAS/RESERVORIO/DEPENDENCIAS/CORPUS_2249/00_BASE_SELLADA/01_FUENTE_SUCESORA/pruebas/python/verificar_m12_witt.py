"""Recalcula W12, sus estrellas y el grupo generado, sin usar el JSON legado."""
from __future__ import annotations
import itertools
import json
from collections import deque
from pathlib import Path
AW = ((0, 1, 1, 1, 1, 1), (1, 0, 1, 2, 2, 1), (1, 1, 0, 1, 2, 2), (1, 2, 1, 0, 1, 2), (1, 2, 2, 1, 0, 1), (1, 1, 2, 2, 1, 0))
K = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
P_TRIADS = (141, 592, 653, 589, 793, 238, 462, 643, 383, 279, 502, 884)
E_TRIADS = (718, 281, 828, 459, 45, 235, 360, 287, 471, 352, 662, 497)
PHI_TRIADS = (618, 33, 988, 749, 894, 848, 204, 586, 834, 365, 638, 117)
CHANNEL_WORDS = {'P_pi': (0, 1, 0, 2, 1, 1), 'H_e': (2, 0, 1, 1, 0, 1), 'H_phi': (1, 2, 1, 2, 0, 0), 'H_APP': (0, 2, 2, 0, 2, 0)}
IDENTITY = tuple(range(12))

def codeword(q: tuple[int, ...]) -> tuple[int, ...]:
    right = tuple((sum((q[i] * AW[i][j] for i in range(6))) % 3 for j in range(6)))
    return q + right

def witt_hexads() -> set[frozenset[int]]:
    supports: set[frozenset[int]] = set()
    weight_enumerator: dict[int, int] = {}
    for q in itertools.product(range(3), repeat=6):
        w = codeword(q)
        support = frozenset((i for (i, x) in enumerate(w) if x))
        weight_enumerator[len(support)] = weight_enumerator.get(len(support), 0) + 1
        if len(support) == 6:
            supports.add(support)
    if not weight_enumerator == {0: 1, 6: 264, 9: 440, 12: 24}:
        raise AssertionError('comprobación ejecutable fallida')
    if not len(supports) == 132:
        raise AssertionError('comprobación ejecutable fallida')
    return supports

def star_involution(face: frozenset[int], hexads: set[frozenset[int]]) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]]:
    containing = [h for h in hexads if face <= h]
    if not len(containing) == 4:
        raise AssertionError('comprobación ejecutable fallida')
    pairs = tuple((tuple(sorted(h - face)) for h in containing))
    if not all((len(pair) == 2 for pair in pairs)):
        raise AssertionError('comprobación ejecutable fallida')
    if not set().union(*(set(pair) for pair in pairs)) == set(range(12)) - set(face):
        raise AssertionError('comprobación ejecutable fallida')
    p = list(IDENTITY)
    for (a, b) in pairs:
        (p[a], p[b]) = (b, a)
    return (tuple(p), tuple(sorted(pairs)))

def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """p after q."""
    return tuple((p[q[i]] for i in range(12)))

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
            raise AssertionError('El grupo excede el orden de Aut(W12).')
    return group

def image_set(p: tuple[int, ...], s: frozenset[int]) -> frozenset[int]:
    return frozenset((p[i] for i in s))

def one_based(items: frozenset[int] | tuple[int, ...]) -> list[int]:
    return [i + 1 for i in sorted(items)]

def audit() -> dict[str, object]:
    hexads = witt_hexads()
    channel_supports = {name: frozenset((i for (i, x) in enumerate(codeword(q)) if x)) for (name, q) in CHANNEL_WORDS.items()}
    if not len(channel_supports['P_pi']) == 9:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((len(channel_supports[name]) == 6 for name in ('H_e', 'H_phi', 'H_APP'))):
        raise AssertionError('comprobación ejecutable fallida')
    stars: list[tuple[frozenset[int], tuple[int, ...], tuple[tuple[int, int], ...]]] = []
    for raw_face in itertools.combinations(range(12), 4):
        face = frozenset(raw_face)
        (sigma, pairs) = star_involution(face, hexads)
        if not all((image_set(sigma, h) in hexads for h in hexads)):
            raise AssertionError('comprobación ejecutable fallida')
        stars.append((face, sigma, pairs))
    generators: list[tuple[int, ...]] = []
    generator_faces: list[list[int]] = []
    group: set[tuple[int, ...]] = {IDENTITY}
    order_chain = [1]
    for (face, sigma, _pairs) in stars:
        if sigma not in group:
            generators.append(sigma)
            generator_faces.append(one_based(face))
            group = closure(generators)
            order_chain.append(len(group))
    if not len(stars) == 495:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((sigma in group for (_face, sigma, _pairs) in stars)):
        raise AssertionError('comprobación ejecutable fallida')
    if not len(group) == 95040:
        raise AssertionError('comprobación ejecutable fallida')
    raw_alpha = tuple((p + e - phi - k for (p, e, phi, k) in zip(P_TRIADS, E_TRIADS, PHI_TRIADS, K)))
    h_alpha = frozenset((i for (i, value) in enumerate(raw_alpha) if value < 0))
    h_e = channel_supports['H_e']
    h_phi = channel_supports['H_phi']
    h_app = channel_supports['H_APP']
    frame = (h_alpha, h_e, h_phi, h_app)
    if not all((h in hexads for h in frame)):
        raise AssertionError('comprobación ejecutable fallida')
    threshold = 729
    b_k = frozenset((i for (i, value) in enumerate(K) if value >= threshold))
    if not b_k == h_e & channel_supports['P_pi']:
        raise AssertionError('comprobación ejecutable fallida')
    if not h_alpha == b_k | frozenset((i - 1 for i in (5, 7))):
        raise AssertionError('comprobación ejecutable fallida')
    same_support_thresholds = [candidate for candidate in range(1000) if frozenset((i for (i, value) in enumerate(K) if value >= candidate)) == b_k]
    if not same_support_thresholds == list(range(660, 730)):
        raise AssertionError('comprobación ejecutable fallida')
    selected_hexads = [h for h in hexads if b_k <= h <= channel_supports['P_pi'] and (len(h & h_e), len(h & h_phi), len(h & h_app)) == (4, 3, 2)]
    if not selected_hexads == [h_alpha]:
        raise AssertionError('comprobación ejecutable fallida')
    frame_stabilizer = [p for p in group if all((image_set(p, h) == h for h in frame))]
    if not len(frame_stabilizer) == 1:
        raise AssertionError('comprobación ejecutable fallida')
    (sigma_bk, pairs_bk) = star_involution(b_k, hexads)
    if not sigma_bk in group:
        raise AssertionError('comprobación ejecutable fallida')
    return {'schema': 'HMT.M12_Witt.v1', 'status': 'PASS', 'weight_6_supports': len(hexads), 'four_faces': len(stars), 'all_star_involutions_preserve_W12': True, 'generated_group_order': len(group), 'classical_identification': 'Aut(S(5,6,12)) is M12', 'small_generating_set_size': len(generators), 'small_generating_faces_1based': generator_faces, 'order_chain': order_chain, 'HMT_selected_face_BK_1based': one_based(b_k), 'HMT_threshold_calibration': {'declared_threshold': threshold, 'all_integer_thresholds_with_same_support': same_support_thresholds, 'threshold_is_identified_by_support_equality': False}, 'HMT_selected_star_pairs_1based': [[a + 1, b + 1] for (a, b) in pairs_bk], 'ordered_HMT_frame_stabilizer': len(frame_stabilizer), 'exact_contacts': {'B_K_equals_H_e_intersection_P_pi': True, 'H_alpha_equals_B_K_union_negative_pair': True, 'calibrated_4_3_2_selector_has_unique_hexad': True}, 'channel_supports_1based': {name: one_based(support) for (name, support) in channel_supports.items()}, 'logical_scope': {'proved': 'The global field of all 495 Witt stars generates M12; the declared words, K, threshold and selector produce the displayed frame.', 'not_proved': 'independent provenance of K, the words, threshold 729 or the intersection selector; no chance probability is assigned'}}
if __name__ == '__main__':
    result = audit()
    target = Path(__file__).resolve().parents[2] / 'certificados/m12_witt.json'
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))
