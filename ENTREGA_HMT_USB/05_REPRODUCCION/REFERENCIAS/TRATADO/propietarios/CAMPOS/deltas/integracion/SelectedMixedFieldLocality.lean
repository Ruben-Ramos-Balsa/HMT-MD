import SelectedFieldLocality
import LatticeMixedLocality

/-!
The mixed fields use the same selected origin and the same lattice carrier
as the regional incidence, generation, vacuum products and charged locality.
No second selection or replacement of that carrier is introduced.
-/
noncomputable section
namespace HMT.I.SelectedMixedFieldLocality

open HMT.I.SelectedRegionalIncidence HMT.I.SelectedExceptionalChain
open HMT.I.SelectedGeneratedFields HMT.I.SelectedFieldProducts
open HMT.I.SelectedFieldLocality
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeHeisenbergModes
open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeMixedLocalityCriterion

def SelectedMixedLocalityPublication : Prop :=
  ∀ (i : Fin (BasisSize selectedOrigin)) (y : Lattice selectedOrigin),
    crossing (mixedForward (hmode selectedOrigin i)
      (fieldCoefficient selectedOrigin y)) =
    crossing (mixedBackward (hmode selectedOrigin i)
      (fieldCoefficient selectedOrigin y))

theorem selected_mixed_fields_locality : SelectedMixedLocalityPublication :=
  HMT.IV.LatticeMixedLocality.heisenberg_charged_locality selectedOrigin

theorem selected_incidence_generation_products_and_both_localities :
    ConcreteIncidencePublication ∧ SelectedGenerationPublication ∧
      VacuumProductPublication ∧ SelectedLocalityPublication ∧
      SelectedMixedLocalityPublication := by
  obtain ⟨hi, hg, hp, hl⟩ := selected_incidence_generation_products_and_locality
  exact ⟨hi, hg, hp, hl, selected_mixed_fields_locality⟩

end HMT.I.SelectedMixedFieldLocality
end

#print axioms HMT.I.SelectedMixedFieldLocality.selected_mixed_fields_locality
#print axioms HMT.I.SelectedMixedFieldLocality.selected_incidence_generation_products_and_both_localities
