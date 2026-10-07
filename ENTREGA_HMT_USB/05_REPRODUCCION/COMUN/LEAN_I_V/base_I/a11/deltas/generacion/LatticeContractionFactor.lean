import LatticeExponentialContraction

/-!
The normal-ordering factor is an integral power of the same formal binomial.
Its inverse and pole cancellation follow from its proved recurrence. This
does not assume a vertex-algebra locality identity.
-/

noncomputable section
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeContractionFactor

open HMT.IV.LatticeExponentialContraction
open PowerSeries
open scoped BigOperators

theorem poleSeries_add (o : Fin 12) (p q : ℤ) :
    poleSeries o (p+q) = poleSeries o p + poleSeries o q := by
  ext n
  simp only [poleSeries_coeff, map_add, Int.cast_add, add_smul]

theorem contractionSeries_constant (o : Fin 12) (p : ℤ) :
    coeff (Inner o) 0 (contractionSeries o p) = 1 := by simp

theorem contractionSeries_add (o : Fin 12) (p q : ℤ) :
    contractionSeries o (p+q) = contractionSeries o p * contractionSeries o q := by
  apply first_order_unique (-(poleSeries o (p+q)))
  · rw [contractionSeries_diff, neg_mul]
  · rw [diffSeries_mul, contractionSeries_diff, contractionSeries_diff, poleSeries_add]
    have h := (contractionSeries_commute o p (poleSeries o q)).eq
    calc
      -(poleSeries o p * contractionSeries o p) * contractionSeries o q +
          contractionSeries o p * -(poleSeries o q * contractionSeries o q) =
        -(poleSeries o p * contractionSeries o p * contractionSeries o q) -
          (contractionSeries o p * poleSeries o q) * contractionSeries o q := by
            noncomm_ring
      _ = -(poleSeries o p+poleSeries o q) *
          (contractionSeries o p * contractionSeries o q) := by rw [h]; noncomm_ring
  · simp only [coeff_zero_eq_constantCoeff_apply, map_mul]
    simp only [← coeff_zero_eq_constantCoeff_apply, contractionSeries_constant, mul_one]

theorem scalarContraction_nat_above (p n : ℕ) (hn : p < n) :
    scalarContraction (p : ℤ) n = 0 := by
  induction n with
  | zero => omega
  | succ n ih =>
    rw [scalarContraction]
    by_cases hp : n=p
    · subst n
      simp
    · rw [ih (by omega), mul_zero]

theorem contractionSeries_zero (o : Fin 12) : contractionSeries o 0 = 1 := by
  apply PowerSeries.ext
  intro n
  cases n with
  | zero => simp
  | succ n =>
    have hz : scalarContraction 0 (n+1) = 0 := by
      simpa only [Nat.cast_zero] using scalarContraction_nat_above 0 (n+1) (by omega)
    rw [contractionSeries_coeff, hz]
    simp

def crossVariable (o : Fin 12) : PowerSeries (Inner o) :=
  C (Inner o) (X : Inner o) * X

theorem contractionSeries_one (o : Fin 12) :
    contractionSeries o 1 = 1-crossVariable o := by
  apply PowerSeries.ext
  intro n
  rw [contractionSeries_coeff, map_sub]
  cases n with
  | zero => simp [crossVariable]
  | succ n =>
    cases n with
    | zero => simp [scalarContraction, crossVariable]
    | succ n =>
      have hz : scalarContraction 1 (n+1+1) = 0 := by
        simpa only [Nat.cast_one] using scalarContraction_nat_above 1 (n+1+1) (by omega)
      rw [hz]
      simp [crossVariable, coeff_C_mul_X_pow]

theorem contractionSeries_nat (o : Fin 12) (n : ℕ) :
    contractionSeries o (n : ℤ) = (1-crossVariable o)^n := by
  induction n with
  | zero => simp [contractionSeries_zero]
  | succ n ih =>
    rw [Nat.cast_add, Nat.cast_one, contractionSeries_add, ih,
      contractionSeries_one, pow_succ]

/-- Every negative exponent has a finite polynomial pole cancellation. -/
theorem contractionSeries_cancel (o : Fin 12) (p : ℤ) :
    contractionSeries o p * contractionSeries o (-p) = 1 := by
  rw [← contractionSeries_add, add_neg_cancel, contractionSeries_zero]

theorem contractionSeries_cancel_nat (o : Fin 12) (n : ℕ) :
    (1-crossVariable o)^n * contractionSeries o (-(n : ℤ)) = 1 := by
  rw [← contractionSeries_nat, contractionSeries_cancel]

end HMT.IV.LatticeContractionFactor
end

#print axioms HMT.IV.LatticeContractionFactor.contractionSeries_add
#print axioms HMT.IV.LatticeContractionFactor.scalarContraction_nat_above
#print axioms HMT.IV.LatticeContractionFactor.contractionSeries_one
#print axioms HMT.IV.LatticeContractionFactor.contractionSeries_nat
#print axioms HMT.IV.LatticeContractionFactor.contractionSeries_cancel
#print axioms HMT.IV.LatticeContractionFactor.contractionSeries_cancel_nat
