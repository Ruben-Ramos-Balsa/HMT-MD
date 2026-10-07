import ProjectionCompressedNorm
import APPFiberOperators
import Mathlib.Analysis.CStarAlgebra.Matrix

noncomputable section

namespace HMT.I.APPGlobalCommutator

open ContinuousLinearMap Matrix
open HMT.I.APPFiberCensus HMT.I.APPFiberOperators HMT.I.ProjectionNorm

def rectMap {m n : Type*} [Fintype m] [Fintype n]
    [DecidableEq m] [DecidableEq n]
    (A : Matrix m n ℝ) : EuclideanSpace ℝ n →L[ℝ] EuclideanSpace ℝ m :=
  (Matrix.toEuclideanLin A).toContinuousLinearMap

theorem rectMap_mul {m n k : Type*} [Fintype m] [Fintype n] [Fintype k]
    [DecidableEq m] [DecidableEq n] [DecidableEq k]
    (A : Matrix m n ℝ) (B : Matrix n k ℝ) : rectMap (A*B)=(rectMap A).comp (rectMap B) := by
  ext x i
  change ((A*B)*ᵥ (WithLp.ofLp x)) i = (A*ᵥ (B*ᵥ (WithLp.ofLp x))) i
  rw [Matrix.mulVec_mulVec]

theorem rectMap_transpose {m n : Type*} [Fintype m] [Fintype n]
    [DecidableEq m] [DecidableEq n]
    (A : Matrix m n ℝ) : rectMap Aᵀ=adjoint (rectMap A) := by
  change (Matrix.toEuclideanLin Aᵀ).toContinuousLinearMap =
    adjoint ((Matrix.toEuclideanLin A).toContinuousLinearMap)
  have h : Aᴴ=Aᵀ := by ext i j; simp
  rw [← h, Matrix.toEuclideanLin_conjTranspose_eq_adjoint,
    LinearMap.adjoint_toContinuousLinearMap]

def squareMap {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℝ) : EuclideanSpace ℝ n →L[ℝ] EuclideanSpace ℝ n :=
  Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) A

theorem rectMap_square {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℝ) : rectMap A=squareMap A := rfl

theorem rectMap_one {n : Type*} [Fintype n] [DecidableEq n] :
    rectMap (1 : Matrix n n ℝ)=1 := by rw [rectMap_square]; exact map_one (Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ))

def sigmaColumn : EuclideanSpace ℝ Digit →L[ℝ] EuclideanSpace ℝ Triple := rectMap VSigma
def sigmaProjection : EuclideanSpace ℝ Triple →L[ℝ] EuclideanSpace ℝ Triple :=
  squareMap PSigma
def piProjection : EuclideanSpace ℝ Triple →L[ℝ] EuclideanSpace ℝ Triple :=
  squareMap PPi
def gramOperator : EuclideanSpace ℝ Digit →L[ℝ] EuclideanSpace ℝ Digit :=
  squareMap generatedGramReal

theorem sigmaColumn_isometry : (adjoint sigmaColumn).comp sigmaColumn=1 := by
  change (adjoint (rectMap VSigma)).comp (rectMap VSigma)=1
  rw [← rectMap_transpose, ← rectMap_mul, sigma_isometry, rectMap_one]

theorem sigmaProjection_eq_column : sigmaProjection=sigmaColumn.comp (adjoint sigmaColumn) := by
  change squareMap (VSigma*VSigmaᵀ)=(rectMap VSigma).comp (adjoint (rectMap VSigma))
  rw [← rectMap_square, rectMap_mul, rectMap_transpose]

theorem piProjection_idempotent : piProjection*piProjection=piProjection := by
  change Matrix.toEuclideanCLM (n := Triple) (𝕜 := ℝ) PPi * Matrix.toEuclideanCLM (n := Triple) (𝕜 := ℝ) PPi = Matrix.toEuclideanCLM (n := Triple) (𝕜 := ℝ) PPi
  rw [← map_mul, PPi_idempotent]

theorem piProjection_selfAdjoint : star piProjection=piProjection := by
  change star (Matrix.toEuclideanCLM (n := Triple) (𝕜 := ℝ) PPi)=Matrix.toEuclideanCLM (n := Triple) (𝕜 := ℝ) PPi
  rw [← map_star]
  change Matrix.toEuclideanCLM (n := Triple) (𝕜 := ℝ) PPiᵀ=Matrix.toEuclideanCLM (n := Triple) (𝕜 := ℝ) PPi
  rw [PPi_symmetric]

theorem compressed_pi_eq_gramOperator :
    ((adjoint sigmaColumn).comp piProjection).comp sigmaColumn=gramOperator := by
  change ((adjoint (rectMap VSigma)).comp (rectMap PPi)).comp (rectMap VSigma)=
    rectMap generatedGramReal
  rw [← rectMap_transpose, ← rectMap_mul, ← rectMap_mul, compressed_pi_eq_generated_gram]

theorem app_global_commutator_norm_sq :
    ‖sigmaProjection*piProjection-piProjection*sigmaProjection‖^2 =
      ‖gramOperator-gramOperator^2‖ := by
  have h := projection_commutator_compressed_norm_sq sigmaColumn sigmaColumn_isometry
    piProjection piProjection_idempotent piProjection_selfAdjoint
  dsimp only at h
  rw [← sigmaProjection_eq_column, compressed_pi_eq_gramOperator] at h
  exact h

#print axioms rectMap_mul
#print axioms rectMap_transpose
#print axioms rectMap_square
#print axioms rectMap_one
#print axioms sigmaColumn_isometry
#print axioms sigmaProjection_eq_column
#print axioms piProjection_idempotent
#print axioms piProjection_selfAdjoint
#print axioms compressed_pi_eq_gramOperator
#print axioms app_global_commutator_norm_sq

end HMT.I.APPGlobalCommutator

end
