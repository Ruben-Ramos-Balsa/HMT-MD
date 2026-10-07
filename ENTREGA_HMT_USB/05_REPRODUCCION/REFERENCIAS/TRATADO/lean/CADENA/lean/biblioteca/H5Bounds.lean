import Mathlib

/-!
# The declared degree-five analytic character and its rational domain

The inputs below are posterior real coordinates of the upstream construction.
The four polynomial coefficients and their assignment to degrees are exactly
the declared character in `05_accion.tex` and `revision_planck.tex`.
The implementation neither extracts these inputs nor fits a Planck datum.
-/

noncomputable section

namespace HMT.II.ActionReturn

/-- Exact printed rational intervals; `p` is the supplied generated pi coordinate. -/
structure PrintedDomain (α φ p : ℝ) : Prop where
  phi_lower : (1618 : ℝ) / 1000 < φ
  phi_upper : φ < (1619 : ℝ) / 1000
  alpha_lower : (7297 : ℝ) / 10 ^ 6 < α
  alpha_upper : α < (7298 : ℝ) / 10 ^ 6
  pi_lower : 3 < p

/-- Literal analytic character, including its degree assignment and signs. -/
def H5 (α φ : ℝ) : ℝ :=
  (1 / 2) * Real.sqrt (1000 * α / φ) - α + (9 / 16) * α ^ 2 -
    (5 / 9) * α ^ 3 + (7 / 48) * α ^ 4 - (1 / 54) * α ^ 5

namespace PrintedDomain

variable {α φ p : ℝ} (h : PrintedDomain α φ p)
include h

theorem alpha_pos : 0 < α := by linarith [h.alpha_lower]
theorem phi_pos : 0 < φ := by linarith [h.phi_lower]
theorem pi_pos : 0 < p := by linarith [h.pi_lower]
theorem alpha_coarse_lower : (7 : ℝ) / 1000 < α := by linarith [h.alpha_lower]
theorem alpha_coarse_upper : α < (1 : ℝ) / 125 := by linarith [h.alpha_upper]
theorem alpha_lt_one : α < 1 := by linarith [h.alpha_coarse_upper]

theorem sqrt_character_lower : 2 < Real.sqrt (1000 * α / φ) := by
  apply Real.lt_sqrt_of_sq_lt
  apply (lt_div_iff₀ h.phi_pos).mpr
  nlinarith [h.alpha_coarse_lower, h.phi_upper]

theorem negative_terms_bound :
    α + (5 / 9 : ℝ) * α ^ 3 + (1 / 54 : ℝ) * α ^ 5 < (8001 : ℝ) / 10 ^ 6 := by
  have h3 : α ^ 3 ≤ ((1 : ℝ) / 125) ^ 3 :=
    pow_le_pow_left₀ h.alpha_pos.le h.alpha_coarse_upper.le 3
  have h5 : α ^ 5 ≤ ((1 : ℝ) / 125) ^ 5 :=
    pow_le_pow_left₀ h.alpha_pos.le h.alpha_coarse_upper.le 5
  calc
    α + (5 / 9 : ℝ) * α ^ 3 + (1 / 54 : ℝ) * α ^ 5 ≤
        1 / 125 + (5 / 9 : ℝ) * (1 / 125) ^ 3 + (1 / 54 : ℝ) * (1 / 125) ^ 5 := by
      linarith [h.alpha_coarse_upper]
    _ < (8001 : ℝ) / 10 ^ 6 := by norm_num

theorem H5_lower : (99 : ℝ) / 100 < H5 α φ := by
  have h2 : 0 ≤ α ^ 2 := sq_nonneg α
  have h4 : 0 ≤ α ^ 4 := pow_nonneg h.alpha_pos.le 4
  have hs := h.sqrt_character_lower
  have hn := h.negative_terms_bound
  unfold H5
  linarith

theorem H5_pos : 0 < H5 α φ := by linarith [h.H5_lower]

end PrintedDomain

#print axioms PrintedDomain.sqrt_character_lower
#print axioms PrintedDomain.negative_terms_bound
#print axioms PrintedDomain.H5_lower
#print axioms PrintedDomain.H5_pos

end HMT.II.ActionReturn
