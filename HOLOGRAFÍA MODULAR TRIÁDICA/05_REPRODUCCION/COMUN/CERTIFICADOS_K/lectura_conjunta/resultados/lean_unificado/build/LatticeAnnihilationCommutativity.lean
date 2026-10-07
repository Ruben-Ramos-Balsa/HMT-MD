import LatticeExponentialCommutator
import LatticeAnnihilationEnergy
import LatticeChargedVertexField

/-!
Positive charged annihilation commutes with every coefficient of the
constructed annihilation exponential. The consequence for finite field
cutoffs is proved on the same Fock carrier; no commutation relation for
the exponentials is postulated.
-/

noncomputable section
namespace HMT.IV.LatticeAnnihilationCommutativity

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeFockMonomialParity HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeAnnihilationEnergy HMT.IV.LatticeExponentialCommutator
open HMT.IV.LatticeChargedVertexField
open PowerSeries
open scoped BigOperators TensorProduct

theorem chargedAnnihilations_commute (o : Fin 12) (u x : Lattice o) (n m : ℕ) :
    Commute (chargeAnnihilation o u n) (chargeAnnihilation o x m) := by
  change chargeAnnihilation o u n * chargeAnnihilation o x m =
    chargeAnnihilation o x m * chargeAnnihilation o u n
  ext v
  change chargeAnnihilation o u n (chargeAnnihilation o x m v) =
    chargeAnnihilation o x m (chargeAnnihilation o u n v)
  simp only [chargeAnnihilation_apply, map_sum, map_smul, Finset.smul_sum, smul_smul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  rw [annihilations_commute_all_modes, mul_comm]

theorem potentialCoefficient_commute (o : Fin 12) (u x : Lattice o) (n d : ℕ) :
    Commute (chargeAnnihilation o u n)
      (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x)) := by
  cases d with
  | zero => rw [annihilationPotential_constant]; exact Commute.zero_right _
  | succ d =>
    rw [annihilationPotential_coefficient_succ]
    exact (chargedAnnihilations_commute o u x n d).smul_right _

theorem powerCoefficient_commute (o : Fin 12) (u x : Lattice o) (n k d : ℕ) :
    Commute (chargeAnnihilation o u n)
      (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ k)) := by
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
    exact (ih p.1).mul_right (potentialCoefficient_commute o u x n p.2)

theorem exponentialCoefficient_commute (o : Fin 12) (u x : Lattice o) (n d : ℕ) :
    Commute (chargeAnnihilation o u n) (exponentialCoefficient o x d) := by
  unfold exponentialCoefficient
  apply Commute.sum_right
  intro k _
  exact (powerCoefficient_commute o u x n k d).smul_right _

theorem exponentialCoefficient_commute_apply (o : Fin 12) (u x : Lattice o)
    (n d : ℕ) (v : Fock o) :
    chargeAnnihilation o u n (exponentialCoefficient o x d v) =
      exponentialCoefficient o x d (chargeAnnihilation o u n v) :=
  LinearMap.congr_fun (exponentialCoefficient_commute o u x n d).eq v

/-- An annihilator cannot invalidate a valid exponential cutoff. -/
theorem cutoff_preserved_by_annihilation (o : Fin 12) (u x : Lattice o)
    (n N : ℕ) (v : Fock o)
    (hv : ∀ d, N < d → exponentialCoefficient o x d v = 0) :
    ∀ d, N < d → exponentialCoefficient o x d (chargeAnnihilation o u n v) = 0 := by
  intro d hd
  rw [← exponentialCoefficient_commute_apply, hv d hd, map_zero]

theorem cutoff_on_annihilated_monomial (o : Fin 12) (u x : Lattice o)
    (n d : ℕ) (a : Occupation o) (ha : occupationWeight o a < d) :
    exponentialCoefficient o x d (chargeAnnihilation o u n (monomialBasis o a)) = 0 := by
  rw [← exponentialCoefficient_commute_apply,
    annihilationCoefficient_cutoff_on_monomial o x d a ha, map_zero]

/-- Finite coefficient expression extended linearly to an oscillator vector;
on a monomial it is exactly the existing basis cutoff. -/
def fieldCutoff (o : Fin 12) (x y : Lattice o) (k : ℤ) (N : ℕ) (v : Fock o) :
    LatticeCarrier o :=
  epsilon o x y • ∑ j ∈ Finset.range (N+1),
    if 0 ≤ k-integerPair o x y+(j : ℤ) then
      creationExponentialMode o x ((k-integerPair o x y+(j : ℤ)).toNat)
        (exponentialCoefficient o x j v) ⊗ₜ[ℂ] basisElement o (x+y)
    else 0

theorem fieldCutoff_monomial (o : Fin 12) (x y : Lattice o) (k : ℤ)
    (N : ℕ) (a : Occupation o) :
    fieldCutoff o x y k N (monomialBasis o a) =
      basisCoefficientCutoff o x k N a y := rfl

theorem fieldCutoff_stable (o : Fin 12) (x y : Lattice o) (k : ℤ)
    (N M : ℕ) (v : Fock o) (hNM : N ≤ M)
    (hv : ∀ d, N < d → exponentialCoefficient o x d v = 0) :
    fieldCutoff o x y k N v = fieldCutoff o x y k M v := by
  unfold fieldCutoff
  congr 1
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro j _ hj
  have hNj : N < j := by simp only [Finset.mem_range] at hj; omega
  split_ifs
  · rw [hv j hNj, map_zero, TensorProduct.zero_tmul]
  · rfl

theorem fieldCutoff_annihilated_monomial_stable (o : Fin 12) (u x y : Lattice o)
    (n : ℕ) (k : ℤ) (a : Occupation o) (N : ℕ)
    (hN : occupationWeight o a ≤ N) :
    fieldCutoff o x y k (occupationWeight o a)
        (chargeAnnihilation o u n (monomialBasis o a)) =
      fieldCutoff o x y k N (chargeAnnihilation o u n (monomialBasis o a)) := by
  apply fieldCutoff_stable o x y k _ N _ hN
  intro d hd
  exact cutoff_on_annihilated_monomial o u x n d a hd

end HMT.IV.LatticeAnnihilationCommutativity
end

#print axioms HMT.IV.LatticeAnnihilationCommutativity.chargedAnnihilations_commute
#print axioms HMT.IV.LatticeAnnihilationCommutativity.exponentialCoefficient_commute
#print axioms HMT.IV.LatticeAnnihilationCommutativity.cutoff_preserved_by_annihilation
#print axioms HMT.IV.LatticeAnnihilationCommutativity.cutoff_on_annihilated_monomial
#print axioms HMT.IV.LatticeAnnihilationCommutativity.fieldCutoff_stable
#print axioms HMT.IV.LatticeAnnihilationCommutativity.fieldCutoff_annihilated_monomial_stable
