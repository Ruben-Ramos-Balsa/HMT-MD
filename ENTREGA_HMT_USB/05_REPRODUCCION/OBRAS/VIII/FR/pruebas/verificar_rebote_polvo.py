#!/usr/bin/env python3
"""Identidades racionales de la solución de polvo; no simulación cosmológica."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
checks=0
def check(name,condition):
    global checks
    if not condition: raise RuntimeError(name)
    checks+=1
for den in range(1,12):
    for num in range(-30,31):
        x=F(num,den)
        # Units tau=1; 4*pi*G*rho_b=2/3.
        z=1+x*x
        H=2*x/(3*z)
        dH=2*(1-x*x)/(3*z*z)
        rho_m=1/z
        rho_s=1/(z*z)
        check("Friedmann",H*H==F(4,9)*(rho_m-rho_s))
        check("Raychaudhuri",dH==-F(2,3)*(rho_m-2*rho_s))
        check("Ricci",6*(dH+2*H*H)==(4+F(4,3)*x*x)/(z*z))
        check("minimum_cube",z>=1)
        check("phase_sign",(H==0 if x==0 else H*x>0))
check("reject_wrong_Friedmann_factor",F(1,9)!=F(2,9)*(F(1,2)-F(1,4)))
print(json.dumps({"status":"PASS_REBOTE_POLVO_VII","exact_checks":checks,
"scope":"Identidades de la solución normalizada; la prueba para todo tiempo está en51",
"initial_amplitude_selected":False,
"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},ensure_ascii=False))

