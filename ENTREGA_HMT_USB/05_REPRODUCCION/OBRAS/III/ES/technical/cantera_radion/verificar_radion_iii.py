#!/usr/bin/env python3
"""Controles focales de la incorporación radional de III.

No genera constantes HMT ni usa valores metrológicos.
Comprueba identidades finitas, dominios y composiciones ya declaradas.
Los testigos x,y son racionales de prueba; no son parámetros físicos.
"""
from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json
import hashlib
import re

HERE = Path(__file__).resolve().parent

def subtract(left, right, terminal):
    carry = terminal
    rests = []
    states = []
    for t, v in zip(reversed(left), reversed(right)):
        raw = t-v+carry
        c, r = divmod(raw, 1000)
        assert raw == 1000*c+r and 0 <= r < 1000
        rests.append(r)
        states.append(c)
        carry = c
    return list(reversed(rests)), carry, list(reversed(states))

def fraction_word(word):
    return sum((Q(v, 1000**i) for i, v in enumerate(word, 1)), Q(0))

def main():
    checks = []
    def check(name, assertion):
        if not assertion:
            raise AssertionError(name)
        checks.append(name)
    active = {1, 4, 7, 2, 5, 8}
    pairs = tuple(combinations(sorted(active), 2))
    check("active_pairs_15", len(pairs)==15)
    d6 = tuple(product(sorted(active), pairs))
    check("sector90", len(d6)==90)
    check("sector120", 8*len(pairs)==120)
    check("two_sheet_density", Q(2*len(d6), 3**6)==Q(20,81))
    check("single_sheet_distinct", Q(len(d6),3**6)==Q(10,81))
    check("calendar_second50_unique",
          [m for m in range(1,13) if 30*m-10 == 50]==[2])
    check("phase50_fraction", Q(50,360)==Q(5,36))
    p_lo,p_hi = Q("3.14159"), Q("3.14160")
    a_lo,a_hi = Q("0.00729735"), Q("0.00729736")
    se_lo = 2*p_lo*(Q(5,36)+Q(25,9)*a_lo)
    se_hi = 2*p_hi*(Q(5,36)+Q(25,9)*a_hi)
    check("unit_cell_from_declared_cylinders", 1 < se_lo < se_hi < 2)
    check("ambient_complement270", 1000-1-3**6==270)
    # Todos son operandos finitos ficticios para controlar la división.
    words = [(0,), (999,), (0,0,0), (999,999,999),
             (125,0,5), (0,998,3), (40,51,600), (900,1,5)]
    count=0
    for left in words:
        for right in words:
            if len(left) != len(right):
                continue
            for terminal in (-1,0,1):
                rests, c1, _ = subtract(left,right,terminal)
                lhs = c1+fraction_word(rests)
                rhs = fraction_word(left)-fraction_word(right)+Q(terminal,1000**len(left))
                assert lhs==rhs
                count+=1
    check("subcarry_telescoping_cases_"+str(count), count>0)
    for n in range(-108,217):
        q,r=divmod(n,9)
        q2,r2=divmod(n+9,9)
        assert (r2,q2)==(r,q+1)
    check("nonadic_return_memory_325_cases", True)

    with localcontext() as ctx:
        ctx.prec=200
        tol=D("1e-85")
        def f(s):
            return (1+s+s*s)/(1+s+s*s+s*s*s)
        def inverse(r):
            lo,hi=D(0),D(1)
            for _ in range(840):
                mid=(lo+hi)/2
                if f(mid)>r: lo=mid
                else: hi=mid
            return (lo+hi)/2
        tests=[(D(1)/8,D(1)/30),(D(2)/3,-D(1)/4),
               (D(1)/5,D(0))]
        distinct=0
        for j,(x,y) in enumerate(tests):
            qp=(-(x+y)).exp(); qm=(-(x-y)).exp()
            sp,sm=qp**30,qm**30
            rp,rm=f(sp),f(sm)
            zh,ch=rm/rp,1/(rp*rm)
            rp2=1/(zh*ch).sqrt(); rm2=(zh/ch).sqrt()
            sp2,sm2=inverse(rp2),inverse(rm2)
            check("inverse_cubic_"+str(j),
                  abs(sp-sp2)<tol and abs(sm-sm2)<tol)
            for s,r in ((sp2,rp2),(sm2,rm2)):
                assert abs(r*s**3+(r-1)*(1+s+s*s))<tol
            check("cubic_equation_"+str(j),True)
            eta=((x+y)/(x-y)).ln()/2
            eta2=(sp2.ln()/sm2.ln()).ln()/2
            ratio2=(sp2.ln()-sm2.ln())/(sp2.ln()+sm2.ln())
            zlc=(-eta).exp()
            zlc2=(sm2.ln()/sp2.ln()).sqrt()
            check("shape_reconstruction_"+str(j),
                  abs(eta-eta2)<tol and abs(zlc-zlc2)<tol and abs(y/x-ratio2)<tol)
            check("sheet_swap_"+str(j),
                  abs((sp.ln()/sm.ln()).sqrt()*zlc-1)<tol)
            check("constitutive_swap_"+str(j), abs((rp/rm)*zh-1)<tol)
            if y:
                distinct += int(abs(zh-zlc)>D("1e-8"))
        check("vacuum_and_LC_not_identified", distinct==2)
        # Cierre: valores racionales de prueba, no cifras objetivo.
        for p,u,a in ((D(3),D(2),D(1)/100),
                      (D(7)/2,D(5)/2,D(1)/200)):
            delta=(p-u*p.ln())/270*(1+p/729)
            se=2*p*(D(5)/36+D(25)*a/9)
            st=1+D(20)*delta/81
            eps=st-se
            assert abs(se-D(20)*delta/81+eps-1)<tol
            deg=D(180)/p
            assert abs(deg-(50+1000*a-D(20)*delta*deg/81+eps*deg))<tol
        check("unit_and_degree_closure_algebraic_witnesses",True)
    hashes={}
    for name in ("radion_iii.tex", "insercion_focal_constitutiva_LC.tex"):
        text=(HERE/name).read_text(encoding="utf-8")
        labels=re.findall(r"\\label\{([^}]+)\}",text)
        check("unique_local_labels_"+name,len(labels)==len(set(labels)))
        hashes[name]=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
    result={"status":"PASS_RADION_III_FOCAL",
            "scope":"Finite identities and reader-composition regression tests; not a new certificate of the HMT generators or SI identification",
            "checks":checks,
            "checks_count":len(checks),
            "artifact_sha256":hashes,
            "se_bounds_exact":[str(se_lo),str(se_hi)]}
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
