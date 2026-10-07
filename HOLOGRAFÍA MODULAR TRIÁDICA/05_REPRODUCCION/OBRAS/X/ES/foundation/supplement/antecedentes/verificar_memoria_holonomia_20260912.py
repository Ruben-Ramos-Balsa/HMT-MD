"""Controles finitos exactos de MEMORIA_HOLONOMIA_Y_SIMETRIA_20260912.md.

No recuenta las emisiones fuente de c27. Las pruebas generales están en la nota.
Sólo biblioteca estándar; ningún resultado depende de assert ni de decimales.
"""
from fractions import Fraction as Q
from itertools import product
import json

checks = 0


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


def mat(a, b, c, d):
    return ((Q(a), Q(b)), (Q(c), Q(d)))


I = mat(1, 0, 0, 1)
O = mat(0, 0, 0, 0)
OM = mat(0, 1, -1, 0)
N = mat(0, 1, 0, 0)
B = mat(1, 0, 18, 1)
V = (Q(1), Q(18))
K = (Q(4), Q(72))


def mm(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(2)) for i in range(2))


def add(A, B):
    return tuple(tuple(A[i][j] + B[i][j] for j in range(2)) for i in range(2))


def scale(A, c):
    return tuple(tuple(c * x for x in row) for row in A)


def va(v, w):
    return tuple(x + y for x, y in zip(v, w))


def vs(v, w):
    return tuple(x - y for x, y in zip(v, w))


def det(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def inv(A):
    d = det(A)
    if d == 0:
        raise ValueError('matriz singular')
    return scale(mat(A[1][1], -A[0][1], -A[1][0], A[0][0]), 1 / d)


def tr(A):
    return tuple(zip(*A))


def pull(A, form=OM):
    return mm(tr(A), mm(form, A))


def compose(f, g):
    A, a = f
    C, c = g
    return mm(A, C), va(a, mv(A, c))


def act(f, v):
    return va(mv(f[0], v), f[1])


def affine_inverse(f):
    A = inv(f[0])
    return A, tuple(-x for x in mv(A, f[1]))


def invariant(v):
    return v[1] - 18 * v[0], v[0] % 4


Nv = mm(B, mm(N, inv(B)))
require(Nv == mat(-18, 1, -324, 18), 'N_v desde base primitiva')
require(mm(Nv, Nv) == O and Nv != O, 'nilpotencia exacta')
for n in range(-25, 26):
    R = add(I, scale(Nv, n))
    require(det(R) == 1 and pull(R) == OM, 'estabilizador unimodular')
    require(mv(R, K) == K, 'incremento fijado')
    for g, s in product(range(-3, 4), repeat=2):
        m = (Q(g), Q(s))
        H = (I, K)
        require(act((R, (0, 0)), act(H, m)) == act(H, mv(R, m)),
                'conmutacion con retorno')
        require(mv(R, m) == va(m, tuple(n * (s - 18 * g) * x for x in V)),
                'carga selecciona desplazamiento')
        require(invariant(mv(R, m)) == (s - 18 * g, (g + n*(s-18*g)) % 4),
                'accion del estabilizador en cociente')
        m2 = va(m, tuple(n * x for x in K))
        require(invariant(m2) == invariant(m), 'invariantes de orbita')
        require((m2 == m) == (n == 0), 'memoria acumulativa')

for a, b, c, d in product(range(-4, 5), repeat=4):
    R = mat(a, b, c, d)
    if det(R) == 1 and mv(R, K) == K:
        require(R == add(I, scale(Nv, b)), 'exhaustividad estabilizador finito')

# La carga sola no clasifica las orbitas de vuelta completa.
require(invariant((0, 0))[0] == invariant((1, 18))[0]
        and invariant((0, 0)) != invariant((1, 18)), 'clase residual necesaria')

# Campos hamiltonianos y Noether en la realizacion adimensional del registro.
for g, s, u, eps in product(range(-3, 4), repeat=4):
    m = (Q(g), Q(s))
    charge = s - 18*g
    dH = (-18*charge, charge)
    XH = (dH[1], -dH[0])
    require(XH == mv(Nv, m), 'Hamiltoniano cuadratico genera N_v')
    require(-18*XH[0] + XH[1] == 0, 'carga de Noether conservada')
    flow = mv(add(I, scale(Nv, u)), m)
    require(flow == va(m, tuple(u*charge*x for x in V)), 'flujo parabólico')
    velocity_g = Q(2, 3)
    L = s*velocity_g - Q(charge*charge, 2)
    shifted = (s+18*eps)*velocity_g - Q((s+18*eps-18*(g+eps))**2, 2)
    require(shifted-L == 18*eps*velocity_g, 'termino de borde variacional')
    require(s-18*g == charge, 'carga momento menos borde')
require(mv(add(I, Nv), V) == V and va(V, K) != V, 'flujo estabilizador distinto de retorno')
for a, g, s in product(range(4), range(-4, 5), range(-4, 5)):
    inv0 = (s - 18 * g, (g - a) % 4)
    inv1 = (s + 18 - 18 * (g + 1), (g + 1 - (a + 1) % 4) % 4)
    require(inv0 == inv1, 'fase y memoria conjuntas')

matrices = (I, add(I, N), mat(1, 1, 1, 2), mat(0, -1, 1, -1), B)
vectors = ((0, 0), (1, 2), (-3, 1), K)
for C, R, k, b, m in product(matrices, matrices, vectors, vectors, vectors):
    H, A = (C, k), (R, b)
    transformed = compose(A, compose(H, affine_inverse(A)))
    Cp = mm(R, mm(C, inv(R)))
    kp = va(mv(R, k), mv(add(I, scale(Cp, -1)), b))
    require(transformed == (Cp, kp), 'cambio afin')
    require(act(transformed, act(A, m)) == act(A, act(H, m)), 'covarianza')
    expected = mm(R, C) == mm(C, R) and mv(add(I, scale(C, -1)), b) == mv(add(I, scale(R, -1)), k)
    require((compose(A, H) == compose(H, A)) == expected, 'criterio de simetria')

# Heisenberg equilibrado: coordenadas (a,b,z), mod9; 1/2=5 mod9.
def sigma(u, v):
    return (u[0] * v[1] - u[1] * v[0]) % 9


def hp(u, v):
    return ((u[0] + v[0]) % 9, (u[1] + v[1]) % 9,
            (u[2] + v[2] - 5 * sigma(u, v)) % 9)


def hi(u):
    return tuple((-x) % 9 for x in u)


uv = [(a, b, 0) for a, b in product(range(9), repeat=2)]
for u, v in product(uv, repeat=2):
    comm = hp(hp(hp(u, v), hi(u)), hi(v))
    require(comm == (0, 0, -sigma(u, v) % 9), 'conmutador central')
    a, b, _ = u
    c, d, _ = v
    require((5*a*b + 5*c*d + b*c - 5*(a+c)*(b+d)) % 9 == -5*sigma(u, v) % 9,
            'cociclo polarizado equilibrado')
for u, v, w in product(uv, repeat=3):
    require(hp(hp(u, v), w) == hp(u, hp(v, w)), 'asociatividad central')
sl = [t for t in product(range(9), repeat=4) if (t[0]*t[3]-t[1]*t[2]) % 9 == 1]
require(len(sl) == 648, 'censo grupo usado en prueba finita')
probes = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (3, 6, 4), (8, 4, 7))
for a, b, c, d in sl:
    def lift(u):
        return ((a*u[0]+b*u[1]) % 9, (c*u[0]+d*u[1]) % 9, u[2])
    for u, v in product(probes, repeat=2):
        require(lift(hp(u, v)) == hp(lift(u), lift(v)), 'automorfismo central')
