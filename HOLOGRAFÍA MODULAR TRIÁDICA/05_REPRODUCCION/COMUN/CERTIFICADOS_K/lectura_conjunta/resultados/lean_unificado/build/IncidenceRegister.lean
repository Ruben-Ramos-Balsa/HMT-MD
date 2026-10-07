import APPArithmetic
import RadixRecovery
import ChannelReconstruction

/-! Finite-support incidence reader, transcribed from
manuscript_es/sections/registro_incidencias_residentes.tex, lines 16--61.
Visits retain APP position and sheet; residue and quotient are evaluated,
not supplied independently. Trace orientation is directed (positive or negative), as in F002,
and is not inferred from the sign of a sum of trits.
The input is an incidence ledger, not a register or a target constant.
The selection of the particular terminal ledger is a separate upstream map.
-/
namespace HMT.IncidenceRegister

open DodecaphaseLinear

inductive Sheet where
  | additive | multiplicative
  deriving DecidableEq, Repr

inductive Orientation where
  | positive | negative
  deriving DecidableEq, Repr

def Orientation.sign : Orientation → Int
  | .positive => 1
  | .negative => -1

def Orientation.reverse : Orientation → Orientation
  | .positive => .negative
  | .negative => .positive

theorem reverse_sign (o : Orientation) : o.reverse.sign = -o.sign := by
  cases o <;> rfl

/-- Zero-based event time t corresponds to the manuscript time t+1. -/
structure Visit where
  time : Nat
  row : APPArithmetic.Digit
  column : APPArithmetic.Digit
  sheet : Sheet
  multiplicity : Nat
  onBoundary : Bool
  route : List Nat
  memory : List Int
  deriving Repr

structure Trace where
  time : Nat
  multiplicity : Nat
  orientation : Orientation
  winding : Nat
  route : List Nat
  memory : List Int
  deriving Repr

structure Ledger where
  visits : List Visit
  traces : List Trace
  deriving Repr

def Visit.raw (v : Visit) : Nat :=
  match v.sheet with
  | .additive => APPArithmetic.sumEval v.row v.column
  | .multiplicative => APPArithmetic.productEval v.row v.column

def Visit.residue (v : Visit) : Nat := APPArithmetic.rho9 v.raw
def Visit.quotient (v : Visit) : Nat := APPArithmetic.q9 v.raw

theorem visit_raw_positive (v : Visit) : 0 < v.raw := by
  cases h : v.sheet
  · simpa [Visit.raw, h] using APPArithmetic.sum_positive v.row v.column
  · simpa [Visit.raw, h] using APPArithmetic.product_positive v.row v.column

theorem visit_reconstruct (v : Visit) : v.raw = v.residue + 9 * v.quotient :=
  APPArithmetic.reconstruct v.raw (visit_raw_positive v)

def inWindow (m : Fin 12) (time : Nat) : Bool :=
  decide (9 * m.val ≤ time ∧ time < 9 * m.val + 9)

def actionSupport (r : Nat) : Bool := r == 1 || r == 3 || r == 5 || r == 7

def visitAction (m : Fin 12) (v : Visit) : Int :=
  if inWindow m v.time && actionSupport v.residue then v.multiplicity else 0

def visitVacancy (m : Fin 12) (v : Visit) : Int :=
  if inWindow m v.time && (v.residue == 9) then
    if v.onBoundary then v.multiplicity else -(v.multiplicity : Int)
  else 0

def traceContribution (m : Fin 12) (t : Trace) : Int :=
  if inWindow m t.time then -(t.multiplicity : Int) * t.orientation.sign else 0

def sumRead {α : Type} (f : α → Int) (xs : List α) : Int := (xs.map f).sum

theorem sum_append_zero (xs : List Int) : (xs ++ [0]).sum = xs.sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [List.sum_cons, ih]

def A (l : Ledger) (m : Fin 12) : Int := sumRead (visitAction m) l.visits
def C (l : Ledger) (m : Fin 12) : Int := sumRead (traceContribution m) l.traces
def V (l : Ledger) (m : Fin 12) : Int := sumRead (visitVacancy m) l.visits

def digit10 (x : Int) : Nat := (x % 10).toNat
def carry10 (x : Int) : Int := x / 10

theorem digit10_lt (x : Int) : digit10 x < 10 := by
  have h0 := Int.emod_nonneg x (by decide : (10 : Int) ≠ 0)
  have h1 := Int.emod_lt_of_pos x (by decide : (0 : Int) < 10)
  unfold digit10
  omega

theorem decimal_reconstruct (x : Int) :
    (digit10 x : Int) + 10 * carry10 x = x := by
  have h0 := Int.emod_nonneg x (by decide : (10 : Int) ≠ 0)
  unfold digit10 carry10
  omega

def block (l : Ledger) (m : Fin 12) : Nat :=
  100 * digit10 (A l m) + 10 * digit10 (C l m) + digit10 (V l m)

theorem block_lt (l : Ledger) (m : Fin 12) : block l m < 1000 := by
  have ha := digit10_lt (A l m)
  have hc := digit10_lt (C l m)
  have hv := digit10_lt (V l m)
  unfold block
  omega

def blocks (l : Ledger) : Vector12 := fun m => block l m

def channels (l : Ledger) : TerminalChannels.Channels := TerminalChannels.extract (blocks l)

