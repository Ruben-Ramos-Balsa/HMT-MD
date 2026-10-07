#!/usr/bin/env python3
"""Controles exactos finitos de la sección de acoplamiento; sin dependencias."""
from fractions import Fraction as F
import json

K = (234,543,140,729,659,824,621,58,914,794,146,601)

def require(ok, message):
    if not ok:
        raise ValueError(message)

def dot(x,y):
    return sum(a*b for a,b in zip(x,y))

def transpose(a):
    return list(map(list,zip(*a)))

def mul(a,b):
    return [[dot(x,y) for y in transpose(b)] for x in a]

def add(a,b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]

def scale(a,c):
    return [[c*x for x in row] for row in a]

def orbit(k):
    return [[k[(i+j)%12] for j in range(12)] for i in range(12)]

def det(a):
    a=[list(map(F,row)) for row in a]
    sign=1
    result=F(1)
    for i in range(len(a)):
        p=next((j for j in range(i,len(a)) if a[j][i]),None)
        if p is None:
            return F(0)
        if p!=i:
            a[i],a[p]=a[p],a[i]
            sign=-sign
        pivot=a[i][i]
        result*=pivot
        for j in range(i+1,len(a)):
            q=a[j][i]/pivot
            a[j]=[x-q*y for x,y in zip(a[j],a[i])]
    return sign*result

def verify_register(k):
    require(len(k)==12 and all(0<=x<1000 for x in k),"tipo de registro")
    n=0
    for x in k:
        n=1000*n+x
    kap=F(n,1000**12-1)
    recovered=[]
    q=n
    for _ in range(12):
        q,r=divmod(q,1000)
        recovered.append(r)
    require(tuple(reversed(recovered))==k and q==0,"inversa posicional")
    gram=mul(transpose(orbit(k)),orbit(k))
    row=gram[0]
    require(row==[4251257,2999323,3163385,3287920,3216553,3344743,
                  2950064,3344743,3216553,3287920,3163385,2999323],
            "Gram diferente")
    # cos(j*pi/6) as exact pairs r+s*sqrt(3).
    cos=[(F(1),F(0)),(F(0),F(1,2)),(F(1,2),F(0)),(F(0),F(0)),
         (F(-1,2),F(0)),(F(0),F(-1,2)),(F(-1),F(0)),
         (F(0),F(-1,2)),(F(-1,2),F(0)),(F(0),F(0)),
         (F(1,2),F(0)),(F(0),F(1,2))]
    spectrum=[tuple(sum(F(row[j])*cos[(m*j)%12][c] for j in range(12))
                    for c in range(2)) for m in range(12)]
    expected=[(39225169,0),(1248025,-345420),(589609,0),(1407529,0),
              (1053157,0),(1248025,345420),(697225,0),
              (1248025,345420),(1053157,0),(1407529,0),
              (589609,0),(1248025,-345420)]
    require(spectrum==expected,"espectro exacto")
    require(658416**2>3*345420**2,"cota inferior")
    require(abs(det(orbit(k)))==5483119259214020183850397930008283625,
            "determinante")
    require(sum(k)==6263 and [i+1 for i,x in enumerate(k) if x>=729]==[4,6,9,10],
            "lecturas de suma e incidencia")
    return {"numerator":n,"denominator":1000**12-1,
            "kappa":str(kap),"gram_spectrum_verified":12}

def run():
    result=verify_register(K)
    negative=0
    bad=list(K);bad[0]+=1
    try:
        verify_register(tuple(bad))
    except ValueError:
        negative+=1
    else:
        raise ValueError("no rechaza alteración de K")
    # Two different isometries R^2 -> R^4; crossed terms are nonzero.
    b=[[1,0],[0,1],[0,0],[0,0]]
    c=[[0,1],[0,0],[1,0],[0,0]]
    identity=[[1,0],[0,1]]
    require(mul(transpose(b),b)==mul(transpose(c),c)==identity,"isometrías")
    tests=0
    for a in (F(1,2),F(1),F(2),F(8),F(11)):
        p=a*a+a+1
        n=(2*a+1)*p
        qm=add(scale(b,a),scale(c,-1))
        qp=add(scale(b,a+1),c)
        lhs=add(scale(mul(transpose(qm),qm),a+1),
                scale(mul(transpose(qp),qp),a))
        require(lhs==scale(identity,n),"balance matricial")
        require(add(qm,qp)==scale(b,2*a+1),"recuperación B")
        require(add(scale(qp,a),scale(qm,-a-1))==scale(c,2*a+1),"recuperación C")
        f=[[2,1,0,0],[1,3,1,0],[0,1,5,1],[0,0,1,7]]
        left=add(scale(mul(mul(transpose(qm),f),qm),a+1),
                 scale(mul(mul(transpose(qp),f),qp),a))
        right=scale(add(scale(mul(mul(transpose(b),f),b),a*(a+1)),
                        mul(mul(transpose(c),f),c)),2*a+1)
        require(left==right,"transformación de lectores")
        tests+=4
    require(8*9+1==73 and (9**3+8**3)==17*73,"especialización nonádica")
    return {"status":"PASS_ACOPLAMIENTO_EXACTO","scope":"Registro, Gram y espectro finitos; 20 identidades matriciales de ejemplo. Las pruebas generales están en LaTeX; no formaliza operadores de Hilbert infinitos.",
            "register":result,"matrix_identities":tests,"negative_tests":negative}

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,indent=2))
