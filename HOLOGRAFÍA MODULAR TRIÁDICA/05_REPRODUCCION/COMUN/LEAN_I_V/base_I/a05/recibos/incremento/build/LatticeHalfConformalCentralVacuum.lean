import LatticeHalfConformalVacuum
import LatticeHalfConformalHeisenberg

/-!
The (2,-2) vacuum calculation on the same half-integer oscillator Fock space.
Only the real quadratic modes and their proved oscillator commutators enter.
The rank/16 shift was derived in LatticeHalfConformalVacuum; after that shift,
the vacuum defect is rank/2. This is a base calculation for subsequent
Virasoro work, not an assumption of the complete relations.
-/

noncomputable section
namespace HMT.IV.LatticeHalfConformalCentralVacuum

open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfConformalModes LatticeHalfConformalVacuum
open LatticeHalfConformalHeisenberg LatticeGramDual
open scoped BigOperators

theorem halfNormalMode_neg_two_vacuum (o : Fin 12)
    (i j : Fin (BasisSize o)) :
    halfNormalMode o i j (-2) 1 =
      create o 0 i (create o 1 j 1) + create o 1 i (create o 0 j 1) := by
  classical
  have hc : Function.support (fun a => creationHalfTerm o i j (-2) a 1)
      ⊆ (Finset.range 2 : Set ℕ) := by
    intro a ha
    simp only [Finset.mem_coe, Finset.mem_range]
    by_contra hn
    apply ha
    simp only [creationHalfTerm, LinearMap.comp_apply,
      halfMode_nonnegative_vacuum o j (-2+a) (by omega), map_zero]
  have ha (a : ℕ) : annihilationHalfTerm o i j (-2) a 1=0 := by
    simp only [annihilationHalfTerm, LinearMap.comp_apply,
      halfAnnihilate_vacuum, map_zero]
  rw [halfNormalMode_apply, finsum_eq_sum_of_support_subset _ hc]
  simp only [ha, finsum_zero, add_zero, Finset.sum_range_succ,
    Finset.range_zero, Finset.sum_empty, zero_add, creationHalfTerm,
    LinearMap.comp_apply, Nat.cast_zero, Nat.cast_one, add_zero]
  rfl

