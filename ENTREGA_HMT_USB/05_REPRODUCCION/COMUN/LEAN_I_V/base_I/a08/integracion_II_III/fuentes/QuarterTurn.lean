import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-! The oriented real plane, its fourth-order action, and the actual bilateral
resolvent. The twelve-coordinate embedding retains the fixed marked basis. -/

noncomputable section

namespace HMT.III.OrientedMoment

abbrev Plane := ℝ × ℝ

def quarter : Plane →ₗ[ℝ] Plane where
  toFun x := (-x.2, x.1)
  map_add' x y := by ext <;> simp [add_comm]
  map_smul' c x := by ext <;> simp

@[simp] theorem quarter_apply (x : Plane) : quarter x = (-x.2, x.1) := rfl

theorem quarter_sq (x : Plane) : quarter (quarter x) = -x := by ext <;> simp

theorem quarter_four (x : Plane) : quarter (quarter (quarter (quarter x))) = x := by
  ext <;> simp

def twelveEmbed (x : Plane) (j : Fin 12) : ℝ :=
  if j.val % 4 = 0 then x.1 else if j.val % 4 = 1 then x.2
  else if j.val % 4 = 2 then -x.1 else -x.2

def cycle12 (v : Fin 12 → ℝ) (j : Fin 12) : ℝ := v (j - 1)

theorem cycle_intertwines (x : Plane) : cycle12 (twelveEmbed x) = twelveEmbed (quarter x) := by
  funext j
  fin_cases j <;> simp [cycle12, twelveEmbed]

theorem twelveEmbed_injective : Function.Injective twelveEmbed := by
  intro x y h
  have h0 := congrFun h (0 : Fin 12)
  have h1 := congrFun h (1 : Fin 12)
  apply Prod.ext <;> simpa [twelveEmbed] using (by assumption)

def resolvent (s : ℝ) : Plane →ₗ[ℝ] Plane :=
  (1 / (1 + s ^ 2)) • (LinearMap.id + s • quarter)

theorem resolvent_formula (s : ℝ) (x : Plane) :
    resolvent s x = ((x.1 - s * x.2) / (1 + s ^ 2), (s * x.1 + x.2) / (1 + s ^ 2)) := by
  ext <;> simp [resolvent, smul_eq_mul] <;> ring

theorem resolvent_left (s : ℝ) (x : Plane) :
    resolvent s (x - s • quarter x) = x := by
  rw [resolvent_formula]
  ext <;> simp [smul_eq_mul] <;> field_simp <;> ring

theorem resolvent_right (s : ℝ) (x : Plane) :
    resolvent s x - s • quarter (resolvent s x) = x := by
  rw [resolvent_formula]
  have hd : 1 + s ^ 2 ≠ 0 := ne_of_gt (by positivity : 0 < 1 + s ^ 2)
  ext <;> simp [smul_eq_mul] <;> field_simp [hd] <;> ring

def kernel (s : ℝ) : ℝ := s / (1 + s ^ 2)

theorem oriented_coefficient (s : ℝ) : (resolvent s (1, 0)).2 = kernel s := by
  rw [resolvent_formula]
  simp [kernel]

theorem reversed_coefficient (s : ℝ) : (resolvent (-s) (1, 0)).2 = -kernel s := by
  rw [oriented_coefficient]
  simp [kernel, neg_div]

def pencilMatrix (s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![1, s; -s, 1]

theorem pencil_determinant (s : ℝ) : (pencilMatrix s).det = 1 + s ^ 2 := by
  simp [pencilMatrix, Matrix.det_fin_two]
  ring

theorem reversed_determinant (s : ℝ) : (pencilMatrix (-s)).det = (pencilMatrix s).det := by
  rw [pencil_determinant, pencil_determinant]
  ring

#print axioms cycle_intertwines
#print axioms quarter_sq
#print axioms resolvent_left
#print axioms resolvent_right
#print axioms oriented_coefficient
#print axioms reversed_coefficient
#print axioms reversed_determinant

end HMT.III.OrientedMoment
