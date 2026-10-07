#!/usr/bin/env python3
"""Exact finite witnesses for the written energy-limit proof.

These checks do not replace the quantified analytic proof in
01_LIMITE_ENERGETICO.md. All arithmetic here is rational.
"""
from fractions import Fraction as F
import json

checks = 0

def require(statement, message):
    global checks
    checks += 1
    if not statement:
        raise RuntimeError(message)

K = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
d = [F(k, sum(K)) for k in K]

def nodes(level):
    points = [F(0)]
    for length in d:
        left = points[-1]
        count = 3**level
        points.extend(left + length*F(i, count) for i in range(1, count+1))
    return points

def energy(points, values):
    return sum((values[i+1]-values[i])**2/(points[i+1]-points[i])
               for i in range(len(points)-1))

energies = []
details = []
for level in range(5):
    x = nodes(level)
    values = [t*t for t in x]
    E = energy(x, values)
    deficit = F(4,3)-E
    widths = [b-a for a,b in zip(x,x[1:])]
    require(deficit == sum(h**3/F(3) for h in widths), 'Exact quadratic error')
    require(deficit == sum(h**3/F(3) for h in d)/9**level, 'Geometric energy convergence')
    require(x[0] == 0 and x[-1] == 1, 'Fixed endpoints')
    require(all(h > 0 for h in widths), 'Positive mesh')
    require(max(widths) == max(d)/3**level, 'Mesh contraction')
    if level:
        old = nodes(level-1)
        old_values = [t*t for t in old]
        extension = []
        for i in range(len(old)-1):
            a,b = old[i:i+2]
            extension.extend(old_values[i]+F(c,3)*(old_values[i+1]-old_values[i]) for c in range(3))
        extension.append(old_values[-1])
        z = [v-w for v,w in zip(values,extension)]
        require(all(z[i] == 0 for i in range(0,len(z),3)), 'Detail has zero old trace')
        Ez = energy(x,z)
        require(E == energies[-1]+Ez, 'Orthogonal energy decomposition')
        details.append(Ez)
        require(E == energies[0]+sum(details), 'Telescoping detail energies')
        require(energy(x,extension) == energies[-1], 'Inherited affine extension')
        cross = sum((extension[i+1]-extension[i])*(z[i+1]-z[i])/(x[i+1]-x[i])
                    for i in range(len(x)-1))
        require(cross == 0, 'Cross term vanishes')
    energies.append(E)

# A bounded visible trace alone is not the finite-energy hypothesis.
# On [0,1], the continuous tent with height 1 supported on an interval of
# length h has energy 4/h; reducing h preserves its maximum and endpoints
# but makes its energy unbounded.
for n in range(1,6):
    h = F(1,3**n)
    x = [F(0),h/2,h,F(1)]
    v = [F(0),F(1),F(0),F(0)]
    require(energy(x,v) == 4/h, 'Energy hypothesis cannot be replaced by bounded height')

print(json.dumps({'status':'PASS_K_ENERGY_LIMIT_FINITE_WITNESSES',
                  'exact_checks':checks,
                  'levels':5,
                  'target_energy_for_x_squared':'4/3',
                  'last_energy':str(energies[-1]),
                  'proof_scope':'Finite exact witnesses; the infinite theorem is proved in prose.'},
                 ensure_ascii=False))
