import PaleyWittDuality
import NativeKSelectedLattice

/-!
The chart in Article I, exc:paley-codigo, constructs the conference matrix
from quadratic residues on F5 in the ordered chart (infinity,0,1,2,3,4).
This file links that rule to the already certified ternary encoder.
The chart identification is explicit; it is not asserted to be selected by
the terminal K producer. No result about FLM or the Monster is assumed here.
-/
namespace HMT.I.PaleyCharacterConstruction

open HMT.IV.CoxeterNeighbor

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

def quadraticCharacter (x : ZMod 5) : ℤ :=
  if x = 0 then 0 else if ∃ y : ZMod 5, y * y = x then 1 else -1

def conference : Matrix (Fin 6) (Fin 6) ℤ := fun i j =>
  if i = 0 then (if j = 0 then 0 else 1)
  else if j = 0 then 1
  else quadraticCharacter (((j.val - 1 : ℕ) : ZMod 5) -
    ((i.val - 1 : ℕ) : ZMod 5))

def reducedConference : Matrix (Fin 6) (Fin 6) (ZMod 3) :=
  fun i j => (conference i j : ZMod 3)

theorem character_values :
    quadraticCharacter 0 = 0 ∧ quadraticCharacter 1 = 1 ∧
    quadraticCharacter 2 = -1 ∧ quadraticCharacter 3 = -1 ∧
    quadraticCharacter 4 = 1 := by decide +kernel

theorem conference_symmetric : Matrix.transpose conference = conference := by
  decide +kernel

theorem conference_square :
    conference * conference = (5 : ℤ) • (1 : Matrix (Fin 6) (Fin 6) ℤ) := by
  decide +kernel

theorem reduced_conference_eq : reducedConference = paleyWitt := by
  decide +kernel

theorem reduced_conference_square :
    reducedConference * reducedConference =
      -(1 : Matrix (Fin 6) (Fin 6) (ZMod 3)) := by
  rw [reduced_conference_eq]
  exact HMT.PaleyWittDuality.paleyWitt_square

def generatedEncode (w : Fin 6 → ZMod 3) : Fin 12 → ZMod 3 :=
  fun i => if h : i.val < 6 then w ⟨i.val, h⟩ else
    Matrix.vecMul w reducedConference ⟨i.val - 6, by have := i.isLt; omega⟩

theorem generated_encode_eq (w : Fin 6 → ZMod 3) : generatedEncode w = encode w := by
  unfold generatedEncode
  rw [reduced_conference_eq]
  rfl

theorem generated_encoder_injective : Function.Injective generatedEncode := by
  intro x y h
  apply HMT.PaleyWittDuality.encoder_injective
  simpa only [generated_encode_eq] using h

theorem generated_image_eq : Set.range generatedEncode = (wittCode : Set (Fin 12 → ZMod 3)) := by
  ext v
  constructor
  · rintro ⟨w, rfl⟩
    rw [generated_encode_eq]
    exact ⟨w, rfl⟩
  · rintro ⟨w, rfl⟩
    exact ⟨w, generated_encode_eq w⟩

theorem generated_code_self_dual :
    HMT.PaleyWittDuality.orthogonal = Set.range generatedEncode := by
  rw [generated_image_eq]
  exact HMT.PaleyWittDuality.wittCode_selfDual

/-! Apply the reconstructed chart to the actual native selectors, not to a
second list of target words. This part has no PublishedRegister assumption. -/
open HMT.I.NativeKSelectedLattice HMT.I.KMarkedIncidence
open HMT.II.CKM.Incidence

theorem native_generated_encodings :
    (TPKLifts.selectedSeeds.map toF3).map generatedEncode =
      [encode closureWord, encode propagationWord, encode autoscaleWord] := by
  rw [native_three_selected_words]
  simp only [List.map_cons, List.map_nil, generated_encode_eq]

def generatedSupport (w : Fin 6 → ZMod 3) : Finset (Fin 12) :=
  Finset.univ.filter fun i => generatedEncode w i ≠ 0

theorem generated_support_eq (w : Fin 6 → ZMod 3) :
    generatedSupport w = wordSupport w := by
  simp only [generatedSupport, generated_encode_eq, wordSupport]

theorem native_generated_supports :
    (TPKLifts.selectedSeeds.map toF3).map generatedSupport =
      [closureSupport, hexadSupport, autoscaleSupport] := by
  have h : generatedSupport = wordSupport := funext generated_support_eq
  rw [h]
  exact native_regional_incidence

#print axioms character_values
#print axioms conference_symmetric
#print axioms conference_square
#print axioms reduced_conference_eq
#print axioms reduced_conference_square
#print axioms generated_encode_eq
#print axioms generated_encoder_injective
#print axioms generated_image_eq
#print axioms generated_code_self_dual
#print axioms native_generated_encodings
#print axioms generated_support_eq
#print axioms native_generated_supports

end HMT.I.PaleyCharacterConstruction
