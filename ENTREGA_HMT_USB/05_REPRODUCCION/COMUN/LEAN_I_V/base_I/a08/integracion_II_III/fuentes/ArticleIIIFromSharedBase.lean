import SharedArticleIBase
import ActionProducedAngles

/-!
Article III: the normalized constitutive branch of the selected shared base.

The same regional register used by Article I publishes alpha. Its previously
proved action domain supplies the angular chamber, ordered channels and
positive response. No PublishedRegister, interval, channel, projector or
positivity premise is supplied again. The statements compose existing proofs.

The outputs epsilon, mu, impedance and speed are normalized coordinates.
Their dimensional realization requires the separately typed unit sections of
Article III. The inverse retains the labelled channels; it does not recover
the complete enriched TPK history. The Barbero statements are the existing
oriented two-channel realization, not general spectral calculus.

The imported S8 and transition-record interfaces remain unchanged. This module
does not claim to formalize every result of Article III. See SOURCES.md for
the exact source theorems and LaTeX statements used in this composition.
-/

noncomputable section
namespace HMT.Shared.ArticleIII

open HMT.III.Constitutive HMT.II.ActionReturn

theorem alpha_uses_shared_register :
    HMT.I.SelectedAction.alpha =
      AlphaAnalyticChart.precoordinate HMT.Shared.ArticleI.register :=
  HMT.Shared.ArticleI.action_alpha_uses_shared_register

/-- The chamber inequalities are discharged by the previously selected domain. -/
def angles : AngularChamber := HMT.I.SelectedAction.action_domain.producedAngles

def channels : OrientedChannels := angles.channels
def vacuum : PositiveResponse := channels.vacuum

def epsilon : ℝ := vacuum.epsilon
def mu : ℝ := vacuum.mu
def impedance : ℝ := vacuum.impedance
def speed : ℝ := vacuum.speed

def constitutiveOperator : Matrix (Fin 2) (Fin 2) ℝ :=
  angles.canonicalConstitutiveOperator

def gamma : ℝ := HMT.OrientedReturn.barbero channels

theorem angles_from_selected_constants :
    angles.x = directRadians HMT.I.SelectedAction.alpha HMT.I.SelectedAction.pi ∧
    angles.y = conjugateRadians HMT.I.SelectedAction.alpha
      HMT.I.SelectedAction.phi HMT.I.SelectedAction.pi := ⟨rfl, rfl⟩

theorem angle_order : 0 < angles.y ∧ angles.y < angles.x :=
  ⟨angles.y_pos, angles.y_lt_x⟩

theorem channels_from_selected_constants :
    channels.qPlus = Real.exp (-(HMT.I.SelectedAction.pi / 180) *
      (1000 * HMT.I.SelectedAction.alpha +
        2 * (etaRet HMT.I.SelectedAction.alpha HMT.I.SelectedAction.phi
          HMT.I.SelectedAction.pi + HMT.I.SelectedAction.alpha))) ∧
    channels.qMinus = Real.exp (-(HMT.I.SelectedAction.pi / 180) *
      (1000 * HMT.I.SelectedAction.alpha -
        2 * (etaRet HMT.I.SelectedAction.alpha HMT.I.SelectedAction.phi
          HMT.I.SelectedAction.pi + HMT.I.SelectedAction.alpha))) :=
  HMT.I.SelectedAction.action_domain.produced_channels_formula

theorem response_order :
    3 / 4 < vacuum.rMinus ∧ vacuum.rMinus < vacuum.rPlus ∧ vacuum.rPlus < 1 :=
  channels.vacuum_order

theorem response_from_channels :
    vacuum.rPlus = (1 - channels.qPlus ^ 90) / (1 - channels.qPlus ^ 120) ∧
    vacuum.rMinus = (1 - channels.qMinus ^ 90) / (1 - channels.qMinus ^ 120) :=
  ⟨rfl, rfl⟩

theorem coordinates_from_response :
    epsilon = vacuum.rPlus ^ 2 ∧ mu = vacuum.rMinus ^ 2 ∧
    impedance = vacuum.rMinus / vacuum.rPlus ∧
    speed = 1 / (vacuum.rPlus * vacuum.rMinus) :=
  ⟨rfl, rfl, rfl, rfl⟩

theorem coordinates_positive :
    0 < epsilon ∧ 0 < mu ∧ 0 < impedance ∧ 0 < speed :=
  vacuum.coordinates_pos

