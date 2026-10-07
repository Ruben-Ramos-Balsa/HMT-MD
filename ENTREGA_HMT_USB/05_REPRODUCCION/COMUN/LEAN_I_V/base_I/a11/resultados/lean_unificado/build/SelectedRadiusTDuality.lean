import SelectedActionDomain
import ActionProducedAngles
import HilbertTAdjoint
import APPSpinRotationClosure

/-!
Composition, not reconstruction, of the selected Article I publication with
the existing angular/ellipse reader and Hilbert T-duality proofs.

Owners: articulo_x/sections/iv_elipse_radio.tex, iv:ellipse:rstar and
iv:ellipse:rstar-compuesto; 02_dualidad_t.tex, iv:cor:radio-especializado.
The positive radius is dimensionless and independent of the common positive
action basis. Integer pairs remain arguments; no route-admissibility selector
for (m,w), compact-resolvent theorem or M-theory identification is asserted.
The selected register, explicit S8 interface and native-evaluation boundary are
inherited unchanged from SelectedActionDomain.
-/

noncomputable section
namespace HMT.IV.SelectedRadiusTDuality

open HMT.I.SelectedAction HMT.II.ActionReturn HMT.III.Constitutive
open HMT.IV.HilbertTDuality HMT.IV.HilbertTAdjoint FiniteWeyl.Duality

def angles : AngularChamber := action_domain.producedAngles

/-- Square root of the previously constructed relative semiaxis ratio. -/
def radius : ℝ := Real.sqrt angles.relativeLC

theorem radius_pos : 0 < radius := Real.sqrt_pos.mpr angles.relativeLC_pos

theorem radius_sq : radius ^ 2 = angles.relativeLC :=
  Real.sq_sqrt angles.relativeLC_pos.le

theorem radius_fourth : radius ^ 4 = (angles.x - angles.y) / (angles.x + angles.y) := by
  calc
    radius ^ 4 = (radius ^ 2) ^ 2 := by ring
    _ = angles.relativeLC ^ 2 := by rw [radius_sq]
    _ = (angles.x - angles.y) / (angles.x + angles.y) := angles.relativeLC_sq

theorem radius_lt_one : radius < 1 := by
  have hplus : 0 < angles.x + angles.y := by linarith [angles.y_pos, angles.y_lt_x]
  have hratio : (angles.x - angles.y) / (angles.x + angles.y) < 1 :=
    (div_lt_one hplus).mpr (by linarith [angles.y_pos])
  rw [← radius_fourth] at hratio
  by_contra h
  have hr : 1 ≤ radius := le_of_not_gt h
  have h2 : 1 ≤ radius ^ 2 := by nlinarith
  nlinarith [sq_nonneg (radius ^ 2 - 1)]

/-- The radius receives the same alpha produced from the regional register. -/
theorem alpha_from_selected_register :
    alpha = AlphaAnalyticChart.precoordinate HMT.I.TerminalSelector.regionalRegister := rfl

theorem radius_degree_formula :
    radius ^ 4 = (directDegrees alpha - conjugateDegrees alpha phi pi) /
      (directDegrees alpha + conjugateDegrees alpha phi pi) := by
  rw [radius_fourth]
  change ((pi / 180) * directDegrees alpha -
      (pi / 180) * conjugateDegrees alpha phi pi) /
    ((pi / 180) * directDegrees alpha +
      (pi / 180) * conjugateDegrees alpha phi pi) = _
  rw [← mul_sub, ← mul_add]
  exact mul_div_mul_left _ _ (ne_of_gt (div_pos action_domain.pi_pos (by norm_num)))

theorem radius_selected_formula :
    radius ^ 4 = (499 * alpha - etaRet alpha phi pi) /
      (501 * alpha + etaRet alpha phi pi) := by
  rw [radius_degree_formula]
  dsimp [directDegrees, conjugateDegrees]
  rw [show 1000 * alpha - 2 * (etaRet alpha phi pi + alpha) =
    2 * (499 * alpha - etaRet alpha phi pi) by ring]
  rw [show 1000 * alpha + 2 * (etaRet alpha phi pi + alpha) =
    2 * (501 * alpha + etaRet alpha phi pi) by ring]
  exact mul_div_mul_left _ _ (by norm_num : (2 : ℝ) ≠ 0)

def selectedRadius : PositiveRadius := ⟨radius, radius_pos⟩

theorem selected_energy_duality (v : ℤ × ℤ) :
    energyAt radius⁻¹ v.swap = energyAt radius v := energyAt_swap_inv radius v

theorem selected_domain_transport (f : State) :
    InDomain radius⁻¹ (exchange f) ↔ InDomain radius f := domain_exchange_iff radius f

theorem selected_form_transport (f : State) :
    InFormDomain radius⁻¹ (exchange f) ↔ InFormDomain radius f :=
  form_domain_exchange_iff radius f

theorem selected_hamiltonian_intertwining (f : operatorDomain radius) :
    hamiltonian radius⁻¹ (exchangeDomain radius f) =
      exchangeIsometry (hamiltonian radius f) := hamiltonian_intertwining radius f

theorem selected_hamiltonian_selfAdjoint : IsSelfAdjoint (hamiltonianPMap radius) :=
  hamiltonianPMap_selfAdjoint radius

theorem reciprocal_hamiltonian_selfAdjoint : IsSelfAdjoint (hamiltonianPMap radius⁻¹) :=
  hamiltonianPMap_selfAdjoint radius⁻¹

/-- Spinorial returns use the already generated closure reader downstream. -/
theorem selected_APP_spin_returns (n : Fin 3 → ℝ)
    (v : HMT.I.APPSpinRotationClosure.Spinor) :
    HMT.I.APPSpinRotationClosure.transportedAPPState n (2 * pi) v =
      -HMT.I.APPSpinRotationClosure.complexEmbedding v ∧
    HMT.I.APPSpinRotationClosure.transportedAPPState n (4 * pi) v =
      HMT.I.APPSpinRotationClosure.complexEmbedding v := by
  simpa only [pi, ClosureAnalytic.value_eq_pi] using
    And.intro (HMT.I.APPSpinRotationClosure.APP_two_pi_return n v)
      (HMT.I.APPSpinRotationClosure.APP_four_pi_return n v)

end HMT.IV.SelectedRadiusTDuality
end

#print axioms HMT.IV.SelectedRadiusTDuality.radius_pos
#print axioms HMT.IV.SelectedRadiusTDuality.radius_sq
#print axioms HMT.IV.SelectedRadiusTDuality.radius_fourth
#print axioms HMT.IV.SelectedRadiusTDuality.radius_lt_one
#print axioms HMT.IV.SelectedRadiusTDuality.alpha_from_selected_register
#print axioms HMT.IV.SelectedRadiusTDuality.radius_degree_formula
#print axioms HMT.IV.SelectedRadiusTDuality.radius_selected_formula
#print axioms HMT.IV.SelectedRadiusTDuality.selected_energy_duality
#print axioms HMT.IV.SelectedRadiusTDuality.selected_domain_transport
#print axioms HMT.IV.SelectedRadiusTDuality.selected_form_transport
#print axioms HMT.IV.SelectedRadiusTDuality.selected_hamiltonian_intertwining
#print axioms HMT.IV.SelectedRadiusTDuality.selected_hamiltonian_selfAdjoint
#print axioms HMT.IV.SelectedRadiusTDuality.reciprocal_hamiltonian_selfAdjoint
#print axioms HMT.IV.SelectedRadiusTDuality.selected_APP_spin_returns
