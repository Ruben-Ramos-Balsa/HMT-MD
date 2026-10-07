#!/usr/bin/env python3
"""Audita por profundidad el acarreo APP--TRIT--TPK del radion.

La construccion principal no recibe como entrada el valor del radion, ni un
epsilon publicado, ni una masa o constante externa.  Reconstruye los
cilindros coinductivos de pi y e con el generador certificado de las Nueve
Puertas y evalua dos secciones fijadas antes de la comparacion:

  * exceso electrico visible: fase C12 phi_2, A=1000*alpha y unidad APP;
  * flujo torsional: densidad two-way 180/729 y quantum Delta4.

El operador SubCarry_1000 resta sus palabras de triadas, conserva todos los
prestamos y toma el limite de los cilindros compatibles. El programa separa
esta formalizacion de dos afirmaciones mas fuertes que no se siguen de ella:

  * que el cociclo real sea funcion solamente del carry entero C108/C9;
  * que coincida con una cola espectral 90/120 preexistente.

Ambas afirmaciones se someten a controles negativos reproducibles.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_FLOOR, localcontext
from fractions import Fraction
import importlib.util
import json
from pathlib import Path


PREC = 240
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GENERATOR = ROOT / "certificados/ley_nueve_puertas_2026-07-30/generar_desde_estructura.py"
ALPHA_CERT = ROOT / "PUBLICACION_HMT/HOLOGRAFIA_MODULAR_TRIADICA/certificados/alpha_dos_vias.json"
CONTRA_CERT = ROOT / "PUBLICACION_HMT/HOLOGRAFIA_MODULAR_TRIADICA/certificados/contraangulo_regional.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("hmt_nine_gates", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se puede cargar {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decimal_fraction(value: Fraction, D: type[Decimal]) -> Decimal:
    return D(value.numerator) / D(value.denominator)


def prefixes(channel: dict[str, object]) -> list[int]:
    result: list[int] = []
    prefix = 0
    rows = channel["rows"]
    assert isinstance(rows, list)
    for row in rows:
        assert isinstance(row, dict)
        prefix = prefix * 729 + int(row["candidate_index"])
        result.append(prefix)
    return result


def cylinder(
    channel: dict[str, object], prefix_values: list[int], depth: int, D: type[Decimal]
) -> tuple[Decimal, Decimal]:
    integer_part = D(int(channel["integer_part"]))
    denominator = D(729) ** depth
    prefix = D(prefix_values[depth - 1])
    return integer_part + prefix / denominator, integer_part + (prefix + 1) / denominator


def fractional_triads(value: Decimal, depth: int) -> list[int]:
    """Primeras ``depth`` triadas de la parte fraccionaria, sin redondeo."""
    B = Decimal(1000)
    integer = value.to_integral_value(rounding=ROUND_FLOOR)
    scaled = ((value - integer) * (B**depth)).to_integral_value(rounding=ROUND_FLOOR)
    digits = f"{int(scaled):0{3 * depth}d}"
    return [int(digits[3 * index : 3 * index + 3]) for index in range(depth)]


def subtract_with_carry(
    left: list[int], right: list[int], terminal_carry: int = 0
) -> tuple[list[int], list[int]]:
    """Resta APP en base 1000, de derecha a izquierda, con carry explicito."""
    if len(left) != len(right):
        raise ValueError("Las palabras deben tener igual profundidad")
    B = 1000
    depth = len(left)
    output = [0] * depth
    carries = [0] * (depth + 1)
    carries[depth] = terminal_carry
    for index in range(depth - 1, -1, -1):
        raw = left[index] - right[index] + carries[index + 1]
        output[index] = raw % B
        carries[index] = (raw - output[index]) // B
        assert raw == output[index] + B * carries[index]
    return output, carries


def triad_word(values: list[int]) -> str:
    return "|".join(f"{value:03d}" for value in values)


def main() -> None:
    with localcontext() as ctx:
        ctx.prec = PREC
        D = Decimal
        one = D(1)

        # Salida previa certificada de la rueda dodecafasica; no se estima
        # con el radion ni se copia desde una tabla metrologica.
        alpha_record = json.loads(ALPHA_CERT.read_text(encoding="utf-8"))
        alpha = D(alpha_record["exact_alpha_carry"]["decimal"])
        assert alpha_record["status"] == "PASS"
        wheel_phase = 2
        phi_2_deg = D(30 * wheel_phase - 10)
        A_deg = D(1000) * alpha

        # Incidencias TPK: 6*C(6,2)=90 y su duplicacion two-way dentro de F3^6.
        hexad = 6
        incidence_90 = hexad * (hexad * (hexad - 1) // 2)
        ambient_729 = 3**6
        two_way_sheets = 2
        crossings_180 = two_way_sheets * incidence_90
        torsion_density = D(crossings_180) / D(ambient_729)
        assert incidence_90 == 90
        assert crossings_180 == 180
        assert torsion_density == D(20) / D(81)
        # Reduccion triadica exacta del coeficiente que multiplica el
        # numerador de Delta4.
        assert Fraction(20, 81 * 270) == Fraction(2, 3**7)
        torsion_kernel_density = D(2) / (D(3) ** 7)

        # Los coeficientes de la seccion visible se obtienen de la carta de vuelta.
        visible_fraction = phi_2_deg / D(360) + A_deg / D(360)
        assert visible_fraction == D(5) / D(36) + D(25) * alpha / D(9)

        gen = load_generator()
        selection = gen.select_structural_orbits()
        target_scale = 3 ** (gen.TOTAL_TRITS + gen.BOUND_GUARD_TRITS)
        pi_lo, pi_hi, _ = gen.closure_pi_bounds(
            len(selection["pi_regions"]), int(selection["companion_regions"]), target_scale
        )
        e_lo, e_hi, _ = gen.propagation_e_bounds(target_scale)
        pi_channel = gen.generate_gate_channel("pi", pi_lo, pi_hi)
        e_channel = gen.generate_gate_channel("e", e_lo, e_hi)
        pi_prefixes = prefixes(pi_channel)
        e_prefixes = prefixes(e_channel)

        def delta4(p: Decimal, e: Decimal) -> Decimal:
            return (p - e * p.ln()) / D(270) * (one + p / D(729))

        def section_visible(p: Decimal) -> Decimal:
            return D(2) * p * visible_fraction

        def electric_excess(p: Decimal) -> Decimal:
            # Exceso de la publicacion visible sobre la unidad conservada.
            return section_visible(p) - one

        def torsion_flux(p: Decimal, e: Decimal) -> Decimal:
            return torsion_density * delta4(p, e)

        def section_torsion(p: Decimal, e: Decimal) -> Decimal:
            return one + torsion_flux(p, e)

        def epsilon_candidate(p: Decimal, e: Decimal) -> Decimal:
            # Operandos upstream: flujo torsional menos exceso electrico.
            # La igualdad con 1+flujo-seccion es un teorema de cierre, no la
            # entrada numerica del operador de acarreo.
            result = torsion_flux(p, e) - electric_excess(p)
            assert abs(result - (section_torsion(p, e) - section_visible(p))) < D(10) ** (-(PREC - 10))
            return result

        # En 3<p<4, 2<e<3, ambas derivadas son negativas. Esto permite
        # transportar los cilindros racionales a intervalos certificados.
        derivative_p_upper = (
            -D(2) * visible_fraction
            + torsion_density
            / D(270)
            * (D("0.5") * (one + D(4) / D(729)) + D(4) / D(729))
        )
        derivative_e_upper = -torsion_density * D(3).ln() / D(270)
        assert derivative_p_upper < 0
        assert derivative_e_upper < 0

        depths = (1, 2, 3, 6, 9, 10, 18, 27, 36, 45)
        depth_rows: list[dict[str, object]] = []
        for depth in depths:
            p_lower, p_upper = cylinder(pi_channel, pi_prefixes, depth, D)
            e_lower, e_upper = cylinder(e_channel, e_prefixes, depth, D)
            eps_lower = epsilon_candidate(p_upper, e_upper)
            eps_upper = epsilon_candidate(p_lower, e_lower)
            eps_mid = epsilon_candidate(
                (p_lower + p_upper) / D(2), (e_lower + e_upper) / D(2)
            )
            phase = int(pi_channel["rows"][depth - 1]["phase9"])
            memory = (depth - 1) // 9
            depth_rows.append(
                {
                    "depth": depth,
                    "phase9": phase,
                    "memory": memory,
                    "epsilon_mid": eps_mid,
                    "epsilon_width": eps_upper - eps_lower,
                    "epsilon_lower": eps_lower,
                    "epsilon_upper": eps_upper,
                }
            )
            assert eps_lower <= eps_mid <= eps_upper

        # Valor limite evaluado desde los 396 bloques generados.
        p_text = D(f"{pi_channel['integer_part']}.{pi_channel['fractional_digits']}")
        e_text = D(f"{e_channel['integer_part']}.{e_channel['fractional_digits']}")
        epsilon_unit = epsilon_candidate(p_text, e_text)
        # Publicacion posterior en la carta de 360 marcas. No interviene en el selector.
        chart_scale = D(360) / (D(2) * p_text)
        epsilon_chart = chart_scale * epsilon_unit

        # Reduccion APP literal del numero: las dos secciones se publican en
        # triadas y su diferencia se obtiene por division euclidea, no por una
        # cifra de cierre suministrada. Se verifica estabilidad por profundidad.
        visible_limit = section_visible(p_text)
        torsion_limit = section_torsion(p_text, e_text)
        electric_excess_limit = electric_excess(p_text)
        torsion_flux_limit = torsion_flux(p_text, e_text)
        carry_rows: list[dict[str, object]] = []
        for triad_depth in (12, 18, 24, 30, 36):
            torsion_triads = fractional_triads(torsion_flux_limit, triad_depth)
            electric_triads = fractional_triads(electric_excess_limit, triad_depth)
            epsilon_triads, carries = subtract_with_carry(torsion_triads, electric_triads)
            # Con terminal 0, la identidad entera de telescopado es exacta.
            Bn = 1000**triad_depth
            left_integer = int("".join(f"{x:03d}" for x in torsion_triads))
            right_integer = int("".join(f"{x:03d}" for x in electric_triads))
            output_integer = int("".join(f"{x:03d}" for x in epsilon_triads))
            assert left_integer - right_integer - output_integer == Bn * carries[0]
            assert carries[0] == 0
            carry_rows.append(
                {
                    "depth": triad_depth,
                    "epsilon_prefix": triad_word(epsilon_triads[:12]),
                    "carry_prefix": ",".join(str(value) for value in carries[:13]),
                }
            )

        expected_prefix = fractional_triads(epsilon_unit, 12)
        for row in carry_rows:
            assert row["epsilon_prefix"] == triad_word(expected_prefix)

        # Cada vuelta nonadica conserva la fase y aumenta una unidad la
        # memoria. Los cilindros fuente tienen diametro 729^-N; por tanto el
        # salto N -> N+9 contrae exactamente ese diametro por 3^-54.
        source_turn_contraction = D(729) ** (-9)
        assert source_turn_contraction == D(3) ** (-54)
        return_rows = [row for row in depth_rows if int(row["depth"]) % 9 == 0]
        return_width_ratios: list[Decimal] = []
        for previous, current in zip(return_rows, return_rows[1:]):
            return_width_ratios.append(
                D(current["epsilon_width"]) / D(previous["epsilon_width"])
            )

        # Hoja two-way J_alpha: involucion exacta a toda profundidad.
        turn_plus = D(2) * p_text
        turn_minus = alpha**2 / turn_plus
        assert turn_plus * turn_minus == alpha**2
        assert alpha**2 / turn_minus == turn_plus

        # La cuadratica P9 finita se audita aparte: su raiz no es exactamente
        # la seccion coinductiva, aunque coinciden a muchas cifras.
        delta_nonad = (D(10) / D(9)).ln() / D(10).ln()
        B9 = (
            delta_nonad
            + D(7) * alpha**2 / D(4)
            - alpha**4 / D(20)
            + D(2) * alpha**5 / D(21)
            + alpha**6 / D(46)
            + alpha**7 / D(120)
            - alpha**8 / D(45)
            - D(2) * alpha**9 / D(495)
        )
        disc = B9**2 - D(4) * alpha**4
        finite_turn = (B9 + disc.sqrt()) / (D(2) * alpha)
        finite_gap = finite_turn - turn_plus

        # Contraangulo: salida previa certificada, nunca escogida con epsilon.
        contra = json.loads(CONTRA_CERT.read_text(encoding="utf-8"))
        Cstar_deg = D(contra["values"]["C_degrees"])

        def split_mode(n: int) -> Decimal:
            q_minus_n = (-(D(n) * turn_plus * (A_deg - Cstar_deg) / D(360))).exp()
            q_plus_n = (-(D(n) * turn_plus * (A_deg + Cstar_deg) / D(360))).exp()
            return q_minus_n - q_plus_n

        m3 = split_mode(180) / D(24) - split_mode(240) / D(54) - D(24) * split_mode(360)
        m4 = m3 + D(7) * split_mode(420) / D(6)
        epsilon_m3 = torsion_density * m3
        epsilon_m4 = torsion_density * m4

        # Cola alta post-C12: se mantiene como objeto distinto.
        h = Cstar_deg / D(6)
        qh_minus = (-(p_text / D(180)) * (A_deg - h)).exp()
        qh_plus = (-(p_text / D(180)) * (A_deg + h)).exp()
        tail = D(0)
        cutoff = D(10) ** (-(PREC - 30))
        for j in range(2, 10000):
            jj = D(j)
            term = (
                (qh_minus ** (90 * j) - qh_plus ** (90 * j))
                - (qh_minus ** (120 * j) - qh_plus ** (120 * j))
            ) / jj
            tail += term
            if abs(term) < cutoff:
                break
        else:
            raise RuntimeError("La cola post-C12 no converge al umbral")
        tail_unit = D(6) * tail

        # Ablaciones de operadores seleccionados antes de conocer la salida.
        epsilon_one_sheet = (
            one + D(incidence_90) / D(ambient_729) * delta4(p_text, e_text)
            - section_visible(p_text)
        )
        phase1_fraction = D(30 * 1 - 10) / D(360) + A_deg / D(360)
        phase3_fraction = D(30 * 3 - 10) / D(360) + A_deg / D(360)
        epsilon_phase1 = section_torsion(p_text, e_text) - D(2) * p_text * phase1_fraction
        epsilon_phase3 = section_torsion(p_text, e_text) - D(2) * p_text * phase3_fraction
        epsilon_no_e = (
            one
            + torsion_density
            * ((p_text - p_text.ln()) / D(270) * (one + p_text / D(729)))
            - section_visible(p_text)
        )

        # Torsion historica A-C*: control de tipo, no sustituto de Delta4 vigente.
        delta4_ac = (
            ((A_deg - Cstar_deg) * p_text / D(180))
            / (D(9) * D(90))
            * (one - D(7) * p_text / (D(12) * D(729)))
        )
        epsilon_delta4_ac = one + torsion_density * delta4_ac - section_visible(p_text)

        print("PASS_CALCULO_OPERADOR_TPK_TARGET_FREE_POR_PROFUNDIDAD")
        print(f"generator={GENERATOR}")
        print(f"alpha={alpha}")
        print(f"phi_2_deg={phi_2_deg}")
        print(f"incidence_90={incidence_90}")
        print(f"two_way_crossings={crossings_180}")
        print(f"ambient={ambient_729}")
        print(f"torsion_density={torsion_density}")
        print(f"torsion_kernel_density={torsion_kernel_density}")
        print(f"source_turn_contraction_3^-54={source_turn_contraction}")
        print("depth,phase9,memory,epsilon_mid,epsilon_width")
        for row in depth_rows:
            print(
                f"{row['depth']},{row['phase9']},{row['memory']},"
                f"{row['epsilon_mid']},{row['epsilon_width']}"
            )
        print(f"epsilon_unit_limit={epsilon_unit}")
        print(f"epsilon_chart_360={epsilon_chart}")
        print(f"section_torsion={torsion_limit}")
        print(f"section_visible={visible_limit}")
        print(f"torsion_flux={torsion_flux_limit}")
        print(f"electric_excess={electric_excess_limit}")
        print(
            "torsion_flux_triads_12="
            + triad_word(fractional_triads(torsion_flux_limit, 12))
        )
        print(
            "electric_excess_triads_12="
            + triad_word(fractional_triads(electric_excess_limit, 12))
        )
        print("triad_depth,epsilon_prefix_12,carry_prefix_13")
        for row in carry_rows:
            print(f"{row['depth']},{row['epsilon_prefix']},{row['carry_prefix']}")
        print("return_width_ratios=" + ",".join(str(x) for x in return_width_ratios))
        print(f"turn_plus={turn_plus}")
        print(f"turn_minus={turn_minus}")
        print(f"J_product_error={turn_plus * turn_minus - alpha**2}")
        print(f"finite_P9_turn_minus_coinductive_turn={finite_gap}")
        print(f"M3={m3}")
        print(f"M4={m4}")
        print(f"epsilon_M3_unit={epsilon_m3}")
        print(f"epsilon_M4_unit={epsilon_m4}")
        print(f"epsilon_M4_minus_candidate={epsilon_m4 - epsilon_unit}")
        print(f"post_C12_tail_unit={tail_unit}")
        print(f"post_C12_tail_minus_candidate={tail_unit - epsilon_unit}")
        print(f"ablation_one_sheet={epsilon_one_sheet}")
        print(f"ablation_phase1={epsilon_phase1}")
        print(f"ablation_phase3={epsilon_phase3}")
        print(f"ablation_no_e_channel={epsilon_no_e}")
        print(f"ablation_Delta4_AC={epsilon_delta4_ac}")

        # Los dos candidatos espectrales quedan falsados como igualdades exactas.
        assert epsilon_m4 != epsilon_unit
        assert tail_unit != epsilon_unit
        assert epsilon_one_sheet != epsilon_unit
        assert epsilon_phase1 != epsilon_unit
        assert epsilon_phase3 != epsilon_unit
        assert epsilon_no_e != epsilon_unit
        assert epsilon_delta4_ac != epsilon_unit


if __name__ == "__main__":
    main()
