import LatticeTranslationOperator
import Mathlib.RingTheory.PowerSeries.Derivative

/-!
Translation of every state created from the vacuum. The exponential
recurrence is proved from finite power sums and the actual oscillator
derivation; differential covariance of all charged fields is not assumed.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeTranslationVacuum

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeChargedVertexField
open HMT.IV.LatticeOscillatorTranslation
open PowerSeries
open scoped BigOperators TensorProduct

abbrev A (o : Fin 12) := Fock o

def coefficientTranslation (o : Fin 12) :
    Derivation ℂ (PowerSeries (A o)) (PowerSeries (A o)) where
  toFun f := PowerSeries.mk fun n => translation o (coeff (A o) n f)
  map_add' f g := by ext n; simp [map_add]
  map_smul' z f := by ext n; simp [Derivation.map_smul]
  map_one_eq_zero' := by
    ext n
    change coeff (A o) n (PowerSeries.mk fun m => translation o (coeff (A o) m 1)) = 0
    simp only [coeff_mk, coeff_one, map_zero]
    split_ifs <;> simp
  leibniz' f g := by
    ext n
    change coeff (A o) n (PowerSeries.mk fun m => translation o (coeff (A o) m (f*g))) =
      coeff (A o) n (f * (PowerSeries.mk fun m => translation o (coeff (A o) m g)) +
        g * (PowerSeries.mk fun m => translation o (coeff (A o) m f)))
    simp only [coeff_mk, coeff_mul, map_sum, (translation o).leibniz,
      smul_eq_mul, map_add, Finset.sum_add_distrib]
    congr 1
    rw [← Finset.Nat.sum_antidiagonal_swap]
    rfl

@[simp] theorem coefficientTranslation_coeff (o : Fin 12)
    (f : PowerSeries (A o)) (d : ℕ) :
    coeff (A o) d (coefficientTranslation o f) =
      translation o (coeff (A o) d f) := by
  change coeff (A o) d (PowerSeries.mk fun n => translation o (coeff (A o) n f)) = _
  exact coeff_mk _ _

def delta (o : Fin 12) : Derivation ℂ (PowerSeries (A o)) (PowerSeries (A o)) :=
  (PowerSeries.derivative (A o)).restrictScalars ℂ - coefficientTranslation o

theorem delta_coeff (o : Fin 12) (f : PowerSeries (A o)) (d : ℕ) :
    coeff (A o) d (delta o f) =
      (d+1 : ℂ) • coeff (A o) (d+1) f - translation o (coeff (A o) d f) := by
  simp only [delta, Derivation.sub_apply, map_sub, Derivation.restrictScalars_apply,
    PowerSeries.coeff_derivative, coefficientTranslation_coeff,
    Algebra.smul_def, map_add, map_natCast, map_one]
  rw [mul_comm]

theorem translation_chargeCreationState (o : Fin 12) (x : Lattice o) (n : ℕ) :
    translation o (chargeCreationState o x n) =
      (n+1 : ℂ) • chargeCreationState o x (n+1) := by
  simp only [chargeCreationState, chargeModeVector, map_sum, map_smul,
    Derivation.map_smul]
  change (∑ i : Fin (BasisSize o), ((latticeBasis o).repr x i : ℂ) •
    translation o (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o (n,i)))) = _
  simp only [translation_mode, Finset.smul_sum, smul_smul]
  apply Finset.sum_congr rfl
  intro i _
  rw [mul_comm]
  rfl

theorem delta_potential (o : Fin 12) (x : Lattice o) :
    delta o (creationPotential o x) = C (A o) (chargeCreationState o x 0) := by
  ext d
  rw [delta_coeff]
  cases d with
  | zero =>
    simp [creationPotential_coefficient_succ, coeff_zero_eq_constantCoeff_apply,
      creationPotential_constant]
  | succ n =>
    rw [creationPotential_coefficient_succ, creationPotential_coefficient_succ,
      Derivation.map_smul, translation_chargeCreationState]
    simp only [coeff_succ_C, smul_smul]
    have h1 : (n+1 : ℂ) ≠ 0 := by exact_mod_cast (by omega : n+1≠0)
    have h2 : (n+1+1 : ℂ) ≠ 0 := by exact_mod_cast (by omega : n+1+1≠0)
    have ha : ((n+1+1 : ℕ) : ℂ) * (1 / ((n+1+1 : ℕ) : ℂ)) = 1 :=
      mul_one_div_cancel (by exact_mod_cast (by omega : n+1+1≠0))
    have hb : (1 / (n+1 : ℂ)) * (n+1 : ℂ) = 1 := one_div_mul_cancel h1
    norm_num only [Nat.cast_add, Nat.cast_one] at *
    rw [ha, hb, one_smul, sub_self]

def expPartial (o : Fin 12) (x : Lattice o) (N : ℕ) : PowerSeries (A o) :=
  ∑ k ∈ Finset.range N, coeff ℂ k (PowerSeries.exp ℂ) • creationPotential o x ^ k

