import SharedArticleIBase
import CommonComposition
import RegionalPublicationComposition

/-!
Stable regression contract for the existing shared HMT construction.

The types below are written out deliberately: changing an imported alias to
a weaker proposition must not silently weaken this contract. The proofs are
reused, not recreated. Finite lift reconstruction, recorded transport,
unbounded compatible publication, and the two readings of the selected
register have distinct types and are not identified with one another.

The inherited X/Y and S8 interfaces remain unchanged. This contract does not
assert a new full-state holonomy theorem, FLM/Moonshine theorem or M-theory
formalization. The complete authorial genealogy is located in the companion
source map; only the propositions actually written here are kernel checked.
-/

noncomputable section
namespace HMT.Shared.FoundationRegression

open HMT.I.TerminalSelector HMT.I.SelectedAction HMT.I.SelectedElectron
open HMT.I.SelectedRegionalIncidence HMT.I.NativeFourPlusOne
open HMT.I.PaleyCharacterConstruction HMT.I.KMarkedIncidence HMT.II.CKM.Incidence
open HMT.II.ActionReturn HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter
open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality
open HMT.IV.NeighborSpan HMT.IV.NeighborLattice
open HMT.IV.NeighborDuality HMT.IV.NeighborMinimum HMT.IV.NeighborRank
open HMT.I.RegionalPublicationComposition

theorem app_trit_at_every_visit (q : TPKTransport.ObservableLift) :
    ∀ n : Nat,
      let qn := TPKTransport.iterate TPKTransport.step n q
      TRITCore.reconstruct (CommonComposition.visitTrit qn).1 =
        (APPArithmetic.sumEval (CommonComposition.cursorMark qn.plus.x)
          (CommonComposition.cursorMark qn.plus.y) : Int) ∧
      TRITCore.reconstruct (CommonComposition.visitTrit qn).2 =
        (APPArithmetic.productEval (CommonComposition.cursorMark qn.times.x)
          (CommonComposition.cursorMark qn.times.y) : Int) :=
  CommonComposition.every_visit_reconstructs q

theorem unique_regional_seeds :
    (∀ c : Channel, candidates c = [seed c]) ∧
    [seed .closure, seed .propagation, seed .autoscale] = TPKLifts.selectedSeeds :=
  ⟨unique_selected_seed, selected_seeds_are_shared⟩

theorem lifts_reconstruct_records :
    TPKLifts.mul TPKLifts.X0 TPKLifts.L0 = TPKLifts.Y0 ∧
    TPKLifts.mul TPKLifts.X1 TPKLifts.L1 = TPKLifts.Y1 :=
  TPKLifts.transition_equations

theorem lifts_are_unique (M : TPKLifts.Matrix) (hM : TPKLifts.TernaryMatrix M) :
    (TPKLifts.mul TPKLifts.X0 M = TPKLifts.Y0 → M = TPKLifts.L0) ∧
    (TPKLifts.mul TPKLifts.X1 M = TPKLifts.Y1 → M = TPKLifts.L1) :=
  ⟨TPKLifts.L0_unique M hM, TPKLifts.L1_unique M hM⟩

theorem lift_histories_truncate (bs : List Bool) (w : TPKOrbits.Word) :
    ∀ n : Nat, (TPKLifts.run bs w).take (n + 1) = TPKLifts.run (bs.take n) w :=
  fun n => TPKLifts.run_take bs n w

/-- This is the recorded transport model, not an identification with all of X_enr. -/
theorem recorded_history_is_retained (q : TPKTransport.HistoryLift) :
    ∀ n : Nat,
      (TPKTransport.iterate TPKTransport.recordStep n q).past.length =
        q.past.length + n ∧
      (∃ tail, (TPKTransport.iterate TPKTransport.recordStep n q).past =
        q.past ++ tail) ∧
      (0 < n → TPKTransport.iterate TPKTransport.recordStep n q ≠ q) := by
  intro n
  exact ⟨TPKTransport.recorded_length n q,
    TPKTransport.recorded_prefix_preserved n q,
    fun hn => TPKTransport.recorded_no_reset n hn q⟩

/-- Base phase returns; the depth-memory coordinate advances. -/
theorem nonadic_phase_and_memory :
    ∀ depth : Nat,
      TPKTransport.nonadicPhase (depth + 9) = TPKTransport.nonadicPhase depth ∧
      TPKTransport.nonadicMemory (depth + 9) = TPKTransport.nonadicMemory depth + 1 ∧
      TPKTransport.nonadicPhase depth + 9 * TPKTransport.nonadicMemory depth = depth :=
  fun depth => ⟨TPKTransport.nonadic_phase_return depth,
    TPKTransport.nonadic_memory_advance depth,
    TPKTransport.phase_memory_reconstruct depth⟩

theorem recorded_nonadic_return_is_not_reset (q : TPKTransport.HistoryLift) :
    TPKTransport.iterate TPKTransport.recordStep 9 q ≠ q :=
  TPKTransport.recorded_no_reset 9 (by decide) q

theorem joint_publication_at_any_scale :
    ∀ scale : Nat, 0 < scale → ∃ N : Nat, ∀ c k, N ≤ k →
      RadixCellSelection.first (lower c k) scale = RadixCellSelection.cell (value c) scale ∧
      RadixCellSelection.last (upper c k) scale = RadixCellSelection.cell (value c) scale :=
  joint_eventual_publication

theorem publication_at_every_depth (base : Nat) (hb : 0 < base) :
    ∀ (c : Channel) (n : Nat),
      publish c base hb n = RadixCellSelection.positionalPrefix (value c) base n :=
  fun c n => publish_eq_prefix c base hb n

