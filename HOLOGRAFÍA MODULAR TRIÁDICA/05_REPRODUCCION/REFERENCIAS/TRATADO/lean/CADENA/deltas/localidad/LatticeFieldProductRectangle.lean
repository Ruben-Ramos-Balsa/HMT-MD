import LatticeFieldProductCutoff
import LatticeAntidiagonalRectangle

/-!
Rectangular normal-order coefficients for the existing charged fields.
The coefficient cutoff and the antidiagonal identity have already been
proved; this module reindexes them and removes terms whose annihilator
is zero above the actual bound of the input state.
-/

noncomputable section
namespace HMT.IV.LatticeFieldProductRectangle

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeCreationExponential
open HMT.IV.LatticeAnnihilationExponential HMT.IV.LatticeExponentialContraction
open HMT.IV.LatticeAnnihilationCommutativity HMT.IV.LatticeOperatorCutoff
open HMT.IV.LatticeFieldProductCutoff HMT.IV.LatticeAntidiagonalRectangle
open HMT.IV.LatticeChargedVertexField
open scoped TensorProduct BigOperators

/-- A signed degree bound can be replaced by a larger uniform finite range. -/
theorem sum_integer_cutoff_extend {V : Type*} [AddCommMonoid V]
    (D B : ℤ) (f : ℕ → V) (hDB : D ≤ B) :
    (if 0 ≤ D then ∑ t ∈ Finset.range (D.toNat+1), f t else 0) =
      ∑ t ∈ Finset.range (B.toNat+1), if (t : ℤ) ≤ D then f t else 0 := by
  by_cases hD : 0 ≤ D
  · rw [if_pos hD]
    calc
      (∑ t ∈ Finset.range (D.toNat+1), f t) =
          ∑ t ∈ Finset.range (D.toNat+1), if (t : ℤ) ≤ D then f t else 0 := by
        apply Finset.sum_congr rfl
        intro t ht
        have ht' : t ≤ D.toNat := by
          simpa only [Finset.mem_range, Nat.lt_succ_iff] using ht
        rw [if_pos (by omega)]
      _ = ∑ t ∈ Finset.range (B.toNat+1), if (t : ℤ) ≤ D then f t else 0 := by
        apply Finset.sum_subset (Finset.range_mono (by omega))
        intro t _ ht
        have ht' : D.toNat < t := by
          simp only [Finset.mem_range] at ht
          omega
        rw [if_neg (by omega)]
  · rw [if_neg hD]
    symm
    apply Finset.sum_eq_zero
    intro t _
    rw [if_neg (by omega)]

theorem fieldCutoff_creation_rectangle (o : Fin 12) (x y z : Lattice o)
    (k : ℤ) (N d : ℕ) (v : Fock o)
    (hv : ∀ q, N < q → exponentialCoefficient o x q v = 0) :
    fieldCutoff o x z k (N+d) (creationExponentialMode o y d v) =
      epsilon o x z • ∑ t ∈ Finset.range (d+1), ∑ q ∈ Finset.range (N+1),
        if 0 ≤ k-integerPair o x z+((t+q : ℕ) : ℤ) then
          scalarContraction (integerPair o x y) t •
            (creationExponentialMode o x ((k-integerPair o x z+((t+q : ℕ) : ℤ)).toNat)
              (creationExponentialMode o y (d-t)
                (exponentialCoefficient o x q v)) ⊗ₜ[ℂ] basisElement o (x+z))
        else 0 := by
  rw [cutoff_creation_normal_order]
  congr 1
  let F : ℕ → ℕ → LatticeCarrier o := fun t q =>
    if 0 ≤ k-integerPair o x z+((t+q : ℕ) : ℤ) then
      scalarContraction (integerPair o x y) t •
        (creationExponentialMode o x ((k-integerPair o x z+((t+q : ℕ) : ℤ)).toNat)
          (creationExponentialMode o y (d-t)
            (exponentialCoefficient o x q v)) ⊗ₜ[ℂ] basisElement o (x+z))
    else 0
  calc
    _ = ∑ r ∈ Finset.range (N+d+1), ∑ p ∈ Finset.antidiagonal r,
        if p.1 ≤ d then F p.1 p.2 else 0 := by
      apply Finset.sum_congr rfl
      intro r _
      by_cases hk : 0 ≤ k-integerPair o x z+(r : ℤ)
      · rw [if_pos hk]
        apply Finset.sum_congr rfl
        intro p hp
        have hs := Finset.mem_antidiagonal.mp hp
        have hsi : (p.1 : ℤ)+(p.2 : ℤ) = (r : ℤ) := by exact_mod_cast hs
        dsimp [F]
        rw [hsi, if_pos hk]
      · rw [if_neg hk]
        symm
        apply Finset.sum_eq_zero
        intro p hp
        have hs := Finset.mem_antidiagonal.mp hp
        have hsi : (p.1 : ℤ)+(p.2 : ℤ) = (r : ℤ) := by exact_mod_cast hs
        dsimp [F]
        rw [hsi, if_neg hk]
        split_ifs <;> rfl
    _ = ∑ t ∈ Finset.range (d+1), ∑ q ∈ Finset.range (N+1), F t q := by
      apply sum_antidiagonal_rectangle N d F
      intro t q hq
      simp only [F, hv q hq, map_zero, TensorProduct.zero_tmul, smul_zero,
        ite_self]

/-- The product of the original fields, with all annihilation indices bounded by N. -/
theorem field_product_rectangle (o : Fin 12) (x y z : Lattice o)
    (k l : ℤ) (N : ℕ) (v : Fock o)
    (hx : ∀ q, N < q → exponentialCoefficient o x q v = 0)
    (hy : ∀ q, N < q → exponentialCoefficient o y q v = 0) :
    fieldCoefficient o x k
        (fieldCoefficient o y l (v ⊗ₜ[ℂ] basisElement o z)) =
      epsilon o y z • ∑ s ∈ Finset.range (N+1),
        if 0 ≤ l-integerPair o y z+(s : ℤ) then
          epsilon o x (y+z) •
            ∑ t ∈ Finset.range ((l-integerPair o y z+(s : ℤ)).toNat+1),
            ∑ q ∈ Finset.range (N+1),
              if 0 ≤ k-integerPair o x (y+z)+((t+q : ℕ) : ℤ) then
                scalarContraction (integerPair o x y) t •
                  (creationExponentialMode o x
                    ((k-integerPair o x (y+z)+((t+q : ℕ) : ℤ)).toNat)
                    (creationExponentialMode o y ((l-integerPair o y z+(s : ℤ)).toNat-t)
                      (exponentialCoefficient o x q (exponentialCoefficient o y s v)))
                    ⊗ₜ[ℂ] basisElement o (x+(y+z)))
              else 0
        else 0 := by
  rw [field_product_eq_nested_cutoff o x y z k l N v hx hy]
  congr 1
  apply Finset.sum_congr rfl
  intro s _
  split_ifs with hs
  · exact fieldCutoff_creation_rectangle o x y (y+z) k N _ _
      (cutoff_preserved_by_exponential o x y s N v hx)
  · rfl

end HMT.IV.LatticeFieldProductRectangle
end

#print axioms HMT.IV.LatticeFieldProductRectangle.fieldCutoff_creation_rectangle
#print axioms HMT.IV.LatticeFieldProductRectangle.field_product_rectangle
#print axioms HMT.IV.LatticeFieldProductRectangle.sum_integer_cutoff_extend
