import LatticeHalfFockPairing
import LatticeFiniteInvariantPairing
import LatticeTwistedLowWeights
import Mathlib.LinearAlgebra.BilinearForm.TensorProduct

/-! The form on the existing twisted tensor carrier. The finite-ground form
is the derived equivariant duality, not an assumed target pairing. No symmetry
of that ground form or complete vertex invariance is presumed. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedTensorPairing
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfFockPairing LatticeFiniteInvariantPairing LatticeFiniteIrreducible
open LatticeTwistedCarrier LatticeTwistedLowWeights LatticeTwistedOscillatorTensor
open scoped TensorProduct

def tensorPairing (o : Fin 12) : LinearMap.BilinForm ℂ (Carrier o) :=
  (contravariantPairing o).tmul (invariantPairing o)

theorem tensorPairing_pure (o : Fin 12) (u v : HalfFock o) (s t : FiniteSpace o) :
    tensorPairing o (u ⊗ₜ[ℂ] s) (v ⊗ₜ[ℂ] t) =
      invariantPairing o s t * contravariantPairing o u v := rfl

def groundRightDual (o : Fin 12) (j : Fin (Module.finrank ℂ (FiniteSpace o))) : FiniteSpace o :=
  (((invariantPairing o).flip).toDual (invariantPairing_nondegenerate o).flip).symm
    ((finiteBasis o).coord j)

def groundLeftDual (o : Fin 12) (j : Fin (Module.finrank ℂ (FiniteSpace o))) : FiniteSpace o :=
  (invariantDuality o).symm ((finiteBasis o).coord j)

theorem groundRightDual_pair (o : Fin 12) (j : Fin (Module.finrank ℂ (FiniteSpace o)))
    (t : FiniteSpace o) : invariantPairing o t (groundRightDual o j) = (finiteBasis o).repr t j := by
  exact LinearMap.BilinForm.apply_toDual_symm_apply (B := (invariantPairing o).flip)
    ((finiteBasis o).coord j) t

theorem groundLeftDual_pair (o : Fin 12) (j : Fin (Module.finrank ℂ (FiniteSpace o)))
    (t : FiniteSpace o) : invariantPairing o (groundLeftDual o j) t = (finiteBasis o).repr t j :=
  invariantDuality_represents o ((finiteBasis o).coord j) t

def groundCoordinates (o : Fin 12) : Carrier o ≃ₗ[ℂ]
    (Fin (Module.finrank ℂ (FiniteSpace o)) →₀ HalfFock o) :=
  TensorProduct.equivFinsuppOfBasisRight (finiteBasis o)

theorem tensorPairing_right_test (o : Fin 12) (w : Carrier o) (u : HalfFock o)
    (j : Fin (Module.finrank ℂ (FiniteSpace o))) :
    tensorPairing o w (u ⊗ₜ[ℂ] groundRightDual o j) =
      contravariantPairing o (groundCoordinates o w j) u := by
  induction w using TensorProduct.induction_on with
  | zero => simp
  | tmul v t =>
    rw [tensorPairing_pure, groundRightDual_pair]
    change _ = contravariantPairing o
      ((TensorProduct.equivFinsuppOfBasisRight (finiteBasis o)) (v ⊗ₜ[ℂ] t) j) u
    rw [TensorProduct.equivFinsuppOfBasisRight_apply_tmul_apply]
    simp only [map_smul, LinearMap.smul_apply, smul_eq_mul]
  | add x y hx hy => simp only [map_add, LinearMap.add_apply, Finsupp.add_apply, hx, hy]

theorem tensorPairing_left_test (o : Fin 12) (w : Carrier o) (u : HalfFock o)
    (j : Fin (Module.finrank ℂ (FiniteSpace o))) :
    tensorPairing o (u ⊗ₜ[ℂ] groundLeftDual o j) w =
      contravariantPairing o u (groundCoordinates o w j) := by
  induction w using TensorProduct.induction_on with
  | zero => simp
  | tmul v t =>
    rw [tensorPairing_pure, groundLeftDual_pair]
    change _ = contravariantPairing o u
      ((TensorProduct.equivFinsuppOfBasisRight (finiteBasis o)) (v ⊗ₜ[ℂ] t) j)
    rw [TensorProduct.equivFinsuppOfBasisRight_apply_tmul_apply]
    simp only [map_smul, smul_eq_mul]
  | add x y hx hy => simp only [map_add, Finsupp.add_apply, hx, hy]

theorem tensorPairing_nondegenerate (o : Fin 12) : (tensorPairing o).Nondegenerate := by
  intro v hv
  apply (groundCoordinates o).injective
  apply Finsupp.ext
  intro j
  simp only [map_zero, Finsupp.zero_apply]
  apply contravariantPairing_nondegenerate o
  intro u
  rw [← tensorPairing_right_test]
  exact hv _

theorem tensorPairing_right_separating (o : Fin 12) (v : Carrier o)
    (h : ∀ w, tensorPairing o w v = 0) : v = 0 := by
  apply (groundCoordinates o).injective
  apply Finsupp.ext
  intro j
  simp only [map_zero, Finsupp.zero_apply]
  apply contravariantPairing_right_separating o
  intro u
  rw [← tensorPairing_left_test]
  exact h _

theorem tensorPairing_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (u v : Carrier o) :
    tensorPairing o (LatticeTwistedCarrier.halfMode o i (Int.negSucc n) u) v =
      -tensorPairing o u (LatticeTwistedCarrier.halfMode o i (n:ℤ) v) := by
  induction u using TensorProduct.induction_on with
  | zero => simp
  | tmul u s =>
    induction v using TensorProduct.induction_on with
    | zero => simp
    | tmul v t =>
      change tensorPairing o (halfModeTensor (FiniteSpace o) o i (Int.negSucc n) (u ⊗ₜ[ℂ] s))
        (v ⊗ₜ[ℂ] t) = -tensorPairing o (u ⊗ₜ[ℂ] s)
        (halfModeTensor (FiniteSpace o) o i (n:ℤ) (v ⊗ₜ[ℂ] t))
      rw [halfModeTensor_tmul, halfModeTensor_tmul, tensorPairing_pure, tensorPairing_pure]
      change _ * contravariantPairing o (create o n i u) v =
        -(_ * contravariantPairing o u (halfAnnihilate o n i v))
      rw [contravariantPairing_create, mul_neg]
    | add x y hx hy => simp only [map_add, hx, hy, neg_add_rev]; abel
  | add x y hx hy => simp only [map_add, LinearMap.add_apply, hx, hy, neg_add_rev]; abel

theorem tensorPairing_charge_invariant (o : Fin 12) (x : Lattice o) (u v : Carrier o) :
    tensorPairing o (chargeOperator o x u) (chargeOperator o x v) = tensorPairing o u v := by
  induction u using TensorProduct.induction_on with
  | zero => simp
  | tmul u s =>
    induction v using TensorProduct.induction_on with
    | zero => simp
    | tmul v t =>
      change tensorPairing o
        (u ⊗ₜ[ℂ] LatticeFiniteGroundState.latticeOperator o x s)
        (v ⊗ₜ[ℂ] LatticeFiniteGroundState.latticeOperator o x t) = _
      rw [tensorPairing_pure, tensorPairing_pure, latticeOperator_preserves_pairing]
    | add x y hx hy => simp only [map_add, hx, hy]
  | add x y hx hy => simp only [map_add, LinearMap.add_apply, hx, hy]

end HMT.IV.LatticeTwistedTensorPairing
end
