import LatticeCreationExponential
import LatticeAnnihilationExponential
import LatticeAnnihilationEnergy
import LatticeFockMonomialParity
import Mathlib.Algebra.Vertex.VertexOperator

/-!
Charged lattice fields on the existing oscillator/twisted-lattice carrier.
The coefficients compose the constructed creation and annihilation
exponentials, the integral pairing and the constructed sign cocycle.
Pointwise Laurent truncation follows on the actual monomial basis and then
on its linear span. This is not an assertion of Jacobi, a complete VOA,
the twisted sector, an orbifold product or the FLM theorem.
-/

noncomputable section
namespace HMT.IV.LatticeChargedVertexField

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeAnnihilationEnergy
open scoped TensorProduct BigOperators

def basisCoefficientCutoff (o : Fin 12) (x : Lattice o) (k : ℤ) (N : ℕ)
    (a : Occupation o) (y : Lattice o) : LatticeCarrier o :=
  epsilon o x y • ∑ j ∈ Finset.range (N+1),
    if 0 ≤ k-integerPair o x y+(j : ℤ) then
      creationExponentialMode o x ((k-integerPair o x y+(j : ℤ)).toNat)
        (exponentialCoefficient o x j (monomialBasis o a)) ⊗ₜ[ℂ]
          basisElement o (x+y)
    else 0

def basisCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ)
    (a : Occupation o) (y : Lattice o) : LatticeCarrier o :=
  basisCoefficientCutoff o x k (occupationWeight o a) a y

theorem basisCoefficientCutoff_stable (o : Fin 12) (x : Lattice o) (k : ℤ)
    (a : Occupation o) (y : Lattice o) (N : ℕ)
    (hN : occupationWeight o a ≤ N) :
    basisCoefficient o x k a y = basisCoefficientCutoff o x k N a y := by
  unfold basisCoefficient basisCoefficientCutoff
  congr 1
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro j _ hj
  have hlt : occupationWeight o a < j := by
    simp only [Finset.mem_range] at hj
    omega
  have hz := annihilationCoefficient_cutoff_on_monomial o x j a hlt
  split_ifs
  · rw [hz, map_zero, TensorProduct.zero_tmul]
  · rfl

def fieldCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    Module.End ℂ (LatticeCarrier o) :=
  (carrierBasis o).constr ℂ (fun p => basisCoefficient o x k p.1 p.2)

@[simp] theorem fieldCoefficient_basis (o : Fin 12) (x : Lattice o) (k : ℤ)
    (a : Occupation o) (y : Lattice o) :
    fieldCoefficient o x k (carrierBasis o (a,y)) = basisCoefficient o x k a y :=
  Basis.constr_basis _ _ _ _

theorem basisCoefficient_below (o : Fin 12) (x y : Lattice o)
    (a : Occupation o) (k : ℤ)
    (hk : k < integerPair o x y - (occupationWeight o a : ℤ)) :
    basisCoefficient o x k a y = 0 := by
  unfold basisCoefficient basisCoefficientCutoff
  have hz : (∑ j ∈ Finset.range (occupationWeight o a+1),
      if 0 ≤ k-integerPair o x y+(j : ℤ) then
        creationExponentialMode o x ((k-integerPair o x y+(j : ℤ)).toNat)
          (exponentialCoefficient o x j (monomialBasis o a)) ⊗ₜ[ℂ]
            basisElement o (x+y)
      else 0) = 0 := by
    apply Finset.sum_eq_zero
    intro j hj
    have hj' : j ≤ occupationWeight o a := by
      simpa only [Finset.mem_range, Nat.lt_succ_iff] using hj
    rw [if_neg (by omega)]
  rw [hz, smul_zero]

theorem fieldCoefficient_basis_below (o : Fin 12) (x y : Lattice o)
    (a : Occupation o) (k : ℤ)
    (hk : k < integerPair o x y - (occupationWeight o a : ℤ)) :
    fieldCoefficient o x k (carrierBasis o (a,y)) = 0 := by
  rw [fieldCoefficient_basis]
  exact basisCoefficient_below o x y a k hk

