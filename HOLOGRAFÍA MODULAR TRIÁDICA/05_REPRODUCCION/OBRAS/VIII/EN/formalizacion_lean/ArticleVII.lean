import Std

/-!
Núcleo algebraico finito del Artículo VII. Formaliza únicamente identidades
explícitas indicadas en el README; no formaliza los espacios funcionales, la
dinámica gravitatoria ni las hipótesis analíticas completas del artículo.
-/

namespace ArticleVII

def reverseChannel {α : Type} (p : α × α) : α × α := (p.2, p.1)

theorem reverse_channel_involution {α : Type} (p : α × α) :
    reverseChannel (reverseChannel p) = p := by
  cases p
  rfl

theorem reverse_channel_exchanges {α : Type} (ret adv : α) :
    reverseChannel (ret, adv) = (adv, ret) := rfl

def symmetricNumerator (ret adv : Int) : Int := ret + adv

def radiativeNumerator (ret adv : Int) : Int := ret - adv

theorem symmetric_numerator_even_under_exchange (ret adv : Int) :
    symmetricNumerator adv ret = symmetricNumerator ret adv := by
  simp [symmetricNumerator, Int.add_comm]

theorem radiative_numerator_odd_under_exchange (ret adv : Int) :
    radiativeNumerator adv ret = -radiativeNumerator ret adv := by
  simp [radiativeNumerator]
  omega

theorem reconstruct_retarded_doubled (ret adv : Int) :
    symmetricNumerator ret adv + radiativeNumerator ret adv = 2 * ret := by
  simp [symmetricNumerator, radiativeNumerator]
  omega

theorem reconstruct_advanced_doubled (ret adv : Int) :
    symmetricNumerator ret adv - radiativeNumerator ret adv = 2 * adv := by
  simp [symmetricNumerator, radiativeNumerator]
  omega

theorem hexad_incidence : 6 * (6 * 5 / 2) = 90 := by decide

theorem octad_incidence : 8 * (6 * 5 / 2) = 120 := by decide

def totalOccupation (n90 n120 : Int) : Int := n90 + n120

def weightedOccupation (n90 n120 : Int) : Int := 90 * n90 + 120 * n120

theorem recover_sector_90_scaled (n90 n120 : Int) :
    120 * totalOccupation n90 n120 - weightedOccupation n90 n120 = 30 * n90 := by
  simp [totalOccupation, weightedOccupation]
  omega

theorem recover_sector_120_scaled (n90 n120 : Int) :
    weightedOccupation n90 n120 - 90 * totalOccupation n90 n120 = 30 * n120 := by
  simp [totalOccupation, weightedOccupation]
  omega

def bouncePolynomial (base curvature u : Int) : Int :=
  base + curvature * u * u

theorem bounce_polynomial_even (base curvature u : Int) :
    bouncePolynomial base curvature (-u) = bouncePolynomial base curvature u := by
  simp [bouncePolynomial, Int.mul_neg, Int.neg_mul, Int.neg_mul_neg]

theorem bounce_polynomial_at_origin (base curvature : Int) :
    bouncePolynomial base curvature 0 = base := by
  simp [bouncePolynomial]

theorem bounce_polynomial_increment (base curvature u : Int) :
    bouncePolynomial base curvature u - base = curvature * u * u := by
  simp [bouncePolynomial, Int.sub_eq_add_neg] <;> omega

end ArticleVII

#print axioms ArticleVII.reverse_channel_involution
#print axioms ArticleVII.radiative_numerator_odd_under_exchange
#print axioms ArticleVII.recover_sector_90_scaled
#print axioms ArticleVII.bounce_polynomial_even
