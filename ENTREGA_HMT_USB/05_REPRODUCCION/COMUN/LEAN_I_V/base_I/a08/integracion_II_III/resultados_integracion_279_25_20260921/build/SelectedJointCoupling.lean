import SelectedCKM
import SelectedAngularBarbero

/-!
Exact downstream composition of the two already compiled selected-state
publications. The angular channels, CKM coordinates and Barbero functional
receive the same selected action domain. No new selector, register premise,
angular datum or target value is introduced.
-/

noncomputable section
open Matrix

namespace HMT.SelectedJointCoupling

open HMT.I.SelectedAction HMT.II.ActionReturn HMT.III.Constitutive HMT.OrientedReturn
open HMT.IV.SelectedRadiusTDuality

theorem selected_angular_coordinate_identity :
    angles.channels.angularX = HMT.II.CKM.Selected.radians HMT.II.CKM.Selected.direct ∧
    angles.channels.angularY = HMT.II.CKM.Selected.radians HMT.II.CKM.Selected.conjugate := by
  simpa only [HMT.II.CKM.Selected.radians, HMT.II.CKM.Selected.direct,
    HMT.II.CKM.Selected.conjugate, directRadians, conjugateRadians] using
    HMT.SelectedAngularBarbero.selected_angular_coordinates

theorem selected_barbero_ckm_functional :
    HMT.SelectedAngularBarbero.value = angularFunctional
      (HMT.II.CKM.Selected.radians HMT.II.CKM.Selected.direct)
      (HMT.II.CKM.Selected.radians HMT.II.CKM.Selected.conjugate) := by
  simpa only [HMT.II.CKM.Selected.radians, HMT.II.CKM.Selected.direct,
    HMT.II.CKM.Selected.conjugate, directRadians, conjugateRadians] using
    HMT.SelectedAngularBarbero.selected_angular_functional

/-- One selected publication: exact angles, Barbero, incidence, action and CKM. -/
theorem selected_joint_coupling :
    (angles.channels.angularX = HMT.II.CKM.Selected.radians HMT.II.CKM.Selected.direct ∧
      angles.channels.angularY = HMT.II.CKM.Selected.radians HMT.II.CKM.Selected.conjugate) ∧
    HMT.SelectedAngularBarbero.value = angularFunctional
      (HMT.II.CKM.Selected.radians HMT.II.CKM.Selected.direct)
      (HMT.II.CKM.Selected.radians HMT.II.CKM.Selected.conjugate) ∧
    HMT.I.SelectedExceptionalChain.ConcreteIncidencePublication ∧
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    (HMT.II.CKM.Selected.matrixᴴ * HMT.II.CKM.Selected.matrix = 1 ∧
      HMT.II.CKM.Selected.matrix * HMT.II.CKM.Selected.matrixᴴ = 1) ∧
    0 < HMT.CKM.ComplexRealization.jarlskog HMT.II.CKM.Selected.matrix :=
  ⟨selected_angular_coordinate_identity, selected_barbero_ckm_functional,
    HMT.I.SelectedExceptionalChain.concrete_incidence_publication,
    action_decimal_order, HMT.II.CKM.Selected.matrix_unitary,
    HMT.II.CKM.Selected.jarlskog_positive⟩

end HMT.SelectedJointCoupling
end

#print axioms HMT.SelectedJointCoupling.selected_angular_coordinate_identity
#print axioms HMT.SelectedJointCoupling.selected_barbero_ckm_functional
#print axioms HMT.SelectedJointCoupling.selected_joint_coupling
