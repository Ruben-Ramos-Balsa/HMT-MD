#!/usr/bin/env python3
"""Identidades locales exactas: actualización publicada, sectores y determinantes.
No genera trayectorias TPK nuevas ni acepta datos metrológicos.
Los recuentos del ensayo son coeficientes formales del lector fuente, no
una afirmación de realizabilidad de todas las palabras del dominio ambiente.
"""
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OWNER = ROOT / "REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/verificar_proyectores_ciclicos_menos_un_doce.py"
spec = importlib.util.spec_from_file_location("projector_owner", OWNER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
n = 12
I = m.identity(n)
Z = m.scale(F(0), I)
sub = lambda a, b: m.add(a, m.scale(F(-1), b))
S = m.cyclic_shift(n, 1)
R = m.transpose(S)
P3 = m.invariant_projector(n, 3)
P4 = m.invariant_projector(n, 4)
P0 = m.invariant_projector(n, 1)
E = sub(P3, P4)
Pminus = m.scale(F(1, 2), sub(I, m.matrix_power(S, 6)))
Pplus = sub(I, Pminus)
J = m.matmul(m.matrix_power(S, 3), Pminus)
Q = m.matmul(P4, Pminus)
D3 = sub(I, m.matrix_power(S, 3))
D4 = sub(I, m.matrix_power(S, 4))
B = m.add(m.matmul(m.transpose(D3), D3), m.matmul(m.transpose(D4), D4))

def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p

def mul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i+j] += a*b
    return trim(r)

def det_identity_minus_s(a):
    # Newton: k c_k = -sum_{j=1}^k tr(A^j)c_{k-j}.
    power = I
    traces = [F(0)]
    for k in range(1, n+1):
        power = m.matmul(power, a)
        traces.append(m.trace(power))
    coeff = [F(1)]
    for k in range(1, n+1):
        coeff.append(-sum(traces[j]*coeff[k-j]
                          for j in range(1, k+1))/k)
    return trim(coeff)

def determinant(a):
    a = [row[:] for row in a]
    value = F(1)
    for k in range(n):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            value = -value
        p = a[k][k]
        value *= p
        for i in range(k+1, n):
            factor = a[i][k]/p
            for j in range(k+1, n):
                a[i][j] -= factor*a[k][j]
            a[i][k] = F(0)
    return value

def evaluate(p, x):
    out = F(0)
    for a in reversed(p):
        out = out*x+a
    return out

def column(j):
    return [[F(int(i == j))] for i in range(n)]

def outer(u, v):
    return m.matmul(u, m.transpose(v))

def energy(v):
    return m.matmul(m.transpose(v), m.matmul(B, v))[0][0]/2

# The generated event count c_m acts on the current window e_m.
# Transport to the moving frame gives y+ = R y + c_m R e0.
u = column(0)
v = m.matmul(R, u)
m.require(m.matmul(m.transpose(R), m.matmul(B, R)) == B,
          "phase transport changes B")
m.require(m.matmul(m.transpose(R), m.matmul(B, v)) == m.matmul(B, u),
          "linear energy coefficient disagrees")
m.require(energy(v) == 2, "quadratic energy coefficient disagrees")

# Coefficient matrix of the twelve source counts through a complete cycle.
W = Z
window_checks = 0
sigma = (1, 1, 1, -1, -1, -1, 1, 1, 1, -1, -1, -1)
for j in range(n):
    W = m.add(m.matmul(R, W), outer(v, column(j)))
    expected = Z
    for k in range(j+1):
        expected = m.add(expected, outer(
            m.matmul(m.matrix_power(R, j+1), column(k)), column(k)))
    m.require(W == expected, "moving frame loses window provenance")
    # Scalar checks supplement the general coefficient identities above.
    for count in range(10):
        c = F(sigma[j]*count)
        y = [[F((3*i+2*j) % 11-5)] for i in range(n)]
        y_next = m.matmul(R, m.add(y, m.scale(c, u)))
        delta = energy(y_next)-energy(y)
        target = c*m.matmul(B, y)[0][0] + 2*c*c
        m.require(delta == target, "event energy balance")
        window_checks += 1
m.require(W == I, "a phase return erased or permuted the counts")
m.require(m.matrix_power(R, 12) == I, "wrong observable phase period")

