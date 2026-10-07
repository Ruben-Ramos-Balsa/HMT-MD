#!/usr/bin/env python3
"""Controles finitos exactos de identidades locales del continuo HMT.

Sólo usa enteros y Fraction de la biblioteca estándar. Cada comprobación
emplea una condición explícita; ejecutar Python con -O no elimina controles.
La salida JSON describe los casos realmente ejecutados. No certifica la
construcción global del continuo, un productor TPK completo ni Weil/RH.

Procedencia matemática: propietarios 04b1, 04b2, 04b3 y desarrollos
05a--05e preservados en antecedentes/integral de este Artículo VIII.
Se contrasta la identidad de Gram bloque-diagonal correcta, no la igualdad
general con U*U que aparece en 04b2:298--303.

Ejecución desde cualquier directorio:
    python3 -I -S verificar_identidades_continuo.py
    python3 -I -S -O verificar_identidades_continuo.py
"""

from fractions import Fraction as F
from itertools import permutations, product
import argparse
import json
from pathlib import Path
import random
import sys


class CheckFailure(Exception):
    pass


class Checks:
    def __init__(self, name):
        self.name = name
        self.count = 0

    def require(self, condition, description):
        self.count += 1
        if not condition:
            raise CheckFailure(self.name + ": " + description)


def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def zero(m, n):
    return mat([[0] * n for _ in range(m)])


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br))
                 for ar, br in zip(a, b))


def scale(s, a):
    return tuple(tuple(s * x for x in row) for row in a)


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0])))
                 for i in range(len(a)))


def transpose(a):
    return tuple(zip(*a))


def mv(a, v):
    return tuple(sum(x * y for x, y in zip(row, v)) for row in a)


def va(u, v):
    return tuple(x + y for x, y in zip(u, v))


def compose_affine(after, before):
    """(C2,k2) o (C1,k1): m |-> C2 C1 m + k2 + C2 k1."""
    c2, k2 = after
    c1, k1 = before
    return mul(c2, c1), va(k2, mv(c2, k1))


def affine_checks(ch):
    alphabet = (
        (mat([[1, 1], [0, 1]]), (F(1), F(-1))),
        (mat([[0, -1], [1, 0]]), (F(-2), F(3))),
        (mat([[1, 0], [1, 1]]), (F(0), F(2))),
    )
    identity = (eye(2), (F(0), F(0)))

    def fold(word):
        result = identity
        for letter in word:
            result = compose_affine(alphabet[letter], result)
        return result

    words = 0
    splittings = 0
    for length in range(5):
        for word in product(range(len(alphabet)), repeat=length):
            words += 1
            total = fold(word)
            for initial in ((F(0), F(0)), (F(2), F(-3)), (F(1, 3), F(-2, 5))):
                direct = initial
                for letter in word:
                    c, k = alphabet[letter]
                    direct = va(mv(c, direct), k)
                ch.require(direct == va(mv(total[0], initial), total[1]),
                           "la iteración y la forma afín discrepan")
            for i in range(length + 1):
                left, right = fold(word[:i]), fold(word[i:])
                ch.require(compose_affine(right, left) == total,
                           "cociclo bajo concatenación")
                for j in range(i, length + 1):
                    a, b, c = fold(word[:i]), fold(word[i:j]), fold(word[j:])
                    l = compose_affine(c, compose_affine(b, a))
                    r = compose_affine(compose_affine(c, b), a)
                    ch.require(l == r == total, "asociatividad afín")
                    splittings += 1
    return {"palabras": words, "longitud_maxima": 4,
            "particiones_en_tres_segmentos": splittings,
            "dominio": "tres transportes afines explícitos sobre Q^2"}


