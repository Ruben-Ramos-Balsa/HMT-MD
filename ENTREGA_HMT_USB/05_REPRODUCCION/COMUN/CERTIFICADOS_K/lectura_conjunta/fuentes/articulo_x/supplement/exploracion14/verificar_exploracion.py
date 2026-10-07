"""Controles exactos de lectores posteriores del registro publicado.

K es un testigo generado archivado del manuscrito de 326 páginas. Este programa
NO reproduce su generación APP--TRIT--TPK, ni incorpora valores metrológicos.
Las pruebas generales y la procedencia se exponen en EXPLORACION.md.
Solo biblioteca estándar; los controles usan excepciones, también con -O.
"""
from fractions import Fraction as F
from math import lcm
from itertools import product
import argparse
import json
from pathlib import Path

K = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
B = 1000
D = B**12 - 1


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def mv(a, x):
    return [sum(u * v for u, v in zip(row, x)) for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def shift(x, j=1):
    return x[j:] + x[:j]


def orbit(x):
    return transpose([shift(x, j) for j in range(len(x))])


def det_bareiss(a):
    a = [row[:] for row in a]
    n, sign, prev = len(a), 1, 1
    for j in range(n - 1):
        pivot = next((r for r in range(j, n) if a[r][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            sign = -sign
        p = a[j][j]
        for r in range(j + 1, n):
            for c in range(j + 1, n):
                value = p * a[r][c] - a[r][j] * a[j][c]
                require(value % prev == 0, "división Bareiss exacta")
                a[r][c] = value // prev
            a[r][j] = 0
        prev = p
    return sign * a[-1][-1]


def inverse(a):
    n = len(a)
    aug = [[F(v) for v in row + erow] for row, erow in zip(a, eye(n))]
    for j in range(n):
        p = next(r for r in range(j, n) if aug[r][j])
        aug[p], aug[j] = aug[j], aug[p]
        v = aug[j][j]
        aug[j] = [x / v for x in aug[j]]
        for r in range(n):
            if r != j:
                v = aug[r][j]
                aug[r] = [x - v*y for x, y in zip(aug[r], aug[j])]
    return [row[n:] for row in aug]


def remainder(a, b):
    a = [F(x) for x in a]
    while len(a) >= len(b):
        c, j = a[-1] / b[-1], len(a) - len(b)
        for i in range(len(b)):
            a[i+j] -= c * b[i]
        while a and a[-1] == 0:
            a.pop()
    return a or [F(0)]


def encode(k):
    return sum(v * B**(len(k)-1-j) for j, v in enumerate(k))


def decode(n):
    out = [0] * 12
    for j in range(11, -1, -1):
        n, out[j] = divmod(n, B)
    require(n == 0, "dominio de doce bloques")
    return out


def nearest(x):
    return (2*x.numerator + x.denominator) // (2*x.denominator)


def decode_two_memories(z, charge, reader):
    """Decodificador de carga conocida en el radio demostrado.

    z son las dos memorias divididas por sqrt(8). La garantía exige que
    sqrt(8)*||error_z|| < 4*sqrt(73)/81. No recibe el registro objetivo.
    Fuera del radio, esta búsqueda acotada no certifica recuperación.
    """
    n = len(reader[0])
    gram = mm(transpose(reader), reader)
    mean = [[F(1, n) for _ in range(n)] for _ in range(n)]
    inv = inverse([[gram[i][j]+mean[i][j] for j in range(n)] for i in range(n)])
    centered = mv(inv, mv(transpose(reader), z))
    estimate = [x+F(charge, n) for x in centered]
    # Bajo el radio, ||estimate-K|| < (9/4)*(4 sqrt(73)/81)<1.
    candidates = []
    for x in estimate:
        lo = x.numerator // x.denominator
        candidates.append([lo] if x == lo else [lo, lo+1])
    best, winners, tested = None, [], 0
    for candidate in product(*candidates):
        if sum(candidate) != charge:
            continue
        tested += 1
        response = mv(reader, candidate)
        distance = sum((a-b)**2 for a, b in zip(response, z))
        if best is None or distance < best:
            best, winners = distance, [list(candidate)]
        elif distance == best:
            winners.append(list(candidate))
    require(len(winners) == 1, "decodificación acotada con ganador único")
    return winners[0], tested, best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    n = len(K)
    O = orbit(K)
    det = det_bareiss(O)
    require(det != 0, "órbita de rango doce")
    inv = inverse(O)
    require(mm(O, inv) == eye(n) and mm(inv, O) == eye(n), "inversa bilateral")
    den = lcm(*(x.denominator for row in inv for x in row))
    adj = [[int(x*den) for x in row] for row in inv]
    require(mm(O, adj) == [[den*v for v in row] for row in eye(n)], "certificado entero de inversión")

    cyclo = {1: [-1, 1], 2: [1, 1], 3: [1, 1, 1], 4: [1, 0, 1],
             6: [1, -1, 1], 12: [1, 0, -1, 0, 1]}
    rem = {str(m): list(map(str, remainder(K, p))) for m, p in cyclo.items()}
    q = sum(K)
    centered12 = [12*x-q for x in K]
    Oc = orbit(centered12)
    centered_minor = [row[:11] for row in Oc[:11]]
    require(det_bareiss(centered_minor) != 0, "rango centrado al menos once")
    require(all(sum(col) == 0 for col in zip(*Oc)), "rango centrado a lo sumo once")

    # Diagonalización exacta en Q(sqrt(3)) del Gram circulante.
    autocorr = [sum(K[i]*K[(i+j) % n] for i in range(n)) for j in range(n)]
    twice_cos = [(2, 0), (0, 1), (1, 0), (0, 0), (-1, 0), (0, -1),
                 (-2, 0), (0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)]
    spectrum = [(F(sum(autocorr[t]*twice_cos[(j*t) % n][0] for t in range(n)), 2),
                 F(sum(autocorr[t]*twice_cos[(j*t) % n][1] for t in range(n)), 2))
                for j in range(n)]
    expected = [(39225169, 0), (1248025, -345420), (589609, 0),
                (1407529, 0), (1053157, 0), (1248025, 345420), (697225, 0),
                (1248025, 345420), (1053157, 0), (1407529, 0),
                (589609, 0), (1248025, -345420)]
    require(spectrum == expected, "espectro exacto de la órbita")
    require(658416**2 > 3*345420**2, "mínimo espectral exacto 589609")
    require(mm(transpose(O), O) == [[autocorr[(c-r) % n] for c in range(n)] for r in range(n)], "Gram circulante")

    N = encode(K)
    kappa = F(N, D)
    require(decode(N) == K, "lectura reversible")
    for j in range(12):
        x = shift(K, j)
        require(F(encode(shift(x)), D) == B*F(encode(x), D)-x[0], "ley afín de fase")
    require(sum(F(encode(shift(K, j)), D) for j in range(12)) == F(q, B-1), "suma orbital")
    recovered = decode(nearest(D*(kappa + F(1, 3*D))))
    require(recovered == K, "recuperación con error menor que media celda")
    wrong = decode(nearest(D*(kappa + F(2, 3*D))))
    require(wrong != K, "falsador fuera del radio")

    # Para H que conmuta con S basta y=HK. Ejemplo no trivial H=2I+3S-S^5.
    S = [[int(c == (r+1) % n) for c in range(n)] for r in range(n)]
    S5 = [[int(c == (r+5) % n) for c in range(n)] for r in range(n)]
    H = [[2*int(r == c)+3*S[r][c]-S5[r][c] for c in range(n)] for r in range(n)]
    y = mv(H, K)
    require(mm(orbit(y), inv) == H, "identificación del operador covariante")

    # Un operador no nulo que anula K impide omitir la hipótesis HS=SH.
    v = [K[1], -K[0]] + [0]*10
    Z = [v] + [[0]*n for _ in range(n-1)]
    require(mv(Z, K) == [0]*n and Z != [[0]*n for _ in range(n)], "falsador respuesta única")
    require(mm(Z, S) != mm(S, Z), "falsador carece de covariancia")

    # Conservar forma centrada no conserva la lectura de clausura.
    Kplus = [x+1 for x in K]
    require([12*x-sum(Kplus) for x in Kplus] == centered12, "misma forma centrada")
    require(F(encode(Kplus)-N, D) == F(1, B-1), "cambio exacto de lectura escalar")

    # M/sqrt(8) conserva coeficientes racionales. Gram calculado sin K.
    S3 = [[int(c == (r+3) % n) for c in range(n)] for r in range(n)]
    S4 = [[int(c == (r+4) % n) for c in range(n)] for r in range(n)]
    T3 = [[F(8*int(r == c)+S3[r][c], 9) for c in range(n)] for r in range(n)]
    # Holonomía relativa: se invierte la respuesta, no se entrega HC al inversor.
    zhol = mv([[F(S4[r][c]-S3[r][c],9) for c in range(n)] for r in range(n)], K)
    delta_hol = mm(orbit(zhol), inv)
    recovered_hc = [[S3[r][c]+9*delta_hol[r][c] for c in range(n)] for r in range(n)]
    relative_hol = mm(transpose(S3), recovered_hc)
    require(relative_hol == S, "holonomía relativa recuperada de respuesta de memoria")
    D3scaled = [[F(S3[r][c]-int(r == c), 9) for c in range(n)] for r in range(n)]
    D4scaled = [[F(S4[r][c]-int(r == c), 9) for c in range(n)] for r in range(n)]
    reader = D3scaled + mm(D4scaled, T3)
    gram_scaled = mm(transpose(reader), reader)
    memory_gram = [[8*x for x in row] for row in gram_scaled]
    Gint = [[int(6561*x) for x in row] for row in memory_gram]
    require(all(F(Gint[i][j], 6561) == memory_gram[i][j] for i in range(n) for j in range(n)), "Gram entero exacto")
    require(Gint[0] == [2336,-64,0,-520,-520,-64,0,-64,-520,-520,0,-64], "Gram de memorias")
    cuts = []
    for mask in range(1, (1 << n)-1):
        a = [(mask >> i) & 1 for i in range(n)]
        cuts.append(sum(x*y for x, y in zip(a, mv(Gint, a))))
    require(len(cuts) == 4094 and min(cuts) == 2336, "control de todos los cortes")
    roots = [(i,j,Gint[i][i]+Gint[j][j]-2*Gint[i][j]) for i in range(n) for j in range(n) if i != j]
    require(len(roots) == 132 and min(x[2] for x in roots) == 4672, "mínimo de raíces de carga cero")
    require({(j-i) % n for i,j,g in roots if g == 4672} == {2,6,10}, "raíces minimizantes")
    require(F(64,81) > F(4672,6561), "exclusión de vectores de norma cuadrada al menos cuatro")
    # Espectro de G: verifica también la cota usada para todos los enteros.
    memory_spectrum = [(F(sum(Gint[0][t]*twice_cos[(j*t) % n][0] for t in range(n)), 2*6561),
                        F(sum(Gint[0][t]*twice_cos[(j*t) % n][1] for t in range(n)), 2*6561)) for j in range(n)]
    require(all(b == 0 for a,b in memory_spectrum), "espectro racional del lector")
    require(memory_spectrum[0] == (0,0) and min(a for a,b in memory_spectrum[1:]) == F(16,81), "mínimo no uniforme16/81")
    z = mv(reader, K)
    noisy = z[:]
    noisy[0] += F(1,10)
    error_squared = F(8,100)
    require(error_squared < F(4672,4*6561), "ejemplo dentro del radio exacto")
    decoded, tested, residual_squared = decode_two_memories(noisy, q, reader)
    require(decoded == K and residual_squared == F(1,100), "recuperación ejecutable desde memorias perturbadas")
    require([i+1 for i,x in enumerate(decoded) if x >= 729] == [4,6,9,10], "recuperación de incidencia umbral729")
    rival = K[:]
    rival[3] -= 1
    rival[5] += 1
    dz = [a-b for a,b in zip(mv(reader,rival),z)]
    require(sum(rival) == q and 8*sum(x*x for x in dz) == F(4672,6561), "falsador de radio óptimo")
    require([i+1 for i,x in enumerate(rival) if x >= 729] == [6,9,10], "falsador altera incidencia")
    require(mv(reader,[x-1 for x in K]) == z, "ausencia de carga mantiene ambigüedad uniforme")
    report = {
        "scope": "consecuencias exactas de lectores posteriores; K archivado, no regenerado",
        "status": "CONTROLES_EXACTOS_COMPLETADOS",
        "K": K, "q": q, "N": str(N), "D": str(D),
        "orbit_matrix_convention": "O[i,j]=K[(i+j) mod12]",
        "det_O": str(det), "inverse_denominator": str(den),
        "integer_inverse_numerator": adj,
        "cyclotomic_remainders_low_to_high": rem,
        "centered_rank": 11,
        "autocorrelation": autocorr,
        "orbit_gram_spectrum_a_plus_b_sqrt3": [[str(a), str(b)] for a, b in spectrum],
        "exact_frame_bounds": [589609, 39225169],
        "condition_number": "6263/sqrt(589609)",
        "det_centered_11_minor": str(det_bareiss(centered_minor)),
        "scalar_decoding_radius_strict": str(F(1, 2*D)),
        "relative_holonomy_example": {"known_reference": "S^3", "received_response": list(map(str,zhol)), "recovered_relative_transport": "S", "unknown_transport_not_received_by_inverse": True},
        "two_memory_decoding": {
            "gram_integer_6561": Gint,
            "cuts_checked": len(cuts), "roots_checked": len(roots),
            "minimum_distance_squared_without_charge": "2336/6561",
            "minimum_distance_squared_with_charge": "4672/6561",
            "strict_radius_with_charge": "4*sqrt(73)/81",
            "noise_normalization": "z=M K/sqrt(8); Euclidean error in M-units",
            "example_noise_squared": str(error_squared),
            "candidate_count_example": tested,
            "decoded_K": decoded,
            "decoded_high_block_support": [4,6,9,10],
            "target_not_received_by_decoder": True,
        },
        "negative_controls": ["error mayor que media celda altera registro", "respuesta única no determina operador arbitrario", "misma forma centrada admite distinta lectura de clausura"],
    }
    data = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(data, encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "integer_inverse_numerator"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
