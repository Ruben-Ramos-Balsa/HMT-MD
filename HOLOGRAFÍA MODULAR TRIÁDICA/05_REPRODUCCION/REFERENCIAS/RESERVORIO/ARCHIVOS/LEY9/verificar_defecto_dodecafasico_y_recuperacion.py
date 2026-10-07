#!/usr/bin/env python3
"""Extensión exacta del certificado local de proyectores; no verifica una EDP.

Reutiliza en solo lectura las operaciones racionales del propietario sellado.
Construye las matrices desde desplazamientos, nunca desde una constante física.
"""
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OWNER = ROOT / "REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/verificar_proyectores_ciclicos_menos_un_doce.py"
spec = importlib.util.spec_from_file_location("proyector_preexistente", OWNER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
I = m.identity(12)
zero = m.scale(F(0), I)
sub = lambda a, b: m.add(a, m.scale(F(-1), b))
P3 = m.invariant_projector(12, 3)
P4 = m.invariant_projector(12, 4)
P0 = m.invariant_projector(12, 1)
E = sub(P3, P4)
D3 = sub(I, m.cyclic_shift(12, 3))
D4 = sub(I, m.cyclic_shift(12, 4))
B = m.add(m.matmul(m.transpose(D3), D3), m.matmul(m.transpose(D4), D4))
S = m.cyclic_shift(12, 1)
m.require(m.matmul(m.transpose(S), m.matmul(B, S)) == B, "energía no covariante bajo fase")
m.require(m.matmul(P3, P4) == P0, "intersección incorrecta")
m.require(m.matmul(P4, P3) == P0, "conmutación incorrecta")
m.require(m.trace(E) / 12 == F(-1, 12), "traza firmada incorrecta")
m.require(m.matrix_power(E, 3) == E, "E no es tripotente")
m.require(m.trace(m.matrix_power(E, 2)) / 12 == F(5, 12), "módulo incorrecto")
e_spectrum = {k: 12-m.rank(sub(E, m.scale(F(k), I))) for k in (-1, 0, 1)}

# B es simétrico semidefinido positivo y sus filas tienen norma l1 <= 8.
# Se buscan autovalores enteros en esa cota, sin presuponer el espectro.
row_bound = int(max(sum(abs(x) for x in row) for row in B))
spectrum = {}
for lam in range(row_bound + 1):
    dim = 12-m.rank(sub(B, m.scale(F(lam), I)))
    if dim:
        spectrum[lam] = dim
m.require(sum(spectrum.values()) == 12, "la búsqueda no agotó el espectro")
projections = {}
for lam in spectrum:
    p = I
    for other in spectrum:
        if other != lam:
            p = m.matmul(p, m.scale(F(1, lam-other), sub(B, m.scale(F(other), I))))
    m.require(m.matmul(p, p) == p and m.transpose(p) == p, "proyector espectral inválido")
    m.require(m.rank(p) == spectrum[lam], "multiplicidad incorrecta")
    projections[lam] = p
m.require(projections[0] == P0, "el modo nulo no es la media")
total = zero
inverse = zero
for lam, p in projections.items():
    total = m.add(total, p)
    if lam:
        inverse = m.add(inverse, m.scale(F(1, lam), p))
m.require(total == I, "resolución espectral incompleta")
m.require(m.add(P0, m.matmul(inverse, B)) == I, "falló la recuperación en todo Q^12")
m.require(m.rank(D3 + D4 + [[F(1)]*12]) == 12, "extractor no inyectivo")
# Controles: cada canal aislado pierde información; E pierde más que D3,D4 juntos.
m.require(m.rank(D3) < 11 and m.rank(D4) < 11, "control de canal aislado")
m.require(m.rank(E) == 5 and m.rank(D3 + D4) == 11, "control de traza aislada")
print(json.dumps({
    "status": "PASS_DEFECTO_DODECAFASICO_Y_RECUPERACION",
    "method": "rational matrix identities on the full 12-dimensional space",
    "source": str(OWNER),
    "signed_trace": "-1/12",
    "absolute_trace": "5/12",
    "signed_spectrum": e_spectrum,
    "difference_energy_spectrum": spectrum,
    "sharp_lower_bound_on_mean_zero": min(k for k in spectrum if k),
    "sharp_upper_bound": max(spectrum),
    "recovery_identity": "P0 + B_dagger B = I",
    "phase_energy_identity": "S^T B S = B",
    "scope": "local dodecaphase register; no assertion of hydrodynamic regularity or capillary coefficient"
}, ensure_ascii=False, indent=2))
