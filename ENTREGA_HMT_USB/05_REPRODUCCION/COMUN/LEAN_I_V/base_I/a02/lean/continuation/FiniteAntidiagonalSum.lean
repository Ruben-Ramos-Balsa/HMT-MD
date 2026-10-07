import Mathlib.Algebra.BigOperators.NatAntidiagonal
import Mathlib.Algebra.BigOperators.Group.Finset.Sigma
import Mathlib.Tactic

/-! Finite triangular support converts sums of antidiagonals to square sums. -/

namespace HMT.Formal.FiniteAntidiagonalSum

open scoped BigOperators

theorem sum_antidiagonals_eq_sum_square {B : Type*} [AddCommMonoid B]
    (f : ℕ × ℕ → B) (n : ℕ)
    (h : ∀ p : ℕ × ℕ, n < p.1 + p.2 → f p = 0) :
    (∑ k ∈ Finset.range (n + 1), ∑ p ∈ Finset.antidiagonal k, f p) =
      ∑ i ∈ Finset.range (n + 1), ∑ j ∈ Finset.range (n + 1), f (i, j) := by
  classical
  let square := (Finset.range (n + 1)) ×ˢ (Finset.range (n + 1))
  let triangle := square.filter fun p : ℕ × ℕ => p.1 + p.2 ≤ n
  have htriangle :
      (∑ k ∈ Finset.range (n + 1), ∑ p ∈ Finset.antidiagonal k, f p) =
        ∑ p ∈ triangle, f p := by
    rw [Finset.sum_sigma']
    apply Finset.sum_bij (fun p _ => p.2)
    · intro p hp
      rcases Finset.mem_sigma.mp hp with ⟨hk, hp⟩
      have hk' := Finset.mem_range.mp hk
      have hp' := Finset.mem_antidiagonal.mp hp
      simp only [triangle, square, Finset.mem_filter, Finset.mem_product,
        Finset.mem_range]
      omega
    · intro p hp q hq hpq
      have hp' := Finset.mem_antidiagonal.mp (Finset.mem_sigma.mp hp).2
      have hq' := Finset.mem_antidiagonal.mp (Finset.mem_sigma.mp hq).2
      have hpq' : p.1 = q.1 := by rw [← hp', ← hq', hpq]
      cases p
      cases q
      simp_all
    · intro p hp
      have hp' : p.1 + p.2 ≤ n := (Finset.mem_filter.mp hp).2
      refine ⟨⟨p.1 + p.2, p⟩, ?_, rfl⟩
      simp only [Finset.mem_sigma, Finset.mem_range, Finset.mem_antidiagonal]
      exact ⟨by omega, trivial⟩
    · intro _ _
      rfl
  rw [htriangle, ← Finset.sum_product]
  apply Finset.sum_subset (Finset.filter_subset _ _)
  intro p hp hpt
  apply h
  have : ¬ p.1 + p.2 ≤ n := by
    intro hle
    exact hpt (Finset.mem_filter.mpr ⟨hp, hle⟩)
  omega

end HMT.Formal.FiniteAntidiagonalSum
