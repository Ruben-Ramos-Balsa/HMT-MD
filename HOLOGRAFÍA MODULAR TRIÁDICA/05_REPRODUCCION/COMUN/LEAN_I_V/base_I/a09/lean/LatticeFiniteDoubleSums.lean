import LatticeNormalOrderedField

/-! Pointwise finite double sums used by normal products. Bounds apply to
values on a fixed state, not to a global finite frequency cutoff. -/
noncomputable section
namespace HMT.IV.LatticeFiniteDoubleSums
open scoped BigOperators

theorem finsum_eq_range {V : Type*} [AddCommMonoid V]
    (f : ℕ → V) (N : ℕ) (h : ∀ a ≥ N, f a = 0) :
    (∑ᶠ a, f a) = ∑ a ∈ Finset.range N, f a := by
  apply finsum_eq_sum_of_support_subset
  intro a ha
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra hn
  exact ha (h a (by omega))

theorem finite_support_of_bound {V : Type*} [Zero V]
    (f : ℕ → V) (N : ℕ) (h : ∀ a ≥ N, f a = 0) :
    (Function.support f).Finite := by
  apply (Finset.range N).finite_toSet.subset
  intro a ha
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra hn
  exact ha (h a (by omega))

theorem finsum_comm_of_rectangle {V : Type*} [AddCommMonoid V]
    (f : ℕ → ℕ → V) (N M : ℕ)
    (hN : ∀ a ≥ N, ∀ b, f a b = 0)
    (hM : ∀ b ≥ M, ∀ a, f a b = 0) :
    (∑ᶠ a, ∑ᶠ b, f a b) = ∑ᶠ b, ∑ᶠ a, f a b := by
  classical
  have hr : ∀ a, (∑ᶠ b, f a b) = ∑ b ∈ Finset.range M, f a b :=
    fun a => finsum_eq_range _ M (fun b hb => hM b hb a)
  have hc : ∀ b, (∑ᶠ a, f a b) = ∑ a ∈ Finset.range N, f a b :=
    fun b => finsum_eq_range _ N (fun a ha => hN a ha b)
  simp only [hr, hc]
  rw [finsum_eq_range _ N (by
    intro a ha
    simp only [hN a ha, Finset.sum_const_zero])]
  rw [finsum_eq_range _ M (by
    intro b hb
    simp only [hM b hb, Finset.sum_const_zero])]
  exact Finset.sum_comm

theorem finite_support_row_sums {V : Type*} [AddCommMonoid V]
    (f : ℕ → ℕ → V) (N : ℕ) (h : ∀ a ≥ N, ∀ b, f a b = 0) :
    (Function.support (fun a => ∑ᶠ b, f a b)).Finite := by
  apply finite_support_of_bound _ N
  intro a ha
  simp only [h a ha, finsum_zero]

end HMT.IV.LatticeFiniteDoubleSums
end

#print axioms HMT.IV.LatticeFiniteDoubleSums.finsum_comm_of_rectangle
