#!/usr/bin/env python3
"""Controles racionales finitos de acoplamiento y covarianza de memoria.

CERTIFICADO_NUEVO: controles de las identidades indicadas, no una prueba
simbolica de la familia infinita ni un certificado global del corpus HMT.
El caso de escala ``hbar`` usa coordenadas racionales positivas de ensayo:
no evalua, calibra ni genera una constante fisica. Es una comprobacion
downstream del cambio de carta de una seccion de accion ya construida.

U = [[T, sqrt(8) D0], [sqrt(8) D0, E]]. Los productos que se comprueban
tienen coeficientes racionales despues de cancelar el factor sqrt(8)
comun a los bloques cruzados. No se aproxima esa raiz.
Tambien se controla la identidad matricial memoria-espectro
-(J W)^2 = I + 8 [D0,J][D0,J]^T, incluido un ejemplo acoplado 4D.

La entropia mencionada es la de un modo gaussiano reducido, bajo esa
realizacion declarada. No se identifica con calor ni con una ley termica.
No hay asserts: las comprobaciones permanecen activas con python -O.
Solo biblioteca estandar; ejecucion prevista: python3 -I -S ESTE_ARCHIVO.
"""

from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
from pathlib import Path


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


I = matrix(((1, 0), (0, 1)))
ZERO = matrix(((0, 0), (0, 0)))
OMEGA = matrix(((0, 1), (-1, 0)))
N_VALUES = tuple(range(-5, 6)) + (10, 20)
S_VALUES = (F(1), F(2), F(3, 2), F(5, 7))
HBAR_VALUES = (F(1), F(2), F(3, 2), F(5, 7), F(1, 10**34))


def add(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(len(a[0])))
                 for i in range(len(a)))


def scale(c, a):
    return tuple(tuple(F(c) * a[i][j] for j in range(len(a[0])))
                 for i in range(len(a)))


def mul(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
                       for j in range(len(b[0]))) for i in range(len(a)))


def transpose(a):
    return tuple(tuple(a[j][i] for j in range(len(a)))
                 for i in range(len(a[0])))


def det(a):
    if len(a) != 2 or any(len(row) != 2 for row in a):
        raise ValueError("det solo admite matrices 2D")
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def identity(n):
    return matrix(tuple(tuple(int(i == j) for j in range(n)) for i in range(n)))


def inverse(a):
    """Gauss-Jordan racional, independiente de las identidades simplecticas."""
    n = len(a)
    eye = identity(n)
    rows = [list(a[i]) + list(eye[i]) for i in range(n)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if rows[r][col]), None)
        if pivot is None:
            raise ValueError("Matriz singular")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        factor = rows[col][col]
        rows[col] = [entry / factor for entry in rows[col]]
        for r in range(n):
            if r != col:
                factor = rows[r][col]
                rows[r] = [rows[r][k] - factor * rows[col][k]
                           for k in range(2 * n)]
    return matrix(tuple(tuple(row[n:]) for row in rows))


def commutator(a, b):
    return add(mul(a, b), scale(-1, mul(b, a)))


def frobenius_squared(a):
    return sum((entry * entry for row in a for entry in row), F(0))


def block_diagonal(a, b):
    na, nb = len(a), len(b)
    return matrix(tuple(tuple(
        a[i][j] if i < na and j < na else
        b[i - na][j - na] if i >= na and j >= na else 0
        for j in range(na + nb)) for i in range(na + nb)))


def family_h(n):
    return matrix(((1 + n, n**2), (n, n**2 - n + 1)))


def gram(a):
    return mul(a, transpose(a))


def form(a, b):
    return mul(mul(a, OMEGA), transpose(b))


def conjugate(a, v):
    return mul(mul(a, v), transpose(a))


def exact_sqrt(value):
    """Raiz racional exacta; rechaza silenciamiento por aproximacion."""
    if value < 0:
        raise ValueError("La raiz solicitada no es real no negativa")
    num = isqrt(value.numerator)
    den = isqrt(value.denominator)
    if num * num != value.numerator or den * den != value.denominator:
        raise ValueError("La raiz solicitada no es racional")
    return F(num, den)


class Checks:
    def __init__(self):
        self.count = 0

    def equal(self, name, actual, expected):
        self.count += 1
        if actual != expected:
            raise RuntimeError(
                f"FAIL {name}: obtenido={actual!r}; esperado={expected!r}"
            )

    def true(self, name, condition):
        self.equal(name, condition, True)


def blocks(h):
    t = scale(F(1, 9), add(scale(8, I), h))
    d0 = scale(F(1, 9), add(h, scale(-1, I)))
    e = scale(F(1, 9), add(I, scale(8, h)))
    return t, d0, e


def block_symplectic(check, label, t, d0, e):
    # U (Omega direct_sum Omega) U^T = Omega direct_sum Omega.
    check.equal(label + ": bloque 11",
                add(form(t, t), scale(8, form(d0, d0))), OMEGA)
    check.equal(label + ": bloque 12 / sqrt(8)",
                add(form(t, d0), form(d0, e)), ZERO)
    check.equal(label + ": bloque 22",
                add(scale(8, form(d0, d0)), form(e, e)), OMEGA)
    # El bloque 21 es el negativo de la transpuesta del bloque 12.


