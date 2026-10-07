import ElectronComposition
import ElectronGeneratedLedgerBridge

/-!
# Electronic scalar composition realized by the generated Article VI operator

This module composes two previously verified outputs.  `ElectronComposition`
produces the positive central electronic scalar from the regional injection,
the local commutator entry, the deficit, memory and the two coincident return
readers.  `ElectronGeneratedLedgerBridge` produces the complete 108-position
nonadic ledger and the positive Article VI mass operator.

The theorems below use the generated scalar as the reference coordinate of
that operator and prove that its action on the central electronic fibre is
exactly the scalar composition already proved in `ElectronComposition`.
The dimensional unit remains explicit; no observed mass or metrological table
is used to select a route, coefficient, exponent or reference coordinate.
-/

namespace HMT.VI.ElectronMassRealization

open HMT.VI.MassOperator
open HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature
open HMTMassCharacter

noncomputable section

/-- The generated dimensionless electronic basal coordinate with an explicit
positive dimensional unit.  The unit supplies dimension, not calibration of
the APP--TRIT--TPK output. -/
def electronReferenceMass (massUnit p phi alpha delta : ℝ) : ℝ :=
  massUnit * ElectronComposition.basal p phi alpha delta

theorem electron_reference_mass_formula (massUnit p phi alpha delta : ℝ) :
    electronReferenceMass massUnit p phi alpha delta =
      massUnit * (Real.sqrt 3 / 4 *
        (Real.exp (phi / p ^ 2) - 22 * alpha ^ 3) *
        (1 + 15 * delta)) := by
  rw [electronReferenceMass, ElectronComposition.basal_formula]

theorem electron_reference_mass_positive
    {massUnit p phi alpha delta : ℝ}
    (hmassUnit : 0 < massUnit) (hp : 0 < p) (hphi : 0 < phi)
    (ha : 0 < alpha) (ha1 : alpha < 1 / 100) (hdelta : 0 ≤ delta) :
    0 < electronReferenceMass massUnit p phi alpha delta := by
  exact mul_pos hmassUnit
    (ElectronComposition.basal_positive p phi alpha delta
      hp hphi ha ha1 hdelta)

/-- The generated electronic reference coordinate inserted into the positive
central mass operator. -/
def electronMassOperator
    (Ract massUnit p phi alpha delta x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) : End CentralRoute :=
  centralMassOperator Ract
    (electronReferenceMass massUnit p phi alpha delta)
    x y delta alpha r η

theorem electron_mass_operator_positive
    (Ract : ℝ) {massUnit p phi alpha delta : ℝ}
    (hmassUnit : 0 < massUnit) (hp : 0 < p) (hphi : 0 < phi)
    (ha : 0 < alpha) (ha1 : alpha < 1 / 100) (hdelta : 0 ≤ delta)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    (electronMassOperator Ract massUnit p phi alpha delta x y r η).IsPositive := by
  exact central_mass_operator_positive Ract
    (electron_reference_mass_positive hmassUnit hp hphi ha ha1 hdelta)
    x y delta alpha r η

/-- The central route is compared with itself and therefore contributes the
unit relative character.  This conclusion is derived from the generated
signature and refinement, rather than installed as a normalization axiom. -/
theorem central_relative_character_is_one
    (x y delta : ℝ) (η : Refinement (internalMoments x y)) :
    refinedCharacter
        (internalCoordinates x y delta (internalMoments x y 120))
        (signature centralDigitalRoute - signature centralDigitalRoute)
        (η.sub η) = 1 := by
  unfold refinedCharacter refinedExponent
  rw [Refinement.value_sub]
  simp

/-- For a positive action ratio, the `rpow` used by the operator is exactly
the exponential return multiplier already derived from the two central
electronic readers. -/
theorem return_rpow_eq_generated_multiplier
    {Ract : ℝ} (hRact : 0 < Ract) (alpha delta : ℝ) :
    Ract ^ (80 - 54 * alpha + 6 * delta) =
      ElectronComposition.returnMultiplier alpha delta Ract := by
  rw [ElectronComposition.returnMultiplier,
    ElectronComposition.generated_exponent,
    Real.rpow_def_of_pos hRact]
  congr 1
  ring

/-- Exact action of the Article VI operator on the central electronic basis:
the full generated ledger contributes the unit relative character and the
remaining scalar is the independently formalized electronic composition,
with a common dimensional unit carried once. -/
theorem electron_mass_operator_basis
    {Ract : ℝ} (hRact : 0 < Ract)
    (massUnit p phi alpha delta x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) :
    electronMassOperator Ract massUnit p phi alpha delta x y r η
        (routeBasis CentralRoute.electron) =
      (massUnit * ElectronComposition.composition
        p phi alpha delta Ract : ℝ) • routeBasis CentralRoute.electron := by
  unfold electronMassOperator
  rw [central_mass_operator_basis hRact]
  rw [central_relative_character_is_one]
  rw [return_rpow_eq_generated_multiplier hRact]
  unfold electronReferenceMass ElectronComposition.composition
  ring