/-- Laurent lower-boundedness is stable under the algebraic operations
of the existing carrier, so the basis bound controls every state. -/
def boundedStates (o : Fin 12) (x : Lattice o) : Submodule ℂ (LatticeCarrier o) where
  carrier := {v | ∃ b : ℤ, ∀ k < b, fieldCoefficient o x k v = 0}
  zero_mem' := ⟨0, by intros; exact map_zero _⟩
  add_mem' := by
    rintro v w ⟨b,hb⟩ ⟨c,hc⟩
    refine ⟨min b c, ?_⟩
    intro k hk
    rw [map_add, hb k (lt_of_lt_of_le hk (min_le_left _ _)),
      hc k (lt_of_lt_of_le hk (min_le_right _ _)), add_zero]
  smul_mem' := by
    rintro r v ⟨b,hb⟩
    refine ⟨b, ?_⟩
    intro k hk
    rw [map_smul, hb k hk, smul_zero]

theorem boundedStates_eq_top (o : Fin 12) (x : Lattice o) :
    boundedStates o x = ⊤ := by
  apply top_unique
  rw [← (carrierBasis o).span_eq]
  apply Submodule.span_le.mpr
  rintro v ⟨⟨a,y⟩,rfl⟩
  exact ⟨integerPair o x y-(occupationWeight o a : ℤ),
    fun k hk => fieldCoefficient_basis_below o x y a k hk⟩

theorem fieldCoefficient_bounded_pole (o : Fin 12) (x : Lattice o)
    (v : LatticeCarrier o) :
    ∃ b : ℤ, ∀ k < b, fieldCoefficient o x k v = 0 := by
  have h : v ∈ boundedStates o x := by rw [boundedStates_eq_top]; trivial
  exact h

def chargedField (o : Fin 12) (x : Lattice o) : VertexOperator ℂ (LatticeCarrier o) :=
  VertexOperator.of_coeff (fieldCoefficient o x) (fieldCoefficient_bounded_pole o x)

theorem chargedField_coefficient (o : Fin 12) (x : Lattice o)
    (v : LatticeCarrier o) (k : ℤ) :
    ((HahnModule.of ℂ).symm (chargedField o x v)).coeff k =
      fieldCoefficient o x k v := rfl

theorem fieldCoefficient_vacuum (o : Fin 12) (x : Lattice o) (k : ℤ) :
    fieldCoefficient o x k (vacuum o) =
      if 0 ≤ k then
        creationExponentialMode o x k.toNat 1 ⊗ₜ[ℂ] basisElement o x
      else 0 := by
  rw [← vacuum_is_empty_monomial, fieldCoefficient_basis]
  simp [basisCoefficient, basisCoefficientCutoff, occupationWeight,
    integerPair_zero_right, epsilon_zero_right, monomialBasis_product,
    annihilationExponential_constant]

theorem fieldCoefficient_vacuum_nonnegative (o : Fin 12) (x : Lattice o) (k : ℕ) :
    fieldCoefficient o x (k : ℤ) (vacuum o) =
      creationExponentialMode o x k 1 ⊗ₜ[ℂ] basisElement o x := by
  rw [fieldCoefficient_vacuum, if_pos (Int.natCast_nonneg k), Int.toNat_natCast]

theorem fieldCoefficient_vacuum_negative (o : Fin 12) (x : Lattice o)
    (k : ℤ) (hk : k < 0) : fieldCoefficient o x k (vacuum o) = 0 := by
  rw [fieldCoefficient_vacuum, if_neg (by omega)]

theorem fieldCoefficient_vacuum_zero (o : Fin 12) (x : Lattice o) :
    fieldCoefficient o x 0 (vacuum o) = (1 : Fock o) ⊗ₜ[ℂ] basisElement o x := by
  rw [fieldCoefficient_vacuum]
  simp [creationExponentialMode_zero]

theorem annihilationPotential_zero_charge (o : Fin 12) :
    annihilationPotential o 0 = 0 := by
  have ht : annihilationTail o 0 = 0 := by
    ext n
    simp [annihilationTail, chargeAnnihilation]
  simp [annihilationPotential, ht]

theorem annihilationCoefficient_zero_charge (o : Fin 12) (d : ℕ) :
    exponentialCoefficient o 0 d =
      if d=0 then (LinearMap.id : Module.End ℂ (Fock o)) else 0 := by
  unfold exponentialCoefficient
  rw [Finset.sum_eq_single 0]
  · simp [PowerSeries.coeff_one]
    rfl
  · intro k _ hk
    rw [annihilationPotential_zero_charge, zero_pow hk]
    simp
  · simp

