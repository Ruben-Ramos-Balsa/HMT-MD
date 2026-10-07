import LatticeAnnihilationCommutativity
import LatticeTranslationVacuum
import Mathlib.Algebra.Algebra.Subalgebra.Lattice

/-!
The differential recurrence of the actual annihilation exponential.
The positive modes generate a commutative subalgebra because their
commutation has already been proved on Fock. Formal differentiation is
performed there and then mapped back to the original endomorphism ring.
No exponential differential equation is introduced as a hypothesis.
-/

noncomputable section
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeAnnihilationRecurrence

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeAnnihilationExponential HMT.IV.LatticeAnnihilationCommutativity
open HMT.IV.LatticeExponentialCommutator
open PowerSeries
open scoped BigOperators

abbrev oscillatorAlgebra (o : Fin 12) (x : Lattice o) :
    Subalgebra ℂ (Module.End ℂ (Fock o)) :=
  Algebra.adjoin ℂ (Set.range (chargeAnnihilation o x))

instance (priority := 100) oscillatorAlgebraCommRing (o : Fin 12) (x : Lattice o) :
    CommRing (oscillatorAlgebra o x) :=
  Algebra.adjoinCommRingOfComm ℂ (by
    rintro a ⟨n,rfl⟩ b ⟨m,rfl⟩
    exact (chargedAnnihilations_commute o x x n m).eq)

def generator (o : Fin 12) (x : Lattice o) (n : ℕ) : oscillatorAlgebra o x :=
  ⟨chargeAnnihilation o x n, Algebra.subset_adjoin ⟨n,rfl⟩⟩

def potential (o : Fin 12) (x : Lattice o) : PowerSeries (oscillatorAlgebra o x) :=
  X * PowerSeries.mk (fun n => (-1/(n+1:ℂ)) • generator o x n)

def generatorSeries (o : Fin 12) (x : Lattice o) :
    PowerSeries (oscillatorAlgebra o x) := PowerSeries.mk (generator o x)

theorem potential_coefficient_zero (o : Fin 12) (x : Lattice o) :
    coeff (oscillatorAlgebra o x) 0 (potential o x) = 0 := by
  simp [potential, coeff_zero_eq_constantCoeff_apply]

theorem potential_coefficient_succ (o : Fin 12) (x : Lattice o) (n : ℕ) :
    coeff (oscillatorAlgebra o x) (n+1) (potential o x) =
      (-1/(n+1:ℂ)) • generator o x n := by
  simp [potential, coeff_succ_X_mul]

theorem map_potential (o : Fin 12) (x : Lattice o) :
    PowerSeries.map (oscillatorAlgebra o x).val.toRingHom (potential o x) =
      annihilationPotential o x := by
  apply PowerSeries.ext
  intro d
  rw [coeff_map]
  cases d with
  | zero => rw [potential_coefficient_zero, annihilationPotential_constant, map_zero]
  | succ n =>
    rw [potential_coefficient_succ, annihilationPotential_coefficient_succ]
    rfl

theorem mapped_power_coefficient (o : Fin 12) (x : Lattice o) (k d : ℕ) :
    (oscillatorAlgebra o x).val
      (coeff (oscillatorAlgebra o x) d (potential o x ^ k)) =
      coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ k) := by
  change (oscillatorAlgebra o x).val.toRingHom
    (coeff (oscillatorAlgebra o x) d (potential o x ^ k)) = _
  rw [← coeff_map, map_pow, map_potential]

