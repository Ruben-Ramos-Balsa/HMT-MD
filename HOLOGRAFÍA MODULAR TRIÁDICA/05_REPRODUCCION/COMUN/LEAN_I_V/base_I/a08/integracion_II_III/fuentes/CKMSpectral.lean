import Mathlib

/-!
Post-publication spectral transport for the HMT CKM reader.
The angular and mass readers are already constructed upstream. This module
does not select their values; it proves exact algebraic invariants of their
complex realization, with arbitrary spectra and no metrological inputs.
-/

noncomputable section
open Matrix Complex

namespace HMT.CKM.Spectral

abbrev Mat3 := Matrix (Fin 3) (Fin 3) ℂ

def commutator (A B : Mat3) : Mat3 := A * B - B * A

theorem diagonal_commutator_entry (a : Fin 3 → ℂ) (B : Mat3)
    (i j : Fin 3) :
    commutator (diagonal a) B i j = (a i - a j) * B i j := by
  simp [commutator, diagonal_mul, mul_diagonal, sub_mul]
  ring

theorem diagonal_commutator_det (a : Fin 3 → ℂ) (B : Mat3) :
    (commutator (diagonal a) B).det =
      (a 0 - a 1) * (a 1 - a 2) * (a 2 - a 0) *
        (B 0 1 * B 1 2 * B 2 0 - B 0 2 * B 2 1 * B 1 0) := by
  rw [Matrix.det_fin_three]
  simp only [diagonal_commutator_entry]
  ring

theorem hermitian_cycle_conjugate (B : Mat3) (hB : B.IsHermitian) :
    B 0 2 * B 2 1 * B 1 0 = star (B 0 1 * B 1 2 * B 2 0) := by
  simp only [StarMul.star_mul, hB.apply]
  ring

theorem hermitian_commutator_det (a : Fin 3 → ℝ) (B : Mat3)
    (hB : B.IsHermitian) :
    (commutator (diagonal (fun i => (a i : ℂ))) B).det =
      2 * I * ((a 0 - a 1) * (a 1 - a 2) * (a 2 - a 0) : ℝ) *
        (B 0 1 * B 1 2 * B 2 0).im := by
  rw [diagonal_commutator_det, hermitian_cycle_conjugate B hB]
  apply Complex.ext
  all_goals simp only [Complex.mul_re, Complex.mul_im, Complex.sub_re, Complex.sub_im,
      Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im,
      Complex.star_def, Complex.conj_re, Complex.conj_im]
  all_goals norm_num
  all_goals ring

theorem unitary_transport_spectrum (V : unitary Mat3) (B : Mat3) :
    spectrum ℂ ((V : Mat3) * B * star (V : Mat3)) = spectrum ℂ B := by
  exact unitary.spectrum.unitary_conjugate

theorem unitary_transport_hermitian (V : Mat3) (B : Mat3)
    (hB : B.IsHermitian) : (V * B * V.conjTranspose).IsHermitian := by
  unfold Matrix.IsHermitian at *
  simp only [conjTranspose_mul, conjTranspose_conjTranspose, hB]
  first | rfl | exact (Matrix.mul_assoc _ _ _).symm

theorem inverse_transport_charpoly (V W B : Mat3) (hVW : V * W = 1) :
    (V * B * W).charpoly = B.charpoly := by
  apply Polynomial.funext
  intro t
  rw [Matrix.eval_charpoly, Matrix.eval_charpoly]
  have hscalar : Matrix.scalar (Fin 3) t - V * B * W =
      V * (Matrix.scalar (Fin 3) t - B) * W := by
    simp only [mul_sub, sub_mul]
    have ht : V * Matrix.scalar (Fin 3) t * W = Matrix.scalar (Fin 3) t := by
      calc
        V * Matrix.scalar (Fin 3) t * W = (t • V) * W := by
          congr 1
          ext i j
          simp [Matrix.scalar_apply, Matrix.mul_diagonal, mul_comm]
        _ = t • (V * W) := by rw [Matrix.smul_mul]
        _ = (Matrix.diagonal (fun _ : Fin 3 => t)) := by rw [hVW]; ext i j; simp [Matrix.one_apply, Matrix.diagonal_apply]
    rw [ht]
  rw [hscalar, Matrix.det_mul, Matrix.det_mul]
  have hdet : V.det * W.det = 1 := by
    rw [← Matrix.det_mul, hVW, Matrix.det_one]
  calc
    V.det * (Matrix.scalar (Fin 3) t - B).det * W.det =
        (V.det * W.det) * (Matrix.scalar (Fin 3) t - B).det := by ring
    _ = _ := by rw [hdet, one_mul]

#print axioms diagonal_commutator_entry
#print axioms diagonal_commutator_det
#print axioms hermitian_cycle_conjugate
#print axioms hermitian_commutator_det
#print axioms unitary_transport_spectrum
#print axioms unitary_transport_hermitian
#print axioms inverse_transport_charpoly

end HMT.CKM.Spectral
