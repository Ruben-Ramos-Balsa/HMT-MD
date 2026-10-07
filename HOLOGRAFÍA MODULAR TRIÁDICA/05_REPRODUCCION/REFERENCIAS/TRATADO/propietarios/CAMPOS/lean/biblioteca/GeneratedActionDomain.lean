import AlphaIncidencePublications
import ActionSections

/-!
The action-domain inequalities are discharged from the already constructed
regional readers and the incidence-register reading. No numerical intervals
for the action inputs are additional assumptions in the terminal theorem.
The identification of the upstream ledger with the published terminal
register is retained exactly as in the imported I-composition; it is not
replaced by a target-defined ledger.
-/

noncomputable section
namespace HMT.II.GeneratedAction

open HMT.IncidenceRegister HMT.II.ActionReturn
open AlphaIncidencePublications

def alpha (l : Ledger) : ℝ := AlphaAnalyticChart.precoordinate (register l)
def phi : ℝ := AlphaCarryLimit.autoscaleValue
def pi : ℝ := ClosureAnalytic.value

/-- All five interval requirements are conclusions of the inherited readers. -/
theorem generated_action_domain (l : Ledger) (hl : PublishedRegister l) :
    PrintedDomain (alpha l) phi pi := by
  have hf := AlphaSourceBounds.autoscale_enclosure
  have hp := AlphaSourceBounds.closure_enclosure
  have ha := AlphaTightBounds.precoordinate_tight_enclosure (register l) hl
  norm_num [AlphaStateLinkBound.aLower, AlphaStateLinkBound.aUpper] at ha
  dsimp [alpha, phi, pi]
  constructor <;> linarith

/-- The analytic publication uses exactly the same input domain, rather than
receiving a second externally assigned value of alpha. -/
theorem analytic_publication_action_domain (l : Ledger) (hl : PublishedRegister l)
    (x : ℝ) (hx : x ∈ Set.Ioo 0 AlphaAnalyticChart.radius)
    (hroot : AlphaAnalyticChart.stateChart (register l)
      VacancyDeltaBounds.vacancyDelta x = 0) :
    x = alpha l ∧ PrintedDomain x phi pi := by
  have ha := AlphaSourceBounds.precoordinate_bounds (register l) hl
  have hd := VacancyDeltaBounds.vacancyDelta_enclosure
  have hlink := AlphaTightBounds.stateLink_bound_of_vacancy_enclosure
    (register l) hl _ hd.1 hd.2
  have he : x = alpha l :=
    (AlphaAnalyticChart.state_chart_root_iff (register l) _ x ha.1 ha.2 hlink hx).mp hroot
  exact ⟨he, he.symm ▸ generated_action_domain l hl⟩

theorem generated_action_decimal_order (l : Ledger) (hl : PublishedRegister l) :
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi (alpha l)) = -34 :=
  HMT.II.DeterminantalAction.actionScale_decimalOrder
    (generated_action_domain l hl).readerIntervals

theorem generated_action_decade (l : Ledger) (hl : PublishedRegister l) :
    actionDecade = (10 : ℝ) ^ HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi (alpha l)) :=
  (generated_action_domain l hl).actionDecade_eq_decimalOrder

/-- The action sections and their return ratio are consequences of the
generated coordinates, with only the positive choice of unit left explicit. -/
theorem generated_action_sections (l : Ledger) (hl : PublishedRegister l)
    (U : ℝ) (hU : 0 < U) :
    0 < hbarRet (alpha l) phi pi U ∧
      hbarRet (alpha l) phi pi U < hbarPre (alpha l) phi U ∧
      1 < hbarPre (alpha l) phi U / hbarRet (alpha l) phi pi U := by
  have h := generated_action_domain l hl
  refine ⟨h.hbarRet_pos hU, ?_, h.section_ratio_gt_one hU⟩
  exact mul_lt_mul_of_pos_right
    (mul_lt_mul_of_pos_right h.etaRet_lt_H5 actionDecade_pos) hU

theorem generated_action_base_independent (l : Ledger) (U V : ℝ)
    (hU : 0 < U) (hV : 0 < V) :
    hbarPre (alpha l) phi U / hbarRet (alpha l) phi pi U =
      hbarPre (alpha l) phi V / hbarRet (alpha l) phi pi V :=
  section_ratio_base_independent _ _ _ hU hV

#print axioms generated_action_domain
#print axioms analytic_publication_action_domain
#print axioms generated_action_decimal_order
#print axioms generated_action_decade
#print axioms generated_action_sections
#print axioms generated_action_base_independent

end HMT.II.GeneratedAction
