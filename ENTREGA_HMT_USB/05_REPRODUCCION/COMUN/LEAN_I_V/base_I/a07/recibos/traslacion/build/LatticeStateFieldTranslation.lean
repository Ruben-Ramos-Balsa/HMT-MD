import LatticeNormalTranslation
import LatticeChargedTranslation
import LatticeTranslationLinear
import LatticeStateFieldCoherence
import LatticeCovariantFieldUniqueness
import LatticeDerivativeLocality
import LatticeDescendantLocality

/-! Differential translation covariance of the previously constructed
state-field map for every state. The charged-field proof supplies the
base case and the proved normal-product calculation supplies each step.
The same oscillator basis then extends the result linearly. -/

noncomputable section
namespace HMT.IV.LatticeStateFieldTranslation

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeDescendantFields
open HMT.IV.LatticeNormalTranslation HMT.IV.LatticeChargedTranslation
open HMT.IV.LatticeTranslationLinear HMT.IV.LatticeStateFieldMap

local notation "T" => HMT.IV.LatticeTranslationOperator.translation

theorem descendant_translation_covariant (o : Fin 12) (x : Lattice o)
    (w : List (Mode o)) : TranslationCovariant (T o) (descendantField o x w) := by
  induction w with
  | nil => exact translation_charged_coefficient o x
  | cons m w ih => exact normalField_translation_covariant o m.2 m.1 _ ih

theorem stateField_translation_covariant (o : Fin 12) (u : LatticeCarrier o) :
    TranslationCovariant (T o) (stateField o u) := by
  apply covariance_linear_extension (carrierBasis o) (stateField o) (T o) _ u
  rintro ⟨a,x⟩
  rw [stateField_basis]
  exact descendant_translation_covariant o x _

/-- Coefficient form on the whole carrier, with neither operand restricted
to the vacuum or to a basis state. -/
theorem stateField_translation (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    T o * HVertexOperator.coeff (stateField o u) k -
      HVertexOperator.coeff (stateField o u) k * T o =
      ((k : ℂ)+1) • HVertexOperator.coeff (stateField o u) (k+1) :=
  stateField_translation_covariant o u k

theorem stateField_translation_vacuum_coefficient (o : Fin 12)
    (u : LatticeCarrier o) :
    HVertexOperator.coeff (stateField o u) 1 (vacuum o) = T o u := by
  have h := LinearMap.congr_fun (stateField_translation o u 0) (vacuum o)
  simp only [LinearMap.sub_apply, Module.End.mul_apply,
    HMT.IV.LatticeTranslationOperator.translation_vacuum, map_zero,
    sub_zero, LinearMap.smul_apply, Int.cast_zero, zero_add, one_smul] at h
  rw [(stateField_creates o u).2] at h
  exact h.symm

/-- Translating the actual state is exactly differentiating its field.
This is deduced from creation, locality and the just-proved covariance;
it is not imposed when the state-field map is defined. -/
theorem stateField_translated_state (o : Fin 12) (u : LatticeCarrier o) :
    stateField o (T o u) =
      HMT.IV.LatticeFieldDerivative.derivativeField (stateField o u) := by
  apply HMT.IV.LatticeCovariantFieldUniqueness.creative_covariant_fields_unique o
    _ _ (T o u)
  · exact HMT.IV.LatticeDescendantLocality.stateField_local o (T o u)
  · intro v
    exact HMT.IV.LatticeDerivativeLocality.derivative_local
      (HMT.IV.LatticeDescendantLocality.stateField_local o u v)
  · exact stateField_translation_covariant o (T o u)
  · exact HMT.IV.LatticeFieldDerivative.derivative_covariant
      (stateField_translation_covariant o u)
  · exact stateField_creates o (T o u)
  · constructor
    · exact HMT.IV.LatticeFieldDerivative.derivative_regular _ _ (stateField_creates o u).1
    · rw [HMT.IV.LatticeFieldDerivative.derivative_constant]
      exact stateField_translation_vacuum_coefficient o u

end HMT.IV.LatticeStateFieldTranslation
end

#print axioms HMT.IV.LatticeStateFieldTranslation.descendant_translation_covariant
#print axioms HMT.IV.LatticeStateFieldTranslation.stateField_translation_covariant
#print axioms HMT.IV.LatticeStateFieldTranslation.stateField_translation
#print axioms HMT.IV.LatticeStateFieldTranslation.stateField_translation_vacuum_coefficient
#print axioms HMT.IV.LatticeStateFieldTranslation.stateField_translated_state