theorem constitutive_identities :
    mu * epsilon = 1 / speed ^ 2 ∧ mu / epsilon = impedance ^ 2 ∧
    epsilon = 1 / (impedance * speed) ∧ mu = impedance / speed :=
  ⟨vacuum.product_identity, vacuum.quotient_identity,
    vacuum.epsilon_from_readings, vacuum.mu_from_readings⟩

/-- The normalized positive pair is produced and unique under its two rules. -/
theorem positive_coordinates_exist_unique :
    ∃! p : ℝ × ℝ, 0 < p.1 ∧ 0 < p.2 ∧
      p.2 * p.1 = 1 / speed ^ 2 ∧ p.2 / p.1 = impedance ^ 2 := by
  refine ⟨(epsilon, mu),
    ⟨coordinates_positive.1, coordinates_positive.2.1,
      constitutive_identities.1, constitutive_identities.2.1⟩, ?_⟩
  intro p hp
  have h := vacuum.quadratic_coordinates_unique hp.1 hp.2.1 hp.2.2.1 hp.2.2.2
  exact Prod.ext h.1 h.2

theorem operator_positive : constitutiveOperator.PosDef :=
  angles.canonical_operator_posDef

/-- The completion equation is unique among all real two by two matrices. -/
theorem operator_completion_unique :
    ∃! W : Matrix (Fin 2) (Fin 2) ℝ,
      W * TwoSheetProjectors.sigma4
        (angles.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30) =
      TwoSheetProjectors.sigma3
        (angles.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30) :=
  angles.completion_from_angles canonicalSheetInvolution canonicalSheetInvolution_square

theorem inverse_readings :
    vacuum.rPlus = 1 / Real.sqrt (impedance * speed) ∧
    vacuum.rMinus = Real.sqrt (impedance / speed) :=
  ⟨vacuum.recover_rPlus, vacuum.recover_rMinus⟩

theorem cubic_roots_exist_unique :
    (∃! s : ℝ, s ∈ Set.Ioo 0 1 ∧
      vacuum.rPlus * s ^ 3 + (vacuum.rPlus - 1) * (1 + s + s ^ 2) = 0) ∧
    (∃! s : ℝ, s ∈ Set.Ioo 0 1 ∧
      vacuum.rMinus * s ^ 3 + (vacuum.rMinus - 1) * (1 + s + s ^ 2) = 0) :=
  ⟨cubic_exists_unique (channelResponse_bounds channels.plus_mem),
    cubic_exists_unique (channelResponse_bounds channels.minus_mem)⟩

theorem inverse_recovers_channels :
    recoverChannel vacuum.rPlus (channelResponse_bounds channels.plus_mem) = channels.qPlus ∧
    recoverChannel vacuum.rMinus (channelResponse_bounds channels.minus_mem) = channels.qMinus :=
  ⟨recoverChannel_response channels.plus_mem, recoverChannel_response channels.minus_mem⟩

theorem inverse_recovers_selected_degrees :
    (180 / HMT.I.SelectedAction.pi) * channels.angularX =
      directDegrees HMT.I.SelectedAction.alpha ∧
    (180 / HMT.I.SelectedAction.pi) * channels.angularY =
      conjugateDegrees HMT.I.SelectedAction.alpha HMT.I.SelectedAction.phi
        HMT.I.SelectedAction.pi :=
  HMT.I.SelectedAction.action_domain.degree_recovery

theorem speed_at_every_refinement :
    ∀ m : Nat, channels.refinedSpeed m = speed :=
  channels.refinedSpeed_eq_constitutive

theorem kinetic_speed_is_constitutive : channels.kinematicSpeed = speed :=
  channels.kinematicSpeed_eq_constitutive

theorem oriented_exchange :
    vacuum.swap.epsilon = mu ∧ vacuum.swap.mu = epsilon ∧
    vacuum.swap.impedance = 1 / impedance ∧ vacuum.swap.speed = speed :=
  vacuum.swap_coordinates

theorem constitutive_recovers_action_shape :
    (Real.log angles.recoveredPowerPlus - Real.log angles.recoveredPowerMinus) /
      (Real.log angles.recoveredPowerPlus + Real.log angles.recoveredPowerMinus) =
        angles.y / angles.x ∧
    Real.log (Real.log angles.recoveredPowerPlus / Real.log angles.recoveredPowerMinus) / 2 =
      angles.ellipseAnisotropy ∧
    Real.sqrt (Real.log angles.recoveredPowerMinus / Real.log angles.recoveredPowerPlus) =
      angles.relativeLC :=
  angles.constitutive_LC_recovery

