import PellSection
import Mathlib.Analysis.Calculus.DSlope
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-! Genuine interval-integral representation of the previously constructed
oriented series. The removable value at zero is derived, not assumed. -/

noncomputable section

open Filter Set MeasureTheory
open scoped Topology

namespace HMT.III.OrientedMoment

def regularAtanKernel : ℝ → ℝ := dslope Real.arctan 0

theorem regularAtanKernel_zero : regularAtanKernel 0 = 1 := by
  simp [regularAtanKernel, Real.deriv_arctan]

theorem regularAtanKernel_eq {s : ℝ} (hs : s ≠ 0) :
    regularAtanKernel s = Real.arctan s / s := by
  simp [regularAtanKernel, dslope_of_ne _ hs, slope_def_field]

theorem regularAtanKernel_continuous : Continuous regularAtanKernel := by
  apply continuous_iff_continuousAt.2
  intro s
  by_cases hs : s = 0
  · subst s
    exact continuousAt_dslope_same.2 (Real.differentiableAt_arctan 0)
  · exact (continuousAt_dslope_of_ne hs).2 Real.continuous_arctan.continuousAt

theorem atanKernel_ae : regularAtanKernel =ᵐ[volume] (fun s : ℝ => Real.arctan s / s) := by
  have hn : ∀ᵐ s : ℝ, s ≠ 0 := by
    rw [ae_iff]
    simp
  filter_upwards [hn] with s hs
  exact regularAtanKernel_eq hs

theorem atanKernel_intervalIntegrable (a b : ℝ) :
    IntervalIntegrable (fun s : ℝ => Real.arctan s / s) volume a b := by
  exact (regularAtanKernel_continuous.intervalIntegrable a b).congr
    (ae_restrict_of_ae atanKernel_ae)

theorem moment_hasDerivAt_quotient {s : ℝ} (hs0 : 0 < s) (hs1 : s < 1) :
    HasDerivAt moment (Real.arctan s / s) s := by
  have hs : ‖s‖ < 1 := by simpa only [Real.norm_eq_abs, abs_of_pos hs0] using hs1
  have he : (∑' n, derivativeTerm n s) = Real.arctan s / s :=
    (eq_div_iff (ne_of_gt hs0)).2 (by simpa only [mul_comm] using weighted_derivativeSeries hs)
  rw [← he]
  exact moment_hasDerivAt hs

theorem moment_integral {s : ℝ} (hs0 : 0 ≤ s) (hs1 : s ≤ 1) :
    moment s = ∫ t in (0 : ℝ)..s, Real.arctan t / t := by
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le hs0
    (moment_continuousOn.mono (Icc_subset_Icc le_rfl hs1))
    (fun t ht => moment_hasDerivAt_quotient ht.1 (lt_of_lt_of_le ht.2 hs1))
    (atanKernel_intervalIntegrable 0 s)
  simpa only [moment_zero, sub_zero] using h.symm

theorem moment_regularIntegral {s : ℝ} (hs0 : 0 ≤ s) (hs1 : s ≤ 1) :
    moment s = ∫ t in (0 : ℝ)..s, regularAtanKernel t := by
  rw [moment_integral hs0 hs1]
  apply intervalIntegral.integral_congr_ae
  filter_upwards [atanKernel_ae] with t ht using fun _ => ht.symm

theorem catalan_integral : catalan = ∫ t in (0 : ℝ)..1, Real.arctan t / t :=
  moment_integral (by norm_num) le_rfl

theorem pell_moment_integral : moment pellRho = ∫ t in (0 : ℝ)..pellRho, Real.arctan t / t :=
  moment_integral pellRho_pos.le pellRho_lt_one.le

#print axioms regularAtanKernel_zero
#print axioms regularAtanKernel_continuous
#print axioms atanKernel_intervalIntegrable
#print axioms moment_integral
#print axioms moment_regularIntegral
#print axioms catalan_integral
#print axioms pell_moment_integral

end HMT.III.OrientedMoment
