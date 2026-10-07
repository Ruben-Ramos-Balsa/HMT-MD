import LatticeHalfCreationExponential
import LatticeHalfAnnihilationEnergy
import LatticeTwistedTensorField
import LatticeTwistedLowWeights

/-! The unnormalized normally ordered exponential kernel on the actual
half-oscillator tensor finite-module carrier. The Laurent shift s is an explicit
integer parameter, not a physical prefactor or a derived normalization.
Coefficients use the proved creation and annihilation exponentials and the
existing latticeOperator. Stabilization uses the actual annihilation cutoff.
The resulting field is lower truncated on every state. No mixed-sector locality,
orbifold multiplication, or restriction of this kernel to the positive sector
is asserted. -/

noncomputable section
namespace HMT.IV.LatticeTwistedExponentialKernel
open TensorProduct
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeHalfIntegerHeisenberg LatticeHalfWeightBasis
open LatticeFiniteIrreducible LatticeFiniteGroundState
open LatticeTwistedCarrier LatticeTwistedLowWeights
open LatticeHalfCreationExponential LatticeHalfAnnihilationExponential
open LatticeHalfAnnihilationEnergy

def basisKernelCutoff (o : Fin 12) (x : Lattice o) (s k : ℤ) (N : ℕ)
    (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o))) : Carrier o :=
  ∑ j ∈ Finset.range (N+1),
    if 0 ≤ k-s+(j:ℤ) then
      halfCreationExponentialMode o x ((k-s+(j:ℤ)).toNat)
        (exponentialCoefficient o x j (monomialBasis o a)) ⊗ₜ[ℂ]
          latticeOperator o x (finiteBasis o q)
    else 0

def basisKernelCoefficient (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o))) : Carrier o :=
  basisKernelCutoff o x s k (twiceWeight o a) a q

theorem basisKernelCutoff_stable (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o))) (N : ℕ)
    (hN : twiceWeight o a ≤ N) :
    basisKernelCoefficient o x s k a q = basisKernelCutoff o x s k N a q := by
  unfold basisKernelCoefficient basisKernelCutoff
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro j _ hj
  have hlt : twiceWeight o a < j := by
    simp only [Finset.mem_range] at hj
    omega
  have hz := annihilationCoefficient_cutoff_on_monomial o x j a hlt
  split_ifs
  · rw [hz, map_zero, TensorProduct.zero_tmul]
  · rfl

def kernelCoefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    Module.End ℂ (Carrier o) :=
  (twistedBasis o).constr ℂ (fun p => basisKernelCoefficient o x s k p.1 p.2)

theorem kernelCoefficient_basis (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o))) :
    kernelCoefficient o x s k (twistedBasis o (a,q)) =
      basisKernelCoefficient o x s k a q := Basis.constr_basis _ _ _ _

theorem basisKernelCoefficient_below (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o)))
    (hk : k < s-(twiceWeight o a : ℤ)) : basisKernelCoefficient o x s k a q = 0 := by
  unfold basisKernelCoefficient basisKernelCutoff
  apply Finset.sum_eq_zero
  intro j hj
  have hj' : j ≤ twiceWeight o a := by
    simpa only [Finset.mem_range, Nat.lt_succ_iff] using hj
  rw [if_neg (by omega)]

