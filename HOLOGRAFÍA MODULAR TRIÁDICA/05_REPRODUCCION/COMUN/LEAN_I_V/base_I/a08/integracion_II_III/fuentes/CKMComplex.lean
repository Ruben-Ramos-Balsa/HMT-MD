import Mathlib

/-!
# Complex realization of the generated CKM angular reader

This file formalizes the downstream complex realization in manuscript II,
sections `08_propagacion_angular.tex` and `08d_conjugacion_amplitudes.tex`.
The real angles are the published output of the preceding angular reader;
this file does not choose its coefficients or inject measured CKM values.
-/

noncomputable section
open Complex Matrix
open scoped ComplexConjugate

namespace HMT.CKM.ComplexRealization

abbrev M3 := Matrix (Fin 3) (Fin 3) ℂ

def phase (δ : ℝ) : ℂ := (Real.cos δ : ℂ) + (Real.sin δ : ℂ) * I

@[simp] theorem phase_re (δ : ℝ) : (phase δ).re = Real.cos δ := by
  simp [phase, -Complex.ofReal_cos, -Complex.ofReal_sin]

@[simp] theorem phase_im (δ : ℝ) : (phase δ).im = Real.sin δ := by
  simp [phase, -Complex.ofReal_cos, -Complex.ofReal_sin]

theorem phase_exp (δ : ℝ) : phase δ = Complex.exp ((δ : ℂ) * I) := by
  rw [Complex.exp_mul_I]
  simp [phase]

@[simp] theorem phase_neg (δ : ℝ) : phase (-δ) = conj (phase δ) := by
  apply Complex.ext <;> simp [phase, -Complex.ofReal_cos, -Complex.ofReal_sin]

@[simp] theorem phase_mul_conj (δ : ℝ) : phase δ * conj (phase δ) = 1 := by
  apply Complex.ext
  · simp [phase, mul_re, mul_im, -Complex.ofReal_cos, -Complex.ofReal_sin]
    nlinarith [Real.sin_sq_add_cos_sq δ]
  · simp [phase, mul_re, mul_im, -Complex.ofReal_cos, -Complex.ofReal_sin]
    ring

@[simp] theorem conj_mul_phase (δ : ℝ) : conj (phase δ) * phase δ = 1 := by
  rw [mul_comm, phase_mul_conj]

def R12 (θ : ℝ) : M3 :=
  !![(Real.cos θ : ℂ), Real.sin θ, 0;
     -(Real.sin θ : ℂ), Real.cos θ, 0;
     0, 0, 1]

def U13 (θ δ : ℝ) : M3 :=
  !![(Real.cos θ : ℂ), 0, (Real.sin θ : ℂ) * conj (phase δ);
     0, 1, 0;
     -(Real.sin θ : ℂ) * phase δ, 0, Real.cos θ]

def R23 (θ : ℝ) : M3 :=
  !![1, 0, 0;
     0, (Real.cos θ : ℂ), Real.sin θ;
     0, -(Real.sin θ : ℂ), Real.cos θ]

theorem trig_circle (θ : ℝ) : (Real.cos θ : ℂ)^2 + (Real.sin θ : ℂ)^2 = 1 := by
  exact_mod_cast Real.cos_sq_add_sin_sq θ

theorem R12_left_unitary (θ : ℝ) : (R12 θ)ᴴ * R12 θ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [R12, Matrix.mul_apply, Fin.sum_univ_succ, Matrix.conjTranspose_apply,
      -Complex.ofReal_cos, -Complex.ofReal_sin]
  all_goals first | (solve | ring) | (convert trig_circle θ using 1; ring)

theorem R12_right_unitary (θ : ℝ) : R12 θ * (R12 θ)ᴴ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [R12, Matrix.mul_apply, Fin.sum_univ_succ, Matrix.conjTranspose_apply,
      -Complex.ofReal_cos, -Complex.ofReal_sin]
  all_goals first | (solve | ring) | (convert trig_circle θ using 1; ring)

theorem R23_left_unitary (θ : ℝ) : (R23 θ)ᴴ * R23 θ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [R23, Matrix.mul_apply, Fin.sum_univ_succ, Matrix.conjTranspose_apply,
      -Complex.ofReal_cos, -Complex.ofReal_sin]
  all_goals first | (solve | ring) | (convert trig_circle θ using 1; ring)

theorem R23_right_unitary (θ : ℝ) : R23 θ * (R23 θ)ᴴ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [R23, Matrix.mul_apply, Fin.sum_univ_succ, Matrix.conjTranspose_apply,
      -Complex.ofReal_cos, -Complex.ofReal_sin]
  all_goals first | (solve | ring) | (convert trig_circle θ using 1; ring)

