import CommonComposition
import EmissionCode

/-!
The finite emitter of extension.tex 8-49, built from pre-transport visits.
Every sample retains the observable state and both lifted APP evaluations;
the emitted channels are readers of that sample, not replacements for it.
No catalogue cardinalities or target real constants are inputs or conclusions.
-/
namespace TPKEmission

open TPKTransport

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

inductive EventKind where
  | additive | multiplicative | neutral
  deriving DecidableEq, Repr

def classify (p : Phase) : EventKind :=
  if p.val % 3 = 0 then .additive
  else if p.val % 3 = 1 then .multiplicative else .neutral

theorem classify_additive : ∀ p : Phase,
    classify p = .additive ↔ active .additive p = true := by decide

theorem classify_multiplicative : ∀ p : Phase,
    classify p = .multiplicative ↔ active .multiplicative p = true := by decide

theorem classify_neutral : ∀ p : Phase,
    classify p = .neutral ↔ TRITCore.phase (p.val + 1) = 0 := by decide

-- The zero extension is a reader; the original residue remains in each sample.
def log9 : Nat → Nat
  | 1 => 0
  | 2 => 1
  | 4 => 2
  | 8 => 3
  | 7 => 4
  | 5 => 5
  | _ => 0

theorem log9_unit_table :
    log9 1 = 0 ∧ log9 2 = 1 ∧ log9 4 = 2 ∧
    log9 8 = 3 ∧ log9 7 = 4 ∧ log9 5 = 5 := by decide

theorem log9_radical : log9 3 = 0 ∧ log9 6 = 0 ∧ log9 9 = 0 := by decide

theorem log9_inverse_on_units : ∀ r : Fin 10,
    r.val = 1 ∨ r.val = 2 ∨ r.val = 4 ∨ r.val = 8 ∨ r.val = 7 ∨ r.val = 5 →
      2 ^ log9 r.val % 9 = r.val := by decide

structure Sample where
  before : ObservableLift
  arithmetic : APPArithmetic.PairedEvaluation
  kind : EventKind
  deriving DecidableEq, Repr

def sample (q : ObservableLift) : Sample :=
  ⟨q, CommonComposition.readVisit q, classify q.phase⟩

def additiveReading (v : Sample) : Nat :=
  if v.kind = .additive then v.arithmetic.additive.residue else 0

def exponentReading (v : Sample) : Nat :=
  if v.kind = .multiplicative then log9 v.arithmetic.multiplicative.residue else 0

def count (kind : EventKind) (vs : List Sample) : Nat :=
  (vs.map (fun v => if v.kind = kind then 1 else 0)).sum

theorem sample_additive_residue (q : ObservableLift) :
    (sample q).arithmetic.additive.residue =
      APPArithmetic.rho9 (APPArithmetic.sumEval
        (CommonComposition.cursorMark q.plus.x) (CommonComposition.cursorMark q.plus.y)) := rfl

theorem sample_multiplicative_residue (q : ObservableLift) :
    (sample q).arithmetic.multiplicative.residue =
      APPArithmetic.rho9 (APPArithmetic.productEval
        (CommonComposition.cursorMark q.times.x) (CommonComposition.cursorMark q.times.y)) := rfl

theorem sample_retains_evaluations (q : ObservableLift) :
    APPArithmetic.decode (sample q).arithmetic.additive =
      APPArithmetic.sumEval (CommonComposition.cursorMark q.plus.x)
        (CommonComposition.cursorMark q.plus.y) ∧
    APPArithmetic.decode (sample q).arithmetic.multiplicative =
      APPArithmetic.productEval (CommonComposition.cursorMark q.times.x)
        (CommonComposition.cursorMark q.times.y) :=
  ⟨(APPArithmetic.paired_reconstruction _ _).1, (APPArithmetic.paired_reconstruction _ _).2⟩

structure Execution where
  current : ObservableLift
  memory : List Sample

def emitStep (q : Execution) : Execution :=
  ⟨step q.current, q.memory ++ [sample q.current]⟩

theorem emitStep_reads_before (q : Execution) :
    (emitStep q).memory = q.memory ++ [sample q.current] ∧
    (emitStep q).current = step q.current := ⟨rfl, rfl⟩

def samples : Nat → ObservableLift → List Sample
  | 0, _ => []
  | n + 1, q => samples n q ++ [sample (iterate step n q)]

theorem samples_length (n : Nat) (q : ObservableLift) : (samples n q).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [samples, ih]

