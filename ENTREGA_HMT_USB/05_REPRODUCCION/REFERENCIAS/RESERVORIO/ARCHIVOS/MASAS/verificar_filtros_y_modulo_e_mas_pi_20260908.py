"""Checks focales de §§16–18; no genera ni clasifica constantes.

Las pruebas generales están en la nota E_MAS_PI_RETORNOS_NATIVOS_729_...
Este archivo implementa un filtro necesario entre fronteras ya producidas
y comprueba identidades en aritmética racional exacta. No implementa por sí
solo la sección forward, no convierte una frontera decimal en generador,
no recibe objetivos metrológicos y no certifica racionalidad/irracionalidad.
Los valores racionales de las pruebas son variables de ensayo algebraico;
ninguno se interpreta como una coordenada de las constantes HMT.
"""

from fractions import Fraction as Q


def ceil_div(n, d):
    assert d > 0
    return -((-n) // d)


def cylinder_interval(P, T, M, block_max=728):
    """Enteros t en [0, block_max] que satisfacen -T < P+T*t < M."""
    if T <= 0 or M <= 0:
        raise ValueError("Las escalas de los cilindros deben ser positivas")
    lo = max(0, (-T - P) // T + 1)
    hi = min(block_max, ceil_div(M - P, T) - 1)
    return None if lo > hi else (lo, hi)


def interval_sum(left, right):
    if left is None or right is None:
        return None
    return (left[0] + right[0], left[1] + right[1])


def difference_envelope(first, later):
    """Intervalo exterior para una emisión posterior menos la primera."""
    if first is None or later is None:
        return None
    return (later[0] - first[1], later[1] - first[0])


def carry_relation(delta_interval, base=729):
    if delta_interval is None:
        return frozenset()
    lo, hi = delta_interval
    return frozenset(
        (j, nxt)
        for j in (-1, 0, 1)
        for nxt in (-1, 0, 1)
        if lo <= base * j - nxt <= hi
    )


def surviving_carries(delta_intervals, initial=(-1, 0, 1)):
    """Filtro exterior no estacionario. Vacío rechaza esa ventana."""
    current = frozenset(initial)
    for interval in delta_intervals:
        relation = carry_relation(interval)
        current = frozenset(nxt for j, nxt in relation if j in current)
        if not current:
            break
    return current


def matrix_product(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def matrix_difference(left, right):
    return tuple(tuple(left[i][j] - right[i][j] for j in range(2)) for i in range(2))


def check_intervals():
    checked = 0
    for T in (1, 2, 7, 1000):
        for M in (1, 3, 729, 2187):
            for P in (-M - T - 1, -T, 0, M - 1, M, M + T):
                interval = cylinder_interval(P, T, M)
                predicted = [] if interval is None else list(range(interval[0], interval[1] + 1))
                direct = [t for t in range(729) if -T < P + T * t < M]
                assert predicted == direct, (P, T, M, interval)
                checked += 1
    return checked


def check_carries():
    labels = {729 * j - nxt: (j, nxt) for j in (-1, 0, 1) for nxt in (-1, 0, 1)}
    assert len(labels) == 9
    for value, pair in labels.items():
        assert carry_relation((value, value)) == frozenset((pair,))
    assert carry_relation((2, 727)) == frozenset()
    assert carry_relation((729, 729)) and carry_relation((730, 730))
    assert not surviving_carries(((729, 729), (730, 730)))
    assert surviving_carries(((729, 729), (1, 1))) == frozenset((-1,))
    assert difference_envelope((10, 20), (30, 45)) == (10, 35)
    assert interval_sum((10, 20), (30, 45)) == (40, 65)


def check_modulus_identities():
    J = ((Q(0), Q(-1)), (Q(1), Q(0)))
    M0 = ((Q(0), Q(-5)), (Q(9), Q(0)))
    for y in (Q(1, 3), Q(1, 2), Q(2, 3), Q(3, 4), Q(1), Q(2)):
        E = ((Q(1), Q(0)), (Q(0), y))
        Einv = ((Q(1), Q(0)), (Q(0), 1 / y))
        L = matrix_product(matrix_product(E, M0), Einv)
        assert L == ((0, -5 / y), (9 * y, 0))
        assert matrix_product(L, L) == ((-45, 0), (0, -45))
        commutator = matrix_difference(matrix_product(L, J), matrix_product(J, L))
        coefficient = 9 * y - 5 / y
        assert commutator == ((coefficient, 0), (0, -coefficient))
        sigma = (1 - y * y) / (1 + y * y)
        rho = 2 * y / (1 + y * y)  # A=1, rho=sqrt(1-sigma^2)>0.
        assert (1 - sigma) / (1 + sigma) == y * y
        assert coefficient == 2 * (2 - 7 * sigma) / rho


def check_algebraic_inversion():
    # D es aquí una variable racional abstracta. No se evalúa ninguna
    # exponencial ni se pretende satisfacer la condición analítica (42).
    checked = 0
    for a in (Q(1, 100), Q(1, 50)):
        for p in (Q(2), Q(3)):
            for h in (Q(1, 2), Q(2, 3)):
                for D in (Q(1, 3), Q(2, 3)):
                    Cc = 169 * a**6 + D * a**7 / (1 - D * a)
                    eta_ret = h - 90 * Cc / p
                    sigma = (eta_ret + a) / (500 * a)
                    B = p * (h + a - 500 * a * sigma) / 90 - 169 * a**6
                    assert B == D * a**7 / (1 - D * a)
                    assert a**7 + a * B == a**7 / (1 - D * a)
                    assert D == B / (a**7 + a * B)
                    checked += 1
    return checked


if __name__ == "__main__":
    interval_cases = check_intervals()
    check_carries()
    check_modulus_identities()
    inversion_cases = check_algebraic_inversion()
    print("IDENTIDADES_FOCALES_VERIFICADAS")
    print(f"Intervalos: {interval_cases}; inversión algebraica: {inversion_cases}; acarreos y conmutadores: correctos.")
    print("Sin cifras de constantes. Sin clasificación de e+pi. Sin certificación universal de supervivencia.")
