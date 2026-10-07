import TPKSimpleRegions

/-!
Unique reconstruction of the two finite lifts from the printed X/Y records.
The records are explicit starting structure, not a claim that this module
produces them from Sel/Tra/Upd.  L0/L1 are solutions computed from those records.
-/
namespace TPKLifts
open TPKOrbits
set_option maxRecDepth 1000000
set_option maxHeartbeats 0

def Ternary (w : Word) : Prop :=
  w.a < 3 ∧ w.b < 3 ∧ w.c < 3 ∧ w.d < 3 ∧ w.e < 3 ∧ w.f < 3

def allWords : List Word :=
  (List.range 3).flatMap fun a => (List.range 3).flatMap fun b =>
  (List.range 3).flatMap fun c => (List.range 3).flatMap fun d =>
  (List.range 3).flatMap fun e => (List.range 3).map fun f => ⟨a,b,c,d,e,f⟩

theorem allWords_complete (w : Word) (h : Ternary w) : w ∈ allWords := by
  rcases w with ⟨a,b,c,d,e,f⟩
  rcases h with ⟨ha,hb,hc,hd,he,hf⟩
  simp only [allWords, List.mem_flatMap, List.mem_map, List.mem_range]
  exact ⟨a,ha,b,hb,c,hc,d,hd,e,he,f,hf,rfl⟩

theorem allWords_cardinality : allWords.length = 729 := by decide +kernel

def component (w : Word) (j : Fin 6) : Nat :=
  match j.val with
  | 0 => w.a | 1 => w.b | 2 => w.c | 3 => w.d | 4 => w.e | _ => w.f

structure Matrix where
  r0 : Word
  r1 : Word
  r2 : Word
  r3 : Word
  r4 : Word
  r5 : Word
  deriving DecidableEq, Repr

def column (M : Matrix) (j : Fin 6) : Word :=
  ⟨component M.r0 j, component M.r1 j, component M.r2 j,
   component M.r3 j, component M.r4 j, component M.r5 j⟩

def fromColumns (a b c d e f : Word) : Matrix :=
  ⟨⟨a.a,b.a,c.a,d.a,e.a,f.a⟩, ⟨a.b,b.b,c.b,d.b,e.b,f.b⟩,
   ⟨a.c,b.c,c.c,d.c,e.c,f.c⟩, ⟨a.d,b.d,c.d,d.d,e.d,f.d⟩,
   ⟨a.e,b.e,c.e,d.e,e.e,f.e⟩, ⟨a.f,b.f,c.f,d.f,e.f,f.f⟩⟩

theorem fromColumns_column (M : Matrix) :
    fromColumns (column M ⟨0,by decide⟩) (column M ⟨1,by decide⟩)
      (column M ⟨2,by decide⟩) (column M ⟨3,by decide⟩)
      (column M ⟨4,by decide⟩) (column M ⟨5,by decide⟩) = M := by
  cases M
  rfl

theorem matrix_ext_columns (A B : Matrix)
    (h : ∀ j : Fin 6, column A j = column B j) : A = B := by
  calc
    A = fromColumns (column A ⟨0,by decide⟩) (column A ⟨1,by decide⟩)
      (column A ⟨2,by decide⟩) (column A ⟨3,by decide⟩)
      (column A ⟨4,by decide⟩) (column A ⟨5,by decide⟩) := (fromColumns_column A).symm
    _ = fromColumns (column B ⟨0,by decide⟩) (column B ⟨1,by decide⟩)
      (column B ⟨2,by decide⟩) (column B ⟨3,by decide⟩)
      (column B ⟨4,by decide⟩) (column B ⟨5,by decide⟩) := by
        rw [h,h,h,h,h,h]
    _ = B := fromColumns_column B

def dot (u v : Word) : Nat :=
  (u.a*v.a + u.b*v.b + u.c*v.c + u.d*v.d + u.e*v.e + u.f*v.f) % 3
