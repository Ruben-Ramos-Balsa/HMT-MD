import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
Finite-dimensional analytic consequences of a centred, already generated reader.
The hypothesis `sum h = 0` is explicit: this file does not formalize its HMT
generation, the exceptional incidence, Mellin theory, or an RH/CH conclusion.
-/

noncomputable section
open scoped BigOperators
namespace FlujoReciproco

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def flow (h : ι → ℝ) (t : ℝ) : Matrix ι ι ℝ :=
  Matrix.diagonal (fun i => Real.exp (t * h i))

omit [Fintype ι] in
theorem flow_positive (h : ι → ℝ) (t : ℝ) (i : ι) :
    0 < flow h t i i := by
  simpa [flow] using Real.exp_pos (t * h i)

theorem flow_add (h : ι → ℝ) (s t : ℝ) :
    flow h s * flow h t = flow h (s + t) := by
  simp only [flow, Matrix.diagonal_mul_diagonal]
  ext i j
  simp [add_mul, Real.exp_add]

omit [Fintype ι] in
theorem flow_zero (h : ι → ℝ) : flow h 0 = 1 := by
  simp [flow]

theorem flow_inverse (h : ι → ℝ) (t : ℝ) :
    flow h t * flow h (-t) = 1 := by
  rw [flow_add]
  simp [flow_zero]

theorem flow_det (h : ι → ℝ) (t : ℝ) :
    Matrix.det (flow h t) = Real.exp (t * ∑ i, h i) := by
  rw [flow, Matrix.det_diagonal]
  rw [Finset.mul_sum, Real.exp_sum]

theorem flow_det_one (h : ι → ℝ) (hs : ∑ i, h i = 0) (t : ℝ) :
    Matrix.det (flow h t) = 1 := by
  rw [flow_det, hs]
  simp

def liftReader (h : Fin 12 → ℝ) : Fin 12 × Fin 2 → ℝ := fun i => h i.1

theorem liftReader_sum (h : Fin 12 → ℝ) (hs : ∑ i, h i = 0) :
    ∑ i, liftReader h i = 0 := by
  simp [liftReader, Fintype.sum_prod_type, Fin.sum_univ_two,
    ← Finset.sum_add_distrib, ← Finset.mul_sum, hs]

theorem lifted_det_one (h : Fin 12 → ℝ) (hs : ∑ i, h i = 0) (t : ℝ) :
    Matrix.det (flow (liftReader h) t) = 1 :=
  flow_det_one _ (liftReader_sum h hs) _

theorem lifted_inverse (h : Fin 12 → ℝ) (t : ℝ) :
    flow (liftReader h) t * flow (liftReader h) (-t) = 1 :=
  flow_inverse _ _

/-- The repeated scalar on each two-dimensional block commutes with any
    operator supported on those blocks. No orthogonality assumption is needed. -/
theorem lifted_commutes (h : Fin 12 → ℝ) (t : ℝ)
    (B : Matrix (Fin 12 × Fin 2) (Fin 12 × Fin 2) ℝ)
    (block : ∀ i j, i.1 ≠ j.1 → B i j = 0) :
    flow (liftReader h) t * B = B * flow (liftReader h) t := by
  ext i j
  simp only [flow, Matrix.diagonal_mul, Matrix.mul_diagonal, liftReader]
  by_cases hij : i.1 = j.1
  · rw [hij, mul_comm]
  · rw [block i j hij]
    simp

#print axioms flow_add
#print axioms flow_inverse
#print axioms flow_det_one
#print axioms lifted_det_one
#print axioms lifted_inverse
#print axioms lifted_commutes

end FlujoReciproco
