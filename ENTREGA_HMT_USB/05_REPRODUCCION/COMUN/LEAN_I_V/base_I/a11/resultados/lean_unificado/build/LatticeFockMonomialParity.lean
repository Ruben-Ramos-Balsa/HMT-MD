import LatticeParityCarrier
import Mathlib.LinearAlgebra.SymmetricAlgebra.Basis
import Mathlib.LinearAlgebra.TensorProduct.Basis

/-!
The actual algebraic oscillator carrier, not a separately postulated model,
has its monomial basis. The already constructed negation is diagonal on this
basis in every degree, and sends lattice charge x to -x on the tensor basis.
This is the operator antecedent of the graded trace in excepcional.tex.
-/

noncomputable section
set_option maxRecDepth 4000
namespace HMT.IV.LatticeFockMonomialParity

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeParityCarrier
open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open scoped TensorProduct

abbrev Occupation (o : Fin 12) := Mode o →₀ ℕ

def oscillatorBasis (o : Fin 12) : Basis (Mode o) ℂ (Oscillators o) :=
  Finsupp.basisSingleOne

def monomialBasis (o : Fin 12) : Basis (Occupation o) ℂ (Fock o) :=
  (oscillatorBasis o).symmetricAlgebra

def occupationLength (o : Fin 12) (a : Occupation o) : ℕ :=
  a.sum fun _ k => k

def occupationWeight (o : Fin 12) (a : Occupation o) : ℕ :=
  a.sum fun p k => (p.1 + 1) * k

theorem monomialBasis_product (o : Fin 12) (a : Occupation o) :
    monomialBasis o a = a.prod (fun p k =>
      (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p)) ^ k) := by
  change (SymmetricAlgebra.equivMvPolynomial (oscillatorBasis o)).symm
    (MvPolynomial.monomial a 1) = _
  rw [MvPolynomial.monomial_eq]
  simp only [map_mul, MvPolynomial.C_1, map_one, one_mul, Finsupp.prod,
    map_prod, map_pow, SymmetricAlgebra.equivMvPolynomial_symm_X]

theorem fockTheta_monomial (o : Fin 12) (a : Occupation o) :
    fockTheta o (monomialBasis o a) =
      (-1 : ℂ) ^ occupationLength o a • monomialBasis o a := by
  rw [monomialBasis_product]
  simp only [Finsupp.prod, map_prod, map_pow, fockTheta_generator]
  have hp : (∏ p ∈ a.support,
      (-SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p)) ^ a p) =
      ∏ p ∈ a.support, (-1 : Fock o) ^ a p *
        (SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorBasis o p)) ^ a p := by
    apply Finset.prod_congr rfl
    intro p _
    exact neg_pow _ _
  rw [hp, Finset.prod_mul_distrib, Finset.prod_pow_eq_pow_sum]
  simp only [occupationLength, Finsupp.sum, Algebra.smul_def, map_pow,
    map_neg, map_one]

def latticeBasisComplex (o : Fin 12) : Basis (Lattice o) ℂ (TwistedAlgebra o) :=
  Finsupp.basisSingleOne

def carrierBasis (o : Fin 12) :
    Basis (Occupation o × Lattice o) ℂ (LatticeCarrier o) :=
  (monomialBasis o).tensorProduct (latticeBasisComplex o)

theorem carrierTheta_basis (o : Fin 12) (a : Occupation o) (x : Lattice o) :
    carrierTheta o (carrierBasis o (a, x)) =
      (-1 : ℂ) ^ occupationLength o a • carrierBasis o (a, -x) := by
  simp only [carrierBasis, Basis.tensorProduct_apply, carrierTheta_pure,
    fockTheta_monomial, TensorProduct.smul_tmul']
  congr 1
  exact WittNegationLift.theta_single o x 1

theorem vacuum_is_empty_monomial (o : Fin 12) :
    carrierBasis o (0, 0) = vacuum o := by
  simp only [carrierBasis, Basis.tensorProduct_apply, monomialBasis_product,
    Finsupp.prod_zero_index, latticeBasisComplex, Finsupp.coe_basisSingleOne]
  rfl

end HMT.IV.LatticeFockMonomialParity
end

#print axioms HMT.IV.LatticeFockMonomialParity.monomialBasis_product
#print axioms HMT.IV.LatticeFockMonomialParity.fockTheta_monomial
#print axioms HMT.IV.LatticeFockMonomialParity.carrierTheta_basis
#print axioms HMT.IV.LatticeFockMonomialParity.vacuum_is_empty_monomial
