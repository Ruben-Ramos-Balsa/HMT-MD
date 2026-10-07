#!/usr/bin/env python3
"""Bounded exact-interval exclusion of the infinite doubling itinerary.

Uses the rational backend and moment polynomial of the existing certificates.
A complete cover excludes Lambda_tau on the declared interval, not an
identification with the local stable sheet or with a global root sequence.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import factorial
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('hmt_bridge_finite', HERE / 'certificar_continuacion_finita.py')
finite = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = finite
spec.loader.exec_module(finite)
base, I, S = finite.base, finite.I, finite.SCALE


def mag(x):
    return max(abs(x.lo), abs(x.hi))


def opposite_tau(x, j):
    valuation = (j & -j).bit_length() - 1
    return x.hi < 0 if valuation % 2 == 0 else x.lo > 0


def center_excludes(radius, bound):
    # |g''| <= bound/S, |g(0)| <= radius/S; g'(0)=0.
    # g(g(0)) and g(0) have equal strict signs, or both are zero.
    return radius >= 0 and bound >= 0 and radius * bound < 2 * S * S


class Family(finite.PolynomialFamily):
    def __init__(self, terms=32):
        super().__init__(terms)
        self.hessian = [c * ((2*j)*(2*j-1))
                        for j,c in enumerate(self.coefficients, 1)]
        j = terms + 1
        r = Q(3,2)
        first = self.moments[j] * r**(2*j-2) / factorial(2*j-2)
        ratio = self.max_frequency_squared*r*r / ((2*j-1)*(2*j))
        tail = first/(1-ratio)
        self.hessian_tail = base.ceildiv(tail.numerator*S, tail.denominator)

    def second(self, x):
        mid, rad = x.radius_bound()
        xx = I.scaled_point(mid).square()
        ans = self.hessian[-1]
        for c in reversed(self.hessian[:-1]):
            ans = ans*xx+c
        # mean omega^2 = 2, max omega < 3, hence |u'''| < 6.
        return ans.expand(self.hessian_tail+6*rad)

    def center_bound(self, parameter, period, radius, deadline):
        x = I(-radius, radius)
        dx, ddx = I.rational(1), I.rational(0)
        for step in range(period):
            if step % 32 == 0 and time.monotonic() >= deadline:
                return None
            potential, slope = self.potential(x)
            second = self.second(x)
            ddx = -parameter*(second*dx.square()+slope*ddx)
            dx = -parameter*slope*dx
            x = 1-parameter*potential
            x = I(max(-S,x.lo),min(S,x.hi))
            if mag(ddx)*radius >= 2*S*S and x.hi-x.lo > S//10:
                return None
        return mag(ddx)

    def exclude(self, parameter, max_iter, deadline):
        x = I.rational(0)
        derivative = I.rational(0)
        midpoint,_ = parameter.radius_bound()
        center_parameter = I.scaled_point(midpoint)
        delta_parameter = parameter-center_parameter
        center_x = I.rational(0)
        for j in range(1,max_iter+1):
            if j % 32 == 0 and time.monotonic() >= deadline:
                return None, j, 'time'
            potential,slope = self.potential(x)
            derivative = -potential-parameter*slope*derivative
            x = 1-parameter*potential
            center_potential,_ = self.potential(center_x)
            center_x = 1-center_parameter*center_potential
            center_x = I(max(-S,center_x.lo),min(S,center_x.hi))
            # Mean-value theorem in the single parameter. The derivative
            # enclosure uses the entire old x-box, not the center orbit.
            centered = center_x+derivative*delta_parameter
            x = I(max(-S,x.lo,centered.lo),min(S,x.hi,centered.hi))
            if opposite_tau(x,j):
                return {'method':'opposite_itinerary_sign','iteration':j,
                        'return_interval':x.record()},j,None
            if j >= 256 and j & (j-1) == 0 and mag(x)<S//10**6:
                bound = self.center_bound(parameter,j,mag(x),deadline)
                if bound is not None and center_excludes(mag(x),bound):
                    return {'method':'equal_sign_double_return',
                            'period':j,'return_interval':x.record(),
                            'second_derivative_upper':base.fixed_decimal(bound),
                            'strict_radius_times_M_below_2':True},j,None
            if x.hi-x.lo > S//20:
                return None,j,'wide_orbit'
        return None,max_iter,'max_iteration'


def tiled(full, boxes):
    if not boxes:
        return False
    boxes = sorted(boxes,key=lambda b:b.lo)
    return (boxes[0].lo==full.lo and boxes[-1].hi==full.hi and
            all(a.hi==b.lo for a,b in zip(boxes,boxes[1:])))


def tests(family):
    assert opposite_tau(I.rational(-1),256)
    assert not opposite_tau(I.rational(1),256)
    assert opposite_tau(I.rational(1),512)
    assert not opposite_tau(I(-1,1),512)
    assert center_excludes(S//100,100*S)  # product 1 < 2
    assert not center_excludes(S//100,200*S)
    assert not tiled(I(0,10),[I(0,4),I(5,10)])
    assert not tiled(I(0,10),[I(0,6),I(5,10)])
    assert tiled(I(0,10),[I(0,4),I(4,10)])
    assert family.second(I.rational(0)).lo <= 2*S <= family.second(I.rational(0)).hi
    return {'status':'PASS','negative_checks':5,'endpoint_tiling':True,
            'hessian_origin_contains_exact_2':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=float,default=240)
    parser.add_argument('--max-boxes',type=int,default=20000)
    parser.add_argument('--max-iteration',type=int,default=2048)
    parser.add_argument('--upper',default='1.874038')
    parser.add_argument('--output',type=Path,default=HERE/'CERTIFICADO_PUENTE_ITINERARIO.json')
    parser.add_argument('--resume',action='store_true')
    args=parser.parse_args()
    family=Family()
    test_result=tests(family)
    root_path=HERE/'CERTIFICADO_RAICES_INTERVALOS.json'
    root_data=json.loads(root_path.read_text())
    root8=next(r for r in root_data['root_certificates'] if r['level']==8)
    left=finite.read_box(root8['root_interval']).lo
    full=I(left,I.rational(args.upper).hi)
    u1,_=family.potential(I.rational(1))
    assert full.lo>0 and (full*u1).hi<2*S
    previous=None
    if args.resume:
        previous=json.loads(args.output.read_text())
        assert finite.read_box(previous['interval'])==full
        assert previous['target_itinerary']=='tau_j=(-1)^v2(j)'
        assert previous['exact_tiling_including_pending']
        assert previous['sha256']['certificar_raices.py']==hashlib.sha256((HERE/'certificar_raices.py').read_bytes()).hexdigest()
        assert previous['sha256']['certificar_continuacion_finita.py']==hashlib.sha256((HERE/'certificar_continuacion_finita.py').read_bytes()).hexdigest()
        stack=list(reversed([finite.read_box(b) for b in previous['pending_intervals']]))
        leaves=list(previous['certified_leaves'])
        counts=dict(previous['counts'])
        deepest=previous['deepest_iteration']
        assert tiled(full,[finite.read_box(r['interval']) for r in leaves]+stack)
    else:
        stack=[full];leaves=[];counts={};deepest=0
    inherited_leaves=len(leaves)
    start=time.monotonic();deadline=start+args.seconds;processed=0
    while stack and processed<args.max_boxes and time.monotonic()<deadline:
        box=stack.pop()
        report,reached,reason=family.exclude(box,args.max_iteration,deadline)
        processed+=1;deepest=max(deepest,reached)
        if report is not None:
            report['interval']=box.record();leaves.append(report)
            counts[report['method']]=counts.get(report['method'],0)+1
        elif reason=='time':
            stack.append(box);break
        else:
            mid=(box.lo+box.hi)//2
            if mid in (box.lo,box.hi):
                stack.append(box);break
            stack.extend((I(mid,box.hi),I(box.lo,mid)))
        if processed%100==0:
            print(json.dumps({'processed':processed,'leaves':len(leaves),
                              'pending':len(stack),'deepest':deepest,
                              'seconds':round(time.monotonic()-start,2)}),flush=True)
    certified=[finite.read_box(r['interval']) for r in leaves]
    assert tiled(full,certified+stack)
    completed=not stack and tiled(full,certified)
    sources=[Path(__file__),HERE/'certificar_raices.py',
             HERE/'certificar_continuacion_finita.py',root_path]
    result={'status':'PASS_EXCLUSION_LAMBDA_TAU_ON_FULL_BRIDGE' if completed else 'PARTIAL_EXCLUSION_BUDGET',
            'family':'1-lambda*mean(1-cos(2*(3m-1)*x/sqrt(899))), m=1..12',
            'target_itinerary':'tau_j=(-1)^v2(j)', 'interval':full.record(),
            'integer_outward_rounding_scale_digits':base.DIGITS,
            'self_map_proof':{'lambda_positive':True,'lambda_times_u1_below_2':True},
            'center_proof':'g=f^p; g_prime(0)=0; |g_second|<=M between 0 and g(0). If M|g(0)|<2, g(g(0)) has the sign of g(0), or both vanish. tau_2p=-tau_p excludes the target.',
            'tests':test_result,'processed':processed,'counts':counts,
            'inherited_leaves':inherited_leaves,
            'new_leaves':len(leaves)-inherited_leaves,
            'parameter_centering':'Intersect natural range with c_j(mid)+D_lambda c_j(parameter_box)*(parameter-mid); D is propagated on the full parameter and state enclosure.',
            'deepest_iteration':deepest,'certified_leaves':leaves,
            'pending_intervals':[b.record() for b in sorted(stack,key=lambda b:b.lo)],
            'exact_tiling_including_pending':True,'full_exclusion':completed,
            'seconds':time.monotonic()-start,
            'not_claimed':['identification with the local stable sheet',
                           'identification with the infinite first-root selector',
                           'exclusion on any pending interval'],
            'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    if previous is not None:
        result['previous_run']=previous
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','processed','counts','deepest_iteration','seconds']}),flush=True)


if __name__=='__main__':
    main()
