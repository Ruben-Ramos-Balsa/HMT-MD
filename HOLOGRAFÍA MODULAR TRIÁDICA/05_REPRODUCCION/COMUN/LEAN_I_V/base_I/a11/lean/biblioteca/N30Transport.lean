import Mathlib
import IncidenceRegister

/-! Prospective N30 transport, matching State/step/walk/rewind in
trazas_dirigidas.py. A direction word is input; no terminal blocks or target
constant select it. The visit reader uses the PREVIOUS sheet at the NEW cell.
This module does not assert PublishedRegister or select the terminal ledger. -/
namespace HMT.N30

structure State where
  row : Fin 9
  column : Fin 9
  sheet : Fin 2
  direction : Fin 4
  phase : Fin 3
  deriving DecidableEq, Repr

def shifted (x : Fin 9) (amount : Nat) : Fin 9 :=
  ⟨(x.val + amount) % 9, Nat.mod_lt _ (by decide)⟩

/-- Directions 0,1,2,3 are N,E,S,W, respectively. -/
def movedRow (s : State) (d : Fin 4) : Fin 9 :=
  if d = 0 then shifted s.row 8 else if d = 2 then shifted s.row 1 else s.row

def movedColumn (s : State) (d : Fin 4) : Fin 9 :=
  if d = 1 then shifted s.column 1 else if d = 3 then shifted s.column 8 else s.column

def rowDelta (d : Fin 4) : Int := if d = 0 then -1 else if d = 2 then 1 else 0
def columnDelta (d : Fin 4) : Int := if d = 1 then 1 else if d = 3 then -1 else 0

theorem movedRow_source_formula (s : State) (d : Fin 4) :
    ((movedRow s d).val : Int) = ((s.row.val : Int) + rowDelta d) % 9 := by
  have h := s.row.isLt
  fin_cases d <;> simp [movedRow, shifted, rowDelta] <;> omega

theorem movedColumn_source_formula (s : State) (d : Fin 4) :
    ((movedColumn s d).val : Int) = ((s.column.val : Int) + columnDelta d) % 9 := by
  have h := s.column.isLt
  fin_cases d <;> simp [movedColumn, shifted, columnDelta] <;> omega

def rawRead (sheet : Fin 2) (i j : Fin 9) : Nat :=
  if sheet = 0 then APPArithmetic.sumEval i j else APPArithmetic.productEval i j

def updatedSheet (old : Fin 2) (trit : Nat) : Fin 2 :=
  if trit = 1 then 0 else if trit = 2 then 1 else old

def advancePhase (phase : Fin 3) : Fin 3 :=
  ⟨(phase.val + 1) % 3, Nat.mod_lt _ (by decide)⟩

structure Edge where
  before : State
  after : State
  raw : Nat
  digit : Nat
  quotient9 : Nat
  tritResidue : Nat
  turn : Nat
  sheetChange : Nat
  deriving DecidableEq, Repr

def step (s : State) (d : Fin 4) : Edge :=
  let i := movedRow s d
  let j := movedColumn s d
  let raw := rawRead s.sheet i j
  let digit := APPArithmetic.rho9 raw
  let trit := digit % 3
  let sheet := updatedSheet s.sheet trit
  { before := s
    after := ⟨i, j, sheet, d, advancePhase s.phase⟩
    raw := raw
    digit := digit
    quotient9 := APPArithmetic.q9 raw
    tritResidue := trit
    turn := if d ≠ s.direction then 1 else 0
    sheetChange := if sheet ≠ s.sheet then 1 else 0 }

theorem rawRead_positive (sheet : Fin 2) (i j : Fin 9) : 0 < rawRead sheet i j := by
  unfold rawRead
  split
  · exact APPArithmetic.sum_positive i j
  · exact APPArithmetic.product_positive i j

theorem rawRead_source_formula (sheet : Fin 2) (i j : Fin 9) :
    rawRead sheet i j = if sheet = 0 then i.val + j.val + 2 else (i.val + 1) * (j.val + 1) := by
  simp only [rawRead, APPArithmetic.sumEval, APPArithmetic.productEval, APPArithmetic.value]
  split <;> omega

