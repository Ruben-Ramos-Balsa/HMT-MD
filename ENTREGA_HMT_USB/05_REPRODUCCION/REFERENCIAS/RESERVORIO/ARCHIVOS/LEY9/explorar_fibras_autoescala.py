"""Fibras exactas del carácter de autoescala del envolvente modal HMT.

Dominio: paseos dirigidos finitos, con extremos, longitud y repeticiones.
No certifica que todo paseo del envolvente admita elevación al TPK completo.
No utiliza cifras de phi, constantes físicas, bibliotecas numéricas ni targets.
"""
from __future__ import annotations
from collections import defaultdict
from functools import lru_cache
import argparse
import hashlib
import json
from pathlib import Path

def modal_incidence():
    # U014: + selecciona Sigma, - selecciona Pi, 0 conserva el modo.
    cycles = []
    for initial in (0, 1):
        mode = initial
        states = []
        for trit in (1, -1, 0):
            if trit == 1:
                mode = 0
            elif trit == -1:
                mode = 1
            states.append(mode)
        cycles.append(tuple(states))
    if cycles[0] != cycles[1]:
        raise AssertionError("La lectura modal depende del arranque descartado")
    cycle = cycles[0]
    matrix = [[0, 0], [0, 0]]
    for i, j in zip(cycle, cycle[1:] + cycle[:1]):
        matrix[i][j] += 1
    return cycle, tuple(tuple(row) for row in matrix)

MODES, INCIDENCE = modal_incidence()
IDENTITY = ((1, 0), (0, 1))

def matrix_product(a, b):
    return tuple(tuple(sum(a[i][h]*b[h][j] for h in range(2))
                       for j in range(2)) for i in range(2))

@lru_cache(None)
def matrix_power(n):
    if n < 0:
        raise ValueError("La longitud debe ser no negativa")
    result, base = IDENTITY, INCIDENCE
    while n:
        if n & 1:
            result = matrix_product(result, base)
        base = matrix_product(base, base)
        n //= 2
    return result

def path_exponent(path):
    if not path or any(type(v) is not int or v not in (0, 1) for v in path):
        raise ValueError("Paseo con estados inválidos")
    if any(INCIDENCE[i][j] != 1 for i, j in zip(path, path[1:])):
        raise ValueError("Transición no admisible")
    return len(path) - 1 + path[0] - path[-1]

def fiber_groups(k):
    if type(k) is not int or k < 0:
        raise ValueError("Exponente fuera del dominio")
    groups = []
    for n in range(max(0, k-1), k+2):
        for i in (0, 1):
            for j in (0, 1):
                if n + i - j == k:
                    count = matrix_power(n)[i][j]
                    if count:
                        groups.append((n, i, j, count))
    return tuple(groups)

def fiber_size(k):
    return sum(item[3] for item in fiber_groups(k))

def closed_walks(k):
    power = matrix_power(k)
    return power[0][0] + power[1][1]

def theoretical_fiber_size(k):
    return 3 if k == 0 else 2 * closed_walks(k)

def return_count(path):
    return sum(i == 1 and j == 0 for i, j in zip(path, path[1:]))

def binomial(n, k):
    if k < 0 or k > n:
        return 0
    value = 1
    for j in range(1, min(k, n-k)+1):
        value = value * (n-j+1) // j
    return value

