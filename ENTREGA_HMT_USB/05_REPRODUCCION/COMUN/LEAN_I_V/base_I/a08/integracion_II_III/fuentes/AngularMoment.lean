import AngularBoundary

/-! Angular substitution and integration by parts, including the zero endpoint.
These exact integral identities do not assume the Fourier evaluation at Pell. -/

noncomputable section

open Set MeasureTheory

namespace HMT.III.OrientedMoment

theorem moment_tan_continuousOn :
    ContinuousOn (fun x : ℝ => moment (Real.tan x)) (Icc 0 (Real.pi / 4)) :=
  moment_continuousOn.comp tan_quarter_continuous (fun _ hx => tan_quarter_bounds hx.1 hx.2)

theorem moment_tan_hasDerivAt {x : ℝ} (hx0 : 0 < x) (hx4 : x < Real.pi / 4) :
    HasDerivAt (fun y : ℝ => moment (Real.tan y))
      ((x / Real.tan x) * (1 / Real.cos x ^ 2)) x := by
  have hb := tan_quarter_interior hx0 hx4
  have hc := ne_of_gt (cos_pos_quarter hx0.le hx4.le)
  convert (moment_hasDerivAt_quotient hb.1 hb.2).comp x (Real.hasDerivAt_tan hc) using 1
  rw [Real.arctan_tan (by linarith [Real.pi_pos]) (by linarith [Real.pi_pos])]

def angularPrimitive (x : ℝ) : ℝ := x * Real.log (Real.tan x) - moment (Real.tan x)

theorem angularPrimitive_continuousOn : ContinuousOn angularPrimitive (Icc 0 (Real.pi / 4)) :=
  mul_log_tan_quarter_continuous.sub moment_tan_continuousOn

theorem angularPrimitive_hasDerivAt {x : ℝ} (hx0 : 0 < x) (hx4 : x < Real.pi / 4) :
    HasDerivAt angularPrimitive (Real.log (Real.tan x)) x := by
  have hp := (tan_quarter_interior hx0 hx4).1
  have hc := ne_of_gt (cos_pos_quarter hx0.le hx4.le)
  convert ((hasDerivAt_id x).mul ((Real.hasDerivAt_tan hc).log (ne_of_gt hp))).sub
    (moment_tan_hasDerivAt hx0 hx4) using 1
  simp only [id_eq]
  ring

theorem angular_moment {θ : ℝ} (hθ0 : 0 ≤ θ) (hθ4 : θ ≤ Real.pi / 4) :
    moment (Real.tan θ) = θ * Real.log (Real.tan θ) -
      ∫ x in (0 : ℝ)..θ, Real.log (Real.tan x) := by
  have hi := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le hθ0
    (angularPrimitive_continuousOn.mono (Icc_subset_Icc le_rfl hθ4))
    (fun x hx => angularPrimitive_hasDerivAt hx.1 (lt_of_lt_of_le hx.2 hθ4))
    (log_tan_intervalIntegrable 0 θ)
  simp only [angularPrimitive, Real.tan_zero, moment_zero, zero_mul, sub_zero, sub_self] at hi
  linarith

theorem angular_change_and_parts {θ : ℝ} (hθ0 : 0 ≤ θ) (hθ4 : θ ≤ Real.pi / 4) :
    (∫ t in (0 : ℝ)..Real.tan θ, Real.arctan t / t) =
      θ * Real.log (Real.tan θ) - ∫ x in (0 : ℝ)..θ, Real.log (Real.tan x) := by
  have hb := tan_quarter_bounds hθ0 hθ4
  rw [← moment_integral hb.1 hb.2]
  exact angular_moment hθ0 hθ4

theorem catalan_log_tangent :
    catalan = -(∫ x in (0 : ℝ)..(Real.pi / 4), Real.log (Real.tan x)) := by
  simpa only [Real.tan_pi_div_four, Real.log_one, mul_zero, zero_sub] using
    angular_moment (θ := Real.pi / 4) (by positivity) le_rfl

theorem pell_log_tangent :
    moment pellRho = -(Real.pi / 12) * Real.log pellLambda -
      ∫ x in (0 : ℝ)..(Real.pi / 12), Real.log (Real.tan x) := by
  have h := angular_moment (θ := Real.pi / 12) (by positivity) (by linarith [Real.pi_pos])
  rw [tan_pi_twelfth, log_pell_reciprocal] at h
  simpa only [mul_neg, neg_mul] using h

#print axioms moment_tan_hasDerivAt
#print axioms angularPrimitive_hasDerivAt
#print axioms angular_moment
#print axioms angular_change_and_parts
#print axioms catalan_log_tangent
#print axioms pell_log_tangent

end HMT.III.OrientedMoment
