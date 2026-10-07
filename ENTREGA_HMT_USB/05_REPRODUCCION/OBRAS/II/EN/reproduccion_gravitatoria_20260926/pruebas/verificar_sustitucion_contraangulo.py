"""Reproduce the native Planck/counterangle substitution inside radial G.

No observed G is used as a target or input. The physical longitudinal section
and the reduced radial reading are the explicit realization being evaluated.
"""
from decimal import Decimal as D, localcontext
from pathlib import Path
import importlib.util
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = HERE / 'verificar_sustitucion_estructural.py'
OWNER = ROOT / 'propietarios' / 'composicion_contraangulo.tex'
PROOF = ROOT / 'demostraciones' / 'SUSTITUCION_CONTRAANGULO_Y_G.md'
spec = importlib.util.spec_from_file_location('structural', SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def evaluate(prec):
    checks = []
    with localcontext() as ctx:
        ctx.prec = prec
        v = {k:D(x) for k,x in m.evaluate(prec).items()}
        a, eta, c = v['alpha'], v['eta_ret'], D(299792458)
        pi, phi = [D((m.TECH/'datos_generados'/f'{name}_1000_decimales.txt').read_text().strip())
                   for name in ('pi','phi')]
        DA = (-100*pi*a/9).exp()
        Cp = 169*a**6+DA*a**7/(1-DA*a)
        B = D(9)/16*a**2-D(5)/9*a**3+D(7)/48*a**4-a**5/54-90/pi*Cp
        A = 1000*a
        C = (1000*a/phi).sqrt()+2*B
        recovered_eta = C/2-a
        xi_ang = C/A
        rn, sstar = D(5759)/23040, D('1e-34')
        g_eta = c**3*rn**2*a**32/(sstar*recovered_eta)
        g_C = 2*c**3*rn**2*a**32/(sstar*(C-2*a))
        g_xi = c**3*rn**2*a**31/(sstar*(500*xi_ang-1))
        x,y = pi*A/180, pi*C/180
        qp,qm = (-x-y).exp(),(-x+y).exp()
        rp,rm = [(1-q**90)/(1-q**120) for q in (qp,qm)]
        chat = 1/(rp*rm)
        cstar = c/chat
        Gdimensionless = rn**2*a**32*chat**3/recovered_eta
        g_constitutive = cstar**3/sstar*Gdimensionless
        tol = D(10)**(-prec+12)
        def ck(name, lhs, rhs):
            assert abs(lhs/rhs-1)<tol,(name,lhs,rhs)
            checks.append(name)
        ck('expanded_counterangle',C,2*(eta+a))
        ck('recovered_action',recovered_eta,eta)
        ck('angular_ratio_action',a*(500*xi_ang-1),eta)
        ck('G_expanded_eta',g_eta,v['G_SI'])
        ck('G_counterangle',g_C,v['G_SI'])
        ck('G_angular_ratio',g_xi,v['G_SI'])
        ck('constitutive_velocity',chat,v['c_hat'])
        ck('G_full_constitutive',g_constitutive,v['G_SI'])
        return {'checks':checks,'values':{k:str(x) for k,x in {
            'alpha':a, 'B_alpha':B, 'angle_deg':A, 'counterangle_deg':C,
            'eta_recovered':recovered_eta, 'xi_angular':xi_ang,
            'c_hat':chat,'dimensionless_G_composition':Gdimensionless,
            'G_from_counterangle_SI':g_C, 'G_from_expanded_eta_SI':g_eta,
            'G_from_constitutive_SI':g_constitutive}.items()}}


if __name__=='__main__':
    lo,hi=evaluate(100),evaluate(140)
    for key in hi['values']:
        assert format(D(lo['values'][key]),'.70E')==format(D(hi['values'][key]),'.70E'),key
    print(json.dumps({
        'status':'PASS_NATIVE_COUNTERANGLE_SUBSTITUTION_IN_RADIAL_G',
        'checks_at_each_precision':hi['checks'],
        'working_precisions':[100,140], 'stable_significant_digits':71,
        'result':hi['values'],
        'scope':{'hbar_is_an_independent_physical_input':False,
                 'G_observed_input':False,
                 'pi_phi_retained_as_upstream_HMT_outputs':True,
                 'dimensional_bases_explicit':True,
                 'physical_reader_selection_proven_by_substitution':False,
                 'PDFs_or_Lean_modified':False},
        'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (SOURCE,OWNER,Path(__file__).resolve(),
                            PROOF)}
    },ensure_ascii=False,indent=2))