/-- Fully expanded central-basis formula, retaining every generated factor
and the explicit dimensional unit. -/
theorem electron_mass_operator_basis_expanded
    {Ract : ℝ} (hRact : 0 < Ract)
    (massUnit p phi alpha delta x y : ℝ) (r : Reader)
    (η : Refinement (internalMoments x y)) :
    electronMassOperator Ract massUnit p phi alpha delta x y r η
        (routeBasis CentralRoute.electron) =
      (massUnit * (Real.sqrt 3 / 4 *
        (Real.exp (phi / p ^ 2) - 22 * alpha ^ 3) *
        (1 + 15 * delta) *
        Real.exp ((80 - 54 * alpha + 6 * delta) * Real.log Ract)) : ℝ) •
        routeBasis CentralRoute.electron := by
  rw [electron_mass_operator_basis hRact]
  rw [ElectronComposition.composition_formula]

/-- Specialization to the regional HMT outputs already constructed upstream:
closure, autoscale, dodecaphase alpha publication and full regional torsion. -/
def regionalElectronReferenceMass
    (massUnit : ℝ) (register : RadixRecovery.K12) : ℝ :=
  electronReferenceMass massUnit ClosureAnalytic.value
    AlphaCarryLimit.autoscaleValue (AlphaCarryLimit.value register)
    ElectronComposition.regionalFull

def regionalElectronMassOperator
    (Ract massUnit x y : ℝ) (register : RadixRecovery.K12) (r : Reader)
    (η : Refinement (internalMoments x y)) : End CentralRoute :=
  electronMassOperator Ract massUnit ClosureAnalytic.value
    AlphaCarryLimit.autoscaleValue (AlphaCarryLimit.value register)
    ElectronComposition.regionalFull x y r η

theorem regional_electron_reference_mass_positive
    {massUnit : ℝ} (hmassUnit : 0 < massUnit)
    (register : RadixRecovery.K12)
    (ha : 0 < AlphaCarryLimit.value register)
    (ha1 : AlphaCarryLimit.value register < 1 / 100) :
    0 < regionalElectronReferenceMass massUnit register := by
  unfold regionalElectronReferenceMass
  apply electron_reference_mass_positive hmassUnit
  · have hp := AlphaPositionalBridge.closure_integer_part
    linarith
  · have hphi := AlphaPositionalBridge.autoscale_integer_part
    linarith
  · exact ha
  · exact ha1
  · exact ElectronComposition.regional_full_pos.le

theorem regional_electron_mass_operator_positive
    (Ract : ℝ) {massUnit : ℝ} (hmassUnit : 0 < massUnit)
    (register : RadixRecovery.K12)
    (ha : 0 < AlphaCarryLimit.value register)
    (ha1 : AlphaCarryLimit.value register < 1 / 100)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    (regionalElectronMassOperator Ract massUnit x y register r η).IsPositive := by
  unfold regionalElectronMassOperator
  apply electron_mass_operator_positive Ract hmassUnit
  · have hp := AlphaPositionalBridge.closure_integer_part
    linarith
  · have hphi := AlphaPositionalBridge.autoscale_integer_part
    linarith
  · exact ha
  · exact ha1
  · exact ElectronComposition.regional_full_pos.le

/-- The concrete regional specialization: the central-basis coefficient is
the upstream generated `regionalComposition`, times the dimensional unit. -/
theorem regional_electron_mass_operator_basis
    {Ract : ℝ} (hRact : 0 < Ract)
    (massUnit x y : ℝ) (register : RadixRecovery.K12) (r : Reader)
    (η : Refinement (internalMoments x y)) :
    regionalElectronMassOperator Ract massUnit x y register r η
        (routeBasis CentralRoute.electron) =
      (massUnit * ElectronComposition.regionalComposition register Ract : ℝ) •
        routeBasis CentralRoute.electron := by
  unfold regionalElectronMassOperator ElectronComposition.regionalComposition
  exact electron_mass_operator_basis hRact massUnit ClosureAnalytic.value
    AlphaCarryLimit.autoscaleValue (AlphaCarryLimit.value register)
    ElectronComposition.regionalFull x y r η

#print axioms electron_reference_mass_formula
#print axioms electron_reference_mass_positive
#print axioms electron_mass_operator_positive
#print axioms central_relative_character_is_one
#print axioms return_rpow_eq_generated_multiplier
#print axioms electron_mass_operator_basis
#print axioms electron_mass_operator_basis_expanded
#print axioms regional_electron_reference_mass_positive
#print axioms regional_electron_mass_operator_positive
#print axioms regional_electron_mass_operator_basis

end
end HMT.VI.ElectronMassRealization
