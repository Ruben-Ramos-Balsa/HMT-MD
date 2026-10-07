import Mathlib.Analysis.SpecificLimits.Basic

/-! Passing from natural reciprocal meshes to arbitrary positive real meshes.
This is an analytic lemma; the application must prove monotonicity of its
actual unnormalised occupation sum and its natural-mesh limit. -/

noncomputable section
open Set Filter
open scoped Topology

namespace HMT.V.ThermodynamicLimit

theorem real_scale_limit_of_natural {T : ℝ → ℝ} {l : ℝ} (p : ℕ)
    (hmono : MonotoneOn T (Ioi 0))
    (hlim : Tendsto (fun n : ℕ => T n / (n : ℝ)^p) atTop (𝓝 l)) :
    Tendsto (fun t : ℝ => T t / t^p) atTop (𝓝 l) := by
  have hlo : ∀ᶠ t : ℝ in atTop, T (⌊t⌋₊ : ℝ) / t^p ≤ T t / t^p := by
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with t ht
    have hf : 0 < (⌊t⌋₊ : ℝ) := by exact_mod_cast Nat.floor_pos.2 ht
    exact div_le_div_of_nonneg_right
      (hmono hf (lt_of_lt_of_le zero_lt_one ht) (Nat.floor_le (by linarith)))
      (pow_nonneg (by linarith) p)
  have hhi : ∀ᶠ t : ℝ in atTop, T t / t^p ≤ T (⌈t⌉₊ : ℝ) / t^p := by
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with t ht
    exact div_le_div_of_nonneg_right
      (hmono ht (ht.trans_le (Nat.le_ceil t)) (Nat.le_ceil t))
      (pow_nonneg ht.le p)
  have hfloor : Tendsto (fun t : ℝ => T (⌊t⌋₊ : ℝ) / t^p) atTop (𝓝 l) := by
    have h := (hlim.comp tendsto_nat_floor_atTop).mul
      (tendsto_nat_floor_div_atTop.pow p)
    simp only [one_pow, mul_one] at h
    apply h.congr'
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with t ht
    have hf : (⌊t⌋₊ : ℝ) ≠ 0 := by
      exact_mod_cast (Nat.floor_pos.2 ht).ne'
    simp only [Function.comp_apply]
    rw [div_pow, mul_div, div_mul_cancel₀ _ (pow_ne_zero _ hf)]
  have hceil : Tendsto (fun t : ℝ => T (⌈t⌉₊ : ℝ) / t^p) atTop (𝓝 l) := by
    have h := (hlim.comp tendsto_nat_ceil_atTop).mul
      (tendsto_nat_ceil_div_atTop.pow p)
    simp only [one_pow, mul_one] at h
    apply h.congr'
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with t ht
    have hc : (⌈t⌉₊ : ℝ) ≠ 0 := (ht.trans_le (Nat.le_ceil t)).ne'
    simp only [Function.comp_apply]
    rw [div_pow, mul_div, div_mul_cancel₀ _ (pow_ne_zero _ hc)]
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le' hfloor hceil hlo hhi

#print axioms real_scale_limit_of_natural

end HMT.V.ThermodynamicLimit
