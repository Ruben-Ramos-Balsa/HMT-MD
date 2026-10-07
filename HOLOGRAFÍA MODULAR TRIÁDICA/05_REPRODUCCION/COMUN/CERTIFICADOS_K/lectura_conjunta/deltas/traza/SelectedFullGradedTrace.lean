import LatticeFullGradedTrace

/-!
One selected origin, one constructed lattice and one carrier. The common
Article-I publication is extended by its full untwisted reflected trace in
all weights, not by a supplied trace identity or a finite coefficient test.
The weight is the oscillator-frequency plus lattice-half-norm grading.
No identification with a Virasoro L0, twisted orbifold or Monster is asserted.
-/

noncomputable section
namespace HMT.I.SelectedFullGradedTrace

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeParityCarrier
open HMT.IV.LatticeFullGradedTrace HMT.IV.OscillatorEulerProduct
open HMT.I.SelectedRegionalIncidence HMT.I.SelectedVOAInput
open HMT.I.SelectedHeisenbergInput HMT.I.SelectedGradedTrace HMT.Shared.ArticleI

theorem selected_full_trace (d : ℕ) :
    LinearMap.trace ℂ (fullWeightSpace selectedOrigin d)
      (fullTheta selectedOrigin d) =
        PowerSeries.coeff ℂ d (oscillatorProduct 24) := by
  rw [fullTheta_trace_product, selected_oscillator_rank]

theorem selected_full_vacuum_trace :
    LinearMap.trace ℂ (fullWeightSpace selectedOrigin 0)
      (fullTheta selectedOrigin 0) = 1 := by
  rw [selected_full_trace, oscillatorProduct_constant]

def FullReflectedTracePublication : Prop :=
  (∀ d, LinearMap.trace ℂ (fullWeightSpace selectedOrigin d)
    (fullTheta selectedOrigin d) = PowerSeries.coeff ℂ d (oscillatorProduct 24)) ∧
  (∀ d (v : fullWeightSpace selectedOrigin d),
    (fullTheta selectedOrigin d v : LatticeCarrier selectedOrigin) =
      carrierTheta selectedOrigin (v : LatticeCarrier selectedOrigin))

open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

theorem shared_action_electron_fields_and_full_trace
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧
      AlgebraicVertexInput ∧ SelectedHeisenbergPublication ∧
      SelectedGradedPublication ∧ FullReflectedTracePublication := by
  obtain ⟨hp, ha, hf, hg⟩ :=
    shared_action_electron_fields_and_graded_trace hU hunit x y r η
  exact ⟨hp, ha, hf, hg, selected_full_trace,
    fullTheta_is_actual_restriction selectedOrigin⟩

end HMT.I.SelectedFullGradedTrace
end

#print axioms HMT.I.SelectedFullGradedTrace.selected_full_trace
#print axioms HMT.I.SelectedFullGradedTrace.selected_full_vacuum_trace
#print axioms HMT.I.SelectedFullGradedTrace.shared_action_electron_fields_and_full_trace
