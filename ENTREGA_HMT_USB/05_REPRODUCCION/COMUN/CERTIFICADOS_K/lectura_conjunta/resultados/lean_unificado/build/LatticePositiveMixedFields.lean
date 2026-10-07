import LatticeFieldCutoff
import LatticeFieldBiOperators
import LatticeHeisenbergModes
import LatticeChargedFieldCharge

/-! Positive Heisenberg modes against the original charged fields.
The relation is derived from finite field coefficients, the actual cutoff,
and the previously proved oscillator exponential commutator. -/
noncomputable section
namespace HMT.IV.LatticePositiveMixedFields
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialCommutator HMT.IV.LatticeAnnihilationCommutativity
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeFieldCutoff
open HMT.IV.LatticeWeightFiltration HMT.IV.LatticeFieldBiOperators
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeChargedFieldCharge
open scoped TensorProduct BigOperators

theorem mixed_signed_degree (o : Fin 12) (x y : Lattice o)
    (n : ℕ) (D : ℤ) (w : Fock o) :
    (if 0 ≤ D then
      chargeAnnihilation o x n (creationExponentialMode o y D.toNat w) -
        creationExponentialMode o y D.toNat (chargeAnnihilation o x n w)
     else 0) =
    if 0 ≤ D-((n+1:ℕ):ℤ) then
      (integerPair o x y : ℂ) •
        creationExponentialMode o y (D-((n+1:ℕ):ℤ)).toNat w
    else 0 := by
  by_cases hD : 0 ≤ D
  · rw [if_pos hD,mixed_exponential_commutator_pairing]
    have he : n+1 ≤ D.toNat ↔ 0 ≤ D-((n+1:ℕ):ℤ) := by omega
    have hd : D.toNat-(n+1)=(D-((n+1:ℕ):ℤ)).toNat := by omega
    simp only [he,hd]
  · rw [if_neg hD,if_neg (by omega)]

