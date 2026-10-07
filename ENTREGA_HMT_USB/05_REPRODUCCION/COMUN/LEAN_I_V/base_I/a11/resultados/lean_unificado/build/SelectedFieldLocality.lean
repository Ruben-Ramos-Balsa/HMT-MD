import SelectedFieldProducts
import LatticeChargedLocalityFull

/-! The uniformly local charged fields are those on the already selected
HMT lattice carrier. Concrete incidence and full field generation are
preserved in the same dependency chain; locality is a proved conclusion. -/
noncomputable section
namespace HMT.I.SelectedFieldLocality
open HMT.I.SelectedRegionalIncidence HMT.I.SelectedExceptionalChain
open HMT.I.SelectedGeneratedFields HMT.I.SelectedFieldProducts
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeFactorConvolution
open HMT.IV.LatticeFieldBiOperators HMT.IV.LatticeChargedLocalityFull

def SelectedLocalityPublication : Prop :=
  ∀ x y : Lattice selectedOrigin, ∃ n : ℕ,
    (crossing^n) (forwardProduct selectedOrigin x y) =
      (crossing^n) (backwardProduct selectedOrigin x y)

theorem selected_charged_fields_locality : SelectedLocalityPublication :=
  charged_fields_locality selectedOrigin

theorem selected_incidence_generation_products_and_locality :
    ConcreteIncidencePublication ∧ SelectedGenerationPublication ∧
      VacuumProductPublication ∧ SelectedLocalityPublication :=
  ⟨concrete_incidence_publication,selected_generation_publication,
    selected_vacuum_products,selected_charged_fields_locality⟩

end HMT.I.SelectedFieldLocality
end
#print axioms HMT.I.SelectedFieldLocality.selected_charged_fields_locality
#print axioms HMT.I.SelectedFieldLocality.selected_incidence_generation_products_and_locality
