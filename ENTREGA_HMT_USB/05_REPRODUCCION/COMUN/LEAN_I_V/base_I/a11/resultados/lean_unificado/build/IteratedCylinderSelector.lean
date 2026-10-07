import FiniteCylinderSelector
import GeneratedTransitionRecords

/-!
Iterated execution of the rational cylinder selector in the Article I
supplement. The constructor uses the previously computed parent, not the
publication at the next level. Rational enclosure search is internal and
terminates by the existing regional reader theorem. Failure is represented
by `none`; the proof establishes that it never occurs on this trajectory.

This is the refinement execution, not an identification of its clock with
nine microscopic Sel/Tra/Upd transitions of the complete enriched state.
-/

noncomputable section
namespace HMT.I.IteratedCylinderSelector

open Filter Topology
open HMT.I.RegionalPublicationComposition HMT.I.FiniteCylinderSelector
open HMT.I.GeneratedN69Rows HMT.I.JointRegionalFrontier
open HMT.I.GeneratedTransitionRecords

theorem endpoint_limits (c : Channel) :
    Tendsto (fun n => (lower c n : ℝ)) atTop (𝓝 (value c)) ∧
    Tendsto (fun n => (upper c n : ℝ)) atTop (𝓝 (value c)) := by
  cases c with
  | closure =>
      exact RadixCellSelection.bracket_limits_of_width _ _ _
        (produced_brackets .closure) ClosureAnalytic.width_tendsto_zero
  | propagation => exact ⟨PropagationLimit.partial_tendsto, PropagationLimit.upper_tendsto⟩
  | autoscale =>
      simpa only [value, autoscale_recognition] using
        And.intro AutoscaleBrackets.lower_tendsto AutoscaleBrackets.upper_tendsto

/-- The exact integer-part guard used by the Python fractional reader. -/
def InitialStops (c : Channel) (j : Nat) : Prop :=
  (⌊lower c j⌋ : Int) = ⌊upper c j⌋

instance (c : Channel) (j : Nat) : Decidable (InitialStops c j) :=
  inferInstanceAs (Decidable (_ = _))

theorem initial_search_terminates (c : Channel) : ∃ j, InitialStops c j := by
  obtain ⟨hl, hu⟩ := endpoint_limits c
  have hstrict : (⌊value c⌋ : ℝ) < value c :=
    lt_of_le_of_ne (Int.floor_le _) (Ne.symm ((value_irrational c).ne_int _))
  have hL : ∀ᶠ j in atTop, (⌊value c⌋ : ℝ) < (lower c j : ℝ) :=
    (tendsto_order.mp hl).1 _ hstrict
  have hU : ∀ᶠ j in atTop, (upper c j : ℝ) < (⌊value c⌋ : ℝ) + 1 :=
    (tendsto_order.mp hu).2 _ (Int.lt_floor_add_one _)
  obtain ⟨j, hlj, huj⟩ := (hL.and hU).exists
  refine ⟨j, ?_⟩
  have hb := produced_brackets c j
  have hlo : ⌊(lower c j : ℝ)⌋ = ⌊value c⌋ :=
    Int.floor_eq_iff.mpr ⟨hlj.le, hb.1.trans_lt (Int.lt_floor_add_one _)⟩
  have hup : ⌊(upper c j : ℝ)⌋ = ⌊value c⌋ :=
    Int.floor_eq_iff.mpr ⟨(Int.floor_le _).trans hb.2, huj⟩
  simpa only [InitialStops, Rat.floor_cast] using hlo.trans hup.symm

def initialDepth (c : Channel) : Nat := Nat.find (initial_search_terminates c)

/-- No initial integer is supplied: it is obtained after the rational guard. -/
def initial (c : Channel) : Nat := ⌊lower c (initialDepth c)⌋.toNat

theorem initial_guard (c : Channel) : InitialStops c (initialDepth c) :=
  Nat.find_spec (initial_search_terminates c)

