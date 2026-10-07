import LatticeOscillatorFock
import Mathlib.RingTheory.PowerSeries.WellKnown
import Mathlib.RingTheory.PowerSeries.Substitution
import Mathlib.Tactic

/-!
The creation half of a lattice exponential on the actual algebraic Fock space.
For a charge x, the existing integral-basis coordinates define x(-n); the
formal potential has coefficient x(-n)/n. Substitution into Mathlib's formal
exponential is valid because the constant coefficient vanishes. Every output
coefficient is a finite sum, uniformly in its degree. This does not assert a
full lattice vertex operator, the annihilation half or the FLM construction.
-/

noncomputable section
namespace HMT.IV.LatticeCreationExponential

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.FockTransport.Symmetric
open PowerSeries
open scoped BigOperators

/-- The negative mode of a lattice charge, using its integral coordinates
in exactly the basis used by the already constructed oscillators. -/
def chargeModeVector (o : Fin 12) (x : Lattice o) (n : ℕ) : Oscillators o :=
  ∑ i : Fin (BasisSize o), ((latticeBasis o).repr x i : ℂ) • modeVector o n i

def chargeCreationState (o : Fin 12) (x : Lattice o) (n : ℕ) : Fock o :=
  SymmetricAlgebra.ι ℂ (Oscillators o) (chargeModeVector o x n)

def chargeCreation (o : Fin 12) (x : Lattice o) (n : ℕ) :
    Module.End ℂ (Fock o) :=
  ∑ i : Fin (BasisSize o), ((latticeBasis o).repr x i : ℂ) • create o n i

theorem chargeCreation_apply (o : Fin 12) (x : Lattice o) (n : ℕ) (v : Fock o) :
    chargeCreation o x n v = chargeCreationState o x n * v := by
  simp only [chargeCreation, chargeCreationState, chargeModeVector,
    LinearMap.sum_apply, LinearMap.smul_apply, create, creation_apply,
    map_sum, map_smul, Finset.sum_mul, smul_mul_assoc]

def potentialTail (o : Fin 12) (x : Lattice o) : PowerSeries (Fock o) :=
  PowerSeries.mk fun n => (1 / (n+1 : ℂ)) • chargeCreationState o x n

def creationPotential (o : Fin 12) (x : Lattice o) : PowerSeries (Fock o) :=
  X * potentialTail o x

theorem creationPotential_constant (o : Fin 12) (x : Lattice o) :
    constantCoeff (Fock o) (creationPotential o x) = 0 := by
  simp [creationPotential]

theorem creationPotential_coefficient_succ (o : Fin 12) (x : Lattice o) (n : ℕ) :
    coeff (Fock o) (n+1) (creationPotential o x) =
      (1 / (n+1 : ℂ)) • chargeCreationState o x n := by
  simp [creationPotential, potentialTail, coeff_succ_X_mul]

theorem creationPotential_substitutable (o : Fin 12) (x : Lattice o) :
    PowerSeries.HasSubst (creationPotential o x) :=
  PowerSeries.HasSubst.of_constantCoeff_zero' (creationPotential_constant o x)

def creationExponential (o : Fin 12) (x : Lattice o) : PowerSeries (Fock o) :=
  PowerSeries.subst (creationPotential o x) (PowerSeries.exp ℂ)

