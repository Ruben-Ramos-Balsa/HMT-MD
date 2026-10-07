import PrefixFrameProjection

noncomputable section
open HMT.I.CalibratedPaleyTransport HMT.I.PrefixFrameProjection

example {State : Type} (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x y : History State) (n m : Nat) (hmn : m ≤ n)
    (h : ∀ j < m, x j = y j) :
    (Q emit g f0 x n).take m = Q emit g f0 y m :=
  projective_naturality emit g f0 x y n m hmn h

example {State : Type} (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (q : Nat → Entry)
    (hq : ∀ n, (List.range n).map q = Q emit g f0 x n) :
    q = Qinf emit g f0 x := Qinf_unique emit g f0 x q hq

example {State : Type} (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x y : History State) (h : Qinf emit g f0 x = Qinf emit g f0 y) :
    (fun n => emit (x n)) = (fun n => emit (y n)) :=
  Qinf_visible_faithful emit g f0 x y h

example {State : Type} (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    (n + 9) % 9 = n % 9 ∧
    (Q emit g f0 x (n + 9)).take n = Q emit g f0 x n ∧
    Q emit g f0 x (n + 9) ≠ Q emit g f0 x n :=
  nine_preserves_and_extends emit g f0 x n

example (f : Frame) (A : Mat) (w : Word) :
    gamma (conjugate f A) (rowChange f w) = pairedChange f (gamma A w) :=
  gamma_covariant f A w

example {State : Type} (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    transportedOperator g f0 x n * transportedOperator g f0 x n = -1 :=
  transported_square g f0 x n

example (n : Nat) :
    Q id (fun _ => 1) 1 emittedHistory n =
      (HMT.I.IteratedJointProjection.Q n).map labelFixedFrame :=
  fixed_frame_extends_previous n

open HMT.I.RegionalPublicationComposition HMT.I.GeneratedN69Rows
open HMT.I.JointRegionalFrontier HMT.I.IteratedCylinderSelector
open HMT.I.NativeKSelectedLattice HMT.I.IteratedJointProjection

example {State : Type} (emit : State → Event) (x : History State)
    (g : Transport State) (f0 : Frame)
    (hstream : ∀ t c, emit (x t) c = toF3 (actualWord t c)) (n m : Nat) :
    (HMT.I.PrefixFrameProjection.Q emit g f0 x (n+m)).take n =
      HMT.I.PrefixFrameProjection.Q emit g f0 x n ∧
    (HMT.I.PrefixFrameProjection.Q emit g f0 x n).map readWords = (historyPrefix x n).map emit ∧
    (∀ c : Fin 3,
      run (channelOfIndex c) 729 (by decide) n =
        some (publish (channelOfIndex c) 729 (by decide) n) ∧
      (⋂ k : Nat, HMT.I.RegionalSemiopenLimit.cylinder (channelOfIndex c) k) =
        {value (channelOfIndex c)} ∧
      ∀ t : Fin n,
        readWords (entry emit g f0 x t.val) c =
          toF3 (wordOfDigit (publicationDigit t.val (n+m) c))) :=
  enriched_double_reading emit x g f0 hstream n m

end
