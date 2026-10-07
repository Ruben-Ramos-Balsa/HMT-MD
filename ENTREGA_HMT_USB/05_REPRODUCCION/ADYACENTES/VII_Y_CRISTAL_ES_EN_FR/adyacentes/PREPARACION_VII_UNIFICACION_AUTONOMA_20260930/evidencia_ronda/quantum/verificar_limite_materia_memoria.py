#!/usr/bin/env python3
"""Focal controls for the mass/memory limit, using the Python standard library.

Test masses, angles and q values are diagnostics, not HMT physical outputs.
These finite controls exercise algebraic identities and falsifiers; the
infinite-dimensional domain and resolvent arguments are in the sibling note.
"""
import importlib.util
import json
import math
from pathlib import Path


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lib = load("memory_matrix_helpers", "verificar_acoplamiento_finito.py")
tor = load("memory_torsion_helpers", "verificar_torsion_fock.py")
zero, eye, diag = lib.zero, lib.eye, lib.diag
adj, mul, add, scale = lib.adj, lib.mul, lib.add, lib.scale
kron, direct, comm = lib.kron, lib.direct, lib.comm


def power(a, n):
    result = eye(len(a))
    for _ in range(n):
        result = mul(result, a)
    return result


def exp_matrix(a):
    result = eye(len(a))
    term = eye(len(a))
    for n in range(1, 65):
        term = scale(mul(term, a), 1 / n)
        result = add(result, term)
    return result


def inverse(a):
    n = len(a)
    b = [list(row) + list(ident) for row, ident in zip(a, eye(n))]
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(b[j][i]))
        b[i], b[pivot] = b[pivot], b[i]
        v = b[i][i]
        if abs(v) < 1e-15:
            raise ArithmeticError("Singular diagnostic matrix")
        b[i] = [x / v for x in b[i]]
        for j in range(n):
            if j != i:
                v = b[j][i]
                b[j] = [x - v * y for x, y in zip(b[j], b[i])]
    return [row[n:] for row in b]


def archive(t, eta, n):
    # Residual FIRST, then all memory increments in their original order.
    v = power(t, n)
    for j in range(n):
        v += mul(eta, power(t, j))
    return v


def refine(t, eta, n):
    d = len(t)
    result = zero((n + 2) * d, (n + 1) * d)
    for i in range(d):
        for j in range(d):
            result[i][j] = t[i][j]
            result[(n + 1) * d + i][j] = eta[i][j]
    for i in range(n * d):
        result[d + i][d + i] = 1
    return result


def omega(word):
    corr = lambda shift: sum(word[j] * word[(j + shift) % 12] for j in range(12))
    return -2 * corr(1) - 4 * corr(2) - 6 * corr(3), corr(6) / 2


