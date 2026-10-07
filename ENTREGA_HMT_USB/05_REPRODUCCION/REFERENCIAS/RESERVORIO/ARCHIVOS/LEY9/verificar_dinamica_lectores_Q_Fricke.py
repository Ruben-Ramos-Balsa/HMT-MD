"""Identidades exactas de dos lectores ya documentados: Q y Fricke 2A.

Q se prolonga algebraicamente de su dominio positivo a (C*)²; no se
identifica esa prolongación con toda la holonomía TPK. El control usa
enteros, fases racionales y polinomios de Laurent, no cifras objetivo.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path

def clean(p):
    return {k: Fraction(v) for k, v in p.items() if v}

def add(*polys):
    result = {}
    for p in polys:
        for k, v in p.items():
            result[k] = result.get(k, Fraction(0)) + v
    return clean(result)

def scale(p, c):
    return clean({k: c*v for k, v in p.items()})

def mul(p, q):
    out = {}
    for i, a in p.items():
        for j, b in q.items():
            out[i+j] = out.get(i+j, Fraction(0)) + a*b
    return clean(out)

def power(p, n):
    result = {0: Fraction(1)}
    for _ in range(n):
        result = mul(result, p)
    return result

def derivative(p):
    return clean({k-1: k*v for k, v in p.items()})

def mirror(p):
    return clean({-k: v*Fraction(4096)**k for k, v in p.items()})

def equal(p, q):
    return add(p, scale(q, -1)) == {}

def eval_poly(p, t):
    return sum(v*Fraction(t)**k for k, v in p.items())

def matmul(a, b):
    return tuple(tuple(sum(a[i][h]*b[h][j] for h in range(2))
                       for j in range(2)) for i in range(2))

def matpower(b, n):
    result = ((1, 0), (0, 1))
    for _ in range(n):
        result = matmul(result, b)
    return result

def mod_one(x):
    return x - x.numerator//x.denominator

def phase_step(x, y):
    return mod_one(x-2*y), mod_one(y-2*x)

def phase_inverse(x, y):
    base = (-x-2*y)/3, (-2*x-y)/3
    return tuple((mod_one(base[0]+Fraction(k,3)),
                  mod_one(base[1]-Fraction(k,3))) for k in range(3))

def verify():
    t = {1: Fraction(1)}
    s = {-1: Fraction(4096)}
    T = add(t, s, {0: Fraction(24)})
    J = mul(power(add(t, {0: Fraction(256)}), 3), {-2: Fraction(1)})
    Js = mirror(J)
    total = add(power(T, 2), T, {0: Fraction(-7256)})
    product = power(add(T, {0: Fraction(248)}), 3)
    checks = {
        "Fricke_involution": equal(mirror(s), t),
        "invariant_T": equal(mirror(T), T),
        "oriented_difference": equal(
            add(J, scale(Js,-1)),
            mul(add(s,scale(t,-1)),add(T,{0:Fraction(23)}))),
        "sum": equal(add(J, Js), total),
        "product": equal(mul(J, Js), product),
        "quadratic_relation": equal(
            add(power(J,2),scale(mul(total,J),-1),product), {}),
        "discriminant": equal(
            add(power(total,2),scale(product,-4)),
            mul(power(add(T,{0:Fraction(23)}),2),
                mul(add(T,{0:Fraction(-152)}),add(T,{0:Fraction(104)})))),
        "reconstruction": equal(
            mul(t,add(T,{0:Fraction(23)})),
            add(power(T,2),scale(J,-1),{0:Fraction(-3904)})),
        "jet_identity": equal(
            derivative(J),
            add(mul(add(s,{0:Fraction(1)}),derivative(T)),
                mul(add(T,{0:Fraction(23)}),derivative(s)))),
        "fixed_point_positive": eval_poly(T,64)==152 and eval_poly(J,64)==8000,
        "fixed_point_negative": eval_poly(T,-64)==-104 and eval_poly(J,-64)==1728,
        "collision_quadratic_field": 47**2-4*4096 == -(45**2)*7,
        "collision_value": (-23)**2-3904 == -3375,
        "collision_is_not_Fricke_fixed": all(v*v+47*v+4096 != 0 for v in (64,-64)),
        "wrong_invariance_rejected": not equal(J,Js),
        "wrong_sum_coefficient_rejected": not equal(
            add(J,Js),add(power(T,2),scale(T,-1),{0:Fraction(-7208)}))
    }
    assert all(checks.values())
    B = ((1,-2),(-2,1))
    powers = []
    for n in range(13):
        m, parity = 3**n, (-1)**n
        a, b = (parity+m)//2, (parity-m)//2
        assert matpower(B,n) == ((a,b),(b,a))
        assert a*a-b*b == (-3)**n
        assert a+b==parity and a-b==m
        powers.append({"n":n,"degree":m,"diagonal":a,"off_diagonal":b})
    kernel_checks = []
    for n in range(5):
        m = 3**n
        Bn = matpower(B,n)
        actual = {(i,j) for i in range(m) for j in range(m)
                  if all((Bn[r][0]*i+Bn[r][1]*j)%m==0 for r in range(2))}
        expected = {(i,(-i)%m) for i in range(m)}
        assert actual == expected
        kernel_checks.append({"n":n,"kernel_count":len(actual)})
    inverses = 0
    for i in range(11):
        for j in range(7):
            target = Fraction(i,11), Fraction(j,7)
            preimages = phase_inverse(*target)
            assert len(set(preimages))==3
            for preimage in preimages:
                assert phase_step(*preimage)==target
                inverses += 1
    carry_checks = 0
    for den in (7,11,17):
        for num in range(den):
            initial = Fraction(num,den)
            remainder = initial
            ledger = 0
            for n in range(1,13):
                raw = 3*remainder
                digit = raw.numerator//raw.denominator
                assert digit in (0,1,2)
                remainder = raw-digit
                ledger = 3*ledger+digit
                assert initial == (ledger+remainder)/(3**n)
                assert ledger == (3**n*initial).numerator//(3**n*initial).denominator
                carry_checks += 1
    return {
        "status":"IDENTIDADES_EXACTAS_VERIFICADAS",
        "Fricke_Laurent_checks":checks,
        "Q_integer_matrix_powers":powers,
        "Q_finite_phase_kernels":kernel_checks,
        "phase_inverse_images_checked":inverses,
        "carry_reconstruction_checks":carry_checks,
        "proof_domains":{
            "Q_source":"positive pairs in c57 and 02_dinamica_tres_hojas",
            "Q_extension":"explicit algebraic extension to nonzero complex pairs",
            "Fricke":"nonzero t, T=t+24+4096/t, j=(t+256)^3/t^2",
            "Gamma9_identification_proved":False,
            "all_enriched_states_reconstructed":False,
            "new_decimal_generation":False,
            "historical_novelty_claimed":False,
            "originals_modified":False
        },
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
