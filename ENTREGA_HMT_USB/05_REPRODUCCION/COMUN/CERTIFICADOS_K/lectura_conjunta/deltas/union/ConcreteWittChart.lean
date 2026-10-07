import ConcreteBinaryGolay
import PaleyCharacterConstruction
import NativeFourPlusOne

/-!
Explicit realization chart for Article I, exc:residuo-binario.
All 132 ternary hexads are transported, not merely the marked tetrad.
The coordinate choice is a chart of the already generated Witt incidence;
it is not an input to the HMT terminal register or a selector of constants.
-/
namespace HMT.I.ConcreteWittChart

open HMT.I.HexadOctadResidual
open HMT.I.PaleyCharacterConstruction
open HMT.I.ConcreteBinaryGolay

def position (i : Fin 12) : Fin 24 :=
  ![0, 1, 3, 4, 5, 6, 12, 7, 14, 8, 11, 10] i

theorem position_injective : Function.Injective position := by decide +kernel

def positions : Fin 12 ↪ Fin 24 := ⟨position, position_injective⟩

theorem positions_image : Finset.univ.image positions = dodecad := by native_decide

def ternaryIndex (w : Fin 6 → ZMod 3) : ℕ :=
  ∑ i, (w i).val * 3 ^ i.val

def sourceHexads : Set (Finset (Fin 12)) :=
  { H | ∃ w : Fin 6 → ZMod 3, generatedSupport w = H ∧ H.card = 6 }

def allHexads : Finset (Finset (Fin 12)) :=
  (Finset.univ.image generatedSupport).filter fun H => H.card = 6

theorem mem_allHexads (H : Finset (Fin 12)) : H ∈ allHexads ↔ H ∈ sourceHexads := by
  simp only [allHexads, Finset.mem_filter, Finset.mem_image, Finset.mem_univ,
    true_and, sourceHexads, Set.mem_setOf_eq]
  aesop

theorem allHexads_card : allHexads.card = 132 := by native_decide

theorem marked_tetrad_image :
    HMT.II.CKM.Incidence.markedFace.image positions = {4, 6, 8, 14} := by native_decide


def witnessIndices : List ℕ := [
  0, 31, 31, 574, 33, 1313, 574, 1313, 33, 120, 667, 1127, 2630, 0, 2649, 326, 165, 89,
  120, 1127, 667, 326, 89, 165, 2630, 2649, 0, 12, 2671, 495, 78, 81, 0, 2638, 1325, 977,
  8, 0, 23, 54, 41, 0, 330, 0, 0, 1416, 2583, 663, 0, 0, 169, 1974, 0, 0,
  12, 495, 2671, 2638, 977, 1325, 78, 0, 81, 1416, 663, 2583, 1974, 0, 0, 0, 169, 0,
  8, 23, 0, 330, 0, 0, 54, 0, 41, 3936, 3, 255, 350, 321, 0, 34, 2625, 705,
  24, 7, 0, 1318, 0, 1337, 90, 0, 0, 664, 2823, 135, 166, 0, 0, 0, 0, 697,
  656, 0, 655, 174, 0, 177, 0, 2637, 0, 20, 11, 0, 0, 0, 0, 0, 0, 0,
  2792, 0, 0, 0, 0, 0, 2262, 0, 0, 272, 15, 1295, 1326, 0, 0, 46, 0, 0,
  0, 0, 1399, 0, 0, 0, 86, 0, 0, 360, 0, 0, 0, 329, 0, 0, 0, 0,
  3936, 255, 3, 34, 705, 2625, 350, 0, 321, 664, 135, 2823, 0, 697, 0, 166, 0, 0,
  24, 0, 7, 90, 0, 0, 1318, 1337, 0, 272, 1295, 15, 46, 0, 0, 1326, 0, 0,
  360, 0, 0, 0, 0, 0, 0, 0, 329, 0, 1399, 0, 86, 0, 0, 0, 0, 0,
  656, 655, 0, 0, 0, 2637, 174, 177, 0, 2792, 0, 0, 2262, 0, 0, 0, 0, 0,
  20, 0, 11, 0, 0, 0, 0, 0, 0, 320, 2271, 95, 2, 0, 29, 1406, 2785, 353,
  184, 167, 0, 646, 665, 0, 0, 0, 281, 2628, 1319, 39, 6, 0, 0, 1286, 0, 0,
  1328, 1327, 0, 14, 0, 17, 2830, 0, 0, 328, 0, 343, 0, 0, 0, 0, 0, 0,
  2632, 0, 0, 0, 0, 0, 0, 3945, 0, 688, 175, 83, 0, 657, 0, 142, 0, 0,
  712, 0, 0, 0, 0, 0, 246, 0, 0, 0, 0, 43, 10, 0, 0, 0, 0, 0,
  32, 0, 63, 30, 1, 0, 2590, 0, 0, 88, 0, 71, 0, 0, 0, 0, 0, 0,
  0, 2631, 0, 0, 0, 0, 2662, 0, 0, 2640, 2639, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  80, 0, 0, 0, 0, 0, 0, 0, 113, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  40, 0, 0, 0, 0, 0, 0, 0, 0, 160, 1983, 323, 670, 0, 0, 0, 1409, 0,
  984, 0, 0, 0, 0, 0, 486, 0, 0, 1316, 0, 0, 0, 0, 5, 0, 0, 0,
  0, 0, 335, 0, 0, 0, 1134, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  1320, 0, 0, 0, 0, 0, 0, 0, 0, 172, 0, 0, 658, 0, 0, 0, 0, 0,
  0, 567, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  320, 95, 2271, 1406, 353, 2785, 2, 29, 0, 2628, 39, 1319, 1286, 0, 0, 6, 0, 0,
  184, 0, 167, 0, 281, 0, 646, 0, 665, 688, 83, 175, 142, 0, 0, 0, 0, 657,
  0, 43, 0, 0, 0, 0, 10, 0, 0, 712, 0, 0, 246, 0, 0, 0, 0, 0,
  1328, 0, 1327, 2830, 0, 0, 14, 17, 0, 2632, 0, 0, 0, 0, 3945, 0, 0, 0,
  328, 343, 0, 0, 0, 0, 0, 0, 0, 160, 323, 1983, 0, 0, 1409, 670, 0, 0,
  1316, 0, 0, 0, 0, 0, 0, 5, 0, 984, 0, 0, 486, 0, 0, 0, 0, 0,
  172, 0, 0, 0, 0, 0, 658, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 567, 0, 0, 0, 0, 0, 0, 0, 335, 0, 1134, 0, 0, 0, 0, 0,
  1320, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  32, 63, 0, 2590, 0, 0, 30, 0, 1, 0, 0, 2631, 2662, 0, 0, 0, 0, 0,
  88, 71, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 113, 0, 0, 0, 0,
  40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  2640, 0, 2639, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 22, 0, 0]