def applyColumn (M : Matrix) (v : Word) : Word :=
  ⟨dot M.r0 v, dot M.r1 v, dot M.r2 v, dot M.r3 v, dot M.r4 v, dot M.r5 v⟩
def rowAction (v : Word) (M : Matrix) : Word :=
  ⟨dot v (column M ⟨0,by decide⟩), dot v (column M ⟨1,by decide⟩),
   dot v (column M ⟨2,by decide⟩), dot v (column M ⟨3,by decide⟩),
   dot v (column M ⟨4,by decide⟩), dot v (column M ⟨5,by decide⟩)⟩

theorem rowAction_ternary (v : Word) (M : Matrix) : Ternary (rowAction v M) := by
  exact ⟨Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide),
    Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide)⟩

def mul (A B : Matrix) : Matrix :=
  fromColumns (applyColumn A (column B ⟨0,by decide⟩)) (applyColumn A (column B ⟨1,by decide⟩))
    (applyColumn A (column B ⟨2,by decide⟩)) (applyColumn A (column B ⟨3,by decide⟩))
    (applyColumn A (column B ⟨4,by decide⟩)) (applyColumn A (column B ⟨5,by decide⟩))

theorem column_mul (A B : Matrix) (j : Fin 6) :
    column (mul A B) j = applyColumn A (column B j) := by
  rcases j with ⟨j,hj⟩
  have h : j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 ∨ j = 5 := by omega
  rcases h with h|h|h|h|h|h <;> subst j <;> rfl

def identity : Matrix :=
  ⟨⟨1,0,0,0,0,0⟩,⟨0,1,0,0,0,0⟩,⟨0,0,1,0,0,0⟩,
   ⟨0,0,0,1,0,0⟩,⟨0,0,0,0,1,0⟩,⟨0,0,0,0,0,1⟩⟩

/- The four published transition records, preserved row-for-row. -/
def X0 : Matrix := ⟨⟨0, 1, 0, 2, 1, 1⟩,
   ⟨0, 1, 2, 2, 2, 2⟩,
   ⟨2, 0, 1, 1, 0, 1⟩,
   ⟨1, 2, 1, 2, 2, 1⟩,
   ⟨1, 2, 1, 2, 0, 0⟩,
   ⟨1, 1, 2, 2, 0, 2⟩⟩
def Y0 : Matrix := ⟨⟨0, 1, 2, 2, 2, 2⟩,
   ⟨0, 1, 0, 2, 1, 1⟩,
   ⟨1, 2, 1, 2, 2, 1⟩,
   ⟨1, 0, 2, 0, 1, 1⟩,
   ⟨1, 1, 2, 2, 0, 2⟩,
   ⟨1, 2, 1, 0, 2, 0⟩⟩
def X1 : Matrix := ⟨⟨0, 1, 0, 2, 1, 1⟩,
   ⟨0, 0, 2, 1, 1, 1⟩,
   ⟨1, 0, 2, 0, 1, 1⟩,
   ⟨0, 1, 2, 2, 2, 2⟩,
   ⟨1, 2, 1, 0, 2, 0⟩,
   ⟨0, 1, 0, 2, 1, 0⟩⟩
def Y1 : Matrix := ⟨⟨0, 0, 2, 1, 1, 1⟩,
   ⟨1, 1, 0, 2, 2, 1⟩,
   ⟨0, 1, 2, 2, 2, 2⟩,
   ⟨1, 0, 2, 0, 1, 1⟩,
   ⟨0, 1, 0, 2, 1, 0⟩,
   ⟨0, 1, 0, 2, 0, 0⟩⟩

/-- Exhaustive exact solving over the full finite domain; no target lift is supplied. -/
def solveColumn (X : Matrix) (y : Word) : Word :=
  (allWords.filter (fun v => applyColumn X v == y)).headD ⟨0,0,0,0,0,0⟩
def solveMatrix (X Y : Matrix) : Matrix :=
  fromColumns (solveColumn X (column Y ⟨0,by decide⟩)) (solveColumn X (column Y ⟨1,by decide⟩))
    (solveColumn X (column Y ⟨2,by decide⟩)) (solveColumn X (column Y ⟨3,by decide⟩))
    (solveColumn X (column Y ⟨4,by decide⟩)) (solveColumn X (column Y ⟨5,by decide⟩))