require(28 % 9 == 1 % 9 and 28 // 9 != 1 // 9, 'fase no retiene cociente')
require(-28 == 8 + 9 * (-4), 'acarreo orientacion inversa')
require(hp(hp(hp((1, 0, 0), (0, 1, 0)), (8, 0, 0)), (0, 8, 0)) == (0, 0, 8),
        'retorno posicional con centro no trivial')

# Balance bilineal: D=sqrt8*L evita cualquier aproximacion irracional.
Es = (mat(0, -1, 1, -1), add(I, N), mat(1, 1, 1, 2))
links = (B, inv(B), mat(2, 1, 1, 1))
P = I
stored = O
for j in range(30):
    E, link = Es[j % 3], links[j % 3]
    require(pull(E) == OM and pull(link) == OM, 'regimen y enlace tipados')
    T = mm(link, scale(add(scale(I, 8), E), Q(1, 9)))
    L = mm(link, scale(add(E, scale(I, -1)), Q(1, 9)))
    require(add(pull(T), scale(pull(L), 8)) == OM, 'balance local')
    stored = add(stored, scale(pull(mm(L, P)), 8))
    P = mm(T, P)
    require(add(pull(P), stored) == OM, 'telescopia sin permutar')
require(pull(P) != OM, 'complemento no omitible')
require(mm(Es[0], Es[1]) != mm(Es[1], Es[0]), 'orden efectivo')

print(json.dumps({
    'status': 'PASS_MEMORIA_HOLONOMIA_EXACTA',
    'checks': checks,
    'arithmetic': 'integer_mod9_and_Fraction',
    'source_c27_recounted': False,
    'new_physical_identifications_certified': False,
    'general_proofs': 'MEMORIA_HOLONOMIA_Y_SIMETRIA_20260912.md §§2–7',
}, ensure_ascii=False))
