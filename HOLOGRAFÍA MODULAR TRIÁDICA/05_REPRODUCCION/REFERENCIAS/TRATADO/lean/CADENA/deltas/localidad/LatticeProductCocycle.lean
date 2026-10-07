import WittTwistedAlgebra
import LatticeTwoRegionFactor

/-! The cocycle of the selected lattice supplies exactly the sign required
by the two formal expansions. No scalar sign is added as an independent input. -/
noncomputable section
namespace HMT.IV.LatticeProductCocycle
open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra

theorem sign_integer_zpow (p : ℤ) :
    ((TC.sign (p : ZMod 2) : ℤ) : ℂ) = (-1 : ℂ)^p := by
  induction p using Int.induction_on with
  | zero => norm_num [TC.sign]
  | succ p ih =>
      rw [Int.cast_add, Int.cast_one, TC.sign_add, Int.cast_mul, ih]
      rw [zpow_add₀ (by norm_num : (-1 : ℂ) ≠ 0)]
      norm_num [TC.sign]
  | pred p ih =>
      rw [Int.cast_sub, Int.cast_one]
      have hs : ∀ q : ZMod 2, q - 1 = q + 1 := by intro q; fin_cases q <;> decide
      rw [hs, TC.sign_add, Int.cast_mul, ih]
      rw [zpow_sub₀ (by norm_num : (-1 : ℂ) ≠ 0)]
      norm_num [TC.sign, div_eq_mul_inv]

theorem epsilon_commutator (o : Fin 12) (x y : Lattice o) :
    epsilon o x y * epsilon o y x = (-1 : ℂ)^(integerPair o x y) := by
  rw [← sign_integer_zpow]
  unfold epsilon
  exact_mod_cast wittSign_commutator o x y

theorem epsilon_reverse (o : Fin 12) (x y : Lattice o) :
    epsilon o y x = (-1 : ℂ)^(integerPair o x y) * epsilon o x y := by
  rw [← epsilon_commutator]
  calc
    epsilon o y x = (epsilon o x y * epsilon o x y) * epsilon o y x := by
      rw [epsilon_square, one_mul]
    _ = _ := by ring

theorem product_cocycle_left (o : Fin 12) (x y z : Lattice o) :
    epsilon o y z * epsilon o x (y+z) =
      epsilon o x y * epsilon o (x+y) z := (epsilon_cocycle o x y z).symm

theorem product_cocycle_right (o : Fin 12) (x y z : Lattice o) :
    epsilon o x z * epsilon o y (x+z) =
      (-1 : ℂ)^(integerPair o x y) *
        (epsilon o x y * epsilon o (x+y) z) := by
  rw [product_cocycle_left, epsilon_reverse o x y, add_comm y x]
  ring

end HMT.IV.LatticeProductCocycle
end

#print axioms HMT.IV.LatticeProductCocycle.sign_integer_zpow
#print axioms HMT.IV.LatticeProductCocycle.epsilon_commutator
#print axioms HMT.IV.LatticeProductCocycle.epsilon_reverse
#print axioms HMT.IV.LatticeProductCocycle.product_cocycle_left
#print axioms HMT.IV.LatticeProductCocycle.product_cocycle_right