theorem U13_left_unitary (θ δ : ℝ) : (U13 θ δ)ᴴ * U13 θ δ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [U13, Matrix.mul_apply, Fin.sum_univ_succ, Matrix.conjTranspose_apply,
      -Complex.ofReal_cos, -Complex.ofReal_sin]
  all_goals first | (solve | ring) |
    (calc
      _ = (Real.cos θ : ℂ)^2 + (Real.sin θ : ℂ)^2 *
        (phase δ * conj (phase δ)) := by ring
      _ = 1 := by rw [phase_mul_conj, mul_one, trig_circle])

theorem U13_right_unitary (θ δ : ℝ) : U13 θ δ * (U13 θ δ)ᴴ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [U13, Matrix.mul_apply, Fin.sum_univ_succ, Matrix.conjTranspose_apply,
      -Complex.ofReal_cos, -Complex.ofReal_sin]
  all_goals first | (solve | ring) |
    (calc
      _ = (Real.cos θ : ℂ)^2 + (Real.sin θ : ℂ)^2 *
        (phase δ * conj (phase δ)) := by ring
      _ = 1 := by rw [phase_mul_conj, mul_one, trig_circle])

def CKM (a b c δ : ℝ) : M3 := R23 b * U13 c δ * R12 a

theorem CKM_left_unitary (a b c δ : ℝ) : (CKM a b c δ)ᴴ * CKM a b c δ = 1 := by
  simp only [CKM, Matrix.conjTranspose_mul]
  calc
    _ = (R12 a)ᴴ * ((U13 c δ)ᴴ * ((R23 b)ᴴ * R23 b) * U13 c δ) * R12 a := by
      simp only [Matrix.mul_assoc]
    _ = 1 := by simp [R23_left_unitary, U13_left_unitary, R12_left_unitary]

theorem CKM_right_unitary (a b c δ : ℝ) : CKM a b c δ * (CKM a b c δ)ᴴ = 1 := by
  simp only [CKM, Matrix.conjTranspose_mul]
  calc
    _ = R23 b * (U13 c δ * (R12 a * (R12 a)ᴴ) * (U13 c δ)ᴴ) * (R23 b)ᴴ := by
      simp only [Matrix.mul_assoc]
    _ = 1 := by simp [R23_right_unitary, U13_right_unitary, R12_right_unitary]

theorem CKM_entries (a b c δ : ℝ) : CKM a b c δ =
  !![(Real.cos a : ℂ) * Real.cos c,
     (Real.sin a : ℂ) * Real.cos c,
     (Real.sin c : ℂ) * conj (phase δ);
     -(Real.sin a : ℂ) * Real.cos b - (Real.cos a : ℂ) * Real.sin b * Real.sin c * phase δ,
     (Real.cos a : ℂ) * Real.cos b - (Real.sin a : ℂ) * Real.sin b * Real.sin c * phase δ,
     (Real.sin b : ℂ) * Real.cos c;
     (Real.sin a : ℂ) * Real.sin b - (Real.cos a : ℂ) * Real.cos b * Real.sin c * phase δ,
     -(Real.cos a : ℂ) * Real.sin b - (Real.sin a : ℂ) * Real.cos b * Real.sin c * phase δ,
     (Real.cos b : ℂ) * Real.cos c] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [CKM, R12, R23, U13, Matrix.mul_apply, Fin.sum_univ_succ,
      -Complex.ofReal_cos, -Complex.ofReal_sin] <;> ring

def conjugate (V : M3) : M3 := fun i j => conj (V i j)

theorem CKM_neg_phase (a b c δ : ℝ) : CKM a b c (-δ) = conjugate (CKM a b c δ) := by
  rw [CKM_entries, CKM_entries]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [conjugate, -Complex.ofReal_cos, -Complex.ofReal_sin]

def quartet (V : M3) : ℂ := V 0 0 * V 1 1 * conj (V 0 1) * conj (V 1 0)

def jarlskog (V : M3) : ℝ := (quartet V).im

theorem CKM_jarlskog (a b c δ : ℝ) : jarlskog (CKM a b c δ) =
    Real.cos a * Real.cos b * (Real.cos c)^2 * Real.sin a * Real.sin b * Real.sin c * Real.sin δ := by
  calc
    _ = (Real.cos a * Real.cos b * (Real.cos c)^2 * Real.sin a * Real.sin b * Real.sin c * Real.sin δ) *
      ((Real.cos a)^2 + (Real.sin a)^2) := by
      rw [CKM_entries]
      simp [jarlskog, quartet, phase, Complex.mul_re, Complex.mul_im,
        -Complex.ofReal_cos, -Complex.ofReal_sin,
        -Real.cos_sq_add_sin_sq, -Real.sin_sq_add_cos_sq]
      ring
    _ = _ := by rw [Real.cos_sq_add_sin_sq, mul_one]

