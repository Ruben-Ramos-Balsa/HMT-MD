import LatticeConformalLowModes
import LatticeGramSymmetry
import LatticeConformalCoefficient

/-! Direct contraction of the nonnegative Heisenberg modes on the quadratic
state, and its central vacuum coefficient. The normal-product sums are
evaluated with their proved finite supports; no Virasoro relation is assumed. -/

noncomputable section
namespace HMT.IV.LatticeConformalCentralCoefficient

open LatticeCocycle LatticeOscillatorFock LatticeHeisenbergModes
open LatticeDescendantFields LatticeConformalState LatticeGramDual
open LatticeNormalOrderedField LatticeHeisenbergField
open LatticeConformalCoefficient
open scoped BigOperators

theorem nonnegative_mode_create (o : Fin 12) (i j : Fin (BasisSize o))
    (a : ℕ) (v : LatticeCarrier o) :
    hmode o i (a : ℤ) (onCarrier o (create o 0 j) v) =
      onCarrier o (create o 0 j) (hmode o i (a : ℤ) v) +
      (if a=1 then gram o i j else 0) • v := by
  have h := heisenberg_relation_apply o i j (a : ℤ) (Int.negSucc 0) v
  rw [hmode_negSucc, Int.cast_natCast] at h
  have hs : (if (a : ℤ) + Int.negSucc 0 = 0 then (a : ℂ) * gram o i j else 0) =
      (if a=1 then gram o i j else 0) := by
    by_cases ha : a=1
    · subst a
      rw [if_pos (by decide), if_pos rfl]
      norm_num
    · rw [if_neg (by omega), if_neg ha]
  rw [hs, sub_eq_iff_eq_add] at h
  exact h.trans (add_comm _ _)

theorem nonnegative_mode_one_creator (o : Fin 12) (i j : Fin (BasisSize o))
    (a : ℕ) :
    hmode o i (a : ℤ) (onCarrier o (create o 0 j) (vacuum o)) =
      (if a=1 then gram o i j else 0) • vacuum o := by
  rw [nonnegative_mode_create, nonnegative_modes_vacuum, map_zero, zero_add]

theorem nonnegative_mode_two_creators (o : Fin 12)
    (i j k : Fin (BasisSize o)) (a : ℕ) :
    hmode o i (a : ℤ) (onCarrier o (create o 0 j)
      (onCarrier o (create o 0 k) (vacuum o))) =
      (if a=1 then gram o i k else 0) • onCarrier o (create o 0 j) (vacuum o) +
      (if a=1 then gram o i j else 0) • onCarrier o (create o 0 k) (vacuum o) := by
  rw [nonnegative_mode_create, nonnegative_mode_one_creator, map_smul]

theorem gram_contract_vectors {V : Type*} [AddCommGroup V] [Module ℂ V]
    (o : Fin 12) (i : Fin (BasisSize o)) (f : Fin (BasisSize o) → V) :
    (∑ a, ∑ b, gramInv o a b • (gram o i a • f b)) = f i := by
  classical
  simp only [smul_smul]
  rw [Finset.sum_comm]
  have inner (b : Fin (BasisSize o)) :
      ∑ a, (gramInv o a b * gram o i a) • f b = (if i=b then (1 : ℂ) else 0) • f b := by
    rw [← Finset.sum_smul]
    have h := pairing_gramInv o i b
    simp_rw [mul_comm (gramInv o _ b)]
    rw [h]
  simp_rw [inner]
  simp

theorem gram_contract_vectors_right {V : Type*} [AddCommGroup V] [Module ℂ V]
    (o : Fin 12) (i : Fin (BasisSize o)) (f : Fin (BasisSize o) → V) :
    (∑ a, ∑ b, gramInv o a b • (gram o i b • f a)) = f i := by
  rw [Finset.sum_comm]
  simp_rw [LatticeGramSymmetry.gramInv_symmetric o]
  exact gram_contract_vectors o i f

theorem nonnegative_mode_conformalState (o : Fin 12) (i : Fin (BasisSize o))
    (a : ℕ) :
    hmode o i (a : ℤ) (conformalState o) =
      if a=1 then onCarrier o (create o 0 i) (vacuum o) else 0 := by
  classical
  simp only [conformalState, map_smul, map_sum, nonnegative_mode_two_creators]
  by_cases ha : a=1
  · simp only [if_pos ha, smul_add, Finset.sum_add_distrib]
    rw [gram_contract_vectors_right, gram_contract_vectors]
    module
  · simp [ha]

