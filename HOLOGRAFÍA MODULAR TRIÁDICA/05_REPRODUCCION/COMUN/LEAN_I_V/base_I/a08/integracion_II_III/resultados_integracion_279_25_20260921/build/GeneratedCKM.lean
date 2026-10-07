import GeneratedAngularData
import RationalCKMChart
import CKMComplex

/-! The generated regional outputs and action-return coordinates are composed
with the source's sector incidence reader and then its complex realization.
The terminal Jarlskog sign is derived from rational enclosures and trigonometry;
it is not an additional input or an experimental fit. -/
noncomputable section
namespace HMT.II.CKM.Generated
open HMT.IncidenceRegister AlphaIncidencePublications
open HMT.II.ActionReturn
open Matrix
open scoped ComplexConjugate

def mixingDegrees (l : Ledger) : Vec3 := chart (coordinates l)
def radians (d : ℝ) : ℝ := (HMT.II.GeneratedAction.pi / 180) * d
def mixingRadians (l : Ledger) : Vec3 := fun i => radians (mixingDegrees l i)
def phaseRadians (l : Ledger) : ℝ := radians (phaseDegrees l)
def matrix (l : Ledger) : HMT.CKM.ComplexRealization.M3 :=
  HMT.CKM.ComplexRealization.CKM
    (mixingRadians l 0) (mixingRadians l 1) (mixingRadians l 2) (phaseRadians l)

theorem generated_sector_evaluation (l : Ledger) :
    sectorRules 4 5 7 6 8 3 (coordinates l) = mixingDegrees l :=
  sector_rules_evaluate _

theorem mixing_degrees_formula (l : Ledger) :
    mixingDegrees l =
      ![2 * direct l - 5 * (conjugate l / 6) + 28 * torsionDegrees,
        7 * (conjugate l / 6) - (25 / 2) * torsionDegrees,
        direct l - 20 * (conjugate l / 6) - (2 / 3) * torsionDegrees] := by
  ext i
  fin_cases i <;>
    simp [mixingDegrees, chart, chartMatrix, coordinates, Matrix.mulVec,
      dotProduct, Fin.sum_univ_succ] <;> ring

theorem generated_recovery (l : Ledger) :
    recover (mixingDegrees l) = coordinates l := recover_chart _

theorem generated_phase_check (l : Ledger) :
    3857 * phaseDegrees l =
      9 * (1528 * mixingDegrees l 0 + 3380 * mixingDegrees l 1 +
        801 * mixingDegrees l 2) := by
  simpa [phase, phaseDegrees, coordinates, mixingDegrees] using
    phase_linear_check (coordinates l)

theorem generated_mixing_intervals (l : Ledger) (hl : PublishedRegister l) :
    ∀ i, 0 < mixingDegrees l i ∧ mixingDegrees l i < 90 := by
  rcases angular_input_bounds l hl with ⟨ha0, ha1, hu0, hu1, hd0, hd1⟩
  intro i
  rw [mixing_degrees_formula]
  fin_cases i <;> dsimp <;> constructor <;> linarith

theorem radians_chamber {d : ℝ} (hd : 0 < d ∧ d < 90) :
    0 < radians d ∧ radians d < Real.pi / 2 := by
  have hp : HMT.II.GeneratedAction.pi = Real.pi := ClosureAnalytic.value_eq_pi
  have hf : 0 < Real.pi / 180 := div_pos Real.pi_pos (by norm_num)
  unfold radians
  rw [hp]
  refine ⟨mul_pos hf hd.1, ?_⟩
  calc
    _ < (Real.pi / 180) * 90 := mul_lt_mul_of_pos_left hd.2 hf
    _ = Real.pi / 2 := by ring

theorem generated_radian_intervals (l : Ledger) (hl : PublishedRegister l) :
    (∀ i, 0 < mixingRadians l i ∧ mixingRadians l i < Real.pi / 2) ∧
      (0 < phaseRadians l ∧ phaseRadians l < Real.pi / 2) := by
  exact ⟨fun i => radians_chamber (generated_mixing_intervals l hl i),
    radians_chamber (generated_phase_interval l hl)⟩

