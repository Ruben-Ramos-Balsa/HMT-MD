"""Controles focales exactos, sin entradas metrológicas ni escrituras.

Las pruebas generales y sus hipótesis están en la nota asociada.
"""
from fractions import Fraction as F
from collections import Counter
import json
import math


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, c):
    return [[c*x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(b, -1))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def det2(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def inv2(a):
    d = det2(a)
    assert d
    return [[a[1][1]/d, -a[0][1]/d], [-a[1][0]/d, a[0][0]/d]]


def product(*matrices):
    out = eye(len(matrices[0]))
    for a in matrices:
        out = mm(out, a)
    return out


def comm(a, b):
    return product(a, b, inv2(a), inv2(b))


def diag(a, b):
    return [[a, F(0)], [F(0), b]]


def phase(t):
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def u(t, co, si):
    # t=exp(zeta)>0, cos/sin from exact rational circle.
    return [[co, t*si], [-si/t, co]]


def response(s):
    return (1-s**3)/(1-s**4)


def sensitivity(s):
    return s**3*(s*s+2*s+3)/((1+s+s*s)*(1+s+s*s+s**3))


def quadratic(g, x):
    return mm(mm(tr(x), g), x)[0][0]


I = eye(2)
counts = {"jacobiano_reciprocidad": 0, "cotas_sensibilidad": 0,
          "momento_catalan": 0, "gradiente_serie_control_numerico": 0,
          "conmutador_general": 0, "ganancia_energia_general": 0,
          "covariancia_referencia": 0, "espejo_cuarto_giro": 0,
          "levantamiento_dodecafasico": 0, "amplificacion": 0,
          "cambio_carta_telescopico": 0, "iteracion_memoria_orientada": 0,
          "restitucion_accion_relativa": 0}
negative = {"traza_pierde_orden": False, "ocupaciones_pierden_orden": False,
            "energia_no_es_autovalor_transporte": False,
            "detector_no_transportado": False}

samples = [F(n, 20) for n in range(1, 20)]
for s in samples:
    a = sensitivity(s)
    assert a == 3*s**3/(1-s**3)-4*s**4/(1-s**4)
    assert s**3/2 < a < min(F(1, 2), 3*s**3)
    assert response(s)*s**3+(response(s)-1)*(1+s+s*s) == 0
    counts["cotas_sensibilidad"] += 1
    for t in samples:
        b = sensitivity(t)
        jac = scale([[a+b, a-b], [a-b, a+b]], F(-30))
        assert jac == tr(jac)
        assert det2(jac) == 3600*a*b
        assert mm(jac, [[F(1)], [F(1)]]) == [[-60*a], [-60*a]]
        assert mm(jac, [[F(1)], [F(-1)]]) == [[-60*b], [60*b]]
        counts["jacobiano_reciprocidad"] += 1

for s in (F(1, 4), F(1, 2), F(3, 4)):
    for nmax in (8, 16, 32, 64):
        im_dilog = sum((F(0) if n % 2 == 0 else (-1)**((n-1)//2)*s**n/F(n*n))
                       for n in range(1, nmax+1))
        catalan_partial = sum((-1)**k*s**(2*k+1)/F((2*k+1)**2)
                              for k in range((nmax+1)//2))
        assert im_dilog == catalan_partial
        counts["momento_catalan"] += 1
        partial = sum((s**(3*n)-s**(4*n))/n for n in range(1, nmax+1))
        tail = s**(3*(nmax+1))/((nmax+1)*(1-s**3))
        target = -math.log(float(response(s)))
        assert abs(float(partial)-target) <= float(tail)+2e-15
        counts["gradiente_serie_control_numerico"] += 1

for ts in (F(1, 3), F(1), F(2), F(3)):
    for tv in (F(1, 2), F(1), F(4, 3)):
        d = ts/tv
        for p in (F(0), F(1, 3), F(1), F(2)):
            co, si = phase(p)
            for q in (F(0), F(1, 2), F(1), F(3)):
                cf, sf = phase(q)
                a, b = u(ts, co, si), u(tv, cf, sf)
                h = comm(a, b)
                chi = (d-1/d)*si*sf/2
                assert det2(h) == 1
                assert trace(h) == 2+4*chi*chi
                assert (h == I) == (chi == 0)
                assert comm(b, a) == inv2(h)
                assert trace(h) == trace(inv2(h))
                counts["conmutador_general"] += 1

                # Traza de los cuadrados de valores singulares en g_r,
                # sin sqrt(tv), mediante tr(g_r^-1 H^T g_r H).
                gr = diag(1/tv, tv)
                gain_trace = trace(product(inv2(gr), tr(h), gr, h))
                k = (d-1/d)*si/2
                assert gain_trace == 2+16*chi*chi*(1+k*k)
                counts["ganancia_energia_general"] += 1
                transform = [[F(1), F(2, 3)], [F(0), F(1)]]
                ip = inv2(transform)
                hp = product(transform, h, ip)
                gp = product(tr(ip), gr, ip)
                state = [[F(2)], [F(3)]]
                ps = mm(transform, state)
                assert trace(hp) == trace(h)
                assert quadratic(gp, mm(hp, ps)) == quadratic(gr, mm(h, state))
                if quadratic(gr, ps) != quadratic(gr, state):
                    negative["detector_no_transportado"] = True
                if h != inv2(h):
                    negative["traza_pierde_orden"] = True
                counts["covariancia_referencia"] += 1

# La base exacta del cuarto de giro se toma de los vectores del manuscrito.
cycle = [[F(i == (j+1) % 12) for j in range(12)] for i in range(12)]
uv0 = [[F([1, 0, -1, 0][i % 4])] for i in range(12)]
vv0 = mm(cycle, uv0)
w0 = [a+b for a, b in zip(uv0, vv0)]
assert mm(tr(w0), w0) == scale(I, F(6))
j0 = [[F(0), F(-1)], [F(1), F(0)]]
assert mm(cycle, w0) == mm(w0, j0)
projector = scale(mm(w0, tr(w0)), F(1, 6))
complement = sub(eye(12), projector)
outside = mm(product(cycle, cycle, cycle), complement)


def lift(a):
    return add(outside, scale(product(w0, a, tr(w0)), F(1, 6)))


for t in (F(1, 3), F(1, 2), F(1), F(2), F(3)):
    a, b = u(t, F(0), F(1)), u(1/t, F(0), F(1))
    h = comm(a, b)
    xi = (t*t-1)/(t*t+1)
    assert product(a, a) == scale(I, F(-1))
    assert product(b, b) == scale(I, F(-1))
    assert h == diag(t**4, t**-4)
    assert trace(h)-2 == 16*xi*xi/(1-xi*xi)**2
    assert ((1+xi)/(1-xi))**2 == t**4
    if t != 1:
        assert Counter(["a", "b", "ai", "bi"]) == Counter(["a", "ai", "b", "bi"])
        assert h != product(a, inv2(a), b, inv2(b))
        negative["ocupaciones_pierden_orden"] = True
        assert t**8 != t**4
        negative["energia_no_es_autovalor_transporte"] = True
    g = diag(1/t, t)
    eq, ep = [[F(1)], [F(0)]], [[F(0)], [F(1)]]
    assert quadratic(g, mm(h, eq))/quadratic(g, eq) == t**8
    assert quadratic(g, mm(h, ep))/quadratic(g, ep) == t**-8
    counts["espejo_cuarto_giro"] += 1

    state = [[F(2)], [F(3)]]
    for iteration in range(-6, 7):
        step = h if iteration >= 0 else inv2(h)
        hn = I
        for unused in range(abs(iteration)):
            hn = mm(hn, step)
        assert hn == diag(t**(4*iteration), t**(-4*iteration))
        final_state = mm(hn, state)
        assert final_state[0][0]*final_state[1][0] == F(6)
        assert det2(hn) == 1
        if t != 1 and iteration != 0:
            assert final_state != state
        counts["iteracion_memoria_orientada"] += 1

    la, lb = lift(a), lift(b)
    assert product(la, la, la, la) == eye(12)
    lifted_comm = product(la, lb, la, la, la, lb, lb, lb)
    expected = add(complement, scale(product(w0, h, tr(w0)), F(1, 6)))
    assert lifted_comm == expected
    assert trace(lifted_comm) == 10+trace(h)
    assert mm(lifted_comm, complement) == complement
    counts["levantamiento_dodecafasico"] += 1

    n = 9
    amp = [[h[i//n][j//n]*F(i % n == j % n) for j in range(2*n)] for i in range(2*n)]
    emb = [[F(i == j*n) for j in range(2)] for i in range(2*n)]
    assert trace(amp)/n == trace(h)
    assert mm(amp, emb) == mm(emb, h)
    counts["amplificacion"] += 1

for alpha in (F(1, 100), F(1, 137), F(2, 271)):
    for quotient in (F(1, 2), F(1), F(100), F(498), F(997, 2)):
        eta = alpha*quotient
        xi = (eta+alpha)/(500*alpha)
        sqrt_rho = (1+xi)/(1-xi)
        rho = sqrt_rho**2
        assert rho == ((501*alpha+eta)/(499*alpha-eta))**2
        assert alpha*(500*(sqrt_rho-1)/(sqrt_rho+1)-1) == eta
        assert rho > F(501, 499)**2
        counts["restitucion_accion_relativa"] += 1

ds = [F(1), F(2), F(3, 2), F(1, 3), F(1)]
phases = [phase(F(1, 3)), phase(F(1, 2)), phase(F(-1, 3)), phase(F(-1, 2))]
total = I
for index, (co, si) in enumerate(phases):
    step = product(diag(ds[index+1], 1/ds[index+1]), u(F(1), co, si),
                   diag(1/ds[index], ds[index]))
    total = mm(step, total)
assert total == I
counts["cambio_carta_telescopico"] += 1
assert all(negative.values())
print(json.dumps({"status": "PASS_COMPATIBILIDAD_HOLONOMIA_FOCAL",
                  "counts": counts, "negative_controls": negative,
                  "arithmetic": "Exacta racional salvo el contraste de logaritmo con cola de serie, señalado separadamente.",
                  "scope": "Operadores y lectores declarados; no certifica actualización autónoma TPK, interacción experimental ni corpus integral."},
                 indent=2, ensure_ascii=False))
