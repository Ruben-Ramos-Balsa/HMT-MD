import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Algebra.GeomSum
import Mathlib.Tactic

/-! Trivalent returns at an arbitrary positive height. The geometric series
is constructed before its rational reading and its one-sided pole limit. -/
noncomputable section
namespace HMT.OrientedReturn
open Filter Set
open scoped Topology BigOperators

def returnSeries (m : ℕ) (q : ℝ) : ℝ := q ^ m / (1 - q ^ (3 * m))

theorem returnSeries_hasSum {m : ℕ} (hm : 0 < m) {q : ℝ} (hq : q ∈ Ioo 0 1) :
    HasSum (fun j : ℕ => q ^ (m + 3 * m * j)) (returnSeries m q) := by
  have hp : q ^ (3 * m) < 1 := pow_lt_one₀ hq.1.le hq.2 (by omega)
  have h := (hasSum_geometric_of_lt_one (pow_nonneg hq.1.le _) hp).mul_left (q ^ m)
  simpa only [← pow_mul, ← pow_add, returnSeries, div_eq_mul_inv] using h

theorem returnSeries_pos {m : ℕ} (hm : 0 < m) {q : ℝ} (hq : q ∈ Ioo 0 1) :
    0 < returnSeries m q :=
  div_pos (pow_pos hq.1 _) (sub_pos.mpr (pow_lt_one₀ hq.1.le hq.2 (by omega)))

theorem returnSeries_truncations {m : ℕ} (hm : 0 < m) {q : ℝ} (hq : q ∈ Ioo 0 1) :
    Tendsto (fun N => ∑ j ∈ Finset.range N, q ^ (m + 3 * m * j))
      atTop (𝓝 (returnSeries m q)) := (returnSeries_hasSum hm hq).tendsto_sum_nat

def poleExtension (m : ℕ) (q : ℝ) : ℝ :=
  q ^ m / ∑ j ∈ Finset.range (3 * m), q ^ j

theorem pole_cancellation (m : ℕ) {q : ℝ} (hq : q ≠ 1) :
    (1 - q) * returnSeries m q = poleExtension m q := by
  have h1 : 1 - q ≠ 0 := sub_ne_zero.mpr (Ne.symm hq)
  rw [returnSeries, ← geom_sum_mul_neg q (3 * m), poleExtension]
  rw [mul_comm (∑ j ∈ Finset.range (3 * m), q ^ j) (1 - q)]
  rw [← mul_div_assoc, mul_div_mul_left _ _ h1]

theorem poleExtension_one (m : ℕ) : poleExtension m 1 = 1 / (3 * m : ℕ) := by
  simp [poleExtension]

theorem poleExtension_continuousAt_one {m : ℕ} (hm : 0 < m) :
    ContinuousAt (poleExtension m) 1 := by
  unfold poleExtension
  apply ContinuousAt.div
  · fun_prop
  · fun_prop
  · simp only [one_pow, Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one]
    exact_mod_cast (show 3 * m ≠ 0 by omega)

theorem returnSeries_pole {m : ℕ} (hm : 0 < m) :
    Tendsto (fun q : ℝ => (1 - q) * returnSeries m q)
      (𝓝[<] 1) (𝓝 (1 / (3 * m : ℕ))) := by
  have h : Tendsto (poleExtension m) (𝓝[<] 1) (𝓝 (poleExtension m 1)) :=
    (poleExtension_continuousAt_one hm).tendsto.mono_left nhdsWithin_le_nhds
  rw [poleExtension_one] at h
  apply h.congr'
  filter_upwards [self_mem_nhdsWithin] with q hq
  exact (pole_cancellation m (ne_of_lt hq)).symm

def fundamentalReturn (q : ℝ) : ℝ := 12 * returnSeries 90 q - returnSeries 120 q

theorem fundamentalReturn_pole :
    Tendsto (fun q : ℝ => (1 - q) * fundamentalReturn q)
      (𝓝[<] 1) (𝓝 ((1 : ℝ) / 24)) := by
  have h := ((returnSeries_pole (by decide : 0 < 90)).const_mul 12).sub
    (returnSeries_pole (by decide : 0 < 120))
  norm_num at h
  convert h using 1
  funext q
  unfold fundamentalReturn
  ring

theorem fundamentalReturn_opposite_coordinate :
    Tendsto (fun q : ℝ => (q - 1) * fundamentalReturn q)
      (𝓝[<] 1) (𝓝 (-(1 : ℝ) / 24)) := by
  convert fundamentalReturn_pole.neg using 1
  · funext q; ring
  · ring

#print axioms returnSeries_hasSum
#print axioms returnSeries_truncations
#print axioms returnSeries_pole
#print axioms fundamentalReturn_pole
#print axioms fundamentalReturn_opposite_coordinate
end HMT.OrientedReturn
