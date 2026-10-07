import RegionalSemiopenLimit
import PaleyCharacterConstruction

/-!
Recovered double reading of the actual iterated regional history. The common
index labels refinement, not nine microscopic Sel/Tra/Upd updates. Each entry
retains all three channels together and encodes the emitted six-trit word as
(w,wA) in the explicitly constructed Paley chart. The initial frame is identity.
No target word list, S8 selector, terminal K producer, changing frame, lattice
limit, vertex algebra or Moonshine identification is constructed here.

The Option execution remains explicit. Its totalization uses a proof of success,
never a default value; this proof comes from the existing iterated selector.
-/

noncomputable section
namespace HMT.I.IteratedJointProjection

open HMT.I.RegionalPublicationComposition HMT.I.GeneratedN69Rows
open HMT.I.JointRegionalFrontier HMT.I.GeneratedTransitionRecords
open HMT.I.IteratedCylinderSelector HMT.I.PaleyCharacterConstruction
open HMT.I.NativeKSelectedLattice HMT.PaleyWittDuality
open HMT.IV.CoxeterNeighbor

theorem word_success (t : Nat) (c : Fin 3) : (word t c).isSome = true := by
  rw [word_correct]
  rfl

/-- Read the actual successful Option; there is no fallback word. -/
def actualWord (t : Nat) (c : Fin 3) : TPKOrbits.Word :=
  (word t c).get (word_success t c)

theorem actualWord_generated (t : Nat) (c : Fin 3) :
    actualWord t c = wordGenerated t c := by
  simp only [actualWord, word_correct, Option.get_some]

theorem actualWord_emitted (t : Nat) (c : Fin 3) :
    word t c = some (actualWord t c) := by
  rw [actualWord_generated, word_correct]

def initialFrame : Equiv.Perm (Fin 12) := Equiv.refl _

/-- Explicit initial-frame realization of the pre-existing (w,wA) encoder. -/
def gamma (w : TPKOrbits.Word) : Word12 :=
  fun j => generatedEncode (toF3 w) (initialFrame.symm j)

theorem gamma_eq (w : TPKOrbits.Word) : gamma w = encode (toF3 w) :=
  generated_encode_eq _

theorem gamma_head (w : TPKOrbits.Word) : head (gamma w) = toF3 w := by
  rw [gamma_eq, head_encode]

theorem gamma_tail (w : TPKOrbits.Word) :
    tail (gamma w) = Matrix.vecMul (toF3 w) reducedConference := by
  rw [gamma_eq, tail_encode, reduced_conference_eq]

theorem gamma_mem (w : TPKOrbits.Word) : gamma w ∈ wittCode := by
  rw [gamma_eq]
  exact ⟨toF3 w, rfl⟩

def recover (v : Word12) : TPKOrbits.Word :=
  ⟨(head v 0).val, (head v 1).val, (head v 2).val,
    (head v 3).val, (head v 4).val, (head v 5).val⟩

theorem recover_digit (d : Fin 729) :
    recover (gamma (wordOfDigit d)) = wordOfDigit d := by
  simp only [recover, gamma_head]
  simp [toF3, wordOfDigit, bandFromWord, ZMod.val_natCast]

theorem actualWord_digit (t : Nat) (c : Fin 3) :
    actualWord t c = wordOfDigit ⟨blockGenerated t c, generated_block_lt t c⟩ := by
  rw [actualWord_generated]
  rfl

theorem recover_actualWord (t : Nat) (c : Fin 3) :
    recover (gamma (actualWord t c)) = actualWord t c := by
  rw [actualWord_digit]
  exact recover_digit _

/-- One chronological entry contains the three regions, not separate clocks. -/
def panel (t : Nat) : Fin 3 → Word12 := fun c => gamma (actualWord t c)

def Q (n : Nat) : List (Fin 3 → Word12) := (List.range n).map panel

/-- Retain the original failure semantics while collecting a joint entry. -/
def attemptPanel (t : Nat) : Option (Fin 3 → Word12) := do
  let a ← word t 0
  let b ← word t 1
  let c ← word t 2
  pure ![gamma a, gamma b, gamma c]

theorem attemptPanel_correct (t : Nat) : attemptPanel t = some (panel t) := by
  simp only [attemptPanel, actualWord_emitted, Bind.bind, Option.bind, Pure.pure]
  congr 1
  funext c
  fin_cases c <;> rfl

def attemptQ : Nat → Option (List (Fin 3 → Word12))
  | 0 => some []
  | n + 1 => do
      let prior ← attemptQ n
      let next ← attemptPanel n
      pure (prior ++ [next])

