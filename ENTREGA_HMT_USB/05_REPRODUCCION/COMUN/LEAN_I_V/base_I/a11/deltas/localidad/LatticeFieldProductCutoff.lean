import LatticeFieldCutoff
import LatticeOperatorCutoff

/-!
Finite coefficient expansion of the product of the two existing charged
fields. The outer cutoff follows from operator commutation and normal
ordering; neither the field nor its product is defined by this formula.
-/

noncomputable section
namespace HMT.IV.LatticeFieldProductCutoff

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeAnnihilationCommutativity
open HMT.IV.LatticeWeightFiltration HMT.IV.LatticeFieldCutoff
open HMT.IV.LatticeOperatorCutoff
open HMT.IV.LatticeNormalOrdering HMT.IV.LatticeExponentialContraction
open scoped TensorProduct BigOperators

/-- Exact normal ordering within a finite field coefficient. -/
theorem cutoff_creation_normal_order (o : Fin 12) (x y z : Lattice o)
    (k : ℤ) (M d : ℕ) (v : Fock o) :
    fieldCutoff o x z k M (creationExponentialMode o y d v) =
      epsilon o x z • ∑ r ∈ Finset.range (M+1),
        if 0 ≤ k-integerPair o x z+(r : ℤ) then
          ∑ p ∈ Finset.antidiagonal r,
            if p.1 ≤ d then
              scalarContraction (integerPair o x y) p.1 •
                (creationExponentialMode o x ((k-integerPair o x z+(r : ℤ)).toNat)
                  (creationExponentialMode o y (d-p.1)
                    (exponentialCoefficient o x p.2 v)) ⊗ₜ[ℂ]
                    basisElement o (x+z))
            else 0
        else 0 := by
  unfold fieldCutoff
  congr 1
  apply Finset.sum_congr rfl
  intro r _
  split_ifs with hr
  · have he := congrArg (fun E : Module.End ℂ (Fock o) => E v)
      (exponential_normal_order_coefficient o x y r d)
    simp only [Module.End.mul_apply, LinearMap.sum_apply, LinearMap.smul_apply] at he
    rw [he, map_sum, TensorProduct.sum_tmul]
    apply Finset.sum_congr rfl
    intro p _
    split_ifs with hp
    · simp only [if_pos hp, Module.End.mul_apply, map_smul,
        ← TensorProduct.smul_tmul']
    · simp only [if_neg hp, LinearMap.zero_apply, smul_zero, map_zero,
        TensorProduct.zero_tmul]
  · rfl

/-- Product expansion on any Fock state with an actual common annihilation cutoff. -/
theorem field_product_eq_nested_cutoff (o : Fin 12) (x y z : Lattice o)
    (k l : ℤ) (N : ℕ) (v : Fock o)
    (hx : ∀ r, N < r → exponentialCoefficient o x r v = 0)
    (hy : ∀ r, N < r → exponentialCoefficient o y r v = 0) :
    fieldCoefficient o x k
        (fieldCoefficient o y l (v ⊗ₜ[ℂ] basisElement o z)) =
      epsilon o y z • ∑ j ∈ Finset.range (N+1),
        if 0 ≤ l-integerPair o y z+(j : ℤ) then
          fieldCutoff o x (y+z) k (N+(l-integerPair o y z+(j : ℤ)).toNat)
            (creationExponentialMode o y ((l-integerPair o y z+(j : ℤ)).toNat)
              (exponentialCoefficient o y j v))
        else 0 := by
  rw [fieldCoefficient_eq_of_annihilation_cutoff o y z l N v hy]
  unfold fieldCutoff
  rw [map_smul, map_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  split_ifs with hj
  · exact fieldCoefficient_eq_of_annihilation_cutoff o x (y+z) k
      (N+(l-integerPair o y z+(j : ℤ)).toNat)
      (creationExponentialMode o y ((l-integerPair o y z+(j : ℤ)).toNat)
        (exponentialCoefficient o y j v))
      (cutoff_after_creation o x y _ N _
        (cutoff_preserved_by_exponential o x y j N v hx))
  · exact map_zero _

/-- The weight bound of the incoming state supplies both cutoffs. -/
theorem field_product_on_filtration (o : Fin 12) (x y z : Lattice o)
    (k l : ℤ) (N : ℕ) (v : Fock o) (hv : v ∈ weightAtMost o N) :
    fieldCoefficient o x k
        (fieldCoefficient o y l (v ⊗ₜ[ℂ] basisElement o z)) =
      epsilon o y z • ∑ j ∈ Finset.range (N+1),
        if 0 ≤ l-integerPair o y z+(j : ℤ) then
          fieldCutoff o x (y+z) k (N+(l-integerPair o y z+(j : ℤ)).toNat)
            (creationExponentialMode o y ((l-integerPair o y z+(j : ℤ)).toNat)
              (exponentialCoefficient o y j v))
        else 0 :=
  field_product_eq_nested_cutoff o x y z k l N v
    (fun r hr => annihilation_cutoff_on_filtration o x N r hr v hv)
    (fun r hr => annihilation_cutoff_on_filtration o y N r hr v hv)

end HMT.IV.LatticeFieldProductCutoff
end

#print axioms HMT.IV.LatticeFieldProductCutoff.field_product_eq_nested_cutoff
#print axioms HMT.IV.LatticeFieldProductCutoff.field_product_on_filtration
#print axioms HMT.IV.LatticeFieldProductCutoff.cutoff_creation_normal_order
