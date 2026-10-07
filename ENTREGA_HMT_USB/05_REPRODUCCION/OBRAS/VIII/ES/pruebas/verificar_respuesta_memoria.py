#!/usr/bin/env python3
"""Controles racionales de la respuesta variacional a transporte de rutas.

Antecedente: 16_tres_hojas_variacion.tex, bloque de energia y refinamiento,
en el corpus conservado de respuesta modular. La energia preexiste; este
certificado comprueba una formalizacion de su diferencial de primer orden.

No genera los datos de ruta APP--TRIT--TPK ni selecciona una corriente material
de espin o una amplitud cosmologica. Los datos racionales son casos de prueba,
no entradas metrologicas ni constantes atribuidas al generador HMT.

Biblioteca estandar; aritmetica Fraction, sin tolerancias ni assert. La salida
normal es exclusivamente JSON por stdout. Solo --receipt ARCHIVO.json escribe
un recibo; sin esa opcion no se modifica ningun archivo. Compatible con -I -S
-B y -O. No importa ni ejecuta propietarios historicos.
"""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


def matrix(rows):
    result = [[F(x) for x in row] for row in rows]
    if not result or not result[0] or any(len(r) != len(result[0]) for r in result):
        raise ValueError("Matriz vacia o no rectangular")
    return result


