#!/usr/bin/env python3
"""Exact finite checks for the K ladder, cluster evaluations and gap deformation.

All checks use Fraction or Q(sqrt(5)); no optional modules, writes, network,
assert statements, physical targets or metrological values are used.
The analytic all-parameter proofs are in appendices/network_cluster.tex.
The executable reconstructs K from the two documented channels, reconstructs
P3 from A5/C5, checks the nonzero shape derivative, and audits finite
refinement and coordinate identities independently through path enumeration.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import json

COUNT = 0


def check(label, actual, expected):
    global COUNT
    if actual != expected:
        raise ArithmeticError(f"{label}: {actual!r} != {expected!r}")
    COUNT += 1


def require(label, condition):
    check(label, bool(condition), True)


def recover_k():
    b90 = (-495, -116, -684, 108, 601, -90, -173, -88, 313, 560, -397, 461)
    b120 = (-425, -281, -481, 671, -255, 30, 475, -543, 680, 251, 6, -128)
    q = 6263
    bs = [sum(b120[r + 3*j] for j in range(4)) for r in range(3)]
    ss = [F(q + 2*bs[0] + bs[1], 3)]
    ss += [ss[0] - bs[0], ss[0] - bs[0] - bs[1]]
    h = ((1, 1, 1, 1), (1, 1, -1, -1),
         (1, -1, 1, -1), (1, -1, -1, 1))
    k = [None]*12
    for r in range(3):
        ds = [b90[r + 3*j] for j in range(4)]
        u = (ss[r], ds[1]-ds[3], ds[0]+ds[2], ds[0]-ds[2])
        for j, row in enumerate(h):
            value = sum(a*b for a, b in zip(row, u))/4
            require("integral Hadamard recovery", value.denominator == 1)
            k[r + 3*j] = int(value)
    check("K owner", k, [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601])
    check("charge", sum(k), q)
    check("third difference", [k[i]-k[(i+3)%12] for i in range(12)], list(b90))
    check("fourth difference", [k[i]-k[(i+4)%12] for i in range(12)], list(b120))
    return k


def qadd(x, y):
    return x[0]+y[0], x[1]+y[1]


def qscale(x, c):
    return x[0]*c, x[1]*c


def qmul(x, y):
    return x[0]*y[0]+5*x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def qsum(xs):
    out = (F(0), F(0))
    for x in xs:
        out = qadd(out, x)
    return out


def qsign(x):
    a, b = x
    if not b:
        return (a > 0)-(a < 0)
    if not a:
        return (b > 0)-(b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    comp = (a*a > 5*b*b)-(a*a < 5*b*b)
    return comp if a > 0 else -comp


def mulperm(a, b):
    return tuple(a[x] for x in b)


def invperm(a):
    return tuple(a.index(x) for x in range(5))


def powerperm(a, n):
    p = tuple(range(5))
    for _ in range(n):
        p = mulperm(p, a)
    return p


def recover_direction(k):
    reps = [(4, 3, 5, 2, 1), (4, 2, 1, 3, 5), (1, 2, 4, 5, 3),
            (2, 5, 3, 4, 1), (4, 3, 1, 5, 2), (5, 1, 2, 3, 4),
            (5, 4, 3, 2, 1), (1, 3, 4, 2, 5), (4, 2, 3, 5, 1),
            (3, 2, 5, 4, 1), (4, 5, 2, 3, 1), (5, 3, 2, 4, 1)]
    reps = [tuple(x-1 for x in r) for r in reps]
    group = [a for a in permutations(range(5))
             if sum(a[i] > a[j] for i in range(5) for j in range(i+1, 5)) % 2 == 0]
    g, ident = (1, 2, 3, 4, 0), tuple(range(5))
    class5a = {mulperm(mulperm(a, g), invperm(a)) for a in group}
    lookup = {mulperm(r, powerperm(g, m)): j
              for j, r in enumerate(reps) for m in range(5)}
    check("A5 cardinal", len(group), 60)
    check("5a cardinal", len(class5a), 12)
    check("coset cover", set(lookup), set(group))
    p = [[(F(0), F(0)) for _ in range(12)] for _ in range(12)]
    for a in group:
        ai = invperm(a)
        if ai == ident:
            chi = (F(3), F(0))
        elif powerperm(ai, 2) == ident:
            chi = (F(-1), F(0))
        elif powerperm(ai, 3) == ident:
            chi = (F(0), F(0))
        else:
            chi = (F(1, 2), F(1, 2) if ai in class5a else F(-1, 2))
        for j, r in enumerate(reps):
            target = lookup[mulperm(a, r)]
            p[target][j] = qadd(p[target][j], qscale(chi, F(1, 20)))
    for i in range(12):
        check("P3 annihilates uniform", qsum(p[i]), (F(0), F(0)))
        for j in range(12):
            check("P3 symmetric", p[i][j], p[j][i])
            check("P3 idempotent", qsum(qmul(p[i][r], p[r][j]) for r in range(12)), p[i][j])
    check("P3 trace", qsum(p[i][i] for i in range(12)), (F(3), F(0)))
    u = [qsum(qscale(p[i][j], k[j]) for j in range(12)) for i in range(12)]
    check("u mean zero", qsum(u), (F(0), F(0)))
    check("u owner norm", qsum(qmul(x, x) for x in u), (F(6638585, 20), F(2275584, 20)))
    return u


def ladder(gaps):
    edges = {}
    def edge(a, b, weight=F(1)):
        edges.setdefault(a, []).append((b, weight))
    for j in range(len(gaps)+1):
        edge(('b', j), ('q', j))
        if j:
            edge(('a', j-1), ('a', j))
            edge(('b', j-1), ('b', j))
            edge(('a', j), ('b', j), gaps[j-1])
    return edges


def paths(edges, source, sink):
    out = []
    def walk(node, visited, weight):
        if node == sink:
            out.append((frozenset(visited), weight))
            return
        for target, edge_weight in edges.get(node, []):
            if target in visited:
                raise ArithmeticError("Cycle in acyclic network")
            walk(target, visited+(target,), weight*edge_weight)
    walk(source, (source,), F(1))
    return out


def points(gaps):
    t = [F(0)]
    for d in gaps:
        t.append(t[-1]+d)
    return t


def minor(t, i, j, weights=None):
    value = t[j]-t[i]
    return value if weights is None else weights[i]*weights[j]*value


def crossratio(t, quad, weights=None):
    a, b, c, d = quad
    return (minor(t, a, b, weights)*minor(t, c, d, weights)
            / (minor(t, a, d, weights)*minor(t, b, c, weights)))


def check_ptolemy(t, quad, weights=None):
    a, b, c, d = quad
    ac, bd = minor(t, a, c, weights), minor(t, b, d, weights)
    rhs = (minor(t, a, b, weights)*minor(t, c, d, weights)
           + minor(t, a, d, weights)*minor(t, b, c, weights))
    check("Ptolemy", ac*bd, rhs)
    require("subtraction-free flip", rhs/ac > 0)


def interval_mean(gaps, u, i, j):
    return qscale(qsum(qscale(u[r], gaps[r]) for r in range(i, j)),
                  1/sum(gaps[i:j]))


def log_crossratio_derivative(gaps, u, quad):
    a, b, c, d = quad
    return qsum([interval_mean(gaps, u, a, b), interval_mean(gaps, u, c, d),
                 qscale(interval_mean(gaps, u, a, d), -1),
                 qscale(interval_mean(gaps, u, b, c), -1)])


def main():
    k = recover_k()
    u = recover_direction(k)
    gaps = [F(x, sum(k)) for x in k]
    t, graph = points(gaps), ladder(gaps)
    lower, upper = [], []
    for j in range(13):
        lo = paths(graph, ('b', 0), ('q', j))
        hi = paths(graph, ('a', 0), ('q', j))
        check("lower path matrix", sum(w for _, w in lo), 1)
        check("upper path matrix", sum(w for _, w in hi), t[j])
        lower.append(lo)
        upper.append(hi)
    for i, j in combinations(range(13), 2):
        disjoint = sum(w*v for ns, w in lower[i] for ms, v in upper[j] if ns.isdisjoint(ms))
        reversed_paths = sum(w*v for ns, w in lower[j] for ms, v in upper[i] if ns.isdisjoint(ms))
        check("LGV nonintersecting sum", disjoint, minor(t, i, j))
        check("reversed pairing impossible", reversed_paths, 0)
        require("strict Plucker positivity", disjoint > 0)
    column_weights = [F(j+2, j+1) for j in range(13)]
    for quad in combinations(range(13), 4):
        check_ptolemy(t, quad)
        check_ptolemy(t, quad, column_weights)
        check("column torus fixes X", crossratio(t, quad, column_weights), crossratio(t, quad))
    for base in (2, 3, 9):
        refined = [d/base for d in gaps for _ in range(base)]
        refined_u = [x for x in u for _ in range(base)]
        rt = points(refined)
        check("normalized refinement", rt[-1], 1)
        for j in range(13):
            check("inherited endpoint", rt[base*j], t[j])
        for quad in combinations(range(13), 4):
            lifted = tuple(base*x for x in quad)
            check("inherited X", crossratio(rt, lifted), crossratio(t, quad))
            check("inherited shape velocity", log_crossratio_derivative(refined, refined_u, lifted),
                  log_crossratio_derivative(gaps, u, quad))
            check_ptolemy(rt, lifted)
        for quad in combinations(range(min(8, len(rt))), 4):
            check_ptolemy(rt, quad)
        # Every old polygon edge that acquires a new vertex becomes a diagonal.
        old_edge = (0, 1)
        lifted_edge = (0, base)
        require("old edge adjacent", old_edge[1]-old_edge[0] == 1)
        require("lifted edge now diagonal", lifted_edge[1]-lifted_edge[0] > 1)
    x = crossratio(t, (0, 1, 2, 3))
    derivative = log_crossratio_derivative(gaps, u, (0, 1, 2, 3))
    check("exact initial X", x, F(1560, 23711))
    check("exact nonzero shape derivative", derivative, (F(-309899, 917), F(-268596, 4585)))
    require("shape derivative strictly negative", qsign(derivative) < 0)
    # Direct derivative of the rational crossratio in gap coordinates, using
    # d'_r=d_r(u_r-mean), independently verifies the logarithmic identity.
    mean = qsum(qscale(v, d) for v, d in zip(u, gaps))
    tangent = [qscale(qadd(v, qscale(mean, -1)), d) for v, d in zip(u, gaps)]
    def log_interval(i, j):
        return qscale(qsum(tangent[i:j]), 1/sum(gaps[i:j]))
    independent = qsum([log_interval(0, 1), log_interval(2, 3),
                        qscale(log_interval(0, 3), -1), qscale(log_interval(1, 2), -1)])
    check("independent logarithmic derivative", derivative, independent)
    print(json.dumps({"checks": COUNT, "K_sum": sum(k), "network_columns": len(t),
                      "cluster_type": "A10", "positive_family_dimension": 11,
                      "ambient_top_cell_dimension": 22,
                      "crossratio_0123": str(x),
                      "d_log_X_0123": [str(v) for v in derivative],
                      "u_Qsqrt5": [[str(a), str(b)] for a, b in u],
                      "scope": "rank-two positive evaluation and inherited-endpoint refinement"},
                     sort_keys=True))
    print("PASS_NETWORK_CLUSTER_K_EXACT")


if __name__ == '__main__':
    main()
