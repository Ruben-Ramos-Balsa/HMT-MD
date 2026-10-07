import LatticeNormalOrdering
import LatticeContractionFactor

/-!
Vacuum coefficients of the actual creation/annihilation exponentials.
The scalar contraction is recovered from the already proved operator
identity by evaluation; it is not used to define the operators. The two
degrees remain arbitrary. This is a coefficient step toward charged-field
products, not a substitute for two-region locality or the orbifold.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeVacuumContraction

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialContraction HMT.IV.LatticeNormalOrdering
open HMT.IV.LatticeContractionFactor
open scoped BigOperators

theorem vacuum_contraction (o : Fin 12) (x y : Lattice o) (r d : ℕ) :
    exponentialCoefficient o x r (creationExponentialMode o y d 1) =
      if r ≤ d then scalarContraction (integerPair o x y) r •
        creationExponentialMode o y (d-r) 1 else 0 := by
  have h := congrArg (fun E : Module.End ℂ (Fock o) => E 1)
    (exponential_normal_order_coefficient o x y r d)
  simp only [Module.End.mul_apply, LinearMap.sum_apply, LinearMap.smul_apply,
    ite_apply, LinearMap.zero_apply, annihilationExponential_vacuum] at h
  rw [Finset.sum_eq_single (r,0)] at h
  · by_cases hrd : r ≤ d
    · simpa only [Prod.fst, Prod.snd, if_pos hrd, Module.End.mul_apply,
        annihilationExponential_constant, LinearMap.id_apply] using h
    · simpa only [Prod.fst, Prod.snd, if_neg hrd,
        LinearMap.zero_apply, smul_zero] using h
  · intro p hp hne
    have hp0 : p.2 ≠ 0 := by
      intro hz
      have hs := Finset.mem_antidiagonal.mp hp
      have hp1 : p.1 = r := by omega
      exact hne (Prod.ext hp1 hz)
    by_cases hpd : p.1 ≤ d
    · rw [if_pos hpd, Module.End.mul_apply, annihilationExponential_vacuum,
        if_neg hp0, map_zero, smul_zero]
    · rw [if_neg hpd, LinearMap.zero_apply, smul_zero]
  · simp

theorem vacuum_contraction_diagonal (o : Fin 12) (x y : Lattice o) (r : ℕ) :
    exponentialCoefficient o x r (creationExponentialMode o y r 1) =
      scalarContraction (integerPair o x y) r • (1 : Fock o) := by
  rw [vacuum_contraction, if_pos le_rfl, Nat.sub_self, creationExponentialMode_zero]
  rfl

theorem vacuum_contraction_degree_bound (o : Fin 12) (x y : Lattice o)
    (r d : ℕ) (h : d < r) :
    exponentialCoefficient o x r (creationExponentialMode o y d 1) = 0 := by
  rw [vacuum_contraction, if_neg (by omega)]

theorem vacuum_contraction_pairing_bound (o : Fin 12) (x y : Lattice o)
    (p r d : ℕ) (hpair : integerPair o x y = p) (hpr : p < r) :
    exponentialCoefficient o x r (creationExponentialMode o y d 1) = 0 := by
  rw [vacuum_contraction, hpair, scalarContraction_nat_above p r hpr]
  split_ifs <;> simp

theorem creation_vacuum_contraction (o : Fin 12) (x y : Lattice o)
    (a r d : ℕ) :
    creationExponentialMode o x a
      (exponentialCoefficient o x r (creationExponentialMode o y d 1)) =
      if r ≤ d then scalarContraction (integerPair o x y) r •
        creationExponentialMode o x a (creationExponentialMode o y (d-r) 1)
      else 0 := by
  rw [vacuum_contraction]
  split_ifs <;> simp

end HMT.IV.LatticeVacuumContraction
end

#print axioms HMT.IV.LatticeVacuumContraction.vacuum_contraction
#print axioms HMT.IV.LatticeVacuumContraction.vacuum_contraction_diagonal
#print axioms HMT.IV.LatticeVacuumContraction.vacuum_contraction_degree_bound
#print axioms HMT.IV.LatticeVacuumContraction.vacuum_contraction_pairing_bound
#print axioms HMT.IV.LatticeVacuumContraction.creation_vacuum_contraction
