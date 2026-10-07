import SectorIncidenceData

/-!
Exact recovery from a basis of twelve weighted Paley-Witt hexad readings.
The basis is chosen from the encoder image without K or terminal channels.
The inverse is verified by the Lean kernel; it is not an axiom or a
certificate imported as an unproved proposition.

This is an inverse to an incidence reader. It does not assert which weighted
readings the full terminal TPK state produces.
-/
namespace HMT.KWeightedIncidenceRecovery

open HMT.II.CKM.Incidence
open scoped Matrix

set_option maxHeartbeats 12000000
set_option maxRecDepth 12000

def witnesses : Fin 12 → Fin 6 → ZMod 3 :=
  ![![1, 1, 2, 2, 1, 0],
  ![1, 2, 2, 1, 0, 1],
  ![1, 2, 1, 2, 0, 0],
  ![1, 1, 1, 1, 0, 0],
  ![1, 2, 1, 0, 1, 2],
  ![1, 1, 1, 0, 2, 0],
  ![1, 2, 2, 0, 2, 0],
  ![1, 1, 2, 0, 0, 2],
  ![1, 1, 1, 0, 0, 1],
  ![1, 1, 0, 1, 2, 2],
  ![1, 0, 1, 2, 2, 1],
  ![0, 1, 1, 1, 1, 1]]

def support (i : Fin 12) : Finset (Fin 12) := wordSupport (witnesses i)

def incidence : Matrix (Fin 12) (Fin 12) ℚ :=
  fun i j => if j ∈ support i then 1 else 0

def checkedIncidence : Matrix (Fin 12) (Fin 12) ℚ :=
  ![![1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
  ![1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0],
  ![1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0],
  ![1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
  ![1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0],
  ![1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
  ![1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0],
  ![1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
  ![1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
  ![1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0],
  ![1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
  ![0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]

theorem incidence_from_encoder : incidence = checkedIncidence := by
  decide +kernel

theorem every_row_is_hexad : ∀ i : Fin 12, (support i).card = 6 := by
  decide +kernel

theorem every_row_in_encoder_image (i : Fin 12) :
    ∃ w : Fin 6 → ZMod 3, wordSupport w = support i :=
  ⟨witnesses i, rfl⟩

def inverseNumerator : Matrix (Fin 12) (Fin 12) ℚ :=
  ![![7, 1, 8, -7, 7, -1, -4, 8, -7, 3, 3, -15],
  ![7, 7, -4, -1, 1, -7, 8, 8, -7, 3, -15, 3],
  ![1, 7, 8, -7, 7, -7, 8, -4, -1, -15, 3, 3],
  ![1, 1, 2, 5, -5, -1, -4, -4, -1, 3, 3, 3],
  ![1, -5, -4, -1, 1, 5, 2, -4, -1, 3, 3, 3],
  ![-5, 1, -4, -1, 1, -1, -4, 2, 5, 3, 3, 3],
  ![-5, -11, 2, 5, -5, 11, -10, 2, 5, 3, 3, 3],
  ![-5, -5, -10, 11, -11, 5, 2, 2, 5, 3, 3, 3],
  ![-11, -5, 2, 5, -5, 5, 2, -10, 11, 3, 3, 3],
  ![-11, -11, -4, 17, 1, 11, -10, -10, 11, 3, 3, 3],
  ![-11, 1, -10, 11, -11, 17, -4, -10, 11, 3, 3, 3],
  ![1, -11, -10, 11, -11, 11, -10, -4, 17, 3, 3, 3]]

def inverse : Matrix (Fin 12) (Fin 12) ℚ :=
  fun i j => inverseNumerator i j / 18

theorem inverse_left : inverse * incidence = 1 := by
  rw [incidence_from_encoder]
  decide +kernel

theorem inverse_right : incidence * inverse = 1 := by
  rw [incidence_from_encoder]
  decide +kernel

def read (v : Fin 12 → ℚ) : Fin 12 → ℚ := incidence *ᵥ v
def recover (y : Fin 12 → ℚ) : Fin 12 → ℚ := inverse *ᵥ y

theorem recover_read (v : Fin 12 → ℚ) : recover (read v) = v := by
  unfold recover read
  rw [Matrix.mulVec_mulVec, inverse_left, Matrix.one_mulVec]

theorem read_recover (y : Fin 12 → ℚ) : read (recover y) = y := by
  unfold recover read
  rw [Matrix.mulVec_mulVec, inverse_right, Matrix.one_mulVec]

theorem read_injective : Function.Injective read := by
  intro u v h
  have h' := congrArg recover h
  simpa only [recover_read] using h'

theorem read_eq_iff (u v : Fin 12 → ℚ) : read u = read v ↔ u = v :=
  ⟨fun h => read_injective h, congrArg read⟩

theorem read_as_sum (v : Fin 12 → ℚ) (i : Fin 12) :
    read v i = ∑ j ∈ support i, v j := by
  simp [read, Matrix.mulVec, dotProduct, incidence, Finset.sum_ite_irrel]

/-- Equality on all weighted hexads implies equality of all twelve components.
Only encoder-image hexads are used, not arbitrary six-element subsets. -/
theorem full_hexad_reading_injective (u v : Fin 12 → ℚ)
    (h : ∀ w : Fin 6 → ZMod 3, (wordSupport w).card = 6 →
      (∑ j ∈ wordSupport w, u j) = ∑ j ∈ wordSupport w, v j) :
    u = v := by
  apply read_injective
  funext i
  rw [read_as_sum, read_as_sum]
  exact h (witnesses i) (every_row_is_hexad i)

theorem unique_recovered_register (y : Fin 12 → ℚ) :
    ∃! v : Fin 12 → ℚ, read v = y := by
  refine ⟨recover y, read_recover y, ?_⟩
  intro v hv
  apply read_injective
  rw [hv, read_recover]

#print axioms incidence_from_encoder
#print axioms every_row_is_hexad
#print axioms every_row_in_encoder_image
#print axioms inverse_left
#print axioms inverse_right
#print axioms recover_read
#print axioms read_recover
#print axioms read_injective
#print axioms read_eq_iff
#print axioms read_as_sum
#print axioms full_hexad_reading_injective
#print axioms unique_recovered_register

end HMT.KWeightedIncidenceRecovery
