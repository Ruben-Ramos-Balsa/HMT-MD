import MomentDerivatives

/-! The Pell evaluation point is downstream of the oriented moment. This file
proves its reciprocal and differential evaluations, not the log-tangent moment
identity involving Catalan's endpoint value. -/

noncomputable section

namespace HMT.III.OrientedMoment

def pellLambda : ℝ := 2 + Real.sqrt 3
def pellRho : ℝ := 2 - Real.sqrt 3

theorem sqrt_three_sq : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)

theorem pellRho_pos : 0 < pellRho := by
  unfold pellRho
  nlinarith [sqrt_three_sq, Real.sqrt_nonneg 3]

theorem pellRho_lt_one : pellRho < 1 := by
  unfold pellRho
  nlinarith [sqrt_three_sq, Real.sqrt_nonneg 3]

theorem pellLambda_pos : 0 < pellLambda := by unfold pellLambda; positivity

theorem pell_norm : pellLambda * pellRho = 1 := by
  unfold pellLambda pellRho
  nlinarith [sqrt_three_sq]

theorem pell_reciprocal : pellRho = pellLambda⁻¹ := by
  apply mul_left_cancel₀ (ne_of_gt pellLambda_pos)
  rw [pell_norm, mul_inv_cancel₀ (ne_of_gt pellLambda_pos)]

theorem pell_sum_reciprocal : pellRho + pellRho⁻¹ = 4 := by
  rw [pell_reciprocal, inv_inv, ← pell_reciprocal]
  unfold pellRho pellLambda
  ring

theorem kernel_pell : kernel pellRho = (1 / 4 : ℝ) := by
  unfold kernel pellRho
  have hs : 1 + (2 - Real.sqrt 3) ^ 2 ≠ 0 := ne_of_gt (by positivity)
  field_simp [hs]
  nlinarith [sqrt_three_sq]

theorem tan_pi_twelfth : Real.tan (Real.pi / 12) = pellRho := by
  have h2 : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num)
  have h3 : 0 < Real.sqrt 3 := Real.sqrt_pos.2 (by norm_num)
  have hd : Real.sqrt 3 + 1 ≠ 0 := ne_of_gt (by positivity)
  calc
    Real.tan (Real.pi / 12) = (Real.sqrt 3 - 1) / (Real.sqrt 3 + 1) := by
      rw [Real.tan_eq_sin_div_cos, show Real.pi / 12 = Real.pi / 4 - Real.pi / 6 by ring,
        Real.sin_sub, Real.cos_sub, Real.sin_pi_div_four, Real.cos_pi_div_four,
        Real.sin_pi_div_six, Real.cos_pi_div_six]
      field_simp
      ring
    _ = pellRho := by
      unfold pellRho
      apply (div_eq_iff hd).2
      nlinarith [sqrt_three_sq]

theorem arctan_pell : Real.arctan pellRho = Real.pi / 12 := by
  rw [← tan_pi_twelfth]
  exact Real.arctan_tan (by linarith [Real.pi_pos]) (by linarith [Real.pi_pos])

theorem euler_pell : euler moment pellRho = Real.pi / 12 := by
  rw [euler_moment (by simpa only [Real.norm_eq_abs, abs_of_pos pellRho_pos] using pellRho_lt_one)]
  exact arctan_pell

theorem second_euler_pell : euler (euler moment) pellRho = (1 / 4 : ℝ) := by
  rw [second_euler_moment
    (by simpa only [Real.norm_eq_abs, abs_of_pos pellRho_pos] using pellRho_lt_one)]
  exact kernel_pell

theorem log_pell_reciprocal : Real.log pellRho = -Real.log pellLambda := by
  rw [pell_reciprocal, Real.log_inv]

#print axioms pell_norm
#print axioms pell_reciprocal
#print axioms kernel_pell
#print axioms arctan_pell
#print axioms euler_pell
#print axioms second_euler_pell

end HMT.III.OrientedMoment
