import LatticeHalfAnnihilationExponential
import LatticeHalfWeightBasis

/-! Pointwise truncation follows from the already constructed conformal
operator and its actual monomial basis. Twice the unshifted zero mode measures
twiceWeight, and degree d of the annihilation exponential lowers that weight
by d. The finite cutoff is extracted from the vector's finite basis support. -/

noncomputable section
namespace HMT.IV.LatticeHalfAnnihilationEnergy
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeHalfIntegerHeisenberg LatticeHalfConformalModes
open LatticeHalfConformalHeisenberg LatticeHalfWeightBasis
open LatticeHalfAnnihilationExponential
open PowerSeries
open scoped BigOperators

def halfDegree (o : Fin 12) : Module.End ℂ (HalfFock o) :=
  (2:ℂ) • quadraticMode o 0

theorem halfDegree_monomial (o : Fin 12) (a : Occupation o) :
    halfDegree o (monomialBasis o a) =
      (twiceWeight o a : ℂ) • monomialBasis o a := by
  simp only [halfDegree, LinearMap.smul_apply, quadratic_zero_monomial, smul_smul]
  congr 1
  ring

def LowersWeight (o : Fin 12) (d : ℕ) (T : Module.End ℂ (HalfFock o)) : Prop :=
  ∀ v, halfDegree o (T v) = T (halfDegree o v) - (d:ℂ) • T v

theorem lowersWeight_zero (o : Fin 12) (d : ℕ) : LowersWeight o d 0 := by
  intro v
  simp

theorem lowersWeight_one (o : Fin 12) : LowersWeight o 0 1 := by
  intro v
  simp

theorem lowersWeight_smul (o : Fin 12) (d : ℕ) (c : ℂ)
    (T : Module.End ℂ (HalfFock o)) (hT : LowersWeight o d T) :
    LowersWeight o d (c • T) := by
  intro v
  simp only [LinearMap.smul_apply, map_smul]
  rw [hT v]
  simp only [smul_sub, smul_smul]
  congr 1
  rw [mul_comm]

theorem lowersWeight_sum (o : Fin 12) (d : ℕ) {ι : Type*}
    (s : Finset ι) (T : ι → Module.End ℂ (HalfFock o))
    (hT : ∀ i ∈ s, LowersWeight o d (T i)) :
    LowersWeight o d (∑ i ∈ s, T i) := by
  intro v
  simp only [LinearMap.sum_apply, map_sum, Finset.smul_sum]
  rw [← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun i hi => hT i hi v

theorem lowersWeight_mul (o : Fin 12) (d e : ℕ)
    (T S : Module.End ℂ (HalfFock o))
    (hT : LowersWeight o d T) (hS : LowersWeight o e S) :
    LowersWeight o (d+e) (T*S) := by
  intro v
  change halfDegree o (T (S v)) = T (S (halfDegree o v)) -
    ((d+e : ℕ) : ℂ) • T (S v)
  rw [hT, hS, map_sub, map_smul, Nat.cast_add, add_smul]
  abel

theorem halfAnnihilate_lowersWeight (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    LowersWeight o (2*n+1) (halfAnnihilate o n i) := by
  intro v
  have h := quadraticMode_half_commutator_apply o i 0 (n:ℤ) v
  simp only [zero_add, halfMode_ofNat, Int.cast_natCast] at h
  rw [sub_eq_iff_eq_add] at h
  simp only [halfDegree, LinearMap.smul_apply, map_smul]
  rw [h]
  push_cast
  module

theorem chargeHalfAnnihilation_lowersWeight (o : Fin 12) (x : Lattice o) (n : ℕ) :
    LowersWeight o (2*n+1) (chargeHalfAnnihilation o x n) := by
  apply lowersWeight_sum
  intro i _
  exact lowersWeight_smul o (2*n+1) _ _ (halfAnnihilate_lowersWeight o n i)

theorem potentialCoefficient_lowersWeight (o : Fin 12) (x : Lattice o) (d : ℕ) :
    LowersWeight o d (coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x)) := by
  rw [annihilationPotential_coefficient]
  split_ifs with hd
  · have he : 2*(d/2)+1 = d := by omega
    have hh := lowersWeight_smul o (2*(d/2)+1)
      (-1 / (((d/2 : ℕ) : ℂ)+1/2)) (chargeHalfAnnihilation o x (d/2))
      (chargeHalfAnnihilation_lowersWeight o x (d/2))
    rw [he] at hh
    exact hh
  · exact lowersWeight_zero o d

theorem powerCoefficient_lowersWeight (o : Fin 12) (x : Lattice o) (k d : ℕ) :
    LowersWeight o d (coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x ^ k)) := by
  induction k generalizing d with
  | zero =>
    simp only [pow_zero, coeff_one]
    split_ifs with h
    · subst d
      exact lowersWeight_one o
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

