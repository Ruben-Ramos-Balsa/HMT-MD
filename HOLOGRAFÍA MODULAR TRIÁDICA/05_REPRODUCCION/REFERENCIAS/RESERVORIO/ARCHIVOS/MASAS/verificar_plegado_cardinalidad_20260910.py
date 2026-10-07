#!/usr/bin/env python3
"""Controles exactos focales. No ejecuta el generador HMT ni demuestra CH.

La prueba para profundidad arbitraria está en la nota adjunta. Los árboles
de este programa son instancias declaradas de control, no censos del TPK.
No modifica archivos. Salida: JSON por stdout.
"""
from fractions import Fraction
from itertools import product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def degree(prefix):
    """Grado variable de control, no selector causal atribuido al TPK."""
    return 1 + (len(prefix) + sum((i + 1) * a for i, a in enumerate(prefix))) % 3


def refinement_control(max_depth=9):
    # prefix, weight, magnification, integer address, ancestral degree list
    level = [((), Fraction(1), 1, 0, ())]
    nodes = 0
    edges = 0
    for depth in range(max_depth + 1):
        require(sum((v[1] for v in level), Fraction()) == 1, "total de pesos")
        following = []
        for prefix, w, mag, q, degrees in level:
            nodes += 1
            require(w * mag == 1, "dualidad w M")
            require(Fraction(q + 1, mag) - Fraction(q, mag) == w, "longitud")
            # Recuperación del código con su secuencia de grados conservada.
            restored = []
            last_q = q
            for d in reversed(degrees):
                last_q, a = divmod(last_q, d)
                restored.append(a)
            require(last_q == 0, "residuo inicial de dirección")
            require(tuple(reversed(restored)) == prefix, "reconstrucción de ruta")
            if depth == max_depth:
                continue
            d = degree(prefix)
            children = []
            for a in range(d):
                child = (prefix + (a,), w / d, mag * d, q * d + a, degrees + (d,))
                children.append(child)
                following.append(child)
                edges += 1
                left = Fraction(child[3], child[2])
                right = Fraction(child[3] + 1, child[2])
                require(Fraction(q, mag) <= left < right <= Fraction(q + 1, mag),
                        "anidamiento")
            require(sum((v[1] for v in children), Fraction()) == w, "conservación local")
            require(children[0][3] * mag == q * children[0][2], "borde izquierdo")
            require(Fraction(children[-1][3] + 1, children[-1][2]) ==
                    Fraction(q + 1, mag), "borde derecho")
            for left_child, right_child in zip(children, children[1:]):
                require(Fraction(left_child[3] + 1, left_child[2]) ==
                        Fraction(right_child[3], right_child[2]), "partición contigua")
        level = following
    return {"depth": max_depth, "nodes": nodes, "edges": edges,
            "scope": "CONTROL_TREE_NOT_TPK_CENSUS", "passed": True}


def neutral_depth_control():
    mag = 1
    for _ in range(100):
        mag *= 1
    require(mag == 1, "grado uno no contrae")
    for n in range(1, 25):
        mag = 3 ** n
        require(Fraction(1, mag) * mag == 1, "refinamiento ternario")
        require(n != mag, "no confundir profundidad y magnificación")
    return {"neutral_steps": 100, "ternary_depth": 24, "passed": True}