def graded_fiber(k):
    if k == 0:
        return (3,)
    values = []
    for b in range(k//2+1):
        numerator = 2*k*binomial(k-b, b)
        quotient, remainder = divmod(numerator, k-b)
        assert remainder == 0
        values.append(quotient)
    return tuple(values)

def graded_fiber_by_recurrence(k):
    if k == 0:
        return (3,)
    older, previous = (2,), (1,)
    for _ in range(2, k+1):
        out = [0] * max(len(previous), len(older)+1)
        for i, value in enumerate(previous):
            out[i] += value
        for i, value in enumerate(older):
            out[i+1] += value
        older, previous = previous, tuple(out)
    return tuple(2*value for value in previous)

def rank_fixed_endpoints(path):
    end = path[-1]
    rank = 0
    for position, actual in enumerate(path[1:], 1):
        current = path[position-1]
        remaining = len(path)-1-position
        for candidate in range(actual):
            if INCIDENCE[current][candidate]:
                rank += matrix_power(remaining)[candidate][end]
    return rank

def encode(path):
    path = tuple(path)
    k = path_exponent(path)
    n, i, j = len(path)-1, path[0], path[-1]
    offset = 0
    for length, start, end, count in fiber_groups(k):
        if (length, start, end) == (n, i, j):
            return k, offset + rank_fixed_endpoints(path)
        offset += count
    raise AssertionError("La ruta no aparece en su fibra")

def unrank_fixed_endpoints(n, start, end, rank):
    total = matrix_power(n)[start][end]
    if not 0 <= rank < total:
        raise ValueError("Índice fuera del sector")
    path = [start]
    for position in range(n):
        remaining = n-position-1
        for nxt in (0, 1):
            if not INCIDENCE[path[-1]][nxt]:
                continue
            count = matrix_power(remaining)[nxt][end]
            if rank < count:
                path.append(nxt)
                break
            rank -= count
        else:
            raise AssertionError("No hay continuación para el índice")
    if path[-1] != end or rank != 0:
        raise AssertionError("Terminación incompatible")
    return tuple(path)

def decode(k, rank):
    if type(rank) is not int or not 0 <= rank < fiber_size(k):
        raise ValueError("Índice fuera de la fibra")
    for n, i, j, count in fiber_groups(k):
        if rank < count:
            return unrank_fixed_endpoints(n, i, j, rank)
        rank -= count
    raise AssertionError("Índice sin grupo")

def extend(encoded, state):
    path = decode(*encoded)
    return encode(path + (state,))

def restrict(encoded):
    path = decode(*encoded)
    if len(path) == 1:
        raise ValueError("Una ruta trivial no tiene prefijo más corto")
    return encode(path[:-1])

def enumerate_length(n):
    # Enumerador independiente de rank/unrank: recorre el grafo directamente.
    stack = [(0,), (1,)]
    while stack:
        path = stack.pop()
        if len(path) == n+1:
            yield path
        else:
            for state in (1, 0):
                if INCIDENCE[path[-1]][state]:
                    stack.append(path+(state,))

def reject_invalid(call):
    try:
        call()
    except (ValueError, TypeError):
        return True
    raise AssertionError("Control negativo aceptado")

def verify(max_k=15):
    found = defaultdict(set)
    for n in range(max_k+2):
        for path in enumerate_length(n):
            k = path_exponent(path)
            if k <= max_k:
                found[k].add(path)
    checked = 0
    extension_squares = 0
    for k in range(max_k+1):
        paths = found[k]
        assert len(paths) == fiber_size(k) == theoretical_fiber_size(k)
        seen = set()
        graded_counts = defaultdict(int)
        for path in paths:
            b = return_count(path)
            holds = sum(i == j == 1 for i, j in zip(path, path[1:]))
            assert k == 2*b + holds
            graded_counts[b] += 1
            encoded = encode(path)
            assert decode(*encoded) == path
            seen.add(encoded[1])
            for nxt in (0, 1):
                if INCIDENCE[path[-1]][nxt]:
                    child = extend(encoded, nxt)
                    assert child[0]-encoded[0] == 1+path[-1]-nxt
                    assert decode(*child) == path+(nxt,)
                    assert restrict(child) == encoded
                    extension_squares += 1
            checked += 1
        assert seen == set(range(fiber_size(k)))
        expected_graded = graded_fiber(k)
        assert expected_graded == graded_fiber_by_recurrence(k)
        assert tuple(graded_counts[b] for b in range(k//2+1)) == expected_graded
        assert sum(expected_graded) == fiber_size(k)
        for index in range(fiber_size(k)):
            assert encode(decode(k, index)) == (k, index)
    arbitrary_precision_samples = []
    for k in (30, 108, 1000):
        count = fiber_size(k)
        for index in (0, count//2, count-1):
            assert encode(decode(k, index)) == (k, index)
        assert count == theoretical_fiber_size(k)
        arbitrary_precision_samples.append({
            "exponent": k, "fiber_count": str(count),
            "minimal_fixed_width_bits": (count-1).bit_length()
        })
    controls = {
        "forbidden_transition_0_to_0": reject_invalid(lambda: encode((0, 0))),
        "negative_exponent": reject_invalid(lambda: decode(-1, 0)),
        "negative_rank": reject_invalid(lambda: decode(1, -1)),
        "rank_at_upper_bound": reject_invalid(lambda: decode(4, fiber_size(4))),
        "negative_state": reject_invalid(lambda: encode((-1,))),
        "wrong_same_exponent_injectivity": (
            encode((1, 1))[0] == encode((0, 1, 1))[0]
            and encode((1, 1)) != encode((0, 1, 1))
        )
    }
    assert all(controls.values())
    examples = []
    for k in (0, 1, 2, 4):
        examples.append({"exponent": k, "count": fiber_size(k),
                         "first": decode(k, 0), "last": decode(k, fiber_size(k)-1)})
    return {
        "status": "VERIFICADO_EN_DOMINIO_ENVOLVENTE_MODAL",
        "new_formalization_candidate": True,
        "historical_novelty_claimed": False,
        "source_model": "U014: regla modal, incidencia, caracter de Parry",
        "modal_cycle": MODES,
        "incidence": INCIDENCE,
        "step_exponent_increments": {"Sigma_to_Pi": 0, "Pi_to_Pi": 1, "Pi_to_Sigma": 2},
        "formula": "N(0)=3; N(k)=2*trace(F^k) for k>=1",
        "graded_formula": "N(k,b)=2*k*binomial(k-b,b)/(k-b) for k>=1; N(0,0)=3",
        "graded_generating_function": "(3-z+t*z^2)/(1-z-t*z^2)",
        "return_mark": "number of Pi->Sigma transitions; k=2*b+number(Pi->Pi)",
        "exponent_four_counts_by_returns": graded_fiber(4),
        "exhaustive_exponents": [0, max_k],
        "distinct_walks_checked": checked,
        "extension_restriction_squares_checked": extension_squares,
        "negative_controls": controls,
        "examples": examples,
        "large_integer_rank_unrank_samples": arbitrary_precision_samples,
        "scope": {
            "finite_directed_walks": True,
            "all_lengths_covered_by_proof_not_enumeration": True,
            "all_TPK_lifts_proved": False,
            "all_continuum_claims_proved": False,
            "physical_or_thermodynamic_entropy_claimed": False,
            "new_decimal_generation": False,
            "target_constants_used": False,
            "originals_modified": False
        }
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-k", type=int, default=15)
    args = parser.parse_args()
    if not 0 <= args.max_k <= 20:
        parser.error("--max-k debe estar entre 0 y 20 para acotar el censo de control")
    result = verify(args.max_k)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
