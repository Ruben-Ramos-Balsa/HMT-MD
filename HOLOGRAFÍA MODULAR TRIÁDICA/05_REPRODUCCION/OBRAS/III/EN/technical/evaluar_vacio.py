#!/usr/bin/env python3
"""Evaluación posterior del artículo III; no es el productor primario APP-TPK."""
from pathlib import Path
import hashlib
import json
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'technical' / 'datos_generados'
mp.mp.dps = 120
records = {}
def read_coordinate(name):
    p = DATA / (name + '_1000_decimales.txt')
    b = p.read_bytes()
    records[name] = {'path': str(p.relative_to(ROOT)),
                     'sha256': hashlib.sha256(b).hexdigest(),
                     'causal_role': 'UPSTREAM_HMT_OUTPUT'}
    return mp.mpf(b.decode().strip())

pi, phi, e = [read_coordinate(n) for n in ('pi', 'phi', 'e')]
# Registro obtenido en base_articulo_I/sections/registro_k.tex, eq:k-vector.
K = (234,543,140,729,659,824,621,58,914,794,146,601)
nk = sum(k*1000**(11-j) for j,k in enumerate(K))
kappa = mp.mpf(nk)/(1000**12-1)
alpha = pi+e-phi-4-kappa
H5 = (mp.sqrt(1000*alpha/phi)/2-alpha+mp.mpf(9)/16*alpha**2
      -mp.mpf(5)/9*alpha**3+mp.mpf(7)/48*alpha**4-alpha**5/54)
DA = mp.exp(-100*pi*alpha/9)
Cpi = 169*alpha**6+DA*alpha**7/(1-DA*alpha)
eta = H5-90/pi*Cpi
A, C = 1000*alpha, 2*(eta+alpha)
x, y = pi*A/180, pi*C/180
qp, qm = mp.exp(-x-y), mp.exp(-x+y)
sp, sm = qp**30, qm**30
def f(s): return (1+s+s*s)/(1+s+s*s+s*s*s)
def k4(s): return s/(1+s*s)
def H(s): return 12*s**3/(1-s**9)-s**4/(1-s**12)-mp.log(s)**2/(20*pi)
def S(q,m): return q**m/(1-q**(3*m))
rp, rm = f(sp), f(sm)
eps, mu, Z, c = rp**2, rm**2, rm/rp, 1/(rp*rm)
gamma = pi*A*C/180+12*(S(qm,90)-S(qp,90))-(S(qm,120)-S(qp,120))
rho = 2-mp.sqrt(3)
C2 = lambda s: mp.quad(lambda t: mp.atan(t)/t if t else mp.mpf(1), [0,s])
G = C2(1)
checks = []
def check(name, condition):
    checks.append({'id':name,'pass':bool(condition)})
    if not condition: raise AssertionError(name)
tol = mp.mpf('1e-95')
check('ordered_chamber',0<y<x and 0<qp<qm<1 and mp.mpf(3)/4<rm<rp<1)
check('product',abs(mu*eps-c**-2)<tol)
check('quotient',abs(mu/eps-Z**2)<tol)
check('gamma_functional',abs(gamma-(H(sm)-H(sp)))<tol)
check('pell_kernel',abs(k4(rho)-mp.mpf(1)/4)<tol)
check('pell_moment',abs(C2(rho)-(mp.mpf(2)/3*G-pi/12*mp.log(2+mp.sqrt(3))))<tol)
check('angular_x',abs(-mp.log(qp*qm)/2-x)<tol)
check('angular_y',abs(mp.log(qm/qp)/2-y)<tol)
for j in range(1,20):
    s=mp.mpf(j)/20; r=f(s)
    check('cubic_'+str(j),abs(r*s**3+(r-1)*(1+s+s*s))<tol)
    check('resolvent_'+str(j),abs(f(s)-(1+s+s*s)/(s*(1+s))*k4(s))<tol)
values = dict(alpha=alpha,H5=H5,eta_ret=eta,A_deg=A,C_deg=C,q_plus=qp,q_minus=qm,
              s_plus=sp,s_minus=sm,r_plus=rp,r_minus=rm,epsilon_hat=eps,mu_hat=mu,
              Z_hat=Z,c_hat=c,gamma=gamma,Catalan=G,rho_Pell=rho)
payload={'scope':'POSTERIOR_NUMERICAL_EVALUATION_AND_LOCAL_IDENTITIES',
         'primary_generator_executed_by_this_script':False,
         'input_coordinates':records,'K':K,'K_source':'base_articulo_I/sections/registro_k.tex:eq:k-vector',
         'alpha_route':'periodic_positional_closure',
         'precision_decimal_digits':120,'checks':checks,
         'values':{k:mp.nstr(v,90) for k,v in values.items()}}
(ROOT/'technical'/'EVALUACION_VACIO.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
labels=[('alpha',r'\alpha'),('H5',r'H_5'),('eta_ret',r'\eta_{\rm ret}'),
        ('A_deg',r'A_{\deg}'),('C_deg',r'C^*_{\deg}'),('q_plus',r'q_+'),('q_minus',r'q_-'),
        ('r_plus',r'r_+'),('r_minus',r'r_-'),('epsilon_hat',r'\widehat\varepsilon'),
        ('mu_hat',r'\widehat\mu'),('Z_hat',r'\widehat Z'),('c_hat',r'\widehat c'),
        ('gamma',r'\gamma'),('Catalan',r'G_{\rm Cat}'),('rho_Pell',r'\rho')]
tex='\\begin{longtable}{@{}ll@{}}\n\\toprule\nObjeto & Evaluación decimal (24 cifras significativas)\\\\\n\\midrule\\endhead\n'
for k,label in labels:
    tex+='$'+label+'$ & $'+mp.nstr(values[k],24)+r'\ldots$ \\'+'\n'
tex+='\\bottomrule\n\\end{longtable}\n'
(ROOT/'manuscrito'/'tabla_evaluacion.tex').write_text(tex)
print('EVALUACION_LOCAL_III checks='+str(len(checks))+' passed='+str(sum(c['pass'] for c in checks)))
for key in ['r_plus','r_minus','epsilon_hat','mu_hat','Z_hat','c_hat','gamma']:
    print(key+'='+mp.nstr(values[key],32))
