import ActionSections
import CanonicalConstitutivePositivity
import ConstitutiveLCRecovery

/-! The printed angular publication is composed with the previously proved
regional action return.  In particular the angular chamber is derived from
the source intervals and the action formula rather than assumed anew.
No action datum in SI or measured coupling selects these coordinates. -/
noncomputable section
namespace HMT.II.ActionReturn
open HMT.III.Constitutive

def directDegrees (α : ℝ) : ℝ := 1000 * α
def conjugateDegrees (α φ p : ℝ) : ℝ := 2 * (etaRet α φ p + α)
def directRadians (α p : ℝ) : ℝ := (p / 180) * directDegrees α
def conjugateRadians (α φ p : ℝ) : ℝ := (p / 180) * conjugateDegrees α φ p

namespace PrintedDomain
variable {α φ p : ℝ} (h : PrintedDomain α φ p)
include h

theorem sqrt_character_upper : Real.sqrt (1000 * α / φ) < 3 := by
  apply (Real.sqrt_lt' (by norm_num : (0 : ℝ) < 3)).mpr
  apply (div_lt_iff₀ h.phi_pos).mpr
  nlinarith [h.alpha_coarse_upper, h.phi_lower]

theorem H5_upper : H5 α φ < 2 := by
  have h2 : α ^ 2 ≤ ((1 : ℝ) / 125) ^ 2 :=
    pow_le_pow_left₀ h.alpha_pos.le h.alpha_coarse_upper.le 2
  have h4 : α ^ 4 ≤ ((1 : ℝ) / 125) ^ 4 :=
    pow_le_pow_left₀ h.alpha_pos.le h.alpha_coarse_upper.le 4
  have h3 : 0 ≤ α ^ 3 := pow_nonneg h.alpha_pos.le 3
  have h5 : 0 ≤ α ^ 5 := pow_nonneg h.alpha_pos.le 5
  have hs := h.sqrt_character_upper
  have ha := h.alpha_pos
  unfold H5
  linarith

theorem published_degrees_chamber :
    0 < conjugateDegrees α φ p ∧ conjugateDegrees α φ p < directDegrees α := by
  have he : etaRet α φ p < 2 := h.etaRet_lt_H5.trans h.H5_upper
  dsimp [conjugateDegrees, directDegrees]
  constructor
  · linarith [h.etaRet_pos, h.alpha_pos]
  · linarith [h.alpha_coarse_lower, h.alpha_coarse_upper]

theorem published_radians_chamber :
    0 < conjugateRadians α φ p ∧
      conjugateRadians α φ p < directRadians α p := by
  have hp : 0 < p / 180 := div_pos h.pi_pos (by norm_num)
  exact ⟨mul_pos hp h.published_degrees_chamber.1,
    mul_lt_mul_of_pos_left h.published_degrees_chamber.2 hp⟩

/-- The output camera is constructed; its inequalities are proof outputs. -/
def producedAngles : AngularChamber where
  x := directRadians α p
  y := conjugateRadians α φ p
  y_pos := h.published_radians_chamber.1
  y_lt_x := h.published_radians_chamber.2

theorem produced_channels_formula :
    h.producedAngles.channels.qPlus =
      Real.exp (-(p / 180) * (1000 * α + 2 * (etaRet α φ p + α))) ∧
    h.producedAngles.channels.qMinus =
      Real.exp (-(p / 180) * (1000 * α - 2 * (etaRet α φ p + α))) := by
  dsimp [producedAngles, AngularChamber.channels, directRadians,
    conjugateRadians, directDegrees, conjugateDegrees]
  constructor <;> congr 1 <;> ring

theorem produced_constitutive_response :
    h.producedAngles.canonicalConstitutiveOperator.PosDef ∧
    (∃! W : Matrix (Fin 2) (Fin 2) ℝ,
      W * TwoSheetProjectors.sigma4
        (h.producedAngles.transport canonicalSheetInvolution
          canonicalSheetInvolution_square ^ 30) =
      TwoSheetProjectors.sigma3
        (h.producedAngles.transport canonicalSheetInvolution
          canonicalSheetInvolution_square ^ 30)) ∧
    (∀ m : ℕ, h.producedAngles.channels.refinedSpeed m =
      h.producedAngles.channels.vacuum.speed) :=
  ⟨h.producedAngles.canonical_operator_posDef,
    h.producedAngles.completion_from_angles canonicalSheetInvolution
      canonicalSheetInvolution_square,
    h.producedAngles.channels.refinedSpeed_eq_constitutive⟩

theorem produced_angular_recovery :
    h.producedAngles.channels.angularX = directRadians α p ∧
    h.producedAngles.channels.angularY = conjugateRadians α φ p :=
  h.producedAngles.channels_angular_recovery

theorem degree_recovery :
    (180 / p) * h.producedAngles.channels.angularX = directDegrees α ∧
    (180 / p) * h.producedAngles.channels.angularY = conjugateDegrees α φ p := by
  rw [h.produced_angular_recovery.1, h.produced_angular_recovery.2]
  have hp := ne_of_gt h.pi_pos
  dsimp [directRadians, conjugateRadians]
  constructor <;> field_simp <;> ring

omit h in
theorem action_angle_reading_covariant (θ hbar : ℝ) :
    hbar * ((p / 180) * θ) = fullTurn p hbar * (θ / 360) := by
  unfold fullTurn
  ring

end PrintedDomain

#print axioms PrintedDomain.sqrt_character_upper
#print axioms PrintedDomain.H5_upper
#print axioms PrintedDomain.published_degrees_chamber
#print axioms PrintedDomain.published_radians_chamber
#print axioms PrintedDomain.produced_channels_formula
#print axioms PrintedDomain.produced_constitutive_response
#print axioms PrintedDomain.produced_angular_recovery
#print axioms PrintedDomain.degree_recovery
#print axioms PrintedDomain.action_angle_reading_covariant
end HMT.II.ActionReturn