/-- The precision of a rational enclosure, not a temporal TPK coordinate. -/
def precision (c : Channel) (base : Nat) (hb : 0 < base) (n : Nat) : Nat :=
  searchDepth c (base^(n + 1)) (pow_pos hb _)

theorem precision_stops (c : Channel) (base : Nat) (hb : 0 < base) (n : Nat) :
    Stops c (base^(n + 1)) (precision c base hb n) :=
  Nat.find_spec (search_terminates c (base^(n + 1)) (pow_pos hb _))

def next (c : Channel) (base : Nat) (hb : 0 < base) (n parent : Nat) :
    Option (Fin base) :=
  let j := precision c base hb n
  choose (lower c j) (upper c j) base hb n parent

def run (c : Channel) (base : Nat) (hb : 0 < base) : Nat → Option Nat
  | 0 => some (initial c)
  | n + 1 => do
      let parent ← run c base hb n
      let digit ← next c base hb n parent
      pure (base * parent + digit.val)

theorem initial_correct (c : Channel) (base : Nat) (hb : 0 < base) :
    initial c = publish c base hb 0 := by
  have hguard := initial_guard c
  change (⌊lower c (initialDepth c)⌋ : Int) = ⌊upper c (initialDepth c)⌋ at hguard
  have hlow : ⌊lower c (initialDepth c)⌋ ≤ ⌊value c⌋ := by
    rw [← Rat.floor_cast (α := ℝ)]
    exact Int.floor_mono (produced_brackets c _).1
  have hupp : ⌊value c⌋ ≤ ⌊lower c (initialDepth c)⌋ := by
    rw [hguard, ← Rat.floor_cast (α := ℝ)]
    exact Int.floor_mono (produced_brackets c _).2
  rw [initial, le_antisymm hlow hupp, publish_eq_prefix]
  simp [RadixCellSelection.positionalPrefix, Int.floor_toNat]

theorem next_correct (c : Channel) (base : Nat) (hb : 0 < base) (n : Nat) :
    next c base hb n (publish c base hb n) =
      some (⟨publish c base hb (n + 1) % base, Nat.mod_lt _ hb⟩ : Fin base) :=
  choose_at_stopping c base hb n (precision c base hb n) (precision_stops c base hb n)

/-- Every parent in this theorem was produced by the recursive execution. -/
theorem run_correct (c : Channel) (base : Nat) (hb : 0 < base) (n : Nat) :
    run c base hb n = some (publish c base hb n) := by
  induction n with
  | zero => exact congrArg some (initial_correct c base hb)
  | succ n ih =>
      simp only [run, ih, Bind.bind, Option.bind, next_correct, Pure.pure]
      exact congrArg some (publication_step c base hb n).symm

theorem run_never_fails (c : Channel) (base : Nat) (hb : 0 < base) (n : Nat) :
    ∃ parent, run c base hb n = some parent :=
  ⟨publish c base hb n, run_correct c base hb n⟩

def emitted (c : Channel) (base : Nat) (hb : 0 < base) (n : Nat) :
    Option (Fin base) := do
  let parent ← run c base hb n
  next c base hb n parent

theorem emitted_correct (c : Channel) (base : Nat) (hb : 0 < base) (n : Nat) :
    emitted c base hb n =
      some (⟨publish c base hb (n + 1) % base, Nat.mod_lt _ hb⟩ : Fin base) := by
  simp only [emitted, run_correct, Bind.bind, Option.bind, next_correct]

def wordOfDigit (d : Fin 729) : TPKOrbits.Word :=
  let b := bandFromWord d.val
  ⟨(b 0).val, (b 1).val, (b 2).val, (b 3).val, (b 4).val, (b 5).val⟩

def word (time : Nat) (channel : Fin 3) : Option TPKOrbits.Word :=
  (emitted (channelOfIndex channel) 729 (by decide) time).map wordOfDigit

theorem word_correct (time : Nat) (channel : Fin 3) :
    word time channel = some (wordGenerated time channel) := by
  simp only [word, emitted_correct, Option.map_some]
  rfl