theorem step_before (s : State) (d : Fin 4) : (step s d).before = s := rfl
theorem step_direction (s : State) (d : Fin 4) : (step s d).after.direction = d := rfl
theorem step_phase (s : State) (d : Fin 4) :
    (step s d).after.phase.val = (s.phase.val + 1) % 3 := rfl

theorem step_raw_positive (s : State) (d : Fin 4) : 0 < (step s d).raw :=
  rawRead_positive s.sheet _ _

theorem step_reconstruct (s : State) (d : Fin 4) :
    (step s d).raw = (step s d).digit + 9 * (step s d).quotient9 :=
  APPArithmetic.reconstruct _ (step_raw_positive s d)

theorem step_digit_range (s : State) (d : Fin 4) :
    1 ≤ (step s d).digit ∧ (step s d).digit ≤ 9 :=
  APPArithmetic.rho9_range _

theorem step_trit_range (s : State) (d : Fin 4) : (step s d).tritResidue < 3 :=
  Nat.mod_lt _ (by decide)

theorem step_sheet_rule (s : State) (d : Fin 4) :
    (step s d).after.sheet =
      if (step s d).tritResidue = 1 then 0
      else if (step s d).tritResidue = 2 then 1 else s.sheet := rfl

inductive Predicate where
  | oddActive | nine | turn | sheetChange | tritZero | tritOne | tritTwo
  deriving DecidableEq, Repr

def impact (e : Edge) : Predicate → Bool
  | .oddActive => decide (e.digit = 1 ∨ e.digit = 3 ∨ e.digit = 5 ∨ e.digit = 7)
  | .nine => decide (e.digit = 9)
  | .turn => decide (e.turn = 1)
  | .sheetChange => decide (e.sheetChange = 1)
  | .tritZero => decide (e.tritResidue = 0)
  | .tritOne => decide (e.tritResidue = 1)
  | .tritTwo => decide (e.tritResidue = 2)

theorem step_turn_binary (s : State) (d : Fin 4) :
    (step s d).turn = 0 ∨ (step s d).turn = 1 := by
  simp only [step]
  split <;> simp

theorem step_sheetChange_binary (s : State) (d : Fin 4) :
    (step s d).sheetChange = 0 ∨ (step s d).sheetChange = 1 := by
  simp only [step]
  split <;> simp

theorem impact_turn_source (s : State) (d : Fin 4) :
    (impact (step s d) .turn).toNat = (step s d).turn := by
  rcases step_turn_binary s d with h | h <;> simp [impact, h]

theorem impact_sheetChange_source (s : State) (d : Fin 4) :
    (impact (step s d) .sheetChange).toNat = (step s d).sheetChange := by
  rcases step_sheetChange_binary s d with h | h <;> simp [impact, h]

def finish : State → List (Fin 4) → State
  | s, [] => s
  | s, d :: ds => finish (step s d).after ds

def walk : State → List (Fin 4) → List Edge
  | _, [] => []
  | s, d :: ds => step s d :: walk (step s d).after ds

/-- Chronological memory is validated from its last edge to its first edge. -/
def rewind : State → List Edge → Option State
  | terminal, [] => some terminal
  | terminal, e :: es => (rewind terminal es).bind fun current =>
      if e.after = current ∧ step e.before e.after.direction = e
      then some e.before else none

theorem finish_append (s : State) (u v : List (Fin 4)) :
    finish s (u ++ v) = finish (finish s u) v := by
  induction u generalizing s with
  | nil => rfl
  | cons d ds ih => simpa only [List.cons_append, finish] using ih (step s d).after

theorem walk_append (s : State) (u v : List (Fin 4)) :
    walk s (u ++ v) = walk s u ++ walk (finish s u) v := by
  induction u generalizing s with
  | nil => rfl
  | cons d ds ih => simp only [List.cons_append, walk, finish, ih]

theorem walk_length (s : State) (word : List (Fin 4)) :
    (walk s word).length = word.length := by
  induction word generalizing s with
  | nil => rfl
  | cons d ds ih => simp only [walk, List.length_cons, ih]

theorem walk_recovers_word (s : State) (word : List (Fin 4)) :
    (walk s word).map (fun e => e.after.direction) = word := by
  induction word generalizing s with
  | nil => rfl
  | cons d ds ih => simp only [walk, List.map_cons, step_direction, ih]

