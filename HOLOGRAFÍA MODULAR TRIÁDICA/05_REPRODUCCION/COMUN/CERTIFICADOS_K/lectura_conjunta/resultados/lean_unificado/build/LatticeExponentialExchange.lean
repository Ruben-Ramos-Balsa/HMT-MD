import LatticeExponentialCommutator
import LatticeAnnihilationCommutativity

/-!
Finite normal ordering of the actual annihilation and creation exponential
coefficients in every pair of degrees. The recursion below is an independent
normal-form algorithm: creation factors remain on the left; each step adds
only an annihilation-potential coefficient on the right or the scalar
contraction read from the inherited integral pairing. Equality with the
original operator product is proved by induction on ordered powers.

This module does not identify the regrouped scalar factor with a binomial
series, nor assert locality or the full vertex-algebra axioms.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeExponentialExchange

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialCommutator HMT.IV.LatticeAnnihilationCommutativity
open PowerSeries
open scoped BigOperators

abbrev FockEnd (o : Fin 12) := Module.End ℂ (Fock o)

def contraction (o : Fin 12) (x y : Lattice o) (r : ℕ) : ℂ :=
  -(integerPair o x y : ℂ) / (r : ℂ)

theorem potentialCoefficient_exchange (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) :
    coeff (FockEnd o) r (annihilationPotential o x) * creationExponentialMode o y d =
      creationExponentialMode o y d * coeff (FockEnd o) r (annihilationPotential o x) +
        if 0 < r ∧ r ≤ d then
          contraction o x y r • creationExponentialMode o y (d-r) else 0 := by
  cases r with
  | zero => simp [annihilationPotential_constant]
  | succ n =>
    rw [annihilationPotential_coefficient_succ]
    apply LinearMap.ext
    intro v
    change ((-1 / (n+1 : ℂ)) • chargeAnnihilation o x n)
        (creationExponentialMode o y d v) = _
    have h := mixed_exponential_commutator_pairing o x y n d v
    rw [sub_eq_iff_eq_add] at h
    simp only [LinearMap.smul_apply, LinearMap.add_apply, Module.End.mul_apply,
      map_smul]
    rw [h]
    by_cases hd : n+1 ≤ d
    · simp only [if_pos hd, Nat.succ_pos, true_and, if_pos hd,
        smul_add, smul_smul, contraction, Nat.cast_add, Nat.cast_one,
        LinearMap.smul_apply]
      have hc : (-1 / (n+1 : ℂ)) * (integerPair o x y : ℂ) =
          -(integerPair o x y : ℂ) / (n+1 : ℂ) := by ring
      rw [hc, add_comm]
    · simp only [if_neg hd, Nat.succ_pos, true_and, if_neg hd,
        zero_add, smul_zero, add_zero, LinearMap.zero_apply]

/-- Normal-ordered coefficient of the k-th ordered power of the
annihilation potential, followed by creation coefficient d. -/
def normalPower (o : Fin 12) (x y : Lattice o) :
    ℕ → ℕ → ℕ → FockEnd o
  | 0, r, d => if r=0 then creationExponentialMode o y d else 0
  | k+1, r, d => ∑ p ∈ Finset.antidiagonal r,
      (normalPower o x y k p.1 d * coeff (FockEnd o) p.2 (annihilationPotential o x) +
        if 0 < p.2 ∧ p.2 ≤ d then
          contraction o x y p.2 • normalPower o x y k p.1 (d-p.2)
        else 0)

theorem powerCoefficient_exchange (o : Fin 12) (x y : Lattice o)
    (k r d : ℕ) :
    coeff (FockEnd o) r (annihilationPotential o x ^ k) *
      creationExponentialMode o y d = normalPower o x y k r d := by
  induction k generalizing r d with
  | zero =>
    simp only [pow_zero, coeff_one, normalPower]
    split_ifs <;> simp
  | succ k ih =>
    rw [pow_succ, coeff_mul, Finset.sum_mul, normalPower]
    apply Finset.sum_congr rfl
    intro p _
    rw [mul_assoc, potentialCoefficient_exchange, mul_add, ← mul_assoc, ih]
    congr 1
    split_ifs
    · rw [mul_smul_comm, ih]
    · rw [mul_zero]