def record (time : Nat) : Option TPKLifts.Matrix := do
  let a ← word time 0
  let b ← word (time + 1) 0
  let c ← word time 1
  let d ← word (time + 1) 1
  let e ← word time 2
  let f ← word (time + 1) 2
  pure ⟨a, b, c, d, e, f⟩

theorem record_correct (time : Nat) :
    record time = some (recordGenerated time) := by
  simp only [record, word_correct, Option.bind_some, pure]
  rfl

def lifts : Option (TPKLifts.Matrix × TPKLifts.Matrix) := do
  let x0 ← record 0
  let y0 ← record 1
  let x1 ← record 2
  let y1 ← record 3
  pure (TPKLifts.solveMatrix x0 y0, TPKLifts.solveMatrix x1 y1)

theorem lifts_correct : lifts = some (generatedLift0, generatedLift1) := by
  simp only [lifts, record_correct, Option.bind_some, pure]
  rfl

/-- The transition equations are certified for the records actually emitted. -/
theorem emitted_transition_equations :
    ∃ x0 y0 x1 y1,
      record 0 = some x0 ∧ record 1 = some y0 ∧
      record 2 = some x1 ∧ record 3 = some y1 ∧
      TPKLifts.mul x0 generatedLift0 = y0 ∧
      TPKLifts.mul x1 generatedLift1 = y1 := by
  exact ⟨_, _, _, _, record_correct 0, record_correct 1,
    record_correct 2, record_correct 3, generated_transition_equations⟩

/-- Uniqueness uses emitted records, not supplied transition tables. -/
theorem emitted_lifts_unique (x0 y0 x1 y1 M0 M1 : TPKLifts.Matrix)
    (hx0 : record 0 = some x0) (hy0 : record 1 = some y0)
    (hx1 : record 2 = some x1) (hy1 : record 3 = some y1)
    (hm0 : TPKLifts.TernaryMatrix M0) (hm1 : TPKLifts.TernaryMatrix M1)
    (h0 : TPKLifts.mul x0 M0 = y0) (h1 : TPKLifts.mul x1 M1 = y1) :
    M0 = generatedLift0 ∧ M1 = generatedLift1 := by
  have ex0 := Option.some.inj ((record_correct 0).symm.trans hx0)
  have ey0 := Option.some.inj ((record_correct 1).symm.trans hy0)
  have ex1 := Option.some.inj ((record_correct 2).symm.trans hx1)
  have ey1 := Option.some.inj ((record_correct 3).symm.trans hy1)
  apply generated_lifts_unique M0 M1 hm0 hm1
  · simpa only [ex0, ey0] using h0
  · simpa only [ex1, ey1] using h1

/-- One terminal statement connects recursive parents, emitted words and records. -/
theorem complete_reader_execution :
    (∀ c base hb n, run c base hb n = some (publish c base hb n)) ∧
    (∀ time channel, word time channel = some (wordGenerated time channel)) ∧
    (∀ time, record time = some (recordGenerated time)) ∧
    lifts = some (generatedLift0, generatedLift1) :=
  ⟨run_correct, word_correct, record_correct, lifts_correct⟩

end HMT.I.IteratedCylinderSelector
end

#print axioms HMT.I.IteratedCylinderSelector.precision_stops
#print axioms HMT.I.IteratedCylinderSelector.initial_search_terminates
#print axioms HMT.I.IteratedCylinderSelector.initial_guard
#print axioms HMT.I.IteratedCylinderSelector.run_correct
#print axioms HMT.I.IteratedCylinderSelector.run_never_fails
#print axioms HMT.I.IteratedCylinderSelector.emitted_correct
#print axioms HMT.I.IteratedCylinderSelector.word_correct
#print axioms HMT.I.IteratedCylinderSelector.record_correct
#print axioms HMT.I.IteratedCylinderSelector.lifts_correct
#print axioms HMT.I.IteratedCylinderSelector.emitted_transition_equations
#print axioms HMT.I.IteratedCylinderSelector.emitted_lifts_unique
#print axioms HMT.I.IteratedCylinderSelector.complete_reader_execution
