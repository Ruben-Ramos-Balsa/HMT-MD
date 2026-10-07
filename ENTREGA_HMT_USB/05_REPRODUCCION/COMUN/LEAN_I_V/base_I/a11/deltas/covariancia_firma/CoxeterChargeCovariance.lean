import LatticeCoxeterTwistedLift
import WittLatticeZeroModes

/-!
Covariance of the actual charge operators under the constructed Coxeter lift.
The same marked lattice, sign cocycle and carrier are used throughout.
This is a composition of the existing lattice isometry and multiplicative
lift, not a new assumption about a vertex algebra or an orbifold.
-/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.CoxeterChargeCovariance

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCoxeterFock HMT.IV.LatticeCoxeterTwistedLift
open HMT.IV.LatticeZeroModes HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeFockMonomialParity
open scoped TensorProduct

theorem twisted_shift (o : Fin 12) (x : Lattice o) (f : TwistedAlgebra o) :
    twistedEquiv o (latticeShift o x f) =
      phase o x • latticeShift o (latticeAction o x) (twistedEquiv o f) := by
  change twistedEquiv o (basisElement o x * f) =
    phase o x • (basisElement o (latticeAction o x) * twistedEquiv o f)
  rw [map_mul, twistedEquiv_basis, smul_mul_assoc]

theorem twisted_zeroMode (o : Fin 12) (x : Lattice o) (f : TwistedAlgebra o) :
    twistedEquiv o (zeroMode o x f) =
      zeroMode o (latticeAction o x) (twistedEquiv o f) := by
  have h : (twistedEquiv o).toLinearMap.comp (zeroMode o x) =
      (zeroMode o (latticeAction o x)).comp (twistedEquiv o).toLinearMap := by
    apply (latticeBasisComplex o).ext
    intro y
    change twistedEquiv o (zeroMode o x (basisElement o y)) =
      zeroMode o (latticeAction o x) (twistedEquiv o (basisElement o y))
    simp only [zeroMode_basis, map_smul, twistedEquiv_basis,
      latticeAction_pairing, smul_smul]
    rw [mul_comm]
  exact LinearMap.congr_fun h f

/-- Lift the existing charge operator, leaving the oscillator factor alone. -/
def onCharge (o : Fin 12) (T : Module.End ℂ (TwistedAlgebra o)) :
    Module.End ℂ (LatticeCarrier o) := TensorProduct.map LinearMap.id T

theorem onCharge_pure (o : Fin 12) (T : Module.End ℂ (TwistedAlgebra o))
    (v : Fock o) (f : TwistedAlgebra o) :
    onCharge o T (v ⊗ₜ[ℂ] f) = v ⊗ₜ[ℂ] T f := rfl

theorem carrier_shift (o : Fin 12) (x : Lattice o) (v : LatticeCarrier o) :
    carrierEquiv o (onCharge o (latticeShift o x) v) =
      phase o x • onCharge o (latticeShift o (latticeAction o x))
        (carrierEquiv o v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp only [map_zero, smul_zero]
  | tmul a b =>
      rw [onCharge_pure, carrierEquiv_pure, twisted_shift,
        TensorProduct.tmul_smul, carrierEquiv_pure, onCharge_pure]
  | add u v hu hv => simp only [map_add, hu, hv, smul_add]

theorem carrier_zeroMode (o : Fin 12) (x : Lattice o) (v : LatticeCarrier o) :
    carrierEquiv o (onCharge o (zeroMode o x) v) =
      onCharge o (zeroMode o (latticeAction o x)) (carrierEquiv o v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp only [map_zero]
  | tmul a b =>
      rw [onCharge_pure, carrierEquiv_pure, twisted_zeroMode,
        carrierEquiv_pure, onCharge_pure]
  | add u v hu hv => simp only [map_add, hu, hv]

theorem empty_charge_basis (o : Fin 12) (x : Lattice o) :
    carrierBasis o (0, x) = (1 : Fock o) ⊗ₜ[ℂ] basisElement o x := by
  simp only [carrierBasis, Basis.tensorProduct_apply, monomialBasis_product,
    Finsupp.prod_zero_index, latticeBasisComplex, Finsupp.coe_basisSingleOne]
  rfl

theorem carrier_empty_charge (o : Fin 12) (x : Lattice o) :
    carrierEquiv o (carrierBasis o (0, x)) =
      phase o x • carrierBasis o (0, latticeAction o x) := by
  rw [empty_charge_basis, carrierEquiv_charge, map_one, empty_charge_basis]

/-- Exact order is witnessed on the same charged vacuum sector. -/
theorem carrierEquiv_ne_one (o : Fin 12) : carrierEquiv o ≠ 1 := by
  intro h
  let x : Lattice o := ⟨CoxeterNeighbor.rootDifference o,
    CoxeterNeighbor.rootDifference o,
    CoxeterNeighbor.rootDifference_mem_kernel CoxeterNeighbor.wittCode o, 0, by simp⟩
  have hx : latticeAction o x ≠ x := by
    intro he
    have hv := congrArg (fun z : Lattice o => (z : CoxeterNeighbor.Space 12)) he
    change CoxeterNeighbor.action CoxeterNeighbor.wittOrientation
      (CoxeterNeighbor.rootDifference o) = CoxeterNeighbor.rootDifference o at hv
    exact CoxeterNeighbor.rootDifference_ne_zero o
      ((CoxeterNeighbor.action_fixed_iff _ _).mp hv)
  have he := congrArg (fun e : LatticeCarrier o ≃ₗ[ℂ] LatticeCarrier o =>
    e (carrierBasis o (0, x))) h
  change carrierEquiv o (carrierBasis o (0, x)) = carrierBasis o (0, x) at he
  rw [carrier_empty_charge] at he
  have hc := congrArg (fun v => (carrierBasis o).repr v (0, x)) he
  simp only [map_smul, Basis.repr_self, Finsupp.smul_apply, smul_eq_mul,
    Finsupp.single_apply, Prod.mk.injEq, true_and] at hc
  simp only [if_neg hx, if_pos rfl, mul_zero] at hc
  exact zero_ne_one hc

theorem carrierEquiv_order (o : Fin 12) : orderOf (carrierEquiv o) = 3 := by
  apply orderOf_eq_prime
  · apply LinearEquiv.ext
    intro v
    exact carrierEquiv_cube o v
  · exact carrierEquiv_ne_one o

end HMT.IV.CoxeterChargeCovariance
end

#print axioms HMT.IV.CoxeterChargeCovariance.twisted_shift
#print axioms HMT.IV.CoxeterChargeCovariance.twisted_zeroMode
#print axioms HMT.IV.CoxeterChargeCovariance.carrier_shift
#print axioms HMT.IV.CoxeterChargeCovariance.carrier_zeroMode
#print axioms HMT.IV.CoxeterChargeCovariance.carrierEquiv_order
