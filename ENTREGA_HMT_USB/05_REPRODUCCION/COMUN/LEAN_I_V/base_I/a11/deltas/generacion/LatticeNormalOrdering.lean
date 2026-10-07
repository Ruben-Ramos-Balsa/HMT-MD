import LatticeExponentialContraction
import LatticeAnnihilationRecurrence

/-!
Exact normal ordering for the already constructed lattice exponentials.
The scalar factor is deduced by uniqueness of the coefficient recurrence;
it is not supplied as an operator relation or a locality assumption.
-/

noncomputable section
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeNormalOrdering

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialExchange HMT.IV.LatticeExponentialContraction
open HMT.IV.LatticeAnnihilationRecurrence
open PowerSeries
open scoped BigOperators

theorem annihilationSeries_diff (o : Fin 12) (x : Lattice o) :
    diffSeries (annihilationSeries o x) =
      -(annihilatorSeries o x * annihilationSeries o x) := by
  apply PowerSeries.ext
  intro r
  rw [diffSeries_coeff, map_neg, coeff_mul]
  simp only [annihilationSeries, annihilatorSeries, coeff_mk]
  have h : (r+1) • exponentialCoefficient o x (r+1) =
      -(∑ p ∈ Finset.antidiagonal r,
        chargeAnnihilation o x p.1 * exponentialCoefficient o x p.2) := by
    rw [← Nat.cast_smul_eq_nsmul ℂ, Nat.cast_add, Nat.cast_one,
      annihilationCoefficient_recurrence_antidiagonal]
  have hm := congrArg ((C (FockEnd o)).toAddMonoidHom) h
  simp only [map_nsmul, map_neg, map_sum] at hm
  change (r+1) • C (FockEnd o) (exponentialCoefficient o x (r+1)) =
    -(∑ p ∈ Finset.antidiagonal r, C (FockEnd o)
      (chargeAnnihilation o x p.1 * exponentialCoefficient o x p.2)) at hm
  simp only [map_mul] at hm
  exact hm

theorem annihilationSeries_constant (o : Fin 12) (x : Lattice o) :
    coeff (Inner o) 0 (annihilationSeries o x) = 1 := by
  simp only [annihilationSeries, coeff_mk, annihilationExponential_constant]
  exact map_one (C (FockEnd o))

theorem contractionSeries_constant (o : Fin 12) (p : ℤ) :
    coeff (Inner o) 0 (contractionSeries o p) = 1 := by
  simp

/-- Equality of the two actual operator series in the nested expansion region.
Every coefficient is covered; no degree or charge bound is introduced. -/
theorem exponential_normal_order (o : Fin 12) (x y : Lattice o) :
    annihilationSeries o x * C (Inner o) (creationSeries o y) =
      contractionSeries o (integerPair o x y) *
        C (Inner o) (creationSeries o y) * annihilationSeries o x := by
  let A := annihilationSeries o x
  let Q := annihilatorSeries o x
  let B := contractionSeries o (integerPair o x y)
  let P := poleSeries o (integerPair o x y)
  let Cc := C (Inner o) (creationSeries o y)
  have hA : diffSeries A = -Q*A := by
    simpa only [A, Q, neg_mul] using annihilationSeries_diff o x
  have hB : diffSeries B = -P*B := by
    simpa only [B, P, neg_mul] using contractionSeries_diff o (integerPair o x y)
  have hC : diffSeries Cc = 0 := diffSeries_C _
  have hQC : Q*Cc = Cc*Q+P*Cc := annihilatorSeries_creation o x y
  have hBQ : B*Q=Q*B := (contractionSeries_commute o (integerPair o x y) Q).eq
  have hBP : B*P=P*B := (contractionSeries_commute o (integerPair o x y) P).eq
  change A*Cc=B*Cc*A
  apply first_order_unique (-Q)
  · rw [diffSeries_mul, hA, hC]
    noncomm_ring
  · rw [diffSeries_mul, diffSeries_mul, hB, hC, hA]
    calc
      (-P * B * Cc + B * 0) * A + B * Cc * (-Q * A) =
          -(P*B*Cc+B*Cc*Q)*A := by noncomm_ring
      _ = -(B*(P*Cc+Cc*Q))*A := by rw [← hBP]; noncomm_ring
      _ = -(B*(Q*Cc))*A := by rw [add_comm (P*Cc), ← hQC]
      _ = -Q*(B*Cc*A) := by rw [← mul_assoc B, hBQ]; noncomm_ring
  · simp only [coeff_zero_eq_constantCoeff_apply, map_mul]
    simp only [← coeff_zero_eq_constantCoeff_apply, A, B, Cc,
      contractionSeries_constant, annihilationSeries_constant,
      coeff_C, if_pos rfl, one_mul, mul_one]

/-- Coefficient form of normal ordering, retaining both degrees separately. -/
theorem exponential_normal_order_coefficient (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) :
    exponentialCoefficient o x r * creationExponentialMode o y d =
      ∑ p ∈ Finset.antidiagonal r,
        scalarContraction (integerPair o x y) p.1 •
          (if p.1 ≤ d then creationExponentialMode o y (d-p.1) *
            exponentialCoefficient o x p.2 else 0) := by
  have h0 := congrArg (coeff (Inner o) r) (exponential_normal_order o x y)
  rw [coeff_mul_C] at h0
  conv_rhs at h0 => rw [coeff_mul]
  simp only [coeff_mul_C, annihilationSeries, coeff_mk, contractionSeries_coeff] at h0
  have h := congrArg (coeff (FockEnd o) d) h0
  simp only [map_sum, coeff_C_mul, coeff_mul_C, smul_mul_assoc,
    coeff_smul, coeff_X_pow_mul', creationSeries, coeff_mk] at h
  simpa only [smul_mul_assoc, ite_mul, zero_mul] using h

end HMT.IV.LatticeNormalOrdering
end

#print axioms HMT.IV.LatticeNormalOrdering.annihilationSeries_diff
#print axioms HMT.IV.LatticeNormalOrdering.exponential_normal_order
#print axioms HMT.IV.LatticeNormalOrdering.exponential_normal_order_coefficient