/-- The conventional notation for pi is recognized after the HMT reader. -/
theorem constructed_pi_recognition : HMT.I.SelectedAction.pi = Real.pi :=
  ClosureAnalytic.value_eq_pi

theorem gamma_from_selected_angles :
    gamma = 180 * angles.x * angles.y / HMT.I.SelectedAction.pi +
      HMT.OrientedReturn.fundamentalReturn (Real.exp (-angles.x + angles.y)) -
      HMT.OrientedReturn.fundamentalReturn (Real.exp (-angles.x - angles.y)) := by
  simpa only [gamma, channels, HMT.OrientedReturn.angularFunctional,
    angles.angularX_channels, angles.angularY_channels, constructed_pi_recognition]
    using HMT.OrientedReturn.barbero_angular angles.channels

theorem gamma_from_constitutive_readings :
    gamma = HMT.OrientedReturn.speedImpedanceFunctional impedance speed
      (HMT.OrientedReturn.vacuum_minus_reading_mem channels)
      (HMT.OrientedReturn.vacuum_plus_reading_mem channels) :=
  HMT.OrientedReturn.barbero_from_speed_impedance channels

theorem gamma_at_every_refinement :
    ∀ m : Nat,
      gamma = -Matrix.trace (HMT.OrientedReturn.amplifiedProduct (9 ^ m)
        (channels.qPlus ^ 30) (channels.qMinus ^ 30)) / (9 : ℝ) ^ m :=
  HMT.OrientedReturn.barbero_nonadic_amplification channels

/-- A single no-new-premise composition from the selected shared register. -/
theorem shared_constitutive_publication :
    HMT.I.SelectedAction.alpha =
      AlphaAnalyticChart.precoordinate HMT.Shared.ArticleI.register ∧
    constitutiveOperator.PosDef ∧
    (0 < epsilon ∧ 0 < mu ∧ 0 < impedance ∧ 0 < speed) ∧
    mu * epsilon = 1 / speed ^ 2 ∧ mu / epsilon = impedance ^ 2 ∧
    (∀ m : Nat, channels.refinedSpeed m = speed) ∧
    gamma = HMT.OrientedReturn.speedImpedanceFunctional impedance speed
      (HMT.OrientedReturn.vacuum_minus_reading_mem channels)
      (HMT.OrientedReturn.vacuum_plus_reading_mem channels) :=
  ⟨alpha_uses_shared_register, operator_positive, coordinates_positive,
    constitutive_identities.1, constitutive_identities.2.1,
    speed_at_every_refinement, gamma_from_constitutive_readings⟩

end HMT.Shared.ArticleIII
end

#print axioms HMT.Shared.ArticleIII.alpha_uses_shared_register
#print axioms HMT.Shared.ArticleIII.angles_from_selected_constants
#print axioms HMT.Shared.ArticleIII.angle_order
#print axioms HMT.Shared.ArticleIII.channels_from_selected_constants
#print axioms HMT.Shared.ArticleIII.response_order
#print axioms HMT.Shared.ArticleIII.response_from_channels
#print axioms HMT.Shared.ArticleIII.coordinates_from_response
#print axioms HMT.Shared.ArticleIII.coordinates_positive
#print axioms HMT.Shared.ArticleIII.constitutive_identities
#print axioms HMT.Shared.ArticleIII.positive_coordinates_exist_unique
#print axioms HMT.Shared.ArticleIII.operator_positive
#print axioms HMT.Shared.ArticleIII.operator_completion_unique
#print axioms HMT.Shared.ArticleIII.inverse_readings
#print axioms HMT.Shared.ArticleIII.cubic_roots_exist_unique
#print axioms HMT.Shared.ArticleIII.inverse_recovers_channels
#print axioms HMT.Shared.ArticleIII.inverse_recovers_selected_degrees
#print axioms HMT.Shared.ArticleIII.speed_at_every_refinement
#print axioms HMT.Shared.ArticleIII.kinetic_speed_is_constitutive
#print axioms HMT.Shared.ArticleIII.oriented_exchange
#print axioms HMT.Shared.ArticleIII.constitutive_recovers_action_shape
#print axioms HMT.Shared.ArticleIII.constructed_pi_recognition
#print axioms HMT.Shared.ArticleIII.gamma_from_selected_angles
#print axioms HMT.Shared.ArticleIII.gamma_from_constitutive_readings
#print axioms HMT.Shared.ArticleIII.gamma_at_every_refinement
#print axioms HMT.Shared.ArticleIII.shared_constitutive_publication
