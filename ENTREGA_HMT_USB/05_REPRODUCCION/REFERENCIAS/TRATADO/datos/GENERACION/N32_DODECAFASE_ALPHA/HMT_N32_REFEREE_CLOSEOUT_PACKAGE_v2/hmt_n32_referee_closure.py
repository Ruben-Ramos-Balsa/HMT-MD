#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HMT — N32 Referee Closeout (single certificate)

This script generates ONE unified certificate that closes three typical
referee requests, without using α anywhere in the *definition* of the internal
mask K_{R12}.

Outputs (created next to this script):
  - HMT_N32_ILP_model.lp
  - HMT_N32_certificate.json
  - HMT_N32_MANIFEST.sha256

What is certified:
  (R1) ILP U→K for K_{R12}: explicit U₁₂, explicit ILP, uniqueness argument
       (invertible linear map) + computational verification of constraints.
  (R2) Frozen "seeds/routes" by SHA256 (explicit strings) for:
         • the executed triads of π, e, φ (w36 inputs)
         • the rotor/route in D^{108} induced by β(b)=4b (mod 12)
         • the w6 seeds + permutations (if you use that layer)
  (R3) Clear separation: DEFINITION vs VERIFICATION.
       Verification computes α from (π,e,φ,K_{R12}) by carry R→L base-1000,
       and reports α^{-1}.