def clock_checks(ch):
    def step(state):
        w, r = state
        return w + (r + 1) // 9, (r + 1) % 9

    cases = 0
    for w, r in product(range(5), range(9)):
        state = (w, r)
        for n in range(37):
            ch.require(state == (w + (r + n) // 9, (r + n) % 9),
                       "fórmula explícita del odómetro")
            if n == 9:
                ch.require(state == (w + 1, r), "sigma_9^9")
                ch.require(state != (w, r), "el retorno reinició el estado")
            state = step(state)
            cases += 1
    return {"estados_iniciales": 45, "iteraciones_maximas": 36,
            "casos_de_formula_iterada": cases}


def balance_checks(ch):
    weights = (
        (F(1, 3), F(2, 3)),
        (F(2, 7), F(5, 7)),
        (F(1, 6), F(1, 3), F(1, 2)),
        (F(1, 7), F(2, 7), F(4, 7)),
        (F(1, 10), F(2, 10), F(3, 10), F(4, 10)),
    )
    cases = 0
    values = (-3, -1, 0, 2, 5)
    for p in weights:
        ch.require(sum(p) == 1 and all(w > 0 for w in p),
                   "pesos positivos normalizados")
        ch.require(len(set(p)) > 1, "el caso debe ser no uniforme")
        for b in product(values, repeat=len(p)):
            mean = sum(w * v for w, v in zip(p, b))
            mean_abs = sum(w * abs(v) for w, v in zip(p, b))
            kappa = (mean_abs - abs(mean)) / 2
            plus = sum(w * max(v, 0) for w, v in zip(p, b))
            minus = sum(w * max(-v, 0) for w, v in zip(p, b))
            ch.require(kappa >= 0, "cancelación negativa")
            ch.require(plus == max(mean, 0) + kappa, "E b+ = (E b)+ + kappa")
            ch.require(minus == max(-mean, 0) + kappa, "E b- = (E b)- + kappa")
            ch.require(plus - minus == mean, "conservación firmada")
            ch.require(plus + minus == abs(mean) + 2 * kappa,
                       "registro de cancelación total")
            cases += 1
    p, b = (F(1, 3), F(2, 3)), (-1, 2)
    mean = sum(w * v for w, v in zip(p, b))
    kappa = (sum(w * abs(v) for w, v in zip(p, b)) - abs(mean)) / 2
    ch.require((mean, kappa) == (F(1), F(1, 3)), "ejemplo racional explícito")
    return {"familias_de_pesos_no_uniformes": len(weights), "vectores": cases,
            "ejemplo": {"pesos": ["1/3", "2/3"], "b": [-1, 2],
                        "E_b": "1", "kappa": "1/3"}}


def residue_vectors(modulus, width, cap=10000):
    """Enumeración exhaustiva cuando cabe; muestra determinista declarada si no."""
    total = modulus ** width
    if total <= cap:
        return product(range(modulus), repeat=width), "exhaustivo", total
    rng = random.Random(9102026 + modulus * 100 + width)
    sample = {(0,) * width, (modulus - 1,) * width}
    for i in range(width):
        sample.add(tuple(int(i == j) for j in range(width)))
    while len(sample) < 512:
        sample.add(tuple(rng.randrange(modulus) for _ in range(width)))
    return iter(sorted(sample)), "muestra_determinista", len(sample)


def rectangle_checks(ch):
    coverage = []
    for precision in (1, 2, 3):
        modulus = 3 ** precision
        for rows, cols in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2)):
            def kappa(u, v):
                return tuple(tuple((u[i] - v[j]) % modulus for j in range(cols))
                             for i in range(rows))

            def delta(w):
                return tuple((w[i][j] - w[i][0] - w[0][j] + w[0][0]) % modulus
                             for i in range(1, rows) for j in range(1, cols))

            vectors, mode_uv, count_uv = residue_vectors(modulus, rows + cols)
            for vector in vectors:
                u, v = vector[:rows], vector[rows:]
                w = kappa(u, v)
                ch.require(all(x == 0 for x in delta(w)), "delta kappa != 0")
                if all(x == 0 for row in w for x in row):
                    ch.require(len(set(vector)) == 1, "núcleo de kappa no diagonal")
                recovered_u = tuple(w[i][0] for i in range(rows))
                recovered_v = tuple((w[0][0] - w[0][j]) % modulus
                                    for j in range(cols))
                ch.require(kappa(recovered_u, recovered_v) == w,
                           "reconstrucción de la imagen de kappa")

            vectors, mode_w, count_w = residue_vectors(modulus, rows * cols)
            kernel_checked = 0
            for vector in vectors:
                w = tuple(tuple(vector[i * cols + j] for j in range(cols))
                          for i in range(rows))
                if all(x == 0 for x in delta(w)):
                    u = tuple(w[i][0] for i in range(rows))
                    v = tuple((w[0][0] - w[0][j]) % modulus for j in range(cols))
                    ch.require(kappa(u, v) == w, "ker delta no reconstruido")
                    kernel_checked += 1

            out_width = (rows - 1) * (cols - 1)
            targets, mode_d, count_d = residue_vectors(modulus, out_width)
            for target in targets:
                w = [[0] * cols for _ in range(rows)]
                index = 0
                for i in range(1, rows):
                    for j in range(1, cols):
                        w[i][j] = target[index]
                        index += 1
                ch.require(delta(w) == target, "sección de delta / sobreyectividad")
            if rows > 1 and cols > 1:
                bad = [[0] * cols for _ in range(rows)]
                bad[1][1] = 1
                ch.require(any(x != 0 for x in delta(bad)),
                           "la prueba negativa aceptó una matriz fuera de ker delta")
            coverage.append({"N": precision, "modulo": modulus,
                             "rectangulo": [rows, cols],
                             "uv": {"modo": mode_uv, "casos": count_uv},
                             "w": {"modo": mode_w, "casos": count_w,
                                   "casos_en_ker_delta": kernel_checked},
                             "seccion_delta": {"modo": mode_d, "casos": count_d}})
    return {"cobertura": coverage,
            "nota": "Los controles finitos acompañan la prueba general de exactitud; no la sustituyen."}


