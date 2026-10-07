import LatticeFactorConvolution
import LatticeNormalOrdering
import LatticeChargedVertexField

/-!
Common finite normal product, using the existing creation/annihilation modes,
integral pairing and lattice cocycle. Its two-variable lower bound is proved.
The expansion identities with the two compositions of chargedField remain a
separate bridge: this definition does not replace those existing fields.
-/
noncomputable section
namespace HMT.IV.LatticeNormalProduct
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeFactorConvolution
open scoped TensorProduct BigOperators

def normalFock (o : Fin 12) (x y : Lattice o) (N : ℕ) (v : Fock o) : BiStates (Fock o) :=
  fun a b => ∑ r ∈ Finset.range (N+1), ∑ s ∈ Finset.range (N+1),
    if 0 ≤ a+(r:ℤ) ∧ 0 ≤ b+(s:ℤ) then
      creationExponentialMode o x (a+(r:ℤ)).toNat
        (creationExponentialMode o y (b+(s:ℤ)).toNat
          (exponentialCoefficient o x r (exponentialCoefficient o y s v)))
    else 0

theorem normalFock_below (o : Fin 12) (x y : Lattice o) (N : ℕ) (v : Fock o)
    (a b : ℤ) (h : a < -(N:ℤ) ∨ b < -(N:ℤ)) : normalFock o x y N v a b = 0 := by
  unfold normalFock
  apply Finset.sum_eq_zero
  intro r hr
  apply Finset.sum_eq_zero
  intro s hs
  have hr' : r ≤ N := by simpa only [Finset.mem_range,Nat.lt_succ_iff] using hr
  have hs' : s ≤ N := by simpa only [Finset.mem_range,Nat.lt_succ_iff] using hs
  rw [if_neg (by omega)]

theorem normalFock_lowerBounded (o : Fin 12) (x y : Lattice o) (N : ℕ) (v : Fock o) :
    LowerBounded (normalFock o x y N v) :=
  ⟨-(N:ℤ),-(N:ℤ),fun a b h => normalFock_below o x y N v a b h⟩

def dressedNormal (o : Fin 12) (x y z : Lattice o) (N : ℕ) (v : Fock o) :
    BiStates (LatticeCarrier o) := fun a b =>
  (epsilon o x y * epsilon o (x+y) z) •
    (normalFock o x y N v (a-integerPair o x z) (b-integerPair o y z)
      ⊗ₜ[ℂ] basisElement o (x+y+z))

theorem dressedNormal_lowerBounded (o : Fin 12) (x y z : Lattice o) (N : ℕ) (v : Fock o) :
    LowerBounded (dressedNormal o x y z N v) := by
  refine ⟨integerPair o x z-(N:ℤ),integerPair o y z-(N:ℤ),?_⟩
  intro a b h
  unfold dressedNormal
  rw [normalFock_below o x y N v _ _ (by omega),TensorProduct.zero_tmul,smul_zero]

/-- A pairing-dependent power works for every charge sector and every finite
normal product on the original carrier. The charged-field bridge is not an
assumption of this lemma and is not claimed by its conclusion. -/
theorem normal_product_polynomial_cancellation (o : Fin 12) (x y : Lattice o) :
    ∃ n : ℕ, ∀ (z : Lattice o) (N : ℕ) (v : Fock o),
      (crossing^n) (leftProduct (integerPair o x y) (dressedNormal o x y z N v)) =
        (crossing^n) (rightProduct (integerPair o x y) (dressedNormal o x y z N v)) := by
  obtain ⟨n,hn⟩ := product_polynomial_cancellation
    (V := LatticeCarrier o) (integerPair o x y)
  exact ⟨n,fun z N v => hn _ (dressedNormal_lowerBounded o x y z N v)⟩

end HMT.IV.LatticeNormalProduct
end

#print axioms HMT.IV.LatticeNormalProduct.normalFock_below
#print axioms HMT.IV.LatticeNormalProduct.normalFock_lowerBounded
#print axioms HMT.IV.LatticeNormalProduct.dressedNormal_lowerBounded
#print axioms HMT.IV.LatticeNormalProduct.normal_product_polynomial_cancellation
