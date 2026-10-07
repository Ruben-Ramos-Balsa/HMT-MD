import LatticeFiniteGroundState
import LatticeTwistedOscillatorTensor

/-! Assemble the proved finite irreducible factor and half-integer oscillators.
This is the actual carrier and commuting actions required by the twisted lattice
construction. The twisted vertex operators and the orbifold multiplication are
separate constructions; no such products are assumed by this module. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedCarrier
open TensorProduct
open CoxeterNeighbor LatticeCocycle LatticeOscillatorFock
open LatticeHalfIntegerHeisenberg hiding halfMode
open LatticeFiniteIrreducible LatticeFiniteGroundState
open LatticeTwistedOscillatorTensor

abbrev Carrier (o : Fin 12) := TensorFock (FiniteSpace o) o

instance carrierAddCommGroup (o : Fin 12) : AddCommGroup (Carrier o) :=
  inferInstanceAs (AddCommGroup (TensorFock (FiniteSpace o) o))

instance carrierModule (o : Fin 12) : Module ℂ (Carrier o) :=
  inferInstanceAs (Module ℂ (TensorFock (FiniteSpace o) o))

def groundEmbedding (o : Fin 12) : FiniteSpace o →ₗ[ℂ] Carrier o :=
  TensorProduct.mk ℂ (HalfFock o) (FiniteSpace o) 1

def groundProjection (o : Fin 12) : Carrier o →ₗ[ℂ] FiniteSpace o :=
  (TensorProduct.lid ℂ (FiniteSpace o)).toLinearMap.comp
    ((SymmetricAlgebra.lift (0 : Oscillators o →ₗ[ℂ] ℂ)).toLinearMap.rTensor (FiniteSpace o))

theorem ground_projection_embedding (o : Fin 12) (t : FiniteSpace o) :
    groundProjection o (groundEmbedding o t) = t := by
  simp [groundProjection, groundEmbedding]

theorem groundEmbedding_injective (o : Fin 12) : Function.Injective (groundEmbedding o) :=
  Function.LeftInverse.injective (ground_projection_embedding o)

def groundSubspace (o : Fin 12) : Submodule ℂ (Carrier o) := LinearMap.range (groundEmbedding o)

theorem groundSubspace_dimension (o : Fin 12) :
    Module.finrank ℂ (groundSubspace o) = 4096 := by
  rw [groundSubspace, LinearMap.finrank_range_of_inj (groundEmbedding_injective o)]
  exact finiteSpace_dimension o

abbrev halfMode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ) : Module.End ℂ (Carrier o) :=
  halfModeTensor (FiniteSpace o) o i m

abbrev conformalMode (o : Fin 12) (m : ℤ) : Module.End ℂ (Carrier o) :=
  conformalModeTensor (FiniteSpace o) o m

def chargeOperator (o : Fin 12) (x : Lattice o) : Module.End ℂ (Carrier o) :=
  secondFactorOperator (FiniteSpace o) o (latticeOperator o x)

theorem chargeOperator_product (o : Fin 12) (x y : Lattice o) :
    chargeOperator o x * chargeOperator o y =
      (wittSign o x y : ℂ) • chargeOperator o (x+y) := by
  unfold chargeOperator secondFactorOperator
  rw [← LinearMap.lTensor_mul, latticeOperator_product, LinearMap.lTensor_smul]

theorem chargeOperator_neg (o : Fin 12) (x : Lattice o) :
    chargeOperator o (-x) = chargeOperator o x := by
  unfold chargeOperator
  rw [latticeOperator_neg]

theorem chargeOperator_comm_half (o : Fin 12) (x : Lattice o)
    (i : Fin (BasisSize o)) (m : ℤ) :
    halfMode o i m * chargeOperator o x = chargeOperator o x * halfMode o i m :=
  halfModeTensor_comm_second (FiniteSpace o) o i m (latticeOperator o x)

theorem chargeOperator_comm_conformal (o : Fin 12) (x : Lattice o) (m : ℤ) :
    conformalMode o m * chargeOperator o x = chargeOperator o x * conformalMode o m :=
  conformalModeTensor_comm_second (FiniteSpace o) o m (latticeOperator o x)

theorem ground_weight (o : Fin 12) (t : FiniteSpace o) :
    conformalMode o 0 (groundEmbedding o t) = (3/2:ℂ) • groundEmbedding o t :=
  vacuum_tensor_weight (FiniteSpace o) o t

theorem ground_annihilated (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (t : FiniteSpace o) : halfMode o i n (groundEmbedding o t) = 0 :=
  vacuum_tensor_annihilation (FiniteSpace o) o i n t

theorem virasoro_central_charge_twentyFour (o : Fin 12) (m n : ℤ) :
    conformalMode o m * conformalMode o n - conformalMode o n * conformalMode o m =
      ((m-n:ℤ):ℂ) • conformalMode o (m+n) +
        (if m+n=0 then (2*((m:ℂ)^3-(m:ℂ))) •
          (LinearMap.id : Module.End ℂ (Carrier o)) else 0) :=
  virasoro_tensor_central_charge_twentyFour (FiniteSpace o) o m n

end HMT.IV.LatticeTwistedCarrier
end
