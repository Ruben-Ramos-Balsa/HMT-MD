import LatticeFieldCutoff
import LatticeFieldBiOperators
import LatticeNegativeExponential

/-!
Finite transport of a creation/annihilation-exponential commutator to the
original charged field. The coefficient relation is an explicit input of
the transport lemma and is supplied by its independently proved operator
identity in the final composition.
-/

noncomputable section
set_option maxHeartbeats 1600000
namespace HMT.IV.LatticeNegativeMixedFields

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeAnnihilationCommutativity HMT.IV.LatticeChargedVertexField
open HMT.IV.LatticeFieldCutoff HMT.IV.LatticeWeightFiltration
open HMT.IV.LatticeFieldBiOperators
open scoped TensorProduct BigOperators

theorem sum_shift_cutoff {V : Type*} [AddCommMonoid V] (N m : ℕ) (f : ℕ → V) :
    (∑ j ∈ Finset.range (N+m+1), if m ≤ j then f (j-m) else 0) =
      ∑ j ∈ Finset.range (N+1), f j := by
  rw [show N+m+1=m+(N+1) by omega, Finset.sum_range_add]
  have hz : (∑ j ∈ Finset.range m, if m ≤ j then f (j-m) else 0) = 0 := by
    apply Finset.sum_eq_zero
    intro j hj
    have hj' := Finset.mem_range.mp hj
    rw [if_neg (by omega)]
  rw [hz, zero_add]
  apply Finset.sum_congr rfl
  intro j _
  rw [if_pos (by omega), Nat.add_sub_cancel_left]

theorem creationMode_chargeCreation_commute (o : Fin 12) (x y : Lattice o)
    (n d : ℕ) (v : Fock o) :
    chargeCreation o x n (creationExponentialMode o y d v) =
      creationExponentialMode o y d (chargeCreation o x n v) := by
  simp only [chargeCreation_apply, creationExponentialMode, LinearMap.mulLeft_apply]
  ring

theorem cutoff_after_chargeCreation_of_commutator (o : Fin 12)
    (x y : Lattice o) (n N : ℕ) (v : Fock o)
    (hcomm : ∀ d (w : Fock o),
      chargeCreation o x n (exponentialCoefficient o y d w) -
        exponentialCoefficient o y d (chargeCreation o x n w) =
          if n+1 ≤ d then (integerPair o x y : ℂ) •
            exponentialCoefficient o y (d-(n+1)) w else 0)
    (hv : ∀ d, N < d → exponentialCoefficient o y d v = 0) :
    ∀ d, N+(n+1) < d →
      exponentialCoefficient o y d (chargeCreation o x n v) = 0 := by
  intro d hd
  have h := hcomm d v
  rw [hv d (by omega), map_zero, if_pos (by omega), hv (d-(n+1)) (by omega),
    smul_zero, zero_sub, neg_eq_zero] at h
  exact h

