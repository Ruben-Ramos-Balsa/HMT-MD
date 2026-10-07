import ScalarSectionNorm
import Mathlib.Analysis.SpecialFunctions.Log.Base

/-! Article II, eq:el-decada. Rational intervals are a downstream interface
for already-published HMT readers. No Planck value or SI reference is used.
Decimal order is the actual integer floor of the base-ten logarithm. -/
namespace HMT.II.DeterminantalAction
noncomputable section

structure ReaderIntervals (phi alpha : ℝ) : Prop where
  phi_lower : 1618 / 1000 < phi
  phi_upper : phi < 1619 / 1000
  alpha_lower : 7297 / 10 ^ 6 < alpha
  alpha_upper : alpha < 7298 / 10 ^ 6

theorem ReaderIntervals.phi_pos {phi alpha : ℝ} (h : ReaderIntervals phi alpha) :
    0 < phi := by linarith [h.phi_lower]

theorem ReaderIntervals.alpha_pos {phi alpha : ℝ} (h : ReaderIntervals phi alpha) :
    0 < alpha := by linarith [h.alpha_lower]

theorem lower_integer_certificate : (10 : ℤ) ^ 65 < 1618 * 7297 ^ 16 := by norm_num

theorem upper_integer_certificate : (1619 : ℤ) * 7298 ^ 16 < 10 ^ 66 := by norm_num

theorem lower_rational_certificate :
    (10 : ℝ) ^ (-34 : ℤ) < (1618 / 1000 : ℝ) * (7297 / 10 ^ 6 : ℝ) ^ 16 := by
  norm_num

theorem upper_rational_certificate :
    (1619 / 1000 : ℝ) * (7298 / 10 ^ 6 : ℝ) ^ 16 < (10 : ℝ) ^ (-33 : ℤ) := by
  norm_num

theorem actionScale_rational_bounds {phi alpha : ℝ} (h : ReaderIntervals phi alpha) :
    (1618 / 1000 : ℝ) * (7297 / 10 ^ 6 : ℝ) ^ 16 < actionScale phi alpha ∧
      actionScale phi alpha < (1619 / 1000 : ℝ) * (7298 / 10 ^ 6 : ℝ) ^ 16 := by
  rw [actionScale_eq]
  have hp := h.phi_pos
  have ha := h.alpha_pos
  constructor
  · gcongr
    · exact h.phi_lower
    · exact h.alpha_lower
  · gcongr
    · exact h.phi_upper
    · exact h.alpha_upper

theorem actionScale_decade_bounds {phi alpha : ℝ} (h : ReaderIntervals phi alpha) :
    (10 : ℝ) ^ (-34 : ℤ) < actionScale phi alpha ∧
      actionScale phi alpha < (10 : ℝ) ^ (-33 : ℤ) :=
  ⟨lower_rational_certificate.trans (actionScale_rational_bounds h).1,
    (actionScale_rational_bounds h).2.trans upper_rational_certificate⟩

def decimalOrder (x : ℝ) : ℤ := ⌊Real.logb 10 x⌋

theorem actionScale_decimalOrder {phi alpha : ℝ} (h : ReaderIntervals phi alpha) :
    decimalOrder (actionScale phi alpha) = -34 := by
  have hs := actionScale_pos h.phi_pos h.alpha_pos
  have hb : (1 : ℝ) < 10 := by norm_num
  have hlo : (-34 : ℝ) < Real.logb 10 (actionScale phi alpha) := by
    apply (Real.lt_logb_iff_rpow_lt hb hs).2
    simpa only [← Real.rpow_intCast, Int.cast_neg, Int.cast_ofNat] using
      (actionScale_decade_bounds h).1
  have hhi : Real.logb 10 (actionScale phi alpha) < (-33 : ℝ) := by
    apply (Real.logb_lt_iff_lt_rpow hb hs).2
    simpa only [← Real.rpow_intCast, Int.cast_neg, Int.cast_ofNat] using
      (actionScale_decade_bounds h).2
  apply Int.floor_eq_iff.mpr
  constructor <;> norm_num
  · exact hlo.le
  · exact hhi

#print axioms lower_integer_certificate
#print axioms upper_integer_certificate
#print axioms actionScale_rational_bounds
#print axioms actionScale_decade_bounds
#print axioms actionScale_decimalOrder

end
end HMT.II.DeterminantalAction
