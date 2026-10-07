import NormalizedQuarterTurn
import Mathlib.Analysis.PSeries
import Mathlib.Analysis.NormedSpace.FunctionSeries

/-! The depth moment is a real series, not a solution postulated from its
differential equation. Absolute and uniform convergence include both endpoints. -/

noncomputable section

open Filter Set

namespace HMT.III.OrientedMoment

def term (n : ℕ) (s : ℝ) : ℝ := (-1) ^ n * s ^ (2 * n + 1) / ((2 * n + 1 : ℕ) : ℝ) ^ 2
def majorant (n : ℕ) : ℝ := 1 / ((2 * n + 1 : ℕ) : ℝ) ^ 2
def moment (s : ℝ) : ℝ := ∑' n, term n s
def catalan : ℝ := moment 1

theorem term_from_character (n : ℕ) (s : ℝ) :
    term n s = (((quarter : Plane → Plane)^[2 * n + 1]) (1, 0)).2 *
      s ^ (2 * n + 1) / ((2 * n + 1 : ℕ) : ℝ) ^ 2 := by
  rw [quarter_odd_character]
  rfl

theorem majorant_summable : Summable majorant := by
  have hi : Function.Injective (fun n : ℕ => 2 * n + 1) := by
    intro m n h
    dsimp only at h
    omega
  exact (Real.summable_one_div_nat_pow.mpr (by decide : 1 < (2 : ℕ))).comp_injective hi

theorem term_norm (n : ℕ) (s : ℝ) :
    ‖term n s‖ = ‖s‖ ^ (2 * n + 1) / ((2 * n + 1 : ℕ) : ℝ) ^ 2 := by
  simp [term, norm_div, norm_mul, norm_pow]

theorem term_bound (n : ℕ) {s : ℝ} (hs : ‖s‖ ≤ 1) : ‖term n s‖ ≤ majorant n := by
  rw [term_norm]
  exact div_le_div_of_nonneg_right (pow_le_one₀ (norm_nonneg s) hs) (sq_nonneg _)

theorem moment_absolute {s : ℝ} (hs : ‖s‖ ≤ 1) : Summable (fun n => ‖term n s‖) :=
  Summable.of_nonneg_of_le (fun _ => norm_nonneg _) (fun n => term_bound n hs) majorant_summable

theorem moment_summable {s : ℝ} (hs : ‖s‖ ≤ 1) : Summable (fun n => term n s) :=
  (moment_absolute hs).of_norm

theorem moment_uniform :
    TendstoUniformlyOn (fun N : ℕ => fun s => ∑ n ∈ Finset.range N, term n s)
      moment atTop (Icc (0 : ℝ) 1) := by
  apply tendstoUniformlyOn_tsum_nat majorant_summable
  intro n s hs
  exact term_bound n (by simpa only [Real.norm_eq_abs, abs_of_nonneg hs.1] using hs.2)

theorem moment_continuousOn : ContinuousOn moment (Icc (0 : ℝ) 1) := by
  apply continuousOn_tsum (fun n => ?_) majorant_summable
  · intro n s hs
    exact term_bound n (by simpa only [Real.norm_eq_abs, abs_of_nonneg hs.1] using hs.2)
  · unfold term
    fun_prop

theorem moment_zero : moment 0 = 0 := by
  simp [moment, term]

theorem catalan_series : catalan = ∑' n : ℕ, (-1 : ℝ) ^ n / ((2 * n + 1 : ℕ) : ℝ) ^ 2 := by
  simp [catalan, moment, term]

#print axioms majorant_summable
#print axioms term_from_character
#print axioms moment_absolute
#print axioms moment_uniform
#print axioms moment_continuousOn
#print axioms moment_zero
#print axioms catalan_series

end HMT.III.OrientedMoment
