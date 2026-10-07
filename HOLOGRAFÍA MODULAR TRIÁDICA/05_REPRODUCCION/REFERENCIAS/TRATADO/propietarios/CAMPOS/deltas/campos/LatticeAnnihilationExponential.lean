import LatticeOscillatorFock
import Mathlib.RingTheory.PowerSeries.WellKnown
import Mathlib.Tactic

/-!
The annihilation half uses the existing annihilation operators and lattice
coordinates. Endomorphisms form a noncommutative ring, so the commutative
PowerSeries.subst API is not applied to them. Instead we construct the
coefficientwise exponential by finite powers and prove exact stabilization
at every degree. Positive coefficients annihilate the vacuum. This is not
the complete lattice field or an FLM hypothesis.
-/

noncomputable section
namespace HMT.IV.LatticeAnnihilationExponential

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.FockTransport.Symmetric
open PowerSeries
open scoped BigOperators

abbrev EndSeries (o : Fin 12) := PowerSeries (Module.End ℂ (Fock o))

def chargeAnnihilation (o : Fin 12) (x : Lattice o) (n : ℕ) :
    Module.End ℂ (Fock o) :=
  ∑ i : Fin (BasisSize o), ((latticeBasis o).repr x i : ℂ) • annihilate o n i

theorem chargeAnnihilation_apply (o : Fin 12) (x : Lattice o) (n : ℕ) (v : Fock o) :
    chargeAnnihilation o x n v =
      ∑ i : Fin (BasisSize o), ((latticeBasis o).repr x i : ℂ) • annihilate o n i v := by
  simp [chargeAnnihilation]

theorem chargeAnnihilation_vacuum (o : Fin 12) (x : Lattice o) (n : ℕ) :
    chargeAnnihilation o x n 1 = 0 := by
  simp [chargeAnnihilation, annihilate]

def annihilationTail (o : Fin 12) (x : Lattice o) : EndSeries o :=
  PowerSeries.mk fun n => (-1 / (n+1 : ℂ)) • chargeAnnihilation o x n

def annihilationPotential (o : Fin 12) (x : Lattice o) : EndSeries o :=
  X * annihilationTail o x

theorem annihilationPotential_constant (o : Fin 12) (x : Lattice o) :
    coeff (Module.End ℂ (Fock o)) 0 (annihilationPotential o x) = 0 := by
  simp [annihilationPotential, coeff_zero_eq_constantCoeff_apply]

theorem annihilationPotential_coefficient_succ (o : Fin 12) (x : Lattice o) (n : ℕ) :
    coeff (Module.End ℂ (Fock o)) (n+1) (annihilationPotential o x) =
      (-1 / (n+1 : ℂ)) • chargeAnnihilation o x n := by
  simp [annihilationPotential, annihilationTail, coeff_succ_X_mul]

theorem annihilationPotential_coefficient_vacuum (o : Fin 12) (x : Lattice o)
    (d : ℕ) :
    coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x) 1 = 0 := by
  cases d with
  | zero => rw [annihilationPotential_constant]; rfl
  | succ n =>
    rw [annihilationPotential_coefficient_succ, LinearMap.smul_apply,
      chargeAnnihilation_vacuum, smul_zero]

/-- A k-fold product of a zero-constant potential has no terms below k;
the proof uses ordered multiplication, not commutativity of endomorphisms. -/
theorem potential_power_coefficient_zero (o : Fin 12) (x : Lattice o)
    (k d : ℕ) (h : d < k) :
    coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ k) = 0 := by
  induction k generalizing d with
  | zero => omega
  | succ k ih =>
    rw [pow_succ, coeff_mul]
    apply Finset.sum_eq_zero
    intro p hp
    have hsum := Finset.mem_antidiagonal.mp hp
    by_cases hz : p.2 = 0
    · rw [hz, annihilationPotential_constant, mul_zero]
    · rw [ih p.1 (by omega), zero_mul]

