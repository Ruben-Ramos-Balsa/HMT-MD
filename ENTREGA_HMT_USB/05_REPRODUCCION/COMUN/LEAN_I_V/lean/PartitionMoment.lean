import ThermalEnergy
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

noncomputable section
open Set MeasureTheory Real

namespace HMT.V.BosonicMoments

def partitionKernel (x : ℝ) : ℝ := -x ^ 2 * Real.log (1 - Real.exp (-x))
def partitionTerm (n : ℕ) (x : ℝ) : ℝ := laplaceTerm 3 n x / (n + 1 : ℝ)

theorem partition_hasSum {x : ℝ} (hx : 0 < x) :
    HasSum (fun n : ℕ => partitionTerm n x) (partitionKernel x) := by
  have he : |Real.exp (-x)| < 1 := by
    rw [abs_of_pos (Real.exp_pos _)]
    simpa using Real.exp_lt_exp.mpr (neg_neg_of_pos hx)
  have h := (Real.hasSum_pow_div_log_of_abs_lt_one he).mul_left (x ^ 2)
  convert h using 1
  · ext n
    dsimp [partitionTerm, laplaceTerm]
    rw [← Real.exp_nat_mul]
    norm_num [Real.rpow_natCast]
    ring
  · dsimp [partitionKernel]
    ring

theorem partitionTerm_integrable (n : ℕ) :
    IntegrableOn (partitionTerm n) (Ioi 0) :=
  (laplaceTerm_integrable (s := 3) (by norm_num) n).div_const _

theorem partitionTerm_integral (n : ℕ) :
    (∫ x in Ioi (0 : ℝ), partitionTerm n x) =
      2 * (1 / (n + 1 : ℝ)) ^ (4 : ℝ) := by
  simp_rw [partitionTerm, integral_div, laplaceTerm_integral (by norm_num : (0 : ℝ) < 3)]
  norm_num [Real.rpow_natCast, Nat.factorial]
  field_simp
  ring

theorem partitionTerm_norm_integral (n : ℕ) :
    (∫ x in Ioi (0 : ℝ), ‖partitionTerm n x‖) =
      2 * (1 / (n + 1 : ℝ)) ^ (4 : ℝ) := by
  rw [← partitionTerm_integral n]
  apply setIntegral_congr_fun measurableSet_Ioi
  intro x hx
  apply norm_of_nonneg
  dsimp [partitionTerm, laplaceTerm]
  apply div_nonneg
  · exact mul_nonneg (Real.rpow_nonneg hx.le _) (Real.exp_pos _).le
  · positivity

theorem partition_kernel_integral :
    (∫ x in Ioi (0 : ℝ), partitionKernel x) = Real.pi ^ 4 / 45 := by
  have hnorm : Summable (fun n : ℕ => ∫ x in Ioi (0 : ℝ), ‖partitionTerm n x‖) := by
    simp_rw [partitionTerm_norm_integral]
    exact (spectral_weights_summable (s := 4) (by norm_num)).mul_left 2
  have h := hasSum_integral_of_summable_integral_norm
    (μ := volume.restrict (Ioi 0)) partitionTerm_integrable hnorm
  have hv : (∫ x in Ioi (0 : ℝ), ∑' n : ℕ, partitionTerm n x) =
      (∫ x in Ioi (0 : ℝ), partitionKernel x) := by
    apply setIntegral_congr_fun measurableSet_Ioi
    intro x hx
    exact (partition_hasSum hx).tsum_eq
  rw [hv] at h
  simp_rw [partitionTerm_integral] at h
  rw [← h.tsum_eq, tsum_mul_left]
  change 2 * zetaSeries 4 = _
  rw [zetaSeries_four]
  ring

theorem partition_kernel_integrable : IntegrableOn partitionKernel (Ioi 0) := by
  apply Integrable.of_integral_ne_zero
  rw [partition_kernel_integral]
  positivity

theorem scaled_partition_integral {b : ℝ} (hb : 0 < b) :
    (∫ x in Ioi (0 : ℝ), -x ^ 2 * Real.log (1 - Real.exp (-(b*x)))) =
      Real.pi ^ 4 / (45 * b ^ 3) := by
  have h := integral_comp_mul_left_Ioi partitionKernel 0 hb
  have hf : (fun x => partitionKernel (b*x)) =
      fun x => b ^ 2 * (-x ^ 2 * Real.log (1 - Real.exp (-(b*x)))) := by
    ext x
    dsimp [partitionKernel]
    ring
  rw [hf, integral_const_mul, mul_zero, partition_kernel_integral] at h
  simp only [smul_eq_mul] at h
  calc
    _ = (b ^ 2)⁻¹ * (b ^ 2 * (∫ x in Ioi (0 : ℝ), -x ^ 2 * Real.log (1 - Real.exp (-(b*x))))) := by
      rw [inv_mul_cancel_left₀ (pow_ne_zero _ hb.ne')]
    _ = (b ^ 2)⁻¹ * (b⁻¹ * (Real.pi ^ 4 / 45)) := by rw [h]
    _ = _ := by field_simp; ring

#print axioms partition_hasSum
#print axioms partitionTerm_integrable
#print axioms partitionTerm_integral
#print axioms partition_kernel_integral
#print axioms partition_kernel_integrable
#print axioms scaled_partition_integral

end HMT.V.BosonicMoments