theorem samples_range (n : Nat) (q : ObservableLift) :
    samples n q = (List.range n).map (fun k => sample (iterate step k q)) := by
  induction n with
  | zero => rfl
  | succ n ih => simp [samples, List.range_succ, ih]

theorem execution_current (n : Nat) (q : Execution) :
    (iterate emitStep n q).current = iterate step n q.current := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [iterate, emitStep, ih]

theorem execution_memory (n : Nat) (q : Execution) :
    (iterate emitStep n q).memory = q.memory ++ samples n q.current := by
  induction n with
  | zero => simp [iterate, samples]
  | succ n ih =>
    simp only [iterate, emitStep, ih, execution_current, samples, List.append_assoc]

theorem execution_memory_length (n : Nat) (q : Execution) :
    (iterate emitStep n q).memory.length = q.memory.length + n := by
  rw [execution_memory, List.length_append, samples_length]

theorem execution_no_reset (n : Nat) (hn : 0 < n) (q : Execution) :
    iterate emitStep n q ≠ q := by
  intro h
  have hl := congrArg (fun x : Execution => x.memory.length) h
  change (iterate emitStep n q).memory.length = q.memory.length at hl
  rw [execution_memory_length] at hl
  omega

theorem samples_append (n m : Nat) (q : ObservableLift) :
    samples (n + m) q = samples n q ++ samples m (iterate step n q) := by
  induction m with
  | zero => simp [samples]
  | succ m ih =>
    change samples (n + m) q ++ [sample (iterate step (n + m) q)] =
      samples n q ++ (samples m (iterate step n q) ++ [sample (iterate step m (iterate step n q))])
    rw [ih, iterate_add, List.append_assoc]

theorem execution_concatenates (n m : Nat) (q : Execution) :
    iterate emitStep (n + m) q = iterate emitStep m (iterate emitStep n q) :=
  iterate_add emitStep n m q

def forgetReadings (q : Execution) : HistoryLift :=
  ⟨q.current, q.memory.map Sample.before⟩

theorem forgetReadings_step (q : Execution) :
    forgetReadings (emitStep q) = recordStep (forgetReadings q) := by
  simp [forgetReadings, emitStep, recordStep, sample, List.map_append]

theorem forgetReadings_execution (n : Nat) (q : Execution) :
    forgetReadings (iterate emitStep n q) = iterate recordStep n (forgetReadings q) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [iterate, forgetReadings_step, ih, iterate]

theorem phase_at_depth (n : Nat) (q : ObservableLift) :
    (iterate step n q).phase = iterate nextPhase n q.phase := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [iterate, step, ih]

def phaseCount (kind : EventKind) : Nat → Phase → Nat
  | 0, _ => 0
  | n + 1, p => phaseCount kind n p +
      if classify (iterate nextPhase n p) = kind then 1 else 0

theorem sum_append (xs ys : List Nat) : (xs ++ ys).sum = xs.sum + ys.sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [List.sum_cons, ih, Nat.add_assoc]

theorem count_samples (kind : EventKind) (n : Nat) (q : ObservableLift) :
    count kind (samples n q) = phaseCount kind n q.phase := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [samples, count, List.map_append, sum_append,
      List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Nat.add_zero]
    change count kind (samples n q) +
      (if classify (iterate step n q).phase = kind then 1 else 0) = _
    rw [ih, phase_at_depth]
    rfl

theorem phaseCount_nine : ∀ (kind : EventKind) (p : Phase),
    phaseCount kind 9 p = 3 := by
  intro kind
  cases kind <;> decide

theorem nine_events_each (kind : EventKind) (q : ObservableLift) :
    count kind (samples 9 q) = 3 := by rw [count_samples, phaseCount_nine]

theorem every_nine_window (kind : EventKind) (q : ObservableLift) (start : Nat) :
    count kind (samples 9 (iterate step start q)) = 3 := nine_events_each kind _

structure WindowTotals where
  s : Nat
  e : Nat
  z : Nat
  deriving DecidableEq, Repr

def totals (vs : List Sample) : WindowTotals :=
  ⟨(vs.map additiveReading).sum, (vs.map exponentReading).sum, count .neutral vs⟩

def addTotals (a b : WindowTotals) : WindowTotals := ⟨a.s + b.s, a.e + b.e, a.z + b.z⟩

theorem totals_append (xs ys : List Sample) :
    totals (xs ++ ys) = addTotals (totals xs) (totals ys) := by
  simp [totals, addTotals, count, List.map_append, sum_append]

theorem totals_concatenate (n m : Nat) (q : ObservableLift) :
    totals (samples (n + m) q) =
      addTotals (totals (samples n q)) (totals (samples m (iterate step n q))) := by
  rw [samples_append, totals_append]

