import LatticeConformalState
import LatticeGramSymmetry
import LatticeTranslationOperator
import LatticeConformalCoefficient
import LatticeGramContractions
import LatticeTranslationCommutators
import LatticePositiveMixedFields
import LatticeFieldGeneration

/-! The coefficient at Laurent exponent -1 of the constructed quadratic
field, retaining its actual pointwise finite normal-product sums. -/

noncomputable section
namespace HMT.IV.LatticeConformalTranslation

open LatticeCocycle LatticeOscillatorFock LatticeNormalOrderedField
open LatticeHeisenbergField LatticeHeisenbergModes
open LatticeConformalState LatticeGramDual LatticeGramSymmetry
open LatticeConformalCoefficient LatticeGramContractions
open LatticeCreationExponential TwistedGroupAlgebra
open scoped BigOperators TensorProduct

theorem creation_translation_mode (o : Fin 12) (i j : Fin (BasisSize o)) (a : ℕ) :
    creationTerm o i 0 (heisenbergField o j) (-1) a =
      (onCarrier o (create o a i)).comp (hmode o j (a : ℤ)) := by
  simp only [creationTerm, Nat.add_zero, Nat.choose_zero_right, Nat.cast_one,
    one_smul]
  change (onCarrier o (create o a i)).comp (hmode o j (-(-1-(a : ℤ))-1)) = _
  rw [show -(-1-(a : ℤ))-1 = (a : ℤ) by omega]

theorem annihilation_translation_mode (o : Fin 12) (i j : Fin (BasisSize o))
    (a : ℕ) :
    annihilationTerm o i 0 (heisenbergField o j) (-1) a =
      (onCarrier o (create o a j)).comp (hmode o i (a : ℤ)) := by
  simp only [annihilationTerm, pow_zero, Nat.add_zero, Nat.choose_zero_right,
    Nat.cast_one, one_mul, one_smul, Nat.cast_zero, add_zero]
  change (hmode o j (-(-1+(a : ℤ)+1)-1)).comp (hmode o i (a : ℤ)) = _
  rw [show -(-1+(a : ℤ)+1)-1 = Int.negSucc a by omega, hmode_negSucc]

theorem normal_translation_cutoff (o : Fin 12) (i j : Fin (BasisSize o))
    (v : LatticeCarrier o) (N : ℕ)
    (hN : ∀ a ≥ N, ∀ l : Fin (BasisSize o), onCarrier o (annihilate o a l) v = 0) :
    normalCoefficient o i 0 (heisenbergField o j) (-1) v =
      onCarrier o (create o 0 i) (hmode o j 0 v) +
      onCarrier o (create o 0 j) (hmode o i 0 v) +
        ∑ a ∈ Finset.range N,
          (onCarrier o (create o (a+1) i) (onCarrier o (annihilate o a j) v) +
           onCarrier o (create o (a+1) j) (onCarrier o (annihilate o a i) v)) := by
  classical
  have hC : Function.support (fun a => creationTerm o i 0 (heisenbergField o j) (-1) a v)
      ⊆ (Finset.range (N+1) : Set ℕ) := by
    intro a ha
    simp only [Finset.mem_coe, Finset.mem_range]
    by_contra hn
    cases a with
    | zero => omega
    | succ a =>
      apply ha
      change creationTerm o i 0 (heisenbergField o j) (-1) (a+1) v = 0
      rw [creation_translation_mode, LinearMap.comp_apply, hmode_castSucc,
        hN a (by omega), map_zero]
  have hA : Function.support (fun a => annihilationTerm o i 0 (heisenbergField o j) (-1) a v)
      ⊆ (Finset.range (N+1) : Set ℕ) := by
    intro a ha
    simp only [Finset.mem_coe, Finset.mem_range]
    by_contra hn
    cases a with
    | zero => omega
    | succ a =>
      apply ha
      change annihilationTerm o i 0 (heisenbergField o j) (-1) (a+1) v = 0
      rw [annihilation_translation_mode, LinearMap.comp_apply, hmode_castSucc,
        hN a (by omega), map_zero]
  rw [normalCoefficient_apply, finsum_eq_sum_of_support_subset _ hC,
    finsum_eq_sum_of_support_subset _ hA]
  rw [Finset.sum_range_succ', Finset.sum_range_succ']
  simp only [creation_translation_mode, annihilation_translation_mode,
    LinearMap.comp_apply, Nat.cast_zero, hmode_castSucc, Finset.sum_add_distrib]
  abel

theorem gram_symmetrized (o : Fin 12)
    (F : Fin (BasisSize o) → Fin (BasisSize o) → LatticeCarrier o) :
    (2 : ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j • (F i j + F j i)) =
      ∑ i, ∑ j, gramInv o i j • F i j := by
  have hs : (∑ i, ∑ j, gramInv o i j • F j i) =
      ∑ i, ∑ j, gramInv o i j • F i j := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    rw [gramInv_symmetric]
  simp only [smul_add, Finset.sum_add_distrib]
  rw [hs]
  module

