import LatticeConvolutionFinite

/-! Explicit finite coefficients of the existing two-variable normal product.
The range of contraction indices is derived from its lower bound. -/
noncomputable section
namespace HMT.IV.LatticeNormalCoefficients
open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeConvolutionFinite
open HMT.IV.LatticeNormalProduct HMT.IV.LatticeExponentialContraction
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open scoped TensorProduct BigOperators

theorem leftProduct_dressed_finite (o : Fin 12) (x y z : Lattice o)
    (N : ℕ) (v : Fock o) (k l : ℤ) :
    leftProduct (integerPair o x y) (dressedNormal o x y z N v) k l =
      (epsilon o x y * epsilon o (x+y) z) •
        ∑ t ∈ Finset.range ((l-integerPair o y z+(N:ℤ)).toNat+1),
        ∑ r ∈ Finset.range (N+1), ∑ s ∈ Finset.range (N+1),
          if 0 ≤ k-integerPair o x y+(t:ℤ)-integerPair o x z+(r:ℤ) ∧
             0 ≤ l-(t:ℤ)-integerPair o y z+(s:ℤ) then
            scalarContraction (integerPair o x y) t •
              (creationExponentialMode o x
                ((k-integerPair o x y+(t:ℤ)-integerPair o x z+(r:ℤ)).toNat)
                (creationExponentialMode o y
                  ((l-(t:ℤ)-integerPair o y z+(s:ℤ)).toNat)
                  (exponentialCoefficient o x r (exponentialCoefficient o y s v)))
                ⊗ₜ[ℂ] basisElement o (x+y+z))
          else 0 := by
  have hb : ∀ a b, b < integerPair o y z-(N:ℤ) →
      dressedNormal o x y z N v a b = 0 := by
    intro a b h
    unfold dressedNormal
    rw [normalFock_below o x y N v _ _ (Or.inr (by omega)),
      TensorProduct.zero_tmul,smul_zero]
  rw [leftProduct_finite _ _ (integerPair o y z-(N:ℤ)) _ _ hb]
  rw [show l-(integerPair o y z-(N:ℤ))=l-integerPair o y z+(N:ℤ) by omega]
  simp only [dressedNormal,normalFock,TensorProduct.sum_tmul,Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro t _
  apply Finset.sum_congr rfl
  intro r _
  apply Finset.sum_congr rfl
  intro s _
  split_ifs
  · exact smul_comm _ _ _
  · simp

end HMT.IV.LatticeNormalCoefficients
end
#print axioms HMT.IV.LatticeNormalCoefficients.leftProduct_dressed_finite