theorem potential_power_coefficient_zero (o : Fin 12) (x : Lattice o)
    (d k : ℕ) (h : d < k) :
    coeff (Fock o) d (creationPotential o x ^ k) = 0 := by
  rw [creationPotential, mul_pow, coeff_X_pow_mul', if_neg (by omega)]

/-- The apparent infinite exponential sum uses only powers 0,...,d for
coefficient d. This holds for every degree, not only for a sampled prefix. -/
theorem creationExponential_coefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    coeff (Fock o) d (creationExponential o x) =
      ∑ k ∈ Finset.range (d+1),
        (coeff ℂ k (PowerSeries.exp ℂ)) •
          coeff (Fock o) d (creationPotential o x ^ k) := by
  rw [creationExponential, PowerSeries.coeff_subst'
    (creationPotential_substitutable o x)]
  apply finsum_eq_sum_of_support_subset
  intro k hk
  apply Finset.mem_coe.mpr
  apply Finset.mem_range.mpr
  by_contra h
  have hdk : d < k := by omega
  have hz := potential_power_coefficient_zero o x d k hdk
  exact hk (by simp only [hz, smul_zero])

/-- Expanding each power gives a completely finite coefficient formula.
The inner antidiagonal enumerates all ordered degree allocations. -/
theorem creationExponential_coefficient_partition (o : Fin 12) (x : Lattice o)
    (d : ℕ) :
    coeff (Fock o) d (creationExponential o x) =
      ∑ k ∈ Finset.range (d+1), (coeff ℂ k (PowerSeries.exp ℂ)) •
        ∑ a ∈ (Finset.range k).finsuppAntidiag d,
          ∏ i ∈ Finset.range k, coeff (Fock o) (a i) (creationPotential o x) := by
  rw [creationExponential_coefficient]
  apply Finset.sum_congr rfl
  intro k _
  rw [PowerSeries.coeff_pow]

theorem creationExponential_constant (o : Fin 12) (x : Lattice o) :
    coeff (Fock o) 0 (creationExponential o x) = 1 := by
  rw [creationExponential_coefficient]
  simp

theorem creationExponential_first (o : Fin 12) (x : Lattice o) :
    coeff (Fock o) 1 (creationExponential o x) = chargeCreationState o x 0 := by
  rw [creationExponential_coefficient]
  simp [Finset.sum_range_succ, creationPotential_coefficient_succ]

theorem creationPotential_zero_charge (o : Fin 12) :
    creationPotential o 0 = 0 := by
  have hz : potentialTail o 0 = 0 := by
    ext n
    simp [potentialTail, chargeCreationState, chargeModeVector]
  simp [creationPotential, hz]

theorem creationExponential_zero_charge (o : Fin 12) :
    creationExponential o 0 = 1 := by
  ext d
  rw [creationExponential_coefficient]
  rw [Finset.sum_eq_single 0]
  · simp
  · intro k _ hk
    rw [creationPotential_zero_charge, zero_pow hk]
    simp
  · simp

/-- Coefficientwise multiplication supplies actual linear operators on the
existing Fock space, not a new abstract carrier. -/
def creationExponentialMode (o : Fin 12) (x : Lattice o) (d : ℕ) :
    Module.End ℂ (Fock o) :=
  LinearMap.mulLeft ℂ (coeff (Fock o) d (creationExponential o x))

theorem creationExponentialMode_vacuum (o : Fin 12) (x : Lattice o) (d : ℕ) :
    creationExponentialMode o x d 1 = coeff (Fock o) d (creationExponential o x) :=
  mul_one _

theorem creationExponentialMode_zero (o : Fin 12) (x : Lattice o) :
    creationExponentialMode o x 0 = (LinearMap.id : Module.End ℂ (Fock o)) := by
  ext v
  change coeff (Fock o) 0 (creationExponential o x) * v = v
  rw [creationExponential_constant, one_mul]

theorem creationExponentialMode_first (o : Fin 12) (x : Lattice o) :
    creationExponentialMode o x 1 = chargeCreation o x 0 := by
  ext v
  change coeff (Fock o) 1 (creationExponential o x) * v = _
  rw [creationExponential_first, chargeCreation_apply]

end HMT.IV.LatticeCreationExponential
end

#print axioms HMT.IV.LatticeCreationExponential.chargeCreation_apply
#print axioms HMT.IV.LatticeCreationExponential.creationPotential_coefficient_succ
#print axioms HMT.IV.LatticeCreationExponential.creationPotential_substitutable
#print axioms HMT.IV.LatticeCreationExponential.creationExponential_coefficient
#print axioms HMT.IV.LatticeCreationExponential.creationExponential_coefficient_partition
#print axioms HMT.IV.LatticeCreationExponential.creationExponential_constant
#print axioms HMT.IV.LatticeCreationExponential.creationExponential_first
#print axioms HMT.IV.LatticeCreationExponential.creationExponential_zero_charge
#print axioms HMT.IV.LatticeCreationExponential.creationExponentialMode_vacuum
#print axioms HMT.IV.LatticeCreationExponential.creationExponentialMode_zero
#print axioms HMT.IV.LatticeCreationExponential.creationExponentialMode_first
