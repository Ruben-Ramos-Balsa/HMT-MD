import CalibratedPaleyTransport
import IteratedJointProjection

/-!
Prefix-determined frame transport for the same emitted three-channel history.
Source: the 775-page monograph, main_autosuficiente.tex:33981-34240,
lector-excepcional-global-rev6 and doble-realizacion-global-rev6.

The frame update is an operation on the accumulated enriched prefix. It is
not a new independent frame choice at each depth. The theorem is parametric
in this declared transport and does not identify it with all hidden fibres
of Gamma9, nor supply a terminal K instance. The actual regional execution
is specialized below; its numeric coordinate is not an input to transport.
-/

noncomputable section
namespace HMT.I.PrefixFrameProjection

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

open HMT.I.CalibratedPaleyTransport
open HMT.I.PaleyCharacterConstruction
open HMT.I.IteratedJointProjection
open HMT.I.NativeKSelectedLattice
open HMT.I.RegionalPublicationComposition HMT.I.GeneratedN69Rows
open HMT.I.JointRegionalFrontier HMT.I.IteratedCylinderSelector

abbrev Event := Fin 3 → Word
abbrev History (State : Type) := Nat → State
abbrev Transport (State : Type) := List State → Frame

variable {State : Type}

def historyPrefix (x : History State) (n : Nat) : List State := (List.range n).map x

def frameAt (g : Transport State) (f0 : Frame) (x : History State) : Nat → Frame
  | 0 => f0
  | n + 1 => g (historyPrefix x (n + 1)) * frameAt g f0 x n

theorem prefix_eq_of_agreement (x y : History State) (n : Nat)
    (h : ∀ j < n, x j = y j) : historyPrefix x n = historyPrefix y n := by
  apply List.map_congr_left
  intro j hj
  exact h j (List.mem_range.mp hj)

theorem frame_depends_only_on_prefix (g : Transport State) (f0 : Frame)
    (x y : History State) (n : Nat) (h : ∀ j < n, x j = y j) :
    frameAt g f0 x n = frameAt g f0 y n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [frameAt, prefix_eq_of_agreement x y (n+1) h,
        ih (fun j hj => h j (by omega))]

def transportedOperator (g : Transport State) (f0 : Frame) (x : History State) (n : Nat) : Mat :=
  conjugate (frameAt g f0 x n) reducedConference

