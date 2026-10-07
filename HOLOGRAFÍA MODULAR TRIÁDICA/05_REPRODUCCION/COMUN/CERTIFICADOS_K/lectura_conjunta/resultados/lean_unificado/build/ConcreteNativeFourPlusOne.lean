import ConcreteWittChart
import ConcreteBinaryGolay
import SelectedRegionalIncidence

/-!
Composition of the existing selected HMT register with the concrete Golay
realization. Neither BinaryGolayData nor IncidenceChart is a hypothesis of
the terminal theorem. The actual selected high support is used, and the
selected negative-support hexad has a unique octad lift in the same chart.
-/
namespace HMT.I.ConcreteNativeFourPlusOne

open HMT.I.HexadOctadResidual HMT.I.HexadOctadFourPlusOne
open HMT.I.ConcreteBinaryGolay HMT.I.ConcreteWittChart
open HMT.I.NativeFourPlusOne HMT.I.SelectedRegionalIncidence

def incidenceChart : golay.IncidenceChart where
  sourceHexads := sourceHexads
  positions := positions
  image_dodecad := positions_image
  preserves := source_hexads_preserved

theorem native_four_plus_one_concrete :
    let T := nativeTetrad.image positions
    (hexadStar golay T).card = 4 ∧ (liftedStar golay T).card = 4 ∧
    (octadStar golay T).card = 5 ∧
    ∃ O : Support, golay.IsOctad O ∧ O ∩ golay.dodecad = T ∧
      O ∉ liftedStar golay T ∧
      octadStar golay T = insert O (liftedStar golay T) :=
  native_four_plus_one golay incidenceChart

theorem selected_register_four_plus_one :
    let T := selectedHighSupport.image positions
    (hexadStar golay T).card = 4 ∧ (liftedStar golay T).card = 4 ∧
    (octadStar golay T).card = 5 ∧
    ∃ O : Support, golay.IsOctad O ∧ O ∩ golay.dodecad = T ∧
      O ∉ liftedStar golay T ∧
      octadStar golay T = insert O (liftedStar golay T) := by
  rw [selected_high_support_is_native_tetrad]
  exact native_four_plus_one_concrete

theorem selected_negative_support_has_unique_octad :
    ∃! O : Support, golay.IsOctad O ∧
      O ∩ golay.dodecad = selectedNegativeSupport.image positions := by
  have h := selected_flag_is_generated_incidence
  have hs : selectedNegativeSupport ∈ sourceHexads := by
    obtain ⟨w, hw⟩ := h.2.2.2.2
    exact ⟨w, hw, h.2.2.1⟩
  exact golay.residual_unique_lift _ (incidenceChart.preserves _ hs)

theorem selected_tetrad_image :
    selectedHighSupport.image positions = {4, 6, 8, 14} := by
  rw [selected_high_support_is_native_tetrad, native_tetrad_eq]
  exact marked_tetrad_image

end HMT.I.ConcreteNativeFourPlusOne

#print axioms HMT.I.ConcreteNativeFourPlusOne.incidenceChart
#print axioms HMT.I.ConcreteNativeFourPlusOne.native_four_plus_one_concrete
#print axioms HMT.I.ConcreteNativeFourPlusOne.selected_register_four_plus_one
#print axioms HMT.I.ConcreteNativeFourPlusOne.selected_negative_support_has_unique_octad
#print axioms HMT.I.ConcreteNativeFourPlusOne.selected_tetrad_image