theorem quartet_conjugate (V : M3) : quartet (conjugate V) = conj (quartet V) := by
  simp [quartet, conjugate]

theorem jarlskog_conjugate (V : M3) : jarlskog (conjugate V) = -jarlskog V := by
  simp [jarlskog, quartet_conjugate]

theorem CKM_jarlskog_neg_phase (a b c δ : ℝ) :
    jarlskog (CKM a b c (-δ)) = -jarlskog (CKM a b c δ) := by
  rw [CKM_neg_phase, jarlskog_conjugate]

def rephase (u d : Fin 3 → ℂ) (V : M3) : M3 := Matrix.diagonal u * V * Matrix.diagonal d

theorem rephase_apply (u d : Fin 3 → ℂ) (V : M3) (i j : Fin 3) :
    rephase u d V i j = u i * V i j * d j := by
  simp [rephase, Matrix.diagonal_mul, Matrix.mul_diagonal]

theorem quartet_rephase (u d : Fin 3 → ℂ) (V : M3)
    (hu : ∀ i, u i * conj (u i) = 1) (hd : ∀ i, d i * conj (d i) = 1) :
    quartet (rephase u d V) = quartet V := by
  calc
    _ = (u 0 * conj (u 0)) * (u 1 * conj (u 1)) *
      (d 0 * conj (d 0)) * (d 1 * conj (d 1)) * quartet V := by
      simp only [quartet, rephase_apply, map_mul]
      ring
    _ = _ := by rw [hu, hu, hd, hd]; ring

theorem jarlskog_rephase (u d : Fin 3 → ℂ) (V : M3)
    (hu : ∀ i, u i * conj (u i) = 1) (hd : ∀ i, d i * conj (d i) = 1) :
    jarlskog (rephase u d V) = jarlskog V := by
  rw [jarlskog, quartet_rephase u d V hu hd]
  rfl

theorem jarlskog_phase_rephase (u d : Fin 3 → ℝ) (V : M3) :
    jarlskog (rephase (phase ∘ u) (phase ∘ d) V) = jarlskog V := by
  apply jarlskog_rephase <;> intro i <;> simp

theorem CKM_mem_unitary (a b c δ : ℝ) : CKM a b c δ ∈ unitary M3 := by
  exact ⟨CKM_left_unitary a b c δ, CKM_right_unitary a b c δ⟩

theorem CKM_jarlskog_nonzero (a b c δ : ℝ)
    (haC : Real.cos a ≠ 0) (hbC : Real.cos b ≠ 0) (hcC : Real.cos c ≠ 0)
    (haS : Real.sin a ≠ 0) (hbS : Real.sin b ≠ 0) (hcS : Real.sin c ≠ 0)
    (hδ : Real.sin δ ≠ 0) : jarlskog (CKM a b c δ) ≠ 0 := by
  rw [CKM_jarlskog]
  exact mul_ne_zero (mul_ne_zero (mul_ne_zero (mul_ne_zero
    (mul_ne_zero (mul_ne_zero haC hbC) (pow_ne_zero 2 hcC)) haS) hbS) hcS) hδ

theorem jarlskog_real (V : M3) (hV : ∀ i j, (V i j).im = 0) : jarlskog V = 0 := by
  simp [jarlskog, quartet, Complex.mul_im, Complex.mul_re, hV]

theorem nonzero_jarlskog_obstructs_real_rephasing (V : M3)
    (hJ : jarlskog V ≠ 0) (u d : Fin 3 → ℂ)
    (hu : ∀ i, u i * conj (u i) = 1) (hd : ∀ i, d i * conj (d i) = 1) :
    ¬ (∀ i j, (rephase u d V i j).im = 0) := by
  intro hreal
  have hz := jarlskog_real (rephase u d V) hreal
  rw [jarlskog_rephase u d V hu hd] at hz
  exact hJ hz

#print axioms phase_exp
#print axioms phase_mul_conj
#print axioms CKM_left_unitary
#print axioms CKM_right_unitary
#print axioms CKM_mem_unitary
#print axioms CKM_entries
#print axioms CKM_neg_phase
#print axioms CKM_jarlskog
#print axioms CKM_jarlskog_nonzero
#print axioms quartet_rephase
#print axioms jarlskog_rephase
#print axioms jarlskog_conjugate
#print axioms CKM_jarlskog_neg_phase
#print axioms nonzero_jarlskog_obstructs_real_rephasing

end HMT.CKM.ComplexRealization
