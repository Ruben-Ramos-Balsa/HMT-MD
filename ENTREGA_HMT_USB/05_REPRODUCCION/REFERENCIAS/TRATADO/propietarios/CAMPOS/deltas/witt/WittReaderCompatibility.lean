import RegionalW24

/-!
# Compatibility of the two declared six-coordinate Witt charts

The regional chart A and the terminal-reader chart B are not literally equal.
Their coordinate change fixes 0,1,2 and cycles the last three coordinates.
The total-charge functional is nevertheless the same. This is the algebraic
6×6 compatibility, not a theorem about the terminal reader's loop encoding.
Neither matrix is replaced, and no terminal selection is performed here.
-/

namespace HMT.I.WittReaderCompatibility

open HMT.N69RegionalSignature HMT.I.GeneratedN69Rows

set_option maxHeartbeats 10000000
set_option maxRecDepth 30000

def coordinateChange : Equiv.Perm (Fin 6) where
  toFun := ![0, 1, 2, 4, 5, 3]
  invFun := ![0, 1, 2, 5, 3, 4]
  left_inv := by decide
  right_inv := by decide

def terminalChart (i j : Fin 6) : Nat :=
  (TerminalSelector.wittMatrix[i.val]!)[j.val]!

theorem charts_related (i j : Fin 6) :
    terminalChart i j = wittMatrix (coordinateChange i) (coordinateChange j) := by
  revert i j
  decide

theorem charts_not_literal : terminalChart 1 3 ≠ wittMatrix 1 3 := by decide

theorem chart_row_totals (i : Fin 6) :
    (∑ j : Fin 6, terminalChart i j) = ∑ j : Fin 6, wittMatrix i j := by
  revert i
  decide

def totalImage (chart : Fin 6 → Fin 6 → Nat) (v : Fin 6 → Nat) : Nat :=
  ∑ j : Fin 6, ∑ i : Fin 6, v i * chart i j

theorem totalImage_eq (v : Fin 6 → Nat) :
    totalImage terminalChart v = totalImage wittMatrix v := by
  simp only [totalImage, Finset.sum_comm, ← Finset.mul_sum, chart_row_totals]

theorem charge_eq (v : Fin 6 → Nat) :
    totalImage terminalChart v % 3 = totalImage wittMatrix v % 3 := by
  rw [totalImage_eq]

end HMT.I.WittReaderCompatibility

#print axioms HMT.I.WittReaderCompatibility.charts_related
#print axioms HMT.I.WittReaderCompatibility.charts_not_literal
#print axioms HMT.I.WittReaderCompatibility.chart_row_totals
#print axioms HMT.I.WittReaderCompatibility.totalImage_eq
#print axioms HMT.I.WittReaderCompatibility.charge_eq
