import SelectedLatticeAlgebra
import LatticeParityCarrier
import WittLatticeZeroModes
import APPFockRigidity
import APPFockIndex

/-!
One entry point from the selected Article I register to the actual algebraic
inputs of its lattice vertex construction. These inputs are constructed,
not supplied by a `VOAExists` or `FLM` assumption. The existing action and
electronic branch is retained, with exactly its prior units and refinement.

The endpoint proved here is the lattice algebraic carrier, integral-form
oscillators, zero modes, cocycle shifts and its untwisted parity splitting.
The state-field correspondence, locality/Jacobi identities, twisted sector,
orbifold product and Monster identification are different later assertions;
this theorem does not encode them as an axiom or rename this carrier Vnatural.
-/

noncomputable section
namespace HMT.I.SelectedVOAInput

open HMT.I.SelectedRegionalIncidence HMT.I.SelectedLatticeAlgebra
open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeParityCarrier
open HMT.IV.LatticeZeroModes
open HMT.Shared.ArticleI

abbrev SelectedCarrier := LatticeCarrier selectedOrigin
abbrev SelectedFock := Fock selectedOrigin

theorem selected_oscillator_rank : BasisSize selectedOrigin = 24 :=
  HMT.IV.NeighborRank.witt_marked_integer_rank selectedOrigin

theorem app_weight_matches_selected_radial :
    APPFockRigidity.digitalWeight APPFockRigidity.generatedAggregate =
      HMT.IV.CoxeterNeighbor.pairing selectedRadial selectedRadial := by
  rw [APPFockRigidity.generated_digital_weight]
  exact selected_incidence_lattice_properties.2.2.2.1.symm

/-- Comparison of two constructed operators with the already selected
radial norm. This is not used to define the register or the lattice. -/
theorem app_fock_selected_radial_compatibility :
    APPFockIndex.orientedTrace =
      HMT.IV.CoxeterNeighbor.pairing selectedRadial selectedRadial ∧
    APPFockIndex.degreeTwoFockTrace =
      HMT.IV.CoxeterNeighbor.pairing selectedRadial selectedRadial := by
  constructor
  · exact APPFockIndex.generated_app_fock_index.trans
      selected_incidence_lattice_properties.2.2.2.1.symm
  · exact APPFockIndex.degree_two_fock_trace.trans
      selected_incidence_lattice_properties.2.2.2.1.symm

def AlgebraicVertexInput : Prop :=
  IncidenceLatticePublication ∧
  BasisSize selectedOrigin = 24 ∧
  (∀ x y : SelectedLattice,
    basisElement selectedOrigin x * basisElement selectedOrigin y =
      epsilon selectedOrigin x y • basisElement selectedOrigin (x+y)) ∧
  (∀ (n m : ℕ) (i j : Fin (BasisSize selectedOrigin)) (v : SelectedCarrier),
    onCarrier selectedOrigin (annihilate selectedOrigin n i)
        (onCarrier selectedOrigin (create selectedOrigin m j) v) -
      onCarrier selectedOrigin (create selectedOrigin m j)
        (onCarrier selectedOrigin (annihilate selectedOrigin n i) v) =
      (if n = m then (n + 1 : ℂ) * gram selectedOrigin i j else 0) • v) ∧
  (∀ h x : SelectedLattice,
    (zeroMode selectedOrigin h).comp (latticeShift selectedOrigin x) -
      (latticeShift selectedOrigin x).comp (zeroMode selectedOrigin h) =
      (integerPair selectedOrigin h x : ℂ) • latticeShift selectedOrigin x) ∧
  (∀ v : SelectedCarrier, carrierTheta selectedOrigin (carrierTheta selectedOrigin v) = v) ∧
  (∀ v : SelectedCarrier,
    evenProjector selectedOrigin v + oddProjector selectedOrigin v = v) ∧
  vacuum selectedOrigin ≠ 0 ∧
  carrierTheta selectedOrigin (vacuum selectedOrigin) = vacuum selectedOrigin

theorem selected_algebraic_vertex_input : AlgebraicVertexInput :=
  ⟨selected_incidence_lattice_properties, selected_oscillator_rank,
    selected_algebra_product, carrier_mode_ccr selectedOrigin,
    zeroMode_latticeShift selectedOrigin, carrierTheta_square selectedOrigin,
    parity_decomposition selectedOrigin, vacuum_ne_zero selectedOrigin,
    carrierTheta_vacuum selectedOrigin⟩

open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

theorem shared_action_electron_vertex_input
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧ AlgebraicVertexInput :=
  ⟨(shared_action_electron_incidence hU hunit x y r η).1,
    selected_algebraic_vertex_input⟩

end HMT.I.SelectedVOAInput
end

#print axioms HMT.I.SelectedVOAInput.selected_oscillator_rank
#print axioms HMT.I.SelectedVOAInput.app_weight_matches_selected_radial
#print axioms HMT.I.SelectedVOAInput.app_fock_selected_radial_compatibility
#print axioms HMT.I.SelectedVOAInput.selected_algebraic_vertex_input
#print axioms HMT.I.SelectedVOAInput.shared_action_electron_vertex_input
