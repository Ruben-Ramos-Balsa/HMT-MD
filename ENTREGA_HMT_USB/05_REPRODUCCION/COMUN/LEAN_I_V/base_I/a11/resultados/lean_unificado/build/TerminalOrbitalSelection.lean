import TerminalInputs
import Mathlib

/-!
Executable finite selection from the published W24, unordered S8, nine-position
functional panel and N69 calendar. All 8! orders are enumerated before selection.
The target register is used only in the statement of the final equality.
This theorem formalizes the finite selector on its declared input domain; it
does not assert that TerminalInputs itself has been generated from APP.
-/
namespace HMT.I.TerminalSelector

def decimalScale : Nat := 10 ^ 36
def cylinderDenominator : Nat := 3 ^ 78

def prefix72From (initial : Nat) (order : List Nat) : Nat :=
  order.foldl (fun acc block => 729 * acc + block) initial

def prefix72 (order : List Nat) : Nat := prefix72From w24Input order

def gridPoints (prefix78 : Nat) : List Nat :=
  let lower := (prefix78 * decimalScale + cylinderDenominator - 1) / cylinderDenominator
  let upperExclusive := ((prefix78 + 1) * decimalScale + cylinderDenominator - 1) /
    cylinderDenominator
  (List.range (upperExclusive - lower)).map (lower + ·)

def indexedCandidatesFrom (initial : Nat) (suffix panel : List Nat) : List Nat :=
  suffix.permutations.flatMap fun order =>
    panel.flatMap fun boundary => gridPoints (729 * prefix72From initial order + boundary)

def indexedCandidates : List Nat := indexedCandidatesFrom w24Input s8Input panelInput

def decimalCandidatesFrom (initial : Nat) (suffix panel : List Nat) : List Nat :=
  let unique : Std.HashSet Nat :=
    (indexedCandidatesFrom initial suffix panel).foldl (fun s n => s.insert n) {}
  unique.toList.mergeSort

def decimalCandidates : List Nat := decimalCandidatesFrom w24Input s8Input panelInput

def highCrown (n : Nat) : List Nat :=
  ((List.range 12).filter fun i => 729 ≤ decimalCoordinate n i).map (· + 1)

def wittCoordinate (word i : Nat) : Nat :=
  if i < 6 then digit6 word i else digit6 (transform6 word) (i - 6)

/-- The exceptional face is read from the two regional words, not from K. -/
def exceptionalFaceFrom (panel : List Nat) : List Nat :=
  ((List.range 12).filter fun i =>
    wittCoordinate (panel.getD 0 0) i != 0 &&
    wittCoordinate (panel.getD 3 0) i != 0).map (· + 1)

def exceptionalFace : List Nat := exceptionalFaceFrom panelInput

def candidatesAtFace : List Nat :=
  decimalCandidates.filter fun n => highCrown n == exceptionalFace

def n69Atlas : Std.HashMap Nat Nat := makeAtlas n69Input

def selectedCandidates : List Nat := candidatesAtFace.filter (heterotypic n69Atlas)

/-- The same selector with explicit interfaces, permitting proved source
constructions to replace finite input tables without changing its rules. -/
def selectFrom (initial : Nat) (suffix panel : List Nat) (rows : Array N69Row) : List Nat :=
  let faceCandidates := (decimalCandidatesFrom initial suffix panel).filter
    fun n => highCrown n == exceptionalFaceFrom panel
  faceCandidates.filter (heterotypic (makeAtlas rows))

theorem selectFrom_published_inputs :
    selectFrom w24Input s8Input panelInput n69Input = selectedCandidates := rfl

theorem n69_rows_valid : n69Input.all validN69Row = true := by
  native_decide

theorem n69_times_are_exact : n69Input.toList.map (·.time) = List.range 100 := by
  native_decide

theorem n69_times_distinct : (n69Input.toList.map (·.time)).Nodup := by
  rw [n69_times_are_exact]
  exact List.nodup_range

theorem all_orders_enumerated : s8Input.permutations.length = 40320 := by
  native_decide

theorem indexed_cylinder_count : indexedCandidates.length = 21902 := by
  native_decide

theorem candidate_count : decimalCandidates.length = 19446 := by
  native_decide

theorem exceptional_face_generated : exceptionalFace = [4, 6, 9, 10] := by
  native_decide

theorem exceptional_face_count : candidatesAtFace.length = 79 := by
  native_decide

theorem terminal_selection :
    selectedCandidates = [234543140729659824621058914794146601] := by
  native_decide

theorem terminal_selection_unique (n : Nat) :
    n ∈ selectedCandidates ↔ n = 234543140729659824621058914794146601 := by
  rw [terminal_selection]
  simp

theorem terminal_coordinates :
    (List.range 12).map (decimalCoordinate 234543140729659824621058914794146601) =
      [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601] := by
  native_decide

end HMT.I.TerminalSelector

#print axioms HMT.I.TerminalSelector.terminal_selection
#print axioms HMT.I.TerminalSelector.terminal_selection_unique
