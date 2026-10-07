import LatticeConformalState
import LatticeFieldTruncation

/-! Exact pointwise finite decomposition of the conformal zero-mode kernel.
The cutoff is supplied by the proved annihilation bound, not by truncating
the carrier. No identity with energy is a premise. -/

noncomputable section
namespace HMT.IV.LatticeNormalZeroMode
open LatticeCocycle LatticeOscillatorFock LatticeNormalOrderedField
open LatticeHeisenbergField LatticeHeisenbergModes
open scoped BigOperators

theorem creation_zero_mode (o : Fin 12) (i j : Fin (BasisSize o)) (a : ℕ) :
    creationTerm o i 0 (heisenbergField o j) (-2) a =
      (onCarrier o (create o a i)).comp (onCarrier o (annihilate o a j)) := by
  simp only [creationTerm, Nat.add_zero, Nat.choose_zero_right, Nat.cast_one,
    one_smul]
  change (onCarrier o (create o a i)).comp (hmode o j (-(-2-(a : ℤ))-1)) = _
  rw [show -(-2-(a : ℤ))-1 = ((a+1 : ℕ) : ℤ) by omega, hmode_castSucc]

theorem annihilation_zero_mode_zero (o : Fin 12) (i j : Fin (BasisSize o)) :
    annihilationTerm o i 0 (heisenbergField o j) (-2) 0 =
      (hmode o j 0).comp (hmode o i 0) := by
  simp only [annihilationTerm, pow_zero, Nat.add_zero, Nat.choose_zero_right,
    Nat.cast_one, one_mul, one_smul, Nat.cast_zero, add_zero,
    Int.cast_zero]
  rfl

theorem annihilation_zero_mode_succ (o : Fin 12) (i j : Fin (BasisSize o)) (a : ℕ) :
    annihilationTerm o i 0 (heisenbergField o j) (-2) (a+1) =
      (onCarrier o (create o a j)).comp (onCarrier o (annihilate o a i)) := by
  simp only [annihilationTerm, pow_zero, Nat.add_zero, Nat.choose_zero_right,
    Nat.cast_one, one_mul, one_smul, Nat.cast_zero, add_zero,
    hmode_castSucc]
  change (hmode o j (-(-2+((a+1 : ℕ) : ℤ)+1)-1)).comp
    (onCarrier o (annihilate o a i)) = _
  rw [show -(-2+((a+1 : ℕ) : ℤ)+1)-1 = Int.negSucc a by omega]
  exact congrArg (fun A => A.comp (onCarrier o (annihilate o a i)))
    (hmode_negSucc o j a)

theorem normal_zero_mode_cutoff (o : Fin 12) (i j : Fin (BasisSize o))
    (v : LatticeCarrier o) (N : ℕ)
    (hN : ∀ a ≥ N, ∀ l : Fin (BasisSize o), onCarrier o (annihilate o a l) v = 0) :
    normalCoefficient o i 0 (heisenbergField o j) (-2) v =
      hmode o j 0 (hmode o i 0 v) +
        ∑ a ∈ Finset.range N,
          (onCarrier o (create o a i) (onCarrier o (annihilate o a j) v) +
           onCarrier o (create o a j) (onCarrier o (annihilate o a i) v)) := by
  classical
  have hC : Function.support (fun a => creationTerm o i 0 (heisenbergField o j) (-2) a v)
      ⊆ (Finset.range N : Set ℕ) := by
    intro a ha
    simp only [Finset.mem_coe, Finset.mem_range]
    by_contra hn
    apply ha
    change creationTerm o i 0 (heisenbergField o j) (-2) a v = 0
    rw [creation_zero_mode, LinearMap.comp_apply, hN a (by omega), map_zero]
  have hA : Function.support (fun a => annihilationTerm o i 0 (heisenbergField o j) (-2) a v)
      ⊆ (Finset.range (N+1) : Set ℕ) := by
    intro a ha
    simp only [Finset.mem_coe, Finset.mem_range]
    by_contra hn
    cases a with
    | zero => omega
    | succ a =>
      apply ha
      change annihilationTerm o i 0 (heisenbergField o j) (-2) (a+1) v = 0
      rw [annihilation_zero_mode_succ, LinearMap.comp_apply, hN a (by omega), map_zero]
  rw [normalCoefficient_apply, finsum_eq_sum_of_support_subset _ hC,
    finsum_eq_sum_of_support_subset _ hA, Finset.sum_range_succ']
  simp only [creation_zero_mode, annihilation_zero_mode_succ,
    annihilation_zero_mode_zero, LinearMap.comp_apply, Finset.sum_add_distrib]
  abel

end HMT.IV.LatticeNormalZeroMode
end

#print axioms HMT.IV.LatticeNormalZeroMode.creation_zero_mode
#print axioms HMT.IV.LatticeNormalZeroMode.annihilation_zero_mode_zero
#print axioms HMT.IV.LatticeNormalZeroMode.annihilation_zero_mode_succ
#print axioms HMT.IV.LatticeNormalZeroMode.normal_zero_mode_cutoff
