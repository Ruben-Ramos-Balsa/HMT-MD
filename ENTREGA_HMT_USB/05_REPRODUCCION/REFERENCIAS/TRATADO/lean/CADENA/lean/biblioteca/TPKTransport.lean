import Std

/-
Observable two-cursor chronology and its route-memory lift.
Source: manuscript_es/sections/tpk_desarrollo_integrado.tex in the active
standalone article I. This file formalizes the observable factor and explicit
history length, not the full enriched cylinder generator.
-/
namespace TPKTransport

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

inductive Direction where
  | north | east | south | west
  deriving DecidableEq, Repr

def opposite : Direction → Direction
  | .north => .south
  | .east => .west
  | .south => .north
  | .west => .east

theorem opposite_twice (d : Direction) : opposite (opposite d) = d := by
  cases d <;> rfl

def dx : Direction → Int
  | .north => -1
  | .south => 1
  | _ => 0

def dy : Direction → Int
  | .east => 1
  | .west => -1
  | _ => 0

theorem opposite_vector (d : Direction) :
    dx (opposite d) = -dx d ∧ dy (opposite d) = -dy d := by
  cases d <;> decide

abbrev Phase := Fin 108

def nextPhase (p : Phase) : Phase := ⟨(p.val + 1) % 108, Nat.mod_lt _ (by decide)⟩
def prevPhase (p : Phase) : Phase := ⟨(p.val + 107) % 108, Nat.mod_lt _ (by decide)⟩

theorem phase_prev_next (p : Phase) : prevPhase (nextPhase p) = p := by
  apply Fin.ext
  simp only [prevPhase, nextPhase]
  have := p.isLt
  omega

theorem phase_next_prev (p : Phase) : nextPhase (prevPhase p) = p := by
  apply Fin.ext
  simp only [prevPhase, nextPhase]
  have := p.isLt
  omega

inductive Sheet where
  | additive | multiplicative
  deriving DecidableEq, Repr

def active (s : Sheet) (p : Phase) : Bool :=
  match s with
  | .additive => p.val % 3 == 0
  | .multiplicative => p.val % 3 == 1

def halfTurn (p : Phase) : Bool := (p.val + 1) % 27 == 0

def orient (turn : Bool) (d : Direction) : Direction :=
  if turn then opposite d else d

theorem orient_twice (b : Bool) (d : Direction) : orient b (orient b d) = d := by
  cases b <;> simp [orient, opposite_twice]

structure Cursor where
  x : Int
  y : Int
  direction : Direction
  deriving DecidableEq, Repr

def stepCursor (s : Sheet) (p : Phase) (c : Cursor) : Cursor :=
  ⟨c.x + (if active s p then dx c.direction else 0),
   c.y + (if active s p then dy c.direction else 0),
   orient (halfTurn p) c.direction⟩

def unstepCursor (s : Sheet) (p : Phase) (c : Cursor) : Cursor :=
  let d := orient (halfTurn p) c.direction
  ⟨c.x - (if active s p then dx d else 0),
   c.y - (if active s p then dy d else 0), d⟩

theorem cursor_unstep_step (s : Sheet) (p : Phase) (c : Cursor) :
    unstepCursor s p (stepCursor s p c) = c := by
  cases c with
  | mk x y d =>
    simp [unstepCursor, stepCursor, orient_twice]

theorem cursor_step_unstep (s : Sheet) (p : Phase) (c : Cursor) :
    stepCursor s p (unstepCursor s p c) = c := by
  cases c with
  | mk x y d =>
    simp [unstepCursor, stepCursor, orient_twice]

structure ObservableLift where
  plus : Cursor
  times : Cursor
  phase : Phase
  deriving DecidableEq, Repr

def step (q : ObservableLift) : ObservableLift :=
  ⟨stepCursor .additive q.phase q.plus,
   stepCursor .multiplicative q.phase q.times, nextPhase q.phase⟩

def unstep (q : ObservableLift) : ObservableLift :=
  let p := prevPhase q.phase
  ⟨unstepCursor .additive p q.plus,
   unstepCursor .multiplicative p q.times, p⟩

theorem unstep_step (q : ObservableLift) : unstep (step q) = q := by
  cases q
  simp [step, unstep, phase_prev_next, cursor_unstep_step]

theorem step_unstep (q : ObservableLift) : step (unstep q) = q := by
  cases q
  simp [step, unstep, phase_next_prev, cursor_step_unstep]