def L0 : Matrix := solveMatrix X0 Y0
def L1 : Matrix := solveMatrix X1 Y1

/- Posterior normal forms, checked against the solver. -/
def L0Witness : Matrix := ⟨⟨2, 2, 2, 1, 2, 1⟩,
   ⟨2, 1, 2, 2, 1, 1⟩,
   ⟨1, 0, 0, 1, 0, 2⟩,
   ⟨0, 0, 1, 1, 1, 0⟩,
   ⟨2, 2, 2, 0, 2, 1⟩,
   ⟨2, 1, 2, 1, 0, 0⟩⟩
def L1Witness : Matrix := ⟨⟨2, 1, 2, 0, 2, 2⟩,
   ⟨1, 2, 1, 1, 2, 0⟩,
   ⟨1, 2, 1, 1, 1, 2⟩,
   ⟨0, 1, 0, 0, 2, 1⟩,
   ⟨2, 0, 2, 1, 0, 1⟩,
   ⟨0, 2, 2, 2, 1, 1⟩⟩

theorem L0_reconstructed : L0 = L0Witness := by decide +kernel
theorem L1_reconstructed : L1 = L1Witness := by decide +kernel

theorem transition_equations : mul X0 L0 = Y0 ∧ mul X1 L1 = Y1 := by
  rw [L0_reconstructed,L1_reconstructed]
  decide +kernel

theorem X0_column_unique_checked : ∀ j : Fin 6, ∀ v ∈ allWords,
    applyColumn X0 v = column Y0 j → v = column L0 j := by
  rw [L0_reconstructed]
  decide +kernel

theorem X1_column_unique_checked : ∀ j : Fin 6, ∀ v ∈ allWords,
    applyColumn X1 v = column Y1 j → v = column L1 j := by
  rw [L1_reconstructed]
  decide +kernel

def TernaryMatrix (M : Matrix) : Prop := ∀ j : Fin 6, Ternary (column M j)

theorem reconstructed_lifts_ternary : TernaryMatrix L0 ∧ TernaryMatrix L1 := by
  rw [L0_reconstructed,L1_reconstructed]
  unfold TernaryMatrix Ternary
  decide +kernel

theorem L0_unique (M : Matrix) (hm : TernaryMatrix M) (heq : mul X0 M = Y0) : M = L0 := by
  apply matrix_ext_columns
  intro j
  apply X0_column_unique_checked j (column M j) (allWords_complete _ (hm j))
  have h := congrArg (fun A => column A j) heq
  change column (mul X0 M) j = column Y0 j at h
  rw [column_mul] at h
  exact h

theorem L1_unique (M : Matrix) (hm : TernaryMatrix M) (heq : mul X1 M = Y1) : M = L1 := by
  apply matrix_ext_columns
  intro j
  apply X1_column_unique_checked j (column M j) (allWords_complete _ (hm j))
  have h := congrArg (fun A => column A j) heq
  change column (mul X1 M) j = column Y1 j at h
  rw [column_mul] at h
  exact h

def inverseX0 : Matrix := ⟨⟨1, 1, 2, 0, 1, 2⟩,
   ⟨0, 0, 1, 0, 0, 1⟩,
   ⟨2, 1, 2, 1, 0, 1⟩,
   ⟨0, 2, 0, 1, 0, 2⟩,
   ⟨2, 1, 1, 0, 2, 2⟩,
   ⟨2, 1, 1, 1, 1, 2⟩⟩
def inverseX1 : Matrix := ⟨⟨1, 0, 1, 2, 0, 0⟩,
   ⟨0, 0, 1, 1, 2, 2⟩,
   ⟨0, 1, 2, 0, 1, 1⟩,
   ⟨1, 1, 0, 2, 0, 0⟩,
   ⟨1, 1, 2, 1, 1, 2⟩,
   ⟨1, 0, 0, 0, 0, 2⟩⟩

