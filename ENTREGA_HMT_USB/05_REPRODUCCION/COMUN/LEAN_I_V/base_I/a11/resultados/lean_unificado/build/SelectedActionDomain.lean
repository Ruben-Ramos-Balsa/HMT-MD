import SelectedFromRegionalInputs
import ActionSections

/-!
The action sections are evaluated on the output of the regional orbital
selector. No incidence ledger is reconstructed backwards from the answer and
no `PublishedRegister` hypothesis is introduced. The selector's explicit S8
interface and its computational trust boundary remain those of the imported
construction. The unit of action is a separate positive dimensional basis.
-/
noncomputable section
namespace HMT.I.SelectedAction

open HMT.II.ActionReturn HMT.I.TerminalSelector

def alpha : ℝ := AlphaAnalyticChart.precoordinate regionalRegister
def phi : ℝ := AlphaCarryLimit.autoscaleValue
def pi : ℝ := ClosureAnalytic.value

theorem selected_register_digits : regionalRegister.digits =
    [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601] := by
  rw [regionalRegister_eq_selected]
  exact TerminalSelector.selected_register_digits

/-- The input intervals of the action proof are derived, not assumed anew. -/
theorem action_domain : PrintedDomain alpha phi pi := by
  have hf := AlphaSourceBounds.autoscale_enclosure
  have hp := AlphaSourceBounds.closure_enclosure
  have ha := AlphaTightBounds.precoordinate_tight_enclosure
    regionalRegister selected_register_digits
  norm_num [AlphaStateLinkBound.aLower, AlphaStateLinkBound.aUpper] at ha
  dsimp [alpha, phi, pi]
  constructor <;> linarith

theorem alpha_eq_carry_value : alpha = AlphaCarryLimit.value regionalRegister := rfl

theorem alpha_is_same_analytic_root (x : ℝ)
    (hx : x ∈ Set.Ioo 0 AlphaAnalyticChart.radius)
    (hroot : AlphaAnalyticChart.stateChart regionalRegister
      VacancyDeltaBounds.vacancyDelta x = 0) : x = alpha := by
  have ha := AlphaSourceBounds.precoordinate_bounds regionalRegister selected_register_digits
  have hd := VacancyDeltaBounds.vacancyDelta_enclosure
  have hlink := AlphaTightBounds.stateLink_bound_of_vacancy_enclosure
    regionalRegister selected_register_digits _ hd.1 hd.2
  exact (AlphaAnalyticChart.state_chart_root_iff
    regionalRegister _ x ha.1 ha.2 hlink hx).mp hroot

theorem action_scale_formula :
    HMT.II.DeterminantalAction.actionScale phi alpha = phi * alpha ^ 16 :=
  HMT.II.DeterminantalAction.actionScale_eq phi alpha

theorem action_decimal_order :
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 :=
  HMT.II.DeterminantalAction.actionScale_decimalOrder action_domain.readerIntervals

theorem action_decade : actionDecade = (10 : ℝ) ^
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) :=
  action_domain.actionDecade_eq_decimalOrder

def actionRatio (U : ℝ) : ℝ := hbarPre alpha phi U / hbarRet alpha phi pi U

theorem action_sections (U : ℝ) (hU : 0 < U) :
    0 < hbarRet alpha phi pi U ∧
      hbarRet alpha phi pi U < hbarPre alpha phi U ∧ 1 < actionRatio U := by
  refine ⟨action_domain.hbarRet_pos hU, ?_, action_domain.section_ratio_gt_one hU⟩
  exact mul_lt_mul_of_pos_right
    (mul_lt_mul_of_pos_right action_domain.etaRet_lt_H5 actionDecade_pos) hU

theorem action_ratio_eq (U : ℝ) (hU : 0 < U) :
    actionRatio U = Ract alpha phi pi := section_ratio_eq _ _ _ hU

theorem action_ratio_gt_one {U : ℝ} (hU : 0 < U) : 1 < actionRatio U :=
  (action_sections U hU).2.2

theorem action_ratio_base_independent {U V : ℝ} (hU : 0 < U) (hV : 0 < V) :
    actionRatio U = actionRatio V := section_ratio_base_independent _ _ _ hU hV

theorem full_turn_ratio (U : ℝ) (hU : 0 < U) :
    fullTurn pi (hbarPre alpha phi U) / fullTurn pi (hbarRet alpha phi pi U) =
      actionRatio U := by
  rw [action_domain.fullTurn_ratio_eq hU, action_ratio_eq U hU]

/-- The complete regional renewal, not a finite numerical truncation. -/
theorem regional_return_formula :
    Cpi alpha pi = 169 * alpha ^ 6 +
      damping alpha pi * alpha ^ 7 / (1 - damping alpha pi * alpha) :=
  action_domain.Cpi_eq

theorem same_root_and_action_sections :
    (∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart regionalRegister VacancyDeltaBounds.vacancyDelta x = 0 ∧
      (∀ n : Nat, (AlphaPublications.publication regionalRegister n).outgoing = 0 ∧
        (AlphaPublications.publication regionalRegister n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat)) ∧
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    (∀ U : ℝ, 0 < U →
      0 < hbarRet alpha phi pi U ∧
      hbarRet alpha phi pi U < hbarPre alpha phi U ∧ 1 < actionRatio U) :=
  ⟨regional_terminal_alpha, action_decimal_order, action_sections⟩

end HMT.I.SelectedAction
end

#print axioms HMT.I.SelectedAction.action_domain
#print axioms HMT.I.SelectedAction.alpha_is_same_analytic_root
#print axioms HMT.I.SelectedAction.action_decimal_order
#print axioms HMT.I.SelectedAction.action_sections
#print axioms HMT.I.SelectedAction.regional_return_formula
#print axioms HMT.I.SelectedAction.same_root_and_action_sections