theorem creationTerm_central_state (o : Fin 12) (i j : Fin (BasisSize o))
    (a : ℕ) : creationTerm o i 0 (heisenbergField o j) (-4) a (conformalState o) = 0 := by
  simp only [creationTerm, Nat.add_zero, Nat.choose_zero_right, Nat.cast_one,
    one_smul, LinearMap.comp_apply]
  change onCarrier o (create o a i) (hmode o j (-(-4-(a : ℤ))-1) (conformalState o)) = 0
  rw [show -(-4-(a : ℤ))-1 = ((a+3 : ℕ) : ℤ) by omega,
    nonnegative_mode_conformalState, if_neg (by omega), map_zero]

theorem annihilationTerm_central_state (o : Fin 12) (i j : Fin (BasisSize o))
    (a : ℕ) : annihilationTerm o i 0 (heisenbergField o j) (-4) a (conformalState o) =
      if a=1 then gram o j i • vacuum o else 0 := by
  simp only [annihilationTerm, pow_zero, Nat.add_zero, Nat.choose_zero_right,
    Nat.cast_one, one_mul, one_smul, LinearMap.comp_apply]
  change hmode o j (-(-4+(a : ℤ)+0+1)-1) (hmode o i (a : ℤ) (conformalState o)) = _
  rw [nonnegative_mode_conformalState]
  by_cases ha : a=1
  · subst a
    rw [if_pos rfl, if_pos rfl]
    change hmode o j ((1 : ℕ) : ℤ) (onCarrier o (create o 0 i) (vacuum o)) = _
    rw [nonnegative_mode_one_creator, if_pos rfl]
  · rw [if_neg ha, if_neg ha, map_zero]

theorem normal_central_state (o : Fin 12) (i j : Fin (BasisSize o)) :
    normalCoefficient o i 0 (heisenbergField o j) (-4) (conformalState o) =
      gram o j i • vacuum o := by
  classical
  rw [normalCoefficient_apply]
  simp only [creationTerm_central_state, finsum_zero, zero_add, annihilationTerm_central_state]
  rw [finsum_eq_single _ 1]
  · simp
  · intro a ha
    simp [ha]

/-- The coefficient giving c/2 is evaluated from the same Gram matrix.
Its rank is not inserted as a target scalar. -/
theorem conformalMode_two_state (o : Fin 12) :
    conformalMode o 2 (conformalState o) =
      ((BasisSize o : ℂ)/2) • vacuum o := by
  classical
  rw [conformalMode_normal_sum_apply]
  simp only [show -(2 : ℤ)-2 = -4 by rfl, normal_central_state, smul_smul]
  have inner (i : Fin (BasisSize o)) :
      (∑ j, (gramInv o i j * gram o j i) • vacuum o) = vacuum o := by
    rw [← Finset.sum_smul, gramInv_pairing, if_pos rfl, one_smul]
  simp_rw [inner]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin]
  rw [← Nat.cast_smul_eq_nsmul ℂ, smul_smul]
  congr 1
  ring

end HMT.IV.LatticeConformalCentralCoefficient
end

#print axioms HMT.IV.LatticeConformalCentralCoefficient.nonnegative_mode_create
#print axioms HMT.IV.LatticeConformalCentralCoefficient.nonnegative_mode_one_creator
#print axioms HMT.IV.LatticeConformalCentralCoefficient.nonnegative_mode_two_creators
#print axioms HMT.IV.LatticeConformalCentralCoefficient.gram_contract_vectors
#print axioms HMT.IV.LatticeConformalCentralCoefficient.gram_contract_vectors_right
#print axioms HMT.IV.LatticeConformalCentralCoefficient.nonnegative_mode_conformalState
#print axioms HMT.IV.LatticeConformalCentralCoefficient.creationTerm_central_state
#print axioms HMT.IV.LatticeConformalCentralCoefficient.annihilationTerm_central_state
#print axioms HMT.IV.LatticeConformalCentralCoefficient.normal_central_state
#print axioms HMT.IV.LatticeConformalCentralCoefficient.conformalMode_two_state
