import CKMMassTransport

noncomputable section
open Matrix Complex
open scoped ComplexConjugate
namespace HMT.CKM.Spectral
open HMT.CKM.ComplexRealization

def spectralX (a : ℝ) (m : Fin 3 → ℝ) : ℝ := m 0 * (Real.cos a)^2 + m 1 * (Real.sin a)^2
def spectralY (a : ℝ) (m : Fin 3 → ℝ) : ℝ := m 0 * (Real.sin a)^2 + m 1 * (Real.cos a)^2
def spectralZ (a : ℝ) (m : Fin 3 → ℝ) : ℝ := (m 1 - m 0) * Real.cos a * Real.sin a

theorem massTransport_01 (a b c δ : ℝ) (m : Fin 3 → ℝ) :
    massTransport a b c δ m 0 1 =
      (Real.cos b * Real.cos c * spectralZ a m : ℝ) +
      (Real.sin b * Real.cos c * Real.sin c * (m 2 - spectralX a m) : ℝ) *
        conj (phase δ) := by
  unfold massTransport
  rw [CKM_entries]
  simp [Matrix.mul_apply, Matrix.vecMul, dotProduct, Matrix.conjTranspose_apply, Matrix.diagonal_apply,
    Fin.sum_univ_succ, spectralX, spectralY, spectralZ,
    -Complex.ofReal_cos, -Complex.ofReal_sin]
  ring

theorem massTransport_20 (a b c δ : ℝ) (m : Fin 3 → ℝ) :
    massTransport a b c δ m 2 0 =
      (-Real.sin b * Real.cos c * spectralZ a m : ℝ) +
      (Real.cos b * Real.cos c * Real.sin c * (m 2 - spectralX a m) : ℝ) * phase δ := by
  unfold massTransport
  rw [CKM_entries]
  simp [Matrix.mul_apply, Matrix.vecMul, dotProduct, Matrix.conjTranspose_apply, Matrix.diagonal_apply,
    Fin.sum_univ_succ, spectralX, spectralY, spectralZ,
    -Complex.ofReal_cos, -Complex.ofReal_sin]
  ring

theorem massTransport_12 (a b c δ : ℝ) (m : Fin 3 → ℝ) :
    massTransport a b c δ m 1 2 =
      (Real.cos b * Real.sin b *
        ((Real.sin c)^2 * spectralX a m + (Real.cos c)^2 * m 2 - spectralY a m) : ℝ) -
      ((Real.cos b)^2 * Real.sin c * spectralZ a m : ℝ) * conj (phase δ) +
      ((Real.sin b)^2 * Real.sin c * spectralZ a m : ℝ) * phase δ := by
  unfold massTransport
  rw [CKM_entries]
  simp [Matrix.mul_apply, Matrix.vecMul, dotProduct, Matrix.conjTranspose_apply, Matrix.diagonal_apply,
    Fin.sum_univ_succ, spectralX, spectralY, spectralZ,
    -Complex.ofReal_cos, -Complex.ofReal_sin]
  have hp := phase_mul_conj δ
  linear_combination (Real.cos b : ℂ) * Real.sin b * (Real.sin c)^2 *
    ((m 0 : ℂ) * (Real.cos a)^2 + (m 1 : ℂ) * (Real.sin a)^2) * hp

#print axioms massTransport_01
#print axioms massTransport_20
#print axioms massTransport_12

theorem spectralXY_sum (a : ℝ) (m : Fin 3 → ℝ) :
    spectralX a m + spectralY a m = m 0 + m 1 := by
  calc
    _ = (m 0 + m 1) * ((Real.cos a)^2 + (Real.sin a)^2) := by
      unfold spectralX spectralY; ring
    _ = _ := by rw [Real.cos_sq_add_sin_sq, mul_one]

theorem spectralXY_determinant (a : ℝ) (m : Fin 3 → ℝ) :
    spectralX a m * spectralY a m - (spectralZ a m)^2 = m 0 * m 1 := by
  calc
    _ = (m 0 * m 1) * ((Real.cos a)^2 + (Real.sin a)^2)^2 := by
      unfold spectralX spectralY spectralZ; ring
    _ = _ := by rw [Real.cos_sq_add_sin_sq]; ring

theorem spectral_quadratic_factor (a : ℝ) (m : Fin 3 → ℝ) :
    (m 2 - spectralX a m) * (m 2 - spectralY a m) - (spectralZ a m)^2 =
      (m 2 - m 0) * (m 2 - m 1) := by
  calc
    _ = (m 2)^2 - m 2 * (spectralX a m + spectralY a m) +
      (spectralX a m * spectralY a m - (spectralZ a m)^2) := by ring
    _ = _ := by rw [spectralXY_sum, spectralXY_determinant]; ring

theorem rotated_cycle_im (p q U V z w δ : ℝ) :
    (((p * U : ℝ) + (q * V : ℝ) * conj (phase δ)) *
      ((p * q * w : ℝ) - (p^2 * z : ℝ) * conj (phase δ) + (q^2 * z : ℝ) * phase δ) *
      ((-q * U : ℝ) + (p * V : ℝ) * phase δ) : ℂ).im =
      p * q * (p^2 + q^2) * Real.sin δ * (z * (V^2 - U^2) + U * V * w) := by
  simp [phase, pow_two, Complex.mul_re, Complex.mul_im,
    -Complex.ofReal_cos, -Complex.ofReal_sin,
    -Real.cos_sq_add_sin_sq, -Real.sin_sq_add_cos_sq]
  linear_combination p * q * (p^2 + q^2) * V^2 * z * Real.sin δ *
    (Real.cos_sq_add_sin_sq δ)

