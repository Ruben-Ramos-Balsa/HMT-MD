#!/usr/bin/env python3
"""Certificado causal de independencia prospectiva de las interfaces HMT--MD.

El programa no consulta ningún catálogo metrológico. Verifica:

1. que los objetivos externos no son antecesores de las salidas internas en
   el DAG declarado;
2. que la intervención simbólica sobre todos los objetivos deja invariantes
   esas salidas, condicionada a la fidelidad y completitud causal del DAG;
3. que las ramas históricamente calibradas quedan fuera del conjunto protegido;
4. los cierres aritméticos y regionales usados por el teorema;
5. un protocolo explícito, falsable y set-valued para futuras interfaces físicas;
6. controles exactos de la completitud reconstructiva de una torre decreciente.

No audita estática ni dinámicamente todas las implementaciones científicas
externas al paquete y no convierte el protocolo multiconjunto en una predicción
ya ejecutada.

Sólo usa la biblioteca estándar y no contiene ``assert``.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "datos" / "interfaces_prospectivas.json"
CATALOG_PATH = ROOT / "certificados" / "catalogo_app_exhaustivo.json"
CHANNELS_PATH = ROOT / "certificados" / "canales_enteros_constantes.json"
CURRENT_PATH = ROOT / "autoridad_consultada" / "CURRENT.json"
CONTRACT_PATH = (
    ROOT / "autoridad_consultada" / "CONTRATO_TESIS_RECTORA_NO_OMITIBLE.md"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def stable_hash(value: Any) -> str:
    raw = json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def resolve_packaged_source(source: str) -> Path:
    """Resuelve una referencia histórica dentro del paquete autocontenido.

    El JSON conserva la procedencia original; esta función no la reescribe,
    sino que exige una residencia empaquetada equivalente y auditable.
    """
    direct = ROOT / source
    if direct.exists():
        return direct
    basename = Path(source).name
    if source.endswith(
        "ADENDA_INDEPENDENCIA_PROSPECTIVA_HMT_MD_2026-07-26_REV_2026-07-26.2/"
        "manuscrito/main.tex"
    ):
        return ROOT / "manuscrito" / "sections" / "md" / "06d_independencia_prospectiva.tex"
    if "/manuscrito/sections/" in source:
        historical_aliases = {
            "09c_persistencia_ruta_mobius_familias.tex":
                "21_persistencia_ruta_mobius_familias_actualizada.tex",
            "09d_bisagra_hojas_pi_phi2.tex":
                "22_bisagra_hojas_pi_phi2_actualizada.tex",
        }
        if basename in historical_aliases:
            return ROOT / "manuscrito" / "sections" / "md" / historical_aliases[basename]
        candidates = sorted((ROOT / "manuscrito" / "sections").rglob(basename))
        if candidates:
            return candidates[0]
    if "/certificados/" in source:
        return ROOT / "certificados" / basename
    if "/pruebas/python/" in source or source.endswith(".py"):
        candidate = ROOT / "pruebas" / "python" / basename
        if candidate.exists():
            return candidate
        if basename == "verificar_alpha_rehecha.py":
            return ROOT / "pruebas" / "python" / "verificar_alpha_dos_vias.py"
    return direct


def determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), "matriz no cuadrada")
    if n == 1:
        return matrix[0][0]
    total = 0
    for j, value in enumerate(matrix[0]):
        minor = [row[:j] + row[j + 1 :] for row in matrix[1:]]
        total += (-1) ** j * value * determinant(minor)
    return total


def minors_gcd(matrix: list[list[int]], order: int) -> int:
    values: list[int] = []
    rows = range(len(matrix))
    cols = range(len(matrix[0]))
    for rs in itertools.combinations(rows, order):
        for cs in itertools.combinations(cols, order):
            sub = [[matrix[i][j] for j in cs] for i in rs]
            values.append(abs(determinant(sub)))
    g = 0
    for value in values:
        g = math.gcd(g, value)
    return g


def dr9(value: int) -> int:
    require(value > 0, "dr9 se usa aquí sólo sobre enteros positivos")
    return 1 + ((value - 1) % 9)


def topological_order(
    node_ids: list[str], edges: list[dict[str, str]]
) -> tuple[list[str], dict[str, list[str]], dict[str, list[str]]]:
    parents: dict[str, list[str]] = defaultdict(list)
    children: dict[str, list[str]] = defaultdict(list)
    indegree = {node: 0 for node in node_ids}
    for edge in edges:
        parent, child = edge["from"], edge["to"]
        require(parent in indegree and child in indegree, "arista con nodo inexistente")
        parents[child].append(parent)
        children[parent].append(child)
        indegree[child] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in sorted(children[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    require(len(order) == len(node_ids), "el grafo causal contiene un ciclo")
    return order, parents, children


def ancestors(node: str, parents: dict[str, list[str]]) -> set[str]:
    result: set[str] = set()
    stack = list(parents[node])
    while stack:
        parent = stack.pop()
        if parent not in result:
            result.add(parent)
            stack.extend(parents[parent])
    return result


def structural_evaluation(
    order: list[str],
    parents: dict[str, list[str]],
    target_nodes: set[str],
    intervention: str,
) -> dict[str, str]:
    """Evalúa el DAG como sistema causal simbólico.

    No pretende sustituir los generadores científicos. Es un control de
    no-interferencia: todos los nodos internos reciben exactamente las mismas
    raíces bajo dos intervenciones incompatibles sobre los blancos.
    """

    result: dict[str, str] = {}
    for node in order:
        parent_values = [(parent, result[parent]) for parent in sorted(parents[node])]
        seed = intervention if node in target_nodes else "FROZEN_INTERNAL_ROOT"
        result[node] = stable_hash(
            {"node": node, "parents": parent_values, "root_seed": seed}
        )
    return result


def verify_graph(spec: dict[str, Any]) -> dict[str, Any]:
    nodes = spec["nodes"]
    ids = [node["id"] for node in nodes]
    require(len(ids) == len(set(ids)), "identificadores de nodo duplicados")
    order, parents, _children = topological_order(ids, spec["edges"])
    kinds = {node["id"]: node["kind"] for node in nodes}
    targets = {node for node, kind in kinds.items() if kind == "external_target"}
    protected = set(spec["protected_outputs"])
    require(protected <= set(ids), "salida protegida inexistente")
    declared = spec["declared_counts"]
    require(len(ids) == declared["nodes"], "recuento de nodos desincronizado")
    require(len(spec["edges"]) == declared["edges"], "recuento de aristas desincronizado")
    require(
        len(protected) == declared["protected_outputs"],
        "recuento de salidas protegidas desincronizado",
    )
    require(
        "BLIND_MULTISET_PROTOCOL_SPEC" in set(ids),
        "falta la especificación del protocolo multiconjunto",
    )
    require(
        "BLIND_MULTISET_PROTOCOL_SPEC" not in protected,
        "un protocolo no ejecutado no puede figurar como salida protegida",
    )
    require(
        set(parents["CHI_MASS_SPECIALIZED"])
        == {"CHI_FORM", "A_RAD", "CSTAR", "DELTA4", "S120", "ZETA270_CORR"},
        "dependencias incompletas de CHI_MASS_SPECIALIZED",
    )
    require(
        "HEXADA_OCTADA_FUNCTIONAL_DECLARED" in parents["GAMMA_6_TO_8"],
        "Gamma_6_to_8 oculta el funcional hexada-octada",
    )
    require(
        "IDEAL_3T_DRIVE_DECLARED" in parents["IDEAL_3T_RESPONSE"],
        "la respuesta 3T oculta el drive declarado",
    )
    require(
        "MINIMUM_INTERACTION_COST_DECLARED" in parents["MINIMUM_INTERACTION_GIBBS"],
        "Gibbs oculta el coste declarado",
    )
    require(
        "SHEET_REPRESENTATION_FACTORIZATION_DECLARED" in parents["SHEET_CONJUGATION"],
        "la conjugación de hojas oculta su representación/factorización",
    )
    require(
        {
            "MASSLESS_SECTOR_SYMMETRY_DECLARED",
            "METROLOGICAL_MASS_TYPE_SCHEMA_DECLARED",
        }
        <= set(parents["BLIND_MULTISET_PROTOCOL_SPEC"]),
        "el protocolo de masas omite el sector nulo o el tipado metrológico",
    )

    contamination: dict[str, list[str]] = {}
    for output in sorted(protected):
        bad = sorted(ancestors(output, parents) & targets)
        if bad:
            contamination[output] = bad
    require(not contamination, f"retroalimentación externa detectada: {contamination}")

    eval_a = structural_evaluation(order, parents, targets, "TARGET_WORLD_A")
    eval_b = structural_evaluation(order, parents, targets, "TARGET_WORLD_B")
    changed_protected = sorted(
        output for output in protected if eval_a[output] != eval_b[output]
    )
    require(not changed_protected, "la intervención alteró una salida protegida")

    comparisons = {
        node
        for node, kind in kinds.items()
        if kind in {"comparison", "calibrated_input", "calibrated_output"}
    }
    changed_comparisons = sorted(
        node for node in comparisons if eval_a[node] != eval_b[node]
    )
    require(
        {
            "ALPHA_RECOGNITION",
            "PLANCK_RECOGNITION",
            "BARBERO_COMPARISON",
            "CKM_COMPARISON",
            "MASS_COMPARISON",
            "GRAVITY_COMPARISON",
            "TIME_CRYSTAL_COMPARISON",
            "P5_CALIBRATED_SELECTION",
            "MASS_SIGNATURE_TABLE_CALIBRATED",
        }
        <= set(changed_comparisons),
        "los controles externos no alcanzan todas las ramas comparativas/calibradas",
    )
    require(
        eval_a["PI_E_PHI_RECOGNITION"] != eval_b["PI_E_PHI_RECOGNITION"],
        "el reconocimiento pi/e/phi debe depender del blanco",
    )

    return {
        "nodes": len(ids),
        "edges": len(spec["edges"]),
        "protected_outputs": len(protected),
        "external_targets": len(targets),
        "topological_order_sha256": stable_hash(order),
        "target_ancestors_of_protected_outputs": contamination,
        "counterfactual_target_worlds_leave_protected_outputs_invariant": True,
        "comparison_or_calibration_nodes_changed": changed_comparisons,
        "scope": "CONDITIONAL_ON_DECLARED_DAG_FIDELITY_AND_COMPLETENESS",
        "dag_assumptions": spec["dag_scope"]["assumptions"],
        "not_certified_by_graph_checker": spec["dag_scope"]["not_certified_by_graph_checker"],
    }


def verify_internal_arithmetic(
    catalog: dict[str, Any], channels: dict[str, Any]
) -> dict[str, Any]:
    app = channels["APP_invariants"]
    require(app["Delta_product_minus_sum"] == 54, "Delta APP incorrecto")
    require(app["S_1_to_9"] == 45, "S=45 incorrecto")
    require(app["kappa"] == 27, "kappa=27 incorrecto")
    require(app["Theta"] == 135, "Theta=135 incorrecto")

    delta, s_value, kappa, theta = 54, 45, 27, 135
    four = {
        "alpha": kappa**2,
        "e": 2 * theta + 1,
        "pi": 2 * theta + s_value,
        "phi": theta + kappa - 1,
    }
    require(four == {"alpha": 729, "e": 271, "pi": 315, "phi": 161}, "cuatrirrelación incorrecta")
    require(1000 == four["alpha"] + four["e"], "completación 1000 incorrecta")
    require(
        four["pi"] + four["e"] + four["phi"] - 3 == 744,
        "cierre 744 incorrecto",
    )
    require(744 == four["alpha"] + 15, "segunda expresión de 744 incorrecta")

    # Generación coinductiva correlacionada con cierre dodecafásico: no es una semejanza decimal,
    # sino una recurrencia afín exacta con cociclo de acarreo.
    p_vec = [141, 592, 653, 589, 793, 238, 462, 643, 383, 279, 502, 884]
    e_vec = [718, 281, 828, 459, 45, 235, 360, 287, 471, 352, 662, 497]
    phi_vec = [618, 33, 988, 749, 894, 848, 204, 586, 834, 365, 638, 117]
    k_vec = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
    carries = [0, 0, 0, -1, -1, -2, -1, 0, -1, -1, 0, 0, 0]
    alpha_triads = [7, 297, 352, 569, 283, 800, 997, 285, 105, 472, 380, 663]
    for index in range(12):
        lhs = (
            p_vec[index]
            + e_vec[index]
            - phi_vec[index]
            - k_vec[index]
            + carries[index + 1]
        )
        rhs = alpha_triads[index] + 1000 * carries[index]
        require(lhs == rhs, f"fallo en la coordenada dodecafásica {index + 1}")
    require(carries[0] == carries[-1] == 0, "el acarreo no telescopa")

    def concatenate_base1000(values: list[int]) -> int:
        result = 0
        for value in values:
            result = 1000 * result + value
        return result

    require(
        concatenate_base1000(p_vec)
        + concatenate_base1000(e_vec)
        - concatenate_base1000(phi_vec)
        - concatenate_base1000(k_vec)
        == concatenate_base1000(alpha_triads),
        "la identidad entera de la generación coinductiva correlacionada no cierra",
    )

    micro = catalog["pi_microfibre"]
    rectangles = micro["rectangles"]
    require(micro["word"] == "010211", "palabra pi incorrecta")
    require(len(rectangles) == 5, "pi no tiene exactamente cinco regiones")
    u6 = [tuple(item["U6"]) for item in rectangles]
    multiplicities = [item["routes"] for item in rectangles]
    require(len(set(u6)) == 5, "las cinco regiones pi no son distintas")
    require(multiplicities == [432, 144, 144, 144, 144], "multiplicidades pi incorrectas")
    require(sum(multiplicities) == 1008 == micro["raw_routes"], "total pi incorrecto")
    require(
        sum(1 for item in rectangles if item["U6"][-3:] == [169, 272, 272]) == 4,
        "el bloque terminal regional 169/272/272 no aparece cuatro veces",
    )
    require(
        rectangles[-1]["U6"][-3:] == [418, 674, 521],
        "terminal de la quinta región incorrecto",
    )
    common_terminal = [169, 272, 272]
    fifth_terminal = rectangles[-1]["U6"][-3:]
    oriented_defect = [
        fifth_terminal[index] - common_terminal[index] for index in range(3)
    ]
    require(
        oriented_defect == [249, 402, 249],
        "defecto orientado de la quinta región incorrecto",
    )

    factor = catalog["global_factorization"]
    require(factor["unique_U6"] == 468, "catálogo U6 incorrecto")
    hist = {int(k): int(v) for k, v in factor["U6_fibre_histogram"].items()}
    require(
        sum(size * count for size, count in hist.items()) == 104_976,
        "censo de semillas incorrecto",
    )

    sum_fibres = Counter(dr9(a + b) for a in range(1, 10) for b in range(1, 10))
    product_fibres = Counter(dr9(a * b) for a in range(1, 10) for b in range(1, 10))
    require(sorted(sum_fibres.values()) == [9] * 9, "fibras aditivas inesperadas")
    require(
        sorted(product_fibres.values(), reverse=True)
        == [21, 12, 12, 6, 6, 6, 6, 6, 6],
        "fibras multiplicativas inesperadas",
    )

    h4 = [
        [1, 1, 1, 1],
        [1, 1, -1, -1],
        [1, -1, 1, -1],
        [1, -1, -1, 1],
    ]
    determinantal_divisors = [minors_gcd(h4, order) for order in range(1, 5)]
    require(determinantal_divisors == [1, 2, 4, 16], "divisores determinantal H4 incorrectos")
    snf = [
        determinantal_divisors[0],
        determinantal_divisors[1] // determinantal_divisors[0],
        determinantal_divisors[2] // determinantal_divisors[1],
        determinantal_divisors[3] // determinantal_divisors[2],
    ]
    require(snf == [1, 2, 2, 4], "SNF(H4) incorrecta")

    alpha_numerator = 7_297_352_569_283_800_997_285_105_472_380_663
    alpha = Fraction(alpha_numerator, 10**36)
    require(
        format(alpha_numerator, "036d")
        == "007297352569283800997285105472380663",
        "numerador exacto de alpha incorrecto",
    )
    # Acotación racional de sqrt(5) a 36 cifras, suficiente para certificar la década.
    sqrt5_low = Fraction(2_236_067_977_499_789_696_409_173_668_731_276, 10**33)
    sqrt5_high = Fraction(2_236_067_977_499_789_696_409_173_668_731_277, 10**33)
    require(sqrt5_low**2 < 5 < sqrt5_high**2, "intervalo racional de sqrt(5) inválido")
    phi_low = (1 + sqrt5_low) / 2
    phi_high = (1 + sqrt5_high) / 2
    sigma_low = phi_low * alpha**16
    sigma_high = phi_high * alpha**16
    require(Fraction(1, 10**34) < sigma_low, "Sigma_H no supera 10^-34")
    require(sigma_high < Fraction(1, 10**33), "Sigma_H no queda por debajo de 10^-33")

    return {
        "APP": {
            "Delta": delta,
            "S": s_value,
            "kappa": kappa,
            "Theta": theta,
            "sum_fibre_sizes": dict(sorted(sum_fibres.items())),
            "product_fibre_sizes": dict(sorted(product_fibres.items())),
        },
        "four_integer_channels": four,
        "dodecaphase_quadrilateral": {
            "identity": "P+E-Phi-K+C_plus-1000C=A",
            "coordinates": 12,
            "carry": carries,
            "telescoping_integer_identity": True,
            "reversible_in_K_given_P_E_Phi_A_and_terminal_carry": True,
        },
        "closure_1000": "1000=729+271",
        "closure_744": "315+271+161-3=744=729+15",
        "catalogue": {
            "seeds": 104_976,
            "U6": 468,
            "visible_words": 243,
        },
        "pi_microfibre": {
            "word": micro["word"],
            "distinct_regions": len(set(u6)),
            "multiplicities": multiplicities,
            "routes": sum(multiplicities),
            "regions": [list(region) for region in u6],
            "common_terminal": common_terminal,
            "fifth_region_terminal": fifth_terminal,
            "oriented_defect": oriented_defect,
        },
        "H4": {
            "determinant": determinant(h4),
            "determinantal_divisors": determinantal_divisors,
            "SNF": snf,
            "cokernel_order": abs(determinant(h4)),
        },
        "alpha_12": {
            "numerator": alpha_numerator,
            "denominator": 10**36,
        },
        "action_order": {
            "strict_lower_bound": "10^-34",
            "strict_upper_bound": "10^-33",
            "certified_by_rational_interval": True,
        },
    }


def nearest_integer_with_lower_tie(value: Fraction) -> int:
    """Entero más próximo; en la semientera exacta elige el menor."""

    lower = value.numerator // value.denominator
    offset = value - lower
    if offset > Fraction(1, 2):
        return lower + 1
    return lower


def verify_tower_completion() -> dict[str, Any]:
    """Controles exactos del algoritmo reconstructivo de torre.

    La demostración general está en el manuscrito. Aquí se comprueban con
    aritmética racional el invariante de residuo, el telescopado y la cota de
    variación total sobre una familia adversarial de residuos. También se
    comprueban las condiciones analíticas de la enumeración creciente de
    <90,120>.
    """

    depth = 80
    a_values = [Fraction(1, 2**k) for k in range(1, depth + 1)]
    residual_inputs = [
        Fraction(7, 5),
        Fraction(-19, 11),
        Fraction(1, 3),
        Fraction(-1, 3),
        Fraction(1, 4),
        Fraction(-1, 4),
        Fraction(0),
    ]
    controls: list[dict[str, Any]] = []
    for initial in residual_inputs:
        residual = initial
        coefficients: list[int] = []
        terms: list[Fraction] = []
        for index, a_k in enumerate(a_values):
            coefficient = nearest_integer_with_lower_tie(residual / a_k)
            term = coefficient * a_k
            residual -= term
            require(
                abs(residual) <= a_k / 2,
                f"falla la cota de residuo en k={index + 1}",
            )
            coefficients.append(coefficient)
            terms.append(term)
        require(
            initial - sum(terms, Fraction(0)) == residual,
            "falla el telescopado reconstructivo",
        )
        absolute_partial_sum = sum((abs(term) for term in terms), Fraction(0))
        generic_bound = abs(terms[0]) + (
            sum(a_values[:-1], Fraction(0)) + sum(a_values[1:], Fraction(0))
        ) / 2
        require(
            absolute_partial_sum <= generic_bound,
            "falla la cota de convergencia absoluta",
        )
        controls.append(
            {
                "input": f"{initial.numerator}/{initial.denominator}",
                "depth": depth,
                "residual_abs_upper_bound": f"1/{2 ** (depth + 1)}",
                "telescoping_exact": True,
                "absolute_partial_sum_bounded": True,
                "coefficient_prefix": coefficients[:12],
            }
        )

    alpha = 0.007297352569283800997285105472380663
    cstar = 2.123738338968645724261951380393
    a_deg = 1000.0 * alpha
    q_plus = math.exp(-math.pi * (a_deg + cstar) / 180.0)
    q_minus = math.exp(-math.pi * (a_deg - cstar) / 180.0)
    require(0.0 < q_plus < q_minus < 1.0, "orden de canales q incorrecto")
    semigroup_prefix = [90, 120] + list(range(180, 180 + 30 * 18, 30))
    generated = sorted(
        {
            90 * a + 120 * b
            for a in range(0, 12)
            for b in range(0, 12)
            if 0 < 90 * a + 120 * b <= semigroup_prefix[-1]
        }
    )
    require(
        generated == semigroup_prefix,
        "la enumeración creciente de <90,120> es incorrecta",
    )
    hmt_terms = [
        q_minus**n_value - q_plus**n_value for n_value in semigroup_prefix
    ]
    require(all(term > 0.0 for term in hmt_terms), "s_(n_k) no es positiva")
    require(
        all(hmt_terms[k] < hmt_terms[k - 1] for k in range(1, len(hmt_terms))),
        "el prefijo de s_(n_k) no decrece",
    )
    infinite_sum = (
        q_minus**90
        + q_minus**120
        + q_minus**180 / (1.0 - q_minus**30)
        - q_plus**90
        - q_plus**120
        - q_plus**180 / (1.0 - q_plus**30)
    )
    require(math.isfinite(infinite_sum) and infinite_sum > 0.0, "suma de torre inválida")

    return {
        "theorem": (
            "For every positive summable a_k tending to zero, nearest-integer "
            "residual recursion reconstructs r; the series is absolutely convergent."
        ),
        "selection_status": "CALIBRATED_WHEN_COEFFICIENTS_READ_THE_TARGET_RESIDUAL",
        "tie_break": "nearest integer; exact half-integer chooses the lower integer",
        "exact_rational_controls": controls,
        "HMT_sequence": {
            "index_set": "<90,120>={90,120,180,210,240,270,300,330,...}",
            "definition": "a_k=s_(n_k)=q_-^(n_k)-q_+^(n_k)",
            "index_prefix": semigroup_prefix,
            "positive_prefix_checked": len(hmt_terms),
            "geometric_sum_finite": True,
            "limit_zero": True,
            "subsequence_90k": "sufficient subfamily, not the principal formulation",
        },
        "domain": "STRICTLY_POSITIVE_RATIOS_ONLY",
        "massless_sector": (
            "Mass zero requires an independent symmetry-protected sector or an "
            "explicit exponent-to-minus-infinity compactification; it is not the "
            "same as an arbitrarily small positive mass."
        ),
        "metrological_type_limit": (
            "The positive character returns one real scalar. It does not by itself "
            "supply widths, complex poles, renormalization running or neutrino "
            "splitting structure."
        ),
    }


def verify_interface_matrix(spec: dict[str, Any]) -> dict[str, Any]:
    interfaces = spec["interfaces"]
    ids = [item["id"] for item in interfaces]
    require(len(ids) == len(set(ids)), "interfaces duplicadas")
    require(ids == [f"IP-{number:02d}" for number in range(1, 17)], "serie IP incompleta")
    valid_status = set(spec["status_vocabulary"])
    require(
        len(interfaces) == spec["declared_counts"]["interfaces"],
        "recuento de interfaces desincronizado",
    )
    source_count = 0
    for interface in interfaces:
        require(interface["status"] in valid_status, "estatuto no declarado")
        for key in ("generator", "target", "independence", "remaining_test", "falsifier"):
            require(str(interface.get(key, "")).strip(), f"{interface['id']} carece de {key}")
        for source in interface["sources"]:
            require(resolve_packaged_source(source).exists(), f"fuente inexistente: {source}")
            source_count += 1
    return {
        "interfaces": len(interfaces),
        "source_references_checked": source_count,
        "all_have_generator_target_independence_delta_and_falsifier": True,
        "semantic_completeness_of_dependencies": "NOT_CERTIFIED_BY_THIS_CHECK",
        "implementation_target_reads": "NOT_AUDITED_OUTSIDE_THIS_PACKAGE",
        "blind_assignment_rule": (
            "Specification only: if several multisections satisfy the non-metrological "
            "constraints, a future execution must emit the full set. No such multiset "
            "is claimed as executed in this revision."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    for path in (SPEC_PATH, CATALOG_PATH, CHANNELS_PATH, CURRENT_PATH, CONTRACT_PATH):
        require(path.is_file(), f"archivo requerido inexistente: {path.name}")
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    channels = json.loads(CHANNELS_PATH.read_text(encoding="utf-8"))
    current = json.loads(CURRENT_PATH.read_text(encoding="utf-8"))
    require(spec["schema"] == "HMT.prospective_interfaces.v2", "schema inesperado")
    require(spec["authority_revision"] == "2026-07-22.2", "autoridad inesperada")
    require(current["revision"] == "2026-07-22.2", "CURRENT no coincide con la adenda")

    result = {
        "schema": "HMT.prospective-interfaces-certificate.v2",
        "status": "PASS_INDEPENDENCIA_PROSPECTIVA_HMT_MD",
        "revision": spec["revision"],
        "authority_revision": spec["authority_revision"],
        "causal_non_interference": verify_graph(spec),
        "exact_internal_controls": verify_internal_arithmetic(catalog, channels),
        "tower_reconstructive_completeness": verify_tower_completion(),
        "interface_matrix": verify_interface_matrix(spec),
        "provenance": {
            "spec_sha256": sha256(SPEC_PATH),
            "catalogue_certificate_sha256": sha256(CATALOG_PATH),
            "integer_channels_certificate_sha256": sha256(CHANNELS_PATH),
            "CURRENT_sha256": sha256(CURRENT_PATH),
            "contract_sha256": sha256(CONTRACT_PATH),
        },
        "interpretation": {
            "proved": (
                "No external target is an ancestor of any protected HMT output in "
                "the declared causal graph; conditional on the fidelity and completeness "
                "of that graph, target interventions leave all protected outputs invariant."
            ),
            "not_claimed": (
                "The graph checker does not prove semantic edge completeness or audit "
                "hidden reads in external scientific implementations. A calibrated "
                "reconstruction is not renamed a prediction, and the blind multiset "
                "object remains a protocol specification that has not been executed."
            ),
        },
    }
    rendered = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print("PASS_INDEPENDENCIA_PROSPECTIVA_HMT_MD")
    print(
        f"nodes={result['causal_non_interference']['nodes']} "
        f"edges={result['causal_non_interference']['edges']} "
        f"interfaces={result['interface_matrix']['interfaces']} "
        f"protected={result['causal_non_interference']['protected_outputs']} "
        "target_ancestors=0 "
        "pi_regions=5 pi_routes=1008 "
        "channels=729,271,315,161 "
        "snf_H4=1,2,2,4 order_action=-34"
    )
    print("certificate_payload_sha256=" + hashlib.sha256(rendered.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
