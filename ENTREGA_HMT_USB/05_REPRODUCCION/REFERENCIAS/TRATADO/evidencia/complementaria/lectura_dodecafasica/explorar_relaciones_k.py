#!/usr/bin/env python3
"""Exploración exacta, no normativa, de relaciones entre las cuatro palabras.

No prueba procedencia; sirve para detectar identidades aritméticas candidatas
que después deben formularse sin emplear el valor objetivo de alpha.
"""

from itertools import product

PI = (141,592,653,589,793,238,462,643,383,279,502,884)
EE = (718,281,828,459,45,235,360,287,471,352,662,497)
PHI = (618,33,988,749,894,848,204,586,834,365,638,117)
ALPHA = (7,297,352,569,283,800,997,285,105,472,380,663)
K = (234,543,140,729,659,824,621,58,914,794,146,601)


def h4(block):
    a,b,c,d=block
    return (a+b+c+d,a+b-c-d,a-b+c-d,a-b-c+d)


def main():
    print("residuos mod 3")
    for name, x in (("pi",PI),("e",EE),("phi",PHI),("alpha",ALPHA),("K",K)):
        print(name, ''.join(str(v%3) for v in x))
    print("H4 por orbitas")
    for name,x in (("pi",PI),("e",EE),("phi",PHI),("alpha",ALPHA),("K",K)):
        print(name,[h4(x[r::3]) for r in range(3)])
    # Busca identidades afines de coeficientes pequeños, coordenada a coordenada mod 1000.
    hits=[]
    for a,b,c,d in product(range(-4,5), repeat=4):
        if a==b==c==d==0:
            continue
        if all((a*PI[i]+b*EE[i]+c*PHI[i]+d) % 1000 == K[i] for i in range(12)):
            hits.append((a,b,c,d))
    print("afines pequenas hacia K",hits)


if __name__ == "__main__":
    main()
