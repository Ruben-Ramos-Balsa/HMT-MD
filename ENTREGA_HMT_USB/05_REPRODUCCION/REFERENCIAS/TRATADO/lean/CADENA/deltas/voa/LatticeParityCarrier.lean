import LatticeOscillatorFock
import WittNegationLift

/-!
Involution on the actual algebraic carrier M(1) tensor C_epsilon[Lambda].
It negates every oscillator generator and lifts lattice negation by the
proved sign-cocycle automorphism. The even and odd projectors are constructed
and checked. This is the untwisted parity decomposition; no twisted module
or orbifold vertex product is assumed or asserted by it.
-/

noncomputable section
namespace HMT.IV.LatticeParityCarrier

open HMT.IV.LatticeOscillatorFock HMT.IV.TwistedGroupAlgebra
open HMT.FockTransport.Symmetric
open scoped TensorProduct

def fockTheta (o : Fin 12) : Fock o →ₐ[ℂ] Fock o :=
  gamma (-LinearMap.id : Oscillators o →ₗ[ℂ] Oscillators o)

@[simp] theorem fockTheta_generator (o : Fin 12) (x : Oscillators o) :
    fockTheta o (SymmetricAlgebra.ι ℂ (Oscillators o) x) =
      -SymmetricAlgebra.ι ℂ (Oscillators o) x := by
  simp [fockTheta]

theorem fockTheta_square (o : Fin 12) (v : Fock o) :
    fockTheta o (fockTheta o v) = v := by
  induction v using SymmetricAlgebra.induction with
  | algebraMap r => simp
  | ι x => simp
  | mul x y hx hy => simp [map_mul, hx, hy]
  | add x y hx hy => simp [map_add, hx, hy]

def carrierTheta (o : Fin 12) : LatticeCarrier o →ₗ[ℂ] LatticeCarrier o :=
  TensorProduct.map (fockTheta o).toLinearMap
    (WittNegationLift.theta o).toLinearEquiv.toLinearMap

@[simp] theorem carrierTheta_pure (o : Fin 12) (v : Fock o)
    (a : TwistedAlgebra o) :
    carrierTheta o (v ⊗ₜ[ℂ] a) = fockTheta o v ⊗ₜ[ℂ] WittNegationLift.theta o a := by
  simp [carrierTheta]

theorem carrierTheta_square (o : Fin 12) (v : LatticeCarrier o) :
    carrierTheta o (carrierTheta o v) = v := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a =>
    simp only [carrierTheta_pure, fockTheta_square]
    rw [WittNegationLift.theta_involutive o a]
  | add x y hx hy => simp [map_add, hx, hy]

theorem carrierTheta_vacuum (o : Fin 12) : carrierTheta o (vacuum o) = vacuum o := by
  simp [vacuum]

def evenProjector (o : Fin 12) : LatticeCarrier o →ₗ[ℂ] LatticeCarrier o :=
  (2 : ℂ)⁻¹ • (LinearMap.id + carrierTheta o)

def oddProjector (o : Fin 12) : LatticeCarrier o →ₗ[ℂ] LatticeCarrier o :=
  (2 : ℂ)⁻¹ • (LinearMap.id - carrierTheta o)

theorem even_fixed (o : Fin 12) (v : LatticeCarrier o) :
    carrierTheta o (evenProjector o v) = evenProjector o v := by
  simp only [evenProjector, LinearMap.smul_apply, LinearMap.add_apply,
    LinearMap.id_apply, map_smul, map_add, carrierTheta_square]
  rw [add_comm]

theorem odd_negated (o : Fin 12) (v : LatticeCarrier o) :
    carrierTheta o (oddProjector o v) = -oddProjector o v := by
  simp only [oddProjector, LinearMap.smul_apply, LinearMap.sub_apply,
    LinearMap.id_apply, map_smul, map_sub, carrierTheta_square]
  module

theorem parity_decomposition (o : Fin 12) (v : LatticeCarrier o) :
    evenProjector o v + oddProjector o v = v := by
  simp only [evenProjector, oddProjector, LinearMap.smul_apply,
    LinearMap.add_apply, LinearMap.sub_apply, LinearMap.id_apply]
  module

theorem even_idempotent (o : Fin 12) (v : LatticeCarrier o) :
    evenProjector o (evenProjector o v) = evenProjector o v := by
  change (2 : ℂ)⁻¹ • (evenProjector o v + carrierTheta o (evenProjector o v)) = _
  rw [even_fixed]
  module

theorem odd_idempotent (o : Fin 12) (v : LatticeCarrier o) :
    oddProjector o (oddProjector o v) = oddProjector o v := by
  change (2 : ℂ)⁻¹ • (oddProjector o v - carrierTheta o (oddProjector o v)) = _
  rw [odd_negated]
  module

theorem even_odd_zero (o : Fin 12) (v : LatticeCarrier o) :
    evenProjector o (oddProjector o v) = 0 := by
  change (2 : ℂ)⁻¹ • (oddProjector o v + carrierTheta o (oddProjector o v)) = 0
  rw [odd_negated]
  simp

theorem odd_even_zero (o : Fin 12) (v : LatticeCarrier o) :
    oddProjector o (evenProjector o v) = 0 := by
  change (2 : ℂ)⁻¹ • (evenProjector o v - carrierTheta o (evenProjector o v)) = 0
  rw [even_fixed]
  simp

end HMT.IV.LatticeParityCarrier
end

#print axioms HMT.IV.LatticeParityCarrier.carrierTheta_square
#print axioms HMT.IV.LatticeParityCarrier.carrierTheta_vacuum
#print axioms HMT.IV.LatticeParityCarrier.parity_decomposition
#print axioms HMT.IV.LatticeParityCarrier.even_idempotent
#print axioms HMT.IV.LatticeParityCarrier.odd_idempotent
#print axioms HMT.IV.LatticeParityCarrier.even_odd_zero
#print axioms HMT.IV.LatticeParityCarrier.odd_even_zero
