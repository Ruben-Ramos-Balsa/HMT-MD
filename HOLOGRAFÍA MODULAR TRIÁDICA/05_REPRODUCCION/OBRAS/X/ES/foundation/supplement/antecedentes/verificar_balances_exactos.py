"""Controles racionales exactos de las identidades finitas del desarrollo.

No verifica el teorema espectral infinito ni identificaciones físicas.
No usa constantes objetivo. Sólo biblioteca estándar; salida JSON a stdout.
"""
from fractions import Fraction as F
import json


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def tr(a):
    return [list(x) for x in zip(*a)]


def mm(a, b):
    bt = tr(b)
    return [[sum((x*y for x, y in zip(r, c)), F(0)) for c in bt] for r in a]


def plus(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(q, a):
    return [[q*x for x in row] for row in a]


def minus(a, b):
    return plus(a, scale(-1, b))


def block(a, count):
    n = len(a)
    return [[a[i % n][j % n] if i//n == j//n else F(0)
             for j in range(n*count)] for i in range(n*count)]


def cyclic(n):
    return [[F(i == (j+1) % n) for j in range(n)] for i in range(n)]


def costura(c):
    n = len(c)
    out = [[F(0) for _ in range(9*n)] for _ in range(9*n)]
    for i in range(n):
        for j in range(n):
            out[i][8*n+j] = c[i][j]
    for phase in range(1, 9):
        for i in range(n):
            out[phase*n+i][(phase-1)*n+i] = F(1)
    return out


def setup(c):
    n = len(c)
    j = [[F(i % n == k, 3) for k in range(n)] for i in range(9*n)]
    p = mm(j, tr(j))
    u = costura(c)
    t = mm(mm(tr(j), u), j)
    eta = mm(minus(eye(9*n), p), mm(u, j))
    return j, p, u, t, eta


def main():
    passed = []

    def check(name, condition):
        if not condition:
            raise RuntimeError('Fallo: '+name)
        passed.append(name)

    n = 3
    c = cyclic(n)
    j, p, u, t, eta = setup(c)
    identity = eye(n)
    check('inclusion_isometrica', mm(tr(j), j) == identity)
    check('costura_unitaria', mm(tr(u), u) == eye(9*n))
    check('compresion_8I_mas_C', t == scale(F(1, 9), plus(scale(8, identity), c)))
    check('balance_norma', plus(mm(tr(t), t), mm(tr(eta), eta)) == identity)
    defect = mm(tr(minus(identity, c)), minus(identity, c))
    check('factor_8_81', mm(tr(eta), eta) == scale(F(8, 81), defect))

    a = plus(identity, scale(F(1, 4), plus(c, tr(c))))
    a9 = block(a, 9)
    check('observable_conmuta', mm(a, c) == mm(c, a))
    check('observable_completo_conservado', mm(mm(tr(u), a9), u) == a9)
    memory_a = mm(mm(tr(eta), a9), eta)
    check('balance_carga', plus(mm(mm(tr(t), a), t), memory_a) == a)
    tn = identity
    total = scale(0, identity)
    for step in range(1, 13):
        total = plus(total, mm(mm(tr(tn), memory_a), tn))
        tn = mm(t, tn)
        check('telescopia_N_'+str(step), plus(mm(mm(tr(tn), a), tn), total) == a)

    pf = [[F(1, n) for _ in range(n)] for _ in range(n)]
    check('sector_fijo_terminal', mm(t, pf) == pf)
    check('memoria_anula_sector_fijo', mm(eta, pf) == [[F(0)]*n for _ in range(9*n)])
    centered = minus(identity, pf)
    check('C3_fijo_libre_factor_19_27',
          mm(mm(tr(t), t), centered) == scale(F(19, 27), centered))
    check('C3_fijo_libre_memoria_8_27',
          mm(mm(tr(eta), eta), centered) == scale(F(8, 27), centered))
    check('omitir_memoria_es_falso', mm(tr(t), t) != identity)
    bad = [[F(i+1 if i == k else 0) for k in range(n)] for i in range(n)]
    bad9 = block(bad, 9)
    check('omitir_invariancia_observable_es_falso',
          plus(mm(mm(tr(t), bad), t), mm(mm(tr(eta), bad9), eta)) != bad)

    r = [[F(i == n-1-k) for k in range(n)] for i in range(n)]
    cp = mm(mm(r, c), tr(r))
    _, _, _, tp, ep = setup(cp)
    check('carta_no_conmuta', mm(r, c) != mm(c, r))
    check('covariancia_compresion', mm(tp, r) == mm(r, t))
    check('covariancia_memoria', mm(ep, r) == mm(block(r, 9), eta))

    # Transportes no isometricos: se conserva su defecto adicional exacto.
    c_half = scale(F(1, 2), c)
    _, _, _, th, eh = setup(c_half)
    full_defect = plus(mm(tr(eh), eh), scale(F(1, 9), minus(identity, mm(tr(c_half), c_half))))
    check('defecto_costura_no_unitaria', minus(identity, mm(tr(th), th)) == full_defect)
    check('suprimir_defecto_costura_es_falso', minus(identity, mm(tr(th), th)) != mm(tr(eh), eh))

    # Forma eliptica: a=exp(eta/2), con valores racionales de prueba.
    def diag2(x, y):
        return [[F(x), F(0)], [F(0), F(y)]]

    a0, a1 = F(2), F(3)
    m0_inv, m1 = diag2(1/a0, a0), diag2(a1, 1/a1)
    d0, d1 = diag2(a0**-2, a0**2), diag2(a1**-2, a1**2)
    rot = [[F(3, 5), F(4, 5)], [-F(4, 5), F(3, 5)]]
    omega_form = [[F(0), F(1)], [F(-1), F(0)]]
    transport = mm(mm(m1, rot), m0_inv)
    check('forma_variable_transporte_simplectico',
          mm(mm(tr(transport), omega_form), transport) == omega_form)
    check('forma_variable_conservacion_accion',
          mm(mm(tr(transport), d1), transport) == d0)
    eta_dot, omega = F(3), F(5)
    fixed_field = scale(omega, mm(omega_form, d0))
    connection = diag2(eta_dot/2, -eta_dot/2)
    field = plus(fixed_field, connection)
    d_dot = diag2(-eta_dot*a0**-2, eta_dot*a0**2)
    zero2 = scale(0, eye(2))
    check('forma_variable_derivada_accion_cero',
          plus(d_dot, plus(mm(tr(field), d0), mm(d0, field))) == zero2)
    check('omitir_conexion_forma_variable_es_falso',
          plus(d_dot, plus(mm(tr(fixed_field), d0), mm(d0, fixed_field))) != zero2)

    print(json.dumps({'status': 'PASS_BALANCES_RACIONALES_EXACTOS',
                      'checks': len(passed), 'names': passed,
                      'scope': 'Identidades finitas; el limite infinito tiene prueba escrita separada.'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
