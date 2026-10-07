import HistoricalIncidenceEvaluation
import WittReaderCompatibility

/-!
# Compatibility of the two scalar dual-charge readers

Source: `derivacion_registro_k.tex`, the compatibility of the charge
functional (lines 600–646). The regional and terminal matrices are distinct;
only their total charge functional is identified here. This does not replace
one vector-valued matrix action by the other without its coordinate change.
-/

namespace HMT.I.ChargeChartCompatibility

open HMT.I.TerminalSelector HMT.I.GeneratedN69Rows
open HMT.I.WittReaderCompatibility

set_option maxHeartbeats 2000000
set_option maxRecDepth 30000

/-- Fixed-width encoding preserves each of its six bounded digits. -/
theorem digit6_encodeSix (b : Fin 6 → Nat) (hb : ∀ i, b i < 3) (j : Fin 6) :
    digit6 (encodeSix b) j.val = b j := by
  have h0 := hb 0
  have h1 := hb 1
  have h2 := hb 2
  have h3 := hb 3
  have h4 := hb 4
  have h5 := hb 5
  fin_cases j
  · change digit6 (encodeSix b) 0 = b 0
    norm_num [encodeSix, digit6]
    omega
  · change digit6 (encodeSix b) 1 = b 1
    norm_num [encodeSix, digit6]
    omega
  · change digit6 (encodeSix b) 2 = b 2
    norm_num [encodeSix, digit6]
    omega
  · change digit6 (encodeSix b) 3 = b 3
    norm_num [encodeSix, digit6]
    omega
  · change digit6 (encodeSix b) 4 = b 4
    norm_num [encodeSix, digit6]
    omega
  · change digit6 (encodeSix b) 5 = b 5
    norm_num [encodeSix, digit6]
    omega

/-- The scalar charge of a fixed-width encoding is its digit sum modulo 3. -/
theorem wordCharge_encodeSix (b : Fin 6 → Nat) (hb : ∀ i, b i < 3) :
    wordCharge (encodeSix b) = (∑ j : Fin 6, b j) % 3 := by
  norm_num [wordCharge, List.range_succ, Fin.sum_univ_succ]
  change (digit6 (encodeSix b) 0 + digit6 (encodeSix b) 1 +
    digit6 (encodeSix b) 2 + digit6 (encodeSix b) 3 +
    digit6 (encodeSix b) 4 + digit6 (encodeSix b) 5) % 3 =
      (b 0 + (b 1 + (b 2 + (b 3 + (b 4 + b 5))))) % 3
  have h0 : digit6 (encodeSix b) 0 = b 0 := digit6_encodeSix b hb 0
  have h1 : digit6 (encodeSix b) 1 = b 1 := digit6_encodeSix b hb 1
  have h2 : digit6 (encodeSix b) 2 = b 2 := digit6_encodeSix b hb 2
  have h3 : digit6 (encodeSix b) 3 = b 3 := digit6_encodeSix b hb 3
  have h4 : digit6 (encodeSix b) 4 = b 4 := digit6_encodeSix b hb 4
  have h5 : digit6 (encodeSix b) 5 = b 5 := digit6_encodeSix b hb 5
  rw [h0, h1, h2, h3, h4, h5]
  congr 1
  omega

def terminalImageDigits (word : Nat) (j : Fin 6) : Nat :=
  (∑ i : Fin 6, digit6 word i.val * terminalChart i j) % 3

/-- Unroll only the six-by-six implementation loops, retaining arbitrary input. -/
theorem transform6_eq_encodeSix (word : Nat) :
    transform6 word = encodeSix (terminalImageDigits word) := by
  norm_num [transform6, terminalImageDigits, terminalChart, wittMatrix,
    encodeSix, Fin.sum_univ_succ, List.range'_succ]
  ring

theorem wordCharge_transform6_totalImage (word : Nat) :
    wordCharge (transform6 word) =
      totalImage terminalChart (fun i => digit6 word i.val) % 3 := by
  have hb : ∀ j, terminalImageDigits word j < 3 :=
    fun _ => Nat.mod_lt _ (by decide)
  rw [transform6_eq_encodeSix, wordCharge_encodeSix _ hb]
  unfold terminalImageDigits totalImage
  exact (Finset.sum_nat_mod Finset.univ 3
    (fun j : Fin 6 => ∑ i : Fin 6, digit6 word i.val * terminalChart i j)).symm

/-- The scalar readers agree for every input; digit access fixes the width. -/
theorem dualChargeWord_eq_wordCharge_transform6 (word : Nat) :
    RegionalW24.dualChargeWord word = wordCharge (transform6 word) := by
  rw [wordCharge_transform6_totalImage, charge_eq]
  norm_num [RegionalW24.dualChargeWord, totalImage,
    HMT.N69RegionalSignature.wittMatrix, Fin.sum_univ_succ]
  omega

theorem dualChargeWord_function_eq :
    RegionalW24.dualChargeWord = fun word => wordCharge (transform6 word) :=
  funext dualChargeWord_eq_wordCharge_transform6

/-- The historical reader with its scalar dual-charge functional exposed.
Only this scalar parameter varies; the words and their coordinate order do not. -/
def readWithDualCharge (dualCharge : Nat → Nat) (prefixes : Fin 3 → Nat)
    (inc : HistoricalIncidenceEvaluation.Incidence) : Nat :=
  let band := fun i : Fin 3 => blockFromPrefix (prefixes i) inc.time.val
  let phase := readerPhase inc.time.val
  let coeff := fun i : Fin 3 => match inc.reader with
    | .comparison dual offset orientation =>
        let charge := if dual then dualCharge else wordCharge
        let sign := orientation.val + 1
        (sign * (if charge (band i) = (phase + offset.val) % 3 then 1 else 2)) % 3
    | .affine => (dualCharge (band i) + phase) % 3
  encodeSix fun j =>
    (coeff 0 * digit6 (band 0) j.val + coeff 1 * digit6 (band 1) j.val +
      coeff 2 * digit6 (band 2) j.val) % 3

theorem readWithDualCharge_regional (prefixes : Fin 3 → Nat)
    (inc : HistoricalIncidenceEvaluation.Incidence) :
    readWithDualCharge RegionalW24.dualChargeWord prefixes inc =
      HistoricalIncidenceEvaluation.read prefixes inc := rfl

/-- Universal reader compatibility, including both comparison and affine cases. -/
theorem readWithDualCharge_terminal (prefixes : Fin 3 → Nat)
    (inc : HistoricalIncidenceEvaluation.Incidence) :
    readWithDualCharge (fun word => wordCharge (transform6 word)) prefixes inc =
      HistoricalIncidenceEvaluation.read prefixes inc := by
  rw [← dualChargeWord_function_eq]
  rfl

/-- Any incidence schedule is preserved; no special schedule is assumed. -/
theorem readPosition_terminal (prefixes : Fin 3 → Nat)
    (schedule : List HistoricalIncidenceEvaluation.Incidence) (p : Fin 8) :
    (((HistoricalIncidenceEvaluation.atPosition schedule p).map
      (readWithDualCharge (fun word => wordCharge (transform6 word)) prefixes)).eraseDups) =
      HistoricalIncidenceEvaluation.readPosition prefixes schedule p := by
  rw [← dualChargeWord_function_eq]
  rfl

#print axioms digit6_encodeSix
#print axioms transform6_eq_encodeSix
#print axioms wordCharge_transform6_totalImage
#print axioms dualChargeWord_eq_wordCharge_transform6
#print axioms readWithDualCharge_terminal
#print axioms readPosition_terminal

end HMT.I.ChargeChartCompatibility