No external dependencies.
"""

from __future__ import annotations

import datetime
import hashlib
import json
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Dict, List, Tuple


def require(condition: bool, message: str) -> None:
    """Falla de forma explícita incluso con optimización de Python."""
    if not condition:
        raise RuntimeError(f"N32 CLOSURE FAIL: {message}")


# ----------------------------- SHA256 helpers -----------------------------

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(s: str) -> str:
    return sha256_bytes(s.encode("utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------- linear algebra -----------------------------

def matvec(M: List[List[int]], v: List[int]) -> List[int]:
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def det_recursive(M: List[List[int]]) -> int:
    """Exact determinant for small integer matrices (n<=4 used here)."""
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    total = 0
    for j in range(n):
        # minor matrix removing row 0 and col j
        minor = [row[:j] + row[j + 1 :] for row in M[1:]]
        cofactor = ((-1) ** j) * M[0][j] * det_recursive(minor)
        total += cofactor
    return total


# ----------------------------- HMT constants -----------------------------

# Hadamard H4 (ordering fixed to match N30.5)
H4: List[List[int]] = [
    [1, 1, 1, 1],
    [1, 1, -1, -1],
    [1, -1, 1, -1],
    [1, -1, -1, 1],
]

# Frozen signed U-blocks (length 4); this script does not derive them upstream.
U_BLOCK_1 = [2378, -452, -668, -322]   # (U1,U4,U7,U10)
U_BLOCK_2 = [1406, 998, -204, -28]     # (U2,U5,U8,U11)
U_BLOCK_3 = [2479, -551, -371, -997]   # (U3,U6,U9,U12)

# Expected canonical K_{R12} (triads base-1000)
K_R12_CANONICAL = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]

# Executed w36 triads of constants (first 12 base-1000 triads after decimal)
PI_TRIADS_12  = [141, 592, 653, 589, 793, 238, 462, 643, 383, 279, 502, 884]
E_TRIADS_12   = [718, 281, 828, 459, 45, 235, 360, 287, 471, 352, 662, 497]
PHI_TRIADS_12 = [618, 33, 988, 749, 894, 848, 204, 586, 834, 365, 638, 117]

# Optional w6 seeds + permutations (from debajoAPP.txt)
BASE_U6 = [541, 478, 694, 923, 810, 870]
BASE_SUPPORT_TYPE = "B"
BASE_E_SIG = "933339"
BASE_MOD3_PATTERN = "111200"

W6_SEEDS = {
    "pi":  {"w6": "010211", "P": [4, 0, 5, 3, 1, 2]},
    "e":   {"w6": "121002", "P": [5, 1, 0, 2, 4, 3]},
    "phi": {"w6": "201220", "P": [2, 3, 5, 0, 4, 1]},
}


# ----------------------------- core constructions -----------------------------

def compute_K_block_from_U(U_block: List[int]) -> List[int]:
    """Given U in Z^4, solve H4*K = U.

    Since H4^{-1} = (1/4) H4, we compute K = (H4*U)/4.
    We then reduce mod 1000 into 0..999 (triad-gauge).
    """
    Hu = matvec(H4, U_block)
    if any(x % 4 != 0 for x in Hu):
        raise ValueError(f"H4*U not divisible by 4: U={U_block}, H4U={Hu}")
    K = [(x // 4) % 1000 for x in Hu]
    return K


def assemble_K_R12(K1: List[int], K2: List[int], K3: List[int]) -> List[int]:
    """Interleave the three 4-blocks into the 12-vector K_{R12}.

    Convention (as in N30.5):
      K^(1) indexes positions (1,4,7,10)
      K^(2) indexes positions (2,5,8,11)
      K^(3) indexes positions (3,6,9,12)
    """
    K = [0] * 12
    idx1 = [0, 3, 6, 9]   # 1,4,7,10 in 0-based
    idx2 = [1, 4, 7, 10]  # 2,5,8,11
    idx3 = [2, 5, 8, 11]  # 3,6,9,12
    for t, i in enumerate(idx1):
        K[i] = K1[t]
    for t, i in enumerate(idx2):
        K[i] = K2[t]
    for t, i in enumerate(idx3):
        K[i] = K3[t]
    return K


def assemble_U12_from_blocks(U1: List[int], U2: List[int], U3: List[int]) -> List[int]:
    """Inverse of the partition: recover (U1..U12) in natural order."""
    U = [0] * 12
    idx1 = [0, 3, 6, 9]
    idx2 = [1, 4, 7, 10]
    idx3 = [2, 5, 8, 11]
    for t, i in enumerate(idx1):
        U[i] = U1[t]
    for t, i in enumerate(idx2):
        U[i] = U2[t]
    for t, i in enumerate(idx3):
        U[i] = U3[t]
    return U


def build_rotor_route_D108() -> List[int]:
    """Route (indices in {1..12}) of length 108 induced by β(b)=4b mod 12.

    For each block b=0..8 (9 blocks) and each position m=0..11:
        idx = (m + 4*b) mod 12  -> 1..12
    """
    route: List[int] = []
    for b in range(9):
        beta = (4 * b) % 12
        for m in range(12):
            route.append(((m + beta) % 12) + 1)
    require(len(route) == 108, "la ruta D108 no tiene longitud 108")
    return route


# ----------------------------- carry arithmetic for α (verification only) -----------------------------

def carry_RTL_base1000(pi: List[int], ee: List[int], phi: List[int], K: List[int]) -> List[int]:
    """Compute the 12 triads of α by the carry rule (right-to-left, base 1000).

    This is the *verification* computation used in N30.6:
        A = (π + e − φ − K) with carry right→left in base-1000.

    Returns A as 12 triads in 0..999.
    """
    if not (len(pi) == len(ee) == len(phi) == len(K) == 12):
        raise ValueError("All inputs must have length 12 triads")

    A = [0] * 12
    carry_next = 0
    for i in range(11, -1, -1):
        S = pi[i] + ee[i] - phi[i] - K[i] + carry_next
        carry_k = S // 1000
        digit_k = S - 1000 * carry_k
        A[i] = digit_k
        carry_next = carry_k
    return A


def triads_to_decimal(alpha_triads: List[int]) -> Decimal:
    """0.(triads) in base-1000 as Decimal."""
    getcontext().prec = 200
    x = Decimal(0)
    base = Decimal(1000)
    denom = base
    for t in alpha_triads:
        x += Decimal(int(t)) / denom
        denom *= base
    return x


def format_triads_as_0dot(triads: List[int]) -> str:
    return "0." + "".join(f"{t:03d}" for t in triads)


# ----------------------------- ILP model emission -----------------------------

def write_ilp_model(path: Path, U1: List[int], U2: List[int], U3: List[int]) -> None:
    """Write a plain LP/ILP model that encodes H4*K = U with 0<=K_i<=999."""

    # Variable blocks
    idx1 = [1, 4, 7, 10]
    idx2 = [2, 5, 8, 11]
    idx3 = [3, 6, 9, 12]

    def block_eqs(var_idx: List[int], Ublk: List[int], tag: str) -> List[str]:
        a, b, c, d = var_idx
        # rows of H4
        return [
            f" k{a} + k{b} + k{c} + k{d} = {Ublk[0]}",
            f" k{a} + k{b} - k{c} - k{d} = {Ublk[1]}",
            f" k{a} - k{b} + k{c} - k{d} = {Ublk[2]}",
            f" k{a} - k{b} - k{c} + k{d} = {Ublk[3]}",
        ]

    lines: List[str] = []
    lines.append("\\ ILP model for K_{R12} (HMT N32 referee closeout)")
    lines.append("Minimize")
    lines.append(" obj: 0")
    lines.append("Subject To")

    eqs = []
    eqs += [f" c1_{i+1}: {s}" for i, s in enumerate(block_eqs(idx1, U1, "B1"))]
    eqs += [f" c2_{i+1}: {s}" for i, s in enumerate(block_eqs(idx2, U2, "B2"))]
    eqs += [f" c3_{i+1}: {s}" for i, s in enumerate(block_eqs(idx3, U3, "B3"))]
    lines.extend(eqs)

    lines.append("Bounds")
    for i in range(1, 13):
        lines.append(f" 0 <= k{i} <= 999")

    lines.append("Generals")
    lines.append(" " + " ".join(f"k{i}" for i in range(1, 13)))

    lines.append("End")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ----------------------------- main certificate -----------------------------

def main() -> None:
    out_dir = Path(__file__).resolve().parent

    # R1: compute K from U (no α anywhere)
    K1 = compute_K_block_from_U(U_BLOCK_1)
    K2 = compute_K_block_from_U(U_BLOCK_2)
    K3 = compute_K_block_from_U(U_BLOCK_3)
    K = assemble_K_R12(K1, K2, K3)

    # Validate
    if K != K_R12_CANONICAL:
        raise AssertionError(f"Computed K does not match canonical.\ncomputed={K}\ncanon={K_R12_CANONICAL}")

    # Recover U12 (natural order)
    U12 = assemble_U12_from_blocks(U_BLOCK_1, U_BLOCK_2, U_BLOCK_3)
    require(U12 == [2378, 1406, 2479, -452, 998, -551,
                    -668, -204, -371, -322, -28, -997],
            "observable U12 firmado inesperado")

    # Emit ILP model
    ilp_path = out_dir / "HMT_N32_ILP_model.lp"
    write_ilp_model(ilp_path, U_BLOCK_1, U_BLOCK_2, U_BLOCK_3)

    # Uniqueness evidence (algebraic): det(H4)=±16, so det = det(H4)^3 = ±4096
    det_H4 = det_recursive(H4)
    det_A = det_H4 ** 3
    require(det_H4 == -16, "det(H4) distinto de -16")
    require(det_A == -4096, "det(A) distinto de -4096")

    # R2: freeze seeds/routes by hash
    route108 = build_rotor_route_D108()

    # Strings to freeze
    freeze_payloads: Dict[str, str] = {
        "U12": ",".join(str(x) for x in U12),
        "U_blocks": "|".join(",".join(str(x) for x in blk) for blk in [U_BLOCK_1, U_BLOCK_2, U_BLOCK_3]),
        "K_R12": ",".join(f"{x:03d}" for x in K),
        "route_D108": ",".join(str(i) for i in route108),
        "pi_triads_12": ",".join(f"{x:03d}" for x in PI_TRIADS_12),
        "e_triads_12": ",".join(f"{x:03d}" for x in E_TRIADS_12),
        "phi_triads_12": ",".join(f"{x:03d}" for x in PHI_TRIADS_12),
        "base_U6": ",".join(str(x) for x in BASE_U6),
        "base_mod3_pattern": BASE_MOD3_PATTERN,
        "base_support_type": BASE_SUPPORT_TYPE,
        "base_E_sig": BASE_E_SIG,
        "w6_pi": json.dumps(W6_SEEDS["pi"], separators=(",", ":")),
        "w6_e": json.dumps(W6_SEEDS["e"], separators=(",", ":")),
        "w6_phi": json.dumps(W6_SEEDS["phi"], separators=(",", ":")),
    }

    freeze_hashes = {k: sha256_text(v) for k, v in freeze_payloads.items()}

    # Optional: include Golay hexads csv hash if present
    golay_csv = out_dir / "golay_hexads_S_5_6_12.csv"
    golay_csv_sha = sha256_file(golay_csv) if golay_csv.exists() else None

    # R3 verification: compute α and α^{-1} from (π,e,φ,K) by carry
    alpha_triads = carry_RTL_base1000(PI_TRIADS_12, E_TRIADS_12, PHI_TRIADS_12, K)
    require(alpha_triads == [7, 297, 352, 569, 283, 800,
                             997, 285, 105, 472, 380, 663],
            "acarreo finito de alpha inesperado")
    alpha_dec = triads_to_decimal(alpha_triads)
    getcontext().prec = 200
    alpha_inv_dec = (Decimal(1) / alpha_dec)

    # Prepare certificate JSON
    cert: Dict[str, Any] = {
        "schema": "HMT.N32.referee_closeout.v1",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc)
        .isoformat(timespec="seconds").replace("+00:00", "Z"),
        "files": {},
        "R1_ILP_U_to_K": {
            "U_blocks": {"U1": U_BLOCK_1, "U2": U_BLOCK_2, "U3": U_BLOCK_3},
            "U12": U12,
            "H4": H4,
            "det_H4": det_H4,
            "det_A": det_A,
            "K_blocks": {"K1": K1, "K2": K2, "K3": K3},
            "K_R12": K,
            "uniqueness_note": (
                "A is a row/column permutation of blockdiag(H4,H4,H4), hence det(A)=det(H4)^3≠0. "
                "Therefore A*K=U has at most one rational solution. Since the computed solution is integer and "
                "satisfies 0≤K_i≤999, the ILP feasible set has exactly one point."
            ),
        },
        "R2_frozen_seeds_routes": {
            "payloads": freeze_payloads,
            "sha256": freeze_hashes,
            "golay_hexads_csv_sha256": golay_csv_sha,
        },
        "R3_verification_alpha": {
            "alpha_triads": alpha_triads,
            "alpha_decimal_string": format_triads_as_0dot(alpha_triads),
            "alpha_inverse_decimal_prefix": str(alpha_inv_dec)[:32],
        },
    }

    # Record file hashes
    this_path = Path(__file__).resolve()
    cert["files"][this_path.name] = sha256_file(this_path)
    cert["files"][ilp_path.name] = sha256_file(ilp_path)

    # Write certificate
    cert_path = out_dir / "HMT_N32_certificate.json"
    cert_path.write_text(json.dumps(cert, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cert["files"][cert_path.name] = sha256_file(cert_path)

    # Manifest
    manifest_path = out_dir / "HMT_N32_MANIFEST.sha256"
    manifest_lines = []
    for fname, h in sorted(cert["files"].items()):
        manifest_lines.append(f"{h}  {fname}")
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # Console summary (minimal)
    print("[OK] K_R12 canonical reproduced exactly.")
    print("[OK] ILP model written:", ilp_path)
    print("[OK] Certificate written:", cert_path)
    print("[OK] Manifest written:", manifest_path)
    print("PASS — cierre N32 U12/K/alpha verificado")


if __name__ == "__main__":
    main()
