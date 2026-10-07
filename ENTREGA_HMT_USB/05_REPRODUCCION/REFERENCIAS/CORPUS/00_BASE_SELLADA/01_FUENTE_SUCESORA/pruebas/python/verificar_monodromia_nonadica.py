"""Certificado autocontenido de la conexión nonádica de supervivencia.

El programa trabaja exclusivamente con los datos publicados junto al
manuscrito.  Verifica, sin consultar rutas históricas externas:

* la recurrencia entera residuo--cociente que genera veinte bloques;
* el prefijo de treinta trits y la primera frontera de treinta y seis;
* las nueve fases consecutivas K=5,...,13;
* la fibra de tres salidas en el retorno 9->1 y la selección 3->1 a
  profundidad futura dos;
* el eje phi y el agregado pi+e comunes a las tres salidas;
* nueve retornos de fase con cambio del estado visible;
* la lectura exacta de doce ternas decimales desde trece bloques;
* el calendario de Beatty de separaciones 21/22.

Alcance: los estados iniciales, las matrices y las relaciones de frontera son
datos calibrados publicados. El certificado demuestra sus consecuencias en la
ventana finita; no convierte esa ventana en un teorema coinductivo global ni
construye un emisor independiente de los valores usados al calibrarla.
"""
from __future__ import annotations
import csv
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, getcontext
import hashlib
import json
from pathlib import Path
from typing import Sequence
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'datos'
OUTPUT = ROOT / 'certificados/monodromia_nonadica.json'
FLOW = DATA / 'flujo_hensel_20_bloques.json'
GATE_BRANCHES = DATA / 'ramas_frontera_fase9.csv'
BOUNDARY_DETAILS = DATA / 'detalles_seleccion_frontera.csv'
LEDGER = DATA / 'monodromia_20_bloques.csv'
PHASE_WINDOW = DATA / 'supervivencia_fases_5_a_13.csv'
ARCHIMEDEAN_READING = DATA / 'lectura_arquimediana_12_bloques.csv'
SUMMARY = DATA / 'resumen_monodromia_20_bloques.json'
INPUTS = (FLOW, GATE_BRANCHES, BOUNDARY_DETAILS, LEDGER, PHASE_WINDOW, ARCHIMEDEAN_READING, SUMMARY)
CHANNELS = ('pi', 'e', 'phi')
EXPECTED_W30 = {'pi': '010211|012222|010211|002111|110221', 'e': '201101|121221|102011|012222|102011', 'phi': '121200|112202|121020|010210|010200'}
EXPECTED_R36 = {'pi': '222220', 'e': '021222', 'phi': '102011'}
EXPECTED_B9 = ('100100', '020112', '010122')
EXPECTED_B10 = ('101222', '112221', '112002')
EXPECTED_B11 = ('022212', '110001', '100021')
EXPECTED_CANDIDATES = (('101222', '112221', '112002'), ('102221', '111222', '112002'), ('111221', '102222', '112002'))
EXPECTED_DELTAS = ((279, 352, 365), (280, 351, 365), (282, 350, 365))
EXPECTED_NEXT_DELTA = (502, 662, 638)
EXPECTED_PHASES = (5, 6, 7, 8, 9, 1, 2, 3, 4)
EXPECTED_LOCAL_COUNTS = (1, 1, 3, 3, 2, 1, 1, 1, 1)
EXPECTED_BEATTY_START = (20, 42, 64, 86, 108, 130, 151, 173, 195, 217)

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda : stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))

def row_times_matrix(row: Sequence[int], matrix: Sequence[Sequence[int]]) -> list[int]:
    return [sum((int(row[i]) * int(matrix[i][j]) for i in range(len(row)))) for j in range(len(matrix[0]))]

def matrix_product(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]) -> list[list[int]]:
    return [row_times_matrix(row, right) for row in left]

def determinant_bareiss(matrix: Sequence[Sequence[int]]) -> int:
    """Calcula el determinante entero mediante eliminación de Bareiss."""
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if a[r][k] != 0), None)
        if pivot is None:
            return 0
        if pivot != k:
            (a[k], a[pivot]) = (a[pivot], a[k])
            sign *= -1
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * p - a[i][k] * a[k][j]) // previous
        previous = p
    return sign * a[n - 1][n - 1]

