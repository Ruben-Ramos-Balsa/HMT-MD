import ActionProducedAngles
import ElectricQuanta

/-! Electrical publication from the same action return and angular channels.
Positivity of alpha, both actions and the response is discharged from the
existing source domain.  The positive basis U is the common units chart. -/
noncomputable section
namespace HMT.III.ActionElectricComposition
open HMT.II.ActionReturn HMT.III.Constitutive HMT.III.ElectricQuanta

def preAction (α φ p U : ℝ) : ℝ := fullTurn p (hbarPre α φ U)
def retAction (α φ p U : ℝ) : ℝ := fullTurn p (hbarRet α φ p U)

variable {α φ p U : ℝ} (h : PrintedDomain α φ p) (hU : 0 < U)
include h hU

theorem preAction_pos : 0 < preAction α φ p U :=
  mul_pos (mul_pos (by norm_num) h.pi_pos) (h.hbarPre_pos hU)

theorem retAction_pos : 0 < retAction α φ p U :=
  mul_pos (mul_pos (by norm_num) h.pi_pos) (h.hbarRet_pos hU)

theorem full_action_return :
    preAction α φ p U / retAction α φ p U = Ract α φ p :=
  h.fullTurn_ratio_eq hU

theorem generated_charge_exists_unique :
    ∃! e : ℝ, 0 < e ∧ h.producedAngles.channels.vacuum.impedance * e ^ 2 =
      2 * α * retAction α φ p U :=
  positive_charge_exists_unique h.alpha_pos (retAction_pos h hU)
    h.producedAngles.channels.vacuum

theorem generated_charge_return :
    charge α (preAction α φ p U) h.producedAngles.channels.vacuum /
      charge α (retAction α φ p U) h.producedAngles.channels.vacuum =
        Real.sqrt (Ract α φ p) := by
  rw [charge_return_ratio h.alpha_pos (preAction_pos h hU) (retAction_pos h hU),
    full_action_return h hU]

theorem generated_flux_return :
    flux α (preAction α φ p U) h.producedAngles.channels.vacuum /
      flux α (retAction α φ p U) h.producedAngles.channels.vacuum =
        Real.sqrt (Ract α φ p) := by
  rw [flux_return_ratio h.alpha_pos (preAction_pos h hU) (retAction_pos h hU),
    full_action_return h hU]

theorem generated_josephson_return :
    josephson α (preAction α φ p U) h.producedAngles.channels.vacuum /
      josephson α (retAction α φ p U) h.producedAngles.channels.vacuum =
        (Real.sqrt (Ract α φ p))⁻¹ := by
  rw [josephson_return_ratio h.alpha_pos (preAction_pos h hU) (retAction_pos h hU),
    full_action_return h hU]

/-- The electrical identities use the generated angular response and returned
action. No independent charge or electromagnetic scalar is supplied. -/
theorem generated_electric_identities :
    let W := h.producedAngles.channels.vacuum
    let S := retAction α φ p U
    resistance α S W * conductance α S W = 2 ∧
    conductance α S W * W.impedance = 4 * α ∧
    josephson α S W * flux α S W = 1 ∧
    josephson α S W ^ 2 * resistance α S W = 4 / S :=
  electric_quanta_identities h.alpha_pos (retAction_pos h hU)
    h.producedAngles.channels.vacuum

theorem generated_coupling_identity :
    α = charge α (retAction α φ p U) h.producedAngles.channels.vacuum ^ 2 /
      (4 * p * h.producedAngles.channels.vacuum.epsilon * hbarRet α φ p U *
        h.producedAngles.channels.vacuum.speed) := by
  rw [charge_sq h.alpha_pos (retAction_pos h hU)]
  have hp := ne_of_gt h.pi_pos
  have hbar := ne_of_gt (h.hbarRet_pos hU)
  have hrp := ne_of_gt h.producedAngles.channels.vacuum.plus_pos
  have hrm := ne_of_gt h.producedAngles.channels.vacuum.minus_pos
  dsimp [retAction, fullTurn, PositiveResponse.impedance,
    PositiveResponse.epsilon, PositiveResponse.speed]
  field_simp
  ring

theorem generated_action_return_is_detectable :
    1 < charge α (preAction α φ p U) h.producedAngles.channels.vacuum /
      charge α (retAction α φ p U) h.producedAngles.channels.vacuum := by
  rw [generated_charge_return h hU]
  exact Real.lt_sqrt_of_sq_lt (by simpa using h.Ract_gt_one)

#print axioms preAction_pos
#print axioms retAction_pos
#print axioms full_action_return
#print axioms generated_charge_exists_unique
#print axioms generated_charge_return
#print axioms generated_flux_return
#print axioms generated_josephson_return
#print axioms generated_electric_identities
#print axioms generated_coupling_identity
#print axioms generated_action_return_is_detectable
end HMT.III.ActionElectricComposition
