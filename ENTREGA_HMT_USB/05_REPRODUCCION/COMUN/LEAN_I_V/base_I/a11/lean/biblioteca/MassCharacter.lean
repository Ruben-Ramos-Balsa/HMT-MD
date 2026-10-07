import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

/-!
Article VI, 05_registro_operador_masa.tex: the character on integer signatures.
The source's internal coordinates are supplied after their upstream publication.
No additivity of the map from histories to signatures is postulated here.
-/

noncomputable section

namespace HMTMassCharacter

abbrev Signature := Fin 5 → ℤ
abbrev Coordinates := Fin 5 → ℝ

def exponent (X : Coordinates) (σ : Signature) : ℝ :=
  ∑ i, (σ i : ℝ) * X i

def character (X : Coordinates) (σ : Signature) : ℝ := Real.exp (exponent X σ)

theorem exponent_add (X : Coordinates) (σ τ : Signature) :
    exponent X (σ + τ) = exponent X σ + exponent X τ := by
  simp [exponent, Int.cast_add, add_mul, Finset.sum_add_distrib]

theorem exponent_sub (X : Coordinates) (σ τ : Signature) :
    exponent X (σ - τ) = exponent X σ - exponent X τ := by
  simp [exponent, Int.cast_sub, sub_mul, Finset.sum_sub_distrib]

@[simp] theorem exponent_zero (X : Coordinates) : exponent X 0 = 0 := by
  simp [exponent]

theorem character_pos (X : Coordinates) (σ : Signature) : 0 < character X σ :=
  Real.exp_pos _

theorem character_add (X : Coordinates) (σ τ : Signature) :
    character X (σ + τ) = character X σ * character X τ := by
  rw [character, exponent_add, Real.exp_add]
  rfl

@[simp] theorem character_zero (X : Coordinates) : character X 0 = 1 := by
  simp [character]

theorem character_sub (X : Coordinates) (σ τ : Signature) :
    character X (σ - τ) = character X σ / character X τ := by
  rw [character, exponent_sub, Real.exp_sub]
  rfl

/-- Literal internal specialization: the integer total sC is divided exactly once. -/
def internalCoordinates (x y delta s120 : ℝ) : Coordinates :=
  ![x, y / 6, delta, s120, 135 * delta ^ 2]

theorem internal_exponent (σ : Signature) (x y delta s120 : ℝ) :
    exponent (internalCoordinates x y delta s120) σ =
      (σ 0 : ℝ) * x + ((σ 1 : ℝ) / 6) * y + (σ 2 : ℝ) * delta +
      (σ 3 : ℝ) * s120 + (σ 4 : ℝ) * (135 * delta ^ 2) := by
  simp [exponent, internalCoordinates, Fin.sum_univ_succ]
  ring

def basalMass (mRef : ℝ) (X : Coordinates) (σ σRef : Signature) : ℝ :=
  mRef * character X (σ - σRef)

theorem basalMass_pos {mRef : ℝ} (hm : 0 < mRef) (X : Coordinates)
    (σ σRef : Signature) : 0 < basalMass mRef X σ σRef :=
  mul_pos hm (character_pos X _)

/-- The common absolute scale cancels only in a ratio in the same chart. -/
theorem basalMass_ratio {mRef : ℝ} (hm : 0 < mRef) (X : Coordinates)
    (σ τ σRef : Signature) :
    basalMass mRef X σ σRef / basalMass mRef X τ σRef = character X (σ - τ) := by
  rw [basalMass, basalMass, mul_div_mul_left _ _ (ne_of_gt hm)]
  rw [← character_sub]
  congr 1
  ext i
  simp

/-- Transporting the reference also transports its normalization. -/
theorem change_reference (mRef : ℝ) (X : Coordinates) (σ oldRef newRef : Signature) :
    basalMass (basalMass mRef X newRef oldRef) X σ newRef =
      basalMass mRef X σ oldRef := by
  simp only [basalMass, mul_assoc]
  rw [← character_add]
  congr 2
  ext i
  simp

#print axioms character_add
#print axioms character_pos
#print axioms internal_exponent
#print axioms basalMass_ratio
#print axioms change_reference

end HMTMassCharacter
