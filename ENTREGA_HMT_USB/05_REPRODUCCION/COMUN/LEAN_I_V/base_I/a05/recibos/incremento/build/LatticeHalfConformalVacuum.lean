import LatticeHalfConformalModes
import LatticeGramSymmetry
import LatticeConformalCentralCharge

/-!
The scalar vacuum correction forced by the real half-integer oscillators.
The unshifted modes first give [Q1,Q-1]1 = rank/8 times the vacuum. A scalar
correction of Q0 therefore satisfies the zero-central-term relation at (1,-1)
exactly when it equals rank/16. No target rank-normalized scalar is inserted
into the oscillator definitions and no full Virasoro assertion is made here.
-/

noncomputable section
namespace HMT.IV.LatticeHalfConformalVacuum

open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfConformalModes LatticeGramDual LatticeGramSymmetry
open scoped BigOperators

theorem halfAnnihilate_single (o : Fin 12) (a : ℕ) (i p : Fin (BasisSize o)) :
    halfAnnihilate o a i (create o 0 p 1) =
      (if a=0 then ((a:ℂ)+1/2)*gram o i p else 0) • (1 : HalfFock o) := by
  simpa only [halfAnnihilate_vacuum, map_zero, sub_zero] using
    half_mode_ccr_apply o a 0 i p (1 : HalfFock o)

theorem halfAnnihilate_double_nonzero (o : Fin 12) (a : ℕ)
    (i p q : Fin (BasisSize o)) (ha : a≠0) :
    halfAnnihilate o a i (create o 0 p (create o 0 q 1))=0 := by
  have h := half_mode_ccr_apply o a 0 i p (create o 0 q 1)
  simpa only [halfAnnihilate_single, if_neg ha, zero_smul, map_zero, sub_zero] using h

theorem halfAnnihilate_double_zero (o : Fin 12) (i p q : Fin (BasisSize o)) :
    halfAnnihilate o 0 i (create o 0 p (create o 0 q 1)) =
      ((1/2:ℂ)*gram o i q) • create o 0 p 1 +
        ((1/2:ℂ)*gram o i p) • create o 0 q 1 := by
  have h := half_mode_ccr_apply o 0 0 i p (create o 0 q 1)
  simp only [halfAnnihilate_single, if_pos rfl, ite_true, Nat.cast_zero, zero_add,
    map_smul] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h, add_comm]

theorem half_double_contraction (o : Fin 12) (i j p q : Fin (BasisSize o)) :
    halfAnnihilate o 0 j (halfAnnihilate o 0 i (create o 0 p (create o 0 q 1))) =
      ((1/4:ℂ)*(gram o i q*gram o j p+gram o i p*gram o j q)) • (1 : HalfFock o) := by
  rw [halfAnnihilate_double_zero]
  simp only [map_add, map_smul, halfAnnihilate_single, if_pos rfl, ite_true,
    Nat.cast_zero, zero_add, smul_smul]
  module

theorem halfNormalMode_one_double (o : Fin 12) (i j p q : Fin (BasisSize o)) :
    halfNormalMode o i j 1 (create o 0 p (create o 0 q 1)) =
      ((1/4:ℂ)*(gram o i q*gram o j p+gram o i p*gram o j q)) • (1 : HalfFock o) := by
  have hc (a : ℕ) : creationHalfTerm o i j 1 a (create o 0 p (create o 0 q 1))=0 := by
    have hk : (1:ℤ)+(a:ℤ)=((a+1:ℕ):ℤ) := by omega
    simp only [creationHalfTerm, LinearMap.comp_apply, hk, halfMode_ofNat,
      halfAnnihilate_double_nonzero o (a+1) j p q (by omega), map_zero]
  have ha (a : ℕ) (hne : a≠0) :
      annihilationHalfTerm o i j 1 a (create o 0 p (create o 0 q 1))=0 := by
    simp only [annihilationHalfTerm, LinearMap.comp_apply,
      halfAnnihilate_double_nonzero o a i p q hne, map_zero]
  rw [halfNormalMode_apply, finsum_eq_single _ 0 ha]
  simp only [hc, finsum_zero, zero_add, annihilationHalfTerm, LinearMap.comp_apply,
    Nat.cast_zero, sub_zero, sub_self, halfMode_ofNat]
  exact half_double_contraction o i j p q

theorem gram_double_contraction (o : Fin 12) (p q : Fin (BasisSize o)) :
    (∑ i, ∑ j, gramInv o i j *
      (gram o i q*gram o j p+gram o i p*gram o j q)) = 2*gram o p q := by
  classical
  have inner (i : Fin (BasisSize o)) :
      (∑ j, gramInv o i j *
        (gram o i q*gram o j p+gram o i p*gram o j q)) =
      gram o i q*(if i=p then 1 else 0) + gram o i p*(if i=q then 1 else 0) := by
    simp_rw [mul_add]
    rw [Finset.sum_add_distrib]
    have h (r s : Fin (BasisSize o)) :
        (∑ j, gramInv o i j * (gram o i r * gram o j s)) =
          gram o i r * (if i=s then 1 else 0) := by
      calc
        _ = gram o i r * ∑ j, gramInv o i j * gram o j s := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro j _
          ring
        _ = _ := by rw [gramInv_pairing]
    rw [h q p, h p q]
  simp_rw [inner]
  rw [Finset.sum_add_distrib]
  simp only [mul_ite, mul_one, mul_zero]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, if_pos]
  rw [gram_symmetric o q p]
  ring

