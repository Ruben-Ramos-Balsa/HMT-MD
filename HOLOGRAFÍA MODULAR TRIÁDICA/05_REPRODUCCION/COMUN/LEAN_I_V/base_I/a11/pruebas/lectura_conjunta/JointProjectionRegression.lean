import IteratedJointProjection
import NonadicJointRenewal

/-!
Fixed-type regression tests contributed by the independent reviewer and
integrated into the focal verifier. These apply existing proofs, not new
K-selection assumptions. The common witness remains outside all universals.
-/
noncomputable section
open HMT.I HMT.IV.CoxeterNeighbor
open HMT.I.RegionalPublicationComposition HMT.I.GeneratedN69Rows
open HMT.I.JointRegionalFrontier HMT.I.GeneratedTransitionRecords
open HMT.I.IteratedCylinderSelector HMT.I.PaleyCharacterConstruction
open HMT.I.NativeKSelectedLattice HMT.PaleyWittDuality
open HMT.I.IteratedJointProjection

example (start : Nat) :
    ∃ j : Nat, ∀ c : Fin 3, ∀ r : Fin 9,
      ((run (channelOfIndex c) 729 (by decide) (start + r.val)).bind
        (fun parent => FiniteCylinderSelector.choose
          (lower (channelOfIndex c) j) (upper (channelOfIndex c) j)
          729 (by decide) (start + r.val) parent)).map
        (fun d => gamma (wordOfDigit d)) = some (panel (start + r.val) c) :=
  joint_nine_code_selection start

example (n m : Nat) :
    attemptQ n = some (Q n) ∧ (Q (n + m)).take n = Q n ∧
    ∀ c : Fin 3,
      run (channelOfIndex c) 729 (by decide) n =
        some (publish (channelOfIndex c) 729 (by decide) n) ∧
      publish (channelOfIndex c) 729 (by decide) (n + m) / 729^m =
        publish (channelOfIndex c) 729 (by decide) n ∧
      value (channelOfIndex c) ∈ HMT.I.RegionalSemiopenLimit.cylinder (channelOfIndex c) n ∧
      (⋂ k : Nat, HMT.I.RegionalSemiopenLimit.cylinder (channelOfIndex c) k) =
        {value (channelOfIndex c)} ∧
      ∀ t : Fin n,
        recover (panel t.val c) = wordOfDigit (publicationDigit t.val (n + m) c) ∧
        panel t.val c ∈ wittCode :=
  double_reading_compatible n m

example (n : Nat) :
    (n + 9) % 9 = n % 9 ∧ (Q (n + 9)).take n = Q n ∧ Q (n + 9) ≠ Q n :=
  nine_more_preserves_and_extends n

example (n m : Nat) :
    (attemptQ (n + m)).map (List.take n) = attemptQ n :=
  attemptQ_truncate n m

open HMT.I.NonadicJointRenewal

example (f : PhaseObservable) (r : Fin 9) : iterate 9 f r = renewal (f r) :=
  ninefold_joint_renewal f r

example (r : Fin 9) (v u : Fibre) :
    iterate 9 (fun _ => pointIndicator v) r u = 1 / 468 :=
  ninefold_full_support r v u

example (u v : Fibre) : renewal (pointIndicator v) u ≠ pointIndicator v v :=
  renewal_not_point_evaluation u v

end
