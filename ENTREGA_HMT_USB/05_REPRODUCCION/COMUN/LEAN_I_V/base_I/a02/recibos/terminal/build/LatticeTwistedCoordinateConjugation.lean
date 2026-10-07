import LatticeTwistedCoordinateSign
import LatticeTwistedCoordinateExponential

/-! The coordinate sign conjugates the existing positive-sector exponential
to its proved formal inverse. No analytic convergence assertion is used. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedCoordinateConjugation
open LatticeTwistedPositiveSector LatticeTwistedContragredientTruncation
open LatticeTwistedCoordinateSign LatticeTwistedCoordinateExponential
open PowerSeries

theorem inverseCoefficient_eq_signed (o : Fin 12) (n : ℕ) :
    coeff (EndSpace o) n (inverseCoordinateExponential o) =
      (-1 : ℂ)^n • inversionCoefficient o n := by
  rw [inverseCoordinateExponential_coefficient, ← neg_one_smul ℂ (lowering o), smul_pow]
  simp only [inversionCoefficient]
  module

theorem sign_conjugates_exponential (o : Fin 12) :
    C (EndSpace o) (coordinateSign o) * coordinateExponential o *
      C (EndSpace o) (coordinateSign o) = inverseCoordinateExponential o := by
  apply PowerSeries.ext
  intro n
  rw [coeff_mul_C, coeff_C_mul, coordinateExponential, coeff_mk,
    coordinateSign_inversionCoefficient, inverseCoefficient_eq_signed]

theorem sign_conjugates_inverse (o : Fin 12) :
    C (EndSpace o) (coordinateSign o) * inverseCoordinateExponential o *
      C (EndSpace o) (coordinateSign o) = coordinateExponential o := by
  apply PowerSeries.ext
  intro n
  rw [coeff_mul_C, coeff_C_mul, inverseCoefficient_eq_signed,
    mul_smul_comm, smul_mul_assoc, coordinateSign_inversionCoefficient,
    coordinateExponential, coeff_mk, smul_smul, ← mul_pow]
  simp

theorem signed_exponential_square (o : Fin 12) :
    (coordinateExponential o * C (EndSpace o) (coordinateSign o)) *
      (coordinateExponential o * C (EndSpace o) (coordinateSign o)) = 1 := by
  calc
    _ = coordinateExponential o *
        (C (EndSpace o) (coordinateSign o) * coordinateExponential o *
          C (EndSpace o) (coordinateSign o)) := by simp only [mul_assoc]
    _ = 1 := by rw [sign_conjugates_exponential, coordinateExponential_mul_inverse]

end HMT.IV.LatticeTwistedCoordinateConjugation
end