theorem quadraticMode_neg_two_vacuum (o : Fin 12) :
    quadraticMode o (-2) 1=
      (2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j •
        (create o 0 i (create o 1 j 1) + create o 1 i (create o 0 j 1)) := by
  simp only [quadraticMode_apply, halfNormalMode_neg_two_vacuum]

theorem quadraticMode_two_single (o : Fin 12) (i : Fin (BasisSize o))
    (a : ℕ) (ha : a<2) : quadraticMode o 2 (create o a i 1)=0 := by
  have h := quadraticMode_half_commutator_apply o i 2 (Int.negSucc a) (1 : HalfFock o)
  simpa only [halfMode_negSucc, quadraticMode_nonnegative_vacuum o 2 (by omega),
    map_zero, sub_zero,
    halfMode_nonnegative_vacuum o i (2+Int.negSucc a) (by omega), smul_zero] using h

theorem quadraticMode_two_pair (o : Fin 12) (i j : Fin (BasisSize o))
    (a b : ℕ) (hab : a+b=1) :
    quadraticMode o 2 (create o a i (create o b j 1)) =
      (((a:ℂ)+1/2)*((b:ℂ)+1/2)*gram o i j) • (1 : HalfFock o) := by
  have h := quadraticMode_half_commutator_apply o i 2 (Int.negSucc a) (create o b j 1)
  have hk : (2:ℤ)+Int.negSucc a=(b:ℤ) := by omega
  have hc : (-(Int.negSucc a:ℂ)-1/2)=((a:ℂ)+1/2) := by
    push_cast
    ring
  have hsingle := half_mode_ccr_apply o b b i j (1 : HalfFock o)
  simp only [halfAnnihilate_vacuum, map_zero, sub_zero, if_pos rfl, ite_true] at hsingle
  simpa only [halfMode_negSucc, quadraticMode_two_single o j b (by omega),
    map_zero, sub_zero, hk, halfMode_ofNat, hsingle, hc, smul_smul, mul_assoc] using h

theorem quadraticMode_two_pair_zero_one (o : Fin 12) (i j : Fin (BasisSize o)) :
    quadraticMode o 2 (create o 0 i (create o 1 j 1)) =
      ((3/4:ℂ)*gram o i j) • (1 : HalfFock o) := by
  have h := quadraticMode_two_pair o i j 0 1 (by omega)
  norm_num at h
  exact h

theorem quadraticMode_two_pair_one_zero (o : Fin 12) (i j : Fin (BasisSize o)) :
    quadraticMode o 2 (create o 1 i (create o 0 j 1)) =
      ((3/4:ℂ)*gram o i j) • (1 : HalfFock o) := by
  have h := quadraticMode_two_pair o i j 1 0 (by omega)
  norm_num at h
  exact h

theorem quadratic_commutator_two_neg_two_vacuum (o : Fin 12) :
    quadraticMode o 2 (quadraticMode o (-2) 1) -
      quadraticMode o (-2) (quadraticMode o 2 1) =
        (3*(BasisSize o : ℂ)/4) • (1 : HalfFock o) := by
  rw [quadraticMode_nonnegative_vacuum o 2 (by omega), map_zero, sub_zero,
    quadraticMode_neg_two_vacuum]
  simp only [map_smul, map_sum, map_add,
    quadraticMode_two_pair_zero_one, quadraticMode_two_pair_one_zero]
  have h (i j : Fin (BasisSize o)) :
      gramInv o i j • (((3/4:ℂ)*gram o i j) • (1 : HalfFock o) +
        ((3/4:ℂ)*gram o i j) • (1 : HalfFock o)) =
      ((3/2:ℂ)*(gramInv o i j*gram o i j)) • (1 : HalfFock o) := by
    module
  simp_rw [h]
  simp only [← Finset.sum_smul, ← Finset.mul_sum]
  rw [LatticeConformalCentralCharge.gram_trace]
  module

theorem shifted_two_vacuum_defect (o : Fin 12) (c : ℂ) :
    shiftedQuadraticMode o c 2 (shiftedQuadraticMode o c (-2) 1) -
      shiftedQuadraticMode o c (-2) (shiftedQuadraticMode o c 2 1) -
        (4:ℂ) • shiftedQuadraticMode o c 0 1 =
      (3*(BasisSize o:ℂ)/4-4*c) • (1 : HalfFock o) := by
  have h2 : shiftedQuadraticMode o c 2=quadraticMode o 2 := by
    simp only [shiftedQuadraticMode, if_neg (by norm_num : (2:ℤ)≠0), add_zero]
  have hn2 : shiftedQuadraticMode o c (-2)=quadraticMode o (-2) := by
    simp only [shiftedQuadraticMode, if_neg (by norm_num : (-2:ℤ)≠0), add_zero]
  rw [h2, hn2, quadratic_commutator_two_neg_two_vacuum, shifted_zero_vacuum]
  module

theorem forced_shift_central_vacuum (o : Fin 12) :
    shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 2
        (shiftedQuadraticMode o ((BasisSize o:ℂ)/16) (-2) 1) -
      shiftedQuadraticMode o ((BasisSize o:ℂ)/16) (-2)
        (shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 2 1) -
      (4:ℂ) • shiftedQuadraticMode o ((BasisSize o:ℂ)/16) 0 1 =
        ((BasisSize o:ℂ)/2) • (1 : HalfFock o) := by
  rw [shifted_two_vacuum_defect]
  congr 1
  ring

end HMT.IV.LatticeHalfConformalCentralVacuum
end

#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.halfNormalMode_neg_two_vacuum
#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.quadraticMode_neg_two_vacuum
#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.quadraticMode_two_single
#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.quadraticMode_two_pair
#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.quadraticMode_two_pair_zero_one
#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.quadraticMode_two_pair_one_zero
#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.quadratic_commutator_two_neg_two_vacuum
#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.shifted_two_vacuum_defect
#print axioms HMT.IV.LatticeHalfConformalCentralVacuum.forced_shift_central_vacuum
