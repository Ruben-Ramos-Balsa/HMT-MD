import APPGramSpectrum
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.CStarAlgebra.Basic

/-! The norm here is the Hilbert operator norm, not the entrywise matrix norm. -/
namespace HMT.I.APPGramNorm

open Matrix HMT.I.APPGramSpectrum
open scoped Matrix.L2OpNorm

noncomputable def defectValues : Fin 9 → ℝ :=
  fun i => realEigenvalues i * (1 - realEigenvalues i)

theorem orthogonalEigenvectors_unitary :
    orthogonalEigenvectors ∈ unitary RealMat := by
  rw [unitary.mem_iff]
  simpa only [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_eq_transpose_of_trivial]
    using And.intro orthogonalEigenvectors_transpose_mul orthogonalEigenvectors_mul_transpose

theorem defect_intertwining :
    (realGram - realGram * realGram) * orthogonalEigenvectors =
      orthogonalEigenvectors * diagonal defectValues := by
  have hs : (realGram * realGram) * orthogonalEigenvectors =
      orthogonalEigenvectors * (diagonal realEigenvalues * diagonal realEigenvalues) := by
    rw [mul_assoc, orthogonal_gram_intertwining, ← mul_assoc,
      orthogonal_gram_intertwining, mul_assoc]
  rw [sub_mul, orthogonal_gram_intertwining, hs, ← mul_sub]
  congr 1
  rw [diagonal_mul_diagonal, diagonal_sub]
  apply congrArg Matrix.diagonal
  funext i
  simp [defectValues, mul_sub]

theorem defect_reconstruction :
    realGram - realGram * realGram =
      orthogonalEigenvectors * diagonal defectValues * orthogonalEigenvectors.transpose := by
  rw [← defect_intertwining, mul_assoc, orthogonalEigenvectors_mul_transpose, mul_one]

theorem diagonal_opNorm_le {n : ℕ} (d : Fin n → ℝ) (c : ℝ) (hc : 0 ≤ c)
    (hd : ∀ i, |d i| ≤ c) :
    ‖Matrix.toEuclideanCLM (n := Fin n) (𝕜 := ℝ) (diagonal d)‖ ≤ c := by
  apply ContinuousLinearMap.opNorm_le_bound _ hc
  intro x
  apply (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hc (norm_nonneg _))).mp
  rw [mul_pow, PiLp.norm_sq_eq_of_L2, PiLp.norm_sq_eq_of_L2]
  have happly (i : Fin n) : (Matrix.toEuclideanCLM (n := Fin n) (𝕜 := ℝ) (diagonal d) x) i = d i * x i := by
    change (diagonal d *ᵥ (fun j => x j)) i = d i * x i
    exact Matrix.mulVec_diagonal d (fun j => x j) i
  simp_rw [happly, norm_mul, mul_pow]
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i _
  apply mul_le_mul_of_nonneg_right _ (sq_nonneg _)
  exact (sq_le_sq₀ (norm_nonneg _) hc).2 (by simpa only [Real.norm_eq_abs] using hd i)

theorem diagonal_opNorm_lower {n : ℕ} (d : Fin n → ℝ) (i : Fin n) :
    |d i| ≤ ‖Matrix.toEuclideanCLM (n := Fin n) (𝕜 := ℝ) (diagonal d)‖ := by
  let x : EuclideanSpace ℝ (Fin n) := EuclideanSpace.single i 1
  have hx : ‖x‖ = 1 := by simp [x]
  have hy : Matrix.toEuclideanCLM (n := Fin n) (𝕜 := ℝ) (diagonal d) x = EuclideanSpace.single i (d i) := by
    ext j
    change (diagonal d *ᵥ Pi.single i 1) j = (Pi.single i (d i) : Fin n → ℝ) j
    rw [diagonal_mulVec_single]
    simp
  have h := (Matrix.toEuclideanCLM (n := Fin n) (𝕜 := ℝ) (diagonal d)).le_opNorm x
  simpa [hy, hx] using h

theorem diagonal_defect_norm :
    ‖Matrix.toEuclideanCLM (n := Fin 9) (𝕜 := ℝ) (diagonal defectValues)‖ = 3/16 := by
  apply le_antisymm
  · apply diagonal_opNorm_le defectValues (3/16) (by norm_num)
    intro i
    change |realEigenvalues i * (1 - realEigenvalues i)| ≤ 3/16
    rw [abs_of_nonneg (real_spectral_defect_bound i).1]
    exact (real_spectral_defect_bound i).2
  · have h := diagonal_opNorm_lower defectValues (1 : Fin 9)
    simpa only [defectValues, real_spectral_defect_attained,
      abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 3/16)] using h

theorem gram_defect_norm :
    ‖Matrix.toEuclideanCLM (n := Fin 9) (𝕜 := ℝ) (realGram - realGram * realGram)‖ = 3/16 := by
  rw [← Matrix.cstar_norm_def, defect_reconstruction]
  have hstar : orthogonalEigenvectors.transpose ∈ unitary RealMat := by
    simpa only [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_eq_transpose_of_trivial]
      using unitary.star_mem orthogonalEigenvectors_unitary
  rw [CStarRing.norm_mul_mem_unitary _ hstar,
    CStarRing.norm_mem_unitary_mul _ orthogonalEigenvectors_unitary,
    Matrix.cstar_norm_def, diagonal_defect_norm]

theorem gramCLM_defect_norm :
    ‖Matrix.toEuclideanCLM (n := Fin 9) (𝕜 := ℝ) realGram -
      Matrix.toEuclideanCLM (n := Fin 9) (𝕜 := ℝ) realGram *
      Matrix.toEuclideanCLM (n := Fin 9) (𝕜 := ℝ) realGram‖ = 3/16 := by
  simpa only [map_sub, map_mul] using gram_defect_norm

#print axioms orthogonalEigenvectors_unitary
#print axioms defect_intertwining
#print axioms defect_reconstruction
#print axioms diagonal_opNorm_le
#print axioms diagonal_opNorm_lower
#print axioms diagonal_defect_norm
#print axioms gram_defect_norm
#print axioms gramCLM_defect_norm

end HMT.I.APPGramNorm