theorem conformal_translation_cutoff (o : Fin 12) (v : LatticeCarrier o) (N : ℕ)
    (hN : ∀ a ≥ N, ∀ l : Fin (BasisSize o), onCarrier o (annihilate o a l) v = 0) :
    conformalMode o (-1) v =
      ∑ i, ∑ j, gramInv o i j •
        (onCarrier o (create o 0 i) (hmode o j 0 v) +
          ∑ a ∈ Finset.range N,
            onCarrier o (create o (a+1) i) (onCarrier o (annihilate o a j) v)) := by
  rw [conformalMode_normal_sum_apply]
  simp only [show -(-1 : ℤ)-2 = -1 by omega]
  let F := fun i j => onCarrier o (create o 0 i) (hmode o j 0 v) +
    ∑ a ∈ Finset.range N,
      onCarrier o (create o (a+1) i) (onCarrier o (annihilate o a j) v)
  have hF (i j : Fin (BasisSize o)) :
      normalCoefficient o i 0 (heisenbergField o j) (-1) v = F i j + F j i := by
    dsimp only [F]
    rw [normal_translation_cutoff o i j v N hN, Finset.sum_add_distrib]
    abel
  simp_rw [hF]
  exact gram_symmetrized o F

theorem charge_term_creator_commute (o : Fin 12) (i j k : Fin (BasisSize o))
    (n : ℕ) (v : LatticeCarrier o) :
    onCarrier o (create o 0 i) (hmode o j 0 (onCarrier o (create o n k) v)) =
      onCarrier o (create o n k) (onCarrier o (create o 0 i) (hmode o j 0 v)) := by
  rw [hmode_zero, ← oscillator_lattice_commute, carrier_creations_commute]

theorem shift_term_creator_commutator (o : Fin 12) (i j k : Fin (BasisSize o))
    (a n : ℕ) (v : LatticeCarrier o) :
    onCarrier o (create o (a+1) i)
        (onCarrier o (annihilate o a j) (onCarrier o (create o n k) v)) -
      onCarrier o (create o n k)
        (onCarrier o (create o (a+1) i) (onCarrier o (annihilate o a j) v)) =
      (if a=n then (a+1 : ℂ) * gram o j k else 0) •
        onCarrier o (create o (a+1) i) v := by
  have h := congrArg (onCarrier o (create o (a+1) i)) (carrier_mode_ccr o a n j k v)
  simpa only [map_sub, map_smul, carrier_creations_commute o (a+1) n i k] using h

theorem conformal_translation_creator (o : Fin 12) (n : ℕ)
    (k : Fin (BasisSize o)) (v : LatticeCarrier o) :
    conformalMode o (-1) (onCarrier o (create o n k) v) -
      onCarrier o (create o n k) (conformalMode o (-1) v) =
      (n+1 : ℂ) • onCarrier o (create o (n+1) k) v := by
  classical
  obtain ⟨M, hM⟩ := LatticeFieldTruncation.exists_carrier_annihilation_bound o v
  let N := max M (n+1)
  have hn : n < N := by dsimp [N]; omega
  have hN (a : ℕ) (ha : a ≥ N) (l : Fin (BasisSize o)) :
      onCarrier o (annihilate o a l) v = 0 := hM a (by dsimp [N] at ha; omega) l
  have hC (a : ℕ) (ha : a ≥ N) (l : Fin (BasisSize o)) :
      onCarrier o (annihilate o a l) (onCarrier o (create o n k) v) = 0 := by
    have h := carrier_mode_ccr o a n l k v
    rw [hN a ha l, map_zero, sub_zero, if_neg (by omega), zero_smul] at h
    exact h
  rw [conformal_translation_cutoff o _ N hC, conformal_translation_cutoff o v N hN]
  simp only [map_sum, map_smul, map_add]
  rw [← Finset.sum_sub_distrib]
  have hinner (i : Fin (BasisSize o)) :
      (∑ j, gramInv o i j •
        (onCarrier o (create o 0 i) (hmode o j 0 (onCarrier o (create o n k) v)) +
          ∑ a ∈ Finset.range N, onCarrier o (create o (a+1) i)
            (onCarrier o (annihilate o a j) (onCarrier o (create o n k) v)))) -
      (∑ j, gramInv o i j •
        (onCarrier o (create o n k) (onCarrier o (create o 0 i) (hmode o j 0 v)) +
          ∑ a ∈ Finset.range N, onCarrier o (create o n k)
            (onCarrier o (create o (a+1) i) (onCarrier o (annihilate o a j) v)))) =
      ((n+1 : ℂ) * (if i=k then 1 else 0)) •
        onCarrier o (create o (n+1) i) v := by
    rw [← Finset.sum_sub_distrib]
    simp only [← smul_sub, charge_term_creator_commute, add_sub_add_left_eq_sub,
      ← Finset.sum_sub_distrib, shift_term_creator_commutator]
    have hs (j : Fin (BasisSize o)) :
        (∑ a ∈ Finset.range N, (if a=n then (a+1 : ℂ) * gram o j k else 0) •
          onCarrier o (create o (a+1) i) v) =
        ((n+1 : ℂ) * gram o j k) • onCarrier o (create o (n+1) i) v := by
      rw [Finset.sum_eq_single n]
      · simp
      · intro a _ ha
        simp [ha]
      · intro h
        exact False.elim (h (Finset.mem_range.mpr hn))
    simp_rw [hs, smul_smul]
    rw [← Finset.sum_smul]
    congr 1
    calc
      _ = (n+1 : ℂ) * ∑ j, gramInv o i j * gram o j k := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intros
        ring
      _ = _ := by rw [gramInv_pairing]
  simp_rw [hinner]
  simp

