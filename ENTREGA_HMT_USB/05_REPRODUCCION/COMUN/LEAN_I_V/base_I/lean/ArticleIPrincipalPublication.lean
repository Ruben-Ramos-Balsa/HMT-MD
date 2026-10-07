import ArticleIExceptionalInterface
import SelectedCylinderSignature
import APPSpinBridge
import ElectronSpinRotation

/-!
# Regional generation and the algebraic electronic structure of Article I

This entry composes the existing results in the order announced by Article I:
regional publication at every depth, the two correlated alpha publications,
action and electronic composition, the actual APP principal plane, its
spinorial realization and helicity, and the exceptional lattice interface.
No upstream construction or classical theorem is re-proved here.

All objects are those of the imported modules. Positive dimensional units,
the mass refinement, and a unit direction remain explicit parameters. The
analytic alpha chart is the correlated representation specified upstream,
not a second causally independent selection. The inherited terminal selector
retains its declared input domain and Lean.ofReduceBool dependency.

The exceptional conclusion supplies the hypotheses for the bibliographic
Leech/FLM application; it does not assert a kernel proof of FLM or Moonshine.
-/

noncomputable section
namespace HMT.I.ArticleIPrincipalPublication

open Matrix
open HMT.I.RegionalPublicationComposition HMT.I.TerminalSelector
open HMT.I.SelectedAction HMT.I.SelectedElectron HMT.I.APPSpinBridge
open HMT.I.APPFiberOperators HMT.I.APPGlobalCommutator
open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger HMT.VI.LedgerSignature
open HMTMassCharacter ElectronSpin HMT.I.ElectronSpinRotation
open HMT.I.ArticleIExceptionalInterface HMT.I.SelectedRegionalIncidence
open HMT.I.SelectedExceptionalChain HMT.I.SelectedVOAInput

/-- A single consumer of the already proved principal outputs. The explicit
APP intertwining identifies the electronic matrices with the actual plane;
the selected regional composition is the same one in the mass operator.
The helicity direction and the dimensional normalization are not inferred
from a numerical agreement. -/
theorem article_I_principal_publication
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y))
    (n : Fin 3 → ℝ) (hn : n 0 ^ 2 + n 1 ^ 2 + n 2 ^ 2 = 1) :
    (∀ (base : Nat) (hb : 0 < base) (depth : Nat),
      publish .closure base hb depth =
        RadixCellSelection.positionalPrefix Real.pi base depth ∧
      publish .propagation base hb depth =
        RadixCellSelection.positionalPrefix (Real.exp 1) base depth ∧
      publish .autoscale base hb depth =
        RadixCellSelection.positionalPrefix goldenRatio base depth) ∧
    (∀ d k : Nat, SelectedCylinderSignature.produce d k =
      some (SelectedCylinderSignature.generatedOutput d k)) ∧
    (∃! a : ℝ, a ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart regionalRegister VacancyDeltaBounds.vacancyDelta a = 0 ∧
      (∀ d : Nat, (AlphaPublications.publication regionalRegister d).outgoing = 0 ∧
        (AlphaPublications.publication regionalRegister d).digits =
          (AlphaCanonicalSection.digits a (12 * d)).map Int.ofNat)) ∧
    HMT.Shared.ArticleI.ActionElectronPublication U massUnit x y r η ∧
    (SelectedElectron.composition U = ‖APPGlobalPrefactor.incompatibility‖ *
      (Real.exp (phi / pi ^ 2) - 22 * alpha ^ 3) *
      (1 + 15 * ElectronComposition.regionalFull) *
      Real.exp ((80 - 54 * alpha + 6 * ElectronComposition.regionalFull) *
        Real.log (actionRatio U))) ∧
    (∀ v : LocalPlane, ‖planeEmbedding v‖ = ‖v‖ ∧
      sigmaProjection (planeEmbedding v) =
        planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) P v) ∧
      piProjection (planeEmbedding v) =
        planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) Q v)) ∧
    (S * S = 1 ∧ ElectronSpin.J * ElectronSpin.J = -1 ∧
      S * ElectronSpin.J = -(ElectronSpin.J * S) ∧
      nilPlus * nilPlus = 0 ∧ nilMinus * nilMinus = 0 ∧
      nilPlus * nilMinus + nilMinus * nilPlus = 1) ∧
    (projectorPlus n + projectorMinus n = 1 ∧
      projectorPlus n * projectorMinus n = 0 ∧
      projectorMinus n * projectorPlus n = 0 ∧
      helicity n * projectorPlus n = (1 / 2 : ℂ) • projectorPlus n ∧
      helicity n * projectorMinus n = (-1 / 2 : ℂ) • projectorMinus n ∧
      (∃ v : Fin 2 → ℂ, v ≠ 0 ∧ helicity n *ᵥ v = (1 / 2 : ℂ) • v) ∧
      (∃ v : Fin 2 → ℂ, v ≠ 0 ∧ helicity n *ᵥ v = (-1 / 2 : ℂ) • v)) ∧
    ((∀ theta : ℝ,
      (rotation n theta).conjTranspose * rotation n theta = 1 ∧
      rotation n theta * (rotation n theta).conjTranspose = 1) ∧
      rotation n (2 * Real.pi) = -1 ∧ rotation n (4 * Real.pi) = 1) ∧
    ((((massUnit * SelectedElectron.composition U : ℝ) : ℂ) • (1 : MatC)) *
      helicity n = helicity n *
        (((massUnit * SelectedElectron.composition U : ℝ) : ℂ) • (1 : MatC))) ∧
    ClassicalLeechHypotheses selectedRadial ∧
    ConcreteIncidencePublication ∧ AlgebraicVertexInput := by
  exact ⟨recognized_publications, SelectedCylinderSignature.produce_correct,
    regional_terminal_alpha,
    SelectedArticleI.principal_action_electron_composition hU hunit x y r η,
    SelectedElectron.composition_formula_from_APP U,
    actual_APP_local_block,
    ⟨S_square, J_square, SJ_anticommute, nilPlus_square, nilMinus_square, nil_pairing⟩,
    ⟨projectors_sum n, (projectors_orthogonal n hn).1,
      (projectors_orthogonal n hn).2, helicity_plus n hn, helicity_minus n hn,
      exists_plus_eigenvector n hn, exists_minus_eigenvector n hn⟩,
    ⟨unitary n hn, two_pi_return n, four_pi_return n⟩,
    scalar_commutes _ _,
    selected_classical_hypotheses, concrete_incidence_publication,
    selected_algebraic_vertex_input⟩

end HMT.I.ArticleIPrincipalPublication
end

#print axioms HMT.I.ArticleIPrincipalPublication.article_I_principal_publication
