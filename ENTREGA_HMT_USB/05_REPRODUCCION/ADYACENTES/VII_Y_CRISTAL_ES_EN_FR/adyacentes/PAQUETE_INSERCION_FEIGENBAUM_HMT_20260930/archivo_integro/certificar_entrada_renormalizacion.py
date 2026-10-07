#!/usr/bin/env python3
"""Outward-rounded l1 enclosures for the HMT critical reader and its tangent.

The HMT family is unchanged. Lanford's polynomial is a comparison centre,
never a generator input. This program certifies a finite renormalization
entry and a cone condition, not all subsequent parameter scaling by itself.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from fractions import Fraction as Q
import sys

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('hmt_intervals', BASE/'certificar_raices.py')
iv = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = iv
spec.loader.exec_module(iv)
I = iv.Interval
S = iv.SCALE
N = 32


def ab(x):
    return max(abs(x.lo), abs(x.hi))


def up(a, b):
    return iv.ceildiv(a*b, S)


class Series:
    """Polynomial interval coefficients plus an arbitrary analytic l1 error.

    err bounds the l1 norm, in fixed-point units, of an unknown power series
    on the unit disc. Products/compositions include its low coefficients;
    it is never silently treated as a tail with zero low coefficients.
    """
    def __init__(self, c=(), err=0):
        c = list(c)
        self.err = err + sum(ab(v) for v in c[N+1:])
        self.c = c[:N+1] + [I.rational(0)]*max(0, N+1-len(c))

    @staticmethod
    def const(x):
        return Series([x if isinstance(x, I) else I.rational(x)])

    def norm(self):
        return sum(ab(v) for v in self.c)+self.err

    def value0(self):
        return self.c[0].expand(self.err)

    def evaluate(self,x):
        if ab(x)>S:
            raise ValueError('Real evaluation outside unit disc')
        out=I.rational(0)
        for a in reversed(self.c):
            out=out*x+a
        return out.expand(self.err)

    def __neg__(self):
        return Series([-v for v in self.c], self.err)

    def __add__(self, o):
        if not isinstance(o, Series):
            o = Series.const(o)
        return Series([a+b for a,b in zip(self.c,o.c)], self.err+o.err)

    __radd__ = __add__

    def __sub__(self, o):
        return self + (-o)

    def __rsub__(self, o):
        return -self+o

    def __mul__(self, o):
        if not isinstance(o, Series):
            o = Series.const(o)
        c = [I.rational(0)]*(2*N+1)
        for j,a in enumerate(self.c):
            if a.lo == a.hi == 0:
                continue
            for k,b in enumerate(o.c):
                if b.lo == b.hi == 0:
                    continue
                c[j+k] = c[j+k]+a*b
        pn = sum(ab(v) for v in self.c)
        qn = sum(ab(v) for v in o.c)
        err = up(pn,o.err)+up(qn,self.err)+up(self.err,o.err)
        return Series(c,err)

    __rmul__ = __mul__

    def shift(self):
        return Series(self.c[1:],self.err)

    def compose(self, q):
        r = q.norm()
        if r >= S:
            raise ValueError('Composition argument norm >= 1: '+iv.fixed_decimal(r))
        result = Series.const(0)
        for a in reversed(self.c):
            result = result*q+a
        result.err += self.err
        return result

    def derivative_at(self,q):
        r = q.norm()
        if r >= S:
            raise ValueError('Derivative composition argument norm >= 1')
        result = Series.const(0)
        for j in range(N,0,-1):
            result = result*q+self.c[j]*j
        # sum |e_j| <= err implies sum j |e_j| r^(j-1)
        # <= err/(1-r)^2, including all unknown low coefficients.
        result.err += iv.ceildiv(self.err*S*S,(S-r)**2)
        return result

    def record(self):
        return {'l1_error':iv.fixed_decimal(self.err),
                'coefficients':[v.record() for v in self.c]}


class Dual:
    def __init__(self,v,d=None):
        self.v = v if isinstance(v,Series) else Series.const(v)
        self.d = d if d is not None else Series.const(0)

    def __neg__(self):
        return Dual(-self.v,-self.d)

    def __add__(self,o):
        if not isinstance(o,Dual): o=Dual(o)
        return Dual(self.v+o.v,self.d+o.d)

    __radd__=__add__

    def __sub__(self,o):
        if not isinstance(o,Dual): o=Dual(o)
        return self+-o

    def __rsub__(self,o):
        return -self+o

    def __mul__(self,o):
        if not isinstance(o,Dual): o=Dual(o)
        return Dual(self.v*o.v,self.d*o.v+self.v*o.d)

    __rmul__=__mul__

    def compose(self,q):
        return Dual(self.v.compose(q.v),
                    self.d.compose(q.v)+self.v.derivative_at(q.v)*q.d)

    def shift(self):
        return Dual(self.v.shift(),self.d.shift())


CENTRE = [
 '1.399535280247654509657069657886239',
 '-0.37020336425570944099807863650264',
 '-0.1051644130848705939530670467124',
 '0.046892245318664173569020642588375',
 '-0.006571964344294895159402341197265625',
 '-0.00092424880356949042888086870078125',
 '0.0006019977571546570340827287265625',
 '-0.0000726635816090358011441621484375',
 '-0.00003921160572782132082950382843017578125',
 '0.000001057835068053822221515655517578125',
]


def initial(lo,hi):
    lam=I(I.rational(lo).lo,I.rational(hi).hi)
    # u(sqrt(s))/s = sum_j (-1)^(j+1) mu_(2j) s^(j-1)/(2j)!.
    # After s=1+(5/2)z, ||s||_1=7/2. The omitted factorial
    # series is bounded by the first term and a geometric ratio.
    coeff=[Q(0)]*(N+1)
    for j in range(1,N+2):
        a=Q((-1)**(j+1)*4**j*sum(k**(2*j) for k in iv.K),
            12*899**j*math.factorial(2*j))
        for k in range(j):
            coeff[k] += a*math.comb(j-1,k)*Q(5,2)**k
    j=N+2
    first=Q(4**j*sum(k**(2*j) for k in iv.K),
            12*899**j*math.factorial(2*j))*Q(7,2)**(j-1)
    ratio=Q(4900,899)*Q(7,2)/((2*j+1)*(2*j+2))
    assert ratio<1
    err=I.rational(first/(1-ratio)).hi
    base=Series([I.rational(v) for v in coeff],err)
    return Dual(base*lam,base)


def renormalize(v):
    a=Dual(v.v.value0()-1,Series.const(v.d.value0()))
    ai=a.v.value0()
    assert 0<ai.lo and ai.hi<S, 'Renormalization scale outside (0,1)'
    def f_at(x):
        return 1-x.square()*v.v.evaluate((x.square()-1)*I.rational(Q(2,5)))
    bi=f_at(ai)
    ci=f_at(bi)
    assert bi.lo>ai.hi and ci.hi<ai.lo, 'Real return domain not certified'
    s=Dual(Series([I.rational(1),I.rational(Q(5,2))]))
    arg=(a*a*s-1)*Q(2,5)
    inner=v.compose(arg)
    h=1-a*a*s*inner
    t=(h*h-1)*Q(2,5)
    w=v+v.shift()*Q(2,5)
    return a*inner*(h+1)*w.compose(t), {
        'scale_a':ai.record(), 'b_equals_fa':bi.record(), 'f_of_b':ci.record(),
        'real_return_domain_certified':True,
        'inner_argument_l1':iv.fixed_decimal(arg.v.norm()),
        'outer_argument_l1':iv.fixed_decimal(t.v.norm())}


def status(v):
    centre=[I.rational(x) for x in CENTRE]
    diff=[x-(centre[j] if j<len(centre) else 0) for j,x in enumerate(v.v.c)]
    # Lanford u = 10*v0. Thus the norm is 10|dv0|+sum|dvi|.
    distance=10*ab(diff[0])+sum(ab(x) for x in diff[1:])+10*v.v.err
    delta_u=diff[0].expand(v.v.err)*10
    nu_distance=sum(ab(x) for x in diff[1:])+v.v.err
    du=v.d.value0()*10
    lower=0 if du.contains_zero() else min(abs(du.lo),abs(du.hi))
    tail=sum(ab(x) for x in v.d.c[1:])+v.d.err
    return {'distance_to_Lanford_centre_upper':iv.fixed_decimal(distance),
            'delta_u_centre':delta_u.record(),
            'nu_distance_centre_upper':iv.fixed_decimal(nu_distance),
            'in_ball_0_01':distance<S//100,
            'du_interval':du.record(),
            'nu_tangent_l1_upper':iv.fixed_decimal(tail),
            'cone_quarter':4*tail<lower,
            'cone_ratio_upper':iv.fixed_decimal(iv.ceildiv(tail*S,lower)) if lower else None,
            'value_error_l1':iv.fixed_decimal(v.v.err),
            'tangent_error_l1':iv.fixed_decimal(v.d.err)}


def main():
    global N
    p=argparse.ArgumentParser()
    p.add_argument('--lower',default='1.874038')
    p.add_argument('--upper',default='1.874039')
    p.add_argument('--levels',type=int,default=3)
    p.add_argument('--order',type=int,default=32)
    p.add_argument('--pieces',type=int,default=1)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    N=args.order
    if N<9 or args.pieces<1 or args.levels<1:
        raise ValueError('Require order>=9, pieces>=1 and levels>=1')
    lo,hi=Q(args.lower),Q(args.upper)
    def evaluate(a,b,quiet=False):
        v=initial(a,b)
        levels=[{'level':0,**status(v)}]
        for n in range(1,args.levels+1):
            v,domains=renormalize(v)
            entry={'level':n,**status(v),**domains}
            levels.append(entry)
            if not quiet:
                print(json.dumps(entry),flush=True)
        return v,levels
    pieces=[]
    for j in range(args.pieces):
        a=lo+(hi-lo)*Q(j,args.pieces)
        b=lo+(hi-lo)*Q(j+1,args.pieces)
        v,levels=evaluate(a,b,args.pieces>1)
        pieces.append({'parameter_interval':[str(a),str(b)],'levels':levels})
        if args.pieces>1:
            print(json.dumps({'piece':j+1,'final':levels[-1]}),flush=True)
    _,left=evaluate(lo,lo,True)
    _,right=evaluate(hi,hi,True)
    def rational_field(record,key):
        return Q(record[key])
    radius=Q(1,250)
    lip=Q(4,25)
    epsilon=Q(1,25000)
    left_margin=Q(left[-1]['delta_u_centre']['upper'])+epsilon+lip*(Q(left[-1]['nu_distance_centre_upper'])+epsilon)
    right_margin=Q(right[-1]['delta_u_centre']['lower'])-epsilon-lip*(Q(right[-1]['nu_distance_centre_upper'])+epsilon)
    crossing={
        'stable_graph_lipschitz':str(lip), 'stable_coordinate_radius':str(radius),
        'fixed_point_centre_error':str(epsilon),
        'left_signed_margin_upper':iv.fixed_decimal(I.rational(left_margin).hi),
        'right_signed_margin_lower':iv.fixed_decimal(I.rational(right_margin).lo),
        'opposite_sides':left_margin<0<right_margin,
        'whole_curve_in_graph_domain':all(Q(p['levels'][-1]['nu_distance_centre_upper'])+epsilon<radius for p in pieces),
        'whole_curve_positive_transverse':all(Q(p['levels'][-1]['du_interval']['lower'])>lip*Q(p['levels'][-1]['nu_tangent_l1_upper']) for p in pieces)}
    result={'arithmetic':'Rational outward rounding; polynomial l1 balls and analytic tail bounds',
            'parameter_interval':[args.lower,args.upper], 'order':N,
            'pieces':pieces, 'left_endpoint':left[-1], 'right_endpoint':right[-1],
            'stable_graph_crossing':crossing,
            'scope':'Finite entry and tangent cone only; no automatic global continuation or parameter tail certificate',
            'comparison_centre_source':'Hertling-Spandl 2014, Table2; Lanford estimates'}
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    good=all(p['levels'][-1]['in_ball_0_01'] and p['levels'][-1]['cone_quarter'] for p in pieces)
    good=good and crossing['opposite_sides'] and crossing['whole_curve_in_graph_domain'] and crossing['whole_curve_positive_transverse']
    print(json.dumps(crossing),flush=True)
    print('PASS_FINITE_RENORMALIZATION_ENTRY_AND_CONE' if good else 'ENTRY_OR_CONE_NOT_CERTIFIED')
    return 0 if good else 1


if __name__=='__main__':
    raise SystemExit(main())
