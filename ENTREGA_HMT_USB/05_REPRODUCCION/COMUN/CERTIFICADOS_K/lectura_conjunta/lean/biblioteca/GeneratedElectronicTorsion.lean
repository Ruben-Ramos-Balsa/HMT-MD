import GeneratedActionDomain
import ElectronMassRealization
import GeneratedElectronMassPublication
import ElectronTorsionSeparation

/-!
# The electronic torsion in the generated mass publication

This corrects a binding, not the previously proved algebraic family.  The
electronic reader is `ElectronComposition.regionalFull`; the logarithmic
vacancy reader remains in the analytic alpha chart.  Both basal and return
factors use the same electronic torsion, as in Article I, electron.tex,
definition `eq:el-delta` and equations `eq:el-selector-enteros` onward.

The concrete terminal-register proposition is kept explicit.  This file does
not manufacture its prospective incidence ledger from the published digits.
-/

noncomputable section

namespace HMT.I.GeneratedElectronicTorsion

open HMT.IncidenceRegister HMT.II.ActionReturn HMT.II.GeneratedAction
open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMT.VI.ElectronMassRealization
open HMTMassCharacter AlphaIncidencePublications

def electronicTorsion : ℝ := ElectronComposition.regionalFull

theorem electronic_torsion_formula :
    electronicTorsion =
      (pi - PropagationLimit.value * Real.log pi) / 270 * (1 + pi / 729) := rfl

theorem electronic_torsion_positive : 0 < electronicTorsion :=
  ElectronComposition.regional_full_pos

def actionRatio (l : Ledger) (U : ℝ) : ℝ :=
  hbarPre (alpha l) phi U / hbarRet (alpha l) phi pi U

theorem action_ratio_gt_one (l : Ledger) (hl : PublishedRegister l)
    {U : ℝ} (hU : 0 < U) : 1 < actionRatio l U :=
  (generated_action_sections l hl U hU).2.2

def electronicComposition (l : Ledger) (U : ℝ) : ℝ :=
  ElectronComposition.regionalComposition (register l) (actionRatio l U)

def referenceMass (l : Ledger) (massUnit : ℝ) : ℝ :=
  regionalElectronReferenceMass massUnit (register l)

def massOperator (l : Ledger) (U massUnit x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) : End CentralRoute :=
  regionalElectronMassOperator (actionRatio l U) massUnit x y (register l) r η

theorem electronic_composition_correct_reader (l : Ledger) (U : ℝ) :
    electronicComposition l U =
      ElectronComposition.composition pi phi (alpha l) electronicTorsion
        (actionRatio l U) := rfl

theorem electronic_composition_formula (l : Ledger) (U : ℝ) :
    electronicComposition l U = Real.sqrt 3 / 4 *
      (Real.exp (phi / pi ^ 2) - 22 * (alpha l) ^ 3) *
      (1 + 15 * ((pi - PropagationLimit.value * Real.log pi) / 270 *
        (1 + pi / 729))) *
      Real.exp ((80 - 54 * alpha l +
        6 * ((pi - PropagationLimit.value * Real.log pi) / 270 *
          (1 + pi / 729))) * Real.log (actionRatio l U)) := by
  rw [electronic_composition_correct_reader, ElectronComposition.composition_formula,
    electronic_torsion_formula]

theorem electronic_composition_positive (l : Ledger) (hl : PublishedRegister l)
    (U : ℝ) : 0 < electronicComposition l U := by
  have h := generated_action_domain l hl
  apply ElectronComposition.regional_composition_positive
  · exact h.alpha_pos
  · change alpha l < 1 / 100
    linarith [h.alpha_coarse_upper]

theorem electronic_composition_unit_independent (l : Ledger)
    {U V : ℝ} (hU : 0 < U) (hV : 0 < V) :
    electronicComposition l U = electronicComposition l V := by
  unfold electronicComposition actionRatio
  rw [generated_action_base_independent l U V hU hV]

