import LatticeNormalOrdering
import LatticeContractionFactor

/-!
Finite polynomial exchange for the actual creation/annihilation series.
The exponents are produced by the inherited integral pairing. This is an
identity in one nested expansion region, not an assumed two-region locality
or an orbifold product.
-/

noncomputable section
namespace HMT.IV.LatticePolynomialExchange

open HMT.IV.LatticeCocycle
open HMT.IV.LatticeExponentialContraction
open HMT.IV.LatticeContractionFactor
open HMT.IV.LatticeNormalOrdering
open PowerSeries

theorem normal_order_nonnegative (o : Fin 12) (x y : Lattice o) (n : ℕ)
    (h : integerPair o x y = (n : ℤ)) :
    annihilationSeries o x * C (Inner o) (creationSeries o y) =
      (1-crossVariable o)^n *
        (C (Inner o) (creationSeries o y) * annihilationSeries o x) := by
  rw [exponential_normal_order, h, contractionSeries_nat, mul_assoc]

theorem normal_order_negative (o : Fin 12) (x y : Lattice o) (n : ℕ)
    (h : integerPair o x y = -(n : ℤ)) :
    (1-crossVariable o)^n *
        (annihilationSeries o x * C (Inner o) (creationSeries o y)) =
      C (Inner o) (creationSeries o y) * annihilationSeries o x := by
  rw [exponential_normal_order, h]
  calc
    (1-crossVariable o)^n *
        (contractionSeries o (-(n : ℤ)) * C (Inner o) (creationSeries o y) *
          annihilationSeries o x) =
      ((1-crossVariable o)^n * contractionSeries o (-(n : ℤ))) *
        (C (Inner o) (creationSeries o y) * annihilationSeries o x) := by
          simp only [mul_assoc]
    _ = _ := by rw [contractionSeries_cancel_nat, one_mul]

/-- Finite pole orders exist for every pair of charges of the constructed lattice. -/
theorem polynomial_exchange_all_charges (o : Fin 12) (x y : Lattice o) :
    ∃ n m : ℕ, (m : ℤ)-(n : ℤ)=integerPair o x y ∧
      (1-crossVariable o)^n *
          (annihilationSeries o x * C (Inner o) (creationSeries o y)) =
        (1-crossVariable o)^m *
          (C (Inner o) (creationSeries o y) * annihilationSeries o x) := by
  cases h : integerPair o x y with
  | ofNat m =>
    refine ⟨0,m,by simp,?_⟩
    simpa only [pow_zero, one_mul] using normal_order_nonnegative o x y m h
  | negSucc n =>
    refine ⟨n+1,0,by omega,?_⟩
    have hp : integerPair o x y = -((n+1 : ℕ) : ℤ) := by omega
    simpa only [pow_zero, one_mul] using normal_order_negative o x y (n+1) hp

end HMT.IV.LatticePolynomialExchange
end

#print axioms HMT.IV.LatticePolynomialExchange.normal_order_nonnegative
#print axioms HMT.IV.LatticePolynomialExchange.normal_order_negative
#print axioms HMT.IV.LatticePolynomialExchange.polynomial_exchange_all_charges
