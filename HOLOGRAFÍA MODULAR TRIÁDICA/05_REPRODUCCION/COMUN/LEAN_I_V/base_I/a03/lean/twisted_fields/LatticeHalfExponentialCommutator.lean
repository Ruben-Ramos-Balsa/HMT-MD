import LatticeHalfCreationExponential
import LatticeHalfAnnihilationExponential
import LatticeExponentialCommutator

/-! Mixed commutator for the half-integer creation exponential. The inherited
lattice pairing is obtained by differentiating the actual potential and its
finite coefficient expansion; neither BCH nor a twisted Jacobi identity is
assumed. All oscillator indices, coefficient degrees and Fock vectors occur. -/

noncomputable section
namespace HMT.IV.LatticeHalfExponentialCommutator
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeCreationExponential LatticeHalfCreationExponential
open LatticeHalfAnnihilationExponential LatticeExponentialCommutator
open PowerSeries
open scoped BigOperators

def halfChargedDerivation (o : Fin 12) (x : Lattice o) (n : ℕ) :
    Derivation ℂ (HalfFock o) (HalfFock o) :=
  annihilationScale n • chargedDerivation o x n

theorem halfChargedDerivation_apply (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v : HalfFock o) : halfChargedDerivation o x n v = chargeHalfAnnihilation o x n v := by
  rw [halfChargedDerivation, Derivation.smul_apply, chargedDerivation_apply,
    chargeHalfAnnihilation_eq_scale, LinearMap.smul_apply]

theorem halfChargedDerivation_creationState (o : Fin 12) (x y : Lattice o)
    (n m : ℕ) : halfChargedDerivation o x n (chargeCreationState o y m) =
      if n=m then (((n:ℂ)+1/2) * (integerPair o x y : ℂ)) • (1:HalfFock o) else 0 := by
  rw [halfChargedDerivation, Derivation.smul_apply, chargedDerivation_creationState,
    coordinatePair_eq_integerPair]
  split_ifs
  · rw [smul_smul, ← mul_assoc, annihilationScale_cancel]
  · exact smul_zero _

theorem derivative_halfCreationPotential (o : Fin 12) (x y : Lattice o) (n : ℕ) :
    seriesDerivation (halfChargedDerivation o x n) (halfCreationPotential o y) =
      (integerPair o x y : ℂ) • (X^(2*n+1) : PowerSeries (HalfFock o)) := by
  ext d
  rw [seriesDerivation_coefficient, coeff_smul, coeff_X_pow]
  by_cases he : d%2=0
  · obtain ⟨m, rfl⟩ : ∃m, d=2*m := ⟨d/2, by omega⟩
    rw [halfCreationPotential_coefficient_even, map_zero, if_neg (by omega), smul_zero]
  · obtain ⟨m, rfl⟩ : ∃m, d=2*m+1 := ⟨d/2, by omega⟩
    rw [halfCreationPotential_frequency_coefficient, Derivation.map_smul,
      halfChargedDerivation_creationState]
    by_cases h : n=m
    · subst m
      rw [if_pos rfl, if_pos rfl, smul_smul]
      have hn : (n:ℂ)+1/2 ≠ 0 := by
        have hnc : 2*(n:ℂ)+1 ≠ 0 := by
          exact_mod_cast (show 2*n+1 ≠ 0 by omega)
        intro hz
        apply hnc
        linear_combination 2*hz
      congr 1
      rw [one_div, ← mul_assoc, inv_mul_cancel₀ hn, one_mul]
    · rw [if_neg h, smul_zero, if_neg (by omega), smul_zero]

