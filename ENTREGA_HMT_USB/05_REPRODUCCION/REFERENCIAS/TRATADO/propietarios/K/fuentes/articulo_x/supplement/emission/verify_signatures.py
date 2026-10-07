"""Check the preserved emission signatures from the inherited recurrence.

Only the recurrence functions are imported. The historical main function,
which reads an external comparison catalog, is deliberately not invoked.
"""
from pathlib import Path
from collections import defaultdict, Counter
import importlib.util
import json
import hashlib

ROOT = Path(__file__).resolve().parent

def require(value, message):
    if not value:
        raise RuntimeError(message)

def main():
    spec = importlib.util.spec_from_file_location("emission_reference", ROOT / "verificar_catalogo_app.py")
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    witness = json.loads((ROOT / "FIRMAS_EMISION.json").read_text())
    seeds = [(i, j, d) for i in range(9) for j in range(9) for d in model.DIRS]
    images = {}
    for channel, key in (("plus", "plus_classes"), ("times", "times_classes")):
        actual = defaultdict(list)
        for identifier, seed in enumerate(seeds):
            actual[model.channel_signature(seed, channel)].append(identifier)
        expected = {tuple(row["signature"]): row["seed_ids_zero_based"] for row in witness[key]}
        require(dict(actual) == expected, channel + " full preimage mismatch")
        for row in witness[key]:
            require(len(actual[tuple(row["signature"])]) == row["multiplicity"], "multiplicity mismatch")
        images[channel] = actual
    counts = Counter()
    for sp in seeds:
        for st in seeds:
            value = model.combine(model.channel_signature(sp, "plus"), model.channel_signature(st, "times"))
            require(value == model.direct_u6(sp, st), "direct/factored emitter mismatch")
            counts[value] += 1
    require(len(counts) == 468, "emission cardinal")
    require(sum(counts.values()) == 104976, "initial-condition cardinal")
    require(len({model.w6(u) for u in counts}) == 243, "ternary image cardinal")
    report = {
        "status": "PASS_RESIDUAL_EMITTER_SIGNATURES",
        "initial_states_per_channel": len(seeds),
        "additive_signatures": len(images["plus"]),
        "multiplicative_signatures": len(images["times"]),
        "full_preimages_compared": 648,
        "direct_factored_pairs_compared": 104976,
        "emissions": len(counts),
        "ternary_images": 243,
        "scope": "Finite residual-emitter census only; no global coinductive or physical certification.",
        "reference_sha256": hashlib.sha256((ROOT / "verificar_catalogo_app.py").read_bytes()).hexdigest(),
        "witness_sha256": hashlib.sha256((ROOT / "FIRMAS_EMISION.json").read_bytes()).hexdigest(),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
