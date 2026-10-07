#!/usr/bin/env python3
"""Comprobación entera focal de APP-004–008 y APP-016–019.

No certifica el resto del inventario ni reproduce la generación de constantes.
"""
import json

def rho(n):
    assert n > 0
    return 1 + (n - 1) % 9

def read(n):
    r = rho(n)
    q = (n-r)//9
    assert n == r+9*q
    return r, q

def cell(i, j):
    return read(i+j), read(i*j)

def main():
    totals = [0]*6
    for i in range(1, 10):
        for j in range(1, 10):
            (a, qa), (b, qb) = cell(i, j)
            totals = [x+y for x,y in zip(totals, (i+j, i*j, a, b, qa, qb))]
    assert totals == [810, 2025, 405, 459, 45, 174]
    assert totals[1]-totals[0] == (totals[3]-totals[2])+9*(totals[5]-totals[4])
    assert cell(5,5) == ((1,1),(7,2))
    assert cell(8,2) == ((1,1),(7,1))
    direct = [x % 3 for x in (3,6,9)]
    internal = [(x//3) % 3 for x in (3,6,9)]
    assert direct == [0,0,0]
    assert internal == [1,2,0]
    image = sorted({(3*x)%9 for x in range(9)})
    kernel = [x for x in range(9) if (3*x)%9 == 0]
    assert image == kernel == [0,3,6]
    assert all((x*y)%9 == 0 for x in image for y in image)
    print(json.dumps({'status':'PASS_APP_ELEMENTAL_FOCAL', 'cells':81,
        'totals':totals, 'cell_5_5':cell(5,5), 'cell_8_2':cell(8,2),
        'direct_mod3':direct, 'internal_coordinate':internal,
        'image_times3':image, 'kernel_times3':kernel,
        'scope':'Arithmetic checks only; not a global HMT proof'}, indent=2))

if __name__ == '__main__':
    main()
