"""Single downstream evaluator for the accumulated radial HMT realization.

Archived generated coordinates feed the constructor. Reference measurements
are deliberately absent. The SI sections are explicit and may be changed
covariantly; additional digits are numerical precision, not measured accuracy.
"""
from decimal import Decimal as D, localcontext
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

UPSTREAM = Path(__file__).resolve().parents[1] / 'pruebas' / 'verificar_sustitucion_estructural.py'
spec = importlib.util.spec_from_file_location('hmt_upstream_substitution',UPSTREAM)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


def evaluate(precision=130, length_section_m='1', action_section_Js='1e-34',
             velocity_m_s='299792458'):
    with localcontext() as ctx:
        ctx.prec=precision
        v={k:D(x) for k,x in native.evaluate(precision).items()}
        pi=D((native.TECH/'datos_generados/pi_1000_decimales.txt').read_text().strip())
        alpha,eta=v['alpha'],v['eta_ret']
        Lstar,Sstar,c=map(D,(length_section_m,action_section_Js,velocity_m_s))
        if min(Lstar,Sstar,c)<=0:
            raise ValueError('The three dimensional sections must be positive')
        N=12*4*120
        rn=D(N-1)/(4*N)
        L=rn*alpha**16*Lstar
        hbar=eta*Sstar
        G=c**3*L**2/hbar
        t0=pi*L/(54*c)
        Q=hbar*c/L
        mclk=Q/c**2
        A=1000*alpha
        C=2*(eta+alpha)
        x,y=pi*A/180,pi*C/180
        qp,qm=(-x-y).exp(),(-x+y).exp()
        rp,rm=[(1-q**90)/(1-q**120) for q in (qp,qm)]
        chat=1/(rp*rm)
        Sn=lambda n,q:q**n/(1-q**(3*n))
        gamma=pi*A*C/180+12*(Sn(90,qm)-Sn(90,qp))-(Sn(120,qm)-Sn(120,qp))
        # The known functional rule of the Catalan moment, not just G_Cat.
        splus,sminus=qp**30,qm**30
        kernel=lambda s:s/(1+s*s)
        reader=lambda s:(1+s+s*s)/(s*(1+s))*kernel(s)
        Eelectron=v['electron_beta_MeV']*D('1.602176634e-13')
        me=Eelectron/c**2
        Le=hbar/(me*c)
        Re=G*me/c**2
        thermal_energy=Q/D(3).ln()
        tol=D(10)**(-precision+12)
        identities=[]
        def ck(name,a,b):
            if abs(a/b-1)>=tol:
                raise AssertionError((name,a,b))
            identities.append(name)
        ck('clock_formula',G,(54/pi)**2*c**5*t0**2/hbar)
        ck('counterangle_formula',G,2*c**3*L**2/(Sstar*(C-2*alpha)))
        ck('Planck_area',hbar*G/c**3,L**2)
        ck('clock_radial_normalization',G*mclk/c**2,L)
        ck('electron_reciprocity',Re*Le,L**2)
        ck('Catalan_function_plus',reader(splus),rp)
        ck('Catalan_function_minus',reader(sminus),rm)
        ck('constitutive_c',chat,v['c_hat'])
        ck('thermal_clock',thermal_energy,(2*pi*hbar)/(108*t0*D(3).ln()))
        vals={
            'alpha_HMT':alpha,'return_factor':rn,'length_Planck_m':L,
            'eta_return':eta,'hbar_return_Js':hbar,'G_m3_kg_s2':G,
            't0_s':t0,'clock_energy_J':Q,'clock_mass_kg':mclk,
            'kB_times_clock_temperature_J':thermal_energy,
            'angle_deg':A,'counterangle_deg':C,'Barbero_gamma':gamma,
            'r_plus':rp,'r_minus':rm,'c_hat':chat,
            'epsilon_hat':rp**2,'mu_hat':rm**2,'Z_hat':rm/rp,
            'electron_reduced_Compton_m':Le,'electron_reduced_radial_m':Re,
            'electron_dimensionless_gravity':G*me**2/(hbar*c),
            'gamma_times_Planck_area_m2':gamma*L**2}
        return {'values':{k:str(x) for k,x in vals.items()},'identities':identities,
                'dimensional_sections':{'length_m':str(Lstar),'action_Js':str(Sstar),'velocity_m_s':str(c)}}


def report():
    low,high=evaluate(100),evaluate(140)
    for key,value in high['values'].items():
        if format(D(low['values'][key]),'.70E')!=format(D(value),'.70E'):
            raise AssertionError(('unstable precision',key))
    paths=[UPSTREAM,native.VALUES,Path(__file__).resolve()]
    paths += [native.TECH/'datos_generados'/f'{k}_1000_decimales.txt' for k in ('pi','phi','e')]
    return {'status':'PASS_JOINT_DOWNSTREAM_EVALUATION',
            'working_precisions':[100,140],'stable_significant_digits':71,
            'G_measured_input':False,'Planck_length_tabulated_input':False,
            'full_generator_rerun':False,'physical_realization':'marked longitudinal reader, returned action, reduced radial response',
            'result':high,
            'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    result=report()
    if args.receipt:
        args.receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(result['status'],args.receipt)
    else:
        print(json.dumps(result,ensure_ascii=False,indent=2))
