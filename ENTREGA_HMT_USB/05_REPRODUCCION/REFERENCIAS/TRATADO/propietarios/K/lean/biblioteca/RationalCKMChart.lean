import Mathlib

/-! Exact rational CKM reader, downstream of generated HMT angular coordinates.
The rules are the explicit sector system in sections/08b_reglas_sectoriales.tex.
No measured mixing angle or target value occurs in this module. -/

namespace HMT.II.CKM

noncomputable section

set_option maxHeartbeats 2000000

open Matrix

abbrev Vec3 := Fin 3 → ℝ
abbrev Mat3 := Matrix (Fin 3) (Fin 3) ℝ

def chartMatrix : Mat3 := !![2, -5, 28; 0, 7, -(25 / 2); 1, -20, -(2 / 3)]

def inverseMatrix : Mat3 :=
  !![1528 / 3857, 3380 / 3857, 801 / 3857;
     75 / 3857, 176 / 3857, -(150 / 3857);
     6 / 551, -(30 / 551), -(12 / 551)]

def sheetMatrix : Mat3 := !![1, 0, 0; 0, -1, 0; 0, 0, 1]

def chart (x : Vec3) : Vec3 := chartMatrix *ᵥ x
def recover (y : Vec3) : Vec3 := inverseMatrix *ᵥ y
def phase (x : Vec3) : ℝ := 9 * x 0

/-- The full declared sector system, before evaluating its six invariants. -/
def sectorRules (b p q h6 o8 t : ℝ) (x : Vec3) : Vec3 :=
  ![2 * x 0 - p * x 1 + b * q * x 2,
    q * x 1 - p ^ 2 / 2 * x 2,
    x 0 - p * b * x 1 - (o8 - h6) / t * x 2]

theorem sector_rules_evaluate (x : Vec3) :
    sectorRules 4 5 7 6 8 3 x = chart x := by
  ext i
  fin_cases i <;>
    simp [sectorRules, chart, chartMatrix, Matrix.mulVec, dotProduct,
      Fin.sum_univ_succ] <;> ring

theorem chart_det : chartMatrix.det = -(3857 / 6 : ℝ) := by
  rw [Matrix.det_fin_three]
  change (2 : ℝ) * 7 * (-(2 / 3)) - 2 * (-(25 / 2)) * (-20) -
    (-5) * 0 * (-(2 / 3)) + (-5) * (-(25 / 2)) * 1 +
    28 * 0 * (-20) - 28 * 7 * 1 = -(3857 / 6)
  norm_num

theorem inverse_mul_chart : inverseMatrix * chartMatrix = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [inverseMatrix, chartMatrix, Matrix.mul_apply, Fin.sum_univ_succ]

theorem chart_mul_inverse : chartMatrix * inverseMatrix = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [inverseMatrix, chartMatrix, Matrix.mul_apply, Fin.sum_univ_succ]

theorem recover_chart (x : Vec3) : recover (chart x) = x := by
  simp [recover, chart, Matrix.mulVec_mulVec, inverse_mul_chart]

theorem chart_recover (y : Vec3) : chart (recover y) = y := by
  simp [recover, chart, Matrix.mulVec_mulVec, chart_mul_inverse]

theorem chart_injective : Function.Injective chart :=
  Function.LeftInverse.injective recover_chart

theorem recover_injective : Function.Injective recover :=
  Function.LeftInverse.injective chart_recover

