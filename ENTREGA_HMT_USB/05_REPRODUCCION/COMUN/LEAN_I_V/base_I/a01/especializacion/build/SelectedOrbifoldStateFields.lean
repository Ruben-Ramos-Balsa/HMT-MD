import SelectedConformalVertex
import LatticeOrbifoldFullStateFields
import LatticeOrbifoldGrading

/-! Specialization to the same HMT-selected marked lattice. The terminal
selection is reused, not supplied again or reconstructed. Its existing
Lean.ofReduceBool computational trust dependency is recorded explicitly by
the public axiom probes; it is not hidden among ordinary-only generic lemmas. -/

noncomputable section
namespace HMT.I.SelectedOrbifoldStateFields
open SelectedRegionalIncidence
open HMT.IV.LatticeOrbifoldCarrier HMT.IV.LatticeOrbifoldGrading
open HMT.IV.LatticeOrbifoldFullStateFields HMT.IV.LatticeTwistedPairProduct
open HMT.IV.LatticeEvenVertexFields HMT.IV.LatticeTwistedPositiveSector
open HMT.IV.LatticeTwistedContragredientCoefficients HMT.IV.LatticeEvenPairingRepresentability
open HMT.IV.LatticeOrbifoldEvenAction HMT.IV.LatticeTwistedPositiveStateDescent
open HMT.IV.LatticeTwistedEvenProduct

abbrev carrier := Space selectedOrigin

def Y : carrier →ₗ[ℂ] VertexOperator ℂ carrier := stateField selectedOrigin

theorem selected_all_products_constructed :
    (∀ u v : carrier, ∀ k : ℤ,
      HVertexOperator.coeff (Y u) k v =
        (evenCoefficient selectedOrigin u.1 k v.1 + pairCoefficient selectedOrigin k u.2 v.2,
         HVertexOperator.coeff (positiveDescendedAssignment selectedOrigin u.1) k v.2 +
           HVertexOperator.coeff (twistedEvenField selectedOrigin u.2) k v.1)) ∧
    (∀ v w : positiveSector selectedOrigin, ∀ k : ℤ, ∀ a : evenSpace selectedOrigin,
      evenPairing selectedOrigin
        (pairCoefficient selectedOrigin k v w) a =
      contragredientCoefficient selectedOrigin k v w a) :=
  ⟨stateField_coefficient selectedOrigin,
    fun v w k a => pairCoefficient_pair selectedOrigin k v w a⟩

theorem selected_vacuum_creation :
    (∀ k : ℤ, HVertexOperator.coeff (Y (vacuum selectedOrigin)) k =
      if k=0 then (1 : Module.End ℂ carrier) else 0) ∧
    (∀ u : carrier, HVertexOperator.coeff (Y u) 0 (vacuum selectedOrigin) = u) ∧
    (∀ u : carrier, ∀ k < (0:ℤ), HVertexOperator.coeff (Y u) k (vacuum selectedOrigin) = 0) ∧
    Function.Injective Y :=
  ⟨stateField_vacuum selectedOrigin, stateField_creation selectedOrigin,
    stateField_negative_vacuum selectedOrigin, stateField_injective selectedOrigin⟩

theorem selected_conformal_fields (m : ℤ) :
    HVertexOperator.coeff (Y (conformalState selectedOrigin)) (-m-2) =
      modes selectedOrigin m := stateField_conformal_coefficient selectedOrigin m

theorem selected_low_weights :
    Module.End.eigenspace (modes selectedOrigin 0) (0:ℂ) =
      Submodule.span ℂ {vacuum selectedOrigin} ∧
    Module.End.eigenspace (modes selectedOrigin 0) (1:ℂ) = ⊥ :=
  ⟨weight_zero_vacuum_line selectedOrigin, weight_one_zero selectedOrigin⟩

end HMT.I.SelectedOrbifoldStateFields
end

#print axioms HMT.I.SelectedOrbifoldStateFields.carrier
#print axioms HMT.I.SelectedOrbifoldStateFields.Y
#print axioms HMT.I.SelectedOrbifoldStateFields.selected_all_products_constructed
#print axioms HMT.I.SelectedOrbifoldStateFields.selected_vacuum_creation
#print axioms HMT.I.SelectedOrbifoldStateFields.selected_conformal_fields
#print axioms HMT.I.SelectedOrbifoldStateFields.selected_low_weights
