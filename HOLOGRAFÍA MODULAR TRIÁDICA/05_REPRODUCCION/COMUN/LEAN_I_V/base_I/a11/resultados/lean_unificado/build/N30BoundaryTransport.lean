import N30Transport

/-!
Boundary balance on one generated N30 history.  The return occupation is
read from the recorded edges in reverse order; it is not a second freely
chosen direction word.  No numerical terminal register is an input.

APP supplies the additive and multiplicative raw readings. TRIT updates
the operative sheet in N30.step. The TPK realization N30.walk preserves
each edge, its residue, quotient, previous sheet and updated sheet.
The causal cutoff of these finite identities is the enriched trajectory.
-/
namespace HMT.N30.Boundary

def beforeOccupation (f : State → Int) (edges : List Edge) : Int :=
  (edges.map (fun e => f e.before)).sum

def afterOccupation (f : State → Int) (edges : List Edge) : Int :=
  (edges.map (fun e => f e.after)).sum

/-- The second orientation reads the same recorded edges from the endpoint. -/
def returnOccupation (f : State → Int) (edges : List Edge) : Int :=
  afterOccupation f edges.reverse

theorem return_eq_after (f : State → Int) (edges : List Edge) :
    returnOccupation f edges = afterOccupation f edges := by
  simp [returnOccupation, afterOccupation, List.map_reverse]

theorem occupation_boundary (f : State → Int) (s : State) (word : List (Fin 4)) :
    afterOccupation f (walk s word) - beforeOccupation f (walk s word) =
      f (finish s word) - f s := by
  induction word generalizing s with
  | nil => simp [walk, finish, beforeOccupation, afterOccupation]
  | cons d ds ih =>
      have h := ih (step s d).after
      simp only [walk, finish, beforeOccupation, afterOccupation,
        List.map_cons, List.sum_cons, step_before] at *
      omega

theorem return_boundary (f : State → Int) (s : State) (word : List (Fin 4)) :
    returnOccupation f (walk s word) = beforeOccupation f (walk s word) +
      f (finish s word) - f s := by
  rw [return_eq_after]
  have h := occupation_boundary f s word
  omega

theorem before_append (f : State → Int) (s : State) (u v : List (Fin 4)) :
    beforeOccupation f (walk s (u ++ v)) =
      beforeOccupation f (walk s u) + beforeOccupation f (walk (finish s u) v) := by
  simp [walk_append, beforeOccupation]

theorem after_append (f : State → Int) (s : State) (u v : List (Fin 4)) :
    afterOccupation f (walk s (u ++ v)) =
      afterOccupation f (walk s u) + afterOccupation f (walk (finish s u) v) := by
  simp [walk_append, afterOccupation]

theorem boundary_cocycle (f : State → Int) (s : State) (u v : List (Fin 4)) :
    f (finish s (u ++ v)) - f s =
      (f (finish s u) - f s) +
        (f (finish (finish s u) v) - f (finish s u)) := by
  rw [finish_append]
  ring

/-- Boundary vanishes exactly when this observable, not merely phase, returns. -/
theorem equal_occupations_iff (f : State → Int) (s : State) (word : List (Fin 4)) :
    returnOccupation f (walk s word) = beforeOccupation f (walk s word) ↔
      f (finish s word) = f s := by
  rw [return_boundary]
  omega

def potential (s : State) : Int := rawRead s.sheet s.row s.column

def spatialIncrement (e : Edge) : Int := (e.raw : Int) - potential e.before

def sheetDefect (e : Edge) : Int := potential e.after - (e.raw : Int)

def spatialSum (edges : List Edge) : Int := (edges.map spatialIncrement).sum

def sheetSum (edges : List Edge) : Int := (edges.map sheetDefect).sum

theorem edge_balance (e : Edge) :
    spatialIncrement e + sheetDefect e = potential e.after - potential e.before := by
  unfold spatialIncrement sheetDefect
  ring

theorem sum_balance (edges : List Edge) :
    spatialSum edges + sheetSum edges =
      afterOccupation potential edges - beforeOccupation potential edges := by
  induction edges with
  | nil => simp [spatialSum, sheetSum, afterOccupation, beforeOccupation]
  | cons e es ih =>
      have he := edge_balance e
      simp only [spatialSum, sheetSum, afterOccupation, beforeOccupation,
        List.map_cons, List.sum_cons] at *
      omega

theorem trajectory_balance (s : State) (word : List (Fin 4)) :
    spatialSum (walk s word) + sheetSum (walk s word) =
      potential (finish s word) - potential s := by
  rw [sum_balance, occupation_boundary]

theorem sheetDefect_same_sheet (s : State) (d : Fin 4)
    (h : (step s d).after.sheet = s.sheet) : sheetDefect (step s d) = 0 := by
  unfold sheetDefect potential
  rw [h]
  change ((step s d).raw : Int) - (step s d).raw = 0
  exact sub_self _

theorem step_previous_sheet (s : State) (d : Fin 4) :
    (step s d).raw = rawRead s.sheet (step s d).after.row (step s d).after.column := rfl

