import Mathlib

/-!
# Normalized regional renewal, coefficients and analytic realization

The first continuation weight is `D`.  This is the declared normalization in
`revision_planck.tex`, not something inferred from the selector cardinality 169.
The coefficient recurrence is the literal coefficient form of
`R(z) = D z^7 + D z R(z)` and is solved uniquely before summing its realization.
-/

noncomputable section

namespace HMT.II.ActionReturn

open scoped BigOperators

/-- Coefficientwise form of the manuscript's normalized renewal equation. -/
def IsRenewal (D : ℝ) (r : ℕ → ℝ) : Prop :=
  r 0 = 0 ∧ ∀ n, r (n + 1) = (if n + 1 = 7 then D else 0) + D * r n

/-- Coefficients produced by the renewal rule, not by evaluating a rational formula. -/
def renewalCoefficient (D : ℝ) : ℕ → ℝ
  | 0 => 0
  | n + 1 => (if n + 1 = 7 then D else 0) + D * renewalCoefficient D n

theorem renewalCoefficient_isRenewal (D : ℝ) : IsRenewal D (renewalCoefficient D) :=
  ⟨rfl, fun _ => rfl⟩

theorem renewal_unique (D : ℝ) {r : ℕ → ℝ} (hr : IsRenewal D r) :
    r = renewalCoefficient D := by
  funext n
  induction n with
  | zero => exact hr.1
  | succ n ih => rw [hr.2, renewalCoefficient, ih]

theorem renewalCoefficient_low (D : ℝ) (n : ℕ) (hn : n < 7) :
    renewalCoefficient D n = 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [renewalCoefficient, if_neg (by omega), ih (by omega)]
    ring

theorem renewalCoefficient_seven (D : ℝ) : renewalCoefficient D 7 = D := by
  rw [renewalCoefficient, if_pos rfl, renewalCoefficient_low D 6 (by omega)]
  ring

theorem renewalCoefficient_shift (D : ℝ) (n : ℕ) :
    renewalCoefficient D (n + 7) = D ^ (n + 1) := by
  induction n with
  | zero => simpa using renewalCoefficient_seven D
  | succ n ih =>
    rw [show n + 1 + 7 = (n + 7) + 1 by omega, renewalCoefficient,
      if_neg (by omega), ih]
    simp only [zero_add, pow_succ]
    ring

/-- Uniqueness includes the order-seven zero coefficients and normalized leading term. -/
theorem normalized_renewal_iff (D : ℝ) (r : ℕ → ℝ) :
    IsRenewal D r ↔
      (∀ n < 7, r n = 0) ∧ (∀ n, r (n + 7) = D ^ (n + 1)) := by
  constructor
  · intro h
    rw [renewal_unique D h]
    exact ⟨renewalCoefficient_low D, renewalCoefficient_shift D⟩
  · rintro ⟨hlow, hhigh⟩
    have heq : r = renewalCoefficient D := by
      funext n
      by_cases hn : n < 7
      · rw [hlow n hn, renewalCoefficient_low D n hn]
      · obtain ⟨m, rfl⟩ : ∃ m, n = m + 7 := ⟨n - 7, by omega⟩
        rw [hhigh, renewalCoefficient_shift]
    rw [heq]
    exact renewalCoefficient_isRenewal D

/-- The order-six selector and normalized strict continuations are kept distinct. -/
def regionalCoefficient (D : ℝ) (n : ℕ) : ℝ :=
  (if n = 6 then 169 else 0) + renewalCoefficient D n

theorem regionalCoefficient_six (D : ℝ) : regionalCoefficient D 6 = 169 := by
  simp [regionalCoefficient, renewalCoefficient_low D 6 (by omega)]

theorem regionalCoefficient_shift (D : ℝ) (n : ℕ) :
    regionalCoefficient D (n + 7) = D ^ (n + 1) := by
  simp [regionalCoefficient, show n + 7 ≠ 6 by omega, renewalCoefficient_shift]

/-- Analytic realization sums the generated coefficients, with zero terms omitted. -/
def renewalValue (D z : ℝ) : ℝ :=
  ∑' n : ℕ, renewalCoefficient D (n + 7) * z ^ (n + 7)

theorem renewal_hasSum (D z : ℝ) (h : |D * z| < 1) :
    HasSum (fun n : ℕ => renewalCoefficient D (n + 7) * z ^ (n + 7))
      (D * z ^ 7 / (1 - D * z)) := by
  convert (hasSum_geometric_of_abs_lt_one h).mul_left (D * z ^ 7) using 1
  · ext n
    rw [renewalCoefficient_shift, pow_succ, pow_add, mul_pow]
    ring

theorem renewalValue_eq (D z : ℝ) (h : |D * z| < 1) :
    renewalValue D z = D * z ^ 7 / (1 - D * z) :=
  (renewal_hasSum D z h).tsum_eq

theorem renewal_absolutely_summable (D z : ℝ) (h : |D * z| < 1) :
    Summable (fun n : ℕ => ‖renewalCoefficient D (n + 7) * z ^ (n + 7)‖) :=
  summable_norm_iff.mpr (renewal_hasSum D z h).summable

theorem renewal_analytic_equation (D z : ℝ) (h : |D * z| < 1) :
    renewalValue D z = D * z ^ 7 + D * z * renewalValue D z := by
  rw [renewalValue_eq D z h]
  have hden : 1 - D * z ≠ 0 := by
    have := (abs_lt.mp h).2
    linarith
  field_simp [hden]
  ring

/-- Exact tail after retaining indices zero through `N`, inclusively. -/
theorem renewal_tail_hasSum (D z : ℝ) (h : |D * z| < 1) (N : ℕ) :
    HasSum
      (fun n : ℕ => renewalCoefficient D (n + (N + 1) + 7) *
        z ^ (n + (N + 1) + 7))
      (D ^ (N + 2) * z ^ (N + 8) / (1 - D * z)) := by
  convert (hasSum_geometric_of_abs_lt_one h).mul_left
    (D ^ (N + 2) * z ^ (N + 8)) using 1
  · ext n
    rw [renewalCoefficient_shift]
    simp only [show n + (N + 1) + 1 = n + (N + 2) by omega,
      show n + (N + 1) + 7 = n + (N + 8) by omega, pow_add, mul_pow]
    ring

theorem renewal_remainder_exact (D z : ℝ) (h : |D * z| < 1) (N : ℕ) :
    renewalValue D z -
        ∑ n ∈ Finset.range (N + 1), renewalCoefficient D (n + 7) * z ^ (n + 7) =
      D ^ (N + 2) * z ^ (N + 8) / (1 - D * z) := by
  have hs := (renewal_hasSum D z h).summable.sum_add_tsum_nat_add (N + 1)
  rw [(renewal_tail_hasSum D z h N).tsum_eq] at hs
  change _ = renewalValue D z at hs
  linarith

/-- The selector term is not part of the recurrence normalization. -/
def regionalValue (D z : ℝ) : ℝ := 169 * z ^ 6 + renewalValue D z

theorem regionalValue_eq (D z : ℝ) (h : |D * z| < 1) :
    regionalValue D z = 169 * z ^ 6 + D * z ^ 7 / (1 - D * z) := by
  rw [regionalValue, renewalValue_eq D z h]

#print axioms renewal_unique
#print axioms normalized_renewal_iff
#print axioms renewal_hasSum
#print axioms renewal_absolutely_summable
#print axioms renewal_analytic_equation
#print axioms renewal_remainder_exact
#print axioms regionalValue_eq

end HMT.II.ActionReturn
