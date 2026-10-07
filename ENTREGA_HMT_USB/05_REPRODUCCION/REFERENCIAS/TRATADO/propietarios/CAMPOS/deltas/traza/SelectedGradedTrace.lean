import FockFiniteParityPiece
import LatticeWeightFiniteness
import WeightedEulerBridge
import SelectedHeisenbergInput

/-!
The selected Article-I oscillator algebra has finite pieces at every weight.
The restriction of its already constructed involution has exactly the
coefficient of the arbitrary-depth product of inverse oscillator factors.
No additional parity operator, target coefficient, or FLM axiom is an input.
-/

noncomputable section
namespace HMT.I.SelectedGradedTrace

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeParityCarrier
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeWeightFiniteness
open HMT.IV.LatticeCocycle HMT.IV.FockFiniteParityPiece
open HMT.IV.OscillatorEulerProduct
open HMT.I.SelectedRegionalIncidence HMT.I.SelectedVOAInput
open HMT.I.SelectedHeisenbergInput HMT.Shared.ArticleI

abbrev weightLabels (o : Fin 12) (d : ℕ) : WeightOccupation o d → Occupation o :=
  Subtype.val

abbrev OscillatorWeightSpace (o : Fin 12) (d : ℕ) := piece o (weightLabels o d)

def weightTheta (o : Fin 12) (d : ℕ) : Module.End ℂ (OscillatorWeightSpace o d) :=
  pieceTheta o (weightLabels o d) Subtype.val_injective

theorem weightTheta_is_restriction (o : Fin 12) (d : ℕ)
    (v : OscillatorWeightSpace o d) :
    (weightTheta o d v : Fock o) = fockTheta o (v : Fock o) :=
  pieceTheta_is_actual_restriction o (weightLabels o d) Subtype.val_injective v

theorem weight_trace_product (o : Fin 12) (d : ℕ) :
    LinearMap.trace ℂ (OscillatorWeightSpace o d) (weightTheta o d) =
      PowerSeries.coeff ℂ d (oscillatorProduct (BasisSize o)) := by
  rw [← HMT.IV.WeightedEulerBridge.trace_eq_oscillator_coefficient d d (BasisSize o) le_rfl]
  rw [HMT.IV.WeightedOscillatorTrace.trace_parityOperator]
  change LinearMap.trace ℂ (piece o (weightLabels o d))
    (pieceTheta o (weightLabels o d) Subtype.val_injective) = _
  rw [actual_piece_trace]
  apply Fintype.sum_equiv (weightEquivFinite o d)
  intro a
  rw [occupationLength_equiv o d a]

theorem selected_weight_trace (d : ℕ) :
    LinearMap.trace ℂ (OscillatorWeightSpace selectedOrigin d)
      (weightTheta selectedOrigin d) =
        PowerSeries.coeff ℂ d (oscillatorProduct 24) := by
  rw [weight_trace_product, selected_oscillator_rank]

theorem selected_vacuum_weight_trace :
    LinearMap.trace ℂ (OscillatorWeightSpace selectedOrigin 0)
      (weightTheta selectedOrigin 0) = 1 := by
  rw [selected_weight_trace, oscillatorProduct_constant]

def SelectedGradedPublication : Prop :=
  (∀ d, LinearMap.trace ℂ (OscillatorWeightSpace selectedOrigin d)
    (weightTheta selectedOrigin d) = PowerSeries.coeff ℂ d (oscillatorProduct 24)) ∧
  (∀ d (v : OscillatorWeightSpace selectedOrigin d),
    (weightTheta selectedOrigin d v : Fock selectedOrigin) =
      fockTheta selectedOrigin (v : Fock selectedOrigin))

open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

theorem shared_action_electron_fields_and_graded_trace
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧
      AlgebraicVertexInput ∧ SelectedHeisenbergPublication ∧ SelectedGradedPublication := by
  obtain ⟨hp, ha, hf⟩ := shared_action_electron_heisenberg_fields hU hunit x y r η
  exact ⟨hp, ha, hf, selected_weight_trace, weightTheta_is_restriction selectedOrigin⟩

end HMT.I.SelectedGradedTrace
end

#print axioms HMT.I.SelectedGradedTrace.weightTheta_is_restriction
#print axioms HMT.I.SelectedGradedTrace.weight_trace_product
#print axioms HMT.I.SelectedGradedTrace.selected_weight_trace
#print axioms HMT.I.SelectedGradedTrace.selected_vacuum_weight_trace
#print axioms HMT.I.SelectedGradedTrace.shared_action_electron_fields_and_graded_trace