theorem conformal_translation_ground (o : Fin 12) (x : Lattice o) :
    conformalMode o (-1) ((1 : Fock o) ⊗ₜ[ℂ] basisElement o x) =
      LatticeTranslationOperator.translation o ((1 : Fock o) ⊗ₜ[ℂ] basisElement o x) := by
  have hN (a : ℕ) (_ : a ≥ 0) (l : Fin (BasisSize o)) :
      onCarrier o (annihilate o a l) ((1 : Fock o) ⊗ₜ[ℂ] basisElement o x) = 0 := by
    simp only [onCarrier_pure, annihilate_vacuum, TensorProduct.zero_tmul]
  rw [conformal_translation_cutoff o _ 0 hN]
  simp only [Finset.range_zero, Finset.sum_empty, add_zero, hmode_zero,
    onLattice_pure, LatticeZeroModes.zeroMode_basis, TensorProduct.tmul_smul,
    map_smul, onCarrier_pure, smul_smul]
  have hi (i : Fin (BasisSize o)) :
      (∑ j, (gramInv o i j * (integerPair o (latticeBasis o j) x : ℂ)) •
        (create o 0 i 1 ⊗ₜ[ℂ] basisElement o x)) =
      ((latticeBasis o).repr x i : ℂ) •
        (create o 0 i 1 ⊗ₜ[ℂ] basisElement o x) := by
    rw [← Finset.sum_smul, dual_pair_coordinates]
  simp_rw [hi]
  rw [LatticeTranslationOperator.translation_pure]
  simp only [Derivation.map_one_eq_zero, zero_add, mul_one]
  simp_rw [TensorProduct.smul_tmul']
  rw [← TensorProduct.sum_tmul]
  congr 1
  have hc := chargeCreation_apply o x 0 (1 : Fock o)
  simpa only [chargeCreation, LinearMap.sum_apply, LinearMap.smul_apply, mul_one] using hc

theorem conformalMode_neg_one_eq_translation (o : Fin 12) :
    conformalMode o (-1) = LatticeTranslationOperator.translation o := by
  let T := LatticeTranslationOperator.translation o
  let S := LinearMap.ker (conformalMode o (-1) - T)
  have htop : S = ⊤ := by
    apply LatticeFieldGeneration.carrier_generated_by_ground_states o
    · intro x
      change conformalMode o (-1) ((1 : Fock o) ⊗ₜ[ℂ] basisElement o x) -
        T ((1 : Fock o) ⊗ₜ[ℂ] basisElement o x) = 0
      exact sub_eq_zero.mpr (conformal_translation_ground o x)
    · intro n i v hv
      have hv' : conformalMode o (-1) v = T v := sub_eq_zero.mp hv
      have hL := conformal_translation_creator o n i v
      have hT : T.comp (onCarrier o (create o n i)) -
          (onCarrier o (create o n i)).comp T =
          (n+1 : ℂ) • onCarrier o (create o (n+1) i) := by
        simpa only [LatticePositiveMixedFields.chargeCreation_basis] using
          LatticeTranslationCommutators.translation_chargeCreate o (latticeBasis o i) n
      have hTv := LinearMap.congr_fun hT v
      simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply] at hTv
      rw [hv'] at hL
      change conformalMode o (-1) (onCarrier o (create o n i) v) -
        T (onCarrier o (create o n i) v) = 0
      exact sub_eq_zero.mpr (sub_left_inj.mp (hL.trans hTv.symm))
  apply LinearMap.ext
  intro v
  have hv : v ∈ S := by rw [htop]; trivial
  exact sub_eq_zero.mp hv

end HMT.IV.LatticeConformalTranslation
end

#print axioms HMT.IV.LatticeConformalTranslation.creation_translation_mode
#print axioms HMT.IV.LatticeConformalTranslation.annihilation_translation_mode
#print axioms HMT.IV.LatticeConformalTranslation.normal_translation_cutoff
#print axioms HMT.IV.LatticeConformalTranslation.gram_symmetrized
#print axioms HMT.IV.LatticeConformalTranslation.conformal_translation_cutoff
#print axioms HMT.IV.LatticeConformalTranslation.charge_term_creator_commute
#print axioms HMT.IV.LatticeConformalTranslation.shift_term_creator_commutator
#print axioms HMT.IV.LatticeConformalTranslation.conformal_translation_creator
#print axioms HMT.IV.LatticeConformalTranslation.conformal_translation_ground
#print axioms HMT.IV.LatticeConformalTranslation.conformalMode_neg_one_eq_translation
