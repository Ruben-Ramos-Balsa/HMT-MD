import APPArithmetic
import TRITCore
import TPKTransport
import ModalIncidence

/- Explicit compatibility maps between the checked local constructions.
   This file does not replace the yet separate full-state cylinder selector.
   In particular, observable transport is not renamed the entire TPK. -/
namespace CommonComposition

def appTrit (i j : APPArithmetic.Digit) :
    (TRITCore.Digit × Int) × (TRITCore.Digit × Int) :=
  let a := APPArithmetic.evaluate i j
  (TRITCore.balanced (APPArithmetic.decode a.additive),
   TRITCore.balanced (APPArithmetic.decode a.multiplicative))

theorem app_trit_additive (i j : APPArithmetic.Digit) :
    TRITCore.reconstruct (appTrit i j).1 = (APPArithmetic.sumEval i j : Int) := by
  unfold appTrit
  rw [TRITCore.reconstruct_balanced, (APPArithmetic.paired_reconstruction i j).1]

theorem app_trit_multiplicative (i j : APPArithmetic.Digit) :
    TRITCore.reconstruct (appTrit i j).2 = (APPArithmetic.productEval i j : Int) := by
  unfold appTrit
  rw [TRITCore.reconstruct_balanced, (APPArithmetic.paired_reconstruction i j).2]

theorem modal_selector_same (n : Int) : ModalIncidence.phase n = TRITCore.phase n := rfl

theorem additive_selector_matches : ∀ p : TPKTransport.Phase,
    TPKTransport.active .additive p = decide (TRITCore.phase (p.val + 1) = 1) := by
  decide

theorem multiplicative_selector_matches : ∀ p : TPKTransport.Phase,
    TPKTransport.active .multiplicative p = decide (TRITCore.phase (p.val + 1) = -1) := by
  decide

theorem neutral_selector_matches : ∀ p : TPKTransport.Phase,
    TRITCore.phase (p.val + 1) = 0 ↔
      TPKTransport.active .additive p = false ∧
      TPKTransport.active .multiplicative p = false := by
  decide

def cursorMark (z : Int) : APPArithmetic.Digit :=
  ⟨(z % 9).toNat, by omega⟩

-- extension.tex uses zero-based cursor indices and positive APP labels i+1.
theorem cursor_positive_chart (z : Int) :
    (APPArithmetic.value (cursorMark z) : Int) = TPKTransport.residue9 (z + 1) := by
  change (((z % 9).toNat + 1 : Nat) : Int) = 1 + (z + 1 - 1) % 9
  have hm : 0 ≤ z % 9 := Int.emod_nonneg z (by decide)
  omega

theorem cursor_mark_periodic (z winding : Int) :
    cursorMark (z + 9 * winding) = cursorMark z := by
  apply Fin.ext
  have h : (z + 9 * winding) % 9 = z % 9 := by omega
  simp [cursorMark, h]

def readCursor (c : TPKTransport.Cursor) : APPArithmetic.PairedEvaluation :=
  APPArithmetic.evaluate (cursorMark c.x) (cursorMark c.y)

def readVisit (q : TPKTransport.ObservableLift) : APPArithmetic.PairedEvaluation :=
  ⟨(readCursor q.plus).additive, (readCursor q.times).multiplicative⟩

def visitTrit (q : TPKTransport.ObservableLift) :
    (TRITCore.Digit × Int) × (TRITCore.Digit × Int) :=
  (TRITCore.balanced (APPArithmetic.decode (readVisit q).additive),
   TRITCore.balanced (APPArithmetic.decode (readVisit q).multiplicative))

theorem visit_additive_reconstruction (q : TPKTransport.ObservableLift) :
    TRITCore.reconstruct (visitTrit q).1 =
      (APPArithmetic.sumEval (cursorMark q.plus.x) (cursorMark q.plus.y) : Int) := by
  unfold visitTrit readVisit readCursor
  rw [TRITCore.reconstruct_balanced, (APPArithmetic.paired_reconstruction _ _).1]

theorem visit_multiplicative_reconstruction (q : TPKTransport.ObservableLift) :
    TRITCore.reconstruct (visitTrit q).2 =
      (APPArithmetic.productEval (cursorMark q.times.x) (cursorMark q.times.y) : Int) := by
  unfold visitTrit readVisit readCursor
  rw [TRITCore.reconstruct_balanced, (APPArithmetic.paired_reconstruction _ _).2]

-- At every chronological depth the same APP/TRIT reading is used.
theorem every_visit_reconstructs (q : TPKTransport.ObservableLift) (n : Nat) :
    let qn := TPKTransport.iterate TPKTransport.step n q
    TRITCore.reconstruct (visitTrit qn).1 =
      (APPArithmetic.sumEval (cursorMark qn.plus.x) (cursorMark qn.plus.y) : Int) ∧
    TRITCore.reconstruct (visitTrit qn).2 =
      (APPArithmetic.productEval (cursorMark qn.times.x) (cursorMark qn.times.y) : Int) := by
  exact ⟨visit_additive_reconstruction _, visit_multiplicative_reconstruction _⟩

#print axioms app_trit_additive
#print axioms app_trit_multiplicative
#print axioms modal_selector_same
#print axioms additive_selector_matches
#print axioms multiplicative_selector_matches
#print axioms neutral_selector_matches
#print axioms cursor_positive_chart
#print axioms cursor_mark_periodic
#print axioms visit_additive_reconstruction
#print axioms visit_multiplicative_reconstruction
#print axioms every_visit_reconstructs

end CommonComposition
