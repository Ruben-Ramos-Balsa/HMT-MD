import SelectedActionDomain
import ElectronicAPPClosure
import ElectronOrientationBridge

/-!
# Electronic publication from the selected regional register

The selected register and its action-domain bounds feed the existing electronic
composition and central mass operator. No incidence ledger is reconstructed
from terminal digits, and no `PublishedRegister` hypothesis is introduced.
The electronic torsion is the full regional reader, not the logarithmic vacancy
coordinate used by the analytic alpha chart. The positive action unit, positive
mass unit, reader label, and internal-moment refinement retain their types.

The upstream construction generates W24, the regional panel, and N69; unordered
S8 remains the explicit input interface of the terminal selector. This module
does not select S8 or identify a dimensional unit with an experimental target.
-/

noncomputable section

namespace HMT.I.SelectedElectron

open HMT.I.TerminalSelector HMT.I.SelectedAction
open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMT.VI.ElectronMassRealization
open HMTMassCharacter

def composition (U : ℝ) : ℝ :=
  ElectronComposition.regionalComposition regionalRegister (actionRatio U)

/-- The action and the electron use the very same selected alpha coordinate. -/
theorem composition_correct_reader (U : ℝ) :
    composition U = ElectronComposition.composition pi phi alpha
      ElectronComposition.regionalFull (actionRatio U) := rfl

/-- Reuse the global APP norm and the full electronic torsion, without replacing
either reader by a numerical target or repeating the upstream norm proof. -/
theorem composition_formula_from_APP (U : ℝ) :
    composition U = ‖HMT.I.APPGlobalPrefactor.incompatibility‖ *
      (Real.exp (phi / pi ^ 2) - 22 * alpha ^ 3) *
      (1 + 15 * ElectronComposition.regionalFull) *
      Real.exp ((80 - 54 * alpha + 6 * ElectronComposition.regionalFull) *
        Real.log (actionRatio U)) := by
  rw [composition_correct_reader, ElectronComposition.composition_formula,
    HMT.I.APPGlobalPrefactor.incompatibility_norm]

/-- The orientation bridge feeds the same formula, rather than being a
disconnected identity about two arbitrary real numbers. -/
theorem composition_formula_from_regional_character (U : ℝ) :
    composition U = ‖HMT.I.APPGlobalPrefactor.incompatibility‖ *
      (ElectronOrientationBridge.electronicCharacter - 22 * alpha ^ 3) *
      (1 + 15 * ElectronComposition.regionalFull) *
      Real.exp ((80 - 54 * alpha + 6 * ElectronComposition.regionalFull) *
        Real.log (actionRatio U)) := by
  rw [ElectronOrientationBridge.electronic_character_recognition]
  exact composition_formula_from_APP U

theorem composition_positive (U : ℝ) : 0 < composition U := by
  apply ElectronComposition.regional_composition_positive
  · exact action_domain.alpha_pos
  · change alpha < 1 / 100
    linarith [action_domain.alpha_coarse_upper]

theorem composition_unit_independent {U V : ℝ} (hU : 0 < U) (hV : 0 < V) :
    composition U = composition V := by
  have hRatio := HMT.I.SelectedAction.action_ratio_base_independent hU hV
  unfold composition
  rw [hRatio]

def referenceMass (massUnit : ℝ) : ℝ :=
  regionalElectronReferenceMass massUnit regionalRegister

theorem reference_mass_positive {massUnit : ℝ} (hunit : 0 < massUnit) :
    0 < referenceMass massUnit := by
  apply regional_electron_reference_mass_positive hunit
  · exact action_domain.alpha_pos
  · change alpha < 1 / 100
    linarith [action_domain.alpha_coarse_upper]

def massOperator (U massUnit x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) : End CentralRoute :=
  regionalElectronMassOperator (actionRatio U) massUnit x y regionalRegister r η

theorem mass_operator_positive (U : ℝ) {massUnit : ℝ} (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    (massOperator U massUnit x y r η).IsPositive := by
  apply regional_electron_mass_operator_positive _ hunit
  · exact action_domain.alpha_pos
  · change alpha < 1 / 100
    linarith [action_domain.alpha_coarse_upper]

/-- The generated central electronic route is an eigenvector with precisely
the regional scalar coefficient; the dimensional mass unit occurs once. -/
theorem mass_operator_basis {U : ℝ} (hU : 0 < U)
    (massUnit x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    massOperator U massUnit x y r η (routeBasis CentralRoute.electron) =
      (massUnit * composition U : ℝ) • routeBasis CentralRoute.electron := by
  exact regional_electron_mass_operator_basis
    (lt_trans zero_lt_one (action_ratio_gt_one hU))
    massUnit x y regionalRegister r η

theorem mass_operator_basis_from_APP {U : ℝ} (hU : 0 < U)
    (massUnit x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    massOperator U massUnit x y r η (routeBasis CentralRoute.electron) =
      (massUnit * (‖HMT.I.APPGlobalPrefactor.incompatibility‖ *
        (Real.exp (phi / pi ^ 2) - 22 * alpha ^ 3) *
        (1 + 15 * ElectronComposition.regionalFull) *
        Real.exp ((80 - 54 * alpha + 6 * ElectronComposition.regionalFull) *
          Real.log (actionRatio U))) : ℝ) • routeBasis CentralRoute.electron := by
  rw [mass_operator_basis hU, composition_formula_from_APP]

theorem electronic_publication {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    0 < referenceMass massUnit ∧
      1 < actionRatio U ∧
      0 < composition U ∧
      (massOperator U massUnit x y r η).IsPositive ∧
      massOperator U massUnit x y r η (routeBasis CentralRoute.electron) =
        (massUnit * composition U : ℝ) • routeBasis CentralRoute.electron :=
  ⟨reference_mass_positive hunit, action_ratio_gt_one hU, composition_positive U,
    mass_operator_positive U hunit x y r η, mass_operator_basis hU massUnit x y r η⟩

end HMT.I.SelectedElectron
end

#print axioms HMT.I.SelectedElectron.composition_correct_reader
#print axioms HMT.I.SelectedElectron.composition_formula_from_APP
#print axioms HMT.I.SelectedElectron.composition_formula_from_regional_character
#print axioms HMT.I.SelectedElectron.composition_positive
#print axioms HMT.I.SelectedElectron.composition_unit_independent
#print axioms HMT.I.SelectedElectron.reference_mass_positive
#print axioms HMT.I.SelectedElectron.mass_operator_positive
#print axioms HMT.I.SelectedElectron.mass_operator_basis
#print axioms HMT.I.SelectedElectron.mass_operator_basis_from_APP
#print axioms HMT.I.SelectedElectron.electronic_publication