def main():
    checks = []

    def yes(name, condition, residual=None):
        checks.append({"name": name, "passed": bool(condition), "residual": residual})
        if not condition:
            raise AssertionError(name)

    def eq(name, a, b):
        error = lib.residual(a, b)
        yes(name, error < 2e-11, error)

    def ne(name, a, b):
        error = lib.residual(a, b)
        yes(name, error > 1e-7, error)

    c = [[0, 1], [1, 0]]
    t = scale(add(scale(eye(2), 8), c), 1 / 9)
    # This is the compressed defect D=sqrt(8)/9 (C-I). It differs from
    # the nine-component eta by an isometric embedding of the defect range.
    eta = scale(add(c, eye(2), -1), math.sqrt(8) / 9)
    eq("nonadic_defect_identity", add(eye(2), mul(adj(t), t), -1), mul(adj(eta), eta))
    h, a = diag([2, 5]), [[0, 1j], [-1j, 0]]
    for n in (0, 1, 3, 6):
        v = archive(t, eta, n)
        w = refine(t, eta, n)
        vp = archive(t, eta, n + 1)
        eq("archive_isometry_%d" % n, mul(adj(v), v), eye(2))
        eq("refinement_isometry_%d" % n, mul(adj(w), w), eye(2 * (n + 1)))
        eq("archive_exact_square_%d" % n, mul(w, v), vp)
        hn = mul(mul(v, h), adj(v))
        hp = mul(mul(vp, h), adj(vp))
        eq("operator_intertwining_%d" % n, mul(w, hn), mul(hp, w))
        an = mul(mul(v, a), adj(v))
        eq("ordered_product_conserved_%d" % n, mul(hn, an), mul(mul(v, mul(h, a)), adj(v)))
        eq("commutator_conserved_%d" % n, comm(hn, an), mul(mul(v, comm(h, a)), adj(v)))
    v = archive(t, eta, 3)
    erased = v[2:]
    ne("negative_erase_residual_breaks_isometry", mul(adj(erased), erased), eye(2))
    eq("lost_norm_is_exact_residual", add(eye(2), mul(adj(erased), erased), -1), mul(adj(power(t, 3)), power(t, 3)))

    hist_a = [2, 2, 5, -4, -3, -2] * 2
    hist_b = [4, 3, 2, -2, -2, -5] * 2
    yes("histories_same_absolute_histogram", sorted(map(abs, hist_a)) == sorted(map(abs, hist_b)))
    memories = []
    for name, history in (("plus", hist_a), ("minus", hist_b)):
        p = [history[i] + history[i + 6] for i in range(6)]
        anti = [history[i] - history[i + 6] for i in range(6)]
        sc = sum(p)
        memory = [p[i] - p[5] for i in range(5)]
        p5 = (sc - sum(memory)) / 6
        pp = [p5 + v for v in memory] + [p5]
        decoded = [(pp[i] + anti[i]) / 2 for i in range(6)] + [(pp[i] - anti[i]) / 2 for i in range(6)]
        yes("ordered_history_recovered_" + name, decoded == history)
        memories.append(memory)
    yes("negative_histogram_does_not_determine_memory", memories[0] != memories[1])
    yes("electron_return_reader", omega([1, 1, 1, -1, -1, -1] * 2) == (80, 6))
    yes("negative_same_sign_count_different_reader", omega([1, -1] * 6) == (48, 6))

    # Use the actual Clifford current of VIII/33, restricted to Lambda^2 C^4.
    j, r, z = [[0, -1], [1, 0]], [[0, 1], [1, 0]], diag([1, -1])
    gs = [kron(j, eye(2)), kron(r, eye(2)), kron(z, r), kron(z, z)]
    adirac = scale(gs[0], -1j)
    triplets = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
    ms = [mul(mul(mul(adirac, gs[i]), gs[k]), gs[l]) for i, k, l in triplets]
    qfull = tor.normal_quartic(ms)
    ids = [state for state in range(16) if bin(state).count("1") == 2]
    restrict = lambda matrix: [[matrix[i][k] for k in ids] for i in ids]
    q = restrict(qfull)
    # Diagnostic bilinears in the same finite CAR space. These matrices
    # exercise ordered evolution; they do not select physical Yukawa data.
    y0 = [[0, 0, 1, .5], [0, 0, .3, 2], [1, .3, 0, 0], [.5, 2, 0, 0]]
    y1 = [[0, 0, 2, .2j], [0, 0, -.2j, 1], [2, .2j, 0, 0], [-.2j, 1, 0, 0]]
    b0, b1 = restrict(tor.dg(y0)), restrict(tor.dg(y1))
    h0, h1 = add(b0, scale(q, -3 / 20)), add(b1, scale(q, -3 / 40))
    eq("local_interaction_0_Hermitian", h0, adj(h0))
    eq("local_interaction_1_Hermitian", h1, adj(h1))
    ne("ordered_local_interactions_do_not_commute", comm(h0, h1), zero(6))
    e0, e1 = exp_matrix(scale(h0, -.04j)), exp_matrix(scale(h1, -.04j))
    clock = kron(c, eye(6))
    local = direct(e0, e1)
    u = mul(clock, local)
    eq("joint_return_unitary", mul(adj(u), u), eye(12))
    eq("two_returns_ordered_product", mul(u, u), direct(mul(e1, e0), mul(e0, e1)))
    ne("negative_reverse_fibre_order", mul(u, u), direct(mul(e0, e1), mul(e1, e0)))
    mass = direct(scale(eye(6), 2), scale(eye(6), 5))
    eq("mass_transport_uses_arrival_history", mul(mul(adj(u), mass), u), direct(scale(eye(6), 5), scale(eye(6), 2)))
    ne("negative_assume_every_return_preserves_mass", comm(mass, u), zero(12))
    eq("return_inverse_exact", mul(u, adj(u)), eye(12))

    # Infinite tower tail on h=30n, n>=6, within <90,120>. q are fixtures.
    qm, qp = .99, .97
    b = qm ** 30
    terms = lambda n: ((-1) ** n) * (n + 1) * (qm ** (30 * n) - qp ** (30 * n))
    linf = .1 + sum(terms(n) for n in range(6, 2000))
    minf = math.exp(linf)
    hinf = add(scale(b0, minf), scale(q, -3 / 20))
    rinfty = inverse(add(hinf, scale(eye(6), -1j)))
    previous_bound = float("inf")
    for stop in (6, 9, 12, 18):
        ln = .1 + sum(terms(n) for n in range(6, stop))
        # sum_(n>=stop) (n+1)b^n, exact closed-form bound.
        tail = b ** stop * ((stop + 1) / (1 - b) + b / (1 - b) ** 2)
        yes("tower_tail_bound_%d" % stop, abs(linf - ln) <= tail + 1e-14)
        yes("mass_relative_tail_bound_%d" % stop, abs(math.exp(ln) / minf - 1) <= math.expm1(tail) + 1e-13)
        yes("tower_bounds_contract_%d" % stop, tail < previous_bound)
        previous_bound = tail
        hn = add(scale(b0, math.exp(ln)), scale(q, -3 / 20))
        rn = inverse(add(hn, scale(eye(6), -1j)))
        eq("resolvent_identity_%d" % stop, add(rn, rinfty, -1), mul(mul(rn, add(hinf, hn, -1)), rinfty))
        delta = add(hinf, hn, -1)
        frobenius = math.sqrt(sum(abs(v) ** 2 for row in delta for v in row))
        yes("resolvent_error_control_%d" % stop, lib.residual(rn, rinfty) <= frobenius + 1e-12)

    # A raw lifted calendar coordinate k=9q+phase advances by nine;
    # its quotient memory q advances by ONE and the phase does not change.
    for lifted in (-108, -1, 0, 8, 9, 108):
        phase = lifted % 9
        moved = lifted + 9
        yes("phase_return_memory_survives_%d" % lifted,
            moved % 9 == phase and moved // 9 == lifted // 9 + 1)

    print(json.dumps({
        "status": "PASS_MASS_MEMORY_INTERACTION_LIMIT_CONTROLS",
        "checks_passed": len(checks),
        "scope": "Archive/refinement, ordered CAR interaction, mass memory and tower-resolvent estimates; proof of the infinite limit is in LIMITE_MATERIA_MEMORIA.md.",
        "checks": checks,
    }, indent=2))


if __name__ == "__main__":
    main()
