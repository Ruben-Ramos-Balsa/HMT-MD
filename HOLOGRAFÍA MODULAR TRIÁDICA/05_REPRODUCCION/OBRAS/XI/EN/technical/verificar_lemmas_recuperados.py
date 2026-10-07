#!/usr/bin/env python3
"""Instancias finitas exactas para los lemas incorporados al artículo.

Las ejecuciones acompañan las pruebas simbólicas; no las sustituyen.
"""

from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise SystemExit("FAIL_INSTANCIAS_RECUPERADAS " + reason)


# Matriz unimodular A=((1,1),(0,1)), vectores fila, p=3.
checked = 0
for depth in range(1, 5):
    modulus = 3**depth
    images = set()
    for initial in product(range(modulus), repeat=2):
        state, word = initial, []
        for _ in range(depth):
            lifted = (state[0], state[0] + state[1])
            digit = tuple(value % 3 for value in lifted)
            word.append(digit)
            state = tuple((value - residue) // 3
                          for value, residue in zip(lifted, digit))
        backward = (0, 0)
        for digit in reversed(word):
            lifted = tuple(residue + 3 * tail
                           for residue, tail in zip(digit, backward))
            backward = (lifted[0], lifted[1] - lifted[0])
        require(tuple(value % modulus for value in backward) == initial,
                "hensel_inverse")
        require(tuple(word) not in images, "hensel_emission_not_injective")
        images.add(tuple(word))
        checked += 1
    require(len(images) == modulus**2, "hensel_count")


def pair(left: int, right: int) -> int:
    return (left + right) * (left + right + 1) // 2 + right


def order_code(domain, relation):
    return {2 * value for value in domain} | {
        2 * pair(left, right) + 1 for left, right in relation
    }


require(order_code([], []) != order_code([0], []), "empty_singleton_order")

states = list(range(27))
enriched = {(state % 3, state // 3): state for state in states}
require(len(enriched) == len(states), "enriched_reader_not_injective")
require(len({state % 3 for state in states}) < len(states),
        "residual_reader_unexpectedly_injective")

# Certificado combinatorio de seis trisecciones registradas. La palabra
# ordenada, no la suma de sus dígitos, separa los 729 bloques.
branch_ledgers = {
    branch: tuple((phase, branch, phase == 9)
                  for phase in range(1, 10))
    for branch in (-1, 0, +1)
}
block_ledgers = {
    tuple(entry for branch in word for entry in branch_ledgers[branch])
    for word in product((-1, 0, +1), repeat=6)
}
require(len(block_ledgers) == 729, "registered_block_count")
require(all(len(ledger) == 54 for ledger in block_ledgers),
        "registered_block_length")

source = (ROOT / "sections" / "ch_tres_vueltas_ext.tex").read_text(
    encoding="utf-8"
)
require(r"\mathcal U^{(1),\rm cal}_{e_{\varepsilon,n,r}}" in source,
        "calibrated_transition_graph_missing")
require(r"\mathfrak T_{\rm TPK}^{\rm cal}" in source,
        "calibrated_tpk_model_missing")
require(r"\operatorname{Ext}^{\APP,\rm cal}" in source,
        "app_extension_missing")
require(r"\operatorname{Ext}^{\rm fib,cal}" in source,
        "fiber_extension_missing")

elevation = (ROOT / "sections" / "ch_elevacion_catalogal.tex").read_text(
    encoding="utf-8"
)
require(r"\Phi_N:=\Psi_N^{-1}\circ\beta_{{\rm blk},N}" in elevation,
        "multilevel_hensel_intertwiner_missing")
require(r"\pi_{N+1,N}\circ\Phi_{N+1}" in elevation,
        "hensel_truncation_identity_missing")
require(r"\mathscr Z_N(x)" in elevation,
        "actual_limit_cylinder_missing")
require(r"\bigsqcup_{b\in\mathbb F_3^6}" in elevation,
        "disjoint_729_partition_missing")

print(
    "PASS_INSTANCIAS_RECUPERADAS "
    f"hensel_instances={checked} order_codes=distinct "
    "enriched_reader=injective ext_local_entries=27 "
    "ext_block_edges=54 ext_block_ledgers=729 "
    "proof_status=manuscript_not_replaced_by_execution"
)
