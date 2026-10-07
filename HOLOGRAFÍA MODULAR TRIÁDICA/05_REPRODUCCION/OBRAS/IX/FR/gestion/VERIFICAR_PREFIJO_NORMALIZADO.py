#!/usr/bin/env python3
"""Control exacto de la composición del prefijo; no prueba de admisibilidad."""

import json
import runpy
from pathlib import Path


root = Path(__file__).resolve().parents[1]
native = runpy.run_path(str(root / "fuente/pruebas/python/a9_native.py"))
encode = native["encode_bijective9"]
value = native["word_value"]
add = native["add_words"]
product = native["native_product_words"]
base = encode(729)
checks = 0

for n in range(33):
    parent = encode(n)
    shifted = product(base, parent)
    for block in range(729):
        child = add(shifted, encode(block))
        expected = 729 * n + block
        assert value(child) == expected
        assert child == encode(expected)
        recovered_parent = encode(value(child) // 729)
        recovered_block = value(child) % 729
        assert recovered_parent == parent
        assert recovered_block == block
        checks += 1

assert value(base) == 729
assert tuple(base) == (9, 8, 8)
assert tuple(base)[3:] != tuple(encode(1))
print(json.dumps({
    "status": "PASS_COMPOSICION_PREFIJO_NORMALIZADO",
    "prefix_block_pairs": checks,
    "prefix_range": [0, 32],
    "block_range": [0, 728],
    "arithmetic": "exact_integer",
    "negative_control": "Deleting three bijective digits does not equal quotient by 729.",
    "scope": "Composition of previously defined native sum/product and prefix update.",
    "not_certified": [
        "Admissibility of every tested pair as a generated regional TPK state",
        "Recovery of the full state from a single numerical prefix",
        "Global identification of tree depth k and block depth K",
        "Weil moments or RH"
    ]
}, ensure_ascii=False, indent=2))
