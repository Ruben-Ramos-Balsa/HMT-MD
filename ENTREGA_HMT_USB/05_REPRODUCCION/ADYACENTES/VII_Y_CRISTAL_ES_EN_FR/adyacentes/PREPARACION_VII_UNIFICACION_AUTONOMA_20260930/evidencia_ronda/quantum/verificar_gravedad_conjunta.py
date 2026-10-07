"""Falsadores racionales de GRAVEDAD_EN_EL_SISTEMA_CONJUNTO.

Los argumentos generales están en la nota. Estos fixtures no son valores
físicos, no generan constantes y no certifican planitud cuántica global.
"""
from fractions import Fraction as F


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def add(a, b):
    return [[x+y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(s, a):
    return [[s*x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1, b))


def tr(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)]
            for row in a]


def inv(a):
    n = len(a)
    m = [row[:] + unit for row, unit in zip(a, eye(n))]
    for j in range(n):
        pivot = next(i for i in range(j, n) if m[i][j])
        m[j], m[pivot] = m[pivot], m[j]
        v = m[j][j]
        m[j] = [x/v for x in m[j]]
        for i in range(n):
            if i != j:
                v = m[i][j]
                m[i] = [x-v*y for x, y in zip(m[i], m[j])]
    return [row[n:] for row in m]


def kron(a, b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0]))
             for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


def block(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def schur(a, z=F(0)):
    bb = sub(block(a, (0, 1), (0, 1)), scale(z, eye(2)))
    bi = block(a, (0, 1), (2,))
    ii = sub(block(a, (2,), (2,)), [[z]])
    return sub(bb, mul(mul(bi, inv(ii)), tr(bi)))


checks = 0


def eq(a, b):
    global checks
    assert a == b, (a, b)
    checks += 1


Y = mat([[4, 1, 1], [1, 3, 1], [1, 1, 2]])
# Principal minors 4, 11, 17 verify positive definiteness of this fixture.
eq(Y[0][0], 4)
eq(Y[0][0]*Y[1][1]-Y[0][1]**2, 11)
eq(Y[0][0]*(Y[1][1]*Y[2][2]-Y[1][2]**2)
   -Y[0][1]*(Y[0][1]*Y[2][2]-Y[1][2]*Y[0][2])
   +Y[0][2]*(Y[0][1]*Y[1][2]-Y[1][1]*Y[0][2]), 17)
N = 12*4*8*15
eq(N, 5760)
eq(F(N-1, 4*N), F(5759, 23040))

for hbar in (F(2, 7), F(9, 5)):
    for length in (F(3, 11), F(7, 2)):
        c = F(5, 3)
        energy_unit = hbar*c/length
        grav = c**3*length**2/hbar
        chi = grav/c**4
        H = scale(energy_unit, Y)
        M = scale(1/c**2, H)
        R = scale(length, Y)
        lam = scale(length, inv(Y))
        eq(R, scale(grav/c**2, M))
        eq(R, scale(chi, H))
        eq(mul(R, lam), scale(length**2, eye(3)))
        eq(mul(H, lam), scale(hbar*c, eye(3)))
        for y1, y2 in ((F(1, 9), F(2, 3)), (F(3), F(7))):
            m1, m2 = hbar*y1/(c*length), hbar*y2/(c*length)
            eq(grav*m1*m2/(hbar*c), y1*y2)
            eq((length*y1)/(length/y1), y1**2)
            for rho in (F(2, 9), F(7)):
                eq((grav/rho)*(rho*m1)*(rho*m2)/(rho*hbar*c), y1*y2)
        for z in (F(0), F(-1, 7), F(-3)):
            eq(schur(R, chi*z), scale(chi, schur(H, z)))
        He, Re = schur(H), schur(R)
        lamb = block(lam, (0, 1), (0, 1))
        eq(mul(Re, lamb), scale(length**2, eye(2)))
        T = mat([[2, 1], [1, 3]])
        Ti = inv(T)
        Hcan = mul(mul(tr(Ti), He), Ti)
        Rcan = mul(mul(tr(Ti), Re), Ti)
        Lcan = mul(mul(T, lamb), tr(T))
        eq(Rcan, scale(chi, Hcan))
        eq(mul(Rcan, Lcan), scale(length**2, eye(2)))
        eq(comm(T, Re) == scale(0, Re), False)
        # Incorrectly transporting the inverse length by the same congruence fails.
        Lwrong = mul(mul(tr(Ti), lamb), Ti)
        eq(mul(Rcan, Lwrong) == scale(length**2, eye(2)), False)
        # Keeping only the visible block loses the memory correction.
        eq(block(R, (0, 1), (0, 1)) == Re, False)

# Exact interaction block: geometric transitions see a different material response.
X = mat([[0, 1], [1, 0]])
P0, P1 = mat([[1, 0], [0, 0]]), mat([[0, 0], [0, 1]])
B0, B1 = mat([[1, 1], [1, 2]]), mat([[3, 0], [0, 1]])
A = kron(X, eye(2))
B = kron(eye(2), mat([[2, 0], [0, 5]]))
V = add(kron(P0, B0), kron(P1, B1))
H = add(add(A, B), V)
eq(block(comm(A, V), (0, 1), (2, 3)), sub(B1, B0))
eq(comm(A, V) == scale(0, H), False)
eq(add(add(comm(H, A), comm(H, B)), comm(H, V)), scale(0, H))
# If the responses coincide, this particular exchange vanishes exactly.
eq(comm(A, kron(eye(2), B0)), scale(0, H))

print(f'PASS_FOCAL_GRAVEDAD_CONJUNTA: {checks} controles exactos; '
      'alcance: identidades y retroaccion declaradas, no curvatura cuantica total.')
