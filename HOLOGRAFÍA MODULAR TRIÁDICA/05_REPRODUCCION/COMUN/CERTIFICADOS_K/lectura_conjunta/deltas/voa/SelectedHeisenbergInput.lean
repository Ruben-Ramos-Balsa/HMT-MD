import SelectedVOAInput
import LatticeHeisenbergField

/-!
The selected Article I lattice now carries actual Mathlib `VertexOperator`
fields: linear maps into vector-valued Laurent series with pointwise lower
truncation proved from the algebraic construction. Their normalized modes
are identified with the generated Heisenberg modes and satisfy coefficientwise
order-two locality. The action/electronic publication keeps its exact prior
parameters and hypotheses. This is a generating-field result, not a claim
that a full lattice VOA, the twisted sector, FLM or Moonshine is formalized.
-/

noncomputable section
namespace HMT.I.SelectedHeisenbergInput

open HMT.I.SelectedRegionalIncidence HMT.I.SelectedVOAInput
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeHeisenbergField
open HMT.Shared.ArticleI

/-- These are constructed fields on the same selected carrier, not fields
supplied as a further assumption to the common theorem. -/
def selectedFields (i : Fin (BasisSize selectedOrigin)) :
    VertexOperator ℂ SelectedCarrier := heisenbergField selectedOrigin i

def SelectedHeisenbergPublication : Prop :=
  (∀ (i : Fin (BasisSize selectedOrigin)) (n : ℤ),
    VertexOperator.ncoeff (selectedFields i) n = hmode selectedOrigin i n) ∧
  (∀ (i j : Fin (BasisSize selectedOrigin)) (m n : ℤ),
    (VertexOperator.ncoeff (selectedFields i) m).comp
        (VertexOperator.ncoeff (selectedFields j) n) -
      (VertexOperator.ncoeff (selectedFields j) n).comp
        (VertexOperator.ncoeff (selectedFields i) m) =
      (if m+n=0 then (m : ℂ) * gram selectedOrigin i j else 0) •
        (LinearMap.id : Module.End ℂ SelectedCarrier)) ∧
  (∀ (i j : Fin (BasisSize selectedOrigin)) (m n : ℤ),
    orderTwoLocalityCoefficient selectedOrigin i j m n = 0)

open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

/-- A common endpoint keeps the existing action/electronic branch and its
algebraic vertex inputs, and appends the constructed local Heisenberg fields. -/
theorem shared_action_electron_heisenberg_fields
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧
      AlgebraicVertexInput ∧ SelectedHeisenbergPublication := by
  obtain ⟨hpublication, halgebraic⟩ :=
    shared_action_electron_vertex_input hU hunit x y r η
  refine ⟨hpublication, halgebraic, ?_, ?_, ?_⟩
  · intro i n
    exact heisenbergField_ncoeff selectedOrigin i n
  · intro i j m n
    exact heisenbergField_mode_relation selectedOrigin i j m n
  · intro i j m n
    exact heisenbergField_locality_order_two selectedOrigin i j m n

end HMT.I.SelectedHeisenbergInput
end

#print axioms HMT.I.SelectedHeisenbergInput.shared_action_electron_heisenberg_fields