def step(state: Sequence[int], matrix: Sequence[Sequence[int]]) -> tuple[list[int], list[int]]:
    image = row_times_matrix(state, matrix)
    residue = [value % 3 for value in image]
    quotient = [(value - digit) // 3 for (value, digit) in zip(image, residue)]
    if not image == [digit + 3 * value for (digit, value) in zip(residue, quotient)]:
        raise AssertionError('comprobación ejecutable fallida')
    return (residue, quotient)

def emit(initial: Sequence[int], matrix: Sequence[Sequence[int]], count: int) -> tuple[list[str], list[list[int]]]:
    state = list(map(int, initial))
    states = [state]
    blocks: list[str] = []
    for _ in range(count):
        (residue, state) = step(state, matrix)
        blocks.append(''.join(map(str, residue)))
        states.append(state)
    return (blocks, states)

def parse_word(word: str) -> list[int]:
    return [int(character) for character in word]

def trit_sum(*words: str) -> str:
    return ''.join((str(sum((int(word[index]) for word in words)) % 3) for index in range(len(words[0]))))

def trit_subtract(left: str, right: str) -> str:
    return ''.join((str((int(a) - int(b)) % 3) for (a, b) in zip(left, right)))

def scalar_trit_product(scalar: int, word: str) -> str:
    return ''.join((str(scalar * int(character) % 3) for character in word))

def cylinder_intersects(blocks: Sequence[str], triads: Sequence[int]) -> bool:
    word = ''.join(blocks)
    length = len(word)
    visible = 0
    power1000 = 1
    bound = 3 ** length
    while power1000 * 1000 <= bound:
        power1000 *= 1000
        visible += 1
    if not len(triads) >= visible:
        raise AssertionError('comprobación ejecutable fallida')
    ternary_integer = int(word, 3)
    decimal_integer = 0
    for triad in triads[:visible]:
        decimal_integer = 1000 * decimal_integer + int(triad)
    return ternary_integer * 1000 ** visible < (decimal_integer + 1) * 3 ** length and (ternary_integer + 1) * 1000 ** visible > decimal_integer * 3 ** length

def exact_triads(blocks: Sequence[str], count: int) -> list[int]:
    word = ''.join(blocks)
    length = len(word)
    integer = int(word, 3)
    decimal_prefix = 1000 ** count * integer // 3 ** length
    digits = f'{decimal_prefix:0{3 * count}d}'
    return [int(digits[3 * i:3 * i + 3]) for i in range(count)]

def verify_hensel_and_ledger(flow: dict[str, object], ledger: list[dict[str, str]], summary: dict[str, object]) -> tuple[dict[str, list[str]], dict[str, list[list[int]]], dict[str, object]]:
    matrix = [list(map(int, row)) for row in flow['A']]
    inverse = [list(map(int, row)) for row in flow['A_inv']]
    identity = [[int(i == j) for j in range(6)] for i in range(6)]
    if not determinant_bareiss(matrix) == 1:
        raise AssertionError('comprobación ejecutable fallida')
    if not matrix_product(matrix, inverse) == identity:
        raise AssertionError('comprobación ejecutable fallida')
    if not matrix_product(inverse, matrix) == identity:
        raise AssertionError('comprobación ejecutable fallida')
    blocks_by_channel: dict[str, list[str]] = {}
    states_by_channel: dict[str, list[list[int]]] = {}
    channels = flow['channels']
    for channel in CHANNELS:
        (blocks, states) = emit(channels[channel]['x0_mod_3^180'], matrix, 20)
        if not blocks == summary['blocks'][channel]:
            raise AssertionError('comprobación ejecutable fallida')
        if not blocks == [row[f'{channel}_block'] for row in ledger]:
            raise AssertionError('comprobación ejecutable fallida')
        blocks_by_channel[channel] = blocks
        states_by_channel[channel] = states
        for (index, row) in enumerate(ledger):
            if not row[f'{channel}_prefix'] == '|'.join(blocks[:index + 1]):
                raise AssertionError('comprobación ejecutable fallida')
    if not [int(row['K_visible']) for row in ledger] == list(range(20)):
        raise AssertionError('comprobación ejecutable fallida')
    if not [int(row['phase9']) for row in ledger] == [9 if index % 9 == 0 else index % 9 for index in range(20)]:
        raise AssertionError('comprobación ejecutable fallida')
    return (blocks_by_channel, states_by_channel, {'matrix_determinant': 1, 'matrix_inverse_verified': True, 'division_identity_verified_steps': 20 * len(CHANNELS), 'published_blocks_verified': 20 * len(CHANNELS)})

def verify_prefix_and_first_boundary(blocks_by_channel: dict[str, list[str]]) -> dict[str, object]:
    w30 = {channel: '|'.join(blocks_by_channel[channel][:5]) for channel in CHANNELS}
    r36 = {channel: blocks_by_channel[channel][5] for channel in CHANNELS}
    if not w30 == EXPECTED_W30:
        raise AssertionError('comprobación ejecutable fallida')
    if not r36 == EXPECTED_R36:
        raise AssertionError('comprobación ejecutable fallida')
    return {'w30_five_blocks': w30, 'R36_first_boundary': r36, 'interpretation': 'w30 es un prefijo de cinco bloques; R36 es el sexto bloque y la primera frontera publicada, no el término de la rama'}

def verify_phase_window(rows: list[dict[str, str]], blocks_by_channel: dict[str, list[str]]) -> dict[str, object]:
    if not [int(row['K']) for row in rows] == list(range(5, 14)):
        raise AssertionError('comprobación ejecutable fallida')
    if not tuple((int(row['puerta']) for row in rows)) == EXPECTED_PHASES:
        raise AssertionError('comprobación ejecutable fallida')
    if not tuple((int(row['locales']) for row in rows)) == EXPECTED_LOCAL_COUNTS:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((int(row['candidatos_qa']) == 729 for row in rows)):
        raise AssertionError('comprobación ejecutable fallida')
    if not all((int(row['supervivientes_1paso']) == 1 for row in rows)):
        raise AssertionError('comprobación ejecutable fallida')
    for row in rows:
        index = int(row['K'])
        for channel in CHANNELS:
            if not row[channel] == blocks_by_channel[channel][index]:
                raise AssertionError('comprobación ejecutable fallida')
    return {'K_window': [5, 13], 'phases': list(EXPECTED_PHASES), 'local_candidate_counts': list(EXPECTED_LOCAL_COUNTS), 'ambient_candidates_per_phase': 729, 'selected_branch_per_phase': 1}

def verify_gate(branch_rows: list[dict[str, str]], detail_rows: list[dict[str, str]], blocks_by_channel: dict[str, list[str]], flow: dict[str, object]) -> dict[str, object]:
    candidates = tuple((tuple(row['rows'].split('|')) for row in branch_rows))
    if not candidates == EXPECTED_CANDIDATES:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((int(row['surv_h1']) > 0 for row in branch_rows)):
        raise AssertionError('comprobación ejecutable fallida')
    if not int(branch_rows[0]['surv_h2']) > 0:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((int(row['surv_h2']) == 0 for row in branch_rows[1:])):
        raise AssertionError('comprobación ejecutable fallida')
    b9 = tuple((blocks_by_channel[channel][9] for channel in CHANNELS))
    b10 = tuple((blocks_by_channel[channel][10] for channel in CHANNELS))
    b11 = tuple((blocks_by_channel[channel][11] for channel in CHANNELS))
    if not b9 == EXPECTED_B9:
        raise AssertionError('comprobación ejecutable fallida')
    if not b10 == EXPECTED_B10:
        raise AssertionError('comprobación ejecutable fallida')
    if not b11 == EXPECTED_B11:
        raise AssertionError('comprobación ejecutable fallida')
    fixed_phi = {candidate[2] for candidate in candidates}
    fixed_pi_plus_e = {trit_sum(candidate[0], candidate[1]) for candidate in candidates}
    if not fixed_phi == {'112002'}:
        raise AssertionError('comprobación ejecutable fallida')
    if not fixed_pi_plus_e == {'210110'}:
        raise AssertionError('comprobación ejecutable fallida')
    axis_identities: list[dict[str, str]] = []
    for candidate in candidates:
        q = trit_sum(candidate[0], candidate[1], candidate[2])
        aggregate = trit_sum(candidate[0], candidate[1])
        a = trit_subtract(aggregate, candidate[2])
        recovered_phi = scalar_trit_product(2, trit_subtract(q, a))
        recovered_aggregate = trit_subtract(q, recovered_phi)
        if not recovered_phi == candidate[2]:
            raise AssertionError('comprobación ejecutable fallida')
        if not recovered_aggregate == aggregate:
            raise AssertionError('comprobación ejecutable fallida')
        axis_identities.append({'q': q, 'a': a, 'recovered_phi': recovered_phi, 'recovered_pi_plus_e': recovered_aggregate})
    gate_details = [row for row in detail_rows if int(row['t']) == 9]
    if not tuple((tuple(row['rows'].split('|')) for row in gate_details)) == candidates:
        raise AssertionError('comprobación ejecutable fallida')
    deltas = tuple((tuple((int(row[f'delta_options_{channel}']) for channel in CHANNELS)) for row in gate_details))
    if not deltas == EXPECTED_DELTAS:
        raise AssertionError('comprobación ejecutable fallida')
    cylinder_checks: dict[str, object] = {}
    channels = flow['channels']
    for (branch_index, candidate) in enumerate(candidates):
        per_channel: dict[str, object] = {}
        for (channel_index, channel) in enumerate(CHANNELS):
            base_triads = list(channels[channel]['triads_171_from_1080trits'])
            triads = base_triads[:9] + [deltas[branch_index][channel_index]]
            blocks = blocks_by_channel[channel][:10] + [candidate[channel_index]]
            current_ok = cylinder_intersects(blocks, triads)
            next_ok = cylinder_intersects(blocks + [EXPECTED_B11[channel_index]], triads + [EXPECTED_NEXT_DELTA[channel_index]])
            if not current_ok:
                raise AssertionError('comprobación ejecutable fallida')
            if not next_ok is (branch_index == 0 or channel == 'phi'):
                raise AssertionError('comprobación ejecutable fallida')
            per_channel[channel] = {'current_cylinder_intersects': current_ok, 'next_published_cylinder_intersects': next_ok}
        cylinder_checks[f'branch_{branch_index}'] = per_channel
    return {'input_B9': list(b9), 'candidate_outputs_B10': [list(candidate) for candidate in candidates], 'selected_output_B10': list(b10), 'next_state_B11': list(b11), 'fixed_phi_axis': next(iter(fixed_phi)), 'fixed_pi_plus_e': next(iter(fixed_pi_plus_e)), 'axis_identities': axis_identities, 'survivors_h1': 3, 'survivors_h2': 1, 'deltas_at_gate': [list(values) for values in deltas], 'next_published_delta': list(EXPECTED_NEXT_DELTA), 'cylinder_checks': cylinder_checks}

def verify_returns(ledger: list[dict[str, str]]) -> dict[str, object]:
    returns: list[dict[str, object]] = []
    for index in range(1, 10):
        initial = ledger[index]
        returned = ledger[index + 9]
        if not initial['phase9'] == returned['phase9']:
            raise AssertionError('comprobación ejecutable fallida')
        before = tuple((initial[f'{channel}_block'] for channel in CHANNELS))
        after = tuple((returned[f'{channel}_block'] for channel in CHANNELS))
        if not before != after:
            raise AssertionError('comprobación ejecutable fallida')
        if not before[2] != after[2]:
            raise AssertionError('comprobación ejecutable fallida')
        if not trit_sum(before[0], before[1]) != trit_sum(after[0], after[1]):
            raise AssertionError('comprobación ejecutable fallida')
        returns.append({'K': index, 'K_plus_9': index + 9, 'phase': int(initial['phase9']), 'state_changed': True, 'phi_changed': True, 'pi_plus_e_changed': True})
    return {'verified_returns': returns, 'law_in_published_window': 'g(K+9)=g(K) and B(K+9)!=B(K)'}

def verify_archimedean_reading(rows: list[dict[str, str]], blocks_by_channel: dict[str, list[str]], ledger: list[dict[str, str]], summary: dict[str, object]) -> dict[str, object]:
    published = {row['constant']: [int(item) for item in row['triads_12'].split('|')] for row in rows}
    result: dict[str, object] = {}
    for channel in CHANNELS:
        computed = exact_triads(blocks_by_channel[channel][:13], 12)
        if not computed == published[channel]:
            raise AssertionError('comprobación ejecutable fallida')
        if not '|'.join((f'{item:03d}' for item in computed)) == summary['triads12'][channel]:
            raise AssertionError('comprobación ejecutable fallida')
        if not ledger[12][f'{channel}_decimal_prefix'] == '|'.join((f'{item:03d}' for item in computed)):
            raise AssertionError('comprobación ejecutable fallida')
        result[channel] = {'ternary_blocks_used': 13, 'ternary_digits_used': 78, 'decimal_triads': [f'{item:03d}' for item in computed], 'decimal_digits': 36}
    return result

def verify_beatty_calendar() -> dict[str, object]:
    getcontext().prec = 100
    three = Decimal(3)
    thousand = Decimal(1000)
    lam = Decimal(6) * three.ln() / thousand.ln()
    delta = Decimal(1) - lam

    def floor(value: Decimal) -> int:
        return int(value.to_integral_value(rounding=ROUND_FLOOR))

    def ceil(value: Decimal) -> int:
        return int(value.to_integral_value(rounding=ROUND_CEILING))
    formula = [ceil(Decimal(m) / delta) - 2 for m in range(1, 101)]
    direct = [t for t in range(0, formula[-1] + 2) if floor(lam * Decimal(t + 2)) == floor(lam * Decimal(t + 1))]
    if not formula == direct[:len(formula)]:
        raise AssertionError('comprobación ejecutable fallida')
    if not tuple(formula[:10]) == EXPECTED_BEATTY_START:
        raise AssertionError('comprobación ejecutable fallida')
    gaps = {right - left for (left, right) in zip(formula, formula[1:])}
    if not gaps == {21, 22}:
        raise AssertionError('comprobación ejecutable fallida')
    return {'lambda': str(lam), 'delta': str(delta), 'first_reopenings': formula[:10], 'verified_reopenings': len(formula), 'gap_set': sorted(gaps)}

def main() -> None:
    for path in INPUTS:
        if not path.is_file():
            raise FileNotFoundError(path)
    flow = json.loads(FLOW.read_text(encoding='utf-8'))
    summary = json.loads(SUMMARY.read_text(encoding='utf-8'))
    ledger = read_csv(LEDGER)
    phase_rows = read_csv(PHASE_WINDOW)
    branch_rows = read_csv(GATE_BRANCHES)
    detail_rows = read_csv(BOUNDARY_DETAILS)
    reading_rows = read_csv(ARCHIMEDEAN_READING)
    (blocks, states, hensel) = verify_hensel_and_ledger(flow, ledger, summary)
    if not all((len(states[channel]) == 21 for channel in CHANNELS)):
        raise AssertionError('comprobación ejecutable fallida')
    result = {'schema': 'HMT.monodromia-nonadica.finita.v2', 'status': 'PASS', 'input_sha256': {path.relative_to(ROOT).as_posix(): sha256(path) for path in INPUTS}, 'residue_quotient_recurrence': hensel, 'prefix_and_boundary': verify_prefix_and_first_boundary(blocks), 'nine_phase_window': verify_phase_window(phase_rows, blocks), 'gate_9_to_1': verify_gate(branch_rows, detail_rows, blocks, flow), 'phase_returns': verify_returns(ledger), 'twenty_block_branch': {channel: blocks[channel] for channel in CHANNELS}, 'archimedean_reading': verify_archimedean_reading(reading_rows, blocks, ledger, summary), 'beatty_calendar': verify_beatty_calendar(), 'scope': {'proved': 'Todas las identidades enumeradas se derivan de la matriz, los estados iniciales y las relaciones de frontera publicados.', 'premise': 'La carta Hensel y el ledger de frontera son datos calibrados; el archivo de flujo declara que sus estados iniciales se obtuvieron usando las constantes como oráculo.', 'not_proved': 'No se demuestra aquí supervivencia unitaria en toda profundidad ni una realización APP-min independiente de los objetivos.', 'conditional_extension': 'Si en cada profundidad existe un único prefijo superviviente y las truncaciones son compatibles, el límite inverso contiene una única historia global.'}}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PASS_MONODROMIA_NONADICA_FINITA')
    print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == '__main__':
    main()
