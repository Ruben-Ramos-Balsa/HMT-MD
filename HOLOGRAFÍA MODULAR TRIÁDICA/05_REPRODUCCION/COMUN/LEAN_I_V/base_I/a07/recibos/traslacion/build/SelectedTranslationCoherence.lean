import SelectedDescendantLocality
import LatticeStateFieldTranslation

/-! Locality, creation and both translation identities on the one lattice
already selected by the HMT regional incidence. No second origin, carrier,
vacuum, translation or state-field map is supplied. -/

noncomputable section
namespace HMT.I.SelectedTranslationCoherence

open HMT.I.SelectedRegionalIncidence HMT.I.SelectedStateField
open HMT.I.SelectedDescendantLocality
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFieldLocality
open HMT.IV.LatticeTranslationOperator HMT.IV.LatticeTranslationLinear
open HMT.IV.LatticeStateFieldTranslation HMT.IV.LatticeFieldDerivative
open HMT.IV.LatticeDescendantFields

theorem selected_translation_covariant (u : carrier) :
    TranslationCovariant (translation selectedOrigin) (Y u) :=
  stateField_translation_covariant selectedOrigin u

theorem selected_translated_state (u : carrier) :
    Y (translation selectedOrigin u) = derivativeField (Y u) :=
  stateField_translated_state selectedOrigin u

/-- The local vertex-algebra identities are proved for the actual inherited
state-field map, not received as parameters of a prospective realization. -/
theorem selected_local_translation_publication :
    translation selectedOrigin (vacuum selectedOrigin) = 0 ∧
    (∀ u : carrier, Creates selectedOrigin (Y u) u) ∧
    (∀ k : ℤ, HVertexOperator.coeff (Y (vacuum selectedOrigin)) k =
      if k=0 then (LinearMap.id : Module.End ℂ carrier) else 0) ∧
    (∀ u v : carrier, Local (Y u) (Y v)) ∧
    (∀ u : carrier, TranslationCovariant (translation selectedOrigin) (Y u)) ∧
    (∀ u : carrier, Y (translation selectedOrigin u) = derivativeField (Y u)) :=
  ⟨translation_vacuum selectedOrigin, selected_field_creates, selected_vacuum_field,
    selected_fields_local, selected_translation_covariant, selected_translated_state⟩

end HMT.I.SelectedTranslationCoherence
end

#print axioms HMT.I.SelectedTranslationCoherence.selected_translation_covariant
#print axioms HMT.I.SelectedTranslationCoherence.selected_translated_state
#print axioms HMT.I.SelectedTranslationCoherence.selected_local_translation_publication
