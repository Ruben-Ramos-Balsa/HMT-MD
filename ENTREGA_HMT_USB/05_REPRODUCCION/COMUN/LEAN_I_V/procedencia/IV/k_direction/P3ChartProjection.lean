import SelectedKDirection

/-! Exact matrix identities for the delivered real A5/C5 chart.
The character-sum provenance remains the separate exact Python check.
No representation-theoretic or physical identification is assumed here. -/

noncomputable section
open scoped BigOperators Matrix

namespace HMT.IV.P3ChartProjection
open SelectedKDirection

set_option maxHeartbeats 10000000
set_option maxRecDepth 10000

theorem P3_transpose : P3.transpose = P3 := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

private theorem numerator_mul_self :
    P3Numerator (Real.sqrt 5) * P3Numerator (Real.sqrt 5) =
      (20 : ℝ) • P3Numerator (Real.sqrt 5) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, P3Numerator, Fin.sum_univ_succ] <;>
    ring_nf

theorem P3_mul_self : P3 * P3 = P3 := by
  ext i j
  have h := congrArg (fun M => M i j) numerator_mul_self
  simp only [Matrix.mul_apply, Matrix.smul_apply, smul_eq_mul] at h
  change (∑ k, (P3Numerator (Real.sqrt 5) i k / 20) *
    (P3Numerator (Real.sqrt 5) k j / 20)) = P3Numerator (Real.sqrt 5) i j / 20
  simp_rw [div_mul_div_comm]
  rw [← Finset.sum_div, h]
  ring

theorem P3_uniform_zero : P3.mulVec (fun _ : Fin 12 => (1 : ℝ)) = 0 := by
  ext i
  fin_cases i <;>
    simp [P3, P3Numerator, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> ring

theorem P3_trace : Matrix.trace P3 = 3 := by
  norm_num [Matrix.trace, P3, P3Numerator, Fin.sum_univ_succ]

end HMT.IV.P3ChartProjection

#print axioms HMT.IV.P3ChartProjection.P3_transpose
#print axioms HMT.IV.P3ChartProjection.P3_mul_self
#print axioms HMT.IV.P3ChartProjection.P3_uniform_zero
#print axioms HMT.IV.P3ChartProjection.P3_trace
