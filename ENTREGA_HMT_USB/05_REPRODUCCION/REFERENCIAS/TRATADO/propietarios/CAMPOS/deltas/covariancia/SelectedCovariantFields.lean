import SelectedEnergyInput
import LatticeChargedFieldCharge
import LatticeChargedFieldParity
import LatticeTranslationOperator
import LatticeExponentialCommutator
import LatticeAnnihilationCommutativity
import LatticeCoxeterTwistedLift
import LatticeTranslationVacuum

/-!
Operator continuation of the same selected Article-I origin. Charge,
parity, translation and mixed commutators concern the actual fields and
carrier already constructed. Earlier action/electron conditions are not
discarded or silently promoted. This theorem is not named as FLM or VOA
Jacobi, neither of which is its conclusion.
-/

noncomputable section
namespace HMT.I.SelectedCovariantFields

open HMT.IV
open HMT.I.SelectedRegionalIncidence HMT.I.SelectedVOAInput
open HMT.I.SelectedHeisenbergInput HMT.I.SelectedGradedTrace
open HMT.I.SelectedFullGradedTrace HMT.I.SelectedEnergyInput HMT.Shared.ArticleI
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeEnergyGrading HMT.IV.LatticeZeroModes
open HMT.IV.LatticeParityCarrier HMT.IV.LatticeChargedVertexField
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeChargedFieldCharge HMT.IV.LatticeChargedFieldParity
open HMT.IV.LatticeExponentialCommutator HMT.IV.LatticeCoxeterTwistedLift

def SelectedCovariancePublication : Prop :=
  (∀ (u x : Lattice selectedOrigin) (k : ℤ),
    (onLattice selectedOrigin (zeroMode selectedOrigin u)).comp
        (fieldCoefficient selectedOrigin x k) -
      (fieldCoefficient selectedOrigin x k).comp
        (onLattice selectedOrigin (zeroMode selectedOrigin u)) =
      (integerPair selectedOrigin u x : ℂ) • fieldCoefficient selectedOrigin x k) ∧
  (∀ (x : Lattice selectedOrigin) (k : ℤ),
    (carrierTheta selectedOrigin).comp (fieldCoefficient selectedOrigin x k) =
      (fieldCoefficient selectedOrigin (-x) k).comp (carrierTheta selectedOrigin)) ∧
  (LatticeTranslationOperator.translation selectedOrigin (vacuum selectedOrigin) = 0) ∧
  ((energy selectedOrigin).comp (LatticeTranslationOperator.translation selectedOrigin) -
    (LatticeTranslationOperator.translation selectedOrigin).comp (energy selectedOrigin) =
      LatticeTranslationOperator.translation selectedOrigin) ∧
  (∀ (x y : Lattice selectedOrigin) (n d : ℕ) (v : Fock selectedOrigin),
    chargeAnnihilation selectedOrigin x n (creationExponentialMode selectedOrigin y d v) -
      creationExponentialMode selectedOrigin y d (chargeAnnihilation selectedOrigin x n v) =
      if n+1 ≤ d then (integerPair selectedOrigin x y : ℂ) •
        creationExponentialMode selectedOrigin y (d-(n+1)) v else 0) ∧
  (∀ f : TwistedAlgebra selectedOrigin,
    twistedEquiv selectedOrigin (twistedEquiv selectedOrigin (twistedEquiv selectedOrigin f)) = f) ∧
  (∀ (x : Lattice selectedOrigin) (k : ℤ),
    LatticeTranslationOperator.translation selectedOrigin
      (fieldCoefficient selectedOrigin x k (vacuum selectedOrigin)) =
      ((k : ℂ)+1) • fieldCoefficient selectedOrigin x (k+1) (vacuum selectedOrigin))

theorem selected_covariance_publication : SelectedCovariancePublication :=
  ⟨zeroMode_fieldCoefficient selectedOrigin, theta_fieldCoefficient selectedOrigin,
    LatticeTranslationOperator.translation_vacuum selectedOrigin,
    LatticeTranslationOperator.translation_energy selectedOrigin,
    mixed_exponential_commutator_pairing selectedOrigin,
    twistedEquiv_cube selectedOrigin,
    LatticeTranslationVacuum.translation_vacuum_coefficient selectedOrigin⟩

open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

theorem shared_action_electron_covariant_fields
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧
      AlgebraicVertexInput ∧ SelectedHeisenbergPublication ∧
      SelectedGradedPublication ∧ FullReflectedTracePublication ∧
      SelectedEnergyPublication ∧ SelectedChargedFieldPublication ∧
      SelectedCovariancePublication := by
  obtain ⟨ha,hb,hc,hd,he,hf,hg⟩ :=
    shared_action_electron_energy_and_fields hU hunit x y r η
  exact ⟨ha,hb,hc,hd,he,hf,hg,selected_covariance_publication⟩

end HMT.I.SelectedCovariantFields
end

#print axioms HMT.I.SelectedCovariantFields.selected_covariance_publication
#print axioms HMT.I.SelectedCovariantFields.shared_action_electron_covariant_fields
