import ActionReturn
import ActionDecade

/-!
# Common-base action sections

This module uses a positive real coordinate `U` for the positive basis of the
oriented action line.  The decade is linked to the actual quotient norm and its
proved decimal order through the imported determinant block,
not a second dimensional factor inserted into a mass expressed in MeV.
The determinant and upstream extraction are intentionally separate modules.
-/

noncomputable section

namespace HMT.II.ActionReturn

def actionDecade : ℝ := 1 / 10 ^ 34

theorem actionDecade_pos : 0 < actionDecade := by unfold actionDecade; positivity

/-- The same printed intervals feed both determinant scale and regional return. -/
def PrintedDomain.readerIntervals {α φ p : ℝ} (h : PrintedDomain α φ p) :
    HMT.II.DeterminantalAction.ReaderIntervals φ α :=
  ⟨h.phi_lower, h.phi_upper, h.alpha_lower, h.alpha_upper⟩

/-- The section decade is the decimal order of the actual local-quotient norm. -/
theorem PrintedDomain.actionDecade_eq_decimalOrder {α φ p : ℝ}
    (h : PrintedDomain α φ p) :
    actionDecade = (10 : ℝ) ^ HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale φ α) := by
  rw [HMT.II.DeterminantalAction.actionScale_decimalOrder h.readerIntervals]
  norm_num [actionDecade]

def hbarPre (α φ U : ℝ) : ℝ := H5 α φ * actionDecade * U

def hbarRet (α φ p U : ℝ) : ℝ := etaRet α φ p * actionDecade * U

def deltaRet (α φ p : ℝ) : ℝ := H5 α φ - etaRet α φ p

theorem deltaRet_eq_correction (α φ p : ℝ) :
    deltaRet α φ p = returnCorrection α p := by
  unfold deltaRet etaRet
  ring

/-- Both section coordinates change contravariantly with the same positive basis factor. -/
theorem common_base_ratio (a b k : ℝ) (hk : 0 < k) :
    (a / k) / (b / k) = a / b := by
  exact div_div_div_cancel_right₀ (ne_of_gt hk) a b

namespace PrintedDomain

variable {α φ p : ℝ} (h : PrintedDomain α φ p)
include h

theorem hbarPre_pos {U : ℝ} (hU : 0 < U) : 0 < hbarPre α φ U :=
  mul_pos (mul_pos h.H5_pos actionDecade_pos) hU

theorem hbarRet_pos {U : ℝ} (hU : 0 < U) : 0 < hbarRet α φ p U :=
  mul_pos (mul_pos h.etaRet_pos actionDecade_pos) hU

end PrintedDomain

theorem section_ratio_eq (α φ p : ℝ) {U : ℝ} (hU : 0 < U) :
    hbarPre α φ U / hbarRet α φ p U = Ract α φ p := by
  unfold hbarPre hbarRet Ract
  rw [mul_div_mul_right _ _ (ne_of_gt hU),
    mul_div_mul_right _ _ (ne_of_gt actionDecade_pos)]

theorem PrintedDomain.section_ratio_gt_one {α φ p U : ℝ}
    (h : PrintedDomain α φ p) (hU : 0 < U) :
    1 < hbarPre α φ U / hbarRet α φ p U := by
  rw [section_ratio_eq _ _ _ hU]
  exact h.Ract_gt_one

theorem section_ratio_base_independent (α φ p : ℝ) {U V : ℝ}
    (hU : 0 < U) (hV : 0 < V) :
    hbarPre α φ U / hbarRet α φ p U = hbarPre α φ V / hbarRet α φ p V := by
  rw [section_ratio_eq _ _ _ hU, section_ratio_eq _ _ _ hV]

theorem section_coordinate_base_change (α φ p U : ℝ) {k : ℝ} (hk : 0 < k) :
    (hbarPre α φ U / k) / (hbarRet α φ p U / k) =
      hbarPre α φ U / hbarRet α φ p U := common_base_ratio _ _ _ hk

/-- One full turn is the declared angular-to-full-turn reading, in each section. -/
def fullTurn (p angularSection : ℝ) : ℝ := 2 * p * angularSection

theorem fullTurn_section_relation (α φ p U : ℝ) :
    fullTurn p (hbarPre α φ U) = 2 * p * hbarPre α φ U ∧
      fullTurn p (hbarRet α φ p U) = 2 * p * hbarRet α φ p U := ⟨rfl, rfl⟩

theorem fullTurn_ratio (p a b : ℝ) (hp : 0 < p) :
    fullTurn p a / fullTurn p b = a / b := by
  unfold fullTurn
  exact mul_div_mul_left _ _ (ne_of_gt (mul_pos (by norm_num) hp))

theorem PrintedDomain.fullTurn_ratio_eq {α φ p U : ℝ}
    (h : PrintedDomain α φ p) (hU : 0 < U) :
    fullTurn p (hbarPre α φ U) / fullTurn p (hbarRet α φ p U) = Ract α φ p := by
  rw [fullTurn_ratio _ _ _ h.pi_pos, section_ratio_eq _ _ _ hU]

#print axioms common_base_ratio
#print axioms PrintedDomain.readerIntervals
#print axioms PrintedDomain.actionDecade_eq_decimalOrder
#print axioms deltaRet_eq_correction
#print axioms section_ratio_eq
#print axioms PrintedDomain.section_ratio_gt_one
#print axioms section_ratio_base_independent
#print axioms fullTurn_section_relation
#print axioms PrintedDomain.fullTurn_ratio_eq

end HMT.II.ActionReturn
