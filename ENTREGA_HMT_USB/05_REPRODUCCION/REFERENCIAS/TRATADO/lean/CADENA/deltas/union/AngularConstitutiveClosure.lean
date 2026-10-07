import AngularChannels
import InvolutionProjectors
import ObservedBarbero

/-! Composition of the angular realization with the involution-generated
two-sheet response. The positive chamber and sheet involution are the precise
upstream objects used here; projectors, contraction, completion, response and
inverse recovery are proved. No physical target value is an input. -/
noncomputable section
namespace HMT.III.Constitutive
open Set

namespace OrientedChannels

def logBalance (Q : OrientedChannels) : ℝ :=
  Real.log ((1 - Q.qPlus ^ 90) * (1 - Q.qMinus ^ 90)) -
    Real.log ((1 - Q.qPlus ^ 120) * (1 - Q.qMinus ^ 120))

theorem numerator_product_pos (Q : OrientedChannels) :
    0 < (1 - Q.qPlus ^ 90) * (1 - Q.qMinus ^ 90) := by
  apply mul_pos <;> apply sub_pos.mpr
  · exact pow_lt_one₀ Q.plus_mem.1.le Q.plus_mem.2 (by decide)
  · exact pow_lt_one₀ Q.minus_mem.1.le Q.minus_mem.2 (by decide)

theorem denominator_product_pos (Q : OrientedChannels) :
    0 < (1 - Q.qPlus ^ 120) * (1 - Q.qMinus ^ 120) :=
  mul_pos (channel_denominator_pos Q.plus_mem) (channel_denominator_pos Q.minus_mem)

theorem logBalance_eq_log_response (Q : OrientedChannels) :
    Q.logBalance = Real.log (Q.vacuum.rPlus * Q.vacuum.rMinus) := by
  unfold logBalance
  rw [← Real.log_div (ne_of_gt Q.numerator_product_pos)
    (ne_of_gt Q.denominator_product_pos)]
  congr 1
  change _ = channelResponse Q.qPlus * channelResponse Q.qMinus
  unfold channelResponse
  exact (div_mul_div_comm _ _ _ _).symm

def kinematicSpeed (Q : OrientedChannels) : ℝ := Real.exp (-Q.logBalance)

theorem kinematicSpeed_eq_constitutive (Q : OrientedChannels) :
    Q.kinematicSpeed = Q.vacuum.speed := by
  rw [kinematicSpeed, Q.logBalance_eq_log_response, Real.exp_neg,
    Real.exp_log (mul_pos Q.vacuum.plus_pos Q.vacuum.minus_pos)]
  simp only [PositiveResponse.speed, one_div]

theorem speed_impedance_preserve_angles (Q R : OrientedChannels)
    (hZ : Q.vacuum.impedance = R.vacuum.impedance)
    (hc : Q.kinematicSpeed = R.kinematicSpeed) :
    Q.angularX = R.angularX ∧ Q.angularY = R.angularY := by
  rw [Q.kinematicSpeed_eq_constitutive, R.kinematicSpeed_eq_constitutive] at hc
  have readings := Q.vacuum.readings_determine_response R.vacuum hZ hc
  exact Q.labelled_responses_determine_angles R readings.1 readings.2

def amplifiedLogResponse (Q : OrientedChannels) (n : ℕ) :
    Matrix (Fin 2 × Fin n) (Fin 2 × Fin n) ℝ :=
  Matrix.diagonal (fun i => if i.1 = 0 then Real.log Q.vacuum.rPlus
    else Real.log Q.vacuum.rMinus)

theorem amplified_log_trace (Q : OrientedChannels) (n : ℕ) :
    Matrix.trace (Q.amplifiedLogResponse n) =
      (n : ℝ) * (Real.log Q.vacuum.rPlus + Real.log Q.vacuum.rMinus) := by
  simp [amplifiedLogResponse, Matrix.trace_diagonal, Fintype.sum_prod_type,
    Fin.sum_univ_two]
  ring

def refinedSpeed (Q : OrientedChannels) (m : ℕ) : ℝ :=
  Real.exp (-Matrix.trace (Q.amplifiedLogResponse (9 ^ m)) / (9 : ℝ) ^ m)

theorem refinedSpeed_eq_constitutive (Q : OrientedChannels) (m : ℕ) :
    Q.refinedSpeed m = Q.vacuum.speed := by
  rw [refinedSpeed, Q.amplified_log_trace]
  push_cast
  have hn : (9 : ℝ) ^ m ≠ 0 := pow_ne_zero _ (by norm_num)
  have hcancel : -((9 : ℝ) ^ m * (Real.log Q.vacuum.rPlus + Real.log Q.vacuum.rMinus)) /
      (9 : ℝ) ^ m = -(Real.log Q.vacuum.rPlus + Real.log Q.vacuum.rMinus) := by
    field_simp
    ring
  rw [hcancel, ← Real.log_mul (ne_of_gt Q.vacuum.plus_pos)
    (ne_of_gt Q.vacuum.minus_pos), Real.exp_neg,
    Real.exp_log (mul_pos Q.vacuum.plus_pos Q.vacuum.minus_pos)]
  simp only [PositiveResponse.speed, one_div]

end OrientedChannels

namespace AngularChamber

theorem vacuum_bounds (a : AngularChamber) :
    3 / 4 < a.channels.vacuum.rMinus ∧
      a.channels.vacuum.rMinus < a.channels.vacuum.rPlus ∧
      a.channels.vacuum.rPlus < 1 := a.channels.vacuum_order