def liftMessage (w : Fin 6 → ZMod 3) : Message :=
  messageOfIndex ⟨(witnessIndices.getD (ternaryIndex w) 0) % 4096,
    Nat.mod_lt _ (by decide)⟩

theorem finite_lift_certificate : ∀ w : Fin 6 → ZMod 3,
    (generatedSupport w).card = 6 →
    (encodeSupport (liftMessage w)).card = 8 ∧
    encodeSupport (liftMessage w) ∩ dodecad = (generatedSupport w).image positions := by
  native_decide

theorem source_hexads_preserved (H : Finset (Fin 12)) (hH : H ∈ sourceHexads) :
    golay.IsResidualHexad (H.image positions) := by
  obtain ⟨w, rfl, hw⟩ := hH
  refine ⟨?_, encodeSupport (liftMessage w), ?_, (finite_lift_certificate w hw).2⟩
  · rw [Finset.card_image_of_injective _ positions.injective]
    exact hw
  · exact ⟨(mem_code_iff _).mpr ⟨liftMessage w, rfl⟩,
      (finite_lift_certificate w hw).1⟩

def residualHexads : Finset Support :=
  (octads.image fun O => O ∩ dodecad).filter fun H => H.card = 6

theorem residualHexads_card : residualHexads.card = 132 := by native_decide

theorem complete_hexad_transport :
    allHexads.image (fun H => H.image positions) = residualHexads := by native_decide

theorem mem_residualHexads (H : Support) :
    H ∈ residualHexads ↔ golay.IsResidualHexad H := by
  simp only [residualHexads, Finset.mem_filter, Finset.mem_image]
  constructor
  · rintro ⟨⟨O, hO, hOH⟩, h6⟩
    exact ⟨h6, O, (mem_octads O).mp hO, hOH⟩
  · rintro ⟨h6, O, hO, hOH⟩
    exact ⟨⟨O, (mem_octads O).mpr hO, hOH⟩, h6⟩

theorem chart_covers_every_residual_hexad (H : Support) :
    golay.IsResidualHexad H ↔
      ∃ h ∈ sourceHexads, h.image positions = H := by
  rw [← mem_residualHexads, ← complete_hexad_transport]
  simp only [Finset.mem_image, mem_allHexads]

end HMT.I.ConcreteWittChart
#print axioms HMT.I.ConcreteWittChart.position_injective
#print axioms HMT.I.ConcreteWittChart.positions_image
#print axioms HMT.I.ConcreteWittChart.allHexads_card
#print axioms HMT.I.ConcreteWittChart.marked_tetrad_image
#print axioms HMT.I.ConcreteWittChart.finite_lift_certificate
#print axioms HMT.I.ConcreteWittChart.source_hexads_preserved
#print axioms HMT.I.ConcreteWittChart.residualHexads_card
#print axioms HMT.I.ConcreteWittChart.complete_hexad_transport
#print axioms HMT.I.ConcreteWittChart.chart_covers_every_residual_hexad