theorem transported_square (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    transportedOperator g f0 x n * transportedOperator g f0 x n = -1 :=
  generated_square_preserved (frameAt g f0 x n)

abbrev Entry := Frame × (Fin 3 → Word × Word)

def entry (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) : Entry :=
  (frameAt g f0 x n, fun c =>
    CalibratedPaleyTransport.gamma (transportedOperator g f0 x n) (emit (x n) c))

def readWords (a : Entry) : Event := fun c => (a.2 c).1

theorem read_entry (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    readWords (entry emit g f0 x n) = emit (x n) := rfl

theorem entry_depends_only_on_prefix (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x y : History State) (n : Nat) (h : ∀ j < n + 1, x j = y j) :
    entry emit g f0 x n = entry emit g f0 y n := by
  have hf := frame_depends_only_on_prefix g f0 x y n (fun j hj => h j (by omega))
  simp only [entry, transportedOperator, hf, h n (by omega)]

def Q (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) : List Entry :=
  (List.range n).map (entry emit g f0 x)

theorem Q_length (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    (Q emit g f0 x n).length = n := by simp [Q]

theorem Q_truncate (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n m : Nat) :
    (Q emit g f0 x (n + m)).take n = Q emit g f0 x n := by
  simp [Q, ← List.map_take, List.take_range, Nat.min_eq_left (Nat.le_add_right n m)]

theorem Q_depends_only_on_prefix (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x y : History State) (n : Nat) (h : ∀ j < n, x j = y j) :
    Q emit g f0 x n = Q emit g f0 y n := by
  apply List.map_congr_left
  intro j hj
  apply entry_depends_only_on_prefix
  intro k hk
  exact h k (by have := List.mem_range.mp hj; omega)

/-- Naturality for two enriched extensions of the same finite prefix. -/
theorem projective_naturality (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x y : History State) (n m : Nat) (hmn : m ≤ n)
    (h : ∀ j < m, x j = y j) :
    (Q emit g f0 x n).take m = Q emit g f0 y m := by
  have hn : n = m + (n - m) := by omega
  rw [hn, Q_truncate]
  exact Q_depends_only_on_prefix emit g f0 x y m h

theorem Q_visible_prefix (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    (Q emit g f0 x n).map readWords = (historyPrefix x n).map emit := by
  simp only [Q, historyPrefix, List.map_map, Function.comp_def, read_entry]

def Qinf (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) : Nat → Entry := entry emit g f0 x

theorem Qinf_compatible (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    (List.range n).map (Qinf emit g f0 x) = Q emit g f0 x n := rfl

theorem Qinf_unique (emit : State → Event) (g : Transport State) (f0 : Frame) (x : History State)
    (q : Nat → Entry)
    (hq : ∀ n, (List.range n).map q = Q emit g f0 x n) :
    q = Qinf emit g f0 x := by
  funext j
  have h := (List.map_inj_left.mp (hq (j + 1))) j (List.mem_range.mpr (by omega))
  exact h

theorem Qinf_visible_faithful (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x y : History State) (h : Qinf emit g f0 x = Qinf emit g f0 y) :
    (fun n => emit (x n)) = (fun n => emit (y n)) := by
  funext n
  exact congrArg readWords (congrFun h n)

theorem nine_preserves_and_extends (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    (n + 9) % 9 = n % 9 ∧
    (Q emit g f0 x (n + 9)).take n = Q emit g f0 x n ∧
    Q emit g f0 x (n + 9) ≠ Q emit g f0 x n := by
  refine ⟨by omega, Q_truncate emit g f0 x n 9, ?_⟩
  intro h
  have hl := congrArg List.length h
  simp only [Q_length] at hl
  omega

def emittedHistory : History Event := fun t c => toF3 (actualWord t c)

theorem identity_frames (x : History State) (n : Nat) :
    frameAt (fun _ => (1 : Frame)) 1 x n = 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [frameAt, ih, one_mul]

def labelFixedFrame (p : Fin 3 → HMT.PaleyWittDuality.Word12) : Entry :=
  (1, fun c => (HMT.PaleyWittDuality.head (p c), HMT.PaleyWittDuality.tail (p c)))

/-- The older fixed-frame construction is recovered exactly, not replaced. -/
theorem fixed_frame_extends_previous (n : Nat) :
    Q id (fun _ => 1) 1 emittedHistory n =
      (IteratedJointProjection.Q n).map labelFixedFrame := by
  simp only [Q, IteratedJointProjection.Q, List.map_map]
  apply List.map_congr_left
  intro t _
  simp only [entry, transportedOperator, identity_frames, conjugate,
    Units.val_one, inv_one, one_mul, mul_one, emittedHistory, id_eq,
    labelFixedFrame, Function.comp_apply, IteratedJointProjection.panel]
  congr 1
  funext c
  rw [generated_pair, generated_encode_eq, IteratedJointProjection.gamma_eq]

/-- Retain the complete enriched witness while connecting its emission to the
existing regional run. The compatibility is an explicit interface, not a new
producer or a terminal-register selection premise. Hidden memory stays in x
and is available to g before every frame update. -/
theorem enriched_double_reading (emit : State → Event) (x : History State)
    (g : Transport State) (f0 : Frame)
    (hstream : ∀ t c, emit (x t) c = toF3 (actualWord t c)) (n m : Nat) :
    (Q emit g f0 x (n+m)).take n = Q emit g f0 x n ∧
    (Q emit g f0 x n).map readWords = (historyPrefix x n).map emit ∧
    (∀ c : Fin 3,
      run (channelOfIndex c) 729 (by decide) n =
        some (publish (channelOfIndex c) 729 (by decide) n) ∧
      (⋂ k : Nat, RegionalSemiopenLimit.cylinder (channelOfIndex c) k) =
        {value (channelOfIndex c)} ∧
      ∀ t : Fin n,
        readWords (entry emit g f0 x t.val) c =
          toF3 (wordOfDigit (publicationDigit t.val (n+m) c))) := by
  refine ⟨Q_truncate _ _ _ _ _ _, Q_visible_prefix _ _ _ _ _, ?_⟩
  intro c
  refine ⟨run_correct _ _ _ _, RegionalSemiopenLimit.intersection_singleton _, ?_⟩
  intro t
  rw [read_entry, hstream t.val c, actualWord_from_publication t.val (n+m) c (by omega)]

/-- The transported incidence and the numerical limit use the same actual
successful run. No second history or independently selected word is added. -/
theorem transported_double_reading (g : Transport Event) (f0 : Frame) (n m : Nat) :
    (Q id g f0 emittedHistory (n+m)).take n = Q id g f0 emittedHistory n ∧
    (Q id g f0 emittedHistory n).map readWords = historyPrefix emittedHistory n ∧
    (∀ c : Fin 3,
      run (channelOfIndex c) 729 (by decide) n =
        some (publish (channelOfIndex c) 729 (by decide) n) ∧
      (⋂ k : Nat, RegionalSemiopenLimit.cylinder (channelOfIndex c) k) =
        {value (channelOfIndex c)} ∧
      ∀ t : Fin n,
        readWords (entry id g f0 emittedHistory t.val) c =
          toF3 (wordOfDigit (publicationDigit t.val (n+m) c))) := by
  simpa using enriched_double_reading id emittedHistory g f0 (fun _ _ => rfl) n m

end HMT.I.PrefixFrameProjection
end
