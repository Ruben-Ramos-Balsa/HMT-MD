#!/usr/bin/env python3
"""Auditoría independiente de convenciones APP, tipos, lifts, K y rutas.

No importa código HMT. Recalcula con biblioteca estándar los hechos finitos y
lee los programas del corpus únicamente para clasificar la procedencia de sus
entradas (upstream frente a target-conditioned/oracle).
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "03_PAPER/HMT_MACROPAPER_V3/auditoria/RESULTADOS_PROCEDENCIA_APP_LIFTS_K.json"

N33_DIR = ROOT / (
    "05_ENTREGA/HMT_CIERRE_HOLOGRAFICO_V2_PRINCETON/certificados/"
    "N33_PI_E_PHI/HMT_N33_PI_PHI_E_CLOSEOUT"
)
N32_DIR = ROOT / (
    "05_ENTREGA/HMT_CIERRE_HOLOGRAFICO_V2_PRINCETON/certificados/"
    "N32_DODECAFASE_ALPHA/HMT_N32_REFEREE_CLOSEOUT_PACKAGE_v2"
)
NEWSO = ROOT / (
    "05_ENTREGA/HMT_CIERRE_HOLOGRAFICO_V2_PRINCETON/certificados/"
    "NEWSO/verificar_newso_ct108.py"
)
F006 = ROOT / "01_ORIGINALES/2026-01/F006_numeros y modulos holograficos.txt"
F054 = ROOT / "01_ORIGINALES/2025-12/F054_HMT-NUCLEO.txt"
F053_SCAN = ROOT / (
    "02_LECTURA/paquetes_descomprimidos/"
    "F053_APP_HMT_Overleaf_Publicacion_Doble_Salida_v5_SOURCE/"
    "APP_HMT_Overleaf_Publicacion_Doble_Salida_v5_SOURCE/code/"
    "hmt_n32_upstream_u12_gauge_scan.py"
)
F053_TEX = ROOT / (
    "02_LECTURA/paquetes_descomprimidos/"
    "F053_APP_HMT_Overleaf_Publicacion_Doble_Salida_v5_SOURCE/"
    "APP_HMT_Overleaf_Publicacion_Doble_Salida_v5_SOURCE/appendix_docs/"
    "ventana_HMT_N32_upstream_U12_gauge_canonicity.tex"
)
F013_DIR = ROOT / (
    "02_LECTURA/paquetes_descomprimidos/F013_hmt_g9_rama_20bloques/"
    "hmt_g9_rama_20bloques"
)
N72_DIR = ROOT / (
    "02_LECTURA/paquetes_descomprimidos/F082_gemma1/gemma1/__extraido__/"
    "HMT_N72_supervivencia_coinductiva_novena_puerta_v1/"
    "HMT_N72_supervivencia_coinductiva_novena_puerta_v1"
)
N75 = ROOT / (
    "02_LECTURA/paquetes_descomprimidos/F082_gemma1/gemma1/"
    "N75_ventana_sintesis_cierre_holografico_infinito.tex"
)
BODY_TPK = ROOT / (
    "03_PAPER/HMT_MACROPAPER_V3/paper/sections/body/03_app_tpk.tex"
)
BODY_OBJECTS = ROOT / (
    "03_PAPER/HMT_MACROPAPER_V3/paper/sections/body/02_objetos.tex"
)
BODY_NUMBER = ROOT / (
    "03_PAPER/HMT_MACROPAPER_V3/paper/sections/body/04_numero_medicion_v3.tex"
)
V3_README = ROOT / "03_PAPER/HMT_MACROPAPER_V3/README.md"
THESIS_CONTRACT = ROOT / (
    "03_PAPER/HMT_MACROPAPER_V3/auditoria/CONTRATO_TESIS_RECTORA_NO_OMITIBLE.md"
)
LOGIC_AUDIT = ROOT / (
    "03_PAPER/HMT_MACROPAPER_V3/auditoria/CORRECCION_LOGICA_HMT.md"
)
CORE_CLAIMS = ROOT / (
    "03_PAPER/HMT_MACROPAPER_V3/auditoria/CLAIMS_NUCLEO_CONSTANTES.json"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def dr9(n: int) -> int:
    r = n % 9
    return 9 if r == 0 else r


PLUS9_MIN = [[dr9((i + 1) + (j + 1)) for j in range(9)] for i in range(9)]
TIMES9_MIN = [[dr9((i + 1) * (j + 1)) for j in range(9)] for i in range(9)]
LOG9_MIN = {1: 0, 2: 1, 4: 2, 8: 3, 7: 4, 5: 5, 3: 0, 6: 0, 9: 0}
DIRS_MIN = ((-1, 0), (0, 1), (1, 0), (0, -1))


def rank_mod3(matrix: list[list[int]]) -> int:
    a = [[x % 3 for x in row] for row in matrix]
    if not a:
        return 0
    rows, cols, pivot_row = len(a), len(a[0]), 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        inv = pow(a[pivot_row][col], -1, 3)
        a[pivot_row] = [(inv * x) % 3 for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r][col]:
                factor = a[r][col]
                a[r] = [(x - factor * y) % 3 for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def inverse_mod3(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    a = [
        [x % 3 for x in row] + [int(i == j) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        require(pivot is not None, "matriz singular en F3")
        a[col], a[pivot] = a[pivot], a[col]
        inv = pow(a[col][col], -1, 3)
        a[col] = [(inv * x) % 3 for x in a[col]]
        for r in range(n):
            if r != col and a[r][col]:
                factor = a[r][col]
                a[r] = [(x - factor * y) % 3 for x, y in zip(a[r], a[col])]
    return [row[n:] for row in a]


def matmul_mod3(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(row[k] * b[k][j] for k in range(len(b))) % 3 for j in range(len(b[0]))]
        for row in a
    ]


def row_times_mod3(row: list[int], matrix: list[list[int]]) -> list[int]:
    return [sum(row[k] * matrix[k][j] for k in range(6)) % 3 for j in range(6)]


def matrix_order_mod3(matrix: list[list[int]], limit: int = 10000) -> int:
    n = len(matrix)
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    power = identity
    for order in range(1, limit + 1):
        power = matmul_mod3(power, matrix)
        if power == identity:
            return order
    raise RuntimeError(f"orden no hallado antes de {limit}")


def rank_q(matrix: list[list[int]]) -> int:
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    rows, cols, pivot_row = len(a), len(a[0]), 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        p = a[pivot_row][col]
        a[pivot_row] = [x / p for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r][col]:
                factor = a[r][col]
                a[r] = [x - factor * y for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
    return pivot_row


def app_audit() -> dict:
    canonical = [[dr9(i + j) for j in range(1, 10)] for i in range(1, 10)]
    transport = [[dr9(i + j - 1) for j in range(1, 10)] for i in range(1, 10)]
    # tau(j)=dr9(j-1): column j of the transport chart is column tau(j)
    # of the canonical chart.
    tau = [dr9(j - 1) for j in range(1, 10)]
    conjugate = all(
        transport[i - 1][j - 1] == canonical[i - 1][tau[j - 1] - 1]
        for i in range(1, 10) for j in range(1, 10)
    )
    require(conjugate, "falló la conjugación de cartas APP")
    return {
        "status": "PASS",
        "canonical_emission_chart": "A_plus(i,j)=dr9(i+j), i,j in {1,...,9}",
        "transport_chart": "A_plus_tr(i,j)=dr9(i+j-1)",
        "chart_change_tau_columns": tau,
        "identity": "A_plus_tr(i,j)=A_plus(i,tau(j))",
        "interpretation": "same toroidal Latin square; one-column origin/phase shift",
    }


def catalogue_audit() -> dict:
    path = N33_DIR / "n33_uid_catalog.csv"
    u6_rows: list[tuple[int, ...]] = []
    words: set[tuple[int, ...]] = set()
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            u6 = tuple(int(x) for x in row["U6"].split("|"))
            w6 = tuple(int(x) for x in row["w6"])
            require(len(u6) == len(w6) == 6, "tipo de fila N33 inesperado")
            require(all(0 <= x <= 999 for x in u6), "U6 fuera de 0..999")
            require(w6 == tuple((-x) % 3 for x in u6), "reducción rho inconsistente")
            u6_rows.append(u6)
            words.add(w6)
    require(len(u6_rows) == len(set(u6_rows)) == 468, "catálogo U6 no tiene 468 elementos")
    require(len(words) == 243, "imagen ternaria no tiene 243 elementos")
    zero = (0, 0, 0, 0, 0, 0)
    closure_witness = None
    ordered = sorted(words)
    for a in ordered:
        for b in ordered:
            c = tuple((x + y) % 3 for x, y in zip(a, b))
            if c not in words:
                closure_witness = {"a": a, "b": b, "a_plus_b": c}
                break
        if closure_witness:
            break
    span_rank = rank_mod3([list(w) for w in words])
    require(zero not in words and closure_witness is not None and span_rank == 6,
            "la imagen ternaria cambió de estructura")
    return {
        "status": "PASS",
        "typed_chain": (
            "Omega(104976) -> U6_image subset {0,...,999}^6 (468) "
            "->rho W6_image subset F3^6 (243)"
        ),
        "u6_distinct": 468,
        "w6_distinct": 243,
        "w6_zero_present": False,
        "w6_closed_under_addition": False,
        "w6_linear_span_rank": span_rank,
        "addition_counterexample": closure_witness,
        "conclusion": "cardinality 243=3^5 does not make the attained image a 5-dimensional subspace",
    }


def compute_u12_min(seed: tuple[int, int, int, int, int, int]) -> tuple[int, ...]:
    """Reimplementación independiente del motor mínimo de dos cursores.

    La rutina reproduce la regla publicada sin importar ningún módulo HMT. Se
    usa para distinguir el catálogo periódico U6||U6 del testigo firmado de la
    estructura enriquecida.
    """
    ip, jp, it, jt, hp, ht = seed
    hpi, hpj = DIRS_MIN[hp]
    hti, htj = DIRS_MIN[ht]
    out: list[int] = []
    tick = 0
    for _event in range(12):
        s = e = t0 = 0
        for _ in range(9):
            tick += 1
            phase = ((tick - 1) % 9) + 1
            if phase in {1, 4, 7}:
                s += PLUS9_MIN[ip][jp]
                ip, jp = (ip + hpi) % 9, (jp + hpj) % 9
            elif phase in {2, 5, 8}:
                e += LOG9_MIN[TIMES9_MIN[it][jt]]
                it, jt = (it + hti) % 9, (jt + htj) % 9
            else:
                t0 += 1
            if tick in {27, 54, 81, 108}:
                hpi, hpj = -hpi, -hpj
                hti, htj = -hti, -htj
        d1, d2, d3 = s % 10, (s + e) % 10, (3 * s + 5 * e + 7 * t0) % 10
        out.append(100 * d1 + 10 * d2 + d3)
    return tuple(out)


def two_cursor_target_free_audit() -> dict:
    counts: Counter[tuple[int, ...]] = Counter()
    for ip in range(9):
        for jp in range(9):
            for it in range(9):
                for jt in range(9):
                    for hp in range(4):
                        for ht in range(4):
                            counts[compute_u12_min((ip, jp, it, jt, hp, ht))] += 1
    require(sum(counts.values()) == 104_976, "cambió el número de semillas del motor mínimo")
    require(len(counts) == 468, "cambió el catálogo U12 del motor mínimo")
    require(all(u[:6] == u[6:] for u in counts), "apareció una salida no periódica de periodo 6")
    shadows = {tuple((-x) % 3 for x in u[:6]) for u in counts}
    require(len(shadows) == 243, "cambió la sombra ternaria del motor mínimo")
    require(set(counts.values()) == {144, 432, 1944}, "cambiaron las multiplicidades de las fibras")
    canonical_seed = (0, 0, 0, 0, 1, 1)
    canonical = compute_u12_min(canonical_seed)
    require(canonical == (903, 850, 850, 252, 109, 252) * 2,
            "cambió la salida de la semilla canónica E/E")
    uid = sorted(counts).index(canonical)
    require(uid == 416, "cambió el identificador estable de la semilla canónica")
    signed_target = tuple(U_SIGNED)
    require(signed_target not in counts, "el testigo firmado apareció en el catálogo mínimo")
    return {
        "status": "PASS_TARGET_FREE_MINIMAL_ENGINE_SCOPE",
        "seeds": 104_976,
        "distinct_U12_catalogue_states": len(counts),
        "distinct_ternary_shadows": len(shadows),
        "fiber_multiplicities": sorted(set(counts.values())),
        "all_outputs_have_period_6": True,
        "canonical_seed_ip_jp_it_jt_hp_ht": list(canonical_seed),
        "canonical_uid": uid,
        "canonical_output": list(canonical),
        "signed_U12_occurs": False,
        "interpretation": (
            "the target-free two-cursor executable certifies APP_min -> U6||U6; "
            "it is not the executable source of the enriched signed witness"
        ),
    }


L0 = [
    [2, 2, 2, 1, 2, 1], [2, 1, 2, 2, 1, 1], [1, 0, 0, 1, 0, 2],
    [0, 0, 1, 1, 1, 0], [2, 2, 2, 0, 2, 1], [2, 1, 2, 1, 0, 0],
]
L1 = [
    [2, 1, 2, 0, 2, 2], [1, 2, 1, 1, 2, 0], [1, 2, 1, 1, 1, 2],
    [0, 1, 0, 0, 2, 1], [2, 0, 2, 1, 0, 1], [0, 2, 2, 2, 1, 1],
]
TARGET_WORDS = {
    "pi": "010211012222010211002111110221",
    "e": "201101121221102011012222102011",
    "phi": "121200112202121020010210010200",
}


def split_blocks(word: str) -> list[list[int]]:
    return [[int(c) for c in word[i:i + 6]] for i in range(0, 30, 6)]


def lift_interpolation_audit() -> dict:
    x0: list[list[int]] = []
    y0: list[list[int]] = []
    x1: list[list[int]] = []
    y1: list[list[int]] = []
    for word in TARGET_WORDS.values():
        b = split_blocks(word)
        x0.extend([b[0], b[1]])
        y0.extend([b[1], b[2]])
        x1.extend([b[2], b[3]])
        y1.extend([b[3], b[4]])
    r0, r1 = rank_mod3(x0), rank_mod3(x1)
    require(r0 == r1 == 6, "los sistemas de interpolación dejaron de tener rango 6")
    recovered_l0 = matmul_mod3(inverse_mod3(x0), y0)
    recovered_l1 = matmul_mod3(inverse_mod3(x1), y1)
    require(recovered_l0 == L0 and recovered_l1 == L1, "no se recuperaron los lifts publicados")
    require(all(row_times_mod3(x, L0) == y for x, y in zip(x0, y0)), "pares L0 fallan")
    require(all(row_times_mod3(x, L1) == y for x, y in zip(x1, y1)), "pares L1 fallan")
    return {
        "status": "PASS_INTERPOLATION_IDENTITY",
        "rank_inputs_L0": r0,
        "rank_inputs_L1": r1,
        "unique_matrix_from_six_L0_transitions": recovered_l0,
        "unique_matrix_from_six_L1_transitions": recovered_l1,
        "logical_scope": (
            "the published matrices are uniquely determined by the twelve transitions "
            "inside the same three named target words; this proves exact interpolation, "
            "not independent APP/TPK provenance"
        ),
        "axiomatic_status": (
            "L0 and L1 are typed operators of the complete TPK-full/EF-G9 protocol state; "
            "a projection called APP_min must not replace that state or erase its fields"
        ),
    }


def historical_app_to_l0_claim_audit() -> dict:
    """Falsación literal del viejo bloque que decía derivar L0 desde APP.

    El cuaderno F004 define U={1,2,4,5,7,8}, intenta indexar dr9(a+b)
    otra vez en U y reduce una etiqueta de F3^2 a un solo trit. Se comprueba
    aquí la fórmula exactamente en sus puntos verificables.
    """
    units = [1, 2, 4, 5, 7, 8]
    nonunit_sums = [
        {"a": a, "b": b, "dr9_a_plus_b": dr9(a + b)}
        for a in units for b in units if dr9(a + b) not in units
    ]
    require(nonunit_sums, "inesperadamente el conjunto de unidades cerró bajo suma")
    f_map = {1: (0, 0), 2: (1, 0), 4: (0, 1), 5: (1, 1), 7: (1, 2), 8: (2, 1)}
    scalarized = {u: (3 * x + y) % 3 for u, (x, y) in f_map.items()}
    fibers: dict[int, list[int]] = {}
    for u, value in scalarized.items():
        fibers.setdefault(value, []).append(u)
    l0_order = matrix_order_mod3(L0)
    normalized_kronecker_trace = Fraction(sum(L0[i][i] for i in range(6)), 6)
    require(l0_order == 80, f"orden inesperado de L0: {l0_order}")
    require(normalized_kronecker_trace == 1, "traza normalizada inesperada")
    return {
        "status": "FAIL_AS_WRITTEN_HISTORICAL_CANDIDATE",
        "first_undefined_pair": nonunit_sums[0],
        "number_of_ordered_pairs_whose_sum_leaves_units": len(nonunit_sums),
        "reason_1": (
            "the stated U.index(dr9(a+b)) operation is undefined whenever the sum "
            "is 3, 6, or 9; the first failure is a=1,b=2"
        ),
        "scalarization_mod3": scalarized,
        "scalarization_fibers": fibers,
        "reason_2": "(3*x+y) mod 3 discards x, so it is not an isomorphism F3^2 -> F3",
        "published_L0_actual_order_in_GL6_F3": l0_order,
        "historical_claimed_order": 27,
        "normalized_trace_of_kron_L0_I3": str(normalized_kronecker_trace),
        "historical_claimed_normalized_trace": "-1/12",
        "conclusion": (
            "this old APP-to-L0 paragraph cannot establish provenance; a repaired rule "
            "would need an explicit closure/projection back to the units and a canonical "
            "functional, neither of which is specified"
        ),
    }


K = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
U_SIGNED = [2378, 1406, 2479, -452, 998, -551, -668, -204, -371, -322, -28, -997]
H4 = [[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]


def four_cursor_mask(weight_a: int = 2, weight_c: int = 5,
                     additive_offset: int = 0) -> list[int]:
    """Ejecuta literalmente el pseudocódigo APP/SU-12/TPK de F004.

    additive_offset=0 corresponde a P[i,j]=dr9(i+j), tal como está escrito.
    Los offsets 1 y 2 permiten auditar el cambio de carta aditiva.
    """
    p_table = [[dr9(i + j + additive_offset) for j in range(9)] for i in range(9)]
    x_table = [[dr9((i + 1) * (j + 1)) for j in range(9)] for i in range(9)]
    heads = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
    positions = {"N": [0, 0], "E": [0, 3], "S": [3, 0], "O": [3, 3]}
    parity_bit = 0
    digits: list[int] = []
    mask: list[int] = []
    order = ("N", "E", "S", "O")
    for tick in range(1, 109):
        residue = ((tick - 1) % 9) + 1
        delta = 1 if residue in (1, 4, 7) else -1 if residue in (2, 5, 8) else 0
        for cursor in positions:
            hi, hj = heads[cursor]
            i, j = positions[cursor]
            positions[cursor] = [(i + delta * hi) % 9, (j + delta * hj) % 9]
        if residue in (3, 6, 9):
            vals_p = [p_table[positions[w][0]][positions[w][1]] for w in order]
            vals_x = [x_table[positions[w][0]][positions[w][1]] for w in order]
            a_value = sum(vals_p) % 10
            product = 1
            for value in vals_x:
                product = product * (value % 9) % 9
            c_value = 9 if product == 0 else product
            digits.append((weight_a * a_value + weight_c * c_value + parity_bit) % 10)
        if tick in (27, 54, 81, 108):
            parity_bit = 1 - parity_bit
        if tick % 9 == 0:
            mask.append(100 * digits[-3] + 10 * digits[-2] + digits[-1])
    return mask


def four_cursor_mask_audit() -> dict:
    literal = four_cursor_mask()
    collapsed = [222, 222, 222, 333, 333, 333] * 2
    require(literal == collapsed,
            f"cambió la salida literal del pseudocódigo histórico: {literal}")
    weight_hits = [
        [wa, wc] for wa in range(10) for wc in range(10)
        if four_cursor_mask(wa, wc) == K
    ]
    require(weight_hits == [], f"algún par de pesos produjo inesperadamente K: {weight_hits}")
    chart_outputs = {str(offset): four_cursor_mask(additive_offset=offset) for offset in range(3)}
    require(all(output != K for output in chart_outputs.values()),
            "alguna carta aditiva produjo inesperadamente K")
    min_rotation = min(K[i:] + K[:i] for i in range(12))
    require(min_rotation[0] == 58 and min_rotation != K, "rotación mínima inesperada")
    return {
        "status": "FAIL_AS_WRITTEN_HISTORICAL_CANDIDATE",
        "claimed_chain": "four cardinal cursors N/E/S/O + APP sum/product + doors 3/6/9 + flips -> K",
        "output": literal,
        "expected_K_in_historical_text": K,
        "matches_expected_K": False,
        "collapse_pattern": collapsed,
        "target_constants_used": [],
        "weight_pair_search_0_to_9": {
            "number_of_pairs_returning_K": len(weight_hits),
            "pairs": weight_hits,
        },
        "diagnosis": (
            "the four cursors move synchronously and the door observables repeat; the literal "
            "routine collapses and therefore cannot establish either K or U12_signed. This "
            "negative result does not identify an omitted raw aggregator"
        ),
        "additive_chart_phase_outputs": chart_outputs,
        "chart_note": (
            "the executable uses zero-coordinate P[i,j]=dr9(i+j) together with "
            "X[i,j]=dr9((i+1)(j+1)); changing the additive chart does not repair the collapse"
        ),
        "stated_lexicographic_gauge_is_false": {
            "K_as_printed": K,
            "lexicographically_minimal_cyclic_rotation": min_rotation,
            "reason": "the minimum rotation begins with 058, not 234",
        },
        "v3_use": (
            "classify this block as an obsolete/incomplete implementation, never as the "
            "definition of the enriched model. The current profile declares its enriched "
            "fields and a separate primitive U12_signed coordinate; it does not cite this "
            "APP_min routine as their executable source"
        ),
    }


def h4(block: list[int]) -> list[int]:
    return [sum(row[j] * block[j] for j in range(4)) for row in H4]


def difference(value: list[int], step: int) -> list[int]:
    return [value[i] - value[(i + step) % 12] for i in range(12)]


def difference_matrix(step: int) -> list[list[int]]:
    out = []
    for i in range(12):
        row = [0] * 12
        row[i] = 1
        row[(i + step) % 12] -= 1
        out.append(row)
    return out


def k_audit() -> dict:
    blocks = [K[0::3], K[1::3], K[2::3]]
    hb = [h4(block) for block in blocks]
    interleaved = [hb[i % 3][i // 3] for i in range(12)]
    b90, b120, q = difference(K, 3), difference(K, 4), sum(K)
    require(interleaved == U_SIGNED, "H4(K) no devuelve U12 firmado")
    require(b90 == [-495, -116, -684, 108, 601, -90, -173, -88, 313, 560, -397, 461],
            "D3K cambió")
    require(b120 == [-425, -281, -481, 671, -255, 30, 475, -543, 680, 251, 6, -128],
            "D4K cambió")
    m = difference_matrix(3) + difference_matrix(4)
    rank_without_q = rank_q(m)
    rank_with_q = rank_q(m + [[1] * 12])
    require((rank_without_q, rank_with_q, q) == (11, 12, 6263), "rangos E90/120 inesperados")
    upstream_text = (N32_DIR / "hmt_n32_upstream_u12_gauge_scan.py").read_text(encoding="utf-8")
    closeout_text = (N32_DIR / "hmt_n32_referee_closure.py").read_text(encoding="utf-8")
    require("does not produce the signed dodecaphase witness U12sgn" in upstream_text,
            "el escáner N32 ya no declara su alcance")
    require("U_BLOCK_1" in closeout_text and "[2378, -452, -668, -322]" in closeout_text,
            "el cierre N32 ya no congela U firmado como input")
    return {
        "status": "PASS_CONDITIONAL_CLOSURE",
        "K": K,
        "U12_signed": interleaved,
        "D3K": b90,
        "D4K": b120,
        "Q": q,
        "rank_D3_D4": rank_without_q,
        "rank_D3_D4_Q": rank_with_q,
        "closed_maps": ["K<->H12(K)=U12_signed", "K<->(D3K,D4K,Q)"],
        "N32_scan_scope": "APP_min two-cursor catalogue -> U6 (and periodic unsigned U6||U6)",
        "enriched_model_scope": (
            "TPK-full declares U12_signed as a primitive signed coordinate; current "
            "certificates do not extract it from a seed or from a raw 108-tick ledger"
        ),
        "N32_closeout_scope": (
            "N32 takes frozen U12_signed as input and certifies the downstream "
            "Hadamard K roundtrip and the D3/D4/Q chart"
        ),
        "reduction_theorem_scope": (
            "a seed -> raw108 -> twelve-sector aggregator -> U12_signed realization is "
            "not established by the current corpus and cannot be imported as a premise "
            "of K<->U12_signed"
        ),
    }


def source_layering_audit() -> dict:
    """Distingue ejecutable APP_min de ledger enriquecido EF--G9.

    La clasificación no invalida el segundo: registra que su estatus matemático
    correcto es el de estado tipado del protocolo completo. APP_min es la
    proyección que elimina campos y no puede sustituir a su dominio.
    """
    scan = F053_SCAN.read_text(encoding="utf-8")
    tex = F053_TEX.read_text(encoding="utf-8")
    f013_summary = json.loads((F013_DIR / "summary.json").read_text(encoding="utf-8"))
    n72_tex = (N72_DIR / "N72_supervivencia_coinductiva_novena_puerta.tex").read_text(
        encoding="utf-8"
    )
    n72_header = (N72_DIR / "N72_coinductive_survival_profile_t5_t25_h9.csv").read_text(
        encoding="utf-8"
    ).splitlines()[0]
    n75 = N75.read_text(encoding="utf-8")

    f053_only_u6 = (
        "FLIPS_U6 = {27, 54}" in scan
        and "U6_to_count" in scan
        and "unique_U6" in scan
        and "2378" not in scan
        and "U12_signed" not in scan
    )
    f053_tex_adds_signed = (
        "2378,1406,2479,-452" in tex and "En la realizaci" in tex
    )
    f013_has_no_generator = not any(F013_DIR.glob("*.py"))
    f013_uses_sample_ledger = (
        "sample_output_12triads" in f013_summary.get("source_basis", "")
    )
    n72_has_no_generator = not any(N72_DIR.glob("*.py"))
    n72_uses_actual_trace = "actual_rows" in n72_header and "actual_chain_count" in n72_header
    n72_declares_finite = "auditoría finita" in n72_tex
    n75_defines_inverse_limit = "rama de límite inverso" in n75
    checks = {
        "F053_executable_emits_only_U6_catalogue": f053_only_u6,
        "F053_tex_then_introduces_signed_U12": f053_tex_adds_signed,
        "F013_contains_no_generator_script": f013_has_no_generator,
        "F013_declares_sample_output_ledger_basis": f013_uses_sample_ledger,
        "N72_contains_no_generator_script": n72_has_no_generator,
        "N72_tables_mark_actual_trace": n72_uses_actual_trace,
        "N72_declares_finite_audit": n72_declares_finite,
        "N75_defines_number_as_inverse_limit_branch": n75_defines_inverse_limit,
    }
    require(all(checks.values()), f"cambió la jerarquía documental: {checks}")
    return {
        "status": "PASS_LAYERED_MODEL_CLASSIFICATION",
        "checks": checks,
        "APP_min_executable_layer": (
            "F053 certifies 104976 -> 468 U6 states. It does not compute the signed "
            "dodecaphase witness later printed by its companion TeX."
        ),
        "TPK_full_EF_G9_layer": (
            "frontier signature, Hensel/cylinder state, carry, route ledgers and the "
            "survival relation form a typed protocol state; U12_signed is a separately "
            "declared primitive coordinate"
        ),
        "theorem_inside_enriched_model": (
            "given the typed extension relation, finite survival and the conditional "
            "inverse-limit uniqueness theorem are legitimate mathematical results"
        ),
        "separate_realization_question": (
            "no current certificate realizes seed -> raw108 -> aggregator -> U12_signed; "
            "that realization is separate from the exact downstream charts"
        ),
        "publication_rule": (
            "state explicitly which fields each layer retains, never cite the F053 U6 scan "
            "as the complete signed state, and label the N72 window as finite evidence"
        ),
    }


def publication_contract_audit() -> dict:
    """Bloquea las dos sobreafirmaciones de tipos detectadas en revisión."""

    tpk = BODY_TPK.read_text(encoding="utf-8")
    objects = BODY_OBJECTS.read_text(encoding="utf-8")
    number = BODY_NUMBER.read_text(encoding="utf-8")
    readme = V3_README.read_text(encoding="utf-8")
    contract = THESIS_CONTRACT.read_text(encoding="utf-8")
    logic_audit = LOGIC_AUDIT.read_text(encoding="utf-8")
    logic_audit_flat = " ".join(logic_audit.split())
    core_claims = json.loads(CORE_CLAIMS.read_text(encoding="utf-8"))
    core_by_id = {row["id"]: row for row in core_claims["claims"]}
    checks = {
        "U12_is_declared_primitive_coordinate": (
            "declara como primitiva una coordenada dodecafásica" in tpk
        ),
        "raw108_aggregator_certificate_explicitly_absent": (
            "no contiene un certificado que" in tpk
            and r"\text{semilla}\longmapsto L_{108}^{\rm raw}" in tpk
        ),
        "N32_scope_stops_at_U6": (
            "N32/F053 se detiene en el catálogo" in tpk
            and "no extrae" in tpk
        ),
        "false_certificate_inventory_removed": (
            "la salida firmada antes de aplicar Hadamard o diferencias" not in tpk
        ),
        "dependent_enrichment_fibres_declared": (
            r"\mathsf E_a=" in objects
            and r"\mathsf H_a\times\mathsf C_a\times\mathsf S_a\times\mathsf\Lambda_a"
            in objects
        ),
        "carry_cocycle_law_typed": (
            r"\kappa(r_2\circ r_1)" in objects
            and r"\mathsf C(r_2)\bigl(\kappa(r_1)\bigr)" in objects
        ),
        "global_route_category_declared": (
            r"\mathsf P_{\rm surv}" in number
            and r"\mathsf E_{j+1,j}" in number
            and r"\mathsf G_{\rm surv}" in number
        ),
        "local_carry_not_mistyped_as_cocycle": (
            "La coordenada $c_m$ no es por sí sola un cociclo" in number
        ),
        "old_theorem_local_groupoid_placeholder_removed": (
            "grupoide de estados y transiciones declarado en cada teorema" not in number
        ),
        "README_preserves_upstream_scope": (
            "coordenada primitiva declarada" in readme
            and "semilla--raw108--agregador" in readme
        ),
        "thesis_contract_preserves_upstream_scope": (
            "coordenada primitiva" in contract
            and "semilla--raw108--agregador" in contract
        ),
        "logic_audit_preserves_upstream_scope": (
            "no contiene un certificado que ejecute la cadena semilla" in logic_audit_flat
            and "N32 closeout toma" in logic_audit_flat
        ),
        "canonical_TPK_claim_preserves_upstream_scope": (
            "coordenada primitiva separada" in core_by_id["TPK-FULL-001"]["statement"]
            and "no ejecutan una cadena semilla->raw108->agregador->U12sgn"
            in core_by_id["TPK-FULL-001"]["statement"]
        ),
    }
    require(all(checks.values()), f"regresión en el contrato de publicación: {checks}")
    return {"status": "PASS_PUBLICATION_TYPE_CONTRACT", "checks": checks}


def route_and_deep_state_audit() -> dict:
    newso = NEWSO.read_text(encoding="utf-8")
    f006 = F006.read_text(encoding="utf-8")
    f054 = F054.read_text(encoding="utf-8")
    checks = {
        "newso_dp_receives_target": "def dp_min_turn_route(target:" in newso,
        "newso_targets_recomputed_from_pi_e_phi_definitions": (
            "assert targets_81 == reference_ternary_targets()" in newso
        ),
        "old_nal_has_G9_G36_5_23": (
            "G–9 (memoria)" in f054 and "G–\\(\\{3,6\\}\\)" in f054 and "5,23" in f054
        ),
        "old_nal_executable_has_fallback_completion": "completa con los menores restantes" in f006,
        "old_x0_certificate_declares_oracle": "This uses the constant as an oracle" in f006,
        "old_wtz_writes_alpha_directly": "10^{3t}\\alpha" in f054,
        "old_wtz_freezes_A_1000alpha": "A = 10^3 * alpha" in f054,
    }
    require(all(checks.values()), f"cambió la evidencia de procedencia: {checks}")
    return {
        "status": "PASS_CLASSIFICATION",
        "checks": checks,
        "G9_G36_5_23_scope": (
            "upstream event-index sampler on four cardinal routes; it neither derives L0/L1 "
            "nor selects the deep Hensel state x0"
        ),
        "WTZ_scope": (
            "a target-conditioned checksum/acceptance construction: its event writer contains "
            "alpha explicitly and therefore cannot certify an upstream derivation of alpha"
        ),
        "NEWSO_scope": (
            "minimum-turn witness routes conditioned on ternary targets recomputed from the "
            "definitions of pi, e and phi; valid existence witnesses, not autonomous generation"
        ),
        "deep_x0_scope": (
            "x0 mod 3 follows from w6 and A inverse; x0 mod 3^T in the historical JSON is "
            "back-reconstructed from the target word and explicitly labelled oracle"
        ),
    }


def main() -> None:
    result = {
        "overall_status": "PASS_WITH_EXPLICIT_MODEL_LAYERING",
        "APP_phase_convention": app_audit(),
        "typed_468_to_243_chain": catalogue_audit(),
        "target_free_two_cursor_engine": two_cursor_target_free_audit(),
        "L0_L1_interpolation": lift_interpolation_audit(),
        "historical_APP_to_L0_claim": historical_app_to_l0_claim_audit(),
        "four_cursor_TPK_raw_to_K": four_cursor_mask_audit(),
        "K_and_signed_U12": k_audit(),
        "APP_min_vs_TPK_full_EF_G9": source_layering_audit(),
        "publication_type_contract": publication_contract_audit(),
        "routes_WTZ_and_deep_x0": route_and_deep_state_audit(),
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
