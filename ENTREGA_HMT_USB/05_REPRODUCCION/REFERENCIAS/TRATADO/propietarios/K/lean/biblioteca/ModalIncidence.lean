/-
  Modal incidence generated from the three-event TRIT selector calendar.
  Source: article I, generacion.tex and retorno_areal_volumetrico.tex.
  No real constant, spectral root, target ratio or eigenvector is an input.
  The matrix is a posterior modal publication, not the full TPK transition.
-/
import Std

namespace ModalIncidence

inductive Mode where
  | sigma
  | pi
  deriving DecidableEq, Repr

/-- The same oriented mod-3 selector used by the local TRIT chart. -/
def phase (r : Int) : Int := if r % 3 = 0 then 0 else if r % 3 = 1 then 1 else -1

def select (t : Int) (m : Mode) : Mode :=
  if t = 1 then .sigma else if t = -1 then .pi else m

def calendar : List Int := [phase 1, phase 2, phase 3]

theorem calendar_values : calendar = [1, -1, 0] := by decide

def modalCycle (initial : Mode) : Mode × Mode × Mode :=
  let m₁ := select (phase 1) initial
  let m₂ := select (phase 2) m₁
  let m₃ := select (phase 3) m₂
  (m₁, m₂, m₃)

theorem modal_cycle_values (initial : Mode) :
    modalCycle initial = (.sigma, .pi, .pi) := by
  cases initial <;> rfl

/-- Includes the closing edge from the last mode back to the first. -/
def cycleEdges (initial : Mode) : List (Mode × Mode) :=
  let m := modalCycle initial
  [(m.1, m.2.1), (m.2.1, m.2.2), (m.2.2, m.1)]

theorem cycle_edges_values (initial : Mode) :
    cycleEdges initial = [(.sigma, .pi), (.pi, .pi), (.pi, .sigma)] := by
  simp only [cycleEdges, modal_cycle_values]

def edgeCount (initial src dst : Mode) : Nat :=
  (cycleEdges initial).count (src, dst)

theorem primitive_counts (initial : Mode) :
    (edgeCount initial .sigma .sigma,
     edgeCount initial .sigma .pi,
     edgeCount initial .pi .sigma,
     edgeCount initial .pi .pi) = (0, 1, 1, 1) := by
  cases initial <;> decide

def repeatedEdges (initial : Mode) : Nat → List (Mode × Mode)
  | 0 => []
  | n + 1 => cycleEdges initial ++ repeatedEdges initial n

theorem repeated_count (initial src dst : Mode) (n : Nat) :
    (repeatedEdges initial n).count (src, dst) = n * edgeCount initial src dst := by
  induction n with
  | zero => simp [repeatedEdges]
  | succ n ih =>
    simp only [repeatedEdges, List.count_append, ih, edgeCount, Nat.succ_mul]
    omega

theorem repeated_length (initial : Mode) (n : Nat) :
    (repeatedEdges initial n).length = 3 * n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [repeatedEdges, List.length_append, cycle_edges_values,
      List.length_cons, List.length_nil, ih]
    omega

/-- Explicit 2×2 integer matrix in the mode order (Σ, Π). -/
structure Matrix where
  aa : Int
  av : Int
  va : Int
  vv : Int
  deriving DecidableEq, Repr

def F : Matrix :=
  ⟨edgeCount .pi .sigma .sigma, edgeCount .pi .sigma .pi,
   edgeCount .pi .pi .sigma, edgeCount .pi .pi .pi⟩

theorem incidence_generated : F = ⟨0, 1, 1, 1⟩ := by decide

def incidenceAfter (n : Nat) : Matrix :=
  ⟨(repeatedEdges .pi n).count (.sigma, .sigma),
   (repeatedEdges .pi n).count (.sigma, .pi),
   (repeatedEdges .pi n).count (.pi, .sigma),
   (repeatedEdges .pi n).count (.pi, .pi)⟩

theorem incidence_after (n : Nat) : incidenceAfter n = ⟨0, n, n, n⟩ := by
  simp [incidenceAfter, repeated_count, edgeCount, cycle_edges_values]

theorem macro_calendar_counts :
    incidenceAfter 3 = ⟨0, 3, 3, 3⟩ ∧
    incidenceAfter 9 = ⟨0, 9, 9, 9⟩ ∧
    incidenceAfter 36 = ⟨0, 36, 36, 36⟩ := by
  rw [incidence_after, incidence_after, incidence_after]
  decide

def identity : Matrix := ⟨1, 0, 0, 1⟩

def mul (A B : Matrix) : Matrix :=
  ⟨A.aa * B.aa + A.av * B.va, A.aa * B.av + A.av * B.vv,
   A.va * B.aa + A.vv * B.va, A.va * B.av + A.vv * B.vv⟩

