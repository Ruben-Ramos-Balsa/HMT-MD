import LatticeTranslationOperator
import LatticeExponentialCommutator
import LatticeHeisenbergModes

/-!
Commutators of the constructed translation with the existing oscillator
and lattice charge operators. Frequencies use n+1 for the natural index n.
The zero-frequency crossing is supplied by the charge part of translation,
not by extending the oscillator derivation by a desired relation.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeTranslationCommutators

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialCommutator HMT.IV.LatticeZeroModes
open HMT.IV.LatticeHeisenbergModes
open HMT.FockTransport.Symmetric
open scoped BigOperators TensorProduct

local notation "D" => HMT.IV.LatticeOscillatorTranslation.translation
local notation "T" => HMT.IV.LatticeTranslationOperator.translation

theorem oscillator_translation_annihilation_zero (o : Fin 12) (i : Fin (BasisSize o)) :
    ⁅D o, annihilation (modeCovector o 0 i)⁆ = 0 := by
  apply HMT.IV.LatticeOscillatorTranslation.derivation_ext_generators
  have h : (⁅D o, annihilation (modeCovector o 0 i)⁆).toLinearMap.comp
      (SymmetricAlgebra.ι ℂ (Oscillators o)) = 0 := by
    apply (oscillatorBasis o).ext
    rintro ⟨m,j⟩
    change D o (annihilation (modeCovector o 0 i)
        (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o m j))) -
      annihilation (modeCovector o 0 i)
        (D o (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o (m,j)))) = 0
    rw [annihilation_generator, Derivation.map_algebraMap,
      HMT.IV.LatticeOscillatorTranslation.translation_mode,
      Derivation.map_smul, annihilation_generator]
    change 0 - (m+1:ℂ) • algebraMap ℂ (Fock o)
      (modeCovector o 0 i (modeVector o (m+1) j)) = 0
    simp
  intro v
  exact LinearMap.congr_fun h v

theorem oscillator_translation_annihilation_succ (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) :
    ⁅D o, annihilation (modeCovector o (n+1) i)⁆ =
      (-(n+2 : ℂ)) • annihilation (modeCovector o n i) := by
  apply HMT.IV.LatticeOscillatorTranslation.derivation_ext_generators
  have h : (⁅D o, annihilation (modeCovector o (n+1) i)⁆).toLinearMap.comp
      (SymmetricAlgebra.ι ℂ (Oscillators o)) =
      ((-(n+2 : ℂ)) • annihilation (modeCovector o n i)).toLinearMap.comp
        (SymmetricAlgebra.ι ℂ (Oscillators o)) := by
    apply (oscillatorBasis o).ext
    rintro ⟨m,j⟩
    change D o (annihilation (modeCovector o (n+1) i)
        (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o m j))) -
      annihilation (modeCovector o (n+1) i)
        (D o (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o (m,j)))) =
      (-(n+2:ℂ)) • annihilation (modeCovector o n i)
        (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o m j))
    rw [annihilation_generator, Derivation.map_algebraMap,
      HMT.IV.LatticeOscillatorTranslation.translation_mode,
      Derivation.map_smul, annihilation_generator, annihilation_generator]
    change 0 - (m+1:ℂ) • algebraMap ℂ (Fock o)
      (modeCovector o (n+1) i (modeVector o (m+1) j)) =
      (-(n+2:ℂ)) • algebraMap ℂ (Fock o)
        (modeCovector o n i (modeVector o m j))
    simp only [modeCovector_modeVector, Nat.add_right_cancel_iff]
    by_cases hnm : n=m
    · subst m
      simp only [if_true, Algebra.algebraMap_eq_smul_one, smul_smul, zero_sub]
      rw [← neg_smul]
      congr 1
      push_cast
      ring
    · simp [hnm]
  intro v
  exact LinearMap.congr_fun h v

theorem oscillator_translation_annihilate_zero_apply (o : Fin 12)
    (i : Fin (BasisSize o)) (v : Fock o) :
    D o (annihilate o 0 i v) - annihilate o 0 i (D o v) = 0 := by
  have h := congrArg (fun E : Derivation ℂ (Fock o) (Fock o) => E v)
    (oscillator_translation_annihilation_zero o i)
  exact h

