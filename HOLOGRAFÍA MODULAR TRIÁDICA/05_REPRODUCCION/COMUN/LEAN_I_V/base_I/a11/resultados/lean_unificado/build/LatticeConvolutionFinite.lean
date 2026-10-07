import LatticeNormalProduct

/-! Finite coefficient formula for the left-region contraction with the
already constructed normal product. The summation bound follows from the
lower bound of the second variable, not from a numerical truncation. -/
noncomputable section
namespace HMT.IV.LatticeConvolutionFinite
open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeExponentialContraction
open HMT.IV.LatticeTwoRegionFactor
open scoped BigOperators
variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem leftProduct_finite (p : ℤ) (h : BiStates V) (u a b : ℤ)
    (hu : ∀ a b, b < u → h a b = 0) :
    leftProduct p h a b =
      ∑ n ∈ Finset.range ((b-u).toNat+1),
        scalarContraction p n • h (a-p+(n:ℤ)) (b-(n:ℤ)) := by
  let e : ℕ ↪ ℤ := ⟨fun n => (n:ℤ), by intro a b h; exact Int.ofNat.inj h⟩
  let s := (Finset.range ((b-u).toNat+1)).map e
  have hs : Function.support (fun j : ℤ => leftKernel p j • h (a-p+j) (b-j)) ⊆ s := by
    intro j hj
    change leftKernel p j • h (a-p+j) (b-j) ≠ 0 at hj
    have hj0 : 0 ≤ j := by
      by_contra hn
      have hz : leftKernel p j = 0 := by simp [leftKernel,leftExpansion,hn]
      exact hj (by rw [hz,zero_smul])
    have hju : j ≤ b-u := by
      by_contra hn
      exact hj (by rw [hu _ _ (by omega),smul_zero])
    apply Finset.mem_map.mpr
    refine ⟨j.toNat,?_,?_⟩
    · simp only [Finset.mem_range]; omega
    · exact Int.toNat_of_nonneg hj0
  change (∑ᶠ j : ℤ, leftKernel p j • h (a-p+j) (b-j)) = _
  rw [finsum_eq_sum_of_support_subset _ hs]
  rw [Finset.sum_map]
  apply Finset.sum_congr rfl
  intro n _
  simp [e,leftKernel,leftExpansion]

end HMT.IV.LatticeConvolutionFinite
end

#print axioms HMT.IV.LatticeConvolutionFinite.leftProduct_finite
