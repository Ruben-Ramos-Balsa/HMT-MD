import N30Transport

/-! Routes produce the first 108 incidence visits prospectively. A boundary
predicate and route are declared inputs; neither a terminal register nor a
target constant is used to select them. The previous-sheet convention is
inherited from N30Transport.toVisit. -/
namespace HMT.N30VisitLedger

open N30

structure Route where
  seed : State
  word : List (Fin 4)
  multiplicity : Nat
  multiplicity_positive : 0 < multiplicity
  word_long : 108 ≤ word.length
  boundary : Fin 9 → Fin 9 → Bool

def wordPrefix (r : Route) : List (Fin 4) := r.word.take 108
def edges (r : Route) : List Edge := walk r.seed (wordPrefix r)

theorem prefix_length (r : Route) : (wordPrefix r).length = 108 := by
  simp [wordPrefix, List.length_take, Nat.min_eq_left r.word_long]

theorem edges_length (r : Route) : (edges r).length = 108 := by
  simp [edges, walk_length, prefix_length]

theorem walk_take (s : State) (word : List (Fin 4)) (n : Nat) :
    walk s (word.take n) = (walk s word).take n := by
  induction word generalizing s n with
  | nil => simp [walk]
  | cons d ds ih =>
      cases n with
      | zero => simp [walk]
      | succ n => simp only [List.take_succ_cons, walk, ih]

theorem edges_first108 (r : Route) : edges r = (walk r.seed r.word).take 108 :=
  walk_take _ _ _

theorem walk_getElem (s : State) (word : List (Fin 4)) (n : Nat) (h : n < word.length) :
    (walk s word)[n]'(by rw [walk_length]; exact h) =
      step (finish s (word.take n)) word[n] := by
  induction word generalizing s n with
  | nil => simp at h
  | cons d ds ih =>
      cases n with
      | zero => simp [walk, finish]
      | succ n =>
          simpa only [walk, List.getElem_cons_succ, List.take_succ_cons, finish]
            using ih (step s d).after n (by simpa using h)

def edgeAt (r : Route) (tick : Fin 108) : Edge :=
  (edges r)[tick.val]'(by rw [edges_length]; exact tick.isLt)

