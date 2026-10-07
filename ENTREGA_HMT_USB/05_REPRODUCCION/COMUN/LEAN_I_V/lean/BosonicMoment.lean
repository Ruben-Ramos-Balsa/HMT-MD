import Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral
import Mathlib.Analysis.PSeries
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.NumberTheory.ZetaValues

noncomputable section
open Set MeasureTheory Real

namespace HMT.V.BosonicMoments

def occupation (x : ℝ) : ℝ := (Real.exp x - 1)⁻¹

theorem occupation_hasSum {x : ℝ} (hx : 0 < x) :
    HasSum (fun n : ℕ => Real.exp (-((n + 1 : ℝ) * x))) (occupation x) := by
  have he : Real.exp (-x) < 1 := by simpa using Real.exp_lt_exp.mpr (neg_neg_of_pos hx)
  have hg := (hasSum_geometric_of_lt_one (Real.exp_pos (-x)).le he).mul_left (Real.exp (-x))
  have hc : Real.exp (-x) * (1 - Real.exp (-x))⁻¹ = occupation x := by
    rw [Real.exp_neg, occupation]
    have hne : Real.exp x - 1 ≠ 0 := ne_of_gt (sub_pos.mpr (by simpa using Real.exp_lt_exp.mpr hx))
    field_simp
  rw [hc] at hg
  convert hg using 1
  ext n
  rw [← Real.exp_nat_mul, ← Real.exp_add]
  congr 1
  ring

def laplaceTerm (s : ℝ) (n : ℕ) (x : ℝ) : ℝ :=
  x ^ (s - 1) * Real.exp (-((n + 1 : ℝ) * x))

theorem laplaceTerm_integrable {s : ℝ} (hs : 0 < s) (n : ℕ) :
    IntegrableOn (laplaceTerm s n) (Ioi 0) := by
  have h := integrableOn_rpow_mul_exp_neg_mul_rpow
      (s := s - 1) (p := 1) (b := n + 1) (by linarith) le_rfl (by positivity)
  apply h.congr_fun _ measurableSet_Ioi
  intro x _
  dsimp [laplaceTerm]
  rw [Real.rpow_one, neg_mul]

theorem laplaceTerm_integral {s : ℝ} (hs : 0 < s) (n : ℕ) :
    (∫ x in Ioi (0 : ℝ), laplaceTerm s n x) =
      (1 / (n + 1 : ℝ)) ^ s * Real.Gamma s := by
  exact Real.integral_rpow_mul_exp_neg_mul_Ioi hs (by positivity)

theorem laplaceTerm_norm_integral {s : ℝ} (hs : 0 < s) (n : ℕ) :
    (∫ x in Ioi (0 : ℝ), ‖laplaceTerm s n x‖) =
      (1 / (n + 1 : ℝ)) ^ s * Real.Gamma s := by
  rw [← laplaceTerm_integral hs n]
  apply setIntegral_congr_fun measurableSet_Ioi
  intro x hx
  exact norm_of_nonneg (mul_nonneg (Real.rpow_nonneg hx.le _) (Real.exp_pos _).le)

theorem spectral_weights_summable {s : ℝ} (hs : 1 < s) :
    Summable (fun n : ℕ => (1 / (n + 1 : ℝ)) ^ s) := by
  have h := (Real.summable_one_div_nat_rpow.mpr hs).comp_injective Nat.succ_injective
  convert h using 1
  ext n
  simp only [Function.comp_apply, Nat.cast_succ, one_div]
  exact Real.inv_rpow (by positivity) _

def zetaSeries (s : ℝ) : ℝ := ∑' n : ℕ, (1 / (n + 1 : ℝ)) ^ s

theorem bosonic_moment {s : ℝ} (hs : 1 < s) :
    (∫ x in Ioi (0 : ℝ), x ^ (s - 1) * occupation x) =
      Real.Gamma s * zetaSeries s := by
  have h0 : 0 < s := lt_trans zero_lt_one hs
  have hnorm : Summable (fun n : ℕ => ∫ x in Ioi (0 : ℝ), ‖laplaceTerm s n x‖) := by
    simp_rw [laplaceTerm_norm_integral h0]
    exact (spectral_weights_summable hs).mul_right _
  have hh := hasSum_integral_of_summable_integral_norm
    (μ := volume.restrict (Ioi 0)) (laplaceTerm_integrable h0) hnorm
  have hv : (∫ x in Ioi (0 : ℝ), ∑' n : ℕ, laplaceTerm s n x) =
      (∫ x in Ioi (0 : ℝ), x ^ (s - 1) * occupation x) := by
    apply setIntegral_congr_fun measurableSet_Ioi
    intro x hx
    exact ((occupation_hasSum hx).mul_left (x ^ (s - 1))).tsum_eq
  rw [hv] at hh
  simp_rw [laplaceTerm_integral h0] at hh
  rw [← hh.tsum_eq, tsum_mul_right, mul_comm]
  rfl

theorem zetaSeries_pos {s : ℝ} (hs : 1 < s) : 0 < zetaSeries s := by
  apply (spectral_weights_summable hs).tsum_pos (fun n => by positivity) 0
  simp

theorem bosonic_moment_integrable {s : ℝ} (hs : 1 < s) :
    IntegrableOn (fun x : ℝ => x ^ (s - 1) * occupation x) (Ioi 0) := by
  apply Integrable.of_integral_ne_zero
  rw [bosonic_moment hs]
  exact (mul_pos (Real.Gamma_pos_of_pos (by linarith)) (zetaSeries_pos hs)).ne'

theorem zetaSeries_four : zetaSeries 4 = Real.pi ^ 4 / 90 := by
  have h := hasSum_zeta_four.summable.tsum_eq_zero_add
  have he : zetaSeries 4 = ∑' n : ℕ, (1 : ℝ) / (n + 1 : ℝ) ^ 4 := by
    apply tsum_congr
    intro n
    norm_num [Real.rpow_natCast, div_pow]
  rw [he, ← hasSum_zeta_four.tsum_eq]
  simpa only [Nat.cast_zero, zero_pow (by decide : 4 ≠ 0), div_zero, zero_add,
    Nat.cast_add, Nat.cast_one] using h.symm

theorem energy_kernel_integral :
    (∫ x in Ioi (0 : ℝ), x ^ 3 * occupation x) = Real.pi ^ 4 / 15 := by
  have h := bosonic_moment (s := 4) (by norm_num)
  norm_num [zetaSeries_four, Real.rpow_natCast] at h
  norm_num [Nat.factorial] at h
  linarith

theorem energy_kernel_integrable :
    IntegrableOn (fun x : ℝ => x ^ 3 * occupation x) (Ioi 0) := by
  simpa only [show (4 : ℝ) - 1 = 3 by norm_num, Real.rpow_ofNat] using
    bosonic_moment_integrable (s := 4) (by norm_num)

#print axioms occupation_hasSum
#print axioms laplaceTerm_integrable
#print axioms laplaceTerm_integral
#print axioms spectral_weights_summable
#print axioms bosonic_moment
#print axioms bosonic_moment_integrable
#print axioms zetaSeries_four
#print axioms energy_kernel_integral
#print axioms energy_kernel_integrable

end HMT.V.BosonicMoments
