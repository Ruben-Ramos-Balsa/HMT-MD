import LatticeFieldNormalBridge
import LatticeDressedSymmetry
import LatticeWeightFiltration

/-! Uniform polynomial locality of the original charged lattice fields on
every charged Fock state. The exponent depends only on the lattice pairing.
Both products are compositions of the existing fieldCoefficient operators. -/
noncomputable section
namespace HMT.IV.LatticeChargedLocality
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeAnnihilationExponential HMT.IV.LatticeChargedVertexField
open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeNormalProduct
open HMT.IV.LatticeFieldNormalBridge HMT.IV.LatticeDressedSymmetry
open HMT.IV.LatticeWeightFiltration
open scoped TensorProduct

theorem field_product_eq_rightProduct (o : Fin 12) (x y z : Lattice o)
    (k l : ℤ) (N : ℕ) (v : Fock o)
    (hx : ∀ q, N < q → exponentialCoefficient o x q v = 0)
    (hy : ∀ q, N < q → exponentialCoefficient o y q v = 0) :
    fieldCoefficient o y l (fieldCoefficient o x k (v ⊗ₜ[ℂ] basisElement o z)) =
      rightProduct (integerPair o x y) (dressedNormal o x y z N v) k l := by
  rw [rightProduct_dressed_swap,integerPair_comm o x y]
  exact field_product_eq_leftProduct o y x z l k N v hy hx

theorem charged_locality_on_pure_states (o : Fin 12) (x y : Lattice o) :
    ∃ n : ℕ, ∀ (v : Fock o) (z : Lattice o),
      (crossing^n) (fun k l =>
        fieldCoefficient o x k (fieldCoefficient o y l (v ⊗ₜ[ℂ] basisElement o z))) =
      (crossing^n) (fun k l =>
        fieldCoefficient o y l (fieldCoefficient o x k (v ⊗ₜ[ℂ] basisElement o z))) := by
  obtain ⟨n,hn⟩ := normal_product_polynomial_cancellation o x y
  refine ⟨n,?_⟩
  intro v z
  obtain ⟨N,hv⟩ := exists_weight_bound o v
  have hx : ∀ q, N < q → exponentialCoefficient o x q v = 0 :=
    fun q hq => annihilation_cutoff_on_filtration o x N q hq v hv
  have hy : ∀ q, N < q → exponentialCoefficient o y q v = 0 :=
    fun q hq => annihilation_cutoff_on_filtration o y N q hq v hv
  have hleft : (fun k l => fieldCoefficient o x k
      (fieldCoefficient o y l (v ⊗ₜ[ℂ] basisElement o z))) =
      leftProduct (integerPair o x y) (dressedNormal o x y z N v) := by
    funext k l
    exact field_product_eq_leftProduct o x y z k l N v hx hy
  have hright : (fun k l => fieldCoefficient o y l
      (fieldCoefficient o x k (v ⊗ₜ[ℂ] basisElement o z))) =
      rightProduct (integerPair o x y) (dressedNormal o x y z N v) := by
    funext k l
    exact field_product_eq_rightProduct o x y z k l N v hx hy
  rw [hleft,hright]
  exact hn z N v

end HMT.IV.LatticeChargedLocality
end
#print axioms HMT.IV.LatticeChargedLocality.field_product_eq_rightProduct
#print axioms HMT.IV.LatticeChargedLocality.charged_locality_on_pure_states
