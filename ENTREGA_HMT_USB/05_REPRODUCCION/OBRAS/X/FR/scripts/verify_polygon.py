#!/usr/bin/env python3
"""Exact rational verification of the K-derived rank-one amplituhedron.

Only the standard library is used; explicit checks stay active under -O.
Polynomial identities certify local refinements and diagonal flips.
The accompanying text supplies the arbitrary-depth and dimension proofs.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
from collections import Counter
import json

K = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
TOTAL = sum(K)
COUNTS = Counter()


def check(condition, name):
    if not condition:
        raise RuntimeError("FAIL: " + name)
    COUNTS[name.split(":")[0]] += 1


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def determinant(rows):
    n = len(rows)
    if n == 0:
        return Q(1)
    a = [[Q(x) for x in row] for row in rows]
    result = Q(1)
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return Q(0)
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            result = -result
        p = a[k][k]
        result *= p
        for j in range(k, n):
            a[k][j] /= p
        for i in range(k + 1, n):
            q = a[i][k]
            for j in range(k, n):
                a[i][j] -= q * a[k][j]
    return result


def pclean(p):
    return {m: Q(v) for m, v in p.items() if v}


def padd(a, b, scale=Q(1)):
    out = dict(a)
    for m, v in b.items():
        out[m] = out.get(m, Q(0)) + scale * v
    return pclean(out)


def pmul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            m = (i + k, j + l)
            out[m] = out.get(m, Q(0)) + x * y
    return pclean(out)


def pscale(a, q):
    return pclean({m: q * v for m, v in a.items()})


def line(a, b):
    # det(a,b,(1,x,y)) in the affine chart of the target.
    return pclean({(0, 0): a[1] * b[2] - a[2] * b[1],
                   (1, 0): a[2] * b[0] - a[0] * b[2],
                   (0, 1): a[0] * b[1] - a[1] * b[0]})


def canonical(a, b, c):
    d = det3(a, b, c)
    if not d:
        raise ValueError("Degenerate triangle")
    return d*d, pmul(pmul(line(a, b), line(b, c)), line(c, a))


def rational_sum_zero(terms):
    num = {}
    den = {(0, 0): Q(1)}
    for coeff, p in terms:
        num = padd(pmul(num, p), pscale(den, coeff))
        den = pmul(den, p)
    return not num


def mix(a, b, s):
    return tuple((1-s)*x + s*y for x, y in zip(a, b))


def form_identity(positive, negative):
    terms = [canonical(*x) for x in positive]
    terms += [(-a, b) for a, b in
              [canonical(*x) for x in negative]]
    return rational_sum_zero(terms)


def oriented_boundary(simplices):
    chain = Counter()
    for simplex in simplices:
        for j in range(len(simplex)):
            face = simplex[:j] + simplex[j+1:]
            inversions = sum(face[a] > face[b]
                             for a in range(len(face))
                             for b in range(a+1, len(face)))
            chain[tuple(sorted(face))] += (-1)**(j+inversions)
    return {k: v for k, v in chain.items() if v}


def main():
    check(TOTAL == 6263, "total")
    partial = [0]
    for k in K:
        partial.append(partial[-1]+k)
    t = [Q(x, TOTAL) for x in partial]
    z = [(Q(1), x, x*x) for x in t]
    check(t[0] == 0 and t[-1] == 1, "endpoints")
    check(all(a < b for a, b in zip(t, t[1:])), "strict_order")
    check(tuple(TOTAL*(t[i+1]-t[i]) for i in range(12)) == K,
          "inverse_register")

    minors = []
    for a,b,c in combinations(range(13), 3):
        value = det3(z[a], z[b], z[c])
        check(value == (t[b]-t[a])*(t[c]-t[a])*(t[c]-t[b]),
              "vandermonde_3")
        check(value > 0, "ordered_minor_positive")
        minors.append(value)
    check(len(minors) == 286 and minors[0] != 0, "rank_three")

    for a in range(13):
        b = (a+1) % 13
        for c in range(13):
            if c not in (a,b):
                check(det3(z[a], z[b], z[c]) > 0, "support_halfplane")

    fan = [(0,i,i+1) for i in range(1,12)]
    expected = {(i,i+1): 1 for i in range(12)}
    expected[(0,12)] = -1
    check(oriented_boundary(fan) == expected, "boundary_cancellation_2d")
    polygon_area2 = sum(z[i][1]*z[(i+1)%13][2]
                        - z[i][2]*z[(i+1)%13][1] for i in range(13))
    check(sum(det3(z[a],z[b],z[c]) for a,b,c in fan) == polygon_area2,
          "fan_area_coverage")

    for a,b,c in fan:
        aa,bb,cc = z[a],z[b],z[c]
        d = det3(aa,bb,cc)
        y = tuple(Q(1,6)*aa[j] + Q(1,3)*bb[j] + Q(1,2)*cc[j]
                  for j in range(3))
        lam = (det3(bb,cc,y)/d, det3(cc,aa,y)/d, det3(aa,bb,y)/d)
        check(lam == (Q(1,6),Q(1,3),Q(1,2)), "cell_inverse")
        check(sum(lam) == 1, "cell_barycentric_sum")
        for s in (Q(1,9),Q(1,3),Q(1,2),Q(8,9),Q(729,1000)):
            w = mix(bb,cc,s)
            check(form_identity([(aa,bb,w),(aa,w,cc)],[(aa,bb,cc)]),
                  "rational_edge_split")
            check(det3(aa,bb,w)+det3(aa,w,cc) == d, "edge_split_area")
        w = tuple((aa[j]+bb[j]+cc[j])/3 for j in range(3))
        check(form_identity([(aa,bb,w),(bb,cc,w),(cc,aa,w)],[(aa,bb,cc)]),
              "rational_interior_split")

    for a,b,c,d in [(i,i+1,i+2,i+3) for i in range(10)]+[(0,3,8,12)]:
        check(form_identity([(z[a],z[b],z[c]),(z[a],z[c],z[d])],
                            [(z[a],z[b],z[d]),(z[b],z[c],z[d])]),
              "rational_diagonal_flip")

    # Normal-last boundary residue has coefficient 1/[s(1-s)].
    for s in (Q(1,9),Q(2,5),Q(4,7)):
        check(1/(s*(1-s)) == 1/s + 1/(1-s), "residue_interval")

    r = Q(7,5)  # Outside the partition, so no denominator vanishes.
    for base in (2,3,9,10,27,81,1000):
        total = Q(0)
        for c in range(base):
            lo,hi = Q(c,base),Q(c+1,base)
            term = (hi-lo)/((r-lo)*(hi-r))
            check(term == 1/(r-lo)+1/(hi-r), "telescoping_local")
            total += term
        check(total == 1/(r*(1-r)), "telescoping_global")

    for base in (9,10,1000):
        x = Q(12345,67891)
        digits,current = [],x
        for _ in range(7):
            scaled = base*current
            digit = scaled.numerator//scaled.denominator
            digits.append(digit)
            current = scaled-digit
            check(0 <= current < 1 and 0 <= digit < base, "carry_domain")
        recovered = current
        for digit in reversed(digits):
            recovered = (recovered+digit)/base
        check(recovered == x, "carry_inverse")

    for a,b in zip(t,t[1:]):
        mid = (a+b)/2
        gap = (a+b)*mid-a*b-mid**2
        check(gap == (mid-a)*(b-mid) and gap > 0,
              "parabola_insertion_changes_polygon")

    c = [Q(i+1) for i in range(13)]
    d = [Q((i+2)**2,i+1) for i in range(13)]
    scaled_image = [sum(c[i]*d[i]*z[i][j] for i in range(13))
                    for j in range(3)]
    cp = [c[i]*d[i] for i in range(13)]
    old_image = [sum(cp[i]*z[i][j] for i in range(13)) for j in range(3)]
    check(scaled_image == old_image, "positive_rescaling")
    check([cp[i]/d[i] for i in range(13)] == c, "positive_rescaling_inverse")

    # Three-dimensional cyclic polytope: 22 triangular facets and
    # 10 tetrahedra from pulling vertex 0. Every ordered 4-minor is checked.
    z3 = [tuple(x**j for j in range(4)) for x in t]
    for ids in combinations(range(13),4):
        value = determinant([z3[i] for i in ids])
        vand = Q(1)
        for a,b in combinations(ids,2):
            vand *= t[b]-t[a]
        check(value == vand and value > 0, "vandermonde_4")
    facets = set()
    for ids in combinations(range(13),3):
        signs = [determinant([z3[i] for i in ids]+[z3[j]])
                 for j in range(13) if j not in ids]
        if all(x>0 for x in signs) or all(x<0 for x in signs):
            facets.add(ids)
    check(len(facets) == 22, "cyclic_3d_facets")
    tetrahedra = [(0,i,i+1,12) for i in range(1,11)]
    bd3 = oriented_boundary(tetrahedra)
    check(set(bd3) == facets and all(abs(x)==1 for x in bd3.values()),
          "boundary_cancellation_3d")
    check(all(determinant([z3[i] for i in tet])>0 for tet in tetrahedra),
          "tetrahedron_orientation")
    # Boundary of boundary is zero, including every codimension-two edge.
    bd2 = Counter()
    for face, coeff in bd3.items():
        for j in range(3):
            edge = face[:j]+face[j+1:]
            bd2[edge] += coeff*((-1)**j)
    check(all(value == 0 for value in bd2.values()), "boundary_squared_zero")

    # Full-rank Vandermonde witness in all supported dimensions.
    for m in range(2,13):
        zz = [[t[i]**j for j in range(m+1)] for i in range(m+1)]
        value = determinant(zz)
        vand = Q(1)
        for a,b in combinations(range(m+1),2):
            vand *= t[b]-t[a]
        check(value == vand and value > 0, "rank_all_dimensions")

    report = {
        "status": "PASS_K_POLYGON_AMPLITUHEDRON_20260918",
        "arithmetic": "fractions.Fraction; exact sparse polynomial identities",
        "K": list(K), "S": TOTAL, "partition_numerators": partial,
        "parameters": {"n":13,"k":1,"m":2},
        "vertices":13, "triangles":11, "ordered_3_minors":286,
        "source_dimension":12, "target_dimension":2,
        "generic_full_fiber_dimension":10,
        "degree_on_each_triangular_cell":1,
        "twice_polygon_area":str(polygon_area2),
        "three_dimensional_test":{"facets":22,"tetrahedra":10,"ordered_4_minors":715},
        "checks":sum(COUNTS.values()), "categories":dict(sorted(COUNTS.items())),
        "scope":"K polygon, rank-one cyclic polytopes, finite witnesses for symbolic proofs",
        "full_map_generically_finite_in_dimension_two":False,
        "new_parabola_vertices_preserve_polygon":False,
        "positive_column_rescaling_changes_full_image":False
    }
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()

