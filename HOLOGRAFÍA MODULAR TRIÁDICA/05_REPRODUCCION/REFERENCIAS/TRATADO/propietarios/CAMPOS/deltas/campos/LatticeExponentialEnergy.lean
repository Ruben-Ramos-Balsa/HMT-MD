import LatticeEulerEnergy
import LatticeCreationExponential

/-!
Every coefficient of the already constructed creation exponential has its
stated oscillator energy. The proof starts from the frequency operator on
charge modes, propagates homogeneity through coefficient convolution and
finite powers, then uses the proved finite coefficient expansion of exp.
All degrees and charges are covered. No FLM construction is asserted.
-/

noncomputable section
namespace HMT.IV.LatticeExponentialEnergy

open scoped BigOperators
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCocycle HMT.IV.LatticeEulerEnergy
open HMT.IV.LatticeCreationExponential
open PowerSeries

def HomogeneousSeries (o : Fin 12) (f : PowerSeries (Fock o)) : Prop :=
  ∀ d, euler o (coeff (Fock o) d f) = (d : ℂ) • coeff (Fock o) d f

theorem euler_chargeCreationState (o : Fin 12) (x : Lattice o) (n : ℕ) :
    euler o (chargeCreationState o x n) = (n+1 : ℂ) • chargeCreationState o x n := by
  simp only [chargeCreationState, chargeModeVector, map_sum, map_smul,
    Derivation.map_smul, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro i _
  have h : euler o (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i)) =
      (n+1 : ℂ) • SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i) :=
    euler_mode o (n,i)
  rw [h, smul_comm]

theorem creationPotential_homogeneous (o : Fin 12) (x : Lattice o) :
    HomogeneousSeries o (creationPotential o x) := by
  intro d
  cases d with
  | zero =>
    rw [coeff_zero_eq_constantCoeff_apply, creationPotential_constant]
    simp
  | succ n =>
    rw [creationPotential_coefficient_succ, Derivation.map_smul, euler_chargeCreationState]
    simp only [Nat.cast_add, Nat.cast_one]
    rw [smul_comm]

theorem homogeneous_one (o : Fin 12) : HomogeneousSeries o 1 := by
  intro d
  simp only [coeff_one]
  split_ifs with hd
  · subst d
    simp
  · simp

theorem homogeneous_mul (o : Fin 12) {f g : PowerSeries (Fock o)}
    (hf : HomogeneousSeries o f) (hg : HomogeneousSeries o g) :
    HomogeneousSeries o (f*g) := by
  intro d
  rw [coeff_mul, map_sum, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro p hp
  have hpd := Finset.mem_antidiagonal.mp hp
  rw [(euler o).leibniz, hf, hg]
  have hcast : (d : ℂ) = (p.1 : ℂ) + (p.2 : ℂ) := by exact_mod_cast hpd.symm
  rw [hcast]
  simp [Algebra.smul_def, smul_eq_mul, map_add]
  ring

theorem homogeneous_pow (o : Fin 12) {f : PowerSeries (Fock o)}
    (hf : HomogeneousSeries o f) (k : ℕ) : HomogeneousSeries o (f^k) := by
  induction k with
  | zero => simpa using homogeneous_one o
  | succ k ih => simpa only [pow_succ] using homogeneous_mul o ih hf

theorem creationPotential_power_energy (o : Fin 12) (x : Lattice o) (k d : ℕ) :
    euler o (coeff (Fock o) d (creationPotential o x ^ k)) =
      (d : ℂ) • coeff (Fock o) d (creationPotential o x ^ k) :=
  homogeneous_pow o (creationPotential_homogeneous o x) k d

theorem creationExponential_coefficient_energy (o : Fin 12) (x : Lattice o) (d : ℕ) :
    euler o (coeff (Fock o) d (creationExponential o x)) =
      (d : ℂ) • coeff (Fock o) d (creationExponential o x) := by
  rw [creationExponential_coefficient, map_sum, Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [Derivation.map_smul, creationPotential_power_energy, smul_comm]

theorem creationExponential_homogeneous (o : Fin 12) (x : Lattice o) :
    HomogeneousSeries o (creationExponential o x) :=
  creationExponential_coefficient_energy o x

end HMT.IV.LatticeExponentialEnergy
end

#print axioms HMT.IV.LatticeExponentialEnergy.euler_chargeCreationState
#print axioms HMT.IV.LatticeExponentialEnergy.creationPotential_homogeneous
#print axioms HMT.IV.LatticeExponentialEnergy.homogeneous_mul
#print axioms HMT.IV.LatticeExponentialEnergy.creationPotential_power_energy
#print axioms HMT.IV.LatticeExponentialEnergy.creationExponential_coefficient_energy