theorem recover_coordinates (y : Vec3) :
    recover y =
      ![(1528 * y 0 + 3380 * y 1 + 801 * y 2) / 3857,
        (75 * y 0 + 176 * y 1 - 150 * y 2) / 3857,
        (6 * y 0 - 30 * y 1 - 12 * y 2) / 551] := by
  ext i
  fin_cases i <;>
    simp [recover, inverseMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> ring

theorem phase_linear_check (x : Vec3) :
    3857 * phase x =
      9 * (1528 * chart x 0 + 3380 * chart x 1 + 801 * chart x 2) := by
  simp [phase, chart, chartMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  ring

def sheet (x : Vec3) : Vec3 := sheetMatrix *ᵥ x

theorem sheet_coordinates (x : Vec3) : sheet x = ![x 0, -x 1, x 2] := by
  ext i
  fin_cases i <;> simp [sheet, sheetMatrix, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ]

theorem sheet_involution (x : Vec3) : sheet (sheet x) = x := by
  simp only [sheet_coordinates]
  ext i
  fin_cases i <;> simp

theorem phase_sheet (x : Vec3) : phase (sheet x) = phase x := by
  simp [phase, sheet_coordinates]

def reflectionMatrix : Mat3 := chartMatrix * sheetMatrix * inverseMatrix
def reflection (y : Vec3) : Vec3 := reflectionMatrix *ᵥ y

theorem reflection_explicit : reflectionMatrix =
    !![4607 / 3857, 1760 / 3857, -(1500 / 3857);
       -(150 / 551), 199 / 551, 300 / 551;
       3000 / 3857, 7040 / 3857, -(2143 / 3857)] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [reflectionMatrix, chartMatrix, sheetMatrix, inverseMatrix,
      Matrix.mul_apply, Fin.sum_univ_succ]

theorem reflection_det : reflectionMatrix.det = -1 := by
  have hi : inverseMatrix.det * chartMatrix.det = 1 := by
    rw [← Matrix.det_mul, inverse_mul_chart, Matrix.det_one]
  have hd : sheetMatrix.det = -1 := by
    rw [Matrix.det_fin_three]
    change (1 : ℝ) * (-1) * 1 - 1 * 0 * 0 - 0 * 0 * 1 +
      0 * 0 * 0 + 0 * 0 * 0 - 0 * (-1) * 0 = -1
    norm_num
  simp only [reflectionMatrix, Matrix.det_mul, hd]
  nlinarith

theorem reflection_intertwining :
    reflectionMatrix * chartMatrix = chartMatrix * sheetMatrix := by
  simp [reflectionMatrix, Matrix.mul_assoc, inverse_mul_chart]

theorem reflection_chart (x : Vec3) : reflection (chart x) = chart (sheet x) := by
  simp only [reflection, chart, sheet, Matrix.mulVec_mulVec,
    reflection_intertwining]

theorem reflection_recover (y : Vec3) :
    reflection y = chart (sheet (recover y)) := by
  simp only [reflection, reflectionMatrix, chart, sheet, recover,
    Matrix.mulVec_mulVec, Matrix.mul_assoc]

theorem reflection_involution (y : Vec3) : reflection (reflection y) = y := by
  conv_lhs => arg 1; rw [reflection_recover]
  rw [reflection_chart, sheet_involution, chart_recover]

theorem reflection_squared : reflectionMatrix * reflectionMatrix = 1 := by
  rw [reflection_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.mul_apply, Fin.sum_univ_succ]

def angularMetric : Mat3 := inverseMatrix.transpose * inverseMatrix

theorem sheetMatrix_squared : sheetMatrix * sheetMatrix = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [sheetMatrix, Matrix.mul_apply, Fin.sum_univ_succ]

theorem sheetMatrix_transpose : sheetMatrix.transpose = sheetMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [sheetMatrix]

theorem reflection_preserves_metric :
    reflectionMatrix.transpose * angularMetric * reflectionMatrix = angularMetric := by
  have htrans : chartMatrix.transpose * inverseMatrix.transpose = 1 := by
    rw [← Matrix.transpose_mul, inverse_mul_chart, Matrix.transpose_one]
  unfold reflectionMatrix angularMetric
  rw [Matrix.transpose_mul, Matrix.transpose_mul]
  calc
    (inverseMatrix.transpose * (sheetMatrix.transpose * chartMatrix.transpose)) *
        (inverseMatrix.transpose * inverseMatrix) *
        (chartMatrix * sheetMatrix * inverseMatrix) =
      inverseMatrix.transpose * sheetMatrix.transpose *
        (chartMatrix.transpose * inverseMatrix.transpose) *
        (inverseMatrix * chartMatrix) * sheetMatrix * inverseMatrix := by
          simp only [Matrix.mul_assoc]
    _ = inverseMatrix.transpose * (sheetMatrix * sheetMatrix) * inverseMatrix := by
      rw [htrans, inverse_mul_chart, sheetMatrix_transpose]
      simp only [Matrix.mul_one, Matrix.one_mul, Matrix.mul_assoc]
    _ = inverseMatrix.transpose * inverseMatrix := by
      rw [sheetMatrix_squared, Matrix.mul_one]

theorem metric_quadratic (y : Vec3) :
    y ⬝ᵥ (angularMetric *ᵥ y) =
      (recover y 0) ^ 2 + (recover y 1) ^ 2 + (recover y 2) ^ 2 := by
  simp [angularMetric, recover, inverseMatrix, Matrix.mulVec, Matrix.mul_apply,
    Matrix.transpose_apply, dotProduct, Fin.sum_univ_succ]
  ring

theorem metric_positive (y : Vec3) (hy : y ≠ 0) :
    0 < y ⬝ᵥ (angularMetric *ᵥ y) := by
  rw [metric_quadratic]
  have hn : recover y ≠ 0 := by
    intro h
    apply hy
    calc
      y = chart (recover y) := (chart_recover y).symm
      _ = 0 := by simp [h, chart]
  have h0 := sq_nonneg (recover y 0)
  have h1 := sq_nonneg (recover y 1)
  have h2 := sq_nonneg (recover y 2)
  by_contra h
  have hz0 : recover y 0 = 0 := by nlinarith
  have hz1 : recover y 1 = 0 := by nlinarith
  have hz2 : recover y 2 = 0 := by nlinarith
  apply hn
  ext i
  fin_cases i <;> simp [hz0, hz1, hz2]

theorem angularMetric_posDef : angularMetric.PosDef := by
  constructor
  · ext i j
    simp [angularMetric, Matrix.IsHermitian, Matrix.conjTranspose_apply,
      Matrix.mul_apply, Matrix.transpose_apply, mul_comm]
  · intro y hy
    simpa using metric_positive y hy

def directColumn : Vec3 := ![2, 0, 1]
def sheetColumn : Vec3 := ![-5, 7, -20]
def defectColumn : Vec3 := ![28, -(25 / 2), -(2 / 3)]

theorem chart_decomposition (x : Vec3) :
    chart x = x 0 • directColumn + x 1 • sheetColumn + x 2 • defectColumn := by
  ext i
  fin_cases i <;>
    simp [chart, chartMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_succ,
      directColumn, sheetColumn, defectColumn] <;> ring

theorem even_odd_decomposition (x : Vec3) :
    (1 / 2 : ℝ) • (chart x + chart (sheet x)) =
      x 0 • directColumn + x 2 • defectColumn ∧
    (1 / 2 : ℝ) • (chart x - chart (sheet x)) = x 1 • sheetColumn := by
  constructor <;> ext i <;> fin_cases i <;>
    simp [chart_decomposition, sheet_coordinates, directColumn, sheetColumn,
      defectColumn] <;> ring

#print axioms sector_rules_evaluate
#print axioms chart_det
#print axioms inverse_mul_chart
#print axioms chart_mul_inverse
#print axioms recover_chart
#print axioms chart_recover
#print axioms recover_coordinates
#print axioms phase_linear_check
#print axioms sheet_involution
#print axioms phase_sheet
#print axioms reflection_explicit
#print axioms reflection_det
#print axioms reflection_intertwining
#print axioms reflection_involution
#print axioms reflection_squared
#print axioms reflection_preserves_metric
#print axioms angularMetric_posDef
#print axioms even_odd_decomposition

end

end HMT.II.CKM
