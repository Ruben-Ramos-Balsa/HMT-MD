import HeisenbergDerivativeModes
import LatticeNormalOrderedField
import LatticeChargedVertexField

/-!
The already constructed locally finite normal product is precisely the
normal product of the divided Heisenberg derivative, coefficient by
coefficient.  These are operator equalities, not only vacuum evaluations.
The original normal-product source and all inherited constructions remain
unchanged.  No vertex-algebra or orbifold axiom is introduced.
-/

noncomputable section
namespace HMT.IV.LatticeNormalProductDerivativeBridge

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.HeisenbergDerivativeModes HMT.IV.LatticeNormalOrderedField

theorem creationTerm_eq_derivative (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    creationTerm o i n B k a =
      (derivativeCoefficient o i n (a : ℤ)).comp
        (HVertexOperator.coeff B (k-a)) := by
  rw [derivativeCoefficient_creation]
  rfl

theorem annihilationTerm_eq_derivative (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    annihilationTerm o i n B k a =
      (HVertexOperator.coeff B (k+a+n+1)).comp
        (derivativeCoefficient o i n (-(a : ℤ)-(n : ℤ)-1)) := by
  rw [derivativeCoefficient_nonnegativeMode]
  apply LinearMap.ext
  intro v
  simp only [annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply, map_smul]

/-- Both sums are the original pointwise finite sums, now expressed in
terms of the single normalized derivative field and the correct order of
composition in its creation and nonnegative-mode parts. -/
theorem normalCoefficient_eq_derivative_sums (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    normalCoefficient o i n B k v =
      (∑ᶠ a : ℕ, derivativeCoefficient o i n (a : ℤ)
        (HVertexOperator.coeff B (k-a) v)) +
      ∑ᶠ a : ℕ, HVertexOperator.coeff B (k+a+n+1)
        (derivativeCoefficient o i n (-(a : ℤ)-(n : ℤ)-1) v) := by
  rw [normalCoefficient_apply]
  simp only [creationTerm_eq_derivative, annihilationTerm_eq_derivative,
    LinearMap.comp_apply]

theorem normalField_eq_derivative_sums (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    HVertexOperator.coeff (normalField o i n B) k v =
      (∑ᶠ a : ℕ, derivativeCoefficient o i n (a : ℤ)
        (HVertexOperator.coeff B (k-a) v)) +
      ∑ᶠ a : ℕ, HVertexOperator.coeff B (k+a+n+1)
        (derivativeCoefficient o i n (-(a : ℤ)-(n : ℤ)-1) v) := by
  rw [normalField_coefficient, normalCoefficient_eq_derivative_sums]

private theorem finsum_nat_int_eq {V : Type*} [AddCommGroup V]
    (r : ℤ) (v : V) :
    (∑ᶠ a : ℕ, if (a : ℤ) = r then v else 0) = if 0 ≤ r then v else 0 := by
  classical
  by_cases hr : 0 ≤ r
  · lift r to ℕ using hr
    rw [if_pos (by omega)]
    rw [finsum_eq_single _ r]
    · simp
    · intro a ha
      simp [show (a : ℤ) ≠ (r : ℤ) by omega]
  · have hz : ∀ a : ℕ, (a : ℤ) ≠ r := by intro a; omega
    simp [hz, hr]

theorem normalCoefficient_zero_charge (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) :
    normalCoefficient o i n (LatticeChargedVertexField.chargedField o 0) k =
      derivativeCoefficient o i n k := by
  classical
  apply LinearMap.ext
  intro v
  rw [normalCoefficient_eq_derivative_sums]
  have hid (j : ℤ) (w : LatticeCarrier o) :
      HVertexOperator.coeff (LatticeChargedVertexField.chargedField o 0) j w =
        if j = 0 then w else 0 :=
    LatticeChargedVertexField.chargedField_zero_charge_coefficient o w j
  have hcreate (a : ℕ) :
      derivativeCoefficient o i n (a : ℤ)
          (HVertexOperator.coeff (LatticeChargedVertexField.chargedField o 0) (k-a) v) =
        if (a : ℤ) = k then derivativeCoefficient o i n k v else 0 := by
    rw [hid]
    by_cases ha : (a : ℤ) = k
    · simp [ha]
    · simp [ha, show k-(a : ℤ) ≠ 0 by omega]
  have hann (a : ℕ) :
      HVertexOperator.coeff (LatticeChargedVertexField.chargedField o 0) (k+a+n+1)
          (derivativeCoefficient o i n (-(a : ℤ)-(n : ℤ)-1) v) =
        if (a : ℤ) = -k-(n : ℤ)-1 then derivativeCoefficient o i n k v else 0 := by
    rw [hid]
    by_cases ha : (a : ℤ) = -k-(n : ℤ)-1
    · have he : -(a : ℤ)-(n : ℤ)-1 = k := by omega
      rw [if_pos (show k+(a : ℤ)+(n : ℤ)+1 = 0 by omega), if_pos ha, he]
    · simp [ha, show k+(a : ℤ)+(n : ℤ)+1 ≠ 0 by omega]
  simp only [hcreate, hann, finsum_nat_int_eq]
  by_cases hk : 0 ≤ k
  · rw [if_pos hk, if_neg (show ¬ (0 ≤ -k-(n : ℤ)-1) by omega), add_zero]
  · by_cases hkn : 0 ≤ -k-(n : ℤ)-1
    · rw [if_neg hk, if_pos hkn, zero_add]
    · rw [derivativeCoefficient_gap o i n k (by omega) (by omega)]
      simp

theorem normalField_zero_charge (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    normalField o i n (LatticeChargedVertexField.chargedField o 0) =
      derivativeField o i n := by
  apply VertexOperator.ext
  intro v
  apply (HahnModule.of ℂ).symm.injective
  apply HahnSeries.ext
  funext k
  change normalCoefficient o i n (LatticeChargedVertexField.chargedField o 0) k v =
    derivativeCoefficient o i n k v
  rw [normalCoefficient_zero_charge]

end HMT.IV.LatticeNormalProductDerivativeBridge
end

#print axioms HMT.IV.LatticeNormalProductDerivativeBridge.creationTerm_eq_derivative
#print axioms HMT.IV.LatticeNormalProductDerivativeBridge.annihilationTerm_eq_derivative
#print axioms HMT.IV.LatticeNormalProductDerivativeBridge.normalCoefficient_eq_derivative_sums
#print axioms HMT.IV.LatticeNormalProductDerivativeBridge.normalField_eq_derivative_sums
#print axioms HMT.IV.LatticeNormalProductDerivativeBridge.normalCoefficient_zero_charge
#print axioms HMT.IV.LatticeNormalProductDerivativeBridge.normalField_zero_charge
