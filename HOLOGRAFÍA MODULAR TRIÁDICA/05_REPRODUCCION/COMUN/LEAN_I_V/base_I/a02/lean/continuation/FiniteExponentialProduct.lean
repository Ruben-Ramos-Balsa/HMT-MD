import ScalarFactorBinomial
import FiniteAntidiagonalSum
import Mathlib.RingTheory.PowerSeries.Order
import Mathlib.Data.Nat.Choose.Sum

/-! Finite coefficient formulas for products of formal exponentials.
The coefficient ring need not be commutative. -/
namespace HMT.Formal.FiniteExponentialProduct

open PowerSeries
open scoped BigOperators

noncomputable section
variable {A : Type*} [Ring A] [Algebra ℂ A]

def expCoeff_fin (s : PowerSeries A) (n : ℕ) : A :=
  ∑ k ∈ Finset.range (n + 1),
    coeff ℂ k (PowerSeries.exp ℂ) • coeff A n (s ^ k)

def expPartial (s : PowerSeries A) (n : ℕ) : PowerSeries A :=
  ∑ k ∈ Finset.range (n + 1), coeff ℂ k (PowerSeries.exp ℂ) • s ^ k

omit [Algebra ℂ A] in
theorem pow_order_lower (s : PowerSeries A) (hs : constantCoeff A s = 0)
    (k : ℕ) : (k : ℕ∞) ≤ order (s ^ k) := by
  have hs1 : (1 : ℕ∞) ≤ order s := by
    apply nat_le_order s 1
    intro i hi
    have : i = 0 := by omega
    simpa [this] using hs
  induction k with
  | zero => simp
  | succ k ih =>
    calc
      ((k + 1 : ℕ) : ℕ∞) = (k : ℕ∞) + 1 := by simp
      _ ≤ order (s ^ k) + order s := add_le_add ih hs1
      _ ≤ order (s ^ (k + 1)) := by
        simpa [pow_succ] using le_order_mul (s ^ k) s

omit [Algebra ℂ A] in
theorem coeff_pow_zero_of_lt (s : PowerSeries A) (hs : constantCoeff A s = 0)
    (n k : ℕ) (hnk : n < k) : coeff A n (s ^ k) = 0 := by
  apply coeff_of_lt_order
  exact lt_of_lt_of_le (by exact_mod_cast hnk) (pow_order_lower s hs k)

omit [Algebra ℂ A] in
theorem coeff_pow_mul_zero_of_lt (a b : PowerSeries A)
    (ha : constantCoeff A a = 0) (hb : constantCoeff A b = 0)
    (n i j : ℕ) (h : n < i + j) : coeff A n (a ^ i * b ^ j) = 0 := by
  apply coeff_of_lt_order
  have hle : ((i + j : ℕ) : ℕ∞) ≤ order (a ^ i * b ^ j) := by
    calc
      ((i + j : ℕ) : ℕ∞) = (i : ℕ∞) + (j : ℕ∞) := by simp
      _ ≤ order (a ^ i) + order (b ^ j) :=
        add_le_add (pow_order_lower a ha i) (pow_order_lower b hb j)
      _ ≤ order (a ^ i * b ^ j) := le_order_mul _ _
  exact lt_of_lt_of_le (by exact_mod_cast h) hle

theorem coeff_expPartial_self (s : PowerSeries A) (n : ℕ) :
    coeff A n (expPartial s n) = expCoeff_fin s n := by
  simp [expPartial, expCoeff_fin]

theorem coeff_expPartial (s : PowerSeries A) (hs : constantCoeff A s = 0)
    (n N : ℕ) (hn : n ≤ N) :
    coeff A n (expPartial s N) = expCoeff_fin s n := by
  simp only [expPartial, expCoeff_fin, map_sum, coeff_smul]
  symm
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro k _ hk
  have hnk : n < k := by simpa using hk
  rw [coeff_pow_zero_of_lt s hs n k hnk, smul_zero]

theorem expCoeff_fin_add_triangular (a b : PowerSeries A) (hab : Commute a b)
    (n : ℕ) :
    expCoeff_fin (a + b) n =
      ∑ k ∈ Finset.range (n + 1), ∑ p ∈ Finset.antidiagonal k,
        (coeff ℂ p.1 (PowerSeries.exp ℂ) * coeff ℂ p.2 (PowerSeries.exp ℂ)) •
          coeff A n (a ^ p.1 * b ^ p.2) := by
  unfold expCoeff_fin
  apply Finset.sum_congr rfl
  intro k _
  rw [hab.add_pow']
  simp only [map_sum, map_nsmul, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro p hp
  have hpSum : p.1 + p.2 = k := Finset.mem_antidiagonal.mp hp
  have hchoose := ScalarFactorBinomial.exponential_coefficient_add_choose p.1 p.2
  rw [hpSum] at hchoose
  rw [← hchoose]
  simp only [mul_smul]
  congr 1
  simp only [Nat.cast_smul_eq_nsmul]

theorem coeff_expPartial_mul (a b : PowerSeries A) (n N : ℕ) :
    coeff A n (expPartial a N * expPartial b N) =
      ∑ i ∈ Finset.range (N + 1), ∑ j ∈ Finset.range (N + 1),
        (coeff ℂ i (PowerSeries.exp ℂ) * coeff ℂ j (PowerSeries.exp ℂ)) •
          coeff A n (a ^ i * b ^ j) := by
  simp only [expPartial, Finset.sum_mul, Finset.mul_sum, map_sum,
    smul_mul_smul_comm, coeff_smul]
  rw [Finset.sum_comm]

theorem expCoeff_fin_add (a b : PowerSeries A)
    (ha : constantCoeff A a = 0) (hb : constantCoeff A b = 0)
    (hab : Commute a b) (n : ℕ) :
    expCoeff_fin (a + b) n =
      ∑ p ∈ Finset.antidiagonal n, expCoeff_fin a p.1 * expCoeff_fin b p.2 := by
  calc
    expCoeff_fin (a + b) n = coeff A n (expPartial a n * expPartial b n) := by
      rw [expCoeff_fin_add_triangular a b hab, coeff_expPartial_mul]
      apply FiniteAntidiagonalSum.sum_antidiagonals_eq_sum_square
      intro p hp
      rw [coeff_pow_mul_zero_of_lt a b ha hb n p.1 p.2 hp, smul_zero]
    _ = _ := by
      rw [coeff_mul]
      apply Finset.sum_congr rfl
      intro p hp
      have hpSum : p.1 + p.2 = n := Finset.mem_antidiagonal.mp hp
      rw [coeff_expPartial a ha p.1 n (by omega),
        coeff_expPartial b hb p.2 n (by omega)]

theorem expCoeff_fin_add_eq_coeff_mul (a b : PowerSeries A)
    (ha : constantCoeff A a = 0) (hb : constantCoeff A b = 0)
    (hab : Commute a b) (n : ℕ) :
    expCoeff_fin (a + b) n =
      coeff A n (mk (expCoeff_fin a) * mk (expCoeff_fin b)) := by
  rw [coeff_mul]
  simpa only [coeff_mk] using expCoeff_fin_add a b ha hb hab n

end
end HMT.Formal.FiniteExponentialProduct

#print axioms HMT.Formal.FiniteExponentialProduct.expCoeff_fin_add
#print axioms HMT.Formal.FiniteExponentialProduct.expCoeff_fin_add_eq_coeff_mul
