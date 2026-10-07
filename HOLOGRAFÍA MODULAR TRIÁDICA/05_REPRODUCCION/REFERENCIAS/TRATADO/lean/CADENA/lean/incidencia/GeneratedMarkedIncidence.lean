import NativeFourPlusOne

/-!
Reunited composition of the native TPK seed selector with the Paley support
reader, the unique marked hexad, its incidence origin and the marked lattice.

The three regional words are obtained from `TPKLifts.selectedSeeds`; they are
not parameters. The additional APP word is the source word `appWord`, whose
membership in the produced TPK catalogue is proved. Membership alone is not
asserted to be a unique selector of that additional word.

This module does not assume `PublishedRegister` or any twelve-block register.
It proves selection of the incidence flag and the marked lattice. It does not
identify uniqueness of the hexad with uniqueness or generation of the integer
register K, and does not add a VOA or Moonshine conclusion.
-/

namespace HMT.I.GeneratedMarkedIncidence

set_option maxRecDepth 12000
set_option maxHeartbeats 12000000

open HMT.I.PaleyCharacterConstruction HMT.I.NativeKSelectedLattice
open HMT.I.NativeFourPlusOne HMT.I.KMarkedIncidence HMT.I.KSelectedLattice
open HMT.II.CKM.Incidence
open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality
open HMT.IV.NeighborSpan HMT.IV.NeighborLattice
open HMT.IV.NeighborDuality HMT.IV.NeighborMinimum HMT.IV.NeighborRank

noncomputable section

/-- Keep the reconstructed lifts and their common calendar in the composition.
The X/Y transition records retain the status declared by the source module. -/
theorem reconstructed_transport_and_calendar :
    (TPKLifts.mul TPKLifts.X0 TPKLifts.L0 = TPKLifts.Y0 ∧
      TPKLifts.mul TPKLifts.X1 TPKLifts.L1 = TPKLifts.Y1) ∧
    (∀ M, TPKLifts.TernaryMatrix M →
      TPKLifts.mul TPKLifts.X0 M = TPKLifts.Y0 → M = TPKLifts.L0) ∧
    (∀ M, TPKLifts.TernaryMatrix M →
      TPKLifts.mul TPKLifts.X1 M = TPKLifts.Y1 → M = TPKLifts.L1) ∧
    TPKLifts.calendar = [false, false, true, true] ∧
    TPKLifts.acceptedCalendars.length = 1 ∧
    TPKLifts.biographies = TPKLifts.referenceBiographies := by
  exact ⟨TPKLifts.transition_equations, TPKLifts.L0_unique,
    TPKLifts.L1_unique, TPKLifts.calendar_reconstructed,
    TPKLifts.calendar_unique, TPKLifts.biographies_match_records⟩

def generatedSupports : List (Finset (Fin 12)) :=
  (TPKLifts.selectedSeeds.map toF3).map generatedSupport

def generatedClosure : Finset (Fin 12) := (generatedSupports[0]?).getD ∅
def generatedPropagation : Finset (Fin 12) := (generatedSupports[1]?).getD ∅
def generatedAutoscale : Finset (Fin 12) := (generatedSupports[2]?).getD ∅

theorem generated_supports_exact :
    generatedSupports = [closureSupport, hexadSupport, autoscaleSupport] :=
  native_generated_supports

theorem generated_closure_eq : generatedClosure = closureSupport := by
  simp only [generatedClosure, generated_supports_exact]
  rfl

theorem generated_propagation_eq : generatedPropagation = hexadSupport := by
  simp only [generatedPropagation, generated_supports_exact]
  rfl

theorem generated_autoscale_eq : generatedAutoscale = autoscaleSupport := by
  simp only [generatedAutoscale, generated_supports_exact]
  rfl

theorem generated_tetrad_eq :
    generatedPropagation ∩ generatedClosure = nativeTetrad := by
  rw [generated_propagation_eq, generated_closure_eq, native_tetrad_eq]
  rfl

def generatedIncidenceRule (h : Finset (Fin 12)) : Prop :=
  h.card = 6 ∧ nativeTetrad ⊆ h ∧ h ⊆ generatedClosure ∧
    (h ∩ generatedPropagation).card = 4 ∧
    (h ∩ generatedAutoscale).card = 3 ∧
    (h ∩ generatedSupport appWord).card = 2

theorem generated_incidence_rule_iff (h : Finset (Fin 12)) :
    generatedIncidenceRule h ↔ incidenceRule h := by
  unfold generatedIncidenceRule incidenceRule
  rw [native_tetrad_eq, generated_closure_eq, generated_propagation_eq,
    generated_autoscale_eq, generated_support_eq]
  rfl

theorem generated_hexad_existsUnique :
    ∃! h : Finset (Fin 12),
      (∃ w : Fin 6 → ZMod 3, generatedSupport w = h) ∧
      generatedIncidenceRule h := by
  refine ⟨alphaHexad, ?_, ?_⟩
  · constructor
    · obtain ⟨w, hw⟩ := selected_hexad_exists
      exact ⟨w, (generated_support_eq w).trans hw⟩
    · exact (generated_incidence_rule_iff alphaHexad).mpr alpha_incidence_rule
  · rintro h ⟨⟨w, hw⟩, hh⟩
    have hs : wordSupport w = h := (generated_support_eq w).symm.trans hw
    have hi := (generated_incidence_rule_iff h).mp hh
    have hu := selected_hexad_unique w (hs.symm ▸ hi)
    exact hs.symm.trans hu

