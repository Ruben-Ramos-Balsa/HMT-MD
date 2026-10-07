"""Controles algebraicos focales; no generador de constantes ni modelo físico.

Complementan las pruebas de TRAZA_GENERATIVA_COORDINADA, 10.18--10.23.
No leen datos experimentales ni modifican fuentes o recibos.
"""

from fractions import Fraction as F


def transpose(a):
    return [list(c) for c in zip(*a)]


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def neg(a):
    return [[-x for x in row] for row in a]


def shift(v, k):
    return [v[(m + k) % len(v)] for m in range(len(v))]


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def sign(x):
    return (x > 0) - (x < 0)


def subtract(a, b):
    return [x - y for x, y in zip(a, b)]


def scale(a, k):
    return [[k * x for x in row] for row in a]


def madd(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def msub(a, b):
    return madd(a, neg(b))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def frobenius(a, b):
    return sum(x * y for ar, br in zip(a, b) for x, y in zip(ar, br))


def commutator(a, b):
    return msub(mm(a, b), mm(b, a))


def tensor_rotation(r, q):
    return mm(mm(r, q), transpose(r))


def tt(n, q):
    assert dot(n, n) == 1
    p = msub(identity(3), [[x * y for y in n] for x in n])
    return msub(mm(mm(p, q), p), scale(p, trace(mm(p, q)) / F(2)))


def quadratic_product(x, y):
    # Exact arithmetic in Q[t]/(t^2-t-1), only for a posterior geometric test.
    # This is not used to generate phi or any HMT output.
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def geometric_checks():
    zero, one, t = (F(0), F(0)), (F(1), F(0)), (F(0), F(1))
    verts = []
    for s in (-1, 1):
        for r in (-1, 1):
            so, rt = tuple(s * a for a in one), tuple(r * a for a in t)
            verts.extend([(zero, so, rt), (so, rt, zero), (rt, zero, so)])
    assert len(set(verts)) == 12
    antipode = [verts.index(tuple(tuple(-a for a in x) for x in v)) for v in verts]
    ai = [[int(j == antipode[i]) for j in range(12)] for i in range(12)]
    p0 = [[F(1, 12)] * 12 for _ in range(12)]
    pe = scale(madd(identity(12), ai), F(1, 2))
    po = scale(msub(identity(12), ai), F(1, 2))
    p5 = msub(pe, p0)
    norm_fourth = quadratic_product((F(2), F(1)), (F(2), F(1)))
    gram = []
    for i, v in enumerate(verts):
        row = []
        for j, w in enumerate(verts):
            products = [quadratic_product(x, y) for x, y in zip(v, w)]
            d = tuple(sum(x[k] for x in products) for k in range(2))
            ratio = F(1) if j in (i, antipode[i]) else F(1, 5)
            assert quadratic_product(d, d) == tuple(ratio * x for x in norm_fourth)
            row.append(ratio - F(1, 3))
        gram.append(row)
    assert scale(gram, F(5, 8)) == p5
    projectors = (p0, p5, po)
    for i, p in enumerate(projectors):
        assert mm(p, p) == p == transpose(p)
        for j, q in enumerate(projectors):
            if i != j:
                assert mm(p, q) == [[0] * 12 for _ in range(12)]
    assert [trace(p) for p in projectors] == [1, 5, 6]
    assert madd(madd(p0, p5), po) == identity(12)

    basis = [[[1, 0, 0], [0, -1, 0], [0, 0, 0]],
             [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
             [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
             [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
             [[-1, 0, 0], [0, -1, 0], [0, 0, 2]]]
    jz = [[0, -1, 0], [1, 0, 0], [0, 0, 0]]
    jx = [[0, 0, 0], [0, 0, -1], [0, 1, 0]]
    zero_matrix = [[0] * 3 for _ in range(3)]
    expected = [scale(basis[1], 2), scale(basis[0], -2),
                basis[3], neg(basis[2]), zero_matrix]
    rz = [[F(3, 5), F(-4, 5), 0], [F(4, 5), F(3, 5), 0], [0, 0, 1]]
    rx = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
    n = [0, 0, 1]
    for i, q in enumerate(basis):
        assert q == transpose(q) and trace(q) == 0
        assert commutator(jz, q) == expected[i]
        assert tt(n, q) == (q if i < 2 else zero_matrix)
        lhs = msub(commutator(jx, commutator(jz, q)),
                   commutator(jz, commutator(jx, q)))
        assert lhs == commutator(commutator(jx, jz), q)
        for r in (rz, rx, mm(rx, rz)):
            rq = tensor_rotation(r, q)
            rn = [dot(row, n) for row in r]
            assert mm(transpose(r), r) == identity(3)
            assert frobenius(rq, rq) == frobenius(q, q)
            assert tt(rn, rq) == tensor_rotation(r, tt(n, q))
        for v in basis:
            assert frobenius(commutator(jz, q), v) == -frobenius(q, commutator(jz, v))
    # A moving transverse plane is necessary: fixed-plane commutation fails.
    assert tt(n, tensor_rotation(rx, basis[0])) != tensor_rotation(rx, tt(n, basis[0]))


def defect_checks():
    d0 = [[1, 0], [0, -1]]
    d1 = [[0, -1, 0], [1, 0, 1], [0, -1, 0]]
    d2 = [[1, 1], [0, 2]]
    t1 = [[1, 0], [0, 1], [1, 1]]
    t2 = [[1, 2, 0], [0, 1, -1]]
    defect1 = msub(mm(d1, t1), mm(t1, d0))
    defect2 = msub(mm(d2, t2), mm(t2, d1))
    t21 = mm(t2, t1)
    assert msub(mm(d2, t21), mm(t21, d0)) == madd(mm(defect2, t1), mm(t2, defect1))
    t = [[1, 1], [0, 1]]
    inv = [[1, -1], [0, 1]]
    defect = msub(mm(d2, t), mm(t, d0))
    assert mm(t, inv) == identity(2)
    assert msub(mm(d0, inv), mm(inv, d2)) == neg(mm(mm(inv, defect), inv))


def j2(d):
    assert 1 <= d <= 9
    return 0 if d == 9 else (1 if d % 2 == 0 else -1)


def cyclic_torsion(word):
    assert len(word) % 108 == 0
    zeta = [int(d == 9) * j2(word[i - 1]) for i, d in enumerate(word)]
    total = sum(zeta)
    corona = sum(zeta[26::27])
    return total, corona, total - 2 * corona


def signed_event_balance(block):
    sigma = [1, 1, 1, -1, -1, -1] * 2
    return sum(sigma[i // 9] for i, d in enumerate(block) if d in (2, 4, 6, 8))


def concatenation_checks():
    for n in range(-216, 217):
        q, sr = divmod(n, 108)
        s, r = divmod(sr, 9)
        assert n == 108 * q + 9 * s + r
        nonadic_height = 12 * q + s
        for blocks in (1, 10, 100):
            q1, sr1 = divmod(n + 108 * blocks, 108)
            s1, r1 = divmod(sr1, 9)
            assert (q1, s1, r1) == (q + blocks, s, r)
            assert 12 * q1 + s1 == nonadic_height + 12 * blocks

    first = [1] * 108
    first[0], first[1], first[-1] = 9, 2, 2
    balanced = [first] + [[1] * 108 for _ in range(9)]
    assert all(signed_event_balance(b) == 0 for b in balanced)
    assert cyclic_torsion(first) == (1, 0, 1)
    assert cyclic_torsion([d for b in balanced for d in b]) == (-1, 0, -1)

    examples = [balanced,
                [[(i + 2 * b) % 9 + 1 for i in range(108)] for b in range(10)],
                [[9] + [1 + b % 8] * 106 + [1 + (3 * b) % 9] for b in range(10)]]
    for blocks in examples:
        closed = [cyclic_torsion(b) for b in blocks]
        joined = cyclic_torsion([d for b in blocks for d in b])
        correction = sum(int(b[0] == 9) * (j2(blocks[k - 1][-1]) - j2(b[-1]))
                         for k, b in enumerate(blocks))
        assert joined[0] - sum(x[0] for x in closed) == correction
        assert joined[1] == sum(x[1] for x in closed)
        assert joined[2] - sum(x[2] for x in closed) == correction

    u = [1] + [0] * 5 + [-1] + [0] * 5
    history = [shift(u, 3 * b) for b in range(10)]
    omega = [[dot(shift(x, 3), y) for y in history] for x in history]
    assert all(sum(x) == 0 for x in history)
    assert omega == neg(transpose(omega))
    assert all(omega[b][b] == 0 for b in range(10))
    assert omega[0][1] == dot(u, u) == 2

    h = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    reader = [[1, 0]]
    observations = reader + mm(reader, h)
    assert observations[0][0] * observations[1][1] - observations[0][1] * observations[1][0] == F(-4, 5)
    assert mm([[0, 0]], h) == [[0, 0]]


def viability(vertices, edges):
    v = set(vertices)
    while True:
        nxt = {x for x in vertices if any(a == x and b in v for a, b in edges)}
        if nxt == v:
            return v
        assert nxt < v
        v = nxt


def main():
    d = [[-1, 1, 0], [0, -1, 1], [1, 0, -1]]
    lap = [[3 * int(i == j) - 1 for j in range(3)] for i in range(3)]
    assert mm(transpose(d), d) == mm(d, transpose(d)) == lap
    assert mm(transpose(neg(d)), neg(d)) == lap
    r = [[-1, 0, 0], [0, 1, 0], [0, 0, -1]]
    dr = mm(r, d)
    assert mm(transpose(dr), dr) == lap
    assert mm(dr, transpose(dr)) == mm(mm(r, lap), transpose(r))

    m = [[F(2), F(-5), F(28)], [F(0), F(7), F(-25, 2)],
         [F(1), F(-20), F(-2, 3)]]
    inv = [[F(1528, 3857), F(3380, 3857), F(801, 3857)],
           [F(75, 3857), F(176, 3857), F(-150, 3857)],
           [F(6, 551), F(-30, 551), F(-12, 551)]]
    assert mm(m, inv) == mm(inv, m) == identity(3)
    dh = [[1, 0, 0], [0, -1, 0], [0, 0, 1]]
    reflection = mm(mm(m, dh), inv)
    assert mm(reflection, reflection) == identity(3)
    assert mm(reflection, m) == mm(m, dh)

    # Six basis vectors of the antipodal sector; not a census of HMT seeds.
    basis = []
    for i in range(6):
        v = [int(k == i) for k in range(6)]
        basis.append(v + [-x for x in v])
    for u in basis:
        ju = shift(u, 3)
        assert shift(ju, 3) == [-x for x in u]
        assert dot(ju, ju) == dot(u, u)
        du = subtract(ju, u)
        for v in basis:
            jv = shift(v, 3)
            assert dot(ju, v) == -dot(u, jv)
            assert dot(du, subtract(jv, v)) == 2 * dot(u, v)

    examples = [[0] * 12,
                [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                list(range(12)),
                [2, -1, 0, 3, -2, 1, 5, -3, 2, 0, 1, -4]]
    for t in examples:
        e = subtract(t, shift(t, 6))
        tau = [sign(x) for x in e]
        assert shift(e, 6) == [-x for x in e]
        assert shift(tau, 6) == [-x for x in tau]
        b = [sign(sum(e[(a + 4 * j) % 12] for j in range(3))) for a in range(4)]
        corr = [tau[m] * tau[(m + 3) % 12] for m in range(12)]
        assert b[2:] == [-b[0], -b[1]]
        assert sum(b) == sum(corr) == 0
        assert shift(corr, 3) == [-x for x in corr]
        even = [(x + y) / F(2) for x, y in zip(t, shift(t, 6))]
        assert [x + y / F(2) for x, y in zip(even, e)] == t

    # Counterexample to extending the antipodal cancellation to general events.
    general = [1] + [0] * 11
    general_b = [sign(sum(general[(a + 4 * j) % 12] for j in range(3))) for a in range(4)]
    assert sum(general_b) == 1

    v = viability(range(4), {(0, 1), (0, 2), (1, 1), (2, 3)})
    assert v == {0, 1}
    assert {y for x, y in {(0, 1), (0, 2)} if y in v} == {1}
    assert viability(range(2), {(0, 0), (0, 1), (1, 1)}) == {0, 1}
    geometric_checks()
    defect_checks()
    concatenation_checks()
    print("COMPROBACIONES_ALGEBRAICAS_FOCALES_OK")
    print("Incidencia, reflexión CKM, sector antipodal, cancelaciones, poda finita,")
    print("proyector icosaédrico 1+5+6, transporte STF/TT y composición de defectos.")
    print("Alturas 108/1080, empalmes torsionales y observaciones entre bloques.")
    print("No acredita selección física, generación de constantes ni problemas del Milenio.")


if __name__ == "__main__":
    main()
