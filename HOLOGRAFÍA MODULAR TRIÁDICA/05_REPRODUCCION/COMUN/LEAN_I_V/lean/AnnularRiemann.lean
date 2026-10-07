import Mathlib.Analysis.BoxIntegral.UnitPartition
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.MeasureTheory.Constructions.HaarToSphere

/-!
The compact-annulus step in the periodic thermodynamic limit of Article V.
The Euclidean radius is distinct from the sup norm used only to cut off cubes.
This module does not assume or assert the full improper lattice-sum limit.
-/

noncomputable section

open Set Filter MeasureTheory Bornology
open scoped Topology Pointwise

namespace HMT.V.ThermodynamicLimit

abbrev CoordinateSpace := Fin 3 → ℝ

def euclideanRadius (x : CoordinateSpace) : ℝ :=
  ‖WithLp.toLp 2 x‖

lemma continuous_euclideanRadius : Continuous euclideanRadius :=
  (PiLp.continuous_toLp 2 _).norm

lemma supNorm_le_euclideanRadius (x : CoordinateSpace) : ‖x‖ ≤ euclideanRadius x := by
  apply (pi_norm_le_iff_of_nonneg (norm_nonneg (WithLp.toLp 2 x))).2
  intro i
  exact PiLp.norm_apply_le (WithLp.toLp 2 x) i

def cubicAnnulus (δ R : ℝ) : Set CoordinateSpace :=
  Metric.closedBall 0 R ∩ (Metric.ball 0 δ)ᶜ

lemma mem_cubicAnnulus (x : CoordinateSpace) (δ R : ℝ) :
    x ∈ cubicAnnulus δ R ↔ δ ≤ ‖x‖ ∧ ‖x‖ ≤ R := by
  simp only [cubicAnnulus, Set.mem_inter_iff, Metric.mem_closedBall,
    dist_zero_right, Set.mem_compl_iff, Metric.mem_ball, not_lt]
  exact and_comm

lemma cubicAnnulus_measurable (δ R : ℝ) : MeasurableSet (cubicAnnulus δ R) :=
  measurableSet_closedBall.inter measurableSet_ball.compl

lemma cubicAnnulus_bounded (δ R : ℝ) : IsBounded (cubicAnnulus δ R) :=
  Metric.isBounded_closedBall.subset Set.inter_subset_left

lemma cubicAnnulus_frontier_null (δ R : ℝ) :
    volume (frontier (cubicAnnulus δ R)) = 0 := by
  apply measure_mono_null (frontier_inter_subset _ _)
  apply measure_union_null
  · exact measure_mono_null (Set.inter_subset_left.trans Metric.frontier_closedBall_subset_sphere)
      (Measure.addHaar_sphere volume (0 : CoordinateSpace) R)
  · rw [frontier_compl]
    exact measure_mono_null (Set.inter_subset_right.trans Metric.frontier_ball_subset_sphere)
      (Measure.addHaar_sphere volume (0 : CoordinateSpace) δ)

def radialExtension (F : ℝ → ℝ) (δ : ℝ) (x : CoordinateSpace) : ℝ :=
  F (max δ (euclideanRadius x))

lemma radialExtension_continuous {F : ℝ → ℝ} (hF : ContinuousOn F (Ioi 0))
    {δ : ℝ} (hδ : 0 < δ) : Continuous (radialExtension F δ) := by
  apply hF.comp_continuous (continuous_const.max continuous_euclideanRadius)
  intro x
  exact lt_of_lt_of_le hδ (le_max_left _ _)

lemma radialExtension_eq {F : ℝ → ℝ} {δ R : ℝ} {x : CoordinateSpace}
    (hx : x ∈ cubicAnnulus δ R) : radialExtension F δ x = F (euclideanRadius x) := by
  have hxδ := (mem_cubicAnnulus x δ R).1 hx
  simp only [radialExtension, max_eq_right (hxδ.1.trans (supNorm_le_euclideanRadius x))]

def standardIntegerLattice : Submodule ℤ CoordinateSpace :=
  Submodule.span ℤ (Set.range (Pi.basisFun ℝ (Fin 3)))

def annularLatticeIntegral (F : ℝ → ℝ) (δ R : ℝ) (n : ℕ) : ℝ :=
  (∑' x : ↑(cubicAnnulus δ R ∩ (n : ℝ)⁻¹ • (standardIntegerLattice : Set CoordinateSpace)),
    F (euclideanRadius x)) / (n : ℝ) ^ 3

theorem annular_lattice_tendsto {F : ℝ → ℝ} (hF : ContinuousOn F (Ioi 0))
    {δ : ℝ} (hδ : 0 < δ) (R : ℝ) :
    Tendsto (annularLatticeIntegral F δ R) atTop
      (𝓝 (∫ x in cubicAnnulus δ R, F (euclideanRadius x))) := by
  have h := tendsto_tsum_div_pow_atTop_integral (cubicAnnulus δ R)
    (radialExtension F δ) (radialExtension_continuous hF hδ)
    (cubicAnnulus_bounded δ R) (cubicAnnulus_measurable δ R)
    (cubicAnnulus_frontier_null δ R)
  have heq : (∫ x in cubicAnnulus δ R, radialExtension F δ x) =
      ∫ x in cubicAnnulus δ R, F (euclideanRadius x) := by
    apply setIntegral_congr_fun (cubicAnnulus_measurable δ R)
    intro x hx
    exact radialExtension_eq hx
  rw [heq] at h
  convert h using 1
  funext n
  unfold annularLatticeIntegral standardIntegerLattice
  congr 1
  · apply tsum_congr
    intro x
    exact (radialExtension_eq x.property.1).symm

#print axioms annular_lattice_tendsto

end HMT.V.ThermodynamicLimit
