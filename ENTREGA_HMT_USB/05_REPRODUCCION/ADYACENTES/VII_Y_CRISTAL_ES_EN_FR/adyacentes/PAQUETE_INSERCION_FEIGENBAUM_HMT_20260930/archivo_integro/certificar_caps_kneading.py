#!/usr/bin/env python3
"""Finite kneading exclusion for coefficient caps around Lanford's fixed point.

The HMT family is not changed. This is a comparison-space certificate only.
All computed bounds use rational outward rounding. A first-order Taylor model
retains the shared coefficient perturbations through the whole critical orbit.
The infinite coefficient tail and the nonlinear remainder are explicit.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import runpy

D = runpy.run_path(str(Path(__file__).with_name('certificar_entrada_renormalizacion.py')),
                  run_name='comparison_reader_only')
I, SCALE, up, cd = D['I'], D['S'], D['up'], D['iv'].ceildiv
BASE = [I.rational(x) for x in D['CENTRE']]
ZERO, ONE = I.rational(0), I.rational(1)


def ab(x):
    return max(abs(x.lo), abs(x.hi))


def polynomial(coeff, z):
    out = ZERO
    for a in reversed(coeff):
        out = out*z+a
    return out


def function_data(coeff, x):
    z = (x.square()-1)*I.rational(Q(2, 5))
    v = polynomial(coeff, z)
    vp = polynomial([coeff[j]*j for j in range(1, len(coeff))], z)
    vpp = polynomial([coeff[j]*j*(j-1) for j in range(2, len(coeff))], z)
    return (1-x.square()*v,
            -x*2*v-x*x*x*I.rational(Q(4, 5))*vp,
            -v*2-x.square()*4*vp-x.square().square()*I.rational(Q(16, 25))*vpp)


def certify(sign, lower, upper, extra=Q(0), order=40, steps=192,
            cone=Q(1, 4), intersect_self_maps=False, stable_slope=None):
    """g + (du,dnu) + e; ||dnu||_1<=cone*upper, ||e||_A<=extra.

    The certified fixed-point error ||g-g0||_A<=4e-5 is added separately.
    Thus even the rectangle containing the desired cone cap is controlled.
    """
    assert sign in (-1, 1) and 0 < lower <= upper and extra >= 0 and cone >= 0
    epsilon = I.rational(Q(1, 25000)+extra).hi
    fixed_error = I.rational(Q(1, 25000)).hi
    extra_error = I.rational(extra).hi
    if not intersect_self_maps:
        assert upper+cone*upper+Q(epsilon, SCALE) < Q(1, 100)
    # Within .01, §7 proves real self-mapping. Outside that ball this function
    # certifies only the intersection with the explicitly assumed class of
    # maps taking [-1,1] into itself. Renormalizations of a tau-realization
    # belong to that class independently of their distance from g0.
    midpoint = sign*(lower+upper)/2
    halfwidth = I.rational((upper-lower)/2).hi
    tail_radius = I.rational(cone*upper).hi
    coeff = BASE.copy()
    coeff[0] = coeff[0]+I.rational(midpoint/10)
    x = ZERO
    sensitivities = [ZERO]*(order+1)  # u=10v0, then v1,...,v_order
    sensitivity_tail = remainder = 0
    first_uncertain = None
    observations = []
    critical_boxes = [ZERO]

    def error_support(u_dual, nu_dual):
        """Support of the fixed-point error plus stable graph residual.

        If the optional stable slope L is supplied, the latter obeys
        |e_u|+||e_nu||<=extra and |e_u|<=L||e_nu||. Its exact positive
        dual support is extra*max(b,(L*a+b)/(1+L)).
        """
        if stable_slope is None:
            return up(epsilon, max(u_dual, nu_dual))
        L = Q(stable_slope)
        dual = max(nu_dual, cd(L.numerator*u_dual+L.denominator*nu_dual,
                              L.numerator+L.denominator))
        return (up(fixed_error, max(u_dual, nu_dual))
                +up(extra_error, dual))

    def derivative_bound(local):
        """Uniform first derivative on a real interval for the whole cap."""
        _, fp, _ = function_data(coeff, local)
        z = (local.square()-1)*I.rational(Q(2, 5))
        p = ONE
        md = 0
        for k in range(1, order+1):
            pn = p*z
            md = max(md, ab(-local*2*pn
                            -local*local*local*I.rational(Q(4*k, 5))*p))
            p = pn
        r, xx = Q(ab(z), SCALE), Q(ab(local), SCALE)
        tail = (2*xx*r**(order+1)
                +Q(4, 5)*xx**3*(order+1)*r**order/(1-r)**2)
        md = max(md, I.rational(tail).hi)
        ud = ab(local*I.rational(Q(1, 5)))
        return (ab(fp)+up(tail_radius, md)
                +error_support(ud, md)+up(halfwidth, ud))

    def contraction_exclusion():
        """If f^n contracts [-r,r] and f^n(0) lies there, the two
        successive dyadic critical values have the same sign (or vanish).
        Their required tau signs are opposite, giving a finite exclusion.
        """
        rr = ab(critical_boxes[-1])
        if rr >= SCALE:
            return None
        product = SCALE
        displacement = rr
        for box in critical_boxes[:-1]:
            local = box.expand(displacement)
            local = I(max(-SCALE, local.lo), min(SCALE, local.hi))
            derivative = derivative_bound(local)
            product = up(product, derivative)
            displacement = up(displacement, derivative)
        if product < SCALE:
            return {'return_period': len(critical_boxes)-1,
                    'critical_radius': D['iv'].fixed_decimal(rr),
                    'return_lipschitz_bound': D['iv'].fixed_decimal(product)}
        return None

    def uncertainty():
        nu_dual = max([ab(w) for w in sensitivities[1:]]+[sensitivity_tail])
        return (up(tail_radius, nu_dual)
                +error_support(ab(sensitivities[0]), nu_dual)
                +up(halfwidth, ab(sensitivities[0]))+remainder)

    for j in range(1, steps+1):
        radius = uncertainty()
        # The centre orbit must also lie in the convex real interval used
        # for the Taylor remainder. This is verified, not extrapolated.
        assert -SCALE <= x.lo <= x.hi <= SCALE
        local = x.expand(radius)
        local = I(max(-SCALE, local.lo), min(SCALE, local.hi))
        xnext, fp, _ = function_data(coeff, x)
        _, _, fpp = function_data(coeff, local)
        z = (x.square()-1)*I.rational(Q(2, 5))
        local_z = (local.square()-1)*I.rational(Q(2, 5))
        r, xx = Q(ab(local_z), SCALE), Q(ab(local), SCALE)
        assert r < 1
        zpower = ONE
        derivative_max = 0
        for k in range(1, order+1):
            nextpower = zpower*local_z
            derivative = (-local*2*nextpower
                          -local*local*local*I.rational(Q(4*k, 5))*zpower)
            derivative_max = max(derivative_max, ab(derivative))
            zpower = nextpower
        # Sum majorant bounds every derivative with k>order.
        tail_derivative = (2*xx*r**(order+1)
                           +Q(4, 5)*xx**3*(order+1)*r**order/(1-r)**2)
        derivative_max = max(derivative_max, I.rational(tail_derivative).hi)
        u_derivative = ab(local*I.rational(Q(1, 5)))
        perturbation_derivative = (
            up(tail_radius, derivative_max)
            +error_support(u_derivative, derivative_max)
            +up(halfwidth, u_derivative))
        remainder = (up(ab(fp), remainder)
                     +cd(up(ab(fpp), up(radius, radius)), 2)
                     +up(perturbation_derivative, radius))
        nextsens = [fp*sensitivities[0]-x.square()/10]
        zpower = ONE
        for k in range(1, order+1):
            zpower = zpower*z
            nextsens.append(fp*sensitivities[k]-x.square()*zpower)
        sensitivity_tail = (
            up(ab(fp), sensitivity_tail)
            +I.rational(Q(ab(x), SCALE)**2
                        *Q(ab(z), SCALE)**(order+1)).hi)
        sensitivities, x = nextsens, xnext
        radius = uncertainty()
        enclosure = x.expand(radius)
        critical_boxes.append(enclosure)
        tau = 1 if ((j & -j).bit_length()-1) % 2 == 0 else -1
        if enclosure.contains_zero() and first_uncertain is None:
            first_uncertain = j
        contradiction = ((tau > 0 and enclosure.hi < 0)
                         or (tau < 0 and enclosure.lo > 0))
        if j in (16, 32, 64, 96, 128, 192) or contradiction:
            observations.append({'iterate': j, 'tau': tau,
                                 'enclosure': enclosure.record(),
                                 'remainder': D['iv'].fixed_decimal(remainder)})
        if contradiction:
            return {'status': 'PASS_FINITE_KNEADING_CAP_EXCLUSION',
                    'sign': sign, 'du_band': [str(lower), str(upper)],
                    'extra_norm_radius': str(extra), 'order': order,
                    'cone_slope': str(cone),
                    'restricted_to_self_maps': intersect_self_maps,
                    'stable_residual_slope': str(stable_slope),
                    'first_uncertain': first_uncertain,
                    'contradiction_at': j, 'observations': observations}
        if j >= 8 and j & (j-1) == 0 and enclosure.contains_zero():
            contracting = contraction_exclusion()
            if contracting is not None:
                return {'status': 'PASS_FINITE_KNEADING_CAP_EXCLUSION',
                        'sign': sign, 'du_band': [str(lower), str(upper)],
                        'extra_norm_radius': str(extra), 'order': order,
                        'cone_slope': str(cone),
                        'restricted_to_self_maps': intersect_self_maps,
                        'stable_residual_slope': str(stable_slope),
                        'first_uncertain': first_uncertain,
                        'contraction_exclusion': contracting,
                        'observations': observations}
        if radius > 4*SCALE:
            break
    return {'status': 'CAP_NOT_CERTIFIED', 'sign': sign,
            'du_band': [str(lower), str(upper)], 'extra_norm_radius': str(extra),
            'first_uncertain': first_uncertain, 'last_iterate': j,
            'observations': observations}


def certify_first_exit_cover():
    """Finite cover of the negative first-exit cap, intersected with M."""
    lower, upper = Q('.006'), Q('.0485322')
    queue = [(lower+(upper-lower)*j/64,
              lower+(upper-lower)*(j+1)/64, 0) for j in range(64)]
    accepted, failed = [], []
    while queue:
        a, b, depth = queue.pop(0)
        result = certify(-1, a, b, Q('.001666'), 40, 128,
                         cone=Q('.21'), intersect_self_maps=True,
                         stable_slope=Q('.16'))
        if result['status'] == 'PASS_FINITE_KNEADING_CAP_EXCLUSION':
            accepted.append(result)
        elif depth < 4:
            midpoint = (a+b)/2
            queue[:0] = [(a, midpoint, depth+1), (midpoint, b, depth+1)]
        else:
            failed.append(result)
    accepted.sort(key=lambda r: Q(r['du_band'][0]))
    cursor = lower
    for result in accepted:
        a, b = map(Q, result['du_band'])
        if a != cursor:
            break
        cursor = b
    complete = not failed and cursor == upper
    return {'status': ('PASS_NEGATIVE_FIRST_EXIT_CAP_EXCLUSION' if complete
                       else 'FAIL_NEGATIVE_FIRST_EXIT_CAP_EXCLUSION'),
            'cap': {'sign': -1, 'du_band': [str(lower), str(upper)],
                    'cone_slope': '.21', 'stable_norm_radius': '.001666',
                    'stable_graph_slope': '.16',
                    'fixed_point_error': '.00004',
                    'restricted_to_self_maps': True},
            'covered_intervals': len(accepted), 'failed_intervals': len(failed),
            'cover_endpoint': str(cursor), 'certificates': accepted,
            'failures': failed}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lower', default='0.000615384615384615')
    parser.add_argument('--upper', default='0.000666666666666667')
    parser.add_argument('--extra', default='0')
    parser.add_argument('--order', type=int, default=40)
    parser.add_argument('--steps', type=int, default=192)
    parser.add_argument('--first-exit-cover', action='store_true')
    parser.add_argument('--receipt')
    args = parser.parse_args()
    if args.first_exit_cover:
        result = certify_first_exit_cover()
        if args.receipt:
            Path(args.receipt).write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({k: v for k, v in result.items()
                          if k not in ('certificates', 'failures')}), flush=True)
    else:
        for sign in (-1, 1):
            print(json.dumps(certify(sign, Q(args.lower), Q(args.upper),
                                     Q(args.extra), args.order, args.steps)), flush=True)
