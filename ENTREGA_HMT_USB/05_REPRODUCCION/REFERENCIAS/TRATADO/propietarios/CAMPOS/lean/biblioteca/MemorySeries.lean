import MemoryResolvent

/-!
# Forced memory series and the manuscript's reader tail

All convergence is proved from a contractive transport and bounded increments.
The event bound is parametrized first and then specialized to nine.  No data
are forgotten by reducing the sequence to its final value in a cycle.
-/

noncomputable section

namespace HMT.II.Memory

open scoped BigOperators

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [NormedSpace 𝕜 E]

/-- Accumulated moving-frame memory, with arbitrary preserved initial history. -/
def record (R : E →L[𝕜] E) (η : ℕ → E) (y₀ : E) : ℕ → E
  | 0 => y₀
  | n + 1 => R (record R η y₀ n) + η n

@[simp] theorem record_zero (R : E →L[𝕜] E) (η : ℕ → E) (y₀ : E) :
    record R η y₀ 0 = y₀ := rfl

@[simp] theorem record_succ (R : E →L[𝕜] E) (η : ℕ → E) (y₀ : E) (n : ℕ) :
    record R η y₀ (n + 1) = R (record R η y₀ n) + η n := rfl

theorem norm_record_le (R : E →L[𝕜] E) (hR : ‖R‖ ≤ 1)
    (η : ℕ → E) (K : ℝ) (hη : ∀ n, ‖η n‖ ≤ K) (y₀ : E) (n : ℕ) :
    ‖record R η y₀ n‖ ≤ ‖y₀‖ + K * n := by
  induction n with
  | zero => simp
  | succ n ih =>
    calc
      ‖record R η y₀ (n + 1)‖ ≤ ‖R (record R η y₀ n)‖ + ‖η n‖ := norm_add_le _ _
      _ ≤ ‖R‖ * ‖record R η y₀ n‖ + K := add_le_add (R.le_opNorm _) (hη n)
      _ ≤ ‖record R η y₀ n‖ + K := by nlinarith [norm_nonneg (record R η y₀ n)]
      _ ≤ ‖y₀‖ + K * (n + 1 : ℕ) := by push_cast; linarith

/-- Closed form for the scalar majorant, proved from convergent geometric sums. -/
theorem hasSum_growth_majorant (r M K : ℝ) (hr₀ : 0 ≤ r) (hr : r < 1) :
    HasSum (fun n : ℕ => (M + K * n) * r ^ n)
      (M / (1 - r) + K * r / (1 - r) ^ 2) := by
  have hg := (hasSum_geometric_of_lt_one hr₀ hr).mul_left M
  have hn := (hasSum_coe_mul_geometric_of_norm_lt_one
    (show ‖r‖ < 1 by simpa only [Real.norm_eq_abs, abs_of_nonneg hr₀] using hr)).mul_left K
  convert hg.add hn using 1 <;> first | (ext n; ring) | ring

/-- Shifted majorant; `N` is the first omitted index, not the last retained one. -/
theorem hasSum_growth_tail (r M K : ℝ) (hr₀ : 0 ≤ r) (hr : r < 1) (N : ℕ) :
    HasSum (fun n : ℕ => (M + K * (n + N : ℕ)) * r ^ (n + N))
      (r ^ N * ((M + K * N) / (1 - r) + K * r / (1 - r) ^ 2)) := by
  convert (hasSum_growth_majorant r (M + K * N) K hr₀ hr).mul_left (r ^ N) using 1
  ext n
  push_cast
  rw [pow_add]
  ring

/-- Absolute convergence derived from linear growth, throughout the open unit disk. -/
theorem summable_weighted_of_growth [CompleteSpace E] (y : ℕ → E)
    (M K : ℝ) (hy : ∀ n, ‖y n‖ ≤ M + K * n)
    (u : 𝕜) (hu : ‖u‖ < 1) : Summable (fun n => u ^ n • y n) := by
  apply (hasSum_growth_majorant ‖u‖ M K (norm_nonneg _) hu).summable.of_norm_bounded
  intro n
  rw [norm_smul, norm_pow]
  simpa only [mul_comm] using mul_le_mul_of_nonneg_left (hy n) (pow_nonneg (norm_nonneg u) n)

/-- Vector series, not a scalar-only model. -/
def memorySeries (R : E →L[𝕜] E) (η : ℕ → E) (y₀ : E) (u : 𝕜) : E :=
  ∑' n : ℕ, u ^ n • record R η y₀ n

def forcingSeries (η : ℕ → E) (u : 𝕜) : E := ∑' n : ℕ, u ^ n • η n

