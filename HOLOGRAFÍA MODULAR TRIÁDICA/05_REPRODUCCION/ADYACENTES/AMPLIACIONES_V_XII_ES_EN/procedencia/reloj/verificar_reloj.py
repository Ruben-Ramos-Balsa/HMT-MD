#!/usr/bin/env python3
"""Comprobación exacta del reloj y de sus lectores; no introduce decimales objetivo."""
from fractions import Fraction as F
from collections import defaultdict
import json
from pathlib import Path

def verify():
    families = defaultdict(int)
    def check(name, assertion):
        assert assertion, name
        families[name] += 1
    fibers = defaultdict(list)
    for t in range(108):
        r, beta = t % 9, t // 9
        b, k, j, z = beta % 4, beta % 3, t % 4, t % 27
        check('inversa_CRT108', (81*j + 28*z) % 108 == t)
        check('coordenada_plano_con_acarreo', j == (r+b) % 4)
        check('inversa_CRT12', (9*b+4*k) % 12 == beta)
        check('caracter_fiel_exacto', (F(t,108)-3*F(j,4)-7*F(z,27)).denominator == 1)
        fibers[(r,b)].append(t)
        for u in range(108):
            v=(t+u)%108
            check('homomorfismo_CRT108', v%4==(j+u%4)%4 and v%27==(z+u%27)%27)
            ru, bu=u%9, (u//9)%4
            check('acarreo_reducido', (v//9)%4==(b+bu+(r+ru)//9)%4 and v%9==(r+ru)%9)
    check('36_fibras', len(fibers)==36)
    for values in fibers.values():
        check('fibra_ternaria', len(values)==3 and values[1]-values[0]==36 and values[2]-values[1]==36)
    for beta in range(12):
        t=9*beta
        check('inclusion_nucleo', t%4==beta%4 and t%27==(9*beta)%27)
        check('caracter_plano_restriccion', (3*F(t,108)-F(beta,4)).denominator==1)
    for n in range(9):
        check('seccion_C36', (28*n%36)%9==n)
        for m in range(9):
            check('seccion_C36_aditiva', (28*((n+m)%9))%36==(28*n+28*m)%36)
    extensions=[]
    for ell in range(108):
        holds=all((F(ell*9*b,108)-F(b,4)).denominator==1 for b in range(12))
        check('extensiones_caracter', holds==(ell%12==3))
        if holds: extensions.append(ell)
    check('nueve_extensiones', len(extensions)==9)
    check('falsador_beta_no_homomorfismo', ((8//9)+(1//9))%4 != (9//9)%4)
    check('falsador_cubo_necesario', (F(27,108)-F(27%4,4)).denominator != 1)
    check('falsador_reduccion_no_inyectiva', fibers[(0,0)]==[0,36,72])
    check('no_seccion_C27_C9', all(not(9*x%27==0 and x%9==1) for x in range(27)))
    return dict(status='PASS_RELOJ_CUARTO_Y_ACARREO', arithmetic='integer_and_rational_exact',
                domain='finite_observable_clock_C108_and_declared_quotients',
                checks_by_family=dict(families),checks_total=sum(families.values()),
                extensions_C108_of_C12_quarter=extensions,
                counterexample_same_reduced_reading=[0,36,72],
                no_global_corpus_certification=True)

if __name__=='__main__':
    result=verify()
    (Path(__file__).parent/'RESULTADOS_RELOJ.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
