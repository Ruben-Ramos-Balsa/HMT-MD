import LatticeAnnihilationEnergy
import LatticeFockMonomialParity

/-!
The weight filtration of the existing algebraic Fock space. Every vector
belongs to a finite stage, and the actual annihilation exponential vanishes
above that stage. No field, lattice, or selected HMT datum is redefined.
-/

noncomputable section
namespace HMT.IV.LatticeWeightFiltration

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeAnnihilationExponential HMT.IV.LatticeAnnihilationEnergy

def weightAtMost (o : Fin 12) (N : ℕ) : Submodule ℂ (Fock o) :=
  Submodule.span ℂ {v | ∃ a, occupationWeight o a ≤ N ∧ monomialBasis o a = v}

theorem monomial_mem (o : Fin 12) (N : ℕ) (a : Occupation o)
    (ha : occupationWeight o a ≤ N) : monomialBasis o a ∈ weightAtMost o N :=
  Submodule.subset_span ⟨a, ha, rfl⟩

theorem weightAtMost_mono (o : Fin 12) : Monotone (weightAtMost o) := by
  intro N M hNM
  apply Submodule.span_mono
  rintro v ⟨a, ha, hv⟩
  exact ⟨a, ha.trans hNM, hv⟩

/-- The maximum weight in the finite basis support supplies the bound. -/
theorem exists_weight_bound (o : Fin 12) (v : Fock o) :
    ∃ N : ℕ, v ∈ weightAtMost o N := by
  classical
  let S := ((monomialBasis o).repr v).support
  refine ⟨S.sup (occupationWeight o), ?_⟩
  rw [← (monomialBasis o).linearCombination_repr v,
    Finsupp.linearCombination_apply, Finsupp.sum]
  apply Submodule.sum_mem
  intro a ha
  apply Submodule.smul_mem
  exact monomial_mem o _ a (Finset.le_sup ha)

theorem annihilation_cutoff_on_filtration (o : Fin 12) (x : Lattice o)
    (N d : ℕ) (hNd : N < d) (v : Fock o) (hv : v ∈ weightAtMost o N) :
    exponentialCoefficient o x d v = 0 := by
  have hker : weightAtMost o N ≤ LinearMap.ker (exponentialCoefficient o x d) := by
    apply Submodule.span_le.mpr
    rintro w ⟨a, ha, rfl⟩
    change exponentialCoefficient o x d (monomialBasis o a) = 0
    exact annihilationCoefficient_cutoff_on_monomial o x d a (ha.trans_lt hNd)
  exact hker hv

end HMT.IV.LatticeWeightFiltration
end

#print axioms HMT.IV.LatticeWeightFiltration.monomial_mem
#print axioms HMT.IV.LatticeWeightFiltration.weightAtMost_mono
#print axioms HMT.IV.LatticeWeightFiltration.exists_weight_bound
#print axioms HMT.IV.LatticeWeightFiltration.annihilation_cutoff_on_filtration
