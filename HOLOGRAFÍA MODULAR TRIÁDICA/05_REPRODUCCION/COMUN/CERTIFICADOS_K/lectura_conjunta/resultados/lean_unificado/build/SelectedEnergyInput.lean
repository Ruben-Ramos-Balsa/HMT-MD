import SelectedFullGradedTrace
import LatticeEnergyModes
import LatticeLowWeightParity
import LatticeExponentialEnergy
import LatticeAnnihilationEnergy
import LatticeChargedVertexField
import LatticeChargedFieldEnergy
import LatticeCoxeterFock

/-!
The same selected Article-I origin now supplies an energy operator, its
actual integer modes and charged fields. Earlier action/electron conditions
are preserved verbatim. The following endpoint does not claim Jacobi,
a conformal vector, the twisted orbifold or the FLM/Monster theorem.
-/

noncomputable section
namespace HMT.I.SelectedEnergyInput

open HMT.I.SelectedRegionalIncidence HMT.I.SelectedVOAInput
open HMT.I.SelectedHeisenbergInput HMT.I.SelectedGradedTrace
open HMT.I.SelectedFullGradedTrace HMT.Shared.ArticleI
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeFullGradedTrace HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeEnergyGrading HMT.IV.LatticeEnergyModes
open HMT.IV.LatticeEnergyShift HMT.IV.LatticeChargeEnergy
open HMT.IV.LatticeEulerEnergy HMT.IV.LatticeLowWeightParity
open HMT.IV.LatticeZeroModes HMT.IV.LatticeWeightShells
open HMT.IV.LatticeParityCarrier HMT.IV.LatticeHeisenbergModes
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeExponentialEnergy
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeCoxeterFock
open HMT.IV.LatticeChargedFieldEnergy
open scoped TensorProduct

def SelectedEnergyPublication : Prop :=
  (energy selectedOrigin =
    onCarrier selectedOrigin (euler selectedOrigin).toLinearMap +
      onLattice selectedOrigin (chargeEnergy selectedOrigin)) ∧
  (∀ d : ℕ, fullWeightSpace selectedOrigin d =
    Module.End.eigenspace (energy selectedOrigin) (d : ℂ)) ∧
  (∀ (i : Fin (BasisSize selectedOrigin)) (n : ℤ),
    (energy selectedOrigin).comp (hmode selectedOrigin i n) -
      (hmode selectedOrigin i n).comp (energy selectedOrigin) =
      (-(n : ℂ)) • hmode selectedOrigin i n) ∧
  (∀ x : Lattice selectedOrigin,
    (energy selectedOrigin).comp (onLattice selectedOrigin (latticeShift selectedOrigin x)) -
      (onLattice selectedOrigin (latticeShift selectedOrigin x)).comp (energy selectedOrigin) =
      (onLattice selectedOrigin (latticeShift selectedOrigin x)).comp
          (onLattice selectedOrigin (zeroMode selectedOrigin x)) +
        (halfnormNat selectedOrigin x : ℂ) •
          onLattice selectedOrigin (latticeShift selectedOrigin x)) ∧
  (Module.End.eigenspace (energy selectedOrigin) 0 =
    Submodule.span ℂ {vacuum selectedOrigin}) ∧
  (∀ v : LatticeCarrier selectedOrigin, v ∈ fullWeightSpace selectedOrigin 1 →
    carrierTheta selectedOrigin v = v → v = 0)

theorem selected_energy_publication : SelectedEnergyPublication :=
  ⟨energy_eq_euler_plus_charge selectedOrigin,
    fullWeightSpace_eq_eigenspace selectedOrigin,
    energy_hmode selectedOrigin, energy_shift selectedOrigin,
    energy_zero_is_vacuum_line selectedOrigin,
    fixed_weight_one_eq_zero selectedOrigin⟩