def local_complex(c):
    """Base (f,e,b,r,g), grados (2,1,1,1,0), diferencial de grado -1.

    El propietario histórico usa (1,0,0,0,-1). Aquí se explicita el
    desplazamiento de grados utilizado en el capítulo 05 del artículo VIII.
    """
    d = [[0] * 5 for _ in range(5)]
    d[1][0], d[2][0], d[4][1], d[4][2] = 3 * c, 1, 1, -3 * c
    return mat(d)


def psi(c, new_c):
    p = [list(row) for row in eye(5)]
    p[1][2] = F(3 * (new_c - c))
    return mat(p)


def complex_checks(ch):
    params = tuple(range(-6, 7))
    for c in params:
        d = local_complex(c)
        ch.require(mul(d, d) == zero(5, 5), "diferencial al cuadrado")
        for new_c in params:
            p = psi(c, new_c)
            ch.require(mul(local_complex(new_c), p) == mul(p, d),
                       "naturalidad del diferencial bajo cambio de c")
            ch.require(mul(psi(new_c, c), p) == eye(5), "inversa del transporte local")
            for third_c in (-4, 0, 3):
                ch.require(mul(psi(new_c, third_c), p) == psi(c, third_c),
                           "composición functorial local")
        for v in (-3, -1, 0, 2):
            zminus = (F(0), F(0), F(0), F(1), F(0))
            zplus = (F(0), F(3 * c * v), F(v), F(1), F(0))
            filler = (F(-v), F(0), F(0), F(0), F(0))
            ch.require(mv(d, zminus) == (F(0),) * 5, "z- cerrado")
            ch.require(mv(d, zplus) == (F(0),) * 5, "z+ cerrado")
            ch.require(mv(d, filler) == va(zminus, tuple(-x for x in zplus)),
                       "relleno explícito")
    return {"valores_c": list(params), "pares_c": len(params) ** 2,
            "terceros_parametros": [-4, 0, 3],
            "base": ["f", "e", "b", "r", "g"],
            "nota": "Igualdades sobre Z; también válidas tras reducción módulo 3^N."}