theorem record_inverses_checked :
    mul inverseX0 X0 = identity ∧ mul X0 inverseX0 = identity ∧
    mul inverseX1 X1 = identity ∧ mul X1 inverseX1 = identity := by decide +kernel

theorem reconstruction_inverse_formula :
    L0 = mul inverseX0 Y0 ∧ L1 = mul inverseX1 Y1 := by
  rw [L0_reconstructed,L1_reconstructed]
  decide +kernel

def inverseL0 : Matrix := ⟨⟨1, 2, 0, 2, 0, 2⟩,
   ⟨2, 0, 2, 2, 0, 0⟩,
   ⟨2, 1, 2, 0, 2, 0⟩,
   ⟨1, 0, 0, 0, 2, 0⟩,
   ⟨0, 2, 1, 1, 2, 0⟩,
   ⟨2, 2, 2, 2, 2, 2⟩⟩
def inverseL1 : Matrix := ⟨⟨2, 0, 2, 1, 2, 1⟩,
   ⟨2, 1, 0, 0, 2, 0⟩,
   ⟨2, 0, 2, 2, 0, 2⟩,
   ⟨2, 0, 0, 1, 1, 0⟩,
   ⟨1, 1, 1, 1, 1, 0⟩,
   ⟨2, 0, 1, 2, 2, 0⟩⟩

theorem lift_inverse_matrices_checked :
    mul inverseL0 L0 = identity ∧ mul L0 inverseL0 = identity ∧
    mul inverseL1 L1 = identity ∧ mul L1 inverseL1 = identity := by
  rw [L0_reconstructed,L1_reconstructed]
  decide +kernel

theorem word_inverse_checked : ∀ w ∈ allWords,
    rowAction (rowAction w L0) inverseL0 = w ∧
    rowAction (rowAction w inverseL0) L0 = w ∧
    rowAction (rowAction w L1) inverseL1 = w ∧
    rowAction (rowAction w inverseL1) L1 = w := by
  rw [L0_reconstructed,L1_reconstructed]
  decide +kernel

theorem word_inverse (w : Word) (hw : Ternary w) :
    rowAction (rowAction w L0) inverseL0 = w ∧
    rowAction (rowAction w inverseL0) L0 = w ∧
    rowAction (rowAction w L1) inverseL1 = w ∧
    rowAction (rowAction w inverseL1) L1 = w :=
  word_inverse_checked w (allWords_complete w hw)

def chooseLift (regime : Bool) : Matrix := if regime then L1 else L0
def run : List Bool → Word → List Word
  | [], w => [w]
  | b :: bs, w => w :: run bs (rowAction w (chooseLift b))

theorem run_length (bs : List Bool) (w : Word) : (run bs w).length = bs.length + 1 := by
  induction bs generalizing w with
  | nil => rfl
  | cons b bs ih => simp [run, ih, Nat.add_assoc]

theorem run_ternary (bs : List Bool) (w : Word) (hw : Ternary w) :
    ∀ v ∈ run bs w, Ternary v := by
  induction bs generalizing w with
  | nil =>
    intro v hv
    have hvw : v = w := by simpa [run] using hv
    exact hvw ▸ hw
  | cons b bs ih =>
    intro v hv
    simp only [run, List.mem_cons] at hv
    rcases hv with hv | hv
    · exact hv ▸ hw
    · exact ih _ (rowAction_ternary _ _) v hv

theorem run_take (bs : List Bool) (n : Nat) (w : Word) :
    (run bs w).take (n+1) = run (bs.take n) w := by
  induction bs generalizing n w with
  | nil => simp [run]
  | cons b bs ih =>
    cases n with
    | zero => rfl
    | succ n => simpa [run, Nat.add_assoc] using congrArg (List.cons w) (ih n (rowAction w (chooseLift b)))

def selectedSeeds : List Word :=
  TPKRegions.orientedClosure ++ TPKSimpleRegions.propagationWords ++ TPKSimpleRegions.autoscaleWords

