import APPGlobalCommutator
import APPGramNorm
import APPPhaseMode

/-! The complete APP fibre census fixes the global commutator norm. All norms
below are Hilbert operator norms. The uniform normalization on the 729-point
space is treated explicitly by its sharp bound, not by an entrywise norm. -/

noncomputable section
namespace HMT.I.APPGlobalPrefactor

open HMT.I.APPGlobalCommutator HMT.I.APPFiberCensus

def incompatibility : EuclideanSpace ℝ Triple →L[ℝ] EuclideanSpace ℝ Triple :=
  sigmaProjection * piProjection - piProjection * sigmaProjection

theorem generated_gram_identification :
    APPFiberOperators.generatedGramReal = APPGramSpectrum.realGram := by
  ext a c
  exact (APPGramSpectrum.realGram_entry a c).symm

theorem incompatibility_norm_squared : ‖incompatibility‖ ^ 2 = 3 / 16 := by
  rw [incompatibility, app_global_commutator_norm_sq]
  change ‖Matrix.toEuclideanCLM (n := Digit) (𝕜 := ℝ) APPFiberOperators.generatedGramReal -
    (Matrix.toEuclideanCLM (n := Digit) (𝕜 := ℝ) APPFiberOperators.generatedGramReal)^2‖ = 3 / 16
  rw [generated_gram_identification, pow_two]
  exact APPGramNorm.gramCLM_defect_norm

theorem incompatibility_norm : ‖incompatibility‖ = Real.sqrt 3 / 4 := by
  have hsq := incompatibility_norm_squared
  have hs := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)
  have h0 := norm_nonneg incompatibility
  have hs0 := Real.sqrt_nonneg (3 : ℝ)
  nlinarith

/-- The vector norm for uniform measure on 729 triples is the counting norm
divided by sqrt(729)=27. Scaling both sides preserves every operator bound. -/
theorem uniform_bound_iff (T : EuclideanSpace ℝ Triple →L[ℝ] EuclideanSpace ℝ Triple)
    (b : ℝ) (hb : 0 ≤ b) :
    (∀ x, ‖T x‖ / 27 ≤ b * (‖x‖ / 27)) ↔ ‖T‖ ≤ b := by
  constructor
  · intro h
    apply ContinuousLinearMap.opNorm_le_bound _ hb
    intro x
    have hx := h x
    nlinarith
  · intro h x
    have hx := (T.le_opNorm x).trans (mul_le_mul_of_nonneg_right h (norm_nonneg x))
    nlinarith

/-- A sharp characterization in the manuscript's uniform-measure norm. -/
theorem uniform_incompatibility_sharp_bound (b : ℝ) (hb : 0 ≤ b) :
    (∀ x, ‖incompatibility x‖ / 27 ≤ b * (‖x‖ / 27)) ↔
      Real.sqrt 3 / 4 ≤ b := by
  rw [uniform_bound_iff _ b hb, incompatibility_norm]

#print axioms generated_gram_identification
#print axioms incompatibility_norm_squared
#print axioms incompatibility_norm
#print axioms uniform_bound_iff
#print axioms uniform_incompatibility_sharp_bound

end HMT.I.APPGlobalPrefactor
