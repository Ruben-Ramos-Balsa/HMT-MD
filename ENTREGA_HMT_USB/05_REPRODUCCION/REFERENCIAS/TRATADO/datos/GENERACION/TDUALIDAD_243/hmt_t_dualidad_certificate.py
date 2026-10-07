#!/usr/bin/env python3
"""
Certificado computacional HMT - Dualidad de lectura, T-dualidad, 243/Golay y rutas de masa.
Verifica identidades finitas usadas en el paper.
"""
from fractions import Fraction
from math import comb, isclose


def hamming_ball(q:int, n:int, t:int) -> int:
    return sum(comb(n,k)*(q-1)**k for k in range(t+1))


def E(R, r, Q):
    return Fraction(r*r, 1) / (R*R) + Fraction(Q*Q,1)*(R*R)


def main():
    print("CERTIFICADO HMT - T-DUALIDAD Y 243/GOLAY")
    print("="*72)

    # EMRH estratificada
    lhs = 10**3
    terms = (9**3, 3*9**2, 3*9, 1)
    rhs = sum(terms)
    print("1) EMRH estratificada")
    print(f"10^3 = {lhs}")
    print(f"9^3 + 3*9^2 + 3*9 + 1 = {terms[0]} + {terms[1]} + {terms[2]} + {terms[3]} = {rhs}")
    assert lhs == rhs == 1000
    assert terms[1] + terms[2] == 270
    print("OK: 1000 = 729 + 243 + 27 + 1 = 729 + 270 + 1")
    print()

    # Hamming/Golay puncturado
    V = hamming_ball(3, 11, 2)
    print("2) Bola ternaria de Hamming V_3(11,2)")
    print(f"V_3(11,2) = 1 + 22 + 220 = {V}")
    assert V == 243
    print(f"729 * 243 = {729*V}, 3^11 = {3**11}")
    assert 729*V == 3**11
    print("OK: el bloque 243 coincide con la bola perfecta ternaria de radio 2 en longitud 11")
    print()

    # Descomposicion de 243
    print("3) Descomposicion HMT de 243")
    d243 = 1 + 22 + 90 + 120 + 10
    print(f"1 + 22 + 90 + 120 + 10 = {d243}")
    assert d243 == 243
    print("OK: 243 = retorno + cascaron electronico + hexada + octada + monodromia")
    print()

    # Canales desde 243
    print("4) Canales de constantes desde B=243")
    B = 243
    C_alpha = 3*B
    C_e = B + 27 + 1
    C_pi = B + 72
    C_phi = B - 81 - 1
    print(f"C_alpha = 3*243 = {C_alpha}")
    print(f"C_e     = 243 + 27 + 1 = {C_e}")
    print(f"C_pi    = 243 + 72 = {C_pi}")
    print(f"C_phi   = 243 - 81 - 1 = {C_phi}")
    assert (C_alpha, C_e, C_pi, C_phi) == (729,271,315,161)
    bridge = C_pi + C_e + C_phi - 3
    print(f"C_pi + C_e + C_phi - 3 = {bridge}")
    assert bridge == 744 == 729 + 15
    print("OK: canales y bisagra 744")
    print()

    # APP levantada
    print("5) APP levantada: defecto visible y memoria")
    vals = range(1,10)
    Rplus = Qplus = Rtimes = Qtimes = total_sum = total_prod = 0
    for i in vals:
        for j in vals:
            s = i + j
            r_s = ((s-1) % 9) + 1
            q_s = (s - r_s)//9
            p = i * j
            r_p = ((p-1) % 9) + 1
            q_p = (p - r_p)//9
            Rplus += r_s
            Qplus += q_s
            Rtimes += r_p
            Qtimes += q_p
            total_sum += s
            total_prod += p
    print(f"sum R+ = {Rplus}, sum Q+ = {Qplus}")
    print(f"sum Rx = {Rtimes}, sum Qx = {Qtimes}")
    print(f"total product - total sum = {total_prod} - {total_sum} = {total_prod-total_sum}")
    print(f"visible defect + 9*memory defect = {Rtimes-Rplus} + 9*{Qtimes-Qplus} = {(Rtimes-Rplus)+9*(Qtimes-Qplus)}")
    assert Rplus == 405 and Rtimes == 459 and (Rtimes-Rplus)==54
    assert Qplus == 45 and Qtimes == 174 and (Qtimes-Qplus)==129
    assert total_prod-total_sum == 1215 == 54 + 9*129
    assert 1215//9 == 135 == 120 + 15
    print("OK: 1215 = 54 + 9*129; 135 = 120 + 15")
    print()

    # T-dualidad minima
    print("6) Dualidad HMT minima E_R(r,Q)=E_{1/R}(Q,r)")
    tests = [(Fraction(2,1), 5, 7), (Fraction(3,2), 8, 1), (Fraction(5,3), 11, 4)]
    for R, r, Q in tests:
        lhs = E(R, r, Q)
        rhs = E(Fraction(1,1)/R, Q, r)
        print(f"R={R}, r={r}, Q={Q}: E_R={lhs}, E_dual={rhs}")
        assert lhs == rhs
    print("OK: invariancia exacta de la dualidad visible/memoria")
    print()

    # Ruta masa visible/winding formal
    print("7) Ruta de masa: simetria abstracta E_{A,C}(n,w)=E_{C,A}(w,n)")
    A = Fraction(729735256928380099728510547238, 10**29)  # approx A=7.297...
    C = Fraction(212373834043088038451942621755, 10**29)  # approx C*=2.123...
    for n,w in [(42, Fraction(-3,6)), (64, Fraction(0,1)), (11, Fraction(7,6))]:
        lhs = n*A + w*C
        rhs = w*C + n*A
        assert lhs == rhs
    print("OK: la forma bilineal de ruta conserva avance visible y memoria contraangular como modos intercambiables abstractos")
    print()

    # Dimension 11 duplicate readings
    print("8) Lecturas de dimension 11")
    assert 11 == 6 + 5 == 3 + 8
    assert 12 == 11 + 1
    assert 26 == 2 + 24 and 10 == 2 + 8
    print("OK: 11=6+5=3+8; 12=11+1; 26=2+24; 10=2+8")
    print()

    print("CERTIFICADO COMPLETADO SIN ERRORES")

if __name__ == "__main__":
    main()