theorem creator_fieldCutoff_commutator_of_coefficients (o : Fin 12)
    (x y z : Lattice o) (n N : ℕ) (k : ℤ) (v : Fock o)
    (hcomm : ∀ d (w : Fock o),
      chargeCreation o x n (exponentialCoefficient o y d w) -
        exponentialCoefficient o y d (chargeCreation o x n w) =
          if n+1 ≤ d then (integerPair o x y : ℂ) •
            exponentialCoefficient o y (d-(n+1)) w else 0) :
    onCarrier o (chargeCreation o x n) (fieldCutoff o y z k (N+(n+1)) v) -
      fieldCutoff o y z k (N+(n+1)) (chargeCreation o x n v) =
        (integerPair o x y : ℂ) • fieldCutoff o y z (k+((n+1:ℕ):ℤ)) N v := by
  let T : ℕ → LatticeCarrier o := fun r =>
    if 0 ≤ k+((n+1:ℕ):ℤ)-integerPair o y z+(r:ℤ) then
      creationExponentialMode o y ((k+((n+1:ℕ):ℤ)-integerPair o y z+(r:ℤ)).toNat)
        (exponentialCoefficient o y r v) ⊗ₜ[ℂ] basisElement o (y+z)
    else 0
  unfold fieldCutoff
  rw [map_smul, map_sum, smul_comm (integerPair o x y : ℂ), ← smul_sub]
  congr 1
  rw [← Finset.sum_sub_distrib, Finset.smul_sum]
  change _ = ∑ r ∈ Finset.range (N+1), (integerPair o x y : ℂ) • T r
  calc
    _ = ∑ j ∈ Finset.range (N+(n+1)+1),
        if n+1 ≤ j then (integerPair o x y : ℂ) • T (j-(n+1)) else 0 := by
      apply Finset.sum_congr rfl
      intro j _
      by_cases hd : 0 ≤ k-integerPair o y z+(j:ℤ)
      · rw [if_pos hd, if_pos hd, onCarrier_pure,
          creationMode_chargeCreation_commute, ← TensorProduct.sub_tmul,
          ← map_sub, hcomm]
        by_cases hj : n+1 ≤ j
        · rw [if_pos hj, if_pos hj, map_smul, ← TensorProduct.smul_tmul']
          have hdeg : k+((n+1:ℕ):ℤ)-integerPair o y z+((j-(n+1):ℕ):ℤ) =
              k-integerPair o y z+(j:ℤ) := by omega
          simp only [T, hdeg, if_pos hd]
        · rw [if_neg hj, if_neg hj, map_zero, TensorProduct.zero_tmul]
      · rw [if_neg hd, if_neg hd, map_zero, sub_self]
        by_cases hj : n+1 ≤ j
        · rw [if_pos hj]
          have hdeg : k+((n+1:ℕ):ℤ)-integerPair o y z+((j-(n+1):ℕ):ℤ) =
              k-integerPair o y z+(j:ℤ) := by omega
          simp only [T, hdeg, if_neg hd, smul_zero]
        · rw [if_neg hj]
    _ = _ := sum_shift_cutoff N (n+1) (fun r => (integerPair o x y : ℂ) • T r)

theorem negative_mode_field_commutator (o : Fin 12) (x y : Lattice o)
    (n : ℕ) (k : ℤ) :
    onCarrier o (chargeCreation o x n) * fieldCoefficient o y k -
      fieldCoefficient o y k * onCarrier o (chargeCreation o x n) =
        (integerPair o x y : ℂ) • fieldCoefficient o y (k+((n+1:ℕ):ℤ)) := by
  apply end_ext_charged o
  intro v z
  obtain ⟨N,hv⟩ := exists_weight_bound o v
  have hcut : ∀ d, N < d → exponentialCoefficient o y d v = 0 :=
    fun d hd => annihilation_cutoff_on_filtration o y N d hd v hv
  have hcomm := HMT.IV.LatticeNegativeExponential.chargeCreation_exponentialCoefficient_apply
    o x y n
  have hbig : ∀ d, N+(n+1) < d → exponentialCoefficient o y d v = 0 :=
    fun d hd => hcut d (by omega)
  have hcreated := cutoff_after_chargeCreation_of_commutator o x y n N v hcomm hcut
  change onCarrier o (chargeCreation o x n)
      (fieldCoefficient o y k (v ⊗ₜ[ℂ] basisElement o z)) -
    fieldCoefficient o y k
      (onCarrier o (chargeCreation o x n) (v ⊗ₜ[ℂ] basisElement o z)) = _
  rw [onCarrier_pure,
    fieldCoefficient_eq_of_annihilation_cutoff o y z k (N+(n+1)) v hbig,
    fieldCoefficient_eq_of_annihilation_cutoff o y z k (N+(n+1)) _ hcreated]
  change _ = (integerPair o x y : ℂ) •
    fieldCoefficient o y (k+((n+1:ℕ):ℤ)) (v ⊗ₜ[ℂ] basisElement o z)
  rw [fieldCoefficient_eq_of_annihilation_cutoff o y z _ N v hcut]
  exact creator_fieldCutoff_commutator_of_coefficients o x y z n N k v hcomm

end HMT.IV.LatticeNegativeMixedFields
end

#print axioms HMT.IV.LatticeNegativeMixedFields.sum_shift_cutoff
#print axioms HMT.IV.LatticeNegativeMixedFields.creationMode_chargeCreation_commute
#print axioms HMT.IV.LatticeNegativeMixedFields.cutoff_after_chargeCreation_of_commutator
#print axioms HMT.IV.LatticeNegativeMixedFields.creator_fieldCutoff_commutator_of_coefficients
#print axioms HMT.IV.LatticeNegativeMixedFields.negative_mode_field_commutator
