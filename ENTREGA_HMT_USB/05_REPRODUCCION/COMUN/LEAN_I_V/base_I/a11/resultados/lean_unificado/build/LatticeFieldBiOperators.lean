import LatticeFactorConvolution
import LatticeFieldCutoff
import LatticeFieldProductLinearity

/-!
Two-variable coefficients of the existing composed fields. Evaluation
commutes with every crossing power, and equality on charged pure states
extends to the full carrier through its already constructed basis.
-/

noncomputable section
namespace HMT.IV.LatticeFieldBiOperators

open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeChargedVertexField
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeFieldCutoff
open scoped TensorProduct

def forwardProduct (o : Fin 12) (x y : Lattice o) :
    BiStates (Module.End ℂ (LatticeCarrier o)) := fun k l =>
  fieldCoefficient o x k * fieldCoefficient o y l

def backwardProduct (o : Fin 12) (x y : Lattice o) :
    BiStates (Module.End ℂ (LatticeCarrier o)) := fun k l =>
  fieldCoefficient o y l * fieldCoefficient o x k

theorem forwardProduct_apply (o : Fin 12) (x y : Lattice o)
    (v : LatticeCarrier o) :
    (fun k l => forwardProduct o x y k l v) =
      LatticeFieldProductLinearity.forwardProduct o x y v := rfl

theorem backwardProduct_apply (o : Fin 12) (x y : Lattice o)
    (v : LatticeCarrier o) :
    (fun k l => backwardProduct o x y k l v) =
      LatticeFieldProductLinearity.reverseProduct o x y v := rfl

theorem crossing_pow_apply {V : Type*} [AddCommGroup V] [Module ℂ V]
    (f : BiStates (Module.End ℂ V)) (n : ℕ) (v : V) (k l : ℤ) :
    ((crossing^n) f k l) v = (crossing^n) (fun a b => f a b v) k l := by
  induction n generalizing k l with
  | zero => rfl
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply]
    change (((crossing^n) f (k-1) l) v - ((crossing^n) f k (l-1)) v) = _
    rw [ih, ih]
    rw [pow_succ', Module.End.mul_apply]
    rfl

theorem end_ext_charged (o : Fin 12) (F G : Module.End ℂ (LatticeCarrier o))
    (h : ∀ (v : Fock o) (z : Lattice o),
      F (v ⊗ₜ[ℂ] basisElement o z) = G (v ⊗ₜ[ℂ] basisElement o z)) : F = G := by
  apply (carrierBasis o).ext
  rintro ⟨a,z⟩
  rw [carrierBasis_pure]
  exact h (monomialBasis o a) z

end HMT.IV.LatticeFieldBiOperators
end

#print axioms HMT.IV.LatticeFieldBiOperators.forwardProduct_apply
#print axioms HMT.IV.LatticeFieldBiOperators.backwardProduct_apply
#print axioms HMT.IV.LatticeFieldBiOperators.crossing_pow_apply
#print axioms HMT.IV.LatticeFieldBiOperators.end_ext_charged
