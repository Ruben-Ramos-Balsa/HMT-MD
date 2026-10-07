import LatticeCreationExponential
import LatticeHalfIntegerHeisenberg

/-! Creation exponential for the half-integer lattice modes, in the ramified
coordinate t with z=t². The potential has degree 2n+1 and coefficient
x(-n-1/2)/(n+1/2), in the same inherited Fock algebra and lattice basis.
Every coefficient is a finite sum at every degree; there is no frequency cutoff.
This is the creation factor, not an assertion of mixed-sector locality. -/

noncomputable section
namespace HMT.IV.LatticeHalfCreationExponential
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeCreationExponential PowerSeries
open scoped BigOperators

def halfPotentialTail (o : Fin 12) (x : Lattice o) : PowerSeries (HalfFock o) :=
  PowerSeries.mk fun d => if d % 2 = 0 then
    (2 / (d+1 : ℂ)) • chargeCreationState o x (d/2) else 0

def halfCreationPotential (o : Fin 12) (x : Lattice o) : PowerSeries (HalfFock o) :=
  X * halfPotentialTail o x

theorem halfCreationPotential_constant (o : Fin 12) (x : Lattice o) :
    constantCoeff (HalfFock o) (halfCreationPotential o x) = 0 := by
  simp [halfCreationPotential]

theorem halfCreationPotential_coefficient_odd (o : Fin 12) (x : Lattice o) (n : ℕ) :
    coeff (HalfFock o) (2*n+1) (halfCreationPotential o x) =
      (2 / (2*(n:ℂ)+1)) • chargeCreationState o x n := by
  simp [halfCreationPotential, halfPotentialTail, coeff_succ_X_mul]

theorem halfCreationPotential_coefficient_even (o : Fin 12) (x : Lattice o) (n : ℕ) :
    coeff (HalfFock o) (2*n) (halfCreationPotential o x) = 0 := by
  cases n with
  | zero => simpa only [Nat.mul_zero, coeff_zero_eq_constantCoeff_apply] using
      halfCreationPotential_constant o x
  | succ n =>
    have h : 2*(n+1) = (2*n+1)+1 := by omega
    rw [h]
    simp [halfCreationPotential, halfPotentialTail, coeff_succ_X_mul]

theorem halfCreationPotential_frequency_coefficient (o : Fin 12) (x : Lattice o)
    (n : ℕ) : coeff (HalfFock o) (2*n+1) (halfCreationPotential o x) =
      (1 / ((n:ℂ)+1/2)) • chargeCreationState o x n := by
  rw [halfCreationPotential_coefficient_odd]
  congr 1
  rw [show (n:ℂ)+1/2 = (2*(n:ℂ)+1)/2 by ring, one_div_div]

theorem halfCreationPotential_substitutable (o : Fin 12) (x : Lattice o) :
    PowerSeries.HasSubst (halfCreationPotential o x) :=
  PowerSeries.HasSubst.of_constantCoeff_zero' (halfCreationPotential_constant o x)

def halfCreationExponential (o : Fin 12) (x : Lattice o) : PowerSeries (HalfFock o) :=
  PowerSeries.subst (halfCreationPotential o x) (PowerSeries.exp ℂ)

