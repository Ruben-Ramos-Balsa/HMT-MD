import SharedArticleIBase
import ActionProducedAngles
import ConstitutiveBarbero

/-!
Article II receives the selected Article I construction through its shared
entry point. The angular chamber and both oriented channels are produced by
the already proved action domain: no new K, PublishedRegister assumption,
numerical interval hypothesis or measured Barbero value is introduced.

Source owners: 05b_coordenadas_angulares.tex (angular publication, degree /
radian conversion and action covariance) and 06_barbero.tex (oriented 90/120
chain functional). etaRet is the dimensionless return coefficient, not a
dimensionful action. Real.pi in the imported analytic representation is
identified with the already produced closure reader, not supplied upstream.

The explicit S8 input and native-evaluation trust boundary of Article I are
inherited unchanged. This adapter does not claim the entire Article II or
its CKM continuation. Its declarations compose the existing angular and
Barbero proofs on exactly the same selected register.
-/

noncomputable section
namespace HMT.II.FromSharedBase

open HMT.I.SelectedAction HMT.II.ActionReturn
open HMT.III.Constitutive HMT.OrientedReturn

theorem alpha_uses_shared_register :
    alpha = AlphaAnalyticChart.precoordinate HMT.Shared.ArticleI.register :=
  HMT.Shared.ArticleI.action_alpha_uses_shared_register

def angleDegrees : ℝ := directDegrees alpha
def contraAngleDegrees : ℝ := conjugateDegrees alpha phi pi
def angleRadians : ℝ := directRadians alpha pi
def contraAngleRadians : ℝ := conjugateRadians alpha phi pi

def angles : AngularChamber := action_domain.producedAngles
def channels : OrientedChannels := angles.channels

theorem degree_publication :
    angleDegrees = 1000 * alpha ∧
    contraAngleDegrees = 2 * (etaRet alpha phi pi + alpha) := ⟨rfl, rfl⟩

theorem degree_chamber :
    0 < contraAngleDegrees ∧ contraAngleDegrees < angleDegrees :=
  action_domain.published_degrees_chamber

theorem radian_chamber :
    0 < contraAngleRadians ∧ contraAngleRadians < angleRadians :=
  action_domain.published_radians_chamber

theorem degree_radian_conversion :
    angleRadians = (pi / 180) * angleDegrees ∧
    contraAngleRadians = (pi / 180) * contraAngleDegrees := ⟨rfl, rfl⟩

theorem channel_source_formula :
    channels.qPlus =
      Real.exp (-(pi / 180) * (1000 * alpha + 2 * (etaRet alpha phi pi + alpha))) ∧
    channels.qMinus =
      Real.exp (-(pi / 180) * (1000 * alpha - 2 * (etaRet alpha phi pi + alpha))) :=
  action_domain.produced_channels_formula

theorem channels_contractive_ordered :
    0 < channels.qPlus ∧ channels.qPlus < channels.qMinus ∧ channels.qMinus < 1 :=
  ⟨channels.plus_pos, channels.ordered, channels.minus_lt_one⟩

theorem angular_recovery :
    channels.angularX = angleRadians ∧ channels.angularY = contraAngleRadians :=
  action_domain.produced_angular_recovery

theorem degree_recovery :
    (180 / pi) * channels.angularX = angleDegrees ∧
    (180 / pi) * channels.angularY = contraAngleDegrees :=
  action_domain.degree_recovery

/-- The coefficient is evaluated on the ordered channels just constructed. -/
def barberoValue : ℝ := HMT.OrientedReturn.barbero channels

/-- Recognition of the closure reader is downstream of the selected state. -/
theorem pi_is_produced_reader : pi = Real.pi := ClosureAnalytic.value_eq_pi

theorem barbero_angular_formula :
    barberoValue = angularFunctional angleRadians contraAngleRadians := by
  rw [barberoValue, HMT.OrientedReturn.barbero_angular,
    angular_recovery.1, angular_recovery.2]