def shape(a):
    return len(a), len(a[0])


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def identity(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def transpose(a):
    return [list(row) for row in zip(*a)]


def scale(q, a):
    return [[F(q) * x for x in row] for row in a]


def add(a, b):
    if shape(a) != shape(b):
        raise ValueError("Suma de matrices de tipos distintos")
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    if len(a[0]) != len(b):
        raise ValueError("Composicion de matrices de tipos incompatibles")
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def hstack(a, b):
    if len(a) != len(b):
        raise ValueError("Concatenacion horizontal incompatible")
    return [ra + rb for ra, rb in zip(a, b)]


def vstack(a, b):
    if len(a[0]) != len(b[0]):
        raise ValueError("Concatenacion vertical incompatible")
    return [row[:] for row in a + b]


def blockdiag(a, b):
    an, am = shape(a)
    bn, bm = shape(b)
    return vstack(hstack(a, zeros(an, bm)), hstack(zeros(bn, am), b))


def trace(a):
    if len(a) != len(a[0]):
        raise ValueError("Traza de una matriz no cuadrada")
    return sum((a[i][i] for i in range(len(a))), F(0))


def pairing(x, y):
    if len(x[0]) != 1 or len(y[0]) != 1:
        raise ValueError("El emparejamiento requiere vectores columna")
    return mul(transpose(x), y)[0][0]


def determinant(a):
    if len(a) != len(a[0]):
        raise ValueError("Determinante de una matriz no cuadrada")
    b = [row[:] for row in a]
    result = F(1)
    for col in range(len(b)):
        pivot = next((i for i in range(col, len(b)) if b[i][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            b[col], b[pivot] = b[pivot], b[col]
            result = -result
        value = b[col][col]
        result *= value
        for i in range(col + 1, len(b)):
            factor = b[i][col] / value
            for j in range(col + 1, len(b)):
                b[i][j] -= factor * b[col][j]
            b[i][col] = F(0)
    return result


def positive_definite(a):
    return a == transpose(a) and all(
        determinant([row[:n] for row in a[:n]]) > 0
        for n in range(1, len(a) + 1)
    )


def commutator(a, b):
    return sub(mul(a, b), mul(b, a))


def conjugate(g, a):
    # Todas las matrices g utilizadas aqui son ortogonales: g^{-1}=g^T.
    return mul(mul(g, a), transpose(g))


def residual(u, source, target):
    return sub(target, mul(u, source))


def energy(u, w, source, target):
    r = residual(u, source, target)
    return pairing(r, mul(w, r))


def current(u, w, source, target, a):
    r = residual(u, source, target)
    return -2 * pairing(r, mul(w, mul(a, mul(u, source))))


def representative(u, w, source, target):
    v = mul(u, source)
    r = residual(u, source, target)
    return sub(mul(mul(v, transpose(r)), w), mul(mul(w, r), transpose(v)))


def general_variation(u, w, source, target, a, ds, dt, dw):
    r = residual(u, source, target)
    dr = sub(sub(dt, mul(u, ds)), mul(a, mul(u, source)))
    return 2 * pairing(r, mul(w, dr)) + pairing(r, mul(dw, r))


# Polinomios matriciales: se conserva cada coeficiente de epsilon, sin usar
# la formula del diferencial. Los jets U+epsilon A U son tangentes a O(n);
# no se afirma que ese polinomio lineal sea ortogonal a orden dos o superior.
def polynomial_add(a, b):
    if shape(a[0]) != shape(b[0]):
        raise ValueError("Suma de polinomios matriciales incompatible")
    z = zeros(*shape(a[0]))
    return [add(a[i] if i < len(a) else z, b[i] if i < len(b) else z)
            for i in range(max(len(a), len(b)))]


def polynomial_sub(a, b):
    return polynomial_add(a, [scale(-1, x) for x in b])


def polynomial_mul(a, b):
    result = [zeros(len(a[0]), len(b[0][0]))
              for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] = add(result[i + j], mul(x, y))
    return result


def polynomial_energy(u, w, source, target, du, dw, ds, dt):
    r = polynomial_sub([target, dt], polynomial_mul([u, du], [source, ds]))
    rt = [transpose(x) for x in r]
    return [a[0][0] for a in polynomial_mul(rt, polynomial_mul([w, dw], r))]


def householder(v):
    return sub(identity(len(v)), scale(2 / pairing(v, v), mul(v, transpose(v))))


def rational_cases():
    cases = []
    for n, count in ((2, 4), (3, 3)):
        for k in range(count):
            hs = householder(matrix([[F(i + 1, k + 2)] for i in range(n)]))
            ht = householder(matrix([[F((-1) ** i * (i + k + 2), i + 1)]
                                     for i in range(n)]))
            u = mul(hs, ht)
            c = matrix([[F((i + 1) * (j + k + 2) + int(i == j), i + j + 2)
                         for j in range(n)] for i in range(n)])
            w = add(mul(transpose(c), c), scale(F(k + 1, 3), identity(n)))
            a = matrix([[F((j - i) * (k + 1), i + j + 1)
                         for j in range(n)] for i in range(n)])
            source = matrix([[F(i + k + 1, i + 2)] for i in range(n)])
            target = matrix([[F((-1) ** i * (i + 2 * k + 3), k + 2)]
                             for i in range(n)])
            ds = matrix([[F((-1) ** (i + 1) * (k + 1), i + 1)] for i in range(n)])
            dt = matrix([[F(i + 2, k + 3)] for i in range(n)])
            b = matrix([[F((i + 1) * (j + 2), k + i + j + 2)
                         for j in range(n)] for i in range(n)])
            dw = add(b, transpose(b))
            cases.append(("dimension_%d_caso_%d" % (n, k),
                          u, w, source, target, a, ds, dt, dw, hs, ht))
    return cases


class CheckFailure(ArithmeticError):
    pass


def run_checks():
    checks = []

    def require(name, condition, category):
        if not condition:
            raise CheckFailure(name)
        checks.append({"name": name, "category": category, "pass": True})

    cases = rational_cases()
    sum_coefficient, sum_current = F(0), F(0)
    for name, u, w, source, target, a, ds, dt, dw, gs, gt in cases:
        n = len(u)
        z, zv = zeros(n, n), zeros(n, 1)
        ident = identity(n)
        check = lambda suffix, condition, category="identidad": require(
            name + ":" + suffix, condition, category)
        check("transporte_ortogonal", mul(transpose(u), u) == ident, "dominio")
        check("peso_positivo", positive_definite(w), "dominio")
        check("generador_antisimetrico", transpose(a) == scale(-1, a), "dominio")
        du = mul(a, u)
        check("jet_tangente_ortogonal",
              add(mul(transpose(du), u), mul(transpose(u), du)) == z, "dominio")
        p = polynomial_energy(u, w, source, target, du, z, zv, zv)
        j = current(u, w, source, target, a)
        check("coeficiente_constante", p[0] == energy(u, w, source, target))
        check("coeficiente_epsilon_corriente", p[1] == j)
        sum_coefficient += p[1]
        sum_current += j
        rep = representative(u, w, source, target)
        check("representante_antisimetrico", transpose(rep) == scale(-1, rep))
        check("representante_hilbert_schmidt", trace(mul(transpose(rep), a)) == j)
        check("linealidad_real", current(u, w, source, target, scale(F(7, 3), a))
              == F(7, 3) * j)
        another = matrix([[F((j - i) * (i + j + 2), (i + 1) * (j + 1))
                           for j in range(n)] for i in range(n)])
        check("aditividad", current(u, w, source, target, add(a, another))
              == j + current(u, w, source, target, another))

        # Transformacion de calibre fija, distinta en origen y destino.
        up = mul(mul(gt, u), transpose(gs))
        wp, ap = conjugate(gt, w), conjugate(gt, a)
        sp, tp = mul(gs, source), mul(gt, target)
        check("gauges_ortogonales",
              mul(transpose(gs), gs) == ident and mul(transpose(gt), gt) == ident,
              "dominio")
        check("calibre_residuo", residual(up, sp, tp) == mul(gt, residual(u, source, target)))
        check("calibre_energia", energy(up, wp, sp, tp) == p[0])
        check("calibre_covector", current(up, wp, sp, tp, ap) == j)
        check("calibre_representante", representative(up, wp, sp, tp) == conjugate(gt, rep))

        # Inversion: el peso inverso depende del transporte variado.
        ui = transpose(u)
        wi = conjugate(ui, w)
        ai = scale(-1, conjugate(ui, a))
        dwi = conjugate(ui, commutator(w, a))
        r = residual(u, source, target)
        ri = residual(ui, target, source)
        ji = current(ui, wi, target, source, ai)
        correction = pairing(ri, mul(dwi, ri))
        check("inversion_residuo", ri == scale(-1, mul(ui, r)))
        check("inversion_energia", energy(ui, wi, target, source) == p[0])
        check("inversion_jet", mul(ai, ui) == transpose(du))
        check("inversion_derivada_peso",
              dwi == add(mul(mul(transpose(du), w), u), mul(mul(ui, w), du)))
        check("inversion_covector_parcial",
              ji == j - 2 * pairing(r, mul(w, mul(a, r))))
        check("inversion_peso_compensador",
              correction == pairing(r, mul(commutator(w, a), r)))
        pi = polynomial_energy(ui, wi, target, source, mul(ai, ui), dwi, zv, zv)
        check("inversion_diferencial_total", pi[1] == ji + correction == j)

        ws = scale(F(2 * n + 1, 3), ident)
        wsi = conjugate(ui, ws)
        js = current(u, ws, source, target, a)
        check("peso_escalar_conmuta", commutator(ws, a) == z)
        check("inversion_escalar", current(ui, wsi, target, source, ai) == js)
        check("imparidad_covector_escalar",
              current(ui, wsi, target, source, conjugate(ui, a)) == -js)

        # Kx=(x,x): isometria PONDERADA, no isometria euclidea.
        kmap = vstack(ident, ident)
        jmap = blockdiag(kmap, kmap)
        uf, af = blockdiag(u, u), blockdiag(a, a)
        wf = blockdiag(scale(F(1, 2), w), scale(F(1, 2), w))
        sf, tf = mul(kmap, source), mul(kmap, target)
        dc = hstack(scale(-1, u), ident)
        df = hstack(scale(-1, uf), identity(2 * n))
        dotdc = hstack(scale(-1, du), z)
        dotdf = hstack(scale(-1, mul(af, uf)), zeros(2 * n, 2 * n))
        check("refinamiento_isometria_ponderada", mul(mul(transpose(kmap), wf), kmap) == w)
        check("refinamiento_no_isometria_euclidea", mul(transpose(kmap), kmap) == scale(2, ident))
        check("refinamiento_entrelazado_D", mul(df, jmap) == mul(kmap, dc))
        check("refinamiento_entrelazado_dotD", mul(dotdf, jmap) == mul(kmap, dotdc))
        check("refinamiento_energia", energy(uf, wf, sf, tf) == p[0])
        check("refinamiento_corriente", current(uf, wf, sf, tf, af) == j)
        pf = polynomial_energy(uf, wf, sf, tf, mul(af, uf), zeros(2 * n, 2 * n),
                               zeros(2 * n, 1), zeros(2 * n, 1))
        check("refinamiento_coeficiente_epsilon", pf[1] == p[1])
        # El peso sin 1/2 conserva una escala doble, no la identidad pedida.
        check("sin_normalizacion_factor_dos",
              energy(uf, blockdiag(w, w), sf, tf) == 2 * p[0] and p[0] != 0,
              "control_negativo")

        pg = polynomial_energy(u, w, source, target, du, dw, ds, dt)
        dg = general_variation(u, w, source, target, a, ds, dt, dw)
        check("variacion_general", pg[1] == dg)
        check("variacion_general_calibre",
              general_variation(up, wp, sp, tp, ap, mul(gs, ds), mul(gt, dt),
                                conjugate(gt, dw)) == dg)
        dwf = blockdiag(scale(F(1, 2), dw), scale(F(1, 2), dw))
        check("refinamiento_derivada_peso", mul(mul(transpose(kmap), dwf), kmap) == dw)
        pgf = polynomial_energy(uf, wf, sf, tf, mul(af, uf), dwf,
                                mul(kmap, ds), mul(kmap, dt))
        check("refinamiento_variacion_general", pgf[1] == dg)

        # Un calibre movil exige variar campos y peso, ademas del transporte.
        xi_s, xi_t = scale(F(2, 3), a), scale(F(-3, 2), a)
        ag = sub(xi_t, conjugate(u, xi_s))
        dsg, dtg, dwg = mul(xi_s, source), mul(xi_t, target), commutator(xi_t, w)
        pgauge = polynomial_energy(u, w, source, target, mul(ag, u), dwg, dsg, dtg)
        check("calibre_movil_diferencial_total",
              pgauge[1] == general_variation(u, w, source, target, ag, dsg, dtg, dwg) == 0)

    require("suma_de_aristas_coeficiente_lineal", sum_coefficient == sum_current, "identidad")

    # Testigo negativo solicitado: la variacion del peso no puede omitirse.
    u = identity(2)
    w = matrix([[1, 0], [0, 2]])
    a = matrix([[0, -1], [1, 0]])
    source, target = matrix([[1], [0]]), matrix([[2], [1]])
    z, zv = zeros(2, 2), zeros(2, 1)
    r = residual(u, source, target)
    j = current(u, w, source, target, a)
    ji = current(u, w, target, source, scale(-1, a))
    delta_w = commutator(w, a)
    correction = pairing(r, mul(delta_w, r))
    require("testigo_inversion_menos4_menos6_mas2", (j, ji, correction) == (-4, -6, 2), "control_negativo")
    require("testigo_inversion_peso_omitido_detectado", ji != j, "control_negativo")
    require("testigo_inversion_compensada", ji + correction == j, "identidad")

    # Igualdad de energias en el punto base no implica igualdad de derivadas.
    # Ambas copias coinciden inicialmente, pero solo una recibe la variacion.
    uf = blockdiag(u, u)
    wf = blockdiag(scale(F(1, 2), w), scale(F(1, 2), w))
    sf, tf = vstack(source, source), vstack(target, target)
    af_bad = blockdiag(a, z)
    jf_bad = current(uf, wf, sf, tf, af_bad)
    require("refinamiento_base_igual_sin_tangencia", energy(uf, wf, sf, tf) == energy(u, w, source, target), "control_negativo")
    require("refinamiento_tangencia_incompatible_detectada", jf_bad == -2 and jf_bad != j, "control_negativo")

    # J(epsilon) variable: D se mantiene fijo; el termino de campo es efectivo.
    # J(epsilon)f=(f+epsilon f,f+epsilon f), no se exige preservar energia aqui.
    p_field = polynomial_energy(uf, wf, sf, tf, zeros(4, 4), zeros(4, 4), sf, tf)
    field_term = 2 * energy(uf, wf, sf, tf)
    require("J_variable_termino_campo", p_field[1] == field_term and field_term != 0, "control_negativo")
    require("J_variable_covector_solo_no_basta", current(uf, wf, sf, tf, zeros(4, 4)) != p_field[1], "control_negativo")

    # Variacion del peso solo: detecta la omision del termino r^T dot W r.
    p_weight = polynomial_energy(u, w, source, target, z, identity(2), zv, zv)
    require("peso_variable_termino_no_nulo", p_weight[1] == pairing(r, r) == 2, "control_negativo")

    # Ruta de tres factores U_gamma=U_3 U_2 U_1. Dos generadores de so(3)
    # no conmutan; se coteja el producto polinomico con la suma transportada.
    factors = [householder(matrix([[1], [1], [0]])),
               matrix([[1, 0, 0], [0, F(3, 5), F(-4, 5)],
                       [0, F(4, 5), F(3, 5)]]),
               householder(matrix([[1], [2], [3]]))]
    generators = [matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]),
                  matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]]), zeros(3, 3)]
    require("ruta_tres_factores_ortogonales", all(
        mul(transpose(x), x) == identity(3) for x in factors), "dominio")
    require("ruta_dos_variaciones_no_conmutativas",
            commutator(generators[0], generators[1]) != zeros(3, 3), "dominio")
    route_polynomial = [identity(3)]
    for factor, generator in zip(factors, generators):
        route_polynomial = polynomial_mul([factor, mul(generator, factor)], route_polynomial)
    ug, dug = route_polynomial[:2]
    suffixes = [mul(factors[2], factors[1]), factors[2], identity(3)]
    transported = [conjugate(b, ak) for b, ak in zip(suffixes, generators)]
    ag = add(add(transported[0], transported[1]), transported[2])
    require("ruta_regla_producto_y_suma_ad", mul(dug, transpose(ug)) == ag, "identidad")
    require("ruta_jet_tangente", add(mul(transpose(dug), ug), mul(transpose(ug), dug)) == zeros(3, 3), "identidad")
    wg = matrix([[2, 0, 0], [0, 3, 0], [0, 0, 5]])
    sg, tg = matrix([[1], [2], [-1]]), matrix([[-2], [1], [3]])
    rg_poly = polynomial_sub([tg], polynomial_mul(route_polynomial, [sg]))
    eg_poly = polynomial_mul([transpose(x) for x in rg_poly], polynomial_mul([wg], rg_poly))
    jg = current(ug, wg, sg, tg, ag)
    require("ruta_coeficiente_energia_producto_completo", eg_poly[1][0][0] == jg, "identidad")
    jg_rep = representative(ug, wg, sg, tg)
    contributions = []
    for k, (b, ak, transported_a) in enumerate(zip(suffixes, generators, transported), 1):
        jk = mul(mul(transpose(b), jg_rep), b)
        contribution = trace(mul(transpose(jk), ak))
        require("ruta_pullback_representante_" + str(k),
                contribution == current(ug, wg, sg, tg, transported_a), "identidad")
        contributions.append(contribution)
    require("ruta_suma_contribuciones", sum(contributions, F(0)) == jg, "identidad")
    require("ruta_dos_contribuciones_efectivas", all(x != 0 for x in contributions[:2]), "dominio")

    # Dos aristas con un peso global acoplado: q=Wr, no q_a=W_aa r_a.
    uc = blockdiag(matrix([[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]),
                   matrix([[1, 0], [0, -1]]))
    wc = matrix([[3, 1, 1, 0], [1, 4, 0, 1], [1, 0, 3, 1], [0, 1, 1, 4]])
    ac = blockdiag(a, scale(2, a))
    sc, tc = matrix([[1], [0], [2], [-1]]), matrix([[2], [1], [-1], [3]])
    rc, vc = residual(uc, sc, tc), mul(uc, sc)
    qc = mul(wc, rc)
    edge_sum = sum((-2 * pairing(qc[i:i + 2], mul(
        [row[i:i + 2] for row in ac[i:i + 2]], vc[i:i + 2])) for i in (0, 2)), F(0))
    pc = polynomial_energy(uc, wc, sc, tc, mul(ac, uc), zeros(4, 4), zeros(4, 1), zeros(4, 1))
    require("peso_global_acoplado_positivo", positive_definite(wc), "dominio")
    require("peso_global_q_Wr_suma_aristas", pc[1] == edge_sum == current(uc, wc, sc, tc, ac), "identidad")
    w_diagonal_blocks = blockdiag([row[:2] for row in wc[:2]], [row[2:] for row in wc[2:]])
    require("peso_global_acoplamientos_omitidos_detectados",
            current(uc, w_diagonal_blocks, sc, tc, ac) != edge_sum, "control_negativo")

    categories = {}
    for item in checks:
        category = item["category"]
        categories[category] = categories.get(category, 0) + 1
    return {
        "status": "PASS_RESPUESTA_VARIACIONAL_MEMORIA_RACIONAL",
        "provenance_status": "CERTIFICADO_NUEVO",
        "arithmetic": "fractions.Fraction; igualdad exacta; sin tolerancias",
        "mathematical_domain": "Fibras reales racionales de dimension 2 y 3; duplicaciones de dimension 4 y 6",
        "owner": "16_tres_hojas_variacion.tex: energia de rutas y refinamiento",
        "scope": [
            "Coeficiente de epsilon en energia polinomica frente al diferencial de transporte",
            "Representante antisimetrico con emparejamiento real de Hilbert--Schmidt",
            "Covarianza bajo calibres ortogonales fijos y diferencial total de calibre movil",
            "Inversion de aristas con variacion del peso y subcaso de peso escalar",
            "Refinamiento por duplicacion, isometrico para los productos ponderados declarados",
            "Variacion conjunta de campos, transporte y pesos; controles negativos de terminos omitidos",
            "Composicion de tres transportes, dos variaciones no conmutativas y pullback de representantes",
            "Peso global acoplado entre dos aristas: diferencial mediante q=Wr y suma de contribuciones",
        ],
        "assumptions": [
            "U ortogonal, A antisimetrico, W simetrico positivo en el destino; cada arista se cuenta una vez",
            "Los jets U+epsilon A U representan el primer orden de una curva ortogonal",
            "Naturalidad de la corriente para J,K fijos y variaciones compatibles con D_f J=K D_c",
            "K^T W_f K=W_c, incluida su derivada si los pesos varian",
            "Los controles de inversion de aristas se limitan al subcaso de peso por bloques",
        ],
        "limitations": [
            "Casos finitos racionales; la prueba general y su version hermitica compleja se exponen en el manuscrito",
            "No certifica la seleccion APP--TRIT--TPK de los datos de ruta usados como ejemplos de regresion",
            "No identifica esta respuesta con una corriente material de espin ni evalua s0",
            "No certifica una interpretacion gravitatoria, amplitud cosmologica ni completitud global del articulo",
        ],
        "rational_cases": len(cases),
        "checks_count": len(checks),
        "checks_by_category": categories,
        "inversion_negative_witness": {
            "forward_current": str(j),
            "reverse_current_fixed_weight": str(ji),
            "transported_weight_correction": str(correction),
            "corrected_reverse_current": str(ji + correction),
        },
        "physical_spin_current_certified": False,
        "torsional_amplitude_s0_evaluated": False,
        "proof_by_finite_testing": False,
        "article_complete": False,
        "checks": checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, help="Escribir ademas este recibo JSON")
    args = parser.parse_args()
    if args.receipt and (args.receipt.suffix.lower() != ".json"
                         or args.receipt.resolve() == Path(__file__).resolve()):
        parser.error("--receipt requiere una ruta JSON distinta del programa")
    try:
        result = run_checks()
        result["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        code = 0
    except Exception as exc:
        result = {
            "status": "FAIL_RESPUESTA_VARIACIONAL_MEMORIA_RACIONAL",
            "error_type": type(exc).__name__, "error": str(exc),
            "physical_spin_current_certified": False,
            "torsional_amplitude_s0_evaluated": False,
            "article_complete": False,
        }
        code = 1
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(output, encoding="utf-8")
    sys.stdout.write(output)
    return code


if __name__ == "__main__":
    sys.exit(main())
