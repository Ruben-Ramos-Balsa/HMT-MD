import SharedArticleIBase
import ActionElectricComposition

/-!
Article III on the regional register selected in Article I.

The action domain is an existing theorem about the selected regional register,
not a new hypothesis identifying an arbitrary incidence ledger with twelve
prescribed digits. Its angular chamber, constitutive response and electric
section are composed here using the existing Article II/III theorems.
The dimensional action basis remains an explicit positive unit coordinate.
No target charge, permittivity, permeability or speed selects the register.
-/

noncomputable section
namespace HMT.III.SelectedPublication

open HMT.I.SelectedAction HMT.II.ActionReturn
open HMT.III.Constitutive HMT.III.ElectricQuanta

def angles : AngularChamber := action_domain.producedAngles

def response : PositiveResponse := angles.channels.vacuum

def speed : ℝ := response.speed

def action (U : ℝ) : ℝ := ActionElectricComposition.retAction alpha phi pi U

theorem same_selected_register :
    alpha = AlphaAnalyticChart.precoordinate HMT.Shared.ArticleI.register := rfl

theorem angle_order : 0 < angles.y ∧ angles.y < angles.x :=
  ⟨angles.y_pos, angles.y_lt_x⟩

theorem speed_pos : 0 < speed := by
  exact one_div_pos.mpr (mul_pos response.plus_pos response.minus_pos)

theorem action_pos {U : ℝ} (hU : 0 < U) : 0 < action U :=
  ActionElectricComposition.retAction_pos action_domain hU

theorem positive_unique_operator :
    ∃! W : Matrix (Fin 2) (Fin 2) ℝ,
      (W * TwoSheetProjectors.sigma4
        (angles.transport canonicalSheetInvolution
          canonicalSheetInvolution_square ^ 30) =
      TwoSheetProjectors.sigma3
        (angles.transport canonicalSheetInvolution
          canonicalSheetInvolution_square ^ 30)) ∧ W.PosDef :=
  angles.canonical_positive_completion_exists_unique

theorem speed_at_every_refinement (m : ℕ) :
    angles.channels.refinedSpeed m = speed :=
  angles.channels.refinedSpeed_eq_constitutive m

theorem recover_generated_degrees :
    (180 / pi) * angles.channels.angularX = directDegrees alpha ∧
    (180 / pi) * angles.channels.angularY = conjugateDegrees alpha phi pi :=
  action_domain.degree_recovery

theorem constitutive_ellipse_recovery :
    (Real.log angles.recoveredPowerPlus - Real.log angles.recoveredPowerMinus) /
      (Real.log angles.recoveredPowerPlus + Real.log angles.recoveredPowerMinus) =
        angles.y / angles.x ∧
    Real.log (Real.log angles.recoveredPowerPlus /
      Real.log angles.recoveredPowerMinus) / 2 = angles.ellipseAnisotropy ∧
    Real.sqrt (Real.log angles.recoveredPowerMinus /
      Real.log angles.recoveredPowerPlus) = angles.relativeLC :=
  angles.constitutive_LC_recovery

theorem charge_exists_unique (U : ℝ) (hU : 0 < U) :
    ∃! e : ℝ, 0 < e ∧ response.impedance * e ^ 2 = 2 * alpha * action U :=
  ActionElectricComposition.generated_charge_exists_unique action_domain hU

theorem electric_cross_identities (U : ℝ) (hU : 0 < U) :
    resistance alpha (action U) response * conductance alpha (action U) response = 2 ∧
    conductance alpha (action U) response * response.impedance = 4 * alpha ∧
    josephson alpha (action U) response * flux alpha (action U) response = 1 ∧
    josephson alpha (action U) response ^ 2 * resistance alpha (action U) response =
      4 / action U :=
  ActionElectricComposition.generated_electric_identities action_domain hU

theorem electromagnetic_coupling (U : ℝ) (hU : 0 < U) :
    alpha = charge alpha (action U) response ^ 2 /
      (4 * pi * response.epsilon * hbarRet alpha phi pi U * speed) :=
  ActionElectricComposition.generated_coupling_identity action_domain hU

theorem action_return_detectable (U : ℝ) (hU : 0 < U) :
    1 < charge alpha (ActionElectricComposition.preAction alpha phi pi U) response /
      charge alpha (action U) response :=
  ActionElectricComposition.generated_action_return_is_detectable action_domain hU

/-- The selected I -> II -> III consumer.  All source, interval, angular and
positivity conditions, other than the dimensional unit, are inherited proofs. -/
theorem selected_action_constitutive_electric_chain (U : ℝ) (hU : 0 < U) :
    alpha = AlphaAnalyticChart.precoordinate HMT.Shared.ArticleI.register ∧
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    angles.canonicalConstitutiveOperator.PosDef ∧
    0 < speed ∧ 0 < action U ∧
    (∀ m : ℕ, angles.channels.refinedSpeed m = speed) ∧
    (∃! e : ℝ, 0 < e ∧ response.impedance * e ^ 2 = 2 * alpha * action U) ∧
    resistance alpha (action U) response * conductance alpha (action U) response = 2 ∧
    conductance alpha (action U) response * response.impedance = 4 * alpha ∧
    josephson alpha (action U) response * flux alpha (action U) response = 1 ∧
    josephson alpha (action U) response ^ 2 * resistance alpha (action U) response =
      4 / action U :=
  ⟨same_selected_register, action_decimal_order,
    angles.canonical_operator_posDef, speed_pos, action_pos hU,
    speed_at_every_refinement, charge_exists_unique U hU,
    electric_cross_identities U hU⟩

end HMT.III.SelectedPublication
end

#print axioms HMT.III.SelectedPublication.same_selected_register
#print axioms HMT.III.SelectedPublication.positive_unique_operator
#print axioms HMT.III.SelectedPublication.constitutive_ellipse_recovery
#print axioms HMT.III.SelectedPublication.electromagnetic_coupling
#print axioms HMT.III.SelectedPublication.action_return_detectable
#print axioms HMT.III.SelectedPublication.selected_action_constitutive_electric_chain
