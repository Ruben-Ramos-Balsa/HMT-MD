#!/usr/bin/env python3
"""Control focal de P11, u_K y P10 desde el propietario exacto de II.

No genera K: recibe el registro previamente generado y la representación
de incidencia declarada en el artículo. No certifica una realización física.
"""
from fractions import Fraction as F
from pathlib import Path
import runpy

SOURCE = Path(__file__).resolve().parent/'propietarios_k_moonshine/variacional.py'
V = runpy.run_path(str(SOURCE), run_name='propietario_importado')
add, sub, mul, inv = (V[k] for k in ('q5_add', 'q5_sub', 'q5_mul', 'q5_inv'))
mm, mv = V['matmul'], V['matrix_vector']
P3 = V['projector_three']()
P11 = [[(F(int(i == j)) - F(1,12), F(0)) for j in range(12)] for i in range(12)]
K = [(F(k), F(0)) for k in (234,543,140,729,659,824,621,58,914,794,146,601)]
u = mv(P3, mv(P11, K))
n = V['dot'](u,u)
E = [[mul(mul(x,y), inv(n)) for y in u] for x in u]
P10 = [[sub(P11[i][j], E[i][j]) for j in range(12)] for i in range(12)]
tests = {
    'norm_u_exact': n == (F(6638585,20), F(2275584,20)),
    'norm_u_positive': V['q5_sign'](n) == 1,
    'P3_rank': V['rank'](P3) == 3,
    'P11_rank': V['rank'](P11) == 11,
    'P3_P11': mm(P3,P11) == P3,
    'P11_P3': mm(P11,P3) == P3,
    'E_projector': mm(E,E) == E,
    'E_rank': V['rank'](E) == 1,
    'P11_E': mm(P11,E) == E,
    'E_P11': mm(E,P11) == E,
    'P10_symmetric': V['transpose'](P10) == P10,
    'P10_projector': mm(P10,P10) == P10,
    'P10_rank': V['rank'](P10) == 10,
    'P10_trace': V['trace'](P10) == (F(10),F(0)),
    'P10_u_zero': mv(P10,u) == [(F(0),F(0))]*12,
    'P10_uniform_zero': mv(P10,[(F(1),F(0))]*12) == [(F(0),F(0))]*12,
}
for name, ok in tests.items():
    if not ok:
        raise RuntimeError(name)
print('PASS_K_P10_FOCAL', len(tests))
print('norm2_uK =', V['q5_text'](n))
