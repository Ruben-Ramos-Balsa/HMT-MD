import UnorderedTerminalTransfer

/-!
Exact evaluation of the incidence records printed in
`derivacion_registro_k.tex`, tables terminal-incidencias-completas and
terminal-bandas-testigo, together with its affine record at time 30.

The input consists of incidence positions, times, charge-reader kinds,
offsets and orientations. Word values are computed from the already produced
regional prefixes; neither K nor the eight target words is an input to the
reader below. The historical incidence schedule IS an explicit input. This
module does not claim that the microscopic enriched dynamics selects that
schedule, nor that the schedule characterizes all admissible histories.

The historical dual-charge chart is RegionalW24.dualChargeWord. It must not
be silently replaced by TerminalSelector.transform6's different Witt chart.
-/

namespace HMT.I.HistoricalIncidenceEvaluation

open HMT.I.TerminalSelector HMT.I.GeneratedN69Rows

set_option maxRecDepth 30000
set_option maxHeartbeats 10000000

inductive ReaderKind where
  | comparison (dual : Bool) (offset : Fin 3) (orientation : Fin 2)
  | affine
  deriving DecidableEq, Repr

structure Incidence where
  position : Fin 8
  time : Fin 100
  reader : ReaderKind
  deriving DecidableEq, Repr

def read (prefixes : Fin 3 → Nat) (inc : Incidence) : Nat :=
  let band := fun i : Fin 3 => blockFromPrefix (prefixes i) inc.time.val
  let phase := readerPhase inc.time.val
  let coeff := fun i : Fin 3 => match inc.reader with
    | .comparison dual offset orientation =>
        let charge := if dual then RegionalW24.dualChargeWord else wordCharge
        let sign := orientation.val + 1
        (sign * (if charge (band i) = (phase + offset.val) % 3 then 1 else 2)) % 3
    | .affine => (RegionalW24.dualChargeWord (band i) + phase) % 3
  encodeSix fun j =>
    (coeff 0 * digit6 (band 0) j.val + coeff 1 * digit6 (band 1) j.val +
      coeff 2 * digit6 (band 2) j.val) % 3

/-- Positions 0..7 are the printed positions 5..12. Orientation 0 is +1;
orientation 1 is -1, represented by 2 in the ternary chart. -/
def historicalSchedule : List Incidence := [
  ⟨0, 67, .comparison true  1 1⟩,
  ⟨0, 67, .comparison true  2 0⟩,
  ⟨0, 67, .comparison false 1 1⟩,
  ⟨0, 67, .comparison false 2 0⟩,
  ⟨1, 81, .comparison true  0 0⟩,
  ⟨1, 81, .comparison false 2 0⟩,
  ⟨2, 34, .comparison false 1 1⟩,
  ⟨2, 75, .comparison true  1 1⟩,
  ⟨2, 75, .comparison false 2 1⟩,
  ⟨3, 90, .comparison false 0 0⟩,
  ⟨3, 90, .comparison false 1 1⟩,
  ⟨4, 49, .comparison true  0 1⟩,
  ⟨5, 30, .affine⟩,
  ⟨6, 11, .comparison true  2 1⟩,
  ⟨6, 37, .comparison true  0 1⟩,
  ⟨7,  8, .comparison true  0 1⟩,
  ⟨7,  8, .comparison false 1 1⟩,
  ⟨7, 58, .comparison true  1 1⟩,
  ⟨7, 58, .comparison false 0 1⟩]

def atPosition (schedule : List Incidence) (p : Fin 8) : List Incidence :=
  schedule.filter (fun inc => inc.position = p)

def readPosition (prefixes : Fin 3 → Nat) (schedule : List Incidence)
    (p : Fin 8) : List Nat :=
  ((atPosition schedule p).map (read prefixes)).eraseDups

def recover (prefixes : Fin 3 → Nat) (schedule : List Incidence) : List Nat :=
  (List.finRange 8).flatMap (readPosition prefixes schedule)

theorem schedule_multiplicities :
    (List.finRange 8).map (fun p => (atPosition historicalSchedule p).length) =
      [4, 2, 3, 2, 1, 1, 2, 4] := by decide

/-- These numerals occur in the equality certificate, not in `read` or `recover`. -/
theorem position_evaluations : ∀ p : Fin 8,
    readPosition prefixInputs historicalSchedule p =
      [(![55, 175, 498, 437, 98, 28, 687, 714] : Fin 8 → Nat) p] := by
  decide +kernel

theorem recovered_evaluation : recover prefixInputs historicalSchedule =
    [55, 175, 498, 437, 98, 28, 687, 714] := by
  decide +kernel

noncomputable def regionalRecovered : List Nat :=
  recover regionalPrefixes historicalSchedule

theorem regional_positions_singleton : ∀ p : Fin 8,
    ∃! w, readPosition regionalPrefixes historicalSchedule p = [w] := by
  intro p
  rw [regionalPrefixes_eq_inputs, position_evaluations]
  simp

theorem regional_recovered_evaluation : regionalRecovered =
    [55, 175, 498, 437, 98, 28, 687, 714] := by
  unfold regionalRecovered
  rw [regionalPrefixes_eq_inputs]
  exact recovered_evaluation

/-- The prose's final two decimal conversions are transposed. Its ternary
words and incidence tables give 221110₃ = 687 and 222110₃ = 714. -/
theorem printed_order_is_transposed : regionalRecovered ≠
    [55, 175, 498, 437, 98, 28, 714, 687] := by
  rw [regional_recovered_evaluation]
  decide

theorem regional_recovered_perm : regionalRecovered.Perm s8Input := by
  rw [regional_recovered_evaluation]
  decide

noncomputable def selectedFromHistoricalIncidences : List Nat :=
  selectFrom RegionalW24.regionalW24 regionalRecovered regionalPanel
    (generatedRows regionalPrefixes)

/-- Reuse of the selector: all word values now come from evaluating the
declared historical incidences on produced regional bands. The incidence
schedule, not a new proof of its selection, is the remaining input. -/
theorem historical_selection_unique (n : Nat) :
    n ∈ selectedFromHistoricalIncidences ↔
      n = 234543140729659824621058914794146601 :=
  UnorderedTerminalTransfer.regional_unique_for_any_order
    regionalRecovered regional_recovered_perm n

theorem historical_selection_existsUnique :
    ∃! n, n ∈ selectedFromHistoricalIncidences := by
  simp only [historical_selection_unique]
  exact existsUnique_eq

end HMT.I.HistoricalIncidenceEvaluation

#print axioms HMT.I.HistoricalIncidenceEvaluation.position_evaluations
#print axioms HMT.I.HistoricalIncidenceEvaluation.regional_positions_singleton
#print axioms HMT.I.HistoricalIncidenceEvaluation.historical_selection_existsUnique
