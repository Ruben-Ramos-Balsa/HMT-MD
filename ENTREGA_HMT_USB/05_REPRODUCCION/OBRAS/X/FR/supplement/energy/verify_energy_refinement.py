#!/usr/bin/env python3
"""Exact energy, Schur, residual and refinement checks; stdlib, no writes.

Analytic proofs for all positive partitions and all deformation parameters
are provided in energia_refinamiento.tex. This executable checks complete
matrix identities using exact rational arithmetic, including both rational
components of the Q(sqrt(5)) deformation jet at the generated K.
"""
from fractions import Fraction as F
import json

COUNT = 0
K = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
U = ((F(-495,4),F(-233,10)), (F(403,4),F(169,10)),
     (F(-403,4),F(-169,10)), (F(495,4),F(233,10)),
     (F(601,4),F(1031,10)), (F(203,4),F(211,5)),
     (F(-203,4),F(-211,5)), (F(-601,4),F(-1031,10)),
     (F(313,4),F(569,10)), (F(162),F(219,20)),
     (F(-162),F(-219,20)), (F(-313,4),F(-569,10)))


def check(label, actual, expected):
    global COUNT
    if actual != expected:
        raise ArithmeticError(f'{label}: {actual!r} != {expected!r}')
    COUNT += 1


def matrix(rows):
    return [[F(x) for x in row] for row in rows]


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1,b))


def mul(a, b):
    bt=transpose(b)
    return [[sum((x*y for x,y in zip(row,col)), F(0)) for col in bt] for row in a]


def inv(a):
    n=len(a)
    aug=[list(a[i])+eye(n)[i] for i in range(n)]
    for i in range(n):
        j=next((r for r in range(i,n) if aug[r][i]),None)
        if j is None:
            raise ArithmeticError('singular exact block')
        aug[i],aug[j]=aug[j],aug[i]
        divisor=aug[i][i]
        aug[i]=[x/divisor for x in aug[i]]
        for r in range(n):
            if r != i:
                weight=aug[r][i]
                aug[r]=[x-weight*y for x,y in zip(aug[r],aug[i])]
    return [row[n:] for row in aug]