#print axioms spectralXY_sum
#print axioms spectralXY_determinant
#print axioms spectral_quadratic_factor
#print axioms rotated_cycle_im

theorem massTransport_cycle_jarlskog (a b c δ : ℝ) (m : Fin 3 → ℝ) :
    (massTransport a b c δ m 0 1 * massTransport a b c δ m 1 2 *
      massTransport a b c δ m 2 0).im =
      jarlskog (CKM a b c δ) * (m 0 - m 1) * (m 1 - m 2) * (m 2 - m 0) := by
  rw [massTransport_01, massTransport_12, massTransport_20]
  have h := rotated_cycle_im (Real.cos b) (Real.sin b)
    (Real.cos c * spectralZ a m)
    (Real.cos c * Real.sin c * (m 2 - spectralX a m))
    (Real.sin c * spectralZ a m)
    ((Real.sin c)^2 * spectralX a m + (Real.cos c)^2 * m 2 - spectralY a m) δ
  rw [Real.cos_sq_add_sin_sq] at h
  calc
    _ = Real.cos b * Real.sin b * 1 * Real.sin δ *
        (Real.sin c * spectralZ a m *
          ((Real.cos c * Real.sin c * (m 2 - spectralX a m))^2 -
            (Real.cos c * spectralZ a m)^2) +
          (Real.cos c * spectralZ a m) *
            (Real.cos c * Real.sin c * (m 2 - spectralX a m)) *
            ((Real.sin c)^2 * spectralX a m + (Real.cos c)^2 * m 2 - spectralY a m)) := by
      convert h using 1
      congr 1
      push_cast
      ring
    _ = Real.cos b * Real.sin b * (Real.cos c)^2 * Real.sin c * spectralZ a m * Real.sin δ *
        ((m 2 - spectralX a m) *
          (((Real.sin c)^2 + (Real.cos c)^2) * m 2 - spectralY a m) -
          (spectralZ a m)^2) := by ring
    _ = Real.cos b * Real.sin b * (Real.cos c)^2 * Real.sin c * spectralZ a m * Real.sin δ *
        ((m 2 - spectralX a m) * (m 2 - spectralY a m) - (spectralZ a m)^2) := by
      rw [Real.sin_sq_add_cos_sq, one_mul]
    _ = _ := by
      rw [spectral_quadratic_factor, CKM_jarlskog]
      unfold spectralZ
      ring

theorem massTransport_jarlskog_determinant (a b c δ : ℝ) (u d : Fin 3 → ℝ) :
    (commutator (diagonal (fun i => (u i : ℂ))) (massTransport a b c δ d)).det =
      2 * I * (jarlskog (CKM a b c δ) *
        ((u 0 - u 1) * (u 1 - u 2) * (u 2 - u 0)) *
        ((d 0 - d 1) * (d 1 - d 2) * (d 2 - d 0)) : ℝ) := by
  rw [massTransport_commutator, massTransport_cycle_jarlskog]
  push_cast
  ring

#print axioms massTransport_cycle_jarlskog
#print axioms massTransport_jarlskog_determinant

theorem massTransport_jarlskog_determinant_norm (a b c δ : ℝ) (u d : Fin 3 → ℝ) :
    ‖(commutator (diagonal (fun i => (u i : ℂ))) (massTransport a b c δ d)).det‖ =
      2 * |jarlskog (CKM a b c δ)| *
        (|u 0 - u 1| * |u 1 - u 2| * |u 2 - u 0|) *
        (|d 0 - d 1| * |d 1 - d 2| * |d 2 - d 0|) := by
  rw [massTransport_jarlskog_determinant]
  rw [norm_mul, norm_mul, Complex.norm_I, Complex.norm_real]
  norm_num only [norm_ofNat, Real.norm_eq_abs]
  simp only [abs_mul]
  ring

theorem massTransport_jarlskog_determinant_ne_zero_iff (a b c δ : ℝ)
    (u d : Fin 3 → ℝ) :
    (commutator (diagonal (fun i => (u i : ℂ))) (massTransport a b c δ d)).det ≠ 0 ↔
      jarlskog (CKM a b c δ) ≠ 0 ∧
      u 0 ≠ u 1 ∧ u 1 ≠ u 2 ∧ u 2 ≠ u 0 ∧
      d 0 ≠ d 1 ∧ d 1 ≠ d 2 ∧ d 2 ≠ d 0 := by
  rw [massTransport_jarlskog_determinant]
  simp only [ne_eq, mul_eq_zero, Complex.ofReal_eq_zero, sub_eq_zero, not_or]
  norm_num
  tauto

#print axioms massTransport_jarlskog_determinant_norm
#print axioms massTransport_jarlskog_determinant_ne_zero_iff
end HMT.CKM.Spectral