def fold_control():
    # Instancia entera de recuperación de bloque y memoria.
    # No identifica este ejemplo con todos los transportes HMT.
    for n in range(1, 10000):
        phase = 1 + (n - 1) % 9
        memory = (n - 1) // 9
        require(9 * memory + phase == n, "reconstrucción fase-cociente")
    registers = {(n % 729, n // 729) for n in range(5000)}
    require(len(registers) == 5000, "registro conjunto")
    for n in range(5000):
        block, memory = n % 729, n // 729
        require(block + 729 * memory == n, "decodificador")
    require(0 % 729 == 729 % 729 and 0 // 729 != 729 // 729,
            "misma fase, distinta memoria")
    return {"phase_reconstructions": 9999, "block_memory_reconstructions": 5000,
            "scope": "INTEGER_ENCODING_CONTROL", "passed": True}


def fusion_control(max_depth=9):
    # Instancia explícita: dos sucesores separados dentro de la subdivisión
    # ternaria. El árbol HMT completo no se reemplaza por este subárbol.
    level = {(): (Fraction(0), Fraction(1))}
    nodes = 1
    for depth in range(1, max_depth + 1):
        following = {}
        for prefix, (left, right) in level.items():
            third = (right - left) / 3
            low = (left, left + third)
            high = (right - third, right)
            require(low[1] < high[0], "separación de valores")
            for a, interval in [(0, low), (1, high)]:
                require(left <= interval[0] < interval[1] <= right, "anidamiento fusión")
                require(interval[1] - interval[0] == Fraction(1, 3 ** depth),
                        "contracción fusión")
                following[prefix + (a,)] = interval
        level = following
        nodes += len(level)
        require(len(level) == 2 ** depth, "censo subfamilia")
    intervals = sorted(level.values())
    for first, second in zip(intervals, intervals[1:]):
        require(first[1] < second[0], "disjunción final")
    return {"depth": max_depth, "nodes": nodes, "terminal_intervals": len(level),
            "scope": "EXPLICIT_FUSION_INSTANCE_NOT_GENERAL_UNCOUNTABILITY_DECIDER",
            "passed": True}


def boundary_transport_control():
    # E en cada nivel es biyectiva: bloque de tres trits y memoria restante.
    # Conserva el código completo y conmuta con restricción.
    def encode(prefix):
        return (prefix[:3], prefix[3:])
    def decode(register):
        return register[0] + register[1]
    tested = 0
    for depth in range(7):
        for prefix in product(range(3), repeat=depth):
            reg = encode(prefix)
            require(decode(reg) == prefix, "inversa del registro")
            if depth:
                restricted = encode(decode(reg)[:-1])
                require(restricted == encode(prefix[:-1]), "naturalidad")
            tested += 1
    return {"prefixes": tested, "scope": "DECLARED_REVERSIBLE_REGISTER_CONTROL",
            "passed": True}


def full_power_transport_control():
    # Todas las partes de un dominio finito; no sólo cilindros.
    source = set(range(7))
    def encode(x):
        return (x % 3, x // 3)
    def decode(y):
        return y[0] + 3 * y[1]
    target = {encode(x) for x in source}
    parts = [{x for x in source if mask & (1 << x)} for mask in range(128)]
    for subset in parts:
        image = {encode(x) for x in subset}
        require({decode(y) for y in image} == subset, "inversa potencia plena")
        require({encode(x) for x in source - subset} == target - image,
                "complementos potencia plena")
    for a in parts:
        for b in parts:
            ea, eb = {encode(x) for x in a}, {encode(x) for x in b}
            require({encode(x) for x in a | b} == ea | eb, "uniones")
            require({encode(x) for x in a & b} == ea & eb, "intersecciones")
    return {"subsets": len(parts), "pairs": len(parts) ** 2,
            "scope": "ALL_SUBSETS_OF_FINITE_CONTROL_DOMAIN", "passed": True}


def main():
    result = {
        "result": "PASS_CONTROLES_FOCALES_PLEGADO_CARDINALIDAD",
        "checks": [refinement_control(), neutral_depth_control(), fold_control(),
                   fusion_control(), boundary_transport_control(),
                   full_power_transport_control()],
        "arbitrary_depth_proof": "PROPOSITIONS_AND_FUSION_PROOF_IN_COMPANION_NOTE",
        "ambient_universal_ch_proved": False,
        "relative_ch_in_L_h": "SOURCE_THEOREM_NOT_VERIFIED_BY_FINITE_TESTS",
        "full_tpk_generator_executed": False,
        "historical_sources_modified": False,
        "pdfs_modified": False,
        "external_constant_targets": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