def block(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def stiffness(d):
    a=zeros(len(d)+1,len(d)+1)
    for i,gap in enumerate(d):
        w=1/gap
        a[i][i]+=w; a[i+1][i+1]+=w
        a[i][i+1]-=w; a[i+1][i]-=w
    return a


def stiffness_derivative(d, tangent):
    a=zeros(len(d)+1,len(d)+1)
    for i,(gap,derivative) in enumerate(zip(d,tangent)):
        w=-derivative/gap**2
        a[i][i]+=w; a[i+1][i+1]+=w
        a[i][i+1]-=w; a[i+1][i]-=w
    return a


def restriction(boundary, total):
    r=zeros(len(boundary),total)
    for i,j in enumerate(boundary):
        r[i][j]=F(1)
    return r


def refine(d, proportions):
    fine=[]; boundaries=[0]; h=[eye(len(d)+1)[0]]
    for j,gap in enumerate(d):
        check('fractions normalized',sum(proportions[j]),1)
        theta=F(0)
        for fraction in proportions[j]:
            check('positive refinement',fraction>0,True)
            fine.append(gap*fraction)
            theta+=fraction
            row=[F(0)]*(len(d)+1)
            row[j]=1-theta; row[j+1]=theta
            h.append(row)
        boundaries.append(len(fine))
    return fine,boundaries,h


def schur(a, boundary):
    interior=[i for i in range(len(a)) if i not in boundary]
    aa=block(a,boundary,boundary)
    b=block(a,interior,boundary)
    c=block(a,interior,interior)
    ci=inv(c)
    s=sub(aa,mul(transpose(b),mul(ci,b)))
    return s,b,c,ci,interior


def schur_derivative(a,adot,boundary):
    _,b,_,ci,interior=schur(a,boundary)
    ap=block(adot,boundary,boundary)
    bp=block(adot,interior,boundary)
    cp=block(adot,interior,interior)
    out=sub(ap,mul(transpose(bp),mul(ci,b)))
    out=sub(out,mul(transpose(b),mul(ci,bp)))
    return add(out,mul(transpose(b),mul(ci,mul(cp,mul(ci,b)))))


def energy(d, f):
    return sum((f[j+1]-f[j])**2/gap for j,gap in enumerate(d))


def verify_partition(d, proportions):
    fine,boundary,h=refine(d,proportions)
    a,af=stiffness(d),stiffness(fine)
    r=restriction(boundary,len(fine)+1)
    check('RH identity',mul(r,h),eye(len(d)+1))
    check('harmonic residual matrix',mul(af,h),mul(transpose(r),a))
    check('energy pullback matrix',mul(transpose(h),mul(af,h)),a)
    s,b,c,ci,interior=schur(af,boundary)
    check('Schur equals coarse stiffness',s,a)
    check('exact block inverse',mul(c,ci),eye(len(c)))
    check('harmonic block formula',block(h,interior,range(len(d)+1)),scale(-1,mul(ci,b)))
    f=[F((3*j*j+2*j)%11-4) for j in range(len(d)+1)]
    hf=[row[0] for row in mul(h,[[x] for x in f])]
    z=[F(0) if j in boundary else F((j%7)-3,5) for j in range(len(fine)+1)]
    g=[x+y for x,y in zip(hf,z)]
    check('exact detail energy',energy(fine,g),energy(d,f)+energy(fine,z))
    residual=mul(block(af,interior,range(len(af))),[[x] for x in g])
    correction=mul(transpose(residual),mul(ci,residual))[0][0]
    check('positive residual identity',energy(fine,g)-energy(d,f),correction)
    check('residual nonnegative',correction>=0,True)
    # A complete matrix identity for an arbitrary nonharmonic extension.
    zh=block(h,interior,range(len(d)+1))
    zbad=add(zh,[[F((i+2*j)%5-2,17) for j in range(len(d)+1)] for i in range(len(interior))])
    rbad=add(b,mul(c,zbad))
    extension=[None]*len(af)
    for i,j in enumerate(boundary):extension[j]=eye(len(d)+1)[i]
    for i,j in enumerate(interior):extension[j]=zbad[i]
    defect=sub(mul(transpose(extension),mul(af,extension)),s)
    check('matrix residual Gram',defect,mul(transpose(rbad),mul(ci,rbad)))
    for j,gap in enumerate(d):
        check('recover gap from nodal matrix',-1/a[j][j+1],gap)
    dt,_,_,_,_=schur(a,[0,len(d)])
    check('two-end response',dt,scale(1/sum(d),matrix([[1,-1],[-1,1]])))
    return fine,boundary,h


def main():
    check('K charge',sum(K),6263)
    check('direction sum rational',sum(x[0] for x in U),0)
    check('direction sum radical',sum(x[1] for x in U),0)
    norm_a=sum(a*a+5*b*b for a,b in U)
    norm_b=sum(2*a*b for a,b in U)
    check('source direction norm',(norm_a,norm_b),(F(6638585,20),F(2275584,20)))
    d=[F(k,6263) for k in K]
    proportions=[[F(1,6),F(1,3),F(1,2)] for _ in d]
    fine,boundary,h=verify_partition(d,proportions)
    # Arbitrary exact positive weights instantiate the identity whose proof
    # covers exp(s*u_j); no floating-point exponential is used as evidence.
    weights=[F(j+2,j+1) for j in range(len(d))]
    z=sum(x*w for x,w in zip(d,weights))
    flow_d=[x*w/z for x,w in zip(d,weights)]
    flow_fine,flow_boundary,flow_h=verify_partition(flow_d,proportions)
    check('local interpolation constant along inherited flow',flow_h,h)
    check('refinement keeps same boundary indices',flow_boundary,boundary)
    for j in range(len(d)):
        for c in range(3):
            check('flow and refinement commute',flow_fine[3*j+c],fine[3*j+c]*weights[j]/z)
    # Two full rational components of the exact Q(sqrt(5)) derivative at s=0.
    a,af=stiffness(d),stiffness(fine)
    for component in (0,1):
        v=[x[component] for x in U]
        mean=sum(x*w for x,w in zip(d,v))
        tangent=[x*(w-mean) for x,w in zip(d,v)]
        fine_tangent=[t*p for t,ps in zip(tangent,proportions) for p in ps]
        ap=stiffness_derivative(d,tangent)
        afp=stiffness_derivative(fine,fine_tangent)
        check('tangent normalization',sum(tangent),0)
        check('Schur derivative commutes',schur_derivative(af,afp,boundary),ap)
        check('constant-H energy derivative',mul(transpose(h),mul(afp,h)),ap)
        check('global two-end derivative zero',schur_derivative(a,ap,[0,len(d)]),zeros(2,2))
        check('global interpolation moves',any(tangent),True)
    # Nested nonuniform refinement: composition of harmonic extensions.
    first=[[F(1,3),F(2,3)] for _ in d]
    d1,_,h1=refine(d,first)
    second=[[F(1,4),F(3,4)] for _ in d1]
    d2,_,h2=refine(d1,second)
    direct=[[F(1,12),F(1,4),F(1,6),F(1,2)] for _ in d]
    dd,_,hh=refine(d,direct)
    check('nested subdivision exact',d2,dd)
    check('harmonic extensions compose',mul(h2,h1),hh)
    check('constant vector kernel',mul(stiffness(d),[[F(1)]]*(len(d)+1)),[[F(0)]]*(len(d)+1))
    print(json.dumps({'checks':COUNT,'coarse_edges':len(d),'fine_edges':len(fine),
                      'total_length':str(sum(d)),
                      'flow_derivative_field':'Q(sqrt(5))',
                      'local_interpolation_parameter_independent':True,
                      'global_endpoint_interpolation_parameter_dependent':True,
                      'two_endpoint_response_keeps_only_total_length':True},sort_keys=True))
    print('PASS_K_INTERVAL_ENERGY_SCHUR_EXACT')


if __name__=='__main__':
    main()