def window (q : ObservableLift) : WindowTotals := totals (samples 9 q)

theorem window_neutral (q : ObservableLift) : (window q).z = 3 := nine_events_each .neutral q

def decimalValue (t : WindowTotals) : Nat :=
  100 * (t.s % 10) + 10 * ((t.s + t.e) % 10) + ((3 * t.s + 5 * t.e + 7 * t.z) % 10)

theorem decimalValue_bound (t : WindowTotals) : decimalValue t < 1000 := by
  have h1 := Nat.mod_lt t.s (by decide : 0 < 10)
  have h2 := Nat.mod_lt (t.s + t.e) (by decide : 0 < 10)
  have h3 := Nat.mod_lt (3 * t.s + 5 * t.e + 7 * t.z) (by decide : 0 < 10)
  unfold decimalValue
  omega

def block (q : ObservableLift) : Fin 1000 := ⟨decimalValue (window q), decimalValue_bound _⟩

theorem block_source_formula (q : ObservableLift) :
    (block q).val = 100 * ((window q).s % 10) +
      10 * (((window q).s + (window q).e) % 10) +
      ((3 * (window q).s + 5 * (window q).e + 7 * 3) % 10) := by
  simp only [block, decimalValue, window_neutral]

theorem block_as_encode (q : ObservableLift) :
    block q = EmissionCode.encode (EmissionCode.ofNat (window q).s)
      (EmissionCode.ofNat (window q).e) := by
  apply Fin.ext
  exact EmissionCode.sourceCode_reduced_of_neutral
    (window q).s (window q).e (window q).z (window_neutral q)

theorem block_recovers_signatures (q : ObservableLift) :
    EmissionCode.recoverS (block q) = EmissionCode.ofNat (window q).s ∧
    EmissionCode.recoverE (block q) = EmissionCode.ofNat (window q).e := by
  rw [block_as_encode]
  exact ⟨EmissionCode.recoverS_encode _ _, EmissionCode.recoverE_encode _ _⟩

def word (q : ObservableLift) : Fin 6 → Fin 1000 :=
  fun j => block (iterate step (9 * j.val) q)

def additiveSignature (q : ObservableLift) : EmissionCode.Signature :=
  fun j => EmissionCode.ofNat (window (iterate step (9 * j.val) q)).s

def exponentSignature (q : ObservableLift) : EmissionCode.Signature :=
  fun j => EmissionCode.ofNat (window (iterate step (9 * j.val) q)).e

theorem word_as_encodeWord (q : ObservableLift) :
    word q = EmissionCode.encodeWord (additiveSignature q) (exponentSignature q) := by
  funext j
  exact block_as_encode _

theorem word_recovers_signatures (q : ObservableLift) :
    EmissionCode.recoverSWord (word q) = additiveSignature q ∧
    EmissionCode.recoverEWord (word q) = exponentSignature q := by
  rw [word_as_encodeWord]
  exact ⟨EmissionCode.recoverSWord_encode _ _, EmissionCode.recoverEWord_encode _ _⟩

theorem equal_words_equal_signatures (q r : ObservableLift) (h : word q = word r) :
    additiveSignature q = additiveSignature r ∧ exponentSignature q = exponentSignature r := by
  rw [word_as_encodeWord, word_as_encodeWord] at h
  exact EmissionCode.encodeWord_injective _ _ _ _ h

def windowWord : Nat → ObservableLift → List (Fin 1000)
  | 0, _ => []
  | n + 1, q => windowWord n q ++ [block (iterate step (9 * n) q)]

theorem windowWord_length (n : Nat) (q : ObservableLift) : (windowWord n q).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [windowWord, ih]

theorem windowWord_range (n : Nat) (q : ObservableLift) :
    windowWord n q = (List.range n).map (fun j => block (iterate step (9 * j) q)) := by
  induction n with
  | zero => rfl
  | succ n ih => simp [windowWord, List.range_succ, ih]

theorem windowWord_append (n m : Nat) (q : ObservableLift) :
    windowWord (n + m) q =
      windowWord n q ++ windowWord m (iterate step (9 * n) q) := by
  induction m with
  | zero => simp [windowWord]
  | succ m ih =>
    change windowWord (n + m) q ++ [block (iterate step (9 * (n + m)) q)] =
      windowWord n q ++ (windowWord m (iterate step (9 * n) q) ++
        [block (iterate step (9 * m) (iterate step (9 * n) q))])
    rw [ih, Nat.mul_add, iterate_add, List.append_assoc]