theorem creationMode_zero_charge_apply (o : Fin 12) (d : ℕ) (v : Fock o) :
    creationExponentialMode o 0 d v = if d=0 then v else 0 := by
  change PowerSeries.coeff (Fock o) d (creationExponential o 0) * v = _
  rw [creationExponential_zero_charge]
  simp only [PowerSeries.coeff_one]
  split_ifs <;> simp

theorem basisCoefficient_zero_charge (o : Fin 12) (k : ℤ)
    (a : Occupation o) (y : Lattice o) :
    basisCoefficient o 0 k a y =
      if k=0 then carrierBasis o (a,y) else 0 := by
  unfold basisCoefficient basisCoefficientCutoff
  simp only [epsilon_zero_left, integerPair_zero_left, sub_zero, zero_add, one_smul]
  rw [Finset.sum_eq_single 0]
  · simp only [Nat.cast_zero, add_zero, annihilationCoefficient_zero_charge,
      if_pos rfl, LinearMap.id_apply, creationMode_zero_charge_apply]
    by_cases hk : k=0
    · subst k
      simp only [le_refl, if_pos, Int.toNat_zero]
      simp only [carrierBasis, Basis.tensorProduct_apply, latticeBasisComplex,
        Finsupp.coe_basisSingleOne, LinearMap.id_apply]
      rfl
    · rw [if_neg hk]
      by_cases hnonneg : 0 ≤ k
      · have hnat : k.toNat ≠ 0 := by omega
        rw [if_pos hnonneg, if_neg hnat, TensorProduct.zero_tmul]
      · rw [if_neg hnonneg]
  · intro j _ hj
    rw [annihilationCoefficient_zero_charge, if_neg hj]
    simp only [LinearMap.zero_apply, map_zero, TensorProduct.zero_tmul, ite_self]
  · simp

theorem fieldCoefficient_zero_charge (o : Fin 12) (k : ℤ) :
    fieldCoefficient o 0 k =
      if k=0 then (LinearMap.id : Module.End ℂ (LatticeCarrier o)) else 0 := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  rw [fieldCoefficient_basis, basisCoefficient_zero_charge]
  split_ifs <;> rfl

theorem chargedField_zero_charge_coefficient (o : Fin 12)
    (v : LatticeCarrier o) (k : ℤ) :
    ((HahnModule.of ℂ).symm (chargedField o 0 v)).coeff k =
      if k=0 then v else 0 := by
  rw [chargedField_coefficient, fieldCoefficient_zero_charge]
  split_ifs <;> rfl

end HMT.IV.LatticeChargedVertexField
end

#print axioms HMT.IV.LatticeChargedVertexField.fieldCoefficient_basis
#print axioms HMT.IV.LatticeChargedVertexField.basisCoefficientCutoff_stable
#print axioms HMT.IV.LatticeChargedVertexField.basisCoefficient_below
#print axioms HMT.IV.LatticeChargedVertexField.fieldCoefficient_basis_below
#print axioms HMT.IV.LatticeChargedVertexField.boundedStates_eq_top
#print axioms HMT.IV.LatticeChargedVertexField.fieldCoefficient_bounded_pole
#print axioms HMT.IV.LatticeChargedVertexField.chargedField_coefficient
#print axioms HMT.IV.LatticeChargedVertexField.fieldCoefficient_vacuum
#print axioms HMT.IV.LatticeChargedVertexField.fieldCoefficient_vacuum_nonnegative
#print axioms HMT.IV.LatticeChargedVertexField.fieldCoefficient_vacuum_negative
#print axioms HMT.IV.LatticeChargedVertexField.fieldCoefficient_vacuum_zero
#print axioms HMT.IV.LatticeChargedVertexField.annihilationCoefficient_zero_charge
#print axioms HMT.IV.LatticeChargedVertexField.creationMode_zero_charge_apply
#print axioms HMT.IV.LatticeChargedVertexField.fieldCoefficient_zero_charge
#print axioms HMT.IV.LatticeChargedVertexField.chargedField_zero_charge_coefficient
