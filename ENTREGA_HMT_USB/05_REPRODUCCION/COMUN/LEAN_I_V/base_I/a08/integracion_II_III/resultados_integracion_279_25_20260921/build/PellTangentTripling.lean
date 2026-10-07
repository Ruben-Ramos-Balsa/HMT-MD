import AngularMoment

/-! An elementary alternative to the Fourier bridge: tangent tripling, affine
changes of variable, and reflection evaluate the required logarithmic integral.
No special-value identity is supplied as a hypothesis. -/

noncomputable section

open Set MeasureTheory

namespace HMT.III.OrientedMoment

theorem sin_shift_product (x : ℝ) :
    Real.sin (Real.pi / 3 + x) * Real.sin (Real.pi / 3 - x) =
      (3 - 4 * Real.sin x ^ 2) / 4 := by
  calc
    _ = (Real.sqrt 3 ^ 2 * Real.cos x ^ 2 - Real.sin x ^ 2) / 4 := by
      rw [Real.sin_add, Real.sin_sub, Real.sin_pi_div_three, Real.cos_pi_div_three]
      ring
    _ = _ := by
      rw [sqrt_three_sq]
      nlinarith [Real.sin_sq_add_cos_sq x]

theorem cos_shift_product (x : ℝ) :
    Real.cos (Real.pi / 3 + x) * Real.cos (Real.pi / 3 - x) =
      (4 * Real.cos x ^ 2 - 3) / 4 := by
  calc
    _ = (Real.cos x ^ 2 - Real.sqrt 3 ^ 2 * Real.sin x ^ 2) / 4 := by
      rw [Real.cos_add, Real.cos_sub, Real.sin_pi_div_three, Real.cos_pi_div_three]
      ring
    _ = _ := by
      rw [sqrt_three_sq]
      nlinarith [Real.sin_sq_add_cos_sq x]

theorem sin_triple_product (x : ℝ) :
    Real.sin (3 * x) = 4 * Real.sin x *
      (Real.sin (Real.pi / 3 + x) * Real.sin (Real.pi / 3 - x)) := by
  rw [Real.sin_three_mul, sin_shift_product]
  ring

theorem cos_triple_product (x : ℝ) :
    Real.cos (3 * x) = 4 * Real.cos x *
      (Real.cos (Real.pi / 3 + x) * Real.cos (Real.pi / 3 - x)) := by
  rw [Real.cos_three_mul, cos_shift_product]
  ring

theorem tangent_triple_product (x : ℝ) :
    Real.tan (3 * x) = Real.tan x * Real.tan (Real.pi / 3 + x) * Real.tan (Real.pi / 3 - x) := by
  simp only [Real.tan_eq_sin_div_cos]
  rw [sin_triple_product, cos_triple_product]
  simp only [div_eq_mul_inv, mul_inv_rev]
  ring

def logTan (x : ℝ) : ℝ := Real.log (Real.tan x)

theorem logTan_triple {x : ℝ} (hx0 : 0 < x) (hx12 : x ≤ Real.pi / 12) :
    logTan (3 * x) = logTan x + logTan (Real.pi / 3 + x) + logTan (Real.pi / 3 - x) := by
  have h0 : 0 < Real.tan x :=
    Real.tan_pos_of_pos_of_lt_pi_div_two hx0 (by linarith [Real.pi_pos])
  have hp : 0 < Real.tan (Real.pi / 3 + x) :=
    Real.tan_pos_of_pos_of_lt_pi_div_two (by linarith [Real.pi_pos]) (by linarith [Real.pi_pos])
  have hm : 0 < Real.tan (Real.pi / 3 - x) :=
    Real.tan_pos_of_pos_of_lt_pi_div_two (by linarith [Real.pi_pos]) (by linarith [Real.pi_pos])
  unfold logTan
  rw [tangent_triple_product, Real.log_mul (ne_of_gt (mul_pos h0 hp)) (ne_of_gt hm),
    Real.log_mul (ne_of_gt h0) (ne_of_gt hp)]

theorem logTan_reflection (x : ℝ) : logTan (Real.pi / 2 - x) = -logTan x := by
  simp [logTan, Real.tan_pi_div_two_sub, Real.log_inv]

theorem logTan_integrable (a b : ℝ) : IntervalIntegrable logTan volume a b :=
  log_tan_intervalIntegrable a b

theorem logTan_shift_plus_integrable (a b c : ℝ) :
    IntervalIntegrable (fun x => logTan (c + x)) volume a b := by
  convert (logTan_integrable (c + a) (c + b)).comp_add_left c using 1 <;> ring

theorem logTan_shift_minus_integrable (a b c : ℝ) :
    IntervalIntegrable (fun x => logTan (c - x)) volume a b := by
  convert (logTan_integrable (c - a) (c - b)).comp_sub_left c using 1 <;> ring

