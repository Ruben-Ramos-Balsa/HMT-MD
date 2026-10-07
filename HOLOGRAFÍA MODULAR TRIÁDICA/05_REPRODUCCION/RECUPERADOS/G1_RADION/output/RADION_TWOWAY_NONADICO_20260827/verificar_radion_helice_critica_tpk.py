#!/usr/bin/env python3
"""Certifica la lectura helicoidal y el cierre interno del radion HMT.

El programa mantiene separados cuatro enunciados:

1. La coordenada critica 1/2 y la fase dodecafasica theta_2 publican 50
   en la carta arquimediana de una cara 10^2.
2. La fase nonadica retorna cada nueve niveles mientras el cilindro y la
   memoria se refinan: el objeto levantado no es un circulo plano.
3. Dos evaluaciones aguas arriba del mismo estado producen un elemento de
   transicion real

       epsilon = Phi_T - rem_1(S_E).

   Esta es una diferencia canonica de secciones. No se usa como entrada el
   decimal de epsilon, 180/pi ni una tabla metrologica.
4. El jet P9 define una vuelta two-way finita muy proxima a 2*pi, pero no es
   identica a la seccion coinductiva. El cierre exacto usa pi y e generados
   por la conexion nonadica; P9 se conserva como control, no como sustituto.

La identidad algebraica final no se presenta como una segunda prediccion de
pi: certifica que el elemento de transicion generado por las dos secciones
es exactamente el que cierra su diagrama.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_FLOOR, localcontext
from fractions import Fraction
import importlib.util
import json
from pathlib import Path


PREC = 260
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RECTOR = PROJECT / "referencia_integral"
GENERATOR = PROJECT / "certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py"
PI_DIGITS = PROJECT / "certificados/ley_nueve_puertas_2026-07-30/salidas/pi_1000_decimales.txt"
E_DIGITS = PROJECT / "certificados/ley_nueve_puertas_2026-07-30/salidas/e_1000_decimales.txt"
ALPHA_T1_DIGITS = (
    RECTOR
    / "manuscrito/generated/decimals_10000_rev9/alpha_T1_10000_decimales_96col.txt"
)
ALPHA_CERT = PROJECT / "PUBLICACION_HMT/HOLOGRAFIA_MODULAR_TRIADICA/certificados/alpha_dos_vias.json"


def read_decimal_prefix(path: Path, digits: int) -> Decimal:
    text = "".join(path.read_text(encoding="utf-8").split())
    if "." not in text:
        raise ValueError(f"No hay separador decimal en {path}")
    integer, fractional = text.split(".", 1)
    return Decimal(integer + "." + fractional[:digits])


def load_generator():
    spec = importlib.util.spec_from_file_location("hmt_nine_gates_radion", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se puede cargar {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prefixes(channel: dict[str, object]) -> list[int]:
    output: list[int] = []
    prefix = 0
    rows = channel["rows"]
    assert isinstance(rows, list)
    for row in rows:
        assert isinstance(row, dict)
        prefix = prefix * 729 + int(row["candidate_index"])
        output.append(prefix)
    return output


def cylinder(
    channel: dict[str, object], values: list[int], depth: int
) -> tuple[Decimal, Decimal]:
    integer = Decimal(int(channel["integer_part"]))
    denominator = Decimal(729) ** depth
    prefix = Decimal(values[depth - 1])
    return integer + prefix / denominator, integer + (prefix + 1) / denominator


def triads(value: Decimal, depth: int) -> str:
    base = Decimal(1000)
    integer = value.to_integral_value(rounding=ROUND_FLOOR)
    scaled = ((value - integer) * base**depth).to_integral_value(rounding=ROUND_FLOOR)
    digits = f"{int(scaled):0{3 * depth}d}"
    return "|".join(digits[index : index + 3] for index in range(0, len(digits), 3))


def main() -> None:
    with localcontext() as ctx:
        ctx.prec = PREC
        D = Decimal
        one = D(1)

        # Cara arquimediana (10^2) y volumen de publicacion (10^3).
        critical_coordinate = Fraction(1, 2)
        face_scale = 10**2
        volume_scale = 10**3
        critical_mark = Fraction(face_scale) * critical_coordinate
        theta = {m: 30 * m - 10 for m in range(1, 13)}
        equalizer_phases = [m for m, angle in theta.items() if Fraction(angle) == critical_mark]
        assert critical_mark == 50
        assert equalizer_phases == [2]
        assert 1000 == 729 + 243 + 27 + 1

        # Perfil finito y perfil coinductivo: nunca se mezclan sus colas.
        alpha_record = json.loads(ALPHA_CERT.read_text(encoding="utf-8"))
        alpha_12 = D(alpha_record["exact_alpha_carry"]["decimal"])
        alpha_inf = read_decimal_prefix(ALPHA_T1_DIGITS, PREC - 30)
        pi_hmt = read_decimal_prefix(PI_DIGITS, PREC - 30)
        e_hmt = read_decimal_prefix(E_DIGITS, PREC - 30)

        incidence_90 = 6 * (6 * 5 // 2)
        two_way_crossings = 2 * incidence_90
        ambient = 3**6
        rho = D(two_way_crossings) / D(ambient)
        assert incidence_90 == 90
        assert two_way_crossings == 180
        assert Fraction(two_way_crossings, ambient) == Fraction(20, 81)

        def delta4(p: Decimal, e_value: Decimal) -> Decimal:
            return (p - e_value * p.ln()) / D(270) * (one + p / D(729))

        def section_electric(p: Decimal, alpha: Decimal) -> Decimal:
            return D(2) * p * (D(5) / D(36) + D(25) * alpha / D(9))

        def transition(p: Decimal, e_value: Decimal, alpha: Decimal) -> tuple[Decimal, ...]:
            s_e = section_electric(p, alpha)
            quotient = s_e.to_integral_value(rounding=ROUND_FLOOR)
            assert quotient == 1
            d_e = s_e - quotient
            phi_t = rho * delta4(p, e_value)
            epsilon = phi_t - d_e
            return s_e, quotient, d_e, phi_t, epsilon

        rows: dict[str, dict[str, Decimal]] = {}
        for profile, alpha in (("alpha_12", alpha_12), ("alpha_infty", alpha_inf)):
            s_e, quotient, d_e, phi_t, epsilon = transition(pi_hmt, e_hmt, alpha)
            turn = D(2) * pi_hmt
            # El cociente 1 pertenece a la division APP por la unidad radial.
            # No es un numero de vueltas: la vuelta angular completa mide 2*pi.
            assert one < s_e < D(2) < turn
            radion_deg = D(360) / turn
            epsilon_deg = radion_deg * epsilon
            delta4_deg = radion_deg * delta4(pi_hmt, e_hmt)
            direct_deg = D(50) + D(volume_scale) * alpha
            torsion_correction_deg = rho * delta4_deg
            after_torsion_deg = direct_deg - torsion_correction_deg
            closure_unit = s_e - phi_t + epsilon - one
            closure_deg = (
                direct_deg
                - torsion_correction_deg
                + epsilon_deg
                - radion_deg
            )
            assert closure_unit == 0
            assert abs(closure_deg) < D(10) ** (-(PREC - 20))
            rows[profile] = {
                "alpha": alpha,
                "section_electric": s_e,
                "quotient": quotient,
                "electric_remainder": d_e,
                "torsion_flux": phi_t,
                "epsilon_unit": epsilon,
                "epsilon_deg": epsilon_deg,
                "radion_deg": radion_deg,
                "direct_deg": direct_deg,
                "torsion_correction_deg": torsion_correction_deg,
                "after_torsion_deg": after_torsion_deg,
                "closure_unit": closure_unit,
                "closure_deg": closure_deg,
            }

        # La conexion nonadica proporciona cilindros anidados. En los niveles
        # 9k la fase observable coincide y la memoria vertical aumenta.
        gen = load_generator()
        selection = gen.select_structural_orbits()
        target_scale = 3 ** (gen.TOTAL_TRITS + gen.BOUND_GUARD_TRITS)
        pi_lo, pi_hi, _ = gen.closure_pi_bounds(
            len(selection["pi_regions"]), int(selection["companion_regions"]), target_scale
        )
        e_lo, e_hi, _ = gen.propagation_e_bounds(target_scale)
        pi_channel = gen.generate_gate_channel("pi", pi_lo, pi_hi)
        e_channel = gen.generate_gate_channel("e", e_lo, e_hi)
        pi_pref = prefixes(pi_channel)
        e_pref = prefixes(e_channel)

        def epsilon_value(p: Decimal, e_value: Decimal) -> Decimal:
            return transition(p, e_value, alpha_inf)[-1]

        helix_rows: list[tuple[int, int, int, Decimal, Decimal]] = []
        for depth in (9, 18, 27, 36, 45):
            p_lower, p_upper = cylinder(pi_channel, pi_pref, depth)
            e_lower, e_upper = cylinder(e_channel, e_pref, depth)
            # En 3<p<4 y 2<e<3 el funcional decrece en ambas variables.
            lower = epsilon_value(p_upper, e_upper)
            upper = epsilon_value(p_lower, e_lower)
            middle = epsilon_value(
                (p_lower + p_upper) / D(2), (e_lower + e_upper) / D(2)
            )
            assert lower <= middle <= upper
            row = pi_channel["rows"][depth - 1]
            assert isinstance(row, dict)
            phase = int(row["phase9"])
            memory = (depth - 1) // 9
            helix_rows.append((depth, phase, memory, middle, upper - lower))

        assert len({row[1] for row in helix_rows}) == 1
        assert [row[2] for row in helix_rows] == [0, 1, 2, 3, 4]
        source_contraction = D(729) ** (-9)
        assert source_contraction == D(3) ** (-54)

        # Jet nonadico P9: genera una pareja two-way exacta relativa a su
        # polinomio, pero se audita contra la vuelta coinductiva y no se funde.
        alpha = alpha_inf
        vacancy = (D(10) / D(9)).ln() / D(10).ln()
        b9 = (
            vacancy
            + D(7) * alpha**2 / D(4)
            - alpha**4 / D(20)
            + D(2) * alpha**5 / D(21)
            + alpha**6 / D(46)
            + alpha**7 / D(120)
            - alpha**8 / D(45)
            - D(2) * alpha**9 / D(495)
        )
        discriminant = b9**2 - D(4) * alpha**4
        t9_plus = (b9 + discriminant.sqrt()) / (D(2) * alpha)
        t9_minus = alpha**2 / t9_plus
        assert t9_plus * t9_minus == alpha**2
        t_coinductive = D(2) * pi_hmt
        t9_gap = t9_plus - t_coinductive
        assert t9_gap != 0

        active = rows["alpha_infty"]
        finite = rows["alpha_12"]
        print("PASS_RADION_HELICE_CRITICA_TPK")
        print(f"critical_coordinate={critical_coordinate}")
        print(f"critical_face_scale={face_scale}")
        print(f"critical_mark_deg={critical_mark}")
        print(f"theta_equalizer_phase={equalizer_phases[0]}")
        print(f"theta_2_deg={theta[2]}")
        print(f"alpha_12={alpha_12}")
        print(f"alpha_infty={alpha_inf}")
        print(f"alpha_boundary_difference={alpha_12-alpha_inf}")
        print(f"incidence_90={incidence_90}")
        print(f"two_way_crossings={two_way_crossings}")
        print(f"ambient_729={ambient}")
        print(f"rho={rho}")
        print(f"full_turn_rad=2*pi_HMT={D(2)*pi_hmt}")
        print("radion_target_rad=1")
        print(f"radion_deg=360/(2*pi_HMT)={active['radion_deg']}")
        print(f"direct_50_plus_A_deg={active['direct_deg']}")
        print(f"torsion_correction_20_over_81_Delta4_deg={active['torsion_correction_deg']}")
        print(f"after_torsion_deg={active['after_torsion_deg']}")
        print(f"electric_section={active['section_electric']}")
        print(f"electric_quotient={active['quotient']}")
        print(f"electric_remainder={active['electric_remainder']}")
        print(f"torsion_flux={active['torsion_flux']}")
        print(f"epsilon_unit_alpha_infty={active['epsilon_unit']}")
        print(f"epsilon_deg_alpha_infty={active['epsilon_deg']}")
        print(f"epsilon_deg_alpha_12={finite['epsilon_deg']}")
        print(f"profile_difference_deg={active['epsilon_deg']-finite['epsilon_deg']}")
        print(f"epsilon_triads={triads(active['epsilon_unit'], 16)}")
        print(f"closure_unit_alpha_infty={active['closure_unit']}")
        print(f"closure_deg_alpha_infty={active['closure_deg']}")
        print(f"source_contraction_per_return_3^-54={source_contraction}")
        print("depth,phase9,memory,epsilon_mid,certified_width,increment_from_previous_return")
        previous: Decimal | None = None
        for depth, phase, memory, middle, width in helix_rows:
            increment = D(0) if previous is None else middle - previous
            print(f"{depth},{phase},{memory},{middle},{width},{increment}")
            previous = middle
        print(f"T9_plus={t9_plus}")
        print(f"T9_minus={t9_minus}")
        print(f"T9_product_minus_alpha2={t9_plus*t9_minus-alpha**2}")
        print(f"T_coinductive={t_coinductive}")
        print(f"T9_minus_Tcoinductive={t9_gap}")
        print("target_epsilon_used=False")
        print("target_180_over_pi_used=False")
        print("classification=canonical_transition_of_two_upstream_sections")
        print("electric_integer_quotient_is_winding_number=False")
        print("angular_cover_period_is_2pi=True")
        print("helix_role=preserves_return_memory_and_refinement_not_numeric_addition")
        print("local_C108_carry_alone_generates_epsilon=False")
        print("P9_equals_coinductive_pi=False")


if __name__ == "__main__":
    main()
