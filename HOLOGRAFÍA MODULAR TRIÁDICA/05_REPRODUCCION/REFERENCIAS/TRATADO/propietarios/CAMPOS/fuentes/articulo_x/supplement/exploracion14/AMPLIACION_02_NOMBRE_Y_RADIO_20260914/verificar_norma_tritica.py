"""Comprobaciones focales exactas; sólo biblioteca estándar.

Los operadores actúan después del registro APP--TRIT--TPK ya archivado.
La comparación con la salida alfa NO selecciona ningún coeficiente o estado.
No regenera K ni alfa y no acredita por sí sola el corpus completo.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
from functools import reduce
from math import gcd
import argparse
import json

def require(ok, label):
    if not ok:
        raise ArithmeticError(label)

def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def tr(a):
    return list(map(list, zip(*a)))

def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]

def sc(k, a):
    return [[k*x for x in r] for r in a]

def mm(a, b):
    return [[sum(x*y for x, y in zip(r, c)) for c in zip(*b)] for r in a]

def mv(a, v):
    return [sum(x*y for x, y in zip(r, v)) for r in a]

def dot(v, w):
    return sum(x*y for x, y in zip(v, w))

def norm(v):
    return dot(v, v)

def det2(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]

def shift(n, j):
    return [[F(c == (r+j) % n) for c in range(n)] for r in range(n)]

def dec(x):
    return Decimal(x.numerator)/Decimal(x.denominator)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    I = eye(2)
    C = [[F(0),F(-1)],[F(1),F(-1)]]
    B = [[F(2),F(-1)],[F(-1),F(2)]]
    C2 = mm(C,C)
    require(add(add(C2,C),I) == sc(0,I), "C²+C+I=0")
    require(mm(mm(tr(C),B),C) == B, "métrica ternaria conservada")
    samples = [F(1,100),F(1,8),F(1,2),F(1),F(2),F(8),F(100)]
    param_results = []
    for a in samples:
        p = a*a+a+1
        qm = add(sc(a,I),sc(-1,C))
        qp = add(sc(a+1,I),C)
        require(mm(qm,qp) == sc(p,I), "producto conjugado")
        require(mm(mm(tr(qm),B),qm) == sc(p,B), "norma trítica")
        require(det2(qm) == p and det2(qp) == p, "determinantes")
        require(mm(tr(qm),B) == mm(B,qp), "adjunto métrico")
        rq2 = 2*a*p/(a+1)**4
        inva = 1/a
        require(rq2 == 2*inva*(inva*inva+inva+1)/(inva+1)**4, "dualidad a inverso")
        require(rq2 <= F(3,8), "máximo de radio cuadrado")
        param_results.append({"a":str(a), "p":str(p), "radio_carga_cuadrado":str(rq2)})
    qm8 = add(sc(8,I),sc(-1,C))
    require(reduce(gcd, (abs(int(x)) for r in qm8 for x in r)) == 1, "primer factor de Smith")
    require(det2(qm8) == 73, "índice 73")
    require(pow(8,3,73) == 1 and 8 != 1 and (8*64) % 73 == 1, "orden y conjugación en cociente")
    require(10*73 == 9**3+1 and 7*73 == 8**3-1, "factores enteros del ciclo completo")

    n=12
    I12=eye(n)
    S3,S4=shift(n,3),shift(n,4)
    U=S4
    U2=mm(U,U)
    P0=sc(F(1,3),add(add(I12,U),U2))
    require(mm(U2,U) == I12, "ciclo ternario completo")
    require(mm(P0,P0) == P0 and tr(P0) == P0, "proyector fijo")
    require(sum(P0[i][i] for i in range(n)) == 4, "cuatro modos fijos")
    for a in samples:
        p=a*a+a+1
        minus=add(sc(a,I12),sc(-1,U))
        plus=add(sc(a+1,I12),U)
        gminus=mm(tr(minus),minus)
        gplus=mm(tr(plus),plus)
        require(gminus == add(sc(p,I12),sc(-3*a,P0)), "norma de orientación menos")
        require(gplus == add(sc(p,I12),sc(3*(a+1),P0)), "norma de orientación más")
        require(mm(plus,minus) == add(sc(p,I12),sc(-3,P0)), "producto bilateral")
        require(add(sc(a+1,gminus),sc(a,gplus)) == sc((2*a+1)*p,I12), "balance bilateral")
        reversed_minus=add(sc(a,I12),sc(-1,U2))
        require(mm(tr(reversed_minus),reversed_minus) == gminus, "inversión de fase conserva norma")
    L=add(sc(8,I12),sc(-1,U))
    plus=add(sc(9,I12),U)
    require(add(sc(9,mm(tr(L),L)),sc(8,mm(tr(plus),plus))) == sc(1241,I12), "balance 1241")
    require(add(plus,sc(-1,tr(L))) == sc(3,P0), "adjunto difiere en modo fijo")

    T3=sc(F(1,9),add(sc(8,I12),S3))
    T4=sc(F(1,9),add(sc(8,I12),S4))
    Z3=sc(F(1,9),add(S3,sc(-1,I12)))
    Z4=sc(F(1,9),add(S4,sc(-1,I12)))
    T=mm(T4,T3)
    Z43=mm(Z4,T3)
    G=add(sc(8,mm(tr(Z3),Z3)),sc(8,mm(tr(Z43),Z43)))
    require(add(mm(tr(T),T),G) == I12, "isometría de terminal y memorias")
    require(G[0][0] == F(2336,6561), "diagonal 2336/6561")
    require(F(1,2)*G[0][0] == F(16*73,81**2), "radio 4 sqrt73 /81 al cuadrado")
    require(mm(P0,Z43) == sc(0,I12), "segunda memoria anula modo fijo")

    K=[F(x) for x in [234,543,140,729,659,824,621,58,914,794,146,601]]
    centered=[x-sum(K)/12 for x in K]
    states=[("K",K,F(1)),("P11K",centered,F(1)),
            ("D3K",mv(Z3,K),F(8)),("D4T3K",mv(Z43,K),F(8))]
    expected=[
        (F(4251257),F(10684363,3)),
        (F(11789915,12),F(1170761,4)),
        (F(15413392,81),F(16838032,243)),
        (F(1105759232,6561),F(0))]
    state_results=[]
    for (label,v,factor),(aexp,bexp) in zip(states,expected):
        a,b=factor*norm(v),factor*norm(mv(P0,v))
        require((a,b)==(aexp,bexp), "normas exactas "+label)
        s=(73*a-24*b)/a
        require(factor*norm(mv(L,v))/a == s, "lectura exacta "+label)
        state_results.append({"objeto":label,"norma2":str(a),"norma_fija2":str(b),
                              "w":str(b/a),"s":str(s)})
    for v in [K,centered]:
        channels=[(mv(T,v),F(1)),(mv(Z3,v),F(8)),(mv(Z43,v),F(8))]
        for R in [I12,P0,L]:
            require(norm(mv(R,v)) == sum(f*norm(mv(R,z)) for z,f in channels),
                    "balance completo con operador transportado")
    lo=F(7297352569283800997285105472380662,10**36)
    hi=F(7297352569283800997285105472380663,10**36)
    slo,shi=10**4*lo,10**4*hi
    require(72<slo<=shi<73, "intervalo de alfa archivada")
    for row in state_results:
        s=F(row["s"])
        require(s < slo or s > shi, "separación de intervalo "+row["objeto"])
    wlo,whi=(73-shi)/24,(73-slo)/24
    require(0<wlo<=whi<F(1,24), "peso inverso requerido")
    require(16*shi/81**2 < F(16*73,81**2), "radio conservador menor que óptimo")
    inverse_iterations=[]
    for row in state_results[:3]:
        w0=F(row["w"])
        odds=w0/(1-w0)
        previous=None
        for k in range(1000):
            w=odds/(1+odds)
            if w < wlo:
                require(previous is not None and previous > whi,
                        "cruce estricto sin coincidencia del intervalo alfa")
                inverse_iterations.append({"objeto":row["objeto"],
                    "n_before":k-1,"n_after":k,
                    "s_before":str(73-24*previous),"s_after":str(73-24*w),
                    "scope":"Todos los n enteros no negativos por monotonía estricta de (49/73)^n."})
                break
            previous=w
            odds*=F(49,73)
        else:
            raise ArithmeticError("no se encontró el cruce de la familia inversa")
    # Testigo límite: e0-e2 alcanza la distancia mínima de carga.
    h=[F(1),F(0),F(-1)]+[F(0)]*9
    require(dot(h,mv(G,h)) == F(64*73,81**2), "testigo de separación exacta")
    # Mezclar libremente el sector fijo permite ajustar una lectura: no es generador.
    wf=F(1,2)
    require(73-24*wf == 61, "control: lectura libre distinta de 73")
    with localcontext() as ctx:
        ctx.prec=70
        rq=Decimal(4)*Decimal(73).sqrt()/Decimal(81)
        ralpha=Decimal(4)*dec(shi).sqrt()/Decimal(81)
        a_inverse=(-Decimal(1)+(4*dec(shi)-3).sqrt())/2
        result={
            "scope":"Controles focales exactos de operadores posteriores; no regeneración de K o alfa.",
            "status":"PASS_IDENTIDADES_NORMA_TRITICA_Y_BALANCE_BILATERAL",
            "samples":param_results,
            "states":state_results,
            "alpha_archive_interval":[str(lo),str(hi)],
            "scaled_alpha_interval":[str(slo),str(shi)],
            "required_weight_interval":[str(wlo),str(whi)],
            "radius_exact_form":"4*sqrt(73)/81",
            "radius_decimal":str(rq),
            "alpha_radius_upper_decimal":str(ralpha),
            "inverse_diagnostic_a_upper_decimal":str(a_inverse),
            "inverse_diagnostic_note":"El parámetro inverso se calcula sólo después; no se usa como generador.",
            "bilateral_balance":"9||Q-v||²+8||Q+v||²=1241||v||²",
            "inverse_iteration_brackets":inverse_iterations,
            "integer_factorization":{"729_plus_one":730,"nontrivial_factor":73,"fixed_factor":10}
        }
    payload=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:
        Path(args.output).write_text(payload+"\n",encoding="utf-8")
    print(payload)

if __name__=="__main__":
    main()