theorem publication_retains_all_prefixes (base : Nat) (hb : 0 < base) :
    ∀ (c : Channel) (n m : Nat),
      publish c base hb (n + m) / base ^ m = publish c base hb n :=
  fun c n m => publications_compatible c base hb n m

/-- Recognition follows the constructed regional readers and their publication. -/
theorem pi_e_phi_recognition_at_every_depth (base : Nat) (hb : 0 < base) :
    ∀ n : Nat,
      publish .closure base hb n = RadixCellSelection.positionalPrefix Real.pi base n ∧
      publish .propagation base hb n = RadixCellSelection.positionalPrefix (Real.exp 1) base n ∧
      publish .autoscale base hb n = RadixCellSelection.positionalPrefix goldenRatio base n :=
  recognized_publications base hb

theorem shared_register_is_selected :
    HMT.Shared.ArticleI.register = regionalRegister := rfl

theorem alpha_uses_selected_register :
    alpha = AlphaAnalyticChart.precoordinate HMT.Shared.ArticleI.register := rfl

theorem high_support_uses_selected_register :
    selectedHighSupport = Finset.univ.filter
      (fun i : Fin 12 => 729 ≤ HMT.Shared.ArticleI.register.digits[i.val]!) := rfl

theorem precarry_uses_selected_register :
    selectedPrecarry = fun i : Fin 12 =>
      HMT.I.RegionalPrecarry.regionalBlock .closure i +
        HMT.I.RegionalPrecarry.regionalBlock .propagation i -
        HMT.I.RegionalPrecarry.regionalBlock .autoscale i -
        (HMT.Shared.ArticleI.register.digits[i.val]! : Int) := rfl

theorem alpha_at_every_depth :
    ∀ n : Nat,
      (AlphaPublications.publication HMT.Shared.ArticleI.register n).outgoing = 0 ∧
      (AlphaPublications.publication HMT.Shared.ArticleI.register n).digits =
        (AlphaCanonicalSection.digits alpha (12 * n)).map Int.ofNat :=
  HMT.I.SelectedArticleI.alpha_published_at_every_depth

/-- This test also fixes the exact dimensional and reader parameters. -/
theorem shared_action_electron_contract
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    (∀ n : Nat, (AlphaPublications.publication regionalRegister n).outgoing = 0 ∧
      (AlphaPublications.publication regionalRegister n).digits =
        (AlphaCanonicalSection.digits alpha (12 * n)).map Int.ofNat) ∧
    HMT.II.DeterminantalAction.decimalOrder
      (HMT.II.DeterminantalAction.actionScale phi alpha) = -34 ∧
    (0 < hbarRet alpha phi pi U ∧
      hbarRet alpha phi pi U < hbarPre alpha phi U ∧ 1 < actionRatio U) ∧
    (0 < composition U ∧
      (massOperator U massUnit x y r η).IsPositive ∧
      massOperator U massUnit x y r η (routeBasis CentralRoute.electron) =
        (massUnit * composition U : ℝ) • routeBasis CentralRoute.electron) :=
  (HMT.Shared.ArticleI.shared_action_electron_incidence hU hunit x y r η).1

theorem shared_incidence_lattice_contract :
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
    (∃ x ∈ neighbor wittCode selectedRadial, pairing x x = 4) :=
  show HMT.Shared.ArticleI.IncidenceLatticePublication from
    selected_incidence_lattice_properties

/-- A finite publication cannot be used where the contract requires every depth. -/
example : True := by
  fail_if_success
    have _ : ∀ n : Nat,
        (AlphaPublications.publication regionalRegister n).outgoing = 0 ∧
        (AlphaPublications.publication regionalRegister n).digits =
          (AlphaCanonicalSection.digits alpha (12 * n)).map Int.ofNat :=
      HMT.I.SelectedArticleI.alpha_published_at_every_depth 0
  trivial

/-- Equality of a phase reading cannot replace equality of recorded states. -/
example (q : TPKTransport.HistoryLift) : q = q := by
  fail_if_success
    have _ : TPKTransport.iterate TPKTransport.recordStep 9 q = q :=
      TPKTransport.nonadic_phase_return 0
  rfl

end HMT.Shared.FoundationRegression
end

#print axioms HMT.Shared.FoundationRegression.app_trit_at_every_visit
#print axioms HMT.Shared.FoundationRegression.unique_regional_seeds
#print axioms HMT.Shared.FoundationRegression.lifts_reconstruct_records
#print axioms HMT.Shared.FoundationRegression.lifts_are_unique
#print axioms HMT.Shared.FoundationRegression.lift_histories_truncate
#print axioms HMT.Shared.FoundationRegression.recorded_history_is_retained
#print axioms HMT.Shared.FoundationRegression.nonadic_phase_and_memory
#print axioms HMT.Shared.FoundationRegression.recorded_nonadic_return_is_not_reset
#print axioms HMT.Shared.FoundationRegression.joint_publication_at_any_scale
#print axioms HMT.Shared.FoundationRegression.publication_at_every_depth
#print axioms HMT.Shared.FoundationRegression.publication_retains_all_prefixes
#print axioms HMT.Shared.FoundationRegression.pi_e_phi_recognition_at_every_depth
#print axioms HMT.Shared.FoundationRegression.shared_register_is_selected
#print axioms HMT.Shared.FoundationRegression.alpha_uses_selected_register
#print axioms HMT.Shared.FoundationRegression.high_support_uses_selected_register
#print axioms HMT.Shared.FoundationRegression.precarry_uses_selected_register
#print axioms HMT.Shared.FoundationRegression.alpha_at_every_depth
#print axioms HMT.Shared.FoundationRegression.shared_action_electron_contract
#print axioms HMT.Shared.FoundationRegression.shared_incidence_lattice_contract