def contraction_checks(ch):
    """Retracción explícita a A[r] en grado 1; no elimina memoria de cadena."""
    h_raw = [[0] * 5 for _ in range(5)]
    h_raw[1][4], h_raw[0][2] = 1, 1
    h = mat(h_raw)
    inclusion = mat([[0], [0], [0], [1], [0]])
    projection = mat([[0, 0, 0, 1, 0]])
    ip = mul(inclusion, projection)
    target = add(eye(5), scale(-1, ip))
    expected_images = {0: (0, 0, 0, 0, 0), 1: (0, 0, 0, 0, 0),
                       2: (1, 0, 0, 0, 0), 3: (0, 0, 0, 0, 0),
                       4: (0, 1, 0, 0, 0)}
    for j, expected in expected_images.items():
        basis = tuple(F(int(i == j)) for i in range(5))
        ch.require(mv(h, basis) == expected, "acción de h en un generador")
    ch.require(mul(projection, inclusion) == eye(1), "p iota = I")
    ch.require(mul(h, h) == zero(5, 5), "h^2 = 0")
    ch.require(mul(projection, h) == zero(1, 5), "p h = 0")
    ch.require(mul(h, inclusion) == zero(5, 1), "h iota = 0")
    for c in range(-6, 7):
        d = local_complex(c)
        ch.require(add(mul(d, h), mul(h, d)) == target, "d h + h d = I - iota p sobre Z")
        ch.require(mul(projection, d) == zero(1, 5), "p es mapa de complejos")
        ch.require(mul(d, inclusion) == zero(5, 1), "iota es mapa de complejos")

    def reduce_matrix(a, modulus):
        for row in a:
            ch.require(all(x.denominator == 1 for x in row), "reducción de matriz entera")
        return tuple(tuple(int(x) % modulus for x in row) for row in a)

    modular_cases = 0
    for n in (1, 2, 3):
        modulus = 3 ** n
        for c in range(modulus):
            d = local_complex(c)
            ch.require(reduce_matrix(add(mul(d, h), mul(h, d)), modulus)
                       == reduce_matrix(target, modulus),
                       "contracción sobre Z/3^N")
            modular_cases += 1

    # Para cada ciclo de grado 1 módulo 3, la parte sin r es d h del ciclo.
    cycle_cases = 0
    for c, a, b, r in product(range(3), repeat=4):
        vector = (F(0), F(a), F(b), F(r), F(0))
        d = local_complex(c)
        if all(int(x) % 3 == 0 for x in mv(d, vector)):
            reduced_cycle = va(vector, tuple(-x for x in mv(ip, vector)))
            boundary = mv(d, mv(h, vector))
            ch.require(tuple(int(x) % 3 for x in reduced_cycle)
                       == tuple(int(x) % 3 for x in boundary),
                       "representante homológico r y frontera explícita")
            cycle_cases += 1
    return {"base": ["f", "e", "b", "r", "g"], "grados": [2, 1, 1, 1, 0],
            "h": {"g": "e", "b": "f", "f": "0", "e": "0", "r": "0"},
            "valores_enteros_c": list(range(-6, 7)),
            "casos_modulares_c_exhaustivos": modular_cases,
            "ciclos_grado_1_comprobados_modulo_3": cycle_cases,
            "identidad": "d h + h d = I - iota p; p iota = I",
            "consecuencia_algebraica_de_la_identidad": "H0=H2=0, H1=A[r] en la graduación indicada",
            "alcance": "La retracción homológica no identifica ni elimina los ledgers y rutas de cadena."}


def publication_checks(ch):
    def zplus(c, v):
        return (F(0), F(3 * c * v), F(v), F(1), F(0))

    def coherence(v, new_v):
        return (F(new_v - v), F(0), F(0), F(0), F(0))

    def filler(v):
        return (F(-v), F(0), F(0), F(0), F(0))

    cases = 0
    triples = 0
    zminus = (F(0), F(0), F(0), F(1), F(0))
    for c, new_c, v, new_v in product((-4, 0, 3), (-2, 1, 5), (-3, 0, 2), (-1, 1, 4)):
        transport = psi(c, new_c)
        k = coherence(v, new_v)
        difference = va(zplus(new_c, new_v), tuple(-x for x in mv(transport, zplus(c, v))))
        ch.require(difference == mv(local_complex(new_c), k),
                   "zplus(c',v') - Psi zplus(c,v) = d K")
        ch.require(mv(transport, zminus) == zminus, "naturalidad estricta de zminus")
        ch.require(va(filler(new_v), tuple(-x for x in mv(transport, filler(v))))
                   == tuple(-x for x in k), "hstar' - Psi hstar = -K")
        cases += 1
        for third_c, third_v in product((-1, 2), (-2, 3)):
            composed = va(coherence(new_v, third_v), mv(psi(new_c, third_c), k))
            ch.require(composed == coherence(v, third_v), "K_betaalpha = K_beta + Psi_beta K_alpha")
            ch.require(mul(psi(new_c, third_c), transport) == psi(c, third_c),
                       "transporte usado por el cociclo")
            triples += 1
    return {"pares_de_publicaciones": cases, "composiciones_en_tres_residencias": triples,
            "coherencia": "K=(v'-v)f en el complejo de llegada",
            "igualdad": "zplus(c',v') - Psi(c,c')zplus(c,v) = d K",
            "nota": "Prueba finita exacta sobre Z de naturalidad homotópica, no igualdad de cadenas."}


def projector(bits):
    return mat([[int(i == j) * bits[i] for j in range(len(bits))]
                for i in range(len(bits))])


