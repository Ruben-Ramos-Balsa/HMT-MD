import LatticeChargedLocality
import LatticeFieldBiOperators

/-! Locality of the existing charged fields as an equality of their
endomorphism-valued bivariate series, on the full original carrier. -/
noncomputable section
namespace HMT.IV.LatticeChargedLocalityFull
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeFactorConvolution
open HMT.IV.LatticeChargedLocality HMT.IV.LatticeFieldBiOperators
open scoped TensorProduct

theorem charged_fields_locality (o : Fin 12) (x y : Lattice o) :
    ∃ n : ℕ, (crossing^n) (forwardProduct o x y) =
      (crossing^n) (backwardProduct o x y) := by
  obtain ⟨n,hn⟩ := charged_locality_on_pure_states o x y
  refine ⟨n,?_⟩
  funext k l
  apply end_ext_charged o
  intro v z
  rw [crossing_pow_apply,crossing_pow_apply]
  exact congrFun (congrFun (hn v z) k) l

theorem charged_fields_locality_all_states (o : Fin 12) (x y : Lattice o) :
    ∃ n : ℕ, ∀ (v : LatticeCarrier o),
      (crossing^n) (fun k l => fieldCoefficient o x k (fieldCoefficient o y l v)) =
      (crossing^n) (fun k l => fieldCoefficient o y l (fieldCoefficient o x k v)) := by
  obtain ⟨n,hn⟩ := charged_fields_locality o x y
  refine ⟨n,?_⟩
  intro v
  funext k l
  have h := congrArg (fun f => (f k l) v) hn
  dsimp only at h
  rw [crossing_pow_apply,crossing_pow_apply] at h
  exact h

end HMT.IV.LatticeChargedLocalityFull
end
#print axioms HMT.IV.LatticeChargedLocalityFull.charged_fields_locality
#print axioms HMT.IV.LatticeChargedLocalityFull.charged_fields_locality_all_states
