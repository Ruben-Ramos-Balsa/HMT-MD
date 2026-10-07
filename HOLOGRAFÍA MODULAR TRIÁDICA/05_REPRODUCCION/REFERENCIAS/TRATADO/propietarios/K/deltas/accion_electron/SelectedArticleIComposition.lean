import SelectedElectronPublication

/-! The same selected alpha coordinate is published at every depth and then
used by the action sections and the electronic mass operator. This theorem
does not introduce a second alpha coordinate or an incidence-ledger premise.
It preserves the source selector and dimensional interfaces of the imports. -/
noncomputable section
namespace HMT.I.SelectedArticleI

open HMT.I.TerminalSelector HMT.I.SelectedAction HMT.I.SelectedElectron
open HMT.II.ActionReturn HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

def PublishedAtEveryDepth (a : ℝ) : Prop :=
  ∀ n : Nat, (AlphaPublications.publication regionalRegister n).outgoing = 0 ∧
    (AlphaPublications.publication regionalRegister n).digits =
      (AlphaCanonicalSection.digits a (12*n)).map Int.ofNat

theorem alpha_published_at_every_depth : PublishedAtEveryDepth alpha := by
  obtain ⟨a, ha, _⟩ := regional_terminal_alpha
  have heq := alpha_is_same_analytic_root a ha.1 ha.2.1
  simpa only [heq] using ha.2.2

/-- One selected coordinate feeds the all-depth publication, the deterministic
action decade, both sections, and the positive central electronic operator. -/
theorem principal_action_electron_composition
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    PublishedAtEveryDepth alpha ∧
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    (0 < hbarRet alpha phi pi U ∧
      hbarRet alpha phi pi U < hbarPre alpha phi U ∧ 1 < actionRatio U) ∧
    (0 < composition U ∧
      (massOperator U massUnit x y r η).IsPositive ∧
      massOperator U massUnit x y r η (routeBasis CentralRoute.electron) =
        (massUnit * composition U : ℝ) • routeBasis CentralRoute.electron) :=
  ⟨alpha_published_at_every_depth, action_decimal_order, action_sections U hU,
    composition_positive U, mass_operator_positive U hunit x y r η,
    mass_operator_basis hU massUnit x y r η⟩

end HMT.I.SelectedArticleI
end

#print axioms HMT.I.SelectedArticleI.alpha_published_at_every_depth
#print axioms HMT.I.SelectedArticleI.principal_action_electron_composition
