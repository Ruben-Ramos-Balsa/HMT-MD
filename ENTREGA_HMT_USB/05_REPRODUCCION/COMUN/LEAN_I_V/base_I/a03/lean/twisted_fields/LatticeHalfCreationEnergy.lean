import LatticeHalfCreationExponential
import LatticeHalfAnnihilationEnergy

/-! The existing conformal degree operator is a derivation of the actual
Fock algebra, as follows from its already proved action on the monomial basis.
This proves, in every degree, the homogeneity of the half-integer creation
exponential and the graded commutator of its multiplication operators. -/

noncomputable section
namespace HMT.IV.LatticeHalfCreationEnergy
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity LatticeModeWeights
open LatticeHalfIntegerHeisenberg LatticeHalfWeightBasis
open LatticeCreationExponential LatticeHalfCreationExponential
open LatticeHalfAnnihilationEnergy
open PowerSeries
open scoped BigOperators

theorem monomialBasis_mul (o : Fin 12) (a b : Occupation o) :
    monomialBasis o a * monomialBasis o b = monomialBasis o (a+b) := by
  apply (polynomialEquiv o).injective
  simp only [map_mul, polynomialEquiv_monomial, MvPolynomial.monomial_mul, one_mul]

theorem halfDegree_one (o : Fin 12) : halfDegree o 1 = 0 := by
  have h := halfDegree_monomial o 0
  simpa [monomialBasis_product] using h

theorem halfDegree_mul (o : Fin 12) (u v : HalfFock o) :
    halfDegree o (u*v) = halfDegree o u * v + u * halfDegree o v := by
  have h : (LinearMap.mul ℂ (HalfFock o)).compr₂ (halfDegree o) =
      (LinearMap.mul ℂ (HalfFock o)).comp (halfDegree o) +
        (LinearMap.mul ℂ (HalfFock o)).compl₂ (halfDegree o) := by
    apply (monomialBasis o).ext
    intro a
    apply (monomialBasis o).ext
    intro b
    change halfDegree o (monomialBasis o a * monomialBasis o b) =
      halfDegree o (monomialBasis o a) * monomialBasis o b +
        monomialBasis o a * halfDegree o (monomialBasis o b)
    rw [monomialBasis_mul, halfDegree_monomial, halfDegree_monomial,
      halfDegree_monomial, smul_mul_assoc, mul_smul_comm, monomialBasis_mul,
      twiceWeight_add, Nat.cast_add, add_smul]
  exact congrArg (fun f : HalfFock o →ₗ[ℂ] HalfFock o →ₗ[ℂ] HalfFock o => f u v) h

theorem halfDegree_mode (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    halfDegree o (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i)) =
      ((2*n+1 : ℕ) : ℂ) • SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i) := by
  have h := halfDegree_monomial o (Finsupp.single (n,i) 1)
  simpa [monomialBasis_product, oscillatorBasis_mode] using h