def power : Nat → Matrix
  | 0 => identity
  | n + 1 => mul F (power n)

def act (A : Matrix) (v : Int × Int) : Int × Int :=
  (A.aa * v.1 + A.av * v.2, A.va * v.1 + A.vv * v.2)

theorem incidence_action (x y : Int) : act F (x, y) = (y, x + y) := by
  simp [act, incidence_generated]

/-- The sequence is emitted by the generated matrix, not supplied beforehand. -/
def modalVector : Nat → Int × Int
  | 0 => (0, 1)
  | n + 1 => act F (modalVector n)

def sequence (n : Nat) : Int := (modalVector n).1

theorem vector_next (n : Nat) :
    modalVector (n + 1) = ((modalVector n).2, (modalVector n).1 + (modalVector n).2) := by
  exact incidence_action (modalVector n).1 (modalVector n).2

theorem sequence_next (n : Nat) : sequence (n + 1) = (modalVector n).2 := by
  simp only [sequence, vector_next]

theorem sequence_zero : sequence 0 = 0 := by rfl

theorem sequence_one : sequence 1 = 1 := by decide

theorem sequence_recurrence (n : Nat) :
    sequence (n + 2) = sequence n + sequence (n + 1) := by
  rw [sequence_next (n + 1), vector_next, sequence_next]
  rfl

theorem power_entries (n : Nat) :
    power (n + 1) =
      ⟨sequence n, sequence (n + 1), sequence (n + 1), sequence (n + 2)⟩ := by
  induction n with
  | zero => decide
  | succ n ih =>
    change mul F (power (n + 1)) = _
    rw [ih]
    simp only [mul, incidence_generated, Int.zero_mul, Int.one_mul, Int.zero_add]
    have h := sequence_recurrence n
    have h' := sequence_recurrence (n + 1)
    simp only [Nat.add_assoc] at *
    rw [← h, ← h']

def determinant (A : Matrix) : Int := A.aa * A.vv - A.av * A.va

theorem determinant_left_step (A : Matrix) :
    determinant (mul F A) = - determinant A := by
  simp only [determinant, mul, incidence_generated,
    Int.zero_mul, Int.one_mul, Int.zero_add, Int.mul_add]
  rw [Int.mul_comm A.va A.av, Int.mul_comm A.vv A.aa, Int.mul_comm A.vv A.va]
  omega

theorem power_determinant (n : Nat) : determinant (power n) = (-1 : Int) ^ n := by
  induction n with
  | zero => decide
  | succ n ih =>
    rw [power, determinant_left_step, ih, Int.pow_succ]
    simp

theorem cassini (n : Nat) :
    sequence (n + 1) * sequence (n + 1) - sequence n * sequence (n + 2) =
      (-1 : Int) ^ n := by
  have h := power_determinant (n + 1)
  rw [power_entries, determinant, Int.pow_succ] at h
  simp only [Int.mul_neg, Int.mul_one] at h
  omega

theorem modal_vector_nonnegative (n : Nat) :
    0 ≤ (modalVector n).1 ∧ 0 ≤ (modalVector n).2 := by
  induction n with
  | zero => decide
  | succ n ih =>
    rw [vector_next]
    dsimp
    omega

theorem sequence_positive (n : Nat) : 0 < sequence (n + 1) := by
  induction n with
  | zero => decide
  | succ n ih =>
    have hn := modal_vector_nonnegative n
    rw [sequence_recurrence]
    change 0 ≤ sequence n ∧ _ at hn
    omega

set_option maxRecDepth 20000 in
theorem finite_108_return_counts :
    sequence 107 = 10284720757613717413913 ∧
    sequence 109 = 26925748508234281076009 := by
  decide

theorem repeated_counts_not_power :
    (repeatedEdges .pi 2).count (.sigma, .sigma) = 0 ∧ (power 2).aa = 1 := by
  decide

#print axioms calendar_values
#print axioms modal_cycle_values
#print axioms cycle_edges_values
#print axioms primitive_counts
#print axioms repeated_count
#print axioms repeated_length
#print axioms incidence_generated
#print axioms incidence_after
#print axioms macro_calendar_counts
#print axioms incidence_action
#print axioms vector_next
#print axioms sequence_next
#print axioms sequence_zero
#print axioms sequence_one
#print axioms sequence_recurrence
#print axioms power_entries
#print axioms determinant_left_step
#print axioms power_determinant
#print axioms cassini
#print axioms modal_vector_nonnegative
#print axioms sequence_positive
#print axioms finite_108_return_counts
#print axioms repeated_counts_not_power

end ModalIncidence