theorem annihilator_fieldCutoff_commutator (o : Fin 12) (x y z : Lattice o)
    (n N : ℕ) (k : ℤ) (v : Fock o) :
    onCarrier o (chargeAnnihilation o x n) (fieldCutoff o y z k N v) -
      fieldCutoff o y z k N (chargeAnnihilation o x n v) =
        (integerPair o x y : ℂ) • fieldCutoff o y z (k-((n+1:ℕ):ℤ)) N v := by
  unfold fieldCutoff
  rw [map_smul,map_sum,smul_comm (integerPair o x y : ℂ),← smul_sub]
  congr 1
  rw [← Finset.sum_sub_distrib,Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  have he := mixed_signed_degree o x y n (k-integerPair o y z+(j:ℤ))
    (exponentialCoefficient o y j v)
  have hdeg : k-integerPair o y z+(j:ℤ)-((n+1:ℕ):ℤ) =
      k-((n+1:ℕ):ℤ)-integerPair o y z+(j:ℤ) := by omega
  rw [hdeg] at he
  have ht := congrArg (fun w : Fock o => w ⊗ₜ[ℂ] basisElement o (y+z)) he
  by_cases hd : 0 ≤ k-integerPair o y z+(j:ℤ)
  · rw [if_pos hd,if_pos hd,onCarrier_pure,
      ← exponentialCoefficient_commute_apply,← TensorProduct.sub_tmul]
    rw [if_pos hd] at ht
    by_cases hr : 0 ≤ k-((n+1:ℕ):ℤ)-integerPair o y z+(j:ℤ)
    · rw [if_pos hr] at ht ⊢
      simpa only [← TensorProduct.smul_tmul'] using ht
    · rw [if_neg hr] at ht ⊢
      simpa only [TensorProduct.zero_tmul,smul_zero] using ht
  · have hr : ¬0 ≤ k-((n+1:ℕ):ℤ)-integerPair o y z+(j:ℤ) := by omega
    simp only [if_neg hd,if_neg hr,map_zero,sub_self,smul_zero]

theorem positive_mode_field_commutator (o : Fin 12) (x y : Lattice o)
    (n : ℕ) (k : ℤ) :
    (onCarrier o (chargeAnnihilation o x n)) * fieldCoefficient o y k -
      fieldCoefficient o y k * (onCarrier o (chargeAnnihilation o x n)) =
        (integerPair o x y : ℂ) • fieldCoefficient o y (k-((n+1:ℕ):ℤ)) := by
  apply end_ext_charged o
  intro v z
  obtain ⟨N,hv⟩ := exists_weight_bound o v
  have hcut : ∀ d, N < d → exponentialCoefficient o y d v = 0 :=
    fun d hd => annihilation_cutoff_on_filtration o y N d hd v hv
  change onCarrier o (chargeAnnihilation o x n)
      (fieldCoefficient o y k (v ⊗ₜ[ℂ] basisElement o z)) -
    fieldCoefficient o y k
      (onCarrier o (chargeAnnihilation o x n) (v ⊗ₜ[ℂ] basisElement o z)) = _
  rw [onCarrier_pure,fieldCoefficient_eq_of_annihilation_cutoff o y z k N v hcut,
    fieldCoefficient_eq_of_annihilation_cutoff o y z k N _
      (cutoff_preserved_by_annihilation o x y n N v hcut)]
  change _ = (integerPair o x y : ℂ) •
    fieldCoefficient o y (k-((n+1:ℕ):ℤ)) (v ⊗ₜ[ℂ] basisElement o z)
  rw [fieldCoefficient_eq_of_annihilation_cutoff o y z _ N v hcut]
  exact annihilator_fieldCutoff_commutator o x y z n N k v

theorem chargeAnnihilation_basis (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    chargeAnnihilation o (latticeBasis o i) n = annihilate o n i := by
  classical
  simp [chargeAnnihilation,Finsupp.single_apply,ite_smul]

theorem chargeCreation_basis (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    chargeCreation o (latticeBasis o i) n = create o n i := by
  classical
  simp [chargeCreation,Finsupp.single_apply,ite_smul]

theorem positive_heisenberg_field_commutator (o : Fin 12)
    (i : Fin (BasisSize o)) (y : Lattice o) (n : ℕ) (k : ℤ) :
    hmode o i ((n+1:ℕ):ℤ) * fieldCoefficient o y k -
      fieldCoefficient o y k * hmode o i ((n+1:ℕ):ℤ) =
        (integerPair o (latticeBasis o i) y : ℂ) •
          fieldCoefficient o y (k-((n+1:ℕ):ℤ)) := by
  simpa only [hmode_castSucc,chargeAnnihilation_basis] using
    positive_mode_field_commutator o (latticeBasis o i) y n k

theorem zero_heisenberg_field_commutator (o : Fin 12)
    (i : Fin (BasisSize o)) (y : Lattice o) (k : ℤ) :
    hmode o i 0 * fieldCoefficient o y k - fieldCoefficient o y k * hmode o i 0 =
      (integerPair o (latticeBasis o i) y : ℂ) • fieldCoefficient o y k := by
  exact zeroMode_fieldCoefficient o (latticeBasis o i) y k

end HMT.IV.LatticePositiveMixedFields
end
#print axioms HMT.IV.LatticePositiveMixedFields.mixed_signed_degree
#print axioms HMT.IV.LatticePositiveMixedFields.annihilator_fieldCutoff_commutator
#print axioms HMT.IV.LatticePositiveMixedFields.positive_mode_field_commutator
#print axioms HMT.IV.LatticePositiveMixedFields.chargeAnnihilation_basis
#print axioms HMT.IV.LatticePositiveMixedFields.chargeCreation_basis
#print axioms HMT.IV.LatticePositiveMixedFields.positive_heisenberg_field_commutator
#print axioms HMT.IV.LatticePositiveMixedFields.zero_heisenberg_field_commutator