theorem rewind_walk (s : State) (word : List (Fin 4)) :
    rewind (finish s word) (walk s word) = some s := by
  induction word generalizing s with
  | nil => rfl
  | cons d ds ih => simp only [finish, walk, rewind, ih, Option.bind_some, step_before, step_direction, and_self, ite_true]

theorem rewind_append (terminal : State) (xs ys : List Edge) :
    rewind terminal (xs ++ ys) =
      (rewind terminal ys).bind (fun middle => rewind middle xs) := by
  induction xs with
  | nil => simp [rewind]
  | cons e es ih => simp only [List.cons_append, rewind, ih, Option.bind_assoc]

theorem rewind_rejects_raw_tampering (s : State) (d : Fin 4) :
    rewind (step s d).after [{step s d with raw := (step s d).raw + 1}] = none := by
  have hne : step s d ≠ {step s d with raw := (step s d).raw + 1} := by
    intro h
    have hh := congrArg Edge.raw h
    simp only at hh
    omega
  simpa only [rewind, Option.bind_some, step_before, step_direction, true_and, ite_false] using
    (if_neg hne : (if step s d = {step s d with raw := (step s d).raw + 1}
      then some (step s d).before else none) = none)

theorem finish_phase (s : State) (word : List (Fin 4)) :
    (finish s word).phase.val = (s.phase.val + word.length) % 3 := by
  induction word generalizing s with
  | nil => simpa [finish] using (Nat.mod_eq_of_lt s.phase.isLt).symm
  | cons d ds ih =>
      rw [finish, ih, step_phase, List.length_cons]
      omega

theorem phase_return (s : State) (word : List (Fin 4)) (h : word.length % 3 = 0) :
    (finish s word).phase = s.phase := by
  apply Fin.ext
  rw [finish_phase, Nat.add_mod, h, Nat.add_zero, Nat.mod_mod, Nat.mod_eq_of_lt s.phase.isLt]

structure Enriched where
  state : State
  memory : List Edge
  deriving DecidableEq, Repr

def transport (x : Enriched) (word : List (Fin 4)) : Enriched :=
  ⟨finish x.state word, x.memory ++ walk x.state word⟩

theorem transport_append (x : Enriched) (u v : List (Fin 4)) :
    transport x (u ++ v) = transport (transport x u) v := by
  simp [transport, finish_append, walk_append, List.append_assoc]

theorem transport_memory_length (x : Enriched) (word : List (Fin 4)) :
    (transport x word).memory.length = x.memory.length + word.length := by
  simp [transport, walk_length]

theorem nonempty_transport_not_reset (x : Enriched) (word : List (Fin 4)) (h : word ≠ []) :
    transport x word ≠ x := by
  intro heq
  have hlen := transport_memory_length x word
  rw [heq] at hlen
  have hw : word.length > 0 := List.length_pos_iff.mpr h
  omega

def State.code (s : State) : List Int :=
  [s.row.val, s.column.val, s.sheet.val, s.direction.val, s.phase.val]

def Edge.code (e : Edge) : List Int :=
  e.before.code ++ e.after.code ++
    [(e.raw : Int), e.digit, e.quotient9, e.tritResidue, e.turn, e.sheetChange]

theorem State.code_injective : Function.Injective State.code := by
  intro a b h
  cases a
  cases b
  simpa [State.code, State.mk.injEq, Fin.ext_iff] using h

theorem Edge.code_injective : Function.Injective Edge.code := by
  intro a b h
  cases a with
  | mk before after raw digit quotient trit turn sheetChange =>
    cases b with
    | mk before' after' raw' digit' quotient' trit' turn' sheetChange' =>
      cases before
      cases after
      cases before'
      cases after'
      simpa [Edge.code, State.code, Edge.mk.injEq, State.mk.injEq, Fin.ext_iff, and_assoc] using h

def sheetReading (s : Fin 2) : IncidenceRegister.Sheet :=
  if s = 0 then .additive else .multiplicative

/-- Position is posterior; the evaluation sheet is anterior. Memory retains the
complete edge, and the direction is appended to the declared route prefix. -/
def toVisit (e : Edge) (time multiplicity : Nat) (boundary : Bool)
    (route : List Nat) (memory : List Int) : IncidenceRegister.Visit where
  time := time
  row := e.after.row
  column := e.after.column
  sheet := sheetReading e.before.sheet
  multiplicity := multiplicity
  onBoundary := boundary
  route := route ++ [e.after.direction.val]
  memory := memory ++ e.code

