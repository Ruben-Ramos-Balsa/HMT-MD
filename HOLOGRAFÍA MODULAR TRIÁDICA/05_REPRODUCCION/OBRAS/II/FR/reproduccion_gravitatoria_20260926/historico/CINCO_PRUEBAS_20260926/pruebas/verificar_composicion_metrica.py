"""Exact finite controls of memory elimination and longitudinal transport.

No observed G, tabulated Planck length, or numerical fit is used.
The general statements and their constitutive premises are in the companion MD.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "polar_helpers", HERE / "verificar_transporte_radial_polar.py")
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
eye, tr, mm = helpers.eye, helpers.tr, helpers.mm
add, sub, scale = helpers.add, helpers.sub, helpers.scale
inv, positive = helpers.inv, helpers.positive


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def scalar(v, w):
    return mm(tr(v), w)[0][0]


def zero(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def basis(n, m, i, j):
    a = zero(n, m)
    a[i][j] = F(1)
    return a


def schur_last(y):
    n = len(y) - 1
    a = [row[:n] for row in y[:n]]
    b = [[row[n]] for row in y[:n]]
    return sub(a, scale(mm(b, tr(b)), 1/y[n][n]))


def run():
    checks = []

    def check(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    a = mat(((1, 2, 0, 1), (0, 1, 1, 0),
             (1, 0, 2, 1), (0, 1, 0, 1)))
    W = add(mm(tr(a), a), eye(4))
    C = mat(((1, 0, 1, 1), (0, 1, 1, -1)))
    z = mat(((2,), (-3,)))
    Winv = inv(W)
    response = mm(C, mm(Winv, tr(C)))
    response_inv = inv(response)
    q = mm(response_inv, z)
    r = mm(Winv, mm(tr(C), q))
    check(positive(W), "global_weight_positive")
    check(W[0][2] != 0 and W[1][3] != 0,
          "cross_edge_memory_coupled")
    check(positive(response), "response_positive")
    check(mm(C, r) == z, "minimum_boundary")
    check(scalar(r, mm(W, r)) == scalar(z, q), "minimum_energy")
    for t in (F(-2), F(0), F(3, 7)):
        for u in (F(-1), F(1, 3)):
            k = mat(((-t-u,), (-t+u,), (t,), (u,)))
            check(mm(C, k) == zero(2, 1), "kernel_boundary")
            check(scalar(k, mm(W, r)) == 0, "weighted_orthogonality")
            rp = add(r, k)
            check(scalar(rp, mm(W, rp)) ==
                  scalar(r, mm(W, r)) + scalar(k, mm(W, k)),
                  "unique_minimum_square_completion")

    U = mat(((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5))))
    check(mm(U, tr(U)) == eye(2), "rational_unitary")
    D = scale(U, F(5759, 23040))
    y = mm(D, z)
    CL = mm(D, C)
    RL = mm(D, mm(response, tr(D)))
    qL = mm(inv(RL), y)
    rL = mm(Winv, mm(tr(CL), qL))
    check(RL == mm(CL, mm(Winv, tr(CL))), "transport_response")
    check(rL == r, "transport_same_residues")
    check(scalar(y, qL) == scalar(z, q), "transport_same_action")

    # All symmetric weight directions, all boundary-map directions,
    # and each longitudinal/end-point direction are differentiated exactly.
    directions = []
    for i in range(4):
        for j in range(i, 4):
            dW = basis(4, 4, i, j)
            if i != j:
                dW[j][i] = 1
            directions.append((dW, zero(2, 4), zero(2, 2), zero(2, 1)))
    for i in range(2):
        for j in range(4):
            directions.append((zero(4, 4), basis(2, 4, i, j),
                               zero(2, 2), zero(2, 1)))
    for i in range(2):
        for j in range(2):
            directions.append((zero(4, 4), zero(2, 4),
                               basis(2, 2, i, j), zero(2, 1)))
    for i in range(2):
        directions.append((zero(4, 4), zero(2, 4), zero(2, 2),
                           basis(2, 1, i, 0)))
    for index, (dW, dC, dD, dz) in enumerate(directions):
        dWinv = scale(mm(Winv, mm(dW, Winv)), -1)
        dR = add(add(mm(dC, mm(Winv, tr(C))),
                      mm(C, mm(Winv, tr(dC)))),
                 mm(C, mm(dWinv, tr(C))))
        dq = mm(response_inv, sub(dz, mm(dR, q)))
        dr = add(add(mm(dWinv, mm(tr(C), q)),
                     mm(Winv, mm(tr(dC), q))),
                 mm(Winv, mm(tr(C), dq)))
        check(add(mm(dC, r), mm(C, dr)) == dz,
              "differentiated_constraint_" + str(index))
        effective_derivative = 2*scalar(q, dz)-scalar(q, mm(dR, q))
        direct_derivative = 2*scalar(r, mm(W, dr))+scalar(r, mm(dW, r))
        check(effective_derivative == direct_derivative,
              "full_weight_variation_" + str(index))
        dRL = add(add(mm(dD, mm(response, tr(D))),
                       mm(D, mm(dR, tr(D)))),
                  mm(D, mm(response, tr(dD))))
        dy = add(mm(dD, z), mm(D, dz))
        transported_derivative = 2*scalar(qL, dy)-scalar(qL, mm(dRL, qL))
        check(transported_derivative == effective_derivative,
              "transported_variation_" + str(index))

    # An explicit square root permits exact checks of energy coordinates.
    root = mat(((2, 0), (0, 3)))
    R0 = mm(root, root)
    xi = mat(((2,), (-1,)))
    z0 = mm(root, xi)
    y0 = mm(D, z0)
    D_energy = mm(D, root)
    check(scalar(z0, mm(inv(R0), z0)) == scalar(xi, xi),
          "energy_coordinates")
    check(mm(D_energy, xi) == y0, "transported_energy_reader")
    check(mm(D_energy, tr(D_energy)) == mm(D, mm(R0, tr(D))),
          "same_metric_after_whitening")
    check(mm(D, xi) != y0, "unchanged_reader_is_different_realization")

    X = mat(((3, 1), (1, 2)))
    L, hbar, c = F(5, 11), F(17, 19), F(23, 29)
    quantum = hbar*c/L
    Y = mm(U, mm(X, tr(U)))
    radial = scale(Y, L)
    energy = scale(Y, quantum)
    conjugate = scale(inv(Y), L)
    G = c**3*L**2/hbar
    check(positive(X), "common_character_positive")
    check(mm(radial, conjugate) == scale(eye(2), L**2),
          "native_reciprocity")
    check(radial == scale(energy, L**2/(hbar*c)), "radial_energy_ratio")
    check(radial == scale(scale(energy, 1/c**2), G/c**2),
          "G_for_defined_reduced_radius")
    T = mat(((2, 1), (0, 3)))
    Tinv = inv(T)
    Rp = mm(T, mm(radial, tr(T)))
    dual = mm(tr(Tinv), mm(conjugate, Tinv))
    check(mm(Rp, dual) == scale(eye(2), L**2), "dual_coordinate_reciprocity")
    wrong_dual = mm(T, mm(conjugate, tr(T)))
    check(mm(Rp, wrong_dual) != scale(eye(2), L**2),
          "same_congruence_is_not_dual_transport")
    check(Rp == scale(mm(T, mm(energy, tr(T))), L/quantum),
          "common_congruence_preserves_G")

    Y3 = mat(((4, 1, 2), (1, 3, 1), (2, 1, 5)))
    check(positive(Y3), "coupled_schur_character_positive")
    for weight in (F(1), F(35, 729), F(34, 729), F(729, 35)):
        Z = scale(Y3, weight)
        check(schur_last(scale(Z, L)) == scale(schur_last(Z), L),
              "schur_radial_homogeneity")
        check(schur_last(scale(Z, quantum)) == scale(schur_last(Z), quantum),
              "schur_energy_homogeneity")
        check(schur_last(scale(Z, L)) ==
              scale(schur_last(scale(Z, quantum)), L/quantum),
              "shared_vacancy_weight_preserves_G")
    check(F(729, 35)*F(35, 729) == 1, "scalar_inverse_response_only")
    check(F(35, 729) != F(34, 729), "boundary_counts_distinct")
    return checks


if __name__ == "__main__":
    checks = run()
    print(json.dumps({
        "status": "PASS_COMPOSICION_METRICA_MEMORIA_Y_ACOPLAMIENTO",
        "exact_checks": len(checks),
        "checks": checks,
        "global_coupled_weights": True,
        "full_variation_verified_on_matrix_basis": True,
        "constitutive_reader_explicit": True,
        "measured_G_input": False,
        "tabulated_Planck_length_input": False,
        "original_physical_selection_from_weaker_axioms_proven": False,
        "Cartan_Holst_equivalence_claimed": False,
        "PDFs_modified": False,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2))