def normalExponential (o : Fin 12) (x y : Lattice o) (r d : ℕ) : FockEnd o :=
  ∑ k ∈ Finset.range (r+1), coeff ℂ k (PowerSeries.exp ℂ) • normalPower o x y k r d

/-- Exact normal-ordering identity for both actual exponential coefficients.
All sums are finite at each pair of degrees r,d; no extra cutoff is assumed. -/
theorem exponentialCoefficient_exchange (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) :
    exponentialCoefficient o x r * creationExponentialMode o y d =
      normalExponential o x y r d := by
  rw [exponentialCoefficient, Finset.sum_mul, normalExponential]
  apply Finset.sum_congr rfl
  intro k _
  rw [smul_mul_assoc, powerCoefficient_exchange]

theorem exponentialCoefficient_exchange_apply (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) (v : Fock o) :
    exponentialCoefficient o x r (creationExponentialMode o y d v) =
      normalExponential o x y r d v :=
  LinearMap.congr_fun (exponentialCoefficient_exchange o x y r d) v

theorem normalExponential_zero_annihilation (o : Fin 12) (x y : Lattice o)
    (d : ℕ) : normalExponential o x y 0 d = creationExponentialMode o y d := by
  rw [← exponentialCoefficient_exchange, annihilationExponential_constant]
  exact one_mul _

theorem normalExponential_zero_creation (o : Fin 12) (x y : Lattice o)
    (r : ℕ) : normalExponential o x y r 0 = exponentialCoefficient o x r := by
  rw [← exponentialCoefficient_exchange, creationExponentialMode_zero]
  exact mul_one _

theorem orthogonal_potential_commute (o : Fin 12) (x y : Lattice o)
    (hxy : integerPair o x y = 0) (r d : ℕ) :
    Commute (coeff (FockEnd o) r (annihilationPotential o x))
      (creationExponentialMode o y d) := by
  change _ * _ = _ * _
  rw [potentialCoefficient_exchange]
  simp [contraction, hxy]

theorem orthogonal_power_commute (o : Fin 12) (x y : Lattice o)
    (hxy : integerPair o x y = 0) (k r d : ℕ) :
    Commute (coeff (FockEnd o) r (annihilationPotential o x ^ k))
      (creationExponentialMode o y d) := by
  induction k generalizing r with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs
    · exact Commute.one_left _
    · exact Commute.zero_left _
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    apply Commute.sum_left
    intro p _
    exact (ih p.1).mul_left (orthogonal_potential_commute o x y hxy p.2 d)

theorem orthogonal_exponentials_commute (o : Fin 12) (x y : Lattice o)
    (hxy : integerPair o x y = 0) (r d : ℕ) :
    Commute (exponentialCoefficient o x r) (creationExponentialMode o y d) := by
  unfold exponentialCoefficient
  apply Commute.sum_left
  intro k _
  exact (orthogonal_power_commute o x y hxy k r d).smul_left _

end HMT.IV.LatticeExponentialExchange
end

#print axioms HMT.IV.LatticeExponentialExchange.potentialCoefficient_exchange
#print axioms HMT.IV.LatticeExponentialExchange.powerCoefficient_exchange
#print axioms HMT.IV.LatticeExponentialExchange.exponentialCoefficient_exchange
#print axioms HMT.IV.LatticeExponentialExchange.exponentialCoefficient_exchange_apply
#print axioms HMT.IV.LatticeExponentialExchange.normalExponential_zero_annihilation
#print axioms HMT.IV.LatticeExponentialExchange.normalExponential_zero_creation
#print axioms HMT.IV.LatticeExponentialExchange.orthogonal_exponentials_commute
