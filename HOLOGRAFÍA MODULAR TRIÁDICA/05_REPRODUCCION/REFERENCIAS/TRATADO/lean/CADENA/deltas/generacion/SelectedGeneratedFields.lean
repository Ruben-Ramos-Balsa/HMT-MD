import SelectedCovariantFields
import APPWittOperatorTransport
import LatticeTranslationCommutators
import LatticeFieldGeneration
import LatticePolynomialExchange

/-!
The previous Article-I selected origin, with its entire published conjunction,
now has a proved generating family and the exact normal-ordering factor.
No earlier hypothesis is erased, and FLM is not inserted as an assumption.
-/

noncomputable section
namespace HMT.I.SelectedGeneratedFields

open HMT.IV
open HMT.I.SelectedRegionalIncidence HMT.I.SelectedVOAInput
open HMT.I.SelectedHeisenbergInput HMT.I.SelectedGradedTrace
open HMT.I.SelectedFullGradedTrace HMT.I.SelectedEnergyInput
open HMT.I.SelectedCovariantFields HMT.Shared.ArticleI
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialContraction HMT.IV.LatticeNormalOrdering
open HMT.IV.LatticeContractionFactor HMT.IV.LatticePolynomialExchange
open HMT.IV.LatticeFieldGeneration HMT.IV.LatticeTranslationCommutators
open HMT.IV.LatticeZeroModes

def SelectedGenerationPublication : Prop :=
  generatedSpace selectedOrigin = ⊤ ∧
  (∀ x y : Lattice selectedOrigin,
    annihilationSeries selectedOrigin x *
        PowerSeries.C (Inner selectedOrigin) (creationSeries selectedOrigin y) =
      contractionSeries selectedOrigin (integerPair selectedOrigin x y) *
        PowerSeries.C (Inner selectedOrigin) (creationSeries selectedOrigin y) *
        annihilationSeries selectedOrigin x) ∧
  (∀ (x : Lattice selectedOrigin) (n : ℕ),
    (LatticeTranslationOperator.translation selectedOrigin).comp
        (onCarrier selectedOrigin (chargeCreation selectedOrigin x n)) -
      (onCarrier selectedOrigin (chargeCreation selectedOrigin x n)).comp
        (LatticeTranslationOperator.translation selectedOrigin) =
      (n+1 : ℂ) • onCarrier selectedOrigin (chargeCreation selectedOrigin x (n+1))) ∧
  (∀ x : Lattice selectedOrigin,
    (LatticeTranslationOperator.translation selectedOrigin).comp
        (onCarrier selectedOrigin (chargeAnnihilation selectedOrigin x 0)) -
      (onCarrier selectedOrigin (chargeAnnihilation selectedOrigin x 0)).comp
        (LatticeTranslationOperator.translation selectedOrigin) =
      -onLattice selectedOrigin (zeroMode selectedOrigin x)) ∧
  (∀ z : APPWittOperatorTransport.APP,
    CoxeterNeighbor.action CoxeterNeighbor.wittOrientation
        (APPWittOperatorTransport.transport z) =
      APPWittOperatorTransport.transport (APPWittOperatorTransport.appAction z)) ∧
  (∀ x y : Lattice selectedOrigin,
    ∃ n m : ℕ, (m : ℤ)-(n : ℤ)=integerPair selectedOrigin x y ∧
      (1-crossVariable selectedOrigin)^n *
          (annihilationSeries selectedOrigin x *
            PowerSeries.C (Inner selectedOrigin) (creationSeries selectedOrigin y)) =
        (1-crossVariable selectedOrigin)^m *
          (PowerSeries.C (Inner selectedOrigin) (creationSeries selectedOrigin y) *
            annihilationSeries selectedOrigin x))

theorem selected_generation_publication : SelectedGenerationPublication :=
  ⟨generatedSpace_eq_top selectedOrigin, exponential_normal_order selectedOrigin,
    translation_chargeCreate selectedOrigin, translation_chargeAnnihilate_zero selectedOrigin,
    APPWittOperatorTransport.transport_intertwines,
    polynomial_exchange_all_charges selectedOrigin⟩

open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

theorem shared_action_electron_generated_fields
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧
      AlgebraicVertexInput ∧ SelectedHeisenbergPublication ∧
      SelectedGradedPublication ∧ FullReflectedTracePublication ∧
      SelectedEnergyPublication ∧ SelectedChargedFieldPublication ∧
      SelectedCovariancePublication ∧ SelectedGenerationPublication := by
  obtain ⟨ha,hb,hc,hd,he,hf,hg,hh⟩ :=
    shared_action_electron_covariant_fields hU hunit x y r η
  exact ⟨ha,hb,hc,hd,he,hf,hg,hh,selected_generation_publication⟩

end HMT.I.SelectedGeneratedFields
end

#print axioms HMT.I.SelectedGeneratedFields.selected_generation_publication
#print axioms HMT.I.SelectedGeneratedFields.shared_action_electron_generated_fields
