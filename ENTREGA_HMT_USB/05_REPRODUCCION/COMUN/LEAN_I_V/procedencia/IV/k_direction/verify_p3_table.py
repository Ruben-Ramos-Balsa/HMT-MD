#!/usr/bin/env python3
"""Read-only comparison of exact character-sum owner, table, and Lean table."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import runpy

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", type=Path, required=True,
                        help="Exact delivered propietarios_k_moonshine/variacional.py")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    data = json.loads((here / "P3_table.json").read_text())
    owner = args.owner.resolve()
    require(hashlib.sha256(owner.read_bytes()).hexdigest() == data["owner_sha256"],
            "owner SHA256 differs from the recorded source")
    v = runpy.run_path(str(owner), run_name="read_only_p3_owner")
    p = v["projector_three"]()
    d = data["denominator"]
    expected = [[(F(a,d), F(b,d)) for a,b in zip(ar,br)]
                for ar,br in zip(data["rational_numerator"],
                                  data["radical_numerator"])]
    require(p == expected, "A5 character sum does not equal the delivered table")
    p11 = [[(F(int(i==j))-F(1,12),F(0)) for j in range(12)] for i in range(12)]
    k = [(F(n),F(0)) for n in data["selected_K"]]
    u = v["matrix_vector"](p, v["matrix_vector"](p11,k))
    require(u == [(F(a,d),F(b,d)) for a,b in data["u_numerator"]],
            "P3 P11 K direction differs")
    require(v["dot"](u,u) == tuple(F(n,d) for n in data["norm_sq_numerator"]),
            "norm square differs")
    require(v["matmul"](p,p11) == p, "P3 P11 differs from P3")
    require(v["matmul"](p11,p) == p, "P11 P3 differs from P3")
    require(v["matmul"](p,p) == p, "P3 is not idempotent")
    require(v["transpose"](p) == p and v["rank"](p)==3,
            "P3 symmetry or rank differs")
    def entry(a,b):
        if b == 0:
            return str(a)
        require(a == 0 and abs(b)==1, "unexpected lean table encoding")
        return "s" if b==1 else "-s"
    body = ",\n".join("  ![" + ", ".join(entry(a,b) for a,b in zip(ar,br)) + "]"
                        for ar,br in zip(data["rational_numerator"],
                                          data["radical_numerator"]))
    expected_lean = ("def P3Numerator (s : ℝ) : Matrix (Fin 12) (Fin 12) ℝ := ![\n"
                     + body + "]")
    lean_text = (here / "SelectedKDirection.lean").read_text()
    require(expected_lean in lean_text, "Lean P3Numerator differs from verified table")
    require("fun i j => P3Numerator (Real.sqrt 5) i j / 20" in lean_text,
            "Lean P3 normalization differs")
    print("PASS_P3_CHARACTER_TABLE_AND_LEAN_TABLE")
    print("owner_sha256=" + data["owner_sha256"])
    print("table_sha256=" + hashlib.sha256((here / "P3_table.json").read_bytes()).hexdigest())
    print("character_sum_checked_in=Python exact Q(sqrt(5)); no Lean character-sum claim")
if __name__ == "__main__":
    main()