theorem logTan_integral_tripling :
    (∫ x in (0 : ℝ)..(Real.pi / 12), logTan (3 * x)) =
      (∫ x in (0 : ℝ)..(Real.pi / 12), logTan x) +
      (∫ x in (0 : ℝ)..(Real.pi / 12), logTan (Real.pi / 3 + x)) +
      (∫ x in (0 : ℝ)..(Real.pi / 12), logTan (Real.pi / 3 - x)) := by
  calc
    _ = ∫ x in (0 : ℝ)..(Real.pi / 12),
        (logTan x + logTan (Real.pi / 3 + x) + logTan (Real.pi / 3 - x)) := by
      apply intervalIntegral.integral_congr_ae
      filter_upwards [] with x hx
      have hi : x ∈ Ioc (0 : ℝ) (Real.pi / 12) := by
        simpa only [uIoc_of_le (by positivity : (0 : ℝ) ≤ Real.pi / 12)] using hx
      exact logTan_triple hi.1 hi.2
    _ = _ := by
      rw [intervalIntegral.integral_add
        ((logTan_integrable _ _).add (logTan_shift_plus_integrable _ _ _))
        (logTan_shift_minus_integrable _ _ _),
        intervalIntegral.integral_add (logTan_integrable _ _) (logTan_shift_plus_integrable _ _ _)]

theorem logTan_pell_ratio :
    (∫ x in (0 : ℝ)..(Real.pi / 12), logTan x) =
      (2 / 3 : ℝ) * (∫ x in (0 : ℝ)..(Real.pi / 4), logTan x) := by
  have hscale : (∫ x in (0 : ℝ)..(Real.pi / 12), logTan (3 * x)) =
      (1 / 3 : ℝ) * (∫ x in (0 : ℝ)..(Real.pi / 4), logTan x) := by
    rw [intervalIntegral.integral_comp_mul_left _ (by norm_num : (3 : ℝ) ≠ 0)]
    rw [mul_zero, show 3 * (Real.pi / 12) = Real.pi / 4 by ring]
    simp only [smul_eq_mul, one_div]
  have hplus : (∫ x in (0 : ℝ)..(Real.pi / 12), logTan (Real.pi / 3 + x)) =
      ∫ x in (Real.pi / 3)..(5 * Real.pi / 12), logTan x := by
    rw [intervalIntegral.integral_comp_add_left, add_zero,
      show Real.pi / 3 + Real.pi / 12 = 5 * Real.pi / 12 by ring]
  have hminus : (∫ x in (0 : ℝ)..(Real.pi / 12), logTan (Real.pi / 3 - x)) =
      ∫ x in (Real.pi / 4)..(Real.pi / 3), logTan x := by
    rw [intervalIntegral.integral_comp_sub_left, sub_zero,
      show Real.pi / 3 - Real.pi / 12 = Real.pi / 4 by ring]
  have hreflect : (∫ x in (Real.pi / 4)..(5 * Real.pi / 12), logTan x) =
      -(∫ x in (Real.pi / 12)..(Real.pi / 4), logTan x) := by
    have h := intervalIntegral.integral_comp_sub_left logTan (a := Real.pi / 4)
      (b := 5 * Real.pi / 12) (Real.pi / 2)
    simp_rw [logTan_reflection, intervalIntegral.integral_neg] at h
    rw [show Real.pi / 2 - 5 * Real.pi / 12 = Real.pi / 12 by ring,
      show Real.pi / 2 - Real.pi / 4 = Real.pi / 4 by ring] at h
    linarith
  have hjoin := intervalIntegral.integral_add_adjacent_intervals
    (logTan_integrable (Real.pi / 4) (Real.pi / 3))
    (logTan_integrable (Real.pi / 3) (5 * Real.pi / 12))
  have hsplit := intervalIntegral.integral_add_adjacent_intervals
    (logTan_integrable 0 (Real.pi / 12)) (logTan_integrable (Real.pi / 12) (Real.pi / 4))
  have ht := logTan_integral_tripling
  rw [hscale, hplus, hminus] at ht
  linarith

theorem catalan_pell_value :
    moment pellRho = (2 / 3 : ℝ) * catalan - (Real.pi / 12) * Real.log pellLambda := by
  have hr := logTan_pell_ratio
  unfold logTan at hr
  rw [pell_log_tangent, hr, catalan_log_tangent]
  ring

theorem catalan_pell_complete :
    moment pellRho = (2 / 3 : ℝ) * catalan - (Real.pi / 12) * Real.log pellLambda ∧
    euler moment pellRho = Real.pi / 12 ∧
    euler (euler moment) pellRho = (1 / 4 : ℝ) :=
  ⟨catalan_pell_value, euler_pell, second_euler_pell⟩

#print axioms tangent_triple_product
#print axioms logTan_triple
#print axioms logTan_integral_tripling
#print axioms logTan_pell_ratio
#print axioms catalan_pell_value
#print axioms catalan_pell_complete

end HMT.III.OrientedMoment
