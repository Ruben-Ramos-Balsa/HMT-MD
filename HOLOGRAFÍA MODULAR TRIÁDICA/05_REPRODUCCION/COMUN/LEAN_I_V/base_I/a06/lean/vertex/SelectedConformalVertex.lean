import SelectedTranslationCoherence
import LatticeStateFieldProducts
import LatticeConformalGrading
import LatticeVirasoroRelations
import LatticeConformalTranslation
import LatticeEvenTranslation

/-! One terminal interface for the actual HMT-selected lattice fields.
The origin, carrier, vacuum and fields are inherited; no new selection,
lattice, vertex product or central charge is supplied as a hypothesis.
The classic twisted extension is not defined by this untwisted interface. -/

noncomputable section
namespace HMT.I.SelectedConformalVertex

open SelectedRegionalIncidence SelectedStateField SelectedTranslationCoherence
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeDescendantFields
open HMT.IV.LatticeFieldLocality HMT.IV.LatticeTranslationOperator
open HMT.IV.LatticeTranslationLinear HMT.IV.LatticeFieldDerivative
open HMT.IV.LatticeResidueProducts HMT.IV.LatticeStateFieldProducts
open HMT.IV.LatticeConformalState HMT.IV.LatticeConformalEnergy
open HMT.IV.LatticeConformalTranslation HMT.IV.LatticeConformalGrading
open HMT.IV.LatticeVirasoroRelations HMT.IV.LatticeEnergyGrading
open HMT.IV.LatticeParityCarrier HMT.IV.LatticeEvenTranslation
open HMT.IV.LatticeStateFieldParity

theorem selected_vertex_products (p : ℤ) (u v : carrier) :
    Y (HVertexOperator.coeff (Y u) (-p-1) v) = residueField p (Y u) (Y v) :=
  stateField_residue_product selectedOrigin p u v

theorem selected_virasoro (m n : ℤ) :
    conformalMode selectedOrigin m * conformalMode selectedOrigin n -
      conformalMode selectedOrigin n * conformalMode selectedOrigin m =
    ((m-n : ℤ) : ℂ) • conformalMode selectedOrigin (m+n) +
      (if m+n=0 then (2*((m : ℂ)^3-(m : ℂ))) •
        (LinearMap.id : Module.End ℂ carrier) else 0) :=
  virasoro_central_charge_twentyFour selectedOrigin m n

/-- The locality presentation, residue-product identity, Virasoro action,
finite nonnegative conformal grading and reflection all refer to one Y.
Every field of this proposition is a proved output, not an input record. -/
theorem selected_local_conformal_publication :
    translation selectedOrigin (vacuum selectedOrigin) = 0 ∧
    (∀ u : carrier, Creates selectedOrigin (Y u) u) ∧
    (∀ k : ℤ, HVertexOperator.coeff (Y (vacuum selectedOrigin)) k =
      if k=0 then (LinearMap.id : Module.End ℂ carrier) else 0) ∧
    (∀ u v : carrier, Local (Y u) (Y v)) ∧
    (∀ u : carrier, TranslationCovariant (translation selectedOrigin) (Y u)) ∧
    (∀ u : carrier, Y (translation selectedOrigin u) = derivativeField (Y u)) ∧
    (∀ p : ℤ, ∀ u v : carrier,
      Y (HVertexOperator.coeff (Y u) (-p-1) v) = residueField p (Y u) (Y v)) ∧
    conformalMode selectedOrigin (-1) = translation selectedOrigin ∧
    conformalMode selectedOrigin 0 = energy selectedOrigin ∧
    (∀ m n : ℤ, conformalMode selectedOrigin m * conformalMode selectedOrigin n -
      conformalMode selectedOrigin n * conformalMode selectedOrigin m =
      ((m-n : ℤ) : ℂ) • conformalMode selectedOrigin (m+n) +
        (if m+n=0 then (2*((m : ℂ)^3-(m : ℂ))) •
          (LinearMap.id : Module.End ℂ carrier) else 0)) ∧
    (∀ d : ℕ, FiniteDimensional ℂ
      (Module.End.eigenspace (conformalMode selectedOrigin 0) (d : ℂ))) ∧
    (⨆ d : ℕ, Module.End.eigenspace (conformalMode selectedOrigin 0) (d : ℂ)) = ⊤ ∧
    Module.End.eigenspace (conformalMode selectedOrigin 0) 0 =
      Submodule.span ℂ {vacuum selectedOrigin} ∧
    carrierTheta selectedOrigin (conformalState selectedOrigin) =
      conformalState selectedOrigin ∧
    (∀ u : carrier, ∀ k : ℤ,
      carrierTheta selectedOrigin * HVertexOperator.coeff (Y u) k =
      HVertexOperator.coeff (Y (carrierTheta selectedOrigin u)) k *
        carrierTheta selectedOrigin) := by
  rcases selected_local_translation_publication with ⟨h1,h2,h3,h4,h5,h6⟩
  exact ⟨h1,h2,h3,h4,h5,h6,selected_vertex_products,
    conformalMode_neg_one_eq_translation selectedOrigin,
    conformalMode_zero_eq_energy selectedOrigin,selected_virasoro,
    conformal_weight_finite selectedOrigin,conformal_weights_span selectedOrigin,
    conformal_weight_zero selectedOrigin,conformalState_fixed selectedOrigin,
    theta_stateField_intertwines selectedOrigin⟩

end HMT.I.SelectedConformalVertex
end

#print axioms HMT.I.SelectedConformalVertex.selected_vertex_products
#print axioms HMT.I.SelectedConformalVertex.selected_virasoro
#print axioms HMT.I.SelectedConformalVertex.selected_local_conformal_publication
