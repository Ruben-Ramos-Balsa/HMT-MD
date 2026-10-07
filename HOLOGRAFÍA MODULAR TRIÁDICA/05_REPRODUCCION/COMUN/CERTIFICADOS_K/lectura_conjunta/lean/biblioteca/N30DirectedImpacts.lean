import DirectedTraceLedger
import N30Transport

/-! Composition of the prospective N30 transport with directed-impact counts.
The supplied words and impact predicate are explicit construction data. Their
selection as the particular terminal family is not asserted here. -/

namespace HMT.N30DirectedImpacts

open N30 IncidenceRegister

/-- The publication channel C uses r=120; the motor itself remains generic. -/
structure Pair where
  seed : State
  positive : List (Fin 4)
  negative : List (Fin 4)
  predicate : Predicate
  window : Fin 12
  multiplicity : Nat
  multiplicity_positive : 0 < multiplicity
  winding : Nat
  channel : Nat
  channel_valid : channel = 120
  positive_length : positive.length = channel * (1 + 3 * winding)
  negative_length : negative.length = channel * (1 + 3 * winding)

def positiveHistory (p : Pair) : List Edge := walk p.seed p.positive
def negativeHistory (p : Pair) : List Edge := walk p.seed p.negative

def publicationData (p : Pair) : DirectedTraceLedger.Data where
  window := p.window
  multiplicity := p.multiplicity
  winding := p.winding
  positiveHits := (positiveHistory p).map (fun e => impact e p.predicate)
  negativeHits := (negativeHistory p).map (fun e => impact e p.predicate)
  positiveRoute := p.positive.map Fin.val
  negativeRoute := p.negative.map Fin.val
  positiveMemory := (positiveHistory p).flatMap Edge.code
  negativeMemory := (negativeHistory p).flatMap Edge.code

def generatedLedger (p : Pair) : Ledger := DirectedTraceLedger.ledger (publicationData p)

def positiveCount (p : Pair) : Nat :=
  DirectedTraceLedger.hits ((positiveHistory p).map (fun e => impact e p.predicate))

def negativeCount (p : Pair) : Nat :=
  DirectedTraceLedger.hits ((negativeHistory p).map (fun e => impact e p.predicate))

theorem generated_directed_count (p : Pair) :
    C (generatedLedger p) p.window =
      (p.multiplicity : Int) * ((negativeCount p : Int) - (positiveCount p : Int)) :=
  DirectedTraceLedger.directed_count (publicationData p)

theorem generated_other_count (p : Pair) (n : Fin 12) (hne : n ≠ p.window) :
    C (generatedLedger p) n = 0 :=
  DirectedTraceLedger.directed_other_count (publicationData p) n hne

theorem generated_memory_lengths (p : Pair) :
    (positiveHistory p).length = p.channel * (1 + 3 * p.winding) ∧
    (negativeHistory p).length = p.channel * (1 + 3 * p.winding) := by
  simp only [positiveHistory, negativeHistory, walk_length,
    p.positive_length, p.negative_length, and_self]

theorem generated_C_channel_domain (p : Pair) :
    0 < p.multiplicity ∧
    (positiveHistory p).length = 120 * (1 + 3 * p.winding) ∧
    (negativeHistory p).length = 120 * (1 + 3 * p.winding) := by
  have h := generated_memory_lengths p
  rw [p.channel_valid] at h
  exact ⟨p.multiplicity_positive, h⟩

theorem generated_routes_recovered (p : Pair) :
    (positiveHistory p).map (fun e => e.after.direction) = p.positive ∧
    (negativeHistory p).map (fun e => e.after.direction) = p.negative :=
  ⟨walk_recovers_word _ _, walk_recovers_word _ _⟩

theorem generated_seed_recovered (p : Pair) :
    rewind (finish p.seed p.positive) (positiveHistory p) = some p.seed ∧
    rewind (finish p.seed p.negative) (negativeHistory p) = some p.seed :=
  ⟨rewind_walk _ _, rewind_walk _ _⟩

theorem generated_ledger_extends_counts (l : Ledger) (p : Pair) :
    A (DirectedTraceLedger.append l (generatedLedger p)) p.window = A l p.window ∧
    C (DirectedTraceLedger.append l (generatedLedger p)) p.window = C l p.window +
      (p.multiplicity : Int) * ((negativeCount p : Int) - (positiveCount p : Int)) ∧
    V (DirectedTraceLedger.append l (generatedLedger p)) p.window = V l p.window :=
  DirectedTraceLedger.attach_directed_counts l (publicationData p)

theorem generated_ledger_publication_reversible (l : Ledger) (p : Pair) :
    RadixRecovery.decode 1000 12
      (register (DirectedTraceLedger.append l (generatedLedger p))).publish =
      (register (DirectedTraceLedger.append l (generatedLedger p))).digits :=
  DirectedTraceLedger.directed_publication_reversible l (publicationData p)

/-- The seed recovery and directed count are composed before radix publication. -/
theorem prospective_trace_to_register (l : Ledger) (p : Pair) :
    rewind (finish p.seed p.positive) (positiveHistory p) = some p.seed ∧
    rewind (finish p.seed p.negative) (negativeHistory p) = some p.seed ∧
    C (generatedLedger p) p.window =
      (p.multiplicity : Int) * ((negativeCount p : Int) - (positiveCount p : Int)) ∧
    RadixRecovery.decode 1000 12
      (register (DirectedTraceLedger.append l (generatedLedger p))).publish =
      (register (DirectedTraceLedger.append l (generatedLedger p))).digits :=
  ⟨(generated_seed_recovered p).1, (generated_seed_recovered p).2,
    generated_directed_count p, generated_ledger_publication_reversible l p⟩

#print axioms generated_directed_count
#print axioms generated_other_count
#print axioms generated_memory_lengths
#print axioms generated_C_channel_domain
#print axioms generated_routes_recovered
#print axioms generated_seed_recovered
#print axioms generated_ledger_extends_counts
#print axioms generated_ledger_publication_reversible
#print axioms prospective_trace_to_register

end HMT.N30DirectedImpacts
