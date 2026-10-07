import LatticeNormalProduct
import LatticeOperatorCutoff

/-!
Symmetry of the finite oscillator normal product on the already constructed
Fock carrier. Creation coefficients commute because they act by multiplication
in its symmetric algebra; annihilation coefficients use the independently
proved commutation theorem. No vertex-algebra or locality axiom is introduced.
-/

noncomputable section
namespace HMT.IV.LatticeNormalSymmetry

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeNormalProduct HMT.IV.LatticeOperatorCutoff
open scoped BigOperators

theorem creationExponentialModes_commute_apply (o : Fin 12)
    (x y : Lattice o) (a b : ℕ) (v : Fock o) :
    creationExponentialMode o x a (creationExponentialMode o y b v) =
      creationExponentialMode o y b (creationExponentialMode o x a v) := by
  change
    PowerSeries.coeff (Fock o) a (creationExponential o x) *
        (PowerSeries.coeff (Fock o) b (creationExponential o y) * v) =
      PowerSeries.coeff (Fock o) b (creationExponential o y) *
        (PowerSeries.coeff (Fock o) a (creationExponential o x) * v)
  exact mul_left_comm _ _ _

theorem creationExponentialModes_commute (o : Fin 12)
    (x y : Lattice o) (a b : ℕ) :
    Commute (creationExponentialMode o x a) (creationExponentialMode o y b) := by
  show creationExponentialMode o x a * creationExponentialMode o y b =
    creationExponentialMode o y b * creationExponentialMode o x a
  ext v
  exact creationExponentialModes_commute_apply o x y a b v

theorem normalFock_swap (o : Fin 12) (x y : Lattice o) (N : ℕ)
    (v : Fock o) (a b : ℤ) :
    normalFock o x y N v a b = normalFock o y x N v b a := by
  unfold normalFock
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro s hs
  apply Finset.sum_congr rfl
  intro r hr
  by_cases h : 0 ≤ a + (r : ℤ) ∧ 0 ≤ b + (s : ℤ)
  · have h' : 0 ≤ b + (s : ℤ) ∧ 0 ≤ a + (r : ℤ) := h.symm
    simp only [if_pos h, if_pos h']
    rw [creationExponentialModes_commute_apply,
      exponentialCoefficients_commute_apply]
  · have h' : ¬(0 ≤ b + (s : ℤ) ∧ 0 ≤ a + (r : ℤ)) := fun h' => h h'.symm
    simp only [if_neg h, if_neg h']

end HMT.IV.LatticeNormalSymmetry
end

#print axioms HMT.IV.LatticeNormalSymmetry.creationExponentialModes_commute_apply
#print axioms HMT.IV.LatticeNormalSymmetry.creationExponentialModes_commute
#print axioms HMT.IV.LatticeNormalSymmetry.normalFock_swap