def iterate {α : Type} (f : α → α) : Nat → α → α
  | 0, x => x
  | n + 1, x => f (iterate f n x)

theorem iterate_add {α : Type} (f : α → α) (n m : Nat) (x : α) :
    iterate f (n + m) x = iterate f m (iterate f n x) := by
  induction m with
  | zero => simp [iterate]
  | succ m ih => simp [iterate, ih]

structure HistoryLift where
  current : ObservableLift
  past : List ObservableLift

def recordStep (q : HistoryLift) : HistoryLift :=
  ⟨step q.current, q.past ++ [q.current]⟩

theorem recorded_projection (n : Nat) (q : HistoryLift) :
    (iterate recordStep n q).current = iterate step n q.current := by
  induction n with
  | zero => rfl
  | succ n ih => simp [iterate, recordStep, ih]

theorem recorded_length (n : Nat) (q : HistoryLift) :
    (iterate recordStep n q).past.length = q.past.length + n := by
  induction n with
  | zero => simp [iterate]
  | succ n ih => simp [iterate, recordStep, ih, Nat.add_assoc]

theorem recorded_no_reset (n : Nat) (hn : 0 < n) (q : HistoryLift) :
    iterate recordStep n q ≠ q := by
  intro h
  have hlen := congrArg (fun z : HistoryLift => z.past.length) h
  change (iterate recordStep n q).past.length = q.past.length at hlen
  rw [recorded_length] at hlen
  omega

theorem recorded_prefix_preserved (n : Nat) (q : HistoryLift) :
    ∃ tail, (iterate recordStep n q).past = q.past ++ tail := by
  induction n with
  | zero => exact ⟨[], by simp [iterate]⟩
  | succ n ih =>
    obtain ⟨tail, ht⟩ := ih
    exact ⟨tail ++ [(iterate recordStep n q).current], by
      simp [iterate, recordStep, ht, List.append_assoc]⟩

def nonadicPhase (depth : Nat) : Nat := depth % 9
def nonadicMemory (depth : Nat) : Nat := depth / 9

theorem nonadic_phase_return (depth : Nat) :
    nonadicPhase (depth + 9) = nonadicPhase depth := by
  simp [nonadicPhase, Nat.add_mod]

theorem nonadic_memory_advance (depth : Nat) :
    nonadicMemory (depth + 9) = nonadicMemory depth + 1 := by
  simp [nonadicMemory, Nat.add_div_right]

theorem phase_memory_reconstruct (depth : Nat) :
    nonadicPhase depth + 9 * nonadicMemory depth = depth := by
  exact Nat.mod_add_div depth 9

def residue9 (z : Int) : Int := 1 + (z - 1) % 9
def quotient9 (z : Int) : Int := (z - 1) / 9

theorem lifted_coordinate_reconstruct (z : Int) :
    residue9 z + 9 * quotient9 z = z := by
  simp only [residue9, quotient9]
  omega

def boundaryCarry (z delta : Int) : Int := quotient9 (z + delta) - quotient9 z

theorem boundary_transport (z delta : Int) :
    residue9 (z + delta) + 9 * boundaryCarry z delta = residue9 z + delta := by
  have h0 := lifted_coordinate_reconstruct z
  have h1 := lifted_coordinate_reconstruct (z + delta)
  unfold boundaryCarry
  omega

theorem boundary_cocycle (z a b : Int) :
    boundaryCarry z (a + b) = boundaryCarry z a + boundaryCarry (z + a) b := by
  simp only [boundaryCarry]
  have : z + (a + b) = z + a + b := by omega
  rw [this]
  omega

#print axioms opposite_twice
#print axioms opposite_vector
#print axioms phase_prev_next
#print axioms phase_next_prev
#print axioms orient_twice
#print axioms cursor_unstep_step
#print axioms cursor_step_unstep
#print axioms unstep_step
#print axioms step_unstep
#print axioms iterate_add
#print axioms recorded_projection
#print axioms recorded_length
#print axioms recorded_no_reset
#print axioms recorded_prefix_preserved
#print axioms nonadic_phase_return
#print axioms nonadic_memory_advance
#print axioms phase_memory_reconstruct
#print axioms lifted_coordinate_reconstruct
#print axioms boundary_transport
#print axioms boundary_cocycle

end TPKTransport