variable {A : Type*} [Ring A] [Algebra ℝ A]

def transport (a : AngularChamber) (R : A) (hR : R * R = 1) : A :=
  (projectorsOfInvolution R hR).transport a.channels.qPlus a.channels.qMinus

def constitutiveOperator (a : AngularChamber) (R : A) (hR : R * R = 1) : A :=
  (projectorsOfInvolution R hR).vacuum a.channels.qPlus a.channels.qMinus

theorem operator_from_angles (a : AngularChamber) (R : A) (hR : R * R = 1) :
    a.constitutiveOperator R hR =
      channelResponse (Real.exp (-a.x - a.y)) • sheetPlus R +
      channelResponse (Real.exp (-a.x + a.y)) • sheetMinus R :=
  (projectorsOfInvolution R hR).vacuum_decomposition _ _

theorem completion_from_angles (a : AngularChamber) (R : A) (hR : R * R = 1) :
    ∃! W : A, W * TwoSheetProjectors.sigma4 (a.transport R hR ^ 30) =
      TwoSheetProjectors.sigma3 (a.transport R hR ^ 30) :=
  involution_response_unique R hR a.channels

theorem operator_uses_genuine_inverse (a : AngularChamber) (R : A) (hR : R * R = 1) :
    a.constitutiveOperator R hR = (1 - a.transport R hR ^ 90) *
      (((projectorsOfInvolution R hR).denominatorUnit
        a.channels.plus_mem a.channels.minus_mem)⁻¹ : Aˣ) := rfl

theorem barbero_from_angular_response (a : AngularChamber) :
    HMT.OrientedReturn.angularFunctional a.x a.y =
      HMT.OrientedReturn.speedImpedanceFunctional
        a.channels.vacuum.impedance a.channels.vacuum.speed
        (HMT.OrientedReturn.vacuum_minus_reading_mem a.channels)
        (HMT.OrientedReturn.vacuum_plus_reading_mem a.channels) := by
  have h := HMT.OrientedReturn.barbero_from_speed_impedance a.channels
  rw [HMT.OrientedReturn.barbero_angular,
    a.angularX_channels, a.angularY_channels] at h
  exact h

/-- One composed terminal statement: the angular realization determines a unique
operator response, recovers its two angular coordinates, and publishes the same
speed in the kinetic and constitutive readings. -/
theorem angular_constitutive_closure (a : AngularChamber) (R : A) (hR : R * R = 1) :
    (∃! W : A, W * TwoSheetProjectors.sigma4 (a.transport R hR ^ 30) =
      TwoSheetProjectors.sigma3 (a.transport R hR ^ 30)) ∧
    a.channels.angularX = a.x ∧ a.channels.angularY = a.y ∧
    a.channels.kinematicSpeed = a.channels.vacuum.speed ∧
    (0 < a.channels.vacuum.epsilon ∧ 0 < a.channels.vacuum.mu ∧
      0 < a.channels.vacuum.impedance ∧ 0 < a.channels.vacuum.speed) :=
  ⟨a.completion_from_angles R hR, a.angularX_channels, a.angularY_channels,
   a.channels.kinematicSpeed_eq_constitutive, a.channels.vacuum.coordinates_pos⟩

end AngularChamber

def canonicalSheetInvolution : Matrix (Fin 2) (Fin 2) ℝ := Matrix.diagonal ![1, -1]

theorem canonicalSheetInvolution_square :
    canonicalSheetInvolution * canonicalSheetInvolution = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [canonicalSheetInvolution, Matrix.mul_apply, Fin.sum_univ_two]

/-- No arbitrary projectors or scalar channels enter this two-sheet realization:
both are produced by the angle pair and fixed sheet labels. -/
theorem canonical_angular_constitutive_closure (a : AngularChamber) :
    (∃! W : Matrix (Fin 2) (Fin 2) ℝ,
      W * TwoSheetProjectors.sigma4
        (a.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30) =
      TwoSheetProjectors.sigma3
        (a.transport canonicalSheetInvolution canonicalSheetInvolution_square ^ 30)) ∧
    a.channels.angularX = a.x ∧ a.channels.angularY = a.y ∧
    (∀ m : ℕ, a.channels.refinedSpeed m = a.channels.vacuum.speed) :=
  ⟨a.completion_from_angles canonicalSheetInvolution canonicalSheetInvolution_square,
   a.angularX_channels, a.angularY_channels, a.channels.refinedSpeed_eq_constitutive⟩

#print axioms OrientedChannels.numerator_product_pos
#print axioms OrientedChannels.denominator_product_pos
#print axioms OrientedChannels.logBalance_eq_log_response
#print axioms OrientedChannels.kinematicSpeed_eq_constitutive
#print axioms OrientedChannels.speed_impedance_preserve_angles
#print axioms OrientedChannels.amplified_log_trace
#print axioms OrientedChannels.refinedSpeed_eq_constitutive
#print axioms AngularChamber.vacuum_bounds
#print axioms AngularChamber.operator_from_angles
#print axioms AngularChamber.completion_from_angles
#print axioms AngularChamber.operator_uses_genuine_inverse
#print axioms AngularChamber.barbero_from_angular_response
#print axioms AngularChamber.angular_constitutive_closure
#print axioms canonicalSheetInvolution_square
#print axioms canonical_angular_constitutive_closure
end HMT.III.Constitutive
