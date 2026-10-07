#!/usr/bin/env python3
"""Controles finitos de las identidades del capítulo 03, no certificado de RH."""

import cmath
import argparse
import json
import math
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--receipt", type=Path)
args = parser.parse_args()


def zeros(n, m):
    return [[0j for _ in range(m)] for _ in range(n)]


def eye(n):
    return [[complex(i == j) for j in range(n)] for i in range(n)]


def adj(a):
    return [[complex(x).conjugate() for x in col] for col in zip(*a)]


def mul(a, b):
    return [
        [sum(x * y for x, y in zip(row, col)) for col in zip(*b)]
        for row in a
    ]


def diff(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def norm(a):
    return math.sqrt(sum(abs(x) ** 2 for row in a for x in row))


def power(a, n):
    out = eye(len(a))
    for _ in range(n):
        out = mul(out, a)
    return out


def scale(a, c):
    return [[c * x for x in row] for row in a]


errors = {}
gammas = [-100.0, -5.0, -0.5, 0.0, 0.5, 5.0, 14.134725, 100.0]
for gamma in gammas:
    tau = (gamma + 0.5j) / (gamma - 0.5j)
    recovered = 0.5j * (tau + 1) / (tau - 1)
    errors[f"cayley_inverse_{gamma}"] = abs(recovered - gamma)
    errors[f"cayley_unitarity_{gamma}"] = abs(abs(tau) - 1)

tau = cmath.exp(0.73j)
s = zeros(9, 9)
for j in range(8):
    s[j + 1][j] = 1
s[0][8] = tau
errors["calendar_unitarity"] = norm(diff(mul(adj(s), s), eye(9)))
errors["calendar_ninth_power"] = norm(diff(power(s, 9), scale(eye(9), tau)))
u = [[1 / 3] for _ in range(9)]
a = mul(mul(adj(u), s), u)[0][0]
errors["uniform_compression"] = abs(a - (8 + tau) / 9)
errors["compression_defect"] = abs(1 - abs(a) ** 2 - 8 / 81 * abs(1 - tau) ** 2)
q = 5 / 9
errors["per_turn_normalization"] = norm(
    diff(power(scale(s, q ** (1 / 9)), 9), scale(eye(9), q * tau))
)
wrong_turn = power(scale(s, q), 9)
if not norm(diff(wrong_turn, scale(eye(9), q * tau))) > 0.1:
    raise RuntimeError("El control negativo no distingue el factor por paso del factor por vuelta")

# Dos niveles binarios de pesos compatibles y memoria entera no uniforme.
mu0 = [0.4, 0.6]
mu1 = [0.1, 0.3, 0.2, 0.4]
mu2 = [0.025, 0.075, 0.12, 0.18, 0.05, 0.15, 0.1, 0.3]
mem0 = [-1, 2]
mem1 = [0, 4, 3, 2]
mem2 = [2, 1, 5, 7, 1, 4, 8, 3]


def transport(parent_mu, child_mu, parent_mem, child_mem):
    out = zeros(len(child_mu), len(parent_mu))
    for j, weight in enumerate(child_mu):
        p = j // 2
        out[j][p] = math.sqrt(weight / parent_mu[p]) * tau ** (
            child_mem[j] - parent_mem[p]
        )
    return out


v01 = transport(mu0, mu1, mem0, mem1)
v12 = transport(mu1, mu2, mem1, mem2)
errors["cylinder_isometry_01"] = norm(diff(mul(adj(v01), v01), eye(2)))
errors["cylinder_isometry_12"] = norm(diff(mul(adj(v12), v12), eye(4)))
v02 = zeros(8, 2)
for j, weight in enumerate(mu2):
    p = j // 4
    v02[j][p] = math.sqrt(weight / mu0[p]) * tau ** (mem2[j] - mem0[p])
errors["cylinder_cocycle_composition"] = norm(diff(mul(v12, v01), v02))

# La hipótesis incremento uno se comprueba por separado, no se infiere
# de la compatibilidad de pesos.
unit_increment = zeros(4, 2)
for j, weight in enumerate(mu1):
    p = j // 2
    unit_increment[j][p] = math.sqrt(weight / mu0[p]) * tau
j0 = [[math.sqrt(weight)] for weight in mu0]
j1 = [[math.sqrt(weight) * tau] for weight in mu1]
errors["one_memory_return"] = norm(diff(mul(unit_increment, j0), j1))

maximum = max(errors.values())
if not maximum < 1e-11:
    raise RuntimeError("Fallo en las identidades finitas: " + repr(errors))
report = {
    "status": "PASS_CONTROLES_FINITOS_CAPITULO_03",
    "checks": len(errors),
    "optimization_level": sys.flags.optimize,
    "maximum_absolute_error": maximum,
    "negative_control_per_step_vs_per_turn": "DETECTED",
    "scope": "Identidades finitas de Cayley, calendario y transporte cilíndrico.",
    "not_certified": [
        "Codificador nativo de los dos momentos de Weil",
        "Positividad global de Weil",
        "Hipótesis de Riemann",
        "Autonomía demostrativa del artículo completo"
    ]
}
encoded = json.dumps(report, ensure_ascii=False, indent=2)
if args.receipt:
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(encoded + "\n", encoding="utf-8")
print(encoded)