theorem edgeAt_is_step (r : Route) (tick : Fin 108) :
    edgeAt r tick = step (finish r.seed ((wordPrefix r).take tick.val))
      ((wordPrefix r)[tick.val]'(by rw [prefix_length]; exact tick.isLt)) :=
  walk_getElem _ _ _ (by rw [prefix_length]; exact tick.isLt)

def visitAt (r : Route) (tick : Fin 108) : IncidenceRegister.Visit :=
  let e := edgeAt r tick
  toVisit e tick.val r.multiplicity (r.boundary e.after.row e.after.column)
    (((wordPrefix r).take tick.val).map Fin.val)
    (((edges r).take tick.val).flatMap Edge.code)

def visits (r : Route) : List IncidenceRegister.Visit := List.ofFn (visitAt r)

def ledger (r : Route) : IncidenceRegister.Ledger := ⟨visits r, []⟩

theorem visits_length (r : Route) : (visits r).length = 108 := List.length_ofFn

theorem visits_getElem (r : Route) (tick : Fin 108) :
    (visits r)[tick.val]'(by rw [visits_length]; exact tick.isLt) = visitAt r tick := by
  exact List.getElem_ofFn _

theorem visitAt_time (r : Route) (tick : Fin 108) : (visitAt r tick).time = tick.val := rfl
theorem visitAt_multiplicity (r : Route) (tick : Fin 108) :
    (visitAt r tick).multiplicity = r.multiplicity := rfl
theorem visitAt_multiplicity_positive (r : Route) (tick : Fin 108) :
    0 < (visitAt r tick).multiplicity := r.multiplicity_positive
theorem visitAt_boundary (r : Route) (tick : Fin 108) :
    (visitAt r tick).onBoundary = r.boundary (edgeAt r tick).after.row (edgeAt r tick).after.column := rfl
theorem visitAt_previous_sheet (r : Route) (tick : Fin 108) :
    (visitAt r tick).sheet = sheetReading (edgeAt r tick).before.sheet := rfl
theorem visitAt_cell (r : Route) (tick : Fin 108) :
    (visitAt r tick).row = (edgeAt r tick).after.row ∧
    (visitAt r tick).column = (edgeAt r tick).after.column := ⟨rfl, rfl⟩

theorem visitAt_raw (r : Route) (tick : Fin 108) :
    (visitAt r tick).raw = (edgeAt r tick).raw := by
  unfold visitAt
  rw [edgeAt_is_step]
  exact step_visit_raw _ _ _ _ _ _ _

theorem visitAt_residue (r : Route) (tick : Fin 108) :
    (visitAt r tick).residue = (edgeAt r tick).digit := by
  unfold visitAt
  rw [edgeAt_is_step]
  exact step_visit_residue _ _ _ _ _ _ _

theorem visitAt_quotient (r : Route) (tick : Fin 108) :
    (visitAt r tick).quotient = (edgeAt r tick).quotient9 := by
  unfold visitAt
  rw [edgeAt_is_step]
  exact step_visit_quotient _ _ _ _ _ _ _

theorem visitAt_reconstruct (r : Route) (tick : Fin 108) :
    (edgeAt r tick).raw = (visitAt r tick).residue + 9 * (visitAt r tick).quotient := by
  rw [← visitAt_raw]
  exact IncidenceRegister.visit_reconstruct _

theorem visitAt_complete_memory (r : Route) (tick : Fin 108) :
    (visitAt r tick).memory = ((edges r).take (tick.val + 1)).flatMap Edge.code := by
  change ((edges r).take tick.val).flatMap Edge.code ++ (edgeAt r tick).code = _
  rw [List.take_succ_eq_append_getElem (by rw [edges_length]; exact tick.isLt)]
  rw [List.flatMap_append]
  rfl

theorem visitAt_complete_route (r : Route) (tick : Fin 108) :
    (visitAt r tick).route = ((wordPrefix r).take (tick.val + 1)).map Fin.val := by
  rw [List.take_succ_eq_append_getElem (by rw [prefix_length]; exact tick.isLt)]
  simp only [visitAt, toVisit, List.map_append, List.map_cons, List.map_nil]
  rw [edgeAt_is_step, step_direction]

theorem actionSupport_impact (e : Edge) :
    IncidenceRegister.actionSupport e.digit = impact e .oddActive := by
  simp [IncidenceRegister.actionSupport, impact, Bool.decide_or, Bool.or_assoc, Bool.beq_eq_decide_eq]

theorem visitAt_action (r : Route) (tick : Fin 108) (window : Fin 12) :
    IncidenceRegister.visitAction window (visitAt r tick) =
      if IncidenceRegister.inWindow window tick.val && impact (edgeAt r tick) .oddActive
      then (r.multiplicity : Int) else 0 := by
  simp only [IncidenceRegister.visitAction, visitAt_time, visitAt_residue,
    visitAt_multiplicity, actionSupport_impact]

theorem visitAt_vacancy (r : Route) (tick : Fin 108) (window : Fin 12) :
    IncidenceRegister.visitVacancy window (visitAt r tick) =
      if IncidenceRegister.inWindow window tick.val && impact (edgeAt r tick) .nine then
        if r.boundary (edgeAt r tick).after.row (edgeAt r tick).after.column
        then (r.multiplicity : Int) else -(r.multiplicity : Int)
      else 0 := by
  simp [IncidenceRegister.visitVacancy, visitAt_time, visitAt_residue,
    visitAt_multiplicity, visitAt_boundary, impact]

theorem ledger_A_impacts (r : Route) (window : Fin 12) :
    IncidenceRegister.A (ledger r) window =
      ∑ tick : Fin 108,
        if IncidenceRegister.inWindow window tick.val && impact (edgeAt r tick) .oddActive
        then (r.multiplicity : Int) else 0 := by
  change ((List.ofFn (visitAt r)).map (IncidenceRegister.visitAction window)).sum = _
  rw [List.map_ofFn, List.sum_ofFn]
  exact Finset.sum_congr rfl (fun tick _ => visitAt_action r tick window)

theorem ledger_V_boundary_impacts (r : Route) (window : Fin 12) :
    IncidenceRegister.V (ledger r) window =
      ∑ tick : Fin 108,
        if IncidenceRegister.inWindow window tick.val && impact (edgeAt r tick) .nine then
          if r.boundary (edgeAt r tick).after.row (edgeAt r tick).after.column
          then (r.multiplicity : Int) else -(r.multiplicity : Int)
        else 0 := by
  change ((List.ofFn (visitAt r)).map (IncidenceRegister.visitVacancy window)).sum = _
  rw [List.map_ofFn, List.sum_ofFn]
  exact Finset.sum_congr rfl (fun tick _ => visitAt_vacancy r tick window)

def extend (r : Route) (suffix : List (Fin 4)) : Route where
  seed := r.seed
  word := r.word ++ suffix
  multiplicity := r.multiplicity
  multiplicity_positive := r.multiplicity_positive
  word_long := by simpa only [List.length_append] using Nat.le_trans r.word_long (Nat.le_add_right _ _)
  boundary := r.boundary

theorem prefix_extend (r : Route) (suffix : List (Fin 4)) :
    wordPrefix (extend r suffix) = wordPrefix r := by
  exact List.take_append_of_le_length r.word_long

theorem edges_extend (r : Route) (suffix : List (Fin 4)) :
    edges (extend r suffix) = edges r := by
  change walk r.seed (wordPrefix (extend r suffix)) = walk r.seed (wordPrefix r)
  rw [prefix_extend]

theorem edgeAt_extend (r : Route) (suffix : List (Fin 4)) (tick : Fin 108) :
    edgeAt (extend r suffix) tick = edgeAt r tick := by
  simp only [edgeAt, edges_extend]

theorem visitAt_extend (r : Route) (suffix : List (Fin 4)) (tick : Fin 108) :
    visitAt (extend r suffix) tick = visitAt r tick := by
  unfold visitAt
  rw [edgeAt_extend, prefix_extend, edges_extend]
  rfl

theorem visits_extend (r : Route) (suffix : List (Fin 4)) :
    visits (extend r suffix) = visits r := by
  apply congrArg List.ofFn
  funext tick
  exact visitAt_extend r suffix tick

theorem ledger_extend (r : Route) (suffix : List (Fin 4)) :
    ledger (extend r suffix) = ledger r := by
  simp only [ledger, visits_extend]

theorem counts_extend (r : Route) (suffix : List (Fin 4)) (window : Fin 12) :
    IncidenceRegister.A (ledger (extend r suffix)) window = IncidenceRegister.A (ledger r) window ∧
    IncidenceRegister.V (ledger (extend r suffix)) window = IncidenceRegister.V (ledger r) window := by
  rw [ledger_extend]
  exact ⟨rfl, rfl⟩

#print axioms prefix_length
#print axioms edges_length
#print axioms walk_take
#print axioms edges_first108
#print axioms walk_getElem
#print axioms edgeAt_is_step
#print axioms visits_length
#print axioms visits_getElem
#print axioms visitAt_time
#print axioms visitAt_multiplicity
#print axioms visitAt_multiplicity_positive
#print axioms visitAt_boundary
#print axioms visitAt_previous_sheet
#print axioms visitAt_cell
#print axioms visitAt_raw
#print axioms visitAt_residue
#print axioms visitAt_quotient
#print axioms visitAt_reconstruct
#print axioms visitAt_complete_memory
#print axioms visitAt_complete_route
#print axioms actionSupport_impact
#print axioms visitAt_action
#print axioms visitAt_vacancy
#print axioms ledger_A_impacts
#print axioms ledger_V_boundary_impacts
#print axioms prefix_extend
#print axioms edges_extend
#print axioms edgeAt_extend
#print axioms visitAt_extend
#print axioms visits_extend
#print axioms ledger_extend
#print axioms counts_extend

end HMT.N30VisitLedger