theorem selected_seeds_checked : selectedSeeds = [⟨0, 1, 0, 2, 1, 1⟩, ⟨2, 0, 1, 1, 0, 1⟩, ⟨1, 2, 1, 2, 0, 0⟩] := by
  rw [selectedSeeds,TPKRegions.oriented_closure_checked,
    TPKSimpleRegions.propagation_oriented_checked,TPKSimpleRegions.autoscale_oriented_checked]
  rfl

def referenceBiographies : List (List Word) :=
  [[X0.r0,Y0.r0,Y0.r1,Y1.r0,Y1.r1],
   [X0.r2,Y0.r2,Y0.r3,Y1.r2,Y1.r3],
   [X0.r4,Y0.r4,Y0.r5,Y1.r4,Y1.r5]]

theorem record_stitching :
    X0.r1 = Y0.r0 ∧ X1.r0 = Y0.r1 ∧ X1.r1 = Y1.r0 ∧
    X0.r3 = Y0.r2 ∧ X1.r2 = Y0.r3 ∧ X1.r3 = Y1.r2 ∧
    X0.r5 = Y0.r4 ∧ X1.r4 = Y0.r5 ∧ X1.r5 = Y1.r4 := by decide +kernel

def binaryCalendars : List (List Bool) :=
  [false,true].flatMap fun a => [false,true].flatMap fun b =>
  [false,true].flatMap fun c => [false,true].map fun d => [a,b,c,d]

theorem binaryCalendars_complete (a b c d : Bool) : [a,b,c,d] ∈ binaryCalendars := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem binaryCalendars_cardinality : binaryCalendars.length = 16 := by decide +kernel

def compatible (cal : List Bool) : Bool := selectedSeeds.map (run cal) == referenceBiographies
def acceptedCalendars : List (List Bool) := binaryCalendars.filter compatible
def calendar : List Bool := acceptedCalendars.headD []

theorem accepted_calendars_checked : acceptedCalendars = [[false,false,true,true]] := by
  unfold acceptedCalendars compatible
  rw [selected_seeds_checked]
  simp only [binaryCalendars, List.flatMap_cons, List.flatMap_nil, List.map_cons,
    List.map_nil, List.cons_append, List.nil_append, run, chooseLift,
    L0_reconstructed,L1_reconstructed]
  decide +kernel

theorem calendar_reconstructed : calendar = [false,false,true,true] := by
  rw [calendar, accepted_calendars_checked]
  rfl

theorem calendar_unique : acceptedCalendars.length = 1 := by
  rw [accepted_calendars_checked]
  rfl

def biographies : List (List Word) := selectedSeeds.map (run calendar)

theorem biographies_checked : biographies = [[⟨0, 1, 0, 2, 1, 1⟩, ⟨0, 1, 2, 2, 2, 2⟩, ⟨0, 1, 0, 2, 1, 1⟩, ⟨0, 0, 2, 1, 1, 1⟩, ⟨1, 1, 0, 2, 2, 1⟩],
    [⟨2, 0, 1, 1, 0, 1⟩, ⟨1, 2, 1, 2, 2, 1⟩, ⟨1, 0, 2, 0, 1, 1⟩, ⟨0, 1, 2, 2, 2, 2⟩, ⟨1, 0, 2, 0, 1, 1⟩],
    [⟨1, 2, 1, 2, 0, 0⟩, ⟨1, 1, 2, 2, 0, 2⟩, ⟨1, 2, 1, 0, 2, 0⟩, ⟨0, 1, 0, 2, 1, 0⟩, ⟨0, 1, 0, 2, 0, 0⟩]] := by
  rw [biographies,selected_seeds_checked,calendar_reconstructed]
  simp only [run,chooseLift,L0_reconstructed,L1_reconstructed]
  decide +kernel

theorem biographies_match_records : biographies = referenceBiographies := by
  rw [biographies_checked]
  decide +kernel

