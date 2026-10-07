import LatticeStateFieldMap
import SelectedMixedFieldLocality

/-!
State-field realization over the same origin already selected by the regional
incidence of K and alpha. No independent lattice, Gram matrix, charge panel,
or replacement of the selected register is supplied here.
-/

noncomputable section
namespace HMT.I.SelectedStateField

open HMT.I.SelectedRegionalIncidence
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeStateFieldMap HMT.IV.LatticeDescendantFields
open HMT.IV.TwistedGroupAlgebra
open scoped TensorProduct

abbrev carrier := LatticeCarrier selectedOrigin

def Y : carrier →ₗ[ℂ] VertexOperator ℂ carrier := stateField selectedOrigin

theorem selected_field_creates (v : carrier) :
    Creates selectedOrigin (Y v) v := stateField_creates selectedOrigin v

theorem selected_field_injective : Function.Injective Y :=
  stateField_injective selectedOrigin

theorem selected_ground_field (x : Lattice selectedOrigin) :
    Y ((1 : Fock selectedOrigin) ⊗ₜ[ℂ] basisElement selectedOrigin x) =
      HMT.IV.LatticeChargedVertexField.chargedField selectedOrigin x :=
  stateField_ground_state selectedOrigin x

theorem selected_vacuum_field (k : ℤ) :
    HVertexOperator.coeff (Y (vacuum selectedOrigin)) k =
      if k=0 then (LinearMap.id : Module.End ℂ carrier) else 0 :=
  stateField_vacuum_coefficient selectedOrigin k

theorem selected_field_truncation (u v : carrier) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff (Y u) k v = 0 :=
  stateField_laurent_bound selectedOrigin u v

/-- The constructed state-field map and the generating-field localities
share one selected portador. Locality of arbitrary descendants is not
silently substituted for these already proved generating-field statements. -/
theorem selected_state_fields_and_generator_localities :
    (∀ v : carrier, Creates selectedOrigin (Y v) v) ∧
    Function.Injective Y ∧
    HMT.I.SelectedFieldLocality.SelectedLocalityPublication ∧
    HMT.I.SelectedMixedFieldLocality.SelectedMixedLocalityPublication :=
  ⟨selected_field_creates, selected_field_injective,
    HMT.I.SelectedFieldLocality.selected_charged_fields_locality,
    HMT.I.SelectedMixedFieldLocality.selected_mixed_fields_locality⟩

end HMT.I.SelectedStateField
end

#print axioms HMT.I.SelectedStateField.selected_field_creates
#print axioms HMT.I.SelectedStateField.selected_field_injective
#print axioms HMT.I.SelectedStateField.selected_ground_field
#print axioms HMT.I.SelectedStateField.selected_vacuum_field
#print axioms HMT.I.SelectedStateField.selected_field_truncation
#print axioms HMT.I.SelectedStateField.selected_state_fields_and_generator_localities
