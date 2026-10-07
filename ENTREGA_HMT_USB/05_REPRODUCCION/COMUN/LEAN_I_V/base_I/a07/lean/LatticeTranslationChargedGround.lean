import LatticeTranslationVacuum
import LatticeTranslationCommutators
import LatticeNegativeMixedFields
import LatticeFieldCutoff

/-!
Differential covariance on every pure lattice-charge state. The coefficient
formula comes from the proved annihilation cutoff at zero, and its derivative
from the existing creation exponential recurrence. The incoming charge term
is retained through the actual negative-mode commutator.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeTranslationChargedGround

open LatticeOscillatorFock LatticeCocycle TwistedGroupAlgebra
open LatticeCreationExponential LatticeAnnihilationExponential
open LatticeChargedVertexField LatticeFieldCutoff LatticeAnnihilationCommutativity
open LatticeTranslationVacuum LatticeTranslationCommutators LatticeNegativeMixedFields
open scoped TensorProduct BigOperators

local notation "T" => LatticeTranslationOperator.translation

theorem field_charged_ground (o : Fin 12) (x y : Lattice o) (k : ℤ) :
    fieldCoefficient o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) =
      epsilon o x y • (if 0 ≤ k - integerPair o x y then
        PowerSeries.coeff (Fock o) ((k - integerPair o x y).toNat)
          (creationExponential o x) ⊗ₜ[ℂ] basisElement o (x+y) else 0) := by
  rw [fieldCoefficient_eq_of_annihilation_cutoff o x y k 0 1
    (fun d hd => annihilationExponential_positive_vacuum o x d hd)]
  simp [fieldCutoff, annihilationExponential_constant, creationExponentialMode_vacuum]

theorem field_charged_ground_nonnegative (o : Fin 12) (x y : Lattice o) (d : ℕ) :
    fieldCoefficient o x (integerPair o x y + (d : ℤ))
        ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) =
      epsilon o x y • (PowerSeries.coeff (Fock o) d (creationExponential o x)
        ⊗ₜ[ℂ] basisElement o (x+y)) := by
  rw [field_charged_ground]
  simp

theorem field_charged_ground_negative (o : Fin 12) (x y : Lattice o) (k : ℤ)
    (hk : k < integerPair o x y) :
    fieldCoefficient o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) = 0 := by
  rw [field_charged_ground, if_neg (by omega), smul_zero]

theorem translation_ground_nonnegative (o : Fin 12) (x y : Lattice o) (d : ℕ) :
    T o (fieldCoefficient o x (integerPair o x y + (d : ℤ))
        ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)) -
      onCarrier o (chargeCreation o y 0)
        (fieldCoefficient o x (integerPair o x y + (d : ℤ))
          ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)) =
      (d+1 : ℂ) • fieldCoefficient o x (integerPair o x y + ((d+1 : ℕ) : ℤ))
        ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) := by
  rw [field_charged_ground_nonnegative, field_charged_ground_nonnegative]
  rw [map_smul, map_smul, LatticeTranslationOperator.translation_pure,
    onCarrier_pure, chargeCreation_apply, chargeCreationState_add]
  rw [← smul_sub, ← TensorProduct.sub_tmul]
  have he :
      LatticeOscillatorTranslation.translation o
          (PowerSeries.coeff (Fock o) d (creationExponential o x)) +
        (chargeCreationState o x 0 + chargeCreationState o y 0) *
          PowerSeries.coeff (Fock o) d (creationExponential o x) -
        chargeCreationState o y 0 *
          PowerSeries.coeff (Fock o) d (creationExponential o x) =
      (d+1 : ℂ) • PowerSeries.coeff (Fock o) (d+1) (creationExponential o x) := by
    rw [add_mul]
    convert creation_exponential_recurrence o x d using 1
    abel
  rw [he, TensorProduct.smul_tmul']
  exact smul_comm (epsilon o x y) (d+1 : ℂ)
    (PowerSeries.coeff (Fock o) (d+1) (creationExponential o x)
      ⊗ₜ[ℂ] basisElement o (x+y))

theorem translation_ground_shift (o : Fin 12) (x y : Lattice o) (k : ℤ) :
    T o (fieldCoefficient o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)) -
      onCarrier o (chargeCreation o y 0)
        (fieldCoefficient o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)) =
      ((k - integerPair o x y : ℤ) + 1 : ℂ) •
        fieldCoefficient o x (k+1) ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) := by
  by_cases hk : integerPair o x y ≤ k
  · let d : ℕ := (k-integerPair o x y).toNat
    have hd : (d : ℤ) = k-integerPair o x y := Int.toNat_of_nonneg (by omega)
    have he : k = integerPair o x y + (d : ℤ) := by omega
    have hn : k+1 = integerPair o x y + ((d+1 : ℕ) : ℤ) := by omega
    rw [hn, he]
    simpa using translation_ground_nonnegative o x y d
  · have hneg : k < integerPair o x y := by omega
    rw [field_charged_ground_negative o x y k hneg, map_zero, map_zero, sub_self]
    by_cases hn : k+1 < integerPair o x y
    · rw [field_charged_ground_negative o x y (k+1) hn, smul_zero]
    · have he : k - integerPair o x y = -1 := by omega
      rw [he]
      norm_num

theorem translation_pure_charge (o : Fin 12) (y : Lattice o) :
    T o ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) =
      onCarrier o (chargeCreation o y 0) ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) := by
  rw [LatticeTranslationOperator.translation_pure, onCarrier_pure, chargeCreation_apply]
  simp

theorem translation_charged_ground (o : Fin 12) (x y : Lattice o) (k : ℤ) :
    T o (fieldCoefficient o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)) -
      fieldCoefficient o x k (T o ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)) =
      ((k : ℂ)+1) • fieldCoefficient o x (k+1)
        ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) := by
  have hs := translation_ground_shift o x y k
  have hc := LinearMap.congr_fun (negative_mode_field_commutator o y x 0 k)
    ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    Nat.zero_add, Nat.cast_one, integerPair_comm o y x] at hc
  rw [translation_pure_charge]
  calc
    _ = (T o (fieldCoefficient o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)) -
          onCarrier o (chargeCreation o y 0)
            (fieldCoefficient o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y))) +
        (onCarrier o (chargeCreation o y 0)
            (fieldCoefficient o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y)) -
          fieldCoefficient o x k
            (onCarrier o (chargeCreation o y 0)
              ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y))) := by abel
    _ = _ := by rw [hs, hc, ← add_smul]; congr 1; push_cast; ring

end HMT.IV.LatticeTranslationChargedGround
end

#print axioms HMT.IV.LatticeTranslationChargedGround.field_charged_ground
#print axioms HMT.IV.LatticeTranslationChargedGround.translation_ground_nonnegative
#print axioms HMT.IV.LatticeTranslationChargedGround.translation_ground_shift
#print axioms HMT.IV.LatticeTranslationChargedGround.translation_pure_charge
#print axioms HMT.IV.LatticeTranslationChargedGround.translation_charged_ground
