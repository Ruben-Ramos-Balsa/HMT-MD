import json, math
from fractions import Fraction


def require(condition: bool, message: str) -> None:
    """Falla de forma explícita incluso si Python se ejecuta con ``-O``."""
    if not condition:
        raise RuntimeError(f"APP_TEOREMAS FAIL: {message}")

def dr9(n:int)->int:
    return n % 9 if n % 9 else 9
M=[[dr9(i*j) for j in range(1,10)] for i in range(1,10)]
A=[[dr9(i+j-1) for j in range(1,10)] for i in range(1,10)]
classes=[[1,4,7],[2,5,8],[3,6,9]]
def block_sums(mat):
    return [[sum(mat[i-1][j-1] for i in c1 for j in c2) for c2 in classes] for c1 in classes]
Sx=block_sums(M)
Sa=block_sums(A)
Qx=[[v//9 for v in row] for row in Sx]
Qa=[[v//9 for v in row] for row in Sa]
D=[[Qx[i][j]-Qa[i][j] for j in range(3)] for i in range(3)]
rad={3,6,9}
union=sum(M[i-1][j-1] for i in range(1,10) for j in range(1,10) if i in rad or j in rad)
inner=sum(M[i-1][j-1] for i in rad for j in rad)
arms=union-inner
B=[[7,2],[2,7]]
det=B[0][0]*B[1][1]-B[0][1]*B[1][0]
eta=0.5*math.log(9/5)
blocks={
    "tau=-1": [[1,8],[8,1]],
    "tau=0": [[4,5],[5,4]],
    "tau=+1": [[7,2],[2,7]],
}
def eig_block(B):
    a,b=B[0]
    return [a+b,a-b]
summary={
    "multiplicative_total": sum(map(sum,M)),
    "additive_total_transport_convention": sum(map(sum,A)),
    "Delta_APP": sum(map(sum,M))-sum(map(sum,A)),
    "S_times_blocks": Sx,
    "Q_times": Qx,
    "Q_plus_transport": Qa,
    "Q_difference": D,
    "trace_difference": D[0][0]+D[1][1]+D[2][2],
    "sum_difference": sum(map(sum,D)),
    "global_defect_from_compression": 9*sum(map(sum,D)),
    "central_block": B,
    "central_eigenvalues": eig_block(B),
    "central_determinant": det,
    "central_rapidity_half_log_9_over_5": eta,
    "two_way_blocks_eigenvalues": {k:eig_block(v) for k,v in blocks.items()},
    "radical_union_sum": union,
    "radical_inner_sum": inner,
    "radical_arms_sum": arms,
    "compression_identities": {"3*72":3*72,"3*27":3*27,"3*99":3*99},
    "central_row_digits": {"72+27":72+27,"72-27":72-27,"77+22":77+22,"77-22":77-22},
}

# Gate matemático explícito sobre los enunciados numéricos de este módulo.
require(summary["multiplicative_total"] == 459, "total multiplicativo")
require(summary["additive_total_transport_convention"] == 405, "total aditivo")
require(summary["Delta_APP"] == 54, "defecto global")
require(summary["Q_times"] == [[4, 5, 6], [5, 4, 6], [6, 6, 9]],
        "compresión multiplicativa")
require(summary["Q_plus_transport"] == [[4, 5, 6], [5, 6, 4], [6, 4, 5]],
        "compresión aditiva")
require(summary["Q_difference"] == [[0, 0, 0], [0, -2, 2], [0, 2, 4]],
        "defecto comprimido")
require(summary["trace_difference"] == 2, "traza del defecto")
require(summary["sum_difference"] == 6, "suma del defecto")
require(summary["global_defect_from_compression"] == 54,
        "recuperación del defecto global")
require(summary["central_eigenvalues"] == [9, 5], "espectro central")
require(summary["central_determinant"] == 45, "determinante central")
require(math.isclose(summary["central_rapidity_half_log_9_over_5"],
                     0.5 * math.log(9 / 5), rel_tol=0.0, abs_tol=1e-15),
        "rapidez central")
require(summary["two_way_blocks_eigenvalues"] == {
    "tau=-1": [9, -7], "tau=0": [9, -1], "tau=+1": [9, 5]
}, "espectros two-way")
require((summary["radical_inner_sum"], summary["radical_arms_sum"],
         summary["radical_union_sum"]) == (81, 216, 297),
        "descomposición radical")
print(json.dumps(summary, indent=2, ensure_ascii=False))
print("PASS — teoremas APP numéricos verificados")
