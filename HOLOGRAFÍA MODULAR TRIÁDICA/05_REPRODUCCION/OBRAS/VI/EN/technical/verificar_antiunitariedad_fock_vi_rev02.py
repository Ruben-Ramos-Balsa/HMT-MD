#!/usr/bin/env python3
"""Controles finitos exactos de las correcciones locales 08/10/13 de VI REV02.

No valida la construcción completa de partículas ni un productor del registro.
Los checks son explícitos y siguen activos con python -O.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path


CHECKS = []


def check(name, condition):
    if not condition:
        raise RuntimeError("FAIL: " + name)
    CHECKS.append(name)


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def adj(a):
    return [[a[j][i].conjugate() for j in range(len(a))]
            for i in range(len(a[0]))]


def scale(a, c):
    return [[c * x for x in row] for row in a]


def ident(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def determinant(a):
    n = len(a)
    total = Q(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = Q((-1) ** inversions)
        for i in range(n):
            term *= a[i][p[i]]
        total += term
    return total


def basis(n):
    return [s for k in range(n + 1) for s in combinations(range(n), k)]


def wedge_gamma(t):
    source, target = basis(len(t[0])), basis(len(t))
    result = [[Q(0) for _ in source] for _ in target]
    for i, out in enumerate(target):
        for j, inp in enumerate(source):
            if len(out) == len(inp):
                result[i][j] = determinant([[t[r][c] for c in inp] for r in out])
    return result


def annihilator(n, g):
    states = basis(n)
    position = {s: i for i, s in enumerate(states)}
    result = [[Q(0) for _ in states] for _ in states]
    for j, state in enumerate(states):
        for k, mode in enumerate(state):
            out = state[:k] + state[k + 1:]
            result[position[out]][j] += (-1) ** k * g[mode].conjugate()
    return result


def mv(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def run():
    # Entries 0, +/-1, +/-i are represented exactly; no approximate exponential.
    h = [[1, 0], [0, 2]]
    u = [[-1j, 0], [0, -1]]  # exp(-i*pi*H/2), hbar=1.
    conjugate = [[x.conjugate() for x in row] for row in u]
    check("H_real_conmuta_con_conjugacion", h == [[x.conjugate() for x in r] for r in h])
    check("CUC_inv_es_U_menos_t", conjugate == adj(u))
    check("control_negativo_CU_no_es_UC", conjugate != u)
    evolved = mv(u, [1, 0])
    check("vector_real_no_permanece_real", evolved != [x.conjugate() for x in evolved])
    sigma_y = [[0, -1j], [1j, 0]]
    check("CHC_inv_menos_H", [[x.conjugate() for x in r] for r in sigma_y] == scale(sigma_y, -1))
    rotation = scale(sigma_y, -1j)  # exp(-i*pi*sigma_y/2).
    check("generador_imaginario_grupo_real", rotation == [[x.conjugate() for x in r] for r in rotation])
    check("grupo_real_unitario", mm(adj(rotation), rotation) == ident(2))

    for name, t in [
        ("contraccion", [[Q(1, 2), Q(1, 4)], [Q(0), Q(1, 2)]]),
        ("isometria_rectangular", [[Q(1), Q(0)], [Q(0), Q(1)], [Q(0), Q(0)]]),
    ]:
        n, m = len(t[0]), len(t)
        gamma = wedge_gamma(t)
        for j in range(m):
            g = [Q(i == j) for i in range(m)]
            left = mm(annihilator(m, g), gamma)
            right = mm(gamma, annihilator(n, mv(adj(t), g)))
            check(name + "_aniquilacion_adjunto_" + str(j), left == right)
        for j in range(n):
            f = [Q(i == j) for i in range(n)]
            tf = mv(t, f)
            left = mm(gamma, adj(annihilator(n, f)))
            right = mm(adj(annihilator(m, tf)), gamma)
            check(name + "_creacion_" + str(j), left == right)
            if name == "isometria_rectangular":
                check(name + "_mismo_modo_" + str(j),
                      mm(annihilator(m, tf), gamma) == mm(gamma, annihilator(n, f)))
                ns = mm(adj(annihilator(n, f)), annihilator(n, f))
                nt = mm(adj(annihilator(m, tf)), annihilator(m, tf))
                check(name + "_ocupacion_" + str(j), mm(nt, gamma) == mm(gamma, ns))
        if name == "contraccion":
            f = [Q(1), Q(0)]
            check("control_negativo_mismo_modo_no_isometrico",
                  mm(annihilator(m, mv(t, f)), gamma) != mm(gamma, annihilator(n, f)))

    # Base simétrica no normalizada z^n; aniquilación d/dz, creación z.
    # Es un cambio de base de la identidad normalizada, sin raíces aproximadas.
    for t in (Q(1, 2), Q(1, 3)):
        size = 7
        gamma = [[t ** i if i == j else Q(0) for j in range(size)] for i in range(size)]
        a = [[Q(j) if i == j - 1 else Q(0) for j in range(size)] for i in range(size)]
        c = [[Q(1) if i == j + 1 else Q(0) for j in range(size)] for i in range(size)]
        check("boson_adjunto_" + str(t), mm(a, gamma) == mm(gamma, scale(a, t)))
        check("boson_creacion_" + str(t), mm(gamma, c) == mm(scale(c, t), gamma))

    chat, tau, d, eta, uc, ut = Q(3, 5), Q(7, 11), Q(13, 17), Q(19, 23), Q(2), Q(3)
    ul = uc * ut
    check("cambio_carta_velocidad", (chat / d) * (d * uc) == chat * uc)
    check("cambio_carta_duracion", (tau / eta) * (eta * ut) == tau * ut)
    check("cambio_carta_longitud", (tau / eta) * (chat / d) * (d * eta * ul) == tau * chat * ul)
    check("longitud_elemental_normalizacion", chat * uc * ut == chat * ul)
    check("carta_adaptada", chat / chat == 1)
    rplus = (1 - Q(2, 5) ** 90) / (1 - Q(2, 5) ** 120)
    rminus = (1 - Q(1, 4) ** 90) / (1 - Q(1, 4) ** 120)
    determinant_v = rplus * rminus
    check("canales_constitutivos_positivos", 0 < rplus < 1 and 0 < rminus < 1)
    check("velocidad_determinantal", 1 / determinant_v == 1 / rplus / rminus)
    # La prueba general usa log(det V); este control exacto prueba su lectura
    # multiplicativa, sin aproximar logaritmos ni introducir velocidad metrológica.
    action, duration, speed = Q(31, 37), tau * ut, chat * uc
    clock_mass = action / (108 * duration * speed ** 2)
    scaled_mass = action / (108 * ((tau / eta) * (eta * ut))
                           * ((chat / d) * (d * uc)) ** 2)
    check("masa_cronologica_covariancia_unidades", clock_mass == scaled_mass)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    run()
    root = Path(__file__).resolve().parent.parent
    files = ["sections/08_familias_y_compuestos.tex", "sections/09_dependencias_anteriores.tex",
             "sections/10_sectores_topologicos.tex", "sections/13_fock_pauli_composicion.tex"]
    result = {
        "status": "PASS_CONTROLES_FINITOS_ANTIUNITARIEDAD_FOCK_VI_REV02",
        "scope": "Identidades finitas exactas y controles negativos locales; no valida un productor genealógico ni la autonomía científica del artículo.",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks_count": len(CHECKS),
        "checks": CHECKS,
        "source_hashes": {f: hashlib.sha256((root / f).read_bytes()).hexdigest() for f in files},
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
