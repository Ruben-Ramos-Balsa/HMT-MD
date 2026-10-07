import json
import math
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    """Falla de forma explícita incluso si Python se ejecuta con ``-O``."""
    if not condition:
        raise RuntimeError(f"APP_NUCLEO FAIL: {message}")

def dr9(n: int) -> int:
    r = n % 9
    return 9 if r == 0 else r

M = np.array([[dr9((i+1)*(j+1)) for j in range(9)] for i in range(9)], dtype=int)
A = np.array([[dr9((i+1)+(j+1)-1) for j in range(9)] for i in range(9)], dtype=int)
order = np.array([1,4,7,2,5,8,3,6,9]) - 1
Mr = M[order][:, order]
Ar = A[order][:, order]

def block_sums(X):
    return np.array([[X[3*i:3*i+3, 3*j:3*j+3].sum() for j in range(3)] for i in range(3)], dtype=int)

Sx = block_sums(Mr)
Sa = block_sums(Ar)
Qx = Sx // 9
Qa = Sa // 9
D = Qx - Qa
B = np.array([[7,2],[2,7]], dtype=int)
C = Qx[:2,:2]

rad = np.array([2,5,8]) # zero-based rows/cols 3,6,9
units = np.array([0,1,3,4,6,7])
rows_rad_sum = M[rad,:].sum()
cols_rad_sum = M[:,rad].sum()
core_sum = M[np.ix_(rad,rad)].sum()
arms_sum = M[np.ix_(rad,units)].sum() + M[np.ix_(units,rad)].sum()
union_sum = rows_rad_sum + cols_rad_sum - core_sum

summary = {
    "M_total": int(M.sum()),
    "A_total": int(A.sum()),
    "Delta_APP": int(M.sum()-A.sum()),
    "S_multiplicative_blocks": Sx.tolist(),
    "S_additive_blocks": Sa.tolist(),
    "Q_multiplicative": Qx.tolist(),
    "Q_additive": Qa.tolist(),
    "Q_difference": D.tolist(),
    "trace_Qx": int(np.trace(Qx)),
    "trace_Qa": int(np.trace(Qa)),
    "det_Qx": int(round(np.linalg.det(Qx))),
    "eigen_Qx": sorted([float(x) for x in np.linalg.eigvalsh(Qx)]),
    "central_block": B.tolist(),
    "central_eigenvalues": sorted([float(x) for x in np.linalg.eigvalsh(B)]),
    "central_det": int(round(np.linalg.det(B))),
    "compressed_unit_block": C.tolist(),
    "compressed_unit_eigenvalues": sorted([float(x) for x in np.linalg.eigvalsh(C)]),
    "B_minus_C": (B-C).tolist(),
    "radical_rows_sum": int(rows_rad_sum),
    "radical_columns_sum": int(cols_rad_sum),
    "radical_core_sum": int(core_sum),
    "radical_arms_sum": int(arms_sum),
    "radical_union_sum": int(union_sum),
    "identities": {
        "72_plus_27": 72+27,
        "77_plus_22": 77+22,
        "72_minus_27": 72-27,
        "77_minus_22": 77-22,
        "45_plus_54": 45+54,
        "3_times_72": 3*72,
        "3_times_27": 3*27,
        "3_times_99": 3*99,
    },
}

# Gate matemático: no basta con producir tablas.  Estas igualdades fijan la
# convención APP y sus compresiones enteras rectoras.
require(summary["M_total"] == 459, "total multiplicativo distinto de 459")
require(summary["A_total"] == 405, "total aditivo distinto de 405")
require(summary["Delta_APP"] == 54, "defecto APP distinto de 54")
require(summary["S_multiplicative_blocks"] == [[36, 45, 54], [45, 36, 54], [54, 54, 81]],
        "bloques multiplicativos 3x3 inesperados")
require(summary["S_additive_blocks"] == [[36, 45, 54], [45, 54, 36], [54, 36, 45]],
        "bloques aditivos 3x3 inesperados")
require(summary["Q_multiplicative"] == [[4, 5, 6], [5, 4, 6], [6, 6, 9]],
        "compresión multiplicativa inesperada")
require(summary["Q_additive"] == [[4, 5, 6], [5, 6, 4], [6, 4, 5]],
        "compresión aditiva inesperada")
require(summary["Q_difference"] == [[0, 0, 0], [0, -2, 2], [0, 2, 4]],
        "matriz de defecto comprimido inesperada")
require(summary["central_det"] == 45, "determinante central distinto de 45")
require(summary["radical_core_sum"] == 81, "núcleo radical distinto de 81")
require(summary["radical_arms_sum"] == 216, "brazos radicales distintos de 216")
require(summary["radical_union_sum"] == 297, "unión radical distinta de 297")

np.savetxt(OUT/'app_multiplicative.csv', M, delimiter=',', fmt='%d')
np.savetxt(OUT/'app_additive.csv', A, delimiter=',', fmt='%d')
np.savetxt(OUT/'app_block_sums_multiplicative.csv', Sx, delimiter=',', fmt='%d')
np.savetxt(OUT/'app_block_means_multiplicative.csv', Qx, delimiter=',', fmt='%d')
np.savetxt(OUT/'app_block_means_additive.csv', Qa, delimiter=',', fmt='%d')
(OUT/'app_core_summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False))
print(json.dumps(summary, indent=2, ensure_ascii=False))
print("PASS — núcleo APP y compresiones rectoras verificados")