theorem potential_derivative (o : Fin 12) (x : Lattice o) :
    PowerSeries.derivative (oscillatorAlgebra o x) (potential o x) =
      -generatorSeries o x := by
  apply PowerSeries.ext
  intro d
  rw [coeff_derivative, potential_coefficient_succ, map_neg]
  rw [generatorSeries, coeff_mk]
  change ((-1/(d+1:ℂ)) • generator o x d) * (d+1) = -generator o x d
  rw [mul_comm, mul_smul_comm]
  rw [show (d : oscillatorAlgebra o x)+1 = ((d+1 : ℕ) : oscillatorAlgebra o x) by
    simp only [Nat.cast_add, Nat.cast_one]]
  rw [← nsmul_eq_mul, ← Nat.cast_smul_eq_nsmul ℂ, smul_smul]
  have hd : ((d+1 : ℕ) : ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero d
  have hs : (-1/(d+1:ℂ)) * ((d+1 : ℕ):ℂ) = -1 := by
    push_cast at hd ⊢
    field_simp
  rw [hs, neg_one_smul]

def expPartial (o : Fin 12) (x : Lattice o) (N : ℕ) :
    PowerSeries (oscillatorAlgebra o x) :=
  ∑ k ∈ Finset.range N, coeff ℂ k (PowerSeries.exp ℂ) • potential o x ^ k

theorem mapped_expPartial_coefficient (o : Fin 12) (x : Lattice o) (N d : ℕ)
    (hd : d < N) :
    (oscillatorAlgebra o x).val
      (coeff (oscillatorAlgebra o x) d (expPartial o x N)) =
      exponentialCoefficient o x d := by
  simp only [expPartial, map_sum, coeff_smul, map_smul,
    mapped_power_coefficient, exponentialCoefficient]
  symm
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro k _ hk
  have hdk : d < k := by simp only [Finset.mem_range] at hk; omega
  rw [potential_power_coefficient_zero o x k d hdk, smul_zero]

theorem derivative_expPartial (o : Fin 12) (x : Lattice o) (N : ℕ) :
    PowerSeries.derivative (oscillatorAlgebra o x) (expPartial o x (N+1)) =
      -generatorSeries o x * expPartial o x N := by
  unfold expPartial
  rw [map_sum, Finset.sum_range_succ', Finset.mul_sum]
  simp only [pow_zero, Derivation.map_one_eq_zero,
    Derivation.map_smul_of_tower, smul_zero, add_zero]
  apply Finset.sum_congr rfl
  intro k _
  rw [Derivation.leibniz_pow, potential_derivative]
  simp only [Nat.add_sub_cancel, smul_eq_mul]
  rw [← Nat.cast_smul_eq_nsmul ℂ, smul_smul, Nat.cast_add, Nat.cast_one,
    exp_coefficient_succ_mul]
  simp only [Algebra.smul_def]
  ring

theorem annihilationCoefficient_recurrence_antidiagonal (o : Fin 12)
    (x : Lattice o) (r : ℕ) :
    (r+1 : ℂ) • exponentialCoefficient o x (r+1) =
      -(∑ p ∈ Finset.antidiagonal r,
        chargeAnnihilation o x p.1 * exponentialCoefficient o x p.2) := by
  have h := congrArg (fun f => (oscillatorAlgebra o x).val
    (coeff (oscillatorAlgebra o x) r f)) (derivative_expPartial o x (r+1))
  dsimp only at h
  rw [coeff_derivative, map_mul, mapped_expPartial_coefficient o x (r+2) (r+1) (by omega)] at h
  rw [neg_mul, map_neg, map_neg, coeff_mul, map_sum] at h
  have hl : exponentialCoefficient o x (r+1) *
      (oscillatorAlgebra o x).val ((r+1 : ℕ) : oscillatorAlgebra o x) =
      (r+1 : ℂ) • exponentialCoefficient o x (r+1) := by
    rw [map_natCast, (Nat.cast_commute (r+1) (exponentialCoefficient o x (r+1))).eq.symm,
      ← nsmul_eq_mul]
    simpa only [Nat.cast_add, Nat.cast_one] using
      (Nat.cast_smul_eq_nsmul ℂ (r+1) (exponentialCoefficient o x (r+1))).symm
  simp only [Nat.cast_add, Nat.cast_one] at hl
  rw [hl] at h
  rw [h]
  congr 1
  apply Finset.sum_congr rfl
  intro p hp
  have hpr := Finset.mem_antidiagonal.mp hp
  rw [map_mul, mapped_expPartial_coefficient o x (r+1) p.2 (by omega)]
  simp only [generatorSeries, coeff_mk]
  rfl

theorem annihilationCoefficient_recurrence (o : Fin 12) (x : Lattice o) (r : ℕ) :
    (r+1 : ℂ) • exponentialCoefficient o x (r+1) =
      -(∑ n ∈ Finset.range (r+1),
        chargeAnnihilation o x n * exponentialCoefficient o x (r-n)) := by
  rw [annihilationCoefficient_recurrence_antidiagonal,
    Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]

end HMT.IV.LatticeAnnihilationRecurrence
end

#print axioms HMT.IV.LatticeAnnihilationRecurrence.map_potential
#print axioms HMT.IV.LatticeAnnihilationRecurrence.potential_derivative
#print axioms HMT.IV.LatticeAnnihilationRecurrence.mapped_expPartial_coefficient
#print axioms HMT.IV.LatticeAnnihilationRecurrence.derivative_expPartial
#print axioms HMT.IV.LatticeAnnihilationRecurrence.annihilationCoefficient_recurrence_antidiagonal
#print axioms HMT.IV.LatticeAnnihilationRecurrence.annihilationCoefficient_recurrence
