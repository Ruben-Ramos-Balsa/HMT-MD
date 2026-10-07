import LatticeTwistedNormalParity
import LatticeTwistedRawChargeField

/-! Normal ordering against the actual zero-charge identity field recovers
the divided half-Heisenberg derivative, on every vector and at every order. -/

noncomputable section
namespace HMT.IV.LatticeTwistedNormalVacuum
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeHalfIntegerField LatticeTwistedTensorField
open LatticeTwistedNormalDerivative LatticeTwistedRawChargeField
open LatticeTwistedNormalParity

theorem creationTerm_zero_charge (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) (a : ℕ) (v : Carrier o) :
    creationTerm o i n (rawChargeField o 0) k a v =
      if k+2*(n:ℤ)-2*(a:ℤ)+1=0 then
        dividedFactor (2*(a:ℤ)-1) n • halfMode o i (Int.negSucc a) v else 0 := by
  simp only [creationTerm, LatticeTwistedNormalProduct.creationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, rawChargeField_zero_charge]
  split_ifs <;> simp

theorem annihilationTerm_zero_charge (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) (a : ℕ) (v : Carrier o) :
    annihilationTerm o i n (rawChargeField o 0) k a v =
      if k+2*(n:ℤ)+2*(a:ℤ)+3=0 then
        dividedFactor (-2*(a:ℤ)-3) n • halfMode o i (a:ℤ) v else 0 := by
  simp only [annihilationTerm, LatticeTwistedNormalProduct.annihilationTerm,
    LinearMap.smul_apply, LinearMap.comp_apply, rawChargeField_zero_charge]
  split_ifs <;> simp

theorem normalCoefficient_zero_charge_at_mode (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ) (m : ℤ) :
    normalCoefficient o i n (rawChargeField o 0) (ramifiedExponent m-2*n) =
      dividedFactor (ramifiedExponent m) n • halfMode o i m := by
  classical
  apply LinearMap.ext
  intro v
  rw [normalCoefficient_apply]
  simp only [creationTerm_zero_charge, annihilationTerm_zero_charge, LinearMap.smul_apply]
  cases m with
  | ofNat b =>
    have hc (a : ℕ) : ¬(ramifiedExponent (Int.ofNat b)-2*(n:ℤ)+2*n-2*a+1=0) := by
      simp only [ramifiedExponent, Int.ofNat_eq_coe]
      omega
    have ha (a : ℕ) :
        (ramifiedExponent (Int.ofNat b)-2*(n:ℤ)+2*n+2*a+3=0) ↔ a=b := by
      simp only [ramifiedExponent, Int.ofNat_eq_coe]
      omega
    simp only [if_neg (hc _), finsum_zero, zero_add, ha]
    rw [finsum_eq_single _ b]
    · simp [ramifiedExponent]
    · intro a hab
      simp [hab]
  | negSucc b =>
    have ha (a : ℕ) : ¬(ramifiedExponent (Int.negSucc b)-2*(n:ℤ)+2*n+2*a+3=0) := by
      unfold ramifiedExponent
      omega
    have hc (a : ℕ) :
        (ramifiedExponent (Int.negSucc b)-2*(n:ℤ)+2*n-2*a+1=0) ↔ a=b := by
      unfold ramifiedExponent
      omega
    simp only [if_neg (ha _), finsum_zero, add_zero, hc]
    rw [finsum_eq_single _ b]
    · have he : ramifiedExponent (Int.negSucc b)=2*(b:ℤ)-1 := by
        unfold ramifiedExponent
        omega
      simp [he]
    · intro a hab
      simp [hab]

theorem normalCoefficient_zero_charge (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) :
    normalCoefficient o i n (rawChargeField o 0) k = derivativeCoefficient o i n k := by
  by_cases hk : k%2=0
  · have he : k=2*(k/2) := by omega
    rw [he, derivativeCoefficient_even]
    apply LinearMap.ext
    intro v
    rw [normalCoefficient_apply]
    have hc (a : ℕ) : ¬(2*(k/2)+2*(n:ℤ)-2*(a:ℤ)+1=0) := by omega
    have ha (a : ℕ) : ¬(2*(k/2)+2*(n:ℤ)+2*(a:ℤ)+3=0) := by omega
    simp only [creationTerm_zero_charge, annihilationTerm_zero_charge,
      if_neg (hc _), if_neg (ha _), finsum_zero, add_zero, LinearMap.zero_apply]
  · let m : ℤ := (-k-2*n-3)/2
    have he : k=ramifiedExponent m-2*n := by
      dsimp [m,ramifiedExponent]
      omega
    rw [he, normalCoefficient_zero_charge_at_mode, derivativeCoefficient_at_exponent,
      tensorHalfFieldCoefficient_mode]

theorem derivativeNormalField_zero_charge (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) : derivativeNormalField o i n (rawChargeField o 0) = derivativeField o i n := by
  apply HVertexOperator.coeff_inj
  funext k
  rw [derivativeNormalField_coefficient, derivativeField_coefficient,
    normalCoefficient_zero_charge]

end HMT.IV.LatticeTwistedNormalVacuum
end

#print axioms HMT.IV.LatticeTwistedNormalVacuum.creationTerm_zero_charge
#print axioms HMT.IV.LatticeTwistedNormalVacuum.annihilationTerm_zero_charge
#print axioms HMT.IV.LatticeTwistedNormalVacuum.normalCoefficient_zero_charge_at_mode
#print axioms HMT.IV.LatticeTwistedNormalVacuum.normalCoefficient_zero_charge
#print axioms HMT.IV.LatticeTwistedNormalVacuum.derivativeNormalField_zero_charge
