import LatticeHalfVirasoroRelations
import Mathlib.LinearAlgebra.TensorProduct.Basic

/-!
Tensor transport of the proved half-integer oscillator representation.
The second factor is an arbitrary complex vector space, not an assumed
twisted lattice module. The CCR, Virasoro action and vacuum weight are
transported from the same marked-lattice HalfFock by rTensor. Any linear
representation on the second factor commutes with these oscillator operators.
No twisted lattice vertex operator or orbifold product is constructed here.
-/

noncomputable section
namespace HMT.IV.LatticeTwistedOscillatorTensor

open TensorProduct
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfConformalCentralizer LatticeHalfVirasoroRelations

variable (T : Type*) [AddCommGroup T] [Module ℂ T]

abbrev TensorFock (o : Fin 12) := HalfFock o ⊗[ℂ] T

def halfModeTensor (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ) :
    Module.End ℂ (TensorFock T o) := (halfMode o i m).rTensor T

def conformalModeTensor (o : Fin 12) (m : ℤ) :
    Module.End ℂ (TensorFock T o) := (shiftedModes o m).rTensor T

theorem halfModeTensor_tmul (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ)
    (v : HalfFock o) (t : T) :
    halfModeTensor T o i m (v ⊗ₜ[ℂ] t) = halfMode o i m v ⊗ₜ[ℂ] t :=
  LinearMap.rTensor_tmul T (halfMode o i m) t v

theorem conformalModeTensor_tmul (o : Fin 12) (m : ℤ)
    (v : HalfFock o) (t : T) :
    conformalModeTensor T o m (v ⊗ₜ[ℂ] t) = shiftedModes o m v ⊗ₜ[ℂ] t :=
  LinearMap.rTensor_tmul T (shiftedModes o m) t v

theorem half_heisenberg_tensor (o : Fin 12) (i j : Fin (BasisSize o))
    (m n : ℤ) :
    halfModeTensor T o i m * halfModeTensor T o j n -
      halfModeTensor T o j n * halfModeTensor T o i m =
      (if frequency m + frequency n = 0 then
        (frequency m : ℂ) * gram o i j else 0) •
        (LinearMap.id : Module.End ℂ (TensorFock T o)) := by
  have h := congrArg (fun f : Module.End ℂ (HalfFock o) => f.rTensor T)
    (half_heisenberg_relation o i j m n)
  simpa only [LinearMap.rTensor_sub, LinearMap.rTensor_comp,
    LinearMap.rTensor_smul, LinearMap.rTensor_id, halfModeTensor] using h

theorem virasoro_tensor (o : Fin 12) (m n : ℤ) :
    conformalModeTensor T o m * conformalModeTensor T o n -
      conformalModeTensor T o n * conformalModeTensor T o m =
      ((m-n : ℤ) : ℂ) • conformalModeTensor T o (m+n) +
      (if m+n=0 then ((BasisSize o : ℂ)/12 * ((m : ℂ)^3-(m : ℂ))) •
        (LinearMap.id : Module.End ℂ (TensorFock T o)) else 0) := by
  have h := congrArg (fun f : Module.End ℂ (HalfFock o) => f.rTensor T)
    (virasoro_commutator o m n)
  by_cases hmn : m+n=0
  · simpa only [if_pos hmn, LinearMap.rTensor_sub, LinearMap.rTensor_mul,
      LinearMap.rTensor_add, LinearMap.rTensor_smul, LinearMap.rTensor_id,
      conformalModeTensor] using h
  · simpa only [if_neg hmn, LinearMap.rTensor_sub, LinearMap.rTensor_mul,
      LinearMap.rTensor_add, LinearMap.rTensor_smul, LinearMap.rTensor_zero,
      conformalModeTensor] using h

theorem virasoro_tensor_central_charge_twentyFour (o : Fin 12) (m n : ℤ) :
    conformalModeTensor T o m * conformalModeTensor T o n -
      conformalModeTensor T o n * conformalModeTensor T o m =
      ((m-n : ℤ) : ℂ) • conformalModeTensor T o (m+n) +
      (if m+n=0 then (2*((m : ℂ)^3-(m : ℂ))) •
        (LinearMap.id : Module.End ℂ (TensorFock T o)) else 0) := by
  have hr : BasisSize o = 24 := NeighborRank.witt_marked_integer_rank o
  rw [virasoro_tensor, hr]
  norm_num

