#!/usr/bin/env python3
"""Control racional focal de la descomposición y los signos del residual.

Sin dependencias externas, red, escritura de archivos ni valores físicos
objetivo. Las matrices racionales son testigos algebraicos posteriores;
no generan G, el reloj HMT, una corriente material ni una amplitud cosmológica.
El recibo JSON se emite por stdout mediante --json.
"""

from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import sys


N = 4
SIGN = (-1, 1, 1, 1)


def zero():
    return [[Q(0) for _ in range(N)] for _ in range(N)]


def scale(a, tensor):
    return [[a * v for v in row] for row in tensor]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(N)] for i in range(N)]


def sub(a, b):
    return add(a, scale(Q(-1), b))


METRIC = zero()
for index, sign in enumerate(SIGN):
    METRIC[index][index] = Q(sign)


def trace(tensor):
    return sum((SIGN[i] * tensor[i][i] for i in range(N)), Q(0))


def project_trace(tensor):
    return scale(trace(tensor) / N, METRIC)


def project_zero(tensor):
    return sub(tensor, project_trace(tensor))


def divergence(jet):
    # Coordenadas normales de Levi--Civita en un punto:
    # jet[alpha][mu][nu] = nabla_alpha T_mu,nu.
    return [sum((SIGN[mu] * jet[mu][mu][nu] for mu in range(N)), Q(0))
            for nu in range(N)]


def vector_add(a, b):
    return [x + y for x, y in zip(a, b)]


def vector_sub(a, b):
    return [x - y for x, y in zip(a, b)]


