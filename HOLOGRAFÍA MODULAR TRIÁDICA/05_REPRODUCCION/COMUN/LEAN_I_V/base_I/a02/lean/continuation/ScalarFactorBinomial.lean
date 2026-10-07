import HalfModeScalarFactor

/-! Factorial coefficients used to collect the finite normal-order sums. -/
namespace HMT.Formal.ScalarFactorBinomial
open PowerSeries
open scoped BigOperators

theorem exponential_coefficient_choose (k l : ℕ) (h : l ≤ k) :
    coeff ℂ k (PowerSeries.exp ℂ) * (k.choose l : ℂ) =
      coeff ℂ l (PowerSeries.exp ℂ) * coeff ℂ (k-l) (PowerSeries.exp ℂ) := by
  have hf : (k.choose l : ℂ) * (l.factorial : ℂ) * ((k-l).factorial : ℂ) =
      (k.factorial : ℂ) := by exact_mod_cast Nat.choose_mul_factorial_mul_factorial h
  have hk : (k.factorial : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero k
  have hl : (l.factorial : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero l
  have hd : ((k-l).factorial : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero (k-l)
  simp only [coeff_exp]
  push_cast
  field_simp
  linear_combination hf

theorem exponential_coefficient_add_choose (l t : ℕ) :
    coeff ℂ (l+t) (PowerSeries.exp ℂ) * ((l+t).choose l : ℂ) =
      coeff ℂ l (PowerSeries.exp ℂ) * coeff ℂ t (PowerSeries.exp ℂ) := by
  simpa using exponential_coefficient_choose (l+t) l (by omega)

end HMT.Formal.ScalarFactorBinomial

#print axioms HMT.Formal.ScalarFactorBinomial.exponential_coefficient_choose
#print axioms HMT.Formal.ScalarFactorBinomial.exponential_coefficient_add_choose
