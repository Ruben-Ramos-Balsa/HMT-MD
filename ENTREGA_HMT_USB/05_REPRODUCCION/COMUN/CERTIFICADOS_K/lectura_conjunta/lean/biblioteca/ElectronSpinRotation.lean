import ElectronSpin
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
The spinorial rotation of Article I, helicidad_electron.tex, eq:el-retorno-spin.
The Hermitian directional operator is inherited from the electronic two-sheet
block. Its involution law for a unit direction is proved in ElectronSpin.

This file verifies the explicit trigonometric transport, the composition and
adjoint laws, unitarity, and the two-pi/four-pi returns. It does not assert a new
construction of the upstream principal plane or an equality with a separately
defined matrix-exponential API.
-/

noncomputable section
open Matrix

namespace HMT.I.ElectronSpinRotation

open ElectronSpin

def rotation (n : Fin 3 → ℝ) (theta : ℝ) : MatC :=
  (Real.cos (theta / 2) : ℂ) • (1 : MatC) +
    (-Complex.I * (Real.sin (theta / 2) : ℂ)) • H n

theorem explicit_formula (n : Fin 3 → ℝ) (theta : ℝ) :
    rotation n theta = (Real.cos (theta / 2) : ℂ) • (1 : MatC) -
      (Complex.I * (Real.sin (theta / 2) : ℂ)) • H n := by
  simp [rotation, neg_mul, neg_smul, sub_eq_add_neg]

theorem two_term_product (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) (a b c d : ℂ) :
    (a • (1 : MatC) + b • H n) * (c • (1 : MatC) + d • H n) =
      (a*c+b*d) • (1 : MatC) + (a*d+b*c) • H n := by
  simp only [add_mul, mul_add, Matrix.smul_mul, Matrix.mul_smul,
    one_mul, mul_one, H_unit_square n hn]
  ext i j
  simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

theorem zero_angle (n : Fin 3 → ℝ) : rotation n 0 = 1 := by
  simp [rotation]

theorem composition (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) (a b : ℝ) :
    rotation n (a+b) = rotation n a * rotation n b := by
  unfold rotation
  rw [two_term_product n hn, show (a+b)/2 = a/2+b/2 by ring,
    Real.cos_add, Real.sin_add]
  push_cast
  ext i j
  simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring_nf
  simp [Complex.I_sq]
  ring

theorem adjoint (n : Fin 3 → ℝ) (theta : ℝ) :
    (rotation n theta).conjTranspose = rotation n (-theta) := by
  simp only [rotation, Matrix.conjTranspose_add, Matrix.conjTranspose_smul,
    Matrix.conjTranspose_one, (H_hermitian n).eq, neg_div,
    Real.cos_neg, Real.sin_neg, Complex.ofReal_neg]
  simp only [Complex.star_def, map_neg, map_mul, Complex.conj_ofReal,
    Complex.conj_I, neg_neg, mul_neg, neg_mul]

theorem unitary (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) (theta : ℝ) :
    (rotation n theta).conjTranspose * rotation n theta = 1 ∧
      rotation n theta * (rotation n theta).conjTranspose = 1 := by
  rw [adjoint, ← composition n hn, ← composition n hn]
  simp [zero_angle]

theorem two_pi_return (n : Fin 3 → ℝ) : rotation n (2 * Real.pi) = -1 := by
  simp [rotation, show 2 * Real.pi / 2 = Real.pi by ring]

theorem four_pi_return (n : Fin 3 → ℝ) : rotation n (4 * Real.pi) = 1 := by
  simp [rotation, show 4 * Real.pi / 2 = 2 * Real.pi by ring,
    Real.cos_two_pi, Real.sin_two_pi]

theorem two_pi_vector (n : Fin 3 → ℝ) (v : Fin 2 → ℂ) :
    rotation n (2 * Real.pi) *ᵥ v = -v := by
  rw [two_pi_return]
  rw [Matrix.neg_mulVec, Matrix.one_mulVec]

theorem four_pi_vector (n : Fin 3 → ℝ) (v : Fin 2 → ℂ) :
    rotation n (4 * Real.pi) *ᵥ v = v := by
  rw [four_pi_return, Matrix.one_mulVec]

theorem inverse_angle (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) (theta : ℝ) :
    rotation n (-theta) * rotation n theta = 1 ∧
      rotation n theta * rotation n (-theta) = 1 := by
  simpa only [adjoint] using unitary n hn theta

theorem direction_reversal (n : Fin 3 → ℝ) (theta : ℝ) :
    rotation (-n) theta = rotation n (-theta) := by
  simp [rotation, H_neg, neg_div, Real.cos_neg, Real.sin_neg,
    smul_neg, neg_mul, neg_smul]

end HMT.I.ElectronSpinRotation
end

#print axioms HMT.I.ElectronSpinRotation.explicit_formula
#print axioms HMT.I.ElectronSpinRotation.two_term_product
#print axioms HMT.I.ElectronSpinRotation.zero_angle
#print axioms HMT.I.ElectronSpinRotation.composition
#print axioms HMT.I.ElectronSpinRotation.adjoint
#print axioms HMT.I.ElectronSpinRotation.unitary
#print axioms HMT.I.ElectronSpinRotation.two_pi_return
#print axioms HMT.I.ElectronSpinRotation.four_pi_return
#print axioms HMT.I.ElectronSpinRotation.two_pi_vector
#print axioms HMT.I.ElectronSpinRotation.four_pi_vector
#print axioms HMT.I.ElectronSpinRotation.inverse_angle
#print axioms HMT.I.ElectronSpinRotation.direction_reversal