/-- Same functional in the source's degree convention, with generated pi. -/
theorem barbero_degree_formula :
    barberoValue =
      (pi / 180) * angleDegrees * contraAngleDegrees +
      12 * (returnSeries 90 channels.qMinus - returnSeries 90 channels.qPlus) -
      (returnSeries 120 channels.qMinus - returnSeries 120 channels.qPlus) := by
  have hp : pi ≠ 0 := ne_of_gt action_domain.pi_pos
  have hbilinear :
      180 * angleRadians * contraAngleRadians / pi =
        (pi / 180) * angleDegrees * contraAngleDegrees := by
    rw [degree_radian_conversion.1, degree_radian_conversion.2]
    field_simp [hp]
    ring
  unfold barberoValue HMT.OrientedReturn.barbero
  rw [angular_recovery.1, angular_recovery.2, ← pi_is_produced_reader,
    hbilinear, chainReader_fundamental, chainReader_fundamental]
  unfold fundamentalReturn
  ring

theorem barbero_constitutive_factorization :
    barberoValue = constitutivePrimitive (channels.qMinus ^ 30) -
      constitutivePrimitive (channels.qPlus ^ 30) :=
  HMT.OrientedReturn.barbero_factorization channels

theorem barbero_from_constitutive_response :
    barberoValue = recoveredFunctional
      (channelResponse channels.qMinus) (channelResponse channels.qPlus)
      (channelResponse_bounds channels.minus_mem)
      (channelResponse_bounds channels.plus_mem) :=
  HMT.OrientedReturn.barbero_from_constitutive channels

theorem barbero_oriented_trace :
    barberoValue = -Matrix.trace (orientationMatrix *
      primitiveMatrix (channels.qPlus ^ 30) (channels.qMinus ^ 30)) :=
  HMT.OrientedReturn.barbero_trace channels

/-- The negative orientation is a reading, not a new positive chamber. -/
theorem barbero_reversed_orientation :
    angularFunctional angleRadians (-contraAngleRadians) = -barberoValue := by
  rw [angularFunctional_odd, barbero_angular_formula]

/-- The action basis is arbitrary; no SI normalization is fixed here. -/
theorem action_angle_covariance (theta hbar : ℝ) :
    hbar * ((pi / 180) * theta) = fullTurn pi hbar * (theta / 360) :=
  PrintedDomain.action_angle_reading_covariant theta hbar

/-- Substantive angular and Barbero publication from the shared base. -/
theorem principal_angular_barbero_publication :
    alpha = AlphaAnalyticChart.precoordinate HMT.Shared.ArticleI.register ∧
    (angleDegrees = 1000 * alpha ∧
      contraAngleDegrees = 2 * (etaRet alpha phi pi + alpha)) ∧
    (0 < contraAngleDegrees ∧ contraAngleDegrees < angleDegrees) ∧
    (0 < contraAngleRadians ∧ contraAngleRadians < angleRadians) ∧
    (0 < channels.qPlus ∧ channels.qPlus < channels.qMinus ∧ channels.qMinus < 1) ∧
    (channels.angularX = angleRadians ∧ channels.angularY = contraAngleRadians) ∧
    barberoValue = angularFunctional angleRadians contraAngleRadians ∧
    barberoValue = constitutivePrimitive (channels.qMinus ^ 30) -
      constitutivePrimitive (channels.qPlus ^ 30) :=
  ⟨alpha_uses_shared_register, degree_publication, degree_chamber,
    radian_chamber, channels_contractive_ordered, angular_recovery,
    barbero_angular_formula, barbero_constitutive_factorization⟩

end HMT.II.FromSharedBase
end

#print axioms HMT.II.FromSharedBase.degree_chamber
#print axioms HMT.II.FromSharedBase.radian_chamber
#print axioms HMT.II.FromSharedBase.channel_source_formula
#print axioms HMT.II.FromSharedBase.degree_recovery
#print axioms HMT.II.FromSharedBase.barbero_degree_formula
#print axioms HMT.II.FromSharedBase.barbero_from_constitutive_response
#print axioms HMT.II.FromSharedBase.barbero_oriented_trace
#print axioms HMT.II.FromSharedBase.barbero_reversed_orientation
#print axioms HMT.II.FromSharedBase.action_angle_covariance
#print axioms HMT.II.FromSharedBase.principal_angular_barbero_publication
