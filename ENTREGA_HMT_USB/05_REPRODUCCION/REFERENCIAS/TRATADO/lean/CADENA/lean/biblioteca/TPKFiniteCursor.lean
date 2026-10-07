import TPKEmission

/-
Finite observable cursor factor for the declared finite emitter.
This is a quotient by spatial winding, not a replacement for enriched memory.
The square with integer transport and the emission readers is proved for
every natural iteration length; catalogue cardinalities are not assumptions.
-/
namespace TPKFiniteCursor

open TPKTransport

structure FiniteCursor where
  x : Fin 9
  y : Fin 9
  direction : Direction
  deriving DecidableEq, Repr

abbrev State := FiniteCursor × Phase

def projectCursor (c : TPKTransport.Cursor) : FiniteCursor :=
  ⟨CommonComposition.cursorMark c.x, CommonComposition.cursorMark c.y, c.direction⟩

def liftCursor (c : FiniteCursor) : TPKTransport.Cursor :=
  ⟨(c.x.val : Int), (c.y.val : Int), c.direction⟩

def addCoord (x : Fin 9) (delta : Nat) : Fin 9 :=
  ⟨(x.val + delta) % 9, Nat.mod_lt _ (by decide)⟩

def xOffset : Direction → Nat
  | .north => 8
  | .south => 1
  | _ => 0

def yOffset : Direction → Nat
  | .east => 1
  | .west => 8
  | _ => 0

def stepCursor (s : Sheet) (p : Phase) (c : FiniteCursor) : FiniteCursor :=
  ⟨if active s p then addCoord c.x (xOffset c.direction) else c.x,
   if active s p then addCoord c.y (yOffset c.direction) else c.y,
   orient (halfTurn p) c.direction⟩

def step (s : Sheet) (q : State) : State :=
  (stepCursor s q.2 q.1, nextPhase q.2)

theorem finiteCursor_ext (a b : FiniteCursor)
    (hx : a.x = b.x) (hy : a.y = b.y) (hd : a.direction = b.direction) : a = b := by
  cases a
  cases b
  cases hx
  cases hy
  cases hd
  rfl

theorem mark_add_x (z : Int) (d : Direction) :
    CommonComposition.cursorMark (z + dx d) =
      addCoord (CommonComposition.cursorMark z) (xOffset d) := by
  cases d <;> apply Fin.ext <;> dsimp [CommonComposition.cursorMark, addCoord, dx, xOffset] <;>
    omega

theorem mark_add_y (z : Int) (d : Direction) :
    CommonComposition.cursorMark (z + dy d) =
      addCoord (CommonComposition.cursorMark z) (yOffset d) := by
  cases d <;> apply Fin.ext <;> dsimp [CommonComposition.cursorMark, addCoord, dy, yOffset] <;>
    omega

theorem mark_lift (x : Fin 9) : CommonComposition.cursorMark (x.val : Int) = x := by
  apply Fin.ext
  have hx := x.isLt
  dsimp [CommonComposition.cursorMark]
  omega

theorem project_lift (c : FiniteCursor) : projectCursor (liftCursor c) = c := by
  apply finiteCursor_ext
  · exact mark_lift c.x
  · exact mark_lift c.y
  · rfl

theorem project_direction (c : TPKTransport.Cursor) :
    (projectCursor c).direction = c.direction := rfl

theorem step_direction (s : Sheet) (p : Phase) (c : FiniteCursor) :
    (stepCursor s p c).direction = orient (halfTurn p) c.direction := rfl

theorem step_phase (s : Sheet) (q : State) : (step s q).2 = nextPhase q.2 := rfl

theorem project_stepCursor (s : Sheet) (p : Phase) (c : TPKTransport.Cursor) :
    projectCursor (TPKTransport.stepCursor s p c) = stepCursor s p (projectCursor c) := by
  cases h : active s p
  · apply finiteCursor_ext <;>
      simp [projectCursor, TPKTransport.stepCursor, stepCursor, h]
  · apply finiteCursor_ext
    · simpa [projectCursor, TPKTransport.stepCursor, stepCursor, h] using mark_add_x c.x c.direction
    · simpa [projectCursor, TPKTransport.stepCursor, stepCursor, h] using mark_add_y c.y c.direction
    · rfl

