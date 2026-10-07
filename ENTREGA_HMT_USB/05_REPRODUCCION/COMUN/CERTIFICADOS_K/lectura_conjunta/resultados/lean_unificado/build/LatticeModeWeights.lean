import LatticeFockMonomialParity
import LatticeHeisenbergModes
import Mathlib.Algebra.MvPolynomial.Derivation

/-! Action of the existing Heisenberg operators on the actual monomial
basis. Polynomial coordinates are only a proof representation of those
operators. No independent creation or annihilation operator is substituted.
-/

noncomputable section
namespace HMT.IV.LatticeModeWeights

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCocycle HMT.FockTransport.Symmetric
open scoped BigOperators

def polynomialEquiv (o : Fin 12) :=
  SymmetricAlgebra.equivMvPolynomial (oscillatorBasis o)

@[simp] theorem polynomialEquiv_monomial (o : Fin 12) (a : Occupation o) :
    polynomialEquiv o (monomialBasis o a) = MvPolynomial.monomial a 1 := by
  change (SymmetricAlgebra.equivMvPolynomial (oscillatorBasis o))
    ((SymmetricAlgebra.equivMvPolynomial (oscillatorBasis o)).symm
      (MvPolynomial.monomial a 1)) = _
  exact AlgEquiv.apply_symm_apply _ _

@[simp] theorem oscillatorBasis_mode (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) : oscillatorBasis o (n,i) = modeVector o n i := rfl

theorem create_monomial (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (a : Occupation o) :
    create o n i (monomialBasis o a) =
      monomialBasis o (Finsupp.single (n,i) 1 + a) := by
  apply (polynomialEquiv o).injective
  change polynomialEquiv o
    (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i) * monomialBasis o a) = _
  rw [map_mul, polynomialEquiv_monomial, polynomialEquiv_monomial]
  have hgen : polynomialEquiv o
      (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i)) =
      MvPolynomial.X (R := ℂ) (n,i) :=
    SymmetricAlgebra.equivMvPolynomial_ι_apply (oscillatorBasis o) (n,i)
  rw [hgen]
  simp only [MvPolynomial.X, MvPolynomial.monomial_mul, one_mul]

theorem occupationWeight_add (o : Fin 12) (a b : Occupation o) :
    occupationWeight o (a+b) = occupationWeight o a + occupationWeight o b := by
  unfold occupationWeight
  exact Finsupp.sum_add_index' (by intros; simp) (by intros; simp [mul_add])

@[simp] theorem occupationWeight_single (o : Fin 12) (p : Mode o) (k : ℕ) :
    occupationWeight o (Finsupp.single p k) = (p.1+1)*k := by
  simp [occupationWeight]

