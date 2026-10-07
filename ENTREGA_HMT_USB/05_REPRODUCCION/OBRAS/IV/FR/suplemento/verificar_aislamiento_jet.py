#!/usr/bin/env python3
"""Certificado racional del intervalo publicado para la raíz del jet de orden nueve."""
from pathlib import Path
from fractions import Fraction as F
import runpy
import json
ROOT=Path(__file__).resolve().parent
ns=runpy.run_path(str(ROOT/"alpha/technical/verificar_lector_analitico_alpha.py"),run_name="lector_jet")
p=ns["read_generated_coordinate_interval"]("pi")
numerator=ns["log_bounds"](F(10,9),520)
denominator=ns["log_bounds"](F(10),520)
d=ns["interval_div"](numerator,denominator)
x0=F(729735256928380099,10**20)
x1=F(729735256928380100,10**20)
left=ns["e9_interval"](ns["point"](x0),p,d)
right=ns["e9_interval"](ns["point"](x1),p,d)
if not (left[1]<0<right[0]):
    raise ValueError("El intervalo no aísla la raíz")
if not x0<x1:
    raise ValueError("Extremos desordenados")
print(json.dumps({"status":"PASS_AISLAMIENTO_RACIONAL_JET_9",
 "left_sign":"negative","right_sign":"positive","log_terms":520,
 "scope":"Comprueba los signos del intervalo de prueba, posterior a la generación; no selecciona coeficientes ni sustituye la prueba de unicidad."},ensure_ascii=False))