theorem generated_unitary (l : Ledger) :
    (matrix l)ᴴ * matrix l = 1 ∧ matrix l * (matrix l)ᴴ = 1 :=
  ⟨HMT.CKM.ComplexRealization.CKM_left_unitary _ _ _ _,
    HMT.CKM.ComplexRealization.CKM_right_unitary _ _ _ _⟩

theorem generated_jarlskog (l : Ledger) :
    HMT.CKM.ComplexRealization.jarlskog (matrix l) =
      Real.cos (mixingRadians l 0) * Real.cos (mixingRadians l 1) *
      Real.cos (mixingRadians l 2) ^ 2 * Real.sin (mixingRadians l 0) *
      Real.sin (mixingRadians l 1) * Real.sin (mixingRadians l 2) *
      Real.sin (phaseRadians l) :=
  HMT.CKM.ComplexRealization.CKM_jarlskog _ _ _ _

theorem generated_jarlskog_positive (l : Ledger) (hl : PublishedRegister l) :
    0 < HMT.CKM.ComplexRealization.jarlskog (matrix l) := by
  have h := generated_radian_intervals l hl
  have hs : ∀ i, 0 < Real.sin (mixingRadians l i) := by
    intro i
    apply Real.sin_pos_of_pos_of_lt_pi (h.1 i).1
    linarith [(h.1 i).2, Real.pi_pos]
  have hc : ∀ i, 0 < Real.cos (mixingRadians l i) := by
    intro i
    apply Real.cos_pos_of_mem_Ioo
    constructor
    · linarith [(h.1 i).1, Real.pi_pos]
    · exact (h.1 i).2
  have hd : 0 < Real.sin (phaseRadians l) := by
    apply Real.sin_pos_of_pos_of_lt_pi h.2.1
    linarith [h.2.2, Real.pi_pos]
  rw [generated_jarlskog]
  exact mul_pos (mul_pos (mul_pos (mul_pos (mul_pos
    (mul_pos (hc 0) (hc 1)) (sq_pos_of_pos (hc 2))) (hs 0)) (hs 1)) (hs 2)) hd

/-- The same generated state produces an invertible angular publication, a
unitary mixing matrix, and a strictly positive rephasing-invariant quartet. -/
theorem generated_ckm_chain (l : Ledger) (hl : PublishedRegister l) :
    recover (mixingDegrees l) = coordinates l ∧
      ((matrix l)ᴴ * matrix l = 1 ∧ matrix l * (matrix l)ᴴ = 1) ∧
      0 < HMT.CKM.ComplexRealization.jarlskog (matrix l) :=
  ⟨generated_recovery l, generated_unitary l, generated_jarlskog_positive l hl⟩

/-- The positive quartet of the generated matrix obstructs every row/column
unit-modulus rephasing that would make all entries real. -/
theorem generated_no_real_rephasing (l : Ledger) (hl : PublishedRegister l)
    (u d : Fin 3 → ℂ)
    (hu : ∀ i, u i * conj (u i) = 1)
    (hd : ∀ i, d i * conj (d i) = 1) :
    ¬ (∀ i j, (HMT.CKM.ComplexRealization.rephase u d (matrix l) i j).im = 0) := by
  apply HMT.CKM.ComplexRealization.nonzero_jarlskog_obstructs_real_rephasing
    (matrix l) (ne_of_gt (generated_jarlskog_positive l hl)) u d hu hd

#print axioms generated_sector_evaluation
#print axioms mixing_degrees_formula
#print axioms generated_recovery
#print axioms generated_phase_check
#print axioms generated_mixing_intervals
#print axioms radians_chamber
#print axioms generated_radian_intervals
#print axioms generated_unitary
#print axioms generated_jarlskog
#print axioms generated_jarlskog_positive
#print axioms generated_ckm_chain
#print axioms generated_no_real_rephasing
end HMT.II.CKM.Generated