theorem expPartial_coeff (o : Fin 12) (x : Lattice o) (N d : ℕ) (hd : d < N) :
    coeff (A o) d (expPartial o x N) = coeff (A o) d (creationExponential o x) := by
  rw [expPartial, map_sum, creationExponential_coefficient]
  simp only [coeff_smul]
  symm
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro k _ hk
  have hk' : d < k := by simpa only [Finset.mem_range, not_lt] using hk
  rw [LatticeCreationExponential.potential_power_coefficient_zero o x d k hk', smul_zero]

theorem exp_factorial_step (k : ℕ) :
    coeff ℂ (k+1) (PowerSeries.exp ℂ) * (k+1 : ℂ) =
      coeff ℂ k (PowerSeries.exp ℂ) := by
  simp only [coeff_exp, Nat.factorial_succ, map_div₀, map_one, map_mul,
    map_natCast, Nat.cast_add, Nat.cast_one]
  have hk : (k+1 : ℂ) ≠ 0 := by exact_mod_cast (by omega : k+1≠0)
  have hf : (k.factorial : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero k
  field_simp

theorem delta_expPartial (o : Fin 12) (x : Lattice o) (N : ℕ) :
    delta o (expPartial o x (N+1)) =
      C (A o) (chargeCreationState o x 0) * expPartial o x N := by
  unfold expPartial
  rw [map_sum, Finset.sum_range_succ', Finset.mul_sum]
  simp only [pow_zero, Derivation.map_one_eq_zero, Derivation.map_smul, smul_zero, add_zero]
  apply Finset.sum_congr rfl
  intro k _
  rw [(delta o).leibniz_pow, delta_potential]
  simp only [Nat.add_sub_cancel, smul_eq_mul]
  rw [← Nat.cast_smul_eq_nsmul ℂ]
  rw [smul_smul, Nat.cast_add, Nat.cast_one, exp_factorial_step]
  simp only [Algebra.smul_def]
  ring

theorem creation_exponential_recurrence (o : Fin 12) (x : Lattice o) (d : ℕ) :
    translation o (coeff (A o) d (creationExponential o x)) +
      chargeCreationState o x 0 * coeff (A o) d (creationExponential o x) =
      (d+1 : ℂ) • coeff (A o) (d+1) (creationExponential o x) := by
  have h := congrArg (coeff (A o) d) (delta_expPartial o x (d+1))
  rw [delta_coeff, coeff_C_mul,
    expPartial_coeff o x (d+1+1) (d+1) (by omega),
    expPartial_coeff o x (d+1+1) d (by omega),
    expPartial_coeff o x (d+1) d (by omega)] at h
  rw [sub_eq_iff_eq_add] at h
  rw [h, add_comm]

theorem translation_vacuum_coefficient_nonnegative (o : Fin 12)
    (x : Lattice o) (d : ℕ) :
    LatticeTranslationOperator.translation o
      (fieldCoefficient o x (d : ℤ) (vacuum o)) =
      (d+1 : ℂ) • fieldCoefficient o x ((d+1 : ℕ) : ℤ) (vacuum o) := by
  rw [fieldCoefficient_vacuum_nonnegative, fieldCoefficient_vacuum_nonnegative,
    creationExponentialMode_vacuum, creationExponentialMode_vacuum,
    LatticeTranslationOperator.translation_pure, creation_exponential_recurrence]
  exact (TensorProduct.smul_tmul' _ _ _).symm

theorem translation_vacuum_coefficient (o : Fin 12)
    (x : Lattice o) (k : ℤ) :
    LatticeTranslationOperator.translation o
      (fieldCoefficient o x k (vacuum o)) =
      ((k : ℂ)+1) • fieldCoefficient o x (k+1) (vacuum o) := by
  by_cases hk : 0 ≤ k
  · lift k to ℕ using hk
    simpa only [Int.natCast_add, Int.natCast_one, Int.cast_natCast] using
      translation_vacuum_coefficient_nonnegative o x k
  · have hneg : k < 0 := by omega
    rw [fieldCoefficient_vacuum_negative o x k hneg, map_zero]
    by_cases hn : k+1 < 0
    · rw [fieldCoefficient_vacuum_negative o x (k+1) hn, smul_zero]
    · have he : k = -1 := by omega
      subst k
      norm_num

end HMT.IV.LatticeTranslationVacuum
end

#print axioms HMT.IV.LatticeTranslationVacuum.coefficientTranslation_coeff
#print axioms HMT.IV.LatticeTranslationVacuum.delta_potential
#print axioms HMT.IV.LatticeTranslationVacuum.expPartial_coeff
#print axioms HMT.IV.LatticeTranslationVacuum.delta_expPartial
#print axioms HMT.IV.LatticeTranslationVacuum.creation_exponential_recurrence
#print axioms HMT.IV.LatticeTranslationVacuum.translation_vacuum_coefficient_nonnegative
#print axioms HMT.IV.LatticeTranslationVacuum.translation_vacuum_coefficient