variable [CompleteSpace E]

theorem memory_summable (R : E →L[𝕜] E) (hR : ‖R‖ ≤ 1)
    (η : ℕ → E) (K : ℝ) (hη : ∀ n, ‖η n‖ ≤ K) (y₀ : E)
    (u : 𝕜) (hu : ‖u‖ < 1) : Summable (fun n => u ^ n • record R η y₀ n) :=
  summable_weighted_of_growth _ ‖y₀‖ K (norm_record_le R hR η K hη y₀) u hu

theorem forcing_summable (η : ℕ → E) (K : ℝ) (hη : ∀ n, ‖η n‖ ≤ K)
    (u : 𝕜) (hu : ‖u‖ < 1) : Summable (fun n => u ^ n • η n) :=
  summable_weighted_of_growth η K 0 (by simpa using hη) u hu

/-- Analytic version of `mem:serie`, obtained by summing the actual recurrence. -/
theorem memorySeries_eq_resolvent (R : E →L[𝕜] E) (hR : ‖R‖ ≤ 1)
    (η : ℕ → E) (K : ℝ) (hη : ∀ n, ‖η n‖ ≤ K) (y₀ : E)
    (u : 𝕜) (hu : ‖u‖ < 1) :
    memorySeries R η y₀ u = resolvent R u (y₀ + u • forcingSeries η u) := by
  have hY := (memory_summable R hR η K hη y₀ u hu).hasSum
  have hH := (forcing_summable η K hη u hu).hasSum
  have ht : HasSum (fun n : ℕ => u ^ (n + 1) • record R η y₀ (n + 1))
      (u • R (memorySeries R η y₀ u) + u • forcingSeries η u) := by
    convert (hY.mapL (u • R)).add (hH.const_smul u) using 1
    ext n
    simp only [record_succ, smul_add, pow_succ, mul_smul,
      ContinuousLinearMap.smul_apply, map_smul]
    rw [smul_comm u (u ^ n)]
  have ht' := (hasSum_nat_add_iff' 1).mpr hY
  have heq := ht'.unique ht
  simp only [Finset.sum_range_one, pow_zero, one_smul, record_zero] at heq
  apply (solve_iff R u (contractive_domain R hR u hu) _ _).mp
  change memorySeries R η y₀ u - u • R (memorySeries R η y₀ u) = _
  change memorySeries R η y₀ u - y₀ = _ at heq
  rw [sub_eq_iff_eq_add] at heq ⊢
  conv_lhs => rw [heq]
  abel

omit [CompleteSpace E] in
/-- Exact `mem:cota`, with `N+1` the first omitted term and event bound nine.
The scalar field may be real or complex. The original real absolute value is
its scalar norm. The bound is independent of `u` throughout `‖u‖ ≤ r`. -/
theorem reader_tail_bound (R : E →L[𝕜] E) (hR : ‖R‖ ≤ 1)
    (η : ℕ → E) (hη : ∀ n, ‖η n‖ ≤ 9) (y₀ : E) (ℓ : E →L[𝕜] 𝕜)
    (r : ℝ) (hr₀ : 0 < r) (hr : r < 1) (u : 𝕜) (hu : ‖u‖ ≤ r) (N : ℕ) :
    ‖∑' n : ℕ, u ^ (n + (N + 1)) • ℓ (record R η y₀ (n + (N + 1)))‖ ≤
      ‖ℓ‖ * r ^ (N + 1) *
        ((‖y₀‖ + 9 * (N + 1 : ℕ)) / (1 - r) + 9 * r / (1 - r) ^ 2) := by
  apply (tsum_of_norm_bounded
    ((hasSum_growth_tail r ‖y₀‖ 9 hr₀.le hr (N + 1)).mul_left ‖ℓ‖) ?_).trans_eq
    (by ring)
  intro n
  rw [norm_smul, norm_pow]
  calc
    ‖u‖ ^ (n + (N + 1)) * ‖ℓ (record R η y₀ (n + (N + 1)))‖ ≤
        r ^ (n + (N + 1)) * (‖ℓ‖ * (‖y₀‖ + 9 * (n + (N + 1) : ℕ))) := by
      gcongr
      exact (ℓ.le_opNorm _).trans (mul_le_mul_of_nonneg_left
        (norm_record_le R hR η 9 hη y₀ _) (norm_nonneg ℓ))
    _ = _ := by ring

#print axioms norm_record_le
#print axioms memorySeries_eq_resolvent
#print axioms reader_tail_bound

end HMT.II.Memory