def chooseCursor (s : Sheet) (q : ObservableLift) : TPKTransport.Cursor :=
  match s with | .additive => q.plus | .multiplicative => q.times

def projectState (s : Sheet) (q : ObservableLift) : State :=
  (projectCursor (chooseCursor s q), q.phase)

theorem projectState_phase (s : Sheet) (q : ObservableLift) :
    (projectState s q).2 = q.phase := rfl

theorem projectState_step (s : Sheet) (q : ObservableLift) :
    projectState s (TPKTransport.step q) = step s (projectState s q) := by
  cases s <;>
    simp only [projectState, chooseCursor, TPKTransport.step, step, project_stepCursor]

theorem projectState_iterate (s : Sheet) (n : Nat) (q : ObservableLift) :
    projectState s (iterate TPKTransport.step n q) =
      iterate (step s) n (projectState s q) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [iterate, projectState_step, ih, iterate]

structure FiniteObservable where
  plus : FiniteCursor
  times : FiniteCursor
  phase : Phase
  deriving DecidableEq, Repr

def project (q : ObservableLift) : FiniteObservable :=
  ⟨projectCursor q.plus, projectCursor q.times, q.phase⟩

def jointStep (q : FiniteObservable) : FiniteObservable :=
  ⟨stepCursor .additive q.phase q.plus, stepCursor .multiplicative q.phase q.times,
   nextPhase q.phase⟩

theorem project_step (q : ObservableLift) :
    project (TPKTransport.step q) = jointStep (project q) := by
  simp only [project, TPKTransport.step, jointStep, project_stepCursor]

theorem project_iterate (n : Nat) (q : ObservableLift) :
    project (iterate TPKTransport.step n q) = iterate jointStep n (project q) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [iterate, project_step, ih, iterate]

def arithmetic (c : FiniteCursor) : APPArithmetic.PairedEvaluation :=
  APPArithmetic.evaluate c.x c.y

theorem arithmetic_project (c : TPKTransport.Cursor) :
    arithmetic (projectCursor c) = CommonComposition.readCursor c := rfl

-- Read before stepping, as specified in extension.tex.
def reading (s : Sheet) (q : State) : Nat :=
  match s with
  | .additive =>
    if TPKEmission.classify q.2 = .additive then (arithmetic q.1).additive.residue else 0
  | .multiplicative =>
    if TPKEmission.classify q.2 = .multiplicative then
      TPKEmission.log9 (arithmetic q.1).multiplicative.residue else 0

def sourceReading (s : Sheet) (q : ObservableLift) : Nat :=
  match s with
  | .additive => TPKEmission.additiveReading (TPKEmission.sample q)
  | .multiplicative => TPKEmission.exponentReading (TPKEmission.sample q)

theorem reading_project (s : Sheet) (q : ObservableLift) :
    reading s (projectState s q) = sourceReading s q := by cases s <;> rfl

theorem reading_at_depth (s : Sheet) (n : Nat) (q : ObservableLift) :
    reading s (iterate (step s) n (projectState s q)) =
      sourceReading s (iterate TPKTransport.step n q) := by
  rw [← projectState_iterate]
  exact reading_project s _

def sumReadings (s : Sheet) : Nat → State → Nat
  | 0, _ => 0
  | n + 1, q => sumReadings s n q + reading s (iterate (step s) n q)

def sourceSum (s : Sheet) (n : Nat) (q : ObservableLift) : Nat :=
  match s with
  | .additive => (TPKEmission.totals (TPKEmission.samples n q)).s
  | .multiplicative => (TPKEmission.totals (TPKEmission.samples n q)).e

theorem sourceSum_succ (s : Sheet) (n : Nat) (q : ObservableLift) :
    sourceSum s (n + 1) q = sourceSum s n q +
      sourceReading s (iterate TPKTransport.step n q) := by
  cases s <;>
    simp [sourceSum, sourceReading, TPKEmission.samples, TPKEmission.totals,
      List.map_append, TPKEmission.sum_append]

theorem sumReadings_project (s : Sheet) (n : Nat) (q : ObservableLift) :
    sumReadings s n (projectState s q) = sourceSum s n q := by
  induction n with
  | zero => cases s <;> rfl
  | succ n ih => rw [sumReadings, ih, reading_at_depth, sourceSum_succ]

def window (s : Sheet) (q : State) : Nat := sumReadings s 9 q

