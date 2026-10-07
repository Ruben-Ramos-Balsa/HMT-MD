import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Analysis.Complex.Basic
import Mathlib.Tactic

/-!
# Explicit local electronic block and its spinorial realization

Source: article I, electron.tex, proposition “Álgebra del bloque electrónico
local”, and helicidad_electron.tex. The principal-plane selection is upstream
of this local realization. Here P and Q are the displayed matrices, not
abstract operators assumed to satisfy the desired relations.
-/

noncomputable section
open Matrix

namespace ElectronSpin

abbrev MatR := Matrix (Fin 2) (Fin 2) ℝ
abbrev MatC := Matrix (Fin 2) (Fin 2) ℂ

def P : MatR := !![1, 0; 0, 0]
def Q : MatR := !![1 / 4, Real.sqrt 3 / 4; Real.sqrt 3 / 4, 3 / 4]
def commutator {R : Type*} [Ring R] (A B : Matrix (Fin 2) (Fin 2) R) := A * B - B * A
def S : MatR := (2 : ℝ) • P - 1
def J : MatR := (4 / Real.sqrt 3 : ℝ) • commutator P Q
def nilPlus : MatR := (1 / 2 : ℝ) • (S + J)
def nilMinus : MatR := (1 / 2 : ℝ) • (S - J)

theorem sqrt_three_nonzero : Real.sqrt 3 ≠ 0 := by positivity

theorem P_idempotent : P * P = P := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [P, Matrix.mul_apply, Fin.sum_univ_two]

theorem Q_idempotent : Q * Q = Q := by
  have hs := Real.sq_sqrt (show (0 : ℝ) ≤ 3 by norm_num)
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Q, Matrix.mul_apply, Fin.sum_univ_two] <;> nlinarith

