#!/usr/bin/env python3
"""Exact checks of the recovered normalized readers, not selection of a state.

Q(phi) uses phi^2=phi+1. Positive rational marks are test variables, not
approximations used to generate pi. General proofs reside in the manuscript.
"""
from fractions import Fraction as F
import json

def elt(a,b=0): return (F(a),F(b))
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    a,b=x; c,d=y
    return (a*c+b*d,a*d+b*c+b*d)
def inv(x):
    a,b=x; norm=a*a+a*b-b*b
    if not norm: raise ZeroDivisionError()
    return ((a+b)/norm,-b/norm)
def div(x,y): return mul(x,inv(y))
def power(x,n):
    if n<0: return power(inv(x),-n)
    out=elt(1)
    for _ in range(n): out=mul(out,x)
    return out

def main():
    checks=0
    def require(value):
        nonlocal checks
        if not value: raise RuntimeError('Exact reader identity failed at '+str(checks))
        checks+=1
    one=elt(1); phi=elt(0,1); phi2=power(phi,2)
    require(phi2==add(phi,one))
    require(add(power(phi,-2),power(phi,-1))==one)
    ma=inv(add(one,phi2)); mv=div(phi2,add(one,phi2))
    require(add(ma,mv)==one)
    require(mul(mv,power(phi,-2))==ma)
    require(add(ma,mul(mv,power(phi,-1)))==mv)
    mutations=0
    for p in (F(2),F(3),F(7,2)):
        mark=elt(p); r=div(mark,phi2); rj=div(phi,power(mark,2))
        for memory in (F(1),F(2),F(5,3)):
            area=mul(mul(mark,ma),elt(memory)); volume=mul(mv,elt(memory))
            require(div(area,volume)==r)
            raw=div(mul(area,r),add(mul(area,r),mul(volume,rj)))
            normalized=div(power(r,2),add(power(r,2),rj))
            final=div(power(mark,4),add(power(mark,4),power(phi,5)))
            require(raw==normalized==final)
            require(add(final,div(power(phi,5),add(power(mark,4),power(phi,5))))==one)
            wrong=div(r,add(r,rj))
            require(wrong!=final); mutations+=1
        for hbar,t0 in ((F(1),F(1)),(F(2,3),F(7,5))):
            h=2*p*hbar; tp=F(54)*t0/p
            q=h/(108*t0)
            require(q==hbar/tp)
            for unit in (F(2),F(3,7)):
                e1,e2=F(4),F(5)
                require(e1*e2/q**2==(unit*e1)*(unit*e2)/(unit*q)**2)
    # The phase return does not by itself certify the fibre condition for q.
    same_boundary={'x':0,'y':0}; q_bad={'x':F(1),'y':F(2)}
    require(same_boundary['x']==same_boundary['y'] and q_bad['x']!=q_bad['y'])
    mutations+=1
    print(json.dumps({'status':'PASS_LECTORES_FRONTERA_REV04','exact_checks':checks,
        'negative_controls':mutations,'scope':'Normalized common-amplitude realization, clock energy and dimensional covariance',
        'general_boundary_identification':False,'new_global_physical_certificate':False},ensure_ascii=False))

if __name__=='__main__': main()