m.require(m.matmul(J, J) == m.scale(F(-1), Pminus), "J square")
m.require(m.transpose(J) == m.scale(F(-1), J), "J orientation")
m.require(m.matmul(P3, Pminus) == Z, "H3 has an antipodal part")
m.require(m.rank(Q) == 2 and m.matmul(Q, Q) == Q, "Q is not rank two")
m.require(m.matmul(B, Pminus) == sub(m.scale(F(5), Pminus),
                                   m.scale(F(3), Q)), "antipodal energy")
m.require(m.matmul(E, Pminus) == m.scale(F(-1), Q), "antipodal defect")
m.require(m.matmul(B, Q) == m.scale(F(2), Q), "complex plane energy")

A3 = m.matmul(S, P3)
A4 = m.matmul(S, P4)
AQ = m.matmul(S, Q)
A4plus = m.matmul(S, m.matmul(P4, Pplus))
p3 = det_identity_minus_s(A3)
p4 = det_identity_minus_s(A4)
pq = det_identity_minus_s(AQ)
p4plus = det_identity_minus_s(A4plus)
m.require(p3 == [F(1), F(0), F(0), F(-1)], "3-cycle determinant")
m.require(p4 == [F(1), F(0), F(0), F(0), F(-1)], "4-cycle determinant")
m.require(pq == [F(1), F(0), F(1)], "antipodal determinant")
m.require(mul(pq, p4plus) == p4, "sector factorization")
# Independent elimination at several rational points; polynomial proof is above.
for a, p in ((A3, p3), (A4, p4), (AQ, pq)):
    for x in (F(0), F(1, 3), F(-2, 5), F(2)):
        m.require(determinant(sub(I, m.scale(x, a))) == evaluate(p, x),
                  "Newton polynomial / elimination disagreement")
traces = []
for k in range(25):
    a = m.trace(m.matmul(m.matrix_power(S, k), E))
    expected = F(3*int(k % 3 == 0)-4*int(k % 4 == 0))
    m.require(a == expected, "trace character")
    traces.append(a)
m.require(traces[0]/12 == F(-1, 12), "zeroth normalized trace")
m.require(sum(traces[1:13]) == 0, "periodic mean")
m.require(traces[:13] == traces[12:25], "trace period")
# Formal logarithmic derivative: -s F'/F = sum a_n s^n.
numerator = [F(0)]*13
for k in range(1, 13):
    numerator[k] = traces[k]
# Multiplying the geometric period denominator produces the trace numerator.
# The rational expression is 3s^3/(1-s^3)-4s^4/(1-s^4).
left = mul(numerator, mul(p3, p4))
right_a = [F(0), F(0), F(0), F(3)]
right_b = [F(0), F(0), F(0), F(0), F(-4)]
ra = mul(right_a, p4)
rb = mul(right_b, p3)
r = [F(0)]*max(len(ra), len(rb))
for k in range(len(ra)): r[k] += ra[k]
for k in range(len(rb)): r[k] += rb[k]
period_den = [F(1)]+[F(0)]*11+[F(-1)]
m.require(trim(left) == mul(trim(r), period_den), "logarithmic derivative")

print(json.dumps({
    "status": "PASS_LOCAL_ACTUALIZACION_TPK_Y_DETERMINANTES",
    "method": "exact rational identities on the complete 12-coordinate reader",
    "source_helper": str(OWNER),
    "eta_role": "generated output of the signed event update, not a free input",
    "eta_formula": "c_m S^(-1) e_0",
    "count_formula": "Sigma_m * count(d_t in {2,4,6,8}, t in E_m)",
    "energy_increment": "c_m (B y_m)_0 + 2 c_m^2",
    "whole_cycle_count_coefficient_matrix": "I_12",
    "supplementary_event_checks": window_checks,
    "determinant_coefficients_ascending": {
        "H3": list(map(str, p3)), "H4": list(map(str, p4)),
        "H4_antipodal": list(map(str, pq)),
        "H4_even": list(map(str, p4plus))
    },
    "trace_period_n1_to_12": list(map(str, traces[1:13])),
    "antipodal_rank": m.rank(Pminus),
    "complex_subspace_rank": m.rank(Q),
    "antipodal_energy": "5 I - 3 Q",
    "scope": "published event reader and its spectral consequences; no claim that a count determines full TPK history, no EDP theorem, no empirical calibration"
}, ensure_ascii=False, indent=2))