theorem derivative_halfCreationPower_coefficient (o : Fin 12) (x y : Lattice o)
    (n k d : ℕ) :
    halfChargedDerivation o x n (coeff (HalfFock o) d (halfCreationPotential o y ^ (k+1))) =
      if 2*n+1 ≤ d then ((k+1:ℂ) * (integerPair o x y : ℂ)) •
        coeff (HalfFock o) (d-(2*n+1)) (halfCreationPotential o y ^ k) else 0 := by
  rw [derivative_power_coefficient, derivative_halfCreationPotential,
    mul_smul_comm, coeff_smul, coeff_mul_X_pow']
  split_ifs <;> simp [smul_smul]

theorem halfCreationExponential_coefficient_extended (o : Fin 12) (y : Lattice o)
    (d N : ℕ) (hN : d ≤ N) :
    coeff (HalfFock o) d (halfCreationExponential o y) =
      ∑ k ∈ Finset.range (N+1), coeff ℂ k (PowerSeries.exp ℂ) •
        coeff (HalfFock o) d (halfCreationPotential o y ^ k) := by
  rw [halfCreationExponential_coefficient]
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro k _ hk
  have hdk : d<k := by simp only [Finset.mem_range] at hk; omega
  rw [LatticeHalfCreationExponential.potential_power_coefficient_zero o y d k hdk, smul_zero]

theorem annihilation_halfCreationExponential_coefficient (o : Fin 12) (x y : Lattice o)
    (n d : ℕ) : chargeHalfAnnihilation o x n
      (coeff (HalfFock o) d (halfCreationExponential o y)) =
      if 2*n+1 ≤ d then (integerPair o x y : ℂ) •
        coeff (HalfFock o) (d-(2*n+1)) (halfCreationExponential o y) else 0 := by
  rw [← halfChargedDerivation_apply]
  cases d with
  | zero => rw [halfCreationExponential_constant]; simp
  | succ d =>
    rw [halfCreationExponential_coefficient, map_sum, Finset.sum_range_succ']
    simp only [pow_zero, coeff_one, Nat.succ_ne_zero, if_false,
      smul_zero, map_zero, add_zero]
    by_cases hd : 2*n+1 ≤ d+1
    · rw [if_pos hd, halfCreationExponential_coefficient_extended o y _ d (by omega),
        Finset.smul_sum]
      apply Finset.sum_congr rfl
      intro k _
      rw [Derivation.map_smul, derivative_halfCreationPower_coefficient, if_pos hd,
        smul_smul, ← mul_assoc, exp_coefficient_succ_mul, smul_smul, mul_comm]
    · rw [if_neg hd]
      apply Finset.sum_eq_zero
      intro k _
      rw [Derivation.map_smul, derivative_halfCreationPower_coefficient, if_neg hd, smul_zero]

theorem mixed_half_exponential_commutator (o : Fin 12) (x y : Lattice o)
    (n d : ℕ) (v : HalfFock o) :
    chargeHalfAnnihilation o x n (halfCreationExponentialMode o y d v) -
      halfCreationExponentialMode o y d (chargeHalfAnnihilation o x n v) =
      if 2*n+1 ≤ d then (integerPair o x y : ℂ) •
        halfCreationExponentialMode o y (d-(2*n+1)) v else 0 := by
  change chargeHalfAnnihilation o x n
      (coeff (HalfFock o) d (halfCreationExponential o y)*v) -
    coeff (HalfFock o) d (halfCreationExponential o y) * chargeHalfAnnihilation o x n v = _
  rw [← halfChargedDerivation_apply, Derivation.leibniz]
  simp only [smul_eq_mul, halfChargedDerivation_apply]
  rw [annihilation_halfCreationExponential_coefficient]
  split_ifs <;> simp [halfCreationExponentialMode, smul_eq_mul, Algebra.smul_def,
    mul_comm, mul_left_comm, mul_assoc]

end HMT.IV.LatticeHalfExponentialCommutator
end

#print axioms HMT.IV.LatticeHalfExponentialCommutator.halfChargedDerivation_apply
#print axioms HMT.IV.LatticeHalfExponentialCommutator.halfChargedDerivation_creationState
#print axioms HMT.IV.LatticeHalfExponentialCommutator.derivative_halfCreationPotential
#print axioms HMT.IV.LatticeHalfExponentialCommutator.derivative_halfCreationPower_coefficient
#print axioms HMT.IV.LatticeHalfExponentialCommutator.halfCreationExponential_coefficient_extended
#print axioms HMT.IV.LatticeHalfExponentialCommutator.annihilation_halfCreationExponential_coefficient
#print axioms HMT.IV.LatticeHalfExponentialCommutator.mixed_half_exponential_commutator
