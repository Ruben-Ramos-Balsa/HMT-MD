import N30DirectedImpacts
import N30VisitLedger

/-! Full finite-family composition of the prospective visit and directed-trace
adapters. Family data and the common boundary predicate are explicit. This
module does not identify a declared finite family with the canonical terminal
family and does not insert numerical register digits. -/

namespace HMT.N30FamilyPublication

open IncidenceRegister

structure Family where
  routes : List N30VisitLedger.Route
  routes_nonempty : routes ≠ []
  pairs : List N30DirectedImpacts.Pair
  boundary : Fin 9 → Fin 9 → Bool
  shared_boundary : ∀ r ∈ routes, r.boundary = boundary

def join : List Ledger → Ledger
  | [] => ⟨[], []⟩
  | l :: ls => DirectedTraceLedger.append l (join ls)

theorem join_A (ls : List Ledger) (m : Fin 12) :
    A (join ls) m = (ls.map (fun l => A l m)).sum := by
  induction ls with
  | nil => rfl
  | cons l ls ih =>
    rw [join, (DirectedTraceLedger.append_counts _ _ _).1, ih]
    rfl

theorem join_C (ls : List Ledger) (m : Fin 12) :
    C (join ls) m = (ls.map (fun l => C l m)).sum := by
  induction ls with
  | nil => rfl
  | cons l ls ih =>
    rw [join, (DirectedTraceLedger.append_counts _ _ _).2.1, ih]
    rfl

theorem join_V (ls : List Ledger) (m : Fin 12) :
    V (join ls) m = (ls.map (fun l => V l m)).sum := by
  induction ls with
  | nil => rfl
  | cons l ls ih =>
    rw [join, (DirectedTraceLedger.append_counts _ _ _).2.2, ih]
    rfl

def familyLedger (f : Family) : Ledger :=
  join (f.routes.map N30VisitLedger.ledger ++ f.pairs.map N30DirectedImpacts.generatedLedger)

def pairContribution (p : N30DirectedImpacts.Pair) (m : Fin 12) : Int :=
  if m = p.window then
    (p.multiplicity : Int) *
      ((N30DirectedImpacts.negativeCount p : Int) - (N30DirectedImpacts.positiveCount p : Int))
  else 0

theorem generated_pair_C (p : N30DirectedImpacts.Pair) (m : Fin 12) :
    C (N30DirectedImpacts.generatedLedger p) m = pairContribution p m := by
  by_cases h : m = p.window
  · subst m
    simp only [pairContribution, if_pos rfl]
    exact N30DirectedImpacts.generated_directed_count p
  · simp only [pairContribution, if_neg h]
    exact N30DirectedImpacts.generated_other_count p m h

theorem family_A (f : Family) (m : Fin 12) :
    A (familyLedger f) m = (f.routes.map (fun r => A (N30VisitLedger.ledger r) m)).sum := by
  rw [familyLedger, join_A, List.map_append, List.sum_append]
  have hz : (f.pairs.map (fun p => A (N30DirectedImpacts.generatedLedger p) m)).sum = 0 := by
    have h : ∀ p, A (N30DirectedImpacts.generatedLedger p) m = 0 :=
      fun p => (DirectedTraceLedger.directed_preserves_visit_counts
        (N30DirectedImpacts.publicationData p) m).1
    simp [h]
  simp only [List.map_map, Function.comp_def, hz, add_zero]

theorem family_C (f : Family) (m : Fin 12) :
    C (familyLedger f) m = (f.pairs.map (fun p => pairContribution p m)).sum := by
  rw [familyLedger, join_C, List.map_append, List.sum_append]
  have hz : (f.routes.map (fun r => C (N30VisitLedger.ledger r) m)).sum = 0 := by
    simp [N30VisitLedger.ledger, C, sumRead]
  simp only [List.map_map, Function.comp_def, hz, zero_add, generated_pair_C]

theorem family_V (f : Family) (m : Fin 12) :
    V (familyLedger f) m = (f.routes.map (fun r => V (N30VisitLedger.ledger r) m)).sum := by
  rw [familyLedger, join_V, List.map_append, List.sum_append]
  have hz : (f.pairs.map (fun p => V (N30DirectedImpacts.generatedLedger p) m)).sum = 0 := by
    have h : ∀ p, V (N30DirectedImpacts.generatedLedger p) m = 0 :=
      fun p => (DirectedTraceLedger.directed_preserves_visit_counts
        (N30DirectedImpacts.publicationData p) m).2
    simp [h]
  simp only [List.map_map, Function.comp_def, hz, add_zero]

theorem family_block (f : Family) (m : Fin 12) :
    block (familyLedger f) m =
      100 * digit10 ((f.routes.map (fun r => A (N30VisitLedger.ledger r) m)).sum) +
       10 * digit10 ((f.pairs.map (fun p => pairContribution p m)).sum) +
            digit10 ((f.routes.map (fun r => V (N30VisitLedger.ledger r) m)).sum) := by
  rw [block, family_A, family_C, family_V]

theorem family_publication_reversible (f : Family) :
    RadixRecovery.decode 1000 12 (register (familyLedger f)).publish =
      (register (familyLedger f)).digits := register_recovery _

theorem family_integer_counts_retained (f : Family) (m : Fin 12) :
    (digit10 (A (familyLedger f) m) : Int) + 10 * carry10 (A (familyLedger f) m) =
      A (familyLedger f) m ∧
    (digit10 (C (familyLedger f) m) : Int) + 10 * carry10 (C (familyLedger f) m) =
      C (familyLedger f) m ∧
    (digit10 (V (familyLedger f) m) : Int) + 10 * carry10 (V (familyLedger f) m) =
      V (familyLedger f) m :=
  ⟨decimal_reconstruct _, decimal_reconstruct _, decimal_reconstruct _⟩

#print axioms join_A
#print axioms join_C
#print axioms join_V
#print axioms generated_pair_C
#print axioms family_A
#print axioms family_C
#print axioms family_V
#print axioms family_block
#print axioms family_publication_reversible
#print axioms family_integer_counts_retained

end HMT.N30FamilyPublication
