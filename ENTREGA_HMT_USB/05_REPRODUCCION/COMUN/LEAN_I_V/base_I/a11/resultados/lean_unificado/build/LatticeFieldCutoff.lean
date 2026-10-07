import LatticeWeightFiltration
import LatticeAnnihilationCommutativity

/-!
The existing charged field on every finite-weight Fock state. The finite
formula is the already defined `fieldCutoff`; its equality with the field
constructed by `carrierBasis.constr` is proved, not used as a definition.
-/

noncomputable section
namespace HMT.IV.LatticeFieldCutoff

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeAnnihilationCommutativity
open HMT.IV.LatticeWeightFiltration
open scoped TensorProduct BigOperators

theorem fieldCutoff_zero (o : Fin 12) (x y : Lattice o) (k : ℤ) (N : ℕ) :
    fieldCutoff o x y k N 0 = 0 := by
  simp [fieldCutoff]

theorem fieldCutoff_add (o : Fin 12) (x y : Lattice o) (k : ℤ) (N : ℕ)
    (v w : Fock o) :
    fieldCutoff o x y k N (v+w) =
      fieldCutoff o x y k N v + fieldCutoff o x y k N w := by
  unfold fieldCutoff
  rw [← smul_add, ← Finset.sum_add_distrib]
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  split_ifs
  · rw [map_add, map_add, TensorProduct.add_tmul]
  · simp

theorem fieldCutoff_smul (o : Fin 12) (x y : Lattice o) (k : ℤ) (N : ℕ)
    (c : ℂ) (v : Fock o) :
    fieldCutoff o x y k N (c • v) = c • fieldCutoff o x y k N v := by
  unfold fieldCutoff
  rw [smul_comm c]
  congr 1
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  split_ifs
  · rw [map_smul, map_smul, TensorProduct.smul_tmul']
  · simp

def fieldCutoffLinear (o : Fin 12) (x y : Lattice o) (k : ℤ) (N : ℕ) :
    Fock o →ₗ[ℂ] LatticeCarrier o where
  toFun := fieldCutoff o x y k N
  map_add' := fieldCutoff_add o x y k N
  map_smul' := fieldCutoff_smul o x y k N

theorem carrierBasis_pure (o : Fin 12) (a : Occupation o) (y : Lattice o) :
    carrierBasis o (a,y) = monomialBasis o a ⊗ₜ[ℂ] basisElement o y := by
  simp only [carrierBasis, Basis.tensorProduct_apply, latticeBasisComplex,
    Finsupp.coe_basisSingleOne]
  rfl

/-- Uniform cutoff formula for the original field on an entire filtration stage. -/
theorem fieldCoefficient_eq_cutoff (o : Fin 12) (x y : Lattice o) (k : ℤ)
    (N : ℕ) (v : Fock o) (hv : v ∈ weightAtMost o N) :
    fieldCoefficient o x k (v ⊗ₜ[ℂ] basisElement o y) =
      fieldCutoff o x y k N v := by
  induction hv using Submodule.span_induction with
  | mem v hv =>
    rcases hv with ⟨a, ha, rfl⟩
    rw [← carrierBasis_pure, fieldCoefficient_basis, fieldCutoff_monomial]
    exact basisCoefficientCutoff_stable o x k a y N ha
  | zero => simp [fieldCutoff_zero]
  | add v w _ _ ihv ihw =>
    rw [TensorProduct.add_tmul, map_add, ihv, ihw, fieldCutoff_add]
  | smul c v _ ih =>
    rw [← TensorProduct.smul_tmul', map_smul, ih, fieldCutoff_smul]

/-- Two valid weight bounds give the same coefficient, without an ordering assumption. -/
theorem fieldCutoff_independent (o : Fin 12) (x y : Lattice o) (k : ℤ)
    (N M : ℕ) (v : Fock o) (hN : v ∈ weightAtMost o N)
    (hM : v ∈ weightAtMost o M) :
    fieldCutoff o x y k N v = fieldCutoff o x y k M v := by
  rw [← fieldCoefficient_eq_cutoff o x y k N v hN,
    ← fieldCoefficient_eq_cutoff o x y k M v hM]

/-- Every algebraic Fock state has a single cutoff valid for all charges and modes. -/
theorem exists_uniform_field_cutoff (o : Fin 12) (v : Fock o) :
    ∃ N : ℕ, ∀ (x y : Lattice o) (k : ℤ),
      fieldCoefficient o x k (v ⊗ₜ[ℂ] basisElement o y) =
        fieldCutoff o x y k N v := by
  obtain ⟨N, hN⟩ := exists_weight_bound o v
  exact ⟨N, fun x y k => fieldCoefficient_eq_cutoff o x y k N v hN⟩

/-- An actual annihilation cutoff suffices, independently of the chosen weight bound. -/
theorem fieldCoefficient_eq_of_annihilation_cutoff (o : Fin 12)
    (x y : Lattice o) (k : ℤ) (N : ℕ) (v : Fock o)
    (hv : ∀ d, N < d → exponentialCoefficient o x d v = 0) :
    fieldCoefficient o x k (v ⊗ₜ[ℂ] basisElement o y) =
      fieldCutoff o x y k N v := by
  obtain ⟨M, hM⟩ := exists_weight_bound o v
  calc
    fieldCoefficient o x k (v ⊗ₜ[ℂ] basisElement o y) =
        fieldCutoff o x y k M v := fieldCoefficient_eq_cutoff o x y k M v hM
    _ = fieldCutoff o x y k (max N M) v :=
      fieldCutoff_stable o x y k M (max N M) v (le_max_right _ _)
        (fun d hd => annihilation_cutoff_on_filtration o x M d hd v hM)
    _ = fieldCutoff o x y k N v :=
      (fieldCutoff_stable o x y k N (max N M) v (le_max_left _ _) hv).symm

end HMT.IV.LatticeFieldCutoff
end

#print axioms HMT.IV.LatticeFieldCutoff.fieldCutoff_add
#print axioms HMT.IV.LatticeFieldCutoff.fieldCutoff_smul
#print axioms HMT.IV.LatticeFieldCutoff.fieldCoefficient_eq_cutoff
#print axioms HMT.IV.LatticeFieldCutoff.fieldCutoff_independent
#print axioms HMT.IV.LatticeFieldCutoff.exists_uniform_field_cutoff
#print axioms HMT.IV.LatticeFieldCutoff.fieldCoefficient_eq_of_annihilation_cutoff
