import LatticeAnnihilationExponential
import LatticeHalfIntegerHeisenberg

/-! The annihilation exponential for half-integer oscillators on the existing
Fock space of the same marked lattice and its inherited cocycle coordinates.
The formal variable here records inverse powers of t, with z=t²: frequency
n+1/2 contributes degree 2n+1 and coefficient -1/(n+1/2). Coefficients of the
exponential are finite ordered-power sums, since End is noncommutative.
No twisted state-field map or FLM orbifold product is assumed. -/

noncomputable section
namespace HMT.IV.LatticeHalfAnnihilationExponential
open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open PowerSeries
open scoped BigOperators

abbrev EndSeries (o : Fin 12) := PowerSeries (Module.End ℂ (HalfFock o))

def chargeHalfAnnihilation (o : Fin 12) (x : Lattice o) (n : ℕ) :
    Module.End ℂ (HalfFock o) :=
  ∑ i : Fin (BasisSize o), ((latticeBasis o).repr x i : ℂ) • halfAnnihilate o n i

theorem chargeHalfAnnihilation_apply (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v : HalfFock o) : chargeHalfAnnihilation o x n v =
      ∑ i : Fin (BasisSize o), ((latticeBasis o).repr x i : ℂ) • halfAnnihilate o n i v := by
  simp [chargeHalfAnnihilation]

theorem chargeHalfAnnihilation_eq_scale (o : Fin 12) (x : Lattice o) (n : ℕ) :
    chargeHalfAnnihilation o x n = annihilationScale n •
      LatticeAnnihilationExponential.chargeAnnihilation o x n := by
  simp only [chargeHalfAnnihilation, halfAnnihilate,
    LatticeAnnihilationExponential.chargeAnnihilation, Finset.smul_sum, smul_smul]
  congr 1
  funext i
  rw [mul_comm]

theorem chargeHalfAnnihilation_vacuum (o : Fin 12) (x : Lattice o) (n : ℕ) :
    chargeHalfAnnihilation o x n 1 = 0 := by
  simp [chargeHalfAnnihilation_apply, halfAnnihilate_vacuum]

def annihilationPotential (o : Fin 12) (x : Lattice o) : EndSeries o :=
  PowerSeries.mk fun d => if d % 2 = 1 then
    (-1 / (((d/2 : ℕ) : ℂ)+1/2)) • chargeHalfAnnihilation o x (d/2) else 0

theorem annihilationPotential_coefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x) =
      if d % 2 = 1 then
        (-1 / (((d/2 : ℕ) : ℂ)+1/2)) • chargeHalfAnnihilation o x (d/2) else 0 :=
  coeff_mk _ _

theorem annihilationPotential_coefficient_odd (o : Fin 12) (x : Lattice o) (n : ℕ) :
    coeff (Module.End ℂ (HalfFock o)) (2*n+1) (annihilationPotential o x) =
      (-1 / ((n:ℂ)+1/2)) • chargeHalfAnnihilation o x n := by
  rw [annihilationPotential_coefficient]
  have hm : (2*n+1)%2=1 := by omega
  have hd : (2*n+1)/2=n := by omega
  rw [if_pos hm, hd]

theorem annihilationPotential_coefficient_even (o : Fin 12) (x : Lattice o) (n : ℕ) :
    coeff (Module.End ℂ (HalfFock o)) (2*n) (annihilationPotential o x) = 0 := by
  rw [annihilationPotential_coefficient, if_neg (by omega)]

theorem annihilationPotential_constant (o : Fin 12) (x : Lattice o) :
    coeff (Module.End ℂ (HalfFock o)) 0 (annihilationPotential o x) = 0 :=
  annihilationPotential_coefficient_even o x 0

theorem annihilationPotential_coefficient_vacuum (o : Fin 12) (x : Lattice o)
    (d : ℕ) : coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x) 1 = 0 := by
  rw [annihilationPotential_coefficient]
  split_ifs
  · rw [LinearMap.smul_apply, chargeHalfAnnihilation_vacuum, smul_zero]
  · rfl

theorem potential_power_coefficient_zero (o : Fin 12) (x : Lattice o)
    (k d : ℕ) (h : d < k) :
    coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x ^ k) = 0 := by
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
    coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x ^ (k+1)) 1 = 0 := by
  rw [pow_succ, coeff_mul, LinearMap.sum_apply]
  apply Finset.sum_eq_zero
  intro p _
  change (coeff (Module.End ℂ (HalfFock o)) p.1 (annihilationPotential o x ^ k))
    (coeff (Module.End ℂ (HalfFock o)) p.2 (annihilationPotential o x) 1) = 0
  rw [annihilationPotential_coefficient_vacuum, map_zero]

def exponentialCoefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    Module.End ℂ (HalfFock o) :=
  ∑ k ∈ Finset.range (d+1), coeff ℂ k (PowerSeries.exp ℂ) •
    coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x ^ k)

def annihilationExponential (o : Fin 12) (x : Lattice o) : EndSeries o :=
  PowerSeries.mk (exponentialCoefficient o x)

theorem annihilationExponential_coefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    coeff (Module.End ℂ (HalfFock o)) d (annihilationExponential o x) =
      exponentialCoefficient o x d := coeff_mk _ _

theorem exponentialCoefficient_cutoff (o : Fin 12) (x : Lattice o) (d N : ℕ)
    (hN : d ≤ N) :
    exponentialCoefficient o x d =
      ∑ k ∈ Finset.range (N+1), coeff ℂ k (PowerSeries.exp ℂ) •
        coeff (Module.End ℂ (HalfFock o)) d (annihilationPotential o x ^ k) := by
  unfold exponentialCoefficient
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro k _ hk
  have hdk : d < k := by simpa only [Finset.mem_range, not_lt] using hk
  rw [potential_power_coefficient_zero o x k d hdk, smul_zero]

theorem annihilationExponential_constant (o : Fin 12) (x : Lattice o) :
    exponentialCoefficient o x 0 = (LinearMap.id : Module.End ℂ (HalfFock o)) := by
  simp [exponentialCoefficient]
  rfl

theorem annihilationExponential_first (o : Fin 12) (x : Lattice o) :
    exponentialCoefficient o x 1 = (-2:ℂ) • chargeHalfAnnihilation o x 0 := by
  simp [exponentialCoefficient, Finset.sum_range_succ,
    annihilationPotential_coefficient]

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

end HMT.IV.LatticeHalfAnnihilationExponential
end

#print axioms HMT.IV.LatticeHalfAnnihilationExponential.EndSeries
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.chargeHalfAnnihilation
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.chargeHalfAnnihilation_apply
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.chargeHalfAnnihilation_eq_scale
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.chargeHalfAnnihilation_vacuum
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationPotential
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationPotential_coefficient
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationPotential_coefficient_odd
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationPotential_coefficient_even
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationPotential_constant
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationPotential_coefficient_vacuum
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.potential_power_coefficient_zero
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.positive_power_coefficient_vacuum
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.exponentialCoefficient
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationExponential
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationExponential_coefficient
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.exponentialCoefficient_cutoff
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationExponential_constant
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationExponential_first
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationExponential_positive_vacuum
#print axioms HMT.IV.LatticeHalfAnnihilationExponential.annihilationExponential_vacuum
