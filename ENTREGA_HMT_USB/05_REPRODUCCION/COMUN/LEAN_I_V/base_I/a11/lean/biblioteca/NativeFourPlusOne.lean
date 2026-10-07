import HexadOctadFourPlusOne
import PaleyCharacterConstruction

/-!
Compose the actual native TPK regional selectors with the reconstructed
Paley encoder, its marked tetrad, and the four-plus-one incidence theorem.
The binary design and its incidence chart have the same status as in the
manuscript. No target word, target tetrad or PublishedRegister is an input.
-/

namespace HMT.I.NativeFourPlusOne

open HMT.I.PaleyCharacterConstruction HMT.I.NativeKSelectedLattice
open HMT.II.CKM.Incidence
open HMT.I.HexadOctadResidual HMT.I.HexadOctadResidual.BinaryGolayData
open HMT.I.HexadOctadFourPlusOne

noncomputable def nativeTetrad : Finset (Fin 12) :=
  let supports := (TPKLifts.selectedSeeds.map toF3).map generatedSupport
  (supports[1]?).getD ∅ ∩ (supports[0]?).getD ∅

theorem native_tetrad_eq : nativeTetrad = markedFace := by
  unfold nativeTetrad
  rw [native_generated_supports]
  rfl

theorem native_tetrad_card : nativeTetrad.card = 4 := by
  rw [native_tetrad_eq]
  exact marked_face_card

theorem native_four_plus_one (G : BinaryGolayData) (L : G.IncidenceChart) :
    let T := nativeTetrad.image L.positions
    (hexadStar G T).card = 4 ∧ (liftedStar G T).card = 4 ∧
    (octadStar G T).card = 5 ∧
    ∃ O : Support, G.IsOctad O ∧ O ∩ G.dodecad = T ∧
      O ∉ liftedStar G T ∧ octadStar G T = insert O (liftedStar G T) :=
  four_plus_one_along_chart G L nativeTetrad native_tetrad_card

#print axioms HMT.I.NativeFourPlusOne.native_tetrad_eq
#print axioms HMT.I.NativeFourPlusOne.native_tetrad_card
#print axioms HMT.I.NativeFourPlusOne.native_four_plus_one

end HMT.I.NativeFourPlusOne