theorem generated_hexad_identification (h : Finset (Fin 12))
    (hw : ∃ w : Fin 6 → ZMod 3, generatedSupport w = h)
    (hi : generatedIncidenceRule h) : h = alphaHexad := by
  obtain ⟨w, hw⟩ := hw
  have hs : wordSupport w = h := (generated_support_eq w).symm.trans hw
  exact hs.symm.trans
    (selected_hexad_unique w (hs.symm ▸ (generated_incidence_rule_iff h).mp hi))

/-- The residual singleton is formed from the generated regional supports. -/
def generatedOriginSupport : Finset (Fin 12) :=
  (generatedPropagation ∩ generatedAutoscale) \
    (alphaHexad ∪ generatedSupport appWord)

theorem generated_origin_eq : generatedOriginSupport = originSupport := by
  unfold generatedOriginSupport originSupport
  rw [generated_propagation_eq, generated_autoscale_eq, generated_support_eq]
  rfl

theorem generated_origin_singleton : generatedOriginSupport = {origin} := by
  rw [generated_origin_eq, origin_support_exact, origin_eq_zero]

def generatedOrigin : Fin 12 :=
  generatedOriginSupport.min' (by rw [generated_origin_singleton]; simp)

private theorem minimum_of_singleton (s : Finset (Fin 12)) (point : Fin 12)
    (hs : s = {point}) (hne : s.Nonempty) : s.min' hne = point := by
  subst s
  simp

theorem generated_origin_value : generatedOrigin = origin :=
  minimum_of_singleton generatedOriginSupport origin generated_origin_singleton _

def generatedRadial : Space 12 := radial (marked generatedOrigin)

theorem generated_radial_eq : generatedRadial = selectedRadial := by
  unfold generatedRadial selectedRadial
  rw [generated_origin_value]

theorem generated_lattice_properties :
    Module.Finite ℤ (neighborSubgroup wittCode generatedRadial) ∧
    Module.Free ℤ (neighborSubgroup wittCode generatedRadial) ∧
    Module.finrank ℤ (neighborSubgroup wittCode generatedRadial) = 24 ∧
    Module.finrank ℚ (Submodule.span ℚ (neighbor wittCode generatedRadial)) = 24 ∧
    (∀ x : Space 12, x ≠ 0 → 0 < pairing x x) ∧
    EvenNeighbor wittCode generatedRadial ∧
    IntegralNeighbor wittCode generatedRadial ∧
    integralDual (neighborSubgroup wittCode generatedRadial) =
      neighbor wittCode generatedRadial ∧
    (∀ x ∈ neighbor wittCode generatedRadial, x ≠ 0 → 4 ≤ pairing x x) ∧
    (∃ x ∈ neighbor wittCode generatedRadial, pairing x x = 4) := by
  rw [generated_radial_eq]
  exact selected_lattice_properties

/-- A single statement retains every intermediate object of the composition. -/
theorem native_seed_incidence_lattice_composition :
    appWord ∈ TPKOrbits.producedWords.map toF3 ∧
    generatedSupports = [closureSupport, hexadSupport, autoscaleSupport] ∧
    generatedPropagation ∩ generatedClosure = nativeTetrad ∧
    nativeTetrad.card = 4 ∧
    (∃! h : Finset (Fin 12),
      (∃ w : Fin 6 → ZMod 3, generatedSupport w = h) ∧ generatedIncidenceRule h) ∧
    generatedOriginSupport = {generatedOrigin} ∧
    pairing generatedRadial generatedRadial = 54 ∧
    Module.finrank ℤ (neighborSubgroup wittCode generatedRadial) = 24 ∧
    IntegralNeighbor wittCode generatedRadial ∧
    integralDual (neighborSubgroup wittCode generatedRadial) =
      neighbor wittCode generatedRadial ∧
    (∀ x ∈ neighbor wittCode generatedRadial, x ≠ 0 → 4 ≤ pairing x x) := by
  refine ⟨native_app_word_produced, generated_supports_exact,
    generated_tetrad_eq, native_tetrad_card, generated_hexad_existsUnique,
    ?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [generated_origin_value]
    exact generated_origin_singleton
  · rw [generated_radial_eq]
    exact selected_radial_norm
  · exact generated_lattice_properties.2.2.1
  · exact generated_lattice_properties.2.2.2.2.2.2.1
  · exact generated_lattice_properties.2.2.2.2.2.2.2.1
  · exact generated_lattice_properties.2.2.2.2.2.2.2.2.1

#print axioms reconstructed_transport_and_calendar
#print axioms generated_supports_exact
#print axioms generated_tetrad_eq
#print axioms generated_hexad_existsUnique
#print axioms generated_hexad_identification
#print axioms generated_origin_singleton
#print axioms generated_origin_value
#print axioms generated_lattice_properties
#print axioms native_seed_incidence_lattice_composition

end
end HMT.I.GeneratedMarkedIncidence