def gram_parts(u, input_bits, output_bits):
    p, pp = projector(input_bits), projector(output_bits)
    q, qp = add(eye(len(input_bits)), scale(-1, p)), add(eye(len(output_bits)), scale(-1, pp))
    a = add(mul(mul(pp, u), p), mul(mul(qp, u), q))
    eta = add(mul(mul(qp, u), p), mul(mul(pp, u), q))
    full = mul(transpose(u), u)
    lhs = add(mul(transpose(a), a), mul(transpose(eta), eta))
    block = add(mul(mul(p, full), p), mul(mul(q, full), q))
    return a, eta, full, lhs, block


def gram_checks(ch):
    cases = 0

    def test(u, input_bits, output_bits, isometry=False):
        nonlocal cases
        a, eta, full, lhs, block = gram_parts(u, input_bits, output_bits)
        ch.require(add(a, eta) == u, "U = A + eta")
        ch.require(lhs == block, "identidad de Gram bloque-diagonal")
        if isometry:
            ch.require(full == eye(len(input_bits)), "caso etiquetado isométrico no lo es")
            ch.require(lhs == eye(len(input_bits)), "especialización isométrica")
        cases += 1

    for entries in product(range(-2, 3), repeat=4):
        test(mat([entries[:2], entries[2:]]), (1, 0), (1, 0))
    rng = random.Random(9102026)
    for _ in range(80):
        u = mat([[F(rng.randrange(-5, 6), rng.randrange(1, 5))
                  for _ in range(2)] for _ in range(3)])
        test(u, (1, 0), (1, 0, 1))
    isometries = 0
    for n in (2, 3):
        for perm in permutations(range(n)):
            for signs in product((-1, 1), repeat=n):
                u = mat([[signs[j] * int(i == perm[j]) for j in range(n)]
                         for i in range(n)])
                bits = tuple(int(i % 2 == 0) for i in range(n))
                test(u, bits, bits, isometry=True)
                isometries += 1
    rotation = mat([[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]])
    test(rotation, (1, 0), (1, 0), isometry=True)
    isometries += 1

    bad = mat([[1, 1], [0, 0]])
    _, _, full, lhs, block = gram_parts(bad, (1, 0), (1, 0))
    ch.require(lhs == block == eye(2), "cálculo del contraejemplo")
    ch.require(lhs != full, "contraejemplo a la igualdad general con U*U")

    u1, u2 = scale(F(1, 2), eye(2)), scale(F(3, 2), eye(2))
    mean = add(scale(F(5, 8), mul(transpose(u1), u1)),
               scale(F(3, 8), mul(transpose(u2), u2)))
    ch.require(mean == eye(2), "promedio exacto de Gram")
    ch.require(mul(transpose(u1), u1) != eye(2)
               and mul(transpose(u2), u2) != eye(2),
               "isometría del promedio no obliga a isometría de cada transporte")
    return {"matrices_2x2_enteras_exhaustivas": 625,
            "matrices_3x2_racionales_muestra_determinista": 80,
            "isometrias_exactas": isometries, "casos_de_identidad": cases,
            "dominio": "matrices reales racionales; adjunto = traspuesta",
            "contraejemplo": {"U": [[1, 1], [0, 0]],
                               "U_adjunto_U": [[1, 1], [1, 1]],
                               "Gram_bloque_diagonal": [[1, 0], [0, 1]]},
            "promedio_no_equivalente_a_isometrias_individuales": {
                "U1": "(1/2)I", "U2": "(3/2)I", "pesos": ["5/8", "3/8"],
                "promedio_Gram": "I"}}


