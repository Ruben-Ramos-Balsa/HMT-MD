#!/usr/bin/env python3
"""Certificado autocontenido de rutas NEWSO, CT108/243 y cierre NSEO.

Separa tres capas que en los borradores históricos compartían notación:
rutas espaciales N/E/S/O sobre APP; rotor dodecafásico D108; y corrientes
aritméticas N/E/S/O con acarreo base 1000. No requiere dependencias externas.
"""

from __future__ import annotations

import csv
import json
from decimal import Decimal, localcontext
from pathlib import Path


OUT = Path(__file__).resolve().parent
DIRS = ("N", "E", "S", "O")
VEC = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
NONE = 4


def dr9(n: int) -> int:
    r = n % 9
    return 9 if r == 0 else r


APP_SUM = [[dr9((i + 1) + (j + 1)) for j in range(9)] for i in range(9)]
APP_PROD = [[dr9((i + 1) * (j + 1)) for j in range(9)] for i in range(9)]


def is_door(t: int) -> bool:
    return t % 9 in (3, 6, 0)


def dp_min_turn_route(target: str, length: int, seed: tuple[int, int, int]):
    """Devuelve una ruta de coste mínimo con la semilla fijada."""
    wanted = [int(c) for c in target]
    assert len(wanted) == length // 3
    door_req = [None] * (length + 1)
    k = 0
    for t in range(1, length + 1):
        if is_door(t):
            door_req[t] = wanted[k]
            k += 1

    i0, j0, m0 = seed
    current = {(i0, j0, m0, NONE): 0}
    previous = {}
    for t in range(1, length + 1):
        next_cost = {}
        next_prev = {}
        req = door_req[t]
        for (i, j, mode, last_dir), cost in current.items():
            for d_idx, direction in enumerate(DIRS):
                di, dj = VEC[direction]
                ni, nj = (i + di) % 9, (j + dj) % 9
                digit = APP_SUM[ni][nj] if mode == 0 else APP_PROD[ni][nj]
                trit = digit % 3
                if req is not None and trit != req:
                    continue
                new_mode = 0 if trit == 1 else 1 if trit == 2 else mode
                new_cost = cost + int(last_dir != NONE and last_dir != d_idx)
                state2 = (ni, nj, new_mode, d_idx)
                if state2 not in next_cost or new_cost < next_cost[state2]:
                    next_cost[state2] = new_cost
                    next_prev[state2] = ((i, j, mode, last_dir), d_idx)
        if not next_cost:
            raise RuntimeError(f"No hay ruta admisible en t={t}")
        current = next_cost
        for state2, value in next_prev.items():
            previous[(t, state2)] = value

    end_state, cost = min(current.items(), key=lambda item: (item[1], item[0]))
    route_idx = []
    state = end_state
    for t in range(length, 0, -1):
        state1, d_idx = previous[(t, state)]
        route_idx.append(d_idx)
        state = state1
    route_idx.reverse()
    assert state[:3] == seed and state[3] == NONE
    return cost, [DIRS[d] for d in route_idx]


def simulate(route, seed, target):
    i, j, mode = seed
    rows, emitted = [], []
    target_i = 0
    for t, direction in enumerate(route, 1):
        old_i, old_j, old_mode = i, j, mode
        di, dj = VEC[direction]
        i, j = (i + di) % 9, (j + dj) % 9
        digit = APP_SUM[i][j] if mode == 0 else APP_PROD[i][j]
        trit = digit % 3
        door = is_door(t)
        expected = ""
        if door:
            expected = int(target[target_i])
            assert trit == expected
            emitted.append(trit)
            target_i += 1
        mode = 0 if trit == 1 else 1 if trit == 2 else mode
        rows.append([t, direction, old_i, old_j, old_mode, i, j, mode,
                     digit, trit, int(door), expected])
    assert "".join(map(str, emitted)) == target
    return rows


def ternary_prefix_to_triads(target: str, number_of_triads: int):
    numerator = int(target, 3)
    denominator = 3 ** len(target)
    encoded = (numerator * (1000 ** number_of_triads)) // denominator
    text = f"{encoded:0{3 * number_of_triads}d}"
    return [int(text[3 * i:3 * i + 3]) for i in range(number_of_triads)]


