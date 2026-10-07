import CofinalCylinderSurvival
import GeneratedTransitionRecords
import JointCylinderSignature

/-!
The transition register is forced by a surviving regional block history.
The history is tested by cylinder inequalities at all observed depths; no
equality to a target block, register, or matrix is an input to this test.

This composes survival with the existing register and signature readers. It
does not assert that an unspecified update on the other enriched-state fibres
satisfies these inequalities or realizes the historical nine-step operator.
-/

noncomputable section
namespace HMT.I.SurvivingTransitionHistory

open TPKOrbits TPKLifts HMT.I.GeneratedN69Rows
open HMT.I.RegionalPublicationComposition HMT.I.RegionalCylinderTransition
open HMT.I.SurvivalCylinderSelection HMT.I.CofinalCylinderSurvival
open HMT.I.JointRegionalFrontier HMT.I.JointCylinderSignature
open HMT.I.GeneratedTransitionRecords HMT.I.RegionalTransitionRecords

abbrev BlockHistory := Nat → Fin 3 → Fin 729

def historyPrefix (u : BlockHistory) (i : Fin 3) : Nat → Nat
  | 0 => publish (channelOfIndex i) 729 (by decide) 0
  | n + 1 => 729 * historyPrefix u i n + (u n i).val

def Surviving (u : BlockHistory) : Prop :=
  ∀ n i, SurvivesAllDecimals (channelOfIndex i) n (historyPrefix u i n)

def Observed (u : BlockHistory) (κ : Nat → Nat) : Prop :=
  ∀ n i, ObservedSurvival (channelOfIndex i) n (historyPrefix u i n) κ

theorem observed_implies_surviving (u : BlockHistory) (κ : Nat → Nat)
    (hκ : CofinalDepth κ) (hu : Observed u κ) : Surviving u := by
  intro n i
  exact cofinal_observation_implies_survival _ _ _ κ hκ (hu n i)

theorem surviving_prefix (u : BlockHistory) (hu : Surviving u) (n : Nat) (i : Fin 3) :
    historyPrefix u i n = publish (channelOfIndex i) 729 (by decide) n :=
  survival_selects_publication _ _ _ (hu n i)

theorem surviving_block (u : BlockHistory) (hu : Surviving u) (n : Nat) (i : Fin 3) :
    u n i = jointChild n i := by
  apply Fin.ext
  have hn := surviving_prefix u hu n i
  have hs := surviving_prefix u hu (n + 1) i
  change 729 * historyPrefix u i n + (u n i).val =
    publish (channelOfIndex i) 729 (by decide) (n + 1) at hs
  rw [hn] at hs
  have hp := publication_step (channelOfIndex i) 729 (by decide) n
  dsimp [jointChild, nextTernary]
  omega

theorem joint_prefix (n : Nat) (i : Fin 3) :
    historyPrefix jointChild i n = publish (channelOfIndex i) 729 (by decide) n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change 729 * historyPrefix jointChild i n + (jointChild n i).val = _
      rw [ih]
      exact (publication_step (channelOfIndex i) 729 (by decide) n).symm

theorem joint_history_survives : Surviving jointChild := by
  intro n i
  rw [joint_prefix]
  exact (survival_iff_publication _ _ _).2 rfl

theorem unique_surviving_history : ∃! u : BlockHistory, Surviving u := by
  refine ⟨jointChild, joint_history_survives, ?_⟩
  intro u hu
  funext n i
  exact surviving_block u hu n i

def word (u : BlockHistory) (n : Nat) (i : Fin 3) : Word :=
  let b := bandFromWord (u n i).val
  ⟨(b 0).val, (b 1).val, (b 2).val, (b 3).val, (b 4).val, (b 5).val⟩

def register (u : BlockHistory) (n : Nat) : Matrix :=
  ⟨word u n 0, word u (n + 1) 0, word u n 1, word u (n + 1) 1,
    word u n 2, word u (n + 1) 2⟩

theorem surviving_word (u : BlockHistory) (hu : Surviving u) (n : Nat) (i : Fin 3) :
    word u n i = wordGenerated n i := by
  unfold word
  rw [surviving_block u hu n i]
  rfl

theorem surviving_register (u : BlockHistory) (hu : Surviving u) (n : Nat) :
    register u n = recordGenerated n := by
  unfold register recordGenerated
  simp only [surviving_word u hu]

theorem surviving_registers_recover_lifts (u : BlockHistory) (hu : Surviving u) :
    solveMatrix (register u 0) (register u 1) = regionalLift0 ∧
    solveMatrix (register u 2) (register u 3) = regionalLift1 := by
  simp only [surviving_register u hu]
  exact generated_lifts_eq_regional

theorem surviving_history_has_same_signature (u : BlockHistory) (hu : Surviving u)
    (n : Nat) : signatureFromChildren (u n) = signatureGenerated n := by
  apply signature_of_admissible_children
  intro i
  exact (child_admissible_iff _ _ _).2 (surviving_block u hu n i)

theorem different_block_has_finite_rejection (u : BlockHistory)
    (n : Nat) (i : Fin 3) (h : u n i ≠ jointChild n i) :
    ∃ m k : Nat, ¬ Compatible
      ⟨m, k, historyPrefix u i m, publish (channelOfIndex i) 1000 (by decide) k⟩ := by
  by_contra hnone
  push_neg at hnone
  have hprefix (m : Nat) : historyPrefix u i m = publish (channelOfIndex i) 729 (by decide) m :=
    survival_selects_publication _ _ _ (hnone m)
  have hn := hprefix n
  have hs := hprefix (n + 1)
  change 729 * historyPrefix u i n + (u n i).val = _ at hs
  rw [hn] at hs
  have hp := publication_step (channelOfIndex i) 729 (by decide) n
  apply h
  apply Fin.ext
  dsimp [jointChild, nextTernary]
  omega

end HMT.I.SurvivingTransitionHistory
end

#print axioms HMT.I.SurvivingTransitionHistory.observed_implies_surviving
#print axioms HMT.I.SurvivingTransitionHistory.surviving_prefix
#print axioms HMT.I.SurvivingTransitionHistory.surviving_block
#print axioms HMT.I.SurvivingTransitionHistory.joint_prefix
#print axioms HMT.I.SurvivingTransitionHistory.joint_history_survives
#print axioms HMT.I.SurvivingTransitionHistory.unique_surviving_history
#print axioms HMT.I.SurvivingTransitionHistory.surviving_word
#print axioms HMT.I.SurvivingTransitionHistory.surviving_register
#print axioms HMT.I.SurvivingTransitionHistory.surviving_registers_recover_lifts
#print axioms HMT.I.SurvivingTransitionHistory.surviving_history_has_same_signature
#print axioms HMT.I.SurvivingTransitionHistory.different_block_has_finite_rejection
