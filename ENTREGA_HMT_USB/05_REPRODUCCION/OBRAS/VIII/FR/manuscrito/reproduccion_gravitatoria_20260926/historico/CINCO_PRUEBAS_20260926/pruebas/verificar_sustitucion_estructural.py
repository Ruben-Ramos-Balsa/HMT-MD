"""Reevaluate the declared length candidate from archived HMT coordinates.

This is a downstream substitution, not a reexecution of APP/TRIT/TPK or
a proof that the proposed length reader is physically selected.
No experimental G or tabulated Planck length is an input.
"""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
TECH = ROOT / 'datos'
VALUES = TECH / 'EVALUACION_VACIO.json'


def evaluate(precision):
    archived = json.loads(VALUES.read_text())
    with localcontext() as ctx:
        ctx.prec = precision
        pi, phi, e = [D((TECH/'datos_generados'/f'{name}_1000_decimales.txt').read_text().strip())
                      for name in ('pi', 'phi', 'e')]
        register = archived['K']
        numerator = sum(int(k) * 1000**(11-j) for j, k in enumerate(register))
        kappa = D(numerator) / D(1000**12-1)
        alpha = pi + e - phi - 4 - kappa
        H5 = ((1000*alpha/phi).sqrt()/2 - alpha + D(9)/16*alpha**2
              - D(5)/9*alpha**3 + D(7)/48*alpha**4 - alpha**5/54)
        DA = (-100*pi*alpha/9).exp()
        Cpi = 169*alpha**6 + DA*alpha**7/(1-DA*alpha)
        eta = H5 - 90/pi*Cpi
        delta = (pi-e*pi.ln())/270*(1+pi/729)
        Ract = H5/eta
        exponent = 80-54*alpha+6*delta
        electron = D(3).sqrt()/4*((phi/pi**2).exp()-22*alpha**3)*(1+15*delta)
        electron *= (exponent*Ract.ln()).exp()
        x, y = pi*1000*alpha/180, pi*2*(eta+alpha)/180
        qp, qm = (-x-y).exp(), (-x+y).exp()
        rp, rm = [(1-q**90)/(1-q**120) for q in (qp, qm)]
        chat = 1/(rp*rm)
        # Declared SI realization, not a derivation of this dimensional reader.
        c = D(299792458)
        hbar = eta*D('1e-34')
        energy = electron*D('1.602176634e-13')
        q = alpha**16*D(5759)/23040
        length = q  # q times one metre: explicit hypothesis.
        G = c**3*length**2/hbar
        expanded_G = c**3*D(5759)**2*alpha**32/(D(23040)**2*eta*D('1e-34'))
        coupling = (energy*length/(hbar*c))**2
        mass = energy/c**2
        t0 = pi*length/(54*c)  # induced compatibility, not an independent clock.
        G_clock = (54/pi)**2*c**5*t0**2/hbar
        tol = D(10)**(-precision+10)
        assert abs(expanded_G/G-1) < tol
        assert abs(G_clock/G-1) < tol
        assert abs(G*mass**2/(hbar*c)/coupling-1) < tol
        # Recomputed quantities versus separately archived downstream results.
        for name, value in [('alpha', alpha), ('H5', H5), ('eta_ret', eta), ('c_hat', chat)]:
            assert abs(value/D(archived['values'][name])-1) < D('1e-75'), name
        return {key: str(value) for key, value in {
            'alpha': alpha, 'H5': H5, 'eta_ret': eta,
            'electron_beta_MeV': electron, 'c_hat': chat,
            'length_m': length, 'G_SI': G, 'electron_gravitational_coupling': coupling,
            't0_induced_seconds': t0,
        }.items()}


def exact_checks():
    # Standard radial identity under the declared HMT mode realization.
    count = 0
    for radius in (F(2, 3), F(5), F(11, 7)):
        hbar, speed = F(13, 17), F(19, 23)
        mode_mass = hbar/(speed*radius)
        G = speed**3*radius**2/hbar
        assert G*mode_mass/speed**2 == radius
        for factor in (F(1, 3), F(1), F(7, 2)):
            assert factor*G*mode_mass/speed**2 == factor*radius
            count += 1
    return count


def main():
    low, high = evaluate(100), evaluate(130)
    for key in high:
        assert format(D(low[key]), '.70E') == format(D(high[key]), '.70E'), key
    files = [Path(__file__).resolve(), VALUES]
    files += [TECH/'datos_generados'/f'{name}_1000_decimales.txt' for name in ('pi', 'phi', 'e')]
    print(json.dumps({
        'status': 'PASS_DOWNSTREAM_STRUCTURAL_SUBSTITUTION',
        'exact_radial_cases': exact_checks(),
        'stable_significant_digits': 71,
        'APP_TRIT_TPK_reexecuted': False,
        'K_selection_reexecuted': False,
        'K_and_regions_are_archived_upstream_outputs': True,
        'G_reference_input': False,
        'Planck_length_reference_input': False,
        'length_reader_physically_selected': False,
        'independent_clock_constructed': False,
        'field_coupling_identification_proven': False,
        'result': high,
        'sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
