import LatticeFactorConvolution

/-! Reversing the two expansion regions is a reindexation, with the sign
dictated by the integral lattice pairing. -/
noncomputable section
namespace HMT.IV.LatticeConvolutionSwap
open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeTwoRegionFactor
variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem rightProduct_swap (p : ℤ) (h : BiStates V) (a b : ℤ) :
    rightProduct p h a b =
      (-1:ℂ)^p • leftProduct p (fun a b => h b a) b a := by
  let e : ℤ ≃ ℤ :=
    ⟨fun j => p-j, fun j => p-j, by intro j; dsimp; omega, by intro j; dsimp; omega⟩
  unfold rightProduct leftProduct convolution
  rw [smul_finsum]
  rw [← finsum_comp_equiv e]
  apply finsum_congr
  intro j
  change rightKernel p (p-j) • h (a-p+(p-j)) (b-(p-j)) = _
  rw [show a-p+(p-j)=a-j by omega,show b-(p-j)=b-p+j by omega]
  unfold rightKernel leftKernel rightExpansion
  rw [show p-(p-j)=j by omega]
  exact mul_smul _ _ _

end HMT.IV.LatticeConvolutionSwap
end
#print axioms HMT.IV.LatticeConvolutionSwap.rightProduct_swap