theorem electronic_mass_positive (l : Ledger) (hl : PublishedRegister l)
    (U : ℝ) {massUnit : ℝ} (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    (massOperator l U massUnit x y r η).IsPositive := by
  have h := generated_action_domain l hl
  apply regional_electron_mass_operator_positive _ hunit
  · exact h.alpha_pos
  · change alpha l < 1 / 100
    linarith [h.alpha_coarse_upper]

theorem electronic_mass_basis (l : Ledger) (hl : PublishedRegister l)
    {U : ℝ} (hU : 0 < U) (massUnit x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) :
    massOperator l U massUnit x y r η (routeBasis CentralRoute.electron) =
      (massUnit * electronicComposition l U : ℝ) •
        routeBasis CentralRoute.electron := by
  exact regional_electron_mass_operator_basis
    (lt_trans zero_lt_one (action_ratio_gt_one l hl hU)) massUnit x y (register l) r η

/-- Exact specialization of the strict normalization theorem to the generated
action ratio. Omitting the factor `1 + pi/729` changes the result. -/
theorem reduced_torsion_changes_electronic_result
    (l : Ledger) (hl : PublishedRegister l) {U : ℝ} (hU : 0 < U) :
    ElectronComposition.composition pi phi (alpha l)
        ElectronComposition.regionalReduced (actionRatio l U) <
      electronicComposition l U := by
  have h := generated_action_domain l hl
  exact ElectronComposition.regional_normalization_strict (alpha l)
    (actionRatio l U) h.alpha_pos (by linarith [h.alpha_coarse_upper])
    (action_ratio_gt_one l hl hU)

/-- Regression guard for the previous terminal binding: substituting the
alpha vacancy reader changes the electronic scalar. -/
theorem vacancy_substitution_changes_electronic_result
    (l : Ledger) (hl : PublishedRegister l) {U : ℝ} (hU : 0 < U) :
    electronicComposition l U <
      HMT.VI.GeneratedElectronMassPublication.generatedElectronComposition l U := by
  have h := generated_action_domain l hl
  apply ElectronComposition.composition_normalization_strict
  · exact h.pi_pos
  · exact h.phi_pos
  · exact h.alpha_pos
  · change alpha l < 1 / 100
    linarith [h.alpha_coarse_upper]
  · exact ElectronComposition.regional_full_pos.le
  · exact ElectronTorsionSeparation.regional_torsion_lt_vacancy
  · exact action_ratio_gt_one l hl hU

/-- One alpha coordinate serves the arbitrarily deep compatible publications
and the electronic formula. The alpha chart keeps its own vacancy reader. -/
theorem alpha_publications_and_electronic_reader
    (l : Ledger) (hl : PublishedRegister l) (U : ℝ) :
    (∀ n m : ℕ,
      ((AlphaPublications.publication (register l) (n+m)).digits).take (12*n) =
        (AlphaPublications.publication (register l) n).digits) ∧
    electronicComposition l U =
      ElectronComposition.composition pi phi (alpha l) electronicTorsion (actionRatio l U) ∧
    0 < electronicComposition l U :=
  ⟨compatible_publications_from_vacancy_readout l hl,
    electronic_composition_correct_reader l U, electronic_composition_positive l hl U⟩

#print axioms electronic_torsion_formula
#print axioms electronic_torsion_positive
#print axioms action_ratio_gt_one
#print axioms electronic_composition_correct_reader
#print axioms electronic_composition_formula
#print axioms electronic_composition_positive
#print axioms electronic_composition_unit_independent
#print axioms electronic_mass_positive
#print axioms electronic_mass_basis
#print axioms reduced_torsion_changes_electronic_result
#print axioms vacancy_substitution_changes_electronic_result
#print axioms alpha_publications_and_electronic_reader

end HMT.I.GeneratedElectronicTorsion
