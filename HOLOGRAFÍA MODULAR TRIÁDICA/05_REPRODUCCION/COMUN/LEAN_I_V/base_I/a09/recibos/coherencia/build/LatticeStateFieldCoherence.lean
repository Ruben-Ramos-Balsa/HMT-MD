import LatticeNormalProductCommutation
import LatticeNormalProductLinear

/-! Recursion and uniqueness of the constructed state-field map on the
whole existing lattice carrier. The result does not assert a Jacobi identity. -/
noncomputable section
namespace HMT.IV.LatticeStateFieldCoherence
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeOscillatorWords
open HMT.IV.LatticeDescendantFields HMT.IV.LatticeStateFieldMap
open HMT.IV.LatticeNormalOrderedField HMT.IV.LatticeNormalProductLinear
open HMT.IV.LatticeNormalProductCommutation HMT.IV.TwistedGroupAlgebra
open scoped TensorProduct

theorem stateField_create_intertwines (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) :
    (stateField o).comp (onCarrier o (create o n i)) =
      (normalFieldLinear o i n).comp (stateField o) := by
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  simp only [LinearMap.comp_apply]
  rw [← carrierBasis_wordForOccupation o a x, ← descendantState_eq_word]
  change stateField o (descendantState o x ((n,i) :: wordForOccupation o a)) =
    normalField o i n (stateField o (descendantState o x (wordForOccupation o a)))
  rw [stateField_descendant, stateField_descendant]
  rfl

theorem stateField_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (u : LatticeCarrier o) :
    stateField o (onCarrier o (create o n i) u) = normalField o i n (stateField o u) :=
  LinearMap.congr_fun (stateField_create_intertwines o n i) u

/-- The linear assignment is determined by the previously constructed charged
fields and the actual normal-product recursion, not by a target character. -/
theorem stateField_unique (o : Fin 12)
    (Z : LatticeCarrier o →ₗ[ℂ] VertexOperator ℂ (LatticeCarrier o))
    (hground : ∀ x : Lattice o,
      Z ((1 : Fock o) ⊗ₜ[ℂ] basisElement o x) =
        HMT.IV.LatticeChargedVertexField.chargedField o x)
    (hcreate : ∀ (n : ℕ) (i : Fin (BasisSize o)) (u : LatticeCarrier o),
      Z (onCarrier o (create o n i) u) = normalField o i n (Z u)) :
    Z = stateField o := by
  have hw (x : Lattice o) (w : List (Mode o)) :
      Z (descendantState o x w) = descendantField o x w := by
    induction w with
    | nil => exact hground x
    | cons m w ih =>
      simp only [descendantState, descendantField, hcreate, ih]
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  rw [← carrierBasis_wordForOccupation o a x, ← descendantState_eq_word]
  rw [hw, stateField_descendant]

end HMT.IV.LatticeStateFieldCoherence
end

#print axioms HMT.IV.LatticeStateFieldCoherence.stateField_create_intertwines
#print axioms HMT.IV.LatticeStateFieldCoherence.stateField_create
#print axioms HMT.IV.LatticeStateFieldCoherence.stateField_unique
