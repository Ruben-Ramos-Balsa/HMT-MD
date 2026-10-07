"""Extensión focal, sin recalcular los generadores ni alterar sus fuentes.

Reutiliza las evaluaciones ya guardadas por MASAS. Añade controles algebraicos
y cotas racionales para los extremos de Wien. No introduce coordenadas SI.
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent

def require(value, label):
    if not value:
        raise AssertionError(label)

def times(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j] += x*y
    return c

def derivative(a): return [i*a[i] for i in range(1, len(a))]

def exp_bounds(x, n=100):
    """x>=0, Taylor positivo y mayorante geométrica de su resto."""
    term = total = F(1)
    for k in range(1,n+1):
        term *= x/k
        total += term
    next_term = term*x/(n+1)
    return total, total+next_term/(1-x/(n+2))

def wien_interval(m):
    # f(x)=m(1-exp(-x))-x: f''<0. f'(0)>0 y f(m)<0.
    # Hay una única raíz estrictamente positiva. En [m-1,m], f'<0.
    def signs(x):
        lo,hi=exp_bounds(x)
        return m*(1-1/lo)-x, m*(1-1/hi)-x
    lo,hi=F(m-1),F(m)
    require(signs(lo)[0]>0 and signs(hi)[1]<0, 'intervalo inicial Wien')
    for _ in range(85):
        mid=(lo+hi)/2; fl,fh=signs(mid)
        if fl>0:lo=mid
        elif fh<0:hi=mid
        else:raise AssertionError('Aumentar orden Taylor')
    with localcontext() as c:
        c.prec=35; c.rounding=ROUND_FLOOR
        dl=str(D(lo.numerator)/D(lo.denominator))
        c.rounding=ROUND_CEILING
        dh=str(D(hi.numerator)/D(hi.denominator))
    return {'racionales':[str(lo),str(hi)],'intervalo_decimal_exterior':[dl,dh],
            'ancho_exacto':str(hi-lo),'raiz_cero_excluida':True}

def main():
    numeric_path=AUDIT/'VALORES_RECALCULADOS_CORPUS.json'
    spectral_path=AUDIT/'VALORES_ESPECTRALES_RECALCULADOS.json'
    data=json.loads(numeric_path.read_text())
    spectral=json.loads(spectral_path.read_text())
    values={r['nombre']:D(r['valor']) for r in data['valores']}
    # Identidad polinómica para el numerador de F' en todos los s.
    numerator=[F(1),F(1),F(1)]; denominator=numerator+[F(1)]
    lhs=times(derivative(numerator),denominator)
    rhs=times(numerator,derivative(denominator))
    n=max(len(lhs),len(rhs));lhs += [F(0)]*(n-len(lhs));rhs += [F(0)]*(n-len(rhs))
    require([x-y for x,y in zip(lhs,rhs)]==[0,0,-3,-2,-1], 'derivada exacta F')
    require(F(sum(numerator),sum(denominator))==F(3,4),'limite 3/4')
    with localcontext() as c:
        c.prec=100
        mu,eps,z,speed=[values[k] for k in ('permeabilidad_normalizada','permitividad_normalizada','impedancia_normalizada','velocidad_normalizada')]
        rk,g0,flux,kj=[values[k] for k in ('von_Klitzing_normalizada','conductancia_normalizada','flujo_pre_normalizado','Josephson_pre_normalizada')]
        alpha=values['alpha_12']; h=values['h_pre_en_U_S']; charge=values['carga_pre_normalizada']
        residuals={'mu_eps_c2':mu*eps*speed**2-1,'mu_eps_Z2':mu/eps-z**2,
                   'RK_G0':rk*g0-2,'G0_Z':g0*z-4*alpha,'KJ_Phi0':kj*flux-1,
                   'carga':charge**2*z/(2*alpha*h)-1}
        require(all(abs(x)<D('1e-85') for x in residuals.values()),'identidades sobre datos reutilizados')
        require(0<mu<eps<1 and 0<z<1<speed,'orden de respuestas')
        pi=values['pi_HMT']; log3=D(3).ln(); ap=D(spectral['valores']['Apery_zeta3'])
        additions={
            'lambda_max_sobre_l0':108*log3/values['Wien_x5'],
            'nu_max_por_t0':values['Wien_x3']/(108*log3),
            'coeficiente_flujo_Stefan':2*pi**5/(15*D(108)**4*log3**4),
            'densidad_fotonica_por_lP3':2*ap/(pi**2*log3**3),
            'energia_fotonica_por_lP3_sobre_EP':pi**2/(15*log3**4),
            'entropia_fotonica_por_lP3_sobre_kB':4*pi**2/(45*log3**3),
            'conductancia_termica_por_t0_sobre_kB':pi**2/(324*log3)}
    result={'estado':'COMPROBACIONES_FOCALES_SATISFECHAS',
            'reutilizados':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (numeric_path,spectral_path)},
            'polinomio_derivada_F':[0,0,-3,-2,-1],
            'residuos_numericos':{k:str(v) for k,v in residuals.items()},
            'coeficientes_termicos':{k:str(v) for k,v in additions.items()},
            'intervalos_Wien':{str(m):wien_interval(m) for m in (3,5)},
            'alcance':'Pruebas algebraicas del lector declarado, intervalos racionales de Wien y evaluacion de composiciones termicas. No determina una carta SI ni prueba por si sola una distribucion fisica.'}
    (HERE/'COMPROBACION_VACIO_TERMICAS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
