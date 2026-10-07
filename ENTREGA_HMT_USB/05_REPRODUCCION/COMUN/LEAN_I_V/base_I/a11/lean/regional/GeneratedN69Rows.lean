import N69RegionalSignature
import TerminalInputs
import RegionalSixHundred

/-!
# Finite N69 evaluation from 600-trit regional prefixes

`rowFromPrefixes` extracts a six-trit block at a transition index and computes
the signature. It does not read a table of signatures. The three displayed
integers encode the complete regional prefixes, including integer parts
3, 2, 1. Their derivation from the regional readers is kept in the separate
RegionalSixHundred module; the present theorem is their finite evaluation.

Only q, a, c, colw_mod are stored in TerminalSelector.N69Row. Its exceptional
reader subsequently uses its own declared Witt chart. No identification of
the two matrix charts is asserted here.
-/

namespace HMT.I.GeneratedN69Rows

open HMT.N69RegionalSignature HMT.I.TerminalSelector

set_option maxRecDepth 30000
set_option maxHeartbeats 10000000

def prefixInputs : Fin 3 → Nat := ![
  58871175078828582423602861784915247708935515546555106316035256695887729126437412843995626239311410634754654366838309942471935119906958980617248194957427434479381281283100208979121705879879452308865804958280022621974596599299586901072331835467338092495788056065771135131450066637595112365,
  50938636253160180888179413689343899880058096680583139319351969406550618361183491660978173715064929803522463101705965620207820892484968737588803861713662448187098712731515259457451744290391479777457307498688328575564785514917030398659922548502000937467496477613565943535501702691974540942,
  30320787173456450411059450570937628826773068695035242722820185835779727568438782363522556661749215466090147910298426733894837726975541809544014582262291135933678209524801375812678326344720015103636602750945244918166793903058044540395633023346705455026563404740487452508931290332655453238]

/-- Block t of a complete 100-block prefix, indexed from zero. -/
def blockFromPrefix (p t : Nat) : Nat :=
  (p / 729 ^ (99 - t)) % 729

def bandFromWord (word : Nat) : Band := fun j =>
  ⟨(word / 3 ^ (5 - j.val)) % 3, Nat.mod_lt _ (by decide)⟩

def bandsFromPrefixes (prefixes : Fin 3 → Nat) (t : Nat) : Bands :=
  fun i => bandFromWord (blockFromPrefix (prefixes i) t)

/-- Fixed-width base-three encoding; a leading zero is retained by the type. -/
def encodeSix (word : Fin 6 → Nat) : Nat :=
  243 * word 0 + 81 * word 1 + 27 * word 2 +
    9 * word 3 + 3 * word 4 + word 5

def rowFromPrefixes (prefixes : Fin 3 → Nat) (t : Nat) : N69Row :=
  let B := bandsFromPrefixes prefixes t
  let s := readSignature B
  { bands := #[blockFromPrefix (prefixes 0) t,
               blockFromPrefix (prefixes 1) t,
               blockFromPrefix (prefixes 2) t]
    fields := #[encodeSix s.q, encodeSix s.a, encodeSix s.c, encodeSix s.colwMod]
    time := t }

def generatedRows (prefixes : Fin 3 → Nat) : Array N69Row :=
  ((List.range 100).map (rowFromPrefixes prefixes)).toArray

theorem blockFromPrefix_lt (p t : Nat) : blockFromPrefix p t < 729 :=
  Nat.mod_lt _ (by decide)

theorem row_time_is_transition (prefixes : Fin 3 → Nat) (t : Nat) :
    (rowFromPrefixes prefixes t).time = t := rfl

theorem generatedRows_size (prefixes : Fin 3 → Nat) :
    (generatedRows prefixes).size = 100 := by
  simp [generatedRows]

/-- Kernel-checked evaluation; the target table is not used by the producer. -/
theorem generatedRows_eq_n69Input : generatedRows prefixInputs = n69Input := by
  decide

def channelOfIndex : Fin 3 → RegionalPublicationComposition.Channel :=
  ![.closure, .propagation, .autoscale]

noncomputable def regionalPrefixes (i : Fin 3) : Nat :=
  (RegionalSixHundred.generatedPrefix (channelOfIndex i)).toNat

theorem regionalPrefixes_eq_inputs : regionalPrefixes = prefixInputs := by
  funext i
  unfold regionalPrefixes
  rw [RegionalSixHundred.generatedPrefix_evaluates]
  fin_cases i <;>
    norm_num [channelOfIndex, RegionalSixHundred.expectedPrefix, prefixInputs] <;> rfl

/-- The regional producers, followed by extraction and signature evaluation,
reproduce all rows consumed by the terminal reader. -/
theorem regional_generatedRows_eq_n69Input :
    generatedRows regionalPrefixes = n69Input := by
  rw [regionalPrefixes_eq_inputs]
  exact generatedRows_eq_n69Input

theorem regionalPrefixes_are_publications (i : Fin 3) :
    regionalPrefixes i =
      RegionalPublicationComposition.publish (channelOfIndex i) 3 (by decide) 600 :=
  RegionalSixHundred.generatedPrefix_is_publication (channelOfIndex i)

end HMT.I.GeneratedN69Rows

#print axioms HMT.I.GeneratedN69Rows.blockFromPrefix_lt
#print axioms HMT.I.GeneratedN69Rows.row_time_is_transition
#print axioms HMT.I.GeneratedN69Rows.generatedRows_size
#print axioms HMT.I.GeneratedN69Rows.generatedRows_eq_n69Input
#print axioms HMT.I.GeneratedN69Rows.regionalPrefixes_eq_inputs
#print axioms HMT.I.GeneratedN69Rows.regional_generatedRows_eq_n69Input
#print axioms HMT.I.GeneratedN69Rows.regionalPrefixes_are_publications
