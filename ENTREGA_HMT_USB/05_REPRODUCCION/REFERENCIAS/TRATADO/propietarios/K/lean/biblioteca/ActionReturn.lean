import RegionalRenewal
import H5Bounds

/-!
# Regional return from the printed intervals

No positivity of `H5`, `etaRet`, or `Ract - 1` is taken as a hypothesis.
The source's damping, selector, and degree-seven renewal are used literally.
-/

noncomputable section

namespace HMT.II.ActionReturn

def damping (α p : ℝ) : ℝ := Real.exp (-100 * p * α / 9)

theorem damping_pos (α p : ℝ) : 0 < damping α p := Real.exp_pos _

/-- The full renewal sum, with the declared order-six selector coefficient. -/
def Cpi (α p : ℝ) : ℝ := regionalValue (damping α p) α

def returnCorrection (α p : ℝ) : ℝ := (90 / p) * Cpi α p

def etaRet (α φ p : ℝ) : ℝ := H5 α φ - returnCorrection α p

def Ract (α φ p : ℝ) : ℝ := H5 α φ / etaRet α φ p

namespace PrintedDomain

variable {α φ p : ℝ} (h : PrintedDomain α φ p)
include h

theorem damping_lt_one : damping α p < 1 := by
  apply Real.exp_lt_one_iff.mpr
  have := mul_pos h.pi_pos h.alpha_pos
  nlinarith

theorem damping_product_pos : 0 < damping α p * α := mul_pos (damping_pos α p) h.alpha_pos

theorem damping_product_lt_alpha : damping α p * α < α := by
  nlinarith [h.damping_lt_one, h.alpha_pos]

theorem renewal_domain : |damping α p * α| < 1 := by
  rw [abs_of_pos h.damping_product_pos]
  exact h.damping_product_lt_alpha.trans h.alpha_lt_one

theorem renewal_denominator_pos : 0 < 1 - damping α p * α := by
  have := (abs_lt.mp h.renewal_domain).2
  linarith

theorem Cpi_eq :
    Cpi α p = 169 * α ^ 6 + damping α p * α ^ 7 / (1 - damping α p * α) :=
  regionalValue_eq (damping α p) α h.renewal_domain

theorem Cpi_pos : 0 < Cpi α p := by
  rw [h.Cpi_eq]
  exact add_pos (mul_pos (by norm_num) (pow_pos h.alpha_pos 6))
    (div_pos (mul_pos (damping_pos α p) (pow_pos h.alpha_pos 7)) h.renewal_denominator_pos)

theorem renewal_value_upper :
    renewalValue (damping α p) α ≤ α ^ 7 / (1 - α) := by
  rw [renewalValue_eq _ _ h.renewal_domain]
  apply div_le_div₀ (pow_nonneg h.alpha_pos.le 7)
  · nlinarith [h.damping_lt_one, pow_pos h.alpha_pos 7]
  · linarith [h.alpha_lt_one]
  · linarith [h.damping_product_lt_alpha]

theorem Cpi_upper :
    Cpi α p ≤ 169 * ((1 : ℝ) / 125) ^ 6 +
      ((1 : ℝ) / 125) ^ 7 / (1 - (1 : ℝ) / 125) := by
  have h6 : α ^ 6 ≤ ((1 : ℝ) / 125) ^ 6 :=
    pow_le_pow_left₀ h.alpha_pos.le h.alpha_coarse_upper.le 6
  have h7 : α ^ 7 ≤ ((1 : ℝ) / 125) ^ 7 :=
    pow_le_pow_left₀ h.alpha_pos.le h.alpha_coarse_upper.le 7
  have hd : α ^ 7 / (1 - α) ≤ ((1 : ℝ) / 125) ^ 7 / (1 - (1 : ℝ) / 125) := by
    apply div_le_div₀ (by positivity) h7 (by norm_num)
    linarith [h.alpha_coarse_upper]
  unfold Cpi regionalValue
  linarith [h.renewal_value_upper]

theorem returnCorrection_pos : 0 < returnCorrection α p := by
  exact mul_pos (div_pos (by norm_num) h.pi_pos) h.Cpi_pos

theorem returnCorrection_upper : returnCorrection α p < (1 : ℝ) / 10 ^ 6 := by
  have hfactor : 90 / p < (30 : ℝ) := by
    apply (div_lt_iff₀ h.pi_pos).mpr
    linarith [h.pi_lower]
  have hmul : (90 / p) * Cpi α p < 30 * Cpi α p :=
    mul_lt_mul_of_pos_right hfactor h.Cpi_pos
  have hnumeric :
      (30 : ℝ) * (169 * ((1 : ℝ) / 125) ^ 6 +
        ((1 : ℝ) / 125) ^ 7 / (1 - (1 : ℝ) / 125)) < (1 : ℝ) / 10 ^ 6 := by
    norm_num
  unfold returnCorrection
  linarith [h.Cpi_upper]

theorem etaRet_lower : (989999 : ℝ) / 10 ^ 6 < etaRet α φ p := by
  unfold etaRet
  linarith [h.H5_lower, h.returnCorrection_upper]

theorem etaRet_pos : 0 < etaRet α φ p := by linarith [h.etaRet_lower]

theorem etaRet_lt_H5 : etaRet α φ p < H5 α φ := by
  unfold etaRet
  linarith [h.returnCorrection_pos]

theorem Ract_gt_one : 1 < Ract α φ p := by
  exact (one_lt_div h.etaRet_pos).mpr h.etaRet_lt_H5

/-- The theorem supplies all three inequalities, rather than assuming the return sign. -/
theorem action_return_inequalities :
    0 < etaRet α φ p ∧ etaRet α φ p < H5 α φ ∧ 1 < Ract α φ p :=
  ⟨h.etaRet_pos, h.etaRet_lt_H5, h.Ract_gt_one⟩

end PrintedDomain

#print axioms PrintedDomain.renewal_domain
#print axioms PrintedDomain.Cpi_eq
#print axioms PrintedDomain.Cpi_upper
#print axioms PrintedDomain.returnCorrection_upper
#print axioms PrintedDomain.etaRet_lower
#print axioms PrintedDomain.action_return_inequalities

end HMT.II.ActionReturn
