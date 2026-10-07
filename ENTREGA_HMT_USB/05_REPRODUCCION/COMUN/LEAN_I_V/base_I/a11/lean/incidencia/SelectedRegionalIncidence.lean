import SelectedFromRegionalInputs
import GeneratedMarkedIncidence
import RegionalPrecarry

/-!
Composition of the selected regional-input register with the generated native
incidence flag and marked lattice. The two actual readers are the high-block
support K_i >= 729 and the negative support of regional pre-carry. They are
not a mod-3 support and not the negative support of H4(K).

The regional publications, N69 rows, panel and W24 are produced by the imported
readers. The inherited unordered S8 interface is still explicit; this module
does not assert that it has been generated. The finite terminal selector also
retains its inherited Lean.ofReduceBool assumption. No PublishedRegister
hypothesis or terminal-register equality is added here.
-/

noncomputable section
namespace HMT.I.SelectedRegionalIncidence

open HMT.I.TerminalSelector HMT.I.KMarkedIncidence
open HMT.I.NativeFourPlusOne HMT.I.PaleyCharacterConstruction
open HMT.II.CKM.Incidence
open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality
open HMT.IV.NeighborSpan HMT.IV.NeighborLattice
open HMT.IV.NeighborDuality HMT.IV.NeighborMinimum HMT.IV.NeighborRank

set_option maxHeartbeats 12000000
set_option maxRecDepth 12000

theorem regional_register_digits : regionalRegister.digits =
    [234,543,140,729,659,824,621,58,914,794,146,601] := by
  rw [regionalRegister_eq_selected]
  exact selected_register_digits

def selectedHighSupport : Finset (Fin 12) :=
  Finset.univ.filter fun i => 729 ≤ regionalRegister.digits[i.val]!

theorem selected_high_support_is_native_tetrad :
    selectedHighSupport = nativeTetrad := by
  unfold selectedHighSupport
  rw [regional_register_digits, native_tetrad_eq, marked_face_exact]
  decide +kernel

theorem selected_high_support_is_generated_intersection :
    selectedHighSupport =
      GeneratedMarkedIncidence.generatedPropagation ∩
        GeneratedMarkedIncidence.generatedClosure :=
  selected_high_support_is_native_tetrad.trans
    GeneratedMarkedIncidence.generated_tetrad_eq.symm

/-- Computed before comparison with the historical signed-vector display. -/
def selectedPrecarry (i : Fin 12) : Int :=
  RegionalPrecarry.regionalBlock .closure i +
    RegionalPrecarry.regionalBlock .propagation i -
    RegionalPrecarry.regionalBlock .autoscale i -
    (regionalRegister.digits[i.val]! : Int)

theorem selected_precarry_evaluates : selectedPrecarry = preCarry := by
  funext i
  unfold selectedPrecarry RegionalPrecarry.regionalBlock
  rw [regional_register_digits, RegionalPrecarry.generated_prefix_evaluates.1,
    RegionalPrecarry.generated_prefix_evaluates.2.1,
    RegionalPrecarry.generated_prefix_evaluates.2.2]
  fin_cases i <;> norm_num [preCarry]

def selectedNegativeSupport : Finset (Fin 12) :=
  Finset.univ.filter fun i : Fin 12 => selectedPrecarry i < 0

theorem selected_negative_support_is_alpha_hexad :
    selectedNegativeSupport = alphaHexad := by
  unfold selectedNegativeSupport
  rw [selected_precarry_evaluates]
  exact signed_support_exact

theorem selected_flag_is_generated_incidence :
    selectedHighSupport ⊆ selectedNegativeSupport ∧
    selectedHighSupport.card = 4 ∧ selectedNegativeSupport.card = 6 ∧
    GeneratedMarkedIncidence.generatedIncidenceRule selectedNegativeSupport ∧
    (∃ w : Fin 6 → ZMod 3, generatedSupport w = selectedNegativeSupport) := by
  rw [selected_high_support_is_native_tetrad, selected_negative_support_is_alpha_hexad]
  refine ⟨?_, native_tetrad_card, alpha_incidence_rule.1, ?_, ?_⟩
  · rw [native_tetrad_eq]
    exact alpha_incidence_rule.2.1
  · exact (GeneratedMarkedIncidence.generated_incidence_rule_iff alphaHexad).mpr
      alpha_incidence_rule
  · obtain ⟨w, hw⟩ := selected_hexad_exists
    exact ⟨w, (generated_support_eq w).trans hw⟩

def selectedOriginSupport : Finset (Fin 12) :=
  (GeneratedMarkedIncidence.generatedPropagation ∩
    GeneratedMarkedIncidence.generatedAutoscale) \
    (selectedNegativeSupport ∪ generatedSupport appWord)

theorem selected_origin_support_is_generated :
    selectedOriginSupport = GeneratedMarkedIncidence.generatedOriginSupport := by
  unfold selectedOriginSupport GeneratedMarkedIncidence.generatedOriginSupport
  rw [selected_negative_support_is_alpha_hexad]

theorem selected_origin_singleton :
    selectedOriginSupport = {GeneratedMarkedIncidence.generatedOrigin} := by
  rw [selected_origin_support_is_generated, GeneratedMarkedIncidence.generated_origin_value]
  exact GeneratedMarkedIncidence.generated_origin_singleton

