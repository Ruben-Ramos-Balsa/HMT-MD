import LatticeAnnihilationExponential
import LatticeEulerEnergy
import LatticeModeWeights

/-!
Weight lowering and vectorwise truncation of the actual annihilation
exponential. The Euler operator is the derivation of the symmetric algebra;
the coefficients are the ordered powers constructed previously. No spectral
bound or vanishing condition is supplied as a hypothesis.
-/

noncomputable section
namespace HMT.IV.LatticeAnnihilationEnergy

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeModeWeights
open HMT.IV.LatticeEulerEnergy HMT.IV.LatticeAnnihilationExponential
open PowerSeries
open scoped BigOperators

def LowersWeight (o : Fin 12) (d : ℕ) (T : Module.End ℂ (Fock o)) : Prop :=
  ∀ v, euler o (T v) = T (euler o v) - (d : ℂ) • T v

theorem lowersWeight_zero (o : Fin 12) (d : ℕ) :
    LowersWeight o d 0 := by
  intro v
  simp

theorem lowersWeight_one (o : Fin 12) : LowersWeight o 0 1 := by
  intro v
  simp

theorem lowersWeight_smul (o : Fin 12) (d : ℕ) (c : ℂ)
    (T : Module.End ℂ (Fock o)) (hT : LowersWeight o d T) :
    LowersWeight o d (c • T) := by
  intro v
  simp only [LinearMap.smul_apply, Derivation.map_smul]
  rw [hT v]
  simp only [smul_sub, smul_smul]
  congr 1
  rw [mul_comm]

theorem lowersWeight_sum (o : Fin 12) (d : ℕ) {ι : Type*}
    (s : Finset ι) (T : ι → Module.End ℂ (Fock o))
    (hT : ∀ i ∈ s, LowersWeight o d (T i)) :
    LowersWeight o d (∑ i ∈ s, T i) := by
  intro v
  simp only [LinearMap.sum_apply, map_sum, Finset.smul_sum]
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun i hi => hT i hi v

theorem lowersWeight_mul (o : Fin 12) (d e : ℕ)
    (T S : Module.End ℂ (Fock o))
    (hT : LowersWeight o d T) (hS : LowersWeight o e S) :
    LowersWeight o (d+e) (T*S) := by
  intro v
  change euler o (T (S v)) = T (S (euler o v)) - ((d+e : ℕ) : ℂ) • T (S v)
  rw [hT, hS, map_sub, map_smul, Nat.cast_add, add_smul]
  abel

theorem annihilate_lowersWeight (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    LowersWeight o (n+1) (annihilate o n i) := by
  have h : (euler o).toLinearMap.comp (annihilate o n i) -
      (annihilate o n i).comp (euler o).toLinearMap =
      (-(n+1 : ℂ)) • annihilate o n i := by
    apply (monomialBasis o).ext
    intro a
    change euler o (annihilate o n i (monomialBasis o a)) -
      annihilate o n i (euler o (monomialBasis o a)) =
      (-(n+1 : ℂ)) • annihilate o n i (monomialBasis o a)
    simp only [annihilate_monomial,
      Finsupp.sum, euler_monomial, map_sum, Derivation.map_smul, map_smul,
      Finset.smul_sum, smul_smul]
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro p hp
    rw [← sub_smul]
    by_cases hz : (a p : ℂ) * (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0) = 0
    · rw [hz]
      simp
    · have hw := annihilate_nonzero_term_weight o n i a p hz
      have hwC : (occupationWeight o (a-Finsupp.single p 1) : ℂ) + (n+1 : ℂ) =
          (occupationWeight o a : ℂ) := by exact_mod_cast hw
      congr 1
      linear_combination
        ((a p : ℂ) * (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0)) * hwC
  intro v
  have hv := LinearMap.congr_fun h v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply] at hv
  change euler o (annihilate o n i v) - annihilate o n i (euler o v) =
    (-(n+1 : ℂ)) • annihilate o n i v at hv
  rw [sub_eq_iff_eq_add] at hv
  rw [hv, Nat.cast_add, Nat.cast_one, neg_smul]
  abel

theorem chargeAnnihilation_lowersWeight (o : Fin 12) (x : Lattice o) (n : ℕ) :
    LowersWeight o (n+1) (chargeAnnihilation o x n) := by
  apply lowersWeight_sum
  intro i _
  exact lowersWeight_smul o (n+1) _ _ (annihilate_lowersWeight o n i)

theorem potentialCoefficient_lowersWeight (o : Fin 12) (x : Lattice o) (d : ℕ) :
    LowersWeight o d (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x)) := by
  cases d with
  | zero => rw [annihilationPotential_constant]; exact lowersWeight_zero o 0
  | succ n =>
    rw [annihilationPotential_coefficient_succ]
    exact lowersWeight_smul o (n+1) _ _ (chargeAnnihilation_lowersWeight o x n)

