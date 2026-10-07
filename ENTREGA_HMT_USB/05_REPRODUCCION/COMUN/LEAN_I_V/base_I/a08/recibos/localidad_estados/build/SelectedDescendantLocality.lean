import SelectedStateField
import LatticeDescendantLocality

/-!
Mutual locality of the state-field map on the same HMT-selected lattice.
The origin, carrier and map Y are imported unchanged. No second lattice,
selector, target register or replacement state-field map is supplied.
-/

noncomputable section
namespace HMT.I.SelectedDescendantLocality

open HMT.I.SelectedRegionalIncidence HMT.I.SelectedStateField
open HMT.IV.LatticeFieldLocality HMT.IV.LatticeDescendantLocality
open HMT.IV.LatticeDescendantFields HMT.IV.LatticeOscillatorFock

theorem selected_fields_local (u v : carrier) : Local (Y u) (Y v) :=
  stateField_local selectedOrigin u v

/-- The actual selected state-field map has creation, injectivity,
the vacuum identity and pairwise locality on its entire carrier.
This publication is not relabeled as a twisted-sector or FLM theorem. -/
theorem selected_local_state_field_publication :
    (∀ v : carrier, Creates selectedOrigin (Y v) v) ∧
    Function.Injective Y ∧
    (∀ k : ℤ, HVertexOperator.coeff (Y (vacuum selectedOrigin)) k =
      if k=0 then (LinearMap.id : Module.End ℂ carrier) else 0) ∧
    (∀ u v : carrier, Local (Y u) (Y v)) :=
  ⟨selected_field_creates, selected_field_injective,
    selected_vacuum_field, selected_fields_local⟩

end HMT.I.SelectedDescendantLocality
end

#print axioms HMT.I.SelectedDescendantLocality.selected_fields_local
#print axioms HMT.I.SelectedDescendantLocality.selected_local_state_field_publication
