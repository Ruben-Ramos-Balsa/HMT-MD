import SelectedArticleIComposition
import SelectedRegionalIncidence

/-!
Reusable entry point for the selected Article I construction.

Both branches below use TerminalSelector.regionalRegister. This module
composes existing proofs; it neither substitutes a new register nor copies
their proofs. Downstream action, constitutive and exceptional developments
can import this entry point without rebuilding a different common base.

The upstream unordered S8 interface and the finite selector's
Lean.ofReduceBool dependency are inherited unchanged. The lattice statement
below is not an assertion that the FLM construction or Moonshine has been
formalized in this module. Dimensional units and mass refinements remain
explicit parameters, exactly as in the imported electronic construction.
-/

noncomputable section
namespace HMT.Shared.ArticleI

open HMT.I.TerminalSelector HMT.I.SelectedAction HMT.I.SelectedElectron
open HMT.I.SelectedRegionalIncidence HMT.I.NativeFourPlusOne
open HMT.I.PaleyCharacterConstruction HMT.I.KMarkedIncidence HMT.II.CKM.Incidence
open HMT.II.ActionReturn HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter
open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality
open HMT.IV.NeighborSpan HMT.IV.NeighborLattice
open HMT.IV.NeighborDuality HMT.IV.NeighborMinimum HMT.IV.NeighborRank

abbrev register := regionalRegister

theorem action_alpha_uses_shared_register :
    alpha = AlphaAnalyticChart.precoordinate register := rfl

theorem incidence_reader_uses_shared_register :
    selectedHighSupport =
      Finset.univ.filter (fun i : Fin 12 => 729 ≤ register.digits[i.val]!) := rfl

def ActionElectronPublication (U massUnit x y : ℝ)
    (r : Reader) (η : Refinement (internalMoments x y)) : Prop :=
  HMT.I.SelectedArticleI.PublishedAtEveryDepth alpha ∧
  HMT.II.DeterminantalAction.decimalOrder
    (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
  (0 < hbarRet alpha phi pi U ∧
    hbarRet alpha phi pi U < hbarPre alpha phi U ∧ 1 < actionRatio U) ∧
  (0 < composition U ∧
    (massOperator U massUnit x y r η).IsPositive ∧
    massOperator U massUnit x y r η (routeBasis CentralRoute.electron) =
      (massUnit * composition U : ℝ) • routeBasis CentralRoute.electron)

def IncidenceLatticePublication : Prop :=
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
  (∃ x ∈ neighbor wittCode selectedRadial, pairing x x = 4)

theorem shared_action_electron_incidence
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧
      IncidenceLatticePublication :=
  ⟨HMT.I.SelectedArticleI.principal_action_electron_composition
      hU hunit x y r η,
    HMT.I.SelectedRegionalIncidence.selected_incidence_lattice_properties⟩

end HMT.Shared.ArticleI
end

#print axioms HMT.Shared.ArticleI.action_alpha_uses_shared_register
#print axioms HMT.Shared.ArticleI.incidence_reader_uses_shared_register
#print axioms HMT.Shared.ArticleI.shared_action_electron_incidence
