import Mathlib

/-!
A finite reindexing used for the existing normal-order coefficient sums.
Only additivity and the declared vanishing beyond the second-coordinate
cutoff are needed. The ambient antidiagonal index is recovered as t+q.
-/

namespace HMT.IV.LatticeAntidiagonalRectangle

open scoped BigOperators

theorem sum_antidiagonal_rectangle {V : Type*} [AddCommMonoid V]
    (N d : ℕ) (f : ℕ → ℕ → V)
    (hf : ∀ t q, N < q → f t q = 0) :
    (∑ r ∈ Finset.range (N+d+1),
      ∑ p ∈ Finset.antidiagonal r, if p.1 ≤ d then f p.1 p.2 else 0) =
      ∑ t ∈ Finset.range (d+1), ∑ q ∈ Finset.range (N+1), f t q := by
  classical
  rw [Finset.sum_sigma', ← Finset.sum_product']
  apply Finset.sum_bij_ne_zero (fun a _ _ => a.2)
  · intro a _ ha
    have ht : a.2.1 ≤ d := by
      by_contra ht
      simp [ht] at ha
    have hq : a.2.2 ≤ N := by
      by_contra hq
      have hz := hf a.2.1 a.2.2 (by omega)
      simp [ht, hz] at ha
    exact Finset.mem_product.mpr
      ⟨Finset.mem_range.mpr (by omega), Finset.mem_range.mpr (by omega)⟩
  · intro a ha _ b hb _ hab
    obtain ⟨r, p⟩ := a
    obtain ⟨s, q⟩ := b
    dsimp only at hab
    have hr := Finset.mem_antidiagonal.mp (Finset.mem_sigma.mp ha).2
    have hs := Finset.mem_antidiagonal.mp (Finset.mem_sigma.mp hb).2
    dsimp only at hr hs
    have hrs : r = s := by rw [← hr, ← hs, hab]
    cases hrs
    cases hab
    rfl
  · intro b hb hfb
    obtain ⟨ht, hq⟩ := Finset.mem_product.mp hb
    have ht' : b.1 ≤ d := by simpa only [Finset.mem_range, Nat.lt_succ_iff] using ht
    have hq' : b.2 ≤ N := by simpa only [Finset.mem_range, Nat.lt_succ_iff] using hq
    refine ⟨⟨b.1+b.2, b⟩, ?_, ?_, rfl⟩
    · exact Finset.mem_sigma.mpr
        ⟨Finset.mem_range.mpr (by change b.1 + b.2 < N+d+1; omega),
          Finset.mem_antidiagonal.mpr rfl⟩
    · simpa only [ht', if_pos] using hfb
  · intro a _ ha
    have ht : a.2.1 ≤ d := by
      by_contra ht
      simp [ht] at ha
    exact if_pos ht

end HMT.IV.LatticeAntidiagonalRectangle

#print axioms HMT.IV.LatticeAntidiagonalRectangle.sum_antidiagonal_rectangle