theorem positive_power_coefficient_vacuum (o : Fin 12) (x : Lattice o)
    (k d : ℕ) :
    coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ (k+1)) 1 = 0 := by
  rw [pow_succ, coeff_mul, LinearMap.sum_apply]
  apply Finset.sum_eq_zero
  intro p _
  change (coeff (Module.End ℂ (Fock o)) p.1 (annihilationPotential o x ^ k))
    (coeff (Module.End ℂ (Fock o)) p.2 (annihilationPotential o x) 1) = 0
  rw [annihilationPotential_coefficient_vacuum, map_zero]

/-- Finite, ordered-power coefficient of exp(-sum x(n) w^n/n). -/
def exponentialCoefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    Module.End ℂ (Fock o) :=
  ∑ k ∈ Finset.range (d+1), coeff ℂ k (PowerSeries.exp ℂ) •
    coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ k)

def annihilationExponential (o : Fin 12) (x : Lattice o) : EndSeries o :=
  PowerSeries.mk (exponentialCoefficient o x)

theorem annihilationExponential_coefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    coeff (Module.End ℂ (Fock o)) d (annihilationExponential o x) =
      exponentialCoefficient o x d := coeff_mk _ _

/-- Enlarging the exponential cutoff beyond the requested degree has no
effect; no infinite operator sum is evaluated on a vector. -/
theorem exponentialCoefficient_cutoff (o : Fin 12) (x : Lattice o) (d N : ℕ)
    (hN : d ≤ N) :
    exponentialCoefficient o x d =
      ∑ k ∈ Finset.range (N+1), coeff ℂ k (PowerSeries.exp ℂ) •
        coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ k) := by
  unfold exponentialCoefficient
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro k _ hk
  have hdk : d < k := by simpa only [Finset.mem_range, not_lt] using hk
  rw [potential_power_coefficient_zero o x k d hdk, smul_zero]

theorem annihilationExponential_constant (o : Fin 12) (x : Lattice o) :
    exponentialCoefficient o x 0 = (LinearMap.id : Module.End ℂ (Fock o)) := by
  simp [exponentialCoefficient]
  rfl

theorem annihilationExponential_first (o : Fin 12) (x : Lattice o) :
    exponentialCoefficient o x 1 = -chargeAnnihilation o x 0 := by
  simp [exponentialCoefficient, Finset.sum_range_succ,
    annihilationPotential_coefficient_succ]

theorem annihilationExponential_positive_vacuum (o : Fin 12) (x : Lattice o)
    (d : ℕ) (hd : 0 < d) : exponentialCoefficient o x d 1 = 0 := by
  rw [exponentialCoefficient, LinearMap.sum_apply]
  apply Finset.sum_eq_zero
  intro k _
  rw [LinearMap.smul_apply]
  cases k with
  | zero => simp [PowerSeries.coeff_one, Nat.ne_of_gt hd]
  | succ k => rw [positive_power_coefficient_vacuum, smul_zero]

theorem annihilationExponential_vacuum (o : Fin 12) (x : Lattice o) (d : ℕ) :
    exponentialCoefficient o x d 1 = if d = 0 then 1 else 0 := by
  by_cases hd : d = 0
  · subst d
    rw [annihilationExponential_constant]
    simp
  · rw [annihilationExponential_positive_vacuum o x d (Nat.pos_of_ne_zero hd), if_neg hd]

end HMT.IV.LatticeAnnihilationExponential
end

#print axioms HMT.IV.LatticeAnnihilationExponential.chargeAnnihilation_apply
#print axioms HMT.IV.LatticeAnnihilationExponential.chargeAnnihilation_vacuum
#print axioms HMT.IV.LatticeAnnihilationExponential.annihilationPotential_coefficient_succ
#print axioms HMT.IV.LatticeAnnihilationExponential.potential_power_coefficient_zero
#print axioms HMT.IV.LatticeAnnihilationExponential.positive_power_coefficient_vacuum
#print axioms HMT.IV.LatticeAnnihilationExponential.exponentialCoefficient_cutoff
#print axioms HMT.IV.LatticeAnnihilationExponential.annihilationExponential_constant
#print axioms HMT.IV.LatticeAnnihilationExponential.annihilationExponential_first
#print axioms HMT.IV.LatticeAnnihilationExponential.annihilationExponential_positive_vacuum
#print axioms HMT.IV.LatticeAnnihilationExponential.annihilationExponential_vacuum
