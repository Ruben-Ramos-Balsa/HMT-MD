import PrefixFrameProjection
import SelectedCylinderSignature

/-!
Compose the existing successful mixed-radix producer with the calibrated
exceptional reader. A produced JointOutput contains the three actual cylinder
states, their children, and their jointly computed signature. The child used
by the reader is the child actually returned by produce, not another input.

This is the regional cylinder/signature realization of the prefix theorem in
main_autosuficiente.tex:33981-34240. It does not rename JointOutput the complete
enriched state. The declared prefix-dependent frame transport remains explicit;
this file does not manufacture its microscopic rule or the terminal K domain.
-/

noncomputable section
namespace HMT.I.ProducedFrameProjection

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

open HMT.I.CalibratedPaleyTransport HMT.I.PrefixFrameProjection
open HMT.I.SelectedCylinderSignature HMT.I.JointRegionalFrontier
open HMT.I.JointCylinderSignature HMT.I.RegionalCylinderTransition
open HMT.I.RegionalPublicationComposition HMT.I.GeneratedN69Rows
open HMT.I.NativeKSelectedLattice HMT.I.IteratedJointProjection
open HMT.I.IteratedCylinderSelector

theorem produce_success (n k : Nat) : (produce n k).isSome = true := by
  rw [produce_correct]
  rfl

/-- Read the proven successful producer; no fallback state or output table. -/
def actualOutput (n k : Nat) : JointOutput :=
  (produce n k).get (produce_success n k)

theorem actualOutput_generated (n k : Nat) :
    actualOutput n k = generatedOutput n k := by
  simp only [actualOutput, produce_correct, Option.get_some]

theorem actualOutput_produced (n k : Nat) :
    produce n k = some (actualOutput n k) := by
  rw [actualOutput_generated, produce_correct]

def emit (out : JointOutput) : Event :=
  fun c => toF3 (wordOfDigit (out.children c))

def producedHistory (decimalDepth : Nat → Nat) : History JointOutput :=
  fun n => actualOutput n (decimalDepth n)

/-- This discharges the emission interface for the actual producer. -/
theorem produced_emission (decimalDepth : Nat → Nat) (n : Nat) (c : Fin 3) :
    emit (producedHistory decimalDepth n) c = toF3 (actualWord n c) := by
  rw [actualWord_digit]
  simp only [producedHistory, actualOutput_generated, emit, generatedOutput]
  rfl

/-- The signature remains the signature of exactly the emitted children. -/
theorem produced_signature (decimalDepth : Nat → Nat) (n : Nat) :
    (producedHistory decimalDepth n).signature =
      signatureFromChildren (producedHistory decimalDepth n).children := by
  simp only [producedHistory, actualOutput_generated, generatedOutput]
  rfl

theorem produced_prefixes (decimalDepth : Nat → Nat) (n : Nat) (c : Fin 3) :
    Compatible ((producedHistory decimalDepth n).cylinders c) ∧
    ((producedHistory decimalDepth n).cylinders c).ternaryPrefix / 729 =
      publish (channelOfIndex c) 729 (by decide) n ∧
    ((producedHistory decimalDepth n).cylinders c).decimalPrefix / 1000 =
      publish (channelOfIndex c) 1000 (by decide) (decimalDepth n) :=
  selected_prefix_recovery n (decimalDepth n) _ (actualOutput_produced _ _) c

theorem produced_column_carry (decimalDepth : Nat → Nat) (n : Nat) (j : Fin 6) :
    (producedHistory decimalDepth n).signature.q j +
      3 * (producedHistory decimalDepth n).signature.c j =
      HMT.N69RegionalSignature.columnTotal (bandsGenerated n) j :=
  selected_column_carry n (decimalDepth n) _ (actualOutput_produced _ _) j

theorem produced_witt_charge (decimalDepth : Nat → Nat) (n : Nat) (c : Fin 3) :
    (producedHistory decimalDepth n).signature.wittDual c =
      (∑ j : Fin 6, HMT.N69RegionalSignature.wittResidue (bandsGenerated n) c j) % 3 :=
  selected_witt_charge n (decimalDepth n) _ (actualOutput_produced _ _) c

/-- One produced history, rather than a supplied agreement with a second one,
supports the transported code reader and the nested numerical cylinders. -/
theorem produced_double_reading (decimalDepth : Nat → Nat)
    (g : Transport JointOutput) (f0 : Frame) (n m : Nat) :
    (PrefixFrameProjection.Q emit g f0 (producedHistory decimalDepth) (n+m)).take n =
      PrefixFrameProjection.Q emit g f0 (producedHistory decimalDepth) n ∧
    (PrefixFrameProjection.Q emit g f0 (producedHistory decimalDepth) n).map readWords =
      (historyPrefix (producedHistory decimalDepth) n).map emit ∧
    (∀ c : Fin 3,
      IteratedCylinderSelector.run (channelOfIndex c) 729 (by decide) n =
        some (publish (channelOfIndex c) 729 (by decide) n) ∧
      (⋂ k : Nat, RegionalSemiopenLimit.cylinder (channelOfIndex c) k) =
        {value (channelOfIndex c)} ∧
      ∀ t : Fin n,
        readWords (entry emit g f0 (producedHistory decimalDepth) t.val) c =
          toF3 (wordOfDigit (publicationDigit t.val (n+m) c))) :=
  enriched_double_reading emit (producedHistory decimalDepth) g f0
    (produced_emission decimalDepth) n m

/-- The same returned state supplies the code head, unreduced column sum,
carry and both previous prefixes. None is selected independently. -/
theorem same_produced_state (decimalDepth : Nat → Nat)
    (g : Transport JointOutput) (f0 : Frame) (n : Nat) :
    produce n (decimalDepth n) = some (producedHistory decimalDepth n) ∧
    (∀ c : Fin 3,
      readWords (entry emit g f0 (producedHistory decimalDepth) n) c =
        toF3 (actualWord n c) ∧
      Compatible ((producedHistory decimalDepth n).cylinders c)) ∧
    (∀ j : Fin 6,
      (producedHistory decimalDepth n).signature.q j +
        3 * (producedHistory decimalDepth n).signature.c j =
        HMT.N69RegionalSignature.columnTotal (bandsGenerated n) j) := by
  refine ⟨actualOutput_produced _ _, ?_, produced_column_carry decimalDepth n⟩
  intro c
  exact ⟨produced_emission decimalDepth n c, (produced_prefixes decimalDepth n c).1⟩

end HMT.I.ProducedFrameProjection
end
