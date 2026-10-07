import Mathlib.LinearAlgebra.Trace
import Mathlib.LinearAlgebra.Matrix.Diagonal
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Polynomial.BigOperators
import Mathlib.Tactic

/-!
# Finite weight pieces of the oscillator parity trace

The index set records N positive frequencies and r independent directions.
All occupations of weight d are represented, not just numerical examples.
The diagonal is the parity action on these monomial labels. Its connection
to the actual symmetric-algebra action is supplied by a separate module.
The theorem here equates its trace with the coefficient of a finite product.
It does not assert the twisted-sector construction or the FLM theorem.
-/

noncomputable section
namespace HMT.IV.WeightedOscillatorTrace

open scoped BigOperators
open Polynomial

abbrev Mode (N r : ℕ) := Fin N × Fin r
abbrev Occupation (d N r : ℕ) := Mode N r → Fin (d + 1)

def occupationWeight {d N r : ℕ} (a : Occupation d N r) : ℕ :=
  ∑ p, (p.1.val + 1) * (a p).val

def occupationLength {d N r : ℕ} (a : Occupation d N r) : ℕ :=
  ∑ p, (a p).val

abbrev WeightPiece (d N r : ℕ) :=
  {a : Occupation d N r // occupationWeight a = d}

abbrev PieceSpace (d N r : ℕ) := WeightPiece d N r → ℂ

def diagonalSign {d N r : ℕ} (a : WeightPiece d N r) : ℂ :=
  (-1) ^ occupationLength a.val

def parityOperator (d N r : ℕ) : Module.End ℂ (PieceSpace d N r) :=
  Matrix.toLin' (Matrix.diagonal diagonalSign)

@[simp] theorem parityOperator_apply (d N r : ℕ)
    (v : PieceSpace d N r) (a : WeightPiece d N r) :
    parityOperator d N r v a = diagonalSign a * v a := by
  simp [parityOperator, Matrix.toLin'_apply, Matrix.mulVec_diagonal]

theorem piece_finrank (d N r : ℕ) :
    Module.finrank ℂ (PieceSpace d N r) = Fintype.card (WeightPiece d N r) := by
  exact Module.finrank_pi _

theorem trace_parityOperator (d N r : ℕ) :
    LinearMap.trace ℂ (PieceSpace d N r) (parityOperator d N r) =
      ∑ a : WeightPiece d N r, (-1 : ℂ) ^ occupationLength a.val := by
  rw [LinearMap.trace_eq_matrix_trace ℂ (Pi.basisFun ℂ (WeightPiece d N r))]
  simp [parityOperator, LinearMap.toMatrix_eq_toMatrix', Matrix.trace,
    diagonalSign]

def geometricFactor (d : ℕ) (frequency : ℕ) : ℂ[X] :=
  ∑ k : Fin (d + 1), monomial (frequency * k.val) ((-1 : ℂ) ^ k.val)

def finiteProduct (d N r : ℕ) : ℂ[X] :=
  ∏ p : Mode N r, geometricFactor d (p.1.val + 1)

theorem prod_monomial {ι : Type*} [Fintype ι]
    (w : ι → ℕ) (c : ι → ℂ) :
    (∏ i, monomial (w i) (c i)) = monomial (∑ i, w i) (∏ i, c i) := by
  classical
  suffices h : ∀ s : Finset ι,
      (∏ i ∈ s, monomial (w i) (c i)) =
        monomial (∑ i ∈ s, w i) (∏ i ∈ s, c i) by
    exact h Finset.univ
  intro s
  induction s using Finset.induction_on with
  | empty => simp
  | @insert i s hi ih =>
    simp only [Finset.prod_insert hi, Finset.sum_insert hi]
    rw [ih, monomial_mul_monomial]

theorem product_expansion (d N r : ℕ) :
    finiteProduct d N r =
      ∑ a : Occupation d N r,
        monomial (occupationWeight a) ((-1 : ℂ) ^ occupationLength a) := by
  unfold finiteProduct geometricFactor
  rw [Fintype.prod_sum]
  apply Finset.sum_congr rfl
  intro a _
  rw [prod_monomial]
  simp only [occupationWeight, occupationLength, Finset.prod_pow_eq_pow_sum]

theorem coefficient_sum_all (d N r : ℕ) :
    (finiteProduct d N r).coeff d =
      ∑ a : Occupation d N r,
        if occupationWeight a = d then (-1 : ℂ) ^ occupationLength a else 0 := by
  rw [product_expansion]
  simp only [finset_sum_coeff, coeff_monomial]

theorem coefficient_weight_piece (d N r : ℕ) :
    (finiteProduct d N r).coeff d =
      ∑ a : WeightPiece d N r, (-1 : ℂ) ^ occupationLength a.val := by
  rw [coefficient_sum_all]
  rw [← Finset.sum_filter]
  exact Finset.sum_subtype _ (by simp) _

theorem trace_eq_product_coefficient (d N r : ℕ) :
    LinearMap.trace ℂ (PieceSpace d N r) (parityOperator d N r) =
      (finiteProduct d N r).coeff d := by
  rw [trace_parityOperator, coefficient_weight_piece]

end HMT.IV.WeightedOscillatorTrace
end

#print axioms HMT.IV.WeightedOscillatorTrace.parityOperator_apply
#print axioms HMT.IV.WeightedOscillatorTrace.piece_finrank
#print axioms HMT.IV.WeightedOscillatorTrace.trace_parityOperator
#print axioms HMT.IV.WeightedOscillatorTrace.product_expansion
#print axioms HMT.IV.WeightedOscillatorTrace.coefficient_weight_piece
#print axioms HMT.IV.WeightedOscillatorTrace.trace_eq_product_coefficient
