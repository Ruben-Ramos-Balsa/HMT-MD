import LatticeDescendantFields
import LatticeOscillatorWords
import LatticeNormalProductDerivativeBridge

/-!
The linear state-field map on the entire existing marked-lattice carrier.
Each oscillator occupation is represented by its multiset word. The genuine
normal products constructed previously supply its field; the existing basis
extends this assignment linearly. The creation and vacuum identities below
are proved. Mutual locality/Jacobi of arbitrary descendants and the twisted
orbifold are separate theorems, not assumptions hidden in this definition.
-/

noncomputable section
namespace HMT.IV.LatticeStateFieldMap

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeOscillatorWords
open HMT.IV.LatticeDescendantFields HMT.IV.TwistedGroupAlgebra
open scoped TensorProduct

theorem descendantState_eq_word (o : Fin 12) (x : Lattice o) (w : List (Mode o)) :
    descendantState o x w = stateForWord o w x := by
  induction w with
  | nil => rfl
  | cons m w ih => simp only [descendantState, stateForWord, ih]

def stateField (o : Fin 12) :
    LatticeCarrier o →ₗ[ℂ] VertexOperator ℂ (LatticeCarrier o) :=
  (carrierBasis o).constr ℂ (fun p =>
    descendantField o p.2 (wordForOccupation o p.1))

theorem stateField_basis (o : Fin 12) (a : Occupation o) (x : Lattice o) :
    stateField o (carrierBasis o (a,x)) =
      descendantField o x (wordForOccupation o a) :=
  Basis.constr_basis _ _ _ _

/-- Evaluation of a coefficient at the existing vacuum, as a linear map
on fields. This is used to prove, not prescribe, the creation identities. -/
def vacuumRead (o : Fin 12) (k : ℤ) :
    VertexOperator ℂ (LatticeCarrier o) →ₗ[ℂ] LatticeCarrier o where
  toFun B := HVertexOperator.coeff B k (vacuum o)
  map_add' B C := by
    simp only [HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
  map_smul' c B := by
    simp only [HVertexOperator.coeff_smul, Pi.smul_apply,
      LinearMap.smul_apply, RingHom.id_apply]

theorem stateField_creation_identity (o : Fin 12) :
    (vacuumRead o 0).comp (stateField o) = LinearMap.id := by
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  simp only [LinearMap.comp_apply, LinearMap.id_apply, stateField_basis,
    vacuumRead, LinearMap.coe_mk, AddHom.coe_mk,
    descendantField_recovers_state, descendantState_eq_word,
    carrierBasis_wordForOccupation]

theorem stateField_negative_vacuum (o : Fin 12) (k : ℤ) (hk : k < 0) :
    (vacuumRead o k).comp (stateField o) = 0 := by
  apply (carrierBasis o).ext
  rintro ⟨a,x⟩
  simp only [LinearMap.comp_apply, LinearMap.zero_apply, stateField_basis,
    vacuumRead, LinearMap.coe_mk, AddHom.coe_mk,
    descendantField_regular_at_vacuum o x _ k hk]

/-- Every state, not just a basis state or a chosen energy shell, is
recovered as the constant vacuum coefficient of its constructed field. -/
theorem stateField_creates (o : Fin 12) (v : LatticeCarrier o) :
    Creates o (stateField o v) v := by
  constructor
  · intro k hk
    exact LinearMap.congr_fun (stateField_negative_vacuum o k hk) v
  · exact LinearMap.congr_fun (stateField_creation_identity o) v

theorem stateField_injective (o : Fin 12) : Function.Injective (stateField o) := by
  intro v w h
  have hc := congrArg (vacuumRead o 0) h
  change ((vacuumRead o 0).comp (stateField o)) v =
    ((vacuumRead o 0).comp (stateField o)) w at hc
  simpa only [stateField_creation_identity, LinearMap.id_apply] using hc

theorem stateField_ground_state (o : Fin 12) (x : Lattice o) :
    stateField o ((1 : Fock o) ⊗ₜ[ℂ] basisElement o x) =
      HMT.IV.LatticeChargedVertexField.chargedField o x := by
  have hb : carrierBasis o (0,x) = (1 : Fock o) ⊗ₜ[ℂ] basisElement o x := by
    simpa only [wordOccupation, stateForWord] using (stateForWord_basis o [] x).symm
  rw [← hb, stateField_basis]
  simp only [wordForOccupation, Finsupp.toMultiset_zero, Multiset.toList_zero,
    descendantField]

theorem stateField_vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (stateField o (vacuum o)) k =
      if k=0 then (LinearMap.id : Module.End ℂ (LatticeCarrier o)) else 0 := by
  have hv : stateField o (vacuum o) =
      HMT.IV.LatticeChargedVertexField.chargedField o 0 :=
    stateField_ground_state o 0
  rw [hv]
  exact HMT.IV.LatticeChargedVertexField.fieldCoefficient_zero_charge o k

theorem stateField_laurent_bound (o : Fin 12) (u v : LatticeCarrier o) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff (stateField o u) k v = 0 :=
  HMT.IV.LatticeNormalOrderedField.field_has_bound o (stateField o u) v

theorem wordForOccupation_single (o : Fin 12) (m : Mode o) :
    wordForOccupation o (Finsupp.single m 1) = [m] := by
  simp only [wordForOccupation, Finsupp.toMultiset_single,
    one_nsmul, Multiset.toList_singleton]

/-- The state-field map agrees with the already constructed divided
Heisenberg field on every one-oscillator state. It does not introduce a
second family of Heisenberg generators. -/
theorem stateField_one_oscillator (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    stateField o (onCarrier o (create o n i) (vacuum o)) =
      HMT.IV.HeisenbergDerivativeModes.derivativeField o i n := by
  have hb : onCarrier o (create o n i) (vacuum o) =
      carrierBasis o (Finsupp.single (n,i) 1, 0) := by
    have h := stateForWord_basis o [(n,i)] 0
    simpa only [stateForWord, wordOccupation, add_zero] using h
  rw [hb, stateField_basis, wordForOccupation_single]
  exact HMT.IV.LatticeNormalProductDerivativeBridge.normalField_zero_charge o i n

end HMT.IV.LatticeStateFieldMap
end

#print axioms HMT.IV.LatticeStateFieldMap.stateField_creation_identity
#print axioms HMT.IV.LatticeStateFieldMap.stateField_negative_vacuum
#print axioms HMT.IV.LatticeStateFieldMap.stateField_creates
#print axioms HMT.IV.LatticeStateFieldMap.stateField_injective
#print axioms HMT.IV.LatticeStateFieldMap.stateField_ground_state
#print axioms HMT.IV.LatticeStateFieldMap.stateField_vacuum_coefficient
#print axioms HMT.IV.LatticeStateFieldMap.stateField_laurent_bound
#print axioms HMT.IV.LatticeStateFieldMap.stateField_one_oscillator
