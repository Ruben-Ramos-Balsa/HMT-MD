import IncidenceRegister
import Mathlib

/-!
Prospective directed-impact adapter for the F002/N30 composition. A directed
trace retains the full word and edge memory; its sign is given by its directed
channel, never inferred from a sum of trits. Zero-weight records retain the
positions with no impact. No expected register, alpha, or metric value is input.
-/

namespace HMT.DirectedTraceLedger

open IncidenceRegister

structure Data where
  window : Fin 12
  multiplicity : Nat
  winding : Nat
  positiveHits : List Bool
  negativeHits : List Bool
  positiveRoute : List Nat
  negativeRoute : List Nat
  positiveMemory : List Int
  negativeMemory : List Int
  deriving Repr

def hits : List Bool → Nat
  | [] => 0
  | b :: bs => (if b then 1 else 0) + hits bs

def hitCode (bs : List Bool) : List Int := bs.map (fun b => if b then 1 else 0)

/-- Every position is retained; non-impacts have weight zero. -/
def records (m : Fin 12) (mult winding : Nat) (o : Orientation)
    (route : List Nat) (memory : List Int) (bs : List Bool) : List Trace :=
  bs.map fun b =>
    { time := 9 * m.val
      multiplicity := if b then mult else 0
      orientation := o
      winding := winding
      route := route
      memory := memory ++ hitCode bs }

def ledger (d : Data) : Ledger :=
  { visits := []
    traces :=
      records d.window d.multiplicity d.winding .positive
        d.positiveRoute d.positiveMemory d.positiveHits ++
      records d.window d.multiplicity d.winding .negative
        d.negativeRoute d.negativeMemory d.negativeHits }

theorem inWindow_start (m : Fin 12) : inWindow m (9 * m.val) = true := by
  simp [inWindow]

theorem inWindow_other_start (m n : Fin 12) (hne : n ≠ m) :
    inWindow n (9 * m.val) = false := by
  have hval : n.val ≠ m.val := fun h => hne (Fin.ext h)
  simp only [inWindow, decide_eq_false_iff_not]
  omega

theorem records_length (m : Fin 12) (mult winding : Nat) (o : Orientation)
    (route : List Nat) (memory : List Int) (bs : List Bool) :
    (records m mult winding o route memory bs).length = bs.length := by
  simp [records]

theorem records_read (m : Fin 12) (mult winding : Nat) (o : Orientation)
    (route : List Nat) (memory : List Int) (bs : List Bool) :
    sumRead (traceContribution m) (records m mult winding o route memory bs) =
      -(mult : Int) * o.sign * (hits bs : Int) := by
  unfold records sumRead
  have aux : ∀ (rest : List Bool) (mem : List Int),
      ((rest.map fun b =>
        traceContribution m
          { time := 9 * m.val, multiplicity := if b then mult else 0,
            orientation := o, winding := winding, route := route, memory := mem }).sum) =
        -(mult : Int) * o.sign * (hits rest : Int) := by
    intro rest mem
    induction rest with
    | nil => simp [hits]
    | cons b bs ih =>
      rw [List.map_cons, List.sum_cons, ih]
      cases b <;>
        simp [traceContribution, inWindow_start,
          hits, Nat.cast_add, Nat.cast_one]
      ring
  simpa only [List.map_map, Function.comp_def] using aux bs (memory ++ hitCode bs)

theorem records_other_read (m n : Fin 12) (hne : n ≠ m)
    (mult winding : Nat) (o : Orientation)
    (route : List Nat) (memory : List Int) (bs : List Bool) :
    sumRead (traceContribution n) (records m mult winding o route memory bs) = 0 := by
  simp [sumRead, records, List.map_map, Function.comp_def, traceContribution,
    inWindow_other_start m n hne]

theorem directed_count (d : Data) :
    C (ledger d) d.window = (d.multiplicity : Int) *
      ((hits d.negativeHits : Int) - (hits d.positiveHits : Int)) := by
  unfold C ledger sumRead
  rw [List.map_append, List.sum_append]
  change sumRead (traceContribution d.window)
      (records d.window d.multiplicity d.winding .positive
        d.positiveRoute d.positiveMemory d.positiveHits) +
    sumRead (traceContribution d.window)
      (records d.window d.multiplicity d.winding .negative
        d.negativeRoute d.negativeMemory d.negativeHits) = _
  rw [records_read, records_read]
  simp only [Orientation.sign]
  ring

theorem directed_other_count (d : Data) (n : Fin 12) (hne : n ≠ d.window) :
    C (ledger d) n = 0 := by
  unfold C ledger sumRead
  rw [List.map_append, List.sum_append]
  change sumRead (traceContribution n)
      (records d.window d.multiplicity d.winding .positive
        d.positiveRoute d.positiveMemory d.positiveHits) +
    sumRead (traceContribution n)
      (records d.window d.multiplicity d.winding .negative
        d.negativeRoute d.negativeMemory d.negativeHits) = _
  rw [records_other_read _ _ hne, records_other_read _ _ hne]
  rfl

theorem directed_preserves_visit_counts (d : Data) (m : Fin 12) :
    A (ledger d) m = 0 ∧ V (ledger d) m = 0 := by
  simp [A, V, ledger, sumRead]

def append (l r : Ledger) : Ledger :=
  { visits := l.visits ++ r.visits, traces := l.traces ++ r.traces }

theorem append_counts (l r : Ledger) (m : Fin 12) :
    A (append l r) m = A l m + A r m ∧
    C (append l r) m = C l m + C r m ∧
    V (append l r) m = V l m + V r m := by
  simp [A, C, V, append, sumRead, List.map_append, List.sum_append]

theorem attach_directed_counts (l : Ledger) (d : Data) :
    A (append l (ledger d)) d.window = A l d.window ∧
    C (append l (ledger d)) d.window = C l d.window +
      (d.multiplicity : Int) *
        ((hits d.negativeHits : Int) - (hits d.positiveHits : Int)) ∧
    V (append l (ledger d)) d.window = V l d.window := by
  have h := append_counts l (ledger d) d.window
  have z := directed_preserves_visit_counts d d.window
  simpa only [z.1, z.2, add_zero, directed_count] using h

def reverse (d : Data) : Data :=
  { d with
    positiveHits := d.negativeHits
    negativeHits := d.positiveHits
    positiveRoute := d.negativeRoute
    negativeRoute := d.positiveRoute
    positiveMemory := d.negativeMemory
    negativeMemory := d.positiveMemory }

theorem reverse_involutive (d : Data) : reverse (reverse d) = d := by
  cases d
  rfl

theorem reverse_directed_count (d : Data) :
    C (ledger (reverse d)) d.window = -C (ledger d) d.window := by
  have h := directed_count (reverse d)
  change C (ledger (reverse d)) d.window = _ at h
  rw [h, directed_count]
  simp only [reverse]
  ring

theorem directed_publication_reversible (l : Ledger) (d : Data) :
    RadixRecovery.decode 1000 12 (register (append l (ledger d))).publish =
      (register (append l (ledger d))).digits :=
  register_recovery _

#print axioms inWindow_start
#print axioms inWindow_other_start
#print axioms records_length
#print axioms records_read
#print axioms records_other_read
#print axioms directed_count
#print axioms directed_other_count
#print axioms directed_preserves_visit_counts
#print axioms append_counts
#print axioms attach_directed_counts
#print axioms reverse_involutive
#print axioms reverse_directed_count
#print axioms directed_publication_reversible

end HMT.DirectedTraceLedger