def pi_chudnovsky(precision: int) -> Decimal:
    """Pi por Chudnovsky, usado sólo para auditar la cola ternaria."""
    with localcontext() as ctx:
        ctx.prec = precision + 30
        c = Decimal(426880) * Decimal(10005).sqrt()
        m, ell, x, k = 1, 13591409, 1, 6
        series = Decimal(ell)
        for n in range(1, precision // 14 + 4):
            m = (m * (k ** 3 - 16 * k)) // (n ** 3)
            ell += 545140134
            x *= -262537412640768000
            series += Decimal(m * ell) / Decimal(x)
            k += 12
        return +(c / series)


def first_ternary_digits(value: Decimal, count: int) -> str:
    with localcontext() as ctx:
        ctx.prec = 150
        x = +value
        x -= int(x)
        out = []
        for _ in range(count):
            x *= 3
            digit = int(x)
            out.append(str(digit))
            x -= digit
        return "".join(out)


def reference_ternary_targets() -> dict[str, str]:
    with localcontext() as ctx:
        ctx.prec = 150
        values = {
            "pi": pi_chudnovsky(140),
            "e": Decimal(1).exp(),
            "phi": (Decimal(1) + Decimal(5).sqrt()) / Decimal(2),
        }
        return {name: first_ternary_digits(value, 81)
                for name, value in values.items()}


def rotor_d108():
    route = []
    for block in range(9):
        beta = (4 * block) % 12
        for m in range(12):
            route.append((len(route) + 1, block, beta, ((m + beta) % 12) + 1))
    assert len(route) == 108
    return route


def h4(block):
    a, b, c, d = block
    return [a + b + c + d, a + b - c - d,
            a - b + c - d, a - b - c + d]


def carry_nseo(pi, ee, phi, seal):
    """E=pi, N=e, O=phi, S=sello; acarreo de derecha a izquierda."""
    out = [0] * 12
    carries = [0] * 13
    rows = []
    for k in range(11, -1, -1):
        x = pi[k] + ee[k] - phi[k] - seal[k] + carries[k + 1]
        out[k] = x % 1000
        carries[k] = x // 1000
        rows.append([k + 1, pi[k], ee[k], phi[k], seal[k],
                     carries[k + 1], x, out[k], carries[k]])
    rows.reverse()
    return out, carries, rows


def write_csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    targets_81 = {
        "pi": "010211012222010211002111110221222220111201212121200121100100101222022212012012111",
        "e": "201101121221102011012222102011021222201202222210212212020112112221110001202222112",
        "phi": "121200112202121020010210010200102011221021200221110110010122112002100021000120211",
    }
    assert targets_81 == reference_ternary_targets()
    seeds = {"pi": (2, 3, 0), "e": (1, 8, 0), "phi": (6, 6, 1)}
    expected_costs = {
        108: {"pi": 15, "e": 18, "phi": 17},
        # Reauditoría con los 81 trits ternarios exactos, semilla fijada y
        # orden de desempate N,E,S,O. Corrige 35/40/45 de una nota histórica.
        243: {"pi": 35, "e": 37, "phi": 40},
    }
    expected_triads = {
        "pi": [141, 592, 653, 589, 793, 238, 462, 643, 383, 279, 502, 884],
        "e": [718, 281, 828, 459, 45, 235, 360, 287, 471, 352, 662, 497],
        "phi": [618, 33, 988, 749, 894, 848, 204, 586, 834, 365, 638, 117],
    }

    route_report, all_route_rows = {}, []
    for length in (108, 243):
        for name in ("pi", "e", "phi"):
            target = targets_81[name][:length // 3]
            cost, route = dp_min_turn_route(target, length, seeds[name])
            assert cost == expected_costs[length][name], (length, name, cost)
            rows = simulate(route, seeds[name], target)
            all_route_rows.extend([[name, length] + row for row in rows])
            route_report[f"{name}_{length}"] = {
                "seed": list(seeds[name]), "turns": cost,
                "door_trits": target, "route": "".join(route),
            }

    triads = {name: ternary_prefix_to_triads(target, 12)
              for name, target in targets_81.items()}
    assert triads == expected_triads

    seal = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
    alpha, carries, carry_rows = carry_nseo(
        triads["pi"], triads["e"], triads["phi"], seal
    )
    expected_alpha = [7, 297, 352, 569, 283, 800, 997, 285, 105, 472, 380, 663]
    assert alpha == expected_alpha

    blocks = [seal[0::3], seal[1::3], seal[2::3]]
    harmonics = [h4(block) for block in blocks]
    signed = [harmonics[m % 3][m // 3] for m in range(12)]
    expected_signed = [2378, 1406, 2479, -452, 998, -551,
                       -668, -204, -371, -322, -28, -997]
    assert signed == expected_signed

    write_csv(
        OUT / "rutas_newso_108_243.csv",
        ["channel", "length", "tick", "direction", "i_before", "j_before",
         "mode_before", "i_after", "j_after", "mode_after", "digit",
         "trit", "is_door", "target_trit"], all_route_rows,
    )
    write_csv(OUT / "rotor_dodecafasico_D108.csv",
              ["tick", "block", "beta", "sector"], rotor_d108())
    write_csv(
        OUT / "acarreo_NSEO_alpha.csv",
        ["sector", "E_pi", "N_e", "O_phi", "S_seal", "carry_right",
         "x", "alpha_triad", "carry_left"], carry_rows,
    )

    certificate = {
        "schema": "HMT.NEWSO.CT108-243.v1",
        "status": "PASS",
        "routes": route_report,
        "triads_from_81_door_trits": triads,
        "ternary_targets_recomputed_from_definitions": True,
        "stability_bound": {
            "numerator": 1000 ** 12,
            "denominator": 3 ** 81,
            "strictly_less_than_one": 1000 ** 12 < 3 ** 81,
        },
        "rotor_D108_length": len(rotor_d108()),
        "seal_K": seal,
        "H4_blocks": harmonics,
        "signed_U12": signed,
        "NSEO": {
            "assignment": {"E": "pi", "N": "e", "O": "phi", "S": "seal_K"},
            "direction": "right-to-left", "carries": carries,
            "alpha_triads": alpha,
            "alpha_decimal": "0." + "".join(f"{x:03d}" for x in alpha),
        },
    }
    (OUT / "certificado_newso_ct108_243.json").write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PASS — NEWSO/CT108/243, D108, H4 y acarreo NSEO verificados")


if __name__ == "__main__":
    main()
