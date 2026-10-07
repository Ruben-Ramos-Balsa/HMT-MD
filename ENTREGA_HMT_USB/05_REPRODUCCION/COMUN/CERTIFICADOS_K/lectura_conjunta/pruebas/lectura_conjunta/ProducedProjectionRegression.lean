import ProducedFrameProjection

noncomputable section
open HMT.I.ProducedFrameProjection HMT.I.SelectedCylinderSignature
open HMT.I.CalibratedPaleyTransport HMT.I.PrefixFrameProjection
open HMT.I.NativeKSelectedLattice HMT.I.IteratedJointProjection
open HMT.I.IteratedCylinderSelector
open HMT.I.JointRegionalFrontier HMT.I.JointCylinderSignature

example (k : Nat → Nat) (n : Nat) (c : Fin 3) :
    HMT.I.ProducedFrameProjection.emit (producedHistory k n) c = toF3 (actualWord n c) :=
  produced_emission k n c

example (k : Nat → Nat) (n : Nat) :
    (producedHistory k n).signature = signatureFromChildren (producedHistory k n).children :=
  produced_signature k n

example (k : Nat → Nat) (g : Transport JointOutput) (f0 : Frame) (n : Nat) :
    produce n (k n) = some (producedHistory k n) ∧
    (∀ c : Fin 3,
      readWords (entry HMT.I.ProducedFrameProjection.emit g f0 (producedHistory k) n) c =
        toF3 (actualWord n c) ∧
      HMT.I.RegionalCylinderTransition.Compatible ((producedHistory k n).cylinders c)) ∧
    (∀ j : Fin 6,
      (producedHistory k n).signature.q j + 3 * (producedHistory k n).signature.c j =
        HMT.N69RegionalSignature.columnTotal (bandsGenerated n) j) :=
  same_produced_state k g f0 n

example (k : Nat → Nat) (n : Nat) (c : Fin 3) :
    (producedHistory k n).signature.wittDual c =
      (∑ j : Fin 6, HMT.N69RegionalSignature.wittResidue (bandsGenerated n) c j) % 3 :=
  produced_witt_charge k n c

open HMT.I.RegionalPublicationComposition HMT.I.GeneratedN69Rows

example (k : Nat → Nat) (g : Transport JointOutput) (f0 : Frame) (n m : Nat) :
    (HMT.I.PrefixFrameProjection.Q HMT.I.ProducedFrameProjection.emit g f0
      (producedHistory k) (n+m)).take n =
      HMT.I.PrefixFrameProjection.Q HMT.I.ProducedFrameProjection.emit g f0
        (producedHistory k) n ∧
    (HMT.I.PrefixFrameProjection.Q HMT.I.ProducedFrameProjection.emit g f0
      (producedHistory k) n).map readWords =
      (historyPrefix (producedHistory k) n).map HMT.I.ProducedFrameProjection.emit ∧
    (∀ c : Fin 3,
      HMT.I.IteratedCylinderSelector.run (channelOfIndex c) 729 (by decide) n =
        some (publish (channelOfIndex c) 729 (by decide) n) ∧
      (⋂ j : Nat, HMT.I.RegionalSemiopenLimit.cylinder (channelOfIndex c) j) =
        {value (channelOfIndex c)} ∧
      ∀ t : Fin n,
        readWords (entry HMT.I.ProducedFrameProjection.emit g f0 (producedHistory k) t.val) c =
          toF3 (wordOfDigit (publicationDigit t.val (n+m) c))) :=
  produced_double_reading k g f0 n m

-- Protect the inherited no-reset property without adding another theorem.
example {State : Type} (emit : State → Event) (g : Transport State) (f0 : Frame)
    (x : History State) (n : Nat) :
    (n + 9) % 9 = n % 9 ∧
    (Q emit g f0 x (n + 9)).take n = Q emit g f0 x n ∧
    Q emit g f0 x (n + 9) ≠ Q emit g f0 x n :=
  nine_preserves_and_extends emit g f0 x n

end
