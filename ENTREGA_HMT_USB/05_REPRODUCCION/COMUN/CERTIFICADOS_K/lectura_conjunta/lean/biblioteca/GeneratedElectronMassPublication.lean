import GeneratedActionDomain
import ElectronMassRealization

/-!
# Generated Article I--II--VI electronic mass publication

This terminal module composes, without introducing a metrological target,
the exact incidence-register readers of Article I, the generated action
sections of Article II, and the generated central electronic ledger and mass
operator of Article VI.

The ledger hypothesis remains the exact `PublishedRegister` proposition.  The
positive dimensional unit and the refinement of the internal moments remain
explicit.  Neither is promoted to a producer of the HMT coordinates.
-/

noncomputable section

namespace HMT.VI.GeneratedElectronMassPublication

open HMT.IncidenceRegister
open HMT.II.ActionReturn
open HMT.II.GeneratedAction
open HMT.VI.MassOperator
open HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature
open HMT.VI.ElectronMassRealization
open HMTMassCharacter
open AlphaIncidencePublications

/-- The action ratio is read from the two sections generated from the same
positive basis coordinate. -/
def actionRatio (l : Ledger) (U : ℝ) : ℝ :=
  hbarPre (alpha l) phi U / hbarRet (alpha l) phi pi U

/-- The electronic reference coordinate after instantiating all four
dimensionless readers with generated HMT outputs. -/
def generatedElectronReferenceMass
    (l : Ledger) (massUnit : ℝ) : ℝ :=
  electronReferenceMass massUnit pi phi (alpha l)
    VacancyDeltaBounds.vacancyDelta

/-- The scalar published on the central electronic fibre. -/
def generatedElectronComposition (l : Ledger) (U : ℝ) : ℝ :=
  ElectronComposition.composition pi phi (alpha l)
    VacancyDeltaBounds.vacancyDelta (actionRatio l U)

/-- The Article VI operator with Article I coordinates, the generated
vacancy coordinate, and the Article II return ratio. -/
def generatedElectronMassOperator
    (l : Ledger) (U massUnit x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) : End CentralRoute :=
  electronMassOperator (actionRatio l U) massUnit pi phi (alpha l)
    VacancyDeltaBounds.vacancyDelta x y r η

theorem vacancy_delta_nonnegative :
    0 ≤ VacancyDeltaBounds.vacancyDelta := by
  have h := VacancyDeltaBounds.vacancyDelta_enclosure.1
  have hLower : 0 < AlphaStateLinkBound.deltaLower := by
    norm_num [AlphaStateLinkBound.deltaLower]
  exact le_of_lt (hLower.trans h)

theorem action_ratio_gt_one
    (l : Ledger) (hl : PublishedRegister l) {U : ℝ} (hU : 0 < U) :
    1 < actionRatio l U := by
  simpa [actionRatio] using
    (generated_action_sections l hl U hU).2.2

theorem action_ratio_positive
    (l : Ledger) (hl : PublishedRegister l) {U : ℝ} (hU : 0 < U) :
    0 < actionRatio l U :=
  lt_trans zero_lt_one (action_ratio_gt_one l hl hU)

theorem action_ratio_base_independent
    (l : Ledger) {U V : ℝ} (hU : 0 < U) (hV : 0 < V) :
    actionRatio l U = actionRatio l V := by
  simpa [actionRatio] using generated_action_base_independent l U V hU hV

theorem generated_electron_reference_mass_positive
    (l : Ledger) (hl : PublishedRegister l)
    {massUnit : ℝ} (hmassUnit : 0 < massUnit) :
    0 < generatedElectronReferenceMass l massUnit := by
  have hDomain := generated_action_domain l hl
  have hAlphaUpper : alpha l < (1 : ℝ) / 100 := by
    linarith [hDomain.alpha_coarse_upper]
  unfold generatedElectronReferenceMass
  exact electron_reference_mass_positive hmassUnit hDomain.pi_pos
    hDomain.phi_pos hDomain.alpha_pos hAlphaUpper vacancy_delta_nonnegative

theorem generated_electron_composition_positive
    (l : Ledger) (hl : PublishedRegister l)
    (U : ℝ) :
    0 < generatedElectronComposition l U := by
  have hDomain := generated_action_domain l hl
  have hAlphaUpper : alpha l < (1 : ℝ) / 100 := by
    linarith [hDomain.alpha_coarse_upper]
  unfold generatedElectronComposition
  exact ElectronComposition.composition_positive pi phi (alpha l)
    VacancyDeltaBounds.vacancyDelta (actionRatio l U)
    hDomain.pi_pos hDomain.phi_pos hDomain.alpha_pos hAlphaUpper
    vacancy_delta_nonnegative

