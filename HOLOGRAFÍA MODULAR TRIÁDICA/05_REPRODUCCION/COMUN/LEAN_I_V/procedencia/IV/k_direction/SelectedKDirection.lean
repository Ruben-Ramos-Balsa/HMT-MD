import SharedArticleIBase
import SelectedRegionalIncidence
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Data.Matrix.Mul
import Mathlib.Tactic

/-!
Concrete direction recovered from the selected HMT register, not an input
used to select it. P3 is the exact Q(sqrt(5)) table of projector_three in the
delivered variacional.py. verify_p3_table.py checks the character-sum/table
provenance separately; this file does not claim a Lean character-sum theorem.
The real Euclidean chart is a downstream realization of that finite record.
-/

noncomputable section
open scoped BigOperators Matrix

namespace HMT.IV.SelectedKDirection

set_option maxHeartbeats 3000000

abbrev E := EuclideanSpace ℝ (Fin 12)

/-- Real coordinate reader of the existing selected register. -/
def selectedK : E := WithLp.toLp 2
  (fun i : Fin 12 => (HMT.Shared.ArticleI.register.digits[i.val]! : ℝ))

theorem selectedK_coordinates :
    selectedK = WithLp.toLp 2
      (![234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601] : Fin 12 → ℝ) := by
  ext i
  change (HMT.I.TerminalSelector.regionalRegister.digits[i.val]! : ℝ) = _
  rw [HMT.I.SelectedRegionalIncidence.regional_register_digits]
  fin_cases i <;> norm_num

/-- Twenty times P3, in the ordered A5/C5 chart of the source certificate. -/
def P3Numerator (s : ℝ) : Matrix (Fin 12) (Fin 12) ℝ := ![
  ![5, -s, s, -5, -s, s, -s, s, -s, s, -s, s],
  ![-s, 5, -5, s, s, s, -s, -s, -s, -s, s, s],
  ![s, -5, 5, -s, -s, -s, s, s, s, s, -s, -s],
  ![-5, s, -s, 5, s, -s, s, -s, s, -s, s, -s],
  ![-s, s, -s, s, 5, s, -s, -5, s, s, -s, -s],
  ![s, s, -s, -s, s, 5, -5, -s, -s, s, -s, s],
  ![-s, -s, s, s, -s, -5, 5, s, s, -s, s, -s],
  ![s, -s, s, -s, -5, -s, s, 5, -s, -s, s, s],
  ![-s, -s, s, s, s, -s, s, -s, 5, s, -s, -5],
  ![s, -s, s, -s, s, s, -s, -s, s, 5, -5, -s],
  ![-s, s, -s, s, -s, -s, s, s, -s, -5, 5, s],
  ![s, s, -s, -s, -s, s, -s, s, -5, -s, s, 5]]

def P3 : Matrix (Fin 12) (Fin 12) ℝ :=
  fun i j => P3Numerator (Real.sqrt 5) i j / 20

/-- I - J/12, only its coordinate formula; geometric projection is downstream. -/
def P11Matrix : Matrix (Fin 12) (Fin 12) ℝ :=
  fun i j => (if i = j then 1 else 0) - 1 / 12

def meanZeroK : E := WithLp.toLp 2
  (fun i => selectedK i - (∑ j, selectedK j) / 12)

/-- The direction is computed from P3 applied to the mean-zero selected K. -/
def uK : E := WithLp.toLp 2 (P3.mulVec meanZeroK)

theorem selectedK_sum : ∑ i, selectedK i = 6263 := by
  rw [selectedK_coordinates]
  norm_num [Fin.sum_univ_succ]

theorem meanZeroK_eq_P11 :
    meanZeroK = WithLp.toLp 2 (P11Matrix.mulVec selectedK) := by
  ext i
  simp [meanZeroK, P11Matrix, Matrix.mulVec, dotProduct, sub_mul,
    Finset.sum_sub_distrib, ← Finset.mul_sum, div_eq_mul_inv, mul_comm]

theorem meanZeroK_apply (i : Fin 12) :
    meanZeroK i = selectedK i - 6263 / 12 := by
  simp [meanZeroK, selectedK_sum]

theorem uK_eq_P3_P11_K :
    uK = WithLp.toLp 2 (P3.mulVec (P11Matrix.mulVec selectedK)) := by
  rw [uK, meanZeroK_eq_P11]
  rfl

/-- Explicit evaluated coordinates, all retained in Q(sqrt(5)). -/
def directionCoordinates : Fin 12 → ℝ :=
  let s := Real.sqrt 5
  ![(-2475 - 466*s)/20, (2015 + 338*s)/20,
    (-2015 - 338*s)/20, (2475 + 466*s)/20,
    (3005 + 2062*s)/20, (1015 + 844*s)/20,
    (-1015 - 844*s)/20, (-3005 - 2062*s)/20,
    (1565 + 1138*s)/20, (3240 + 219*s)/20,
    (-3240 - 219*s)/20, (-1565 - 1138*s)/20]

theorem uK_coordinates : uK = WithLp.toLp 2 directionCoordinates := by
  ext i
  fin_cases i <;>
    simp [uK, P3, P3Numerator, meanZeroK_apply, selectedK_coordinates,
      Matrix.mulVec, dotProduct, Fin.sum_univ_succ, directionCoordinates] <;> ring

theorem sum_uK : ∑ i, uK i = 0 := by
  rw [uK_coordinates]
  simp [directionCoordinates, Fin.sum_univ_succ]
  ring

theorem inner_ones_uK :
    inner ℝ (WithLp.toLp 2 (fun _ : Fin 12 => (1 : ℝ))) uK = 0 := by
  rw [uK_coordinates, EuclideanSpace.inner_toLp_toLp]
  simpa [uK_coordinates, dotProduct] using sum_uK

theorem norm_sq_uK :
    ‖uK‖ ^ 2 = (6638585 + 2275584 * Real.sqrt 5) / 20 := by
  rw [← real_inner_self_eq_norm_sq, uK_coordinates, EuclideanSpace.inner_toLp_toLp]
  simp [dotProduct, directionCoordinates, Fin.sum_univ_succ]
  have hs : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  nlinarith [hs]

theorem norm_sq_uK_pos : 0 < ‖uK‖ ^ 2 := by
  rw [norm_sq_uK]
  positivity

theorem uK_ne_zero : uK ≠ 0 := by
  intro h
  simpa [h] using norm_sq_uK_pos

end HMT.IV.SelectedKDirection

#print axioms HMT.IV.SelectedKDirection.uK_eq_P3_P11_K
#print axioms HMT.IV.SelectedKDirection.norm_sq_uK
#print axioms HMT.IV.SelectedKDirection.uK_ne_zero
