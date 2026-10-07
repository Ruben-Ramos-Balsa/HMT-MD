import LatticeTranslationCommutators
import LatticeAnnihilationRecurrence

/-!
The negative charged oscillator acts on the existing annihilation exponential.
The minus sign of its potential cancels the reversed Heisenberg commutator;
the frequency n+1 cancels its denominator. No commutation relation is assumed.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeNegativeExponential

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialCommutator HMT.IV.LatticeTranslationCommutators
open PowerSeries
open scoped BigOperators

theorem chargeCreation_annihilation (o : Fin 12) (x y : Lattice o) (n m : ℕ) :
    chargeCreation o x n * chargeAnnihilation o y m -
      chargeAnnihilation o y m * chargeCreation o x n =
      (if m=n then -((m+1 : ℂ) * (integerPair o x y : ℂ)) else 0) •
        (1 : Module.End ℂ (Fock o)) := by
  apply LinearMap.ext
  intro v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    Module.End.one_apply, chargeCreation_apply, chargeAnnihilation_product,
    chargeAnnihilation_creationState, integerPair_comm o y x]
  (split_ifs <;> simp [Algebra.smul_def]); ring

theorem creation_potential_commutator (o : Fin 12) (x y : Lattice o) (n : ℕ) :
    C (Module.End ℂ (Fock o)) (chargeCreation o x n) * annihilationPotential o y -
      annihilationPotential o y * C (Module.End ℂ (Fock o)) (chargeCreation o x n) =
      (integerPair o x y : ℂ) • (X^(n+1) : EndSeries o) := by
  apply PowerSeries.ext
  intro d
  rw [map_sub, coeff_C_mul, coeff_mul_C, coeff_smul, coeff_X_pow]
  cases d with
  | zero => simp [annihilationPotential_constant]
  | succ m =>
    rw [annihilationPotential_coefficient_succ, mul_smul_comm, smul_mul_assoc,
      ← smul_sub, chargeCreation_annihilation]
    by_cases h : m=n
    · subst m
      simp only [if_pos rfl, smul_smul]
      have hn : (n+1 : ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero n
      congr 1
      field_simp
    · simp [h, Nat.succ.injEq]

private theorem central_commutator_power {R : Type*} [Ring R]
    (a p z : R) (h : a*p-p*a=z) (hz : Commute p z) (k : ℕ) :
    a*p^(k+1)-p^(k+1)*a = (k+1) • (z*p^k) := by
  induction k with
  | zero => simpa using h
  | succ k ih =>
    calc
      a*p^(k+1+1)-p^(k+1+1)*a =
          (a*p^(k+1)-p^(k+1)*a)*p + p^(k+1)*(a*p-p*a) := by
            rw [pow_succ]
            noncomm_ring
      _ = (k+1) • (z*p^k)*p + p^(k+1)*z := by rw [ih, h]
      _ = (k+1+1) • (z*p^(k+1)) := by
        rw [smul_mul_assoc, mul_assoc, ← pow_succ, (hz.pow_left (k+1)).eq]
        simp only [succ_nsmul]

theorem creation_power_commutator (o : Fin 12) (x y : Lattice o)
    (n k d : ℕ) :
    chargeCreation o x n * coeff (Module.End ℂ (Fock o)) d
        (annihilationPotential o y ^ (k+1)) -
      coeff (Module.End ℂ (Fock o)) d (annihilationPotential o y ^ (k+1)) *
        chargeCreation o x n =
      if n+1 ≤ d then ((k+1 : ℂ) * (integerPair o x y : ℂ)) •
        coeff (Module.End ℂ (Fock o)) (d-(n+1)) (annihilationPotential o y ^ k)
      else 0 := by
  have h := congrArg (coeff (Module.End ℂ (Fock o)) d)
    (central_commutator_power
      (C (Module.End ℂ (Fock o)) (chargeCreation o x n))
      (annihilationPotential o y)
      ((integerPair o x y : ℂ) • (X^(n+1) : EndSeries o))
      (creation_potential_commutator o x y n)
      ((commute_X_pow (annihilationPotential o y) (n+1)).smul_right _) k)
  rw [map_sub, coeff_C_mul, coeff_mul_C, map_nsmul, smul_mul_assoc,
    coeff_smul, coeff_X_pow_mul'] at h
  rw [h]
  split_ifs
  · rw [← Nat.cast_smul_eq_nsmul ℂ, smul_smul]
    simp only [Nat.cast_add, Nat.cast_one]
  · simp

theorem chargeCreation_exponentialCoefficient (o : Fin 12) (x y : Lattice o)
    (n d : ℕ) :
    chargeCreation o x n * exponentialCoefficient o y d -
      exponentialCoefficient o y d * chargeCreation o x n =
      if n+1 ≤ d then (integerPair o x y : ℂ) •
        exponentialCoefficient o y (d-(n+1)) else 0 := by
  cases d with
  | zero =>
    rw [annihilationExponential_constant]
    change _ * (1 : Module.End ℂ (Fock o)) - 1 * _ = _
    simp
  | succ d =>
    rw [exponentialCoefficient, Finset.mul_sum, Finset.sum_mul,
      ← Finset.sum_sub_distrib, Finset.sum_range_succ']
    simp only [pow_zero, coeff_one, Nat.succ_ne_zero, if_false,
      smul_zero, mul_zero, zero_mul, sub_self, add_zero,
      mul_smul_comm, smul_mul_assoc, ← smul_sub]
    by_cases hd : n+1 ≤ d+1
    · rw [if_pos hd, exponentialCoefficient_cutoff o y _ d (by omega), Finset.smul_sum]
      apply Finset.sum_congr rfl
      intro k _
      rw [creation_power_commutator, if_pos hd, smul_smul, ← mul_assoc,
        exp_coefficient_succ_mul, smul_smul, mul_comm]
    · rw [if_neg hd]
      apply Finset.sum_eq_zero
      intro k _
      rw [creation_power_commutator, if_neg hd, smul_zero]

theorem chargeCreation_exponentialCoefficient_apply (o : Fin 12) (x y : Lattice o)
    (n d : ℕ) (v : Fock o) :
    chargeCreation o x n (exponentialCoefficient o y d v) -
      exponentialCoefficient o y d (chargeCreation o x n v) =
      if n+1 ≤ d then (integerPair o x y : ℂ) •
        exponentialCoefficient o y (d-(n+1)) v else 0 := by
  have h := LinearMap.congr_fun (chargeCreation_exponentialCoefficient o x y n d) v
  split_ifs at h ⊢ <;> exact h

end HMT.IV.LatticeNegativeExponential
end

#print axioms HMT.IV.LatticeNegativeExponential.chargeCreation_annihilation
#print axioms HMT.IV.LatticeNegativeExponential.creation_potential_commutator
#print axioms HMT.IV.LatticeNegativeExponential.creation_power_commutator
#print axioms HMT.IV.LatticeNegativeExponential.chargeCreation_exponentialCoefficient
#print axioms HMT.IV.LatticeNegativeExponential.chargeCreation_exponentialCoefficient_apply