theorem generated_electron_composition_base_independent
    (l : Ledger) {U V : ℝ} (hU : 0 < U) (hV : 0 < V) :
    generatedElectronComposition l U = generatedElectronComposition l V := by
  unfold generatedElectronComposition
  rw [action_ratio_base_independent l hU hV]

theorem generated_electron_mass_operator_positive
    (l : Ledger) (hl : PublishedRegister l)
    (U : ℝ) {massUnit : ℝ} (hmassUnit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    (generatedElectronMassOperator l U massUnit x y r η).IsPositive := by
  have hDomain := generated_action_domain l hl
  have hAlphaUpper : alpha l < (1 : ℝ) / 100 := by
    linarith [hDomain.alpha_coarse_upper]
  unfold generatedElectronMassOperator
  exact electron_mass_operator_positive (actionRatio l U) hmassUnit
    hDomain.pi_pos hDomain.phi_pos hDomain.alpha_pos hAlphaUpper
    vacancy_delta_nonnegative x y r η

/-- Exact generated publication on the central electronic basis. -/
theorem generated_electron_mass_operator_basis
    (l : Ledger) (hl : PublishedRegister l)
    {U : ℝ} (hU : 0 < U) (massUnit x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) :
    generatedElectronMassOperator l U massUnit x y r η
        (routeBasis CentralRoute.electron) =
      (massUnit * generatedElectronComposition l U : ℝ) •
        routeBasis CentralRoute.electron := by
  unfold generatedElectronMassOperator generatedElectronComposition
  exact electron_mass_operator_basis (action_ratio_positive l hl hU)
    massUnit pi phi (alpha l) VacancyDeltaBounds.vacancyDelta x y r η

/-- Fully expanded terminal coefficient, with every generated factor visible
and the dimensional unit carried exactly once. -/
theorem generated_electron_mass_operator_basis_expanded
    (l : Ledger) (hl : PublishedRegister l)
    {U : ℝ} (hU : 0 < U) (massUnit x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) :
    generatedElectronMassOperator l U massUnit x y r η
        (routeBasis CentralRoute.electron) =
      (massUnit * (Real.sqrt 3 / 4 *
        (Real.exp (phi / pi ^ 2) - 22 * (alpha l) ^ 3) *
        (1 + 15 * VacancyDeltaBounds.vacancyDelta) *
        Real.exp ((80 - 54 * alpha l +
          6 * VacancyDeltaBounds.vacancyDelta) *
          Real.log (actionRatio l U))) : ℝ) •
        routeBasis CentralRoute.electron := by
  unfold generatedElectronMassOperator
  exact electron_mass_operator_basis_expanded
    (action_ratio_positive l hl hU)
    massUnit pi phi (alpha l) VacancyDeltaBounds.vacancyDelta x y r η

/-- Terminal conjunction: the generated reference is positive, the return
ratio is nontrivial, the operator is positive, and its central action is the
exact generated scalar publication. -/
theorem generated_electron_mass_publication
    (l : Ledger) (hl : PublishedRegister l)
    {U massUnit : ℝ} (hU : 0 < U) (hmassUnit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    0 < generatedElectronReferenceMass l massUnit ∧
      1 < actionRatio l U ∧
      (generatedElectronMassOperator l U massUnit x y r η).IsPositive ∧
      generatedElectronMassOperator l U massUnit x y r η
          (routeBasis CentralRoute.electron) =
        (massUnit * generatedElectronComposition l U : ℝ) •
          routeBasis CentralRoute.electron := by
  exact ⟨generated_electron_reference_mass_positive l hl hmassUnit,
    action_ratio_gt_one l hl hU,
    generated_electron_mass_operator_positive l hl U hmassUnit x y r η,
    generated_electron_mass_operator_basis l hl hU massUnit x y r η⟩

#print axioms vacancy_delta_nonnegative
#print axioms action_ratio_gt_one
#print axioms action_ratio_positive
#print axioms action_ratio_base_independent
#print axioms generated_electron_reference_mass_positive
#print axioms generated_electron_composition_positive
#print axioms generated_electron_composition_base_independent
#print axioms generated_electron_mass_operator_positive
#print axioms generated_electron_mass_operator_basis
#print axioms generated_electron_mass_operator_basis_expanded
#print axioms generated_electron_mass_publication

end HMT.VI.GeneratedElectronMassPublication
