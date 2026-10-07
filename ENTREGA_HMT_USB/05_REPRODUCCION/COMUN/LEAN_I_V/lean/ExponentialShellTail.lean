import Mathlib

/-!
# Uniform exponential shell tails

Analytic component of article V, `71_limite_termodinamico.tex`.
The positive shell index is represented by `n + 1`. No lattice-counting or
Riemann-sum convergence theorem is asserted here.
-/

noncomputable section
open Set Real Filter
open scoped BigOperators

namespace HMT.V.ThermodynamicLimit

/-- Convexity of exp, equivalently concavity of `1 - exp (-c*x)`. -/
theorem exponential_gap_lower (c : ℝ) {delta : ℝ}
    (hdelta : 0 ≤ delta) (hdelta1 : delta ≤ 1) :
    delta * (1 - Real.exp (-c)) ≤ 1 - Real.exp (-(c * delta)) := by
  have h := convexOn_exp.2 (mem_univ (-c)) (mem_univ 0)
    hdelta (sub_nonneg.mpr hdelta1) (by ring : delta + (1 - delta) = 1)
  simp only [smul_eq_mul, mul_zero, add_zero, Real.exp_zero, mul_one] at h
  have he : delta * -c = -(c * delta) := by ring
  rw [he] at h
  linarith

theorem square_geometric_hasSum {q : ℝ} (hq0 : 0 ≤ q) (hq1 : q < 1) :
    HasSum (fun n : ℕ => (n + 1 : ℝ) ^ 2 * q ^ n)
      ((1 + q) / (1 - q) ^ 3) := by
  have hqn : ‖q‖ < 1 := by simpa [Real.norm_eq_abs, abs_of_nonneg hq0] using hq1
  have h2 := (hasSum_choose_mul_geometric_of_norm_lt_one 2 hqn).mul_left 2
  have h1 := hasSum_choose_mul_geometric_of_norm_lt_one 1 hqn
  convert h2.sub h1 using 1
  · ext n
    simp only [Nat.cast_choose_two, Nat.cast_add, Nat.cast_ofNat, Nat.choose_one_right,
      Nat.cast_one]
    ring
  · field_simp [ne_of_gt (sub_pos.mpr hq1)]
    ring

def shellWeight (n : ℕ) : ℝ := 24 * (n + 1 : ℝ) ^ 2 + 2

theorem shellWeight_pos (n : ℕ) : 0 < shellWeight n := by
  unfold shellWeight
  positivity

theorem shell_geometric_hasSum {q : ℝ} (hq0 : 0 ≤ q) (hq1 : q < 1) :
    HasSum (fun n : ℕ => shellWeight n * q ^ (n + 1))
      (24 * q * (1 + q) / (1 - q) ^ 3 + 2 * q / (1 - q)) := by
  have hs := ((square_geometric_hasSum hq0 hq1).mul_left (24 * q)).add
    ((hasSum_geometric_of_lt_one hq0 hq1).mul_left (2 * q))
  convert hs using 1
  · ext n
    simp only [shellWeight, pow_succ]
    ring
  · ring