theorem powerCoefficient_lowersWeight (o : Fin 12) (x : Lattice o) (k d : ℕ) :
    LowersWeight o d (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ k)) := by
  induction k generalizing d with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs with h
    · subst d; exact lowersWeight_one o
    · exact lowersWeight_zero o d
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    apply lowersWeight_sum
    intro p hp
    have hd := Finset.mem_antidiagonal.mp hp
    rw [← hd]
    exact lowersWeight_mul o p.1 p.2 _ _ (ih p.1)
      (potentialCoefficient_lowersWeight o x p.2)

theorem exponentialCoefficient_lowersWeight (o : Fin 12) (x : Lattice o) (d : ℕ) :
    LowersWeight o d (exponentialCoefficient o x d) := by
  apply lowersWeight_sum
  intro k _
  exact lowersWeight_smul o d _ _ (powerCoefficient_lowersWeight o x k d)

theorem euler_coefficient (o : Fin 12) (v : Fock o) (a : Occupation o) :
    (monomialBasis o).repr (euler o v) a =
      (occupationWeight o a : ℂ) * (monomialBasis o).repr v a := by
  classical
  have h : ((monomialBasis o).coord a).comp (euler o).toLinearMap =
      (occupationWeight o a : ℂ) • (monomialBasis o).coord a := by
    apply (monomialBasis o).ext
    intro b
    change (monomialBasis o).repr (euler o (monomialBasis o b)) a =
      (occupationWeight o a : ℂ) * (monomialBasis o).repr (monomialBasis o b) a
    simp only [euler_monomial, map_smul,
      Finsupp.smul_apply, Basis.repr_self,
      Finsupp.single_apply, smul_eq_mul]
    split_ifs with hb
    · subst b; rfl
    · simp
  exact LinearMap.congr_fun h v

theorem negative_euler_eigenvector_zero (o : Fin 12) (v : Fock o) (m d : ℕ)
    (hmd : m < d) (hv : euler o v = ((m : ℂ)-(d : ℂ)) • v) : v = 0 := by
  apply (monomialBasis o).repr.injective
  ext a
  simp only [map_zero, Finsupp.zero_apply]
  by_contra hn
  have h := congrArg (fun w => (monomialBasis o).repr w a) hv
  dsimp only at h
  rw [euler_coefficient] at h
  simp only [map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  have hw : (occupationWeight o a : ℂ) = (m : ℂ)-(d : ℂ) :=
    mul_right_cancel₀ hn h
  have hw' : ((occupationWeight o a + d : ℕ) : ℂ) = (m : ℂ) := by
    rw [Nat.cast_add, hw]
    ring
  have hw'' : occupationWeight o a + d = m := by exact_mod_cast hw'
  omega

theorem annihilationCoefficient_cutoff_on_monomial (o : Fin 12) (x : Lattice o)
    (d : ℕ) (a : Occupation o) (h : occupationWeight o a < d) :
    exponentialCoefficient o x d (monomialBasis o a) = 0 := by
  apply negative_euler_eigenvector_zero o _ (occupationWeight o a) d h
  rw [exponentialCoefficient_lowersWeight o x d, euler_monomial,
    map_smul, sub_smul]

/-- Every algebraic Fock vector has a finite, explicitly constructed cutoff.
The bound is one greater than the largest weight in its finite basis support. -/
theorem exists_annihilationExponential_bound (o : Fin 12) (x : Lattice o)
    (v : Fock o) :
    ∃ N : ℕ, ∀ d ≥ N, exponentialCoefficient o x d v = 0 := by
  classical
  let S := ((monomialBasis o).repr v).support
  refine ⟨S.sup (occupationWeight o) + 1, ?_⟩
  intro d hd
  conv_lhs => rw [← (monomialBasis o).linearCombination_repr v]
  rw [Finsupp.linearCombination_apply, Finsupp.sum, map_sum]
  apply Finset.sum_eq_zero
  intro a ha
  rw [map_smul]
  have hw : occupationWeight o a ≤ S.sup (occupationWeight o) := Finset.le_sup ha
  rw [annihilationCoefficient_cutoff_on_monomial o x d a (by omega), smul_zero]

end HMT.IV.LatticeAnnihilationEnergy
end

#print axioms HMT.IV.LatticeAnnihilationEnergy.annihilate_lowersWeight
#print axioms HMT.IV.LatticeAnnihilationEnergy.exponentialCoefficient_lowersWeight
#print axioms HMT.IV.LatticeAnnihilationEnergy.euler_coefficient
#print axioms HMT.IV.LatticeAnnihilationEnergy.negative_euler_eigenvector_zero
#print axioms HMT.IV.LatticeAnnihilationEnergy.annihilationCoefficient_cutoff_on_monomial
#print axioms HMT.IV.LatticeAnnihilationEnergy.exists_annihilationExponential_bound
