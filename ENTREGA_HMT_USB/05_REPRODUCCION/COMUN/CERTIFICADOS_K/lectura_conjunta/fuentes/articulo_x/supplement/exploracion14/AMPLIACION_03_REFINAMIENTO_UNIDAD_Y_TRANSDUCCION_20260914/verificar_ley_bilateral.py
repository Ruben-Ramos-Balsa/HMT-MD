"""Controles exactos de la ampliación 03, posteriores al generador HMT.

Las demostraciones para dimensión y profundidad arbitrarias están en las notas.
Estos ensayos finitos contrastan identidades, inversas y un ejemplo con ruido;
no sustituyen esas pruebas ni reproducen la generación APP--TRIT--TPK de K.
La cota antecedente de alfa sólo interviene al final como ensayo inverso.
Biblioteca estándar; comprobaciones activas incluso con python -O.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import runpy


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def tr(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    require(len(a[0]) == len(b), "dimensiones del producto")
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def mv(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def add(a, b):
    require(len(a) == len(b) and len(a[0]) == len(b[0]), "dimensiones de suma")
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(a, q):
    return [[q*x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(b, -1))


def gram(a, form=None):
    return mm(tr(a), a if form is None else mm(form, a))


def shift(n, k):
    return [[int(j == (i+k) % n) for j in range(n)] for i in range(n)]


def norm2(v):
    return sum(x*x for x in v)


def refined(x, y, base, c):
    return base*x-c, base*y+c


def unrefined(x, y, base):
    c = y % base
    require((x+c) % base == 0, "inversa entera")
    return (x+c)//base, (y-c)//base, c


def check_refinement():
    central, local, words = 0, 0, 0
    for b in range(3, 31):
        base, p = b+1, b*b-b+1
        x, y = base*(b-2)+2, 2*base+b-2
        require((x, y) == (p-1, 3*b), "concatenaciones centrales")
        require(x+y == base**2-1, "complemento unitario")
        require(refined(x+1, y, base, 1) == (b**3, base**3-b**3), "completación cúbica")
        central += 1
    for base in range(2, 13):
        for mass in range(1, 8):
            for y in range(base*mass+1):
                x = base*mass-y
                u, v, c = unrefined(x, y, base)
                require(u+v == mass and u >= 0 and v >= 0, "preimagen positiva")
                require(refined(u, v, base, c) == (x, y), "inversa local exacta")
                local += 1
    for base in (2, 3, 10):
        for depth in range(1, 4):
            for word in product(range(base), repeat=depth):
                x0, y0 = base**2-base+1, 3*base
                x, y, csum = x0, y0, 0
                for c in word:
                    x, y = refined(x, y, base, c)
                    csum = base*csum+c
                require((x, y) == (base**depth*x0-csum, base**depth*y0+csum), "cociclo exacto")
                reverse = []
                for _ in word:
                    x, y, c = unrefined(x, y, base)
                    reverse.append(c)
                require((x, y) == (x0, y0) and tuple(reversed(reverse)) == word, "historia recuperada")
                words += 1
    signed_collisions = []
    for base in range(2, 13):
        lhs = refined(*refined(73, 27, base, 1), base, -1)
        rhs = refined(*refined(73, 27, base, 0), base, base-1)
        require(lhs == rhs, "acarreo firmado requiere elevación")
        signed_collisions.append(base)
    return {"central_families": central, "local_inverses": local,
            "finite_words": words, "signed_carry_falsators": signed_collisions}


def check_general_balance():
    i2 = eye(2)
    rotation = [[0, -1], [1, 0]]
    reflection = [[1, 0], [0, -1]]
    rational_rotation = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    embedding = [[1, 0], [0, 1], [0, 0]]
    other_embedding = [[0, 0], [1, 0], [0, 1]]
    cases = [(i2, rotation), (rotation, reflection), (i2, rational_rotation),
             (embedding, other_embedding), (eye(12), shift(12, 1)),
             (eye(12), shift(12, 4))]
    require(mm(rotation, reflection) != mm(reflection, rotation), "ejemplo no conmutativo")
    require(mm(mm(rotation, rotation), rotation) != i2, "ejemplo sin orden tres")
    count = 0
    for b, c in cases:
        ident = eye(len(b[0]))
        require(gram(b) == ident and gram(c) == ident, "transportes isométricos")
        for a in (F(1, 2), F(1), F(2), F(8), F(11)):
            p = a*a+a+1
            normal = (2*a+1)*p
            minus = sub(scale(b, a), c)
            plus = add(scale(b, a+1), c)
            require(add(scale(gram(minus), a+1), scale(gram(plus), a)) == scale(ident, normal), "balance bilateral")
            # Un lector simétrico no constante comprueba la ley más fuerte.
            f = [[F((i+1)*(j+1), 3)+int(i == j) for j in range(len(b))] for i in range(len(b))]
            read_balance = scale(add(scale(gram(minus, f), a+1), scale(gram(plus, f), a)), 1/normal)
            read_pair = scale(add(scale(gram(b, f), a*(a+1)), gram(c, f)), 1/p)
            require(read_balance == read_pair, "ley exacta de lectores")
            require(add(minus, plus) == scale(b, 2*a+1), "recuperación de B")
            require(sub(scale(plus, a), scale(minus, a+1)) == scale(c, 2*a+1), "recuperación de C")
            require(normal == (a+1)**3+a**3 and 0 < (a+1)**3/normal < 1, "contracción uniforme")
            # La factorización E_a/R_a se comprueba tras cancelar radicales positivos.
            require(a*(a+1)+1 == p and a+(a+1) == 2*a+1, "normalizaciones de E y R")
            if len(b) == len(b[0]) and b == ident:
                require(mm(minus, plus) == mm(plus, minus), "conmutación polinómica")
                require(mm(minus, tr(minus)) == gram(minus), "normalidad minus")
                require(mm(plus, tr(plus)) == gram(plus), "normalidad plus")
                require(mm(minus, tr(plus)) == mm(tr(plus), minus), "bloques unitarios")
            count += 1
    # Conservación alternante y lorentziana: no se les impone contracción positiva.
    forms = [([[0, 1], [-1, 0]], [[1, 1], [1, 2]]),
             ([[1, 0], [0, -1]], [[F(5, 3), F(4, 3)], [F(4, 3), F(5, 3)]])]
    for form, c in forms:
        require(gram(c, form) == form, "transporte de forma")
        minus, plus = sub(scale(i2, 8), c), add(scale(i2, 9), c)
        require(add(scale(gram(minus, form), 9), scale(gram(plus, form), 8)) == scale(form, 1241), "balance de forma")
        require(gram(c) != i2, "separación respecto a isometría positiva")
    return {"isometric_cases": count, "indefinite_or_alternating_cases": len(forms)}


def check_unitary_refinement():
    """La biyección de bases da una unitaria, no la norma euclídea de L_c."""
    cases = []
    for base, mass in ((2, 3), (3, 2), (10, 100)):
        domain = [(x, mass-x, c) for x in range(mass+1)
                  for c in range(base) if c <= base*x]
        image = [refined(x, y, base, c) for x, y, c in domain]
        expected = {(base*mass-y, y) for y in range(base*mass+1)}
        require(len(domain) == base*mass+1 and set(image) == expected, "biyección de bases")
        require(len(set(image)) == len(image), "sin colisión canónica")
        permutation = [y for x, y in image]

        def forward(v):
            out = [0]*len(v)
            for i, j in enumerate(permutation):
                out[j] = v[i]
            return out

        def backward(v):
            return [v[j] for j in permutation]

        v = [F((7*i) % 19-9, 7) for i in range(len(domain))]
        lv = forward(v)
        require(norm2(lv) == norm2(v) and backward(lv) == v, "norma e inversa del levantamiento")
        # Segundo transporte: la misma biyección compuesta con una permutación.
        cv = forward(v[1:]+v[:1])
        minus = [8*x-y for x, y in zip(lv, cv)]
        plus = [9*x+y for x, y in zip(lv, cv)]
        require(9*norm2(minus)+8*norm2(plus) == 1241*norm2(v), "refinamiento compuesto con balance")
        require(backward([F(x+y, 17) for x, y in zip(minus, plus)]) == v, "recuperación de amplitudes refinadas")
        for (x, y, c), (xx, yy) in zip(domain, image):
            require(F(xx, base*mass) == F(x, mass)-F(c, base*mass), "lector fracción primera")
            require(F(yy, base*mass) == F(y, mass)+F(c, base*mass), "lector fracción segunda")
            require(unrefined(xx, yy, base) == (x, y, c), "lector del acarreo")
        cases.append({"base": base, "initial_mass": mass, "dimension": len(domain)})
    for base, mass, depth in ((2, 2, 5), (3, 2, 3), (10, 1, 2)):
        image = []
        for y0 in range(mass+1):
            for word in product(range(base), repeat=depth):
                x, y, valid = mass-y0, y0, True
                for c in word:
                    if c > base*x:
                        valid = False
                        break
                    x, y = refined(x, y, base, c)
                if valid:
                    image.append((x, y))
                    restored = []
                    for _ in word:
                        x, y, c = unrefined(x, y, base)
                        restored.append(c)
                    require((x, y) == (mass-y0, y0) and tuple(reversed(restored)) == word, "inversa multiprofundidad")
        require(len(image) == len(set(image)) == base**depth*mass+1, "dimensión exacta de historias admitidas")
    return {"unitary_base_cases": cases, "multi_depth_bijections": 3,
            "restriction": "alfabeto canónico completo declarado; ninguna promoción a todas las historias TPK"}


def check_archive_and_transduction():
    parent = Path(__file__).resolve().parent.parent / "verificar_exploracion.py"
    old = runpy.run_path(str(parent), run_name="read_only_bilateral_tests")
    k = old["K"][:]
    ident, u = eye(12), shift(12, 4)
    minus, plus = sub(scale(ident, 8), u), add(scale(ident, 9), u)
    fixed = scale(add(add(ident, u), mm(u, u)), F(1, 3))
    require(mm(fixed, fixed) == fixed, "sector fijo ternario")
    require(scale(gram(minus), F(9, 1241)) == add(scale(fixed, F(441, 1241)), scale(sub(ident, fixed), F(9, 17))), "contracción exacta9/17")
    qminus, qplus = mv(minus, k), mv(plus, k)
    require([F(x+y, 17) for x, y in zip(qminus, qplus)] == k, "recuperación del registro entero")
    require(9*norm2(qminus)+8*norm2(qplus) == 1241*norm2(k), "balance sobre K")
    praw, memory_gram = ident, scale(ident, 0)
    stages = []
    for n in range(12):
        raw_memory = mm(plus, praw)
        memory_gram = add(memory_gram, scale(gram(raw_memory), F(8*9**n, 1241**(n+1))))
        praw = mm(minus, praw)
        terminal = scale(gram(praw), F(9**(n+1), 1241**(n+1)))
        require(add(memory_gram, terminal) == ident, "telescopía matricial exacta")
        reconstructed = mv(memory_gram, k)
        bias = [x-y for x, y in zip(k, reconstructed)]
        require(bias == mv(terminal, k), "sesgo del adjunto truncado")
        require(norm2(bias) <= F(9, 17)**(2*(n+1))*norm2(k), "cota cuantitativa del sesgo")
        if n in (0, 1, 5, 11):
            recovered = mv(old["inverse"](memory_gram), reconstructed)
            require(recovered == k, "inversa finita sin terminal ni sesgo")
            stages.append({"depth": n+1, "bias_squared": str(norm2(bias)), "bound_squared": str(F(9, 17)**(2*(n+1))*norm2(k))})
    # Reproduce la cadena de ejemplo: memorias previas -> canales -> recuperación.
    s3, s4 = shift(12, 3), u
    t3 = scale(add(scale(ident, 8), s3), F(1, 9))
    d3 = scale(sub(s3, ident), F(1, 9))
    d4 = scale(sub(s4, ident), F(1, 9))
    reader = d3 + mm(d4, t3)
    noisy = mv(reader, k)
    noisy[0] += F(1, 10)
    recovered_memory = []
    for offset in (0, 12):
        x = noisy[offset:offset+12]
        m, p = mv(minus, x), mv(plus, x)
        recovered_memory.extend(F(v+w, 17) for v, w in zip(m, p))
    require(recovered_memory == noisy, "recuperación de memorias transportadas")
    decoded, candidates, residual = old["decode_two_memories"](recovered_memory, sum(k), reader)
    require(decoded == k and candidates == 924 and residual == F(1, 100), "decodificación con ruido y carga")
    support = [j+1 for j, x in enumerate(decoded) if x >= 729]
    require(support == [4, 6, 9, 10], "incidencia recuperada después de decodificar")
    require(F(8, 100) < F(16*73, 81**2), "ruido dentro del radio")
    base, denominator = 1000, 1000**12-1
    row = [F(base**(11-j), denominator) for j in range(12)]
    require(norm2(row) == F(base**12+1, (base**2-1)*(base**12-1)), "norma exacta del lector escalar")
    return {"K": k, "norm_squared": norm2(k), "Q_minus_K": qminus,
            "Q_plus_K": qplus, "finite_archive_tests": stages,
            "decoded_candidates": candidates, "noise_squared_original_memory": "2/25",
            "decoded_incidence": support, "source_verifier": str(parent)}


def inverse_alpha_diagnostic():
    # Salida antecedente ya acotada en 02, sólo usada como dato posterior.
    lo = F(7297352569283800997285105472380662, 10**36)
    hi = F(7297352569283800997285105472380663, 10**36)
    target_lo, target_hi = 10000*lo, 10000*hi
    paired_lo = 73+F(9, 8)*(73-target_hi)
    paired_hi = 73+F(9, 8)*(73-target_lo)
    require(9*target_lo+8*paired_hi == 1241 and 9*target_hi+8*paired_lo == 1241, "respuesta complementaria condicionada")
    require(F(49) < target_lo < target_hi < F(81), "rango admisible del ensayo")
    return {"role": "diagnostico_inverso_posterior_no_derivacion_independiente",
            "paired_lower": str(paired_lo), "paired_upper": str(paired_hi)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    result = {"refinement": check_refinement(), "bilateral_balance": check_general_balance(),
              "unitary_refinement": check_unitary_refinement(),
              "archive_transduction": check_archive_and_transduction(),
              "inverse_alpha": inverse_alpha_diagnostic(),
              "scope": "controles finitos exactos; pruebas generales en notas; K es salida antecedente",
              "status": "PASS_CONTROLES_EXACTOS_AMPLIACION_03"}
    payload = json.dumps(result, ensure_ascii=False, indent=2)+"\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
