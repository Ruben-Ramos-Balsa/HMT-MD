import AnnularRiemann
import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls

noncomputable section
open Set Filter MeasureTheory
open scoped Topology

namespace HMT.V.ThermodynamicLimit

theorem euclidean_radial_integral (F : ℝ → ℝ) :
    (∫ x : EuclideanSpace ℝ (Fin 3), F ‖x‖) =
      4 * Real.pi * ∫ r in Ioi (0 : ℝ), r ^ 2 * F r := by
  rw [integral_fun_norm_addHaar volume F]
  norm_num [measureReal_def, EuclideanSpace.volume_ball_fin_three,
    ENNReal.toReal_ofReal (by positivity : 0 ≤ Real.pi * 4 / 3)]
  ring

theorem coordinate_radial_integral (F : ℝ → ℝ) :
    (∫ x : CoordinateSpace, F (euclideanRadius x)) =
      4 * Real.pi * ∫ r in Ioi (0 : ℝ), r ^ 2 * F r := by
  rw [← euclidean_radial_integral F]
  exact (PiLp.volume_preserving_toLp (Fin 3)).integral_comp
    (EuclideanSpace.measurableEquiv (Fin 3)).symm.measurableEmbedding (fun x => F ‖x‖)

theorem coordinate_radial_integrable {F : ℝ → ℝ}
    (hF : (∫ r in Ioi (0 : ℝ), r ^ 2 * F r) ≠ 0) :
    Integrable (fun x : CoordinateSpace => F (euclideanRadius x)) := by
  apply Integrable.of_integral_ne_zero
  rw [coordinate_radial_integral]
  exact mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hF

#print axioms coordinate_radial_integral
#print axioms coordinate_radial_integrable

end HMT.V.ThermodynamicLimit
