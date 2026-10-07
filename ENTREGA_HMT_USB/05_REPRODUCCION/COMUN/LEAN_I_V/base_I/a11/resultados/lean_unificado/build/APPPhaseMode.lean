import APPGramSpectrum
import TRITCore

/-! The eigenmode attaining the APP defect is the already defined TRIT phase
selector on nonadic symbols. The equality is a recognition after the census,
not a selector installed in that census. The lift retains the residue identity
and does not discard the APP quotient from the enriched state. -/

namespace HMT.I.APPPhaseMode

open Matrix
open APPFiberCensus APPGramSpectrum

def phaseMode : Fin 9 → ℚ := fun a =>
  (TRITCore.phase (APPArithmetic.value a : ℤ) : ℚ)

theorem phase_mode_values :
    phaseMode = ![1,-1,0,1,-1,0,1,-1,0] := by
  funext a
  fin_cases a <;> norm_num [phaseMode, TRITCore.phase, APPArithmetic.value]

theorem phase_mode_is_eigenvector_column :
    phaseMode = fun a => eigenvectors a 1 := by
  rw [phase_mode_values]
  decide

theorem phase_mode_nonzero : phaseMode ≠ 0 := by
  intro h
  have h0 := congrFun h 0
  norm_num [phase_mode_values] at h0

theorem gram_phase_mode : gram *ᵥ phaseMode = (1 / 4 : ℚ) • phaseMode := by
  rw [phase_mode_is_eigenvector_column]
  funext a
  have h := congrArg (fun M : Mat => M a 1) gram_eigenvectors
  simpa [Matrix.mul_apply, Matrix.mulVec, dotProduct, eigenvalues,
    Matrix.diagonal, Pi.smul_apply, smul_eq_mul, mul_comm] using h

theorem phase_mode_squared_length : ∑ a, (phaseMode a)^2 = 6 := by
  rw [phase_mode_values]
  norm_num [Fin.sum_univ_succ]

theorem phase_defect_value :
    (1 / 4 : ℚ) * (1 - 1 / 4) = 3 / 16 := by norm_num

/-- The phase is unchanged by publishing the nonadic residue. The quotient
identity is retained separately by APPFiberCensus.sum_reconstruction. -/
theorem phase_of_sum_residue (x : Triple) :
    TRITCore.phase (sumValue x : ℤ) = TRITCore.phase (sumDigit x : ℤ) := by
  have h := congrArg (fun n : ℕ => (n : ℤ)) (sum_reconstruction x)
  push_cast at h
  have he : (sumValue x : ℤ) =
      (sumDigit x : ℤ) + 3 * (3 * (APPArithmetic.q9 (sumValue x) : ℤ)) := by
    linarith
  rw [he, TRITCore.phase_periodic]

#print axioms phase_mode_values
#print axioms phase_mode_is_eigenvector_column
#print axioms phase_mode_nonzero
#print axioms gram_phase_mode
#print axioms phase_mode_squared_length
#print axioms phase_defect_value
#print axioms phase_of_sum_residue

end HMT.I.APPPhaseMode
