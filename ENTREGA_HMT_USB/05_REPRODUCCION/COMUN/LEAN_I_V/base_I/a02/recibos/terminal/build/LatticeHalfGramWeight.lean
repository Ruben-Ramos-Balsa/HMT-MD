import LatticeHalfFockPairing
import LatticeTwistedGrading

/-! The Gram transport preserves the actual conformal zero-mode grading.
This is a commutation proof on the unbounded oscillator algebra, not a new
grading or a finite frequency cutoff. -/

noncomputable section
namespace HMT.IV.LatticeHalfGramWeight
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity LatticeModeWeights
open LatticeHalfIntegerHeisenberg LatticeHalfConformalModes LatticeHalfWeightBasis
open LatticeHalfConformalVacuum LatticeHalfGramTransport LatticeFactorialPairing
open HMT.FockTransport.Symmetric
open scoped BigOperators

theorem block_gamma_create (o : Fin 12)
    (A : Fin (BasisSize o) → Fin (BasisSize o) → ℂ) (s : ℕ → ℂ)
    (n : ℕ) (i : Fin (BasisSize o)) (v : Fock o) :
    gamma (blockMap o A s) (create o n i v) =
      ∑ j, (s n*A i j) • create o n j (gamma (blockMap o A s) v) := by
  change gamma (blockMap o A s)
    (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i)*v) = _
  rw [map_mul, gamma_generator, blockMap_mode]
  simp only [map_sum, map_smul, Finset.sum_mul, smul_mul_assoc]
  rfl

theorem block_gamma_quadratic_create (o : Fin 12)
    (A : Fin (BasisSize o) → Fin (BasisSize o) → ℂ) (s : ℕ → ℂ)
    (n : ℕ) (i : Fin (BasisSize o)) (v : Fock o)
    (h : quadraticMode o 0 (gamma (blockMap o A s) v) =
      gamma (blockMap o A s) (quadraticMode o 0 v)) :
    quadraticMode o 0 (gamma (blockMap o A s) (create o n i v)) =
      gamma (blockMap o A s) (quadraticMode o 0 (create o n i v)) := by
  rw [block_gamma_create, map_sum, quadratic_zero_create, map_add, map_smul,
    block_gamma_create, block_gamma_create]
  simp only [map_smul, quadratic_zero_create, h, smul_add,
    Finset.sum_add_distrib, Finset.smul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  exact smul_comm _ _ _

theorem block_gamma_quadratic (o : Fin 12)
    (A : Fin (BasisSize o) → Fin (BasisSize o) → ℂ) (s : ℕ → ℂ)
    (v : Fock o) :
    quadraticMode o 0 (gamma (blockMap o A s) v) =
      gamma (blockMap o A s) (quadraticMode o 0 v) := by
  have hm (a : Occupation o) :
      quadraticMode o 0 (gamma (blockMap o A s) (monomialBasis o a)) =
        gamma (blockMap o A s) (quadraticMode o 0 (monomialBasis o a)) := by
    classical
    induction a using Finsupp.induction with
    | zero =>
      rw [monomialBasis_product, Finsupp.prod_zero_index, map_one,
        quadraticMode_nonnegative_vacuum o 0 (by omega), map_zero]
    | @single_add p k a _ hk0 ih =>
      clear hk0
      induction k with
      | zero => simpa using ih
      | succ k hk =>
        have heq : Finsupp.single p (k+1)+a =
            Finsupp.single p 1+(Finsupp.single p k+a) := by
          rw [← add_assoc, ← Finsupp.single_add]
          congr 2
          omega
        rw [heq, ← create_monomial]
        exact block_gamma_quadratic_create o A s p.1 p.2 _ hk
  have he : (quadraticMode o 0).comp (gamma (blockMap o A s)).toLinearMap =
      (gamma (blockMap o A s)).toLinearMap.comp (quadraticMode o 0) := by
    apply (monomialBasis o).ext
    exact hm
  exact LinearMap.congr_fun he v

theorem block_gamma_coefficient_off_weight (o : Fin 12)
    (A : Fin (BasisSize o) → Fin (BasisSize o) → ℂ) (s : ℕ → ℂ)
    (a b : Occupation o) (hab : twiceWeight o a ≠ twiceWeight o b) :
    (monomialBasis o).repr (gamma (blockMap o A s) (monomialBasis o a)) b = 0 := by
  classical
  let c := (monomialBasis o).repr (gamma (blockMap o A s) (monomialBasis o a))
  have diagonal (v : Fock o) :
      (monomialBasis o).repr (quadraticMode o 0 v) b =
        ((twiceWeight o b : ℂ)/2) * (monomialBasis o).repr v b := by
    have he : ((monomialBasis o).coord b).comp (quadraticMode o 0) =
        ((twiceWeight o b : ℂ)/2) • (monomialBasis o).coord b := by
      apply (monomialBasis o).ext
      intro q
      simp only [LinearMap.comp_apply, quadratic_zero_monomial, map_smul,
        LinearMap.smul_apply, Basis.coord_apply, Basis.repr_self,
        Finsupp.single_apply, smul_eq_mul]
      split_ifs with hq
      · subst q; rfl
      · simp
    exact LinearMap.congr_fun he v
  have h := congrArg (fun v => (monomialBasis o).repr v b)
    (block_gamma_quadratic o A s (monomialBasis o a))
  dsimp only at h
  rw [diagonal, quadratic_zero_monomial] at h
  simp only [map_smul, Finsupp.smul_apply, smul_eq_mul] at h
  by_contra hn
  have hw := mul_right_cancel₀ hn h
  have hc : (twiceWeight o b : ℂ) = (twiceWeight o a : ℂ) := by
    linear_combination 2*hw
  exact hab (by exact_mod_cast hc.symm)

end HMT.IV.LatticeHalfGramWeight
end