def sourceWindow (s : Sheet) (q : ObservableLift) : Nat :=
  match s with
  | .additive => (TPKEmission.window q).s
  | .multiplicative => (TPKEmission.window q).e

theorem window_project (s : Sheet) (q : ObservableLift) :
    window s (projectState s q) = sourceWindow s q := sumReadings_project s 9 q

theorem window_at_depth (s : Sheet) (n : Nat) (q : ObservableLift) :
    window s (iterate (step s) n (projectState s q)) =
      sourceWindow s (iterate TPKTransport.step n q) := by
  rw [← projectState_iterate]
  exact window_project s _

def signatureVector (s : Sheet) (q : State) : EmissionCode.Signature :=
  fun j => EmissionCode.ofNat (window s (iterate (step s) (9 * j.val) q))

def signatureAt (s : Sheet) (q : State) : List Nat :=
  (List.finRange 6).map (fun j => (signatureVector s q j).val)

def initialPhase : Phase := ⟨0, by decide⟩

def signature (s : Sheet) (seed : FiniteCursor) : List Nat :=
  signatureAt s (seed, initialPhase)

def sourceSignature (s : Sheet) (q : ObservableLift) : EmissionCode.Signature :=
  match s with
  | .additive => TPKEmission.additiveSignature q
  | .multiplicative => TPKEmission.exponentSignature q

theorem signatureVector_project (s : Sheet) (q : ObservableLift) :
    signatureVector s (projectState s q) = sourceSignature s q := by
  funext j
  unfold signatureVector
  rw [window_at_depth]
  cases s <;> rfl

theorem signatureAt_project (s : Sheet) (q : ObservableLift) :
    signatureAt s (projectState s q) =
      (List.finRange 6).map (fun j => (sourceSignature s q j).val) := by
  unfold signatureAt
  rw [signatureVector_project]

theorem signatureAt_length (s : Sheet) (q : State) : (signatureAt s q).length = 6 := by
  simp [signatureAt]

theorem signature_length (s : Sheet) (seed : FiniteCursor) :
    (signature s seed).length = 6 := signatureAt_length s _

def seedObservable (plus times : FiniteCursor) : ObservableLift :=
  ⟨liftCursor plus, liftCursor times, initialPhase⟩

theorem project_seed_additive (plus times : FiniteCursor) :
    projectState .additive (seedObservable plus times) = (plus, initialPhase) := by
  simp [projectState, seedObservable, chooseCursor, project_lift]

theorem project_seed_multiplicative (plus times : FiniteCursor) :
    projectState .multiplicative (seedObservable plus times) = (times, initialPhase) := by
  simp [projectState, seedObservable, chooseCursor, project_lift]

theorem signatures_two_cursor (plus times : FiniteCursor) :
    signature .additive plus = (List.finRange 6).map
      (fun j => (TPKEmission.additiveSignature (seedObservable plus times) j).val) ∧
    signature .multiplicative times = (List.finRange 6).map
      (fun j => (TPKEmission.exponentSignature (seedObservable plus times) j).val) := by
  constructor
  · have h := signatureAt_project .additive (seedObservable plus times)
    rw [project_seed_additive] at h
    exact h
  · have h := signatureAt_project .multiplicative (seedObservable plus times)
    rw [project_seed_multiplicative] at h
    exact h

-- The finite factors can be coupled without enumerating the product seed set.
theorem word_from_finite_factors (q : ObservableLift) :
    TPKEmission.word q = EmissionCode.encodeWord
      (signatureVector .additive (projectState .additive q))
      (signatureVector .multiplicative (projectState .multiplicative q)) := by
  rw [signatureVector_project, signatureVector_project]
  exact TPKEmission.word_as_encodeWord q

-- Tail execution computes each transition once.  It is an implementation of
-- the same reader, not an independent emitter or a precomputed catalogue.
def runTicks (s : Sheet) : Nat → State → Nat → Nat × State
  | 0, q, acc => (acc, q)
  | n + 1, q, acc => runTicks s n (step s q) (acc + reading s q)

theorem iterate_succ_start {α : Type} (f : α → α) (n : Nat) (q : α) :
    iterate f (n + 1) q = iterate f n (f q) := by
  rw [Nat.add_comm n 1, iterate_add]
  rfl