def signed (l : Ledger) : Vector12 := TerminalChannels.harmonic (channels l)

theorem signed_is_H12 (l : Ledger) : signed l = H12 (blocks l) :=
  TerminalChannels.harmonic_extract _

theorem channels_compatible (l : Ledger) : TerminalChannels.Compatible (channels l) :=
  ⟨blocks l, rfl⟩

theorem signed_integral_inverse (l : Ledger) :
    TerminalChannels.inverseH (signed l) = blocks l := by
  rw [signed_is_H12, TerminalChannels.inverseH_H12]

theorem channel_return (l : Ledger) :
    TerminalChannels.extract (TerminalChannels.recover (channels l)) = channels l :=
  TerminalChannels.return_compatible _ (channels_compatible l)

/-- The radix object is constructed by evaluating counts, not by an expected list. -/
def register (l : Ledger) : RadixRecovery.K12 where
  digits := List.ofFn (block l)
  valid := by
    intro d hd
    obtain ⟨m, hm⟩ := List.mem_ofFn.mp hd
    rw [← hm]
    exact block_lt l m
  length_eq := List.length_ofFn

theorem register_digit (l : Ledger) (m : Fin 12) :
    (register l).digits[m.val]'(by rw [(register l).length_eq]; exact m.isLt) = block l m := by
  exact List.getElem_ofFn _

theorem register_recovery (l : Ledger) :
    RadixRecovery.decode 1000 12 (register l).publish = (register l).digits :=
  RadixRecovery.k12_recover _

theorem out_of_window (m : Fin 12) (t : Nat) (h : 108 ≤ t) : inWindow m t = false := by
  have hm := m.isLt
  simp only [inWindow, decide_eq_false_iff_not]
  omega

theorem later_visit_zero (m : Fin 12) (v : Visit) (h : 108 ≤ v.time) :
    visitAction m v = 0 ∧ visitVacancy m v = 0 := by
  simp [visitAction, visitVacancy, out_of_window m v.time h]

theorem later_trace_zero (m : Fin 12) (t : Trace) (h : 108 ≤ t.time) :
    traceContribution m t = 0 := by
  simp [traceContribution, out_of_window m t.time h]

def appendVisit (l : Ledger) (v : Visit) : Ledger := ⟨l.visits ++ [v], l.traces⟩
def appendTrace (l : Ledger) (t : Trace) : Ledger := ⟨l.visits, l.traces ++ [t]⟩

theorem append_later_visit_counts (l : Ledger) (v : Visit) (h : 108 ≤ v.time) (m : Fin 12) :
    A (appendVisit l v) m = A l m ∧ C (appendVisit l v) m = C l m ∧
      V (appendVisit l v) m = V l m := by
  have hz := later_visit_zero m v h
  simp [A, C, V, appendVisit, sumRead, hz.1, hz.2, sum_append_zero]

theorem append_later_trace_counts (l : Ledger) (t : Trace) (h : 108 ≤ t.time) (m : Fin 12) :
    A (appendTrace l t) m = A l m ∧ C (appendTrace l t) m = C l m ∧
      V (appendTrace l t) m = V l m := by
  simp [A, C, V, appendTrace, sumRead, later_trace_zero m t h, sum_append_zero]

theorem append_later_visit_blocks (l : Ledger) (v : Visit) (h : 108 ≤ v.time) :
    blocks (appendVisit l v) = blocks l := by
  funext m
  have hc := append_later_visit_counts l v h m
  simp only [blocks, block, hc.1, hc.2.1, hc.2.2]

theorem append_later_trace_blocks (l : Ledger) (t : Trace) (h : 108 ≤ t.time) :
    blocks (appendTrace l t) = blocks l := by
  funext m
  have hc := append_later_trace_counts l t h m
  simp only [blocks, block, hc.1, hc.2.1, hc.2.2]

theorem append_later_visit_signed (l : Ledger) (v : Visit) (h : 108 ≤ v.time) :
    signed (appendVisit l v) = signed l := by
  rw [signed_is_H12, signed_is_H12, append_later_visit_blocks l v h]

theorem append_later_trace_signed (l : Ledger) (t : Trace) (h : 108 ≤ t.time) :
    signed (appendTrace l t) = signed l := by
  rw [signed_is_H12, signed_is_H12, append_later_trace_blocks l t h]

theorem reverse_trace_contribution (m : Fin 12) (t : Trace) :
    traceContribution m {t with orientation := t.orientation.reverse} =
      -traceContribution m t := by
  simp only [traceContribution, reverse_sign]
  split <;> simp [Int.mul_neg]

#print axioms reverse_sign
#print axioms sum_append_zero
#print axioms visit_raw_positive
#print axioms visit_reconstruct
#print axioms digit10_lt
#print axioms decimal_reconstruct
#print axioms block_lt
#print axioms signed_is_H12
#print axioms channels_compatible
#print axioms signed_integral_inverse
#print axioms channel_return
#print axioms register_digit
#print axioms register_recovery
#print axioms out_of_window
#print axioms later_visit_zero
#print axioms later_trace_zero
#print axioms append_later_visit_counts
#print axioms append_later_trace_counts
#print axioms append_later_visit_blocks
#print axioms append_later_trace_blocks
#print axioms append_later_visit_signed
#print axioms append_later_trace_signed
#print axioms reverse_trace_contribution

end HMT.IncidenceRegister
