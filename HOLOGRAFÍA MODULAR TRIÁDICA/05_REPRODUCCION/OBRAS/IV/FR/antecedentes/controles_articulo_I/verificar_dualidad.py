#!/usr/bin/env python3
"""Control exacto finito adicional de las pruebas de dualidad del PDF."""
from fractions import Fraction as F

def q(x, radius):
    return x[0]**2/radius**2+x[1]**2*radius**2

def energy(x, radius, lattice):
    a, b = lattice
    vertex = -(F(x[0]*a)/radius**2+F(x[1]*b)*radius**2)/(F(a*a)/radius**2+F(b*b)*radius**2)
    floor = vertex.numerator//vertex.denominator
    return min(q((x[0]+k*a,x[1]+k*b),radius) for k in (floor,floor+1))

checks = 0
for radius in (F(1,3),F(1,2),F(1),F(2),F(3),F(7,5)):
    for m in range(-12,13):
        for w in range(-12,13):
            x = (m,w)
            if q(x,radius) != q((w,m),1/radius):
                raise RuntimeError('Invariancia cuadrática')
            if energy(x,radius,(9,-1)) != energy((w,m),1/radius,(-1,9)):
                raise RuntimeError('Dualidad de cocientes')
            if energy(x,radius,(9,-1)) != energy((m+9,w-1),radius,(9,-1)):
                raise RuntimeError('Cambio de representante')
            checks += 3
print('PASS_DUALIDAD_NORMALIZADA_Y_COCIENTE', checks)
