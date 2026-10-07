import AngularConstitutiveClosure

/-! Exact composition of the constitutive inverse with the action-ellipse
shape and the relative LC impedance.  The marked angular chamber is the
upstream object; absolute action, clock and dimensional units are not inferred
from its two normalized response coordinates. -/
noncomputable section
namespace HMT.III.Constitutive
open Set

theorem recover_channel_power {q : ℝ} (hq : q ∈ Ioo 0 1) :
    recover (channelResponse q) (channelResponse_bounds hq) = q ^ 30 := by
  have h := recover_spec (channelResponse q) (channelResponse_bounds hq)
  apply response_strictAntiOn.injOn h.1.1.le (channel_power_mem hq).1.le
  exact h.2.trans (channelResponse_eq hq)

namespace AngularChamber

def logPlus (a : AngularChamber) : ℝ := Real.log (a.channels.qPlus ^ 30)
def logMinus (a : AngularChamber) : ℝ := Real.log (a.channels.qMinus ^ 30)

theorem logarithmic_powers (a : AngularChamber) :
    a.logPlus = -30 * (a.x + a.y) ∧ a.logMinus = -30 * (a.x - a.y) := by
  simp only [logPlus, logMinus, Real.log_pow, channels, Real.log_exp]
  constructor <;> ring

theorem log_signs (a : AngularChamber) : a.logPlus < 0 ∧ a.logMinus < 0 := by
  rw [a.logarithmic_powers.1, a.logarithmic_powers.2]
  constructor <;> nlinarith [a.y_pos, a.y_lt_x]

theorem angular_ratio_from_logs (a : AngularChamber) :
    (a.logPlus - a.logMinus) / (a.logPlus + a.logMinus) = a.y / a.x := by
  rw [a.logarithmic_powers.1, a.logarithmic_powers.2]
  have hx : a.x ≠ 0 := ne_of_gt (a.y_pos.trans a.y_lt_x)
  have hsum : -30 * (a.x + a.y) + -30 * (a.x - a.y) ≠ 0 := by
    nlinarith [a.y_pos, a.y_lt_x]
  apply (div_eq_div_iff hsum hx).mpr
  ring

def ellipseAnisotropy (a : AngularChamber) : ℝ :=
  Real.log ((a.x + a.y) / (a.x - a.y)) / 2

theorem ellipseAnisotropy_from_logs (a : AngularChamber) :
    a.ellipseAnisotropy = Real.log (a.logPlus / a.logMinus) / 2 := by
  rw [a.logarithmic_powers.1, a.logarithmic_powers.2]
  unfold ellipseAnisotropy
  congr 2
  exact (mul_div_mul_left _ _ (by norm_num : (-30 : ℝ) ≠ 0)).symm

def relativeLC (a : AngularChamber) : ℝ := Real.exp (-a.ellipseAnisotropy)

theorem relativeLC_pos (a : AngularChamber) : 0 < a.relativeLC := Real.exp_pos _

theorem relativeLC_sq (a : AngularChamber) :
    a.relativeLC ^ 2 = (a.x - a.y) / (a.x + a.y) := by
  have hminus : 0 < a.x - a.y := sub_pos.mpr a.y_lt_x
  have hplus : 0 < a.x + a.y := by linarith [a.y_pos, a.y_lt_x]
  dsimp [relativeLC, ellipseAnisotropy]
  rw [sq, ← Real.exp_add]
  have he : -(Real.log ((a.x + a.y) / (a.x - a.y)) / 2) +
      -(Real.log ((a.x + a.y) / (a.x - a.y)) / 2) =
      -Real.log ((a.x + a.y) / (a.x - a.y)) := by ring
  rw [he, Real.exp_neg, Real.exp_log (div_pos hplus hminus), inv_div]

theorem relativeLC_from_logs (a : AngularChamber) :
    a.relativeLC = Real.sqrt (a.logMinus / a.logPlus) := by
  have hratio : a.logMinus / a.logPlus = (a.x - a.y) / (a.x + a.y) := by
    rw [a.logarithmic_powers.1, a.logarithmic_powers.2]
    exact mul_div_mul_left _ _ (by norm_num : (-30 : ℝ) ≠ 0)
  rw [hratio, ← a.relativeLC_sq, Real.sqrt_sq a.relativeLC_pos.le]

def recoveredPowerPlus (a : AngularChamber) : ℝ :=
  recover (1 / Real.sqrt (a.channels.vacuum.impedance * a.channels.vacuum.speed))
    (HMT.OrientedReturn.vacuum_plus_reading_mem a.channels)

def recoveredPowerMinus (a : AngularChamber) : ℝ :=
  recover (Real.sqrt (a.channels.vacuum.impedance / a.channels.vacuum.speed))
    (HMT.OrientedReturn.vacuum_minus_reading_mem a.channels)

theorem recovered_powers (a : AngularChamber) :
    a.recoveredPowerPlus = a.channels.qPlus ^ 30 ∧
    a.recoveredPowerMinus = a.channels.qMinus ^ 30 := by
  constructor
  · simpa only [recoveredPowerPlus, ← a.channels.vacuum.recover_rPlus] using
      recover_channel_power a.channels.plus_mem
  · simpa only [recoveredPowerMinus, ← a.channels.vacuum.recover_rMinus] using
      recover_channel_power a.channels.minus_mem

/-- Terminal inverse composition: normalized (Z,c) determines the two unique
cubic roots, then the angular ratio, ellipse shape and relative LC impedance. -/
theorem constitutive_LC_recovery (a : AngularChamber) :
    (Real.log a.recoveredPowerPlus - Real.log a.recoveredPowerMinus) /
      (Real.log a.recoveredPowerPlus + Real.log a.recoveredPowerMinus) = a.y / a.x ∧
    Real.log (Real.log a.recoveredPowerPlus / Real.log a.recoveredPowerMinus) / 2 =
      a.ellipseAnisotropy ∧
    Real.sqrt (Real.log a.recoveredPowerMinus / Real.log a.recoveredPowerPlus) =
      a.relativeLC := by
  rw [a.recovered_powers.1, a.recovered_powers.2]
  exact ⟨a.angular_ratio_from_logs, a.ellipseAnisotropy_from_logs.symm,
    a.relativeLC_from_logs.symm⟩

end AngularChamber

#print axioms recover_channel_power
#print axioms AngularChamber.logarithmic_powers
#print axioms AngularChamber.log_signs
#print axioms AngularChamber.angular_ratio_from_logs
#print axioms AngularChamber.ellipseAnisotropy_from_logs
#print axioms AngularChamber.relativeLC_pos
#print axioms AngularChamber.relativeLC_sq
#print axioms AngularChamber.relativeLC_from_logs
#print axioms AngularChamber.recovered_powers
#print axioms AngularChamber.constitutive_LC_recovery
end HMT.III.Constitutive
