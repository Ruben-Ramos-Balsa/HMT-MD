import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Topology.Algebra.InfiniteSum.Module
import Mathlib.Tactic

/-!
# Analytic memory resolvent (Article II)

The series is constructed in the Banach algebra of continuous endomorphisms,
not postulated as an inverse.  Its convergence domain is `‖u‖ * ‖D‖ < 1`.
For a contractive transport this contains the manuscript's disk `‖u‖ < 1`.
The parameter counts windows of nine transitions; it is not rescaled here.
-/

noncomputable section

namespace HMT.II.Memory

open scoped BigOperators

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
  [NormedSpace 𝕜 E] [CompleteSpace E]

/-- The operator-valued Neumann series; no inverse is used in its definition. -/
def resolvent (D : E →L[𝕜] E) (u : 𝕜) : E →L[𝕜] E :=
  ∑' n : ℕ, (u • D) ^ n

theorem hasSum_resolvent (D : E →L[𝕜] E) (u : 𝕜)
    (hu : ‖u‖ * ‖D‖ < 1) :
    HasSum (fun n : ℕ => (u • D) ^ n) (resolvent D u) :=
  (summable_geometric_of_norm_lt_one (by simpa only [norm_smul] using hu)).hasSum

omit [CompleteSpace E] in
/-- The manuscript writes each term as `u^n D^n`. -/
theorem resolvent_eq_weighted_powers (D : E →L[𝕜] E) (u : 𝕜) :
    resolvent D u = ∑' n : ℕ, u ^ n • D ^ n := by
  simp only [resolvent, smul_pow]

theorem resolvent_mul_one_sub (D : E →L[𝕜] E) (u : 𝕜)
    (hu : ‖u‖ * ‖D‖ < 1) :
    resolvent D u * (1 - u • D) = 1 :=
  geom_series_mul_neg _ (by simpa only [norm_smul] using hu)

theorem one_sub_mul_resolvent (D : E →L[𝕜] E) (u : 𝕜)
    (hu : ‖u‖ * ‖D‖ < 1) :
    (1 - u • D) * resolvent D u = 1 :=
  mul_neg_geom_series _ (by simpa only [norm_smul] using hu)

/-- Both inverse laws needed by the additive Schur reduction are consequences. -/
theorem resolvent_bilateral (D : E →L[𝕜] E) (u : 𝕜)
    (hu : ‖u‖ * ‖D‖ < 1) :
    (∀ x : E, resolvent D u ((1 - u • D) x) = x) ∧
    (∀ x : E, (1 - u • D) (resolvent D u x) = x) := by
  constructor
  · intro x
    have h := congrArg (fun T : E →L[𝕜] E => T x) (resolvent_mul_one_sub D u hu)
    simpa using h
  · intro x
    have h := congrArg (fun T : E →L[𝕜] E => T x) (one_sub_mul_resolvent D u hu)
    simpa using h

theorem solve_iff (D : E →L[𝕜] E) (u : 𝕜) (hu : ‖u‖ * ‖D‖ < 1)
    (x b : E) : (1 - u • D) x = b ↔ x = resolvent D u b := by
  obtain ⟨hl, hr⟩ := resolvent_bilateral D u hu
  constructor
  · intro h
    rw [← hl x, h]
  · rintro rfl
    exact hr b

omit [CompleteSpace E] in
theorem contractive_domain (D : E →L[𝕜] E) (hD : ‖D‖ ≤ 1)
    (u : 𝕜) (hu : ‖u‖ < 1) : ‖u‖ * ‖D‖ < 1 :=
  lt_of_le_of_lt (by nlinarith [norm_nonneg u]) hu

omit [CompleteSpace E] in
theorem norm_resolvent_le (D : E →L[𝕜] E) (u : 𝕜)
    (hu : ‖u‖ * ‖D‖ < 1) :
    ‖resolvent D u‖ ≤ 1 / (1 - ‖u‖ * ‖D‖) := by
  have h := tsum_geometric_le_of_norm_lt_one (u • D)
    (by simpa only [norm_smul] using hu)
  have hI : ‖(1 : E →L[𝕜] E)‖ ≤ 1 := ContinuousLinearMap.norm_id_le
  simp only [norm_smul] at h
  change ‖resolvent D u‖ ≤ _ at h
  rw [one_div]
  linarith

/-- Exact remainder after the terms indexed by `0,...,N-1`. -/
theorem resolvent_sub_partialSum (D : E →L[𝕜] E) (u : 𝕜)
    (hu : ‖u‖ * ‖D‖ < 1) (N : ℕ) :
    resolvent D u - ∑ n ∈ Finset.range N, (u • D) ^ n =
      (u • D) ^ N * resolvent D u := by
  have hs := (hasSum_resolvent D u hu).summable
  have h := hs.sum_add_tsum_nat_add N
  have ht : (∑' n : ℕ, (u • D) ^ (n + N)) =
      (u • D) ^ N * resolvent D u := by
    simp_rw [Nat.add_comm _ N, pow_add]
    exact hs.tsum_mul_left _
  rw [ht] at h
  exact sub_eq_iff_eq_add.mpr (by simpa [add_comm, resolvent] using h.symm)

/-- Operator norm tail bound; valid also for `N=0` and `u=0`. -/
theorem norm_resolvent_tail_le (D : E →L[𝕜] E) (u : 𝕜)
    (hu : ‖u‖ * ‖D‖ < 1) (N : ℕ) :
    ‖resolvent D u - ∑ n ∈ Finset.range N, (u • D) ^ n‖ ≤
      (‖u‖ * ‖D‖) ^ N / (1 - ‖u‖ * ‖D‖) := by
  rw [resolvent_sub_partialSum D u hu N]
  have hpow : ‖(u • D) ^ N‖ ≤ (‖u‖ * ‖D‖) ^ N := by
    induction N with
    | zero => simpa using (ContinuousLinearMap.norm_id_le (𝕜 := 𝕜) (E := E))
    | succ n ih =>
      calc
        ‖(u • D) ^ (n + 1)‖ ≤ ‖(u • D) ^ n‖ * ‖u • D‖ := by
          rw [pow_succ]; exact norm_mul_le _ _
        _ ≤ (‖u‖ * ‖D‖) ^ n * (‖u‖ * ‖D‖) := by
          rw [norm_smul]; gcongr
        _ = (‖u‖ * ‖D‖) ^ (n + 1) := (pow_succ _ _).symm
  calc
    ‖(u • D) ^ N * resolvent D u‖ ≤ ‖(u • D) ^ N‖ * ‖resolvent D u‖ :=
      norm_mul_le _ _
    _ ≤ (‖u‖ * ‖D‖) ^ N * (1 / (1 - ‖u‖ * ‖D‖)) := by
      gcongr
      exact norm_resolvent_le D u hu
    _ = _ := by ring

#print axioms hasSum_resolvent
#print axioms resolvent_bilateral
#print axioms norm_resolvent_tail_le

end HMT.II.Memory
