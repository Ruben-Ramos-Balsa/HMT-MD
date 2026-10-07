import APPArithmetic
import SelectedExceptionalChain
import SelectedVOAInput

/-! Final interface for the exceptional construction of Article I.

The HMT-native incidence, the selected mark and the lattice are reused.
The conclusion consists of proved outputs, not assumed fields of a certificate.
The visible sum/product defect and the radial norm are compared after their
respective constructions, with the quotient contribution retained separately.

The classical uniqueness theorem for the Leech lattice and the FLM construction
are referenced in the accompanying application note. They are not inserted as
Lean axioms and are not claimed to have been reproved by this file.
The inherited selector's Lean.ofReduceBool dependency is reported explicitly.
-/

noncomputable section
namespace HMT.I.ArticleIExceptionalInterface

open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality
open HMT.IV.NeighborSpan HMT.IV.NeighborLattice HMT.IV.NeighborDuality
open HMT.I.SelectedRegionalIncidence HMT.I.SelectedExceptionalChain
open HMT.I.SelectedVOAInput

/-- Intrinsic lattice properties required before the classical Leech
classification and FLM application. The rational realization is the same
constructed neighbor, not an independently postulated lattice. -/
def ClassicalLeechHypotheses (v : Space 12) : Prop :=
  Module.Finite ℤ (neighborSubgroup wittCode v) ∧
  Module.Free ℤ (neighborSubgroup wittCode v) ∧
  Module.finrank ℤ (neighborSubgroup wittCode v) = 24 ∧
  Module.finrank ℚ (Submodule.span ℚ (neighbor wittCode v)) = 24 ∧
  (∀ x : Space 12, x ≠ 0 → 0 < pairing x x) ∧
  EvenNeighbor wittCode v ∧
  IntegralNeighbor wittCode v ∧
  integralDual (neighborSubgroup wittCode v) = neighbor wittCode v ∧
  (∀ x ∈ neighbor wittCode v, x ≠ 0 → 4 ≤ pairing x x) ∧
  (∃ x ∈ neighbor wittCode v, pairing x x = 4)

theorem selected_classical_hypotheses : ClassicalLeechHypotheses selectedRadial := by
  rw [selected_radial_is_generated]
  exact GeneratedMarkedIncidence.generated_lattice_properties

theorem same_generated_mark_and_lattice :
    selectedOrigin = GeneratedMarkedIncidence.generatedOrigin ∧
    selectedRadial = GeneratedMarkedIncidence.generatedRadial ∧
    neighbor wittCode selectedRadial =
      neighbor wittCode GeneratedMarkedIncidence.generatedRadial := by
  exact ⟨selected_origin_is_generated, selected_radial_is_generated,
    congrArg (neighbor wittCode) selected_radial_is_generated⟩

theorem selected_radial_norm_is_54 : pairing selectedRadial selectedRadial = 54 :=
  selected_incidence_lattice_properties.2.2.2.1

theorem sum_product_defect_matches_selected_norm :
    ((APPArithmetic.totalOverSupport APPArithmetic.productResidue -
      APPArithmetic.totalOverSupport APPArithmetic.sumResidue : ℕ) : ℚ) =
      pairing selectedRadial selectedRadial := by
  rw [APPArithmetic.census_product_residue, APPArithmetic.census_sum_residue,
    selected_radial_norm_is_54]
  norm_num

/-- The equality with the radial norm does not discard the quotient defect. -/
theorem full_sum_product_defect_retained :
    APPArithmetic.totalOverSupport APPArithmetic.productEval -
      APPArithmetic.totalOverSupport APPArithmetic.sumEval =
      (APPArithmetic.totalOverSupport APPArithmetic.productResidue -
        APPArithmetic.totalOverSupport APPArithmetic.sumResidue) +
        9 * (APPArithmetic.totalOverSupport APPArithmetic.productQuotient -
          APPArithmetic.totalOverSupport APPArithmetic.sumQuotient) :=
  APPArithmetic.integrated_defect

theorem selected_neighbor_no_roots (x : Space 12)
    (hx : x ∈ neighbor wittCode selectedRadial) (hne : x ≠ 0) :
    pairing x x ≠ 2 := by
  have hmin := selected_classical_hypotheses.2.2.2.2.2.2.2.2.1 x hx hne
  linarith

/-- The terminal interface conserves the concrete four-plus-one incidence,
the selected lattice and its algebraic realization on that same origin.
No K equality, alternative lattice or FLM conclusion is an input. -/
theorem article_I_exceptional_interface :
    ClassicalLeechHypotheses selectedRadial ∧
    ConcreteIncidencePublication ∧
    AlgebraicVertexInput ∧
    ((APPArithmetic.totalOverSupport APPArithmetic.productResidue -
      APPArithmetic.totalOverSupport APPArithmetic.sumResidue : ℕ) : ℚ) =
      pairing selectedRadial selectedRadial ∧
    APPFockIndex.orientedTrace = pairing selectedRadial selectedRadial ∧
    APPFockIndex.degreeTwoFockTrace = pairing selectedRadial selectedRadial :=
  ⟨selected_classical_hypotheses, concrete_incidence_publication,
    selected_algebraic_vertex_input, sum_product_defect_matches_selected_norm,
    app_fock_selected_radial_compatibility⟩

end HMT.I.ArticleIExceptionalInterface
end

#print axioms HMT.I.ArticleIExceptionalInterface.selected_classical_hypotheses
#print axioms HMT.I.ArticleIExceptionalInterface.ClassicalLeechHypotheses
#print axioms HMT.I.ArticleIExceptionalInterface.same_generated_mark_and_lattice
#print axioms HMT.I.ArticleIExceptionalInterface.selected_radial_norm_is_54
#print axioms HMT.I.ArticleIExceptionalInterface.sum_product_defect_matches_selected_norm
#print axioms HMT.I.ArticleIExceptionalInterface.full_sum_product_defect_retained
#print axioms HMT.I.ArticleIExceptionalInterface.selected_neighbor_no_roots
#print axioms HMT.I.ArticleIExceptionalInterface.article_I_exceptional_interface
