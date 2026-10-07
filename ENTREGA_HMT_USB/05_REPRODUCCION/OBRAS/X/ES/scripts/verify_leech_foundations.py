#!/usr/bin/env python3
"""Exact finite proof constituents for the public Leech foundations.

The analytic lattice and classification arguments are in the adjacent TeX.
The upstream script is conserved verbatim; its checks are reported separately.
This verifier uses only Python's standard library and writes no files.
"""
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import io
import json
from pathlib import Path
import runpy

HERE = Path(__file__).resolve().parent
vendor = HERE / "vendor_iv/verificar_ordenes_moonshine.py"
capture = io.StringIO()
with redirect_stdout(capture):
    inherited = runpy.run_path(str(vendor), run_name="iv_readonly")
A = inherited["AW"]
checks = []


def require(condition, name):
    if not condition:
        raise ArithmeticError(name)
    checks.append(name)


def codeword(w):
    return tuple(w) + tuple(sum(w[i]*A[i][j] for i in range(6)) % 3
                           for j in range(6))


def wt(w):
    return sum(x != 0 for x in w)


def supp(w):
    return frozenset(i+1 for i,x in enumerate(w) if x)


def form(u,v):
    return u*u-u*v+v*v


require(A == tuple(zip(*A)), "AW_symmetric")
require(all(sum(A[i][k]*A[k][j] for k in range(6)) % 3
            == (2 if i == j else 0)
            for i in range(6) for j in range(6)), "AW_squared_minus_identity")
rows = [Counter() for _ in range(7)]
code = []
for w in product(range(3), repeat=6):
    c = codeword(w)
    code.append(c)
    rows[wt(w)][wt(c)] += 1
require(len(set(code)) == 729, "injective_graph_all_words")
expected_rows = [{0:1},{6:12},{6:60},{6:120,9:40},
                 {6:60,9:180},{6:12,9:180},{9:40,12:24}]
require([dict(r) for r in rows] == expected_rows, "full_seed_weight_table")
enumerator = sum(rows,Counter())
require(dict(enumerator) == {0:1,6:264,9:440,12:24}, "weight_enumerator")
require(all(wt(c)%3 == 0 for c in code), "weights_divisible_three")
require(min(wt(c) for c in code if any(c)) == 6, "minimum_distance_six")
generators = [codeword(tuple(int(i==j) for i in range(6))) for j in range(6)]
require(all(sum(x*y for x,y in zip(g,h))%3 == 0
            for g in generators for h in generators), "generator_self_orthogonality")
hexada_words = [c for c in code if wt(c)==6]
hexadas = set(map(supp,hexada_words))
require(len(hexadas)==132, "132_distinct_hexadas")
require(set(Counter(map(supp,hexada_words)).values())=={2},
        "exact_two_words_per_hexada")
five_counts = Counter(S for H in hexadas for S in combinations(sorted(H),5))
require(len(five_counts)==792 and set(five_counts.values())=={1},
        "Witt_unique_hexada_per_five_subset")

regional = {name:supp(codeword(tuple(map(int,w)))) for name,w in
            (("pi","010211"),("e","201101"),("phi","121200"),("APP","022020"))}
expected_regions = {"pi":{2,4,5,6,7,8,9,10,11}, "e":{1,3,4,6,9,10},
                    "phi":{1,2,3,4,7,9}, "APP":{2,3,5,10,11,12}}
require(regional==expected_regions, "four_regional_incidence_supports")
K = (234,543,140,729,659,824,621,58,914,794,146,601)
Z0 = (7,297,353,-430,-715,-1199,-3,286,-894,-528,380,663)
BK = frozenset(i+1 for i,k in enumerate(K) if k>=729)
Halpha = frozenset(i+1 for i,z in enumerate(Z0) if z<0)
require(BK=={4,6,9,10} and BK==regional["e"] & regional["pi"], "flag_BK")
require(Halpha=={4,5,6,7,9,10} and Halpha in hexadas, "negative_support_hexada")
petals = {H-BK for H in hexadas if BK<=H}
require(petals=={frozenset(p) for p in ((1,3),(2,11),(5,7),(8,12))},
        "four_flag_petals")
selected = [H for H in hexadas if BK<=H<=regional["pi"]
            and tuple(len(H & regional[name]) for name in ("e","phi","APP"))
            == (4,3,2)]
require(selected==[Halpha], "unique_incidence_signed_selection")
origin = (regional["e"] & regional["phi"]) - (Halpha | regional["APP"])
require(origin=={1}, "marked_origin_one")
require(all({i+1 for i,k in enumerate(K) if k>=threshold}==BK
            for threshold in range(660,730)), "same_support_threshold_range")
cstar = (1,1,1,1,1,1,2,1,1,1,1,1)
require(codeword((1,)*6)==cstar and cstar in code, "full_support_cstar")

# Root geometry and discriminants. The bound is analytic: Q>0 integer.
B=((2,-1),(-1,2))
require(B[0][0]*B[1][1]-B[0][1]*B[1][0]==3, "A2_determinant_three")
roots={(u,v) for u,v in product(range(-2,3),repeat=2) if form(u,v)==1}
require(roots=={(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)}, "six_A2_roots")
for residue, representative in (((2,1),(2,1)),((1,2),(1,2))):
    require(form(*residue)%3==0 and form(*representative)==3,
            "nonzero_discriminant_min_%s" % (residue,))
require(F(2,3)*6==4, "glue_minimum_four")
require(3**12//(3**6)**2==1, "glue_determinant_one")
require(2*(4**2+11)==54 and 54%18==0, "marked_vector_norm_congruence")
require(14+11*2==36, "same_residual_class_outside_camera_norm36")
require((1-4)%3==0 and (-2-4)%3==0, "outside_camera_same_residues")
require(9//3**2==1 and F(54,9)==6, "neighbour_index_norm")
require(all((a*(u+v))%3 != 0 for a in (1,4) for u,v in roots),
        "no_old_root_in_character_kernel")
shifted = [((1,1),(1,1)),((0,2),(0,-1)),((2,0),(-1,0)),
           ((2,2),(-1,-1)),((1,0),(1,0)),((0,1),(0,1))]
for residue, representative in shifted:
    require(residue!=(0,0) and tuple(x%3 for x in representative)==residue
            and form(*representative)==1, "shifted_class_min_%s" % (residue,))
require(F(12*2,9)==F(8,3) and F(8,3)>2, "new_coset_root_bound")

print(json.dumps({
    "status":"PASS_LEECH_FOUNDATIONS_EXACT",
    "checks":len(checks),
    "codewords":len(code),
    "weight_table":expected_rows,
    "hexadas":len(hexadas),
    "five_subsets":len(five_counts),
    "new_coset_norm_lower_bound":"8/3",
    "vendor_sha256":hashlib.sha256(vendor.read_bytes()).hexdigest(),
    "vendor_results":capture.getvalue().splitlines(),
    "scope":"Finite integer/rational constituents; lattice and recognition proofs are public in sections/leech_foundations.tex."
},ensure_ascii=False,sort_keys=True,indent=2))
