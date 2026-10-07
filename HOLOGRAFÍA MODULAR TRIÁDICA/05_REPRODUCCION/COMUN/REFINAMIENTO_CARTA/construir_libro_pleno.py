#!/usr/bin/env python3
"""Instancia prospectiva APP -> TRIT -> TPK-full -> S12.

La construccion no recibe U, K, Cterm, alfa ni coordenadas terminales esperadas.
Materializa una seccion determinista de los mapas activos que estaban tipados
pero no reunidos en un unico ejecutor:

* calendario C108 y selector tritico M_ph;
* dos cursores APP por ruta y transporte cardinal, con inversion cada 27 pasos;
* division euclidea noadica, carry, winding, memoria vertical y ledger;
* cilindros ternario--decimales exactos y prueba de supervivencia;
* corona/interior en la carta 3x3 de macro-celdas;
* incidencias F90 y F120 con una orientacion finita, declarada y falsable;
* bloque incidencial z y lectura orbital S12 = H12 z.

Estatuto: FORMALIZACION_NUEVA.  No se identifica por decreto con la seccion
terminal historica publicada.  Sus invariantes y perturbaciones se certifican
sin consultar una expectativa numerica.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Any


ROUTE_ORDER = ("N", "E", "S", "O")
DEFAULT_SEEDS = {
    "N": ((0, 0), (-1, 0)),
    "E": ((0, 3), (0, 1)),
    "S": ((3, 0), (1, 0)),
    "O": ((3, 3), (0, -1)),
}
H_ACTIVE = (1, 2, 4, 5, 7, 8)
O_PHASE = tuple(range(1, 9))
ACTIVE_PAIRS = tuple(combinations(H_ACTIVE, 2))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sign(value: int) -> int:
    return (value > 0) - (value < 0)


def selector(phase: int) -> int:
    if phase in (1, 4, 7):
        return 1
    if phase in (2, 5, 8):
        return -1
    return 0


def dr9(value: int) -> tuple[int, int]:
    residue = 1 + (value - 1) % 9
    return residue, (value - residue) // 9


def rho3_oriented(value: int) -> int:
    residue = value % 3
    return 0 if residue == 0 else (1 if residue == 1 else -1)


def encode_trits(values: list[int]) -> int:
    require(len(values) == 6, "un bloque ternario contiene seis trits")
    inverse_oriented = {0: 0, 1: 1, -1: 2}
    result = 0
    for value in values:
        result = 3 * result + inverse_oriented[value]
    return result


def move(position: tuple[int, int], direction: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    raw_i = position[0] + direction[0]
    raw_j = position[1] + direction[1]
    winding = (
        -1 if raw_i < 0 else (1 if raw_i >= 9 else 0),
        -1 if raw_j < 0 else (1 if raw_j >= 9 else 0),
    )
    return (raw_i % 9, raw_j % 9), winding


def negate(direction: tuple[int, int]) -> tuple[int, int]:
    return -direction[0], -direction[1]


def position_text(position: tuple[int, int]) -> str:
    return f"{position[0]},{position[1]}"


def vector_text(vector: tuple[int, int] | list[int]) -> str:
    return ",".join(str(value) for value in vector)


def macro_boundary(position: tuple[int, int]) -> tuple[str, int]:
    """8+1 decomposition of the chosen 3x3 macro-cell chart.

    The local coordinates are i=3a+a', j=3b+b'.  The unique macro-cell
    (a,b)=(1,1) is interior; the other eight form the crown.  This realizes
    the historical phrase 'borde exterior ... patron 3x3' as a falsable
    chart predicate, rather than guessing from a desired terminal digit.
    """
    macro = position[0] // 3, position[1] // 3
    if macro == (1, 1):
        return "interior", -1
    return "crown", 1


@dataclass
class Cursor:
    position: tuple[int, int]
    direction: tuple[int, int]


@dataclass
class Cylinder:
    N: int = 0
    L: int = 0
    D: int = 0
    K_triads: int = 0
    A: int = 0
    B: int = 1
    pending_trits: list[int] = field(default_factory=list)
    emitted: list[int] = field(default_factory=list)

    def append_trit(self, trit: int) -> dict[str, Any]:
        self.pending_trits.append(trit)
        if len(self.pending_trits) < 6:
            return {"block": False, "u6": "", "delta": ""}

        u6 = encode_trits(self.pending_trits)
        self.pending_trits.clear()
        old_N, old_L, old_D, old_K, old_A = self.N, self.L, self.D, self.K_triads, self.A
        new_N = 729 * old_N + u6
        new_L = old_L + 6

        no_emit_A = 729 * old_A + u6 * (1000 ** old_K)
        require(
            no_emit_A == new_N * (1000 ** old_K) - old_D * (3 ** new_L),
            "fallo de la recurrencia de cilindro sin emision",
        )

        denominator = 3 ** new_L
        scale = 1000 ** (old_K + 1)
        lower_prefix = (new_N * scale) // denominator
        upper_prefix = (((new_N + 1) * scale) - 1) // denominator
        delta: int | None = None

        if lower_prefix == upper_prefix and lower_prefix // 1000 == old_D:
            delta = lower_prefix % 1000
            new_D = 1000 * old_D + delta
            new_K = old_K + 1
            new_A = (
                729000 * old_A
                + u6 * (1000 ** (old_K + 1))
                - delta * 729 * (3 ** old_L)
            )
            require(
                new_A == new_N * (1000 ** new_K) - new_D * (3 ** new_L),
                "fallo de la recurrencia de cilindro con emision",
            )
            self.emitted.append(delta)
        else:
            new_D, new_K, new_A = old_D, old_K, no_emit_A

        new_B = new_A + 1000 ** new_K
        require(new_A < 3 ** new_L and new_B > 0, "extension de cilindro no superviviente")
        self.N, self.L, self.D, self.K_triads, self.A, self.B = (
            new_N,
            new_L,
            new_D,
            new_K,
            new_A,
            new_B,
        )
        return {"block": True, "u6": u6, "delta": "" if delta is None else delta}


@dataclass
class RouteState:
    name: str
    plus: Cursor
    times: Cursor
    last_active_sheet: str = "sum"
    carry: int = 0
    winding: list[int] = field(default_factory=lambda: [0, 0])
    memory_turn: int = 0
    ledger: list[dict[str, Any]] = field(default_factory=list)
    cylinder: Cylinder = field(default_factory=Cylinder)


def initial_routes(seeds: dict[str, tuple[tuple[int, int], tuple[int, int]]]) -> dict[str, RouteState]:
    """Diagonal lift X9 -> X9^2 of each historical route seed."""
    routes: dict[str, RouteState] = {}
    for name in ROUTE_ORDER:
        position, direction = seeds[name]
        routes[name] = RouteState(
            name=name,
            plus=Cursor(position, direction),
            times=Cursor(position, direction),
        )
    return routes


def route_tick(state: RouteState, tick: int) -> tuple[dict[str, Any], dict[str, Any]]:
    phase = 1 + (tick - 1) % 9
    sector = 1 + (tick - 1) // 9
    selected = selector(phase)
    orientation_epoch = -1 if ((tick - 1) // 27) % 2 else 1
    memory_before = state.memory_turn
    # Natural unfolded multiplicity of the vertical-memory sheet: it is the
    # unique affine normalization w(0)=1, w(q+1)=w(q)+1 under Gamma_9.
    incidence_multiplicity = 1 + memory_before
    plus_before = state.plus.position
    times_before = state.times.position
    plus_direction_before = state.plus.direction
    times_direction_before = state.times.direction
    winding_increment = (0, 0)

    if selected == 1:
        state.last_active_sheet = "sum"
        state.plus.position, winding_increment = move(state.plus.position, state.plus.direction)
        eval_position = state.plus.position
        raw = (eval_position[0] + 1) + (eval_position[1] + 1)
        sheet = "sum"
    elif selected == -1:
        state.last_active_sheet = "product"
        state.times.position, winding_increment = move(state.times.position, state.times.direction)
        eval_position = state.times.position
        raw = (eval_position[0] + 1) * (eval_position[1] + 1)
        sheet = "product"
    else:
        # El umbral no borra el estado: conserva la ultima hoja para localizar
        # la frontera, pero publica el representante noadico 9 y carry cero.
        cursor = state.plus if state.last_active_sheet == "sum" else state.times
        eval_position = cursor.position
        raw = 9
        sheet = "threshold"

    digit, quotient = dr9(raw)
    local_trit = rho3_oriented(digit)
    transported_trit = orientation_epoch * local_trit
    state.carry += quotient
    state.winding[0] += winding_increment[0]
    state.winding[1] += winding_increment[1]
    boundary_kind, boundary_sign = ("not-nine", 0)
    if digit == 9:
        boundary_kind, boundary_sign = macro_boundary(eval_position)

    cylinder_event = state.cylinder.append_trit(transported_trit)

    phase_return = phase == 9
    if phase_return:
        state.memory_turn += 1

    if tick % 27 == 0:
        state.plus.direction = negate(state.plus.direction)
        state.times.direction = negate(state.times.direction)

    record = {
        "id": f"{state.name}:{tick}",
        "route": state.name,
        "tick": tick,
        "sector": sector,
        "phase": phase,
        "selector": selected,
        "orientation_epoch": orientation_epoch,
        "sheet": sheet,
        "sum_before": position_text(plus_before),
        "sum_after": position_text(state.plus.position),
        "product_before": position_text(times_before),
        "product_after": position_text(state.times.position),
        "sum_direction_before": vector_text(plus_direction_before),
        "sum_direction_after": vector_text(state.plus.direction),
        "product_direction_before": vector_text(times_direction_before),
        "product_direction_after": vector_text(state.times.direction),
        "eval_position": position_text(eval_position),
        "raw": raw,
        "digit": digit,
        "quotient9": quotient,
        "local_trit": local_trit,
        "transported_trit": transported_trit,
        "carry_total": state.carry,
        "winding_increment": vector_text(winding_increment),
        "winding_total": vector_text(state.winding),
        "boundary": boundary_kind,
        "boundary_sign": boundary_sign,
        "memory_turn": state.memory_turn,
        "memory_turn_before": memory_before,
        "phase_return": int(phase_return),
        "ledger_length": len(state.ledger) + 1,
        "cylinder_block": int(cylinder_event["block"]),
        "cylinder_u6": cylinder_event["u6"],
        "emitted_triad": cylinder_event["delta"],
        "cylinder_N": state.cylinder.N,
        "cylinder_L": state.cylinder.L,
        "cylinder_D": state.cylinder.D,
        "cylinder_K_triads": state.cylinder.K_triads,
        "cylinder_A": state.cylinder.A,
        "cylinder_B": state.cylinder.B,
        "inc_A": int(digit in (1, 3, 5, 7)),
        "inc_V": boundary_sign if digit == 9 else 0,
        "multiplicity": incidence_multiplicity,
    }
    state.ledger.append(record)
    signature = {
        "residue": digit,
        "quotient": quotient,
        "carry": state.carry,
        "trit": transported_trit,
        "boundary": boundary_sign,
        "winding": tuple(state.winding),
        "memory_turn": state.memory_turn,
        "ledger_length": len(state.ledger),
    }
    record["signature"] = json.dumps(signature, sort_keys=True, separators=(",", ":"))
    return record, cylinder_event


def incidence_counts(visits: list[dict[str, Any]], first_factors: tuple[int, ...]) -> dict[str, int]:
    """Finite signed incidence realization on F90 or F120.

    For each route and sector, the first factor and the active unordered pair
    select three ledger visits.  Their minimal integral fiber signatures
    (transported TRIT plus quotient/carry increment) are added.  This extends
    the strict compiler's sign-of-sum rule to the active H/C fiber instead of
    discarding its quotient.  Neutral incidences remain visible and are not
    forced into either channel.
    """
    # Minimal integral realization of Sig(h,c,lambda): oriented residue plus
    # the Euclidean quotient/carry increment.  The cumulative carry remains
    # separately in the state and is recoverable from the ledger.
    by_phase = {
        int(visit["phase"]): int(visit["transported_trit"]) + int(visit["quotient9"])
        for visit in visits
    }
    require(set(by_phase) == set(range(1, 10)), "faltan fases en una ventana")
    multiplicities = {int(visit["multiplicity"]) for visit in visits}
    require(len(multiplicities) == 1, "la ventana cruza dos hojas de memoria vertical")
    multiplicity = multiplicities.pop()
    counts = {
        "positive": 0, "negative": 0, "neutral": 0, "total": 0,
        "weighted_positive": 0, "weighted_negative": 0, "weighted_neutral": 0,
    }
    for first in first_factors:
        for left, right in ACTIVE_PAIRS:
            orientation = sign(by_phase[first] + by_phase[left] + by_phase[right])
            key = "positive" if orientation > 0 else ("negative" if orientation < 0 else "neutral")
            counts[key] += 1
            counts["weighted_" + key] += multiplicity
            counts["total"] += 1
    return counts


def hadamard_orbital(blocks: list[int]) -> list[int]:
    require(len(blocks) == 12, "S12 necesita doce bloques")
    output = [0] * 12
    for r in range(3):
        a, b, c, d = (blocks[r + 3 * j] for j in range(4))
        output[r] = a + b + c + d
        output[r + 3] = a + b - c - d
        output[r + 6] = a - b + c - d
        output[r + 9] = a - b - c + d
    return output


def transverse(blocks: list[int]) -> dict[str, list[int] | int]:
    return {
        "b90": [blocks[m] - blocks[(m + 3) % 12] for m in range(12)],
        "b120": [blocks[m] - blocks[(m + 4) % 12] for m in range(12)],
        "Q": sum(blocks),
    }


def pi_h(channels: dict[str, list[int] | int]) -> list[int]:
    b90 = list(channels["b90"])
    b120 = list(channels["b120"])
    total = int(channels["Q"])
    sums_b = [sum(b120[r + 3 * j] for j in range(4)) for r in range(3)]
    numerator = total + 2 * sums_b[0] + sums_b[1]
    require(numerator % 3 == 0, "salida transversal incompatible con Pi_H integral")
    orbit_sums = [numerator // 3]
    orbit_sums.append(orbit_sums[0] - sums_b[0])
    orbit_sums.append(orbit_sums[1] - sums_b[1])
    blocks: list[list[int]] = []
    for r in range(3):
        d = [b90[r + 3 * j] for j in range(4)]
        blocks.append([orbit_sums[r], d[1] - d[3], d[0] + d[2], d[0] - d[2]])
    return [blocks[r][column] for column in range(4) for r in range(3)]


def simulate(seeds: dict[str, tuple[tuple[int, int], tuple[int, int]]]) -> dict[str, Any]:
    states = initial_routes(seeds)
    visits: list[dict[str, Any]] = []
    pulse_rows: list[dict[str, Any]] = []
    visible_initial = {
        name: (
            state.plus.position,
            state.times.position,
            state.plus.direction,
            state.times.direction,
        )
        for name, state in states.items()
    }
    visible_snapshots: dict[int, dict[str, Any]] = {}

    for tick in range(1, 109):
        pulse: dict[str, Any] = {
            "tick": tick,
            "sector": 1 + (tick - 1) // 9,
            "phase": 1 + (tick - 1) % 9,
            "selector": selector(1 + (tick - 1) % 9),
            "orientation_epoch": -1 if ((tick - 1) // 27) % 2 else 1,
            "phase_return": int(tick % 9 == 0),
            "orientation_flip": int(tick % 27 == 0),
        }
        for name in ROUTE_ORDER:
            record, _ = route_tick(states[name], tick)
            visits.append(record)
            for key in (
                "sheet", "sum_before", "sum_after", "product_before", "product_after",
                "sum_direction_before", "sum_direction_after", "product_direction_before",
                "product_direction_after", "eval_position", "raw", "digit", "quotient9",
                "local_trit", "transported_trit", "carry_total", "winding_increment",
                "winding_total", "boundary", "boundary_sign", "memory_turn_before", "memory_turn",
                "multiplicity", "ledger_length",
                "cylinder_block", "cylinder_u6", "emitted_triad", "cylinder_N", "cylinder_L",
                "cylinder_D", "cylinder_K_triads", "cylinder_A", "cylinder_B", "signature",
            ):
                pulse[f"{name}_{key}"] = record[key]
        pulse_rows.append(pulse)
        if tick in (54, 108):
            visible_snapshots[tick] = {
                name: (
                    states[name].plus.position,
                    states[name].times.position,
                    states[name].plus.direction,
                    states[name].times.direction,
                )
                for name in ROUTE_ORDER
            }

    sector_rows: list[dict[str, Any]] = []
    z: list[int] = []
    for sector in range(1, 13):
        sector_visits = [visit for visit in visits if int(visit["sector"]) == sector]
        raw_A = sum(int(visit["inc_A"]) * int(visit["multiplicity"]) for visit in sector_visits)
        raw_V = sum(int(visit["inc_V"]) * int(visit["multiplicity"]) for visit in sector_visits)
        count_keys = (
            "positive", "negative", "neutral", "total",
            "weighted_positive", "weighted_negative", "weighted_neutral",
        )
        f90 = {key: 0 for key in count_keys}
        f120 = {key: 0 for key in count_keys}
        for route in ROUTE_ORDER:
            route_visits = [visit for visit in sector_visits if visit["route"] == route]
            route_90 = incidence_counts(route_visits, H_ACTIVE)
            route_120 = incidence_counts(route_visits, O_PHASE)
            for key in f90:
                f90[key] += route_90[key]
                f120[key] += route_120[key]
        raw_C = f120["weighted_negative"] - f120["weighted_positive"]
        residues = (raw_A % 10, raw_C % 10, raw_V % 10)
        block = 100 * residues[0] + 10 * residues[1] + residues[2]
        z.append(block)
        sector_rows.append({
            "sector": sector,
            "visits": len(sector_visits),
            "A_raw": raw_A,
            "C_raw": raw_C,
            "V_raw": raw_V,
            "A_mod10": residues[0],
            "C_mod10": residues[1],
            "V_mod10": residues[2],
            "z": block,
            "F90_positive": f90["positive"],
            "F90_negative": f90["negative"],
            "F90_neutral": f90["neutral"],
            "F90_total": f90["total"],
            "F90_weighted_positive": f90["weighted_positive"],
            "F90_weighted_negative": f90["weighted_negative"],
            "F90_weighted_neutral": f90["weighted_neutral"],
            "F120_positive": f120["positive"],
            "F120_negative": f120["negative"],
            "F120_neutral": f120["neutral"],
            "F120_total": f120["total"],
            "F120_weighted_positive": f120["weighted_positive"],
            "F120_weighted_negative": f120["weighted_negative"],
            "F120_weighted_neutral": f120["weighted_neutral"],
        })

    channels = transverse(z)
    s12_direct = hadamard_orbital(z)
    s12_via_channels = pi_h(channels)
    require(s12_direct == s12_via_channels, "fallo de la identidad Pi_H o H12")

    return {
        "states": states,
        "visits": visits,
        "pulses": pulse_rows,
        "sectors": sector_rows,
        "z": z,
        "channels": channels,
        "S12": s12_direct,
        "visible_initial": visible_initial,
        "visible_snapshots": visible_snapshots,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    require(bool(rows), f"tabla vacia: {path.name}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verification(result: dict[str, Any]) -> dict[str, Any]:
    states: dict[str, RouteState] = result["states"]
    require(len(result["pulses"]) == 108, "la tabla no contiene 108 pulsos")
    require(len(result["visits"]) == 432, "el libro no contiene 4x108 visitas")
    require(len(result["sectors"]) == 12, "el registro no contiene doce sectores")
    require(all(row["F90_total"] == 4 * 90 for row in result["sectors"]), "fallo cardinal F90")
    require(all(row["F120_total"] == 4 * 120 for row in result["sectors"]), "fallo cardinal F120")
    require(result["visible_snapshots"][54] == result["visible_initial"], "Fobs^54 no retorno")
    require(result["visible_snapshots"][108] == result["visible_initial"], "Fobs^108 no retorno")
    require(all(state.memory_turn == 12 for state in states.values()), "memoria no avanzo doce vueltas")
    require(all(len(state.ledger) == 108 for state in states.values()), "ledger de ruta incompleto")
    require(all(state.cylinder.L == 108 for state in states.values()), "cilindro no conserva 108 trits")
    require(all(state.cylinder.A < 3 ** state.cylinder.L and state.cylinder.B > 0 for state in states.values()), "cilindro terminal no superviviente")
    require(pi_h(result["channels"]) == result["S12"], "S12 no cierra por los canales")

    # Falsador de constancia/fixture: una perturbacion de semilla se ejecuta con
    # la misma regla y debe modificar la salida generada.
    perturbed = dict(DEFAULT_SEEDS)
    perturbed["N"] = ((0, 1), DEFAULT_SEEDS["N"][1])
    alternate = simulate(perturbed)
    require(
        alternate["z"] != result["z"] or alternate["S12"] != result["S12"],
        "el productor ignora una perturbacion de semilla",
    )

    return {
        "status": "PASS_INSTANCIA_TPK_FULL_S12_TARGET_FREE",
        "counts": {"pulses": 108, "routes": 4, "visits": 432, "sectors": 12},
        "observable_return": {"tick54": True, "tick108": True},
        "memory_not_reset": {
            name: {"turns": state.memory_turn, "carry": state.carry, "ledger_length": len(state.ledger)}
            for name, state in states.items()
        },
        "incidence_cardinals_per_sector": {"F90": 360, "F120": 480},
        "cylinder_survival": True,
        "pi_h_equals_orbital_hadamard": True,
        "seed_perturbation_changes_output": True,
        "target_values_used": False,
        "forbidden_inputs": ["U", "K", "Cterm", "alpha", "terminal_expected_values"],
    }


def public_result(result: dict[str, Any], checks: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    files = {
        "script": output_dir / "construir_libro_pleno.py",
        "pulses": output_dir / "pulsos_108.csv",
        "visits": output_dir / "visitas_432.csv",
        "sectors": output_dir / "sectores_12.csv",
    }
    return {
        "status": checks["status"],
        "provenance_status": "FORMALIZACION_NUEVA",
        "causal_chain": "APP->TRIT->TPK-full->R12/incidences->z->S12",
        "input": {
            "route_seeds": {
                name: {"position": list(DEFAULT_SEEDS[name][0]), "direction": list(DEFAULT_SEEDS[name][1])}
                for name in ROUTE_ORDER
            },
            "seed_lift": "diagonal X9 -> X9^2 for the two APP cursors",
            "target_values_used": False,
        },
        "formalized_maps": {
            "boundary": "macro=(floor(i/3),floor(j/3)); interior iff macro=(1,1), crown otherwise",
            "visit_multiplicity": "w(q_mem)=q_mem+1, the affine unfolding w(0)=1 and w(q+1)=w(q)+1 under Gamma9",
            "F90": "H_active x P2(H_active)",
            "F120": "O_phase x P2(H_active)",
            "incidence_orientation": "sign of the sum of three minimal fiber signatures (transported local TRIT + quotient9); neutral stays neutral",
            "C_sector": "#negative F120 incidences - #positive F120 incidences",
            "z_sector": "100[A]_10+10[C]_10+[V]_10",
            "S12": "P_orb^-1 (H4+H4+H4) P_orb z",
        },
        "blocks_z": result["z"],
        "transverse_channels": result["channels"],
        "S12": result["S12"],
        "terminal_route_state": {
            name: {
                "sum_position": list(state.plus.position),
                "product_position": list(state.times.position),
                "sum_direction": list(state.plus.direction),
                "product_direction": list(state.times.direction),
                "carry": state.carry,
                "winding": state.winding,
                "memory_turn": state.memory_turn,
                "ledger_length": len(state.ledger),
                "cylinder": {
                    "N": state.cylinder.N, "L": state.cylinder.L,
                    "D": state.cylinder.D, "decimal_triad_depth": state.cylinder.K_triads,
                    "A": state.cylinder.A, "B": state.cylinder.B,
                    "emitted_triads": state.cylinder.emitted,
                },
            }
            for name, state in result["states"].items()
        },
        "verification": checks,
        "file_sha256": {name: sha256(path) for name, path in files.items()},
        "scope": {
            "claim": "numeric target-free instance of the declared HMT full-state maps",
            "not_claimed": "identity with the historically published canonical terminal section",
            "falsifier": "change a seed, boundary chart, incidence orientation, or fiber section and rerun; outputs must be recomputed",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    result = simulate(DEFAULT_SEEDS)
    checks = verification(result)
    if not args.verify_only:
        write_csv(output_dir / "pulsos_108.csv", result["pulses"])
        write_csv(output_dir / "visitas_432.csv", result["visits"])
        write_csv(output_dir / "sectores_12.csv", result["sectors"])
        payload = public_result(result, checks, output_dir)
        with (output_dir / "resultado.json").open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    print(checks["status"])
    print("z=" + json.dumps(result["z"], separators=(",", ":")))
    print("S12=" + json.dumps(result["S12"], separators=(",", ":")))


if __name__ == "__main__":
    main()