def run():
    checks = []
    failures = []

    def check(name, actual, expected):
        checks.append(name)
        if actual != expected:
            failures.append(name)

    bases = []
    for i in range(N):
        for j in range(i, N):
            tensor = zero()
            tensor[i][j] = tensor[j][i] = Q(1)
            bases.append(tensor)

    for number, tensor in enumerate(bases):
        pt, pz = project_trace(tensor), project_zero(tensor)
        check(f"base {number}: recomposicion", add(pt, pz), tensor)
        check(f"base {number}: P_tr idempotente", project_trace(pt), pt)
        check(f"base {number}: P_0 idempotente", project_zero(pz), pz)
        check(f"base {number}: traza nula", trace(pz), Q(0))
        check(f"base {number}: P_tr P_0", project_trace(pz), zero())
        check(f"base {number}: P_0 P_tr", project_zero(pt), zero())

    for alpha in range(N):
        for number, tensor in enumerate(bases):
            jet = [zero() for _ in range(N)]
            jet[alpha] = tensor
            jt = [project_trace(component) for component in jet]
            jz = [project_zero(component) for component in jet]
            grad = [trace(component) / N for component in jet]
            div = divergence(jet)
            prefix = f"jet {alpha},{number}"
            check(prefix + ": divergencia traza", divergence(jt), grad)
            check(prefix + ": balance residual cero",
                  divergence(jz), vector_sub(div, grad))
            check(prefix + ": recomposicion divergencia",
                  vector_add(divergence(jt), divergence(jz)), div)

    # Tensor conservado con traza variable: en espacio plano,
    # T_11=x^0 y todas las demás componentes nulas.
    jet = [zero() for _ in range(N)]
    jet[0][1][1] = Q(1)
    j_trace = divergence([project_trace(component) for component in jet])
    j_zero = divergence([project_zero(component) for component in jet])
    check("conservacion total con traza variable", divergence(jet), [Q(0)] * N)
    check("intercambio de traza variable", j_trace, [Q(1, 4), Q(0), Q(0), Q(0)])
    check("intercambio opuesto", j_zero, [-v for v in j_trace])

    for number in range(1, 7):
        kappa, h_squared = Q(number + 1, number + 2), Q(number, number + 3)
        rho = 3 * h_squared / kappa
        tensor = scale(-rho, METRIC)
        energy = tensor[0][0]
        pressure = sum((tensor[i][i] for i in range(1, N)), Q(0)) / 3
        check(f"de Sitter {number}: densidad", energy, rho)
        check(f"de Sitter {number}: presion", pressure, -rho)
        check(f"de Sitter {number}: traza", trace(tensor), -4 * rho)
        check(f"de Sitter {number}: sector puro", project_trace(tensor), tensor)
        check(f"de Sitter {number}: sector cero", project_zero(tensor), zero())
        check(f"de Sitter {number}: aceleracion",
              -kappa * (energy + 3 * pressure) / 6, h_squared)

    # Sustitución de la ecuación efectiva de 31. Es un control algebraico
    # de la identidad de fuentes, no una solución de ecuaciones materiales.
    kappa, lambda_int, lambda_ref = Q(7, 3), Q(5, 11), Q(-2, 13)
    for number, lc in enumerate(bases):
        spin = scale(Q(2, 5), bases[(number + 1) % len(bases)])
        material = scale(Q(-3, 7), bases[(number + 2) % len(bases)])
        einstein = sub(scale(kappa, add(lc, spin)), scale(lambda_int, METRIC))
        residual = sub(scale(1 / kappa,
                             add(einstein, scale(lambda_ref, METRIC))), material)
        expected = add(sub(add(lc, spin), material),
                       scale((lambda_ref - lambda_int) / kappa, METRIC))
        check(f"composicion Cartan {number}", residual, expected)

    # Controles negativos: las tres alteraciones deben ser rechazadas.
    mutations = {
        "reemplazar 1/4 por 1/3": trace(sub(METRIC,
                                         scale(trace(METRIC) / 3, METRIC))) != 0,
        "usar p=+rho en aceleracion": -Q(1, 6) * (3 + 3 * 3) != 1,
        "deducir conservacion separada de conservacion total":
            j_trace != [Q(0)] * N,
    }
    for name, rejected in mutations.items():
        check("mutacion rechazada: " + name, rejected, True)

    source = Path(__file__).resolve().parent.parent / "manuscrito" / "60_tensor_residual_y_balance.tex"
    source_sha = hashlib.sha256(source.read_bytes()).hexdigest() if source.is_file() else None
    return {
        "schema": "HMT.VII.tensor-residual.control-racional.v1",
        "status": "PASS_IDENTIDADES_TENSOR_RESIDUAL" if not failures else "FAIL_IDENTIDADES_TENSOR_RESIDUAL",
        "checks": len(checks),
        "symmetric_basis_size": len(bases),
        "first_jet_basis_size": N * len(bases),
        "negative_controls": mutations,
        "failed_checks": failures,
        "source": "manuscrito/60_tensor_residual_y_balance.tex",
        "source_sha256": source_sha,
        "scope": {
            "arithmetic": "racional exacta; firma (-+++); dimension cuatro",
            "projection_identities": True,
            "trace_divergence_identity_in_normal_coordinates": True,
            "cartan_source_substitution": True,
            "de_sitter_density_pressure_acceleration_signs": True,
            "bianchi_identity_geometric_proof_executed": False,
            "de_sitter_curvature_computed_by_this_script": False,
            "physical_current_or_density_evaluated": False,
            "generated_hmt_constants_verified_by_this_script": False,
            "global_hmt_or_article_autonomy_certified": False,
        },
    }


def main():
    if sys.argv[1:] not in ([], ["--json"]):
        print("Uso: verificar_tensor_residual.py [--json]", file=sys.stderr)
        return 2
    receipt = run()
    if sys.argv[1:] == ["--json"]:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(receipt["status"])
        print("Controles exactos:", receipt["checks"])
        if receipt["failed_checks"]:
            print("Fallos:", "; ".join(receipt["failed_checks"]))
    return 0 if not receipt["failed_checks"] else 1


if __name__ == "__main__":
    sys.exit(main())