def selectedOrigin : Fin 12 :=
  selectedOriginSupport.min' (by rw [selected_origin_singleton]; simp)

private theorem minimum_of_singleton (s : Finset (Fin 12)) (point : Fin 12)
    (hs : s = {point}) (hne : s.Nonempty) : s.min' hne = point := by
  subst s
  simp

theorem selected_origin_is_generated :
    selectedOrigin = GeneratedMarkedIncidence.generatedOrigin :=
  minimum_of_singleton selectedOriginSupport
    GeneratedMarkedIncidence.generatedOrigin selected_origin_singleton _

def selectedRadial : Space 12 := radial (marked selectedOrigin)

theorem selected_radial_is_generated :
    selectedRadial = GeneratedMarkedIncidence.generatedRadial := by
  unfold selectedRadial GeneratedMarkedIncidence.generatedRadial
  rw [selected_origin_is_generated]

theorem selected_incidence_lattice_properties :
    selectedHighSupport = nativeTetrad ∧
    selectedNegativeSupport = alphaHexad ∧
    selectedOriginSupport = {selectedOrigin} ∧
    pairing selectedRadial selectedRadial = 54 ∧
    Module.Finite ℤ (neighborSubgroup wittCode selectedRadial) ∧
    Module.Free ℤ (neighborSubgroup wittCode selectedRadial) ∧
    Module.finrank ℤ (neighborSubgroup wittCode selectedRadial) = 24 ∧
    EvenNeighbor wittCode selectedRadial ∧
    IntegralNeighbor wittCode selectedRadial ∧
    integralDual (neighborSubgroup wittCode selectedRadial) =
      neighbor wittCode selectedRadial ∧
    (∀ x ∈ neighbor wittCode selectedRadial, x ≠ 0 → 4 ≤ pairing x x) ∧
    (∃ x ∈ neighbor wittCode selectedRadial, pairing x x = 4) := by
  refine ⟨selected_high_support_is_native_tetrad,
    selected_negative_support_is_alpha_hexad, ?_, ?_⟩
  · rw [selected_origin_is_generated]
    exact selected_origin_singleton
  · rw [selected_radial_is_generated]
    have hp := GeneratedMarkedIncidence.generated_lattice_properties
    refine ⟨?_, hp.1, hp.2.1, hp.2.2.1, hp.2.2.2.2.2⟩
    rw [GeneratedMarkedIncidence.generated_radial_eq]
    exact KSelectedLattice.selected_radial_norm

/-- Arithmetic realization and incidence realization of the same selected
register. This is not a whole-HMT double-projection or Moonshine theorem. -/
theorem arithmetic_and_incidence_of_same_register :
    (∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart regionalRegister VacancyDeltaBounds.vacancyDelta x = 0 ∧
      (∀ n : Nat, (AlphaPublications.publication regionalRegister n).outgoing = 0 ∧
        (AlphaPublications.publication regionalRegister n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat)) ∧
    (selectedHighSupport = nativeTetrad ∧
      selectedNegativeSupport = alphaHexad ∧
      selectedOriginSupport = {selectedOrigin} ∧
      pairing selectedRadial selectedRadial = 54 ∧
      Module.Finite ℤ (neighborSubgroup wittCode selectedRadial) ∧
      Module.Free ℤ (neighborSubgroup wittCode selectedRadial) ∧
      Module.finrank ℤ (neighborSubgroup wittCode selectedRadial) = 24 ∧
      EvenNeighbor wittCode selectedRadial ∧
      IntegralNeighbor wittCode selectedRadial ∧
      integralDual (neighborSubgroup wittCode selectedRadial) =
        neighbor wittCode selectedRadial ∧
      (∀ x ∈ neighbor wittCode selectedRadial, x ≠ 0 → 4 ≤ pairing x x) ∧
      (∃ x ∈ neighbor wittCode selectedRadial, pairing x x = 4)) :=
  ⟨regional_terminal_alpha, selected_incidence_lattice_properties⟩

end HMT.I.SelectedRegionalIncidence
end

#print axioms HMT.I.SelectedRegionalIncidence.regional_register_digits
#print axioms HMT.I.SelectedRegionalIncidence.selected_high_support_is_native_tetrad
#print axioms HMT.I.SelectedRegionalIncidence.selected_high_support_is_generated_intersection
#print axioms HMT.I.SelectedRegionalIncidence.selected_precarry_evaluates
#print axioms HMT.I.SelectedRegionalIncidence.selected_negative_support_is_alpha_hexad
#print axioms HMT.I.SelectedRegionalIncidence.selected_flag_is_generated_incidence
#print axioms HMT.I.SelectedRegionalIncidence.selected_origin_support_is_generated
#print axioms HMT.I.SelectedRegionalIncidence.selected_origin_singleton
#print axioms HMT.I.SelectedRegionalIncidence.selected_origin_is_generated
#print axioms HMT.I.SelectedRegionalIncidence.selected_radial_is_generated
#print axioms HMT.I.SelectedRegionalIncidence.selected_incidence_lattice_properties
#print axioms HMT.I.SelectedRegionalIncidence.arithmetic_and_incidence_of_same_register