theorem create_monomial_weight (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (a : Occupation o) :
    occupationWeight o (Finsupp.single (n,i) 1 + a) =
      occupationWeight o a + (n+1) := by
  rw [occupationWeight_add, occupationWeight_single]
  simp [add_comm]

theorem remove_mode_weight (o : Fin 12) (a : Occupation o) (p : Mode o)
    (hp : a p ≠ 0) :
    occupationWeight o (a-Finsupp.single p 1) + (p.1+1) =
      occupationWeight o a := by
  have hle : Finsupp.single p 1 ≤ a := by
    rw [Finsupp.single_le_iff]
    omega
  have hsum : a-Finsupp.single p 1 + Finsupp.single p 1 = a :=
    tsub_add_cancel_of_le hle
  have hw := congrArg (occupationWeight o) hsum
  simpa only [occupationWeight_add, occupationWeight_single, mul_one] using hw

/-- The existing annihilation derivation in polynomial coordinates. -/
def transportedAnnihilation (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    Derivation ℂ (MvPolynomial (Mode o) ℂ) (MvPolynomial (Mode o) ℂ) where
  toLinearMap := (polynomialEquiv o).toLinearMap.comp
    ((annihilation (modeCovector o n i)).toLinearMap.comp
      (polynomialEquiv o).symm.toLinearMap)
  map_one_eq_zero' := by simp
  leibniz' x y := by
    change polynomialEquiv o (annihilation (modeCovector o n i)
      ((polynomialEquiv o).symm (x*y))) = _
    rw [map_mul, annihilation_product, map_add, map_mul, map_mul]
    simp only [AlgEquiv.apply_symm_apply, smul_eq_mul]
    rfl

@[simp] theorem transportedAnnihilation_X (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (p : Mode o) :
    transportedAnnihilation o n i (MvPolynomial.X p) =
      MvPolynomial.C (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0) := by
  change polynomialEquiv o (annihilation (modeCovector o n i)
    ((polynomialEquiv o).symm (MvPolynomial.X p))) = _
  have hs : (polynomialEquiv o).symm (MvPolynomial.X p) =
      SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p) :=
    SymmetricAlgebra.equivMvPolynomial_symm_X _ p
  rw [hs, annihilation_generator, AlgEquiv.commutes]
  cases p with
  | mk m j =>
    simp only [oscillatorBasis_mode, modeCovector_modeVector]
    rfl

theorem transportedAnnihilation_eq_mk (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) :
    transportedAnnihilation o n i = MvPolynomial.mkDerivation ℂ
      (fun p : Mode o => MvPolynomial.C
        (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0)) := by
  apply MvPolynomial.derivation_ext
  intro p
  rw [transportedAnnihilation_X, MvPolynomial.mkDerivation_X]

theorem annihilate_monomial_coordinates (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (a : Occupation o) :
    polynomialEquiv o (annihilate o n i (monomialBasis o a)) =
      a.sum (fun p k => MvPolynomial.monomial (a-Finsupp.single p 1)
        ((k : ℂ) * (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0))) := by
  have he : polynomialEquiv o (annihilate o n i (monomialBasis o a)) =
      transportedAnnihilation o n i (MvPolynomial.monomial a 1) := by
    change _ = polynomialEquiv o (annihilate o n i
      ((polynomialEquiv o).symm (MvPolynomial.monomial a 1)))
    congr 2
  rw [he, transportedAnnihilation_eq_mk, MvPolynomial.mkDerivation_monomial,
    one_smul]
  apply Finsupp.sum_congr
  intro p _
  simp only [smul_eq_mul]
  rw [mul_comm, MvPolynomial.C_mul_monomial, mul_comm]

theorem annihilate_monomial (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (a : Occupation o) :
    annihilate o n i (monomialBasis o a) =
      a.sum (fun p k =>
        ((k : ℂ) * (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0)) •
          monomialBasis o (a-Finsupp.single p 1)) := by
  apply (polynomialEquiv o).injective
  rw [annihilate_monomial_coordinates]
  simp only [Finsupp.sum, map_sum, map_smul, polynomialEquiv_monomial]
  apply Finset.sum_congr rfl
  intro p _
  simp only [MvPolynomial.smul_monomial, smul_eq_mul, mul_one]

theorem annihilate_nonzero_term_weight (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (a : Occupation o) (p : Mode o)
    (h : (a p : ℂ) * (if n=p.1 then (n+1 : ℂ)*gram o i p.2 else 0) ≠ 0) :
    occupationWeight o (a-Finsupp.single p 1) + (n+1) =
      occupationWeight o a := by
  have hphase : n=p.1 := by by_contra hn; simp [hn] at h
  have ha : a p ≠ 0 := by intro hz; simp [hz] at h
  rw [hphase]
  exact remove_mode_weight o a p ha

end HMT.IV.LatticeModeWeights
end

#print axioms HMT.IV.LatticeModeWeights.create_monomial
#print axioms HMT.IV.LatticeModeWeights.occupationWeight_add
#print axioms HMT.IV.LatticeModeWeights.create_monomial_weight
#print axioms HMT.IV.LatticeModeWeights.remove_mode_weight
#print axioms HMT.IV.LatticeModeWeights.transportedAnnihilation_eq_mk
#print axioms HMT.IV.LatticeModeWeights.annihilate_monomial_coordinates
#print axioms HMT.IV.LatticeModeWeights.annihilate_monomial
#print axioms HMT.IV.LatticeModeWeights.annihilate_nonzero_term_weight