theorem residue_quotient_spatial (s : State) (d : Fin 4) :
    spatialIncrement (step s d) =
      (step s d).digit + 9 * (step s d).quotient9 - potential s := by
  have h := step_reconstruct s d
  have hz : ((step s d).raw : Int) = (step s d).digit + 9 * (step s d).quotient9 := by
    exact_mod_cast h
  unfold spatialIncrement
  rw [step_before, hz]

theorem residue_quotient_sheet (s : State) (d : Fin 4) :
    sheetDefect (step s d) = potential (step s d).after -
      ((step s d).digit + 9 * (step s d).quotient9) := by
  have h := step_reconstruct s d
  have hz : ((step s d).raw : Int) = (step s d).digit + 9 * (step s d).quotient9 := by
    exact_mod_cast h
  unfold sheetDefect
  rw [hz]

theorem spatial_append (s : State) (u v : List (Fin 4)) :
    spatialSum (walk s (u ++ v)) =
      spatialSum (walk s u) + spatialSum (walk (finish s u) v) := by
  simp [walk_append, spatialSum]

theorem sheet_append (s : State) (u v : List (Fin 4)) :
    sheetSum (walk s (u ++ v)) =
      sheetSum (walk s u) + sheetSum (walk (finish s u) v) := by
  simp [walk_append, sheetSum]

/-- One nine-step block returns phase and extends the same chronological memory. -/
theorem nine_step_balance (x : Enriched) (word : List (Fin 4)) (h : word.length = 9) :
    (transport x word).state.phase = x.state.phase ∧
    (transport x word).memory.length = x.memory.length + 9 ∧
    transport x word ≠ x ∧
    spatialSum (walk x.state word) + sheetSum (walk x.state word) =
      potential (transport x word).state - potential x.state := by
  have hnonempty : word ≠ [] := by
    intro he
    simp [he] at h
  refine ⟨?_, ?_, nonempty_transport_not_reset x word hnonempty, ?_⟩
  · exact phase_return x.state word (by omega)
  · simpa [h] using transport_memory_length x word
  · exact trajectory_balance x.state word

/-- A faithful return of the stored trajectory recovers its initial state. -/
theorem same_history_return (s : State) (word : List (Fin 4)) :
    rewind (finish s word) (walk s word) = some s ∧
    returnOccupation potential (walk s word) =
      beforeOccupation potential (walk s word) + potential (finish s word) - potential s :=
  ⟨rewind_walk s word, return_boundary potential s word⟩

/-- A boundary identity is preserved before decimal reduction. -/
theorem boundary_mod_ten (f : State → Int) (s : State) (word : List (Fin 4)) :
    (returnOccupation f (walk s word) - beforeOccupation f (walk s word)) % 10 =
      (f (finish s word) - f s) % 10 := by
  rw [return_eq_after, occupation_boundary]

def boundaryWitness : State := ⟨0, 8, 0, 0, 0⟩
def northNine : List (Fin 4) := List.replicate 9 0

/-- An exact route witness, not a numerical target for a terminal selector. -/
theorem phase_return_with_nonzero_boundary :
    finish boundaryWitness northNine = (⟨0, 8, 1, 0, 0⟩ : State) ∧
    potential boundaryWitness = 10 ∧
    potential (finish boundaryWitness northNine) = 9 ∧
    spatialSum (walk boundaryWitness northNine) = -56 ∧
    sheetSum (walk boundaryWitness northNine) = 55 := by
  decide

theorem witness_occupation_asymmetry :
    returnOccupation potential (walk boundaryWitness northNine) =
      beforeOccupation potential (walk boundaryWitness northNine) - 1 := by
  have h := phase_return_with_nonzero_boundary
  rw [return_boundary, h.2.1, h.2.2.1]
  omega

theorem witness_residue_quotient_change :
    APPArithmetic.rho9 (rawRead boundaryWitness.sheet boundaryWitness.row boundaryWitness.column) = 1 ∧
    APPArithmetic.q9 (rawRead boundaryWitness.sheet boundaryWitness.row boundaryWitness.column) = 1 ∧
    APPArithmetic.rho9 (rawRead (finish boundaryWitness northNine).sheet
      (finish boundaryWitness northNine).row (finish boundaryWitness northNine).column) = 9 ∧
    APPArithmetic.q9 (rawRead (finish boundaryWitness northNine).sheet
      (finish boundaryWitness northNine).row (finish boundaryWitness northNine).column) = 0 := by
  decide

end HMT.N30.Boundary

#print axioms HMT.N30.Boundary.return_boundary
#print axioms HMT.N30.Boundary.boundary_cocycle
#print axioms HMT.N30.Boundary.equal_occupations_iff
#print axioms HMT.N30.Boundary.trajectory_balance
#print axioms HMT.N30.Boundary.sheetDefect_same_sheet
#print axioms HMT.N30.Boundary.residue_quotient_spatial
#print axioms HMT.N30.Boundary.residue_quotient_sheet
#print axioms HMT.N30.Boundary.nine_step_balance
#print axioms HMT.N30.Boundary.same_history_return
#print axioms HMT.N30.Boundary.boundary_mod_ten
#print axioms HMT.N30.Boundary.phase_return_with_nonzero_boundary
#print axioms HMT.N30.Boundary.witness_occupation_asymmetry
#print axioms HMT.N30.Boundary.witness_residue_quotient_change
