import SelectedExceptionalChain
import LatticeVacuumContraction

/-! The same selected origin with the all-degree vacuum product coefficients.
The predecessor entry and all its hypotheses are preserved by import. -/
noncomputable section
namespace HMT.I.SelectedFieldProducts

open HMT.I.SelectedExceptionalChain HMT.I.SelectedGeneratedFields
open HMT.I.SelectedRegionalIncidence
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialContraction HMT.IV.LatticeVacuumContraction

def VacuumProductPublication : Prop :=
  ∀ (x y : Lattice selectedOrigin) (r d : ℕ),
    exponentialCoefficient selectedOrigin x r
        (creationExponentialMode selectedOrigin y d 1) =
      if r ≤ d then scalarContraction (integerPair selectedOrigin x y) r •
        creationExponentialMode selectedOrigin y (d-r) 1 else 0

theorem selected_vacuum_products : VacuumProductPublication :=
  vacuum_contraction selectedOrigin

theorem selected_incidence_generation_and_products :
    ConcreteIncidencePublication ∧ SelectedGenerationPublication ∧
      VacuumProductPublication :=
  ⟨concrete_incidence_publication, selected_generation_publication,
    selected_vacuum_products⟩

end HMT.I.SelectedFieldProducts
end

#print axioms HMT.I.SelectedFieldProducts.selected_vacuum_products
#print axioms HMT.I.SelectedFieldProducts.selected_incidence_generation_and_products
