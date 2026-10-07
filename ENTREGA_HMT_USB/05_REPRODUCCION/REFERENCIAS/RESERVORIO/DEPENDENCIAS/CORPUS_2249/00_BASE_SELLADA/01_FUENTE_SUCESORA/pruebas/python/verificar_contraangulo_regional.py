"""Certifica la realizacion analitica graduada de la microfibra de pi.

El programa separa tres capas:

1. hechos finitos obtenidos por enumeracion del catalogo TPK;
2. reglas declaradas del lector analitico graduado;
3. consecuencias analiticas y controles numericos.

El valor publicado del contraangulo se usa solo al final como contraste. No
interviene como argumento de ``realizacion_analitica``.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
import sys

# Dependencia vendorizada para reproducción bajo ``python -I -S``.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mpmath as mp
ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / 'datos/TPK_U_catalog_468.json'
ALPHA_CERTIFICATE = ROOT / 'certificados/alpha_dos_vias.json'
OUTPUT = ROOT / 'certificados/contraangulo_regional.json'
mp.mp.dps = 100
ALPHA = mp.mpf(json.loads(ALPHA_CERTIFICATE.read_text(encoding='utf-8'))['exact_alpha_carry']['decimal'])
C_PUBLICADO = mp.mpf('2.123738338968646')
H_SI_MANTISSA = mp.mpf('6.62607015')

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def parse_u6(value: str) -> tuple[int, ...]:
    return tuple((int(part) for part in value.split('|')))

def psi(u6: tuple[int, ...]) -> str:
    return ''.join((str(-value % 3) for value in u6))

def singleton_coordinate(block: tuple[int, int, int]) -> int:
    """Devuelve la coordenada de multiplicidad uno de un bloque (a,b,b)."""
    counts = Counter(block)
    singletons = [value for (value, multiplicity) in counts.items() if multiplicity == 1]
    doubles = [value for (value, multiplicity) in counts.items() if multiplicity == 2]
    if len(singletons) != 1 or len(doubles) != 1:
        raise AssertionError(f'el bloque no tiene tipo (a,b,b): {block!r}')
    return singletons[0]

def modal_return(regions: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, int, int], int]:
    returns = Counter((tuple(region[3:]) for region in regions))
    maximum = max(returns.values())
    modes = [block for (block, multiplicity) in returns.items() if multiplicity == maximum]
    if len(modes) != 1:
        raise AssertionError('el bloque terminal modal no es unico')
    return (modes[0], maximum)

def round_decimal(value: mp.mpf, places: int) -> mp.mpf:
    scale = mp.mpf(10) ** places
    return mp.floor(value * scale + mp.mpf('0.5')) / scale

def nstr(value: mp.mpf, digits: int=80) -> str:
    return mp.nstr(value, digits)

def realizacion_analitica(alpha: mp.mpf, selector: int=169) -> dict[str, mp.mpf]:
    """Evalua el lector sin recibir C*, hbar, Barbero ni un dato SI."""
    phi = (1 + mp.sqrt(5)) / 2
    angle_A = 1000 * alpha
    x = mp.pi * angle_A / 180
    determinant_A = mp.exp(-2 * x)
    action_jet_5 = mp.mpf(1) / 2 * mp.sqrt(1000 * alpha / phi) - alpha + mp.mpf(9) / 16 * alpha ** 2 - mp.mpf(5) / 9 * alpha ** 3 + mp.mpf(7) / 48 * alpha ** 4 - mp.mpf(1) / 54 * alpha ** 5
    return_impulse = selector * alpha ** 6
    determinant_tail = determinant_A * alpha ** 7 / (1 - determinant_A * alpha)
    regional_character = return_impulse + determinant_tail
    y = mp.pi / 90 * (action_jet_5 + alpha) - regional_character
    contraangle = 180 / mp.pi * y
    reduced_action_after_return = contraangle / 2 - alpha
    q_minus = mp.exp(-x + y)
    q_plus = mp.exp(-x - y)

    def moment_90(q: mp.mpf) -> mp.mpf:
        return q ** 90 / (1 - q ** 270)

    def moment_120(q: mp.mpf) -> mp.mpf:
        return q ** 120 / (1 - q ** 360)
    transition_6_to_8 = 12 * (moment_90(q_minus) - moment_90(q_plus))
    transition_6_to_8 -= moment_120(q_minus) - moment_120(q_plus)
    barbero_hmt = 180 / mp.pi * x * y + transition_6_to_8
    return {'phi': phi, 'A_degrees': angle_A, 'x_radians': x, 'D_A': determinant_A, 'H5': action_jet_5, 'return_impulse': return_impulse, 'determinant_tail': determinant_tail, 'regional_character': regional_character, 'y_radians': y, 'C_degrees': contraangle, 'q_minus': q_minus, 'q_plus': q_plus, 'barbero_base': 180 / mp.pi * x * y, 'barbero_transition_6_to_8': transition_6_to_8, 'barbero_HMT': barbero_hmt, 'hbar_reduced_after_return': reduced_action_after_return, 'h_pre_return_mantissa': 2 * mp.pi * action_jet_5, 'h_post_return_mantissa': 2 * mp.pi * reduced_action_after_return}

def main() -> None:
    catalogue = json.loads(CATALOG.read_text(encoding='utf-8'))
    pi_regions = tuple((parse_u6(item['U6']) for item in catalogue if psi(parse_u6(item['U6'])) == '010211'))
    expected_regions = {(501, 614, 498, 169, 272, 272), (810, 923, 870, 169, 272, 272), (810, 983, 810, 169, 272, 272), (870, 923, 810, 169, 272, 272), (870, 923, 810, 418, 674, 521)}
    if not len(pi_regions) == 5:
        raise AssertionError('comprobación ejecutable fallida')
    if not set(pi_regions) == expected_regions:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((len(region) == 6 for region in pi_regions)):
        raise AssertionError('comprobación ejecutable fallida')
    (block, block_multiplicity) = modal_return(pi_regions)
    selector = singleton_coordinate(block)
    if not block == (169, 272, 272):
        raise AssertionError('comprobación ejecutable fallida')
    if not block_multiplicity == 4:
        raise AssertionError('comprobación ejecutable fallida')
    if not selector == 169:
        raise AssertionError('comprobación ejecutable fallida')
    all_words = tuple((parse_u6(item['U6']) for item in catalogue))
    selector_position_counts = tuple((sum((word[position] == selector for word in all_words)) for position in range(6)))
    if not selector_position_counts == (14, 14, 14, 14, 14, 14):
        raise AssertionError('comprobación ejecutable fallida')
    if not sum(selector_position_counts) == 84:
        raise AssertionError('comprobación ejecutable fallida')
    mutated_block = next((terminal for terminal in (tuple(region[3:]) for region in pi_regions) if terminal != block))
    terminal_defect = tuple((b - a for (a, b) in zip(block, mutated_block)))
    if not mutated_block == (418, 674, 521):
        raise AssertionError('comprobación ejecutable fallida')
    if not terminal_defect == (249, 402, 249):
        raise AssertionError('comprobación ejecutable fallida')
    if not sum(terminal_defect) == 900:
        raise AssertionError('comprobación ejecutable fallida')
    for branch_permutation in itertools.permutations(pi_regions):
        (permuted_block, multiplicity) = modal_return(branch_permutation)
        if not permuted_block == block:
            raise AssertionError('comprobación ejecutable fallida')
        if not multiplicity == 4:
            raise AssertionError('comprobación ejecutable fallida')
    for coordinate_permutation in itertools.permutations(range(3)):
        transformed_regions = tuple((region[:3] + tuple((region[3 + index] for index in coordinate_permutation)) for region in pi_regions))
        (transformed_block, multiplicity) = modal_return(transformed_regions)
        if not multiplicity == 4:
            raise AssertionError('comprobación ejecutable fallida')
        if not singleton_coordinate(transformed_block) == 169:
            raise AssertionError('comprobación ejecutable fallida')
    values = realizacion_analitica(ALPHA, selector)
    determinant_A = values['D_A']
    if not 0 < ALPHA < 1:
        raise AssertionError('comprobación ejecutable fallida')
    if not 0 < determinant_A < 1:
        raise AssertionError('comprobación ejecutable fallida')
    if not 0 < determinant_A * ALPHA < 1:
        raise AssertionError('comprobación ejecutable fallida')
    if not mp.almosteq(determinant_A, mp.exp(-100 * mp.pi * ALPHA / 9)):
        raise AssertionError('comprobación ejecutable fallida')
    if not mp.almosteq(values['q_minus'] * values['q_plus'], determinant_A):
        raise AssertionError('comprobación ejecutable fallida')
    if not mp.almosteq(-mp.mpf(9) / (100 * mp.pi) * mp.log(determinant_A), ALPHA):
        raise AssertionError('comprobación ejecutable fallida')
    coefficients = {6: mp.mpf(selector), 7: determinant_A}
    for degree in range(7, 40):
        coefficients[degree + 1] = determinant_A * coefficients[degree]
    for degree in range(7, 40):
        if not mp.almosteq(coefficients[degree], determinant_A ** (degree - 6)):
            raise AssertionError('comprobación ejecutable fallida')
    partial = selector * ALPHA ** 6 + mp.fsum((coefficients[degree] * ALPHA ** degree for degree in range(7, 40)))
    omitted_bound = determinant_A ** 34 * ALPHA ** 40 / (1 - determinant_A * ALPHA)
    if not abs(partial - values['regional_character']) <= omitted_bound * (1 + mp.mpf('1e-80')):
        raise AssertionError('comprobación ejecutable fallida')
    truncated_character = selector * ALPHA ** 6 + determinant_A * ALPHA ** 7
    truncated_y = mp.pi / 90 * (values['H5'] + ALPHA) - truncated_character
    truncated_C = 180 / mp.pi * truncated_y
    exact_omitted_tail = determinant_A ** 2 * ALPHA ** 8 / (1 - determinant_A * ALPHA)
    if not mp.almosteq(values['regional_character'] - truncated_character, exact_omitted_tail):
        raise AssertionError('comprobación ejecutable fallida')
    C_selector_168 = realizacion_analitica(ALPHA, 168)['C_degrees']
    C_selector_170 = realizacion_analitica(ALPHA, 170)['C_degrees']
    no_determinant_tail = 2 * (values['H5'] + ALPHA) - 180 / mp.pi * selector * ALPHA ** 6
    unit_tail_character = selector * ALPHA ** 6 + ALPHA ** 7 / (1 - ALPHA)
    C_unit_tail = 2 * (values['H5'] + ALPHA) - 180 / mp.pi * unit_tail_character
    if not C_selector_168 != values['C_degrees']:
        raise AssertionError('comprobación ejecutable fallida')
    if not C_selector_170 != values['C_degrees']:
        raise AssertionError('comprobación ejecutable fallida')
    if not no_determinant_tail != values['C_degrees']:
        raise AssertionError('comprobación ejecutable fallida')
    if not C_unit_tail != values['C_degrees']:
        raise AssertionError('comprobación ejecutable fallida')
    rounded_prediction = round_decimal(values['C_degrees'], 15)
    if not rounded_prediction == C_PUBLICADO:
        raise AssertionError('comprobación ejecutable fallida')
    hbar_si = H_SI_MANTISSA / (2 * mp.pi)
    if not values['H5'] != hbar_si:
        raise AssertionError('comprobación ejecutable fallida')
    if not values['hbar_reduced_after_return'] != hbar_si:
        raise AssertionError('comprobación ejecutable fallida')
    checks = {'catalogue_has_exact_five_pi_regions': True, 'all_regional_words_have_length_six': True, 'modal_terminal_block_is_unique': True, 'modal_terminal_block_has_multiplicity_four': True, 'singleton_selector_is_169': True, 'selector_169_occurs_globally_84_times_uniformly_14_per_position': True, 'oriented_terminal_defect_is_249_402_249_with_sum_900': True, 'selector_is_S5_invariant_and_S3_equivariant': True, 'determinant_depends_only_on_alpha': True, 'determinant_character_is_multiplicative': True, 'regional_series_converges_absolutely_at_alpha': True, 'closed_form_matches_recurrence': True, 'published_fifteen_decimal_rounding_is_reproduced': True, 'barbero_is_recomputed_from_the_generated_phase': True, 'H5_and_post_return_action_are_distinct': True, 'neither_action_value_equals_SI_hbar_mantissa': True}
    result = {'schema': 'HMT.realizacion-analitica-regional.v1', 'status': 'TEOREMA_RELATIVO_A_LAS_REGLAS_DECLARADAS_DEL_LECTOR', 'authors': ['Oumar Haidara Fall', 'Rubén Ramos Balsa'], 'source_hashes': {CATALOG.relative_to(ROOT).as_posix(): sha256(CATALOG), ALPHA_CERTIFICATE.relative_to(ROOT).as_posix(): sha256(ALPHA_CERTIFICATE)}, 'finite_catalogue_theorem': {'fiber': 'Psi^{-1}(010211)', 'region_count': 5, 'word_length': 6, 'terminal_block_multiset': {'169|272|272': 4, '418|674|521': 1}, 'unique_modal_block': '169|272|272', 'mutated_block': '418|674|521', 'oriented_terminal_defect': list(terminal_defect), 'terminal_defect_sum': sum(terminal_defect), 'equivariant_singleton_selector': selector, 'selector_global_occurrences': sum(selector_position_counts), 'selector_occurrences_by_position': list(selector_position_counts)}, 'declared_analytic_reader_rules': ['cylindrical word length equals analytic degree', 'the finite return impulse and the strict continuation are additive summands', 'the strict continuation begins at the unit of the determinant line', 'each subsequent degree is transported by exterior-square character D_A', 'the oriented return correction is subtracted from the fifth-order action phase'], 'recurrence': {'kappa_6': str(selector), 'kappa_7': nstr(determinant_A), 'rule_for_n_ge_7': 'kappa_(n+1)=D_A*kappa_n', 'closed_form': '169*z^6 + D_A*z^7/(1-D_A*z)', 'D_A': nstr(determinant_A), 'alpha_times_D_A': nstr(ALPHA * determinant_A), 'radius_of_convergence': nstr(1 / determinant_A)}, 'values': {key: nstr(value) for (key, value) in values.items()}, 'seventh_order_truncation': {'C_degrees': nstr(truncated_C), 'omitted_tail_exact': nstr(exact_omitted_tail)}, 'ablations': {'selector_168_C_degrees': nstr(C_selector_168), 'selector_170_C_degrees': nstr(C_selector_170), 'without_determinant_tail_C_degrees': nstr(no_determinant_tail), 'unit_instead_of_D_A_tail_C_degrees': nstr(C_unit_tail)}, 'external_controls_not_used_by_generator': {'published_C_degrees': nstr(C_PUBLICADO), 'prediction_rounded_to_15_decimals': nstr(rounded_prediction), 'exact_SI_h_mantissa': nstr(H_SI_MANTISSA), 'SI_hbar_mantissa': nstr(hbar_si), 'pre_return_h_minus_SI_h': nstr(values['h_pre_return_mantissa'] - H_SI_MANTISSA), 'post_return_h_minus_SI_h': nstr(values['h_post_return_mantissa'] - H_SI_MANTISSA)}, 'checks': checks, 'all_checks_pass': all(checks.values())}
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result['all_checks_pass']:
        raise SystemExit(1)
    print('PASS_REALIZACION_ANALITICA_REGIONAL')
if __name__ == '__main__':
    main()