theorem halfDegree_chargeCreationState (o : Fin 12) (x : Lattice o) (n : ℕ) :
    halfDegree o (chargeCreationState o x n) =
      ((2*n+1 : ℕ) : ℂ) • chargeCreationState o x n := by
  simp only [chargeCreationState, chargeModeVector, map_sum, map_smul, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [halfDegree_mode, smul_comm]

def HomogeneousSeries (o : Fin 12) (f : PowerSeries (HalfFock o)) : Prop :=
  ∀ d, halfDegree o (coeff (HalfFock o) d f) = (d:ℂ) • coeff (HalfFock o) d f

theorem halfCreationPotential_homogeneous (o : Fin 12) (x : Lattice o) :
    HomogeneousSeries o (halfCreationPotential o x) := by
  intro d
  by_cases hd : d%2=0
  · have he : d=2*(d/2) := by omega
    rw [he, halfCreationPotential_coefficient_even]
    simp
  · have he : d=2*(d/2)+1 := by omega
    rw [he, halfCreationPotential_coefficient_odd, map_smul,
      halfDegree_chargeCreationState, smul_comm]

theorem homogeneous_one (o : Fin 12) : HomogeneousSeries o 1 := by
  intro d
  simp only [coeff_one]
  split_ifs with hd
  · subst d
    simp [halfDegree_one]
  · simp

theorem homogeneous_mul (o : Fin 12) {f g : PowerSeries (HalfFock o)}
    (hf : HomogeneousSeries o f) (hg : HomogeneousSeries o g) :
    HomogeneousSeries o (f*g) := by
  intro d
  rw [coeff_mul, map_sum, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro p hp
  have hpd := Finset.mem_antidiagonal.mp hp
  rw [halfDegree_mul, hf, hg, smul_mul_assoc, mul_smul_comm,
    ← add_smul, ← Nat.cast_add, hpd]

theorem homogeneous_pow (o : Fin 12) {f : PowerSeries (HalfFock o)}
    (hf : HomogeneousSeries o f) (k : ℕ) : HomogeneousSeries o (f^k) := by
  induction k with
  | zero => simpa using homogeneous_one o
  | succ k ih => simpa only [pow_succ] using homogeneous_mul o ih hf

theorem halfCreationPotential_power_energy (o : Fin 12) (x : Lattice o) (k d : ℕ) :
    halfDegree o (coeff (HalfFock o) d (halfCreationPotential o x ^ k)) =
      (d:ℂ) • coeff (HalfFock o) d (halfCreationPotential o x ^ k) :=
  homogeneous_pow o (halfCreationPotential_homogeneous o x) k d

theorem halfCreationExponential_coefficient_energy (o : Fin 12) (x : Lattice o) (d : ℕ) :
    halfDegree o (coeff (HalfFock o) d (halfCreationExponential o x)) =
      (d:ℂ) • coeff (HalfFock o) d (halfCreationExponential o x) := by
  rw [halfCreationExponential_coefficient, map_sum, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [map_smul, halfCreationPotential_power_energy, smul_comm]

theorem halfCreationExponential_homogeneous (o : Fin 12) (x : Lattice o) :
    HomogeneousSeries o (halfCreationExponential o x) :=
  halfCreationExponential_coefficient_energy o x

theorem halfCreationExponentialMode_commutator (o : Fin 12) (x : Lattice o) (d : ℕ) :
    halfDegree o * halfCreationExponentialMode o x d -
      halfCreationExponentialMode o x d * halfDegree o =
        (d:ℂ) • halfCreationExponentialMode o x d := by
  apply LinearMap.ext
  intro v
  change halfDegree o (coeff (HalfFock o) d (halfCreationExponential o x) * v) -
    coeff (HalfFock o) d (halfCreationExponential o x) * halfDegree o v =
      (d:ℂ) • (coeff (HalfFock o) d (halfCreationExponential o x) * v)
  rw [halfDegree_mul, halfCreationExponential_coefficient_energy, smul_mul_assoc]
  abel

end HMT.IV.LatticeHalfCreationEnergy
end

#print axioms HMT.IV.LatticeHalfCreationEnergy.monomialBasis_mul
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfDegree_one
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfDegree_mul
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfDegree_mode
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfDegree_chargeCreationState
#print axioms HMT.IV.LatticeHalfCreationEnergy.HomogeneousSeries
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfCreationPotential_homogeneous
#print axioms HMT.IV.LatticeHalfCreationEnergy.homogeneous_one
#print axioms HMT.IV.LatticeHalfCreationEnergy.homogeneous_mul
#print axioms HMT.IV.LatticeHalfCreationEnergy.homogeneous_pow
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfCreationPotential_power_energy
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfCreationExponential_coefficient_energy
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfCreationExponential_homogeneous
#print axioms HMT.IV.LatticeHalfCreationEnergy.halfCreationExponentialMode_commutator
