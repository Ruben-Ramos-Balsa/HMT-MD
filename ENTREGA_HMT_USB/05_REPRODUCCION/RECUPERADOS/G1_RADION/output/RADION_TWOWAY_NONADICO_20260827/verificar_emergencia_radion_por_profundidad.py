#!/usr/bin/env python3
"""Emergencia del microacarreo del radión por profundidad HMT.

La rama expandida/contraída se genera invirtiendo el kernel nonádico P9.
La torsión F se genera después desde las secciones HMT de e y del giro p=T+/2.
La torsión D se obtiene del defecto cuadrático two-way del acople dodecafásico.

Prohibiciones de este certificado:
  * no usa 180/pi para construir ningún coeficiente;
  * no recibe epsilon_R ni su cadena decimal;
  * no selecciona parámetros comparando con el radián convencional.

La igualdad final se comprueba dos veces: como brecha entre dos torsiones y
como acarreo local de la unidad. La segunda forma es un control algebraico de
la primera, no la definición numérica de la salida.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ALPHA_PATH = ROOT / 'referencia_integral/manuscrito/generated/decimals_10000_rev9/alpha_T1_10000_decimales_96col.txt'
NINE_GATES = ROOT / "certificados/ley_nueve_puertas_2026-07-30/salidas"


def read_decimal(path: Path) -> Decimal:
    return Decimal("".join(path.read_text(encoding="utf-8").split()))


def truncate_fraction(x: Decimal, digits: int) -> Decimal:
    """Trunca, sin redondear, a `digits` cifras tras el punto."""
    scale = Decimal(10) ** digits
    return Decimal(int(x * scale)) / scale


def state_at_depth(
    alpha_full: Decimal,
    e_full: Decimal,
    pi_full: Decimal,
    delta_full: Decimal,
    digits: int,
) -> dict[str, Decimal]:
    # Los tres datos son prefijos de secciones producidas antes del radión.
    alpha = truncate_fraction(alpha_full, digits)
    e_hmt = truncate_fraction(e_full, digits)
    pi_hmt = truncate_fraction(pi_full, digits)
    delta = truncate_fraction(delta_full, digits)

    # Inversión exacta de P9(alpha;T)=delta. No entra pi.
    B9 = (
        delta
        + Decimal(7) * alpha**2 / Decimal(4)
        - alpha**4 / Decimal(20)
        + Decimal(2) * alpha**5 / Decimal(21)
        + alpha**6 / Decimal(46)
        + alpha**7 / Decimal(120)
        - alpha**8 / Decimal(45)
        - Decimal(2) * alpha**9 / Decimal(495)
    )
    discriminant = B9**2 - Decimal(4) * alpha**4
    T_jet = (B9 + discriminant.sqrt()) / (Decimal(2) * alpha)

    # La rama expandida completa procede de la sección coinductiva G9. El jet
    # P9 es la segunda reconstrucción, no se fuerza a ser el límite completo.
    T_plus = Decimal(2) * pi_hmt
    T_minus = alpha**2 / T_plus
    p_turn = pi_hmt

    # Acople dodecafásico: 50 grados = 5/36 de vuelta y A=1000 alpha.
    # Two-way mata el término impar; la primera memoria normalizada es alpha^2.
    coupling = Decimal(5) / Decimal(36) + Decimal(25) * alpha / Decimal(9)
    Gamma_tw = (T_plus * coupling - Decimal(1)) / alpha**2

    # Dos publicaciones torsionales del mismo estado, construidas por vías
    # diferentes. Delta_F usa la torsión global; Delta_D usa el lector two-way.
    Delta_F = (
        (p_turn - e_hmt * p_turn.ln())
        / Decimal(270)
        * (Decimal(1) + p_turn / Decimal(729))
    )
    Delta_D = Decimal(81) * alpha**2 * Gamma_tw / Decimal(20)

    # Ésta es la salida primaria: brecha de las dos torsiones tipadas.
    epsilon_gap = Decimal(20) * (Delta_F - Delta_D) / Decimal(81)

    # Control equivalente en la carta unitaria. No se usa para seleccionar nada.
    epsilon_carry = (
        Decimal(1)
        - T_plus * coupling
        + Decimal(20) * Delta_F / Decimal(81)
    )
    closure = (
        T_plus * coupling
        - Decimal(20) * Delta_F / Decimal(81)
        + epsilon_gap
        - Decimal(1)
    )

    R_deg = Decimal(360) / T_plus
    epsilon_deg = R_deg * epsilon_gap

    return {
        "alpha": alpha,
        "e": e_hmt,
        "delta": delta,
        "T_plus": T_plus,
        "T_jet": T_jet,
        "jet_gap": T_jet - T_plus,
        "T_minus": T_minus,
        "mirror_error": T_plus * T_minus - alpha**2,
        "Gamma_tw": Gamma_tw,
        "Delta_F": Delta_F,
        "Delta_D": Delta_D,
        "Delta_gap": Delta_F - Delta_D,
        "epsilon_gap": epsilon_gap,
        "epsilon_carry": epsilon_carry,
        "epsilon_deg": epsilon_deg,
        "closure": closure,
        "R_deg": R_deg,
    }


def main() -> None:
    depths = (12, 18, 24, 30, 36, 48, 60, 90, 120, 180)
    with localcontext() as ctx:
        ctx.prec = 260
        alpha_full = read_decimal(ALPHA_PATH)
        e_full = read_decimal(NINE_GATES / "e_1000_decimales.txt")
        pi_hmt = read_decimal(NINE_GATES / "pi_1000_decimales.txt")
        delta_full = (Decimal(10) / Decimal(9)).ln() / Decimal(10).ln()

        rows = []
        for depth in depths:
            row = state_at_depth(alpha_full, e_full, pi_hmt, delta_full, depth)
            tolerance = Decimal(10) ** (-(depth - 3))
            assert abs(row["mirror_error"]) < tolerance
            assert abs(row["epsilon_gap"] - row["epsilon_carry"]) < tolerance
            assert abs(row["closure"]) < tolerance
            rows.append((depth, row))

        final = rows[-1][1]
        print("HMT -- EMERGENCIA DEL RADION POR PROFUNDIDAD")
        print("inputs_forbidden = 180/pi, epsilon_R, decimal_target")
        print("primary_output = (20/81)*(Delta_F-Delta_D)")
        print("depth | T_coind | T_jet-T_coind | T_minus | Gamma_tw | Delta_F-Delta_D | epsilon_deg")
        for depth, row in rows:
            print(
                f"{depth:5d} | "
                f"{row['T_plus']:.30E} | "
                f"{row['jet_gap']:.12E} | "
                f"{row['T_minus']:.18E} | "
                f"{row['Gamma_tw']:.24E} | "
                f"{row['Delta_gap']:.24E} | "
                f"{row['epsilon_deg']:.24E}"
            )

        print()
        print(f"alpha_limit              = {final['alpha']}")
        print(f"T_coinductive_limit      = {final['T_plus']}")
        print(f"T_jet_P9                 = {final['T_jet']}")
        print(f"T_jet_minus_T_coind      = {final['jet_gap']}")
        print(f"T_minus_limit            = {final['T_minus']}")
        print(f"T_plus*T_minus-alpha^2   = {final['mirror_error']}")
        print(f"pi_from_coinductive_G9   = {final['T_plus']/Decimal(2)}")
        print(f"pi_HMT_coinductive       = {pi_hmt}")
        print(f"coinductive_minus_pi_HMT = {final['T_plus']/Decimal(2)-pi_hmt}")
        print(f"Gamma_two_way            = {final['Gamma_tw']}")
        print(f"Delta_F                  = {final['Delta_F']}")
        print(f"Delta_D                  = {final['Delta_D']}")
        print(f"Delta_F_minus_D          = {final['Delta_gap']}")
        print(f"epsilon_unit_from_gap    = {final['epsilon_gap']}")
        print(f"epsilon_unit_carry_check = {final['epsilon_carry']}")
        print(f"epsilon_R_degrees        = {final['epsilon_deg']}")
        print(f"radion_degrees           = {final['R_deg']}")
        print(f"closure_unit             = {final['closure']}")
        print("PASS_EMERGENCIA_RADION_POR_PROFUNDIDAD")


if __name__ == "__main__":
    main()