def horizon_checks(ch):
    u = mat([[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]])
    a, eta, full, _, _ = gram_parts(u, (1, 0), (1, 0))
    ch.require(full == eye(2), "rotación racional isométrica")
    ch.require(a == scale(F(3, 5), eye(2)), "A = (3/5)I")
    ch.require(eta == mat([[0, F(-4, 5)], [F(4, 5), 0]]), "eta cruzada")
    eta_gram = mul(transpose(eta), eta)
    ch.require(eta_gram == scale(F(16, 25), eye(2)), "Gram de eta")
    details = []
    for n in range(1, 13):
        f_n = scale(F(3, 5) ** n, eye(2))
        f_next = mul(a, f_n)
        terminal = mul(transpose(f_n), f_n)
        next_terminal = mul(transpose(f_next), f_next)
        loss = mul(mul(transpose(f_n), eta_gram), f_n)
        difference = add(terminal, scale(-1, next_terminal))
        ch.require(difference == loss, "T_N - T_(N+1) = F_N* eta* eta F_N")
        ch.require(terminal == scale(F(9, 25) ** n, eye(2)), "terminal exacto")
        ch.require(loss == scale(F(16, 25) * F(9, 25) ** n, eye(2)), "pérdida exacta")

        # Xi_N empila todas las salidas eta F_k y el terminal F_N.
        blocks = [mul(eta, scale(F(3, 5) ** k, eye(2))) for k in range(n)] + [f_n]
        xi = tuple(row for block in blocks for row in block)
        pi_terminal = projector((0,) * (2 * n) + (1, 1))
        first_moment = mul(transpose(xi), xi)
        second_moment = mul(mul(transpose(xi), pi_terminal), xi)
        ch.require(first_moment == eye(2), "primer momento Xi_N* Xi_N = I")
        ch.require(second_moment == terminal, "segundo momento Xi_N* Pi_N Xi_N = T_N")

        # Con R=I fijo, R* T_N R es T_N y cambia estrictamente con N.
        r = eye(2)
        current_second = mul(mul(transpose(r), terminal), r)
        next_second = mul(mul(transpose(r), next_terminal), r)
        ch.require(current_second != next_second, "el segundo Gram no es constante con R=I")
        ch.require(mul(mul(eta, f_n), r) != zero(2, 2),
                   "la obstrucción de horizonte eta F_N R es no nula")
        details.append({"N": n, "T_N_factor": str(F(9, 25) ** n),
                        "T_N_menos_T_N1_factor": str(F(16, 25) * F(9, 25) ** n)})
    return {"horizontes": list(range(1, 13)), "U": [["3/5", "-4/5"], ["4/5", "3/5"]],
            "P": [[1, 0], [0, 0]], "R": "I fijo", "A": "(3/5)I",
            "primer_Gram": "I", "segundo_Gram": "T_N=(9/25)^N I, no constante",
            "evaluaciones_exactas": details,
            "alcance": "Ejemplo racional finito de dependencia de horizonte; no identificación con columnas de Weil."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, help="Guardar el resultado focal JSON, sin certificar el artículo completo")
    args = parser.parse_args()

    def emit(report):
        encoded = json.dumps(report, ensure_ascii=False, indent=2)
        if args.receipt:
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(encoded + "\n", encoding="utf-8")
        print(encoded)

    report = {
        "schema": "HMT_VIII_IDENTIDADES_LOCALES_EXACTAS_V1",
        "alcance": "Controles finitos exactos de identidades locales sobre datos explícitos.",
        "no_certifica": ["construcción global del continuo", "productor TPK desde semillas",
                         "identificación con formas de Weil", "hipótesis de Riemann"],
        "aritmetica": "enteros y fractions.Fraction; sin redondeo",
        "python": sys.version.split()[0], "optimization_level": sys.flags.optimize,
        "grupos": [],
    }
    groups = (
        ("cociclo_afin", affine_checks), ("retorno_nonadico", clock_checks),
        ("balance_condicional", balance_checks), ("secuencia_rectangular", rectangle_checks),
        ("complejo_local", complex_checks), ("gram_bloque_diagonal", gram_checks),
        ("contraccion_y_homologia_local", contraction_checks),
        ("publicaciones_y_cociclo", publication_checks),
        ("principio_de_horizonte", horizon_checks),
    )
    for name, run in groups:
        ch = Checks(name)
        try:
            details = run(ch)
        except Exception as exc:
            report["grupos"].append({"nombre": name, "estado": "FAIL",
                                      "comprobaciones_ejecutadas": ch.count,
                                      "error": type(exc).__name__ + ": " + str(exc)})
            report["status"] = "FAIL_IDENTIDADES_LOCALES_CONTINUO"
            emit(report)
            return 1
        report["grupos"].append({"nombre": name, "estado": "PASS_FOCAL",
                                  "comprobaciones_ejecutadas": ch.count,
                                  "detalle": details})
    report["status"] = "PASS_IDENTIDADES_LOCALES_CONTINUO_FINITO"
    report["comprobaciones_totales"] = sum(g["comprobaciones_ejecutadas"]
                                            for g in report["grupos"])
    emit(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