theorem attemptQ_correct (n : Nat) : attemptQ n = some (Q n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [attemptQ, ih, attemptPanel_correct, Option.bind_some, pure]
      simp [Q, List.range_succ, List.map_append]

theorem Q_length (n : Nat) : (Q n).length = n := by simp [Q]

/-- The whole joint history, not merely the latest block, is conserved. -/
theorem Q_truncate (n m : Nat) : (Q (n + m)).take n = Q n := by
  simp [Q, ← List.map_take, List.take_range, Nat.min_eq_left (Nat.le_add_right n m)]

/-- Equal phase labels do not erase the accumulated coded history. This is a
statement about refinement indices, not an identification with TPK holonomy. -/
theorem nine_more_preserves_and_extends (n : Nat) :
    (n + 9) % 9 = n % 9 ∧ (Q (n + 9)).take n = Q n ∧ Q (n + 9) ≠ Q n := by
  refine ⟨by omega, Q_truncate n 9, ?_⟩
  intro h
  have hl := congrArg List.length h
  simp only [Q_length] at hl
  omega

theorem attemptQ_truncate (n m : Nat) :
    (attemptQ (n + m)).map (List.take n) = attemptQ n := by
  rw [attemptQ_correct, attemptQ_correct, Option.map_some, Q_truncate]

theorem Q_get (n : Nat) (t : Fin n) :
    (Q n).get ⟨t.val, by simpa only [Q_length] using t.isLt⟩ = panel t.val := by
  simp [Q]

theorem Q_visible_history (n : Nat) :
    (Q n).map (fun p c => recover (p c)) =
      (List.range n).map (fun t c => actualWord t c) := by
  simp only [Q, List.map_map]
  congr 1
  funext t c
  exact recover_actualWord t c

theorem Q_membership (n : Nat) (p : Fin 3 → Word12) (hp : p ∈ Q n)
    (c : Fin 3) : p c ∈ wittCode := by
  obtain ⟨t, _, rfl⟩ := List.mem_map.mp hp
  exact gamma_mem _

def publicationDigit (t n : Nat) (c : Fin 3) : Fin 729 :=
  ⟨(publish (channelOfIndex c) 729 (by decide) n / 729 ^ (n - (t + 1))) % 729,
    Nat.mod_lt _ (by decide)⟩

/-- Any later computed publication recovers the same emitted natural word. -/
theorem actualWord_from_publication (t n : Nat) (c : Fin 3) (h : t < n) :
    actualWord t c = wordOfDigit (publicationDigit t n c) := by
  rw [actualWord_digit]
  apply congrArg wordOfDigit
  apply Fin.ext
  exact generated_block_from_longer_prefix t n c h

/-- Regeneration is the existing code map, not an independently stored target. -/
theorem panel_from_publication (t n : Nat) (c : Fin 3) (h : t < n) :
    panel t c = gamma (wordOfDigit (publicationDigit t n c)) := by
  exact congrArg gamma (actualWord_from_publication t n c h)

theorem recover_from_publication (t n : Nat) (c : Fin 3) (h : t < n) :
    recover (panel t c) = wordOfDigit (publicationDigit t n c) := by
  rw [panel, recover_actualWord, actualWord_from_publication t n c h]

/-- One common enclosure precision produces the entire nine-position,
three-channel coded window from the actual recursive parents. The existential
precision is shared; this is not nine independently assumed acceptance tests. -/
theorem joint_nine_code_selection (start : Nat) :
    ∃ j : Nat, ∀ c : Fin 3, ∀ r : Fin 9,
      ((run (channelOfIndex c) 729 (by decide) (start + r.val)).bind
        (fun parent => FiniteCylinderSelector.choose
          (lower (channelOfIndex c) j) (upper (channelOfIndex c) j)
          729 (by decide) (start + r.val) parent)).map
        (fun d => gamma (wordOfDigit d)) = some (panel (start + r.val) c) := by
  obtain ⟨j, hj⟩ := RegionalSemiopenLimit.common_nine_position_selection start
  refine ⟨j, ?_⟩
  intro c r
  rw [run_correct, Option.bind_some, hj (channelOfIndex c) r, Option.map_some]
  congr 1
  rw [panel, actualWord_digit]
  rfl

/-- Both readings use all prefixes of precisely the same successful execution. -/
theorem double_reading_compatible (n m : Nat) :
    attemptQ n = some (Q n) ∧ (Q (n + m)).take n = Q n ∧
    ∀ c : Fin 3,
      run (channelOfIndex c) 729 (by decide) n =
        some (publish (channelOfIndex c) 729 (by decide) n) ∧
      publish (channelOfIndex c) 729 (by decide) (n + m) / 729^m =
        publish (channelOfIndex c) 729 (by decide) n ∧
      value (channelOfIndex c) ∈ RegionalSemiopenLimit.cylinder (channelOfIndex c) n ∧
      (⋂ k : Nat, RegionalSemiopenLimit.cylinder (channelOfIndex c) k) =
        {value (channelOfIndex c)} ∧
      ∀ t : Fin n,
        recover (panel t.val c) = wordOfDigit (publicationDigit t.val (n + m) c) ∧
        panel t.val c ∈ wittCode := by
  refine ⟨attemptQ_correct n, Q_truncate n m, ?_⟩
  intro c
  refine ⟨run_correct _ _ _ _, publications_compatible _ _ _ _ _,
    RegionalSemiopenLimit.value_mem _ _, RegionalSemiopenLimit.intersection_singleton _, ?_⟩
  intro t
  exact ⟨recover_from_publication _ _ c (by omega), gamma_mem _⟩

end HMT.I.IteratedJointProjection
end

#print axioms HMT.I.IteratedJointProjection.attemptQ_correct
#print axioms HMT.I.IteratedJointProjection.Q_truncate
#print axioms HMT.I.IteratedJointProjection.nine_more_preserves_and_extends
#print axioms HMT.I.IteratedJointProjection.Q_visible_history
#print axioms HMT.I.IteratedJointProjection.panel_from_publication
#print axioms HMT.I.IteratedJointProjection.joint_nine_code_selection
#print axioms HMT.I.IteratedJointProjection.double_reading_compatible
