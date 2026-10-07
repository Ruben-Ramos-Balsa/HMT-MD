import LatticeCoxeterFieldCovariance
import CoxeterChargeCovariance
import LatticePositiveMixedFields

/-!
All integer Heisenberg modes transform under the same, already constructed
Coxeter lift. A lattice charge is read in the inherited integral basis;
the zero, negative and positive modes are the existing charge, creation
and annihilation operators. The original basis-indexed hmode is recovered
exactly. This joins the oscillator and charged-field generators, without
declaring a vertex-algebra reconstruction or an orbifold.
-/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeCoxeterHeisenbergCovariance

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeCoxeterFock HMT.IV.LatticeCoxeterTwistedLift
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeCoxeterFieldCovariance HMT.IV.CoxeterChargeCovariance
open HMT.IV.LatticeZeroModes HMT.IV.LatticeHeisenbergModes
open HMT.IV.LatticePositiveMixedFields HMT.IV.LatticeChargedVertexField
open scoped TensorProduct BigOperators

theorem fockAction_chargeCreation (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v : Fock o) :
    fockAction o (chargeCreation o x n v) =
      chargeCreation o (latticeAction o x) n (fockAction o v) := by
  rw [chargeCreation_apply, map_mul, fockAction_creationState, chargeCreation_apply]

theorem carrier_chargeCreation (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v : LatticeCarrier o) :
    carrierEquiv o (onCarrier o (chargeCreation o x n) v) =
      onCarrier o (chargeCreation o (latticeAction o x) n) (carrierEquiv o v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp only [map_zero]
  | tmul a b =>
    rw [onCarrier_pure, carrierEquiv_pure, carrierEquiv_pure, onCarrier_pure]
    change fockAction o (chargeCreation o x n a) ⊗ₜ[ℂ] twistedEquiv o b = _
    rw [fockAction_chargeCreation]
    rfl
  | add u v hu hv => simp only [map_add, hu, hv]

theorem carrier_chargeAnnihilation (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v : LatticeCarrier o) :
    carrierEquiv o (onCarrier o (chargeAnnihilation o x n) v) =
      onCarrier o (chargeAnnihilation o (latticeAction o x) n) (carrierEquiv o v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp only [map_zero]
  | tmul a b =>
    rw [onCarrier_pure, carrierEquiv_pure, carrierEquiv_pure, onCarrier_pure]
    change fockAction o (chargeAnnihilation o x n a) ⊗ₜ[ℂ] twistedEquiv o b = _
    rw [fockAction_chargeAnnihilation]
    rfl
  | add u v hu hv => simp only [map_add, hu, hv]

/-- Charge-linear extension of the existing integer-indexed modes. -/
def chargedHmode (o : Fin 12) (x : Lattice o) (m : ℤ) :
    Module.End ℂ (LatticeCarrier o) :=
  if m < 0 then onCarrier o (chargeCreation o x ((-m-1).toNat))
  else if m = 0 then onCharge o (zeroMode o x)
  else onCarrier o (chargeAnnihilation o x ((m-1).toNat))

theorem chargedHmode_basis (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ) :
    chargedHmode o (latticeBasis o i) m = hmode o i m := by
  unfold chargedHmode hmode
  rw [chargeCreation_basis, chargeAnnihilation_basis]
  rfl

theorem carrier_chargedHmode (o : Fin 12) (x : Lattice o) (m : ℤ)
    (v : LatticeCarrier o) :
    carrierEquiv o (chargedHmode o x m v) =
      chargedHmode o (latticeAction o x) m (carrierEquiv o v) := by
  unfold chargedHmode
  split_ifs
  · exact carrier_chargeCreation o x _ v
  · exact carrier_zeroMode o x v
  · exact carrier_chargeAnnihilation o x _ v

/-- Every original integer mode, not only positive frequencies. -/
theorem carrier_hmode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ)
    (v : LatticeCarrier o) :
    carrierEquiv o (hmode o i m v) =
      chargedHmode o (latticeAction o (latticeBasis o i)) m (carrierEquiv o v) := by
  rw [← chargedHmode_basis]
  exact carrier_chargedHmode o (latticeBasis o i) m v

theorem carrier_chargedHmode_operator (o : Fin 12) (x : Lattice o) (m : ℤ) :
    (carrierEquiv o).toLinearMap.comp (chargedHmode o x m) =
      (chargedHmode o (latticeAction o x) m).comp (carrierEquiv o).toLinearMap := by
  apply LinearMap.ext
  intro v
  exact carrier_chargedHmode o x m v

theorem carrier_conjugates_chargedHmode (o : Fin 12) (x : Lattice o) (m : ℤ)
    (v : LatticeCarrier o) :
    carrierEquiv o (chargedHmode o x m ((carrierEquiv o).symm v)) =
      chargedHmode o (latticeAction o x) m v := by
  simpa only [LinearEquiv.apply_symm_apply] using
    carrier_chargedHmode o x m ((carrierEquiv o).symm v)

/-- The same exact order-three operator transports both generating families. -/
theorem generator_covariance (o : Fin 12) :
    orderOf (carrierEquiv o) = 3 ∧
    carrierEquiv o (vacuum o) = vacuum o ∧
    (∀ (i : Fin (BasisSize o)) (m : ℤ) (v : LatticeCarrier o),
      carrierEquiv o (hmode o i m v) =
        chargedHmode o (latticeAction o (latticeBasis o i)) m (carrierEquiv o v)) ∧
    (∀ (x : Lattice o) (k : ℤ) (v : LatticeCarrier o),
      carrierEquiv o (fieldCoefficient o x k ((carrierEquiv o).symm v)) =
        phase o x • fieldCoefficient o (latticeAction o x) k v) :=
  ⟨carrierEquiv_order o, carrierEquiv_vacuum o,
    carrier_hmode o, carrierEquiv_conjugates_field o⟩

end HMT.IV.LatticeCoxeterHeisenbergCovariance
end

#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.fockAction_chargeCreation
#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.carrier_chargeCreation
#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.carrier_chargeAnnihilation
#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.chargedHmode_basis
#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.carrier_chargedHmode
#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.carrier_hmode
#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.carrier_chargedHmode_operator
#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.carrier_conjugates_chargedHmode
#print axioms HMT.IV.LatticeCoxeterHeisenbergCovariance.generator_covariance
