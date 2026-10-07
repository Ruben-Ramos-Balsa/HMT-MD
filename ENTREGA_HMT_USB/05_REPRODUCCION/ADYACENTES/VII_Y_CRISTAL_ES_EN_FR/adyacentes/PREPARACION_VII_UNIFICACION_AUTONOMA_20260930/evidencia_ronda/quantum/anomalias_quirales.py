#!/usr/bin/env python3
"""Exact anomaly coefficients for the received HMT matter realization.

No numerical physical constants, experimental targets or floating point are
used. Electric charge labels are read as the representation already published
in the HMT catalogue, then Y=Q-T3 is applied in the declared weak realization.
This verifies compatibility of that representation; it does not produce a
nonperturbative chiral functional measure or quantize the gravitational field.
Run: python3 -I -S anomalias_quirales.py
"""

from dataclasses import dataclass
from fractions import Fraction as F
import json


@dataclass(frozen=True)
class Multiplet:
    name: str
    dc: int
    dw: int
    Y: F
    T3: F
    T2: F
    A3: int


Q = {"up": F(2, 3), "down": F(-1, 3), "nu": F(0), "lepton": F(-1)}
Yq = Q["up"] - F(1, 2)
Yl = Q["nu"] - F(1, 2)
if Yq != Q["down"] + F(1, 2) or Yl != Q["lepton"] + F(1, 2):
    raise ValueError("Charge reader is incompatible with the declared doublets")

# Every entry is a LEFT-handed Weyl multiplet. Right-handed particles are
# represented by their left-handed charge conjugates, reversing hypercharge
# and SU(3) cubic index, but NOT the quadratic Dynkin index.
MATTER = (
    Multiplet("q_L", 3, 2, Yq, F(1, 2), F(1, 2), 1),
    Multiplet("u_R^c", 3, 1, -Q["up"], F(1, 2), F(0), -1),
    Multiplet("d_R^c", 3, 1, -Q["down"], F(1, 2), F(0), -1),
    Multiplet("l_L", 1, 2, Yl, F(0), F(1, 2), 0),
    Multiplet("e_R^c", 1, 1, -Q["lepton"], F(0), F(0), 0),
)
STERILE = Multiplet("nu_R^c_optional", 1, 1, F(0), F(0), F(0), 0)
LOCAL = ("SU3^2_U1", "SU2^2_U1", "U1^3", "gravity^2_U1", "SU3^3")


def coefficients(matter, generations=1):
    return {
        "SU3^2_U1": generations * sum((m.dw * m.Y * m.T3 for m in matter), F(0)),
        "SU2^2_U1": generations * sum((m.dc * m.Y * m.T2 for m in matter), F(0)),
        "U1^3": generations * sum((m.dc * m.dw * m.Y**3 for m in matter), F(0)),
        "gravity^2_U1": generations * sum((m.dc * m.dw * m.Y for m in matter), F(0)),
        "SU3^3": generations * sum(m.dw * m.A3 for m in matter),
        "SU2_doublets": generations * sum(m.dc for m in matter if m.dw == 2),
    }


def inconsistent(c):
    return any(c[k] != 0 for k in LOCAL) or c["SU2_doublets"] % 2 != 0


def stringify(c):
    return {k: str(v) for k, v in c.items()}


def main():
    checks = []

    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

    for n in (1, 2, 3, 4, 17):
        c = coefficients(MATTER, n)
        for key in LOCAL:
            check(f"{n}_generations_{key}", c[key] == 0)
        check(f"{n}_generations_even_doublets", c["SU2_doublets"] == 4 * n)

    check("neutral_singlet_preserves_every_coefficient", coefficients(MATTER + (STERILE,)) == coefficients(MATTER))
    removed = {}
    for m in MATTER:
        c = coefficients(tuple(x for x in MATTER if x != m))
        removed[m.name] = stringify(c)
        check(f"negative_remove_{m.name}", inconsistent(c))

    result = {
        "status": "PASS_CHIRAL_REPRESENTATION_ANOMALIES",
        "checks_passed": len(checks),
        "checks_expected": 36,
        "arithmetic": "exact rational; no floating point",
        "scope": "Published charge labels, declared weak representation and Weyl chirality; no claim of a chiral measure or quantum gravity.",
        "source_charge_catalogue": "/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VI_ES/sections/11_apendices_catalogo.tex:297",
        "source_charge_character": "/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VI_ES/sections/03_conjugacion_mobius.tex:114",
        "hypercharge_convention": "Q = T3 + Y; global integral normalization y = 6Y",
        "one_generation": stringify(coefficients(MATTER)),
        "three_generations": stringify(coefficients(MATTER, 3)),
        "quarks_only_negative": stringify(coefficients(MATTER[:3])),
        "multiplet_removal_negative": removed,
        "checks": checks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