theorem shell_geometric_le {q : ℝ} (hq0 : 0 ≤ q) (hq1 : q < 1) :
    (∑' n : ℕ, shellWeight n * q ^ (n + 1)) ≤ 50 / (1 - q) ^ 3 := by
  rw [(shell_geometric_hasSum hq0 hq1).tsum_eq]
  have hk : 0 < 1 - q := sub_pos.mpr hq1
  have hq : q ≤ 1 := hq1.le
  have hk1 : 1 - q ≤ 1 := by linarith
  have hk2 : (1 - q) ^ 2 ≤ 1 := by nlinarith
  have hprod : q * (1 + q) ≤ 2 := by nlinarith [sq_nonneg q]
  have hprod2 : q * (1 - q) ^ 2 ≤ 1 :=
    (mul_le_mul hq hk2 (sq_nonneg _) (by norm_num)).trans_eq (by ring)
  have he : 24 * q * (1 + q) / (1 - q) ^ 3 + 2 * q / (1 - q) =
      (24 * q * (1 + q) + 2 * q * (1 - q) ^ 2) / (1 - q) ^ 3 := by
    field_simp [hk.ne']
    ring
  rw [he]
  apply div_le_div_of_nonneg_right _ (pow_nonneg hk.le _)
  nlinarith

/-- Shell sum with a generic positive exponential rate. -/
def exponentialShellSum (c delta : ℝ) : ℝ :=
  ∑' n : ℕ, shellWeight n * Real.exp (-(c * delta * (n + 1 : ℝ)))

theorem exponential_shell_hasSum {c delta : ℝ} (hc : 0 < c) (hd : 0 < delta) :
    HasSum (fun n : ℕ => shellWeight n * Real.exp (-(c * delta * (n + 1 : ℝ))))
      (24 * Real.exp (-(c * delta)) * (1 + Real.exp (-(c * delta))) /
        (1 - Real.exp (-(c * delta))) ^ 3 +
      2 * Real.exp (-(c * delta)) / (1 - Real.exp (-(c * delta)))) := by
  have hq : Real.exp (-(c * delta)) < 1 := Real.exp_lt_one_iff.mpr (neg_neg_of_pos (mul_pos hc hd))
  convert shell_geometric_hasSum (Real.exp_pos _).le hq using 1
  ext n
  rw [← Real.exp_nat_mul]
  congr 2
  push_cast
  ring

theorem exponential_shell_summable {c delta : ℝ} (hc : 0 < c) (hd : 0 < delta) :
    Summable (fun n : ℕ => shellWeight n * Real.exp (-(c * delta * (n + 1 : ℝ)))) :=
  (exponential_shell_hasSum hc hd).summable

theorem exponential_shell_bound {c delta : ℝ} (hc : 0 < c) (hd : 0 < delta) :
    exponentialShellSum c delta ≤ 50 / (1 - Real.exp (-(c * delta))) ^ 3 := by
  have hq : Real.exp (-(c * delta)) < 1 := Real.exp_lt_one_iff.mpr (neg_neg_of_pos (mul_pos hc hd))
  have h := shell_geometric_le (Real.exp_pos (-(c * delta))).le hq
  have he : exponentialShellSum c delta =
      ∑' n : ℕ, shellWeight n * Real.exp (-(c * delta)) ^ (n + 1) := by
    apply tsum_congr
    intro n
    rw [← Real.exp_nat_mul]
    congr 2
    push_cast
    ring
  rw [he]
  exact h

/-- The mesh-independent constant is constructed, not assumed. -/
def shellUniformConstant (c : ℝ) : ℝ := 50 / (1 - Real.exp (-c)) ^ 3

theorem shellUniformConstant_pos {c : ℝ} (hc : 0 < c) :
    0 < shellUniformConstant c := by
  unfold shellUniformConstant
  exact div_pos (by norm_num) (pow_pos (sub_pos.mpr (Real.exp_lt_one_iff.mpr (by linarith))) _)

theorem exponential_shell_uniform {c delta : ℝ} (hc : 0 < c)
    (hd : 0 < delta) (hd1 : delta ≤ 1) :
    delta ^ 3 * exponentialShellSum c delta ≤ shellUniformConstant c := by
  have ha : 0 < 1 - Real.exp (-c) := sub_pos.mpr (Real.exp_lt_one_iff.mpr (by linarith))
  have hk : 0 < 1 - Real.exp (-(c * delta)) :=
    sub_pos.mpr (Real.exp_lt_one_iff.mpr (neg_neg_of_pos (mul_pos hc hd)))
  have hg := exponential_gap_lower c hd.le hd1
  have hpow : (delta * (1 - Real.exp (-c))) ^ 3 ≤
      (1 - Real.exp (-(c * delta))) ^ 3 := by gcongr
  calc
    _ ≤ delta ^ 3 * (50 / (1 - Real.exp (-(c * delta))) ^ 3) :=
      mul_le_mul_of_nonneg_left (exponential_shell_bound hc hd) (pow_nonneg hd.le _)
    _ ≤ delta ^ 3 * (50 / (delta * (1 - Real.exp (-c))) ^ 3) := by
      gcongr
    _ = shellUniformConstant c := by
      unfold shellUniformConstant
      field_simp [hd.ne', ha.ne']
      ring

/-- Source normalization: the rate is d/2. -/
theorem exponential_shell_uniform_half {d delta : ℝ} (hd : 0 < d)
    (hdelta : 0 < delta) (hdelta1 : delta ≤ 1) :
    delta ^ 3 * exponentialShellSum (d / 2) delta ≤ shellUniformConstant (d / 2) :=
  exponential_shell_uniform (half_pos hd) hdelta hdelta1

/-- The selected shells beyond the Euclidean-to-sup threshold of the source. -/
def exponentialShellTailTerm (d delta R : ℝ) (n : ℕ) : ℝ :=
  if R / (Real.sqrt 3 * delta) < (n + 1 : ℝ) then
    shellWeight n * Real.exp (-(d * delta * (n + 1 : ℝ))) else 0

def exponentialShellTail (d delta R : ℝ) : ℝ :=
  ∑' n : ℕ, exponentialShellTailTerm d delta R n

theorem exponential_tail_term_nonneg (d delta R : ℝ) (n : ℕ) :
    0 ≤ exponentialShellTailTerm d delta R n := by
  unfold exponentialShellTailTerm
  split_ifs
  · exact mul_nonneg (shellWeight_pos n).le (Real.exp_pos _).le
  · rfl

theorem exponential_tail_term_le {d delta R : ℝ} (hd : 0 < d)
    (hdelta : 0 < delta) (n : ℕ) :
    exponentialShellTailTerm d delta R n ≤
      Real.exp (-d * R / (2 * Real.sqrt 3)) *
        (shellWeight n * Real.exp (-((d / 2) * delta * (n + 1 : ℝ)))) := by
  have hs : 0 < Real.sqrt (3 : ℝ) := Real.sqrt_pos.mpr (by norm_num)
  unfold exponentialShellTailTerm
  split_ifs with hn
  · have hm : R / Real.sqrt 3 ≤ delta * (n + 1 : ℝ) := by
      apply (div_le_iff₀ hs).mpr
      have h := (div_lt_iff₀ (mul_pos hs hdelta)).mp hn
      nlinarith
    have hmul := mul_le_mul_of_nonneg_left hm (half_pos hd).le
    have hexp : Real.exp (-((d / 2) * delta * (n + 1 : ℝ))) ≤
        Real.exp (-d * R / (2 * Real.sqrt 3)) := by
      apply Real.exp_le_exp.mpr
      have he : -d * R / (2 * Real.sqrt 3) = -(d / 2 * (R / Real.sqrt 3)) := by ring
      rw [he]
      nlinarith
    calc
      _ = Real.exp (-((d / 2) * delta * (n + 1 : ℝ))) *
          (shellWeight n * Real.exp (-((d / 2) * delta * (n + 1 : ℝ)))) := by
        rw [mul_left_comm, mul_assoc, ← Real.exp_add]
        congr 2
        ring
      _ ≤ _ := mul_le_mul_of_nonneg_right hexp
        (mul_nonneg (shellWeight_pos n).le (Real.exp_pos _).le)
  · exact mul_nonneg (Real.exp_pos _).le
      (mul_nonneg (shellWeight_pos n).le (Real.exp_pos _).le)

theorem exponential_tail_summable {d delta R : ℝ} (hd : 0 < d) (hdelta : 0 < delta) :
    Summable (exponentialShellTailTerm d delta R) := by
  exact Summable.of_nonneg_of_le (exponential_tail_term_nonneg d delta R)
    (exponential_tail_term_le hd hdelta)
    ((exponential_shell_summable (half_pos hd) hdelta).mul_left _)

theorem exponential_tail_bound {d delta R : ℝ} (hd : 0 < d) (hdelta : 0 < delta) :
    exponentialShellTail d delta R ≤ Real.exp (-d * R / (2 * Real.sqrt 3)) *
      exponentialShellSum (d / 2) delta := by
  unfold exponentialShellTail exponentialShellSum
  rw [← tsum_mul_left]
  exact (exponential_tail_summable hd hdelta).tsum_le_tsum
    (exponential_tail_term_le hd hdelta)
    ((exponential_shell_summable (half_pos hd) hdelta).mul_left _)

/-- A uniform tail estimate, valid for every real threshold R and positive mesh at most one. -/
theorem exponential_tail_uniform {d delta R : ℝ} (hd : 0 < d)
    (hdelta : 0 < delta) (hdelta1 : delta ≤ 1) :
    delta ^ 3 * exponentialShellTail d delta R ≤
      shellUniformConstant (d / 2) * Real.exp (-d * R / (2 * Real.sqrt 3)) := by
  calc
    _ ≤ delta ^ 3 * (Real.exp (-d * R / (2 * Real.sqrt 3)) *
        exponentialShellSum (d / 2) delta) :=
      mul_le_mul_of_nonneg_left (exponential_tail_bound hd hdelta) (pow_nonneg hdelta.le _)
    _ = (delta ^ 3 * exponentialShellSum (d / 2) delta) *
        Real.exp (-d * R / (2 * Real.sqrt 3)) := by ring
    _ ≤ _ := mul_le_mul_of_nonneg_right
      (exponential_shell_uniform_half hd hdelta hdelta1) (Real.exp_pos _).le

/-- The mesh-independent majorant really tends to zero at the outer boundary. -/
theorem exponential_tail_majorant_tendsto {d : ℝ} (hd : 0 < d) :
    Tendsto (fun R : ℝ => shellUniformConstant (d / 2) *
      Real.exp (-d * R / (2 * Real.sqrt 3))) atTop (nhds 0) := by
  have hs : 0 < 2 * Real.sqrt (3 : ℝ) := by positivity
  have h := Real.tendsto_exp_atBot.comp
    ((tendsto_id.const_mul_atTop_of_neg (neg_neg_of_pos hd)).atBot_div_const hs)
  simpa using h.const_mul (shellUniformConstant (d / 2))

/-- The outer cutoff can be chosen once for every mesh in `(0,1]`. -/
theorem exponential_tails_uniformly_small {d epsilon : ℝ}
    (hd : 0 < d) (hepsilon : 0 < epsilon) :
    ∃ R0 : ℝ, 1 ≤ R0 ∧ ∀ R : ℝ, R0 ≤ R → ∀ delta : ℝ,
      0 < delta → delta ≤ 1 → delta ^ 3 * exponentialShellTail d delta R < epsilon := by
  obtain ⟨R0, hR0⟩ := eventually_atTop.1
    ((tendsto_order.1 (exponential_tail_majorant_tendsto hd)).2 epsilon hepsilon)
  refine ⟨max R0 1, le_max_right _ _, ?_⟩
  intro R hR delta hdelta hdelta1
  exact lt_of_le_of_lt (exponential_tail_uniform hd hdelta hdelta1)
    (hR0 R (le_trans (le_max_left _ _) hR))

#print axioms exponential_gap_lower
#print axioms square_geometric_hasSum
#print axioms shell_geometric_hasSum
#print axioms exponential_shell_summable
#print axioms exponential_shell_uniform
#print axioms exponential_shell_uniform_half
#print axioms exponential_tail_summable
#print axioms exponential_tail_uniform
#print axioms exponential_tail_majorant_tendsto
#print axioms exponential_tails_uniformly_small

end HMT.V.ThermodynamicLimit
