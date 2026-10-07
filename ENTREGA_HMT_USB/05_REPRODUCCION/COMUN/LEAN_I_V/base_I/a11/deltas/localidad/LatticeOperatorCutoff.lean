import LatticeNormalOrdering
import LatticeAnnihilationCommutativity

/-!
Coefficientwise commutation and propagation of a valid annihilation cutoff
for the existing Fock operators. The two annihilation exponentials commute
by the already proved charged-annihilator relation. Creation raises a cutoff
by its coefficient degree, using the exact normal-ordering antidiagonal.
No field or oscillator operator is redefined and no locality relation is
assumed.
-/

noncomputable section
namespace HMT.IV.LatticeOperatorCutoff

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeAnnihilationCommutativity HMT.IV.LatticeNormalOrdering
open PowerSeries
open scoped BigOperators

theorem exponential_potentialCoefficient_commute (o : Fin 12)
    (x y : Lattice o) (r d : ℕ) :
    Commute (exponentialCoefficient o x r)
      (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o y)) := by
  cases d with
  | zero =>
    rw [annihilationPotential_constant]
    exact Commute.zero_right _
  | succ d =>
    rw [annihilationPotential_coefficient_succ]
    exact (exponentialCoefficient_commute o y x d r).symm.smul_right _

theorem exponential_powerCoefficient_commute (o : Fin 12)
    (x y : Lattice o) (r k d : ℕ) :
    Commute (exponentialCoefficient o x r)
      (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o y ^ k)) := by
  induction k generalizing d with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs
    · exact Commute.one_right _
    · exact Commute.zero_right _
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    apply Commute.sum_right
    intro p _
    exact (ih p.1).mul_right (exponential_potentialCoefficient_commute o x y r p.2)

/-- Both charges and both coefficient degrees are arbitrary. -/
theorem exponentialCoefficients_commute (o : Fin 12)
    (x y : Lattice o) (r d : ℕ) :
    Commute (exponentialCoefficient o x r) (exponentialCoefficient o y d) := by
  change Commute (exponentialCoefficient o x r)
    (∑ k ∈ Finset.range (d+1), coeff ℂ k (PowerSeries.exp ℂ) •
      coeff (Module.End ℂ (Fock o)) d (annihilationPotential o y ^ k))
  apply Commute.sum_right
  intro k _
  exact (exponential_powerCoefficient_commute o x y r k d).smul_right _

theorem exponentialCoefficients_commute_apply (o : Fin 12)
    (x y : Lattice o) (r d : ℕ) (v : Fock o) :
    exponentialCoefficient o x r (exponentialCoefficient o y d v) =
      exponentialCoefficient o y d (exponentialCoefficient o x r v) :=
  LinearMap.congr_fun (exponentialCoefficients_commute o x y r d).eq v

/-- A coefficient of another annihilation exponential preserves the same cutoff. -/
theorem cutoff_preserved_by_exponential (o : Fin 12) (x y : Lattice o)
    (j N : ℕ) (v : Fock o)
    (hv : ∀ r, N < r → exponentialCoefficient o x r v = 0) :
    ∀ r, N < r →
      exponentialCoefficient o x r (exponentialCoefficient o y j v) = 0 := by
  intro r hr
  rw [exponentialCoefficients_commute_apply, hv r hr, map_zero]

/-- Degree d creation raises a valid cutoff by at most d. -/
theorem cutoff_after_creation (o : Fin 12) (x y : Lattice o)
    (d N : ℕ) (v : Fock o)
    (hv : ∀ r, N < r → exponentialCoefficient o x r v = 0) :
    ∀ r, N+d < r →
      exponentialCoefficient o x r (creationExponentialMode o y d v) = 0 := by
  intro r hr
  change (exponentialCoefficient o x r * creationExponentialMode o y d) v = 0
  rw [exponential_normal_order_coefficient, LinearMap.sum_apply]
  apply Finset.sum_eq_zero
  intro p hp
  rw [LinearMap.smul_apply]
  by_cases hpd : p.1 ≤ d
  · rw [if_pos hpd]
    have hsum := Finset.mem_antidiagonal.mp hp
    have hpN : N < p.2 := by omega
    change _ • creationExponentialMode o y (d-p.1)
      (exponentialCoefficient o x p.2 v) = 0
    rw [hv p.2 hpN, map_zero, smul_zero]
  · rw [if_neg hpd]
    simp

end HMT.IV.LatticeOperatorCutoff
end

#print axioms HMT.IV.LatticeOperatorCutoff.exponential_potentialCoefficient_commute
#print axioms HMT.IV.LatticeOperatorCutoff.exponential_powerCoefficient_commute
#print axioms HMT.IV.LatticeOperatorCutoff.exponentialCoefficients_commute
#print axioms HMT.IV.LatticeOperatorCutoff.exponentialCoefficients_commute_apply
#print axioms HMT.IV.LatticeOperatorCutoff.cutoff_preserved_by_exponential
#print axioms HMT.IV.LatticeOperatorCutoff.cutoff_after_creation
