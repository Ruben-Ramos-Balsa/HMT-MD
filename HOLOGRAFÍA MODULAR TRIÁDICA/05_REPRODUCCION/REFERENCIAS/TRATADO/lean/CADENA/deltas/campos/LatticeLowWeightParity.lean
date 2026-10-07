import LatticeEnergyGrading
import MarkedNeighborMinimum

/-!
The low energy spaces of the same constructed, root-free lattice carrier.
The zero space is exactly the vacuum line. The reflected untwisted sector
has no even vectors of weight one. The latter is not, by itself, a theorem
about the still separate twisted module of the FLM orbifold.
-/

noncomputable section
namespace HMT.IV.LatticeLowWeightParity

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeWeightFiniteness
open HMT.IV.LatticeWeightShells HMT.IV.LatticeFullGradedTrace
open HMT.IV.LatticeEnergyGrading HMT.IV.LatticeParityCarrier
open HMT.IV.CoxeterNeighbor
open scoped BigOperators

theorem occupationWeight_zero_iff (o : Fin 12) (a : Occupation o) :
    occupationWeight o a = 0 ↔ a = 0 := by
  constructor
  · intro h
    ext p
    have hp := entry_le_weight o a p
    rw [h] at hp
    exact Nat.eq_zero_of_le_zero hp
  · rintro rfl
    simp [occupationWeight]

theorem occupationLength_le_weight (o : Fin 12) (a : Occupation o) :
    occupationLength o a ≤ occupationWeight o a := by
  unfold occupationLength occupationWeight Finsupp.sum
  apply Finset.sum_le_sum
  intro p _
  nlinarith

theorem occupationLength_zero_iff (o : Fin 12) (a : Occupation o) :
    occupationLength o a = 0 ↔ a = 0 := by
  constructor
  · intro h
    ext p
    by_cases hp : p ∈ a.support
    · have ht : a p ≤ occupationLength o a :=
        Finset.single_le_sum (fun _ _ => Nat.zero_le _) hp
      rw [h] at ht
      exact Nat.eq_zero_of_le_zero ht
    · exact Finsupp.notMem_support_iff.mp hp
  · rintro rfl
    simp [occupationLength]

theorem length_of_weight_one (o : Fin 12) (a : Occupation o)
    (ha : occupationWeight o a = 1) : occupationLength o a = 1 := by
  have hle := occupationLength_le_weight o a
  have hne : occupationLength o a ≠ 0 := by
    intro h
    have hz := (occupationLength_zero_iff o a).mp h
    have hw := (occupationWeight_zero_iff o a).mpr hz
    omega
  omega

theorem halfnorm_ne_one (o : Fin 12) (x : Lattice o) : halfnormNat o x ≠ 1 := by
  intro h
  have hi := integerPair_eq_two_halfnorm o x
  rw [h] at hi
  have hq : pairing (x : Space 12) (x : Space 12) = 2 := by
    rw [← cast_integerPair, hi]
    norm_num
  exact witt_marked_neighbor_no_norm_two o x x.property hq

theorem fullLabel_zero (o : Fin 12) (a : FullLabel o 0) : a.val = (0,0) := by
  have h := a.property
  have hweight : occupationWeight o a.val.1 = 0 := by omega
  have hnorm : halfnormNat o a.val.2 = 0 := by omega
  exact Prod.ext ((occupationWeight_zero_iff o _).mp hweight)
    ((halfnormNat_eq_zero_iff o _).mp hnorm)

theorem weight_zero_is_vacuum_line (o : Fin 12) :
    fullWeightSpace o 0 = Submodule.span ℂ {vacuum o} := by
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro _ ⟨a,rfl⟩
    change carrierBasis o a.val ∈ Submodule.span ℂ {vacuum o}
    rw [fullLabel_zero o a, vacuum_is_empty_monomial]
    exact Submodule.subset_span (Set.mem_singleton _)
  · apply Submodule.span_le.mpr
    rintro v hv
    rw [Set.mem_singleton_iff] at hv
    subst v
    rw [← vacuum_is_empty_monomial]
    exact Submodule.subset_span ⟨⟨(0,0), by simp [occupationWeight]⟩,rfl⟩

theorem energy_zero_is_vacuum_line (o : Fin 12) :
    Module.End.eigenspace (energy o) 0 = Submodule.span ℂ {vacuum o} := by
  rw [← Nat.cast_zero (R := ℂ), ← fullWeightSpace_eq_eigenspace,
    weight_zero_is_vacuum_line]

theorem fullLabel_one_charge_zero (o : Fin 12) (a : FullLabel o 1) : a.val.2 = 0 := by
  have h := a.property
  have hn := halfnorm_ne_one o a.val.2
  apply (halfnormNat_eq_zero_iff o _).mp
  omega

theorem fullLabel_one_length (o : Fin 12) (a : FullLabel o 1) :
    occupationLength o a.val.1 = 1 := by
  apply length_of_weight_one
  have h := a.property
  simpa only [fullLabel_one_charge_zero o a, halfnormNat_zero, add_zero] using h

theorem theta_weight_one (o : Fin 12) :
    fullTheta o 1 = -(LinearMap.id : Module.End ℂ (fullWeightSpace o 1)) := by
  apply (fullBasis o 1).ext
  intro a
  rw [fullTheta_basis, fullLabel_one_length, pow_one,
    (reflectedLabel_fixed o 1 a).mpr (fullLabel_one_charge_zero o a)]
  change (-1 : ℂ) • fullBasis o 1 a = -fullBasis o 1 a
  exact neg_one_smul ℂ (fullBasis o 1 a)

theorem fixed_weight_one_eq_zero (o : Fin 12) (v : LatticeCarrier o)
    (hv : v ∈ fullWeightSpace o 1) (hfix : carrierTheta o v = v) : v = 0 := by
  have h := fullTheta_is_actual_restriction o 1 ⟨v,hv⟩
  rw [theta_weight_one] at h
  have he : -v = v := by simpa using h.trans hfix
  have htwo : (2 : ℂ) • v = 0 := by
    rw [two_smul]
    exact neg_eq_iff_add_eq_zero.mp he
  have hhalf := congrArg (fun w : LatticeCarrier o => (1/2 : ℂ) • w) htwo
  simpa only [smul_smul, smul_zero, show (1/2 : ℂ)*2=1 by norm_num,
    one_smul] using hhalf

end HMT.IV.LatticeLowWeightParity
end

#print axioms HMT.IV.LatticeLowWeightParity.occupationWeight_zero_iff
#print axioms HMT.IV.LatticeLowWeightParity.length_of_weight_one
#print axioms HMT.IV.LatticeLowWeightParity.halfnorm_ne_one
#print axioms HMT.IV.LatticeLowWeightParity.weight_zero_is_vacuum_line
#print axioms HMT.IV.LatticeLowWeightParity.energy_zero_is_vacuum_line
#print axioms HMT.IV.LatticeLowWeightParity.theta_weight_one
#print axioms HMT.IV.LatticeLowWeightParity.fixed_weight_one_eq_zero
