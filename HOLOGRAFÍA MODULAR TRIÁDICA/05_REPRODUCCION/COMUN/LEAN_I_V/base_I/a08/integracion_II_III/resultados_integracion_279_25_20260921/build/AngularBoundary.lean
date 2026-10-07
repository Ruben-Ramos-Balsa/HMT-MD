import MomentIntegral
import Mathlib.Analysis.SpecialFunctions.Log.NegMulLog
import Mathlib.Analysis.SpecialFunctions.Integrability.LogMeromorphic

/-! The logarithmic angular boundary is removable after multiplication by x.
The logarithm itself is integrable, including its singular endpoint. -/

noncomputable section

open Filter Set MeasureTheory
open scoped Topology

namespace HMT.III.OrientedMoment

theorem cos_pos_quarter {x : ℝ} (hx0 : 0 ≤ x) (hx4 : x ≤ Real.pi / 4) :
    0 < Real.cos x :=
  Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

theorem tan_quarter_bounds {x : ℝ} (hx0 : 0 ≤ x) (hx4 : x ≤ Real.pi / 4) :
    0 ≤ Real.tan x ∧ Real.tan x ≤ 1 := by
  constructor
  · exact Real.tan_nonneg_of_nonneg_of_le_pi_div_two hx0 (by linarith [Real.pi_pos])
  · have hm := Real.strictMonoOn_tan.monotoneOn
    have h := hm (show x ∈ Ioo (-(Real.pi / 2)) (Real.pi / 2) from
      ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩)
      (show Real.pi / 4 ∈ Ioo (-(Real.pi / 2)) (Real.pi / 2) from
      ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩) hx4
    simpa only [Real.tan_pi_div_four] using h

theorem tan_quarter_interior {x : ℝ} (hx0 : 0 < x) (hx4 : x < Real.pi / 4) :
    0 < Real.tan x ∧ Real.tan x < 1 := by
  constructor
  · exact Real.tan_pos_of_pos_of_lt_pi_div_two hx0 (by linarith [Real.pi_pos])
  · have h := Real.tan_lt_tan_of_nonneg_of_lt_pi_div_two hx0.le
      (by linarith [Real.pi_pos] : Real.pi / 4 < Real.pi / 2) hx4
    simpa only [Real.tan_pi_div_four] using h

theorem tan_quarter_continuous : ContinuousOn Real.tan (Icc (0 : ℝ) (Real.pi / 4)) := by
  intro x hx
  exact (Real.continuousAt_tan.2 (ne_of_gt (cos_pos_quarter hx.1 hx.2))).continuousWithinAt

theorem tan_dslope_zero : dslope Real.tan 0 0 = 1 := by
  rw [dslope_same, (Real.hasDerivAt_tan (x := 0) (by simp)).deriv]
  norm_num

theorem mul_log_tan_factor (x : ℝ) :
    x * Real.log (Real.tan x) =
      (dslope Real.tan 0 x)⁻¹ * (Real.tan x * Real.log (Real.tan x)) := by
  by_cases hx : x = 0
  · subst x
    simp
  · by_cases ht : Real.tan x = 0
    · simp [ht]
    · rw [dslope_of_ne _ hx, slope_def_field]
      simp only [Real.tan_zero, sub_zero, inv_div]
      field_simp [ht]
      ring

theorem mul_log_tan_continuousAt_zero :
    ContinuousAt (fun x : ℝ => x * Real.log (Real.tan x)) 0 := by
  have ht : HasDerivAt Real.tan 1 0 := by
    simpa using Real.hasDerivAt_tan (x := 0) (by simp)
  have hd : ContinuousAt (dslope Real.tan 0) 0 := continuousAt_dslope_same.2 ht.differentiableAt
  have hi := hd.inv₀ (by rw [tan_dslope_zero]; norm_num)
  have hm : ContinuousAt (fun x : ℝ => Real.tan x * Real.log (Real.tan x)) 0 :=
    Real.continuous_mul_log.continuousAt.comp ht.continuousAt
  have he : (fun x : ℝ => x * Real.log (Real.tan x)) =
      (fun x => (dslope Real.tan 0 x)⁻¹ * (Real.tan x * Real.log (Real.tan x))) :=
    funext mul_log_tan_factor
  rw [he]
  exact hi.mul hm

theorem mul_log_tan_origin_limit :
    Tendsto (fun x : ℝ => x * Real.log (Real.tan x)) (𝓝 (0 : ℝ)) (𝓝 0) := by
  simpa only [zero_mul] using mul_log_tan_continuousAt_zero.tendsto

theorem mul_log_tan_quarter_continuous :
    ContinuousOn (fun x : ℝ => x * Real.log (Real.tan x)) (Icc 0 (Real.pi / 4)) := by
  intro x hx
  by_cases hx0 : x = 0
  · subst x
    exact mul_log_tan_continuousAt_zero.continuousWithinAt
  · have hp : 0 < x := lt_of_le_of_ne hx.1 (Ne.symm hx0)
    have htan := Real.continuousAt_tan.2 (ne_of_gt (cos_pos_quarter hx.1 hx.2))
    have htpos := Real.tan_pos_of_pos_of_lt_pi_div_two hp (by linarith [hx.2, Real.pi_pos])
    exact (continuousAt_id.mul (htan.log (ne_of_gt htpos))).continuousWithinAt

theorem log_tan_intervalIntegrable (a b : ℝ) :
    IntervalIntegrable (fun x : ℝ => Real.log (Real.tan x)) volume a b := by
  have hm : MeromorphicOn (fun x : ℝ => Real.sin x / Real.cos x) (uIcc a b) :=
    Real.analyticOnNhd_sin.meromorphicOn.div Real.analyticOnNhd_cos.meromorphicOn
  simpa only [Function.comp_def, Real.tan_eq_sin_div_cos] using hm.intervalIntegrable_log

#print axioms tan_quarter_bounds
#print axioms mul_log_tan_origin_limit
#print axioms mul_log_tan_quarter_continuous
#print axioms log_tan_intervalIntegrable

end HMT.III.OrientedMoment
