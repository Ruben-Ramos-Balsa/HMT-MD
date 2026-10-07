"""Controles racionales de las secciones 10.24--10.27.

Realizaciones posteriores: no genera constantes, no lee valores objetivo,
no modifica fuentes y no verifica una identificación física.
Las pruebas analíticas de trazas y convergencia están en la exposición.
"""

from fractions import Fraction as F
from itertools import product

CHECKS = 0


def require(condition, label):
    global CHECKS
    if not condition:
        raise RuntimeError(label)
    CHECKS += 1


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def scale(a, s):
    return [[s * x for x in row] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return add(a, scale(b, -1))


def power(a, n):
    out = eye(len(a))
    for _ in range(n):
        out = mm(out, a)
    return out


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def chi4(n):
    return (0, 1, 0, -1)[n % 4]


def check_moments():
    j = [[F(0), F(-1)], [F(1), F(0)]]
    e2 = eye(2)
    require(power(j, 2) == scale(e2, -1), "J^2=-I")
    require(power(j, 4) == e2, "J^4=I")
    for n in range(1, 25):
        r, s = F(2, 5), F(3, 7)
        for a, b in product(range(4), repeat=2):
            lhs = mm(scale(power(j, a), r**n),
                     scale(power(j, b), s**n))
            rhs = scale(power(j, (a + b) % 4), (r * s)**n)
            require(lhs == rhs, "Composición profundidad/orientación")
        require(power(scale(j, r**n), 4) == scale(e2, r**(4*n)),
                "Retorno de fase sin cancelar profundidad")
        require(power(j, n)[1][0] == chi4(n), "Carácter de cuarto de giro")
    sine_twice = {1: 1, 3: 2, 5: 1, 7: -1, 9: -2, 11: -1}
    for n in range(1, 242, 2):
        rhs = chi4(n) + (3 * chi4(n // 3) if n % 3 == 0 else 0)
        require(sine_twice[n % 12] == rhs, "Identidad residual de Catalán/Pell")
    # Q[t]/(t^2-3): only the posterior Pell realization, not a seed generator.
    def mul(x, y):
        return (x[0]*y[0] + 3*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
    rho, lam = (F(2), F(-1)), (F(2), F(1))
    require(mul(rho, lam) == (1, 0), "Inversión de Pell")
    r2 = mul(rho, rho)
    require((1 + r2[0], r2[1]) == tuple(4*x for x in rho),
            "Núcleo en rho: 1+rho^2=4rho")


def check_prime_coefficients():
    primes = [p for p in range(2, 44)
              if all(p % d for d in range(2, p))]
    def pk(k):
        return sum(F(1, p**k) for p in primes)
    for p in primes[1:]:
        require((1-F(2, p))/(1-F(1, p))**2 == 1-F(1, (p-1)**2),
                "Factor local C2")
    for k in range(2, 17):
        require(sum(F(1, p**k) for p in primes[1:]) == pk(k)-F(1, 2**k),
                "Retirada del modo dos")
        require(F(2**k-2, k) > 0, "Peso residual positivo")
    for k in range(1, 11):
        tail_b1 = sum(pk(n)/n for n in range(k+1, 41))
        mid = F(2, k+1)*pk(k+1)
        bound = F(1, 2**k*(k+1))*(1+F(2, k))
        require(0 < tail_b1 <= mid <= bound, "Cota B1 en truncación")
        tail_c2 = sum(F(2**n-2, n)*(pk(n)-F(1, 2**n))
                      for n in range(k+1, 41) if n >= 2)
        bound_c2 = F(3, k+1)*F(2, 3)**(k+1)*(1+F(3, k))
        require(0 < tail_c2 <= bound_c2, "Cota C2 en truncación")
    for y in range(2, 9):
        for m in range(y+1, 15):
            actual = F(1)
            for n in range(y+1, m+1):
                actual *= 1-F(1, (n-1)**2)
            require(actual == F(y-1, y)*F(m, m-1), "Producto telescópico")


def check_action():
    g, h, e2 = F(7, 5), F(5, 11), F(13, 17)
    for r in (F(9, 4), F(1, 7), F(2)):
        gp, hp, ep = g/r, r*h, r*e2
        require((gp*hp, gp*ep) == (g*h, g*e2), "Invariantes de órbita")
        require(hp/h == r and gp == g/(hp/h) and ep == (hp/h)*e2,
                "Separación de órbitas positivas")
        for a, b, d in product(range(-3, 4), repeat=3):
            value, moved = g**a*h**b*e2**d, gp**a*hp**b*ep**d
            require(moved == r**(-a+b+d)*value, "Peso Laurent")
            require((moved == value) == (a == b+d), "Núcleo de pesos")
    swap = [[F(0), F(1)], [F(1), F(0)]]
    rot = [[F(0), F(-1)], [F(1), F(0)]]
    omega = [[F(0), F(1)], [F(-1), F(0)]]
    for r in (F(1), F(2, 3), F(7, 4)):
        d = [[r**-2, F(0)], [F(0), r**2]]
        di = [[r**2, F(0)], [F(0), r**-2]]
        for a, orientation in ((swap, -1), (rot, 1)):
            require(mm(mm(tr(a), di), a) == d, "Forma transportada")
            for root_s in (F(1), F(3, 2), F(5, 7)):
                s = root_s**2
                l = scale(a, root_s)
                require(scale(mm(mm(tr(l), omega), l), 1/s)
                        == scale(omega, orientation), "Forma normalizada orientada")
    # Liouville P dQ on a closed polygon; identity of line integrals is exact.
    polygon = [(F(0), F(0)), (F(2), F(0)), (F(1), F(3)), (F(0), F(0))]
    def action(points):
        return sum((p0+p1)*(q1-q0)/2
                   for (q0, p0), (q1, p1) in zip(points, points[1:]))
    baseline = action(polygon)
    require(baseline != 0, "Control orientado no degenerado")
    for a, orientation in ((swap, -1), (rot, 1)):
        for root_s in (F(3, 2), F(5, 7)):
            l = scale(a, root_s)
            moved = [tuple(mm(l, [[q], [p]])[k][0] for k in range(2))
                     for q, p in polygon]
            require(action(moved)/root_s**2 == orientation*baseline,
                    "Acción cerrada normalizada")


def check_cyclic_resolvent():
    i12 = eye(12)
    c = [[F(i == (j+1) % 12) for j in range(12)] for i in range(12)]
    p3 = scale(add(add(i12, power(c, 3)), add(power(c, 6), power(c, 9))), F(1, 4))
    p4 = scale(add(add(i12, power(c, 4)), power(c, 8)), F(1, 3))
    pm = scale(sub(i12, power(c, 6)), F(1, 2))
    q = mm(p4, pm)
    defect = sub(p3, p4)
    d3, d4 = sub(i12, power(c, 3)), sub(i12, power(c, 4))
    b = add(mm(tr(d3), d3), mm(tr(d4), d4))
    require(trace(q) == 2 and mm(q, q) == q, "Plano cíclico de rango dos")
    require(mm(b, pm) == sub(scale(pm, 5), scale(q, 3)), "B antipodal")
    u = [[F((1, 0, -1, 0)[j % 4])] for j in range(12)]
    v = mm(c, u)
    w = [ur + vr for ur, vr in zip(u, v)]
    j = [[F(0), F(-1)], [F(1), F(0)]]
    require(mm(q, w) == w and mm(tr(w), w) == scale(eye(2), 6),
            "Base normalizable de Q")
    require(mm(c, w) == mm(w, j), "Entrelazador C")
    require(mm(power(c, 3), w) == scale(mm(w, j), -1),
            "Orientación C^3=-C en Q")
    for s in (F(1, 7), F(1, 2), F(4, 5)):
        resolvent_on_q = scale(mm(add(i12, scale(c, s)), q), 1/(1+s*s))
        require(mm(sub(i12, scale(c, s)), resolvent_on_q) == q,
                "Resolvente restringido")
        scalar = mm(mm(tr(v), resolvent_on_q), u)[0][0]/6
        require(scalar == s/(1+s*s), "Coeficiente del núcleo orientado")
        inverse_orientation = scale(mm(sub(i12, scale(c, s)), q), 1/(1+s*s))
        require(mm(mm(tr(v), inverse_orientation), u)[0][0]/6 == -scalar,
                "Inversión del coeficiente")
        f = (1-s**3)/(1-s**4)
        require(f == (1+s+s*s)/((1+s)*(1+s*s)), "Factorización F")
    for n in range(25):
        cn = power(c, n)
        require(mm(mm(tr(v), cn), u)[0][0]/6 == chi4(n), "Todos los residuos del núcleo")
        require(trace(mm(cn, defect)) == 3*(n % 3 == 0)-4*(n % 4 == 0),
                "Tabla producida por trazas")
    # The event values are algebraic fixtures, not certified surviving words.
    ct = tr(c)
    for initial in ([[F(0)]]*12, [[F(j-5)] for j in range(12)]):
        state = [row[:] for row in initial]
        expected = [row[:] for row in initial]
        for m in range(12):
            event = F((m % 10) * (1 if m % 6 < 3 else -1))
            before = mm(mm(tr(state), b), state)[0][0]/2
            eta = scale([[row[0]] for row in ct], event)
            after_state = add(mm(ct, state), eta)
            after = mm(mm(tr(after_state), b), after_state)[0][0]/2
            require(after-before == event*mm(b, state)[0][0]+2*event**2,
                    "Balance con incremento producido")
            require(sum(row[0] for row in after_state)-sum(row[0] for row in state)
                    == event, "Carga de registro")
            state = after_state
            expected[m][0] += event
        require(state == expected, "Retorno con doce recuentos conservados")


def main():
    check_moments()
    check_prime_coefficients()
    check_action()
    check_cyclic_resolvent()
    print(f"COMPROBACIONES_COMPOSICIONES_MOMENTOS_ACCION_OK checks={CHECKS}")
    print("Identidades racionales posteriores, orientación, pesos, eventos y resolvente.")
    print("No verifica generación primaria, selección física ni afirmaciones globales.")


if __name__ == "__main__":
    main()
