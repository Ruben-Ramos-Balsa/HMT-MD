#!/usr/bin/env python3
"""Puerta ejecutable de la rectificación probatoria del 3 de septiembre.

El programa combina comprobaciones numéricas independientes con controles
estructurales sobre los dos puntos de entrada sucesores. No compila ni
modifica fuentes.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SYNTH = Path(
    "/Users/ruben/Documents/New project/output/"
    "SINTESIS_ACADEMICA_HMT_MD_AUTONOMIA_DEMOSTRATIVA_REFORZADA_20260903"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(f"FAIL_RECTIFICACION_PROBATORIA: {message}")


def run_gate(path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, "-I", "-S", str(path)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    require(proc.returncode == 0, f"falla el certificado {path}: {proc.stdout[-800:]}")


def pi_chudnovsky(precision: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = precision + 30
        constant = Decimal(426880) * Decimal(10005).sqrt()
        m, ell, x, k = 1, 13591409, 1, 6
        total = Decimal(ell)
        for n in range(1, precision // 14 + 6):
            m = (m * (k**3 - 16 * k)) // (n**3)
            ell += 545140134
            x *= -262537412640768000
            total += Decimal(m * ell) / Decimal(x)
            k += 12
        return +(constant / total)


def roots_and_electron() -> dict[str, str]:
    with localcontext() as ctx:
        ctx.prec = 85
        pi = pi_chudnovsky(80)
        epsilon = (Decimal(10) / Decimal(9)).ln() / Decimal(10).ln()

        def p6(x: Decimal) -> Decimal:
            return (
                2 * pi * x
                - Decimal(7) * x**2 / 4
                + x**3 / (2 * pi)
                + x**4 / 20
                - Decimal(2) * x**5 / 21
                - x**6 / 46
            )

        def p9(x: Decimal) -> Decimal:
            return p6(x) - x**7 / 120 + x**8 / 45 + Decimal(2) * x**9 / 495

        def root(function) -> Decimal:
            lo, hi = Decimal("0.0072"), Decimal("0.0074")
            require(function(lo) < epsilon < function(hi), "la raíz no queda encerrada")
            for _ in range(320):
                mid = (lo + hi) / 2
                if function(mid) < epsilon:
                    lo = mid
                else:
                    hi = mid
            return +(lo + hi) / 2

        xi6, xi9 = root(p6), root(p9)
        alpha = Decimal("0.007297352569283800997285105472380663")

        def trunc9(value: Decimal) -> Decimal:
            scale = Decimal(10) ** 9
            return (value * scale // 1) / scale

        target = Decimal("137.035999084")
        require(xi6 != alpha and xi9 != alpha, "se confundieron las dos raíces con alpha_12")
        require(trunc9(1 / xi6) == target, "Tr_9(xi6^-1) no coincide")
        require(trunc9(1 / xi9) == target, "Tr_9(xi9^-1) no coincide")
        require(trunc9(1 / alpha) == target, "Tr_9(alpha_12^-1) no coincide")

        e_hmt = Decimal(1).exp()
        phi_hmt = (Decimal(1) + Decimal(5).sqrt()) / 2
        delta4 = ((pi - e_hmt * pi.ln()) / Decimal(270)) * (
            Decimal(1) + pi / Decimal(729)
        )
        electron = (
            Decimal(3).sqrt()
            / Decimal(4)
            * ((phi_hmt / pi**2).exp() - Decimal(22) * alpha**3)
            * (Decimal(1) + Decimal(15) * delta4)
        )
        require(
            abs(delta4 - Decimal("0.000111196422692140054051134786120679"))
            < Decimal("1e-32"),
            "Delta_4 no conserva el factor nonádico",
        )
        require(
            abs(electron - Decimal("0.5109989224880660725098708771913494"))
            < Decimal("1e-34"),
            "el basal electrónico no coincide con la definición canónica",
        )
        return {
            "xi6": str(xi6),
            "xi9": str(xi9),
            "alpha12": str(alpha),
            "Tr9_inverse": str(target),
            "Delta4": str(+delta4),
            "electron_basal": str(+electron),
        }


def structural_checks() -> dict[str, str]:
    files = {
        "integral_main": ROOT / "manuscrito/main_sucesor_102_revision_quirurgica_viii_20260903.tex",
        "integral_structure": ROOT / "manuscrito/sucesor_102/estructura_102_capitulos_rectificacion_probatoria_20260903.tex",
        "integral_front": ROOT / "manuscrito/sucesor_102/deltas_ley9/00_teorema_generador_frontal_rectificacion_probatoria_20260903.tex",
        "integral_alpha": ROOT / "manuscrito/sucesor_102/deltas_ley9/c31_dos_vias_alpha_y_prolongacion_nonadica_rectificacion_probatoria_20260903.tex",
        "integral_g": ROOT / "manuscrito/sucesor_102/deltas_ley9/c50_gravedad_accion_rectificacion_probatoria_20260903.tex",
        "integral_barbero": ROOT / "manuscrito/sucesor_102/deltas_ley9/c51_barbero_area_informacion_rectificacion_probatoria_20260903.tex",
        "synthesis_main": SYNTH / "manuscrito/main_rectificacion_probatoria_autonoma_20260903.tex",
        "synthesis_continuum": SYNTH / "manuscrito/sections/rectificacion_probatoria_20260903/12_columna_causal_tpk_continuo.tex",
        "synthesis_alpha": SYNTH / "manuscrito/sections/rectificacion_probatoria_20260903/10g_prueba_constantes_matematicas_alpha_accion.tex",
        "synthesis_mass": SYNTH / "manuscrito/sections/rectificacion_probatoria_20260903/10j_prueba_ley_general_masas.tex",
        "synthesis_g": SYNTH / "manuscrito/sections/rectificacion_probatoria_20260903/10i_prueba_geometria_gravedad_informacion.tex",
    }
    texts: dict[str, str] = {}
    for name, path in files.items():
        require(path.is_file(), f"falta {name}: {path}")
        texts[name] = path.read_text(encoding="utf-8")

    joined = "\n".join(texts.values()).lower()
    for forbidden in ("app-min", "app mínima", "hmt-full", "perfil mínimo", "perfil completo"):
        require(forbidden not in joined, f"dicotomía APP espuria: {forbidden}")
    require(
        "convergen exactamente en la misma" not in joined,
        "igualdad escalar falsa entre las dos vías de alpha",
    )
    require(
        "\\left(1+\\frac{\\pi_{\\rm HMT}}{729}\\right)" in texts["synthesis_mass"],
        "la definición impresa de Delta_4 perdió el factor (1+pi/729)",
    )
    require(
        "Covariancia de las secciones de acción y gravedad" in texts["synthesis_g"],
        "falta la naturalidad dimensional de h y G en la síntesis",
    )
    require(
        "Independencia de carta de las secciones" in texts["integral_g"],
        "falta la naturalidad dimensional de h y G en el integral",
    )
    require(
        "Determinación diofántica del funcional de Barbero--Immirzi" in texts["integral_barbero"],
        "falta la derivación explícita de Barbero--Immirzi",
    )
    require(
        "10h_prueba_corredor_excepcional_rectificacion_probatoria_20260903" in
        (ROOT / "manuscrito/sucesor_102/parte_i_ii_1_26_rectificacion_probatoria_20260903.tex").read_text(encoding="utf-8"),
        "el corredor excepcional completo no está incorporado",
    )
    return {name: str(path) for name, path in files.items()}


def main() -> None:
    run_gate(ROOT / "pruebas/python/verificar_alpha_dos_vias.py")
    run_gate(ROOT / "pruebas/python/verificar_md_core.py")
    result = {
        "schema": "HMT.rectificacion_probatoria_autonoma.20260903.v1",
        "status": "PASS",
        "numerical": roots_and_electron(),
        "sources": structural_checks(),
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    print("PASS_RECTIFICACION_PROBATORIA_AUTONOMA_20260903")


if __name__ == "__main__":
    main()
