import KSelectedLattice
import TPKLifts

/-! Reuse the already proved native TPK region selectors. This is a typed
coordinate conversion, not a second selection of their published words. -/
namespace HMT.I.NativeKSelectedLattice

open HMT.I.KMarkedIncidence HMT.I.KSelectedLattice
open HMT.II.CKM.Incidence
open HMT.IncidenceRegister HMT.IV.CoxeterNeighbor HMT.IV.NeighborLattice

def toF3 (w : TPKOrbits.Word) : Fin 6 → ZMod 3 :=
  ![(w.a : ZMod 3), (w.b : ZMod 3), (w.c : ZMod 3),
    (w.d : ZMod 3), (w.e : ZMod 3), (w.f : ZMod 3)]

theorem native_three_selected_words :
    TPKLifts.selectedSeeds.map toF3 =
      [closureWord, propagationWord, autoscaleWord] := by
  rw [TPKLifts.selected_seeds_checked]
  rfl

theorem native_closure_word :
    TPKRegions.orientedClosure.map toF3 = [closureWord] := by
  rw [TPKRegions.oriented_closure_checked]
  rfl

theorem native_propagation_word :
    TPKSimpleRegions.propagationWords.map toF3 = [propagationWord] := by
  rw [TPKSimpleRegions.propagation_oriented_checked]
  rfl

theorem native_autoscale_word :
    TPKSimpleRegions.autoscaleWords.map toF3 = [autoscaleWord] := by
  rw [TPKSimpleRegions.autoscale_oriented_checked]
  rfl

/-- The fourth frame word belongs to the produced native image. This is not
claimed to be uniqueness of its separate frame selection. -/
theorem native_app_word_produced :
    appWord ∈ TPKOrbits.producedWords.map toF3 := by
  apply List.mem_map.mpr
  refine ⟨⟨0,2,2,0,2,0⟩, ?_, rfl⟩
  rw [TPKOrbits.word_witness_checked]
  decide +kernel

theorem native_regional_incidence :
    (TPKLifts.selectedSeeds.map toF3).map wordSupport =
      [closureSupport, hexadSupport, autoscaleSupport] := by
  rw [native_three_selected_words]
  rfl

theorem native_register_to_lattice (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    TPKLifts.selectedSeeds.map toF3 = [closureWord, propagationWord, autoscaleWord] ∧
    registerHighSupport l = markedFace ∧
    originSupport = {origin} ∧ pairing selectedRadial selectedRadial = 54 ∧
    Module.finrank ℤ (neighborSubgroup wittCode selectedRadial) = 24 ∧
    (∀ x ∈ neighbor wittCode selectedRadial, x ≠ 0 → 4 ≤ pairing x x) := by
  have h := register_to_selected_lattice l hl
  exact ⟨native_three_selected_words, h.1, h.2.1, h.2.2.1,
    h.2.2.2.1, h.2.2.2.2.2.2⟩

#print axioms native_three_selected_words
#print axioms native_closure_word
#print axioms native_propagation_word
#print axioms native_autoscale_word
#print axioms native_app_word_produced
#print axioms native_regional_incidence
#print axioms native_register_to_lattice

end HMT.I.NativeKSelectedLattice