def SelectedChargedFieldPublication : Prop :=
  (∀ (x : Lattice selectedOrigin) (v : LatticeCarrier selectedOrigin) (k : ℤ),
    ((HahnModule.of ℂ).symm (chargedField selectedOrigin x v)).coeff k =
      fieldCoefficient selectedOrigin x k v) ∧
  (∀ (x : Lattice selectedOrigin) (v : LatticeCarrier selectedOrigin),
    ∃ b : ℤ, ∀ k < b, fieldCoefficient selectedOrigin x k v = 0) ∧
  (∀ x : Lattice selectedOrigin,
    fieldCoefficient selectedOrigin x 0 (vacuum selectedOrigin) =
      (1 : Fock selectedOrigin) ⊗ₜ[ℂ] basisElement selectedOrigin x) ∧
  (∀ (x : Lattice selectedOrigin) (d : ℕ),
    euler selectedOrigin (PowerSeries.coeff (Fock selectedOrigin) d
      (creationExponential selectedOrigin x)) = (d : ℂ) •
        PowerSeries.coeff (Fock selectedOrigin) d (creationExponential selectedOrigin x)) ∧
  (∀ (x y : Lattice selectedOrigin) (a : Occupation selectedOrigin)
      (k : ℤ) (N : ℕ), occupationWeight selectedOrigin a ≤ N →
    basisCoefficient selectedOrigin x k a y =
      basisCoefficientCutoff selectedOrigin x k N a y) ∧
  (∀ k : ℤ, fieldCoefficient selectedOrigin 0 k =
    if k=0 then (LinearMap.id : Module.End ℂ (LatticeCarrier selectedOrigin)) else 0) ∧
  (∀ (x : Lattice selectedOrigin) (k : ℤ),
    (energy selectedOrigin).comp (fieldCoefficient selectedOrigin x k) -
      (fieldCoefficient selectedOrigin x k).comp (energy selectedOrigin) =
      ((k : ℂ)+(halfnormNat selectedOrigin x : ℂ)) •
        fieldCoefficient selectedOrigin x k) ∧
  orderOf (fockEquiv selectedOrigin) = 3

theorem selected_charged_field_publication : SelectedChargedFieldPublication :=
  ⟨chargedField_coefficient selectedOrigin,
    fieldCoefficient_bounded_pole selectedOrigin,
    fieldCoefficient_vacuum_zero selectedOrigin,
    creationExponential_coefficient_energy selectedOrigin,
    fun x y a k N hN => basisCoefficientCutoff_stable selectedOrigin x k a y N hN,
    fieldCoefficient_zero_charge selectedOrigin,
    energy_fieldCoefficient selectedOrigin,
    fockEquiv_order selectedOrigin⟩

open HMT.VI.MassOperator HMT.VI.ElectronGeneratedLedger
open HMT.VI.LedgerSignature HMTMassCharacter

theorem shared_action_electron_energy_and_fields
    {U massUnit : ℝ} (hU : 0 < U) (hunit : 0 < massUnit)
    (x y : ℝ) (r : Reader) (η : Refinement (internalMoments x y)) :
    ActionElectronPublication U massUnit x y r η ∧
      AlgebraicVertexInput ∧ SelectedHeisenbergPublication ∧
      SelectedGradedPublication ∧ FullReflectedTracePublication ∧
      SelectedEnergyPublication ∧ SelectedChargedFieldPublication := by
  obtain ⟨ha,hb,hc,hd,he⟩ :=
    shared_action_electron_fields_and_full_trace hU hunit x y r η
  exact ⟨ha,hb,hc,hd,he,selected_energy_publication,selected_charged_field_publication⟩

end HMT.I.SelectedEnergyInput
end

#print axioms HMT.I.SelectedEnergyInput.selected_energy_publication
#print axioms HMT.I.SelectedEnergyInput.selected_charged_field_publication
#print axioms HMT.I.SelectedEnergyInput.shared_action_electron_energy_and_fields
