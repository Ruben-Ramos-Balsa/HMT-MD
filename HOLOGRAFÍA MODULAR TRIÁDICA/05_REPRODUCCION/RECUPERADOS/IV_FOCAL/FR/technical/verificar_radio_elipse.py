"""Regresión exacta del enlace angular–elipse–dualidad de IV REV02.

Biblioteca estándar; no consulta constantes físicas objetivo. Las identidades
generales se prueban en el manuscrito. Este control verifica una identidad
polinómica, cotas racionales, transportes y casos negativos. No certifica por
sí solo los generadores anteriores ni una equivalencia física global.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]


def multiply(p, q):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            key = i + k, j + l
            out[key] = out.get(key, F(0)) + a * b
    return {k: v for k, v in out.items() if v}


def radius_fourth(xi):
    if not -1 < xi < 1:
        raise ValueError("La carta elíptica exige |C/A|<1")
    return (1 - xi) / (1 + xi)


def inverse_ratio(r4):
    if r4 <= 0:
        raise ValueError("El radio exige cuarta potencia positiva")
    return (1 - r4) / (1 + r4)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    checks = []

    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})

    # (A-C)(501α+η)=(A+C)(499α-η), A=1000α,C=2(η+α).
    left = multiply({(1, 0): F(998), (0, 1): F(-2)},
                    {(1, 0): F(501), (0, 1): F(1)})
    right = multiply({(1, 0): F(1002), (0, 1): F(2)},
                     {(1, 0): F(499), (0, 1): F(-1)})
    check("identidad_en_Q_alpha_eta", left == right)

    # Cotas holgadas usadas sólo para pertenencia a la carta.
    amin, amax, phimin, phimax = F(7, 1000), F(8, 1000), F(1618, 1000), F(1619, 1000)
    check("raiz_principal_mayor_2", 1000 * amin > 4 * phimax)
    check("raiz_principal_menor_3", 1000 * amax < 9 * phimin)
    lower_h = 1 - amax - F(5, 9) * amax**3 - F(1, 54) * amax**5
    upper_h = F(3, 2) + F(9, 16) * amax**2 + F(7, 48) * amax**4
    # 0<DA<1 y π>3 implican 90/π Cπ < 30(169a^6+a^7/(1-a)).
    upper_correction = 30 * (169 * amax**6 + amax**7 / (1 - amax))
    check("H5_superior_menor_2", upper_h < 2)
    check("eta_ret_positiva", lower_h - upper_correction > 0)
    check("dominio_angular_C_menor_A", 2 * (upper_h + amax) < 1000 * amin)

    ratios = [F(n, 20) for n in range(-19, 20)]
    check("radio_positivo", all(radius_fourth(x) > 0 for x in ratios))
    check("recuperacion_angular", all(inverse_ratio(radius_fourth(x)) == x for x in ratios))
    check("reciprocidad_orientada", all(radius_fourth(-x) * radius_fourth(x) == 1 for x in ratios))
    check("invariancia_unidad_angular", all((F(7) * x) / F(7) == x for x in ratios))
    for bad in (F(-2), F(-1), F(1), F(2)):
        try:
            radius_fourth(bad)
            rejected = False
        except ValueError:
            rejected = True
        check("rechazo_frontera_" + str(bad), rejected)
    for bad in (F(0), F(-1)):
        try:
            inverse_ratio(bad)
            rejected = False
        except ValueError:
            rejected = True
        check("rechazo_radio_" + str(bad), rejected)

    def energy(m, w, r):
        return F(m * m) / r**2 + w * w * r**2

    radii = [F(1, 3), F(1, 2), F(1), F(2), F(3)]
    check("conservacion_forma", all(energy(m, w, r) == energy(w, m, 1/r)
          for r in radii for m in range(-3, 4) for w in range(-3, 4)))
    check("familia_dos_fibras_estable", all({r, 1/r} == {1/r, r} for r in radii))
    check("fibra_unica_solo_radio_1", all((r == 1/r) == (r == 1) for r in radii))
    for r in radii:
        a, b, hbar = r**-1, r, F(1, 2)
        check("matriz_elipse_" + str(r), a*b == 2*hbar and a*a/(2*hbar) == r**-2 and b*b/(2*hbar) == r**2)

    sources = []
    for name in ("iv_accion_antecedente.tex", "iv_angulos_antecedente.tex", "iv_elipse_radio.tex", "02_dualidad_t.tex", "03_pantallas_coordinadas.tex"):
        p = ROOT / "sections" / name
        check("fuente_presente_" + name, p.is_file())
        if p.is_file():
            sources.append({"path": str(p.relative_to(ROOT)), "sha256": sha256(p.read_bytes()).hexdigest()})
    report = {"schema": "HMT_IV_RADIO_ELIPSE_REV02_V1",
              "status": "PASS_RADIO_ELIPSE_IV_REV02" if all(c["passed"] for c in checks) else "FAIL_RADIO_ELIPSE_IV_REV02",
              "scope": "Identidad polinómica exacta, cotas de pertenencia, regresiones racionales y casos negativos; no prueba global de HMT.",
              "checks": checks, "source_files": sources,
              "verifier_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    out = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(out, encoding="utf-8")
    print(out, end="")
    return 0 if report["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
