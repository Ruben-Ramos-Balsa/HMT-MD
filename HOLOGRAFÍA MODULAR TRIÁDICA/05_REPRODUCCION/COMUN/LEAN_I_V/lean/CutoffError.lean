import ExponentialShellTail
import AnnularExhaustion

noncomputable section
open Set Filter
open scoped Topology

namespace HMT.V.ThermodynamicLimit

def annularErrorBound (C₀ C₁ d : ℝ) (j : ℕ) : ℝ :=
  78*C₀*(1/(j+1 : ℝ))^2 + C₁*shellUniformConstant (d/2)*
    Real.exp (-d*(j+1)/(2*Real.sqrt 3))

theorem annularErrorBound_tendsto (C₀ C₁ : ℝ) {d : ℝ} (hd : 0 < d) :
    Tendsto (annularErrorBound C₀ C₁ d) atTop (𝓝 0) := by
  have hN : Tendsto (fun j : ℕ => (j : ℝ)+1) atTop atTop :=
    tendsto_atTop_add_const_right _ 1 tendsto_natCast_atTop_atTop
  have hsmall : Tendsto (fun j : ℕ => 1/(j+1 : ℝ)) atTop (𝓝 0) := by
    simpa only [one_div] using tendsto_inv_atTop_zero.comp hN
  have hinner := (hsmall.pow 2).const_mul (78*C₀)
  have houter := ((exponential_tail_majorant_tendsto hd).comp hN).const_mul C₁
  have h := hinner.add houter
  simp only [zero_pow (by norm_num : (2 : ℕ) ≠ 0), mul_zero, add_zero] at h
  apply h.congr'
  filter_upwards [] with j
  dsimp [annularErrorBound]
  ring

lemma exhaustion_inner_small {j : ℕ} (hj : 1 ≤ j) :
    Real.sqrt 3 * (1/(j+1 : ℝ)) ≤ 1 := by
  have hs : Real.sqrt 3 ≤ (2 : ℝ) := (Real.sqrt_le_iff).2 ⟨by norm_num, by norm_num⟩
  have hj' : (1 : ℝ) ≤ j := by exact_mod_cast hj
  have hp : (0 : ℝ) < j+1 := by positivity
  rw [mul_one_div, div_le_iff₀ hp]
  linarith

#print axioms annularErrorBound_tendsto

end HMT.V.ThermodynamicLimit