theorem potential_power_coefficient_zero (o : Fin 12) (x : Lattice o)
    (d k : ℕ) (h : d < k) :
    coeff (HalfFock o) d (halfCreationPotential o x ^ k) = 0 := by
  rw [halfCreationPotential, mul_pow, coeff_X_pow_mul', if_neg (by omega)]

theorem halfCreationExponential_coefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    coeff (HalfFock o) d (halfCreationExponential o x) =
      ∑ k ∈ Finset.range (d+1), (coeff ℂ k (PowerSeries.exp ℂ)) •
        coeff (HalfFock o) d (halfCreationPotential o x ^ k) := by
  rw [halfCreationExponential, PowerSeries.coeff_subst'
    (halfCreationPotential_substitutable o x)]
  apply finsum_eq_sum_of_support_subset
  intro k hk
  apply Finset.mem_coe.mpr
  apply Finset.mem_range.mpr
  by_contra h
  have hz := potential_power_coefficient_zero o x d k (by omega)
  exact hk (by simp only [hz, smul_zero])

theorem halfCreationExponential_coefficient_partition (o : Fin 12) (x : Lattice o)
    (d : ℕ) : coeff (HalfFock o) d (halfCreationExponential o x) =
      ∑ k ∈ Finset.range (d+1), (coeff ℂ k (PowerSeries.exp ℂ)) •
        ∑ a ∈ (Finset.range k).finsuppAntidiag d,
          ∏ i ∈ Finset.range k, coeff (HalfFock o) (a i) (halfCreationPotential o x) := by
  rw [halfCreationExponential_coefficient]
  apply Finset.sum_congr rfl
  intro k _
  rw [PowerSeries.coeff_pow]

theorem halfCreationExponential_constant (o : Fin 12) (x : Lattice o) :
    coeff (HalfFock o) 0 (halfCreationExponential o x) = 1 := by
  rw [halfCreationExponential_coefficient]
  simp

theorem halfCreationExponential_first (o : Fin 12) (x : Lattice o) :
    coeff (HalfFock o) 1 (halfCreationExponential o x) =
      (2:ℂ) • chargeCreationState o x 0 := by
  rw [halfCreationExponential_coefficient]
  have h := halfCreationPotential_coefficient_odd o x 0
  simp only [Nat.mul_zero, Nat.zero_add, Nat.cast_zero, mul_zero, zero_add, div_one] at h
  simp [Finset.sum_range_succ, h]

theorem halfCreationPotential_zero_charge (o : Fin 12) :
    halfCreationPotential o 0 = 0 := by
  have hz : halfPotentialTail o 0 = 0 := by
    ext n
    simp [halfPotentialTail, chargeCreationState, chargeModeVector]
  simp [halfCreationPotential, hz]

theorem halfCreationExponential_zero_charge (o : Fin 12) :
    halfCreationExponential o 0 = 1 := by
  ext d
  rw [halfCreationExponential_coefficient]
  rw [Finset.sum_eq_single 0]
  · simp
  · intro k _ hk
    rw [halfCreationPotential_zero_charge, zero_pow hk]
    simp
  · simp

def halfCreationExponentialMode (o : Fin 12) (x : Lattice o) (d : ℕ) :
    Module.End ℂ (HalfFock o) :=
  LinearMap.mulLeft ℂ (coeff (HalfFock o) d (halfCreationExponential o x))

theorem halfCreationExponentialMode_vacuum (o : Fin 12) (x : Lattice o) (d : ℕ) :
    halfCreationExponentialMode o x d 1 =
      coeff (HalfFock o) d (halfCreationExponential o x) := mul_one _

theorem halfCreationExponentialMode_zero (o : Fin 12) (x : Lattice o) :
    halfCreationExponentialMode o x 0 = (LinearMap.id : Module.End ℂ (HalfFock o)) := by
  ext v
  change coeff (HalfFock o) 0 (halfCreationExponential o x) * v = v
  rw [halfCreationExponential_constant, one_mul]

theorem halfCreationExponentialMode_first (o : Fin 12) (x : Lattice o) :
    halfCreationExponentialMode o x 1 = (2:ℂ) • chargeCreation o x 0 := by
  ext v
  change coeff (HalfFock o) 1 (halfCreationExponential o x) * v = _
  rw [halfCreationExponential_first, smul_mul_assoc, LinearMap.smul_apply,
    chargeCreation_apply]

end HMT.IV.LatticeHalfCreationExponential
end

#print axioms HMT.IV.LatticeHalfCreationExponential.halfCreationPotential_coefficient_odd
#print axioms HMT.IV.LatticeHalfCreationExponential.halfCreationPotential_coefficient_even
#print axioms HMT.IV.LatticeHalfCreationExponential.halfCreationPotential_frequency_coefficient
#print axioms HMT.IV.LatticeHalfCreationExponential.halfCreationExponential_coefficient
#print axioms HMT.IV.LatticeHalfCreationExponential.halfCreationExponential_coefficient_partition
#print axioms HMT.IV.LatticeHalfCreationExponential.halfCreationExponential_zero_charge
#print axioms HMT.IV.LatticeHalfCreationExponential.halfCreationExponentialMode_first
