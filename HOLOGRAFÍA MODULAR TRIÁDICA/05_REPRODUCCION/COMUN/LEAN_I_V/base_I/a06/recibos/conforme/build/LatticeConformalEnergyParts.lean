import LatticeGramContractions
import LatticeNormalZeroMode
import LatticeEulerEnergy

noncomputable section
namespace HMT.IV.LatticeConformalEnergyParts
open LatticeCocycle LatticeOscillatorFock LatticeGramDual LatticeGramSymmetry
open LatticeGramContractions LatticeModeWeights LatticeFockMonomialParity
open LatticeChargeEnergy LatticeWeightShells LatticeHeisenbergModes
open scoped BigOperators TensorProduct

theorem number_contraction_monomial (o : Fin 12) (n : ℕ) (a : Occupation o) :
    (∑ i, ∑ j, gramInv o i j • create o n i (annihilate o n j (monomialBasis o a))) =
      (∑ i, (a (n,i) : ℂ)*(n+1 : ℂ)) • monomialBasis o a := by
  classical
  rw [Finset.sum_smul]
  apply Finset.sum_congr rfl
  intro i _
  simp_rw [← (create o n i).map_smul]
  rw [← map_sum, dualAnnihilate_monomial, map_smul, create_monomial]
  by_cases hi : a (n,i)=0
  · simp [hi]
  · have hle : Finsupp.single (n,i) 1 ≤ a := by
      rw [Finsupp.single_le_iff]
      omega
    rw [add_tsub_cancel_of_le hle]

theorem quadratic_pair_contraction (o : Fin 12) (x : Lattice o) :
    (∑ i, ∑ j, gramInv o i j * (integerPair o (latticeBasis o j) x : ℂ) *
        (integerPair o (latticeBasis o i) x : ℂ)) = (integerPair o x x : ℂ) := by
  classical
  simp_rw [← Finset.sum_mul, dual_pair_coordinates]
  have h := congrArg (fun y => integerForm o y x) ((latticeBasis o).sum_repr x)
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply,
    smul_eq_mul] at h
  have hz : (∑ i, (latticeBasis o).repr x i *
      integerPair o (latticeBasis o i) x) = integerPair o x x := h
  have hc := congrArg (fun z : ℤ => (z : ℂ)) hz
  simpa only [Int.cast_sum, Int.cast_mul] using hc

theorem half_quadratic_pair_contraction (o : Fin 12) (x : Lattice o) :
    (2:ℂ)⁻¹ * (∑ i, ∑ j, gramInv o i j *
      (integerPair o (latticeBasis o j) x : ℂ) *
      (integerPair o (latticeBasis o i) x : ℂ)) = (halfnormNat o x : ℂ) := by
  rw [quadratic_pair_contraction]
  have h : (integerPair o x x : ℂ) = 2*(halfnormNat o x : ℂ) := by
    exact_mod_cast integerPair_eq_two_halfnorm o x
  rw [h]
  ring

theorem rectangular_weight (o : Fin 12) (a : Occupation o) (N : ℕ)
    (hN : ∀ p ∈ a.support, p.1 < N) :
    (∑ n ∈ Finset.range N, ∑ i, (a (n,i) : ℂ)*(n+1 : ℂ)) =
      (occupationWeight o a : ℂ) := by
  classical
  have hsub : a.support ⊆ (Finset.range N ×ˢ Finset.univ) := by
    intro p hp
    simp only [Finset.mem_product, Finset.mem_range, Finset.mem_univ, and_true]
    exact hN p hp
  calc
    _ = ∑ p ∈ (Finset.range N ×ˢ Finset.univ), (a p : ℂ)*(p.1+1 : ℂ) := by
      exact (Finset.sum_product (Finset.range N) Finset.univ
        (fun p : Mode o => (a p : ℂ)*(p.1+1 : ℂ))).symm
    _ = ∑ p ∈ a.support, (a p : ℂ)*(p.1+1 : ℂ) := by
      symm
      apply Finset.sum_subset hsub
      intro p _ hp
      have hz : a p=0 := Finsupp.notMem_support_iff.mp hp
      simp [hz]
    _ = _ := by
      simp only [occupationWeight, Finsupp.sum, Nat.cast_sum, Nat.cast_mul,
        Nat.cast_add, Nat.cast_one]
      apply Finset.sum_congr rfl
      intros
      ring

theorem oscillators_energy_cutoff (o : Fin 12) (a : Occupation o) (N : ℕ)
    (hN : ∀ p ∈ a.support, p.1 < N) :
    (∑ n ∈ Finset.range N, ∑ i, ∑ j, gramInv o i j •
      create o n i (annihilate o n j (monomialBasis o a))) =
        (occupationWeight o a : ℂ) • monomialBasis o a := by
  simp_rw [number_contraction_monomial]
  rw [← Finset.sum_smul, rectangular_weight o a N hN]

theorem annihilate_monomial_cutoff (o : Fin 12) (a : Occupation o) (N : ℕ)
    (hN : ∀ p ∈ a.support, p.1 < N) (n : ℕ) (hn : N≤n) (i : Fin (BasisSize o)) :
    annihilate o n i (monomialBasis o a)=0 := by
  rw [annihilate_monomial, Finsupp.sum]
  apply Finset.sum_eq_zero
  intro p hp
  have hne : n≠p.1 := by have := hN p hp; omega
  simp [hne]

end HMT.IV.LatticeConformalEnergyParts
end
#print axioms HMT.IV.LatticeConformalEnergyParts.number_contraction_monomial
#print axioms HMT.IV.LatticeConformalEnergyParts.quadratic_pair_contraction
#print axioms HMT.IV.LatticeConformalEnergyParts.half_quadratic_pair_contraction
#print axioms HMT.IV.LatticeConformalEnergyParts.rectangular_weight
#print axioms HMT.IV.LatticeConformalEnergyParts.oscillators_energy_cutoff
#print axioms HMT.IV.LatticeConformalEnergyParts.annihilate_monomial_cutoff
