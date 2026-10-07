import GeneratedN69Rows

/-!
# Regional reconstruction of the W24 descriptor

This is the oriented descriptor of `verificar_caracter_fase_dual.py`,
build_rombo_prefix and phase_dual_construction. Its regional rows come from
the proved regional publications, not N69's stored table. The selected time
is the first pause of the ternary/decimal publication clock; the other times
are its nine-phase predecessor and its predecessor's predecessor.

The source's saturated half-band defect and its opposite are retained as
explicit operations. This proves their resulting W24 descriptor and the
first-pause characterization of the source time. It does not assert that
these operations generate the unordered S8 repertoire.
-/

noncomputable section
namespace HMT.I.RegionalW24

open HMT.N69RegionalSignature HMT.I.GeneratedN69Rows

set_option maxHeartbeats 10000000
set_option maxRecDepth 30000

theorem pause_exists : ∃ t, publicationClock t = publicationClock (t + 1) := by
  exact ⟨20, distinct_times_same_clock.2⟩

def firstPause : Nat := Nat.find pause_exists

theorem clock_before_twenty_one (t : Fin 21) : publicationClock t.val = t.val := by
  fin_cases t <;> apply publicationClock_unique <;> norm_num [ternaryDepth]

theorem no_earlier_pause : ∀ t : Fin 20,
    publicationClock t.val ≠ publicationClock (t.val + 1) := by
  intro t
  have h0 := clock_before_twenty_one ⟨t.val, by omega⟩
  have h1 := clock_before_twenty_one ⟨t.val + 1, by omega⟩
  simp only [Fin.val_mk] at h0 h1
  omega

theorem firstPause_eq_twenty : firstPause = 20 := by
  apply (Nat.find_eq_iff pause_exists).mpr
  constructor
  · exact distinct_times_same_clock.2
  · intro n hn
    exact no_earlier_pause ⟨n, hn⟩

def addSix (x y : Nat) : Nat := encodeSix fun j =>
  (TerminalSelector.digit6 x j.val + TerminalSelector.digit6 y j.val) % 3

def positiveDefect : Nat := encodeSix fun j => if j.val < 3 then 0 else 1
def negativeDefect : Nat := encodeSix fun j => if j.val < 3 then 0 else 2

def publishedBands (t : Nat) : Array Nat :=
  (rowFromPrefixes regionalPrefixes t).bands

def dualChargeWord (word : Nat) : Nat :=
  (2 * TerminalSelector.digit6 word 0 + TerminalSelector.digit6 word 1 +
    TerminalSelector.digit6 word 2 + TerminalSelector.digit6 word 3 +
    TerminalSelector.digit6 word 4 + TerminalSelector.digit6 word 5) % 3

theorem dualChargeWord_correct (word : Nat) :
    dualChargeWord word = wittDualCharge (fun _ => bandFromWord word) 0 := by
  norm_num [dualChargeWord, wittDualCharge, wittImage, wittMatrix,
    bandFromWord, TerminalSelector.digit6, Fin.sum_univ_succ]
  omega

def phaseDualWord (bands : Array Nat) (phase : Nat) : Nat :=
  let coefficient := fun i : Fin 3 =>
    if dualChargeWord bands[i.val]! = phase then 1 else 2
  encodeSix fun j =>
    (coefficient 0 * TerminalSelector.digit6 bands[0]! j.val +
      coefficient 1 * TerminalSelector.digit6 bands[1]! j.val +
      coefficient 2 * TerminalSelector.digit6 bands[2]! j.val) % 3

def descriptorFromPrefixes (prefixes : Fin 3 → Nat) (time : Nat) : Nat :=
  let bands := fun t => (rowFromPrefixes prefixes t).bands
  let predecessor := time - 9
  let mirrorPropagation := addSix ((bands (time + 1))[1]!) negativeDefect
  let defectTail := (negativeDefect % 27) * 27 + positiveDefect % 27
  let descriptor12 := 729 * mirrorPropagation + defectTail
  let returningSum := addSix ((bands (predecessor + 1))[0]!)
    ((bands (predecessor + 1))[1]!)
  let descriptor18 := 729 * descriptor12 + returningSum
  let phaseWord := phaseDualWord (bands predecessor) ((predecessor - 1) % 3)
  729 * descriptor18 + phaseWord

def regionalW24 : Nat := descriptorFromPrefixes regionalPrefixes firstPause

theorem opposite_defects_cancel : addSix positiveDefect negativeDefect = 0 := by
  decide

theorem descriptor_exact_evaluation : descriptorFromPrefixes prefixInputs 20 =
    TerminalSelector.w24Input := by
  decide

theorem regionalW24_eq_input : regionalW24 = TerminalSelector.w24Input := by
  unfold regionalW24
  rw [regionalPrefixes_eq_inputs, firstPause_eq_twenty]
  exact descriptor_exact_evaluation

theorem regionalW24_value : regionalW24 = 66241910521 := by
  exact regionalW24_eq_input

end HMT.I.RegionalW24
end

#print axioms HMT.I.RegionalW24.firstPause_eq_twenty
#print axioms HMT.I.RegionalW24.dualChargeWord_correct
#print axioms HMT.I.RegionalW24.opposite_defects_cancel
#print axioms HMT.I.RegionalW24.descriptor_exact_evaluation
#print axioms HMT.I.RegionalW24.regionalW24_eq_input
