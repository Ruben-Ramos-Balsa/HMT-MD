#!/usr/bin/env python3
"""Reproduce las cotas racionales de signo del truncamiento de grado nueve.

Los extremos son candidatos de aislamiento de la raíz del polinomio ya
definido. No se emplean para fijar sus coeficientes ni como valores de alfa.
"""
from pathlib import Path
from fractions import Fraction
import json
import runpy

ROOT = Path(__file__).resolve().parent

def main():
    m = runpy.run_path(str(ROOT / 'verificar_lector_analitico_alpha.py'))
    pi = m['read_generated_coordinate_interval']('pi')
    delta = m['delta_bounds']()
    bounds = ((729735256928380099, -4559, -4558),
              (729735256928380100, 1698, 1699))
    results = []
    for numerator, lo, hi in bounds:
        x = Fraction(numerator, 10**20)
        value = m['e9_interval'](m['point'](x), pi, delta)
        if not Fraction(lo, 10**23) < value[0] <= value[1] < Fraction(hi, 10**23):
            raise RuntimeError('El intervalo calculado no satisface las cotas publicadas')
        results.append(dict(x=str(x), lower=str(Fraction(lo, 10**23)),
                            upper=str(Fraction(hi, 10**23))))
    print(json.dumps(dict(status='PASS_AISLAMIENTO_RACIONAL_JET9',
                          arithmetic='fractions.Fraction',
                          scope='Two directed endpoint signs, not full alpha generation',
                          intervals=results), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