theorem quadraticMode_one_double (o : Fin 12) (p q : Fin (BasisSize o)) :
    quadraticMode o 1 (create o 0 p (create o 0 q 1)) =
      ((1/4:ℂ)*gram o p q) • (1 : HalfFock o) := by
  rw [quadraticMode_apply]
  simp_rw [halfNormalMode_one_double, smul_smul]
  have h (i j : Fin (BasisSize o)) :
      gramInv o i j * ((1/4:ℂ)*(gram o i q*gram o j p+gram o i p*gram o j q)) =
      (1/4:ℂ)*(gramInv o i j*(gram o i q*gram o j p+gram o i p*gram o j q)) := by
    ring
  simp_rw [h]
  simp only [← Finset.sum_smul, ← Finset.mul_sum]
  rw [gram_double_contraction]
  module

theorem quadratic_commutator_one_neg_one_vacuum (o : Fin 12) :
    quadraticMode o 1 (quadraticMode o (-1) 1) -
      quadraticMode o (-1) (quadraticMode o 1 1) =
        ((BasisSize o : ℂ)/8) • (1 : HalfFock o) := by
  rw [quadraticMode_nonnegative_vacuum o 1 (by omega), map_zero, sub_zero,
    quadraticMode_neg_one_vacuum]
  simp only [map_smul, map_sum, quadraticMode_one_double, smul_smul]
  have h (i j : Fin (BasisSize o)) :
      gramInv o i j * ((1/4:ℂ)*gram o i j) =
        (1/4:ℂ)*(gramInv o i j*gram o i j) := by ring
  simp_rw [h]
  simp only [← Finset.sum_smul, ← Finset.mul_sum]
  rw [LatticeConformalCentralCharge.gram_trace]
  module

def shiftedQuadraticMode (o : Fin 12) (c : ℂ) (m : ℤ) :
    Module.End ℂ (HalfFock o) :=
  quadraticMode o m + if m=0 then c • LinearMap.id else 0

theorem shifted_zero_vacuum (o : Fin 12) (c : ℂ) :
    shiftedQuadraticMode o c 0 1 = c • (1 : HalfFock o) := by
  simp only [shiftedQuadraticMode, if_pos rfl, ite_true, LinearMap.add_apply,
    LinearMap.smul_apply, LinearMap.id_apply,
    quadraticMode_nonnegative_vacuum o 0 (by omega), zero_add]

theorem vacuum_shift_forced (o : Fin 12) (c : ℂ) :
    (shiftedQuadraticMode o c 1 (shiftedQuadraticMode o c (-1) 1) -
      shiftedQuadraticMode o c (-1) (shiftedQuadraticMode o c 1 1) =
        (2:ℂ) • shiftedQuadraticMode o c 0 1) ↔ c=(BasisSize o:ℂ)/16 := by
  have h1 : shiftedQuadraticMode o c 1=quadraticMode o 1 := by
    simp only [shiftedQuadraticMode, if_neg (by norm_num : (1:ℤ)≠0), add_zero]
  have hn1 : shiftedQuadraticMode o c (-1)=quadraticMode o (-1) := by
    simp only [shiftedQuadraticMode, if_neg (by norm_num : (-1:ℤ)≠0), add_zero]
  rw [h1, hn1, quadratic_commutator_one_neg_one_vacuum, shifted_zero_vacuum, smul_smul]
  constructor
  · intro h
    have hc : (BasisSize o:ℂ)/8=2*c :=
      (smul_left_injective ℂ (one_ne_zero : (1 : HalfFock o)≠0)) h
    linear_combination -hc/2
  · intro hc
    rw [hc]
    congr 1
    ring

end HMT.IV.LatticeHalfConformalVacuum
end

#print axioms HMT.IV.LatticeHalfConformalVacuum.halfAnnihilate_single
#print axioms HMT.IV.LatticeHalfConformalVacuum.halfAnnihilate_double_nonzero
#print axioms HMT.IV.LatticeHalfConformalVacuum.halfAnnihilate_double_zero
#print axioms HMT.IV.LatticeHalfConformalVacuum.half_double_contraction
#print axioms HMT.IV.LatticeHalfConformalVacuum.halfNormalMode_one_double
#print axioms HMT.IV.LatticeHalfConformalVacuum.gram_double_contraction
#print axioms HMT.IV.LatticeHalfConformalVacuum.quadraticMode_one_double
#print axioms HMT.IV.LatticeHalfConformalVacuum.quadratic_commutator_one_neg_one_vacuum
#print axioms HMT.IV.LatticeHalfConformalVacuum.shiftedQuadraticMode
#print axioms HMT.IV.LatticeHalfConformalVacuum.shifted_zero_vacuum
#print axioms HMT.IV.LatticeHalfConformalVacuum.vacuum_shift_forced