def inspect_h(check, label, h):
    check.equal(label + ": det H", det(h), F(1))
    check.equal(label + ": H simplectica", form(h, h), OMEGA)
    t, d0, e = blocks(h)
    block_symplectic(check, label, t, d0, e)
    vnorm = add(gram(t), scale(8, gram(d0)))
    hht = gram(h)
    check.equal(label + ": Vnorm", vnorm,
                scale(F(1, 9), add(scale(8, I), hht)))
    check.equal(label + ": det Vnorm", det(vnorm),
                1 + F(8, 81) * (trace(hht) - 2))
    check.equal(label + ": Vnorm simetrica", transpose(vnorm), vnorm)
    check.true(label + ": Vnorm definida positiva",
               vnorm[0][0] > 0 and det(vnorm) > 0)
    check.true(label + ": det Vnorm >= 1", det(vnorm) >= 1)
    return t, d0, e, vnorm


def memory_spectrum_checks(check, label, h, j):
    """Identidad matricial general y su lectura escalar solo en dimension 2."""
    eye = identity(len(h))
    zero = scale(0, eye)
    check.equal(label + ": J^2=-I", mul(j, j), scale(-1, eye))
    check.equal(label + ": J antisimetrica", transpose(j), scale(-1, j))
    check.equal(label + ": H J H^T=J", conjugate(h, j), j)
    a = gram(h)
    ainv = inverse(a)
    check.equal(label + ": inversa exacta derecha de A", mul(a, ainv), eye)
    check.equal(label + ": inversa exacta izquierda de A", mul(ainv, a), eye)
    check.equal(label + ": A^-1=-J A J", ainv,
                scale(-1, mul(mul(j, a), j)))
    c = commutator(h, j)
    d0 = scale(F(1, 9), add(h, scale(-1, eye)))
    z0 = commutator(d0, j)
    check.equal(label + ": [H,J]=9[D0,J]", c, scale(9, z0))
    check.equal(label + ": C C^T=A+A^-1-2I", gram(c),
                add(add(a, ainv), scale(-2, eye)))
    w = scale(F(1, 9), add(scale(8, eye), a))
    jw = mul(j, w)
    spectrum_squared = scale(-1, mul(jw, jw))
    check.equal(label + ": memoria -> espectro",
                spectrum_squared, add(eye, scale(8, gram(z0))))
    check.equal(label + ": memoria desde C",
                scale(8, gram(z0)), scale(F(8, 81), gram(c)))
    if len(h) == 2:
        nu_squared = det(w)
        check.equal(label + ": espectro escalar 2D",
                    spectrum_squared, scale(nu_squared, eye))
        # ||[D,J]||_F^2 = 8 ||[D0,J]||_F^2: D=sqrt(8) D0.
        commutator_d_squared = 8 * frobenius_squared(z0)
        check.equal(label + ": nu^2=1+||[D,J]||_F^2/2",
                    nu_squared, 1 + commutator_d_squared / 2)
        check.equal(label + ": nu^2=1+4||[H,J]||_F^2/81",
                    nu_squared, 1 + F(4, 81) * frobenius_squared(c))
    if a == eye:
        check.equal(label + ": pasivo conmuta con J", z0, zero)
        check.equal(label + ": pasivo con espectro unitario", spectrum_squared, eye)
    return w, spectrum_squared


def coupled_4d_checks(check):
    """Mezcla racional de dos pares; no afirma entrelazamiento cuantico."""
    label = "caso 4D acoplado"
    eye = identity(4)
    j = block_diagonal(OMEGA, OMEGA)
    hbase = block_diagonal(family_h(1), family_h(2))
    cosine, sine = F(3, 5), F(4, 5)
    mixing = matrix(((cosine, 0, -sine, 0), (0, cosine, 0, -sine),
                     (sine, 0, cosine, 0), (0, sine, 0, cosine)))
    check.equal(label + ": rotacion ortogonal", gram(mixing), eye)
    check.equal(label + ": rotacion canonica", conjugate(mixing, j), j)
    h = conjugate(mixing, hbase)
    check.true(label + ": H no diagonal por pares en la carta fija",
               any(h[i][k] != 0 for i in range(2) for k in range(2, 4)))
    w, spectrum_squared = memory_spectrum_checks(check, label, h, j)
    check.true(label + ": W no diagonal por pares en la carta fija",
               any(w[i][k] != 0 for i in range(2) for k in range(2, 4)))
    # Los dos radios son distintos: no se colapsa 4D a un escalar nu^2 I.
    expected_base = block_diagonal(scale(F(121, 81), I), scale(F(41, 9), I))
    check.equal(label + ": espectro cuadrado transportado",
                spectrum_squared, conjugate(mixing, expected_base))
    check.true(label + ": espectro cuadrado no escalar",
               spectrum_squared != scale(trace(spectrum_squared) / 4, eye))


