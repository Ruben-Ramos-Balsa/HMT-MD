import SelectedRadiusTDuality
import ObservedBarbero
import SelectedExceptionalChain

/-!
The Barbero functional is evaluated on the angular chamber already produced
from the selected regional register. No arbitrary angular chamber, numerical
value of Barbero, or new PublishedRegister hypothesis is supplied.
The finite terminal selector's existing S8 interface is inherited unchanged.
This composition preserves the exact constitutive and nonadic recovery laws.
-/

noncomputable section
namespace HMT.SelectedAngularBarbero

open HMT.I.SelectedAction HMT.II.ActionReturn HMT.III.Constitutive
open HMT.IV.SelectedRadiusTDuality HMT.OrientedReturn

def value : ℝ := barbero angles.channels

theorem selected_angular_coordinates :
    angles.channels.angularX = directRadians alpha pi ∧
    angles.channels.angularY = conjugateRadians alpha phi pi :=
  action_domain.produced_angular_recovery

theorem selected_channels_formula :
    angles.channels.qPlus =
      Real.exp (-(pi / 180) * (1000 * alpha + 2 * (etaRet alpha phi pi + alpha))) ∧
    angles.channels.qMinus =
      Real.exp (-(pi / 180) * (1000 * alpha - 2 * (etaRet alpha phi pi + alpha))) :=
  action_domain.produced_channels_formula

theorem selected_angular_functional :
    value = angularFunctional (directRadians alpha pi)
      (conjugateRadians alpha phi pi) := by
  unfold value
  rw [barbero_angular, selected_angular_coordinates.1,
    selected_angular_coordinates.2]

theorem selected_arithmetic_formula :
    value =
      180 * directRadians alpha pi * conjugateRadians alpha phi pi / pi +
      fundamentalReturn (Real.exp (-directRadians alpha pi +
        conjugateRadians alpha phi pi)) -
      fundamentalReturn (Real.exp (-directRadians alpha pi -
        conjugateRadians alpha phi pi)) := by
  rw [selected_angular_functional]
  unfold angularFunctional
  rw [show pi = Real.pi from ClosureAnalytic.value_eq_pi]

theorem selected_constitutive_recovery :
    value = speedImpedanceFunctional angles.channels.vacuum.impedance
      angles.channels.vacuum.speed
      (vacuum_minus_reading_mem angles.channels)
      (vacuum_plus_reading_mem angles.channels) :=
  barbero_from_speed_impedance angles.channels

theorem selected_nonadic_recovery (m : ℕ) :
    value = -Matrix.trace (amplifiedProduct (9 ^ m)
      (angles.channels.qPlus ^ 30) (angles.channels.qMinus ^ 30)) /
      (9 : ℝ) ^ m :=
  barbero_nonadic_amplification angles.channels m

theorem selected_action_incidence_functional :
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    HMT.I.SelectedExceptionalChain.ConcreteIncidencePublication ∧
    value = angularFunctional (directRadians alpha pi)
      (conjugateRadians alpha phi pi) :=
  ⟨action_decimal_order,
    HMT.I.SelectedExceptionalChain.concrete_incidence_publication,
    selected_angular_functional⟩

end HMT.SelectedAngularBarbero
end

#print axioms HMT.SelectedAngularBarbero.selected_angular_coordinates
#print axioms HMT.SelectedAngularBarbero.selected_channels_formula
#print axioms HMT.SelectedAngularBarbero.selected_angular_functional
#print axioms HMT.SelectedAngularBarbero.selected_arithmetic_formula
#print axioms HMT.SelectedAngularBarbero.selected_constitutive_recovery
#print axioms HMT.SelectedAngularBarbero.selected_nonadic_recovery
#print axioms HMT.SelectedAngularBarbero.selected_action_incidence_functional
