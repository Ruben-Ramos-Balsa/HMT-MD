import SectorialAreaInformation
import SelectedConstitutivePublication
import ObservedBarbero

/-! Article II sectorial area and information on the same generated chamber
as the selected Article I -> III consumer. The Barbero parameter is the
existing oriented functional, never an added hypothesis or target value. -/

noncomputable section
open scoped BigOperators
open Set

namespace HMT.II.SelectedAreaInformation

open HMT.OrientedReturn HMT.III.Constitutive
open HMT.III.SelectedPublication HMT.II.SectorialAreaInformation

private def returnPolynomial (t : ℝ) : ℝ := 12 * t ^ 3 - t ^ 4

private theorem returnPolynomial_strictMonoOn :
    StrictMonoOn returnPolynomial (Ioo 0 1) := by
  apply strictMonoOn_of_deriv_pos (convex_Ioo 0 1)
  · unfold returnPolynomial
    fun_prop
  · intro t ht
    have ht' : t ∈ Ioo (0 : ℝ) 1 := by simpa using ht
    have hd : HasDerivAt returnPolynomial (36 * t ^ 2 - 4 * t ^ 3) t := by
      convert (((hasDerivAt_id t).pow 3).const_mul 12).sub
        ((hasDerivAt_id t).pow 4) using 1
      simp [returnPolynomial]
      ring
    rw [hd.deriv]
    have h := mul_pos (mul_pos (by norm_num : (0 : ℝ) < 4) (sq_pos_of_pos ht'.1))
      (show 0 < 9 - t by linarith [ht'.2])
    nlinarith

private theorem fundamentalReturn_polynomial_hasSum {q : ℝ} (hq : q ∈ Ioo 0 1) :
    HasSum (fun j : ℕ => returnPolynomial (q ^ (30 + 90 * j))) (fundamentalReturn q) := by
  have hs := ((returnSeries_hasSum (by decide : 0 < 90) hq).mul_left 12).sub
    (returnSeries_hasSum (by decide : 0 < 120) hq)
  convert hs using 1
  funext j
  simp only [returnPolynomial, ← pow_mul]
  have h3 : (30 + 90 * j) * 3 = 90 + 3 * 90 * j := by omega
  have h4 : (30 + 90 * j) * 4 = 120 + 3 * 120 * j := by omega
  rw [h3, h4]

theorem fundamentalReturn_monotoneOn : MonotoneOn fundamentalReturn (Ioo 0 1) := by
  intro a ha b hb hab
  apply hasSum_le _ (fundamentalReturn_polynomial_hasSum ha)
    (fundamentalReturn_polynomial_hasSum hb)
  intro j
  apply returnPolynomial_strictMonoOn.monotoneOn
  · exact ⟨pow_pos ha.1 _, pow_lt_one₀ ha.1.le ha.2 (by omega)⟩
  · exact ⟨pow_pos hb.1 _, pow_lt_one₀ hb.1.le hb.2 (by omega)⟩
  · exact pow_le_pow_left₀ ha.1.le hab _

theorem barbero_pos (Q : OrientedChannels) : 0 < barbero Q := by
  have hxy := Q.angular_chamber
  have hx : 0 < Q.angularX := hxy.1.trans hxy.2
  have hterm : 0 < 180 * Q.angularX * Q.angularY / Real.pi :=
    div_pos (mul_pos (mul_pos (by norm_num) hx) hxy.1) Real.pi_pos
  have hret := fundamentalReturn_monotoneOn Q.plus_mem Q.minus_mem Q.ordered.le
  rw [barbero, chainReader_fundamental, chainReader_fundamental]
  linarith

def gamma : ℝ := barbero angles.channels

theorem gamma_pos : 0 < gamma := barbero_pos angles.channels

theorem gamma_ne_zero : gamma ≠ 0 := ne_of_gt gamma_pos

theorem gamma_from_constitutive :
    gamma = recoveredFunctional
      (channelResponse angles.channels.qMinus) (channelResponse angles.channels.qPlus)
      (channelResponse_bounds angles.channels.minus_mem)
      (channelResponse_bounds angles.channels.plus_mem) :=
  barbero_from_constitutive angles.channels

theorem gamma_from_speed_impedance :
    gamma = speedImpedanceFunctional response.impedance response.speed
      (vacuum_minus_reading_mem angles.channels) (vacuum_plus_reading_mem angles.channels) :=
  barbero_from_speed_impedance angles.channels

theorem gamma_transported_trace (U V : Matrix (Fin 2) (Fin 2) ℝ) (hVU : V * U = 1) :
    gamma = -Matrix.trace ((U * orientationMatrix * V) *
      (U * primitiveMatrix (angles.channels.qPlus ^ 30) (angles.channels.qMinus ^ 30) * V)) :=
  barbero_transported_trace angles.channels U V hVU

theorem gamma_nonadic_trace (m : ℕ) :
    gamma = -Matrix.trace (amplifiedProduct (9 ^ m)
      (angles.channels.qPlus ^ 30) (angles.channels.qMinus ^ 30)) / (9 : ℝ) ^ m :=
  barbero_nonadic_amplification angles.channels m

theorem selected_modular_area (a0 delta : ℝ) (ha : a0 ≠ 0) (v : Occupation) :
    -Real.log (reducedDensity delta v v) = logPartition delta +
      modularCoefficient gamma a0 delta 0 * normalizedSectorArea gamma a0 0 v +
      modularCoefficient gamma a0 delta 1 * normalizedSectorArea gamma a0 1 v :=
  modular_area_of_reduced_state gamma a0 delta gamma_ne_zero ha v

theorem selected_area_information (a0 delta : ℝ) (ha : a0 ≠ 0) :
    0 < gamma ∧
    (∀ v, -Real.log (reducedDensity delta v v) = logPartition delta +
      modularCoefficient gamma a0 delta 0 * normalizedSectorArea gamma a0 0 v +
      modularCoefficient gamma a0 delta 1 * normalizedSectorArea gamma a0 1 v) ∧
    entropy delta = logPartition delta + delta * expectedIncidence delta :=
  ⟨gamma_pos, selected_modular_area a0 delta ha, entropy_state_equation delta⟩

/-- The normalized real character of the angular triplet, using the already
generated circular coordinate. Its conventional recognition is only used
to apply the standard cosine positivity theorem. -/
def chi10 : ℝ := (1 + 2 * Real.cos (HMT.I.SelectedAction.pi / 18)) / 3

def thetaClock : ℝ := angles.y / 6

def a0 : ℝ := chi10 * thetaClock

theorem chi10_pos : 0 < chi10 := by
  have hpi : HMT.I.SelectedAction.pi = Real.pi := ClosureAnalytic.value_eq_pi
  have hc : 0 < Real.cos (Real.pi / 18) :=
    Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩
  unfold chi10
  rw [hpi]
  positivity

theorem thetaClock_pos : 0 < thetaClock :=
  div_pos angles.y_pos (by norm_num)

theorem thetaClock_from_degrees :
    thetaClock =
      (HMT.II.ActionReturn.conjugateDegrees HMT.I.SelectedAction.alpha
        HMT.I.SelectedAction.phi HMT.I.SelectedAction.pi / 6) *
        HMT.I.SelectedAction.pi / 180 := by
  rw [thetaClock, ← recover_generated_degrees.2, angles.angularY_channels]
  field_simp [ne_of_gt HMT.I.SelectedAction.action_domain.pi_pos]
  ring

theorem a0_pos : 0 < a0 := mul_pos chi10_pos thetaClock_pos

theorem generated_area_quantum_pos : 0 < gamma * a0 := mul_pos gamma_pos a0_pos

/-- Fully selected areal scale. Only the parameter of the family of reduced
states remains free; neither gamma nor a0 is supplied as an assumption. -/
theorem selected_generated_area_information (delta : ℝ) :
    0 < gamma ∧ 0 < a0 ∧ 0 < gamma * a0 ∧
    (∀ v, -Real.log (reducedDensity delta v v) = logPartition delta +
      modularCoefficient gamma a0 delta 0 * normalizedSectorArea gamma a0 0 v +
      modularCoefficient gamma a0 delta 1 * normalizedSectorArea gamma a0 1 v) ∧
    entropy delta = logPartition delta + delta * expectedIncidence delta :=
  ⟨gamma_pos, a0_pos, generated_area_quantum_pos,
    (selected_area_information a0 delta (ne_of_gt a0_pos)).2⟩

#print axioms gamma_pos
#print axioms gamma_from_speed_impedance
#print axioms gamma_nonadic_trace
#print axioms selected_area_information
#print axioms thetaClock_from_degrees
#print axioms selected_generated_area_information

end HMT.II.SelectedAreaInformation