def executeWindows : Nat → Execution → Execution
  | 0, q => q
  | n + 1, q => iterate emitStep 9 (executeWindows n q)

theorem executeWindows_steps (n : Nat) (q : Execution) :
    executeWindows n q = iterate emitStep (9 * n) q := by
  induction n with
  | zero => rfl
  | succ n ih => rw [executeWindows, ih, Nat.mul_succ, iterate_add]

structure WindowExecution where
  trace : Execution
  emitted : List (Fin 1000)

def emitWindow (q : WindowExecution) : WindowExecution :=
  ⟨iterate emitStep 9 q.trace, q.emitted ++ [block q.trace.current]⟩

theorem window_execution_trace (n : Nat) (q : WindowExecution) :
    (iterate emitWindow n q).trace = iterate emitStep (9 * n) q.trace := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change iterate emitStep 9 (iterate emitWindow n q).trace = _
    rw [ih, Nat.mul_succ, iterate_add]

theorem window_execution_emitted (n : Nat) (q : WindowExecution) :
    (iterate emitWindow n q).emitted = q.emitted ++ windowWord n q.trace.current := by
  induction n with
  | zero => simp [iterate, windowWord]
  | succ n ih =>
    change (iterate emitWindow n q).emitted ++ [block (iterate emitWindow n q).trace.current] = _
    rw [ih, window_execution_trace, execution_current]
    simp only [windowWord, List.append_assoc]

theorem word_reads_window_execution (q : WindowExecution) (j : Fin 6) :
    word q.trace.current j = block (iterate emitWindow j.val q).trace.current := by
  rw [window_execution_trace, execution_current]
  rfl

theorem six_windows_fiftyfour (q : Execution) :
    executeWindows 6 q = iterate emitStep 54 q := executeWindows_steps 6 q

theorem six_window_word_length (q : ObservableLift) : (windowWord 6 q).length = 6 :=
  windowWord_length 6 q

theorem six_windows_memory (q : Execution) :
    (executeWindows 6 q).memory = q.memory ++ samples 54 q.current ∧
    (executeWindows 6 q).memory.length = q.memory.length + 54 := by
  rw [six_windows_fiftyfour]
  exact ⟨execution_memory 54 q, execution_memory_length 54 q⟩

end TPKEmission

#print axioms TPKEmission.classify_additive
#print axioms TPKEmission.classify_multiplicative
#print axioms TPKEmission.classify_neutral
#print axioms TPKEmission.log9_unit_table
#print axioms TPKEmission.log9_radical
#print axioms TPKEmission.log9_inverse_on_units
#print axioms TPKEmission.sample_additive_residue
#print axioms TPKEmission.sample_multiplicative_residue
#print axioms TPKEmission.sample_retains_evaluations
#print axioms TPKEmission.emitStep_reads_before
#print axioms TPKEmission.samples_length
#print axioms TPKEmission.samples_range
#print axioms TPKEmission.execution_current
#print axioms TPKEmission.execution_memory
#print axioms TPKEmission.execution_memory_length
#print axioms TPKEmission.execution_no_reset
#print axioms TPKEmission.samples_append
#print axioms TPKEmission.execution_concatenates
#print axioms TPKEmission.forgetReadings_step
#print axioms TPKEmission.forgetReadings_execution
#print axioms TPKEmission.phase_at_depth
#print axioms TPKEmission.sum_append
#print axioms TPKEmission.count_samples
#print axioms TPKEmission.phaseCount_nine
#print axioms TPKEmission.nine_events_each
#print axioms TPKEmission.every_nine_window
#print axioms TPKEmission.totals_append
#print axioms TPKEmission.totals_concatenate
#print axioms TPKEmission.window_neutral
#print axioms TPKEmission.decimalValue_bound
#print axioms TPKEmission.block_source_formula
#print axioms TPKEmission.block_as_encode
#print axioms TPKEmission.block_recovers_signatures
#print axioms TPKEmission.word_as_encodeWord
#print axioms TPKEmission.word_recovers_signatures
#print axioms TPKEmission.equal_words_equal_signatures
#print axioms TPKEmission.windowWord_length
#print axioms TPKEmission.windowWord_range
#print axioms TPKEmission.windowWord_append
#print axioms TPKEmission.executeWindows_steps
#print axioms TPKEmission.window_execution_trace
#print axioms TPKEmission.window_execution_emitted
#print axioms TPKEmission.word_reads_window_execution
#print axioms TPKEmission.six_windows_fiftyfour
#print axioms TPKEmission.six_window_word_length
#print axioms TPKEmission.six_windows_memory
