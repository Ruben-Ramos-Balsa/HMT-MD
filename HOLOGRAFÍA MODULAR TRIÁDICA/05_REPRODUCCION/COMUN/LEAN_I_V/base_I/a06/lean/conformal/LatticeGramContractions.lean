import LatticeGramSymmetry
import LatticeModeWeights
import LatticeChargeEnergy

/-! Contractions in the actual lattice basis and oscillator monomials.
The inverse matrix identities are derived in LatticeGramDual. -/
noncomputable section
namespace HMT.IV.LatticeGramContractions
open LatticeCocycle LatticeOscillatorFock LatticeGramDual LatticeGramSymmetry
open LatticeModeWeights LatticeFockMonomialParity LatticeChargeEnergy
open scoped BigOperators

theorem dual_mode_kernel (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) (p : Mode o) :
    ∑ j, gramInv o i j * (if n=p.1 then (n+1 : ℂ)*gram o j p.2 else 0) =
      if p=(n,i) then (n+1 : ℂ) else 0 := by
  classical
  by_cases hn : n=p.1
  · simp only [if_pos hn]
    calc
      _ = (n+1 : ℂ) * ∑ j, gramInv o i j * gram o j p.2 := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intros
        ring
      _ = _ := by
        rw [gramInv_pairing]
        by_cases hi : i=p.2
        · have hp : p=(n,i) := Prod.ext hn.symm hi.symm
          simp only [if_pos hi, if_pos hp, mul_one]
        · have hp : p≠(n,i) := by intro h; exact hi (congrArg Prod.snd h).symm
          simp only [if_neg hi, if_neg hp, mul_zero]
  · have hp : p≠(n,i) := by intro h; exact hn (congrArg Prod.fst h).symm
    simp [hn, hp]

theorem dualAnnihilate_monomial (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (a : Occupation o) :
    (∑ j, gramInv o i j • annihilate o n j (monomialBasis o a)) =
      ((a (n,i) : ℂ) * (n+1 : ℂ)) • monomialBasis o (a-Finsupp.single (n,i) 1) := by
  classical
  simp only [annihilate_monomial, Finsupp.sum, Finset.smul_sum, smul_smul]
  rw [Finset.sum_comm]
  have inner (p : Mode o) :
      (∑ j, (gramInv o i j * ((a p : ℂ) *
        (if n=p.1 then (n+1 : ℂ)*gram o j p.2 else 0))) •
        monomialBasis o (a-Finsupp.single p 1)) =
      ((a p : ℂ) * (if p=(n,i) then (n+1 : ℂ) else 0)) •
        monomialBasis o (a-Finsupp.single p 1) := by
    rw [← Finset.sum_smul]
    congr 1
    calc
      _ = (a p : ℂ) * ∑ j, gramInv o i j *
        (if n=p.1 then (n+1 : ℂ)*gram o j p.2 else 0) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intros
        ring
      _ = _ := by rw [dual_mode_kernel]
  simp_rw [inner]
  rw [Finset.sum_eq_single (n,i)]
  · simp
  · intro p _ hp
    simp [hp]
  · intro hp
    have hz : a (n,i)=0 := Finsupp.notMem_support_iff.mp hp
    simp [hz]

theorem pair_basis_coordinates (o : Fin 12) (j : Fin (BasisSize o)) (x : Lattice o) :
    (integerPair o (latticeBasis o j) x : ℂ) =
      ∑ k, ((latticeBasis o).repr x k : ℂ) * gram o j k := by
  have h := congrArg ((integerForm o) (latticeBasis o j))
    ((latticeBasis o).sum_repr x)
  simp only [map_sum, map_smul] at h
  have hz : (∑ k, (latticeBasis o).repr x k *
      integerPair o (latticeBasis o j) (latticeBasis o k)) =
      integerPair o (latticeBasis o j) x := h
  have hc := congrArg (fun z : ℤ => (z : ℂ)) hz
  simpa only [Int.cast_sum, Int.cast_mul, gram] using hc.symm

theorem dual_pair_coordinates (o : Fin 12) (i : Fin (BasisSize o)) (x : Lattice o) :
    ∑ j, gramInv o i j * (integerPair o (latticeBasis o j) x : ℂ) =
      ((latticeBasis o).repr x i : ℂ) := by
  classical
  simp_rw [pair_basis_coordinates, Finset.mul_sum]
  rw [Finset.sum_comm]
  have inner (k : Fin (BasisSize o)) :
      ∑ j, gramInv o i j * (((latticeBasis o).repr x k : ℂ) * gram o j k) =
      ((latticeBasis o).repr x k : ℂ) * (if i=k then 1 else 0) := by
    rw [← gramInv_pairing, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intros
    ring
  simp_rw [inner]
  simp

end HMT.IV.LatticeGramContractions
end
#print axioms HMT.IV.LatticeGramContractions.dual_mode_kernel
#print axioms HMT.IV.LatticeGramContractions.dualAnnihilate_monomial
#print axioms HMT.IV.LatticeGramContractions.pair_basis_coordinates
#print axioms HMT.IV.LatticeGramContractions.dual_pair_coordinates
