from fractions import Fraction
from decimal import Decimal, getcontext
import json, math, cmath
from pathlib import Path

getcontext().prec = 80
OUT = Path('/mnt/data')


def dr9(n:int)->int:
    r=n%9
    return 9 if r==0 else r

# APP 2D
S_plus_2 = sum(dr9(i+j) for i in range(1,10) for j in range(1,10))
S_prod_2 = sum(dr9(i*j) for i in range(1,10) for j in range(1,10))
Delta_2 = S_prod_2 - S_plus_2
Sigma_2 = S_plus_2 + S_prod_2
# APP 3D active
S_plus_3 = sum(dr9(i+j+k) for i in range(1,10) for j in range(1,10) for k in range(1,10))
S_prod_3 = sum(dr9(i*j*k) for i in range(1,10) for j in range(1,10) for k in range(1,10))
Delta_3 = S_prod_3 - S_plus_3
moon_anchor = Delta_2 * (S_plus_3 + 1)
# Unit decomposition
bulk = 9**3
corona = 10**3 - 9**3
unit_frac = Fraction(bulk+corona, 1000)
# Euler triadic shadows
shadow_90_120 = Fraction(90-120,360)
shadow_6_8 = Fraction(6-8,24)
# 90/120 DFT in U12
N=12
vals=[]
for m in range(N):
    theta=2*math.pi*m/N
    vals.append(12*math.cos(3*theta)-math.cos(4*theta))
# DFT: F[k] = sum_m vals[m] exp(-2πikm/N)
F=[]
for k in range(N):
    F.append(sum(vals[m]*cmath.exp(-2j*math.pi*k*m/N) for m in range(N)))
amps=[abs(z) for z in F]
ratio_3_4 = amps[3]/amps[4] if amps[4] else None
nonzero_modes=[(k,amps[k]) for k in range(N) if amps[k] > 1e-8]
# Phi unit law with Decimal
sqrt5 = Decimal(5).sqrt()
phi = (Decimal(1)+sqrt5)/Decimal(2)
phi_plus_unit = phi + Decimal(1)
phi_square = phi*phi
phi_minus_unit = phi - Decimal(1)
phi_inv = Decimal(1)/phi
# finite block -1/12 exact extractor
Ns=[12,36,90,108,120,360,729,1000]
euler_extract=[]
for n in Ns:
    value = Fraction(n*(n+1),2) - Fraction(n*n+n,2) - Fraction(1,12)
    euler_extract.append({'N':n,'extractor':str(value)})

results={
    'APP_2D': {'S_plus':S_plus_2,'S_product':S_prod_2,'Delta':Delta_2,'Sigma':Sigma_2,'744_check_Sigma_minus_120':Sigma_2-120,'1728_check_2Sigma':2*Sigma_2},
    'APP_3D_active': {'S_plus':S_plus_3,'S_product':S_prod_3,'Delta':Delta_3,'bulk':bulk,'corona':corona,'unit_decomposition':str(unit_frac)},
    'Moonshine_anchor': {'Delta2_times_Splus3_plus_1':moon_anchor,'expected':196884,'pass': moon_anchor==196884,'196884_as_196883_plus_1': '196883+1'},
    'Euler_triadic': {'(90-120)/360': str(shadow_90_120), '(6-8)/24':str(shadow_6_8), 'same': shadow_90_120==shadow_6_8==Fraction(-1,12),'finite_extractors': euler_extract},
    'DFT_U12_90_120': {'nonzero_modes': [(int(k), float(v)) for k,v in nonzero_modes], 'amp_k3_over_k4': ratio_3_4},
    'Phi_unit_law': {'phi': str(phi), 'phi_plus_1_minus_phi_square': str(phi_plus_unit-phi_square), 'phi_minus_1_minus_inv_phi': str(phi_minus_unit-phi_inv)},
}
(OUT/'hmt_unidad_euler_triadico_01_results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(results, indent=2, ensure_ascii=False))