theorem sumReadings_shift (s : Sheet) (n : Nat) (q : State) :
    sumReadings s (n + 1) q = reading s q + sumReadings s n (step s q) := by
  induction n with
  | zero => simp [sumReadings, iterate]
  | succ n ih =>
    rw [sumReadings, ih, iterate_succ_start, sumReadings]
    exact Nat.add_assoc _ _ _

theorem runTicks_correct (s : Sheet) (n : Nat) (q : State) (acc : Nat) :
    runTicks s n q acc = (acc + sumReadings s n q, iterate (step s) n q) := by
  induction n generalizing q acc with
  | zero => simp [runTicks, sumReadings, iterate]
  | succ n ih =>
    rw [runTicks, ih, sumReadings_shift, iterate_succ_start, Nat.add_assoc]

def fastWindow (s : Sheet) (q : State) : Nat × State := runTicks s 9 q 0

theorem fastWindow_correct (s : Sheet) (q : State) :
    fastWindow s q = (window s q, iterate (step s) 9 q) := by
  simp [fastWindow, runTicks_correct, window]

def runWindows (s : Sheet) : Nat → State → List Nat
  | 0, _ => []
  | n + 1, q =>
    match fastWindow s q with
    | (total, next) => total % 10 :: runWindows s n next

theorem runWindows_range (s : Sheet) (n : Nat) (q : State) :
    runWindows s n q = (List.range n).map
      (fun j => window s (iterate (step s) (9 * j) q) % 10) := by
  induction n generalizing q with
  | zero => rfl
  | succ n ih =>
    rw [runWindows, fastWindow_correct]
    dsimp only
    rw [ih, List.range_succ_eq_map, List.map_cons,
      List.map_map]
    apply congrArg (List.cons (window s q % 10))
    apply List.map_congr_left
    intro j _
    apply congrArg (fun next => window s next % 10)
    rw [← iterate_add]
    exact congrArg (fun k => iterate (step s) k q) (by omega)

def signatureFast (s : Sheet) (seed : FiniteCursor) : List Nat :=
  runWindows s 6 (seed, initialPhase)

theorem signatureFast_eq (s : Sheet) (seed : FiniteCursor) :
    signatureFast s seed = signature s seed := by
  rw [signatureFast, runWindows_range]
  rfl

end TPKFiniteCursor

#print axioms TPKFiniteCursor.finiteCursor_ext
#print axioms TPKFiniteCursor.mark_add_x
#print axioms TPKFiniteCursor.mark_add_y
#print axioms TPKFiniteCursor.mark_lift
#print axioms TPKFiniteCursor.project_lift
#print axioms TPKFiniteCursor.project_direction
#print axioms TPKFiniteCursor.step_direction
#print axioms TPKFiniteCursor.step_phase
#print axioms TPKFiniteCursor.project_stepCursor
#print axioms TPKFiniteCursor.projectState_phase
#print axioms TPKFiniteCursor.projectState_step
#print axioms TPKFiniteCursor.projectState_iterate
#print axioms TPKFiniteCursor.project_step
#print axioms TPKFiniteCursor.project_iterate
#print axioms TPKFiniteCursor.arithmetic_project
#print axioms TPKFiniteCursor.reading_project
#print axioms TPKFiniteCursor.reading_at_depth
#print axioms TPKFiniteCursor.sourceSum_succ
#print axioms TPKFiniteCursor.sumReadings_project
#print axioms TPKFiniteCursor.window_project
#print axioms TPKFiniteCursor.window_at_depth
#print axioms TPKFiniteCursor.signatureVector_project
#print axioms TPKFiniteCursor.signatureAt_project
#print axioms TPKFiniteCursor.signatureAt_length
#print axioms TPKFiniteCursor.signature_length
#print axioms TPKFiniteCursor.project_seed_additive
#print axioms TPKFiniteCursor.project_seed_multiplicative
#print axioms TPKFiniteCursor.signatures_two_cursor
#print axioms TPKFiniteCursor.word_from_finite_factors
#print axioms TPKFiniteCursor.iterate_succ_start
#print axioms TPKFiniteCursor.sumReadings_shift
#print axioms TPKFiniteCursor.runTicks_correct
#print axioms TPKFiniteCursor.fastWindow_correct
#print axioms TPKFiniteCursor.runWindows_range
#print axioms TPKFiniteCursor.signatureFast_eq