theorem oscillator_translation_annihilate_succ_apply (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (v : Fock o) :
    D o (annihilate o (n+1) i v) - annihilate o (n+1) i (D o v) =
      (-(n+2 : ℂ)) • annihilate o n i v := by
  have h := congrArg (fun E : Derivation ℂ (Fock o) (Fock o) => E v)
    (oscillator_translation_annihilation_succ o n i)
  exact h

theorem oscillator_translation_chargeCreation (o : Fin 12) (x : Lattice o)
    (n : ℕ) (v : Fock o) :
    D o (chargeCreation o x n v) - chargeCreation o x n (D o v) =
      (n+1 : ℂ) • chargeCreation o x (n+1) v := by
  simp only [chargeCreation, LinearMap.sum_apply, LinearMap.smul_apply,
    map_sum, Derivation.map_smul, Finset.smul_sum]
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rw [← smul_sub, HMT.IV.LatticeOscillatorTranslation.translation_create,
    add_sub_cancel_left, smul_comm]

theorem oscillator_translation_chargeAnnihilation_zero (o : Fin 12) (x : Lattice o)
    (v : Fock o) :
    D o (chargeAnnihilation o x 0 v) - chargeAnnihilation o x 0 (D o v) = 0 := by
  simp only [chargeAnnihilation_apply, map_sum, Derivation.map_smul]
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_eq_zero
  intro i _
  rw [← smul_sub, oscillator_translation_annihilate_zero_apply, smul_zero]

theorem oscillator_translation_chargeAnnihilation_succ (o : Fin 12) (x : Lattice o)
    (n : ℕ) (v : Fock o) :
    D o (chargeAnnihilation o x (n+1) v) - chargeAnnihilation o x (n+1) (D o v) =
      (-(n+2 : ℂ)) • chargeAnnihilation o x n v := by
  simp only [chargeAnnihilation_apply, map_sum, Derivation.map_smul, Finset.smul_sum]
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rw [← smul_sub, oscillator_translation_annihilate_succ_apply, smul_comm]

theorem chargeAnnihilation_product (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v w : Fock o) :
    chargeAnnihilation o x n (v*w) =
      v * chargeAnnihilation o x n w + w * chargeAnnihilation o x n v := by
  rw [← chargedDerivation_apply, Derivation.leibniz]
  simp only [smul_eq_mul, chargedDerivation_apply]

theorem chargeAnnihilation_creationState (o : Fin 12) (x y : Lattice o) (n m : ℕ) :
    chargeAnnihilation o x n (chargeCreationState o y m) =
      if n=m then ((n+1 : ℂ) * (integerPair o x y : ℂ)) • (1 : Fock o) else 0 := by
  rw [← chargedDerivation_apply, chargedDerivation_creationState,
    coordinatePair_eq_integerPair]

theorem chargeCreationState_add (o : Fin 12) (x y : Lattice o) (n : ℕ) :
    chargeCreationState o (x+y) n = chargeCreationState o x n +
      chargeCreationState o y n := by
  simp [chargeCreationState, chargeModeVector, add_smul, Finset.sum_add_distrib]

theorem translation_chargeCreate (o : Fin 12) (x : Lattice o) (n : ℕ) :
    (T o).comp (onCarrier o (chargeCreation o x n)) -
      (onCarrier o (chargeCreation o x n)).comp (T o) =
      (n+1 : ℂ) • onCarrier o (chargeCreation o x (n+1)) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [carrierBasis, Basis.tensorProduct_apply]
  change T o (onCarrier o (chargeCreation o x n)
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) -
    onCarrier o (chargeCreation o x n)
      (T o (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) =
    (n+1:ℂ) • onCarrier o (chargeCreation o x (n+1))
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)
  simp only [onCarrier_pure, HMT.IV.LatticeTranslationOperator.translation_pure,
    ← TensorProduct.sub_tmul, ← TensorProduct.smul_tmul']
  congr 1
  rw [map_add]
  have h := oscillator_translation_chargeCreation o x n (monomialBasis o a)
  simp only [chargeCreation_apply] at h ⊢
  linear_combination h

theorem translation_chargeAnnihilate_succ (o : Fin 12) (x : Lattice o) (n : ℕ) :
    (T o).comp (onCarrier o (chargeAnnihilation o x (n+1))) -
      (onCarrier o (chargeAnnihilation o x (n+1))).comp (T o) =
      (-(n+2 : ℂ)) • onCarrier o (chargeAnnihilation o x n) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [carrierBasis, Basis.tensorProduct_apply]
  change T o (onCarrier o (chargeAnnihilation o x (n+1))
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) -
    onCarrier o (chargeAnnihilation o x (n+1))
      (T o (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) =
    (-(n+2):ℂ) • onCarrier o (chargeAnnihilation o x n)
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)
  simp only [onCarrier_pure, HMT.IV.LatticeTranslationOperator.translation_pure,
    ← TensorProduct.sub_tmul, ← TensorProduct.smul_tmul']
  congr 1
  rw [map_add, chargeAnnihilation_product, chargeAnnihilation_creationState]
  simp only [Nat.add_eq_zero_iff, one_ne_zero, and_false, if_false, mul_zero, add_zero]
  have h := oscillator_translation_chargeAnnihilation_succ o x n (monomialBasis o a)
  linear_combination h

theorem translation_chargeAnnihilate_zero (o : Fin 12) (x : Lattice o) :
    (T o).comp (onCarrier o (chargeAnnihilation o x 0)) -
      (onCarrier o (chargeAnnihilation o x 0)).comp (T o) =
      -onLattice o (zeroMode o x) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [carrierBasis, Basis.tensorProduct_apply]
  change T o (onCarrier o (chargeAnnihilation o x 0)
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) -
    onCarrier o (chargeAnnihilation o x 0)
      (T o (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) =
    -(onLattice o (zeroMode o x)
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y))
  simp only [onCarrier_pure, HMT.IV.LatticeTranslationOperator.translation_pure,
    onLattice_pure, zeroMode_basis, TensorProduct.tmul_smul,
    ← TensorProduct.sub_tmul, ← TensorProduct.smul_tmul', ← TensorProduct.neg_tmul]
  congr 1
  rw [map_add, chargeAnnihilation_product, chargeAnnihilation_creationState]
  simp only [if_true, Nat.cast_zero, zero_add, one_mul,
    LinearMap.neg_apply, LinearMap.id_apply]
  have h := oscillator_translation_chargeAnnihilation_zero o x (monomialBasis o a)
  simp only [Algebra.smul_def, mul_one] at h ⊢
  linear_combination h

theorem translation_zeroMode (o : Fin 12) (x : Lattice o) :
    (T o).comp (onLattice o (zeroMode o x)) =
      (onLattice o (zeroMode o x)).comp (T o) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [carrierBasis, Basis.tensorProduct_apply]
  change T o (onLattice o (zeroMode o x)
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) =
    onLattice o (zeroMode o x)
      (T o (monomialBasis o a ⊗ₜ[ℂ] basisElement o y))
  simp only [onLattice_pure, zeroMode_basis, TensorProduct.tmul_smul, map_smul,
    HMT.IV.LatticeTranslationOperator.translation_pure]

theorem translation_latticeShift (o : Fin 12) (x : Lattice o) :
    (T o).comp (onLattice o (latticeShift o x)) -
      (onLattice o (latticeShift o x)).comp (T o) =
      (onCarrier o (chargeCreation o x 0)).comp (onLattice o (latticeShift o x)) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  simp only [carrierBasis, Basis.tensorProduct_apply]
  change T o (onLattice o (latticeShift o x)
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) -
    onLattice o (latticeShift o x)
      (T o (monomialBasis o a ⊗ₜ[ℂ] basisElement o y)) =
    onCarrier o (chargeCreation o x 0) (onLattice o (latticeShift o x)
      (monomialBasis o a ⊗ₜ[ℂ] basisElement o y))
  simp only [onLattice_pure, latticeShift_basis, TensorProduct.tmul_smul,
    map_smul, HMT.IV.LatticeTranslationOperator.translation_pure, onCarrier_pure,
    ← smul_sub, ← TensorProduct.sub_tmul]
  congr 2
  rw [chargeCreationState_add, chargeCreation_apply]
  ring

end HMT.IV.LatticeTranslationCommutators
end

#print axioms HMT.IV.LatticeTranslationCommutators.oscillator_translation_annihilation_zero
#print axioms HMT.IV.LatticeTranslationCommutators.oscillator_translation_annihilation_succ
#print axioms HMT.IV.LatticeTranslationCommutators.oscillator_translation_chargeCreation
#print axioms HMT.IV.LatticeTranslationCommutators.oscillator_translation_chargeAnnihilation_zero
#print axioms HMT.IV.LatticeTranslationCommutators.oscillator_translation_chargeAnnihilation_succ
#print axioms HMT.IV.LatticeTranslationCommutators.translation_chargeCreate
#print axioms HMT.IV.LatticeTranslationCommutators.translation_chargeAnnihilate_succ
#print axioms HMT.IV.LatticeTranslationCommutators.translation_chargeAnnihilate_zero
#print axioms HMT.IV.LatticeTranslationCommutators.translation_zeroMode
#print axioms HMT.IV.LatticeTranslationCommutators.translation_latticeShift
