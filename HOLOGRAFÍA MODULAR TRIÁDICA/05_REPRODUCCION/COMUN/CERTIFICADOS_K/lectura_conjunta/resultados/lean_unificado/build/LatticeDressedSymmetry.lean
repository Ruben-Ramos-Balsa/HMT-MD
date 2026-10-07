import LatticeNormalSymmetry
import LatticeProductCocycle
import LatticeConvolutionSwap

/-!
Interchanging the two charges in the dressed normal product produces exactly
the sign of their integral pairing. The sign is derived from the constructed
lattice cocycle, not supplied as an additional field relation.
-/

noncomputable section
namespace HMT.IV.LatticeDressedSymmetry

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeNormalProduct
open HMT.IV.LatticeNormalSymmetry HMT.IV.LatticeProductCocycle
open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeConvolutionSwap
open scoped TensorProduct BigOperators

theorem dressedNormal_swap (o : Fin 12) (x y z : Lattice o) (N : ℕ)
    (v : Fock o) (a b : ℤ) :
    dressedNormal o y x z N v b a =
      (-1 : ℂ) ^ integerPair o x y • dressedNormal o x y z N v a b := by
  unfold dressedNormal
  rw [epsilon_reverse o x y, add_comm y x,
    normalFock_swap o y x N v]
  rw [mul_assoc, mul_smul]

/-- The right-region convolution becomes the left-region convolution after
interchanging both charges and both formal coordinates. Its scalar sign is
exactly the cocycle sign already proved above. -/
theorem rightProduct_dressed_swap (o : Fin 12) (x y z : Lattice o) (N : ℕ)
    (v : Fock o) (a b : ℤ) :
    rightProduct (integerPair o x y) (dressedNormal o x y z N v) a b =
      leftProduct (integerPair o x y) (dressedNormal o y x z N v) b a := by
  letI : NoZeroSMulDivisors ℂ (LatticeCarrier o) :=
    GroupWithZero.toNoZeroSMulDivisors
  rw [rightProduct_swap]
  unfold leftProduct convolution
  rw [smul_finsum]
  apply finsum_congr
  intro j
  rw [dressedNormal_swap]
  exact smul_comm _ _ _

end HMT.IV.LatticeDressedSymmetry
end

#print axioms HMT.IV.LatticeDressedSymmetry.dressedNormal_swap
#print axioms HMT.IV.LatticeDressedSymmetry.rightProduct_dressed_swap