theorem vacuum_tensor_weight (o : Fin 12) (t : T) :
    conformalModeTensor T o 0 ((1 : HalfFock o) ⊗ₜ[ℂ] t) =
      (3/2 : ℂ) • ((1 : HalfFock o) ⊗ₜ[ℂ] t) := by
  rw [conformalModeTensor_tmul, vacuum_conformal_weight_three_halves,
    TensorProduct.smul_tmul']

theorem vacuum_tensor_annihilation (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (t : T) :
    halfModeTensor T o i (n : ℤ) ((1 : HalfFock o) ⊗ₜ[ℂ] t) = 0 := by
  rw [halfModeTensor_tmul, halfMode_ofNat, halfAnnihilate_vacuum,
    TensorProduct.zero_tmul]

def secondFactorOperator (o : Fin 12) (A : Module.End ℂ T) :
    Module.End ℂ (TensorFock T o) := A.lTensor (HalfFock o)

theorem tensor_factors_commute (o : Fin 12) (A : Module.End ℂ (HalfFock o))
    (B : Module.End ℂ T) :
    A.rTensor T * secondFactorOperator T o B =
      secondFactorOperator T o B * A.rTensor T := by
  change (A.rTensor T).comp (B.lTensor (HalfFock o)) =
    (B.lTensor (HalfFock o)).comp (A.rTensor T)
  rw [LinearMap.rTensor_comp_lTensor, LinearMap.lTensor_comp_rTensor]

theorem halfModeTensor_comm_second (o : Fin 12) (i : Fin (BasisSize o))
    (m : ℤ) (B : Module.End ℂ T) :
    halfModeTensor T o i m * secondFactorOperator T o B =
      secondFactorOperator T o B * halfModeTensor T o i m :=
  tensor_factors_commute T o (halfMode o i m) B

theorem conformalModeTensor_comm_second (o : Fin 12) (m : ℤ)
    (B : Module.End ℂ T) :
    conformalModeTensor T o m * secondFactorOperator T o B =
      secondFactorOperator T o B * conformalModeTensor T o m :=
  tensor_factors_commute T o (shiftedModes o m) B

variable {G : Type*} [Monoid G]

def secondFactorAction (o : Fin 12) (ρ : G →* Module.End ℂ T) :
    G →* Module.End ℂ (TensorFock T o) where
  toFun g := secondFactorOperator T o (ρ g)
  map_one' := by
    change (ρ 1).lTensor (HalfFock o) = 1
    rw [map_one]
    exact LinearMap.lTensor_id (HalfFock o) T
  map_mul' g h := by
    change (ρ (g*h)).lTensor (HalfFock o) =
      (ρ g).lTensor (HalfFock o) * (ρ h).lTensor (HalfFock o)
    rw [map_mul, LinearMap.lTensor_mul]

theorem secondFactorAction_comm_half (o : Fin 12) (ρ : G →* Module.End ℂ T)
    (g : G) (i : Fin (BasisSize o)) (m : ℤ) :
    halfModeTensor T o i m * secondFactorAction T o ρ g =
      secondFactorAction T o ρ g * halfModeTensor T o i m :=
  halfModeTensor_comm_second T o i m (ρ g)

theorem secondFactorAction_comm_conformal (o : Fin 12)
    (ρ : G →* Module.End ℂ T) (g : G) (m : ℤ) :
    conformalModeTensor T o m * secondFactorAction T o ρ g =
      secondFactorAction T o ρ g * conformalModeTensor T o m :=
  conformalModeTensor_comm_second T o m (ρ g)

end HMT.IV.LatticeTwistedOscillatorTensor
end

#print axioms HMT.IV.LatticeTwistedOscillatorTensor.TensorFock
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.halfModeTensor
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.conformalModeTensor
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.halfModeTensor_tmul
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.conformalModeTensor_tmul
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.half_heisenberg_tensor
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.virasoro_tensor
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.virasoro_tensor_central_charge_twentyFour
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.vacuum_tensor_weight
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.vacuum_tensor_annihilation
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.secondFactorOperator
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.tensor_factors_commute
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.halfModeTensor_comm_second
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.conformalModeTensor_comm_second
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.secondFactorAction
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.secondFactorAction_comm_half
#print axioms HMT.IV.LatticeTwistedOscillatorTensor.secondFactorAction_comm_conformal
