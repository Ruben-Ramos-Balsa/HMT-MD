import LatticeTwistedStateConformal
import LatticeTwistedPositiveStateDescent
import LatticeEvenConformal

/-! Restriction and descent of the corrected conformal field identify its
actual coefficients with the inherited positive-sector conformal operators.
No new Virasoro or twisted-module axiom is assumed. -/
noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedPositiveConformal
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeEvenConformal LatticeTwistedPositiveSector
open LatticeTwistedStateField LatticeTwistedStateConformal
open LatticeTwistedPositiveStateDescent

theorem positiveStateCoefficient_conformal (o : Fin 12) (m : ℤ) :
    positiveStateCoefficient o (evenConformalState o) (-2*m-4) =
      positiveConformalMode o m := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  rw [positiveStateCoefficient_coe, evenConformalState_coe,
    twistedStateField_conformalState_coefficient, positiveConformalMode_coe]

theorem positiveDescendedAssignment_conformal_coefficient (o : Fin 12) (m : ℤ) :
    HVertexOperator.coeff (positiveDescendedAssignment o (evenConformalState o)) (-m-2) =
      positiveConformalMode o m := by
  change positiveStateCoefficient o (evenConformalState o) (2*(-m-2)) = _
  rw [show 2*(-m-2) = -2*m-4 by omega, positiveStateCoefficient_conformal]

theorem positiveDescendedField_conformal_coefficient (o : Fin 12) (m : ℤ) :
    HVertexOperator.coeff (positiveDescendedField o (evenConformalState o)) (-m-2) =
      positiveConformalMode o m :=
  positiveDescendedAssignment_conformal_coefficient o m

end HMT.IV.LatticeTwistedPositiveConformal
end

#print axioms HMT.IV.LatticeTwistedPositiveConformal.positiveStateCoefficient_conformal
#print axioms HMT.IV.LatticeTwistedPositiveConformal.positiveDescendedAssignment_conformal_coefficient
#print axioms HMT.IV.LatticeTwistedPositiveConformal.positiveDescendedField_conformal_coefficient
