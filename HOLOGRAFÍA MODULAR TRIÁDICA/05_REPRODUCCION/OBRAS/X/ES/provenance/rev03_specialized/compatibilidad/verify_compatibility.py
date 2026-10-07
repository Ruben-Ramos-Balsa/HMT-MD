#!/usr/bin/env python3
"""Exact finite checks supporting the proofs; standard library only."""
from fractions import Fraction as F
from itertools import combinations
import json

K = (234,543,140,729,659,824,621,58,914,794,146,601)
B = 1000
Q = sum(K)
t = [F(0)]
for a in K:
    t.append(t[-1]+F(a,Q))

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def minor(i,j):
    return t[j]-t[i]

def positional(k):
    return F(sum(a*B**(len(k)-j-1) for j,a in enumerate(k)),B**len(k)-1)

check(tuple(Q*minor(j-1,j)/minor(0,12) for j in range(1,13))==K,'inverse')
# Change both rows by a nontrivial invertible matrix.
cols=[(2+3*x,5+7*x) for x in t]
dm=lambda i,j:cols[i][0]*cols[j][1]-cols[j][0]*cols[i][1]
check(tuple(Q*dm(j-1,j)/dm(0,12) for j in range(1,13))==K,'row gauge')
checks=0
for a,b,c,d in combinations(range(13),4):
    rhs=(minor(a,b)*minor(c,d)+minor(a,d)*minor(b,c))/minor(a,c)
    check(rhs==minor(b,d),'Plucker mutation')
    checks+=1

subdivisions=[]
for j,a in enumerate(K,1):
    pieces=[F(a,Q*(j+1))]*j+[F(a,Q*(j+1))]
    check(sum(pieces)==F(a,Q),'subdivision')
    subdivisions.extend(pieces)
check(sum(subdivisions)==1,'global subdivision')

kappa=positional(K)
N=kappa*(B**12-1)
check(N.denominator==1,'integer positional numerator')
N=int(N)
decode=lambda n:tuple((n//B**(11-j))%B for j in range(12))
check(decode(N)==K,'digit recovery')
check(round(F(N)+F(1,3))==N and round(F(N)-F(1,3))==N,'precision threshold')
delta=(F(1,10000),F(-B-1,10000),F(B,10000))+(F(0),)*9
analytic=tuple(F(a)+h for a,h in zip(K,delta))
check(all(a>0 for a in analytic),'positive analytic perturbation')
check(sum(analytic)==Q and positional(analytic)==kappa,'continuous counterexample')
check(analytic!=K,'nontrivial continuous fibre')

s0=(F(0),F(1,4),F(1,2),F(1))
lam=(1,2,1,1)
orig=lambda i,j:s0[j]-s0[i]
changed=lambda i,j:lam[i]*lam[j]*orig(i,j)
cross=lambda m:m(0,1)*m(2,3)/(m(0,3)*m(1,2))
check(cross(orig)==cross(changed),'torus cross-ratio')
check(sum(changed(j-1,j)/changed(0,3) for j in range(1,4))==F(3,2),
      'torus is not affine marked gauge')

def f(s):
    return (1+s+s*s)/(1+s+s*s+s**3)
for s in (F(1,5),F(1,3),F(1,2),F(4,5)):
    r=f(s)
    check(F(3,4)<r<1,'constitutive range')
    check(r*s**3+(r-1)*(1+s+s*s)==0,'constitutive cubic')
rplus,rminus=f(F(1,3)),f(F(1,2))
eps,mu=rplus*rplus,rminus*rminus
zhat,chat=rminus/rplus,1/(rplus*rminus)
check(mu*eps==1/chat**2 and mu/eps==zhat**2,'constitutive identities')

for c in (F(1,3),F(1,2),F(3,4)):
    for x in (F(1,7),F(2,7),F(4,7),F(6,7)):
        if x==c:
            continue
        o1=c/(x*(c-x));o2=(1-c)/((x-c)*(1-x));o=1/(x*(1-x))
        check(o1+o2==o,'canonical subdivision')
        check((1+x*(c-x))*o1+o2==o+c,'global pole counterexample')

# A third coplanar facet contributes a rational residue on the same
# ambient divisor even where its real interval is not incident.
x=F(1,2)
paired=1/(x*(1-x))-1/(x*(1-x))
other=1/((x-2)*(3-x))
check(paired==0 and paired+other==F(-4,15),'all coplanar divisor terms')

print(json.dumps({
    'status':'PASS_COMPATIBILITY_EXACT_FINITE_CHECKS',
    'plucker_quadruples':checks,
    'original_files_modified':False,
    'test_scope':['marked_inverse','row_gauge','cluster_exchange',
                  'hereditary_subdivision','integer_decoding',
                  'continuous_fibre_counterexample','column_torus_counterexample',
                  'constitutive_cubic','constitutive_product_quotient',
                  'canonical_subdivision','pole_at_infinity_counterexample',
                  'global_divisor_includes_coplanar_facets'],
    'not_certified':['global_TPK_atlas','general_amplituhedron_coverage',
                     'finite_precision_recovery_from_measured_constants',
                     'all_physical_claims_of_corpus']
},ensure_ascii=False,sort_keys=True))
