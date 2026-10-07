#!/usr/bin/env python3
"""Controles exactos y finitos del bloque de observador de VII.

Sólo biblioteca estándar. No escribe archivos ni requiere el corpus exterior.
Las entradas racionales de prueba son ejemplos algebraicos, no valores objetivo
de constantes HMT. Las identidades generales se demuestran en el manuscrito.
"""

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


COUNTS = {}


def require(condition, group, message):
    COUNTS[group] = COUNTS.get(group, 0) + 1
    if not condition:
        raise ValueError(f"{group}: {message}")


def matrix(rows):
    return tuple(tuple(Q(x) for x in row) for row in rows)


def eye(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def unit(n, i, j):
    return matrix([[int(a == i and b == j) for b in range(n)] for a in range(n)])


def add(*items):
    return tuple(tuple(sum(a[i][j] for a in items) for j in range(len(items[0][0])))
                 for i in range(len(items[0])))


def scale(q, a):
    return tuple(tuple(q * x for x in row) for row in a)


def transpose(a):
    return tuple(zip(*a))


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def hs(a, b):
    return trace(mul(transpose(a), b))


def pinching(a, projectors):
    return add(*(mul(mul(p, a), p) for p in projectors))


def cycle_checks():
    group = "ciclo_orientacion_y_coborde"
    n = 9
    v = (Q(2), Q(1))
    lam = Q(3, 7)
    potential = [(Q(k * (n - k)), Q(k * k)) for k in range(n)]
    edges = [tuple(potential[(k + 1) % n][i] - potential[k][i] + lam * v[i]
                   for i in range(2)) for k in range(n)]
    u = tuple(sum(e[i] for e in edges) / n for i in range(2))
    require(u == tuple(lam * x for x in v), group, "modo armónico")
    recovered = [(Q(0), Q(0))]
    for k in range(n):
        recovered.append(tuple(recovered[-1][i] + edges[k][i] - u[i]
                               for i in range(2)))
    require(recovered[n] == recovered[0], group, "cierre de potencial")
    for k in range(n):
        require(recovered[k] == potential[k], group, "recuperación del potencial")
        require(tuple(recovered[(k + 1) % n][i] - recovered[k][i] + u[i]
                      for i in range(2)) == edges[k], group, "reconstrucción arista")
    norm2 = sum(x * x for x in v)

    def density(items):
        boundary = tuple(sum(e[i] for e in items) for i in range(2))
        return sum(boundary[i] * v[i] for i in range(2)) / (n * norm2)

    require(density([v] * n) == 1, group, "unidad residual")
    gauge = [(Q(k ** 3), Q(2 * k - k * k)) for k in range(n)]
    for epsilon in (-1, 1):
        transformed = [tuple(epsilon * edges[k][i]
                             + gauge[(k + 1) % n][i] - gauge[k][i]
                             for i in range(2)) for k in range(n)]
        require(density(transformed) == epsilon * lam, group, "covarianza orientada")


def stokes_checks():
    group = "stokes_celular"
    # Dos triángulos (0,1,2) y (0,2,3): la arista 02 se cancela.
    omega = {(0, 1): Q(2, 3), (1, 2): Q(5, 2), (0, 2): Q(7, 5),
             (2, 3): Q(-3, 2), (0, 3): Q(4, 7)}
    faces = [((0, 1, 1), (1, 2, 1), (0, 2, -1)),
             ((0, 2, 1), (2, 3, 1), (0, 3, -1))]
    boundary = {}
    for face in faces:
        for i, j, sign in face:
            boundary[i, j] = boundary.get((i, j), 0) + sign
    require(boundary[0, 2] == 0, group, "cancelación interior")
    face_sum = sum(sum(sign * omega[i, j] for i, j, sign in f) for f in faces)
    edge_sum = sum(sign * omega[e] for e, sign in boundary.items())
    require(face_sum == edge_sum, group, "emparejamiento cadena-coborde")
    potential = (Q(1), Q(4, 3), Q(-1, 2), Q(9, 5))
    exact = {e: potential[e[1]] - potential[e[0]] for e in omega}
    for face in faces:
        require(sum(sign * exact[i, j] for i, j, sign in face) == 0,
                group, "planitud exacta")


def apparatus_checks():
    group = "aparato_y_expectativa"
    records = ("r0", "r1")
    visible = {r: "mismo_resultado" for r in records}
    lifted = tuple((visible[r], r) for r in records)
    require(len(set(lifted)) == 2, group, "levantamiento inyectivo")
    iota = matrix([[1, 0], [0, 1], [0, 0], [0, 0]])
    next_iota = matrix([[0, 0], [1, 0], [0, 0], [0, 1], [0, 0]])
    partial_w = mul(next_iota, transpose(iota))
    require(mul(transpose(iota), iota) == eye(2), group, "isometría inicial")
    require(mul(transpose(next_iota), next_iota) == eye(2), group, "isometría final")
    require(mul(partial_w, iota) == next_iota, group, "cuadrado de inscripción")
    p0, p1 = unit(4, 0, 0), unit(4, 1, 1)
    complement = add(unit(4, 2, 2), unit(4, 3, 3))
    projectors = (p0, p1, complement)
    pointer = add(p0, p1)
    require(pinching(eye(4), (p0, p1)) == pointer, group, "unidad de esquina")
    require(pointer != eye(4), group, "esquina distinta de aparato")
    require(pinching(eye(4), projectors) == eye(4), group, "extensión unital")
    units = [unit(4, i, j) for i in range(4) for j in range(4)]
    retained = 0
    for a in units:
        ea = pinching(a, projectors)
        require(pinching(ea, projectors) == ea, group, "idempotencia")
        require(trace(ea) == trace(a), group, "traza")
        retained += int(ea == a)
        for b in units:
            require(hs(a, pinching(b, projectors)) == hs(ea, b),
                    group, "autoadjunción Hilbert-Schmidt")
    require(retained == 6, group, "dimensión 1+1+4 de la imagen")
    require(pinching(unit(4, 2, 3), projectors) == unit(4, 2, 3),
            group, "conservación de coherencia en complemento")
    permutation = (2, 0, 3, 1)
    u = matrix([[int(i == permutation[j]) for j in range(4)] for i in range(4)])
    conjugate = lambda a: mul(mul(u, a), transpose(u))
    conjugated_projectors = tuple(conjugate(p) for p in projectors)
    for a in units:
        require(pinching(conjugate(a), conjugated_projectors)
                == conjugate(pinching(a, projectors)), group, "covarianza unitaria")
    next_projectors = (unit(5, 1, 1), unit(5, 3, 3))
    for i in range(2):
        for j in range(2):
            a = unit(4, i, j)
            transported = mul(mul(partial_w, a), transpose(partial_w))
            rhs = mul(mul(partial_w, pinching(a, (p0, p1))), transpose(partial_w))
            require(pinching(transported, next_projectors) == rhs,
                    group, "compatibilidad del lector diagonal")


def boundary_checks():
    group = "imagen_efectiva_y_respuesta"
    boundary = {"x0": "b0", "x1": "b0", "x2": "b1"}
    response = {"x0": Q(2), "x1": Q(2), "x2": Q(3)}
    factor = {}
    for x, beta in boundary.items():
        if beta in factor:
            require(factor[beta] == response[x], group, "constancia en fibra")
        factor[beta] = response[x]
    require(set(factor) == set(boundary.values()), group, "dominio imagen efectiva")
    extension1 = dict(factor, b_exterior=Q(0))
    extension2 = dict(factor, b_exterior=Q(1))
    require(extension1 != extension2, group, "libertad exterior a la imagen")
    for x, beta in boundary.items():
        require(extension1[beta] == extension2[beta] == response[x],
                group, "extensiones con igual composición")

    # Parámetros racionales de prueba: identidades de la fórmula, no metrología.
    def eigenvalues(a, volume, clock, r=Q(7, 4), rj=Q(2, 3)):
        weight = a * r / (a * r + volume * rj)
        return (Q(6) * weight / clock ** 2, Q(6) * (1 - weight) / clock ** 2)

    original = eigenvalues(Q(2), Q(3), Q(5))
    require(all(x > 0 for x in original), group, "positividad")
    require(eigenvalues(Q(4), Q(6), Q(5)) == original,
            group, "escala común areal-volumétrica conserva respuesta")
    require(eigenvalues(Q(2), Q(3), Q(10)) == tuple(x / 4 for x in original),
            group, "variación del reloj")
    swapped = eigenvalues(Q(3), Q(2), Q(5), Q(2, 3), Q(7, 4))
    require(tuple(reversed(swapped)) == original, group, "intercambio de ternas")
    local = {"x0": "local", "x2": "local"}
    require(local["x0"] == local["x2"] and response["x0"] != response["x2"],
            group, "testigo finito de no factorización local")


def projection_checks():
    group = "defecto_cinematico_de_proyeccion"
    # Conexiones planas, pi(x)=x² y x(t)=x0+vt: a_S=2v².
    for velocity in (Q(-2), Q(0), Q(3, 2), Q(3)):
        second_derivative = 2 * velocity ** 2
        hessian_contraction = Q(2) * velocity * velocity
        require(second_derivative == hessian_contraction,
                group, "aceleración publicada de trayectoria geodésica")
    require(Q(2) * Q(1) ** 2 != Q(2) * Q(2) ** 2,
            group, "la cinemática adicional puede distinguir respuestas")


def main():
    cycle_checks()
    stokes_checks()
    apparatus_checks()
    boundary_checks()
    projection_checks()
    print(json.dumps({
        "status": "PASS_CONTROLES_FINITOS_OBSERVADOR_RESPUESTA",
        "controls": sum(COUNTS.values()),
        "groups": COUNTS,
        "arithmetic": "fractions.Fraction; exacta",
        "scope": "Identidades finitas de ciclo, aparato, imagen de borde y respuesta; no validación matemática global ni selección de estados físicos.",
        "external_inputs": False,
        "reads": ["el propio archivo para su SHA-256"],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