theorem kernelCoefficient_basis_below (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (a : Occupation o) (q : Fin (Module.finrank ℂ (FiniteSpace o)))
    (hk : k < s-(twiceWeight o a : ℤ)) :
    kernelCoefficient o x s k (twistedBasis o (a,q)) = 0 := by
  rw [kernelCoefficient_basis]
  exact basisKernelCoefficient_below o x s k a q hk

def boundedStates (o : Fin 12) (x : Lattice o) (s : ℤ) : Submodule ℂ (Carrier o) where
  carrier := {v | ∃ b : ℤ, ∀ k < b, kernelCoefficient o x s k v = 0}
  zero_mem' := ⟨0, by intros; exact map_zero _⟩
  add_mem' := by
    rintro v w ⟨b,hb⟩ ⟨c,hc⟩
    refine ⟨min b c, ?_⟩
    intro k hk
    rw [map_add, hb k (lt_of_lt_of_le hk (min_le_left _ _)),
      hc k (lt_of_lt_of_le hk (min_le_right _ _)), add_zero]
  smul_mem' := by
    rintro c v ⟨b,hb⟩
    refine ⟨b, ?_⟩
    intro k hk
    rw [map_smul, hb k hk, smul_zero]

theorem boundedStates_eq_top (o : Fin 12) (x : Lattice o) (s : ℤ) :
    boundedStates o x s = ⊤ := by
  apply top_unique
  rw [← (twistedBasis o).span_eq]
  apply Submodule.span_le.mpr
  rintro _ ⟨⟨a,q⟩,rfl⟩
  exact ⟨s-(twiceWeight o a : ℤ),
    fun k hk => kernelCoefficient_basis_below o x s k a q hk⟩

theorem kernelCoefficient_bounded_pole (o : Fin 12) (x : Lattice o) (s : ℤ)
    (v : Carrier o) : ∃ b : ℤ, ∀ k < b, kernelCoefficient o x s k v = 0 := by
  have h : v ∈ boundedStates o x s := by rw [boundedStates_eq_top]; trivial
  exact h

def exponentialKernel (o : Fin 12) (x : Lattice o) (s : ℤ) :
    VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (kernelCoefficient o x s) (kernelCoefficient_bounded_pole o x s)

theorem exponentialKernel_coefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    HVertexOperator.coeff (exponentialKernel o x s) k = kernelCoefficient o x s k := by
  apply LinearMap.ext
  intro v
  rfl

theorem basisKernelCoefficient_ground (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (q : Fin (Module.finrank ℂ (FiniteSpace o))) :
    basisKernelCoefficient o x s k 0 q =
      if 0 ≤ k-s then
        halfCreationExponentialMode o x (k-s).toNat 1 ⊗ₜ[ℂ]
          latticeOperator o x (finiteBasis o q)
      else 0 := by
  simp [basisKernelCoefficient, basisKernelCutoff, twiceWeight,
    monomialBasis_product, annihilationExponential_constant]

theorem groundEmbedding_basis (o : Fin 12)
    (q : Fin (Module.finrank ℂ (FiniteSpace o))) :
    groundEmbedding o (finiteBasis o q) = twistedBasis o (0,q) := by
  simp [groundEmbedding, twistedBasis, Basis.tensorProduct_apply', monomialBasis_product]

def groundAction (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    FiniteSpace o →ₗ[ℂ] Carrier o :=
  if 0 ≤ k-s then
    (TensorProduct.mk ℂ (HalfFock o) (FiniteSpace o)
      (halfCreationExponentialMode o x (k-s).toNat 1)).comp (latticeOperator o x)
  else 0

theorem kernelCoefficient_ground_comp (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    (kernelCoefficient o x s k).comp (groundEmbedding o) = groundAction o x s k := by
  apply (finiteBasis o).ext
  intro q
  rw [LinearMap.comp_apply, groundEmbedding_basis, kernelCoefficient_basis,
    basisKernelCoefficient_ground]
  by_cases hk : 0 ≤ k-s
  · simp only [groundAction, if_pos hk, LinearMap.comp_apply, TensorProduct.mk_apply]
  · simp only [groundAction, if_neg hk, LinearMap.zero_apply]

theorem kernelCoefficient_ground (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (t : FiniteSpace o) :
    kernelCoefficient o x s k (groundEmbedding o t) =
      if 0 ≤ k-s then
        halfCreationExponentialMode o x (k-s).toNat 1 ⊗ₜ[ℂ] latticeOperator o x t
      else 0 := by
  have h := LinearMap.congr_fun (kernelCoefficient_ground_comp o x s k) t
  by_cases hk : 0 ≤ k-s
  · simpa only [LinearMap.comp_apply, groundAction, if_pos hk,
      TensorProduct.mk_apply] using h
  · simpa only [LinearMap.comp_apply, groundAction, if_neg hk,
      LinearMap.zero_apply] using h

theorem kernelCoefficient_ground_at_shift (o : Fin 12) (x : Lattice o) (s : ℤ)
    (t : FiniteSpace o) :
    kernelCoefficient o x s s (groundEmbedding o t) = groundEmbedding o (latticeOperator o x t) := by
  rw [kernelCoefficient_ground]
  simp [halfCreationExponentialMode_zero, groundEmbedding]

theorem kernelCoefficient_ground_below_shift (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (t : FiniteSpace o) (hk : k < s) :
    kernelCoefficient o x s k (groundEmbedding o t) = 0 := by
  rw [kernelCoefficient_ground, if_neg (by omega)]

end HMT.IV.LatticeTwistedExponentialKernel
end
