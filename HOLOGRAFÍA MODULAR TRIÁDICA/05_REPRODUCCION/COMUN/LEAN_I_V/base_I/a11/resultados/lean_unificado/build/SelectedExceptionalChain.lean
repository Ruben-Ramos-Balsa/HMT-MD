import SelectedGeneratedFields
import ConcreteNativeFourPlusOne
import SelectedRadiusTDuality

/-!
Single entry for the conserved selected origin, its concrete Golay chart and
the generated reticular fields. The chart and binary code are constructed,
not supplied as hypotheses. The earlier action/electron parameters remain
explicit. Downstream radius/T transport is imported, never used to select K.
This composition does not assert an orbifold or the FLM theorem.
-/

noncomputable section
namespace HMT.I.SelectedExceptionalChain

open HMT.I.HexadOctadResidual HMT.I.HexadOctadFourPlusOne
open HMT.I.ConcreteBinaryGolay HMT.I.ConcreteWittChart
open HMT.I.ConcreteNativeFourPlusOne HMT.I.SelectedRegionalIncidence
open HMT.I.SelectedGeneratedFields
open HMT.I.SelectedVOAInput HMT.I.SelectedHeisenbergInput
open HMT.I.SelectedGradedTrace HMT.I.SelectedFullGradedTrace
open HMT.I.SelectedEnergyInput HMT.I.SelectedCovariantFields
open HMT.Shared.ArticleI

def ConcreteIncidencePublication : Prop :=
  (let T := selectedHighSupport.image positions;
    (hexadStar golay T).card = 4 ∧ (liftedStar golay T).card = 4 ∧
    (octadStar golay T).card = 5 ∧
    ∃ O : Support, golay.IsOctad O ∧ O ∩ golay.dodecad = T ∧
      O ∉ liftedStar golay T ∧
      octadStar golay T = insert O (liftedStar golay T)) ∧
  (∃! O : Support, golay.IsOctad O ∧
    O ∩ golay.dodecad = selectedNegativeSupport.image positions)

theorem concrete_incidence_publication : ConcreteIncidencePublication :=
  ⟨selected_register_four_plus_one, selected_negative_support_has_unique_octad⟩

theorem selected_incidence_and_generated_fields :
    ConcreteIncidencePublication ∧ SelectedGenerationPublication :=
  ⟨concrete_incidence_publication, selected_generation_publication⟩

open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

theorem shared_action_electron_exceptional_chain
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧
      AlgebraicVertexInput ∧ SelectedHeisenbergPublication ∧
      SelectedGradedPublication ∧ FullReflectedTracePublication ∧
      SelectedEnergyPublication ∧ SelectedChargedFieldPublication ∧
      SelectedCovariancePublication ∧ SelectedGenerationPublication ∧
      ConcreteIncidencePublication := by
  obtain ⟨ha,hb,hc,hd,he,hf,hg,hh,hi⟩ :=
    shared_action_electron_generated_fields hU hunit x y r η
  exact ⟨ha,hb,hc,hd,he,hf,hg,hh,hi,concrete_incidence_publication⟩

end HMT.I.SelectedExceptionalChain
end

#print axioms HMT.I.SelectedExceptionalChain.concrete_incidence_publication
#print axioms HMT.I.SelectedExceptionalChain.selected_incidence_and_generated_fields
#print axioms HMT.I.SelectedExceptionalChain.shared_action_electron_exceptional_chain