theorem P_symmetric : P.transpose = P := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem Q_symmetric : Q.transpose = Q := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem commutator_explicit : commutator P Q =
    !![0, Real.sqrt 3 / 4; -(Real.sqrt 3 / 4), 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [commutator, P, Q, Matrix.mul_apply, Fin.sum_univ_two]

theorem S_explicit : S = !![1, 0; 0, -1] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [S, P]

theorem J_explicit : J = !![0, 1; -1, 0] := by
  rw [J, commutator_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [sqrt_three_nonzero, Matrix.smul_apply, smul_eq_mul]

theorem S_square : S * S = 1 := by
  rw [S_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]

theorem J_square : J * J = -1 := by
  rw [J_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]

theorem SJ_anticommute : S * J = -(J * S) := by
  rw [S_explicit, J_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]

theorem S_symmetric : S.transpose = S := by
  rw [S_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem J_skew_symmetric : J.transpose = -J := by
  rw [J_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num

theorem nilPlus_square : nilPlus * nilPlus = 0 := by
  unfold nilPlus
  rw [S_explicit, J_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]

theorem nilMinus_square : nilMinus * nilMinus = 0 := by
  unfold nilMinus
  rw [S_explicit, J_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]

theorem nil_pairing : nilPlus * nilMinus + nilMinus * nilPlus = 1 := by
  unfold nilPlus nilMinus
  rw [S_explicit, J_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]

/-- Explicit spanning formula, with coefficients recovered from the entries. -/
theorem real_matrix_decomposition (A : MatR) :
    A = ((A 0 0 + A 1 1) / 2) • (1 : MatR) +
      ((A 0 0 - A 1 1) / 2) • S + ((A 0 1 - A 1 0) / 2) • J +
      ((A 0 1 + A 1 0) / 2) • (S * J) := by
  rw [S_explicit, J_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem real_coefficients_unique (a b c d : ℝ)
    (h : a • (1 : MatR) + b • S + c • J + d • (S * J) = 0) :
    a = 0 ∧ b = 0 ∧ c = 0 ∧ d = 0 := by
  rw [S_explicit, J_explicit] at h
  have h00 := congrArg (fun A : MatR => A 0 0) h
  have h01 := congrArg (fun A : MatR => A 0 1) h
  have h10 := congrArg (fun A : MatR => A 1 0) h
  have h11 := congrArg (fun A : MatR => A 1 1) h
  norm_num [Matrix.mul_apply, Fin.sum_univ_two] at h00 h01 h10 h11
  constructor
  · linarith
  constructor
  · linarith
  constructor <;> linarith

/-- Entrywise complexification preserves the real block; scalar I is not J. -/
def complexify (A : MatR) : MatC := A.map Complex.ofReal
def Sc : MatC := complexify S
def Jc : MatC := complexify J
def sigma : Fin 3 → MatC := ![Sc * Jc, (-Complex.I) • Jc, Sc]

theorem Sc_explicit : Sc = !![1, 0; 0, -1] := by
  simp only [Sc, complexify, S_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.map_apply]

theorem Jc_explicit : Jc = !![0, 1; -1, 0] := by
  simp only [Jc, complexify, J_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.map_apply]

theorem sigma_zero : sigma 0 = !![0, 1; 1, 0] := by
  simp only [sigma, Matrix.cons_val_zero, Sc_explicit, Jc_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]

theorem sigma_one : sigma 1 = !![0, -Complex.I; Complex.I, 0] := by
  simp only [sigma, Matrix.cons_val_one, Jc_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num

theorem sigma_two : sigma 2 = !![1, 0; 0, -1] := by
  simpa only [sigma, Matrix.cons_val, Fin.reduceFinMk] using Sc_explicit

theorem sigma_hermitian (a : Fin 3) : (sigma a).IsHermitian := by
  fin_cases a
  all_goals
    unfold Matrix.IsHermitian
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [sigma, Sc_explicit, Jc_explicit, Matrix.conjTranspose_apply,
        Matrix.mul_apply, Fin.sum_univ_two]

theorem sigma_trace (a : Fin 3) : Matrix.trace (sigma a) = 0 := by
  fin_cases a <;> simp [sigma_zero, sigma_one, sigma_two, Matrix.trace, Fin.sum_univ_two]

theorem sigma_square (a : Fin 3) : sigma a * sigma a = 1 := by
  fin_cases a
  all_goals
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [sigma, Sc_explicit, Jc_explicit, Matrix.mul_apply,
        Fin.sum_univ_two, Complex.I_sq]

theorem sigma_cyclic_products :
    sigma 0 * sigma 1 = Complex.I • sigma 2 ∧
    sigma 1 * sigma 2 = Complex.I • sigma 0 ∧
    sigma 2 * sigma 0 = Complex.I • sigma 1 := by
  simp only [sigma_zero, sigma_one, sigma_two]
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]
  constructor <;> (ext i j; fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.mul_apply, Fin.sum_univ_two])

theorem sigma_anticommute (a b : Fin 3) (hab : a ≠ b) :
    sigma a * sigma b = -(sigma b * sigma a) := by
  fin_cases a <;> fin_cases b <;> try contradiction
  all_goals
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [sigma, Sc_explicit, Jc_explicit, Matrix.mul_apply, Fin.sum_univ_two]

def H (n : Fin 3 → ℝ) : MatC :=
  (n 0 : ℂ) • sigma 0 + (n 1 : ℂ) • sigma 1 + (n 2 : ℂ) • sigma 2

theorem H_explicit (n : Fin 3 → ℝ) :
    H n = !![(n 2 : ℂ), (n 0 : ℂ) - Complex.I * n 1;
      (n 0 : ℂ) + Complex.I * n 1, -(n 2 : ℂ)] := by
  simp only [H, sigma_zero, sigma_one, sigma_two]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num <;> ring

theorem H_square (n : Fin 3 → ℝ) :
    H n * H n = ((n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 : ℝ) : ℂ) • (1 : MatC) := by
  rw [H_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;>
    norm_num [Matrix.mul_apply, Fin.sum_univ_two, pow_two,
      Complex.mul_re, Complex.mul_im] <;> ring

theorem H_unit_square (n : Fin 3 → ℝ) (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    H n * H n = 1 := by rw [H_square, hn]; simp

theorem H_hermitian (n : Fin 3 → ℝ) : (H n).IsHermitian := by
  unfold Matrix.IsHermitian
  rw [H_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.conjTranspose_apply]
  ring

theorem H_trace (n : Fin 3 → ℝ) : Matrix.trace (H n) = 0 := by
  rw [H_explicit]
  simp [Matrix.trace, Fin.sum_univ_two]

theorem H_neg (n : Fin 3 → ℝ) : H (-n) = -H n := by
  rw [H_explicit, H_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;> simp <;> ring

def helicity (n : Fin 3 → ℝ) : MatC := (1 / 2 : ℂ) • H n
def projectorPlus (n : Fin 3 → ℝ) : MatC := (1 / 2 : ℂ) • (1 + H n)
def projectorMinus (n : Fin 3 → ℝ) : MatC := (1 / 2 : ℂ) • (1 - H n)

theorem projectors_sum (n : Fin 3 → ℝ) : projectorPlus n + projectorMinus n = 1 := by
  ext i j
  simp only [projectorPlus, projectorMinus, Matrix.smul_apply, smul_eq_mul,
    Matrix.add_apply, Matrix.sub_apply]
  ring

theorem projectorPlus_idempotent (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    projectorPlus n * projectorPlus n = projectorPlus n := by
  simp only [projectorPlus, Matrix.smul_mul, Matrix.mul_smul,
    mul_add, add_mul, one_mul, mul_one, H_unit_square n hn]
  ext i j
  simp only [Matrix.smul_apply, smul_eq_mul, Matrix.add_apply]
  ring

theorem projectorMinus_idempotent (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    projectorMinus n * projectorMinus n = projectorMinus n := by
  simp only [projectorMinus, Matrix.smul_mul, Matrix.mul_smul,
    mul_sub, sub_mul, one_mul, mul_one, H_unit_square n hn]
  ext i j
  simp only [Matrix.smul_apply, smul_eq_mul, Matrix.sub_apply]
  ring

theorem projectors_orthogonal (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    projectorPlus n * projectorMinus n = 0 ∧ projectorMinus n * projectorPlus n = 0 := by
  constructor <;>
    simp only [projectorPlus, projectorMinus, Matrix.smul_mul, Matrix.mul_smul,
      mul_sub, sub_mul, mul_add, add_mul, one_mul, mul_one, H_unit_square n hn]
  all_goals
    ext i j
    simp only [Matrix.smul_apply, smul_eq_mul, Matrix.sub_apply, Matrix.add_apply,
      Matrix.zero_apply]
    ring

theorem projectorPlus_hermitian (n : Fin 3 → ℝ) : (projectorPlus n).IsHermitian := by
  simp [Matrix.IsHermitian, projectorPlus, Matrix.conjTranspose_add,
    (H_hermitian n).eq]

theorem projectorMinus_hermitian (n : Fin 3 → ℝ) : (projectorMinus n).IsHermitian := by
  simp [Matrix.IsHermitian, projectorMinus, Matrix.conjTranspose_sub,
    (H_hermitian n).eq]

theorem projectorPlus_trace (n : Fin 3 → ℝ) : Matrix.trace (projectorPlus n) = 1 := by
  simp [projectorPlus, Matrix.trace_smul, Matrix.trace_add, Matrix.trace_one, H_trace]

theorem projectorMinus_trace (n : Fin 3 → ℝ) : Matrix.trace (projectorMinus n) = 1 := by
  simp [projectorMinus, Matrix.trace_smul, Matrix.trace_sub, Matrix.trace_one, H_trace]

theorem projectorPlus_nonzero (n : Fin 3 → ℝ) : projectorPlus n ≠ 0 := by
  intro h
  have ht := projectorPlus_trace n
  rw [h, Matrix.trace_zero] at ht
  norm_num at ht

theorem projectorMinus_nonzero (n : Fin 3 → ℝ) : projectorMinus n ≠ 0 := by
  intro h
  have ht := projectorMinus_trace n
  rw [h, Matrix.trace_zero] at ht
  norm_num at ht

theorem helicity_plus (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    helicity n * projectorPlus n = (1 / 2 : ℂ) • projectorPlus n := by
  simp only [helicity, projectorPlus, Matrix.smul_mul, Matrix.mul_smul,
    mul_add, mul_one, H_unit_square n hn]
  ext i j
  simp only [Matrix.smul_apply, smul_eq_mul, Matrix.add_apply]
  ring

theorem helicity_minus (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    helicity n * projectorMinus n = (-1 / 2 : ℂ) • projectorMinus n := by
  simp only [helicity, projectorMinus, Matrix.smul_mul, Matrix.mul_smul,
    mul_sub, mul_one, H_unit_square n hn]
  ext i j
  simp only [Matrix.smul_apply, smul_eq_mul, Matrix.sub_apply]
  ring

theorem projectors_direction_reversal (n : Fin 3 → ℝ) :
    projectorPlus (-n) = projectorMinus n ∧ projectorMinus (-n) = projectorPlus n := by
  simp [projectorPlus, projectorMinus, H_neg, sub_eq_add_neg]

theorem scalar_commutes (z : ℂ) (A : MatC) : (z • (1 : MatC)) * A = A * (z • (1 : MatC)) := by
  simp [Matrix.smul_mul, Matrix.mul_smul]

theorem spinor_decomposition (n : Fin 3 → ℝ) (v : Fin 2 → ℂ) :
    projectorPlus n *ᵥ v + projectorMinus n *ᵥ v = v := by
  rw [← Matrix.add_mulVec, projectors_sum, Matrix.one_mulVec]

theorem helicity_plus_vector (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) (v : Fin 2 → ℂ) :
    helicity n *ᵥ (projectorPlus n *ᵥ v) = (1 / 2 : ℂ) • (projectorPlus n *ᵥ v) := by
  rw [Matrix.mulVec_mulVec, helicity_plus n hn, Matrix.smul_mulVec_assoc]

theorem helicity_minus_vector (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) (v : Fin 2 → ℂ) :
    helicity n *ᵥ (projectorMinus n *ᵥ v) = (-1 / 2 : ℂ) • (projectorMinus n *ᵥ v) := by
  rw [Matrix.mulVec_mulVec, helicity_minus n hn, Matrix.smul_mulVec_assoc]

theorem projector_images_intersection (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) (v : Fin 2 → ℂ)
    (hp : projectorPlus n *ᵥ v = v) (hm : projectorMinus n *ᵥ v = v) : v = 0 := by
  calc
    v = projectorPlus n *ᵥ v := hp.symm
    _ = projectorPlus n *ᵥ (projectorMinus n *ᵥ v) := congrArg _ hm.symm
    _ = (projectorPlus n * projectorMinus n) *ᵥ v := Matrix.mulVec_mulVec _ _ _
    _ = 0 := by rw [(projectors_orthogonal n hn).1, Matrix.zero_mulVec]

theorem nonzero_matrix_has_nonzero_action (A : MatC) (hA : A ≠ 0) :
    ∃ v : Fin 2 → ℂ, A *ᵥ v ≠ 0 := by
  by_contra! h
  apply hA
  apply Matrix.ext_of_mulVec_single
  intro i
  rw [h, Matrix.zero_mulVec]

theorem exists_plus_eigenvector (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    ∃ v : Fin 2 → ℂ, v ≠ 0 ∧ helicity n *ᵥ v = (1 / 2 : ℂ) • v := by
  obtain ⟨v, hv⟩ := nonzero_matrix_has_nonzero_action _ (projectorPlus_nonzero n)
  exact ⟨projectorPlus n *ᵥ v, hv, helicity_plus_vector n hn v⟩

theorem exists_minus_eigenvector (n : Fin 3 → ℝ)
    (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    ∃ v : Fin 2 → ℂ, v ≠ 0 ∧ helicity n *ᵥ v = (-1 / 2 : ℂ) • v := by
  obtain ⟨v, hv⟩ := nonzero_matrix_has_nonzero_action _ (projectorMinus_nonzero n)
  exact ⟨projectorMinus n *ᵥ v, hv, helicity_minus_vector n hn v⟩

end ElectronSpin
end

#print axioms ElectronSpin.sqrt_three_nonzero
#print axioms ElectronSpin.P_idempotent
#print axioms ElectronSpin.Q_idempotent
#print axioms ElectronSpin.P_symmetric
#print axioms ElectronSpin.Q_symmetric
#print axioms ElectronSpin.commutator_explicit
#print axioms ElectronSpin.S_explicit
#print axioms ElectronSpin.J_explicit
#print axioms ElectronSpin.S_square
#print axioms ElectronSpin.J_square
#print axioms ElectronSpin.SJ_anticommute
#print axioms ElectronSpin.S_symmetric
#print axioms ElectronSpin.J_skew_symmetric
#print axioms ElectronSpin.nilPlus_square
#print axioms ElectronSpin.nilMinus_square
#print axioms ElectronSpin.nil_pairing
#print axioms ElectronSpin.real_matrix_decomposition
#print axioms ElectronSpin.real_coefficients_unique
#print axioms ElectronSpin.Sc_explicit
#print axioms ElectronSpin.Jc_explicit
#print axioms ElectronSpin.sigma_zero
#print axioms ElectronSpin.sigma_one
#print axioms ElectronSpin.sigma_two
#print axioms ElectronSpin.sigma_hermitian
#print axioms ElectronSpin.sigma_trace
#print axioms ElectronSpin.sigma_square
#print axioms ElectronSpin.sigma_cyclic_products
#print axioms ElectronSpin.sigma_anticommute
#print axioms ElectronSpin.H_explicit
#print axioms ElectronSpin.H_square
#print axioms ElectronSpin.H_unit_square
#print axioms ElectronSpin.H_hermitian
#print axioms ElectronSpin.H_trace
#print axioms ElectronSpin.H_neg
#print axioms ElectronSpin.projectors_sum
#print axioms ElectronSpin.projectorPlus_idempotent
#print axioms ElectronSpin.projectorMinus_idempotent
#print axioms ElectronSpin.projectors_orthogonal
#print axioms ElectronSpin.projectorPlus_hermitian
#print axioms ElectronSpin.projectorMinus_hermitian
#print axioms ElectronSpin.projectorPlus_trace
#print axioms ElectronSpin.projectorMinus_trace
#print axioms ElectronSpin.projectorPlus_nonzero
#print axioms ElectronSpin.projectorMinus_nonzero
#print axioms ElectronSpin.helicity_plus
#print axioms ElectronSpin.helicity_minus
#print axioms ElectronSpin.projectors_direction_reversal
#print axioms ElectronSpin.scalar_commutes
#print axioms ElectronSpin.spinor_decomposition
#print axioms ElectronSpin.helicity_plus_vector
#print axioms ElectronSpin.helicity_minus_vector
#print axioms ElectronSpin.projector_images_intersection
#print axioms ElectronSpin.nonzero_matrix_has_nonzero_action
#print axioms ElectronSpin.exists_plus_eigenvector
#print axioms ElectronSpin.exists_minus_eigenvector