theorem halfDegree_coefficient (o : Fin 12) (v : HalfFock o) (a : Occupation o) :
    (monomialBasis o).repr (halfDegree o v) a =
      (twiceWeight o a : ℂ) * (monomialBasis o).repr v a := by
  classical
  have h : ((monomialBasis o).coord a).comp (halfDegree o) =
      (twiceWeight o a : ℂ) • (monomialBasis o).coord a := by
    apply (monomialBasis o).ext
    intro b
    simp only [LinearMap.comp_apply, halfDegree_monomial, map_smul,
      LinearMap.smul_apply, Basis.coord_apply, Basis.repr_self,
      Finsupp.single_apply, smul_eq_mul]
    split_ifs with hb
    · subst b
      rfl
    · simp
  exact LinearMap.congr_fun h v

theorem negative_halfDegree_eigenvector_zero (o : Fin 12) (v : HalfFock o) (m d : ℕ)
    (hmd : m < d) (hv : halfDegree o v = ((m:ℂ)-(d:ℂ)) • v) : v = 0 := by
  apply (monomialBasis o).repr.injective
  ext a
  simp only [map_zero, Finsupp.zero_apply]
  by_contra hn
  have h := congrArg (fun w => (monomialBasis o).repr w a) hv
  dsimp only at h
  rw [halfDegree_coefficient] at h
  simp only [map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  have hw : (twiceWeight o a : ℂ) = (m:ℂ)-(d:ℂ) := mul_right_cancel₀ hn h
  have hc : ((twiceWeight o a + d : ℕ) : ℂ) = (m:ℂ) := by
    rw [Nat.cast_add, hw]
    ring
  have hnat : twiceWeight o a + d = m := by exact_mod_cast hc
  omega

theorem annihilationCoefficient_cutoff_on_monomial (o : Fin 12) (x : Lattice o)
    (d : ℕ) (a : Occupation o) (h : twiceWeight o a < d) :
    exponentialCoefficient o x d (monomialBasis o a) = 0 := by
  apply negative_halfDegree_eigenvector_zero o _ (twiceWeight o a) d h
  rw [exponentialCoefficient_lowersWeight o x d, halfDegree_monomial,
    map_smul, sub_smul]

theorem exists_annihilationExponential_bound (o : Fin 12) (x : Lattice o)
    (v : HalfFock o) :
    ∃ N : ℕ, ∀ d ≥ N, exponentialCoefficient o x d v = 0 := by
  classical
  let S := ((monomialBasis o).repr v).support
  refine ⟨S.sup (twiceWeight o) + 1, ?_⟩
  intro d hd
  conv_lhs => rw [← (monomialBasis o).linearCombination_repr v]
  rw [Finsupp.linearCombination_apply, Finsupp.sum, map_sum]
  apply Finset.sum_eq_zero
  intro a ha
  rw [map_smul]
  have hw : twiceWeight o a ≤ S.sup (twiceWeight o) := Finset.le_sup ha
  rw [annihilationCoefficient_cutoff_on_monomial o x d a (by omega), smul_zero]

end HMT.IV.LatticeHalfAnnihilationEnergy
end

#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.halfDegree
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.halfDegree_monomial
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.LowersWeight
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.lowersWeight_zero
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.lowersWeight_one
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.lowersWeight_smul
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.lowersWeight_sum
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.lowersWeight_mul
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.halfAnnihilate_lowersWeight
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.chargeHalfAnnihilation_lowersWeight
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.potentialCoefficient_lowersWeight
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.powerCoefficient_lowersWeight
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.exponentialCoefficient_lowersWeight
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.halfDegree_coefficient
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.negative_halfDegree_eigenvector_zero
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.annihilationCoefficient_cutoff_on_monomial
#print axioms HMT.IV.LatticeHalfAnnihilationEnergy.exists_annihilationExponential_bound
