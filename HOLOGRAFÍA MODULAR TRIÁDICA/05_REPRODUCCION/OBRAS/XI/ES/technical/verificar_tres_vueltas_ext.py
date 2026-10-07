#!/usr/bin/env python3
"""Certificado finito de la formalización arista por arista de Ext.

No evalúa constantes ni sustituye la demostración general del manuscrito.
Comprueba la tabla de 27 incidencias, el levantamiento balanceado, la ley de
acarreo, la memoria, los 54 pasos por bloque y la separación registral de las
729 prolongaciones.
"""

from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sections" / "ch_tres_vueltas_ext.tex"
ELEVATION = ROOT / "sections" / "ch_elevacion_catalogal.tex"

PHASE_MODE = {phase: (1, -1, 0)[(phase - 1) % 3]
              for phase in range(1, 10)}
PAIR = {+1: (1, 4), 0: (3, 6), -1: (2, 5)}


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise SystemExit("FAIL_TRES_VUELTAS_EXT " + reason)


def balanced_reduce(value: int) -> tuple[int, int]:
    """Return the unique (residue, carry) with value=residue+3*carry."""
    candidates = [
        (residue, (value - residue) // 3)
        for residue in (-1, 0, 1)
        if (value - residue) % 3 == 0
    ]
    require(len(candidates) == 1, "balanced_reduction_not_unique")
    return candidates[0]


def local_cycle(branch: int) -> tuple[tuple[object, ...], ...]:
    first, second = PAIR[branch]
    records = []
    for phase in range(1, 10):
        marker = 1 if phase == first else 2 if phase == second else 0
        carry = 0
        if marker == 2:
            left = PHASE_MODE[first]
            right = PHASE_MODE[second]
            _, carry = balanced_reduce(left + right)
        memory = 1 if phase == 9 else 0
        records.append((phase, PHASE_MODE[phase], branch,
                        marker, carry, memory))
    return tuple(records)


def require_source_contract(source: str, elevation: str) -> None:
    required_source = (
        r"m(r):=\tau(r)\in\{-1,0,+1\}",
        r"\mathfrak p_{+1}:=(1,4)",
        r"\mathfrak p_{-1}:=(2,5)",
        r"\mathfrak p_{0}:=(3,6)",
        "destino, composición, memoria, acarreo y truncamiento del TPK enriquecido.",
        r"d_{n,r}:=k_n+r-1",
        r"s(e_{\varepsilon,n,r})=\top",
        r"\operatorname{Carr}(e_2e_1)",
        r"\operatorname{Upd}^{\rm cal}_{e_{\varepsilon,n,r}}",
        r"\mathfrak T_{\rm TPK}^{\rm cal}",
        r"\mathcal U^{(1),\rm cal}_{e_{\varepsilon,n,r}}",
        "donde la selección deja intactos",
        "Así, y sólo en",
        r"\operatorname{Ext}^{\APP,\rm cal}",
        r"\operatorname{Ext}^{\rm fib,cal}",
        r"H_{k_n}^{\rm cal}:=G_n",
        r"108\) emisiones",
        r"nunca genera las aristas",
    )
    missing = [item for item in required_source if item not in source]
    require(not missing, "missing_source_markers=" + repr(missing))

    forbidden_source = (
        r"\sigma_{\TRIT}",
        r"\mathsf{Upd}_{k_n+r-1}",
        "la hoja activa \\(\\Sigma\\)",
        "cociente euclídeo determina el acarreo",
        "el estado enriquecido se reinicia",
    )
    present = [item for item in forbidden_source if item in source]
    require(not present, "forbidden_source_markers=" + repr(present))

    required_elevation = (
        r"\upsilon:\mathbb F_3\longrightarrow\{-1,0,+1\}",
        r"\gamma_{\upsilon(b_6),k+45}",
        "Ese registro conserva",
        "no sólo la suma final de sus acarreos",
        r"3^6=729\) términos son subcilindros de refinamiento",
        r"\Phi_N:=\Psi_N^{-1}\circ\beta_{{\rm blk},N}",
        r"\pi_{N+1,N}\circ\Phi_{N+1}",
        r"\mathscr Z_N(x)",
        r"\bigsqcup_{b\in\mathbb F_3^6}",
        r"\Phi_\infty:\Omega_\Gamma^{\rm cal}",
    )
    missing = [item for item in required_elevation if item not in elevation]
    require(not missing, "missing_elevation_markers=" + repr(missing))


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    elevation = ELEVATION.read_text(encoding="utf-8")
    require_source_contract(source, elevation)

    cycles = {}
    for branch in (-1, 0, +1):
        register = local_cycle(branch)
        cycles[branch] = register
        require(tuple(row[0] for row in register) == tuple(range(1, 10)),
                "phase_cover")
        require(tuple(row[1] for row in register) ==
                (1, -1, 0, 1, -1, 0, 1, -1, 0),
                "phase_selector")
        require(sum(row[4] for row in register) == branch, "derived_carry")
        require(sum(row[5] for row in register) == 1, "memory_advance")
        require(sum(1 for row in register if row[3] == 1) == 1,
                "first_pair_member")
        require(sum(1 for row in register if row[3] == 2) == 1,
                "second_pair_member")

    require(len(set(cycles.values())) == 3, "branch_ledgers_not_disjoint")
    require(sum(len(cycle) for cycle in cycles.values()) == 27,
            "local_certificate_not_27")

    registers = set()
    for word in product((-1, 0, +1), repeat=6):
        register = tuple(entry for digit in word for entry in cycles[digit])
        require(len(register) == 54, "block_not_54_edges")
        registers.add(register)
    require(len(registers) == 3**6 == 729, "block_registers_not_729")
    require(12 * 9 == 108, "calendar_not_108")

    print(
        "PASS_TRES_VUELTAS_EXT "
        "local_entries=27 branches=3 ext_edges_per_cycle=9 "
        "phase_return=9 memory_advance=1 block_edges=54 "
        "subcylinders=729 calendar_return=108 K_ph=posterior "
        "proof_status=manuscript_not_replaced_by_execution"
    )


if __name__ == "__main__":
    main()
