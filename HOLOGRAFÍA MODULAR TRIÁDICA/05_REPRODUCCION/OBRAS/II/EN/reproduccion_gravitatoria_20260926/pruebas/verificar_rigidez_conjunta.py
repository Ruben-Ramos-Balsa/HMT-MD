"""Exact focal checks for the two-product radial rigidity theorem.

No measured G, tabulated Planck length or fitted coefficient is an input.
The physical interpretation of the reduced radial reader is an explicit
premise; these checks do not establish experimental identification.
"""
from fractions import Fraction as F
import argparse
import hashlib
import json
from pathlib import Path


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def scale(s, a):
    return [[s*x for x in row] for row in a]


def inv2(a):
    (a0, b), (c, d) = a
    det = a0*d-b*c
    return [[d/det, -b/det], [-c/det, a0/det]]


def main():
    checks = []
    def ck(name, value):
        if not value:
            raise AssertionError(name)
        checks.append(name)
    eye = [[F(1), F(0)], [F(0), F(1)]]
    # On the zero space all operator identities hold for distinct scalars.
    # This negative control explains why scalar uniqueness needs a nonzero fiber.
    empty = []
    ck('zero-fiber-does-not-identify-scalar',
       F(1) != F(2) and scale(F(1),empty) == scale(F(2),empty)
       and mm(empty,empty) == scale(F(3),empty))
    matrices = [[[F(2),F(1)],[F(1),F(3)]],
                [[F(7,3),F(2,5)],[F(2,5),F(11,7)]]]
    for idx, H in enumerate(matrices):
        for jdx, (L,c,hbar) in enumerate(((F(3),F(5),F(7)),
                                         (F(2,7),F(11,13),F(17,19)))):
            tag = f'{idx}-{jdx}'
            lam = scale(hbar*c,inv2(H))
            radial = scale(L*L,inv2(lam))
            mass = scale(1/(c*c),H)
            G = c**3*L**2/hbar
            ck(tag+'-phase-product',mm(H,lam)==scale(hbar*c,eye))
            ck(tag+'-area-product',mm(radial,lam)==scale(L*L,eye))
            ck(tag+'-G',radial==scale(G/c**2,mass))
            for z in (F(1,2),F(2),F(5760,5759)):
                Rnew = scale(z,radial)
                lamnew = scale(1/z,lam)
                ck(tag+str(z)+'-single-scale-rejected',mm(Rnew,lam)!=scale(L*L,eye))
                ck(tag+str(z)+'-paired-area-preserved',mm(Rnew,lamnew)==scale(L*L,eye))
                ck(tag+str(z)+'-paired-phase-rejected',mm(H,lamnew)!=scale(hbar*c,eye))
            # A nonorthogonal coordinate change uses opposite congruences
            # for the dual length, preserving both products up to similarity.
            T = [[F(1),F(1)],[F(0),F(1)]]
            Ti = inv2(T)
            tr = lambda a: [list(x) for x in zip(*a)]
            Hc = mm(mm(tr(Ti),H),Ti)
            Rc = mm(mm(tr(Ti),radial),Ti)
            Lc = mm(mm(T,lam),tr(T))
            ck(tag+'-congruence-phase',mm(Hc,Lc)==scale(hbar*c,eye))
            ck(tag+'-congruence-area',mm(Rc,Lc)==scale(L*L,eye))
            ck(tag+'-congruence-proportionality',Rc==scale(L*L/(hbar*c),Hc))

    # Exponents (mass, time, length) of c^a L^b hbar^d.
    a,b,d = F(3),F(2),F(-1)
    ck('dimensions-mass',d==-1)
    ck('dimensions-time',-a-d==-2)
    ck('dimensions-length',a+b+2*d==3)
    dimension_matrix = [[F(0),F(0),F(1)],
                        [F(-1),F(0),F(-1)],
                        [F(1),F(1),F(2)]]
    a0,b0,c0 = dimension_matrix[0]
    d0,e0,f0 = dimension_matrix[1]
    g0,h0,i0 = dimension_matrix[2]
    det = a0*(e0*i0-f0*h0)-b0*(d0*i0-f0*g0)+c0*(d0*h0-e0*g0)
    ck('dimension-matrix-nonsingular',det==-1)
    N = 12*4*120
    r = F(N-1,4*N)
    ck('incidence-count',N==5760)
    ck('marked-return',r==F(5759,23040))
    ck('complement',r+F(1,4*N)==F(1,4))
    ck('whole-archive-not-observed-return',r!=F(1,4))
    # Strictly negative f'(s), and positive rational part of H_B'(s):
    # adding -log(s)/(10*pi*s) is positive on 0<s<1.
    for k in range(1,20):
        s = F(k,20)
        fp = -s*s*(s*s+2*s+3)/(1+s+s*s+s**3)**2
        positive = 36*s*s*(1+2*s**9)/(1-s**9)**2
        subtracted = 4*s**3*(1+2*s**12)/(1-s**12)**2
        ck(f'constitutive-f-{k}',fp<0)
        ck(f'constitutive-H-{k}',positive>9*subtracted)
        f = (1-s**3)/(1-s**4)
        kernel = s/(1+s*s)
        ck(f'Catalan-to-constitutive-{k}',(1+s+s*s)/(s*(1+s))*kernel==f)
        ck(f'constitutive-to-Catalan-{k}',s*(1+s)/(1+s+s*s)*f==kernel)
        for terms in (1,4,9):
            # Applying D^2 cancels the two powers of the odd denominator.
            d2_partial = sum(F((-1)**j,(2*j+1)**2)*(2*j+1)**2*s**(2*j+1)
                             for j in range(terms))
            tail = F((-1)**terms)*s**(2*terms+1)/(1+s*s)
            ck(f'Catalan-Euler-remainder-{k}-{terms}',d2_partial+tail==kernel)
    files = [Path(__file__).resolve(),Path(__file__).resolve().parents[1] / 'demostraciones' / 'RIGIDEZ_Y_EXPLICACION_ESTRUCTURAL.md']
    return {'status':'PASS_FOCAL_RADIAL_RIGIDITY', 'checks':len(checks),
            'check_names':checks,
            'scope':{'theorem':'two normalized products, fixed positive sections, reduced radial reading on a nonzero fiber for scalar uniqueness',
                     'full_TPK_rerun':False,'experimental_identification_certified':False,
                     'absence_of_counterexample_used_as_proof':False},
            'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt',type=Path)
    args = parser.parse_args()
    result = main()
    encoded = json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.receipt:
        args.receipt.write_text(encoded,encoding='utf-8')
        print(json.dumps({k:result[k] for k in ('status','checks','scope')},ensure_ascii=False))
    else:
        print(encoded,end='')