def flattenWords (ws : List Word) : List Nat := ws.flatMap toList
def expansion (n : Nat) (w : Word) : List Nat := flattenWords (run (calendar.take n) w)

theorem flattenWords_length (ws : List Word) : (flattenWords ws).length = 6 * ws.length := by
  induction ws with
  | nil => rfl
  | cons w ws ih =>
    change (toList w ++ flattenWords ws).length = 6 * (ws.length + 1)
    rw [List.length_append, ih]
    simp only [toList, List.length_cons, List.length_nil]
    omega

theorem expansion_length (n : Nat) (w : Word) :
    (expansion n w).length = 6 * (min n 4 + 1) := by
  rw [expansion,flattenWords_length,run_length,List.length_take,calendar_reconstructed]
  rfl

theorem five_prefix_lengths (w : Word) :
    [(expansion 0 w).length,(expansion 1 w).length,(expansion 2 w).length,
      (expansion 3 w).length,(expansion 4 w).length] = [6,12,18,24,30] := by
  rw [expansion_length,expansion_length,expansion_length,expansion_length,expansion_length]
  rfl

theorem four_step_block_truncation (w : Word) :
    (run calendar w).take 1 = run (calendar.take 0) w ∧
    (run calendar w).take 2 = run (calendar.take 1) w ∧
    (run calendar w).take 3 = run (calendar.take 2) w ∧
    (run calendar w).take 4 = run (calendar.take 3) w := by
  exact ⟨run_take calendar 0 w, run_take calendar 1 w,
    run_take calendar 2 w, run_take calendar 3 w⟩

theorem initial_block_preserved (w : Word) : (expansion 4 w).take 6 = toList w := by
  rw [expansion,calendar_reconstructed]
  rfl

theorem four_step_truncation (w : Word) :
    (expansion 4 w).take 6 = expansion 0 w ∧
    (expansion 4 w).take 12 = expansion 1 w ∧
    (expansion 4 w).take 18 = expansion 2 w ∧
    (expansion 4 w).take 24 = expansion 3 w := by
  simp only [expansion,calendar_reconstructed]
  exact ⟨rfl,rfl,rfl,rfl⟩

end TPKLifts

#print axioms TPKLifts.allWords_complete
#print axioms TPKLifts.allWords_cardinality
#print axioms TPKLifts.fromColumns_column
#print axioms TPKLifts.matrix_ext_columns
#print axioms TPKLifts.rowAction_ternary
#print axioms TPKLifts.column_mul
#print axioms TPKLifts.L0_reconstructed
#print axioms TPKLifts.L1_reconstructed
#print axioms TPKLifts.transition_equations
#print axioms TPKLifts.X0_column_unique_checked
#print axioms TPKLifts.X1_column_unique_checked
#print axioms TPKLifts.reconstructed_lifts_ternary
#print axioms TPKLifts.L0_unique
#print axioms TPKLifts.L1_unique
#print axioms TPKLifts.record_inverses_checked
#print axioms TPKLifts.reconstruction_inverse_formula
#print axioms TPKLifts.lift_inverse_matrices_checked
#print axioms TPKLifts.word_inverse_checked
#print axioms TPKLifts.word_inverse
#print axioms TPKLifts.run_length
#print axioms TPKLifts.run_ternary
#print axioms TPKLifts.run_take
#print axioms TPKLifts.selected_seeds_checked
#print axioms TPKLifts.record_stitching
#print axioms TPKLifts.binaryCalendars_complete
#print axioms TPKLifts.binaryCalendars_cardinality
#print axioms TPKLifts.accepted_calendars_checked
#print axioms TPKLifts.calendar_reconstructed
#print axioms TPKLifts.calendar_unique
#print axioms TPKLifts.biographies_checked
#print axioms TPKLifts.biographies_match_records
#print axioms TPKLifts.flattenWords_length
#print axioms TPKLifts.expansion_length
#print axioms TPKLifts.five_prefix_lengths
#print axioms TPKLifts.four_step_block_truncation
#print axioms TPKLifts.initial_block_preserved
#print axioms TPKLifts.four_step_truncation