def covariance_checks(check, label, t, d0, e, vnorm):
    """Marco local de salida M; no se confunde con conjugacion de H."""
    covariance_cases = 0
    for s in S_VALUES:
        m = matrix(((s, 0), (0, 1 / s)))
        name = f"{label}, s={s}"
        check.equal(name + ": M simplectica", form(m, m), OMEGA)
        check.equal(name + ": det M", det(m), F(1))
        mt, md0, me = mul(m, t), mul(m, d0), mul(m, e)
        block_symplectic(check, name + ": (M direct_sum M) U",
                         mt, md0, me)
        framed = conjugate(m, vnorm)
        for hbar in HBAR_VALUES:
            covariance_cases += 1
            prefix = name + f", hbar={hbar}"
            # Covarianza inicial = (hbar/2) I en cada canal independiente.
            v = scale(hbar / 2, add(gram(mt), scale(8, gram(md0))))
            check.equal(prefix + ": covarianza transportada", v,
                        scale(hbar / 2, framed))
            check.equal(prefix + ": determinante dimensional", det(v),
                        (hbar / 2)**2 * det(vnorm))
            check.equal(prefix + ": determinante normalizado",
                        det(v) / (hbar / 2)**2, det(vnorm))
            check.equal(prefix + ": simetria", transpose(v), v)
            check.true(prefix + ": definida positiva",
                       v[0][0] > 0 and det(v) > 0)
            g = scale(2 / hbar, v)
            omega_g = mul(OMEGA, g)
            check.equal(prefix + ": radio simplectico al cuadrado",
                        scale(-1, mul(omega_g, omega_g)),
                        scale(det(vnorm), I))
    return covariance_cases


def main():
    check = Checks()
    covariance_cases = 0
    for n in N_VALUES:
        h = family_h(n)
        label = f"H_{n}"
        t, d0, e, vnorm = inspect_h(check, label, h)
        memory_spectrum_checks(check, label, h, OMEGA)
        check.equal(label + ": polinomio de anisotropia",
                    trace(gram(h)) - 2, F(n**2 * (2*n**2 - 2*n + 5)))
        check.equal(label + ": determinante desde el polinomio",
                    det(vnorm), 1 + F(8, 81) * n**2 * (2*n**2 - 2*n + 5))
        check.equal(label + ": pureza solo en n=0", det(vnorm) == 1, n == 0)
        check.equal(label + ": memoria nula solo en n=0", d0 == ZERO, n == 0)
        covariance_cases += covariance_checks(check, label, t, d0, e, vnorm)
        if n == 1:
            check.equal("n=1: det Vnorm", det(vnorm), F(121, 81))
            r = exact_sqrt(det(vnorm))
            purity = 1 / r
            nbar = (r - 1) / 2
            q = (r - 1) / (r + 1)
            check.equal("n=1: r", r, F(11, 9))
            check.equal("n=1: pureza", purity, F(9, 11))
            check.equal("n=1: nbar", nbar, F(1, 9))
            check.equal("n=1: q", q, F(1, 10))
            check.equal("n=1: nbar desde q", q / (1 - q), nbar)

    # Control contrario a 'memoria no nula implica mezcla/entropia positiva'.
    # H=Omega es una rotacion ortogonal simplectica, no H_n con n distinto de 0.
    label = "rotacion pasiva H=Omega"
    t, d0, e, vnorm = inspect_h(check, label, OMEGA)
    memory_spectrum_checks(check, label, OMEGA, OMEGA)
    check.equal(label + ": H H^T", gram(OMEGA), I)
    check.true(label + ": D no nulo", d0 != ZERO)
    check.equal(label + ": contribucion de memoria",
                scale(8, gram(d0)), scale(F(16, 81), I))
    check.equal(label + ": contribucion visible", gram(t), scale(F(65, 81), I))
    check.equal(label + ": covarianza normalizada", vnorm, I)
    r = exact_sqrt(det(vnorm))
    check.equal(label + ": r", r, F(1))
    check.equal(label + ": pureza", 1 / r, F(1))
    nbar = (r - 1) / 2
    check.equal(label + ": nbar", nbar, F(0))
    check.equal(label + ": q", (r - 1) / (r + 1), F(0))
    # El espectro geometrico tiene p0=1 y pk=0 (k>0): entropia exactamente 0.
    # No se calculan logaritmos aproximados ni se interpreta esa entropia como calor.
    covariance_cases += covariance_checks(check, label, t, d0, e, vnorm)
    coupled_4d_checks(check)

    digest = sha256(Path(__file__).read_bytes()).hexdigest()
    print("PASS_CONTROLES_FINITOS_COVARIANZA_MEMORIA_20260912")
    print(f"checks={check.count}")
    print(f"family_cases={len(N_VALUES)}; passive_cases=1")
    print("memory_spectrum_cases_2d=14; coupled_4d_cases=1")
    print(f"frame_scales={len(S_VALUES)}; action_scales={len(HBAR_VALUES)}; "
          f"covariance_cases={covariance_cases}")
    print("n=1: det=121/81; r=11/9; purity=9/11; nbar=1/9; q=1/10")
    print("H=Omega: memory_nonzero=True; r=1; purity=1; entropy=0")
    print("scope=finite_exact_controls; no_general_symbolic_proof; no_heat_identification")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