theorem visit_preserves_previous_sheet (e : Edge) (t m : Nat) (b : Bool)
    (r : List Nat) (mem : List Int) :
    (toVisit e t m b r mem).sheet = sheetReading e.before.sheet := rfl

theorem visit_preserves_memory (e : Edge) (t m : Nat) (b : Bool)
    (r : List Nat) (mem : List Int) :
    (toVisit e t m b r mem).memory = mem ++ e.code := rfl

theorem toVisit_edge_injective (t m : Nat) (b : Bool) (r : List Nat) (mem : List Int) :
    Function.Injective (fun e => toVisit e t m b r mem) := by
  intro e f h
  have hm := congrArg IncidenceRegister.Visit.memory h
  change mem ++ e.code = mem ++ f.code at hm
  exact Edge.code_injective (List.append_cancel_left hm)

/-- This executable counterexample guards the previous-sheet convention. -/
theorem previous_sheet_changes_the_reading :
    let s : State := ⟨0, 2, 0, 0, 0⟩
    let e := step s 1
    e.raw = 5 ∧ e.after.sheet = 1 ∧
      rawRead e.after.sheet e.after.row e.after.column = 4 := by
  decide

theorem step_visit_raw (s : State) (d : Fin 4) (t m : Nat) (b : Bool)
    (r : List Nat) (mem : List Int) :
    (toVisit (step s d) t m b r mem).raw = (step s d).raw := by
  by_cases hs : s.sheet = 0
  · simp [toVisit, IncidenceRegister.Visit.raw, sheetReading, step, rawRead, hs]
  · simp [toVisit, IncidenceRegister.Visit.raw, sheetReading, step, rawRead, hs]

theorem step_visit_residue (s : State) (d : Fin 4) (t m : Nat) (b : Bool)
    (r : List Nat) (mem : List Int) :
    (toVisit (step s d) t m b r mem).residue = (step s d).digit := by
  rw [IncidenceRegister.Visit.residue, step_visit_raw]
  rfl

theorem step_visit_quotient (s : State) (d : Fin 4) (t m : Nat) (b : Bool)
    (r : List Nat) (mem : List Int) :
    (toVisit (step s d) t m b r mem).quotient = (step s d).quotient9 := by
  rw [IncidenceRegister.Visit.quotient, step_visit_raw]
  rfl

theorem step_visit_reconstruct (s : State) (d : Fin 4) (t m : Nat) (b : Bool)
    (r : List Nat) (mem : List Int) :
    (step s d).raw = (toVisit (step s d) t m b r mem).residue +
      9 * (toVisit (step s d) t m b r mem).quotient := by
  rw [step_visit_residue, step_visit_quotient]
  exact step_reconstruct s d

#print axioms movedRow_source_formula
#print axioms movedColumn_source_formula
#print axioms rawRead_positive
#print axioms rawRead_source_formula
#print axioms step_before
#print axioms step_direction
#print axioms step_phase
#print axioms step_raw_positive
#print axioms step_reconstruct
#print axioms step_digit_range
#print axioms step_trit_range
#print axioms step_sheet_rule
#print axioms step_turn_binary
#print axioms step_sheetChange_binary
#print axioms impact_turn_source
#print axioms impact_sheetChange_source
#print axioms finish_append
#print axioms walk_append
#print axioms walk_length
#print axioms walk_recovers_word
#print axioms rewind_walk
#print axioms rewind_append
#print axioms rewind_rejects_raw_tampering
#print axioms finish_phase
#print axioms phase_return
#print axioms transport_append
#print axioms transport_memory_length
#print axioms nonempty_transport_not_reset
#print axioms State.code_injective
#print axioms Edge.code_injective
#print axioms visit_preserves_previous_sheet
#print axioms visit_preserves_memory
#print axioms toVisit_edge_injective
#print axioms previous_sheet_changes_the_reading
#print axioms step_visit_raw
#print axioms step_visit_residue
#print axioms step_visit_quotient
#print axioms step_visit_reconstruct

end HMT.N30
