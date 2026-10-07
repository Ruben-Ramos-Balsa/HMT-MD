import LatticeFieldProductRectangle
import LatticeNormalCoefficients
import LatticeProductCocycle

/-! Identification of the normal-product expansion with the composition of
the original charged fields. The annihilation bound is derived in the caller
from the weight filtration; it is not an equality postulated for the fields. -/
noncomputable section
namespace HMT.IV.LatticeFieldNormalBridge
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialContraction HMT.IV.LatticeChargedVertexField
open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeNormalProduct
open HMT.IV.LatticeNormalCoefficients HMT.IV.LatticeProductCocycle
open HMT.IV.LatticeFieldProductRectangle
open scoped TensorProduct BigOperators

theorem field_product_eq_leftProduct (o : Fin 12) (x y z : Lattice o)
    (k l : ℤ) (N : ℕ) (v : Fock o)
    (hx : ∀ q, N < q → exponentialCoefficient o x q v = 0)
    (hy : ∀ q, N < q → exponentialCoefficient o y q v = 0) :
    fieldCoefficient o x k (fieldCoefficient o y l (v ⊗ₜ[ℂ] basisElement o z)) =
      leftProduct (integerPair o x y) (dressedNormal o x y z N v) k l := by
  let B : ℤ := l-integerPair o y z+(N:ℤ)
  let F : ℕ → ℕ → ℕ → LatticeCarrier o := fun s t r =>
    if 0 ≤ k-integerPair o x y+(t:ℤ)-integerPair o x z+(r:ℤ) ∧
       0 ≤ l-(t:ℤ)-integerPair o y z+(s:ℤ) then
      scalarContraction (integerPair o x y) t •
        (creationExponentialMode o x
          ((k-integerPair o x y+(t:ℤ)-integerPair o x z+(r:ℤ)).toNat)
          (creationExponentialMode o y
            ((l-(t:ℤ)-integerPair o y z+(s:ℤ)).toNat)
            (exponentialCoefficient o x r (exponentialCoefficient o y s v)))
          ⊗ₜ[ℂ] basisElement o (x+y+z))
    else 0
  rw [field_product_rectangle o x y z k l N v hx hy,
    leftProduct_dressed_finite,← product_cocycle_left,mul_smul]
  change epsilon o y z • _ = epsilon o y z •
    (epsilon o x (y+z) • ∑ t ∈ Finset.range (B.toNat+1),
      ∑ r ∈ Finset.range (N+1), ∑ s ∈ Finset.range (N+1), F s t r)
  congr 1
  have hs : ∀ s ∈ Finset.range (N+1),
      (if 0 ≤ l-integerPair o y z+(s:ℤ) then
        epsilon o x (y+z) •
          ∑ t ∈ Finset.range ((l-integerPair o y z+(s:ℤ)).toNat+1),
          ∑ r ∈ Finset.range (N+1),
            if 0 ≤ k-integerPair o x (y+z)+((t+r:ℕ):ℤ) then
              scalarContraction (integerPair o x y) t •
                (creationExponentialMode o x
                  ((k-integerPair o x (y+z)+((t+r:ℕ):ℤ)).toNat)
                  (creationExponentialMode o y
                    ((l-integerPair o y z+(s:ℤ)).toNat-t)
                    (exponentialCoefficient o x r (exponentialCoefficient o y s v)))
                  ⊗ₜ[ℂ] basisElement o (x+(y+z)))
            else 0
      else 0) = epsilon o x (y+z) •
        ∑ t ∈ Finset.range (B.toNat+1), ∑ r ∈ Finset.range (N+1), F s t r := by
    intro s hs
    have hsN : s ≤ N := by simpa only [Finset.mem_range,Nat.lt_succ_iff] using hs
    let D : ℤ := l-integerPair o y z+(s:ℤ)
    let G : ℕ → ℕ → LatticeCarrier o := fun t r =>
      if 0 ≤ k-integerPair o x (y+z)+((t+r:ℕ):ℤ) then
        scalarContraction (integerPair o x y) t •
          (creationExponentialMode o x
            ((k-integerPair o x (y+z)+((t+r:ℕ):ℤ)).toNat)
            (creationExponentialMode o y (D.toNat-t)
              (exponentialCoefficient o x r (exponentialCoefficient o y s v)))
            ⊗ₜ[ℂ] basisElement o (x+(y+z)))
      else 0
    change (if 0 ≤ D then epsilon o x (y+z) •
      ∑ t ∈ Finset.range (D.toNat+1), ∑ r ∈ Finset.range (N+1), G t r else 0) = _
    have hi : (if 0 ≤ D then epsilon o x (y+z) •
        ∑ t ∈ Finset.range (D.toNat+1), ∑ r ∈ Finset.range (N+1), G t r else 0) =
      epsilon o x (y+z) • (if 0 ≤ D then
        ∑ t ∈ Finset.range (D.toNat+1), ∑ r ∈ Finset.range (N+1), G t r else 0) := by
      split_ifs <;> simp
    rw [hi,sum_integer_cutoff_extend D B _ (by dsimp [D,B]; omega)]
    congr 1
    apply Finset.sum_congr rfl
    intro t _
    by_cases ht : (t:ℤ) ≤ D
    · rw [if_pos ht]
      apply Finset.sum_congr rfl
      intro r _
      have ha : k-integerPair o x (y+z)+((t+r:ℕ):ℤ) =
          k-integerPair o x y+(t:ℤ)-integerPair o x z+(r:ℤ) := by
        rw [integerPair_add_right]; push_cast; omega
      have hb : 0 ≤ l-(t:ℤ)-integerPair o y z+(s:ℤ) := by dsimp [D] at ht; omega
      have hd : D.toNat-t=(l-(t:ℤ)-integerPair o y z+(s:ℤ)).toNat := by
        dsimp [D] at *; omega
      simp only [G,F,ha,hd,add_assoc,and_true,hb]
    · rw [if_neg ht]
      symm
      apply Finset.sum_eq_zero
      intro r _
      have hb : ¬0 ≤ l-(t:ℤ)-integerPair o y z+(s:ℤ) := by dsimp [D] at ht; omega
      simp [F,hb]
  calc
    _ = ∑ s ∈ Finset.range (N+1), epsilon o x (y+z) •
        ∑ t ∈ Finset.range (B.toNat+1), ∑ r ∈ Finset.range (N+1), F s t r := by
      exact Finset.sum_congr rfl hs
    _ = _ := by
      rw [← Finset.smul_sum]
      congr 1
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro t _
      exact Finset.sum_comm

end HMT.IV.LatticeFieldNormalBridge
end
#print axioms HMT.IV.LatticeFieldNormalBridge.field_product_eq_leftProduct
