import HalfModeScalarFactor

/-!
A coefficient bridge from the independently recurrence-defined exponential
to its finite factorial-power expansion. Only formal power series occur here.
-/

namespace HMT.Formal.FormalExpCoefficientBridge

open PowerSeries
open HalfModeScalarFactor
open scoped BigOperators

noncomputable section

def expPartial (s : Series) (N : ℕ) : Series :=
  ∑ k ∈ Finset.range (N + 1), coeff ℂ k (PowerSeries.exp ℂ) • s ^ k

theorem coeff_pow_zero_of_lt (s : Series) (hs : constantCoeff ℂ s = 0)
    (n k : ℕ) (hnk : n < k) : coeff ℂ n (s ^ k) = 0 := by
  exact (X_pow_dvd_iff.mp (pow_dvd_pow_of_dvd (X_dvd_iff.mpr hs) k)) n hnk

theorem coeff_exp_succ_mul (k : ℕ) :
    coeff ℂ (k + 1) (PowerSeries.exp ℂ) * (k + 1) =
      coeff ℂ k (PowerSeries.exp ℂ) := by
  rw [← coeff_derivative, derivative_mathlib_exp]

theorem derivative_exp_term (s : Series) (k : ℕ) :
    derivative ℂ (coeff ℂ (k + 1) (PowerSeries.exp ℂ) • s ^ (k + 1)) =
      derivative ℂ s * (coeff ℂ k (PowerSeries.exp ℂ) • s ^ k) := by
  rw [Derivation.map_smul, Derivation.leibniz_pow, Nat.add_sub_cancel]
  simp only [smul_eq_mul, nsmul_eq_mul, smul_eq_C_mul]
  have hc : C ℂ (coeff ℂ (k + 1) (PowerSeries.exp ℂ)) * (k + 1) =
      C ℂ (coeff ℂ k (PowerSeries.exp ℂ)) := by
    rw [← map_natCast (C ℂ), ← map_one (C ℂ), ← map_add, ← map_mul]
    exact congrArg (C ℂ) (coeff_exp_succ_mul k)
  push_cast
  linear_combination s ^ k * derivative ℂ s * hc

theorem derivative_expPartial_succ (s : Series) (N : ℕ) :
    derivative ℂ (expPartial s (N + 1)) = derivative ℂ s * expPartial s N := by
  simp only [expPartial, map_sum, Finset.mul_sum]
  rw [Finset.sum_range_succ']
  rw [show derivative ℂ (coeff ℂ 0 (PowerSeries.exp ℂ) • s ^ 0) = 0 by
    simp [coeff_exp]]
  rw [add_zero]
  apply Finset.sum_congr rfl
  intro k _
  exact derivative_exp_term s k

theorem coeff_expPartial_stable (s : Series) (hs : constantCoeff ℂ s = 0)
    (n N : ℕ) (hnN : n ≤ N) :
    coeff ℂ n (expPartial s N) = coeff ℂ n (expPartial s n) := by
  simp only [expPartial, map_sum, coeff_smul, smul_eq_mul]
  symm
  apply Finset.sum_subset (Finset.range_mono (Nat.add_le_add_right hnN 1))
  intro k _ hkn
  rw [coeff_pow_zero_of_lt s hs n k (by simp only [Finset.mem_range] at hkn; omega),
    mul_zero]

theorem coeff_formalExp_eq_expPartial (s : Series) (hs : constantCoeff ℂ s = 0)
    (n : ℕ) : coeff ℂ n (formalExp s) = coeff ℂ n (expPartial s n) := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    cases n with
    | zero => simp [expPartial, coeff_exp, expCoeff]
    | succ n =>
      apply mul_right_cancel₀ (show (n + 1 : ℂ) ≠ 0 by exact_mod_cast Nat.succ_ne_zero n)
      rw [← coeff_derivative, ← coeff_derivative, formalExp_derivative,
        derivative_expPartial_succ]
      simp only [coeff_mul, Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
      apply Finset.sum_congr rfl
      intro k _
      rw [ih (n - k) (by omega), coeff_expPartial_stable s hs (n - k) n (by omega)]

/-- Every coefficient of the recurrence-defined normalized exponential is
the finite factorial-weighted sum of powers of its zero-constant argument. -/
theorem coeff_formalExp_eq_sum (s : Series) (hs : constantCoeff ℂ s = 0) (n : ℕ) :
    coeff ℂ n (formalExp s) =
      ∑ k ∈ Finset.range (n + 1),
        coeff ℂ k (PowerSeries.exp ℂ) * coeff ℂ n (s ^ k) := by
  rw [coeff_formalExp_eq_expPartial s hs n]
  simp only [expPartial, map_sum, coeff_smul, smul_eq_mul]

end

end HMT.Formal.FormalExpCoefficientBridge
